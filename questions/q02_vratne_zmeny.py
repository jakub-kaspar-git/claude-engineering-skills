# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 2: Z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu ide\u00e1ln\u00edho plynu.
Rovnice zm\u011bny, pr\u016fb\u011bh diagram\u016f p-v a T-s, sd\u011blen\u00e9 teplo, vykonan\u00e1 pr\u00e1ce.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

def generate_pv_processes():
    """p-v diagram with all basic processes from the same initial state."""
    fig, ax = plt.subplots(figsize=(8, 6))

    R = 287.1
    cv = 718
    cp = 1005
    kappa = cp / cv

    T1 = 400  # K
    p1 = 300e3  # Pa
    v1 = R * T1 / p1

    v = np.linspace(v1 * 0.4, v1 * 3, 500)

    # Isochoric (v = const) - vertical line
    p_izoch = np.linspace(p1 * 0.3, p1 * 2, 100)
    ax.plot(np.full_like(p_izoch, v1), p_izoch / 1e3, color=COLORS[2], linewidth=2.5,
            label="Izochorick\u00e1 (v = konst.)")

    # Isobaric (p = const) - horizontal line
    v_izob = np.linspace(v1 * 0.4, v1 * 3, 100)
    ax.plot(v_izob, np.full_like(v_izob, p1 / 1e3), color=COLORS[1], linewidth=2.5,
            label="Izobarick\u00e1 (p = konst.)")

    # Isothermal (T = const): pv = const
    p_izo = p1 * v1 / v
    ax.plot(v, p_izo / 1e3, color=COLORS[0], linewidth=2.5,
            label="Izotermick\u00e1 (T = konst.)")

    # Isentropic (s = const): pv^kappa = const
    p_izen = p1 * (v1 / v) ** kappa
    ax.plot(v, p_izen / 1e3, color=COLORS[3], linewidth=2.5,
            label="Izoentropick\u00e1 (s = konst.)")

    # Polytropic (n = 1.3)
    n_poly = 1.3
    p_poly = p1 * (v1 / v) ** n_poly
    ax.plot(v, p_poly / 1e3, color="#7C3AED", linewidth=2.5, linestyle="--",
            label="Polytropick\u00e1 (n = 1,3)")

    # Initial state
    ax.plot(v1, p1 / 1e3, "ko", markersize=12, zorder=5)
    ax.annotate("Bod 1", xy=(v1, p1 / 1e3), xytext=(v1 + 0.05, p1 / 1e3 + 50),
                fontsize=10, fontweight="bold", arrowprops=dict(arrowstyle="->", lw=1.5))

    # Work annotation
    ax.text(0.6, 50, "w = $\\int p \\cdot dv$\n(plocha pod k\u0159ivkou)",
            fontsize=9, style="italic", color="#555")

    ax.set_xlabel("M\u011brn\u00fd objem v [m\u00b3/kg]", fontsize=11)
    ax.set_ylabel("Tlak p [kPa]", fontsize=11)
    ax.set_title("p-v diagram: z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu z bodu 1",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, loc="upper right")
    ax.set_xlim(v1 * 0.3, v1 * 3.2)
    ax.set_ylim(0, p1 / 1e3 * 2.5)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q02_pv_processes.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_ts_processes():
    """T-s diagram with all basic processes."""
    fig, ax = plt.subplots(figsize=(8, 6))

    cv = 718
    cp = 1005
    kappa = cp / cv
    T1 = 400

    # From common initial state
    s_range = np.linspace(-300, 600, 300)

    # Isothermal: horizontal
    ax.axhline(y=T1, color=COLORS[0], linewidth=2.5, label="Izotermick\u00e1 (T = konst.)")

    # Isentropic: vertical at s=0
    ax.axvline(x=0, color=COLORS[3], linewidth=2.5, label="Izoentropick\u00e1 (s = konst.)")

    # Isochoric: T = T1 * exp(s/cv)
    T_izoch = T1 * np.exp(s_range / cv)
    mask_v = (T_izoch > 250) & (T_izoch < 700)
    ax.plot(s_range[mask_v], T_izoch[mask_v], color=COLORS[2], linewidth=2.5,
            label="Izochorick\u00e1 (v = konst.)")

    # Isobaric: T = T1 * exp(s/cp)
    T_izob = T1 * np.exp(s_range / cp)
    mask_p = (T_izob > 250) & (T_izob < 700)
    ax.plot(s_range[mask_p], T_izob[mask_p], color=COLORS[1], linewidth=2.5,
            label="Izobarick\u00e1 (p = konst.)")

    # Polytropic (n=1.3)
    n_poly = 1.3
    c_n = cv * (n_poly - kappa) / (n_poly - 1)
    if abs(c_n) > 1:
        T_poly = T1 * np.exp(s_range / c_n)
        mask_n = (T_poly > 250) & (T_poly < 700)
        ax.plot(s_range[mask_n], T_poly[mask_n], color="#7C3AED", linewidth=2.5,
                linestyle="--", label="Polytropick\u00e1 (n = 1,3)")

    ax.plot(0, T1, "ko", markersize=12, zorder=5)
    ax.annotate("Bod 1", xy=(0, T1), xytext=(50, T1 - 30),
                fontsize=10, fontweight="bold", arrowprops=dict(arrowstyle="->", lw=1.5))

    ax.text(200, 620, "q = $\\int T \\cdot ds$\n(plocha pod k\u0159ivkou)",
            fontsize=9, style="italic", color="#555")

    ax.set_xlabel("M\u011brn\u00e1 entropie s [J/(kg\u00b7K)]", fontsize=11)
    ax.set_ylabel("Teplota T [K]", fontsize=11)
    ax.set_title("T-s diagram: z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu z bodu 1",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, loc="upper left")
    ax.set_xlim(-350, 650)
    ax.set_ylim(250, 700)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q02_ts_processes.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_polytropic_overview():
    """Overview of polytropic exponent n and its special cases."""
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(0, 2)
    ax.axis("off")

    # Number line for n
    ax.annotate("", xy=(5, 1), xytext=(0, 1),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2))
    ax.text(5.2, 1, "n", fontsize=12, fontweight="bold")

    # Tick marks and labels
    ticks = [
        (0.5, "0", "Izobarick\u00e1\n(p = konst.)", COLORS[1]),
        (1.5, "1", "Izotermick\u00e1\n(T = konst.)", COLORS[0]),
        (2.5, "\u03ba=1,4", "Izoentropick\u00e1\n(s = konst.)", COLORS[3]),
        (4.0, "\u221e", "Izochorick\u00e1\n(v = konst.)", COLORS[2]),
    ]

    for x, n_label, name, color in ticks:
        ax.plot(x, 1, "o", color=color, markersize=12, zorder=5)
        ax.text(x, 1.35, n_label, fontsize=11, ha="center", fontweight="bold", color=color)
        ax.text(x, 0.4, name, fontsize=8, ha="center", color=color, fontweight="bold")

    fig.suptitle("Polytropick\u00fd exponent n a speci\u00e1ln\u00ed p\u0159\u00edpady",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q02_polytropic.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_pv = generate_pv_processes()
    img_ts = generate_ts_processes()
    img_poly = generate_polytropic_overview()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="2. Z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu ide\u00e1ln\u00edho plynu, rovnice zm\u011bny,\n"
              "    pr\u016fb\u011bh diagram\u016f p-v a T-s, sd\u011blen\u00e9 teplo, vykonan\u00e1 pr\u00e1ce.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Popi\u0161te z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu ide\u00e1ln\u00edho plynu (izochorick\u00e1, "
        "izobarick\u00e1, izotermick\u00e1, izoentropick\u00e1, polytropick\u00e1). Pro ka\u017edou uve\u010fte rovnici "
        "zm\u011bny, pr\u016fb\u011bh v p-v a T-s diagramech, vztahy mezi veli\u010dinami, sd\u011blen\u00e9 teplo "
        "a vykonanou pr\u00e1ci.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 P\u0159ehled zm\u011bn stavu", level=3)

    add_info_box(doc,
        "Polytropick\u00e1 zm\u011bna jako zobecn\u011bn\u00ed",
        "V\u0161echny z\u00e1kladn\u00ed zm\u011bny jsou speci\u00e1ln\u00edm p\u0159\u00edpadem polytropick\u00e9 zm\u011bny "
        "pv\u207f = konst., kde polytropick\u00fd exponent n nab\u00fdv\u00e1 specifick\u00fdch hodnot.")

    add_image(doc, img_poly, width_cm=14,
              caption="Obr. 1: Polytropick\u00fd exponent a jeho speci\u00e1ln\u00ed p\u0159\u00edpady")

    # -- Izochora --
    add_page_break(doc)
    add_heading(doc, "1.2 Izochorick\u00e1 zm\u011bna (v = konst., n \u2192 \u221e)", level=3)

    add_para(doc, "Rovnice zm\u011bny:", keep_with_next=True)
    add_equation(doc, r"v = \text{konst.} \quad \Rightarrow \quad \frac{p_1}{T_1} = \frac{p_2}{T_2}", label="1")

    add_para(doc, "Sd\u011blen\u00e9 teplo:", keep_with_next=True)
    add_equation(doc, r"q = c_v (T_2 - T_1) = \Delta u", label="2")

    add_para(doc, "Pr\u00e1ce:", keep_with_next=True)
    add_equation(doc, r"w = \int p \, dv = 0 \quad \text{(\u017e\u00e1dn\u00e1 objemov\u00e1 pr\u00e1ce!)}", label="3")

    add_para(doc,
        "Ve\u0161ker\u00e9 sd\u011blen\u00e9 teplo se spot\u0159ebuje na zm\u011bnu vnit\u0159n\u00ed energie. "
        "V p-v diagramu svisl\u00e1 p\u0159\u00edmka, v T-s exponenci\u00e1la s\u00a0vysokou strmostí.")

    # -- Izobara --
    add_heading(doc, "1.3 Izobarick\u00e1 zm\u011bna (p = konst., n = 0)", level=3)

    add_equation(doc, r"p = \text{konst.} \quad \Rightarrow \quad \frac{v_1}{T_1} = \frac{v_2}{T_2}", label="4")

    add_para(doc, "Sd\u011blen\u00e9 teplo:", keep_with_next=True)
    add_equation(doc, r"q = c_p (T_2 - T_1) = \Delta h", label="5")

    add_para(doc, "Pr\u00e1ce:", keep_with_next=True)
    add_equation(doc, r"w = p(v_2 - v_1) = r(T_2 - T_1)", label="6")

    add_para(doc, "V p-v diagramu vodorovn\u00e1 p\u0159\u00edmka, v T-s exponenci\u00e1la s men\u0161\u00ed strmostí ne\u017e izochora.")

    # -- Izoterma --
    add_page_break(doc)
    add_heading(doc, "1.4 Izotermick\u00e1 zm\u011bna (T = konst., n = 1)", level=3)

    add_equation(doc, r"T = \text{konst.} \quad \Rightarrow \quad p_1 v_1 = p_2 v_2 = \text{konst.}", label="7")

    add_para(doc, "Sd\u011blen\u00e9 teplo = pr\u00e1ce (proto\u017ee \u0394u = 0):", keep_with_next=True)
    add_equation(doc, r"q = w = r T \ln\frac{v_2}{v_1} = r T \ln\frac{p_1}{p_2}", label="8")

    add_para(doc, "V p-v rovnoosá hyperbola, v T-s vodorovn\u00e1 p\u0159\u00edmka.")

    # -- Izoentropa --
    add_heading(doc, "1.5 Izoentropick\u00e1 zm\u011bna (s = konst., n = \u03ba)", level=3)

    add_equation(doc, r"p v^\kappa = \text{konst.}, \quad \kappa = \frac{c_p}{c_v}", label="9")

    add_para(doc, "Vztahy mezi veli\u010dinami:", keep_with_next=True)
    add_equation(doc, r"\frac{T_2}{T_1} = \left(\frac{v_1}{v_2}\right)^{\kappa-1} = \left(\frac{p_2}{p_1}\right)^{\frac{\kappa-1}{\kappa}}", label="10")

    add_para(doc, "Sd\u011blen\u00e9 teplo:", keep_with_next=True)
    add_equation(doc, r"q = 0 \quad \text{(adiabatick\u00fd + vratn\u00fd d\u011bj)}", label="11")

    add_para(doc, "Pr\u00e1ce:", keep_with_next=True)
    add_equation(doc, r"w = -\Delta u = -c_v(T_2 - T_1) = \frac{p_1 v_1 - p_2 v_2}{\kappa - 1}", label="12")

    add_para(doc, "V p-v strm\u011bj\u0161\u00ed ne\u017e izoterma, v T-s svisl\u00e1 p\u0159\u00edmka.")

    # -- Polytropa --
    add_page_break(doc)
    add_heading(doc, "1.6 Polytropick\u00e1 zm\u011bna (pv\u207f = konst.)", level=3)

    add_equation(doc, r"p v^n = \text{konst.}, \quad n \in (-\infty, +\infty)", label="13")

    add_para(doc, "Vztahy:", keep_with_next=True)
    add_equation(doc, r"\frac{T_2}{T_1} = \left(\frac{v_1}{v_2}\right)^{n-1} = \left(\frac{p_2}{p_1}\right)^{\frac{n-1}{n}}", label="14")

    add_para(doc, "M\u011brn\u00e9 teplo polytropy:", keep_with_next=True)
    add_equation(doc, r"c_n = c_v \frac{\kappa - n}{1 - n}", label="15")

    add_para(doc, "Teplo a pr\u00e1ce:", keep_with_next=True)
    add_equation(doc, r"q = c_n (T_2 - T_1)", label="16")
    add_equation(doc, r"w = \frac{p_1 v_1 - p_2 v_2}{n - 1} = \frac{r(T_1 - T_2)}{n - 1}", label="17")

    # -- Diagramy --
    add_page_break(doc)
    add_heading(doc, "1.7 Diagramy p-v a T-s", level=3)

    add_image(doc, img_pv, width_cm=14,
              caption="Obr. 2: V\u0161echny z\u00e1kladn\u00ed zm\u011bny stavu v p-v diagramu (expanze z bodu 1)")

    add_image(doc, img_ts, width_cm=14,
              caption="Obr. 3: V\u0161echny z\u00e1kladn\u00ed zm\u011bny stavu v T-s diagramu (z bodu 1)")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Souhrnn\u00e1 tabulka", level=3)

    add_styled_table(doc,
        headers=["Zm\u011bna", "n", "Rovnice", "q", "w = \u222bp\u00b7dv", "p-v", "T-s"],
        data=[
            ["Izochorick\u00e1", "\u221e", "p/T = k", "c_v\u0394T", "0", "Svisl\u00e1", "Strm\u00e1 exp."],
            ["Izobarick\u00e1", "0", "v/T = k", "c_p\u0394T", "p\u0394v", "Vodorovn\u00e1", "M\u00edrn\u00e1 exp."],
            ["Izotermick\u00e1", "1", "pv = k", "rT\u00b7ln(v\u2082/v\u2081)", "= q", "Hyperbola", "Vodorovn\u00e1"],
            ["Izoentropick\u00e1", "\u03ba", "pv\u1d4b = k", "0", "\u2212c_v\u0394T", "Strm. hyp.", "Svisl\u00e1"],
            ["Polytropick\u00e1", "n", "pv\u207f = k", "c_n\u0394T", "r\u0394T/(n\u22121)", "Mezi", "Mezi"],
        ],
    )

    add_heading(doc, "2.2 Kde se zm\u011bny vyskytuj\u00ed v praxi", level=3)
    add_styled_table(doc,
        headers=["Zm\u011bna", "Praktick\u00fd p\u0159\u00edklad"],
        data=[
            ["Izochorick\u00e1", "Oh\u0159ev plynu v uzav\u0159en\u00e9 n\u00e1dob\u011b, v\u00fdbuch v\u00e1lci spalov. motoru"],
            ["Izobarick\u00e1", "Oh\u0159ev v kotli (p = konst.), spalovac\u00ed komora turbíny"],
            ["Izotermick\u00e1", "Pomal\u00e1 komprese s intenzivn\u00edm chlazením"],
            ["Izoentropick\u00e1", "Ide\u00e1ln\u00ed turb\u00edna, ide\u00e1ln\u00ed kompresor (adiabat. + vratn\u00fd)"],
            ["Polytropick\u00e1", "Skute\u010dn\u00e1 komprese/expanze (n\u011bkde mezi 1 a \u03ba)"],
        ],
    )

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Polytropick\u00e1 komprese vzduchu", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Vzduch (c_v = 718 J/(kg\u00b7K), \u03ba = 1,4, r = 287,1 J/(kg\u00b7K)) "
        "se polytropicky komprimuje z p\u2081 = 100 kPa, T\u2081 = 300 K na p\u2082 = 500 kPa. "
        "Polytropick\u00fd exponent n = 1,3. Ur\u010dete T\u2082, q, w.", bold=True)

    add_para(doc, "Krok 1: Kone\u010dn\u00e1 teplota", bold=True)
    add_equation(doc, r"T_2 = T_1 \left(\frac{p_2}{p_1}\right)^{\frac{n-1}{n}} = 300 \times \left(\frac{500}{100}\right)^{\frac{0{,}3}{1{,}3}} = 300 \times 5^{0{,}2308}")
    add_equation(doc, r"T_2 = 300 \times 1{,}451 = 435{,}3 \text{ K} = 162{,}2 \text{ \u00b0C}")

    add_para(doc, "Krok 2: M\u011brn\u00e9 teplo polytropy", bold=True)
    add_equation(doc, r"c_n = c_v \frac{\kappa - n}{1 - n} = 718 \times \frac{1{,}4 - 1{,}3}{1 - 1{,}3} = 718 \times \frac{0{,}1}{-0{,}3} = -239{,}3 \text{ J/(kg\cdot K)}")

    add_para(doc, "Krok 3: Sd\u011blen\u00e9 teplo", bold=True)
    add_equation(doc, r"q = c_n (T_2 - T_1) = -239{,}3 \times (435{,}3 - 300) = -239{,}3 \times 135{,}3 = -32\,378 \text{ J/kg}")
    add_equation(doc, r"q = -32{,}4 \text{ kJ/kg} \quad \text{(odvod tepla \u2014 chlazení kompresoru)}")

    add_para(doc, "Krok 4: Objemov\u00e1 pr\u00e1ce", bold=True)
    add_equation(doc, r"w = \frac{r(T_1 - T_2)}{n - 1} = \frac{287{,}1 \times (300 - 435{,}3)}{1{,}3 - 1} = \frac{-38\,829}{0{,}3} = -129\,430 \text{ J/kg}")
    add_equation(doc, r"w = -129{,}4 \text{ kJ/kg} \quad \text{(z\u00e1porn\u00e1 = pr\u00e1ce dodan\u00e1 soustavě)}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "T\u2082 = 435 K (162 \u00b0C) | q = \u221232,4 kJ/kg | w = \u2212129,4 kJ/kg\n\n"
        "Z\u00e1porn\u00e9 q znamen\u00e1 odvod tepla (chlazení). Z\u00e1porn\u00e9 w znamen\u00e1 dodanou pr\u00e1ci.\n"
        "Kontrola 1. z\u00e1kona: q = \u0394u + w \u2192 \u221232,4 = c_v\u0394T + w = 718\u00d7135,3/1000 + (\u2212129,4) "
        "= 97,1 \u2212 129,4 = \u221232,3 \u2714")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d je izoentropa v p-v diagramu strm\u011bj\u0161\u00ed ne\u017e izoterma?",
         "Izoentropa m\u00e1 pv\u1d4b = konst. (\u03ba \u2248 1,4), izoterma pv = konst. (n=1). "
         "Vy\u0161\u0161\u00ed exponent znamen\u00e1, \u017ee p\u0159i stejn\u00e9 zm\u011bn\u011b v kles\u00e1 tlak rychleji. "
         "Fyzik\u00e1ln\u011b: p\u0159i izoentropick\u00e9 expanzi se plyn chlad\u00ed (q=0), tak\u017ee tlak kles\u00e1 "
         "v\u00edce ne\u017e p\u0159i izotermick\u00e9 (kde se dod\u00e1v\u00e1 teplo)."),

        ("Pro\u010d je sd\u011blen\u00e9 teplo p\u0159i izochorick\u00e9 zm\u011bn\u011b rovno zm\u011bn\u011b vnit\u0159n\u00ed energie?",
         "Proto\u017ee p\u0159i v = konst. je objemov\u00e1 pr\u00e1ce w = \u222bp\u00b7dv = 0. "
         "Z prvn\u00edho z\u00e1kona: q = \u0394u + w = \u0394u + 0 = \u0394u. Ve\u0161ker\u00e9 teplo jde "
         "do vnit\u0159n\u00ed energie (teplota roste bez pr\u00e1ce)."),

        ("Co znamen\u00e1 z\u00e1porn\u00e9 m\u011brn\u00e9 teplo polytropy c_n?",
         "P\u0159i kompresi (T roste) se teplo odv\u00e1d\u00ed (q < 0). To se d\u011bje p\u0159i "
         "1 < n < \u03ba \u2014 komprese s \u010d\u00e1ste\u010dn\u00fdm chlazením. Fyzik\u00e1ln\u011b: "
         "kompresor dod\u00e1v\u00e1 pr\u00e1ci, \u010d\u00e1st jde na oh\u0159ev, \u010d\u00e1st se odv\u00e1d\u00ed chlazením."),

        ("Jak\u00e1 zm\u011bna d\u00e1v\u00e1 nejmen\u0161\u00ed kompresi\u00f3n pr\u00e1ci a pro\u010d?",
         "Izotermick\u00e1 (n=1). P\u0159i izoterm\u011b se v\u0161echna pr\u00e1ce p\u0159em\u011bn\u00ed na teplo, "
         "kter\u00e9 se odv\u00e1d\u00ed \u2014 neoh\u0159\u00edv\u00e1 se plyn. Proto je plocha pod k\u0159ivkou "
         "v p-v nejmen\u0161\u00ed. V praxi se p\u0159ibli\u017eujeme v\u00edcestup\u0148ovou kompres\u00ed s\u00a0chlazením."),

        ("Pro\u010d je p\u0159i izobarick\u00e9 zm\u011bn\u011b sd\u011blen\u00e9 teplo rovno zm\u011bn\u011b entalpie?",
         "Z tvaru 1. z\u00e1kona pro otev\u0159enou soustavu: \u03b4q = dh \u2212 v\u00b7dp. "
         "P\u0159i p = konst. je dp = 0, tedy \u03b4q = dh. Entalpie h = u + pv "
         "zahrnuje i pr\u00e1ci na vytla\u010den\u00ed (p\u00b7dv), proto q = \u0394h = c_p\u0394T."),

        ("Vysv\u011btlete, pro\u010d v T-s diagramu izochora b\u011b\u017e\u00ed strm\u011bji ne\u017e izobara.",
         "Sklon dT/ds = T/c. Pro izochoru c = c_v, pro izobaru c = c_p. "
         "Proto\u017ee c_p > c_v (poměr = \u03ba), izobara m\u00e1 men\u0161\u00ed sklon \u2014 "
         "p\u0159i stejn\u00e9 zm\u011bn\u011b T se entropie zm\u011bn\u00ed v\u00edce."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "\u010cengel, Y.A., Boles, M.A.: Thermodynamics \u2014 An Engineering Approach")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "No\u017ei\u010dka, J.: Technick\u00e1 termomechanika, \u010cVUT Praha")
    add_bullet(doc, "Moran, M.J. et al.: Fundamentals of Engineering Thermodynamics")
    add_bullet(doc, "Kousal, M.: P\u0159\u00edklady z technick\u00e9 termomechaniky", is_last=True)

    save_and_export(doc, "02-vratne-zmeny")


if __name__ == "__main__":
    generate()
