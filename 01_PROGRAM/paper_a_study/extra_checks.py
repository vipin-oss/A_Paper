"""Extra robustness checks: modal-classification tolerance and near-fold resolution."""
import json, sys, time
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_figure_data import KB0, KY0, operating_mode, plate, track

DEG = 22
def solve(K, tol=2e-8):
    p = plate(0.0, degree=DEG); p.modal_tol = tol
    mode = track(p, [K], operating_mode(p))[0]
    res, aux = p.edge(KY0, mode["omega"].real, K, KB0)
    q = aux["incident"]["q"]; ib = aux["index_backward"]
    qb = aux["Y"][:p.nw, ib]
    ov = abs(np.vdot(q, qb)) / (np.linalg.norm(q) * np.linalg.norm(qb))
    return dict(K=K, tol=tol, R_B=res["backward_reflection_self_power"], n_out=res["outgoing_modes"],
                Kinc=complex(res["incident_K"]), KB=complex(res["backward_K"]),
                sep=abs(res["incident_K"] - res["backward_K"]) / abs(res["incident_K"]),
                overlap=float(ov), cond=res["edge_condition"], resid=res["edge_scaled_residual"],
                balance=res["power_balance_relative"])
out = {"tolerance": [], "near_fold": []}
for K in (0.7361990195318475, 0.52719):
    for tol in (1e-9, 1e-8, 2e-8, 1e-7, 1e-6):
        t = time.time()
        try: r = solve(K, tol)
        except Exception as e: r = dict(K=K, tol=tol, error=str(e)[:80])
        out["tolerance"].append(r); print(r, round(time.time() - t, 1), flush=True)
for K in (0.5267, 0.5270, 0.52719, 0.5274, 0.5276):
    r = solve(K); out["near_fold"].append(r); print(r, flush=True)
def cl(o):
    if isinstance(o, complex): return [o.real, o.imag]
    raise TypeError
(HERE / "figure_data" / "extra_checks.json").write_text(json.dumps(out, default=cl, indent=1))
