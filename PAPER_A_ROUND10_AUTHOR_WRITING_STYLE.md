# Paper A — Round 10: the author's writing style, as evidenced

**Purpose.** A description of how the author writes, extracted from five papers carrying Vipin Gupta
as an author, and the rules that follow for the language of this manuscript.
**Evidence base:** the five papers and the read depths listed in
`PAPER_A_ROUND10_STYLE_AND_STRUCTURE_AUDIT.md`, section 2. Papers 1–5 below are those five; the
monoclinic interface paper was **not opened** and contributes nothing here.

This report describes habits. It does not import content: no equation, result, boundary condition or
physical explanation from any of these papers appears in this manuscript, and none is cited.

---

## 1. The five papers, in one line each

| # | paper | what it shows about the author's hand |
|---|---|---|
| 1 | Gupta, Barak & Ahmad, *Phys. Scr.* **99** (2024) 025515 — reflection of a quasi plasma wave in a photo-piezo semiconductor | the fullest sample: abstract, introduction, fundamental equations, formulation, limiting cases, nomenclature, results with per-parameter subsections |
| 2 | Gupta, Kumawat, Vishwakarma, Barak & Das, *Compos. Struct.* **359** (2025) 118997 — circumferential SH waves in a layered piezoelectric cylinder | single-paragraph abstract; introduction as a literature walk; contribution paragraph with bullet implications; geometry first, mathematics second |
| 3 | Gupta, Awwad, Ismail, Ahmad & Das, *Int. J. Numer. Methods Heat Fluid Flow* (2025) — piezo-semiconductor-void Rayleigh waves | structured Emerald abstract; nomenclature; introduction opening on what the material *is* |
| 4 | Aldandani, Das, Yadav, Yaylacı & Gupta, *Int. J. Numer. Methods Heat Fluid Flow* (2026) — KG nonlocal fractional piezo-thermo-electric semiconductor | same, with the "gap in the literature" sentence placed first, before the title matter of the abstract |
| 5 | Aldandani, Gupta, Yadav, Sur, Yaylacı & Das, *Sci. Rep.* **16** (2026) 28908 — porous piezo-thermoelectric Rayleigh waves | single-paragraph abstract of ~180 words; introduction built from named authorities, one per sentence |

---

## 2. Nine observable habits

**H1 — the abstract is a paragraph of findings, not of claims about the work.**
Paper 1: *"This article investigates the reflection of thermo-photo-piezo-elastic plane waves from a
homogeneous, orthotropic, and piezo semiconductor medium during the photo-thermal process. A novel
higher-order fractional dual-phase lag hyperbolic two-temperature model is employed to tackle this
study. The analytical solution to the problem in the xz plane reveals the existence of five
interconnected waves."* — system, model, then a result stated as a discovery ("reveals the existence
of"), then what was computed, then what it depends on. Paper 5 is the same shape in 180 words.
There is no sentence in any of the five that certifies, validates or delivers the work.

**H2 — keywords are six and are content words.** Paper 1: *fractional derivative, plasma wave,
semiconductor, hyperbolic two-temperature, photo-piezo-thermoelastic, dual-phase lag.* Paper 5:
*SDG7, Voids, Piezo-thermo-electric material, KG Nonlocal elasticity, Rayleigh type wave, Fractional
order derivative, Three-phase lag model.* The pattern is: material class, wave/process, the one
ingredient that distinguishes the model.

**H3 — the introduction walks the literature by author, in sentences that begin with the author.**
*"Biot was the first proponent of the classical thermoelastic (CT) model [4]."*
*"Lord and Shulman (L-S) [5]… introduced a relaxation time component into Fourier's law."*
*"Chen and his coworkers [9–11] have put forward a classical two-temperature (C2T) heat transfer
model…"* *"Nowacki¹⁸ established coupled thermal elastic diffusion equations."* One thread per
paragraph, each thread ending in what that thread established, never in what it failed to do.

**H4 — the gap is stated once, at the end of the walk, and it is a statement of absence, not of
fault.** *"In the existing literature, no comprehensive study has been conducted on the reflection of
photo-piezo-thermoelastic waves in a semiconductor material. The primary purpose of this manuscript
is to examine and assess the impact of…"* Compare the layered-cylinder paper: *"Despite extensive
research on wave propagation in various layered structures, this study introduces a novel combination
of…"* followed by what the combination buys, in bullets.

**H5 — equations arrive with a lead-in sentence that names their role.**
*"Following [19, 25], and [26], we can express the fundamental equations as"* … *"Equation (3.1), when
combined with equation (2.3), leads to the following motion equations:"* … *"The stresses and
dielectric displacement relations in the xz plane are given as:"* The mathematics is not announced,
it is introduced. Numbered equations are then referred to by number, repeatedly and locally.

