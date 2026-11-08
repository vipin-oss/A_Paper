"""Small independent regression/consistency suite; no production imports."""
import json
from pathlib import Path
import unittest

import numpy as np

from constitutive_check import run as symbolic_run
from dispersion import (Plate, SI, CONST, derived, elastic_matrix,
                        independent_classical_root, track_grid)


class MaterialAndConstitutiveTests(unittest.TestCase):
    def test_transcribed_units_and_hexagonal_stability(self):
        self.assertEqual(SI['electron_mobility'], 100*1e-4)
        self.assertAlmostEqual(SI['electron_diffusivity'], 2.6*1e-4, places=16)
        self.assertEqual(SI['c66'], (SI['c11']-SI['c12'])/2)
        self.assertGreater(np.linalg.eigvalsh(elastic_matrix()).min(), 0)
        self.assertGreater(SI['kappa11'], 0)
        self.assertGreater(SI['kappa33'], 0)

    def test_transport_thermodynamic_consistency(self):
        sc = derived()
        L = sc['n0']*SI['electron_mobility']/CONST['q']
        self.assertAlmostEqual(sc['a']*L/SI['electron_diffusivity'], 1.)

    def test_exact_symbolic_derivatives_and_6mm_reduction(self):
        result = symbolic_run()
        self.assertEqual(result['independent_H_components'], 3)
        self.assertTrue(result['complete_potential_Hessian_reciprocity'])
        self.assertTrue(result['dynamic_elimination_frequency_dependent'])

    def test_strict_admissibility_guard(self):
        with self.assertRaises(ValueError): Plate(8, .05, 1.)
        with self.assertRaises(ValueError): Plate(8, .05, -1.)
        with self.assertRaises(ValueError): Plate(8, 0., .5)

    def test_fixed_physical_H_during_carrier_free_limit(self):
        p = Plate(10, .05, .5, n0=1e19)
        psmall = Plate(10, .05, .05, n0=1e17)
        self.assertAlmostEqual(psmall.h_SI/p.h_SI, 1., places=13)


class DispersionTests(unittest.TestCase):
    def test_frozen_H_invariance(self):
        a = Plate(18,.05,-.8).modes(2.,count=6)
        b = Plate(18,.05,.8).modes(2.,count=6)
        np.testing.assert_array_equal(a['omega'],b['omega'])

    def test_independent_classical_root_and_negative_power(self):
        p = Plate(18)
        m = p.modes(.01,count=6)
        root = independent_classical_root(.01,m['omega'][4])
        self.assertTrue(root['converged'])
        self.assertLess(root['relative_difference'],1e-9)
        dg = p.diagnostics(.01,m['omega'][4],m['U'][:,4],m['Phi'][:,4],m['N'][:,4])
        self.assertLess(dg['direct_power'],0.)
        self.assertLess(dg['strong_mechanical_relative'],1e-8)
        self.assertLess(dg['strong_gauss_relative'],1e-7)
        self.assertAlmostEqual(dg['energy_velocity'],m['group'][4],places=11)

    def test_exact_vacuum_is_not_local_Dn_zero(self):
        exact = Plate(18,vacuum=True).modes(.01,count=6)
        approx = Plate(18,vacuum=False).modes(.01,count=6)
        self.assertLess(exact['group'][4],0.)
        self.assertGreater(approx['group'][4],0.)

    def test_gradient_face_power_term_is_needed(self):
        p = Plate(24,.05,.8)
        m = p.modes(2.,'equilibrated',count=6)
        j = 4
        dg = p.diagnostics(2.,m['omega'][j],m['U'][:,j],m['Phi'][:,j],m['N'][:,j],'equilibrated')
        self.assertGreater(abs(dg['face_hyperstress_power_correction']),.01)
        self.assertAlmostEqual(dg['energy_velocity'],m['group'][j],places=10)
        incorrect = (dg['direct_power']-dg['face_hyperstress_power_correction'])/dg['mean_energy']
        self.assertGreater(abs(incorrect-m['group'][j]),1e-4)

    def test_finite_carrier_passivity_and_dissipation(self):
        p = Plate(28,.05,.8)
        m = p.dynamic_modes(2.)
        self.assertLess(np.max(m['all_s'].real),1e-7)
        dg = p.dynamic_diagnostics(2.,m,4)
        self.assertGreater(dg['energy'],0.)
        self.assertGreater(dg['dissipation'],0.)
        self.assertLess(dg['energy_decay_identity_relative'],1e-7)
        self.assertLess(dg['strong_mechanical_relative'],1e-6)
        self.assertLess(dg['strong_gauss_relative'],1e-7)
        self.assertLess(dg['traction_relative'],1e-7)
        self.assertLess(dg['double_traction_over_stress_d'],1e-8)
        self.assertLess(dg['vacuum_bc_relative'],1e-8)
        self.assertLess(dg['carrier_strong_relative'],1e-7)
        self.assertLess(dg['no_flux_boundary_relative'],1e-7)

    def test_mass_overlap_continuation(self):
        _, minmac = track_grid(Plate(16),np.linspace(.2,3.,31),count=6)
        self.assertGreater(minmac,.95)

    def test_audit_artifacts_preserve_evidence_gaps(self):
        path = Path(__file__).parent/'results'/'validation.json'
        if not path.exists(): self.skipTest('Run a0/run_checks.py to generate audit artifacts first.')
        audit=json.loads(path.read_text())
        self.assertEqual(audit['decision'],'REVISE')
        self.assertGreater(len(audit['unresolved']),0)
        self.assertTrue(audit['all_executed_checks_passed'])
        self.assertTrue(all(check['passed'] for check in audit['checks']))
        self.assertIn('NOT fixed-model feasibility',audit['candidate_classical_only']['qualification'])


if __name__=='__main__':
    unittest.main()
