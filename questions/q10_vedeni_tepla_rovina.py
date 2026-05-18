# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 10: Stacion\u00e1rn\u00ed veden\u00ed a prostup tepla neomezenou st\u011bnou rovinnou,
jednoduchou i slo\u017eenou.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

def generate_simple_wall():
    """Temperature profile through a simple flat wall with convection on both sides."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    # Regions: fluid1 | wall | fluid2
    # x: 0..0.25 (fluid1), 0.25..0.55 (wall, delta=0.3), 0.55..1.0 (fluid2)
    x_f1 = np.linspace(0, 0.25, 50)
    x_wall = np.array([0.25, 0.55])
    x_f2 = np.linspace(0.55, 1.0, 50)

    Tf1, Tw1, Tw2, Tf2 = 90, 75, 25, 10

    # Convective boundary layers (exponential approach)
    T_f1 = Tf1 - (Tf1 - Tw1) * np.exp(-12 * (0.25 - x_f1))
    T_wall = np.array([Tw1, Tw2])
    T_f2 = Tf2 + (Tw2 - Tf2) * np.exp(-12 * (x_f2 - 0.55))

    # Wall fill
    ax.fill_between([0.25, 0.55], -5, 100, alpha=0.12, color="gray")

    ax.plot(x_f1, T_f1, color=COLORS[1], linewidth=2.5)
    ax.plot(x_wall, T_wall, color=COLORS[0], linewidth=3, label="Veden\u00ed st\u011bnou")
    ax.plot(x_f2, T_f2, color=COLORS[2], linewidth=2.5)

    # Dashed lines for T values
    for T, label, x_pos, color in [
        (Tf1, "$T_{f1}$", 0.02, COLORS[1]),
        (Tw1, "$T_{w1}$", 0.27, "black"),
        (Tw2, "$T_{w2}$", 0.57, "black"),
        (Tf2, "$T_{f2}$", 0.92, COLORS[2]),
    ]:
        ax.axhline(y=T, color=color, linestyle=":", linewidth=0.8, alpha=0.5)
        ax.text(x_pos, T + 3, label, fontsize=12, color=color, fontweight="bold")

    # Labels
    ax.text(0.12, 95, "Tekutina 1", fontsize=10, ha="center", color=COLORS[1], fontweight="bold")
    ax.text(0.4, 95, "ST\u011aNA\n(\u03b4, \u03bb)", fontsize=11, ha="center", color="gray", fontweight="bold")
    ax.text(0.78, 95, "Tekutina 2", fontsize=10, ha="center", color=COLORS[2], fontweight="bold")

    # Thermal resistances
    ax.annotate("", xy=(0.25, -2), xytext=(0, -2),
                arrowprops=dict(arrowstyle="<->", color=COLORS[1], lw=1.5))
    ax.text(0.125, -8, "$R_{\\alpha 1}$", fontsize=10, ha="center", color=COLORS[1])

    ax.annotate("", xy=(0.55, -2), xytext=(0.25, -2),
                arrowprops=dict(arrowstyle="<->", color=COLORS[0], lw=1.5))
    ax.text(0.4, -8, "$R_{\\lambda}$", fontsize=10, ha="center", color=COLORS[0])

    ax.annotate("", xy=(1.0, -2), xytext=(0.55, -2),
                arrowprops=dict(arrowstyle="<->", color=COLORS[2], lw=1.5))
    ax.text(0.775, -8, "$R_{\\alpha 2}$", fontsize=10, ha="center", color=COLORS[2])

    ax.set_xlabel("Poloha x", fontsize=11)
    ax.set_ylabel("Teplota T [\u00b0C]", fontsize=11)
    ax.set_title("Prostup tepla jednoduchou rovinnou st\u011bnou\nkonvekce \u2192 veden\u00ed \u2192 konvekce",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-15, 100)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q10_simple_wall.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_composite_wall():
    """Temperature profile through a composite (multi-layer) wall."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # 3-layer wall: fluid1 | layer1 | layer2 | layer3 | fluid2
    layers = [
        (0.15, 0.30, 50, "#FFD6D6", "#DC2626", "Cihla\n\u03bb\u2081=0,8"),
        (0.30, 0.42, None, "#FEF3C7", "#D97706", "Izolace\n\u03bb\u2082=0,04"),
        (0.42, 0.50, None, "#DBEAFE", "#2563EB", "Om\u00edtka\n\u03bb\u2083=0,9"),
    ]

    # Temperatures at interfaces
    Tf1 = 20  # indoor
    Tw = [18, 5, 4.5, -12]  # T at each interface
    Tf2 = -15  # outdoor

    # Wall fills
    for x1, x2, _, fc, ec, label in layers:
        ax.fill_between([x1, x2], -20, 25, alpha=0.2, color=fc)
        ax.axvline(x=x1, color=ec, linewidth=1, linestyle="-", alpha=0.5)
        ax.axvline(x=x2, color=ec, linewidth=1, linestyle="-", alpha=0.5)
        ax.text((x1 + x2) / 2, 22, label, fontsize=8, ha="center", va="top",
                color=ec, fontweight="bold")

    # Temperature profile through wall (linear in each layer)
    x_f1 = np.linspace(0, 0.15, 30)
    T_f1 = Tf1 - (Tf1 - Tw[0]) * np.exp(-15 * (0.15 - x_f1))

    x_profile = [0.15, 0.30, 0.42, 0.50]
    T_profile = Tw

    x_f2 = np.linspace(0.50, 0.65, 30)
    T_f2 = Tf2 + (Tw[3] - Tf2) * np.exp(-15 * (x_f2 - 0.50))

    ax.plot(x_f1, T_f1, color=COLORS[1], linewidth=2.5)
    ax.plot(x_profile, T_profile, "o-", color="black", linewidth=2.5, markersize=6,
            label="Teplotn\u00ed profil")
    ax.plot(x_f2, T_f2, color=COLORS[2], linewidth=2.5)

    # Labels
    ax.text(0.07, 22, "INT.\n($T_{f1}$)", fontsize=9, ha="center", color=COLORS[1], fontweight="bold")
    ax.text(0.58, 22, "EXT.\n($T_{f2}$)", fontsize=9, ha="center", color=COLORS[2], fontweight="bold")

    # Thermal circuit below
    ax.text(0.325, -17, "$R_{\\alpha 1} + R_{\\lambda 1} + R_{\\lambda 2} + R_{\\lambda 3} + R_{\\alpha 2}$",
            fontsize=9, ha="center", color="gray", style="italic")

    ax.set_xlabel("Poloha x", fontsize=11)
    ax.set_ylabel("Teplota T [\u00b0C]", fontsize=11)
    ax.set_title("Prostup tepla slo\u017eenou rovinnou st\u011bnou (3 vrstvy)\nline\u00e1rn\u00ed pokles T v ka\u017ed\u00e9 vrstv\u011b",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(-0.02, 0.67)
    ax.set_ylim(-20, 25)
    ax.legend(fontsize=9, loc="lower left")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q10_composite_wall.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_thermal_circuit():
    """Thermal resistance circuit diagram for composite wall."""
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1, 2)
    ax.set_aspect("equal")
    ax.axis("off")

    # Resistor symbols (zig-zag simplified as rectangles)
    resistors = [
        (0.5, "$R_{\\alpha 1}$", COLORS[1]),
        (2.5, "$R_{\\lambda 1}$", COLORS[0]),
        (4.5, "$R_{\\lambda 2}$", "#D97706"),
        (6.5, "$R_{\\lambda 3}$", COLORS[0]),
        (8.5, "$R_{\\alpha 2}$", COLORS[2]),
    ]

    for x, label, color in resistors:
        rect = Rectangle((x, 0.2), 1.2, 0.6, facecolor="white", edgecolor=color, lw=2)
        ax.add_patch(rect)
        ax.text(x + 0.6, 0.5, label, fontsize=10, ha="center", va="center",
                color=color, fontweight="bold")
        # Connection lines
        if x > 0.5:
            ax.plot([x - 0.3, x], [0.5, 0.5], "k-", lw=1.5)

    # End connections
    ax.plot([0, 0.5], [0.5, 0.5], "k-", lw=1.5)
    ax.plot([9.7, 10.2], [0.5, 0.5], "k-", lw=1.5)

    # Temperature labels
    ax.text(0, 1.2, "$T_{f1}$", fontsize=12, ha="center", fontweight="bold", color=COLORS[1])
    ax.text(10.2, 1.2, "$T_{f2}$", fontsize=12, ha="center", fontweight="bold", color=COLORS[2])

    # Arrow for Q
    ax.annotate("$\\dot{Q}$", xy=(5, -0.3), fontsize=14, fontweight="bold",
                color="#D97706", ha="center")
    ax.annotate("", xy=(7, -0.5), xytext=(3, -0.5),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2))

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q10_thermal_circuit.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH DOKUMENTU
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_simple = generate_simple_wall()
    img_composite = generate_composite_wall()
    img_circuit = generate_thermal_circuit()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="10. Stacion\u00e1rn\u00ed veden\u00ed a prostup tepla neomezenou st\u011bnou rovinnou,\n"
              "      jednoduchou i slo\u017eenou.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Odvo\u010fte vztahy pro stacion\u00e1rn\u00ed veden\u00ed tepla rovinnou st\u011bnou (jednoduchou "
        "a slo\u017eenou). Vysv\u011btlete pojem prostupu tepla, definujte sou\u010dinitel prostupu "
        "tepla k a tepeln\u00e9 odpory. Uve\u010fte teplotn\u00ed profily.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    # -- 1.1 --
    add_heading(doc, "1.1 V\u00fdchoz\u00ed p\u0159edpoklady", level=3)

    add_bullet(doc, "Stacion\u00e1rn\u00ed stav \u2014 teplota se s \u010dasem nem\u011bn\u00ed (\u2202T/\u2202t = 0)")
    add_bullet(doc, "Neomezen\u00e1 st\u011bna \u2014 rozm\u011bry ve sm\u011brech y, z jsou mnohem v\u011bt\u0161\u00ed ne\u017e ve sm\u011bru x; "
               "teplo proud\u00ed pouze ve sm\u011bru x (1D \u00faloha)")
    add_bullet(doc, "Konstantn\u00ed \u03bb \u2014 tepeln\u00e1 vodivost nez\u00e1vis\u00ed na teplot\u011b (v r\u00e1mci ka\u017ed\u00e9 vrstvy)")
    add_bullet(doc, "\u017d\u00e1dn\u00e9 vnit\u0159n\u00ed zdroje tepla (q\u0307_v = 0)", is_last=True)

    # -- 1.2 Jednoducha stena --
    add_heading(doc, "1.2 Veden\u00ed tepla jednoduchou rovinnou st\u011bnou", level=3)

    add_info_box(doc,
        "Fourier\u016fv z\u00e1kon pro rovinnou st\u011bnu",
        "P\u0159i stacion\u00e1rn\u00edm veden\u00ed rovinnou st\u011bnou je teplotn\u00ed profil line\u00e1rn\u00ed "
        "a tepeln\u00fd tok je konstantn\u00ed po cel\u00e9 tlou\u0161\u0165ce st\u011bny.")

    add_para(doc, "Fourierova rovnice pro 1D stacion\u00e1rn\u00ed veden\u00ed bez zdroj\u016f:", keep_with_next=True)
    add_equation(doc, r"\frac{d^2 T}{dx^2} = 0", label="1")

    add_para(doc, "Integrac\u00ed s okrajov\u00fdmi podm\u00ednkami T(0) = T\u2081, T(\u03b4) = T\u2082:", keep_with_next=True)
    add_equation(doc, r"T(x) = T_1 + \frac{T_2 - T_1}{\delta} x = T_1 - \frac{T_1 - T_2}{\delta} x", label="2")

    add_para(doc, "Tepeln\u00fd tok st\u011bnou:", keep_with_next=True)
    add_equation(doc, r"\dot{Q} = \frac{\lambda A}{\delta}(T_1 - T_2) = \frac{T_1 - T_2}{R_\lambda}", label="3")

    add_para(doc, "Tepeln\u00fd odpor veden\u00ed rovinnou st\u011bnou:", keep_with_next=True)
    add_equation(doc, r"R_\lambda = \frac{\delta}{\lambda A} \quad [\text{K/W}]", label="4")

    # -- 1.3 Prostup tepla --
    add_page_break(doc)
    add_heading(doc, "1.3 Prostup tepla jednoduchou rovinnou st\u011bnou", level=3)

    add_info_box(doc,
        "Prostup tepla",
        "P\u0159enos tepla z jedné tekutiny do druh\u00e9 p\u0159es st\u011bnu. Zahrnuje: "
        "p\u0159estup na stran\u011b 1 (konvekce, \u03b1\u2081) \u2192 veden\u00ed st\u011bnou (\u03bb) \u2192 "
        "p\u0159estup na stran\u011b 2 (konvekce, \u03b1\u2082).")

    add_image(doc, img_simple, width_cm=14,
              caption="Obr. 1: Prostup tepla jednoduchou rovinnou st\u011bnou \u2014 teplotn\u00ed profil a tepeln\u00e9 odpory")

    add_para(doc, "Celkov\u00fd tepeln\u00fd odpor (s\u00e9riov\u00e9 \u0159azen\u00ed):", keep_with_next=True)
    add_equation(doc, r"R_{celk} = R_{\alpha 1} + R_\lambda + R_{\alpha 2} = \frac{1}{\alpha_1 A} + \frac{\delta}{\lambda A} + \frac{1}{\alpha_2 A}", label="5")

    add_para(doc, "Tepeln\u00fd tok prostupu:", keep_with_next=True)
    add_equation(doc, r"\dot{Q} = \frac{T_{f1} - T_{f2}}{R_{celk}} = k A (T_{f1} - T_{f2})", label="6")

    add_para(doc, "Sou\u010dinitel prostupu tepla k:", keep_with_next=True)
    add_equation(doc, r"\frac{1}{k} = \frac{1}{\alpha_1} + \frac{\delta}{\lambda} + \frac{1}{\alpha_2}", label="7")

    add_warning_box(doc,
        "Sou\u010dinitel prostupu tepla k [W/(m\u00b2\u00b7K)] zahrnuje v\u0161echny t\u0159i odpory "
        "(konvekce-veden\u00ed-konvekce). Nesm\u00ed se zam\u011b\u0148ovat se sou\u010dinitelem p\u0159estupu "
        "tepla \u03b1 [W/(m\u00b2\u00b7K)], kter\u00fd popisuje pouze konvekci na jedné stran\u011b.")

    # -- 1.4 Slozena stena --
    add_page_break(doc)
    add_heading(doc, "1.4 Prostup tepla slo\u017eenou rovinnou st\u011bnou", level=3)

    add_para(doc,
        "St\u011bna slo\u017een\u00e1 z n vrstev r\u016fzn\u00fdch materi\u00e1l\u016f (\u03bb\u2081, \u03b4\u2081; \u03bb\u2082, \u03b4\u2082; ... \u03bb_n, \u03b4_n). "
        "V ka\u017ed\u00e9 vrstv\u011b je teplotn\u00ed profil line\u00e1rn\u00ed, ale se r\u016fzn\u00fdm sklonem (\u00fam\u011brn\u00fdm \u03b4_i/\u03bb_i).")

    add_image(doc, img_composite, width_cm=14,
              caption="Obr. 2: Prostup tepla slo\u017eenou rovinnou st\u011bnou (3 vrstvy) \u2014 line\u00e1rn\u00ed pokles T v ka\u017ed\u00e9 vrstv\u011b")

    add_para(doc, "Celkov\u00fd tepeln\u00fd odpor slo\u017een\u00e9 st\u011bny:", keep_with_next=True)
    add_equation(doc, r"R_{celk} = \frac{1}{\alpha_1 A} + \sum_{i=1}^{n} \frac{\delta_i}{\lambda_i A} + \frac{1}{\alpha_2 A}", label="8")

    add_para(doc, "Sou\u010dinitel prostupu tepla:", keep_with_next=True)
    add_equation(doc, r"\frac{1}{k} = \frac{1}{\alpha_1} + \sum_{i=1}^{n} \frac{\delta_i}{\lambda_i} + \frac{1}{\alpha_2}", label="9")

    add_para(doc, "Tepeln\u00fd tok:", keep_with_next=True)
    add_equation(doc, r"\dot{Q} = k A (T_{f1} - T_{f2})", label="10")

    add_para(doc, "Teploty na rozhran\u00edch vrstev:", keep_with_next=True)
    add_equation(doc, r"T_{i} = T_{f1} - \dot{Q} \cdot \left(\frac{1}{\alpha_1 A} + \sum_{j=1}^{i} \frac{\delta_j}{\lambda_j A}\right)", label="11")

    add_image(doc, img_circuit, width_cm=14,
              caption="Obr. 3: N\u00e1hradn\u00ed tepeln\u00fd obvod prostupu tepla slo\u017eenou st\u011bnou")

    add_info_box(doc,
        "Praktick\u00e9 pravidlo",
        "Celkov\u00fd tepeln\u00fd odpor ur\u010duje vrstva s nejv\u011bt\u0161\u00edm odporem. "
        "U zd\u011bn\u00e9 st\u011bny s izolac\u00ed dominuje izolace (\u03bb \u2248 0,03\u20130,05 W/(m\u00b7K)) \u2014 "
        "zv\u011bt\u0161ov\u00e1n\u00ed tlou\u0161\u0165ky cihly m\u00e1 minim\u00e1ln\u00ed vliv.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Typick\u00e9 sou\u010dinitele prostupu tepla", level=3)

    add_styled_table(doc,
        headers=["Konstrukce", "k [W/(m\u00b2\u00b7K)]", "Po\u017eadavek \u010cSN"],
        data=[
            ["Neizolovan\u00e1 cihlov\u00e1 st\u011bna 45 cm", "1,2\u20131,5", "\u2014"],
            ["Izolovan\u00e1 st\u011bna (10 cm polystyren)", "0,20\u20130,30", "U \u2264 0,30"],
            ["Pasivn\u00ed d\u016fm (20\u201330 cm izolace)", "0,10\u20130,15", "U \u2264 0,18"],
            ["Dvojsklo (4-16-4)", "2,5\u20133,0", "U \u2264 1,50"],
            ["Trojsklo s Ar", "0,5\u20130,8", "U \u2264 1,20"],
        ],
    )

    add_para(doc,
        "Pozn.: V \u010cesk\u00fdch norm\u00e1ch (\u010cSN 73 0540) se m\u00edsto k pou\u017e\u00edv\u00e1 ozna\u010den\u00ed U "
        "(sou\u010dinitel prostupu tepla). Numericky k = U.")

    add_heading(doc, "2.2 Kontaktn\u00ed tepeln\u00fd odpor", level=3)
    add_para(doc,
        "Na rozhran\u00ed dvou vrstev existuje kontaktn\u00ed tepeln\u00fd odpor R_c, kter\u00fd "
        "zp\u016fsobuje teplotn\u00ed skok na rozhran\u00ed. V praxi je \u010dasto zanedb\u00e1v\u00e1n "
        "u stavebn\u00edch konstrukc\u00ed, ale je v\u00fdznamn\u00fd u kovov\u00fdch spoj\u016f "
        "(nap\u0159. kontakt \u010dipu a chladi\u010de).")

    add_heading(doc, "2.3 Kritick\u00e1 tlou\u0161\u0165ka izolace", level=3)
    add_para(doc,
        "U trubek m\u016f\u017ee p\u0159id\u00e1n\u00ed izolace paradoxn\u011b ZV\u00dd\u0160IT tepeln\u00e9 ztr\u00e1ty, "
        "pokud je polom\u011br izolace men\u0161\u00ed ne\u017e kritick\u00fd polom\u011br r_kr = \u03bb_iz/\u03b1. "
        "U rovinn\u00e9 st\u011bny tento efekt nenast\u00e1v\u00e1 \u2014 izolace v\u017edy sni\u017euje tepeln\u00e9 ztr\u00e1ty.")

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Prostup tepla slo\u017eenou st\u011bnou budovy", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: St\u011bna se skl\u00e1d\u00e1 ze t\u0159\u00ed vrstev: cihla (\u03b4\u2081 = 300 mm, \u03bb\u2081 = 0,8 W/(m\u00b7K)), "
        "tepeln\u00e1 izolace (\u03b4\u2082 = 100 mm, \u03bb\u2082 = 0,04 W/(m\u00b7K)), om\u00edtka (\u03b4\u2083 = 15 mm, "
        "\u03bb\u2083 = 0,9 W/(m\u00b7K)). Sou\u010dinitel p\u0159estupu tepla: \u03b1\u2081 = 8 W/(m\u00b2\u00b7K) (interi\u00e9r), "
        "\u03b1\u2082 = 23 W/(m\u00b2\u00b7K) (exteri\u00e9r). Teploty: T\u2081 = 20 \u00b0C, T\u2082 = -15 \u00b0C. "
        "Ur\u010dete sou\u010dinitel prostupu tepla k a tepelnou ztr\u00e1tu st\u011bnou o plo\u0161e A = 10 m\u00b2.",
        bold=True)

    add_para(doc, "Krok 1: Tepeln\u00e9 odpory", bold=True)
    add_equation(doc, r"\frac{1}{k} = \frac{1}{\alpha_1} + \frac{\delta_1}{\lambda_1} + \frac{\delta_2}{\lambda_2} + \frac{\delta_3}{\lambda_3} + \frac{1}{\alpha_2}")
    add_equation(doc, r"\frac{1}{k} = \frac{1}{8} + \frac{0{,}3}{0{,}8} + \frac{0{,}1}{0{,}04} + \frac{0{,}015}{0{,}9} + \frac{1}{23}")
    add_equation(doc, r"\frac{1}{k} = 0{,}125 + 0{,}375 + 2{,}500 + 0{,}017 + 0{,}043 = 3{,}060 \text{ m}^2\text{K/W}")

    add_para(doc, "Krok 2: Sou\u010dinitel prostupu tepla", bold=True)
    add_equation(doc, r"k = \frac{1}{3{,}060} = 0{,}327 \text{ W/(m}^2\text{\cdot K)}")

    add_para(doc, "Krok 3: Tepeln\u00e1 ztr\u00e1ta", bold=True)
    add_equation(doc, r"\dot{Q} = k A (T_{f1} - T_{f2}) = 0{,}327 \times 10 \times (20 - (-15)) = 0{,}327 \times 10 \times 35 = 114{,}5 \text{ W}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "k = 0,327 W/(m\u00b2\u00b7K) \u2014 spl\u0148uje po\u017eadavek \u010cSN (U \u2264 0,30 W/(m\u00b2\u00b7K)) t\u011bsn\u011b.\n"
        "Tepeln\u00e1 ztr\u00e1ta: 114,5 W pro 10 m\u00b2 st\u011bny.\n\n"
        "Dominantn\u00ed odpor: izolace (R\u2082 = 2,500 z celkov\u00fdch 3,060 = 82 %). "
        "Cihla p\u0159isp\u00edv\u00e1 jen 12 %, konvekce a om\u00edtka jsou zanedbateln\u00e9.")

    # ==================================================================
    # CAST 4: ZKOUZKOVE OTAZKY
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d je teplotn\u00ed profil v rovinné st\u011bn\u011b line\u00e1rn\u00ed?",
         "Plyne z \u0159e\u0161en\u00ed Fourierovy rovnice d\u00b2T/dx\u00b2 = 0 p\u0159i stacion\u00e1rn\u00edm stavu "
         "bez vnit\u0159n\u00edch zdroj\u016f. Dvojn\u00e1sobn\u00e1 integrace d\u00e1v\u00e1 T(x) = C\u2081x + C\u2082, "
         "co\u017e je line\u00e1rn\u00ed funkce. Konstanty C\u2081, C\u2082 se ur\u010d\u00ed z okrajov\u00fdch podm\u00ednek."),

        ("Jak\u00fd je rozd\u00edl mezi sou\u010dinitelem prostupu k a sou\u010dinitelem p\u0159estupu \u03b1?",
         "\u03b1 popisuje p\u0159enos tepla konvekc\u00ed na jedn\u00e9 stran\u011b st\u011bny (tekutina \u2194 povrch). "
         "k zahrnuje cel\u00fd prostup: konvekce + veden\u00ed + konvekce. "
         "k je v\u017edy men\u0161\u00ed ne\u017e nejmen\u0161\u00ed z \u03b1\u2081, \u03b1\u2082, proto\u017ee k obsahuje dal\u0161\u00ed odpory."),

        ("Pro\u010d u slo\u017een\u00e9 st\u011bny dominuje vrstva s nejv\u011bt\u0161\u00edm tepeln\u00fdm odporem?",
         "Tepeln\u00e9 odpory jsou za\u0159azeny v s\u00e9rii \u2014 celkov\u00fd odpor je sou\u010det. "
         "Vrstva s nejv\u011bt\u0161\u00edm odporem (nap\u0159. izolace s n\u00edzk\u00fdm \u03bb) p\u0159edstavuje nejv\u011bt\u0161\u00ed "
         "\u010d\u00e1st celkov\u00e9ho odporu. Zlep\u0161en\u00ed ostatn\u00edch vrstev m\u00e1 minim\u00e1ln\u00ed vliv."),

        ("Co se stane s teplotn\u00edm profilem, pokud \u03bb z\u00e1vis\u00ed na teplot\u011b?",
         "Teplotn\u00ed profil p\u0159estane b\u00fdt line\u00e1rn\u00ed. Pokud \u03bb roste s teplotou, "
         "profil se prohne konvexn\u011b; pokud \u03bb kles\u00e1 s teplotou, prohne se konk\u00e1vn\u011b. "
         "Fourierova rovnice se \u0159e\u0161\u00ed s prom\u011bnnou \u03bb(T)."),

        ("Jak ur\u010d\u00edte teplotu na rozhran\u00ed dvou vrstev slo\u017een\u00e9 st\u011bny?",
         "Z celkov\u00e9ho Q\u0307 (kter\u00fd je konstantn\u00ed p\u0159es v\u0161echny vrstvy) vyj\u00e1d\u0159\u00edte teplotn\u00ed sp\u00e1d "
         "p\u0159es ka\u017edou vrstvu: \u0394T_i = Q\u0307 \u00b7 R_i. Teplota na i-t\u00e9m rozhran\u00ed je "
         "T_i = T\u2081 \u2212 Q\u0307 \u00b7 (R_{\u03b1\u2081} + R_{\u03bb\u2081} + ... + R_{\u03bbi})."),

        ("Pro\u010d je p\u0159i v\u00fdpo\u010dtu prostupu tepla d\u016fle\u017eit\u00fd odpor konvekce?",
         "I kdy\u017e je \u010dasto men\u0161\u00ed ne\u017e odpor st\u011bny, p\u0159i vysok\u00e9 izolaci st\u011bny se odpor "
         "konvekce stane srovnateln\u00fdm. Nap\u0159. u pasivn\u00edho domu odpor izolace R_\u03bb = 5\u20138 K\u00b7m\u00b2/W, "
         "ale 1/\u03b1\u2081 = 0,125 K\u00b7m\u00b2/W (interi\u00e9r) \u2014 st\u00e1le jen 2 % celku."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Incropera, F.P. et al.: Fundamentals of Heat and Mass Transfer, 8th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cSN 73 0540 \u2014 Tepeln\u00e1 ochrana budov")
    add_bullet(doc, "Kozub\u00edk, T.: P\u0159enos tepla, VUT Brno")
    add_bullet(doc, "\u010cengel, Y.A.: Heat Transfer \u2014 A Practical Approach", is_last=True)

    save_and_export(doc, "10-vedeni-tepla-rovina")


if __name__ == "__main__":
    generate()
