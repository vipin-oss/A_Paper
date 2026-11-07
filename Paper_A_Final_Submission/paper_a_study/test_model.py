"""Essential checks, independent propagators, and a solved edge conversion."""
import unittest
from unittest.mock import patch
import numpy as np
from paper_a_study.model import (Plate,MeshPlate,SI,CONST,gradient_strong_root,
    classical_strong_root,edge_field_residuals,temporal_energy_balance)

OMEGA=7.6333735784537335
KY=.12976738826550185
H_TEST=2.00485322e-23


class TestStudy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=Plate(degree=18)
        cls.r,cls.s=cls.p.edge(KY,OMEGA,.736+.00001j,.245-.00001j)

    def test_material_units_and_schur(self):
        self.assertAlmostEqual(self.p.diffusivity/self.p.mobility,.026)
        self.assertAlmostEqual(self.p.cs,2746.608754,places=5)
        self.assertAlmostEqual(Plate(H=H_TEST).schur,.0005,places=10)
        self.assertRaises(ValueError,Plate,H=2e-21)
        self.assertRaises(ValueError,Plate,H=H_TEST,ell=0,flexo=0)

    def test_H_changes_only_prescribed_constitutive_terms(self):
        p=self.p;h=Plate(degree=p.degree,H=H_TEST)
        rng=np.random.default_rng(4)
        q=rng.normal(size=p.nw)+1j*rng.normal(size=p.nw)
        qh=q.copy()
        qh[p.im]+=h.h*np.linalg.solve(p.W,p.b[0].T@(p.weights*(p.b[2]@q[2*p.n:3*p.n])))
        f=p.fields(.4,.1,q);g=h.fields(.4,.1,qh)
        np.testing.assert_allclose(g['N'][0],f['N'][0],atol=1e-12)
        np.testing.assert_allclose(g['sigma'],f['sigma'],atol=1e-12)
        np.testing.assert_allclose(g['D'],f['D'],atol=1e-12)
        np.testing.assert_allclose(g['tau'][2][:,2]-f['tau'][2][:,2],h.h*f['N'][0],atol=2e-12)
        for j in [0,1]:np.testing.assert_allclose(g['tau'][j],f['tau'][j],atol=1e-12)

    def test_temporal_vs_independent_spatial_polynomial(self):
        p=self.p;m=p.temporal(.3,p.cutoff());A=p.matrices(0,m['omega']);D=p.polynomial(A,.3)
        defect=np.linalg.norm(D@m['q'])/(np.linalg.norm(D)*np.linalg.norm(m['q']))
        self.assertLess(defect,1e-13)

    def test_first_order_linearization(self):
        p=self.p;A=p.matrices(.1,OMEGA);F=p.state_operator(A);K=.4
        q=np.random.default_rng(2).normal(size=p.nw);y=p.state_from_q(A,K,q)
        err=F@y-1j*K*y;D=p.polynomial(A,K)@q
        np.testing.assert_allclose(err[p.nw+p.nu:2*p.nw+p.nu],D,rtol=1e-12,atol=1e-7)
        self.assertLess(np.linalg.norm(err[:p.nw+p.nu])/max(np.linalg.norm(y),1e-30),1e-11)

    def test_reciprocity_at_oblique_wavenumber(self):
        p=self.p;A=p.matrices(.13,OMEGA);B=p.matrices(-.13,OMEGA)
        D=p.polynomial(A,.7);E=p.polynomial(B,-.7)
        self.assertLess(np.linalg.norm(D.T-E)/np.linalg.norm(D),1e-13)
        F=p.state_operator(A);G=p.state_operator(B);m=F.shape[0]//2
        J=np.block([[np.zeros((m,m)),np.eye(m)],[-np.eye(m),np.zeros((m,m))]])
        self.assertLess(np.linalg.norm(F.T@J+J@G)/np.linalg.norm(F),1e-12)

    def test_classical_exact_SH_modes(self):
        p=Plate(degree=18,ell=0,flexo=0);K=.8
        sh=[m['omega'] for m in p.temporal(K)
            if np.vdot(m['U'][p.n:2*p.n],p.W@m['U'][p.n:2*p.n]).real>.999]
        for j in range(3):
            exact=np.sqrt(p.C[5,5]*K*K+(j*np.pi)**2)
            self.assertLess(min(abs(a-exact) for a in sh),1e-9)

    def test_gradient_exact_fundamental_SH(self):
        p=self.p;K=.8;exact=np.sqrt(p.C[5,5]*K*K*(1+p.lam*p.lam*K*K))
        sh=[m['omega'] for m in p.temporal(K)
            if np.vdot(m['U'][p.n:2*p.n],p.W@m['U'][p.n:2*p.n]).real>.999]
        self.assertLess(min(abs(a-exact) for a in sh),1e-10)

    def test_independent_classical_grounded_and_open(self):
        for electric in ['ground','open']:
            p=Plate(degree=18,ell=0,flexo=0,electric=electric)
            modes=p.temporal(.1)
            ref=min((m for m in modes if m['omega'].real>1 and
                np.vdot(m['U'][2*p.n:],p.W@m['U'][2*p.n:]).real>.85),
                key=lambda m:m['omega'].real)
            for K in [.3,.7]:
                ref=p.temporal(K,ref)
                root=classical_strong_root(p,K,ref['omega'],electric=electric)
                self.assertLess(abs(root-ref['omega']),1e-10)

    def test_independent_nonzero_f_H_temporal(self):
        for H in [0,-H_TEST,H_TEST]:
            p=Plate(degree=18,H=H);m=p.temporal(.3,p.cutoff())
            root=gradient_strong_root(p,K=.3,guess=m['omega'])
            self.assertLess(abs(root-m['omega']),1e-10)
            self.assertGreater(-m['omega'].imag,0)

    def test_temporal_energy_dissipation_balance(self):
        for H in [0,-H_TEST,H_TEST]:
            p=Plate(degree=18,H=H);m=p.temporal(.3,p.cutoff())
            b=temporal_energy_balance(p,.3,m)
            self.assertGreater(b['energy'],0)
            self.assertGreater(b['dissipation'],0)
            self.assertLess(b['relative_balance'],5e-6)

    def test_independent_spatial_roots(self):
        for H in [0,-H_TEST,H_TEST]:
            p=Plate(degree=18,H=H);r,s=p.edge(KY,OMEGA,.736+.00001j,.245-.00001j)
            for name in ['incident_K','backward_K']:
                K=np.sqrt(r[name]**2+KY*KY)
                exact=gradient_strong_root(p,omega=OMEGA,guess=K)
                self.assertLess(abs(exact-K),1e-10)

    def test_outgoing_count_and_nonzero_backward_conversion(self):
        r=self.r
        self.assertEqual(r['outgoing_modes'],r['edge_size'])
        self.assertEqual(r['edge_rank'],r['edge_size'])
        self.assertTrue(r['negative_direction'])
        self.assertGreater(r['backward_reflection_self_power'],.01)
        self.assertLess(r['backward_reflection_self_power'],.04)
        self.assertLess(r['reflected_angle_deg'],-20)

    def test_modal_energy_flux_and_strong_residuals(self):
        p=self.p;r=self.r;s=self.s
        for diag,y in [(r['incident'],s['incident']['y']),
                       (r['backward'],s['Y'][:,s['index_backward']])]:
            self.assertGreater(diag['energy'],0)
            self.assertGreater(diag['dissipation'],0)
            self.assertAlmostEqual(diag['Px'],p.power(y,OMEGA),places=10)
            self.assertLess(diag['balance'],1e-6)
            for key in ['momentum','gauss','carrier','traction','double_traction','blocking']:
                self.assertLess(diag[key],1e-8,key)

    def test_interference_inclusive_finite_volume_power(self):
        for L in [2,10,30]:
            r,s=self.p.edge(KY,OMEGA,.736+.00001j,.245-.00001j,L=L)
            self.assertLess(r['power_balance_relative'],1e-9)
            self.assertLess(abs(r['edge_power']),1e-10)
            self.assertGreater(r['dissipation_control_volume'],0)
            self.assertGreater(abs(r['cross_power_left']),1e-8)

    def test_independent_weak_corner_reconstruction(self):
        e=edge_field_residuals(self.p,OMEGA,KY,self.s)
        self.assertLess(e['independent_weak_mechanical'],1e-9)
        self.assertLess(e['edge_double_traction_rms'],1e-10)
        self.assertLess(e['grounded_phi_max'],1e-10)
        # Deliberately NOT asserting a resolved pointwise corner traction.
        self.assertGreater(e['corner_line_force_max'],1e-4)

    def test_degree_convergence(self):
        p=Plate(degree=22);r,_=p.edge(KY,OMEGA,.736+.00001j,.245-.00001j)
        self.assertLess(abs(r['backward_reflection_self_power']-self.r['backward_reflection_self_power']),2e-8)
        self.assertLess(abs(r['backward_K']-self.r['backward_K']),1e-10)

    def test_independent_C1_mesh_approaches_spectral_edge(self):
        errors=[]
        for elements in [8,12,18]:
            p=MeshPlate(elements=elements);r,_=p.edge(KY,OMEGA,.736+.00001j,.245-.00001j)
            errors.append(abs(r['backward_reflection_self_power']-self.r['backward_reflection_self_power']))
            self.assertLess(r['power_balance_relative'],1e-7)
        self.assertTrue(errors[2]<errors[1]<errors[0])
        self.assertLess(errors[-1],3e-5)

    def test_singular_edge_system_is_rejected(self):
        from scipy.linalg import svd as actual_svd
        def singular(*args,**kwargs):
            u,s,v=actual_svd(*args,**kwargs);s[-1]=0;return u,s,v
        with patch('paper_a_study.model.svd',side_effect=singular):
            self.assertRaisesRegex(RuntimeError,'rank deficiency',self.p.edge,KY,OMEGA,.736,.245)


