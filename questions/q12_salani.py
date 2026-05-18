# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 12: Z\u00e1kladn\u00ed z\u00e1kony s\u00e1l\u00e1n\u00ed absolutn\u011b \u010dern\u00e9ho t\u011blesa.
S\u00e1l\u00e1n\u00ed skute\u010dn\u00fdch t\u011bles. P\u0159enos tepla s\u00e1l\u00e1n\u00edm mezi dv\u011bma \u0161ed\u00fdmi povrchy
odd\u011blen\u00fdmi dokonale pr\u016fteplivn\u00fdm prost\u0159ed\u00edm, soustava uzav\u0159en\u00e1.
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

def generate_planck_curves():
    """Planck's law for multiple temperatures with Wien displacement."""
    fig, ax = plt.subplots(figsize=(9, 6))

    h = 6.626e-34
    c = 3e8
    k_B = 1.381e-23

    temps = [1000, 2000, 3000, 5000, 5778]
    labels = ["1000 K", "2000 K", "3000 K", "5000 K", "5778 K (Slunce)"]

    for i, (T, lbl) in enumerate(zip(temps, labels)):
        lam = np.linspace(0.1e-6, 15e-6, 1000)
        with np.errstate(over="ignore"):
            exp_arg = h * c / (lam * k_B * T)
            E = np.where(exp_arg < 500,
                         (2 * np.pi * h * c**2 / lam**5) / (np.exp(exp_arg) - 1),
                         0.0)
        ax.plot(lam * 1e6, E / 1e6, color=COLORS[i % len(COLORS)], linewidth=2, label=lbl)

        # Wien peak
        lam_max = 2.898e-3 / T
        if lam_max * 1e6 < 15:
            idx = np.argmin(np.abs(lam - lam_max))
            ax.plot(lam_max * 1e6, E[idx] / 1e6, "o", color=COLORS[i % len(COLORS)],
                    markersize=5, zorder=5)

    # Wien displacement line
    T_wien = np.linspace(800, 6000, 100)
    lam_wien = 2.898e-3 / T_wien
    mask = (lam_wien * 1e6 > 0.3) & (lam_wien * 1e6 < 12)
    # Don't plot this - too confusing. Just annotate.

    # Visible band
    ax.axvspan(0.38, 0.75, alpha=0.1, color="yellow")
    ax.text(0.56, ax.get_ylim()[1] * 0.02, "VIS", fontsize=8, ha="center", color="#555")

    # IR label
    ax.text(5, ax.get_ylim()[1] * 0.02, "Infra\u010derven\u00e9", fontsize=8, ha="center", color="#555")

    ax.set_xlabel("Vlnov\u00e1 d\u00e9lka \u03bb [\u03bcm]", fontsize=11)
    ax.set_ylabel("Spektr\u00e1ln\u00ed intenzita $E_{0\\lambda}$ [MW/(m\u00b2\u00b7\u03bcm)]", fontsize=11)
    ax.set_title("Planck\u016fv z\u00e1kon: spektr\u00e1ln\u00ed vyz\u00e1\u0159en\u00ed absolutn\u011b \u010dern\u00e9ho t\u011blesa",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(0, 15)
    ax.legend(fontsize=9, loc="upper right")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q12_planck.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_stefan_boltzmann():
    """E vs T^4 showing Stefan-Boltzmann law."""
    fig, ax = plt.subplots(figsize=(7, 5))

    T = np.linspace(300, 2000, 200)
    sigma = 5.67e-8
    E = sigma * T**4

    ax.plot(T, E / 1000, color=COLORS[0], linewidth=2.5, label="$E_0 = \\sigma T^4$")

    # Gray bodies
    for eps, lbl, col in [(0.9, "\u03b5 = 0,9 (oxidov. ocel)", COLORS[1]),
                           (0.5, "\u03b5 = 0,5 (beton)", COLORS[3]),
                           (0.1, "\u03b5 = 0,1 (le\u0161t. Al)", COLORS[2])]:
        ax.plot(T, eps * E / 1000, "--", color=col, linewidth=1.5, label=lbl)

    ax.set_xlabel("Teplota T [K]", fontsize=11)
    ax.set_ylabel("Intenzita vyz\u00e1\u0159en\u00ed E [kW/m\u00b2]", fontsize=11)
    ax.set_title("Stefan-Boltzmann\u016fv z\u00e1kon: $E = \\varepsilon \\sigma T^4$",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(300, 2000)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q12_stefan_boltzmann.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_radiation_balance():
    """Diagram of radiation interaction with surface: absorption, reflection, transmission."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Surface (thick slab)
    from matplotlib.patches import Rectangle, FancyBboxPatch
    slab = Rectangle((3, 1.5), 4, 1.5, facecolor="#E5E7EB", edgecolor="black", lw=2)
    ax.add_patch(slab)
    ax.text(5, 2.25, "POVRCH T\u011aLESA", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#555")

    # Incoming radiation
    ax.annotate("", xy=(4, 3.0), xytext=(1.5, 5.0),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=3))
    ax.text(1.5, 5.3, "Dopadaj\u00edc\u00ed z\u00e1\u0159en\u00ed\n$E_{dopad}$ (= 100 %)", fontsize=10,
            fontweight="bold", color="#D97706", ha="center")

    # Reflected
    ax.annotate("", xy=(1.5, 3.5), xytext=(4, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=2.5))
    ax.text(0.8, 3.8, "Odra\u017een\u00e9\nR = $\\rho$", fontsize=9,
            fontweight="bold", color=COLORS[0], ha="center")

    # Absorbed (into slab)
    ax.annotate("", xy=(5, 1.8), xytext=(5, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=2.5))
    ax.text(5.8, 2.5, "Pohlcen\u00e9\nA = $\\alpha$", fontsize=9,
            fontweight="bold", color=COLORS[1], ha="center")

    # Transmitted (through slab)
    ax.annotate("", xy=(6, 0.5), xytext=(6, 1.5),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[2], lw=2.5))
    ax.text(7, 0.7, "Propust\u011bn\u00e9\n$\\tau$", fontsize=9,
            fontweight="bold", color=COLORS[2], ha="center")

    # Equation
    ax.text(5, 5.5, "$\\alpha + \\rho + \\tau = 1$", fontsize=14, ha="center",
            fontweight="bold", color="black",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF3C7", edgecolor="#D97706"))

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q12_radiation_balance.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_two_surface_enclosure():
    """Schematic of radiation exchange between two gray surfaces in an enclosure."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    from matplotlib.patches import Rectangle

    # Surface 1 (hot, left)
    s1 = Rectangle((0.5, 1), 1.5, 4, facecolor="#FEE2E2", edgecolor="#DC2626", lw=2.5)
    ax.add_patch(s1)
    ax.text(1.25, 5.3, "Povrch 1", fontsize=11, fontweight="bold", color="#DC2626", ha="center")
    ax.text(1.25, 3, "$T_1, \\varepsilon_1$\n$A_1$", fontsize=12, ha="center", va="center",
            color="#DC2626", fontweight="bold")

    # Surface 2 (cold, right)
    s2 = Rectangle((8, 1), 1.5, 4, facecolor="#DBEAFE", edgecolor="#2563EB", lw=2.5)
    ax.add_patch(s2)
    ax.text(8.75, 5.3, "Povrch 2", fontsize=11, fontweight="bold", color="#2563EB", ha="center")
    ax.text(8.75, 3, "$T_2, \\varepsilon_2$\n$A_2$", fontsize=12, ha="center", va="center",
            color="#2563EB", fontweight="bold")

    # Radiation waves between surfaces
    for y in [2, 3, 4]:
        xs = np.linspace(2.2, 7.8, 60)
        ys = y + 0.15 * np.sin(6 * np.pi * (xs - 2.2) / 5.6)
        ax.plot(xs, ys, color="#D97706", lw=1.2, alpha=0.5)

    # Net heat flow arrow
    ax.annotate("", xy=(7.5, 3), xytext=(2.5, 3),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=3))
    ax.text(5, 3.5, "$\\dot{Q}_{12}$", fontsize=16, ha="center", fontweight="bold",
            color="#D97706")

    # Medium label
    ax.text(5, 0.5, "Dokonale pr\u016fteplivn\u00e9 prost\u0159ed\u00ed (\u03c4 = 1, \u03b1 = 0)",
            fontsize=9, ha="center", style="italic", color="#555")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q12_enclosure.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_emissivity_chart():
    """Emissivity of various surfaces."""
    fig, ax = plt.subplots(figsize=(8, 5))

    surfaces = [
        "Le\u0161t\u011bn\u00fd hlin\u00edk", "Le\u0161t\u011bn\u00e1 m\u011b\u010f", "Oxidovan\u00e1 ocel",
        "B\u00edl\u00fd n\u00e1t\u011br", "Cihla", "\u010cern\u00fd n\u00e1t\u011br",
        "Voda", "Led/sn\u00edh"
    ]
    emissivities = [0.05, 0.07, 0.80, 0.90, 0.93, 0.97, 0.96, 0.97]
    colors_bar = ["#D97706" if e < 0.3 else "#2563EB" if e < 0.85 else "#16A34A" for e in emissivities]

    bars = ax.barh(surfaces, emissivities, color=colors_bar, edgecolor="white", height=0.6)

    for bar, eps in zip(bars, emissivities):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f"\u03b5 = {eps:.2f}", va="center", fontsize=10, fontweight="bold")

    ax.set_xlabel("Emisivita \u03b5 [-]", fontsize=11)
    ax.set_title("Emisivita vybran\u00fdch povrch\u016f p\u0159i pokojov\u00e9 teplot\u011b",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(0, 1.15)
    ax.invert_yaxis()

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q12_emissivity.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH DOKUMENTU
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_planck = generate_planck_curves()
    img_sb = generate_stefan_boltzmann()
    img_balance = generate_radiation_balance()
    img_encl = generate_two_surface_enclosure()
    img_emis = generate_emissivity_chart()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="12. Z\u00e1kladn\u00ed z\u00e1kony s\u00e1l\u00e1n\u00ed absolutn\u011b \u010dern\u00e9ho t\u011blesa.\n"
              "      S\u00e1l\u00e1n\u00ed skute\u010dn\u00fdch t\u011bles. P\u0159enos tepla s\u00e1l\u00e1n\u00edm mezi dv\u011bma\n"
              "      \u0161ed\u00fdmi povrchy, soustava uzav\u0159en\u00e1.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Uve\u010fte z\u00e1kladn\u00ed z\u00e1kony s\u00e1l\u00e1n\u00ed absolutn\u011b \u010dern\u00e9ho t\u011blesa (Planck, Wien, "
        "Stefan-Boltzmann, Kirchhoff). Vysv\u011btlete s\u00e1l\u00e1n\u00ed skute\u010dn\u00fdch (\u0161ed\u00fdch) t\u011bles. "
        "Odvo\u010fte vztah pro p\u0159enos tepla s\u00e1l\u00e1n\u00edm mezi dv\u011bma \u0161ed\u00fdmi povrchy v uzav\u0159en\u00e9 "
        "soustav\u011b odd\u011blen\u00e9 dokonale pr\u016fteplivn\u00fdm prost\u0159ed\u00edm.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    # -- 1.1 --
    add_heading(doc, "1.1 Absolutn\u011b \u010dern\u00e9 t\u011bleso", level=3)

    add_info_box(doc,
        "Definice: Absolutn\u011b \u010dern\u00e9 t\u011bleso",
        "Ide\u00e1ln\u00ed t\u011bleso, kter\u00e9 pohlcuje ve\u0161ker\u00e9 dopadaj\u00edc\u00ed z\u00e1\u0159en\u00ed p\u0159i v\u0161ech vlnov\u00fdch "
        "d\u00e9lk\u00e1ch a \u00fahlech dopadu (\u03b1 = 1, \u03c1 = 0, \u03c4 = 0). Sou\u010dasn\u011b je nejlep\u0161\u00edm "
        "mo\u017en\u00fdm z\u00e1\u0159i\u010dem (\u03b5 = 1). Realizace: dutina s mal\u00fdm otvorem.")

    # -- 1.2 Planck --
    add_heading(doc, "1.2 Planck\u016fv z\u00e1kon", level=3)

    add_para(doc,
        "Popisuje spektr\u00e1ln\u00ed rozlo\u017een\u00ed intenzity vyz\u00e1\u0159en\u00ed \u010dern\u00e9ho t\u011blesa:", keep_with_next=True)
    add_equation(doc, r"E_{0\lambda} = \frac{C_1}{\lambda^5} \cdot \frac{1}{e^{C_2/(\lambda T)} - 1}", label="1")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "C\u2081 = 2\u03c0hc\u00b2 = 3,742 \u00d7 10\u207b\u00b9\u2076 W\u00b7m\u00b2 \u2014 prvn\u00ed radia\u010dn\u00ed konstanta")
    add_bullet(doc, "C\u2082 = hc/k_B = 1,439 \u00d7 10\u207b\u00b2 m\u00b7K \u2014 druh\u00e1 radia\u010dn\u00ed konstanta")
    add_bullet(doc, "\u03bb \u2014 vlnov\u00e1 d\u00e9lka [m], T \u2014 teplota [K]", is_last=True)

    add_image(doc, img_planck, width_cm=14,
              caption="Obr. 1: Planckovy k\u0159ivky spektr\u00e1ln\u00edho vyz\u00e1\u0159en\u00ed pro r\u016fzn\u00e9 teploty")

    # -- 1.3 Wien --
    add_page_break(doc)
    add_heading(doc, "1.3 Wien\u016fv posunovac\u00ed z\u00e1kon", level=3)

    add_para(doc,
        "Vlnov\u00e1 d\u00e9lka maxim\u00e1ln\u00ed spektr\u00e1ln\u00ed intenzity se posouvá k krat\u0161\u00edm vlnov\u00fdm "
        "d\u00e9lk\u00e1m s rostouc\u00ed teplotou:", keep_with_next=True)
    add_equation(doc, r"\lambda_{max} \cdot T = 2898 \text{ \mu m \cdot K}", label="2")

    add_para(doc, "P\u0159\u00edklady:", keep_with_next=True)
    add_styled_table(doc,
        headers=["T\u011bleso", "T [K]", "\u03bb_max [\u03bcm]", "Oblast spektra"],
        data=[
            ["Slunce", "5778", "0,50", "Viditeln\u00e9 sv\u011btlo (zelenožlut\u00e1)"],
            ["\u017d\u00e1rovka", "2500", "1,16", "Bl\u00edzk\u00e9 infra\u010derven\u00e9"],
            ["Lidsk\u00e9 t\u011blo", "310", "9,35", "St\u0159edn\u00ed infra\u010derven\u00e9"],
            ["Pokoj (20 \u00b0C)", "293", "9,89", "St\u0159edn\u00ed infra\u010derven\u00e9"],
        ],
    )

    # -- 1.4 Stefan-Boltzmann --
    add_heading(doc, "1.4 Stefan-Boltzmann\u016fv z\u00e1kon", level=3)

    add_info_box(doc,
        "Stefan-Boltzmann\u016fv z\u00e1kon",
        "Celkov\u00e1 intenzita vyz\u00e1\u0159en\u00ed \u010dern\u00e9ho t\u011blesa (integr\u00e1l Planckovy funkce "
        "p\u0159es v\u0161echny vlnov\u00e9 d\u00e9lky) je \u00fam\u011brn\u00e1 \u010dtvrt\u00e9 mocnin\u011b teploty.")

    add_equation(doc, r"E_0 = \int_0^\infty E_{0\lambda} \, d\lambda = \sigma T^4", label="3")

    add_para(doc, "kde \u03c3 = 5,670 \u00d7 10\u207b\u2078 W/(m\u00b2\u00b7K\u2074) je Stefan-Boltzmannova konstanta.")

    add_image(doc, img_sb, width_cm=13,
              caption="Obr. 2: Stefan-Boltzmann\u016fv z\u00e1kon \u2014 srovn\u00e1n\u00ed \u010dern\u00e9ho t\u011blesa a \u0161ed\u00fdch povrch\u016f")

    # -- 1.5 Kirchhoff --
    add_page_break(doc)
    add_heading(doc, "1.5 Kirchhoff\u016fv z\u00e1kon", level=3)

    add_para(doc, "Bilance z\u00e1\u0159en\u00ed dopadaj\u00edc\u00edho na povrch:", keep_with_next=True)
    add_equation(doc, r"\alpha + \rho + \tau = 1", label="4")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "\u03b1 \u2014 absorptivita (pohlcen\u00fd pod\u00edl)")
    add_bullet(doc, "\u03c1 \u2014 reflektivita (odra\u017een\u00fd pod\u00edl)")
    add_bullet(doc, "\u03c4 \u2014 transmisivita (propust\u011bn\u00fd pod\u00edl)", is_last=True)

    add_image(doc, img_balance, width_cm=13,
              caption="Obr. 3: Bilance z\u00e1\u0159en\u00ed na povrchu t\u011blesa")

    add_para(doc, "Kirchhoff\u016fv z\u00e1kon: v termodynamick\u00e9 rovnov\u00e1ze:", keep_with_next=True)
    add_equation(doc, r"\varepsilon(\lambda, T) = \alpha(\lambda, T)", label="5")

    add_para(doc,
        "Emisivita se rovn\u00e1 absorptivit\u011b p\u0159i t\u00e9\u017ee vlnov\u00e9 d\u00e9lce a teplot\u011b. "
        "Dobr\u00fd z\u00e1\u0159i\u010d je vždy dobr\u00fd absorbér a naopak.")

    # -- 1.6 Sede teleso --
    add_heading(doc, "1.6 S\u00e1l\u00e1n\u00ed skute\u010dn\u00fdch (\u0161ed\u00fdch) t\u011bles", level=3)

    add_info_box(doc,
        "\u0160ed\u00e9 t\u011bleso",
        "T\u011bleso, jeho\u017e emisivita \u03b5 je konstantn\u00ed pro v\u0161echny vlnov\u00e9 d\u00e9lky (nez\u00e1vis\u00ed na \u03bb), "
        "ale je men\u0161\u00ed ne\u017e 1. V\u011bt\u0161ina technick\u00fdch povrch\u016f se modeluje jako \u0161ed\u00e9 t\u011bleso.")

    add_equation(doc, r"E = \varepsilon \sigma T^4, \quad 0 < \varepsilon < 1", label="6")

    add_para(doc, "Pro nepr\u016fzra\u010dn\u00e9 \u0161ed\u00e9 t\u011bleso (\u03c4 = 0):", keep_with_next=True)
    add_equation(doc, r"\alpha + \rho = 1 \quad \Rightarrow \quad \varepsilon + \rho = 1 \quad \Rightarrow \quad \rho = 1 - \varepsilon", label="7")

    add_image(doc, img_emis, width_cm=13,
              caption="Obr. 4: Emisivita vybran\u00fdch technick\u00fdch povrch\u016f")

    # -- 1.7 Dva sede povrchy --
    add_page_break(doc)
    add_heading(doc, "1.7 P\u0159enos tepla s\u00e1l\u00e1n\u00edm mezi dv\u011bma \u0161ed\u00fdmi povrchy", level=3)

    add_info_box(doc,
        "P\u0159edpoklady",
        "1) Dv\u011b nepr\u016fzra\u010dn\u00e1 \u0161ed\u00e1 t\u011blesa v uzav\u0159en\u00e9 soustav\u011b.\n"
        "2) Prost\u0159ed\u00ed mezi nimi je dokonale pr\u016fteplivn\u00e9 (\u03c4 = 1, nepohlcuje ani nevyz\u00e1\u0159uje).\n"
        "3) Povrchy jsou difuzn\u00ed z\u00e1\u0159i\u010de (vyz\u00e1\u0159en\u00ed nez\u00e1vis\u00ed na sm\u011bru).\n"
        "4) Povrchy jsou izotermn\u00ed (konstantn\u00ed teplota po cel\u00e9 plo\u0161e).")

    add_image(doc, img_encl, width_cm=14,
              caption="Obr. 5: S\u00e1l\u00e1n\u00ed mezi dv\u011bma \u0161ed\u00fdmi povrchy v uzav\u0159en\u00e9 soustav\u011b")

    add_para(doc, "Obecn\u00fd vztah pro \u010dist\u00fd tepeln\u00fd tok:", keep_with_next=True)
    add_equation(doc, r"\dot{Q}_{12} = \frac{\sigma (T_1^4 - T_2^4)}{\frac{1 - \varepsilon_1}{\varepsilon_1 A_1} + \frac{1}{A_1 F_{12}} + \frac{1 - \varepsilon_2}{\varepsilon_2 A_2}}", label="8")

    add_para(doc, "kde F\u2081\u2082 je \u00fahlov\u00fd sou\u010dinitel (view factor, configuration factor).")

    add_para(doc, "Speci\u00e1ln\u00ed p\u0159\u00edpady:", bold=True, keep_with_next=True)

    add_para(doc, "a) Dva nekone\u010dn\u00e9 rovnob\u011b\u017en\u00e9 povrchy (A\u2081 = A\u2082 = A, F\u2081\u2082 = 1):", keep_with_next=True)
    add_equation(doc, r"\dot{Q}_{12} = \frac{A \sigma (T_1^4 - T_2^4)}{\frac{1}{\varepsilon_1} + \frac{1}{\varepsilon_2} - 1}", label="9")

    add_para(doc, "b) Mal\u00e9 t\u011bleso (A\u2081) obklopen\u00e9 velk\u00fdm povrchem (A\u2082 >> A\u2081, F\u2081\u2082 = 1):", keep_with_next=True)
    add_equation(doc, r"\dot{Q}_{12} = \varepsilon_1 A_1 \sigma (T_1^4 - T_2^4)", label="10")

    add_para(doc,
        "V tomto p\u0159\u00edpad\u011b z\u00e1le\u017e\u00ed pouze na emisivit\u011b mal\u00e9ho t\u011blesa \u03b5\u2081, "
        "proto\u017ee vn\u011bj\u0161\u00ed povrch se chov\u00e1 jako \u010dern\u00e9 t\u011bleso (v\u0161echno odra\u017een\u00e9 pohlt\u00ed).")

    add_para(doc, "c) Dva soustředn\u00e9 v\u00e1lce nebo koule (A\u2081 < A\u2082, F\u2081\u2082 = 1):", keep_with_next=True)
    add_equation(doc, r"\dot{Q}_{12} = \frac{A_1 \sigma (T_1^4 - T_2^4)}{\frac{1}{\varepsilon_1} + \frac{A_1}{A_2}\left(\frac{1}{\varepsilon_2} - 1\right)}", label="11")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 \u00dahlov\u00fd sou\u010dinitel (view factor) F\u2081\u2082", level=3)
    add_para(doc,
        "\u00dahlov\u00fd sou\u010dinitel F\u2081\u2082 ud\u00e1v\u00e1 pod\u00edl z\u00e1\u0159en\u00ed opou\u0161t\u011bj\u00edc\u00edho povrch 1, "
        "kter\u00fd dopad\u00e1 na povrch 2. Z\u00e1vis\u00ed \u010dist\u011b na geometrii.")

    add_para(doc, "Z\u00e1kladn\u00ed vlastnosti:", keep_with_next=True)
    add_bullet(doc, "Pravidlo sou\u010dtu: \u03a3 F_{ij} = 1 (v uzav\u0159en\u00e9 soustav\u011b)")
    add_bullet(doc, "Reciprocita: A\u2081\u00b7F\u2081\u2082 = A\u2082\u00b7F\u2082\u2081")
    add_bullet(doc, "Konvexn\u00ed povrch: F\u2081\u2081 = 0 (nevid\u00ed s\u00e1m sebe)")
    add_bullet(doc, "Dva rovnob\u011b\u017en\u00e9 nekone\u010dn\u00e9 povrchy: F\u2081\u2082 = 1", is_last=True)

    add_heading(doc, "2.2 Radia\u010dn\u00ed \u0161t\u00edty (stínění)", level=3)
    add_para(doc,
        "Vlo\u017een\u00ed n tenk\u00fdch \u0161t\u00edt\u016f s emisivitou \u03b5_s mezi dva paraleln\u00ed povrchy "
        "sn\u00ed\u017e\u00ed tepeln\u00fd tok s\u00e1l\u00e1n\u00edm na:", keep_with_next=True)
    add_equation(doc, r"\dot{Q}_{s \text{tity}} = \frac{\dot{Q}_{bez}}{n + 1}", label="12")
    add_para(doc, "(plat\u00ed pro \u0161t\u00edty se stejnou \u03b5 jako povrchy)")

    add_heading(doc, "2.3 Praktick\u00e9 aplikace", level=3)
    add_styled_table(doc,
        headers=["Aplikace", "Princip"],
        data=[
            ["Termoska", "Vakuum + le\u0161t\u011bn\u00e9 st\u011bny (\u03b5 \u2248 0,05)"],
            ["Kosmick\u00e9 lod\u011b", "V\u00edcevrstv\u00e1 izolace (MLI) \u2014 radia\u010dn\u00ed \u0161t\u00edty"],
            ["Pece a kotle", "Vys\u00e1l\u00e1n\u00ed dominuje p\u0159i T > 500 \u00b0C"],
            ["Termovize", "Detekce IR z\u00e1\u0159en\u00ed (\u03bb \u2248 8\u201314 \u03bcm)"],
            ["Slune\u010dn\u00ed kolektory", "Selektivn\u00ed povrch: \u03b1_sol vysok\u00e1, \u03b5_IR n\u00edzk\u00e1"],
            ["Sklen\u00edkov\u00fd efekt", "Sklo: \u03c4 pro VIS, \u03b1 pro IR"],
        ],
    )

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: S\u00e1l\u00e1n\u00ed mezi dv\u011bma rovnob\u011b\u017en\u00fdmi deskami", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Dv\u011b velk\u00e9 rovnob\u011b\u017en\u00e9 desky (A = 2 m\u00b2) s teplotami T\u2081 = 500 \u00b0C a "
        "T\u2082 = 100 \u00b0C. Emisivity: \u03b5\u2081 = 0,8 (oxidovan\u00e1 ocel), \u03b5\u2082 = 0,6 (hlin\u00edk s n\u00e1t\u011brem). "
        "Ur\u010dete \u010dist\u00fd tepeln\u00fd tok s\u00e1l\u00e1n\u00edm a ú\u010dinek vlo\u017een\u00ed jednoho radia\u010dn\u00edho \u0161t\u00edtu.",
        bold=True)

    add_para(doc, "Krok 1: Bez \u0161t\u00edtu (rovnice 9)", bold=True)
    add_equation(doc, r"\dot{Q}_{12} = \frac{A \sigma (T_1^4 - T_2^4)}{\frac{1}{\varepsilon_1} + \frac{1}{\varepsilon_2} - 1}")
    add_equation(doc, r"\dot{Q}_{12} = \frac{2 \times 5{,}67 \times 10^{-8} \times (773{,}15^4 - 373{,}15^4)}{\frac{1}{0{,}8} + \frac{1}{0{,}6} - 1}")
    add_equation(doc, r"\dot{Q}_{12} = \frac{2 \times 5{,}67 \times 10^{-8} \times (3{,}573 \times 10^{11} - 1{,}940 \times 10^{10})}{1{,}25 + 1{,}667 - 1}")
    add_equation(doc, r"\dot{Q}_{12} = \frac{2 \times 5{,}67 \times 10^{-8} \times 3{,}379 \times 10^{11}}{1{,}917} = \frac{38\,316}{1{,}917} = 19\,989 \text{ W} \approx 20{,}0 \text{ kW}")

    add_para(doc, "Krok 2: S jedn\u00edm \u0161t\u00edtem (\u03b5_s = 0,1, le\u0161t\u011bn\u00fd plech)", bold=True)
    add_para(doc, "Pro jeden \u0161t\u00edt se celkov\u00fd odpor p\u0159ibli\u017en\u011b zdvojn\u00e1sob\u00ed:", keep_with_next=True)
    add_equation(doc, r"\dot{Q}_{stit} \approx \frac{\dot{Q}_{bez}}{n + 1} = \frac{20{,}0}{2} = 10{,}0 \text{ kW}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Bez \u0161t\u00edtu: Q\u0307 \u2248 20 kW\n"
        "S 1 \u0161t\u00edtem: Q\u0307 \u2248 10 kW (sn\u00ed\u017een\u00ed o 50 %)\n\n"
        "Poznámka: Zjednodu\u0161en\u00fd v\u00fdpo\u010det s \u0161t\u00edtem (rovnice 12) plat\u00ed pro \u0161t\u00edty "
        "se stejnou \u03b5 jako povrchy. Pro le\u0161t\u011bn\u00fd \u0161t\u00edt (\u03b5_s = 0,1) by skute\u010dn\u00e9 "
        "sn\u00ed\u017een\u00ed bylo je\u0161t\u011b v\u00fdrazn\u011bj\u0161\u00ed.")

    # ==================================================================
    # CAST 4: ZKOUZKOVE OTAZKY
    # ==================================================================
    add_exam_questions(doc, [
        ("Vysv\u011btlete, pro\u010d intenzita vyz\u00e1\u0159en\u00ed roste se \u010dtvrtou mocninou teploty.",
         "Plyne z integrace Planckovy funkce p\u0159es v\u0161echny vlnov\u00e9 d\u00e9lky. "
         "Fyzik\u00e1ln\u011b: s rostouc\u00ed teplotou roste jak po\u010det vyzá\u0159ovan\u00fdch foton\u016f, "
         "tak jejich pr\u016fm\u011brn\u00e1 energie \u2014 oba efekty se n\u00e1sob\u00ed, v\u00fdsledek je T\u2074."),

        ("Co znamen\u00e1 Wien\u016fv posunovac\u00ed z\u00e1kon prakticky?",
         "\u0158\u00edk\u00e1, \u017ee \u010d\u00edm je t\u011bleso teplejší, t\u00edm krat\u0161\u00ed vlnov\u00e9 d\u00e9lky dominuj\u00ed "
         "ve spektru vyz\u00e1\u0159en\u00ed. Rozp\u00e1len\u00e9 \u017eelezo (1000 K) sv\u00edt\u00ed \u010derven\u011b, "
         "Slunce (5778 K) b\u00edle/\u017elut\u011b. Termovize detekuje IR z\u00e1\u0159en\u00ed t\u011bl p\u0159i 300 K."),

        ("Pro\u010d je le\u0161t\u011bn\u00fd kov \u0161patn\u00fdm z\u00e1\u0159i\u010dem i absorbérem?",
         "Kirchhoff\u016fv z\u00e1kon: \u03b5 = \u03b1. Le\u0161t\u011bn\u00fd kov m\u00e1 vysokou reflektivitu "
         "(\u03c1 > 0,9), tedy n\u00edzkou absorptivitu \u03b1 = 1 \u2212 \u03c1 < 0,1. "
         "Pod\u00edl absorbovan\u00e9ho z\u00e1\u0159en\u00ed je mal\u00fd, a proto je \u00fam\u011brn\u011b mal\u00fd i pod\u00edl vyzá\u0159ovan\u00e9ho."),

        ("Jak funguje radia\u010dn\u00ed \u0161t\u00edt a pro\u010d sni\u017euje tepeln\u00fd tok?",
         "\u0160t\u00edt p\u0159id\u00e1v\u00e1 dal\u0161\u00ed povrchov\u00e9 odpory (1\u2212\u03b5)/(\u03b5A) do radia\u010dn\u00ed s\u00edt\u011b. "
         "Ka\u017ed\u00fd \u0161t\u00edt mus\u00ed dos\u00e1hnout teplotn\u00ed rovnov\u00e1hy \u2014 absorbuje a vyz\u00e1\u0159uje, "
         "ale p\u0159i ni\u017e\u0161\u00ed teplot\u011b ne\u017e zdroj. N \u0161t\u00edt\u016f sn\u00ed\u017e\u00ed tok p\u0159ibli\u017en\u011b (n+1)\u00d7."),

        ("Pro\u010d u mal\u00e9ho t\u011blesa v velk\u00e9m prostoru z\u00e1le\u017e\u00ed jen na \u03b5\u2081?",
         "Velk\u00fd obklopuj\u00edc\u00ed povrch (A\u2082 >> A\u2081) pohlt\u00ed prakticky v\u0161echno z\u00e1\u0159en\u00ed "
         "\u2014 chov\u00e1 se jako \u010dern\u00e9 t\u011bleso (\u0159len z\u00e1\u0159en\u00ed odra\u017een\u00e9 od A\u2082 "
         "se vrac\u00ed na A\u2081 v zanedbateln\u00e9m pod\u00edlu). Proto rozhoduje jen schopnost "
         "A\u2081 vyz\u00e1\u0159it, tj. \u03b5\u2081."),

        ("Co je selektivn\u00ed povrch a kde se pou\u017e\u00edv\u00e1?",
         "Povrch, jeho\u017e \u03b5 (a \u03b1) z\u00e1vis\u00ed na vlnov\u00e9 d\u00e9lce \u2014 nen\u00ed \u0161ed\u00fd. "
         "Slune\u010dn\u00ed kolektory: vysok\u00e1 \u03b1 pro kr\u00e1tk\u00e9 vlny (sol\u00e1rn\u00ed spektrum), "
         "n\u00edzk\u00e1 \u03b5 pro dlouh\u00e9 vlny (IR \u2014 sn\u00ed\u017een\u00ed ztr\u00e1t vyzá\u0159ován\u00edm). "
         "P\u0159\u00edklad: \u010dern\u00fd chrom, TiNOx."),

        ("Jak\u00fd je rozd\u00edl mezi \u0161ed\u00fdm a \u010dern\u00fdm t\u011blesem?",
         "\u010cern\u00e9 t\u011bleso: \u03b5 = 1, \u03b1 = 1 \u2014 maxim\u00e1ln\u00ed z\u00e1\u0159en\u00ed i absorpce. "
         "\u0160ed\u00e9 t\u011bleso: \u03b5 < 1, konstantn\u00ed pro v\u0161echny \u03bb \u2014 re\u00e1ln\u00e1 aproximace, "
         "umo\u017e\u0148uje pou\u017e\u00edt jednoduché vzorce (E = \u03b5\u03c3T\u2074) m\u00edsto integrace p\u0159es spektrum."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Incropera, F.P. et al.: Fundamentals of Heat and Mass Transfer, 8th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cengel, Y.A.: Heat Transfer \u2014 A Practical Approach")
    add_bullet(doc, "Modest, M.F.: Radiative Heat Transfer, 3rd Ed.")
    add_bullet(doc, "Howell, J.R. et al.: Thermal Radiation Heat Transfer, 6th Ed.", is_last=True)

    save_and_export(doc, "12-salani")


if __name__ == "__main__":
    generate()
