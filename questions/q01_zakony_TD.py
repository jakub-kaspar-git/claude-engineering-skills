# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 1: Prvn\u00ed z\u00e1kon termomechaniky dva z\u00e1kladn\u00ed tvary.
Druh\u00fd z\u00e1kon termodynamiky. Zm\u011bna entropie. Diagram T-s.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

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

def generate_first_law_schema():
    """Schematic of first law for closed and open systems."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Closed system
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 5)
    ax1.axis("off")
    box = FancyBboxPatch((1, 1), 4, 3, boxstyle="round,pad=0.2",
                          facecolor="#E8F0FE", edgecolor="#2563EB", lw=2.5)
    ax1.add_patch(box)
    ax1.text(3, 2.5, "SOUSTAVA\n(uzav\u0159en\u00e1)\nU, m = konst.", ha="center", va="center",
             fontsize=11, fontweight="bold", color="#2563EB")
    # Q arrow in
    ax1.annotate("", xy=(3, 4), xytext=(3, 4.8),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2.5))
    ax1.text(3, 4.9, "Q (teplo)", ha="center", fontsize=10, fontweight="bold", color="#DC2626")
    # W arrow out
    ax1.annotate("", xy=(5.5, 2.5), xytext=(5, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=2.5))
    ax1.text(5.8, 2.5, "W\n(pr\u00e1ce)", ha="center", va="center", fontsize=10,
             fontweight="bold", color="#16A34A")
    ax1.set_title("Uzav\u0159en\u00e1 soustava\nQ = \u0394U + W", fontsize=12, fontweight="bold")

    # Open system
    ax2.set_xlim(0, 8)
    ax2.set_ylim(0, 5)
    ax2.axis("off")
    box2 = FancyBboxPatch((2, 1), 4, 3, boxstyle="round,pad=0.2",
                           facecolor="#FEF3C7", edgecolor="#D97706", lw=2.5)
    ax2.add_patch(box2)
    ax2.text(4, 2.5, "KONTROLN\u00cd\nOBJEM\n(otev\u0159en\u00fd)", ha="center", va="center",
             fontsize=11, fontweight="bold", color="#D97706")
    # Mass in
    ax2.annotate("", xy=(2, 2.5), xytext=(0.5, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2.5))
    ax2.text(0.3, 3, "m\u0307\u2081, h\u2081", fontsize=9, fontweight="bold", color="#2563EB")
    # Mass out
    ax2.annotate("", xy=(7.5, 2.5), xytext=(6, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2.5))
    ax2.text(7.5, 3, "m\u0307\u2082, h\u2082", fontsize=9, fontweight="bold", color="#2563EB")
    # Q
    ax2.annotate("", xy=(4, 4), xytext=(4, 4.8),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2))
    ax2.text(4, 4.9, "Q\u0307", fontsize=10, fontweight="bold", color="#DC2626", ha="center")
    # W
    ax2.annotate("", xy=(6.5, 4), xytext=(6, 4),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=2))
    ax2.text(7, 4, "P", fontsize=10, fontweight="bold", color="#16A34A")
    ax2.set_title("Otev\u0159en\u00e1 soustava (stacion\u00e1rn\u00ed)\nQ\u0307 = m\u0307(h\u2082\u2212h\u2081) + P", fontsize=12, fontweight="bold")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q01_first_law.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_ts_processes():
    """T-s diagram with basic reversible processes for ideal gas."""
    fig, ax = plt.subplots(figsize=(9, 6))

    R = 287.1  # J/(kg*K) for air
    cv = 718  # J/(kg*K)
    cp = 1005
    kappa = cp / cv

    T1, p1 = 300, 100e3  # initial state
    s1 = 0  # reference

    # Isothermal (T = const)
    s_iso = np.linspace(s1, 600, 100)
    T_iso = np.full_like(s_iso, T1)
    ax.plot(s_iso, T_iso, color=COLORS[0], linewidth=2.5, label="Izotermick\u00e1 (T = konst.)")

    # Isobaric (p = const) from state 1
    T_izob = np.linspace(T1, 550, 100)
    s_izob = cp * np.log(T_izob / T1)
    ax.plot(s_izob, T_izob, color=COLORS[1], linewidth=2.5, label="Izobarick\u00e1 (p = konst.)")

    # Isochoric (v = const) from state 1
    T_izoch = np.linspace(T1, 550, 100)
    s_izoch = cv * np.log(T_izoch / T1)
    ax.plot(s_izoch, T_izoch, color=COLORS[2], linewidth=2.5, label="Izochorick\u00e1 (v = konst.)")

    # Isentropic (s = const) from state 1
    ax.axvline(x=s1, color=COLORS[3], linewidth=2.5, linestyle="-", label="Izoentropick\u00e1 (s = konst.)")

    # Polytropic (n = 1.3) from state 1
    T_poly = np.linspace(T1, 500, 100)
    n_poly = 1.3
    c_n = cv * (n_poly - kappa) / (n_poly - 1)
    s_poly = c_n * np.log(T_poly / T1)
    ax.plot(s_poly, T_poly, color="#7C3AED", linewidth=2.5, linestyle="--",
            label="Polytropick\u00e1 (n = 1,3)")

    # Mark initial state
    ax.plot(s1, T1, "ko", markersize=10, zorder=5)
    ax.annotate("Bod 1\n(p\u2081, T\u2081, v\u2081)", xy=(s1, T1), xytext=(50, T1 - 40),
                fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", lw=1.5))

    # Area annotations
    ax.fill_between(s_izob, T1, T_izob, alpha=0.05, color=COLORS[1])
    ax.text(200, 500, "q = plocha\npod k\u0159ivkou", fontsize=9, style="italic", color="#555")

    ax.set_xlabel("M\u011brn\u00e1 entropie s [J/(kg\u00b7K)]", fontsize=11)
    ax.set_ylabel("Teplota T [K]", fontsize=11)
    ax.set_title("T-s diagram: z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu ide\u00e1ln\u00edho plynu",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, loc="upper left")
    ax.set_xlim(-100, 700)
    ax.set_ylim(200, 600)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q01_ts_processes.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_second_law_schema():
    """Clausius and Kelvin-Planck statements visualization."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    for ax in [ax1, ax2]:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.axis("off")

    # Kelvin-Planck: impossible to convert heat entirely to work
    ax1.set_title("Kelvin-Planck\u016fv v\u00fdrok", fontsize=11, fontweight="bold")
    # Hot reservoir
    h1 = FancyBboxPatch((1, 4.5), 4, 0.8, boxstyle="round,pad=0.1",
                         facecolor="#FEE2E2", edgecolor="#DC2626", lw=2)
    ax1.add_patch(h1)
    ax1.text(3, 4.9, "Hork\u00fd z\u00e1sobn\u00edk T\u2095", ha="center", fontsize=10,
             fontweight="bold", color="#DC2626")
    # Engine
    e1 = FancyBboxPatch((1.5, 2.2), 3, 1.5, boxstyle="round,pad=0.15",
                         facecolor="#E8F0FE", edgecolor="#2563EB", lw=2)
    ax1.add_patch(e1)
    ax1.text(3, 3, "TEPELN\u00dd\nSTROJ", ha="center", fontsize=11, fontweight="bold", color="#2563EB")
    # Q_H in
    ax1.annotate("", xy=(3, 3.7), xytext=(3, 4.5),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2))
    ax1.text(3.5, 4.1, "Q\u2095", fontsize=11, fontweight="bold", color="#DC2626")
    # W out
    ax1.annotate("", xy=(5.5, 3), xytext=(4.5, 3),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=2))
    ax1.text(5.6, 3, "W = Q\u2095 ?", fontsize=10, fontweight="bold", color="#16A34A")
    # Big X
    ax1.text(3, 1.2, "NELZE! (\u03b7 = 100 %)", fontsize=12, fontweight="bold",
             color="#DC2626", ha="center",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEE2E2", edgecolor="#DC2626"))

    # Clausius: heat cannot flow from cold to hot spontaneously
    ax2.set_title("Clausi\u016fv v\u00fdrok", fontsize=11, fontweight="bold")
    # Cold
    c2 = FancyBboxPatch((1, 0.5), 4, 0.8, boxstyle="round,pad=0.1",
                         facecolor="#DBEAFE", edgecolor="#2563EB", lw=2)
    ax2.add_patch(c2)
    ax2.text(3, 0.9, "Studen\u00fd z\u00e1sobn\u00edk T\u2097", ha="center", fontsize=10,
             fontweight="bold", color="#2563EB")
    # Hot
    h2 = FancyBboxPatch((1, 4.5), 4, 0.8, boxstyle="round,pad=0.1",
                         facecolor="#FEE2E2", edgecolor="#DC2626", lw=2)
    ax2.add_patch(h2)
    ax2.text(3, 4.9, "Hork\u00fd z\u00e1sobn\u00edk T\u2095", ha="center", fontsize=10,
             fontweight="bold", color="#DC2626")
    # Q arrow from cold to hot
    ax2.annotate("", xy=(3, 4.5), xytext=(3, 1.3),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2.5))
    ax2.text(3.8, 3, "Q ?", fontsize=12, fontweight="bold", color="#D97706")
    # Big X
    ax2.text(3, 2.2, "NELZE\n(bez pr\u00e1ce)!", fontsize=11, fontweight="bold",
             color="#DC2626", ha="center",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEE2E2", edgecolor="#DC2626"))

    fig.suptitle("Druh\u00fd z\u00e1kon termodynamiky \u2014 dva ekvivalentn\u00ed v\u00fdroky",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q01_second_law.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_carnot_ts():
    """Carnot cycle in T-s diagram."""
    fig, ax = plt.subplots(figsize=(7, 5))

    T_H, T_C = 500, 300  # K
    s1, s2 = 100, 500  # J/(kg*K)

    # Cycle: 1->2 isothermal expansion, 2->3 isentropic, 3->4 isothermal compression, 4->1 isentropic
    cycle_s = [s1, s2, s2, s1, s1]
    cycle_T = [T_H, T_H, T_C, T_C, T_H]

    ax.fill(cycle_s, cycle_T, alpha=0.15, color=COLORS[0])
    ax.plot(cycle_s, cycle_T, color=COLORS[0], linewidth=2.5)

    # Point labels
    points = [(s1, T_H, "1"), (s2, T_H, "2"), (s2, T_C, "3"), (s1, T_C, "4")]
    for s, T, label in points:
        ax.plot(s, T, "o", color=COLORS[0], markersize=10, zorder=5)
        offset_x = -30 if s == s1 else 15
        offset_y = 10 if T == T_H else -20
        ax.annotate(label, (s, T), xytext=(s + offset_x, T + offset_y),
                    fontsize=14, fontweight="bold", color=COLORS[0])

    # Process labels
    ax.text((s1 + s2) / 2, T_H + 15, "Izotermick\u00e1 expanze (Q\u2095)", ha="center",
            fontsize=9, color="#DC2626", fontweight="bold")
    ax.text((s1 + s2) / 2, T_C - 20, "Izotermick\u00e1 komprese (Q\u2097)", ha="center",
            fontsize=9, color="#2563EB", fontweight="bold")
    ax.text(s2 + 20, (T_H + T_C) / 2, "Izoentrop.\nexpanze", fontsize=8, color="#555")
    ax.text(s1 - 80, (T_H + T_C) / 2, "Izoentrop.\nkomprese", fontsize=8, color="#555", ha="center")

    # W_net = area
    ax.text((s1 + s2) / 2, (T_H + T_C) / 2, "$W_{net}$\n= plocha", ha="center",
            fontsize=11, fontweight="bold", color=COLORS[0])

    # Efficiency
    eta = (T_H - T_C) / T_H * 100
    ax.text(450, 520, f"$\\eta_C = 1 - T_C/T_H = {eta:.0f}$ %", fontsize=10,
            fontweight="bold", color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF3C7", edgecolor="#D97706"))

    ax.set_xlabel("M\u011brn\u00e1 entropie s [J/(kg\u00b7K)]", fontsize=11)
    ax.set_ylabel("Teplota T [K]", fontsize=11)
    ax.set_title("Carnot\u016fv cyklus v T-s diagramu", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 600)
    ax.set_ylim(200, 600)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q01_carnot_ts.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_1law = generate_first_law_schema()
    img_ts = generate_ts_processes()
    img_2law = generate_second_law_schema()
    img_carnot = generate_carnot_ts()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="1. Prvn\u00ed z\u00e1kon termomechaniky dva z\u00e1kladn\u00ed tvary, v\u00fdznam veli\u010din.\n"
              "    Druh\u00fd z\u00e1kon termodynamiky, podstata, matematick\u00e1 formulace.\n"
              "    Ur\u010den\u00ed zm\u011bny entropie. Pr\u016fb\u011bh zm\u011bn v diagramu T-s.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Uve\u010fte prvn\u00ed z\u00e1kon termomechaniky v obou z\u00e1kladn\u00edch tvarech (uzav\u0159en\u00e1 "
        "a otev\u0159en\u00e1 soustava). Formulujte druh\u00fd z\u00e1kon termodynamiky a jeho matematick\u00e9 "
        "vyj\u00e1d\u0159en\u00ed. Odvo\u010fte zm\u011bny entropie pro z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu "
        "ide\u00e1ln\u00edho plynu a zn\u00e1zorn\u011bte je v T-s diagramu.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    # -- 1.1 Prvni zakon --
    add_heading(doc, "1.1 Prvn\u00ed z\u00e1kon termomechaniky", level=3)

    add_info_box(doc,
        "Prvn\u00ed z\u00e1kon \u2014 podstata",
        "Z\u00e1kon zachov\u00e1n\u00ed energie: energie se nem\u016f\u017ee vytvo\u0159it ani zni\u010dit, "
        "pouze p\u0159em\u011bnit z jedn\u00e9 formy na jinou. Teplo p\u0159iveden\u00e9 soustav\u011b "
        "se spot\u0159ebuje na zv\u00fd\u0161en\u00ed vnit\u0159n\u00ed energie a na vykon\u00e1n\u00ed pr\u00e1ce.")

    add_image(doc, img_1law, width_cm=14,
              caption="Obr. 1: Prvn\u00ed z\u00e1kon pro uzav\u0159enou a otev\u0159enou soustavu")

    add_para(doc, "Tvar 1: Uzav\u0159en\u00e1 soustava (konstantn\u00ed hmotnost):", bold=True, keep_with_next=True)
    add_equation(doc, r"Q = \Delta U + W", label="1")

    add_para(doc, "Diferenci\u00e1ln\u011b:", keep_with_next=True)
    add_equation(doc, r"\delta q = du + p \, dv", label="2")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "Q (q) \u2014 sd\u011blen\u00e9 teplo [J] (m\u011brn\u00e9 [J/kg])")
    add_bullet(doc, "U (u) \u2014 vnit\u0159n\u00ed energie [J] (m\u011brn\u00e1 [J/kg])")
    add_bullet(doc, "W = \u222bp\u00b7dV \u2014 objemov\u00e1 pr\u00e1ce [J]")
    add_bullet(doc, "p\u00b7dv \u2014 m\u011brn\u00e1 objemov\u00e1 pr\u00e1ce [J/kg]", is_last=True)

    add_page_break(doc)
    add_para(doc, "Tvar 2: Otev\u0159en\u00e1 soustava (stacion\u00e1rn\u00ed proud\u011bn\u00ed):", bold=True, keep_with_next=True)
    add_equation(doc, r"\dot{Q} = \dot{m}(h_2 - h_1) + P + \dot{m}\frac{c_2^2 - c_1^2}{2} + \dot{m}g(z_2 - z_1)", label="3")

    add_para(doc, "Zjednodu\u0161en\u011b (zanedbána kinetick\u00e1 a potenci\u00e1ln\u00ed energie):", keep_with_next=True)
    add_equation(doc, r"\delta q = dh - v \, dp", label="4")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "h = u + pv \u2014 m\u011brn\u00e1 entalpie [J/kg]")
    add_bullet(doc, "P \u2014 technick\u00e1 (h\u0159\u00eddelov\u00e1) pr\u00e1ce [W]")
    add_bullet(doc, "v\u00b7dp \u2014 m\u011brn\u00e1 technick\u00e1 pr\u00e1ce [J/kg]", is_last=True)

    add_warning_box(doc,
        "Rozd\u00edl: objemov\u00e1 pr\u00e1ce p\u00b7dv (uzav\u0159en\u00e1 soustava, p\u00edst) vs. "
        "technick\u00e1 pr\u00e1ce \u2212v\u00b7dp (otev\u0159en\u00e1 soustava, turb\u00edna/kompresor). "
        "Ob\u011b pr\u00e1ce jsou r\u016fzn\u00e9 veli\u010diny!")

    # -- 1.2 Druhy zakon --
    add_page_break(doc)
    add_heading(doc, "1.2 Druh\u00fd z\u00e1kon termodynamiky", level=3)

    add_image(doc, img_2law, width_cm=14,
              caption="Obr. 2: Druh\u00fd z\u00e1kon \u2014 Kelvin-Planck\u016fv a Clausi\u016fv v\u00fdrok")

    add_para(doc, "Kelvin-Planck\u016fv v\u00fdrok:", bold=True, keep_with_next=True)
    add_para(doc,
        "Nelze sestrojit tepeln\u00fd stroj pracuj\u00edc\u00ed v cyklu, kter\u00fd by p\u0159em\u011bnil "
        "ve\u0161ker\u00e9 p\u0159ijat\u00e9 teplo na pr\u00e1ci (bez odveden\u00ed tepla do studen\u00e9ho z\u00e1sobn\u00edku). "
        "D\u016fsledek: \u03b7 < 100 % pro jak\u00fdkoliv tepeln\u00fd stroj.")

    add_para(doc, "Clausi\u016fv v\u00fdrok:", bold=True, keep_with_next=True)
    add_para(doc,
        "Teplo nem\u016f\u017ee samovoln\u011b p\u0159ech\u00e1zet z t\u011blesa chladn\u011bj\u0161\u00edho na t\u011bleso "
        "teplej\u0161\u00ed (bez dod\u00e1n\u00ed pr\u00e1ce). D\u016fsledek: chladi\u010dka/tepeln\u00e9 \u010derpadlo "
        "vy\u017eaduje p\u0159\u00edvod pr\u00e1ce.")

    add_para(doc, "Matematick\u00e1 formulace:", bold=True, keep_with_next=True)
    add_equation(doc, r"\oint \frac{\delta Q}{T} \leq 0 \quad \text{(Clausiova nerovnost)}", label="5")

    add_para(doc, "Pro vratn\u00fd (reverz.) d\u011bj plat\u00ed rovnost, pro nevratn\u00fd ostr\u00e1 nerovnost.")

    # -- 1.3 Entropie --
    add_heading(doc, "1.3 Entropie", level=3)

    add_info_box(doc,
        "Definice: Entropie",
        "Stavov\u00e1 veli\u010dina definovan\u00e1 diferenci\u00e1ln\u011b pro vratn\u00fd d\u011bj:\n"
        "ds = \u03b4q_rev / T\n"
        "Ur\u010duje sm\u011br samovoln\u00fdch d\u011bj\u016f: entropie izolovan\u00e9 soustavy nem\u016f\u017ee klesat.")

    add_equation(doc, r"ds = \frac{\delta q_{rev}}{T} \quad [\text{J/(kg\cdot K)}]", label="6")

    add_para(doc, "Zm\u011bna entropie ide\u00e1ln\u00edho plynu (obecn\u011b):", keep_with_next=True)
    add_equation(doc, r"s_2 - s_1 = c_v \ln\frac{T_2}{T_1} + r \ln\frac{v_2}{v_1}", label="7")
    add_equation(doc, r"s_2 - s_1 = c_p \ln\frac{T_2}{T_1} - r \ln\frac{p_2}{p_1}", label="8")

    # -- 1.4 Zm\u011bny stavu --
    add_page_break(doc)
    add_heading(doc, "1.4 Z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu a jejich entropie", level=3)

    add_styled_table(doc,
        headers=["Zm\u011bna", "Podm\u00ednka", "\u0394s", "q", "w (objemov\u00e1)"],
        data=[
            ["Izochorick\u00e1", "v = konst.", "c_v ln(T\u2082/T\u2081)", "c_v(T\u2082\u2212T\u2081)", "0"],
            ["Izobarick\u00e1", "p = konst.", "c_p ln(T\u2082/T\u2081)", "c_p(T\u2082\u2212T\u2081)", "p(v\u2082\u2212v\u2081)"],
            ["Izotermick\u00e1", "T = konst.", "r ln(v\u2082/v\u2081)", "T\u00b7\u0394s", "p\u2081v\u2081 ln(v\u2082/v\u2081)"],
            ["Izoentropick\u00e1", "s = konst.", "0", "0", "\u2212c_v(T\u2082\u2212T\u2081)"],
            ["Polytropick\u00e1", "pv\u207f = konst.", "c_n ln(T\u2082/T\u2081)", "c_n(T\u2082\u2212T\u2081)", "(p\u2082v\u2082\u2212p\u2081v\u2081)/(1\u2212n)"],
        ],
    )

    add_para(doc, "kde c_n = c_v(\u03ba \u2212 n)/(1 \u2212 n) je m\u011brn\u00e9 teplo polytropy.", keep_with_next=True)

    add_image(doc, img_ts, width_cm=14,
              caption="Obr. 3: Z\u00e1kladn\u00ed vratn\u00e9 zm\u011bny stavu ide\u00e1ln\u00edho plynu v T-s diagramu")

    add_info_box(doc,
        "T-s diagram \u2014 fyzik\u00e1ln\u00ed v\u00fdznam",
        "Plocha pod k\u0159ivkou v T-s diagramu p\u0159edstavuje sd\u011blen\u00e9 teplo:\n"
        "q = \u222bT\u00b7ds\n"
        "Izoentropa je svisl\u00e1 p\u0159\u00edmka (s = konst.), izoterma vodorovn\u00e1 (T = konst.).")

    # -- 1.5 Carnot --
    add_page_break(doc)
    add_heading(doc, "1.5 Carnot\u016fv cyklus a maxim\u00e1ln\u00ed \u00fa\u010dinnost", level=3)

    add_image(doc, img_carnot, width_cm=12,
              caption="Obr. 4: Carnot\u016fv cyklus v T-s diagramu \u2014 obd\u00e9ln\u00edk (nejv\u011bt\u0161\u00ed mo\u017en\u00e1 \u00fa\u010dinnost)")

    add_equation(doc, r"\eta_C = 1 - \frac{T_C}{T_H}", label="9")

    add_para(doc,
        "Carnot\u016fv cyklus ud\u00e1v\u00e1 horn\u00ed mez \u00fa\u010dinnosti jak\u00e9hokoliv tepeln\u00e9ho stroje "
        "pracuj\u00edc\u00edho mezi teplotami T_H a T_C. \u017d\u00e1dn\u00fd re\u00e1ln\u00fd stroj nem\u016f\u017ee "
        "m\u00edt vy\u0161\u0161\u00ed \u00fa\u010dinnost.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Porovn\u00e1n\u00ed objemov\u00e9 a technick\u00e9 pr\u00e1ce", level=3)
    add_styled_table(doc,
        headers=["Vlastnost", "Objemov\u00e1 pr\u00e1ce (p\u00b7dv)", "Technick\u00e1 pr\u00e1ce (\u2212v\u00b7dp)"],
        data=[
            ["Soustava", "Uzav\u0159en\u00e1 (p\u00edst)", "Otev\u0159en\u00e1 (turb\u00edna)"],
            ["Diagram", "Plocha pod k\u0159ivkou v p-v", "Plocha vlevo od k\u0159ivky v p-v"],
            ["1. z\u00e1kon", "\u03b4q = du + p\u00b7dv", "\u03b4q = dh \u2212 v\u00b7dp"],
            ["P\u0159\u00edklad", "Spalovac\u00ed motor", "Parn\u00ed turb\u00edna, kompresor"],
        ],
    )

    add_heading(doc, "2.2 Entropie v praxi", level=3)
    add_bullet(doc, "T-s diagram \u2014 z\u00e1kladn\u00ed n\u00e1stroj pro anal\u00fdzu tepeln\u00fdch ob\u011bh\u016f")
    add_bullet(doc, "Izoentropick\u00e1 \u00fa\u010dinnost turb\u00edny/kompresoru: \u03b7_s = w_s/w_is")
    add_bullet(doc, "Nevratnosti zvy\u0161uj\u00ed entropii \u2014 generov\u00e1n\u00ed entropie = ztráta pou\u017eiteln\u00e9 pr\u00e1ce")
    add_bullet(doc, "Exergie = max. pr\u00e1ce p\u0159i dan\u00e9 zm\u011bn\u011b stavu = T\u2080\u00b7\u0394s_gen", is_last=True)

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Izobarick\u00fd oh\u0159ev vzduchu", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: 1 kg vzduchu (ide\u00e1ln\u00ed plyn, c_p = 1005 J/(kg\u00b7K), r = 287,1 J/(kg\u00b7K)) "
        "se izobaricky oh\u0159eje z T\u2081 = 300 K na T\u2082 = 600 K p\u0159i p = 200 kPa. "
        "Ur\u010dete: sd\u011blen\u00e9 teplo, vykonanou pr\u00e1ci a zm\u011bnu entropie.", bold=True)

    add_para(doc, "Krok 1: Sd\u011blen\u00e9 teplo (izobarick\u00fd d\u011bj)", bold=True)
    add_equation(doc, r"q = c_p (T_2 - T_1) = 1005 \times (600 - 300) = 301\,500 \text{ J/kg} = 301{,}5 \text{ kJ/kg}")

    add_para(doc, "Krok 2: Objemov\u00e1 pr\u00e1ce", bold=True)
    add_equation(doc, r"w = p(v_2 - v_1) = r(T_2 - T_1) = 287{,}1 \times 300 = 86\,130 \text{ J/kg} = 86{,}1 \text{ kJ/kg}")

    add_para(doc, "Krok 3: Zm\u011bna vnit\u0159n\u00ed energie (kontrola: q = \u0394u + w)", bold=True)
    add_equation(doc, r"\Delta u = q - w = 301{,}5 - 86{,}1 = 215{,}4 \text{ kJ/kg} = c_v \Delta T = 718 \times 300 \quad \checkmark")

    add_para(doc, "Krok 4: Zm\u011bna entropie", bold=True)
    add_equation(doc, r"\Delta s = c_p \ln\frac{T_2}{T_1} = 1005 \times \ln\frac{600}{300} = 1005 \times 0{,}6931 = 696{,}6 \text{ J/(kg\cdot K)}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "q = 301,5 kJ/kg | w = 86,1 kJ/kg | \u0394u = 215,4 kJ/kg | \u0394s = 696,6 J/(kg\u00b7K)\n\n"
        "Kontrola: pr\u00e1ce w/q = 86,1/301,5 = 28,6 % \u2014 p\u0159i izobarick\u00e9m d\u011bji se "
        "cca 29 % tepla p\u0159em\u011bn\u00ed na pr\u00e1ci a 71 % zv\u00fd\u0161\u00ed vnit\u0159n\u00ed energii.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Jak\u00fd je rozd\u00edl mezi objemovou a technickou prac\u00ed?",
         "Objemov\u00e1 pr\u00e1ce w = \u222bp\u00b7dv popisuje pr\u00e1ci p\u0159i zm\u011bn\u011b objemu (p\u00edst). "
         "Technick\u00e1 pr\u00e1ce w_t = \u2212\u222bv\u00b7dp popisuje pr\u00e1ci p\u0159i zm\u011bn\u011b tlaku (turb\u00edna). "
         "Pro stejn\u00fd d\u011bj jsou r\u016fzn\u011b velk\u00e9: w_t = \u03ba\u00b7w pro izoentropick\u00fd d\u011bj."),

        ("Pro\u010d nem\u016f\u017ee m\u00edt \u017e\u00e1dn\u00fd tepeln\u00fd stroj \u00fa\u010dinnost 100 %?",
         "Kelvin-Planck\u016fv v\u00fdrok 2. z\u00e1kona: \u010d\u00e1st tepla mus\u00ed b\u00fdt odvedena do studen\u00e9ho "
         "z\u00e1sobn\u00edku. Maxim\u00e1ln\u00ed \u00fa\u010dinnost je Carnotova \u03b7_C = 1 \u2212 T_C/T_H, "
         "kter\u00e1 je rovna 100 % pouze pro T_C = 0 K (nedosa\u017eiteln\u00e9)."),

        ("Co fyzik\u00e1ln\u011b p\u0159edstavuje plocha pod k\u0159ivkou v T-s diagramu?",
         "Sd\u011blen\u00e9 teplo q = \u222bT\u00b7ds. U cyklu je uzav\u0159en\u00e1 plocha rovna \u010dist\u00e9 pr\u00e1ci "
         "w_net = q_in \u2212 q_out. Proto je T-s diagram z\u00e1kladn\u00edm n\u00e1strojem "
         "pro anal\u00fdzu \u00fa\u010dinnosti tepeln\u00fdch ob\u011bh\u016f."),

        ("Pro\u010d je izoentropick\u00fd d\u011bj adiabatick\u00fd a vratn\u00fd?",
         "Z definice ds = \u03b4q/T: pokud ds = 0, pak \u03b4q = 0 (adiabatick\u00fd). "
         "Vratn\u00fd proto, \u017ee p\u0159i nevratn\u00e9m adiabatick\u00e9m d\u011bji by \u0394s > 0 "
         "(generov\u00e1n\u00ed entropie). Izoentropick\u00fd = adiabatick\u00fd + vratn\u00fd."),

        ("Vysv\u011btlete, pro\u010d je izochora v T-s diagramu strm\u011bj\u0161\u00ed ne\u017e izobara.",
         "Sklon v T-s: dT/ds = T/c, kde c je m\u011brn\u00e9 teplo d\u011bje. "
         "U izochory c = c_v, u izobary c = c_p. Proto\u017ee c_p > c_v (\u03ba > 1), "
         "izobara m\u00e1 men\u0161\u00ed sklon (p\u0159i dan\u00e9m T) ne\u017e izochora."),

        ("Jak\u00fd je v\u00fdznam Carnotovy \u00fa\u010dinnosti?",
         "Je to horn\u00ed mez \u00fa\u010dinnosti jak\u00e9hokoliv tepeln\u00e9ho stroje pracuj\u00edc\u00edho "
         "mezi teplotami T_H a T_C: \u03b7_C = 1 \u2212 T_C/T_H. Slou\u017e\u00ed jako referen\u010dn\u00ed "
         "hodnota \u2014 re\u00e1ln\u00e9 stroje dosahuj\u00ed 50\u201375 % Carnotovy \u00fa\u010dinnosti."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "\u010cengel, Y.A., Boles, M.A.: Thermodynamics \u2014 An Engineering Approach, 9th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "Nožička, J.: Technick\u00e1 termomechanika, \u010cVUT Praha")
    add_bullet(doc, "Moran, M.J. et al.: Fundamentals of Engineering Thermodynamics, 9th Ed.")
    add_bullet(doc, "Fermi, E.: Thermodynamics \u2014 klasick\u00e1 u\u010debnice", is_last=True)

    save_and_export(doc, "01-zakony-TD")


if __name__ == "__main__":
    generate()
