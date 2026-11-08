"""Direct two-dimensional solution of the edge-scattering problem.

The plate occupies x<0 (edge at x=0), thickness z in [-1/2,1/2] (units of d), and a
fixed tangential wavenumber k_y.  The variational problem is the *same* one that
`model.Plate` discretises (matrices A[r,s]); here it is solved on a finite strip
-Lt<x<0 with a B-spline basis in x (knots graded toward the edge) and the
through-thickness basis of `Plate`/`MeshPlate`.  No modal expansion is used to
impose the edge: the incident mode enters only through the natural-boundary
load, a smooth mass-proportional absorbing layer closes the far end, and the
reflected amplitudes are then *fitted* to the field in a window of the strip.

Scattered-field form.  a(v,u_sc) = -[v^H T_inc + (dv/dx)^H R_inc]_{x=0}, with T,R the
traction and double-traction rows of the incident state vector (model.state_parts).
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.interpolate import BSpline
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model import Plate, MeshPlate  # noqa: E402


def graded_knots(Lt, n_uniform, n_graded, ratio, first_len):
    """Breakpoints on [-Lt,0]: geometric grading toward x=0 over n_graded cells, then uniform."""
    h = first_len * ratio ** np.arange(n_graded)          # cell sizes from the edge outward
    xg = -np.r_[0.0, np.cumsum(h)]                         # 0, -h0, -(h0+h1)...
    x_start = xg[-1]
    if -x_start >= Lt:
        raise ValueError('graded zone longer than strip')
    xu = np.linspace(x_start, -Lt, n_uniform + 1)[1:]
    return np.r_[xg, xu][::-1]                             # increasing from -Lt to 0


class Strip:
    def __init__(self, plate, ky, omega, Lt=60., Ls=25., gamma=4., degree=4,
                 n_uniform=60, n_graded=8, ratio=1.6, first_len=0.02):
        self.p = plate; self.ky = ky; self.omega = omega
        self.deg = degree
        br = graded_knots(Lt, n_uniform, n_graded, ratio, first_len)
        self.breaks = br
        t = np.r_[[br[0]] * degree, br, [br[-1]] * degree]
        self.t = t
        self.nx = len(t) - degree - 1
        self.Lt = Lt; self.Ls = Ls; self.gamma = gamma
        # Gauss points per cell
        xg, wg = leggauss(degree + 4)
        self.xq = np.concatenate([(a + b) / 2 + (b - a) * xg / 2 for a, b in zip(br[:-1], br[1:])])
        self.wq = np.concatenate([(b - a) * wg / 2 for a, b in zip(br[:-1], br[1:])])
        self.phi = [self._eval(self.xq, r) for r in range(3)]   # derivative orders 0..2, sparse (nq x nx)

    def _eval(self, x, r):
        x = np.asarray(x, float)
        rows, cols, vals = [], [], []
        for k in range(self.nx):
            c = np.zeros(self.nx); c[k] = 1.
            b = BSpline(self.t, c, self.deg, extrapolate=True)
            s, e = self.t[k], self.t[k + self.deg + 1]
            m = (x >= s) & (x <= e)
            if not m.any():
                continue
            d = b.derivative(r) if r else b
            v = d(x[m]); v = np.nan_to_num(v)
            rows.append(np.where(m)[0]); cols.append(np.full(m.sum(), k)); vals.append(v)
        if not rows:
            return sp.csr_matrix((len(x), self.nx))
        return sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                             shape=(len(x), self.nx))

    def sponge(self, x):
        x0 = -(self.Lt - self.Ls)
        s = np.clip((x0 - x) / self.Ls, 0, None)
        return self.gamma * self.omega * s ** 3

    def assemble(self):
        p = self.p; A = p.matrices(self.ky, self.omega)
        w = self.wq
        K = None
        for r in range(3):
            for s_ in range(3):
                Kx = (self.phi[r].T @ sp.diags(w) @ self.phi[s_]).tocsr()
                Ar = A[r, s_].copy(); Ar[abs(Ar) < 1e-13 * max(abs(Ar).max(), 1e-300)] = 0
                blk = sp.kron(Kx, sp.csr_matrix(Ar), format='csr')
                K = blk if K is None else K + blk
        # absorbing layer: omega^2 -> omega^2 + i omega gamma(x) on the displacement rows
        U = np.zeros((p.nw, p.nw), complex)
        U[:p.nu, :p.nu] = p.M
        Kg = (self.phi[0].T @ sp.diags(w * self.sponge(self.xq)) @ self.phi[0]).tocsr()
        K = K + sp.kron(Kg, sp.csr_matrix(-1j * self.omega * U), format='csr')
        self.K = K.tocsc(); self.A = A
        return self.K

    def load(self, inc_y):
        p = self.p
        q, pp, T, R = p.state_parts(inc_y)
        e0 = self._eval(np.array([0.]), 0).toarray()[0]
        e1 = self._eval(np.array([0.]), 1).toarray()[0]
        # right end x=0 is the last knot: BSpline evaluation at the end point
        b = np.zeros(self.nx * p.nw, complex)
        for a in range(self.nx):
            if e0[a] != 0:
                b[a * p.nw:(a + 1) * p.nw] += -e0[a] * T
            if e1[a] != 0:
                b[a * p.nw:a * p.nw + p.nu] += -e1[a] * R
        return b

    def solve(self, inc_y):
        self.assemble()
        b = self.load(inc_y)
        lu = spla.splu(self.K, permc_spec="NATURAL", diag_pivot_thresh=0.0 if False else 1.0)
        c = lu.solve(b)
        self.c = c.reshape(self.nx, self.p.nw)
        return self.c

    def field(self, x):
        B = self._eval(np.atleast_1d(x), 0)
        return B @ self.c

    def fit(self, Y, K, x_lo, x_hi, nx=60, rcond=1e-10, imax=3.0):
        """Fit q_sc(x) in [x_lo,x_hi] (negative numbers) to sum_j a_j Y_j[:nw] exp(iK_j x)."""
        nw = self.p.nw
        xs = np.linspace(x_lo, x_hi, nx)
        F = self.field(xs)                                   # (nx, nw)
        cols = []
        for j in range(Y.shape[1]):
            cols.append((Y[:nw, j][None, :] * np.exp(1j * K[j] * xs)[:, None]).reshape(-1))
        M = np.stack(cols, axis=1)
        nrm = np.linalg.norm(M, axis=0)
        keep = (nrm > 1e-9 * nrm.max()) & (np.abs(np.asarray(K).imag) < imax)
        a = np.zeros(Y.shape[1], complex)
        Mk = M[:, keep] / nrm[keep]
        ak, *_ = np.linalg.lstsq(Mk, F.reshape(-1), rcond=rcond)
        a[keep] = ak / nrm[keep]
        res = np.linalg.norm(M @ a - F.reshape(-1)) / np.linalg.norm(F.reshape(-1))
        return a, res
