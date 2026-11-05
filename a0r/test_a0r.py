"""A0-R regression checks. These do NOT certify novelty or negative reflection."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import unittest
import numpy as np

from complex_dispersion import (ComplexPlate, Plate, SI, derived,
                                independent_spatial_root, independent_temporal_root)

ROOT=Path(__file__).resolve().parents[1]
KBACK=.009890015583941397
DRIVE=7.432543949196749


class A0RTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=ComplexPlate(degree=22)
        cls.t=cls.p.temporal_mode(KBACK)
        cls.forward=cls.p.spatial_root(DRIVE,.0952+.0624j)
        cls.back_formal=cls.p.spatial_root(DRIVE,-.052-.0637j)
        cls.low=ComplexPlate(degree=22,n0=1e17)
        cls.lowback=cls.low.spatial_root(DRIVE,.00888-.00364j)
        cls.h=ComplexPlate(degree=30,ell=50e-9,eta=.8)

    def test_01_analytic_cutoff_and_full_not_checked_window(self):
        o0=np.pi*np.sqrt((SI['c33']+SI['e33']**2/SI['kappa33'])/SI['c44'])
        self.assertAlmostEqual(self.p.frozen_mode(0)['omega'],o0,places=10)
        z=7.432504347986044;fs=derived()['frequency_scale_Hz']
        self.assertAlmostEqual((o0-z)*fs/1e3,58.46099,places=4)
        self.assertGreater((o0-z)*fs,34.6223e3)

    def test_02_formal_real_K_matches_old_Galerkin(self):
        a=Plate(22).matrices(.04);b=self.p.analytic_matrices(.04)
        u,p=self.p.udofs,self.p.pdofs
        for key,rows,cols in [('Kuu',u,u),('Kup',u,p),('P',p,p),('L',p,p)]:
            np.testing.assert_allclose(a[key][np.ix_(rows,cols)],b[key],rtol=2e-13,atol=2e-10)

    def test_03_complex_K_is_analytic_not_Hermitian_reassembly(self):
        z=.03-.004j;h=1e-5
        f=lambda k:self.p.spatial_stiffness(k,DRIVE)[0]
        dx=(f(z+h)-f(z-h))/(2*h)
        dy=(f(z+1j*h)-f(z-1j*h))/(2j*h)
        self.assertLess(np.linalg.norm(dx-dy)/np.linalg.norm(dx),2e-6)
        a=self.p.analytic_matrices(z)
        self.assertGreater(np.linalg.norm(a['Kpu']-a['Kup'].conj().T),1e-4)

    def test_04_independent_temporal_eight_state(self):
        r=independent_temporal_root(KBACK,self.t['omega'])
        self.assertTrue(r['converged'])
        self.assertLess(abs(r['omega']-self.t['omega']),2e-10)
        self.assertLess(self.p.temporal_energy(KBACK,self.t['omega'],self.t)['temporal_balance_relative'],1e-7)

    def test_05_pole_linewidth_lifetime_definitions(self):
        om=self.t['omega'];gamma=-om.imag*self.p.sc['cs']/self.p.sc['d']
        hwhm=gamma/(2*np.pi);fwhm=gamma/np.pi
        self.assertAlmostEqual(fwhm,2*hwhm)
        self.assertAlmostEqual(hwhm/1e6,1.1567269176,places=6)
        self.assertAlmostEqual(1/(2*gamma)*1e9,68.7953832,places=5)

    def test_06_low_concentration_backward_spatial_port(self):
        r=self.lowback;self.assertTrue(r['converged']);self.assertTrue(r['exterior_decays'])
        ind=independent_spatial_root(DRIVE,r['K'],n0=1e17)
        self.assertLess(abs(ind['K']-r['K']),2e-8)
        en=self.low.spatial_energy(r['K'],DRIVE,self.low.spatial_fields(r['K'],DRIVE))
        self.assertTrue(en['backward']);self.assertTrue(en['passive_direction'])
        self.assertLess(r['K'].imag,0)
        self.assertLess(en['spatial_balance_relative'],1e-6)
        self.assertGreater(en['power_fraction_100um'],.45)
        self.assertLess(en['power_fraction_100um'],.55)

    def test_07_original_backward_continuation_is_not_decaying_vacuum(self):
        self.assertTrue(self.back_formal['converged'])
        self.assertFalse(self.back_formal['exterior_decays'])
        self.assertLess(self.back_formal['K'].real,0)
        with self.assertRaises(ValueError):
            self.p.spatial_energy(self.back_formal['K'],DRIVE,self.p.spatial_fields(self.back_formal['K'],DRIVE))

    def test_08_forward_spatial_power_and_lengths_are_separate(self):
        r=self.forward;en=self.p.spatial_energy(r['K'],DRIVE,self.p.spatial_fields(r['K'],DRIVE))
        self.assertFalse(en['backward']);self.assertTrue(en['passive_direction'])
        self.assertLess(en['spatial_balance_relative'],1e-6)
        self.assertAlmostEqual(en['amplitude_1e_length_m'],2*en['energy_1e_length_m'])
        self.assertAlmostEqual(en['energy_1e_length_m']*1e6,8.01672468,places=4)
        self.assertAlmostEqual(en['power_fraction_100um'],np.exp(-1e-4/en['energy_1e_length_m']))

    def test_09_full_three_dimensional_directional_Schur_bound(self):
        for direction in [(1,0,0),(0,1,0),(0,0,1),(1,.4,.3)]:
            p=ComplexPlate(ell=50e-9,eta=.8,direction=direction)
            self.assertAlmostEqual(p.schur_fraction,.64,places=12)
            with self.assertRaises(ValueError):
                ComplexPlate(ell=50e-9,eta=1.01,direction=direction)

    def test_10_nonzero_H_without_gradient_stiffness_is_rejected(self):
        with self.assertRaises(ValueError):ComplexPlate(H=[1e-23,0,0])

    def test_11_frozen_carriers_remove_every_H_direction(self):
        baseline=ComplexPlate(ell=50e-9).frozen_mode(2,near=8.83)['omega']
        for direction in [(1,0,0),(0,1,0),(0,0,1)]:
            p=ComplexPlate(ell=50e-9,eta=.8,direction=direction)
            self.assertEqual(p.frozen_mode(2,near=8.83)['omega'],baseline)

    def test_12_all_H_components_reciprocal_and_temporally_dissipative(self):
        p=ComplexPlate(degree=30,ell=50e-9,eta=.5,direction=(1,.4,.3))
        a=p.analytic_matrices(2.)
        np.testing.assert_allclose(a['Fnu'],a['F'].conj().T,rtol=1e-12,atol=1e-12)
        m=p.temporal_mode(2,near=8.83)
        self.assertLess(m['omega'].imag,0)
        self.assertLess(p.temporal_energy(2,m['omega'],m)['temporal_balance_relative'],1e-6)
        self.assertLess(max(p.residuals(2,m['omega'],m).values()),1e-7)

    def test_13_synthetic_spatial_balance_needs_face_power(self):
        p=self.h;m=p.temporal_mode(2,near=8.83);om=m['omega'].real
        r=p.spatial_root(om,2+.00242j)
        en=p.spatial_energy(r['K'],om,p.spatial_fields(r['K'],om))
        self.assertLess(en['spatial_balance_relative'],1e-6)
        no_face=abs(2*r['K'].imag*(en['power']-en['face_hyperstress_power'])-en['dissipation'])/en['dissipation']
        self.assertGreater(no_face,1e-4)
        self.assertFalse(en['backward'])

    def test_14_fixed_physical_H_carrier_free_limit(self):
        H=self.h.H_SI
        contrasts=[]
        for n0 in [1e19,1e15]:
            p=ComplexPlate(degree=30,ell=50e-9,n0=n0,H=H)
            zero=ComplexPlate(degree=30,ell=50e-9,n0=n0)
            contrasts.append(abs(p.temporal_mode(2,near=8.83)['omega']-zero.temporal_mode(2,near=8.83)['omega']))
        self.assertLess(contrasts[1]/contrasts[0],.001)

    def test_15_transport_probe_must_preserve_thermodynamic_ratio(self):
        with self.assertRaises(ValueError):
            ComplexPlate(overrides={'electron_mobility':1.05*SI['electron_mobility']})
        p=ComplexPlate(overrides={'electron_mobility':1.05*SI['electron_mobility'],
                                 'electron_diffusivity':1.05*SI['electron_diffusivity']})
        self.assertAlmostEqual(p.sc['theta'],self.p.sc['theta'])

    def test_16_retained_sources_and_research_gates(self):
        for path,digest in json.loads((ROOT/'a0r/results/retained_a0_sha256.json').read_text()).items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)
        data=json.loads((ROOT/'a0r/results/validation.json').read_text())
        self.assertTrue(data['all_executed_checks_passed'])
        self.assertEqual(data['decision'],'REVISE')
        self.assertEqual(data['novelty_status'],'NOVELTY UNRESOLVED')
        self.assertFalse(any(data['research_gates'].values()))
        self.assertTrue(data['no_edge_solver']);self.assertTrue(data['stop_after_checkpoint'])


if __name__=='__main__':unittest.main()
