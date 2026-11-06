"""Issue F (round 5): are the reported modal partitions sensitive to the corner?

The edge problem is solved in a spectral Galerkin basis through the thickness,
so the free edge meets the free faces at two corners (x=0, z=+-d/2).  A corner
singularity of the higher-order (strain-gradient) edge problem would show up as
(i) a strain-gradient energy density that concentrates without bound in the
outer band |z|>0.4 d/2 as the degree is raised, or (ii) a pointwise field that
grows with degree.  Both are measured here at the operating point and at the
zero-group-velocity peak, for degrees 18/22/26/30.

Case selection
--------------
The two cases are *incident* configurations and are identified by their
incident axial wavenumber:

    operating point   K0   = 0.7361990195318475  (build_figure_data.K0)
    peak              peak_candidate of certify_peak.CASES (k_x d = 0.55)

The backward-mode wavenumber KB0 = 0.2451746921716515 is *not* an incident
configuration; it is only the target guess handed to ``Plate.edge`` so that the
outgoing-mode search returns the backward branch.  Round 4 of this project used
KB0 as the operating-point incident guess and therefore solved and labelled a
different scattering experiment (R_B = 0.5444 instead of 0.0231).  Every row now
records the incident and backward wavenumbers actually returned by the solver,
asserts that the incident one is the intended one, and cross-checks the
operating-point rows against ``peak_certification.json`` at the same degree.

The density is the x=0 plane value of the strain-gradient energy density
lam^2 * sum_l (d eps/dx_l) : C : (d eps/dx_l), built from the *coherent sum* of
all outgoing modes plus the incident mode (interference retained).

Run:  python -m paper_a_study.corner_assessment      (or as a script)
Writes figure_data/corner_assessment.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_figure_data import KB0, K0, KY0, operating_mode, plate, track  # noqa: E402
from certify_peak import CASES as CERTIFIED_CASES  # noqa: E402

OUT = HERE / "figure_data" / "corner_assessment.json"
BAND = 0.40          # |z| > 0.40 d/2 ... faces are at +-0.5
DEGREES = (18, 22, 26, 30)

# Incident configurations.  K0 is the authoritative operating-point constant;
# the peak is taken from the certification suite so that no number is invented.
PEAK_K = float(dict(CERTIFIED_CASES)["peak_candidate"])
CASES = {"operating_point": float(K0), "peak": PEAK_K}


def gradient_energy(plate_, ky, res, scr):
    """Coherent strain-gradient energy density on the x=0 plane."""
    p = plate_
    Y, K, aa, inc = scr["Y"], scr["K"], scr["amplitudes"], scr["incident"]
    G = [np.zeros((len(p.z), 6), complex) for _ in range(3)]
    modes = [(1.0, inc["y"], inc["K"])] + [(aa[j], Y[:, j], K[j]) for j in range(len(K))]
    for amp, prof, Kj in modes:
        f = p.fields(Kj, ky, prof[:p.nw])
        G[0] += amp * 1j * Kj * f["strain"][0]
        G[1] += amp * 1j * ky * f["strain"][0]
        G[2] += amp * f["strain"][1]
    dens = np.zeros(len(p.z))
    for g in G:
        dens += np.einsum("qi,ij,qj->q", g.conj(), p.C, g).real
    dens *= p.lam ** 2
    w = p.weights
    total = float(np.sum(w * dens))
    band = np.abs(p.z) > BAND
    corner = float(np.sum(w[band] * dens[band]))
    share = corner / total if total > 0 else float("nan")
    peak_ratio = float(np.max(dens[band]) / (total / np.sum(w))) if band.any() else float("nan")
    return dict(total=total, corner_band=corner, corner_share=share,
                corner_peak_over_mean=peak_ratio,
                inner_share=1.0 - share)


def certification_reference():
    """degree -> R_B of the certified operating-point solve, if available."""
    path = HERE / "figure_data" / "peak_certification.json"
    if not path.exists():
        return {}
    ref = {}
    for row in json.loads(path.read_text()).get("rows", []):
        if abs(float(row.get("K", -1)) - float(K0)) < 1e-12 and row.get("status") == "solved":
            ref[int(row["degree"])] = float(row["R_B"])
    return ref


def main():
    ref = certification_reference()
    report = {
        "band": BAND,
        "note": "x=0 plane, coherent modal sum, lam^2|grad eps|_C^2",
        "incident_configurations": {k: v for k, v in CASES.items()},
        "backward_target_guess": float(KB0),
        "relation": ("operating_point uses K0 (incident); KB0 is only the backward "
                     "target guess and must never be used as an incident case"),
        "cases": {},
    }
    ok = True
    for name, K in CASES.items():
        rows = []
        for deg in DEGREES:
            p = plate(degree=deg)
            m = track(p, [K], operating_mode(p))[0]
            res, scr = p.edge(KY0, float(m["omega"].real), K, KB0)
            # Regression guard: the solver must have selected the intended
            # incident branch.  If this fails the whole case is mislabelled.
            got = complex(res["incident_K"])
            # The incident root is propagating but weakly attenuating, so only
            # its real part can be compared with the real input wavenumber.
            if abs(got.real - K) > 1e-6 * max(1.0, abs(K)):
                raise RuntimeError(
                    f"{name}: incident Re K {got.real:.9f} != requested {K:.9f} "
                    f"(an incident case must be an incident wavenumber, not the "
                    f"backward target {KB0:.9f})")
            g = gradient_energy(p, KY0, res, scr)
            row = dict(degree=deg, incident_K=float(got.real),
                       backward_K_real=float(complex(res["backward_K"]).real),
                       backward_K_imag=float(complex(res["backward_K"]).imag),
                       R_B=float(res["backward_reflection_self_power"]),
                       frequency_Hz=float(res["frequency_Hz"]),
                       edge_scaled_residual=float(res["edge_scaled_residual"]),
                       **g)
            if name == "operating_point" and deg in ref:
                row["R_B_certified"] = ref[deg]
                row["R_B_abs_diff"] = abs(row["R_B"] - ref[deg])
                if row["R_B_abs_diff"] > 1e-6 * abs(ref[deg]):
                    ok = False
            rows.append(row)
        rb = [r["R_B"] for r in rows]
        sh = [r["corner_share"] for r in rows]
        pk = [r["corner_peak_over_mean"] for r in rows]
        report["cases"][name] = dict(
            incident_K=K,
            rows=rows,
            R_B_spread_rel=float((max(rb) - min(rb)) / max(abs(np.mean(rb)), 1e-30)),
            corner_share_range=[float(min(sh)), float(max(sh))],
            corner_share_drift_rel=float((sh[-1] - sh[0]) / max(sh[0], 1e-30)),
            corner_peak_over_mean_range=[float(min(pk)), float(max(pk))],
            corner_peak_drift_rel=float((pk[-1] - pk[0]) / max(pk[0], 1e-30)))
    report["certification_cross_check"] = (
        "PASS" if ok else "FAIL - operating-point R_B disagrees with peak_certification.json")
    report["certification_reference_degrees"] = sorted(ref)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print("certification cross-check:", report["certification_cross_check"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