**H6 — limiting cases get their own short subsection, listed as items.**
*"Without fractional derivative by setting α = 1, we can achieve various photo-piezo-thermoelastic
heat conduction models depending on the chosen values for the phase lags…"* followed by one line per
model, each with its citation. This is the habit that most cleanly separates the author's papers from
a specification document.

**H7 — results are discussed effect by effect, with the physical statement first and the number
second.** *"As the angle of incidence increases, there is a corresponding increase in the magnitude
of reflected plasma wave, thermal wave, transverse SV wave, and electric potential wave. This
increment slows down as the incidence angle approaches grazing incidence."* The paragraph then names
the panel: *"Figure 2(b) depicts that the magnitude experiences gradually decreases with increasing
incidence angle."* Panels are named as `figures 2(a)–(e)` and the sub-panel letter is used inside the
sentence, not only in the caption.

**H8 — parameter choices are justified in the text, with a citation, at the point of use.**
*"The choice of phase lags τ_T = 1 × 10⁻³, τ_q = 1 × 10⁻⁵ are made to meet the requirements outlined
by Quintanilla and Racke [37]…"* and *"The choice of the parameters for the higher-order derivatives
has been made based on the constraints specified by Chiriţă et al [38]…"* Numerical work is prefaced
by the material and the software: *"…have been calculated and graphically depicted using MATLAB
software."*

**H9 — captions describe the panel, in one or two sentences, and name the physical quantity.**
They do not carry file names, row counts, tolerances or script names, and they do not argue.

---

## 3. Register: what the author's prose is, and is not

| present in the corpus | absent from the corpus |
|---|---|
| named authorities with numbered citations | first-person claims about the article's own rigour |
| "the present model", "the current model", "this study", "the manuscript" | "certified", "admissible", "gate", "registry", "audit trail" |
| plain trend sentences ("increases", "slows down", "falls steeply") | hedge-on-hedge constructions ("it is not unreasonable to suppose") |
| occasional intensifiers, uneven polish | the connective padding of machine-written prose |
| limitations named in the discussion, in one place | limitations staged as objections to be rebutted |
| mathematical statements of validity (a positivity bound, a lag constraint) | statements of validity addressed to a referee ("the solver refuses to run outside it") |

The corpus is **not** uniformly elegant — it contains comma splices, missing articles and awkward
turns. Round 10 does not imitate defects: it imitates the *manner* (derivational, named, trend-first,
figure-anchored) while keeping the manuscript's existing grammatical standard. That is a deliberate
choice and is recorded here so that a later reader does not read polish as a change of authorship.

---

## 4. Rules adopted for this manuscript

1. **Abstract**: one paragraph, 180–220 words, order = system and model → what is solved → what is
   found → what it depends on → what is synthetic or open. Result literals retained.
2. **Keywords**: six, material class first, mechanism second, method last.
3. **Introduction**: five paragraph groups — phenomenon; the continuum formulation; the wave theory;
   the gap; this paper and its organisation. Named authorities. Gap stated once.
4. **Formulation**: every equation block gets a lead-in sentence naming its role; every later use
   refers back by `\eqref`/`\cref`; a short itemsed subsection for the limiting cases of the
   formulation (here: the classical, the strain-gradient and the no-carrier limits); dimensional and
   thermodynamic statements expressed as conditions on the model, not as corrections of other papers.
5. **Method**: derivational prose; the two solution routes described as two ways of solving one
   dispersion relation; software and testing moved to the appendix.
6. **Results**: each subsection opens with the physical statement, then the panel and the number.
   Panels named in-sentence. Tables introduced by a sentence that says what they are for.
7. **Captions**: quantity, panel, physical content, one clause of interpretation where needed. No
   file names, no row counts, no tolerances, no script names.
8. **Discussion**: mechanism → literature comparison → provenance → limitations (one subsection) →
   what follows. Affirmative voice; a negation only when the negation *is* the claim.
9. **Conclusions**: five to seven findings in the author's itemised form, each a physical result with
   the number inside it, then one horizon sentence. Precision statements folded into the finding.
10. **Vocabulary ban in the article**: *certified, certify, admissibility/admissible, gate, registry,
    audit, panel-source, script, CSV, pipeline, delivery, round, mutation, regression, stale,
    artefact, blunder, mislabelled.* The words stay in the private reports and in the code, where
    they belong.
11. **Connective budget**: at most one of *furthermore / moreover / notably / remarkably /
    importantly / significantly* in the whole manuscript, and none as a paragraph opener; and no
    uniform template imposed on the ten figure discussions — three of them are two paragraphs, four
    are one long paragraph and three are short, because the figures are not equally rich.
12. **Development history**: no sentence in the article refers to a previous version of the work, a
    prior script, a defect that was found, or a correction that was made. That material lives in
    `PAPER_A_CORRECTION_HISTORY.md`.