class TestCornerAssessmentCaseSelection(unittest.TestCase):
    """Regression for the round-5 defect.

    Round 4 passed ``KB0`` -- the *backward-mode* wavenumber -- as the
    *incident* wavenumber of the corner study, which silently solved a
    different scattering experiment (R_B = 0.5444 instead of 0.0231) while
    labelling it ``operating_point``.  The corner study must identify its
    cases by the incident wavenumber.
    """

    def test_cases_are_incident_wavenumbers(self):
        from paper_a_study import corner_assessment as ca
        from paper_a_study.build_figure_data import K0, KB0
        self.assertAlmostEqual(ca.CASES['operating_point'], K0, places=12)
        self.assertNotAlmostEqual(ca.CASES['operating_point'], KB0, places=6)
        # the peak case must come from the certification suite, not be invented
        from paper_a_study.certify_peak import CASES as CERTIFIED
        self.assertAlmostEqual(
            ca.CASES['refined_peak'], float(dict(CERTIFIED)['refined_peak']),
            places=12)

    def test_stored_operating_point_matches_certification(self):
        """The stored JSON must agree with the independent refinement study."""
        import json
        from pathlib import Path
        from paper_a_study.build_figure_data import K0
        data = Path(__file__).resolve().parent / 'figure_data'
        corner = json.loads((data / 'corner_assessment.json').read_text())
        cert = json.loads((data / 'peak_certification.json').read_text())
        ref = {int(r['degree']): float(r['R_B']) for r in cert['rows']
               if abs(float(r.get('K', -1.0)) - float(K0)) < 1e-12 and r.get('status') == 'solved'}
        self.assertTrue(ref, 'no operating-point rows in peak_certification.json')
        op = corner['cases']['operating_point']
        self.assertAlmostEqual(op['incident_K'], float(K0), places=12)
        self.assertLess(abs(op['R_B_spread_rel']), 1e-5)
        for row in op['rows']:
            deg = int(row['degree'])
            self.assertIn(deg, ref)
            self.assertLess(abs(row['R_B'] - ref[deg]), 1e-9 * max(1.0, abs(ref[deg])),
                            f'degree {deg}: corner R_B disagrees with certification')
        self.assertEqual(corner['certification_cross_check'], 'PASS')



