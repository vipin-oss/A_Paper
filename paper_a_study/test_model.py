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


if __name__=='__main__':unittest.main(verbosity=2)
