# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 3: Tepeln\u00e9 ob\u011bhy, p\u0159iveden\u00e9 a odveden\u00e9 teplo, expanzn\u00ed
a kompresn\u00ed pr\u00e1ce, termick\u00e1 \u00fa\u010dinnost. Ob\u011bhy p\u0159\u00edm\u00e9 a obr\u00e1cen\u00e9.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

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

def generate_direct_cycle_pv_ts():
    """Direct (clockwise) cycle in p-v and T-s diagrams."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Generic direct cycle (clockwise in p-v)
    theta = np.linspace(0, 2 * np.pi, 200)
    # Elliptical cycle
    v_c = 0.5 + 0.3 * np.cos(theta)
    p_c = 300 + 150 * np.sin(theta)

    ax1.plot(v_c, p_c, color=COLORS[0], linewidth=2.5)
    ax1.fill(v_c, p_c, alpha=0.1, color=COLORS[0])
    # Arrows for direction (clockwise)
    idx = 50
    ax1.annotate("", xy=(v_c[idx], p_c[idx]), xytext=(v_c[idx-5], p_c[idx-5]),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=2))
    idx = 150
    ax1.annotate("", xy=(v_c[idx], p_c[idx]), xytext=(v_c[idx-5], p_c[idx-5]),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=2))

    ax1.text(0.5, 300, "$W_{net} > 0$\n(po sm\u011bru\nhod. ru\u010di\u010dek)", ha="center", va="center",
             fontsize=10, fontweight="bold", color=COLORS[0])
    ax1.set_xlabel("M\u011brn\u00fd objem v", fontsize=11)
    ax1.set_ylabel("Tlak p", fontsize=11)
    ax1.set_title("P\u0158\u00cdM\u00dd OB\u011aH v p-v\n(tepeln\u00fd stroj)", fontsize=12, fontweight="bold")

    # T-s diagram (clockwise = direct)
    s_c = 200 + 150 * np.cos(theta)
    T_c = 500 + 100 * np.sin(theta)

    ax2.plot(s_c, T_c, color=COLORS[1], linewidth=2.5)
    ax2.fill(s_c, T_c, alpha=0.1, color=COLORS[1])
    idx = 50
    ax2.annotate("", xy=(s_c[idx], T_c[idx]), xytext=(s_c[idx-5], T_c[idx-5]),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=2))

    # Q_in (upper) and Q_out (lower)
    ax2.text(200, 620, "$q_{in}$ (plocha pod horn\u00ed \u010d\u00e1st\u00ed)", fontsize=9,
             color="#DC2626", fontweight="bold", ha="center")
    ax2.text(200, 380, "$q_{out}$ (plocha pod doln\u00ed \u010d\u00e1st\u00ed)", fontsize=9,
             color="#2563EB", fontweight="bold", ha="center")
    ax2.text(200, 500, "$w_{net}$\n= plocha\ncyklu", fontsize=10,
             fontweight="bold", color=COLORS[1], ha="center")

    ax2.set_xlabel("M\u011brn\u00e1 entropie s", fontsize=11)
    ax2.set_ylabel("Teplota T", fontsize=11)
    ax2.set_title("P\u0158\u00cdM\u00dd OB\u011aH v T-s\n$w_{net} = q_{in} - q_{out}$", fontsize=12, fontweight="bold")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q03_direct_cycle.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_reverse_cycle():
    """Reverse (counter-clockwise) cycle schema."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Hot reservoir (top)
    h = FancyBboxPatch((2, 5.5), 4, 0.8, boxstyle="round,pad=0.1",
                        facecolor="#FEE2E2", edgecolor="#DC2626", lw=2)
    ax.add_patch(h)
    ax.text(4, 5.9, "Hork\u00fd z\u00e1sobn\u00edk $T_H$", ha="center", fontsize=11,
            fontweight="bold", color="#DC2626")

    # Cold reservoir (bottom)
    c = FancyBboxPatch((2, 0.5), 4, 0.8, boxstyle="round,pad=0.1",
                        facecolor="#DBEAFE", edgecolor="#2563EB", lw=2)
    ax.add_patch(c)
    ax.text(4, 0.9, "Studen\u00fd z\u00e1sobn\u00edk $T_C$", ha="center", fontsize=11,
            fontweight="bold", color="#2563EB")

    # Left: Heat pump
    bp = FancyBboxPatch((0.3, 2.5), 3, 2, boxstyle="round,pad=0.15",
                         facecolor="#DCFCE7", edgecolor="#16A34A", lw=2)
    ax.add_patch(bp)
    ax.text(1.8, 3.5, "TEPELN\u00c9\n\u010cERPADLO", ha="center", fontsize=10,
            fontweight="bold", color="#16A34A")

    # Q_C in (from cold)
    ax.annotate("", xy=(1.8, 2.5), xytext=(1.8, 1.3),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2))
    ax.text(0.8, 1.8, "$Q_C$", fontsize=12, fontweight="bold", color="#2563EB")
    # Q_H out (to hot)
    ax.annotate("", xy=(1.8, 5.5), xytext=(1.8, 4.5),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2))
    ax.text(0.8, 5, "$Q_H$", fontsize=12, fontweight="bold", color="#DC2626")
    # W in
    ax.annotate("", xy=(0.3, 3.5), xytext=(-0.3, 3.5),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=2))
    ax.text(-0.5, 3.9, "$W$", fontsize=12, fontweight="bold", color="#16A34A")

    # Right: Refrigerator
    br = FancyBboxPatch((4.7, 2.5), 3, 2, boxstyle="round,pad=0.15",
                         facecolor="#F3E8FF", edgecolor="#7C3AED", lw=2)
    ax.add_patch(br)
    ax.text(6.2, 3.5, "CHLADI\u010cKA", ha="center", fontsize=10,
            fontweight="bold", color="#7C3AED")

    # Arrows
    ax.annotate("", xy=(6.2, 2.5), xytext=(6.2, 1.3),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2))
    ax.text(7, 1.8, "$Q_C$", fontsize=12, fontweight="bold", color="#2563EB")
    ax.annotate("", xy=(6.2, 5.5), xytext=(6.2, 4.5),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2))
    ax.text(7, 5, "$Q_H$", fontsize=12, fontweight="bold", color="#DC2626")
    ax.annotate("", xy=(7.7, 3.5), xytext=(8.3, 3.5),
                arrowprops=dict(arrowstyle="-|>", color="#7C3AED", lw=2))
    ax.text(8.5, 3.9, "$W$", fontsize=12, fontweight="bold", color="#7C3AED")

    # COP labels
    ax.text(1.8, 2.2, "$COP_{T\u010c} = Q_H/W$", fontsize=8, ha="center",
            fontweight="bold", color="#16A34A")
    ax.text(6.2, 2.2, "$COP_{ch} = Q_C/W$", fontsize=8, ha="center",
            fontweight="bold", color="#7C3AED")

    fig.suptitle("Obr\u00e1cen\u00e9 ob\u011bhy: tepeln\u00e9 \u010derpadlo a chladi\u010dka",
                 fontsize=12, fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q03_reverse_cycle.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_efficiency_comparison():
    """Thermal efficiency vs temperature ratio for Carnot cycle."""
    fig, ax = plt.subplots(figsize=(7, 5))

    T_C = 300  # K (27 C)
    T_H = np.linspace(310, 1500, 200)
    eta_C = (1 - T_C / T_H) * 100

    ax.plot(T_H - 273.15, eta_C, color=COLORS[0], linewidth=2.5, label="$\\eta_C = 1 - T_C/T_H$")

    # Mark typical ranges
    ranges = [
        (300, 500, "Tepeln\u00e9\n\u010derpadlo", COLORS[2]),
        (500, 900, "Parn\u00ed\nturbina", COLORS[1]),
        (900, 1400, "Plynov\u00e1\nturbina", COLORS[3]),
    ]
    for t_lo, t_hi, label, color in ranges:
        eta_lo = (1 - T_C / (t_lo + 273.15)) * 100
        eta_hi = (1 - T_C / (t_hi + 273.15)) * 100
        ax.fill_between([t_lo, t_hi], eta_lo, eta_hi, alpha=0.15, color=color)
        ax.text((t_lo + t_hi) / 2, (eta_lo + eta_hi) / 2, label, fontsize=8,
                ha="center", fontweight="bold", color=color)

    ax.set_xlabel("Teplota hork\u00e9ho z\u00e1sobn\u00edku $T_H$ [\u00b0C]", fontsize=11)
    ax.set_ylabel("Carnotova \u00fa\u010dinnost $\\eta_C$ [%]", fontsize=11)
    ax.set_title("Carnotova \u00fa\u010dinnost v z\u00e1vislosti na $T_H$ ($T_C$ = 27 \u00b0C)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(0, 1300)
    ax.set_ylim(0, 85)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q03_efficiency.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_direct = generate_direct_cycle_pv_ts()
    img_reverse = generate_reverse_cycle()
    img_eff = generate_efficiency_comparison()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="3. Tepeln\u00e9 ob\u011bhy, p\u0159iveden\u00e9 a odveden\u00e9 teplo, expanzn\u00ed a kompresn\u00ed\n"
              "    pr\u00e1ce, termick\u00e1 \u00fa\u010dinnost. Ob\u011bhy p\u0159\u00edm\u00e9 a obr\u00e1cen\u00e9.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Vysv\u011btlete pojem tepeln\u00e9ho ob\u011bhu (cyklu). Definujte p\u0159iveden\u00e9 a odveden\u00e9 teplo, "
        "expanzn\u00ed a kompresn\u00ed pr\u00e1ci, termickou \u00fa\u010dinnost. Rozli\u0161te p\u0159\u00edm\u00e9 ob\u011bhy "
        "(tepeln\u00e9 stroje) a obr\u00e1cen\u00e9 ob\u011bhy (chladi\u010dky, tepeln\u00e1 \u010derpadla).")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Tepeln\u00fd ob\u011bh (cyklus)", level=3)

    add_info_box(doc,
        "Definice: Tepeln\u00fd ob\u011bh",
        "Uzav\u0159en\u00e1 posloupnost termodynamick\u00fdch zm\u011bn stavu, po kter\u00e9 se pracovn\u00ed "
        "l\u00e1tka vr\u00e1t\u00ed do v\u00fdchoz\u00edho stavu. Proto\u017ee v\u0161echny stavov\u00e9 veli\u010diny "
        "jsou op\u011bt stejn\u00e9: \u0394u = 0, \u0394h = 0, \u0394s = 0.")

    add_para(doc, "D\u016fsledek (\u0394u = 0) z 1. z\u00e1kona:", keep_with_next=True)
    add_equation(doc, r"q_{net} = w_{net} \quad \Rightarrow \quad q_{in} - q_{out} = w_{exp} - w_{komp}", label="1")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "q_{in} \u2014 teplo p\u0159iveden\u00e9 pracovn\u00ed l\u00e1tce (z hork\u00e9ho z\u00e1sobn\u00edku)")
    add_bullet(doc, "q_{out} \u2014 teplo odveden\u00e9 (do studen\u00e9ho z\u00e1sobn\u00edku)")
    add_bullet(doc, "w_{exp} \u2014 expanzn\u00ed pr\u00e1ce (konan\u00e1 pracovn\u00ed l\u00e1tkou)")
    add_bullet(doc, "w_{komp} \u2014 kompresn\u00ed pr\u00e1ce (dodan\u00e1 pracovn\u00ed l\u00e1tce)", is_last=True)

    # -- 1.2 Primy obeh --
    add_page_break(doc)
    add_heading(doc, "1.2 P\u0159\u00edm\u00fd ob\u011bh (tepeln\u00fd stroj)", level=3)

    add_info_box(doc,
        "P\u0159\u00edm\u00fd ob\u011bh",
        "Ob\u011bh prob\u00edh\u00e1 ve sm\u011bru hodinov\u00fdch ru\u010di\u010dek v p-v diagramu.\n"
        "w_{net} > 0 \u2014 stroj koná pr\u00e1ci.\n"
        "P\u0159\u00edklady: parn\u00ed turbina, spalovac\u00ed motor, plynov\u00e1 turbina.")

    add_image(doc, img_direct, width_cm=14,
              caption="Obr. 1: P\u0159\u00edm\u00fd ob\u011bh v p-v a T-s diagramech \u2014 plocha = \u010dist\u00e1 pr\u00e1ce")

    add_para(doc, "Termick\u00e1 \u00fa\u010dinnost:", bold=True, keep_with_next=True)
    add_equation(doc, r"\eta_t = \frac{w_{net}}{q_{in}} = \frac{q_{in} - q_{out}}{q_{in}} = 1 - \frac{q_{out}}{q_{in}}", label="2")

    add_para(doc, "V\u017edy plat\u00ed \u03b7_t < 1 (druh\u00fd z\u00e1kon TD: q_{out} > 0).")

    add_para(doc, "Maxim\u00e1ln\u00ed \u00fa\u010dinnost \u2014 Carnot\u016fv ob\u011bh:", keep_with_next=True)
    add_equation(doc, r"\eta_C = 1 - \frac{T_C}{T_H}", label="3")

    add_image(doc, img_eff, width_cm=13,
              caption="Obr. 2: Carnotova \u00fa\u010dinnost v z\u00e1vislosti na teplot\u011b hork\u00e9ho z\u00e1sobn\u00edku")

    # -- 1.3 Obraceny obeh --
    add_page_break(doc)
    add_heading(doc, "1.3 Obr\u00e1cen\u00fd ob\u011bh (chladi\u010dka, tepeln\u00e9 \u010derpadlo)", level=3)

    add_info_box(doc,
        "Obr\u00e1cen\u00fd ob\u011bh",
        "Ob\u011bh prob\u00edh\u00e1 proti sm\u011bru hodinov\u00fdch ru\u010di\u010dek v p-v diagramu.\n"
        "w_{net} < 0 \u2014 stroji se dod\u00e1v\u00e1 pr\u00e1ce.\n"
        "Teplo se p\u0159en\u00e1\u0161\u00ed z ni\u017e\u0161\u00ed teploty na vy\u0161\u0161\u00ed (proti p\u0159irozen\u00e9mu sm\u011bru).")

    add_image(doc, img_reverse, width_cm=13,
              caption="Obr. 3: Obr\u00e1cen\u00e9 ob\u011bhy \u2014 tepeln\u00e9 \u010derpadlo a chladi\u010dka")

    add_para(doc, "Bilance energie:", keep_with_next=True)
    add_equation(doc, r"Q_H = Q_C + W", label="4")

    add_para(doc, "Chladicí faktor (COP chladi\u010dky):", bold=True, keep_with_next=True)
    add_equation(doc, r"\varepsilon_{ch} = COP_{ch} = \frac{Q_C}{W} = \frac{Q_C}{Q_H - Q_C}", label="5")

    add_para(doc, "Topn\u00fd faktor (COP tepeln\u00e9ho \u010derpadla):", bold=True, keep_with_next=True)
    add_equation(doc, r"\varepsilon_{T\check{C}} = COP_{T\check{C}} = \frac{Q_H}{W} = \frac{Q_H}{Q_H - Q_C}", label="6")

    add_para(doc, "Vztah mezi COP:", keep_with_next=True)
    add_equation(doc, r"COP_{T\check{C}} = COP_{ch} + 1", label="7")

    add_para(doc, "Maxim\u00e1ln\u00ed COP (Carnot):", keep_with_next=True)
    add_equation(doc, r"COP_{ch,C} = \frac{T_C}{T_H - T_C}, \quad COP_{T\check{C},C} = \frac{T_H}{T_H - T_C}", label="8")

    add_warning_box(doc,
        "COP m\u016f\u017ee b\u00fdt v\u011bt\u0161\u00ed ne\u017e 1! Nap\u0159. tepeln\u00e9 \u010derpadlo s COP = 4 dod\u00e1 4 kW tepla "
        "za 1 kW elektrick\u00e9 energie. To nen\u00ed poru\u0161en\u00ed z\u00e1kona zachov\u00e1n\u00ed energie \u2014 "
        "3 kW se odeberou z okol\u00ed (vzduch, zem\u011b, voda).")

    # -- 1.4 Srovnani --
    add_page_break(doc)
    add_heading(doc, "1.4 Srovn\u00e1n\u00ed p\u0159\u00edm\u00e9ho a obr\u00e1cen\u00e9ho ob\u011bhu", level=3)

    add_styled_table(doc,
        headers=["Vlastnost", "P\u0159\u00edm\u00fd ob\u011bh", "Obr\u00e1cen\u00fd ob\u011bh"],
        data=[
            ["Sm\u011br v p-v", "Po hodinov\u00fdch ru\u010di\u010dk\u00e1ch", "Proti hodinov\u00fdm ru\u010di\u010dk\u00e1m"],
            ["\u010cist\u00e1 pr\u00e1ce", "w_{net} > 0 (v\u00fdrob\u00ed)", "w_{net} < 0 (spot\u0159ebuje)"],
            ["Tok tepla", "T_H \u2192 stroj \u2192 T_C", "T_C \u2192 stroj \u2192 T_H"],
            ["\u00da\u010dinnost/COP", "\u03b7 = w/q_{in} < 1", "COP = Q/W > 1 (mo\u017en\u00e9)"],
            ["P\u0159\u00edklady", "Turb\u00edna, spalov. motor", "Chladi\u010dka, klima, T\u010c"],
        ],
    )

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 P\u0159\u00edm\u00e9 ob\u011bhy v praxi", level=3)
    add_styled_table(doc,
        headers=["Ob\u011bh", "Pracovn\u00ed l\u00e1tka", "\u03b7_t [%]", "Aplikace"],
        data=[
            ["Carnot\u016fv", "Ide\u00e1ln\u00ed", "Max. (ref.)", "Teoretick\u00fd"],
            ["Rankine\u016fv", "Voda/p\u00e1ra", "33\u201345", "Parn\u00ed elektr\u00e1rny"],
            ["Otto (v\u00fdbuch.)", "Vzduch", "25\u201335", "Z\u00e1\u017ehov\u00e9 motory"],
            ["Diesel (rovnotl.)", "Vzduch", "30\u201340", "Vzn\u011btov\u00e9 motory"],
            ["Brayton\u016fv", "Vzduch", "30\u201340", "Plynov\u00e9 turb\u00edny"],
            ["Kombinovan\u00fd", "P\u00e1ra + vzduch", "55\u201362", "Paroplyn. el."],
        ],
    )

    add_heading(doc, "2.2 Obr\u00e1cen\u00e9 ob\u011bhy v praxi", level=3)
    add_styled_table(doc,
        headers=["Za\u0159\u00edzen\u00ed", "Pracovn\u00ed l\u00e1tka", "COP", "Pou\u017eit\u00ed"],
        data=[
            ["Kompresorov\u00e1 chladi\u010dka", "R134a, R410A", "2\u20134", "Dom\u00e1cnost, pr\u016fmysl"],
            ["Tepeln\u00e9 \u010derpadlo vzduch-voda", "R410A, R32", "3\u20135", "Vyt\u00e1p\u011bn\u00ed budov"],
            ["Tepeln\u00e9 \u010derpadlo zem\u011b-voda", "R407C", "4\u20136", "N\u00edzkoenergetick\u00e9 domy"],
            ["Absorp\u010dn\u00ed chladi\u010dka", "NH\u2083/H\u2082O", "0,6\u20131,2", "Odpadn\u00ed teplo"],
        ],
    )

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Porovn\u00e1n\u00ed tepeln\u00e9ho stroje a tepeln\u00e9ho \u010derpadla", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Carnot\u016fv ob\u011bh pracuje mezi T_H = 600 K a T_C = 300 K. "
        "a) Ur\u010dete \u03b7 p\u0159\u00edm\u00e9ho ob\u011bhu. "
        "b) Ur\u010dete COP obr\u00e1cen\u00e9ho ob\u011bhu jako chladi\u010dky a jako tepeln\u00e9ho \u010derpadla.",
        bold=True)

    add_para(doc, "a) P\u0159\u00edm\u00fd ob\u011bh (\u03b7):", bold=True)
    add_equation(doc, r"\eta_C = 1 - \frac{T_C}{T_H} = 1 - \frac{300}{600} = 0{,}50 = 50 \%")

    add_para(doc, "b) Obr\u00e1cen\u00fd ob\u011bh (COP):", bold=True)
    add_equation(doc, r"COP_{ch} = \frac{T_C}{T_H - T_C} = \frac{300}{600 - 300} = \frac{300}{300} = 1{,}0")
    add_equation(doc, r"COP_{T\check{C}} = \frac{T_H}{T_H - T_C} = \frac{600}{300} = 2{,}0")

    add_para(doc, "Kontrola:", bold=True)
    add_equation(doc, r"COP_{T\check{C}} = COP_{ch} + 1 = 1{,}0 + 1 = 2{,}0 \quad \checkmark")

    add_info_box(doc,
        "V\u00fdsledky:",
        "P\u0159\u00edm\u00fd ob\u011bh: \u03b7 = 50 % (polovina tepla se p\u0159em\u011bn\u00ed na pr\u00e1ci)\n"
        "Chladi\u010dka: COP = 1,0 (na 1 J pr\u00e1ce odebere 1 J tepla z chlazen\u00e9ho prostoru)\n"
        "Tepeln\u00e9 \u010derpadlo: COP = 2,0 (na 1 J pr\u00e1ce dod\u00e1 2 J tepla do vyt\u00e1p\u011bn\u00e9ho prostoru)\n\n"
        "Pozn.: COP_{T\u010c} = 2,0 znamen\u00e1, \u017ee 50 % tepla je z pr\u00e1ce a 50 % z okol\u00ed.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d je \u010dist\u00e1 pr\u00e1ce ob\u011bhu rovna rozd\u00edlu q_{in} \u2212 q_{out}?",
         "Proto\u017ee v ob\u011bhu se pracovn\u00ed l\u00e1tka vrac\u00ed do v\u00fdchoz\u00edho stavu: "
         "\u0394u = 0. Z 1. z\u00e1kona: q = \u0394u + w, po ob\u011bhu: q_{net} = w_{net}. "
         "A q_{net} = q_{in} \u2212 q_{out}. Plocha cyklu v p-v nebo T-s p\u0159edstavuje w_{net}."),

        ("Pro\u010d je COP tepeln\u00e9ho \u010derpadla v\u017edy COP_{ch} + 1?",
         "Z bilance Q_H = Q_C + W: COP_{T\u010c} = Q_H/W = (Q_C + W)/W = Q_C/W + 1 "
         "= COP_{ch} + 1. Tepeln\u00e9 \u010derpadlo dod\u00e1v\u00e1 v\u00edce tepla ne\u017e chladi\u010dka, "
         "proto\u017ee k odebran\u00e9mu teplu Q_C p\u0159id\u00e1v\u00e1 je\u0161t\u011b pr\u00e1ci W."),

        ("M\u016f\u017ee COP p\u0159ekro\u010dit 1? Nen\u00ed to poru\u0161en\u00ed z\u00e1kona zachov\u00e1n\u00ed energie?",
         "Ano, COP > 1 je b\u011b\u017en\u00e9 (T\u010c: COP = 3\u20135). Nen\u00ed to poru\u0161en\u00ed \u2014 "
         "tepeln\u00e9 \u010derpadlo neVYR\u00c1B\u00cd energii, jen ji P\u0158ESOUVÁ z okol\u00ed (T_C) "
         "na vy\u0161\u0161\u00ed \u00farove\u0148 (T_H). Pr\u00e1ce W slou\u017e\u00ed jen k pohonu tohoto p\u0159esunu."),

        ("Jak\u00fd je rozd\u00edl mezi expanzn\u00ed a kompresn\u00ed prac\u00ed v ob\u011bhu?",
         "Expanzn\u00ed pr\u00e1ce: pracovn\u00ed l\u00e1tka kon\u00e1 pr\u00e1ci (v roste, w > 0). "
         "Kompresn\u00ed pr\u00e1ce: pr\u00e1ce se dod\u00e1v\u00e1 pracovn\u00ed l\u00e1tce (v kles\u00e1, w < 0). "
         "U p\u0159\u00edm\u00e9ho ob\u011bhu: w_{exp} > w_{komp}, rozd\u00edl = w_{net} > 0."),

        ("Pro\u010d je Carnot\u016fv ob\u011bh prakticky nerealizovateln\u00fd?",
         "Vy\u017eaduje izotermick\u00fd p\u0159\u00edvod a odvod tepla (nekone\u010dn\u011b pomal\u00fd) "
         "a izoentropick\u00e9 d\u011bje (bezeztr\u00e1tov\u00e9). V praxi existuje t\u0159en\u00ed, "
         "kone\u010dn\u00e9 teplotn\u00ed rozd\u00edly pro p\u0159enos tepla a jin\u00e9 nevratnosti."),

        ("Jak pozn\u00e1te z T-s diagramu, \u017ee ob\u011bh je p\u0159\u00edm\u00fd nebo obr\u00e1cen\u00fd?",
         "P\u0159\u00edm\u00fd: sm\u011br po hodinov\u00fdch ru\u010di\u010dk\u00e1ch (v T-s: teplo p\u0159ij\u00edm\u00e1 naho\u0159e, "
         "odv\u00e1d\u00ed dole). Obr\u00e1cen\u00fd: proti sm\u011bru (teplo p\u0159ij\u00edm\u00e1 dole, odv\u00e1d\u00ed naho\u0159e). "
         "Plocha cyklu = |w_{net}| v obou p\u0159\u00edpadech."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "\u010cengel, Y.A., Boles, M.A.: Thermodynamics \u2014 An Engineering Approach")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "No\u017ei\u010dka, J.: Technick\u00e1 termomechanika, \u010cVUT Praha")
    add_bullet(doc, "Moran, M.J. et al.: Fundamentals of Engineering Thermodynamics")
    add_bullet(doc, "\u010cSN EN 14511 \u2014 Tepeln\u00e1 \u010derpadla, podm\u00ednky zkou\u0161en\u00ed", is_last=True)

    save_and_export(doc, "03-tepelne-obehy")


if __name__ == "__main__":
    generate()