class TestFrozenReferenceConstants(unittest.TestCase):
    """Guards against a silent change of a material constant or a derived value.

    Every other test compares quantities computed by the same code with each
    other, so a constant entered in the wrong unit would pass all of them.  These
    two tests pin the derived values to a stored reference and the material
    constants to their literature bands.
    """

    @classmethod
    def setUpClass(cls):
        import json
        from pathlib import Path
        cls.ref = json.loads((Path(__file__).resolve().parent
                              / 'reference_constants.json').read_text())

    def test_reference_values_are_frozen(self):
        from paper_a_study import build_figure_data as B
        d = self.ref['derived']
        self.assertAlmostEqual(B.K0 / d['K0'], 1.0, places=10)
        self.assertAlmostEqual(B.KB0 / d['KB0'], 1.0, places=10)
        self.assertAlmostEqual(B.KY0 / d['KY0'], 1.0, places=10)
        self.assertAlmostEqual(B.OMEGA0 / d['OMEGA0'], 1.0, places=10)
        self.assertAlmostEqual(B.HCRIT / d['HCRIT'], 1.0, places=10)

    def test_material_constants_are_physical(self):
        for key, (lo, hi) in self.ref['bands'].items():
            value = SI[key]
            self.assertTrue(lo <= value <= hi,
                            f'{key} = {value!r} is outside the literature band '
                            f'[{lo}, {hi}] - a unit error would land here')
        for key, value in self.ref['material'].items():
            self.assertAlmostEqual(SI[key] / value, 1.0, places=12)


