"""A0-S regression tests; no edge-scattering or reflection assertion."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from dispersion_screen import (ComplexPlate,SI,CONST,C_LIGHT,ROOT,longitudinal_cutoff,
    tracked_mode,mass_mac,twelve_state_operator,strong_root,strong_energy,
    conditioned_root,conditioned_scalar,conditioned_fields,condensed_stiffness,
    spatial_diagnostics,radiation_screen)

P=Path(__file__).resolve().parent
PROTOCOL=json.loads((P/'protocol.json').read_text())
OVERRIDES={'electron_mobility':.0175,'electron_diffusivity':.000455}


def plate(ell=50e-9,H=None,d=.2e-6,n0=2e18,**kwargs):
    return ComplexPlate(degree=28,d=d,n0=n0,ell=ell,H=H,overrides=OVERRIDES,**kwargs)


class TestA0S(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=plate();cls.m0=longitudinal_cutoff(cls.p)
        cls.m=tracked_mode(cls.p,.3,cls.m0)
        cls.w=cls.m['omega'].real
        cls.r=conditioned_root(cls.p,cls.w,.3-.0005j)
        cls.f=conditioned_fields(cls.p,cls.r['K'],cls.w)
        cls.e=cls.p.spatial_energy(cls.r['K'],cls.w,cls.f)

    def test_retained_ten_files_identical(self):
        old=json.loads((P/'results/retained_sha256.json').read_text())
        self.assertEqual(len(old),10)
        for path,digest in old.items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest,path)

    def test_only_two_sourced_carrier_inputs(self):
        self.assertEqual([v['n0_m_minus3'] for v in PROTOCOL['carrier_cases']],[2e18,1e19])
        self.assertEqual(2e12*1e6,2e18)
        self.assertNotIn(1e17,[v['n0_m_minus3'] for v in PROTOCOL['carrier_cases']])

    def test_joint_Hall_pair_and_derived_diffusion(self):
        c=PROTOCOL['carrier_cases'][0]
        self.assertEqual(c['electron_mobility_m2_Vs'],175*1e-4)
        self.assertAlmostEqual(c['electron_diffusivity_m2_s']/c['electron_mobility_m2_Vs'],.026,14)
        self.assertIn('derived',c['status'])
        self.assertIn('Hall-to-drift',c['status'])

    def test_unmeasured_ranges_not_filled_in(self):
        self.assertIsNone(PROTOCOL['H_screen']['physical_range'])
        self.assertFalse(PROTOCOL['radiation']['full_Maxwell_solved'])
        self.assertEqual(PROTOCOL['transport_gate']['distance_m'],100e-6)
        self.assertIn('synthetic',PROTOCOL['model_controls'][1]['status'].lower())

    def test_physical_H_is_fixed_not_renormalized_between_materials(self):
        ref=ComplexPlate(ell=50e-9,n0=1e19,eta=.5,direction=(1,0,0))
        p1=plate(H=ref.H_SI);p2=plate(H=ref.H_SI,d=1e-6,n0=1e19)
        np.testing.assert_array_equal(p1.H_SI,p2.H_SI)
        self.assertAlmostEqual(p1.schur_fraction/p2.schur_fraction,.2,12)
        self.assertFalse(np.allclose(p1.hvec,p2.hvec))

    def test_full_three_dimensional_schur_rejection(self):
        with self.assertRaises(ValueError):ComplexPlate(ell=50e-9,eta=1.01)
        with self.assertRaises(ValueError):ComplexPlate(ell=0,H=[1e-23,0,0])

    def test_mac_is_phase_and_scale_invariant(self):
        self.assertAlmostEqual(mass_mac(self.p,self.m['U'],2j*self.m['U']),1,12)
        close=tracked_mode(self.p,.301,self.m)
        self.assertGreater(close['MAC'],.999)

    def test_synthetic_thin_branch_not_truncated_at_old_small_K(self):
        # Bounded continuation, not nearest-frequency jumps across large steps.
        ref=self.m0;macs=[]
        for K in np.linspace(.01,.7,70):
            ref=tracked_mode(self.p,K,ref);macs.append(ref['MAC'])
        self.assertGreater(min(macs),.98)
        self.assertLess(ref['omega'].real,self.m0['omega'].real-.06)
        self.assertGreater(ref['omega'].real,7.89)

    def test_exact_dynamic_condensation_preserves_determinant(self):
        K=.3-.001j;w=7.92
        D,_,_=self.p.spatial_stiffness(K,w)
        S,lo,hi,_,_,_=condensed_stiffness(self.p,K,w)
        z,ld=np.linalg.slogdet(D);a,la=np.linalg.slogdet(D[np.ix_(hi,hi)]);b,lb=np.linalg.slogdet(S)
        self.assertAlmostEqual(ld,la+lb,places=7)
        self.assertLess(abs(z-a*b),1e-7)
        self.assertEqual(len(lo),8)

    def test_conditioned_spatial_root_and_strong_BCs(self):
        self.assertTrue(self.r['converged'])
        self.assertLess(abs(conditioned_scalar(self.p,self.r['K'],self.w)),1e-10)
        self.assertLess(max(self.p.residuals(self.r['K'],self.w,self.f).values()),1e-7)

    def test_independent_twelve_state_temporal_and_spatial(self):
        a=strong_root(self.p,'temporal',.3,self.m['omega'])
        b=strong_root(self.p,'spatial',self.w,self.r['K'])
        self.assertTrue(a['converged'] and b['converged'])
        self.assertLess(abs(a['value']-self.m['omega']),1e-10)
        self.assertLess(abs(b['value']-self.r['K']),1e-9)

    def test_independent_all_three_H_directions(self):
        for direction in [(1,0,0),(0,1,0),(0,0,1),(1,.2,.1)]:
            q=ComplexPlate(degree=28,d=.2e-6,n0=2e18,ell=50e-9,eta=.3,direction=direction,overrides=OVERRIDES)
            m=tracked_mode(q,.3,longitudinal_cutoff(q))
            independent=strong_root(q,'temporal',.3,m['omega'])
            self.assertTrue(independent['converged'])
            self.assertLess(abs(independent['value']-m['omega']),1e-10)

    def test_strong_equation_bulk_balance_mixed_H(self):
        q=ComplexPlate(degree=28,d=.2e-6,n0=2e18,ell=50e-9,eta=.3,direction=(1,.2,.1),overrides=OVERRIDES)
        K=.4-.02j;om=7.9;F=twelve_state_operator(q,K,om)
        rng=np.random.default_rng(418)
        y=rng.normal(size=12)+1j*rng.normal(size=12);yp=F@y;ypp=F@yp;yppp=F@ypp
        e0=np.array([1j*K*y[0],y[3],y[2]+1j*K*y[1]])
        e1=np.array([1j*K*y[2],yp[3],yp[2]+1j*K*y[3]])
        e2=np.array([1j*K*yp[2],ypp[3],ypp[2]+1j*K*yp[3]])
        e3=np.array([1j*K*ypp[2],yppp[3],yppp[2]+1j*K*ypp[3]])
        C=q.C;E=q.e;ell2=q.ell**2;ha,hb,hc=q.hvec
        hx=np.array([0,0,hc]);hz=np.array([hb,ha,0])
        sig=C@e0+E.T@np.array([1j*K*y[4],yp[4]])
        sigp=C@e1+E.T@np.array([1j*K*yp[4],ypp[4]])
        S=sig-1j*K*(ell2*1j*K*C@e0+hx*y[5])-(ell2*C@e2+hz*yp[5])
        Sp=sigp-1j*K*(ell2*1j*K*C@e1+hx*yp[5])-(ell2*C@e3+hz*ypp[5])
        force=np.array([1j*K*S[0]+Sp[2],1j*K*S[2]+Sp[1]])+om**2*y[:2]
        np.testing.assert_allclose(force,0,atol=2e-9)
        mu=y[5]+ha*yp[3]+(hb+hc)*1j*K*y[2]-hc*K*K*y[1]-q.sc['Q']*y[4]
        mup=yp[5]+ha*ypp[3]+(hb+hc)*1j*K*yp[2]-hc*K*K*y[3]-q.sc['Q']*yp[4]
        self.assertLess(abs(mup+y[11]/q.sc['alpha']),1e-10)
        self.assertLess(abs(yp[11]-(1j*om*y[5]-q.sc['alpha']*K*K*mu)),1e-10)
        d1=(E@e0-q.kap@np.array([1j*K*y[4],yp[4]]))[0]
        self.assertLess(abs(yp[10]+1j*K*d1+q.sc['Q']*y[5]),1e-10)

    def test_independent_strong_flux_and_full_energy_accounting(self):
        independent=strong_energy(self.p,self.r['K'],self.w)
        for name in ['power','mean_energy','dissipation','vacuum_power','face_hyperstress_power']:
            self.assertLess(abs(independent[name]/self.e[name]-1),1e-7,name)
        self.assertLess(independent['spatial_balance_relative'],1e-7)
        self.assertNotEqual(self.e['face_hyperstress_power'],0)
        self.assertNotEqual(self.e['vacuum_power'],0)

    def test_backward_is_energy_not_merely_negative_slope(self):
        self.assertGreater(self.r['K'].real,0)
        self.assertLess(self.r['K'].imag,0)
        self.assertLess(self.e['power'],0)
        self.assertTrue(self.e['backward'] and self.e['passive_direction'])
        self.assertLess(self.e['energy_velocity_m_s'],-100)
        self.assertGreater(self.e['mean_energy'],0)

    def test_100um_and_one_wavelength_are_both_required(self):
        self.assertGreater(self.e['energy_1e_length_m'],100e-6)
        self.assertGreater(self.e['power_fraction_100um'],.5)
        self.assertGreater(self.e['power_fraction_one_phase_wavelength'],.9)
        q=plate(ell=0)
        # Its carrier-shifted frequency bracket, not the old frozen target.
        w=7.432477387131337
        r=conditioned_root(q,w,.004-.009j)
        diag=spatial_diagnostics(q,r['K'],w)
        self.assertTrue(diag['admissible_backward'])
        self.assertFalse(diag['transport_screen_pass'])
        self.assertLess(diag['power_survival_100um'],.001)

    def test_amplitude_energy_and_wavelength_conventions(self):
        self.assertAlmostEqual(self.e['amplitude_1e_length_m']/self.e['energy_1e_length_m'],2,12)
        self.assertAlmostEqual(np.exp(-100e-6/self.e['energy_1e_length_m']),self.e['power_fraction_100um'],12)
        self.assertAlmostEqual(np.exp(-self.e['phase_wavelength_m']/self.e['energy_1e_length_m']),self.e['power_fraction_one_phase_wavelength'],12)

    def test_growing_exterior_formal_root_is_rejected(self):
        q=ComplexPlate(degree=24,d=1e-6,n0=1e19)
        r=conditioned_root(q,7.432543949196749,-.052-.064j)
        self.assertTrue(r['converged']);self.assertLess(r['K'].real,0)
        diag=spatial_diagnostics(q,r['K'],7.432543949196749)
        self.assertFalse(diag['admissible_backward'])
        self.assertNotIn('transport',diag)

    def test_radiation_guard_is_not_a_Maxwell_proof(self):
        rad=radiation_screen(self.p,self.r['K'],self.w)
        self.assertTrue(rad['vacuum_laplace_decay'] and rad['above_vacuum_phase_light_line'])
        self.assertLess(rad['relative_EM_exponent_change'],1e-6)
        self.assertFalse(rad['full_Maxwell_radiation_solved'])
        below=radiation_screen(self.p,complex(1e-5,-1e-6),self.w)
        self.assertFalse(below['above_vacuum_phase_light_line'])
        self.assertEqual(C_LIGHT,299792458)

    def test_correct_power_FWHM_not_HWHM(self):
        q=ComplexPlate(degree=24,d=1e-6,n0=1e19)
        m=q.temporal_mode(.009890015583941397)
        fwhm=-m['omega'].imag*q.sc['cs']/(np.pi*q.sc['d'])
        self.assertAlmostEqual(fwhm,2313453.835,delta=1)
        self.assertGreater(fwhm,2e6)

    def test_independent_eight_state_recovery_for_source_classical_limit(self):
        q=plate(ell=0);m=q.temporal_mode(.01)
        r=strong_root(q,'temporal',.01,m['omega'])
        self.assertTrue(r['converged'])
        self.assertLess(abs(r['value']-m['omega']),1e-10)

    def test_H_changes_finite_rate_damping_not_frozen_label(self):
        q=ComplexPlate(degree=28,d=.2e-6,n0=2e18,ell=50e-9,eta=.3,direction=(1,0,0),overrides=OVERRIDES)
        m=tracked_mode(q,.3,longitudinal_cutoff(q))
        self.assertGreater(-m['omega'].imag,10*(-self.m['omega'].imag))
        self.assertLess(q.schur_fraction,1)
        self.assertFalse(PROTOCOL['H_screen']['physical_range'] is not None)

if __name__=='__main__':unittest.main()
