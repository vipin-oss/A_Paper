"""Isolated A0 diagnostics, NOT the Negative Reflection production solver.

Legendre--Galerkin sagittal plate modes; plane strain, c-axis normal.
The executed physical reference is the CLASSICAL f=A=H=0, frozen-carrier
piezoelectric limit with vacuum exterior.  No nonzero flexoelectric value
is invented.  Optional A,H are SYNTHETIC sensitivity diagnostics at f=0.

K = k*d, Omega = omega*d/sqrt(c44/rho); d is TOTAL thickness.
Time convention exp(i*k*x - i*omega*t).  Basis is orthonormal on [-1/2,1/2].
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import Legendre, leggauss
from scipy.linalg import eigh, eig, expm, solve, svdvals
from scipy.optimize import linear_sum_assignment, root_scalar

ROOT = Path(__file__).resolve().parent
MATERIAL = json.loads((ROOT / "materials.json").read_text())
SI = MATERIAL["SI"]
CONST = MATERIAL["SI_definitions"]


def elastic_matrix():
    c = SI
    return np.array([
        [c['c11'], c['c12'], c['c13'], 0, 0, 0],
        [c['c12'], c['c11'], c['c13'], 0, 0, 0],
        [c['c13'], c['c13'], c['c33'], 0, 0, 0],
        [0, 0, 0, c['c44'], 0, 0],
        [0, 0, 0, 0, c['c44'], 0],
        [0, 0, 0, 0, 0, c['c66']],
    ], dtype=float)


def derived(d=1e-6, n0=1e19):
    c0, kap = SI['c44'], SI['kappa33']
    q, kb = CONST['q'], CONST['kB']
    theta = q * SI['electron_diffusivity'] / SI['electron_mobility']
    a = theta / n0
    cs = np.sqrt(c0 / SI['rho'])
    # Full THREE-dimensional stability bound, not just its plane-strain submatrix.
    cschur = 1.0 / np.linalg.inv(elastic_matrix())[2, 2]
    ld = np.sqrt(kap * theta / (q*q*n0))
    return dict(d=d, n0=n0, c0=c0, cs=cs, theta=theta, T=theta/kb,
                a=a, cschur=cschur, lambda_D=ld,
                tau_dielectric=kap/(q*n0*SI['electron_mobility']),
                tau_diffusion=d*d/SI['electron_diffusivity'],
                Q=d/ld, alpha=SI['electron_diffusivity']/(d*cs),
                frequency_scale_Hz=cs/(2*np.pi*d),
                phi_scale=d*np.sqrt(c0/kap), nu_scale=np.sqrt(c0/a))


def hermitian(a):
    return (a + a.conj().T) * 0.5


def gram(a, b, w, constitutive=None):
    if constitutive is None:
        return np.einsum('qai,qaj,q->ij', a.conj(), b, w, optimize=True)
    return np.einsum('qai,ab,qbj,q->ij', a.conj(), constitutive, b, w, optimize=True)


class Plate:
    def __init__(self, degree=24, ell_rel=0., eta=0., n0=1e19, d=1e-6,
                 vacuum=True):
        if ell_rel < 0 or abs(eta) >= 1:
            raise ValueError('Require ell/d >= 0 and strict |eta| < 1.')
        if ell_rel == 0 and eta != 0:
            raise ValueError('Nonzero H requires a positive strain-gradient modulus.')
        self.degree, self.n = degree, degree+1
        self.ell, self.eta, self.vacuum = ell_rel, eta, vacuum
        self.sc = derived(d, n0)
        c0, kap = self.sc['c0'], SI['kappa33']
        self.C = elastic_matrix()[np.ix_([0, 2, 4], [0, 2, 4])] / c0
        self.e = np.array([[0, 0, SI['e15']], [SI['e31'], SI['e33'], 0.]]) / np.sqrt(c0*kap)
        self.kap = np.diag([SI['kappa11']/kap, 1.])
        self.eps = CONST['epsilon0']/kap if vacuum else 0.
        self.h = eta*ell_rel*np.sqrt(self.sc['cschur']/c0)
        self.h_SI = self.h * d * np.sqrt(self.sc['a']*c0)
        x, wg = leggauss(max(64, 2*degree+6))
        self.z, self.w = x/2, wg/2
        self.b = self.basis(self.z, 4)
        self.ends = self.basis(np.array([-.5, .5]), 4)
        self.W = self.b[0].T @ (self.w[:, None]*self.b[0])
        self.M = np.kron(np.eye(2), self.W)

    def basis(self, z, derivatives=4):
        x = 2*np.asarray(z)
        ans = []
        for r in range(derivatives+1):
            ans.append(np.stack([
                np.sqrt(2*j+1)*2**r*Legendre.basis(j).deriv(r)(x)
                for j in range(self.n)], axis=1))
        return ans

    def operators(self, K, basis=None):
        b = self.b if basis is None else basis
        nq, n = b[0].shape
        B, Bz = np.zeros((nq, 3, 2*n), complex), np.zeros((nq, 3, 2*n), complex)
        dB, dBz = B.copy(), Bz.copy()
        B[:, 0, :n] = 1j*K*b[0]
        B[:, 1, n:] = b[1]
        B[:, 2, :n] = b[1]
        B[:, 2, n:] = 1j*K*b[0]
        Bz[:, 0, :n] = 1j*K*b[1]
        Bz[:, 1, n:] = b[2]
        Bz[:, 2, :n] = b[2]
        Bz[:, 2, n:] = 1j*K*b[1]
        dB[:, 0, :n] = 1j*b[0]
        dB[:, 2, n:] = 1j*b[0]
        dBz[:, 0, :n] = 1j*b[1]
        dBz[:, 2, n:] = 1j*b[1]
        G = np.stack([1j*K*b[0], b[1]], axis=1)
        dG = np.stack([1j*b[0], np.zeros_like(b[0])], axis=1)
        return B, Bz, dB, dBz, G, dG

    def matrices(self, K):
        if K <= 0:
            raise ValueError('Use K>0; the K=0 gauge/charge constraints need a separate limit.')
        B, Bz, dB, dBz, G, dG = self.operators(K)
        base = gram(B, B, self.w, self.C)
        dbase = gram(dB, B, self.w, self.C) + gram(B, dB, self.w, self.C)
        Kuu = base*(1+self.ell**2*K**2) + self.ell**2*gram(Bz, Bz, self.w, self.C)
        dKuu = (1+self.ell**2*K**2)*dbase + 2*self.ell**2*K*base
        dKuu += self.ell**2*(gram(dBz, Bz, self.w, self.C)+gram(Bz, dBz, self.w, self.C))
        Kup = gram(B, G, self.w, self.e.T)
        dKup = gram(dB, G, self.w, self.e.T) + gram(B, dG, self.w, self.e.T)
        ends = self.ends[0]
        P = gram(G, G, self.w, self.kap) + self.eps*K*(ends.T@ends)
        dP = gram(dG, G, self.w, self.kap)+gram(G, dG, self.w, self.kap)+self.eps*(ends.T@ends)
        F = np.zeros((2*self.n, self.n), complex)
        F[self.n:] = self.h * self.b[2].T @ (self.w[:, None]*self.b[0])
        # Gauss law: Kup^H U - P Phi - Q W N = 0.
        Q = self.sc['Q']
        p_u = solve(P, Kup.conj().T, assume_a='pos')
        p_n = solve(P, Q*self.W, assume_a='pos')
        Kf = hermitian(Kuu + Kup@p_u)
        R = F - Kup@p_n
        A = hermitian(self.W + Q*self.W@p_n)
        L = gram(G, G, self.w)  # Laplacian form acting on electrochemical potential
        return dict(Kuu=Kuu, dKuu=dKuu, Kup=Kup, dKup=dKup,
                    P=P, dP=dP, F=F, K=Kf, R=R, A=A, L=L)

    def modes(self, K, closure='frozen', count=12):
        a = self.matrices(K)
        if closure == 'frozen':
            keff = a['K']
        elif closure == 'equilibrated':
            keff = hermitian(a['K'] - a['R']@solve(a['A'], a['R'].conj().T, assume_a='pos'))
        else:
            raise ValueError(closure)
        val, U = eigh(keff, self.M, subset_by_index=[0, min(count, 2*self.n)-1])
        if np.min(val) < -1e-6:
            raise ValueError(f'Unstable conservative stiffness: {np.min(val)}')
        omega = np.sqrt(np.maximum(val, 0))
        N = np.zeros((self.n, len(val)), complex)
        if closure == 'equilibrated':
            N = -solve(a['A'], a['R'].conj().T@U, assume_a='pos')
        Phi = solve(a['P'], a['Kup'].conj().T@U-self.sc['Q']*self.W@N, assume_a='pos')
        group = np.empty(len(val))
        for j, om in enumerate(omega):
            u, p = U[:, j], Phi[:, j]
            envelope = np.vdot(u, a['dKuu']@u)
            envelope += 2*np.real(np.vdot(u, a['dKup']@p)) - np.vdot(p, a['dP']@p)
            # Very small acoustic eigenvalues can be roundoff-dominated when
            # high polynomial degrees and K -> 0 are combined. Do not classify
            # such unresolved points as forward/backward waves.
            group[j] = (np.real(envelope)/(2*om*np.real(np.vdot(u, self.M@u)))
                        if om > 1e-7 else np.nan)
        return dict(omega=omega, U=U, Phi=Phi, N=N, group=group,
                    matrices=a, keff=keff)

    def dynamic_modes(self, K):
        """Finite-mobility diagnostic; s=-i*Omega, NOT a lossless dispersion."""
        a = self.matrices(K)
        n, m = self.n, 2*self.n
        Zmm, Zmn = np.zeros((m, m), complex), np.zeros((m, n), complex)
        Znm = np.zeros((n, m), complex)
        lap = solve(self.W, a['L'], assume_a='pos')
        mobility = self.sc['alpha']*lap@solve(self.W, np.eye(n), assume_a='pos')
        dynamic = np.block([
            [Zmm, np.eye(m), Zmn],
            [-solve(self.M, a['K'], assume_a='pos'), Zmm,
             -solve(self.M, a['R'], assume_a='pos')],
            [-mobility@a['R'].conj().T, Znm, -mobility@a['A']],
        ])
        s, V = eig(dynamic)
        select = np.where(s.imag < -1e-5)[0]
        select = select[np.argsort(-s[select].imag)]
        return dict(s=s[select], omega=1j*s[select], V=V[:, select],
                    all_s=s, operator=dynamic, matrices=a)

    def fields(self, K, U, Phi, N, basis=None):
        b = self.b if basis is None else basis
        n = self.n
        ux = [v@U[:n] for v in b]
        uz = [v@U[n:] for v in b]
        pp = [v@Phi for v in b]
        nn = [v@N for v in b]
        strain = [np.stack([1j*K*ux[r], uz[r+1], ux[r+1]+1j*K*uz[r]], axis=1)
                  for r in range(4)]
        gradp = [np.stack([1j*K*pp[r], pp[r+1]], axis=1) for r in range(3)]
        sigma = strain[0]@self.C.T + gradp[0]@self.e
        dsigma = strain[1]@self.C.T + gradp[1]@self.e
        mx = self.ell**2*(1j*K*strain[0])@self.C.T
        mz = self.ell**2*strain[1]@self.C.T
        mz[:, 1] += self.h*nn[0]
        dzmz = self.ell**2*strain[2]@self.C.T
        dzmz[:, 1] += self.h*nn[1]
        dzzmz = self.ell**2*strain[3]@self.C.T
        dzzmz[:, 1] += self.h*nn[2]
        Sigma = sigma - 1j*K*mx - dzmz
        dSigma = dsigma + self.ell**2*K*K*strain[1]@self.C.T - dzzmz
        D = strain[0]@self.e.T - gradp[0]@self.kap.T
        dD = strain[1]@self.e.T - gradp[1]@self.kap.T
        mu = nn[0] + self.h*strain[1][:, 1] - self.sc['Q']*pp[0]
        return dict(ux=ux, uz=uz, phi=pp, N=nn, strain=strain,
                    sigma=sigma, Sigma=Sigma, dSigma=dSigma,
                    mx=mx, mz=mz, D=D, dD=dD, mu=mu)

    def diagnostics(self, K, om, U, Phi, N, closure='frozen'):
        f = self.fields(K, U, Phi, N)
        b = self.fields(K, U, Phi, N, self.ends)
        u = np.stack([f['ux'][0], f['uz'][0]], axis=1)
        up = np.stack([f['ux'][1], f['uz'][1]], axis=1)
        mech = np.stack([
            1j*K*f['Sigma'][:, 0]+f['dSigma'][:, 2],
            1j*K*f['Sigma'][:, 2]+f['dSigma'][:, 1]], axis=1)
        rm = mech + om*om*u
        rg = 1j*K*f['D'][:, 0]+f['dD'][:, 1]+self.sc['Q']*f['N'][0]
        norm = lambda v: float(np.sqrt(np.sum(self.w*np.sum(np.abs(v)**2, axis=1)))) if v.ndim == 2 else float(np.sqrt(np.sum(self.w*np.abs(v)**2)))
        traction = np.stack([b['Sigma'][:, 2]-1j*K*b['mz'][:, 0],
                             b['Sigma'][:, 1]-1j*K*b['mz'][:, 2]], axis=1)
        double = b['mz'][:, [2, 1]]
        electric = b['D'][:, 1] - np.array([-1., 1.])*self.eps*K*b['phi'][0]
        v, vp, vx = -1j*om*u, -1j*om*up, K*om*u
        Sx = f['Sigma'][:, [0, 2]]
        mechanical_flux = -np.sum(Sx*v.conj(), axis=1)
        mx = f['mx']
        mechanical_flux -= (mx[:, 0]*vx[:, 0].conj()+mx[:, 2]*vp[:, 0].conj()
                            +mx[:, 2]*vx[:, 1].conj()+mx[:, 1]*vp[:, 1].conj())
        electrical_flux = f['phi'][0]*(-1j*om*f['D'][:, 0]).conj()
        power = .5*np.real(np.sum(self.w*(mechanical_flux+electrical_flux)))
        # Free gradient-elastic faces carry a tangential hyperstress power term.
        # With T_i=Sigma_i3-d_x tau_i13=0 and R_i=tau_i33=0,
        # bulk normal power is a tangential divergence, not pointwise zero.
        # Integrating the local balance across thickness therefore requires
        # P_guided = integral(P_bulk) - [tau_i13 * v_i]_(bottom)^(top).
        boundary_velocity = -1j*om*np.stack([b['ux'][0], b['uz'][0]], axis=1)
        face_power = .5*np.real(np.sum(b['mz'][:, [0, 2]]*boundary_velocity.conj(), axis=1))
        face_correction = -(face_power[1]-face_power[0])
        power += face_correction
        # Analytic integral through both unbounded vacuum half-spaces.
        power -= .25*om*self.eps*np.sum(np.abs(b['phi'][0])**2)
        mass = np.real(np.vdot(U, self.M@U))
        # Conservative virial identity: mean total energy = 2*mean kinetic energy.
        mean_energy = .5*om*om*mass
        mscale = max(norm(mech), norm(om*om*u), 1e-15)
        gscale = max(norm(K*f['D'][:, 0]), norm(f['dD'][:, 1]),
                     norm(self.sc['Q']*f['N'][0]), 1e-15)
        sscale = max(norm(f['sigma']), norm(f['Sigma']), 1e-15)
        return dict(strong_mechanical_relative=norm(rm)/mscale,
                    strong_gauss_relative=norm(rg)/gscale,
                    traction_relative=float(np.max(np.abs(traction)))/sscale,
                    double_traction_over_stress_d=float(np.max(np.abs(double)))/sscale,
                    vacuum_bc_relative=float(np.max(np.abs(electric)))/max(norm(f['D']), 1e-15),
                    electrochemical_equilibrium_absolute=norm(f['mu']) if closure == 'equilibrated' else None,
                    direct_power=float(power), mean_energy=float(mean_energy),
                    face_hyperstress_power_correction=float(face_correction),
                    energy_velocity=float(power/mean_energy))

    def dynamic_diagnostics(self, K, mode, index):
        n = self.n
        omega, sval = mode['omega'][index], mode['s'][index]
        state = mode['V'][:, index]
        U, V, N = state[:2*n], state[2*n:4*n], state[4*n:]
        a = mode['matrices']
        Phi = solve(a['P'], a['Kup'].conj().T@U-self.sc['Q']*self.W@N, assume_a='pos')
        f = self.fields(K, U, Phi, N)
        b = self.fields(K, U, Phi, N, self.ends)
        mu = solve(self.W, a['R'].conj().T@U+a['A']@N, assume_a='pos')
        energy = .5*np.real(np.vdot(V, self.M@V)+np.vdot(U, a['K']@U)
                            +2*np.real(np.vdot(U, a['R']@N))+np.vdot(N, a['A']@N))
        diss = self.sc['alpha']*np.real(np.vdot(mu, a['L']@mu))
        norm = lambda v: float(np.sqrt(np.sum(self.w*np.abs(v)**2)))
        mu2 = f['N'][2]+self.h*f['strain'][3][:, 1]-self.sc['Q']*f['phi'][2]
        rate = -1j*omega*f['N'][0]
        diffusion = self.sc['alpha']*(mu2-K*K*f['mu'])
        carrier_residual = norm(rate-diffusion)/max(norm(rate), norm(diffusion), 1e-30)
        mu1_boundary = b['N'][1]+self.h*b['strain'][2][:, 1]-self.sc['Q']*b['phi'][1]
        mu1_bulk = f['N'][1]+self.h*f['strain'][2][:, 1]-self.sc['Q']*f['phi'][1]
        norm2 = lambda x: float(np.sqrt(np.sum(self.w*np.sum(np.abs(x)**2,axis=1))))
        displacement = np.stack([f['ux'][0], f['uz'][0]],axis=1)
        force = np.stack([1j*K*f['Sigma'][:,0]+f['dSigma'][:,2],
                          1j*K*f['Sigma'][:,2]+f['dSigma'][:,1]],axis=1)
        momentum_residual = norm2(force+omega**2*displacement)/max(
            norm2(force),norm2(omega**2*displacement),1e-30)
        gauss = 1j*K*f['D'][:,0]+f['dD'][:,1]+self.sc['Q']*f['N'][0]
        gauss_scale = max(norm(K*f['D'][:,0]),norm(f['dD'][:,1]),
                          norm(self.sc['Q']*f['N'][0]),1e-30)
        traction = np.stack([b['Sigma'][:,2]-1j*K*b['mz'][:,0],
                             b['Sigma'][:,1]-1j*K*b['mz'][:,2]],axis=1)
        electric = b['D'][:,1]-np.array([-1.,1.])*self.eps*K*b['phi'][0]
        stress_scale = max(norm2(f['sigma']),norm2(f['Sigma']),1e-30)
        return dict(energy=float(energy), dissipation=float(diss),
                    energy_decay_identity_relative=float(abs(2*sval.real*energy+diss)/max(diss, 1e-30)),
                    strong_mechanical_relative=momentum_residual,
                    strong_gauss_relative=norm(gauss)/gauss_scale,
                    traction_relative=float(np.max(np.abs(traction)))/stress_scale,
                    double_traction_over_stress_d=float(np.max(np.abs(b['mz'][:,[2,1]])))/stress_scale,
                    vacuum_bc_relative=float(np.max(np.abs(electric)))/max(norm2(f['D']),1e-30),
                    carrier_strong_relative=carrier_residual,
                    no_flux_boundary_relative=float(np.max(np.abs(mu1_boundary)))/max(norm(mu1_bulk),1e-30),
                    eigenpair_relative=float(np.linalg.norm(mode['operator']@state-sval*state)
                                             / max(np.linalg.norm(sval*state),1e-30)))


def track_grid(plate, grid, closure='frozen', count=10):
    """Mass-overlap continuation, not independent frequency sorting at each k."""
    ans, previous, minmac = [], None, 1.
    for K in grid:
        m = plate.modes(float(K), closure, count)
        if previous is not None:
            mac = np.abs(previous.conj().T@plate.M@m['U'])**2
            row, col = linear_sum_assignment(-mac)
            order = col[np.argsort(row)]
            minmac = min(minmac, float(np.min(mac[np.arange(count), order])))
            for key in ['omega', 'group']:
                m[key] = m[key][order]
            for key in ['U', 'Phi', 'N']:
                m[key] = m[key][:, order]
        previous = m['U']
        ans.append(m)
    return ans, minmac


def classical_stroh(K, omega, vacuum=True):
    """Independent constant-coefficient six-state thickness propagator.

    Does not use Galerkin assembly or Legendre differentiation.
    Real transformed state: (Ux/i, Uz, Phi, sigma13/i, sigma33, D3).
    """
    sc = derived()
    c11, c13, c33, c44 = [SI[s]/sc['c0'] for s in ['c11', 'c13', 'c33', 'c44']]
    e15, e31, e33 = [SI[s]/np.sqrt(sc['c0']*SI['kappa33']) for s in ['e15', 'e31', 'e33']]
    ka1 = SI['kappa11']/SI['kappa33']
    ep = CONST['epsilon0']/SI['kappa33'] if vacuum else 0.
    inverse = np.linalg.inv(np.array([[c33, e33], [e33, -1.]]))

    def rhs(y):
        ux, uz, p, t1, t3, d3 = y
        uzp, pp = inverse@np.array([t3-c13*1j*K*ux, d3-e31*1j*K*ux])
        uxp = (t1-e15*1j*K*p)/c44-1j*K*uz
        s11 = c11*1j*K*ux+c13*uzp+e31*pp
        d1 = e15*(uxp+1j*K*uz)-ka1*1j*K*p
        return np.array([uxp, uzp, pp, -omega**2*ux-1j*K*s11,
                         -omega**2*uz-1j*K*t1, -1j*K*d1])
    F = np.stack([rhs(y) for y in np.eye(6)], axis=1)
    transform = np.diag([1j, 1., 1., 1j, 1., 1.])
    Fr = np.real_if_close(np.linalg.solve(transform, F@transform)).real
    bottom = np.zeros((6, 3))
    bottom[:3] = np.eye(3)
    bottom[5, 2] = -ep*K
    topbc = np.zeros((3, 6))
    topbc[0, 3], topbc[1, 4], topbc[2, 5], topbc[2, 2] = 1., 1., 1., -ep*K
    boundary = topbc@expm(Fr)@bottom
    # Row/column scaling only improves conditioning; cannot create a root.
    scaled = boundary/np.maximum(np.linalg.norm(boundary, axis=1), 1e-30)[:, None]
    scaled /= np.maximum(np.linalg.norm(scaled, axis=0), 1e-30)[None, :]
    singular = svdvals(scaled)
    return dict(determinant=float(np.linalg.det(scaled)),
                relative_singular_value=float(singular[-1]/singular[0]))


def independent_classical_root(K, guess, vacuum=True):
    fun = lambda om: classical_stroh(K, om, vacuum)['determinant']
    # A secant refinement about the Galerkin candidate, with no shared operator.
    root = root_scalar(fun, x0=guess*(1-1e-5), x1=guess*(1+1e-5),
                       method='secant', xtol=2e-12, maxiter=30)
    return dict(omega=float(root.root), converged=bool(root.converged),
                relative_difference=float(abs(root.root-guess)/guess),
                **classical_stroh(K, root.root, vacuum))
