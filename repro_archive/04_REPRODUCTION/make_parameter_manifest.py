#!/usr/bin/env python3
"""Generate 09_ARCHIVE_METADATA/parameter_manifest.json from the files that hold the
values, plus the documented provenance of each one.

    python 04_REPRODUCTION/make_parameter_manifest.py

Nothing is typed in twice: values are read from
  * 01_PROGRAM/a0/materials.json                    (material constants + NOT_SOURCED list)
  * 01_PROGRAM/paper_a_study/reference_constants.json (frozen derived constants)
  * 03_DATA/figure_data/build_log.json              (build settings actually used)
  * 01_PROGRAM/paper_a_study/model.py               (Plate defaults, parsed from source)

The `source` field of each entry is one of
  "materials.json:<key>"      value comes from the cited ZnO material set
  "reference_constants.json"  frozen derived value, guarded by a test
  "model.py:Plate(default)"   code default, not a measured material constant
  "NOT_SOURCED"               a modelling choice; stated as such in the manuscript
  "derived:<formula>"         computed from other entries, formula given
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../04_REPRODUCTION
ARCHIVE = HERE.parent                           # unpacked archive root


def locate(*candidates: str) -> Path:
    """Find a file in either the archive layout or the source-repository layout."""
    for c in candidates:
        p = ARCHIVE / c
        if p.exists():
            return p
    # source repository: repro_archive/04_REPRODUCTION -> repo root
    repo = ARCHIVE.parent
    mapping = {"01_PROGRAM/a0/": "a0/",
               "01_PROGRAM/paper_a_study/figure_data/": "paper_a_study/figure_data/",
               "01_PROGRAM/paper_a_study/": "paper_a_study/",
               "03_DATA/figure_data/": "paper_a_study/figure_data/",
               "09_ARCHIVE_METADATA/": "repro_archive/09_ARCHIVE_METADATA/"}
    for c in candidates:
        for src, dst in mapping.items():
            if c.startswith(src):
                p = repo / (dst + c[len(src):])
                if p.exists():
                    return p
    raise FileNotFoundError(f"cannot locate any of {candidates} from {ARCHIVE}")


MAT = json.loads(locate("01_PROGRAM/a0/materials.json").read_text())
REF = json.loads(locate("01_PROGRAM/paper_a_study/reference_constants.json").read_text())
BLOG = json.loads(locate("03_DATA/figure_data/build_log.json").read_text())
SRC = locate("01_PROGRAM/paper_a_study/model.py").read_text()


def plate_defaults() -> dict:
    tree = ast.parse(SRC)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "__init__":
            args = node.args.args
            defs = node.args.defaults
            names = [a.arg for a in args[-len(defs):]]
            out = {}
            for n, d in zip(names, defs):
                try:
                    out[n] = ast.literal_eval(d)
                except Exception:                                   # noqa: BLE001
                    out[n] = ast.unparse(d)
            return out
    return {}


PD = plate_defaults()
SI = MAT["SI"]

E = []            # entries


def add(group, name, symbol, value, unit, source, status, note=""):
    E.append(dict(group=group, name=name, symbol=symbol, value=value, unit=unit,
                  source=source, status=status, note=note))


DOI = MAT["source"]["doi"]

# ---------------------------------------------------------------- material
for key, unit in (("c11", "Pa"), ("c12", "Pa"), ("c13", "Pa"), ("c33", "Pa"),
                  ("c44", "Pa"), ("c66", "Pa"), ("e15", "C/m^2"), ("e31", "C/m^2"),
                  ("e33", "C/m^2"), ("kappa11", "F/m"), ("kappa33", "F/m"),
                  ("rho", "kg/m^3")):
    add("material", key, key, SI[key], unit,
        f"materials.json:SI.{key}", "SOURCED", f"DOI {DOI}, Table 1")
for k in ("q", "kB", "epsilon0"):
    add("material", k, k, MAT["SI_definitions"][k],
        {"q": "C", "kB": "J/K", "epsilon0": "F/m"}[k],
        f"materials.json:SI_definitions.{k}", "SOURCED", "CODATA / SI definition")

# ---------------------------------------------------------------- geometry & design
add("geometry", "thickness", "d", PD.get("d"), "m", "model.py:Plate(default)",
    "NOT_SOURCED", "design value; the A0 study used 1 um as a reference thickness")
add("geometry", "gradient_length", "ell", PD.get("ell"), "m", "model.py:Plate(default)",
    "NOT_SOURCED", "no measured strain-gradient length for ZnO")
add("geometry", "reference_plane", "L", 10.0, "d", "model.py/build_figure_data.py:REF_NORM",
    "modelling choice", "L = 10 d = 2 um; both channels evaluated at the same plane")

# ---------------------------------------------------------------- transport
add("transport", "doping", "n0", PD.get("n0"), "m^-3", "model.py:Plate(default)",
    "NOT_SOURCED", "materials.json lists sample_doping as null; A0 scenario value was 1e19")
add("transport", "mobility", "mu_e", PD.get("mobility"), "m^2/(V s)",
    "model.py:Plate(default)", "NOT_SOURCED",
    "materials.json:SI.electron_mobility = 0.01 was the A0 feasibility value; the "
    "production plate uses 0.0175")
add("transport", "diffusivity", "D", PD.get("diffusivity"), "m^2/s",
    "model.py:Plate(default)", "NOT_SOURCED",
    "materials.json:SI.electron_diffusivity = 2.6e-4; D/mu_e = 0.026 V implies T = 301.72 K")
add("transport", "temperature", "T", 301.72, "K", "derived:D/(mu_e kB)",
    "DERIVED", "not an independent input; the Einstein relation fixes it")

# ---------------------------------------------------------------- coupling
add("coupling", "flexoelectric_f3zz", "f", PD.get("flexo"), "C/m",
    "model.py:Plate(default)", "NOT_SOURCED",
    "placeholder magnitude; -0.012 % effect at 1 nC/m, -1.176 % at 10 nC/m "
    "(figure_data/flexo_control.json)")
add("coupling", "carrier_gradient_H", "H", PD.get("H"), "J m",
    "model.py:Plate(default)", "NOT_SOURCED",
    "production value 0; sweeps at H = eta*H*, |eta| <= 0.05")
for key, unit, status in (("K0", "dimensionless", "frozen"),
                          ("KB0", "dimensionless", "frozen"),
                          ("KY0", "dimensionless", "frozen"),
                          ("OMEGA0", "dimensionless", "frozen"),
                          ("HCRIT", "J m", "frozen")):
    add("operating_point", key, key, REF["derived"][key], unit,
        "reference_constants.json:derived", status,
        "guarded by test_reference_values_are_frozen")

# ---------------------------------------------------------------- derived
add("derived", "schur_bound", "H_bound", REF["derived"]["HCRIT"] * 5 ** 0.5, "J m",
    "derived:ell*sqrt(a c*), c* = c33 - 2c13^2/(c11+c12)", "DERIVED",
    "H* = H_bound/sqrt(5) is the plotting normalisation (s = 0.2)")
add("derived", "shear_wave_speed", "c_s", (SI["c44"] / SI["rho"]) ** 0.5, "m/s",
    "derived:sqrt(c44/rho)", "DERIVED", "2746.6 m/s")
add("derived", "compressibility", "a", MAT["SI_definitions"]["kB"] * 301.72 / PD["n0"],
    "J m^3", "derived:kB*T/n0", "DERIVED", "")
add("derived", "debye_length", "L_D",
    (SI["kappa33"] * MAT["SI_definitions"]["kB"] * 301.72
     / MAT["SI_definitions"]["q"] ** 2 / PD["n0"]) ** 0.5, "m",
    "derived:sqrt(kappa33 kB T/(q^2 n0))", "DERIVED", "")
add("derived", "frequency_unit", "c_s/(2 pi d)", (SI["c44"] / SI["rho"]) ** 0.5
    / (2 * 3.141592653589793 * PD["d"]), "Hz", "derived:c_s/(2 pi d)", "DERIVED",
    "2.1857 GHz at d = 200 nm")

# ---------------------------------------------------------------- numerics
add("numerics", "polynomial_degree", "n-1", BLOG.get("degree", 22), "-",
    "figure_data/build_log.json", "setting", "production degree")
add("numerics", "quadrature_nodes", "nquad", BLOG.get("nquad", 64), "-",
    "model.py:Plate(max(64, 2 degree+10))", "setting", "")
add("numerics", "faces_electric", "-", "ground", "-", "model.py:Plate(electric=...)",
    "setting", "phi = 0 on z = +-d/2 (default)")
add("numerics", "edge_electric", "-", "insulating", "-",
    "model.py:Plate(edge_electric=...)", "setting",
    "D_x(0,z) = 0, the model of record since round 20; 'ground' only reproduces round 19")
add("numerics", "outgoing_cutoff", "tau", "2e-8*max(1,|k_x|)", "-",
    "model.py:Plate.edge", "setting", "")
add("numerics", "svd_rank_cutoff", "-", 1e-12, "relative", "model.py:Plate.edge",
    "setting", "rank deficiency raises RuntimeError instead of regularising")
add("numerics", "random_seed", "-", None, "-", "none used", "NOT APPLICABLE",
    "the production path is fully deterministic; there are no seeds")

# ---------------------------------------------------------------- uncertainty
add("uncertainty", "degree_spread_R_B", "-", 1.1047168215699311e-06, "relative",
    "figure_data/peak_search.json:degree_spread", "MEASURED", "degrees 14..34")
add("uncertainty", "quadrature_spread_R_B", "-", 1.698845860143633e-09, "relative",
    "figure_data/peak_search.json:quadrature_spread", "MEASURED", "64..256 nodes")
add("uncertainty", "restart_spread_R_B", "-", 3.2390049181652003e-06, "relative",
    "figure_data/peak_search.json:restart_spread", "MEASURED", "fixed-point restarts")
add("uncertainty", "experimental_uncertainty", "-", None, "-", "no measurement exists",
    "NOT AVAILABLE", "no measured f or H for this structure")
add("uncertainty", "fisher_information_CRLB", "-", None, "-", "not performed",
    "NOT AVAILABLE", "sensitivity is reported as finite-difference sweeps instead")

doc = dict(
    title="Paper A parameter manifest",
    generated_by="04_REPRODUCTION/make_parameter_manifest.py",
    principle=("Every value is read from a file in this archive.  Entries whose value "
               "is a modelling choice carry status NOT_SOURCED and the manuscript says so. "
               "No value was invented for this manifest."),
    material_set=dict(description=MAT["material"], citation=MAT["source"]),
    materials_json_not_sourced=MAT["NOT_SOURCED"],
    materials_json_choices=MAT["reference_and_synthetic_choices_NOT_measured_material_constants"],
    build_log=dict(degree=BLOG.get("degree"), nquad=BLOG.get("nquad"),
                   H_crit_T=BLOG.get("H_crit_T")),
    entries=E,
)
out = (ARCHIVE / "09_ARCHIVE_METADATA/parameter_manifest.json"
       if (ARCHIVE / "01_PROGRAM").is_dir()
       else Path(__file__).resolve().parent.parent / "09_ARCHIVE_METADATA/parameter_manifest.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(doc, indent=1, default=str) + "\n")
print(f"wrote {out}  ({len(E)} entries, {out.stat().st_size} bytes)")
for e in E[:6]:
    print(" ", e["group"], e["name"], e["value"], e["status"])
