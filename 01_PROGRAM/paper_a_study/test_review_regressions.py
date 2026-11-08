"""Regression tests for the independent review of the original archive (A01, A02, B01, B02)."""
import sys
import os
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_figure_data import KB0, KY0, K0, operating_mode, plate  # noqa: E402
from model import Plate, MeshPlate  # noqa: E402


class ReviewRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = plate(0.0)
        cls.mode = operating_mode(cls.p)
        cls.res, _ = cls.p.edge(KY0, cls.mode['omega'].real, K0, KB0)

    def test_A01_energy_identity_sign(self):
        r = self.res
        self.assertLess(abs(r['total_power_left'] - r['edge_power'] - r['dissipation_control_volume']),
                        1e-9 * r['incident_power_left'])
        wrong = abs(r['total_power_left'] - (r['edge_power'] - r['dissipation_control_volume']))
        self.assertGreater(wrong, 1e-4 * r['incident_power_left'])
        self.assertGreaterEqual(r['dissipation_control_volume'], 0.0)

    def test_A02_single_mode_flux_balance(self):
        w, _, _ = self.p.waves(KY0, self.mode['omega'].real)
        for a in w:
            if abs(a['K'] - K0) < 1e-6 or abs(a['K'] - KB0) < 0.3:
                d = self.p.mode_diagnostics(a['K'], KY0, self.mode['omega'].real, a['y'][:self.p.nw])
                self.assertLess(d['balance'], 1e-6)

    def test_B01_B02_open_circuit_full_basis_and_c1(self):
        sp = Plate(degree=14, H=0.0, electric='open')
        self.assertEqual(sp.np, sp.n)
        ms = MeshPlate(elements=8, H=0.0, electric='open')
        f_sp = operating_mode(sp)['omega'].real
        f_ms = operating_mode(ms)['omega'].real
        self.assertLess(abs(f_sp - f_ms) / f_sp, 1e-4)
        r_sp, _ = sp.edge(KY0, f_sp, K0, KB0)
        r_ms, _ = ms.edge(KY0, f_ms, K0, KB0)
        self.assertLess(abs(r_sp['backward_reflection_self_power'] - r_ms['backward_reflection_self_power']), 1e-9)
        self.assertLess(r_ms['power_balance_relative'], 1e-8)


class FigureDataRegressions(unittest.TestCase):
    """Figure-data consistency checks added after the figure audit."""

    @staticmethod
    def _rows(name):
        import csv
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figure_data", name)) as fh:
            return list(csv.DictReader(fh))

    def test_F01_group_equals_energy_speed(self):
        rows = [r for r in self._rows("fig01_dispersion_velocity_attenuation.csv")
                if float(r["eta"]) == 0.0]
        for r in rows:
            g, e = float(r["group_speed_m_s"]), float(r["energy_speed_m_s"])
            self.assertLess(abs(g - e), 1e-3 * max(abs(e), 1.0))

    def test_F02_fig04_group_speed_matches_fig01(self):
        f1 = {round(float(r["K"]), 4): float(r["group_speed_m_s"])
              for r in self._rows("fig01_dispersion_velocity_attenuation.csv")
              if float(r["eta"]) == 0.0}
        f4 = {round(float(r["K"]), 4): float(r["group_speed_m_s"])
              for r in self._rows("fig04_frequency_reflection.csv")
              if float(r["eta"]) == 0.0}
        common = sorted(set(f1) & set(f4))
        self.assertTrue(common)
        for k in common:
            self.assertLess(abs(f1[k] - f4[k]), 2e-3 * max(abs(f1[k]), 1.0))

    def test_F03_gradient_length_family_is_one_branch(self):
        import collections
        by = collections.defaultdict(dict)
        for r in self._rows("fig03_geometry_sweep.csv"):
            if r["parameter"] == "ell":
                by[round(float(r["K"]), 4)][float(r["value_nm"])] = float(r["frequency_GHz"])
        for k, v in by.items():
            ordered = [v[x] for x in sorted(v)]
            self.assertEqual(ordered, sorted(ordered), msg=f"not monotone in ell at K={k}")


if __name__ == '__main__':
    unittest.main()
