#!/usr/bin/env bash
# Reproduce Paper A from scratch inside the unpacked archive.
#
#   bash 04_REPRODUCTION/repro_test.sh [--fast]
#
# --fast skips the two expensive audits (mechanism_controls, peak_search) via a
#        reduced battery; the full run is the default and is the one that
#        certifies the paper.
#
# Every step writes its log to 04_REPRODUCTION/logs/ and the script prints a
# PASS / PARTIAL / FAIL summary at the end.  Failures are never hidden: a
# non-zero exit of any step is reported with its log path.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOGS="$ROOT/04_REPRODUCTION/logs"
mkdir -p "$LOGS"
FAST=0
[ "${1:-}" = "--fast" ] && FAST=1

step () {                       # step <name> <dir> <command...>
  local name="$1"; shift
  local dir="$1"; shift
  local log="$LOGS/$(printf '%s' "$name" | tr ' /' '__').log"
  echo "== $name"
  ( cd "$dir" && "$@" ) >"$log" 2>&1
  local rc=$?
  if [ $rc -eq 0 ]; then
    echo "   PASS  (log: $log)"
  else
    echo "   FAIL rc=$rc  (log: $log)"
    FAILED+=("$name")
  fi
  return 0
}
declare -a FAILED=()

echo "archive root: $ROOT"
echo "python:       $(command -v python3)  $(python3 -V 2>&1)"

# ---------------------------------------------------------------- 1 environment
step "01_environment" "$ROOT" python3 -c "
import sys, numpy, scipy, matplotlib
print('python', sys.version.split()[0])
print('numpy', numpy.__version__); print('scipy', scipy.__version__)
print('matplotlib', matplotlib.__version__)"

step "02_model_import" "$ROOT/01_PROGRAM/paper_a_study" python3 -c "
import model
p = model.Plate(degree=22)
print('Q', p.Q); print('alpha', p.alpha); print('lambda', p.lam)
print('f', p.f); print('h', p.h); print('nquad', p.nquad)
assert abs(p.lam-0.25) < 1e-15 and p.nquad == 64"

# ---------------------------------------------------------------- 2 data
if [ $FAST -eq 1 ]; then
  echo "== 03_figure_data  (skipped, --fast)"
else
  step "03_figure_data" "$ROOT/01_PROGRAM/paper_a_study" python3 build_figure_data.py
fi

# ---------------------------------------------------------------- 3 figures
step "04_figures" "$ROOT/01_PROGRAM/paper_a_study" python3 generate_final_figures.py

# ---------------------------------------------------------------- 4 compare
step "05_compare_data" "$ROOT/04_REPRODUCTION" python3 compare_outputs.py

# ---------------------------------------------------------------- 5 tests
step "06_unit_tests" "$ROOT/01_PROGRAM" python3 -m unittest paper_a_study.test_model

# ---------------------------------------------------------------- 6 manuscript
step "07_static_check" "$ROOT/02_OVERLEAF" python3 scripts/static_check.py
if command -v pdflatex >/dev/null 2>&1; then
  step "08_pdflatex" "$ROOT/02_OVERLEAF" bash -c "pdflatex -interaction=nonstopmode main >/dev/null && bibtex main >/dev/null && pdflatex -interaction=nonstopmode main >/dev/null && pdflatex -interaction=nonstopmode main"
else
  echo "== 08_pdflatex"
  echo "   SKIP  no TeX engine on this machine; the manuscript is validated statically only"
fi

# ---------------------------------------------------------------- 7 battery
# The battery was written for the source repository layout: it looks for a
# sibling Paper_A_Final_Submission/ next to paper_a_study/.  The archive keeps
# the manuscript in 02_OVERLEAF, so a symlink-only shim re-creates the layout.
if [ $FAST -eq 1 ]; then
  echo "== 09_battery  (skipped, --fast)"
else
  step "09_layout_shim" "$ROOT/01_PROGRAM" python3 prepare_archive_layout.py
  step "10_battery" "$ROOT/01_PROGRAM" python3 paper_a_study/run_all_checks.py
fi

# ---------------------------------------------------------------- summary
echo
echo "================ SUMMARY ================"
if [ ${#FAILED[@]} -eq 0 ]; then
  echo "PASS: every executed step succeeded."
else
  echo "PARTIAL/FAIL: ${#FAILED[@]} step(s) failed:"
  for f in "${FAILED[@]}"; do echo "  - $f  (see $LOGS/$(printf '%s' "$f" | tr ' /' '__').log)"; done
fi
echo "logs: $LOGS"
