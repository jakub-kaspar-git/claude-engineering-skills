# -*- coding: utf-8 -*-
"""
\u0053t\u00e1tnicov\u00e1 ot\u00e1zka 9: Z\u00e1kladn\u00ed druhy p\u0159enosu tepla a jejich stru\u010dn\u00e1 charakteristika.
Z\u00e1kladn\u00ed pojmy a z\u00e1kony.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.patches as mpatches

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

def generate_heat_transfer_modes():
    """Visual comparison of three heat transfer modes."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))

    # 1. Vedeni (kondukce)
    ax = axes[0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    # Wall
    wall = Rectangle((0.3, 0.1), 0.15, 0.8, facecolor="#FFD6D6", edgecolor="#DC2626", lw=2)
    ax.add_patch(wall)
    # Temperature labels
    ax.text(0.15, 0.5, "$T_1$", fontsize=16, ha="center", va="center", color="#DC2626", fontweight="bold")
    ax.text(0.6, 0.5, "$T_2$", fontsize=16, ha="center", va="center", color="#2563EB", fontweight="bold")
    ax.text(0.15, 0.35, "(hot)", fontsize=9, ha="center", color="#DC2626")
    ax.text(0.6, 0.35, "(cold)", fontsize=9, ha="center", color="#2563EB")
    # Arrow
    ax.annotate("", xy=(0.55, 0.7), xytext=(0.2, 0.7),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2.5))
    ax.text(0.375, 0.78, "$\\dot{Q}$", fontsize=14, ha="center", color="#D97706", fontweight="bold")
    ax.set_title("VEDENI (kondukce)", fontsize=11, fontweight="bold", color=COLORS[1])
    ax.text(0.375, 0.02, "Fourieruv zakon", fontsize=8, ha="center", style="italic", color="#555")

    # 2. Proudeni (konvekce)
    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    # Surface
    surf = Rectangle((0.1, 0.15), 0.8, 0.05, facecolor="#FFD6D6", edgecolor="#DC2626", lw=2)
    ax.add_patch(surf)
    ax.text(0.5, 0.1, "$T_w$", fontsize=14, ha="center", color="#DC2626", fontweight="bold")
    ax.text(0.5, 0.88, "$T_f$", fontsize=14, ha="center", color="#2563EB", fontweight="bold")
    # Wavy arrows (convection currents)
    for x_pos in [0.25, 0.5, 0.75]:
        ax.annotate("", xy=(x_pos, 0.8), xytext=(x_pos, 0.25),
                    arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2,
                                    connectionstyle="arc3,rad=0.15"))
    ax.set_title("PROUDENI (konvekce)", fontsize=11, fontweight="bold", color=COLORS[2])
    ax.text(0.5, 0.02, "Newtonuv zakon", fontsize=8, ha="center", style="italic", color="#555")

    # 3. Salani (radiace)
    ax = axes[2]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    # Two surfaces
    surf1 = Rectangle((0.05, 0.3), 0.15, 0.4, facecolor="#FFD6D6", edgecolor="#DC2626", lw=2)
    surf2 = Rectangle((0.75, 0.3), 0.15, 0.4, facecolor="#DBEAFE", edgecolor="#2563EB", lw=2)
    ax.add_patch(surf1)
    ax.add_patch(surf2)
    ax.text(0.125, 0.25, "$T_1$", fontsize=14, ha="center", color="#DC2626", fontweight="bold")
    ax.text(0.825, 0.25, "$T_2$", fontsize=14, ha="center", color="#2563EB", fontweight="bold")
    # Wavy radiation lines
    for y_off in [0.4, 0.5, 0.6]:
        xs = np.linspace(0.22, 0.73, 50)
        ys = y_off + 0.03 * np.sin(8 * np.pi * (xs - 0.22) / 0.51)
        ax.plot(xs, ys, color="#D97706", lw=1.5, alpha=0.7)
    ax.annotate("", xy=(0.73, 0.5), xytext=(0.63, 0.5),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2))
    ax.set_title("SALANI (radiace)", fontsize=11, fontweight="bold", color="#7C3AED")
    ax.text(0.5, 0.02, "Stefan-Boltzmannuv zakon", fontsize=8, ha="center", style="italic", color="#555")

    fig.suptitle("Tri zakladni zpusoby prenosu tepla", fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q09_heat_modes.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_fourier_temperature_profile():
    """Temperature profile through a flat wall (Fourier's law)."""
    fig, ax = plt.subplots(figsize=(7, 5))

    # Wall from x=0.2 to x=0.6, T linear
    x_wall = np.array([0.2, 0.6])
    T_wall = np.array([80, 20])

    # Fluid regions
    x_left = np.linspace(0, 0.2, 50)
    T_left = 100 - 20 * np.exp(5 * (x_left - 0.2))  # convective BL
    x_right = np.linspace(0.6, 1.0, 50)
    T_right = 10 + 10 * (1 - np.exp(-5 * (x_right - 0.6)))

    # Plot
    ax.fill_between([0.2, 0.6], -5, 110, alpha=0.1, color="gray")
    ax.plot(x_left, T_left, color=COLORS[1], linewidth=2.5, label="Konvekce (tekutina)")
    ax.plot(x_wall, T_wall, color=COLORS[0], linewidth=3, label="Vedeni (stena)")
    ax.plot(x_right, T_right, color=COLORS[2], linewidth=2.5)

    # Labels
    ax.text(0.4, 95, "STENA", fontsize=11, ha="center", fontweight="bold", color="gray")
    ax.text(0.08, 95, "Horka\ntekutina", fontsize=9, ha="center", color=COLORS[1])
    ax.text(0.82, 95, "Studena\ntekutina", fontsize=9, ha="center", color=COLORS[2])

    # Temperature annotations
    ax.annotate("$T_{w1}$", xy=(0.2, 80), xytext=(0.25, 88), fontsize=12,
                arrowprops=dict(arrowstyle="->", lw=1), fontweight="bold")
    ax.annotate("$T_{w2}$", xy=(0.6, 20), xytext=(0.55, 30), fontsize=12,
                arrowprops=dict(arrowstyle="->", lw=1), fontweight="bold")

    # Heat flux arrow
    ax.annotate("", xy=(0.75, 50), xytext=(0.25, 50),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=3))
    ax.text(0.5, 54, "$\\dot{q}$", fontsize=14, ha="center", color="#D97706", fontweight="bold")

    ax.set_xlabel("Poloha x [m]", fontsize=11)
    ax.set_ylabel("Teplota T [\u00b0C]", fontsize=11)
    ax.set_title("Teplotni profil: konvekce \u2192 vedeni stenou \u2192 konvekce",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(-5, 110)
    ax.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q09_fourier_profile.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_thermal_conductivity_chart():
    """Bar chart of thermal conductivity for various materials."""
    fig, ax = plt.subplots(figsize=(8, 5))

    materials = [
        "Medi (Cu)", "Hlinik (Al)", "Ocel", "Sklo",
        "Voda", "Vzduch", "Polystyren\n(izolace)"
    ]
    lambdas = [385, 237, 50, 1.0, 0.6, 0.026, 0.035]
    colors_bar = ["#D97706", "#D97706", "#D97706", "#2563EB",
                  "#2563EB", "#16A34A", "#16A34A"]

    bars = ax.barh(materials, lambdas, color=colors_bar, edgecolor="white", height=0.6)
    ax.set_xscale("log")

    for bar, val in zip(bars, lambdas):
        ax.text(bar.get_width() * 1.3, bar.get_y() + bar.get_height()/2,
                f"{val} W/(m\u00b7K)", va="center", fontsize=9, fontweight="bold")

    # Category labels
    ax.text(500, 5.8, "Kovy", fontsize=9, color="#D97706", fontweight="bold")
    ax.text(500, 3.8, "Nekov. lat.", fontsize=9, color="#2563EB", fontweight="bold")
    ax.text(500, 1.8, "Izolace/plyny", fontsize=9, color="#16A34A", fontweight="bold")

    ax.set_xlabel("Soucinitel tepelne vodivosti \u03bb [W/(m\u00b7K)]", fontsize=11)
    ax.set_title("Tepelna vodivost vybranych materialu", fontsize=12, fontweight="bold")
    ax.set_xlim(0.01, 2000)
    ax.invert_yaxis()

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q09_conductivity.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_convection_types():
    """Diagram comparing natural vs forced convection."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")

    # Natural convection
    ax = axes[0]
    plate = Rectangle((0.35, 0.05), 0.08, 0.9, facecolor="#FFD6D6", edgecolor="#DC2626", lw=2)
    ax.add_patch(plate)
    # Upward arrows (buoyancy driven)
    for x_off, alpha in [(0.5, 0.8), (0.55, 0.5), (0.6, 0.3)]:
        ax.annotate("", xy=(x_off, 0.85), xytext=(x_off, 0.15),
                    arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2, alpha=alpha))
    ax.text(0.39, 0.5, "T_w", fontsize=11, ha="center", va="center", color="#DC2626",
            fontweight="bold", rotation=90)
    ax.text(0.75, 0.5, "Vztlakove\nproudeni\n(Archimed.)", fontsize=9, ha="center",
            va="center", color="#555")
    ax.set_title("PRIROZENA konvekce", fontsize=11, fontweight="bold", color=COLORS[1])
    ax.text(0.5, -0.05, "Nu = f(Gr, Pr)", fontsize=9, ha="center", style="italic", color="#555")

    # Forced convection
    ax = axes[1]
    plate = Rectangle((0.1, 0.35), 0.8, 0.08, facecolor="#FFD6D6", edgecolor="#DC2626", lw=2)
    ax.add_patch(plate)
    # Horizontal arrows (flow driven)
    for y_off in [0.5, 0.6, 0.7, 0.8]:
        alpha = 1.0 - (y_off - 0.5) * 1.5
        ax.annotate("", xy=(0.85, y_off), xytext=(0.15, y_off),
                    arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2, alpha=max(alpha, 0.2)))
    ax.text(0.5, 0.3, "T_w", fontsize=11, ha="center", color="#DC2626", fontweight="bold")
    ax.text(0.5, 0.88, "Vynuceny proud u_inf", fontsize=9, ha="center", color="#2563EB")
    ax.text(0.5, 0.15, "Mezni vrstva", fontsize=8, ha="center", style="italic", color="#555")
    ax.set_title("NUCENA konvekce", fontsize=11, fontweight="bold", color=COLORS[0])
    ax.text(0.5, -0.05, "Nu = f(Re, Pr)", fontsize=9, ha="center", style="italic", color="#555")

    fig.suptitle("Typy konvekce", fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q09_convection_types.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_radiation_spectrum():
    """Planck's law: spectral emissive power for different temperatures."""
    fig, ax = plt.subplots(figsize=(8, 5))

    h = 6.626e-34
    c = 3e8
    k = 1.381e-23

    temps = [3000, 4000, 5000, 5778]
    labels = ["3000 K", "4000 K", "5000 K", "5778 K (Slunce)"]

    for i, (T, lbl) in enumerate(zip(temps, labels)):
        lam = np.linspace(0.1e-6, 5e-6, 500)
        # Planck's law
        E = (2 * np.pi * h * c**2 / lam**5) / (np.exp(h * c / (lam * k * T)) - 1)
        ax.plot(lam * 1e6, E / 1e12, color=COLORS[i % len(COLORS)], linewidth=2, label=lbl)

    # Wien's displacement law peak markers
    for T, color_idx in zip(temps, range(4)):
        lam_max = 2.898e-3 / T
        E_max = (2 * np.pi * h * c**2 / lam_max**5) / (np.exp(h * c / (lam_max * k * T)) - 1)
        ax.plot(lam_max * 1e6, E_max / 1e12, "o", color=COLORS[color_idx % len(COLORS)],
                markersize=6, zorder=5)

    # Visible spectrum band
    ax.axvspan(0.38, 0.75, alpha=0.08, color="yellow")
    ax.text(0.56, ax.get_ylim()[1] * 0.92, "VIS", fontsize=8, ha="center", color="#555")

    ax.set_xlabel("Vlnova delka \u03bb [\u03bcm]", fontsize=11)
    ax.set_ylabel("Spektralni intenzita vyzarovani [TW/(m\u00b2\u00b7\u03bcm)]", fontsize=11)
    ax.set_title("Planckov zakon: spektralni vyzarovani cerneho telesa",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(0, 4)
    ax.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q09_planck.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH DOKUMENTU
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_modes = generate_heat_transfer_modes()
    img_fourier = generate_fourier_temperature_profile()
    img_lambda = generate_thermal_conductivity_chart()
    img_conv = generate_convection_types()
    img_planck = generate_radiation_spectrum()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="9. Z\u00e1kladn\u00ed druhy p\u0159enosu tepla a jejich stru\u010dn\u00e1 charakteristika.\n"
              "    Z\u00e1kladn\u00ed pojmy a z\u00e1kony.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    # == ZADANI ==
    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Vysv\u011btlete t\u0159i z\u00e1kladn\u00ed druhy p\u0159enosu tepla (veden\u00ed, proud\u011bn\u00ed, s\u00e1l\u00e1n\u00ed). "
        "Uve\u010fte z\u00e1kladn\u00ed pojmy (tepeln\u00fd tok, hustota tepeln\u00e9ho toku, tepeln\u00e1 vodivost, "
        "sou\u010dinitel p\u0159estupu tepla) a z\u00e1kladn\u00ed z\u00e1kony (Fourier\u016fv, Newton\u016fv, Stefan-Boltzmann\u016fv).")

    # ==================================================================
    # CAST 1: TEORETICKY ROZBOR
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    # -- 1.1 --
    add_heading(doc, "1.1 P\u0159ehled t\u0159\u00ed zp\u016fsob\u016f p\u0159enosu tepla", level=3)

    add_image(doc, img_modes, width_cm=14,
              caption="Obr. 1: T\u0159i z\u00e1kladn\u00ed zp\u016fsoby p\u0159enosu tepla \u2014 veden\u00ed, proud\u011bn\u00ed, s\u00e1l\u00e1n\u00ed")

    add_styled_table(doc,
        headers=["Vlastnost", "Veden\u00ed (kondukce)", "Proud\u011bn\u00ed (konvekce)", "S\u00e1l\u00e1n\u00ed (radiace)"],
        data=[
            ["Mechanismus", "Vibrace a kolize \u010d\u00e1stic", "Pohyb tekutiny", "Elektromagn. vln\u011bn\u00ed"],
            ["Prost\u0159ed\u00ed", "Tuh\u00e9 l\u00e1tky (i tekutiny)", "Tekutiny (plyn, kapalina)", "Nevyžaduje (i vakuum)"],
            ["Z\u00e1kladn\u00ed z\u00e1kon", "Fourier\u016fv", "Newton\u016fv", "Stefan-Boltzmann\u016fv"],
            ["Kl\u00ed\u010dov\u00e1 veli\u010dina", "\u03bb [W/(m\u00b7K)]", "\u03b1 [W/(m\u00b2\u00b7K)]", "\u03c3, \u03b5 [\u2014]"],
            ["Teplotn\u00ed z\u00e1vislost", "Line\u00e1rn\u00ed (\u0394T)", "Line\u00e1rn\u00ed (\u0394T)", "Nelineárn\u00ed (T\u2074)"],
        ],
    )

    # -- 1.2 Zakladni pojmy --
    add_heading(doc, "1.2 Z\u00e1kladn\u00ed pojmy", level=3)

    add_info_box(doc,
        "Tepeln\u00fd tok Q\u0307 [W]",
        "Mno\u017estv\u00ed tepla p\u0159enesen\u00e9 za jednotku \u010dasu. Ekvivalent tepeln\u00e9ho v\u00fdkonu.\n"
        "Q\u0307 = dQ/dt [W = J/s]")

    add_para(doc, "Hustota tepeln\u00e9ho toku (tepeln\u00fd tok na jednotku plochy):", keep_with_next=True)
    add_equation(doc, r"\dot{q} = \frac{\dot{Q}}{A} \quad [\text{W/m}^2]", label="1")

    add_para(doc, "Tepeln\u00fd odpor (analogie s elektrick\u00fdm odporem):", keep_with_next=True)
    add_equation(doc, r"R_t = \frac{\Delta T}{\dot{Q}} \quad [\text{K/W}]", label="2")

    add_para(doc,
        "Tepeln\u00e9 odpory se s\u010d\u00edtaj\u00ed p\u0159i s\u00e9riov\u00e9m \u0159azen\u00ed (prostup v\u00edcevrstvou st\u011bnou) "
        "a po\u010d\u00edtaj\u00ed jako paraleln\u00ed p\u0159i v\u011btven\u00ed tepeln\u00e9ho toku.")

    # -- 1.3 Fourieruv zakon --
    add_page_break(doc)
    add_heading(doc, "1.3 Veden\u00ed tepla \u2014 Fourier\u016fv z\u00e1kon", level=3)

    add_info_box(doc,
        "Fourier\u016fv z\u00e1kon veden\u00ed tepla",
        "Hustota tepeln\u00e9ho toku je \u00fam\u011brn\u00e1 z\u00e1porn\u00e9mu teplotn\u00edmu gradientu. "
        "Teplo proud\u00ed ve sm\u011bru klesaj\u00edc\u00ed teploty.")

    add_equation(doc, r"\dot{q} = -\lambda \frac{dT}{dx}", label="3")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "\u03bb \u2014 sou\u010dinitel tepeln\u00e9 vodivosti [W/(m\u00b7K)] \u2014 materi\u00e1lov\u00e1 vlastnost")
    add_bullet(doc, "dT/dx \u2014 teplotn\u00ed gradient [K/m]")
    add_bullet(doc, "Z\u00e1porn\u00e9 znam\u00e9nko zaji\u0161\u0165uje, \u017ee q\u0307 > 0 ve sm\u011bru klesaj\u00edc\u00ed T", is_last=True)

    add_para(doc, "Pro celkov\u00fd tepeln\u00fd tok rovinnou st\u011bnou tlou\u0161\u0165ky \u03b4:", keep_with_next=True)
    add_equation(doc, r"\dot{Q} = \frac{\lambda A}{\delta} (T_1 - T_2)", label="4")

    add_image(doc, img_lambda, width_cm=13,
              caption="Obr. 2: Sou\u010dinitel tepeln\u00e9 vodivosti \u03bb vybran\u00fdch materi\u00e1l\u016f \u2014 rozp\u011bt\u00ed p\u0159es 4 \u0159\u00e1dy")

    add_image(doc, img_fourier, width_cm=13,
              caption="Obr. 3: Teplotn\u00ed profil p\u0159i prostupu tepla: konvekce \u2192 veden\u00ed st\u011bnou \u2192 konvekce")

    # -- 1.4 Newtonuv zakon --
    add_page_break(doc)
    add_heading(doc, "1.4 Proud\u011bn\u00ed (konvekce) \u2014 Newton\u016fv z\u00e1kon ochlazen\u00ed", level=3)

    add_info_box(doc,
        "Newton\u016fv z\u00e1kon ochlazen\u00ed",
        "Tepeln\u00fd tok konvekc\u00ed je \u00fam\u011brn\u00fd rozd\u00edlu teplot povrchu a tekutiny.\n"
        "Je to sp\u00ed\u0161e definice sou\u010dinitele p\u0159estupu tepla \u03b1 ne\u017e fyzik\u00e1ln\u00ed z\u00e1kon.")

    add_equation(doc, r"\dot{q} = \alpha (T_w - T_f)", label="5")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "\u03b1 \u2014 sou\u010dinitel p\u0159estupu tepla [W/(m\u00b2\u00b7K)]")
    add_bullet(doc, "T_w \u2014 teplota povrchu (st\u011bny)")
    add_bullet(doc, "T_f \u2014 teplota tekutiny (v dostate\u010dn\u00e9 vzd\u00e1lenosti od povrchu)", is_last=True)

    add_warning_box(doc,
        "\u03b1 nen\u00ed materi\u00e1lov\u00e1 konstanta! Z\u00e1vis\u00ed na typu proud\u011bn\u00ed, geometrii, "
        "rychlosti, vlastnostech tekutiny a teplotn\u00edm rozd\u00edlu. Ur\u010duje se "
        "z kriteriln\u00edch rovnic (Nu = f(Re, Pr) nebo Nu = f(Gr, Pr)).")

    add_para(doc, "Nusseltovo \u010d\u00edslo \u2014 bezrozm\u011brn\u00fd sou\u010dinitel p\u0159estupu tepla:", keep_with_next=True)
    add_equation(doc, r"\text{Nu} = \frac{\alpha L}{\lambda_f}", label="6")

    add_para(doc, "Typick\u00e9 hodnoty \u03b1:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["Typ konvekce", "\u03b1 [W/(m\u00b2\u00b7K)]"],
        data=[
            ["P\u0159irozen\u00e1, vzduch", "5\u201325"],
            ["Nucen\u00e1, vzduch", "25\u2013250"],
            ["P\u0159irozen\u00e1, voda", "100\u20131 000"],
            ["Nucen\u00e1, voda", "500\u201310 000"],
            ["Var a kondenzace", "2 500\u2013100 000"],
        ],
    )

    add_image(doc, img_conv, width_cm=13,
              caption="Obr. 4: P\u0159irozen\u00e1 vs. nucen\u00e1 konvekce \u2014 hnac\u00ed s\u00edla a kriteriln\u00ed rovnice")

    # -- 1.5 Stefan-Boltzmannuv zakon --
    add_page_break(doc)
    add_heading(doc, "1.5 S\u00e1l\u00e1n\u00ed (radiace) \u2014 Stefan-Boltzmann\u016fv z\u00e1kon", level=3)

    add_info_box(doc,
        "Stefan-Boltzmann\u016fv z\u00e1kon",
        "Celkov\u00e1 intenzita vyz\u00e1\u0159en\u00ed absolutn\u011b \u010dern\u00e9ho t\u011blesa je \u00fam\u011brn\u00e1 \u010dtvrt\u00e9 mocnin\u011b "
        "jeho termodynamick\u00e9 teploty. Pro re\u00e1ln\u00e1 t\u011blesa se n\u00e1sob\u00ed emisivitou \u03b5.")

    add_equation(doc, r"E_0 = \sigma T^4", label="7")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "\u03c3 = 5,67 \u00d7 10\u207b\u2078 W/(m\u00b2\u00b7K\u2074) \u2014 Stefan-Boltzmannova konstanta")
    add_bullet(doc, "T \u2014 termodynamick\u00e1 teplota [K] (mus\u00ed b\u00fdt v kelvinech!)")
    add_bullet(doc, "E\u2080 \u2014 intenzita vyz\u00e1\u0159en\u00ed absolutn\u011b \u010dern\u00e9ho t\u011blesa [W/m\u00b2]", is_last=True)

    add_para(doc, "Pro re\u00e1ln\u00e9 (\"\u0161ed\u00e9\") t\u011bleso:", keep_with_next=True)
    add_equation(doc, r"E = \varepsilon \sigma T^4", label="8")

    add_para(doc,
        "kde \u03b5 \u2208 (0, 1) je emisivita povrchu. Pro v\u011bt\u0161inu technick\u00fdch povrch\u016f "
        "\u03b5 = 0,1\u20130,95. Le\u0161t\u011bn\u00e9 kovy maj\u00ed \u03b5 \u2248 0,05\u20130,1, oxidovan\u00e9 povrchy 0,6\u20130,9.")

    add_para(doc, "Wien\u016fv posunovac\u00ed z\u00e1kon:", keep_with_next=True)
    add_equation(doc, r"\lambda_{max} \cdot T = 2898 \text{ \mu m \cdot K}", label="9")

    add_para(doc, "Planck\u016fv z\u00e1kon spektr\u00e1ln\u00edho vyz\u00e1\u0159en\u00ed:", keep_with_next=True)
    add_equation(doc, r"E_{0\lambda} = \frac{2\pi h c^2}{\lambda^5} \cdot \frac{1}{e^{hc/(\lambda k T)} - 1}", label="10")

    add_image(doc, img_planck, width_cm=13,
              caption="Obr. 5: Planck\u016fv z\u00e1kon \u2014 spektr\u00e1ln\u00ed intenzita vyz\u00e1\u0159en\u00ed \u010dern\u00e9ho t\u011blesa pro r\u016fzn\u00e9 teploty")

    # -- 1.6 Kirchhoffuv zakon --
    add_heading(doc, "1.6 Kirchhoff\u016fv z\u00e1kon a bilance z\u00e1\u0159en\u00ed", level=3)

    add_para(doc,
        "P\u0159i dopadu z\u00e1\u0159en\u00ed na povrch se \u010d\u00e1st pohlt\u00ed (absorpce A), "
        "\u010d\u00e1st odraz\u00ed (reflexe R) a \u010d\u00e1st projde (transmise \u03c4):", keep_with_next=True)
    add_equation(doc, r"A + R + \tau = 1", label="11")

    add_para(doc,
        "Pro nepr\u016fzra\u010dn\u00e1 t\u011blesa (\u03c4 = 0): A + R = 1. Kirchhoff\u016fv z\u00e1kon: "
        "p\u0159i termodynamick\u00e9 rovnov\u00e1ze plat\u00ed \u03b5 = A (emisivita se rovn\u00e1 absorptivit\u011b).")

    add_equation(doc, r"\varepsilon(\lambda, T) = A(\lambda, T)", label="12")

    # ==================================================================
    # CAST 2: PRAKTICKY ROZBOR
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Kdy dominuje kter\u00fd mechanismus", level=3)

    add_styled_table(doc,
        headers=["Situace", "Dominantn\u00ed mechanismus"],
        data=[
            ["Tepeln\u00e1 izolace budov", "Veden\u00ed (izolant) + konvekce (vzduch. mezery)"],
            ["Ch\u00e1zen\u00ed motoru", "Nucen\u00e1 konvekce (chlazen\u00ed kapalinou/vzduchem)"],
            ["Slune\u010dn\u00ed kolektor", "S\u00e1l\u00e1n\u00ed (p\u0159\u00edjem) + konvekce (ztr\u00e1ty)"],
            ["Varn\u00e1 deska \u2192 hrnec", "Veden\u00ed (kontakt) + konvekce (kapalina)"],
            ["Tepeln\u00fd \u0161t\u00edt raketopln\u00e1nu", "S\u00e1l\u00e1n\u00ed (dominantn\u00ed p\u0159i T > 1000 \u00b0C)"],
            ["V\u00fdm\u011bn\u00edk tepla", "V\u0161echny t\u0159i (konvekce + veden\u00ed + s\u00e1l\u00e1n\u00ed)"],
        ],
    )

    add_heading(doc, "2.2 Bezrozm\u011brn\u00e1 \u010d\u00edsla v p\u0159enosu tepla", level=3)

    add_styled_table(doc,
        headers=["\u010c\u00edslo", "Definice", "V\u00fdznam"],
        data=[
            ["Re (Reynolds)", "Re = u\u00b7L/\u03bd", "Pom\u011br setrva\u010dn\u00fdch a visk\u00f3zn\u00edch sil"],
            ["Pr (Prandtl)", "Pr = \u03bd/a = c_p\u00b7\u03bc/\u03bb", "Pom\u011br hybnostn\u00ed a tepeln\u00e9 difuzivity"],
            ["Nu (Nusselt)", "Nu = \u03b1\u00b7L/\u03bb", "Bezrozm\u011brn\u00fd p\u0159estup tepla"],
            ["Gr (Grashof)", "Gr = g\u00b7\u03b2\u00b7\u0394T\u00b7L\u00b3/\u03bd\u00b2", "Pom\u011br vztlakov\u00fdch a visk\u00f3zn\u00edch sil"],
            ["Ra (Rayleigh)", "Ra = Gr\u00b7Pr", "Kritick\u00e9 \u010d\u00edslo pro p\u0159irozenou konvekci"],
        ],
    )

    add_heading(doc, "2.3 Tepeln\u00e1 analogie: elektrický obvod", level=3)

    add_para(doc,
        "P\u0159enos tepla lze modelovat analogicky s elektrick\u00fdm obvodem: "
        "teplotn\u00ed rozd\u00edl \u0394T odpov\u00edd\u00e1 nap\u011bt\u00ed U, tepeln\u00fd tok Q\u0307 odpov\u00edd\u00e1 proudu I, "
        "tepeln\u00fd odpor R_t odpov\u00edd\u00e1 elektrick\u00e9mu odporu R.")

    add_styled_table(doc,
        headers=["Elektrick\u00e1 veli\u010dina", "Tepeln\u00e1 analogie"],
        data=[
            ["Nap\u011bt\u00ed U [V]", "Teplotn\u00ed rozd\u00edl \u0394T [K]"],
            ["Proud I [A]", "Tepeln\u00fd tok Q\u0307 [W]"],
            ["Odpor R [\u03a9]", "Tepeln\u00fd odpor R_t [K/W]"],
            ["Ohm\u016fv z\u00e1kon: U = R\u00b7I", "Fourier: \u0394T = R_t\u00b7Q\u0307"],
        ],
    )

    # ==================================================================
    # CAST 3: ILUSTRACNI PRIKLAD
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Porovn\u00e1n\u00ed tepeln\u00fdch tok\u016f t\u0159emi mechanismy", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Ocelov\u00e1 deska (A = 1 m\u00b2, \u03b4 = 10 mm, \u03bb = 50 W/(m\u00b7K)) m\u00e1 na jedn\u00e9 stran\u011b "
        "teplotu T\u2081 = 200 \u00b0C a na druh\u00e9 T\u2082 = 180 \u00b0C. Na povrchu s T\u2081 proud\u00ed vzduch o teplot\u011b "
        "T_f = 25 \u00b0C s \u03b1 = 50 W/(m\u00b2\u00b7K). Povrch m\u00e1 emisivitu \u03b5 = 0,8. "
        "Spo\u010dt\u011bte tepeln\u00e9 toky v\u0161emi t\u0159emi mechanismy.", bold=True)

    add_para(doc, "Krok 1: Veden\u00ed (Fourier)", bold=True)
    add_equation(doc, r"\dot{Q}_{ved} = \frac{\lambda A}{\delta}(T_1 - T_2) = \frac{50 \times 1}{0{,}01}(200 - 180) = 100\,000 \text{ W} = 100 \text{ kW}")

    add_para(doc, "Krok 2: Konvekce (Newton)", bold=True)
    add_equation(doc, r"\dot{Q}_{konv} = \alpha A (T_1 - T_f) = 50 \times 1 \times (200 - 25) = 8\,750 \text{ W} = 8{,}75 \text{ kW}")

    add_para(doc, "Krok 3: S\u00e1l\u00e1n\u00ed (Stefan-Boltzmann)", bold=True)
    add_equation(doc, r"\dot{Q}_{s\acute{a}l} = \varepsilon \sigma A (T_1^4 - T_f^4) = 0{,}8 \times 5{,}67 \times 10^{-8} \times 1 \times (473{,}15^4 - 298{,}15^4)")
    add_equation(doc, r"\dot{Q}_{s\acute{a}l} = 0{,}8 \times 5{,}67 \times 10^{-8} \times (5{,}01 \times 10^{10} - 0{,}79 \times 10^{10}) = 1\,916 \text{ W} \approx 1{,}92 \text{ kW}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Veden\u00ed: 100 kW | Konvekce: 8,75 kW | S\u00e1l\u00e1n\u00ed: 1,92 kW\n\n"
        "P\u0159i t\u011bchto teplot\u00e1ch (200 \u00b0C) dominuje veden\u00ed. S\u00e1l\u00e1n\u00ed je v\u00fdznamn\u00e9 "
        "a\u017e p\u0159i vy\u0161\u0161\u00edch teplot\u00e1ch (> 500 \u00b0C), kde roste s T\u2074.")

    # ==================================================================
    # CAST 4: ZKOUZKOVE OTAZKY
    # ==================================================================
    add_exam_questions(doc, [
        ("Vysv\u011btlete, pro\u010d m\u00e1 Fourier\u016fv z\u00e1kon z\u00e1porn\u00e9 znam\u00e9nko.",
         "Z\u00e1porn\u00e9 znam\u00e9nko zaji\u0161\u0165uje, \u017ee tepeln\u00fd tok sm\u011b\u0159uje ve sm\u011bru klesaj\u00edc\u00ed teploty "
         "(od tepl\u00e9ho k studen\u00e9mu). Teplotn\u00ed gradient dT/dx je z\u00e1porn\u00fd ve sm\u011bru toku tepla, "
         "tak\u017ee minus kr\u00e1t minus d\u00e1v\u00e1 kladn\u00fd q\u0307."),

        ("Pro\u010d \u03b1 nen\u00ed materi\u00e1lov\u00e1 konstanta, zat\u00edmco \u03bb ano?",
         "\u03bb je vlastnost materi\u00e1lu \u2014 z\u00e1vis\u00ed jen na typu l\u00e1tky a teplot\u011b. "
         "\u03b1 z\u00e1vis\u00ed na geometrii, rychlosti proud\u011bn\u00ed, typu tekutiny, teplotn\u00edm rozd\u00edlu "
         "a re\u017eimu proud\u011bn\u00ed (lamin\u00e1rn\u00ed/turbulentn\u00ed). Je to sp\u00ed\u0161e v\u00fdpo\u010dtov\u00e1 veli\u010dina "
         "ne\u017e materi\u00e1lov\u00e1 vlastnost."),

        ("Kdy s\u00e1l\u00e1n\u00ed dominuje nad konvekc\u00ed a veden\u00edm?",
         "P\u0159i vysok\u00fdch teplot\u00e1ch (nad ~500 \u00b0C), proto\u017ee s\u00e1l\u00e1n\u00ed roste s T\u2074, zat\u00edmco "
         "konvekce a veden\u00ed rostou line\u00e1rn\u011b s \u0394T. Tak\u00e9 ve vakuu, kde konvekce "
         "neexistuje a veden\u00ed je minim\u00e1ln\u00ed (nap\u0159. kosmick\u00e9 aplikace)."),

        ("Jak\u00fd je rozd\u00edl mezi p\u0159irozenou a nucenou konvekc\u00ed?",
         "P\u0159irozen\u00e1 konvekce je hn\u00e1na vztlakov\u00fdmi s\u00edlami (rozd\u00edl hustot vlivem teplotn\u00edho gradientu). "
         "Nucen\u00e1 konvekce je hn\u00e1na extern\u00edm zdrojem (ventil\u00e1tor, \u010derpadlo). "
         "Nucen\u00e1 d\u00e1v\u00e1 \u0159\u00e1dov\u011b vy\u0161\u0161\u00ed \u03b1 (10\u2013100\u00d7) ne\u017e p\u0159irozen\u00e1."),

        ("Co \u0159\u00edk\u00e1 Kirchhoff\u016fv z\u00e1kon a jak\u00fd m\u00e1 praktick\u00fd v\u00fdznam?",
         "\u0158\u00edk\u00e1, \u017ee v termodynamick\u00e9 rovnov\u00e1ze se emisivita rovn\u00e1 absorptivit\u011b (\u03b5 = A). "
         "Praktick\u00fd v\u00fdznam: dobr\u00fd z\u00e1\u0159i\u010d je i dobr\u00fd absorbér. \u010cern\u00fd povrch "
         "m\u00e1 vysok\u00e9 \u03b5 i A, le\u0161t\u011bn\u00fd kov m\u00e1 n\u00edzk\u00e9 oboj\u00ed (odr\u00e1\u017e\u00ed z\u00e1\u0159en\u00ed)."),

        ("Vysv\u011btlete analogii mezi p\u0159enosem tepla a elektrick\u00fdm obvodem.",
         "\u0394T odpov\u00edd\u00e1 nap\u011bt\u00ed, Q\u0307 proudu, tepeln\u00fd odpor R_t elektrick\u00e9mu odporu. "
         "Prostup v\u00edcevrstvou st\u011bnou je s\u00e9riov\u00fd obvod (R_t se s\u010d\u00edtaj\u00ed). "
         "To umo\u017e\u0148uje snadn\u00fd v\u00fdpo\u010det slo\u017eit\u00fdch p\u0159\u00edpad\u016f metodou tepeln\u00fdch odpor\u016f."),

        ("Co je Nusseltovo \u010d\u00edslo a jak se pou\u017e\u00edv\u00e1?",
         "Nu = \u03b1L/\u03bb_f je bezrozm\u011brn\u00fd sou\u010dinitel p\u0159estupu tepla. Vyjadruje pom\u011br "
         "konvektivn\u00edho p\u0159enosu k \u010dist\u00e9mu veden\u00ed v tekutin\u011b. Z kriteriln\u00edch rovnic "
         "(Nu = f(Re, Pr) nebo Nu = f(Gr, Pr)) z\u00edsk\u00e1me \u03b1 = Nu\u00b7\u03bb_f/L."),
    ])

    # -- Zapati: Zdroje --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Incropera, F.P. et al.: Fundamentals of Heat and Mass Transfer, 8th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cengel, Y.A.: Heat Transfer \u2014 A Practical Approach, 2nd Ed.")
    add_bullet(doc, "Kozub\u00edk, T.: P\u0159enos tepla, VUT Brno")
    add_bullet(doc, "VDI Heat Atlas \u2014 kriteriln\u00ed rovnice a sou\u010dinitele", is_last=True)

    # -- Save --
    save_and_export(doc, "09-prenos-tepla")


if __name__ == "__main__":
    generate()