class TestCertifiedPeak(unittest.TestCase):
    """The four ways the round-7 maximum claim could be (and twice was) wrong.

    These tests are deliberately built on *solver evaluations*, not on stored
    expected values: each one fails if the physics changes, and each one would
    have failed on the previous revision.
    """

    @classmethod
    def setUpClass(cls):
        import sys
        from pathlib import Path
        here = Path(__file__).resolve().parent
        if str(here) not in sys.path:
            sys.path.insert(0, str(here))
        from build_figure_data import (KY0, KB0, operating_mode, plate, track)
        cls.KY0, cls.KB0 = KY0, KB0
        cls.mode_of = staticmethod(operating_mode)
        cls.plate, cls.track = staticmethod(plate), staticmethod(track)
        cls.cache = {}

    def _solve(self, K, degree=22, L=10.0):
        key = (round(K, 9), degree, L)
        if key not in self.cache:
            p = self.plate(0.0, degree=degree)
            m = self.track(p, [K], self.mode_of(p))[0]
            res, _ = p.edge(self.KY0, m['omega'].real, float(K), self.KB0, L=L)
            self.cache[key] = res
        return self.cache[key]

    def test_a_coarse_raster_cannot_be_certified(self):
        """No sample of the 0.01 raster may reach the refined maximum.

        The previous revision read the maximum off a coarse sweep and quoted
        57.92 % (0.55) and later 93.19 % (0.525); both are below the value the
        same solver returns at 0.5275.  A regression that reintroduces a
        coarse-grid maximum fails here.
        """
        coarse = [self._solve(K)['backward_reflection_self_power']
                  for K in (0.52, 0.525, 0.53)]
        refined = self._solve(0.5275)['backward_reflection_self_power']
        self.assertGreater(refined, max(coarse) + 5e-4,
                           'a coarse sample is within 5e-4 of the refined maximum')
        self.assertGreater(refined, 0.94)
        self.assertLess(refined, 1.0)

    def test_incident_mode_is_not_the_backward_target(self):
        """The case label must be an incident wavenumber, not KB0.

        Passing the backward target (0.245) as the incident guess is the blunder
        that produced R_B = 0.5444 in round 4.  It is caught by requiring the
        returned incident root to sit near the requested wavenumber and far from
        the backward target.
        """
        res = self._solve(0.5275)
        ki = complex(res['incident_K'])
        kb = complex(res['backward_K'])
        self.assertLess(abs(ki.real - 0.5275), 2e-3)      # flat-branch offset
        self.assertGreater(abs(ki.real - self.KB0), 0.2)
        self.assertGreater(kb.real, 0.0)                  # positive Re K
        self.assertLess(res['backward']['Px'], 0.0)       # negative x-power
        self.assertTrue(res['negative_direction'])

    def test_partition_is_independent_of_the_reference_plane(self):
        """Both partner modes attenuate; the net exponent must rescale exactly.

        Using the backward decay alone (the previous formula) leaves a 2 %
        discrepancy at the maximum.  This test measures the net exponent from
        the solver instead of assuming it.
        """
        a = self._solve(0.5275, L=10.0)
        b = self._solve(0.5275, L=15.0)
        ki_a, kb_a = complex(a['incident_K']), complex(a['backward_K'])
        ki_b, kb_b = complex(b['incident_K']), complex(b['backward_K'])
        net = 2.0 * (abs(ki_a.imag) + abs(kb_a.imag)) * 5.0
        ratio = (a['backward_reflection_self_power'] /
                 b['backward_reflection_self_power'])
        self.assertAlmostEqual(ratio / np.exp(net), 1.0, places=9)
        self.assertGreater(abs(kb_b.imag), 0.0)

    def test_reported_peak_matches_the_search_record(self):
        """The manuscript's headline must equal the recorded solver value."""
        import json
        from pathlib import Path
        rec = json.loads((Path(__file__).resolve().parent / 'figure_data'
                          / 'peak_search.json').read_text())
        reported = rec['classification']['R_B_reported']
        self.assertEqual(rec['classification']['classification'],
                         'certified_local_maximum')
        self.assertAlmostEqual(
            self._solve(0.5275)['backward_reflection_self_power'] / reported,
            1.0, places=9)
        self.assertGreater(rec['classification']['R_B_at_max'], reported)
        self.assertLess(abs(rec['classification']['R_B_at_max'] - reported), 1e-5)


class _EdgeProfile:
    """Shared reference configuration and a call-time handle on the transform.

    The transform is looked up through the module object on every call, never
    bound at import: that is the only way a mutation that patches
    ``build_figure_data.edge_plane_fraction`` reaches these tests, and a test
    that cannot see a patched function cannot guard anything.
    """

    @classmethod
    def setUpClass(cls):
        import sys
        from pathlib import Path
        here = Path(__file__).resolve().parent
        if str(here) not in sys.path:
            sys.path.insert(0, str(here))
        from paper_a_study import build_figure_data as bfd
        cls.bfd = bfd
        cls.data = here / 'figure_data'
        cls.K0, cls.KB0, cls.KY0 = bfd.K0, bfd.KB0, bfd.KY0
        cls.REF = bfd.REF_NORM
        # the certified maximum, from the solve itself (not from a stored value)
        p = bfd.plate(0.0, degree=22)
        mode = bfd.track(p, [0.5275], bfd.operating_mode(p))[0]
        cls.omega = float(mode['omega'].real)
        cls.p = p
        cls._solves = {}

    def edge(self, R, ki, kb, d, **kw):
        return self.bfd.edge_plane_fraction(R, ki, kb, d, **kw)

    def solve(self, L, K=0.5275, ky=None, omega=None):
        key = (round(L, 6), round(K, 9), ky, omega)
        if key not in self._solves:
            if omega is None:
                m = self.bfd.track(self.p, [K], self.bfd.operating_mode(self.p))[0]
                omega = float(m['omega'].real)
            res, _ = self.p.edge(self.bfd.KY0 if ky is None else float(ky),
                                 omega, float(K), self.KB0, L=L)
            self._solves[key] = res
        return self._solves[key]


