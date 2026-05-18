# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 13: Rekupera\u010dn\u00ed v\u00fdm\u011bn\u00edky tepla. Rovnice tepeln\u00e9 bilance
a sd\u00edlen\u00ed tepla. Ur\u010den\u00ed st\u0159edn\u00edho logaritmick\u00e9ho rozd\u00edlu teplot
a velikosti teplosm\u011bnn\u00e9 plochy.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docx_engine import (
    create_document, save_and_export, add_heading, add_para,
    add_equation, add_bullet, add_image, add_info_box,
    add_warning_box, add_page_break, add_styled_table,
    add_exam_questions, COLORS, IMG_DIR,
)


# ======================================================================
# GRAFY
# ======================================================================

def generate_counterflow_vs_parallel():
    """Temperature profiles for parallel flow and counterflow heat exchangers."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    L = np.linspace(0, 1, 100)

    # Parallel flow (souproud)
    T_h1, T_h2 = 150, 70
    T_c1, T_c2 = 20, 60
    # Exponential profiles
    T_h_par = T_h1 - (T_h1 - T_h2) * (1 - np.exp(-3 * L)) / (1 - np.exp(-3))
    T_c_par = T_c1 + (T_c2 - T_c1) * (1 - np.exp(-3 * L)) / (1 - np.exp(-3))

    ax1.plot(L, T_h_par, color=COLORS[1], linewidth=2.5, label="Hork\u00e1 tekutina $T_h$")
    ax1.plot(L, T_c_par, color=COLORS[0], linewidth=2.5, label="Studen\u00e1 tekutina $T_c$")
    ax1.fill_between(L, T_h_par, T_c_par, alpha=0.08, color="#D97706")

    # Delta T markers
    ax1.annotate("", xy=(0, T_c1), xytext=(0, T_h1),
                arrowprops=dict(arrowstyle="<->", color="#D97706", lw=1.5))
    ax1.text(-0.06, (T_h1 + T_c1) / 2, "$\\Delta T_1$", fontsize=10, color="#D97706",
             fontweight="bold", ha="right")
    ax1.annotate("", xy=(1, T_c2), xytext=(1, T_h2),
                arrowprops=dict(arrowstyle="<->", color="#D97706", lw=1.5))
    ax1.text(1.06, (T_h2 + T_c2) / 2, "$\\Delta T_2$", fontsize=10, color="#D97706",
             fontweight="bold")

    # Flow direction arrows
    ax1.annotate("", xy=(0.9, T_h1 + 5), xytext=(0.1, T_h1 + 5),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=2))
    ax1.annotate("", xy=(0.9, T_c1 - 5), xytext=(0.1, T_c1 - 5),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=2))

    ax1.set_xlabel("Poloha pod\u00e9l v\u00fdm\u011bn\u00edku", fontsize=11)
    ax1.set_ylabel("Teplota T [\u00b0C]", fontsize=11)
    ax1.set_title("SOUPROUD (parallel flow)", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=9)
    ax1.set_ylim(0, 170)

    # Counterflow (protiproud)
    T_h1_c, T_h2_c = 150, 50
    T_c1_c, T_c2_c = 20, 120  # cold IN at x=1, OUT at x=0
    T_h_cnt = T_h1_c - (T_h1_c - T_h2_c) * L
    T_c_cnt = T_c2_c - (T_c2_c - T_c1_c) * L  # cold flows opposite

    ax2.plot(L, T_h_cnt, color=COLORS[1], linewidth=2.5, label="Hork\u00e1 tekutina $T_h$")
    ax2.plot(L, T_c_cnt, color=COLORS[0], linewidth=2.5, label="Studen\u00e1 tekutina $T_c$")
    ax2.fill_between(L, T_h_cnt, T_c_cnt, alpha=0.08, color="#D97706")

    # Delta T markers
    ax2.annotate("", xy=(0, T_c2_c), xytext=(0, T_h1_c),
                arrowprops=dict(arrowstyle="<->", color="#D97706", lw=1.5))
    ax2.text(-0.06, (T_h1_c + T_c2_c) / 2, "$\\Delta T_1$", fontsize=10, color="#D97706",
             fontweight="bold", ha="right")
    ax2.annotate("", xy=(1, T_c1_c), xytext=(1, T_h2_c),
                arrowprops=dict(arrowstyle="<->", color="#D97706", lw=1.5))
    ax2.text(1.06, (T_h2_c + T_c1_c) / 2, "$\\Delta T_2$", fontsize=10, color="#D97706",
             fontweight="bold")

    # Flow direction arrows (opposite)
    ax2.annotate("", xy=(0.9, T_h1_c + 5), xytext=(0.1, T_h1_c + 5),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=2))
    ax2.annotate("", xy=(0.1, T_c1_c - 5), xytext=(0.9, T_c1_c - 5),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=2))

    ax2.set_xlabel("Poloha pod\u00e9l v\u00fdm\u011bn\u00edku", fontsize=11)
    ax2.set_ylabel("Teplota T [\u00b0C]", fontsize=11)
    ax2.set_title("PROTIPROUD (counterflow)", fontsize=12, fontweight="bold")
    ax2.legend(fontsize=9)
    ax2.set_ylim(0, 170)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q13_flow_types.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_lmtd_visualization():
    """Visualization of LMTD vs arithmetic mean."""
    fig, ax = plt.subplots(figsize=(7, 5))

    dT1 = 100
    dT2 = 20

    # LMTD
    lmtd = (dT1 - dT2) / np.log(dT1 / dT2)
    arith = (dT1 + dT2) / 2

    L = np.linspace(0, 1, 100)
    dT = dT1 * np.exp(-np.log(dT1 / dT2) * L)  # exponential decay of delta T

    ax.plot(L, dT, color=COLORS[0], linewidth=2.5, label="$\\Delta T(x)$ skute\u010dn\u00fd pr\u016fb\u011bh")
    ax.axhline(y=lmtd, color=COLORS[2], linewidth=2, linestyle="--",
               label=f"LMTD = {lmtd:.1f} \u00b0C")
    ax.axhline(y=arith, color=COLORS[1], linewidth=1.5, linestyle=":",
               label=f"Aritmetick\u00fd pr\u016fm\u011br = {arith:.1f} \u00b0C")

    ax.fill_between(L, 0, dT, alpha=0.08, color=COLORS[0])

    ax.text(0.02, dT1 + 3, f"$\\Delta T_1$ = {dT1} \u00b0C", fontsize=10, color="#555")
    ax.text(0.85, dT2 + 3, f"$\\Delta T_2$ = {dT2} \u00b0C", fontsize=10, color="#555")

    ax.set_xlabel("Poloha pod\u00e9l v\u00fdm\u011bn\u00edku", fontsize=11)
    ax.set_ylabel("Teplotn\u00ed rozd\u00edl $\\Delta T$ [\u00b0C]", fontsize=11)
    ax.set_title("LMTD vs. aritmetick\u00fd pr\u016fm\u011br teplotn\u00edho rozd\u00edlu",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 120)
    ax.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q13_lmtd.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_exchanger_schema():
    """Schematic of shell-and-tube heat exchanger."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(-1, 12)
    ax.set_ylim(-1, 4)
    ax.axis("off")

    # Shell
    shell = Rectangle((1, 0.5), 9, 2.5, facecolor="#F3F4F6", edgecolor="black", lw=2,
                       joinstyle="round")
    ax.add_patch(shell)
    ax.text(5.5, 2.7, "PL\u00c1\u0160\u0164 (shell)", fontsize=10, ha="center", fontweight="bold", color="#555")

    # Tubes (simplified as lines)
    for y in [1.2, 1.75, 2.3]:
        ax.plot([1.3, 9.7], [y, y], color=COLORS[1], linewidth=3, alpha=0.7)

    # Hot fluid (in tubes)
    ax.annotate("", xy=(9.5, 1.75), xytext=(1.5, 1.75),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=2))
    ax.text(0.2, 1.75, "Hork\u00e1\ntekutina\n(trubky)", fontsize=8, ha="center", va="center",
            color=COLORS[1], fontweight="bold")
    ax.text(11, 1.75, "$T_{h,out}$", fontsize=10, ha="center", va="center",
            color=COLORS[1], fontweight="bold")

    # Cold fluid (in shell)
    ax.annotate("", xy=(1.5, 0.8), xytext=(9.5, 0.8),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=2))
    ax.text(5.5, 0.3, "Studen\u00e1 tekutina (pl\u00e1\u0161\u0165) \u2014 protiproud", fontsize=8,
            ha="center", color=COLORS[0], fontweight="bold")

    ax.set_title("Sch\u00e9ma trubkov\u00e9ho v\u00fdm\u011bn\u00edku (shell-and-tube)",
                 fontsize=12, fontweight="bold")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q13_exchanger.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH DOKUMENTU
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_flows = generate_counterflow_vs_parallel()
    img_lmtd = generate_lmtd_visualization()
    img_schema = generate_exchanger_schema()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="13. Rekupera\u010dn\u00ed v\u00fdm\u011bn\u00edky tepla. Rovnice tepeln\u00e9 bilance a sd\u00edlen\u00ed tepla.\n"
              "      Ur\u010den\u00ed st\u0159edn\u00edho logaritmick\u00e9ho rozd\u00edlu teplot a velikosti\n"
              "      teplosm\u011bnn\u00e9 plochy.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Vysv\u011btlete princip rekupera\u010dn\u00edch v\u00fdm\u011bn\u00edk\u016f tepla. Uve\u010fte rovnice tepeln\u00e9 bilance "
        "a sd\u00edlen\u00ed tepla. Odvo\u010fte st\u0159edn\u00ed logaritmick\u00fd teplotn\u00ed rozd\u00edl (LMTD) "
        "a vysv\u011btlete jeho pou\u017eit\u00ed pro n\u00e1vrh teplosm\u011bnn\u00e9 plochy.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Rekupera\u010dn\u00ed v\u00fdm\u011bn\u00edky tepla", level=3)

    add_info_box(doc,
        "Definice: Rekupera\u010dn\u00ed v\u00fdm\u011bn\u00edk",
        "Za\u0159\u00edzen\u00ed, ve kter\u00e9m se teplo p\u0159en\u00e1\u0161\u00ed z hork\u00e9 tekutiny na studenou "
        "p\u0159es pevnou st\u011bnu (teplosm\u011bnnou plochu). Tekutiny se nem\u00eds\u00ed \u2014 na rozd\u00edl "
        "od sm\u011b\u0161ovac\u00edch v\u00fdm\u011bn\u00edk\u016f.")

    add_image(doc, img_schema, width_cm=14,
              caption="Obr. 1: Sch\u00e9ma trubkov\u00e9ho v\u00fdm\u011bn\u00edku tepla (shell-and-tube)")

    add_para(doc, "Z\u00e1kladn\u00ed uspo\u0159\u00e1d\u00e1n\u00ed tok\u016f:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["Uspo\u0159\u00e1d\u00e1n\u00ed", "Popis", "V\u00fdhody"],
        data=[
            ["Souproud", "Ob\u011b tekutiny t\u00fdm\u017e sm\u011brem", "Rovnom\u011brn\u011bj\u0161\u00ed st\u011bny, lep\u0161\u00ed pro visk\u00f3zn\u00ed tekutiny"],
            ["Protiproud", "Tekutiny proti sob\u011b", "Nejvy\u0161\u0161\u00ed \u00fa\u010dinnost, T_c,out m\u016f\u017ee p\u0159ekro\u010dit T_h,out"],
            ["K\u0159\u00ed\u017eov\u00fd proud", "Tekutiny kolmo na sebe", "Kompaktn\u00ed konstrukce (nap\u0159. autochladiče)"],
        ],
    )

    # -- 1.2 Bilancni rovnice --
    add_page_break(doc)
    add_heading(doc, "1.2 Rovnice tepeln\u00e9 bilance", level=3)

    add_para(doc,
        "P\u0159i stacion\u00e1rn\u00edm provozu bez tepeln\u00fdch ztr\u00e1t plat\u00ed: "
        "teplo odebran\u00e9 hork\u00e9 tekutin\u011b = teplo p\u0159ijat\u00e9 studenou:", keep_with_next=True)
    add_equation(doc, r"\dot{Q} = \dot{m}_h c_{p,h} (T_{h,in} - T_{h,out}) = \dot{m}_c c_{p,c} (T_{c,out} - T_{c,in})", label="1")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "m\u0307_h, m\u0307_c \u2014 hmotnostn\u00ed pr\u016ftoky hork\u00e9 a studen\u00e9 tekutiny [kg/s]")
    add_bullet(doc, "c_{p,h}, c_{p,c} \u2014 m\u011brn\u00e9 tepeln\u00e9 kapacity [J/(kg\u00b7K)]")
    add_bullet(doc, "Sou\u010din m\u0307\u00b7c_p se naz\u00fdv\u00e1 teplotn\u00ed v\u00fdkon (water equivalent) C [W/K]", is_last=True)

    add_equation(doc, r"C_h = \dot{m}_h c_{p,h}, \quad C_c = \dot{m}_c c_{p,c}", label="2")

    # -- 1.3 Rovnice sdileni tepla --
    add_heading(doc, "1.3 Rovnice sd\u00edlen\u00ed tepla", level=3)

    add_para(doc, "Tepeln\u00fd tok p\u0159es teplosm\u011bnnou plochu:", keep_with_next=True)
    add_equation(doc, r"\dot{Q} = k A \Delta T_{str}", label="3")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "k \u2014 sou\u010dinitel prostupu tepla [W/(m\u00b2\u00b7K)]")
    add_bullet(doc, "A \u2014 teplosm\u011bnn\u00e1 plocha [m\u00b2]")
    add_bullet(doc, "\u0394T_str \u2014 st\u0159edn\u00ed teplotn\u00ed rozd\u00edl mezi tekutinami [\u00b0C]", is_last=True)

    add_warning_box(doc,
        "\u0394T se m\u011bn\u00ed pod\u00e9l v\u00fdm\u011bn\u00edku! Nelze pou\u017e\u00edt prost\u00fd aritmetick\u00fd pr\u016fm\u011br. "
        "Spr\u00e1vn\u00fd st\u0159edn\u00ed teplotn\u00ed rozd\u00edl je logaritmick\u00fd \u2014 LMTD.")

    # -- 1.4 LMTD --
    add_page_break(doc)
    add_heading(doc, "1.4 St\u0159edn\u00ed logaritmick\u00fd teplotn\u00ed rozd\u00edl (LMTD)", level=3)

    add_info_box(doc,
        "LMTD (Log Mean Temperature Difference)",
        "Skute\u010dn\u00fd st\u0159edn\u00ed teplotn\u00ed rozd\u00edl zohled\u0148uj\u00edc\u00ed exponenci\u00e1ln\u00ed pokles \u0394T "
        "pod\u00e9l v\u00fdm\u011bn\u00edku. Je v\u017edy men\u0161\u00ed ne\u017e aritmetick\u00fd pr\u016fm\u011br.")

    add_equation(doc, r"\Delta T_{LMTD} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}", label="4")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "\u0394T\u2081 \u2014 teplotn\u00ed rozd\u00edl na jednom konci v\u00fdm\u011bn\u00edku")
    add_bullet(doc, "\u0394T\u2082 \u2014 teplotn\u00ed rozd\u00edl na druh\u00e9m konci v\u00fdm\u011bn\u00edku", is_last=True)

    add_para(doc, "Definice \u0394T\u2081 a \u0394T\u2082:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["", "Souproud", "Protiproud"],
        data=[
            ["\u0394T\u2081", "T_{h,in} \u2212 T_{c,in}", "T_{h,in} \u2212 T_{c,out}"],
            ["\u0394T\u2082", "T_{h,out} \u2212 T_{c,out}", "T_{h,out} \u2212 T_{c,in}"],
        ],
    )

    add_para(doc, "Speci\u00e1ln\u00ed p\u0159\u00edpad: pokud \u0394T\u2081 = \u0394T\u2082, pak LMTD = \u0394T\u2081 = \u0394T\u2082 "
             "(l'H\u00f4pitalovo pravidlo).")

    add_image(doc, img_lmtd, width_cm=13,
              caption="Obr. 2: LMTD vs. aritmetick\u00fd pr\u016fm\u011br \u2014 LMTD je v\u017edy men\u0161\u00ed")

    add_image(doc, img_flows, width_cm=14,
              caption="Obr. 3: Teplotn\u00ed profily souproud\u00e9ho a protiproud\u00e9ho v\u00fdm\u011bn\u00edku")

    # -- 1.5 Navrh plochy --
    add_page_break(doc)
    add_heading(doc, "1.5 N\u00e1vrh teplosm\u011bnn\u00e9 plochy", level=3)

    add_para(doc, "Z rovnic (1) a (3) vypl\u00fdv\u00e1 n\u00e1vrhov\u00e1 rovnice:", keep_with_next=True)
    add_equation(doc, r"A = \frac{\dot{Q}}{k \cdot \Delta T_{LMTD}}", label="5")

    add_para(doc, "Postup n\u00e1vrhu:", bold=True, keep_with_next=True)
    add_bullet(doc, "1. Z bilance (rovnice 1) ur\u010d\u00edt Q\u0307 a nezn\u00e1m\u00e9 teploty")
    add_bullet(doc, "2. Spo\u010d\u00edtat LMTD (rovnice 4)")
    add_bullet(doc, "3. Ur\u010dit k (z sou\u010dinitel\u016f p\u0159estupu \u03b1\u2081, \u03b1\u2082 a veden\u00ed st\u011bnou)")
    add_bullet(doc, "4. Vypo\u010d\u00edtat pot\u0159ebnou plochu A (rovnice 5)", is_last=True)

    add_para(doc, "Pro k\u0159\u00ed\u017eov\u00fd proud a v\u00edcetahov\u00e9 uspo\u0159\u00e1d\u00e1n\u00ed se LMTD koriguje:", keep_with_next=True)
    add_equation(doc, r"\Delta T_{str} = F \cdot \Delta T_{LMTD,protiproud}", label="6")

    add_para(doc,
        "kde F \u2264 1 je korek\u010dn\u00ed faktor z\u00e1visl\u00fd na uspo\u0159\u00e1d\u00e1n\u00ed tok\u016f a teplotn\u00edch "
        "pom\u011brech (odečítá se z graf\u016f nebo tabulek).")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Typy rekupera\u010dn\u00edch v\u00fdm\u011bn\u00edk\u016f", level=3)
    add_styled_table(doc,
        headers=["Typ", "Popis", "Typick\u00e9 pou\u017eit\u00ed"],
        data=[
            ["Trubkov\u00fd (shell-and-tube)", "Svazek trubek v pl\u00e1\u0161ti", "Elektr\u00e1rny, rafinerie, chemie"],
            ["Deskov\u00fd", "Profil. desky s t\u011bsn\u011bn\u00edm/sv\u00e1\u0159en\u00edm", "HVAC, potravin\u00e1\u0159stv\u00ed, farmaci"],
            ["Trubka v trubce", "Souos\u00e9 trubky", "Laborato\u0159, mal\u00e9 v\u00fdkony"],
            ["\u017debrovan\u00fd", "Trubky s \u017eebry (fins)", "Autochladiče, ohř\u00edva\u010de vzduchu"],
            ["Spiral\u00e1ln\u00ed", "Spir\u00e1lovit\u011b vinut\u00e9 kan\u00e1ly", "Visk\u00f3zn\u00ed tekutiny, kaly"],
        ],
    )

    add_heading(doc, "2.2 Typick\u00e9 hodnoty k", level=3)
    add_styled_table(doc,
        headers=["Kombinace tekutin", "k [W/(m\u00b2\u00b7K)]"],
        data=[
            ["Voda \u2014 voda", "800\u20132 500"],
            ["P\u00e1ra \u2014 voda (kondenz\u00e1tor)", "1 500\u20134 000"],
            ["Voda \u2014 vzduch", "25\u201350"],
            ["Vzduch \u2014 vzduch", "10\u201335"],
            ["Olej \u2014 voda", "100\u2013350"],
        ],
    )

    add_heading(doc, "2.3 Zanášen\u00ed (fouling)", level=3)
    add_para(doc,
        "V provozu se na teplosm\u011bnn\u00fdch ploch\u00e1ch usazuj\u00ed n\u00e1nosy (vodní k\u00e1men, koroze, "
        "biologick\u00fd film), kter\u00e9 zvy\u0161uj\u00ed tepeln\u00fd odpor. P\u0159i n\u00e1vrhu se p\u0159id\u00e1v\u00e1 "
        "zane\u0161ovac\u00ed odpor R_f [m\u00b2\u00b7K/W] na ob\u011b strany:")
    add_equation(doc, r"\frac{1}{k_{dirty}} = \frac{1}{k_{clean}} + R_{f,h} + R_{f,c}", label="7")

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: N\u00e1vrh protiproud\u00e9ho v\u00fdm\u011bn\u00edku", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Protiproud\u00fd v\u00fdm\u011bn\u00edk ohř\u00edv\u00e1 vodu z 20 \u00b0C na 80 \u00b0C "
        "pomoc\u00ed hork\u00e9 vody (T_{h,in} = 150 \u00b0C, T_{h,out} = 90 \u00b0C). "
        "Pr\u016ftok studen\u00e9 vody: m\u0307_c = 2 kg/s, c_p = 4180 J/(kg\u00b7K). "
        "k = 1200 W/(m\u00b2\u00b7K). Ur\u010dete pot\u0159ebnou teplosm\u011bnnou plochu.", bold=True)

    add_para(doc, "Krok 1: Tepeln\u00fd v\u00fdkon", bold=True)
    add_equation(doc, r"\dot{Q} = \dot{m}_c c_p (T_{c,out} - T_{c,in}) = 2 \times 4180 \times (80 - 20) = 501\,600 \text{ W} = 501{,}6 \text{ kW}")

    add_para(doc, "Krok 2: LMTD (protiproud)", bold=True)
    add_equation(doc, r"\Delta T_1 = T_{h,in} - T_{c,out} = 150 - 80 = 70 \text{ \u00b0C}")
    add_equation(doc, r"\Delta T_2 = T_{h,out} - T_{c,in} = 90 - 20 = 70 \text{ \u00b0C}")
    add_equation(doc, r"\Delta T_1 = \Delta T_2 = 70 \text{ \u00b0C} \quad \Rightarrow \quad \Delta T_{LMTD} = 70 \text{ \u00b0C}")

    add_para(doc, "Krok 3: Teplosm\u011bnn\u00e1 plocha", bold=True)
    add_equation(doc, r"A = \frac{\dot{Q}}{k \cdot \Delta T_{LMTD}} = \frac{501\,600}{1200 \times 70} = 5{,}97 \text{ m}^2")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Q\u0307 = 501,6 kW\n"
        "LMTD = 70 \u00b0C (zvl\u00e1\u0161tn\u00ed p\u0159\u00edpad \u0394T\u2081 = \u0394T\u2082)\n"
        "A = 5,97 m\u00b2\n\n"
        "Pozn\u00e1mka: Rovnost \u0394T\u2081 = \u0394T\u2082 znamen\u00e1, \u017ee C_h = C_c "
        "(stejn\u00fd teplotn\u00ed v\u00fdkon obou tekutin). V praxi se plocha nav\u00fd\u0161\u00ed "
        "o 10\u201320 % kv\u016fli zanášen\u00ed.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d je protiproud\u00fd v\u00fdm\u011bn\u00edk \u00fa\u010dinn\u011bj\u0161\u00ed ne\u017e souproud\u00fd?",
         "V protiproudu m\u016f\u017ee v\u00fdstupn\u00ed teplota studen\u00e9 tekutiny p\u0159ekro\u010dit v\u00fdstupn\u00ed "
         "teplotu hork\u00e9 tekutiny (T_{c,out} > T_{h,out}). LMTD je p\u0159i stejn\u00fdch "
         "teplot\u00e1ch v\u011bt\u0161\u00ed ne\u017e u souproudu, tak\u017ee sta\u010d\u00ed men\u0161\u00ed plocha."),

        ("Pro\u010d nelze pro st\u0159edn\u00ed \u0394T pou\u017e\u00edt aritmetick\u00fd pr\u016fm\u011br?",
         "Proto\u017ee \u0394T kles\u00e1 exponenci\u00e1ln\u011b pod\u00e9l v\u00fdm\u011bn\u00edku, ne line\u00e1rn\u011b. "
         "Aritmetick\u00fd pr\u016fm\u011br by nadhodnotil st\u0159edn\u00ed \u0394T a vedl k poddimenov\u00e1n\u00ed "
         "plochy. LMTD spr\u00e1vn\u011b zohled\u0148uje exponenci\u00e1ln\u00ed pr\u016fb\u011bh."),

        ("Co je korek\u010dn\u00ed faktor F a kdy se pou\u017e\u00edv\u00e1?",
         "F koriguje LMTD pro uspo\u0159\u00e1d\u00e1n\u00ed jin\u00e1 ne\u017e \u010dist\u00fd protiproud "
         "(k\u0159\u00ed\u017eov\u00fd proud, v\u00edcetahov\u00e9 v\u00fdm\u011bn\u00edky). F \u2264 1 a z\u00e1vis\u00ed na pom\u011brech "
         "teplot P a R. P\u0159i F < 0,75 se doporu\u010duje zm\u011bnit uspo\u0159\u00e1d\u00e1n\u00ed."),

        ("Jak zanášen\u00ed ovliv\u0148uje v\u00fdkon v\u00fdm\u011bn\u00edku?",
         "Zanášen\u00ed p\u0159id\u00e1v\u00e1 tepeln\u00fd odpor R_f na povrch trubek, \u010d\u00edm\u017e sni\u017euje "
         "efektivn\u00ed k. P\u0159i n\u00e1vrhu se p\u0159id\u00e1v\u00e1 10\u201320 % plochy nav\u00edc. "
         "Typick\u00e9 R_f: \u010dist\u00e1 voda 0,0001, chladicí v\u011b\u017e 0,0003, \u0159\u00ed\u010dn\u00ed voda 0,0005 m\u00b2K/W."),

        ("Jak\u00fd je rozd\u00edl mezi rekupera\u010dn\u00edm a regenera\u010dn\u00edm v\u00fdm\u011bn\u00edkem?",
         "Rekupera\u010dn\u00ed: tekutiny jsou odd\u011bleny st\u011bnou trvale, teplo proch\u00e1z\u00ed prostupen. "
         "Regenera\u010dn\u00ed: v\u00fdpl\u0148 (matrice) se st\u0159\u00eddav\u011b oh\u0159\u00edv\u00e1 a chlad\u00ed kontaktem "
         "s hork\u00fdm a studen\u00fdm proudem (nap\u0159. Ljungstr\u00f6m\u016fv oh\u0159\u00edv\u00e1k vzduchu v elektr\u00e1rn\u011b)."),

        ("Jak ze zadan\u00fdch teplot zjist\u00edte, zda jde o souproud nebo protiproud?",
         "U souproudu: T_{h,out} > T_{c,out} (v\u017edy). U protiproudu: T_{c,out} m\u016f\u017ee b\u00fdt "
         "vy\u0161\u0161\u00ed ne\u017e T_{h,out}. D\u00e1le: u souproudu \u0394T\u2081 > \u0394T\u2082 v\u017edy, "
         "u protiproudu mohou b\u00fdt \u0394T\u2081 a \u0394T\u2082 bl\u00edzk\u00e9 nebo i stejn\u00e9."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Incropera, F.P. et al.: Fundamentals of Heat and Mass Transfer, 8th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cengel, Y.A.: Heat Transfer \u2014 A Practical Approach")
    add_bullet(doc, "Shah, R.K., Sekuli\u0107, D.P.: Fundamentals of Heat Exchanger Design")
    add_bullet(doc, "TEMA Standards \u2014 Tubular Exchanger Manufacturers Association", is_last=True)

    save_and_export(doc, "13-vymeniky-tepla")


if __name__ == "__main__":
    generate()
