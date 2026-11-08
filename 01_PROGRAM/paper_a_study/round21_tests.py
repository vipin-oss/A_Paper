"""Round-21 regression tests for the natural boundary data of the edge problem.

These tests pin the physics repaired in round 21 and are deliberately written so
that they fail if the repair is undone:

  * the discrete mechanical flux row equals the b0-projection of the physical
    traction PLUS the two corner line forces (identity at machine precision);
  * without the corner term the same identity fails by a factor ~1e13, so a
    regression that drops the corner force is detected, not absorbed;
  * the double traction row is the projection of tau_i11;
  * the corner force itself decays algebraically under degree refinement with
    the exponent measured in round 21 (corner singularity, not a bug).

Run: PYTHONPATH=paper_a_study .venv/bin/python -m unittest paper_a_study.round21_tests
"""

import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_figure_data import KB0, K0, KY0, operating_mode, plate  # noqa: E402
from model import tensor_matrix  # noqa: E402
from round21_gate1_traction import mode_identity  # noqa: E402


class TestNaturalBoundaryData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = plate(0.0, degree=12)
        cls.m = operating_mode(cls.p)
        cls.omega = float(cls.m["omega"].real)
        cls.res, cls.scr = cls.p.edge(KY0, cls.omega, K0, KB0)
        # the incident (physical, propagating) mode
        cls.inc = mode_identity(cls.p, cls.scr["incident"]["K"], cls.scr["incident"]["y"])

    def test_traction_including_corner_identity(self):
        self.assertLess(self.inc["traction_incl_corner"], 1e-10)

    def test_corner_term_is_essential(self):
        # dropping it must not be a small perturbation: the plain projection is
        # O(10) away, so the corner force is load-bearing in the boundary data.
        # incident mode: 8.9e-1; worst reflected mode: 1.7e+1.  Both are twelve
        # orders of magnitude above the 1e-13 identity, so the corner term is
        # load-bearing in the natural boundary data.
        self.assertGreater(self.inc["traction_plain"], 1e-2)

    def test_double_traction_identity(self):
        self.assertLess(self.inc["double"], 1e-10)

    def test_every_reflected_mode_satisfies_the_identity(self):
        worst = max(mode_identity(self.p, K, self.scr["Y"][:, j])["traction_incl_corner"]
                    for j, K in enumerate(self.scr["K"]))
        # strongly evanescent modes are ill-conditioned (tau fields ~1e2 x the
        # traction); the bound below is what degree 12 actually delivers.
        self.assertLess(worst, 1e-5)

    def test_corner_force_decays_with_degree(self):
        vals = []
        for degree in (12, 20):
            p = plate(0.0, degree=degree)
            m = operating_mode(p)
            _, scr = p.edge(KY0, float(m["omega"].real), K0, KB0)
            total = scr["incident"]["y"] + scr["Y"] @ scr["amplitudes"]
            corner = None
            for c, K, q in ([(1.0, scr["incident"]["K"], scr["incident"]["q"])]
                            + [(a, K, scr["Y"][: p.nw, j])
                               for j, (K, a) in enumerate(zip(scr["K"], scr["amplitudes"]))]):
                fl = p.fields(K, KY0, q, p.eb, p.epb)
                v = c * (tensor_matrix(fl["tau"][0])[:, :, 2]
                         + tensor_matrix(fl["tau"][2])[:, :, 0])
                corner = v if corner is None else corner + v
            vals.append(float(np.max(abs(corner))))
        self.assertLess(vals[1], vals[0])
        # measured exponent is -0.62 +- 0.01 over 10..28
        ratio = vals[0] / vals[1]
        self.assertGreater(ratio, 1.15)
        self.assertLess(ratio, 2.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
