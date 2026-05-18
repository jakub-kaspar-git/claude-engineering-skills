# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 4: Porovn\u00e1vac\u00ed cykly p\u00edstov\u00fdch motor\u016f (v\u00fdbuch., rovnotlak.,
sm\u00ed\u0161en\u00fd) a spalovac\u00ed turb\u00edny. Ur\u010den\u00ed termick\u00e9 \u00fa\u010dinnosti a vykonan\u00e9 pr\u00e1ce.
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

def generate_otto_diesel_pv():
    """p-v diagrams for Otto and Diesel cycles side by side."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
    kappa = 1.4

    # OTTO cycle (1-2 isentropic compression, 2-3 isochoric heat add, 3-4 isentropic expansion, 4-1 isochoric heat reject)
    eps = 8  # compression ratio
    v1, p1, T1 = 1.0, 100, 300
    v2 = v1 / eps
    p2 = p1 * eps**kappa
    T2 = T1 * eps**(kappa - 1)
    T3 = T2 * 2.5  # heat addition
    p3 = p2 * T3 / T2
    T4 = T3 * (v2 / v1)**(kappa - 1)
    p4 = p3 * (v2 / v1)**kappa

    # Plot Otto
    v_12 = np.linspace(v1, v2, 100)
    p_12 = p1 * (v1 / v_12)**kappa
    v_34 = np.linspace(v2, v1, 100)
    p_34 = p3 * (v2 / v_34)**kappa

    ax1.plot(v_12, p_12 / 1e3, color=COLORS[0], linewidth=2.5)
    ax1.plot([v2, v2], [p2 / 1e3, p3 / 1e3], color=COLORS[1], linewidth=2.5)
    ax1.plot(v_34, p_34 / 1e3, color=COLORS[0], linewidth=2.5)
    ax1.plot([v1, v1], [p4 / 1e3, p1 / 1e3], color=COLORS[2], linewidth=2.5)

    # Fill
    v_cycle = np.concatenate([v_12, [v2, v2], v_34[::-1], [v1, v1]])
    p_cycle = np.concatenate([p_12, [p2, p3], p_34[::-1], [p4, p1]])
    ax1.fill(v_cycle, p_cycle / 1e3, alpha=0.08, color=COLORS[0])

    # Labels
    for v, p, label in [(v1, p1, "1"), (v2, p2, "2"), (v2, p3, "3"), (v1, p4, "4")]:
        ax1.plot(v, p / 1e3, "ko", markersize=8, zorder=5)
        ax1.annotate(label, (v, p / 1e3), xytext=(5, 5), textcoords="offset points",
                    fontsize=12, fontweight="bold")

    ax1.text(0.6, p3 / 1e3 * 0.7, "$q_{in}$\n(v=k)", fontsize=9, color=COLORS[1], fontweight="bold")
    ax1.text(1.05, p4 / 1e3 * 0.5, "$q_{out}$\n(v=k)", fontsize=9, color=COLORS[2], fontweight="bold")
    ax1.set_xlabel("v", fontsize=11)
    ax1.set_ylabel("p [kPa]", fontsize=11)
    ax1.set_title("OTTO (v\u00fdbuchov\u00fd)\n$q_{in}$ p\u0159i v = konst.", fontsize=12, fontweight="bold")

    # DIESEL cycle (1-2 isentropic, 2-3 isobaric heat add, 3-4 isentropic, 4-1 isochoric)
    eps_d = 18
    v1d = 1.0
    v2d = v1d / eps_d
    p2d = p1 * eps_d**kappa
    T2d = T1 * eps_d**(kappa - 1)
    rho = 2.0  # cutoff ratio
    v3d = v2d * rho
    T3d = T2d * rho
    p3d = p2d  # isobaric
    T4d = T3d * (v3d / v1d)**(kappa - 1)
    p4d = p3d * (v3d / v1d)**kappa

    v_12d = np.linspace(v1d, v2d, 100)
    p_12d = p1 * (v1d / v_12d)**kappa
    v_34d = np.linspace(v3d, v1d, 100)
    p_34d = p3d * (v3d / v_34d)**kappa

    ax2.plot(v_12d, p_12d / 1e3, color=COLORS[0], linewidth=2.5)
    ax2.plot([v2d, v3d], [p2d / 1e3, p3d / 1e3], color=COLORS[1], linewidth=2.5)
    ax2.plot(v_34d, p_34d / 1e3, color=COLORS[0], linewidth=2.5)
    ax2.plot([v1d, v1d], [p4d / 1e3, p1 / 1e3], color=COLORS[2], linewidth=2.5)

    for v, p, label in [(v1d, p1, "1"), (v2d, p2d, "2"), (v3d, p3d, "3"), (v1d, p4d, "4")]:
        ax2.plot(v, p / 1e3, "ko", markersize=8, zorder=5)
        ax2.annotate(label, (v, p / 1e3), xytext=(5, 5), textcoords="offset points",
                    fontsize=12, fontweight="bold")

    ax2.text(0.08, p2d / 1e3 * 0.85, "$q_{in}$\n(p=k)", fontsize=9, color=COLORS[1], fontweight="bold")
    ax2.set_xlabel("v", fontsize=11)
    ax2.set_ylabel("p [kPa]", fontsize=11)
    ax2.set_title("DIESEL (rovnotlakov\u00fd)\n$q_{in}$ p\u0159i p = konst.", fontsize=12, fontweight="bold")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q04_otto_diesel_pv.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_brayton_pv_ts():
    """Brayton cycle in p-v and T-s diagrams."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    kappa = 1.4

    # Brayton: 1-2 isentropic compression, 2-3 isobaric heat add, 3-4 isentropic expansion, 4-1 isobaric heat reject
    pi = 10  # pressure ratio
    T1, p1 = 300, 100
    T2 = T1 * pi**((kappa - 1) / kappa)
    p2 = p1 * pi
    T3 = 1200  # turbine inlet
    T4 = T3 / pi**((kappa - 1) / kappa)

    # p-v diagram
    v1 = 287.1 * T1 / (p1 * 1e3)
    v2 = 287.1 * T2 / (p2 * 1e3)
    v3 = 287.1 * T3 / (p2 * 1e3)
    v4 = 287.1 * T4 / (p1 * 1e3)

    v_12 = np.linspace(v1, v2, 100)
    p_12 = p1 * (v1 / v_12)**kappa
    v_34 = np.linspace(v3, v4, 100)
    p_34 = p2 * 1e3 * (v3 / v_34)**kappa / 1e3

    ax1.plot(v_12, p_12, color=COLORS[0], linewidth=2.5)
    ax1.plot([v2, v3], [p2, p2], color=COLORS[1], linewidth=2.5)
    ax1.plot(v_34, p_34, color=COLORS[0], linewidth=2.5)
    ax1.plot([v4, v1], [p1, p1], color=COLORS[2], linewidth=2.5)

    for v, p, label in [(v1, p1, "1"), (v2, p2, "2"), (v3, p2, "3"), (v4, p1, "4")]:
        ax1.plot(v, p, "ko", markersize=8, zorder=5)
        ax1.annotate(label, (v, p), xytext=(5, 5), textcoords="offset points",
                    fontsize=12, fontweight="bold")

    ax1.set_xlabel("v [m\u00b3/kg]", fontsize=11)
    ax1.set_ylabel("p [kPa]", fontsize=11)
    ax1.set_title("BRAYTON (spalov. turb\u00edna)\np-v diagram", fontsize=12, fontweight="bold")

    # T-s diagram
    cp = 1005
    s1 = 0
    s2 = s1  # isentropic
    s3 = s2 + cp * np.log(T3 / T2)
    s4 = s3  # isentropic

    ax2.plot([s1, s2], [T1, T2], color=COLORS[0], linewidth=2.5, label="Izoentropick\u00e1")
    ax2.plot([s2, s3], [T2, T3], color=COLORS[1], linewidth=2.5, label="Izobarick\u00e1 ($q_{in}$)")
    ax2.plot([s3, s4], [T3, T4], color=COLORS[0], linewidth=2.5)
    ax2.plot([s4, s1], [T4, T1], color=COLORS[2], linewidth=2.5, label="Izobarick\u00e1 ($q_{out}$)")

    for s, T, label in [(s1, T1, "1"), (s2, T2, "2"), (s3, T3, "3"), (s4, T4, "4")]:
        ax2.plot(s, T, "ko", markersize=8, zorder=5)
        ax2.annotate(label, (s, T), xytext=(5, 5), textcoords="offset points",
                    fontsize=12, fontweight="bold")

    ax2.fill([s1, s2, s3, s4], [T1, T2, T3, T4], alpha=0.08, color=COLORS[0])
    ax2.text((s2 + s3) / 2, (T2 + T3) / 2, "$w_{net}$", fontsize=11,
             fontweight="bold", color=COLORS[0], ha="center")

    ax2.set_xlabel("s [J/(kg\u00b7K)]", fontsize=11)
    ax2.set_ylabel("T [K]", fontsize=11)
    ax2.set_title("BRAYTON (spalov. turb\u00edna)\nT-s diagram", fontsize=12, fontweight="bold")
    ax2.legend(fontsize=8)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q04_brayton.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_eta_vs_compression():
    """Thermal efficiency vs compression ratio for Otto, Diesel, Brayton."""
    fig, ax = plt.subplots(figsize=(8, 5))
    kappa = 1.4

    # Otto: eta = 1 - 1/eps^(kappa-1)
    eps_otto = np.linspace(2, 14, 100)
    eta_otto = (1 - 1 / eps_otto**(kappa - 1)) * 100

    # Diesel: eta = 1 - (rho^kappa - 1) / (kappa * eps^(kappa-1) * (rho - 1))
    eps_diesel = np.linspace(12, 24, 100)
    rho = 2.0
    eta_diesel = (1 - (rho**kappa - 1) / (kappa * eps_diesel**(kappa - 1) * (rho - 1))) * 100

    # Brayton: eta = 1 - 1/pi^((kappa-1)/kappa), pi = pressure ratio
    pi_brayton = np.linspace(2, 30, 100)
    eta_brayton = (1 - 1 / pi_brayton**((kappa - 1) / kappa)) * 100

    ax.plot(eps_otto, eta_otto, color=COLORS[0], linewidth=2.5, label="Otto (\u03b5)")
    ax.plot(eps_diesel, eta_diesel, color=COLORS[1], linewidth=2.5, label="Diesel (\u03b5, \u03c1=2)")
    ax.plot(pi_brayton, eta_brayton, color=COLORS[2], linewidth=2.5, linestyle="--",
            label="Brayton (\u03c0)")

    # Typical operating ranges
    ax.axvspan(6, 12, alpha=0.05, color=COLORS[0])
    ax.text(9, 30, "Otto\ntypick\u00e9", fontsize=8, ha="center", color=COLORS[0])
    ax.axvspan(14, 22, alpha=0.05, color=COLORS[1])
    ax.text(18, 30, "Diesel\ntypick\u00e9", fontsize=8, ha="center", color=COLORS[1])

    ax.set_xlabel("Kompresn\u00ed pom\u011br \u03b5 / tlakov\u00fd pom\u011br \u03c0 [-]", fontsize=11)
    ax.set_ylabel("Termick\u00e1 \u00fa\u010dinnost \u03b7_t [%]", fontsize=11)
    ax.set_title("Termick\u00e1 \u00fa\u010dinnost v z\u00e1vislosti na kompresn\u00edm/tlakov\u00e9m pom\u011bru",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(2, 30)
    ax.set_ylim(20, 75)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q04_eta_compression.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_otto_diesel = generate_otto_diesel_pv()
    img_brayton = generate_brayton_pv_ts()
    img_eta = generate_eta_vs_compression()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="4. Porovn\u00e1vac\u00ed cykly p\u00edstov\u00fdch motor\u016f (v\u00fdbuchov\u00e9ho, rovnotlak\u00e9ho,\n"
              "    sm\u00ed\u0161en\u00e9ho) a spalovac\u00ed turb\u00edny. Termick\u00e1 \u00fa\u010dinnost a pr\u00e1ce.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Popi\u0161te porovn\u00e1vac\u00ed cykly p\u00edstov\u00fdch spalovac\u00edch motor\u016f (Ott\u016fv, Diesel\u016fv, "
        "Sabath\u00e9ho) a spalovac\u00ed turb\u00edny (Brayton\u016fv). Pro ka\u017ed\u00fd cyklus uve\u010fte "
        "p-v a T-s diagramy, vztah pro termickou \u00fa\u010dinnost a vykonanou pr\u00e1ci.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    # -- Otto --
    add_heading(doc, "1.1 Ott\u016fv cyklus (v\u00fdbuchov\u00fd)", level=3)

    add_info_box(doc,
        "Ott\u016fv cyklus \u2014 z\u00e1\u017ehov\u00e9 motory (benzin)",
        "P\u0159\u00edvod tepla p\u0159i konstantn\u00edm objemu (izochora).\n"
        "D\u011bje: 1\u21922 izoentropick\u00e1 komprese, 2\u21923 izochorick\u00fd p\u0159\u00edvod tepla, "
        "3\u21924 izoentropick\u00e1 expanze, 4\u21921 izochorick\u00fd odvod tepla.")

    add_para(doc, "Kompresn\u00ed pom\u011br:", keep_with_next=True)
    add_equation(doc, r"\varepsilon = \frac{v_1}{v_2} = \frac{V_{max}}{V_{min}}", label="1")

    add_para(doc, "Termick\u00e1 \u00fa\u010dinnost:", keep_with_next=True)
    add_equation(doc, r"\eta_{t,Otto} = 1 - \frac{1}{\varepsilon^{\kappa - 1}}", label="2")

    add_para(doc, "Typick\u00e9 \u03b5 = 8\u201312, \u03b7_t = 45\u201360 % (ide\u00e1ln\u00ed), re\u00e1ln\u011b 25\u201335 %.")

    # -- Diesel --
    add_heading(doc, "1.2 Diesel\u016fv cyklus (rovnotlakov\u00fd)", level=3)

    add_info_box(doc,
        "Diesel\u016fv cyklus \u2014 vzn\u011btov\u00e9 motory",
        "P\u0159\u00edvod tepla p\u0159i konstantn\u00edm tlaku (izobara).\n"
        "D\u011bje: 1\u21922 izoentropick\u00e1 komprese, 2\u21923 izobarick\u00fd p\u0159\u00edvod tepla, "
        "3\u21924 izoentropick\u00e1 expanze, 4\u21921 izochorick\u00fd odvod tepla.")

    add_para(doc, "Stupe\u0148 pln\u011bn\u00ed (cutoff ratio):", keep_with_next=True)
    add_equation(doc, r"\varphi = \frac{v_3}{v_2}", label="3")

    add_para(doc, "Termick\u00e1 \u00fa\u010dinnost:", keep_with_next=True)
    add_equation(doc, r"\eta_{t,Diesel} = 1 - \frac{1}{\varepsilon^{\kappa - 1}} \cdot \frac{\varphi^\kappa - 1}{\kappa(\varphi - 1)}", label="4")

    add_para(doc, "Typick\u00e9 \u03b5 = 14\u201322, \u03b7_t = 50\u201365 % (ide\u00e1ln\u00ed), re\u00e1ln\u011b 30\u201340 %.")

    add_image(doc, img_otto_diesel, width_cm=14,
              caption="Obr. 1: p-v diagramy Ottova a Dieselova cyklu")

    # -- Sabathé --
    add_page_break(doc)
    add_heading(doc, "1.3 Sabath\u00e9ho cyklus (sm\u00ed\u0161en\u00fd)", level=3)

    add_info_box(doc,
        "Sabath\u00e9ho (sm\u00ed\u0161en\u00fd) cyklus",
        "Kombinace Ottova a Dieselova: p\u0159\u00edvod tepla \u010d\u00e1ste\u010dn\u011b p\u0159i v = konst. "
        "(izochora) a \u010d\u00e1ste\u010dn\u011b p\u0159i p = konst. (izobara). "
        "Nejl\u00e9pe odpov\u00edd\u00e1 skute\u010dn\u00e9mu pr\u016fb\u011bhu spalov\u00e1n\u00ed v motoru.")

    add_para(doc, "Stupe\u0148 zv\u00fd\u0161en\u00ed tlaku:", keep_with_next=True)
    add_equation(doc, r"\lambda = \frac{p_3}{p_2}", label="5")

    add_para(doc, "Termick\u00e1 \u00fa\u010dinnost:", keep_with_next=True)
    add_equation(doc, r"\eta_{t,Sab} = 1 - \frac{1}{\varepsilon^{\kappa-1}} \cdot \frac{\lambda \varphi^\kappa - 1}{\lambda - 1 + \kappa \lambda (\varphi - 1)}", label="6")

    add_para(doc, "Speci\u00e1ln\u00ed p\u0159\u00edpady: \u03c6 = 1 \u2192 Otto, \u03bb = 1 \u2192 Diesel.")

    # -- Brayton --
    add_heading(doc, "1.4 Brayton\u016fv cyklus (spalovac\u00ed turb\u00edna)", level=3)

    add_info_box(doc,
        "Brayton\u016fv cyklus \u2014 plynov\u00e9 turb\u00edny",
        "Otev\u0159en\u00fd ob\u011bh se vzduchem jako pracovn\u00ed l\u00e1tkou.\n"
        "D\u011bje: 1\u21922 izoentropick\u00e1 komprese (kompresor), 2\u21923 izobarick\u00fd p\u0159\u00edvod tepla "
        "(spalovac\u00ed komora), 3\u21924 izoentropick\u00e1 expanze (turb\u00edna), 4\u21921 izobarick\u00e9 ochlazeni.")

    add_para(doc, "Tlakov\u00fd pom\u011br:", keep_with_next=True)
    add_equation(doc, r"\pi = \frac{p_2}{p_1}", label="7")

    add_para(doc, "Termick\u00e1 \u00fa\u010dinnost:", keep_with_next=True)
    add_equation(doc, r"\eta_{t,Brayton} = 1 - \frac{1}{\pi^{(\kappa-1)/\kappa}}", label="8")

    add_para(doc, "Typick\u00e9 \u03c0 = 10\u201330, T\u2083 = 1200\u20131500 K, \u03b7_t = 30\u201340 % (jednoduch\u00fd cyklus).")

    add_image(doc, img_brayton, width_cm=14,
              caption="Obr. 2: Brayton\u016fv cyklus v p-v a T-s diagramech")

    # -- 1.5 Srovnani --
    add_page_break(doc)
    add_heading(doc, "1.5 Srovn\u00e1n\u00ed cykl\u016f", level=3)

    add_image(doc, img_eta, width_cm=14,
              caption="Obr. 3: Termick\u00e1 \u00fa\u010dinnost v z\u00e1vislosti na kompresn\u00edm/tlakov\u00e9m pom\u011bru")

    add_styled_table(doc,
        headers=["Cyklus", "P\u0159\u00edvod q_{in}", "\u03b7_t z\u00e1vis\u00ed na", "Typick\u00e1 \u03b7_t"],
        data=[
            ["Otto", "v = konst.", "\u03b5, \u03ba", "45\u201360 % (ide\u00e1l)"],
            ["Diesel", "p = konst.", "\u03b5, \u03c6, \u03ba", "50\u201365 % (ide\u00e1l)"],
            ["Sabath\u00e9", "v + p = konst.", "\u03b5, \u03bb, \u03c6, \u03ba", "Mezi Otto a Diesel"],
            ["Brayton", "p = konst.", "\u03c0, \u03ba", "35\u201355 % (ide\u00e1l)"],
        ],
    )

    add_warning_box(doc,
        "P\u0159i STEJN\u00c9M kompresn\u00edm pom\u011bru m\u00e1 Otto vy\u0161\u0161\u00ed \u03b7 ne\u017e Diesel. "
        "Ale Diesel pracuje s vy\u0161\u0161\u00edm \u03b5 (14\u201322 vs. 8\u201312), proto m\u00e1 "
        "v praxi srovnatelnou nebo vy\u0161\u0161\u00ed \u00fa\u010dinnost.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Srovn\u00e1n\u00ed re\u00e1ln\u00fdch motor\u016f", level=3)
    add_styled_table(doc,
        headers=["Parametr", "Z\u00e1\u017ehov\u00fd (Otto)", "Vzn\u011btov\u00fd (Diesel)", "Plynov\u00e1 turb\u00edna"],
        data=[
            ["\u03b5 / \u03c0", "8\u201312", "14\u201322", "\u03c0 = 10\u201330"],
            ["\u03b7 skute\u010dn\u00e1", "25\u201335 %", "30\u201345 %", "30\u201340 %"],
            ["Palivo", "Benzin (oct. 95)", "Motorov\u00e1 nafta", "Kerosin, ZP"],
            ["V\u00fdkon", "50\u2013400 kW", "50\u20131000 kW", "1\u2013500 MW"],
            ["Pou\u017eit\u00ed", "Osobn\u00ed auta", "N\u00e1kladn\u00ed, lod\u011b", "Elektr\u00e1rny, letadla"],
        ],
    )

    add_heading(doc, "2.2 Zvy\u0161ov\u00e1n\u00ed \u00fa\u010dinnosti", level=3)
    add_bullet(doc, "Zvy\u0161ov\u00e1n\u00ed \u03b5 / \u03c0 (omezeno detonac\u00ed u Otto, tlakov\u00fdm nam\u00e1h\u00e1n\u00edm)")
    add_bullet(doc, "Turbodmychadlo (zvy\u0161uje efektivn\u00ed \u03b5)")
    add_bullet(doc, "Mezichlazení a p\u0159ih\u0159\u00edv\u00e1n\u00ed u turb\u00edn")
    add_bullet(doc, "Paroplynov\u00fd cyklus (Brayton + Rankine): \u03b7 = 55\u201362 %", is_last=True)

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Porovn\u00e1n\u00ed Ottova a Dieselova cyklu", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Porovnejte ide\u00e1ln\u00ed termickou \u00fa\u010dinnost Ottova cyklu (\u03b5 = 10) "
        "a Dieselova cyklu (\u03b5 = 18, \u03c6 = 2). Vzduch: \u03ba = 1,4.", bold=True)

    add_para(doc, "Otto:", bold=True)
    add_equation(doc, r"\eta_{Otto} = 1 - \frac{1}{10^{0{,}4}} = 1 - \frac{1}{2{,}512} = 1 - 0{,}398 = 0{,}602 = 60{,}2 \%")

    add_para(doc, "Diesel:", bold=True)
    add_equation(doc, r"\eta_{Diesel} = 1 - \frac{1}{18^{0{,}4}} \cdot \frac{2^{1{,}4} - 1}{1{,}4 \times (2 - 1)}")
    add_equation(doc, r"\eta_{Diesel} = 1 - \frac{1}{3{,}477} \cdot \frac{2{,}639 - 1}{1{,}4} = 1 - 0{,}288 \times 1{,}171 = 1 - 0{,}337 = 0{,}663 = 66{,}3 \%")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Otto (\u03b5 = 10): \u03b7_t = 60,2 %\n"
        "Diesel (\u03b5 = 18): \u03b7_t = 66,3 %\n\n"
        "Diesel m\u00e1 vy\u0161\u0161\u00ed \u00fa\u010dinnost d\u00edky vy\u0161\u0161\u00edmu \u03b5, p\u0159esto\u017ee p\u0159i stejn\u00e9m \u03b5 "
        "by Otto byl lep\u0161\u00ed. Proto je Diesel efektivn\u011bj\u0161\u00ed pro n\u00e1kladn\u00ed dopravu.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d m\u00e1 Diesel vy\u0161\u0161\u00ed kompresn\u00ed pom\u011br ne\u017e Otto?",
         "Diesel komprimuje \u010dist\u00fd vzduch (ne sm\u011bs s palivem), tak\u017e\u0219 nehroz\u00ed "
         "p\u0159ed\u010dasn\u00e9 vzn\u00edcen\u00ed (detonace). Palivo se vst\u0159ikuje a\u017e na konci komprese. "
         "Benzinov\u00fd motor mus\u00ed \u03b5 omezit kv\u016fli klepání (oct. \u010d\u00edslo paliva)."),

        ("Vysv\u011btlete, pro\u010d p\u0159i stejn\u00e9m \u03b5 m\u00e1 Otto vy\u0161\u0161\u00ed \u03b7 ne\u017e Diesel.",
         "U Diesela se \u010d\u00e1st tepla p\u0159iv\u00e1d\u00ed p\u0159i konstantn\u00edm tlaku (izobara), "
         "co\u017e je m\u00e9n\u011b efektivn\u00ed ne\u017e p\u0159\u00edvod p\u0159i konstantn\u00edm objemu (izochora). "
         "Faktor (\u03c6\u1d4b \u2212 1)/(\u03ba(\u03c6 \u2212 1)) > 1 sni\u017euje \u03b7 Diesela."),

        ("Co je Sabath\u00e9ho cyklus a pro\u010d se pou\u017e\u00edv\u00e1?",
         "Kombinace Otto + Diesel: \u010d\u00e1st tepla p\u0159i v = konst., \u010d\u00e1st p\u0159i p = konst. "
         "L\u00e9pe odpov\u00edd\u00e1 skute\u010dn\u00e9mu pr\u016fb\u011bhu spalov\u00e1n\u00ed v motoru, "
         "kde nen\u00ed ani \u010dist\u011b izochorick\u00e9 ani izobarick\u00e9."),

        ("Pro\u010d je paroplynov\u00fd cyklus tak \u00fa\u010dinn\u00fd?",
         "Kombinuje Brayton (plynov\u00e1 turb\u00edna, T_H \u2248 1400 K) a Rankine (parn\u00ed turb\u00edna). "
         "Horn\u00ed cyklus pracuje p\u0159i vysok\u00e9 T_H, doln\u00ed vyu\u017e\u00edv\u00e1 odpadn\u00ed teplo. "
         "Celkov\u00e1 \u03b7 = 55\u201362 %, co\u017e je bl\u00edzko Carnotovy meze."),

        ("Jak ovliv\u0148uje tlakov\u00fd pom\u011br \u03c0 \u00fa\u010dinnost Brayton. cyklu?",
         "S rostouc\u00edm \u03c0 roste \u03b7 (v\u00edce pr\u00e1ce z expanze). Ale p\u0159i p\u0159\u00edli\u0161 vysok\u00e9m \u03c0 "
         "kles\u00e1 \u010dist\u00e1 pr\u00e1ce (kompresor spot\u0159ebuje v\u00edce). Existuje optim\u00e1ln\u00ed \u03c0 "
         "pro max. w_{net} (jin\u00fd ne\u017e pro max. \u03b7)."),

        ("Pro\u010d jsou porovn\u00e1vac\u00ed cykly ide\u00e1ln\u00ed a jak se li\u0161\u00ed od re\u00e1ln\u00fdch?",
         "Porovn\u00e1vac\u00ed cykly p\u0159edpokl\u00e1daj\u00ed vratn\u00e9 d\u011bje, ide\u00e1ln\u00ed plyn s konst. c_p, c_v, "
         "dokonalé spalov\u00e1n\u00ed. Re\u00e1ln\u00e9 motory maj\u00ed: t\u0159en\u00ed, nedokonal\u00e9 spalov\u00e1n\u00ed, "
         "tepeln\u00e9 ztráty, v\u00fdm\u011bnu n\u00e1pln\u011b, prom\u011bnn\u00e9 c_p. Proto \u03b7_{re\u00e1l} \u2248 50\u201370 % \u03b7_{ide\u00e1l}."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "\u010cengel, Y.A., Boles, M.A.: Thermodynamics \u2014 An Engineering Approach")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "Heywood, J.B.: Internal Combustion Engine Fundamentals, 2nd Ed.")
    add_bullet(doc, "Saravanamuttoo, H.I.H. et al.: Gas Turbine Theory, 7th Ed.")
    add_bullet(doc, "Stone, R.: Introduction to Internal Combustion Engines", is_last=True)

    save_and_export(doc, "04-porovnavaci-cykly")


if __name__ == "__main__":
    generate()