class TestEdgePlaneTransform(_EdgeProfile, unittest.TestCase):
    """The two-plane ratio transform, on synthetic data only.

    Four identities and one distinction.  None of these tests reads a stored
    record, so they fail if the transform is wrong for any reason at all --
    halved exponent, flipped sign, wrong reference distance, or the thickness
    replaced by the gradient length.
    """

    KI = 0.528235992 + 1.004047e-3j
    KB = 0.526131801 - 1.002930e-3j
    D = 200e-9
    R = 0.9467952307

    def test_coincident_planes_return_the_input(self):
        got = self.edge(self.R, self.KI, self.KB, self.D, L_to=3.0, L_from=3.0)
        self.assertLess(abs(got / self.R - 1.0), 1e-15,
                        'the transform must be the identity between coincident planes')

    def test_composition_is_additive_in_distance(self):
        at5 = self.edge(self.R, self.KI, self.KB, self.D, L_to=5.0, L_from=10.0)
        at0 = self.edge(at5, self.KI, self.KB, self.D, L_to=0.0, L_from=5.0)
        direct = self.edge(self.R, self.KI, self.KB, self.D, L_to=0.0, L_from=10.0)
        self.assertLess(abs(at0 / direct - 1.0), 1e-15,
                        '10 -> 5 -> 0 must equal 10 -> 0')

    def test_edge_value_uses_both_attenuations(self):
        """The exponent is a sum of magnitudes, not the backward decay alone."""
        expected = self.R * np.exp(2 * (abs(self.KI.imag) + abs(self.KB.imag)) * self.REF)
        got = self.edge(self.R, self.KI, self.KB, self.D)
        self.assertLess(abs(got / expected - 1.0), 1e-12)
        backward_only = self.R * np.exp(2 * abs(self.KB.imag) * self.REF)
        self.assertGreater(abs(backward_only / got - 1.0), 1e-3,
                           'the single-mode decay differs from the ratio transform by '
                           'about 2e-2 here; a transform that reproduces it is wrong')

    def test_round_trip_between_planes(self):
        at15 = self.edge(self.R, self.KI, self.KB, self.D, L_to=15.0, L_from=10.0)
        back = self.edge(at15, self.KI, self.KB, self.D, L_to=10.0, L_from=15.0)
        self.assertLess(abs(back / self.R - 1.0), 1e-15, 'round trip must return the input')
        # moving *away* from the edge lowers the ratio: both modes attenuate and
        # the ratio sees the sum of the two.  (This assertion had the direction
        # reversed when it was first written; the derivation in
        # build_figure_data.edge_plane_fraction is the authority.)
        self.assertLess(at15, self.R,
                        'the ratio must fall as the plane moves away from the edge')

    def test_single_mode_transfer_is_a_different_quantity(self):
        """isolated_transfer is legitimate, but it is not a ratio transform."""
        single = self.bfd.isolated_transfer(self.R, self.KB, self.D, 0.0)
        ratio = self.edge(self.R, self.KI, self.KB, self.D, L_to=0.0, L_from=self.REF)
        self.assertLess(single, ratio)
        self.assertGreater(abs(single / ratio - 1.0), 1e-3,
                           'the two differ by ~2 % at the certified maximum; if they agree, '
                           'someone has reused the single-mode decay as a ratio')

    def test_zero_attenuation_leaves_the_ratio_alone(self):
        got = self.edge(self.R, 0.5282 + 0j, 0.5261 + 0j, self.D)
        self.assertLess(abs(got / self.R - 1.0), 1e-15)


