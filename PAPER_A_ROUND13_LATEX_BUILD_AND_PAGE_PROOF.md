# Paper A — round 13: LaTeX build and page proof

## Build outcome

> ## **BUILD UNVERIFIED — no compiler execution possible.**
>
> No TeX engine exists in this environment, none can be installed through the routes
> available here, and no PDF is shipped, cited or implied. The manuscript has been
> validated statically; it has **not** been typeset, and no page has been inspected
> because no page exists.

This is the same outcome as rounds 11 and 12, arrived at again from scratch rather
than inherited. The attempts are recorded below so the conclusion can be audited.

---

## 1. What was tried

| # | command | output | reading |
|---|---|---|---|
| 1 | `command -v pdflatex` | not found (exit 127) | no engine |
| 2 | `command -v latexmk` | not found (exit 127) | no wrapper |
| 3 | `command -v xelatex` | not found (exit 127) | — |
| 4 | `command -v lualatex` | not found (exit 127) | — |
| 5 | `command -v tectonic` | not found (exit 127) | — |
| 6 | `command -v bibtex` | not found | the bibliography step could not run either |
| 7 | `which pdflatex latexmk xelatex lualatex tectonic tex` | no output | nothing on `PATH` |
| 8 | `ls /usr/share/texlive` | `No such file or directory` | no TeX tree, not even a partial one |
| 9 | `apt-get update` | `E: List directory /var/lib/apt/lists/partial is missing. - Acquire (13: Permission denied)` | the package index cannot even be fetched as this user; `sudo -n` works but the directory is absent and the fetch fails |
| 10 | `curl -sI https://deb.debian.org/debian/` | SSL connect error (rc 35), http_code `000` | the Debian mirror is outside this environment's network policy, so `apt-get install texlive-*` has no route even with elevated rights |
| 11 | `pip download --no-deps tectonic` | `No matching distribution found for tectonic` | no engine on PyPI under that name |
| 12 | `pip download --no-deps tectonic-bin` | no distribution | — |
| 13 | `pip download --no-deps pytexlive` | no distribution | — |
| 14 | `pip download --no-deps pylatex-tex` | no distribution | — |
| 15 | `pip download --no-deps latexmk` | downloads `latexmk-0.0.2.tar.gz`, **2 075 B** | inspected: a stub package (`src/latexmk/__init__.py`, `__main__.py`) that shells out to an external `latexmk`. No engine, no format files, no fonts, no `siunitx`. Installing it would add a command that fails on first use |
| 16 | `curl -s https://api.github.com/repos/tectonic-typesetting/tectonic/releases/latest` | `tectonic@0.17.0`, musl asset 10 151 914 B | metadata is reachable |
| 17 | `curl -sL -o tectonic.tar.gz .../tectonic-0.17.0-x86_64-unknown-linux-musl.tar.gz` | SSL connect error (rc 35) | the release-asset host is blocked as well, so even a static binary cannot be fetched |

**Why a binary alone would not have helped.** Tectonic bootstraps its package set
from a bundle server on first run; that host is no more reachable than the two above.
A TeX distribution here needs both an engine and a few hundred megabytes of packages,
and neither is obtainable.

Effort was capped deliberately: after attempt 17 the conclusion was fixed. No
infrastructure was changed and no source file was altered to fit a compiler that does
not exist.

---

## 2. What was verified instead

`Paper_A_Final_Submission/scripts/static_check.py`, run on the edited tree:

```
Paper A static validation
========================================

files checked: 8
labels: 104   references: 75
citation keys used: 13   bib entries: 13

PASS
```

| checked | result |
|---|---|
| files present and included | 8 (main + 7 sections) |
| environment balance, brace balance | PASS |
| labels defined / referenced | 104 defined, 75 referenced, no duplicate keys |
| citation keys vs `references.bib` | 13 : 13, no undefined key, no unused entry |
| float figures present | 10/10 `figures/fig0*.pdf` exist and are non-empty |
| `\cref` targets exist | PASS (a missing target is an error, not a warning) |
| approximate prose word count | 16 656 (including math tokens) |
| undefined-macro scan | none found |

Informational, not errors: 22 labels are defined and never `\cref`'d (section and
equation labels kept for navigation).

### Where the round-13 changes sit in that check

| change | static-check consequence |
|---|---|
| `results.tex` caption, two words | none; counts unchanged |
| `appendix_reproducibility.tex`, 47 → 52 (three places) | word count moves by a few tokens |
| fig10 PDF replaced, same name | figure-present check still passes; `MANIFEST.json` re-hashed |

---

## 3. What a build would still have to prove, and cannot be proved here

| page-proof item | status |
|---|---|
| title / author block, abstract, keywords | not inspectable |
| section hierarchy and numbering | source is consistent; numbering is a compiler's job |
| equation alignment, numbering, tag placement | not inspectable |
| undefined citations and references at typeset time | statically clean; the compiler is the final word |
| table widths, especially `tab:configurations` and `tab:controls` | not inspectable — the two widest tables are the likeliest source of overfull boxes |
| figure placement and float migration | not inspectable; ten `[htbp]` floats in a 22 mm-margin A4 layout will migrate |
| caption placement and spacing | not inspectable |
| font consistency (`lmodern`, `T1`) | declared; not rendered |
| SI units (`siunitx`) | **highest residual risk**: v2 and v3 differ in `\SI`/`\qty` handling, and several tables use `\si{}` inside `tabularx` cells |
| page breaks, orphan headings, excessive blank space | not inspectable |
| appendix structure | statically consistent |
| bibliography | `bibtex` unavailable; `references.bib` parses and all 13 keys match |
| overfull / underfull boxes | not inspectable; `\emergencystretch` is set for this reason and is not a guarantee |
| Figure 10(c) at print size | inspected as PNG at 400 dpi (§5 of the fig10 report); the vector PDF itself was not rasterised by a PDF engine |

**No page overview is delivered and no page numbers are quoted, because no PDF
exists.** A previous-round PDF is not presented as current.

---

## 4. The exact command the supervisor should run

```bash
cd Paper_A_Final_Submission
pdflatex -interaction=nonstopmode -halt-on-error main.tex   # 1: needs LaTeX
bibtex   main                                               # 2: needs BibTeX
pdflatex -interaction=nonstopmode -halt-on-error main.tex   # 3: resolve refs
pdflatex -interaction=nonstopmode -halt-on-error main.tex   # 4: settle floats
```

Notes for whoever runs it:

* The three-pass sequence is the documented one for this source; the second pass is
  what resolves `cleveref`'s names.
* Package requirements: `geometry`, `lmodern`, `amsmath`, `amssymb`, `mathtools`,
  `siunitx`, `graphicx`, `booktabs`, `tabularx`, `caption`, `subcaption`, `hyperref`,
  `cleveref` — all in TeX Live's `latex-recommended` set.
* `siunitx` v3 is what the source was written against; if the engine has v2, expect
  errors at `\qty`-style constructs and check the `\si{}` use in the tables first.
* If an overfull box appears, it will be in `tab:configurations` (nine columns) or
  `tab:controls` (six columns with superscripts) before anywhere else.

---

## 5. Status carried forward

`BUILD UNVERIFIED` is recorded in the supervisor handoff, in the readiness summary,
in `downloads/README.md` and in the package's `START_HERE.txt`. The distribution of
this project therefore ships LaTeX source, figures, data, scripts and every audit —
and no PDF.
