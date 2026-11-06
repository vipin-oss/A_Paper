"""Build the two-page figure atlas (vector figures + reading notes).

The atlas embeds the delivered PDFs themselves -- not rasters -- so the page
keeps the exact vector content that the manuscript includes.  One atlas page
carries figures 1-5, the second carries 6-10, each with a short reading note
that states what the panel is allowed to claim.
"""

from __future__ import annotations

from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures_final"
OUT = HERE / "figure_atlas_two_page.pdf"

PAGE_W, PAGE_H = 1584.0, 1080.0          # 22 x 15 in landscape
MARGIN, HEADER = 26.0, 34.0
COLS, ROWS = 2, 3
CELL_W = (PAGE_W - 2 * MARGIN) / COLS
CELL_H = (PAGE_H - 2 * MARGIN - HEADER) / ROWS
FIG_FRAC = 0.70                          # share of the cell width used by the figure

NOTES = [
    ("fig01_dispersion", "Dispersion and wave speeds",
     "The five H/H* levels superimpose over the whole zone; the inset resolves "
     "the residual splitting (<60 kHz on a 16.7 GHz carrier). (b) uses the full "
     "wavevector for v_p, a numerical d(omega)/dk_x for v_g and an integrated "
     "Poynting/energy ratio for v_E; the three change sign near k_x d = 0.55, "
     "the backward-branch signature. Attenuation is 2|Im k_x|, never zero."),
    ("fig02_material", "Carrier density and mobility",
     "n_0 scales the linewidth and the attenuation but not the backward "
     "reflectance: (c) collapses five densities onto one R_B curve with a "
     "maximum of 58 % near k_x d = 0.55. Only certified rows are drawn, so the "
     "curves stop where the backward port collapses."),
    ("fig03_geometry", "Thickness versus gradient length",
     "Thickness sets the branch (17 GHz between 120 and 320 nm) while the "
     "gradient length perturbs it by at most 10 % and only at large k_x d. The "
     "two families are separated, as they must be, because they scale "
     "differently."),
    ("fig04_frequency", "Backward conversion on the guided branch",
     "All 50 branch-tracking rows are certified (0<=R_B<=1, |theta_E|<80 deg, "
     "balance<1e-6, edge residual<1e-8). Conversion peaks where v_g -> 0, so the "
     "effect is a slow-mode effect. Rows at |theta_E| -> 90 deg are not "
     "reflectances and are absent by construction."),
    ("fig05_channel", "Energy budget of the edge problem",
     "Incident power is normalised to one and split into a backward far field, "
     "dissipation and a reactive near field. The forward-propagating channel is "
     "exactly zero and is stated as such. The balance error stays at 1e-12 and "
     "the coupling moves R_B by at most 2.5 %."),
    ("fig06_attenuation", "Distance, survival and attenuation",
     "The backward coefficient decays with the observation distance and the "
     "survival factor never exceeds unity. Lengths and loss coefficients in "
     "(c)-(d) come from the solved complex spatial roots, alpha = 2|Im k|, and "
     "are positive everywhere."),
    ("fig07_coupling", "Coupling sensitivity in (k_y, H)",
     "The transverse wavenumber sets the level and the coupling shifts it by at "
     "most 2.5 %. Panel (b) draws the solved grid cell by cell: nothing outside "
     "the computational box is interpolated."),
    ("fig08_boundary", "Through-thickness flux distribution",
     "The x-component of the backward flux changes sign inside the plate while "
     "its thickness integral stays negative, and the z-component does not "
     "vanish at the free surfaces. That is why the reactive near field has to "
     "be carried in the budget rather than dropped."),
    ("fig09_validation", "Convergence and cross-checks",
     "Reflectance and backward wavenumber converge to the round-off floor by "
     "n = 26; residuals stay below 1e-8 and 1e-10. Panel (d) compares two "
     "solution routes for the same dispersion relation -- not two independent "
     "models -- and they agree to 2e-5."),
    ("fig10_field", "Solved field and flux directions",
     "Incident and backward intensity share one logarithmic scale. Every arrow "
     "in (c) is taken from the solved thickness-integrated flux: incidence at "
     "+10 deg, backward flux at -27.9 deg, both components negative."),
]

HEAD = ("Paper A -- figure atlas (1/2)", "Paper A -- figure atlas (2/2)")


def build() -> Path:
    doc = pymupdf.open()
    for page_index in range(2):
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        page.draw_rect(pymupdf.Rect(0, 0, PAGE_W, PAGE_H), color=None,
                       fill=(1, 1, 1))
        page.insert_text((MARGIN, MARGIN + 16), HEAD[page_index],
                         fontsize=15, fontname="Times-Bold", color=(0.07, 0.09, 0.13))
        page.insert_text((PAGE_W - 330, MARGIN + 16),
                         "Negative reflection of guided waves, flexoelectric "
                         "piezoelectric-semiconductor plate",
                         fontsize=7.5, fontname="Times-Roman", color=(0.35, 0.38, 0.42))
        for slot in range(5):
            idx = page_index * 5 + slot
            stem, title, note = NOTES[idx]
            col_i, row_i = slot % COLS, slot // COLS
            cx = MARGIN + col_i * CELL_W
            cy = MARGIN + HEADER + row_i * CELL_H
            cell = pymupdf.Rect(cx, cy, cx + CELL_W, cy + CELL_H)
            page.draw_rect(cell + (2, 2, -2, -2), color=(0.85, 0.87, 0.89),
                           width=0.6)
            fig_w = CELL_W * FIG_FRAC
            fig_h = fig_w * 5.10 / 6.50
            if fig_h > CELL_H - 46:
                fig_h = CELL_H - 46
                fig_w = fig_h * 6.50 / 5.10
            fx0 = cx + 10
            fy0 = cy + 24
            rect = pymupdf.Rect(fx0, fy0, fx0 + fig_w, fy0 + fig_h)
            src = pymupdf.open(FIG / f"{stem}.pdf")
            page.show_pdf_page(rect, src, 0)
            page.insert_text((cx + 10, cy + 15),
                             f"Figure {idx + 1}   {title}",
                             fontsize=11, fontname="Times-Bold",
                             color=(0.07, 0.09, 0.13))
            txt_x0 = fx0 + fig_w + 10
            txt = pymupdf.Rect(txt_x0, cy + 26, cx + CELL_W - 10, cy + CELL_H - 10)
            page.insert_textbox(txt, note, fontsize=8.6, fontname="Times-Roman",
                                color=(0.12, 0.14, 0.18), align=0, lineheight=1.35)
            page.insert_text((txt_x0, cy + CELL_H - 26),
                             f"source: {stem}.csv" if not stem.startswith("fig10")
                             else "source: fig10_field_maps.csv",
                             fontsize=6.5, fontname="Times-Italic",
                             color=(0.45, 0.47, 0.5))
    doc.save(OUT, deflate=True, garbage=4)
    doc.close()
    return OUT


if __name__ == "__main__":
    path = build()
    print(path, f"{path.stat().st_size / 1024:.0f} kB")