class TestPlaneInvariance(_EdgeProfile, unittest.TestCase):
    """Is the reconstructed edge share a property of the edge or of the plane?

    Four solves, no stored values.  A transform with the sign or the exponent
    wrong makes the reconstructed value depend on the plane at which it was
    read, which is exactly the failure this class exists to catch.
    """

    PLANES = (0.0, 10.0, 15.0, 20.0)

    def _edge_from(self, L):
        res = self.solve(L)
        return float(self.edge(
            res['backward_reflection_self_power'],
            complex(res['incident_K']), complex(res['backward_K']), self.p.d,
            L_to=0.0, L_from=L))

    def test_reconstructed_edge_value_is_plane_independent(self):
        direct = float(self.solve(0.0)['backward_reflection_self_power'])
        for L in self.PLANES:
            got = self._edge_from(L)
            rel = abs(got / direct - 1.0)
            self.assertLess(rel, 1e-9,
                            f'reconstructed edge value depends on the plane (L={L}): '
                            f'{rel:.2e} relative; the round-9 defect was 2e-2')

    def test_solved_edge_value_equals_the_transform(self):
        at_ref = self.solve(self.REF)
        expected = float(self.edge(
            at_ref['backward_reflection_self_power'],
            complex(at_ref['incident_K']), complex(at_ref['backward_K']), self.p.d,
            L_to=0.0, L_from=self.REF))
        direct = float(self.solve(0.0)['backward_reflection_self_power'])
        rel = abs(expected / direct - 1.0)
        # the two differ only by the degree sensitivity of the edge solve (5e-9)
        self.assertLess(rel, 1e-6, f'transform and direct solve differ by {rel:.2e}')

    def test_the_raw_values_really_do_move(self):
        """The invariance must not be vacuous: the ratio itself does depend on L."""
        near = float(self.solve(0.0)['backward_reflection_self_power'])
        far = float(self.solve(20.0)['backward_reflection_self_power'])
        self.assertGreater(abs(near / far - 1.0), 1e-2,
                           'the raw ratio must fall measurably over twenty thicknesses')


class TestCrossScriptEdgeFraction(_EdgeProfile, unittest.TestCase):
    """Every producer of an edge-plane share must use the same transform.

    This is the gate for the round-9 defect: peak_search.py moved the ratio with
    the single-mode decay and reported 0.965978 where mechanism_controls.py
    reported 0.985572, and nothing compared the two.
    """

    def test_peak_search_record_matches_the_shared_transform(self):
        import json
        rec = json.loads((self.data / 'peak_search.json').read_text())
        row = [r for r in rec['degree']
               if abs(r['K'] - 0.5275) < 1e-12 and r['degree'] == 22][0]
        expected = float(self.edge(float(row['R_B']), complex(*row['K_incident']),
                                   complex(*row['K_backward']), self.p.d))
        rel = abs(float(row['R_B_edge']) / expected - 1.0)
        self.assertLess(rel, 1e-12,
                        f'peak_search stored edge share vs the shared transform: {rel:.2e}')

    def test_mechanism_controls_record_matches_the_shared_transform(self):
        import json
        mc = json.loads((self.data / 'mechanism_controls.json').read_text())
        row = [r for r in mc['branch_consistent_H_sweep']['refined_peak'] if r['eta'] == 0.0][0]
        ident = json.loads((self.data / 'peak_identity_audit.json').read_text())
        peak = ident['cases']['peak']
        ki = complex(*peak['K_incident'])
        expected = float(self.edge(float(row['R_B']), ki,
                                   complex(row['backward_K_real'], row['backward_K_imag']),
                                   self.p.d))
        rel = abs(float(row['R_B_edge']) / expected - 1.0)
        self.assertLess(rel, 1e-12,
                        f'mechanism_controls stored edge share vs the shared transform: {rel:.2e}')

    def test_figure_csvs_match_the_shared_transform(self):
        import csv  # noqa: F401
        with open(self.data / 'fig05_channel_power.csv') as fh:
            rows5 = [r for r in csv.DictReader(fh) if abs(float(r['eta'])) < 1e-12]
        # fig05 is the operating point (k_x d = K0), not the certified maximum
        res = self.solve(self.REF, K=self.K0)
        expected5 = float(self.edge(float(res['backward_reflection_self_power']),
                                    complex(res['incident_K']), complex(res['backward_K']),
                                    self.p.d))
        rel5 = abs(float(rows5[0]['R_B_edge']) / expected5 - 1.0)
        self.assertLess(rel5, 1e-6, f'fig05 CSV vs shared transform: {rel5:.2e}')
        with open(self.data / 'fig07_coupling_sensitivity.csv') as fh:
            rows7 = [r for r in csv.DictReader(fh) if abs(float(r['eta'])) < 1e-12]
        self.assertTrue(rows7, 'no H = 0 row in fig07')
        # fig07 sweeps k_y at the fixed operating frequency and wavenumber, so the
        # reference solve is posed the same way rather than branch-tracked
        from paper_a_study.build_figure_data import OMEGA0, plate
        p = plate(0.0, degree=22)
        for row in (rows7[0], rows7[len(rows7) // 2], rows7[-1]):
            res7, _ = p.edge(float(row['ky']), OMEGA0, self.K0, self.KB0)
            expected = self.edge(float(res7['backward_reflection_self_power']),
                                 complex(res7['incident_K']), complex(res7['backward_K']), p.d)
            rel7 = abs(float(row['R_B_edge']) / expected - 1.0)
            self.assertLess(rel7, 1e-6,
                            f'fig07 CSV vs shared transform at ky={row["ky"]}: {rel7:.2e}')

    def test_all_producers_agree_with_each_other(self):
        import json
        rec = json.loads((self.data / 'peak_search.json').read_text())
        ps = float([r for r in rec['degree'] if abs(r['K'] - 0.5275) < 1e-12
                    and r['degree'] == 22][0]['R_B_edge'])
        mc = json.loads((self.data / 'mechanism_controls.json').read_text())
        mcv = float([r for r in mc['branch_consistent_H_sweep']['refined_peak']
                     if r['eta'] == 0.0][0]['R_B_edge'])
        rel = abs(ps / mcv - 1.0)
        self.assertLess(rel, 1e-6,
                        f'peak_search and mechanism_controls disagree on the edge fraction '
                        f'({rel:.2e} relative; the round-8 defect was 2.0e-2)')
        # the edge fraction must exceed the reference-plane value it came from
        self.assertGreater(ps, 0.9467952)
        self.assertLess(ps, 1.0)



class TestFigureProvenance(unittest.TestCase):
    """Round-11 defects D1-D7: a figure's labels and its provenance are part of
    the result, and were invisible to the 39 numerical tests that preceded them.
    """

    @classmethod
    def setUpClass(cls):
        import json
        import sys
        from pathlib import Path
        import os
        cls.here = Path(__file__).resolve().parent
        # generate_final_figures.py imports figure_style as a sibling module,
        # exactly as it is run by the renderer
        if str(cls.here) not in sys.path:
            sys.path.insert(0, str(cls.here))
        from generate_final_figures import PANEL_SOURCES
        cls.panel_sources = PANEL_SOURCES
        # the mutation harness points this at a mutated copy of the renderer
        src_root = Path(os.environ.get('PAPER_A_FIGURE_SRC', str(cls.here)))
        cls.src = (src_root / 'generate_final_figures.py').read_text()
        cls.map = json.loads((cls.here / 'figure_data' /
                              'figure_panel_sources.json').read_text())

    def test_panel_map_agrees_with_the_plotting_code(self):
        derived = {f['figure']: f['panels'] for f in self.map['figures']}
        expected = {stem: [f'({letter}) {text}' for letter, text, _ in spec['panels']]
                    for stem, spec in self.panel_sources.items()}
        self.assertEqual(derived, expected,
                         'figure_panel_sources.json has drifted from the plotting code')

    def test_every_figure_is_mapped_with_four_panels(self):
        self.assertEqual(len(self.map['figures']), 10)
        for entry in self.map['figures']:
            self.assertEqual(len(entry['panels']), 4,
                             f'{entry["figure"]} does not list four panels')
            for ext in ('pdf', 'png', 'svg'):
                self.assertIn(ext, entry, f'{entry["figure"]} has no {ext}')

    def test_backward_share_is_never_called_a_reflectance(self):
        self.assertNotIn('backward reflectance', self.src,
                         'R_B is a modal share of the incident power, not a reflectance')
        self.assertNotIn('reflectance $R_B$', self.src)

    def test_the_reference_plane_is_L_and_the_gradient_length_is_l(self):
        self.assertNotIn(r'\ell=2', self.src,
                         'the reference plane is written with the gradient-length symbol')
        self.assertNotIn(r'$R_B(\ell)$', self.src,
                         'the distance from the edge is L, not the gradient length')
        self.assertNotIn(r'distance from edge  $\ell$', self.src,
                         'the distance from the edge is L, not the gradient length')

    def test_residual_panels_declare_their_round_off_floor(self):
        self.assertIn('round-off floor', self.src,
                      'a residual panel drawn on a log axis must name the numerical floor')
        self.assertIn(r'floor $\sim10^{-15}$', self.src)

    def test_the_schematic_panel_is_labelled(self):
        self.assertIn('"schematic"', self.src,
                      'fig10(c) is a drawing and must say so inside the panel')

    def test_figure_csvs_carry_the_columns_the_plotters_read(self):
        """A stale generator writes the same file names with an older schema."""
        required = {
            'fig01_dispersion_velocity_attenuation.csv':
                {'ky', 'attenuation_dB_per_mm', 'K_spatial_imag'},
            'fig04_frequency_reflection.csv': {'R_B_2um', 'K_ratio'},
            'fig05_channel_power.csv': {'R_B_2um', 'power_balance_error'},
            'fig08_thickness_flux.csv': {'backward_Px', 'quadrature_weight'},
            'fig09_validation_convergence.csv': {'edge_scaled_residual', 'power_error'},
            'fig10_field_maps.csv': {'incident_intensity', 'backward_intensity'},
        }
        for name, cols in required.items():
            header = (self.here / 'figure_data' / name).read_text().splitlines()[0]
            missing = cols - set(header.split(','))
            self.assertFalse(missing, f'{name} lacks {sorted(missing)}: built by a stale generator?')

    def test_no_panel_ink_touches_the_canvas_edge(self):
        from PIL import Image
        for entry in self.map['figures']:
            png = self.here / 'figures_final' / f"{entry['figure']}.png"
            im = np.asarray(Image.open(png).convert('L'))
            ink = im < 200
            rows, cols = ink.sum(axis=1), ink.sum(axis=0)
            self.assertEqual(rows[0] + cols[0] + rows[-1] + cols[-1], 0,
                             f'{png.name}: ink reaches the canvas edge (clipped label)')




class TestFigure10BackwardWavenumber(unittest.TestCase):
    """Round-13 defect B1: fig10(c) drew the backward *wavenumber* along
    (0.333, -0.530) -- one ratio from K_Bx/K_ix, one from |k_y|/K_Bx, and the
    sign of the *flux*.  The solved wavevector points into +x,+y at +27.90 deg.
    The guard is exercised below with the reversed vector, so a silent return of
    the defect fails here.
    """

    @classmethod
    def setUpClass(cls):
        import importlib.util
        import json
        import os
        import sys
        from pathlib import Path
        cls.here = Path(__file__).resolve().parent
        if str(cls.here) not in sys.path:
            sys.path.insert(0, str(cls.here))
        # the mutation harness points this at a mutated copy of the renderer
        cls.src_root = Path(os.environ.get('PAPER_A_FIGURE_SRC', str(cls.here)))
        spec = importlib.util.spec_from_file_location(
            'fig10_module_under_test', cls.src_root / 'generate_final_figures.py')
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)
        cls.metrics = json.loads((cls.here / 'figure_data' /
                                  'fig10_field_metrics.json').read_text())

    def test_drawn_backward_wavenumber_is_the_solved_one(self):
        pw = self.metrics['primary_wavenumbers']
        drawn = self.mod.fig10_directions(self.metrics)['k_B']
        expected = np.array([1.0, pw['ky_d'] / pw['backward_kx_d']])
        np.testing.assert_allclose(drawn / np.linalg.norm(drawn),
                                   expected / np.linalg.norm(expected), atol=1e-12)
        self.assertGreater(float(drawn[0]), 0.0)
        self.assertGreater(float(drawn[1]), 0.0, 'k_B points into +y, not into -y')
        # the numbers the manuscript quotes for this panel
        self.assertAlmostEqual(pw['ky_d'] / pw['backward_kx_d'], 0.529, places=3)
        self.assertAlmostEqual(pw['backward_phase_angle_deg'], 27.9, places=1)
        self.assertAlmostEqual(pw['incident_phase_angle_deg'], 10.0, places=6)

    def test_the_drawn_length_keeps_the_solved_magnitude_ratio(self):
        ratio = self.metrics['primary_wavenumbers']['magnitude_ratio_backward_over_incident']
        pw = self.metrics['primary_wavenumbers']
        solved = (np.hypot(pw['backward_kx_d'], pw['ky_d']) /
                  np.hypot(pw['incident_kx_d'], pw['ky_d']))
        self.assertAlmostEqual(ratio, solved, places=12)
        self.assertLess(ratio, 0.5, 'the backward wavenumber is shorter than the incident one')

    def test_flux_opposes_the_wavenumber(self):
        dirs = self.mod.fig10_directions(self.metrics)
        self.assertLess(float(np.dot(dirs['k_B'], dirs['P_B'])), 0.0,
                        'for a backward mode the flux points opposite to the phase vector')
        self.assertLess(float(dirs['P_B'][0]), 0.0)
        self.assertLess(float(dirs['P_B'][1]), 0.0)
        self.assertGreater(float(dirs['P_i'][0]), 0.0)
        self.assertGreater(float(dirs['P_i'][1]), 0.0, 'the incident flux keeps +y')

    def test_reversed_arrow_is_rejected(self):
        drawn = self.mod.fig10_directions(self.metrics)['k_B']
        self.mod.check_backward_wavenumber(drawn, self.metrics)          # passes
        for bad in (-drawn, np.array([drawn[0], -drawn[1]]),
                    np.array([0.333, -0.530])):                          # the old literal
            with self.assertRaises(ValueError):
                self.mod.check_backward_wavenumber(bad, self.metrics)

    def test_the_renderer_calls_the_guard(self):
        src = (self.src_root / 'generate_final_figures.py').read_text()
        self.assertIn('check_backward_wavenumber(dirs["k_B"], metrics)', src,
                      'the schematic must be guarded at render time, not only in tests')


if __name__=='__main__':unittest.main(verbosity=2)
