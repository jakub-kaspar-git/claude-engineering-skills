# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 11: Stacion\u00e1rn\u00ed veden\u00ed a prostup tepla neomezenou st\u011bnou v\u00e1lcovou,
jednoduchou i slo\u017eenou.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

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

def generate_cylinder_cross_section():
    """Cross-section of a simple cylindrical wall with temperature profile."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: cross-section
    r1, r2 = 1.0, 1.8
    theta = np.linspace(0, 2 * np.pi, 100)

    # Inner and outer circles
    ax1.plot(r1 * np.cos(theta), r1 * np.sin(theta), color=COLORS[1], linewidth=2)
    ax1.plot(r2 * np.cos(theta), r2 * np.sin(theta), color=COLORS[0], linewidth=2)

    # Fill wall region
    theta_fill = np.linspace(0, 2 * np.pi, 100)
    ax1.fill_between(r2 * np.cos(theta_fill), r2 * np.sin(theta_fill),
                     alpha=0.1, color="gray")
    ax1.fill_between(r1 * np.cos(theta_fill), r1 * np.sin(theta_fill),
                     alpha=1.0, color="white")

    # Radii labels
    ax1.annotate("", xy=(r1, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="<->", color=COLORS[1], lw=1.5))
    ax1.text(r1 / 2, 0.15, "$r_1$", fontsize=12, ha="center", color=COLORS[1], fontweight="bold")

    ax1.annotate("", xy=(0, r2), xytext=(0, 0),
                arrowprops=dict(arrowstyle="<->", color=COLORS[0], lw=1.5))
    ax1.text(0.15, r2 / 2, "$r_2$", fontsize=12, ha="center", color=COLORS[0], fontweight="bold")

    # Temperature labels
    ax1.text(0, 0, "$T_1$", fontsize=14, ha="center", va="center", color=COLORS[1], fontweight="bold")
    ax1.text(r2 + 0.3, 0, "$T_2$", fontsize=14, ha="center", va="center", color=COLORS[0], fontweight="bold")

    # Heat flow arrows
    for angle in [45, 135, 225, 315]:
        rad = np.deg2rad(angle)
        ax1.annotate("", xy=((r2 + 0.3) * np.cos(rad), (r2 + 0.3) * np.sin(rad)),
                    xytext=((r1 + 0.1) * np.cos(rad), (r1 + 0.1) * np.sin(rad)),
                    arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=2))

    ax1.text(0, -r2 - 0.5, "$\\dot{Q}$ (radi\u00e1ln\u011b ven)", fontsize=10, ha="center",
             color="#D97706", fontweight="bold")
    ax1.set_xlim(-2.8, 2.8)
    ax1.set_ylim(-2.8, 2.8)
    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_title("P\u0159\u00ed\u010dn\u00fd \u0159ez v\u00e1lcovou st\u011bnou", fontsize=11, fontweight="bold")

    # Right: T(r) profile - logarithmic
    r = np.linspace(r1, r2, 100)
    T1, T2 = 200, 50
    T = T1 + (T2 - T1) * np.log(r / r1) / np.log(r2 / r1)

    ax2.plot(r, T, color=COLORS[0], linewidth=3, label="T(r) \u2014 logaritmick\u00fd")

    # Compare with linear (dashed)
    T_linear = T1 + (T2 - T1) * (r - r1) / (r2 - r1)
    ax2.plot(r, T_linear, "--", color="gray", linewidth=1.5, alpha=0.6, label="Line\u00e1rn\u00ed (rovinn\u00e1 st\u011bna)")

    ax2.axvline(x=r1, color=COLORS[1], linestyle=":", linewidth=1)
    ax2.axvline(x=r2, color=COLORS[0], linestyle=":", linewidth=1)
    ax2.text(r1 - 0.05, -5, "$r_1$", fontsize=11, ha="center", color=COLORS[1])
    ax2.text(r2 + 0.05, -5, "$r_2$", fontsize=11, ha="center", color=COLORS[0])

    ax2.set_xlabel("Polom\u011br r", fontsize=11)
    ax2.set_ylabel("Teplota T [\u00b0C]", fontsize=11)
    ax2.set_title("Teplotn\u00ed profil T(r) \u2014 logaritmick\u00fd pokles", fontsize=11, fontweight="bold")
    ax2.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q11_cylinder.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_insulated_pipe():
    """Multi-layer insulated pipe with temperature profile."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    # 3-layer pipe: pipe wall | insulation | cladding
    r_vals = [0.025, 0.030, 0.080, 0.085]  # m
    labels = ["Trubka\n(\u03bb\u2081=50)", "Izolace\n(\u03bb\u2082=0,04)", "Pl\u00e1\u0161\u0165\n(\u03bb\u2083=0,2)"]
    colors_layer = [COLORS[0], "#D97706", COLORS[2]]

    # Temperature profile (logarithmic in each layer)
    T_vals = [250, 248, 45, 43]  # temperatures at interfaces
    T_f1, T_f2 = 260, 20  # fluid temps

    # Plot each layer
    for i in range(3):
        r = np.linspace(r_vals[i], r_vals[i + 1], 100)
        T = T_vals[i] + (T_vals[i + 1] - T_vals[i]) * np.log(r / r_vals[i]) / np.log(r_vals[i + 1] / r_vals[i])
        ax.plot(r * 1000, T, color=colors_layer[i], linewidth=2.5,
                label=f"Vrstva {i + 1}: {labels[i]}")
        ax.fill_between([r_vals[i] * 1000, r_vals[i + 1] * 1000], -10, 270,
                       alpha=0.08, color=colors_layer[i])

    # Convective regions
    r_f1 = np.linspace(0, r_vals[0], 30)
    T_f1_profile = T_f1 - (T_f1 - T_vals[0]) * np.exp(-200 * (r_vals[0] - r_f1))
    ax.plot(r_f1 * 1000, T_f1_profile, color=COLORS[1], linewidth=2, linestyle="--")

    r_f2 = np.linspace(r_vals[3], 0.12, 30)
    T_f2_profile = T_f2 + (T_vals[3] - T_f2) * np.exp(-100 * (r_f2 - r_vals[3]))
    ax.plot(r_f2 * 1000, T_f2_profile, color=COLORS[2], linewidth=2, linestyle="--")

    # Mark temperature points
    for r, T in zip(r_vals, T_vals):
        ax.plot(r * 1000, T, "ko", markersize=6, zorder=5)

    ax.set_xlabel("Polom\u011br r [mm]", fontsize=11)
    ax.set_ylabel("Teplota T [\u00b0C]", fontsize=11)
    ax.set_title("Teplotn\u00ed profil izolovaného potrub\u00ed (3 vrstvy)\nlogaritmick\u00fd pokles v ka\u017ed\u00e9 vrstv\u011b",
                 fontsize=11, fontweight="bold")
    ax.set_xlim(0, 120)
    ax.set_ylim(-10, 270)
    ax.legend(fontsize=8, loc="upper right")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q11_insulated_pipe.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_critical_radius():
    """Plot total thermal resistance vs insulation radius showing critical radius."""
    fig, ax = plt.subplots(figsize=(7, 5))

    lambda_iz = 0.04  # insulation conductivity
    alpha_e = 10  # external convection coefficient
    r1 = 0.025  # pipe outer radius

    r_kr = lambda_iz / alpha_e  # critical radius = 0.004 m = 4 mm

    r2_range = np.linspace(r1, 0.15, 200)
    L = 1.0  # per meter of pipe

    R_ins = np.log(r2_range / r1) / (2 * np.pi * lambda_iz * L)
    R_conv = 1 / (2 * np.pi * r2_range * alpha_e * L)
    R_total = R_ins + R_conv

    ax.plot(r2_range * 1000, R_total, color=COLORS[0], linewidth=2.5, label="$R_{celk} = R_{\\lambda} + R_{\\alpha}$")
    ax.plot(r2_range * 1000, R_ins, "--", color=COLORS[3], linewidth=1.5, alpha=0.6, label="$R_{\\lambda}$ (izolace)")
    ax.plot(r2_range * 1000, R_conv, "--", color=COLORS[2], linewidth=1.5, alpha=0.6, label="$R_{\\alpha}$ (konvekce)")

    # Mark critical radius (only if r_kr > r1)
    if r_kr > r1:
        idx_kr = np.argmin(R_total)
        ax.plot(r2_range[idx_kr] * 1000, R_total[idx_kr], "ko", markersize=10, zorder=5)
        ax.annotate(f"Kritick\u00fd polom\u011br\nr_kr = {r_kr * 1000:.1f} mm",
                    xy=(r2_range[idx_kr] * 1000, R_total[idx_kr]),
                    xytext=(60, R_total[idx_kr] + 0.3),
                    fontsize=9, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", lw=1.5))

    # Mark original pipe radius
    ax.axvline(x=r1 * 1000, color="gray", linestyle=":", linewidth=1)
    ax.text(r1 * 1000 + 1, ax.get_ylim()[1] * 0.9, f"r\u2081 = {r1 * 1000:.0f} mm", fontsize=9, color="gray")

    ax.set_xlabel("Vn\u011bj\u0161\u00ed polom\u011br izolace r\u2082 [mm]", fontsize=11)
    ax.set_ylabel("Tepeln\u00fd odpor R [K/W na 1 m]", fontsize=11)
    ax.set_title("Kritick\u00fd polom\u011br izolace\n$r_{kr} = \\lambda_{iz} / \\alpha_e$",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q11_critical_radius.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH DOKUMENTU
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_cyl = generate_cylinder_cross_section()
    img_pipe = generate_insulated_pipe()
    img_rkr = generate_critical_radius()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="11. Stacion\u00e1rn\u00ed veden\u00ed a prostup tepla neomezenou st\u011bnou v\u00e1lcovou,\n"
              "      jednoduchou i slo\u017eenou.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Odvo\u010fte vztahy pro stacion\u00e1rn\u00ed veden\u00ed tepla v\u00e1lcovou st\u011bnou (jednoduchou "
        "a slo\u017eenou). Vyj\u00e1d\u0159ete tepeln\u00e9 odpory, sou\u010dinitel prostupu tepla "
        "a teplotn\u00ed profil. Vysv\u011btlete pojem kritick\u00e9ho polom\u011bru izolace.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 V\u00fdchoz\u00ed p\u0159edpoklady", level=3)
    add_bullet(doc, "Stacion\u00e1rn\u00ed stav, nekone\u010dn\u011b dlouh\u00fd v\u00e1lec (\u2202T/\u2202z = 0)")
    add_bullet(doc, "Radi\u00e1ln\u00ed symetrie (\u2202T/\u2202\u03c6 = 0) \u2014 teplota z\u00e1vis\u00ed pouze na polom\u011bru r")
    add_bullet(doc, "Konstantn\u00ed \u03bb v ka\u017ed\u00e9 vrstv\u011b, \u017e\u00e1dn\u00e9 vnit\u0159n\u00ed zdroje", is_last=True)

    add_heading(doc, "1.2 Veden\u00ed tepla jednoduchou v\u00e1lcovou st\u011bnou", level=3)

    add_info_box(doc,
        "Kl\u00ed\u010dov\u00fd rozd\u00edl oproti rovinn\u00e9 st\u011bn\u011b",
        "U v\u00e1lcov\u00e9 st\u011bny roste plocha, kterou prot\u00e9k\u00e1 teplo, s polom\u011brem (A = 2\u03c0rL). "
        "Proto tepeln\u00fd tok q\u0307 [W/m\u00b2] kles\u00e1 s r (i kdy\u017e Q\u0307 [W] je konstantn\u00ed) "
        "a teplotn\u00ed profil je logaritmick\u00fd, ne line\u00e1rn\u00ed.")

    add_para(doc, "Fourierova rovnice v cylindrick\u00fdch sou\u0159adnic\u00edch (1D, r):", keep_with_next=True)
    add_equation(doc, r"\frac{1}{r}\frac{d}{dr}\left(r\frac{dT}{dr}\right) = 0", label="1")

    add_para(doc, "\u0158e\u0161en\u00ed integrac\u00ed:", keep_with_next=True)
    add_equation(doc, r"T(r) = C_1 \ln r + C_2", label="2")

    add_para(doc, "S okrajov\u00fdmi podm\u00ednkami T(r\u2081) = T\u2081, T(r\u2082) = T\u2082:", keep_with_next=True)
    add_equation(doc, r"T(r) = T_1 + \frac{T_2 - T_1}{\ln(r_2/r_1)} \ln\frac{r}{r_1}", label="3")

    add_para(doc, "Tepeln\u00fd tok:", keep_with_next=True)
    add_equation(doc, r"\dot{Q} = \frac{2\pi \lambda L}{\ln(r_2/r_1)}(T_1 - T_2)", label="4")

    add_para(doc, "Tepeln\u00fd odpor veden\u00ed v\u00e1lcovou st\u011bnou:", keep_with_next=True)
    add_equation(doc, r"R_\lambda = \frac{\ln(r_2/r_1)}{2\pi \lambda L} \quad [\text{K/W}]", label="5")

    add_image(doc, img_cyl, width_cm=14,
              caption="Obr. 1: V\u00e1lcov\u00e1 st\u011bna \u2014 p\u0159\u00ed\u010dn\u00fd \u0159ez a logaritmick\u00fd teplotn\u00ed profil T(r)")

    add_page_break(doc)
    add_heading(doc, "1.3 Prostup tepla jednoduchou v\u00e1lcovou st\u011bnou", level=3)

    add_para(doc, "Celkov\u00fd tepeln\u00fd odpor (konvekce + veden\u00ed + konvekce):", keep_with_next=True)
    add_equation(doc, r"R_{celk} = \frac{1}{\alpha_1 \cdot 2\pi r_1 L} + \frac{\ln(r_2/r_1)}{2\pi \lambda L} + \frac{1}{\alpha_2 \cdot 2\pi r_2 L}", label="6")

    add_para(doc, "Tepeln\u00fd tok prostupu:", keep_with_next=True)
    add_equation(doc, r"\dot{Q} = \frac{T_{f1} - T_{f2}}{R_{celk}}", label="7")

    add_warning_box(doc,
        "U v\u00e1lcov\u00e9 st\u011bny se sou\u010dinitel prostupu tepla k vztahuje bu\u010f na vnit\u0159n\u00ed plochu "
        "(k\u2081, A\u2081 = 2\u03c0r\u2081L) nebo na vn\u011bj\u0161\u00ed plochu (k\u2082, A\u2082 = 2\u03c0r\u2082L). "
        "Mus\u00ed platit k\u2081A\u2081 = k\u2082A\u2082 = Q\u0307/\u0394T. V\u017edy specifikujte, na jakou plochu se k vztahuje!")

    add_para(doc, "Sou\u010dinitel prostupu tepla vztažen\u00fd na vn\u011bj\u0161\u00ed plochu:", keep_with_next=True)
    add_equation(doc, r"\frac{1}{k_2} = \frac{r_2}{\alpha_1 r_1} + \frac{r_2}{\lambda}\ln\frac{r_2}{r_1} + \frac{1}{\alpha_2}", label="8")

    # -- 1.4 Slozena --
    add_page_break(doc)
    add_heading(doc, "1.4 Slo\u017een\u00e1 v\u00e1lcov\u00e1 st\u011bna", level=3)

    add_para(doc, "Pro n vrstev s polom\u011bry r\u2081, r\u2082, ..., r_{n+1}:", keep_with_next=True)
    add_equation(doc, r"R_{celk} = \frac{1}{\alpha_1 \cdot 2\pi r_1 L} + \sum_{i=1}^{n}\frac{\ln(r_{i+1}/r_i)}{2\pi \lambda_i L} + \frac{1}{\alpha_2 \cdot 2\pi r_{n+1} L}", label="9")

    add_image(doc, img_pipe, width_cm=14,
              caption="Obr. 2: Teplotn\u00ed profil izolovan\u00e9ho potrub\u00ed \u2014 logaritmick\u00fd pokles v ka\u017ed\u00e9 vrstv\u011b")

    add_para(doc, "Srovn\u00e1n\u00ed tepeln\u00fdch odpor\u016f \u2014 rovinn\u00e1 vs. v\u00e1lcov\u00e1 st\u011bna:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["Veli\u010dina", "Rovinn\u00e1 st\u011bna", "V\u00e1lcov\u00e1 st\u011bna"],
        data=[
            ["T(x) / T(r)", "Line\u00e1rn\u00ed", "Logaritmick\u00fd"],
            ["R_\u03bb", "\u03b4/(\u03bbA)", "ln(r\u2082/r\u2081)/(2\u03c0\u03bbL)"],
            ["R_\u03b1", "1/(\u03b1A)", "1/(\u03b1\u00b72\u03c0rL)"],
            ["Plocha A", "Konstantn\u00ed", "Roste s r (2\u03c0rL)"],
            ["Kritick\u00fd r_iz", "Neexistuje", "r_kr = \u03bb_iz/\u03b1_e"],
        ],
    )

    # -- 1.5 Kriticky polomer --
    add_page_break(doc)
    add_heading(doc, "1.5 Kritick\u00fd polom\u011br izolace", level=3)

    add_info_box(doc,
        "Kritick\u00fd polom\u011br izolace",
        "P\u0159i p\u0159id\u00e1v\u00e1n\u00ed izolace na v\u00e1lec se zv\u011bt\u0161uje odpor veden\u00ed (R_\u03bb roste), "
        "ale sou\u010dasn\u011b se zv\u011bt\u0161uje vn\u011bj\u0161\u00ed plocha (R_\u03b1 kles\u00e1). "
        "Existuje polom\u011br, p\u0159i kter\u00e9m je celkov\u00fd odpor minim\u00e1ln\u00ed \u2014 kritick\u00fd polom\u011br.")

    add_equation(doc, r"r_{kr} = \frac{\lambda_{iz}}{\alpha_e}", label="10")

    add_para(doc, "D\u016fsledky:", keep_with_next=True)
    add_bullet(doc, "Pokud r\u2082 < r_kr: p\u0159id\u00e1n\u00ed izolace ZV\u00dd\u0160\u00cd tepeln\u00e9 ztr\u00e1ty (paradox!)")
    add_bullet(doc, "Pokud r\u2082 > r_kr: p\u0159id\u00e1n\u00ed izolace SNI\u017dUJE tepeln\u00e9 ztr\u00e1ty (o\u010dek\u00e1van\u00e9)")
    add_bullet(doc, "P\u0159\u00edklad: \u03bb_iz = 0,04 W/(m\u00b7K), \u03b1_e = 10 W/(m\u00b2\u00b7K) \u2192 r_kr = 4 mm", is_last=True)

    add_image(doc, img_rkr, width_cm=13,
              caption="Obr. 3: Z\u00e1vislost celkov\u00e9ho tepeln\u00e9ho odporu na polom\u011bru izolace \u2014 minimum p\u0159i r_kr")

    add_warning_box(doc,
        "V praxi je kritick\u00fd polom\u011br d\u016fle\u017eit\u00fd u tenk\u00fdch trubek a elektrick\u00fdch vodi\u010d\u016f. "
        "U b\u011b\u017en\u00fdch potrub\u00ed (r\u2082 >> r_kr) je efekt zanedbateln\u00fd a izolace v\u017edy pom\u00e1h\u00e1.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Tepeln\u00e9 izolace potrub\u00ed", level=3)
    add_styled_table(doc,
        headers=["Materi\u00e1l", "\u03bb [W/(m\u00b7K)]", "T_max [\u00b0C]", "Pou\u017eit\u00ed"],
        data=[
            ["Miner\u00e1ln\u00ed vlna", "0,035\u20130,045", "700", "Parovody, pr\u016fmysl"],
            ["P\u011bnov\u00e9 sklo", "0,040\u20130,055", "430", "Kryogenn\u00ed, chemie"],
            ["Polystyren (EPS)", "0,030\u20130,040", "80", "TZB, klimatizace"],
            ["Polyuretan (PUR)", "0,020\u20130,030", "120", "P\u0159edizolovan\u00e9 trubky"],
            ["Aerogel", "0,013\u20130,020", "650", "Kosmick\u00e9, speci\u00e1ln\u00ed"],
        ],
    )

    add_heading(doc, "2.2 Normy a po\u017eadavky", level=3)
    add_para(doc,
        "Vyhl\u00e1\u0161ka 193/2007 Sb. a \u010cSN EN ISO 12241 stanov\u00ed minim\u00e1ln\u00ed tlou\u0161\u0165ky "
        "izolac\u00ed pro rozvody tepla. C\u00edlem je omezit tepeln\u00e9 ztr\u00e1ty pod stanovenou mez.")

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Tepeln\u00e1 ztr\u00e1ta izolovan\u00e9ho parovodu", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Ocelov\u00e9 potrub\u00ed (d\u2081 = 50 mm, d\u2082 = 57 mm, \u03bb\u2081 = 50 W/(m\u00b7K)) "
        "je izolovan\u00e9 miner\u00e1ln\u00ed vlnou (tlou\u0161\u0165ka 50 mm, \u03bb\u2082 = 0,04 W/(m\u00b7K)). "
        "Vnit\u0159n\u00ed tekutina: T_{f1} = 200 \u00b0C, \u03b1\u2081 = 500 W/(m\u00b2\u00b7K). "
        "Vn\u011bj\u0161\u00ed vzduch: T_{f2} = 20 \u00b0C, \u03b1\u2082 = 10 W/(m\u00b2\u00b7K). "
        "D\u00e9lka L = 1 m. Ur\u010dete tepelnou ztr\u00e1tu.", bold=True)

    add_para(doc, "Krok 1: Polom\u011bry", bold=True)
    add_equation(doc, r"r_1 = 25 \text{ mm}, \quad r_2 = 28{,}5 \text{ mm}, \quad r_3 = 78{,}5 \text{ mm}")

    add_para(doc, "Krok 2: Tepeln\u00e9 odpory (na 1 m d\u00e9lky)", bold=True)
    add_equation(doc, r"R_{\alpha 1} = \frac{1}{500 \times 2\pi \times 0{,}025 \times 1} = 0{,}0127 \text{ K/W}")
    add_equation(doc, r"R_{\lambda 1} = \frac{\ln(28{,}5/25)}{2\pi \times 50 \times 1} = 0{,}000\,42 \text{ K/W}")
    add_equation(doc, r"R_{\lambda 2} = \frac{\ln(78{,}5/28{,}5)}{2\pi \times 0{,}04 \times 1} = \frac{1{,}013}{0{,}2513} = 4{,}031 \text{ K/W}")
    add_equation(doc, r"R_{\alpha 2} = \frac{1}{10 \times 2\pi \times 0{,}0785 \times 1} = 0{,}2027 \text{ K/W}")

    add_para(doc, "Krok 3: Celkov\u00fd odpor a tepeln\u00e1 ztr\u00e1ta", bold=True)
    add_equation(doc, r"R_{celk} = 0{,}0127 + 0{,}000\,42 + 4{,}031 + 0{,}2027 = 4{,}247 \text{ K/W}")
    add_equation(doc, r"\dot{Q} = \frac{200 - 20}{4{,}247} = \frac{180}{4{,}247} = 42{,}4 \text{ W/m}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Tepeln\u00e1 ztr\u00e1ta: 42,4 W na 1 m potrub\u00ed.\n\n"
        "Dominantn\u00ed odpor: izolace (R\u2082 = 4,031 z 4,247 = 95 %). "
        "Ocelov\u00e1 st\u011bna trubky je prakticky \u201epr\u016fhledn\u00e1\u201c pro teplo (R\u2081 = 0,01 %).\n"
        "Bez izolace by ztr\u00e1ta byla ~1020 W/m \u2014 izolace sn\u00ed\u017eila ztr\u00e1ty 24\u00d7.")

    # ==================================================================
    # CAST 4: ZKOUZKOVE OTAZKY
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d je teplotn\u00ed profil ve v\u00e1lcov\u00e9 st\u011bn\u011b logaritmick\u00fd, nikoliv line\u00e1rn\u00ed?",
         "Proto\u017ee plocha, kterou prot\u00e9k\u00e1 teplo, roste s polom\u011brem (A = 2\u03c0rL). "
         "Konstantn\u00ed Q\u0307 p\u0159i rostouc\u00ed plo\u0161e znamen\u00e1, \u017ee hustota toku q\u0307 kles\u00e1 s r "
         "a teplotn\u00ed gradient dT/dr mus\u00ed tak\u00e9 klesat \u2014 v\u00fdsledkem je logaritmick\u00fd pr\u016fb\u011bh."),

        ("Vysv\u011btlete paradox kritick\u00e9ho polom\u011bru izolace.",
         "P\u0159id\u00e1n\u00edm izolace roste odpor veden\u00ed, ale sou\u010dasn\u011b roste vn\u011bj\u0161\u00ed plocha "
         "a kles\u00e1 odpor konvekce. Do r_kr = \u03bb_iz/\u03b1_e p\u0159ev\u00e1\u017e\u00ed pokles R_\u03b1 a celkov\u00fd "
         "odpor kles\u00e1 \u2014 tepeln\u00e9 ztr\u00e1ty rostou. Nad r_kr u\u017e p\u0159ev\u00e1\u017e\u00ed r\u016fst R_\u03bb."),

        ("Pro\u010d se u v\u00e1lcov\u00e9 st\u011bny mus\u00ed specifikovat, na jakou plochu se k vztahuje?",
         "Proto\u017ee vnit\u0159n\u00ed a vn\u011bj\u0161\u00ed plocha v\u00e1lce jsou r\u016fzn\u00e9 (A\u2081 = 2\u03c0r\u2081L \u2260 A\u2082 = 2\u03c0r\u2082L). "
         "Hodnota k z\u00e1vis\u00ed na referen\u010dn\u00ed plo\u0161e: k\u2081A\u2081 = k\u2082A\u2082. "
         "U rovinn\u00e9 st\u011bny tento probl\u00e9m nevznik\u00e1, proto\u017ee A = konst."),

        ("Jak\u00fd v\u00fdznam m\u00e1 ocelov\u00e1 st\u011bna trubky v celkov\u00e9m tepeln\u00e9m odporu?",
         "Prakticky \u017e\u00e1dn\u00fd \u2014 ocel m\u00e1 \u03bb \u2248 50 W/(m\u00b7K) a mal\u00fd ln(r\u2082/r\u2081), tak\u017ee R_\u03bb "
         "je \u0159\u00e1dov\u011b 10\u207b\u2074 K/W. Dominuje izolace (R ~ jednotky K/W) "
         "a vn\u011bj\u0161\u00ed konvekce (R ~ 0,1\u20130,2 K/W)."),

        ("Kdy je v\u00fdhodn\u011bj\u0161\u00ed pou\u017e\u00edt v\u00fdpo\u010det pro v\u00e1lcovou vs. rovinnou st\u011bnu?",
         "V\u00e1lcovou geometrii pou\u017e\u00edjeme u trubek, potrub\u00ed a v\u00e1lcov\u00fdch n\u00e1dob. "
         "Pokud je r\u2082/r\u2081 < 1,1 (tenk\u00e1 st\u011bna), lze aproximovat rovinnou geometri\u00ed "
         "s chybou < 5 %. P\u0159i r\u2082/r\u2081 > 1,5 je v\u00e1lcov\u00fd v\u00fdpo\u010det nutn\u00fd."),

        ("Jak se li\u0161\u00ed tepeln\u00e1 izolace parovod\u016f v zimním a letn\u00edm provozu?",
         "Funkce izolace je v obou p\u0159\u00edpadech stejn\u00e1 \u2014 sn\u00ed\u017een\u00ed tepeln\u00fdch ztr\u00e1t. "
         "V l\u00e9t\u011b je \u0394T men\u0161\u00ed (okoln\u00ed vzduch je teplej\u0161\u00ed), tak\u017ee ztr\u00e1ty jsou ni\u017e\u0161\u00ed. "
         "Dimenzov\u00e1n\u00ed izolace se prov\u00e1d\u00ed pro zimn\u00ed podm\u00ednky (nejvy\u0161\u0161\u00ed \u0394T)."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Incropera, F.P. et al.: Fundamentals of Heat and Mass Transfer, 8th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cSN EN ISO 12241 \u2014 Tepeln\u00e9 izolace pro za\u0159\u00edzen\u00ed budov")
    add_bullet(doc, "Kozub\u00edk, T.: P\u0159enos tepla, VUT Brno")
    add_bullet(doc, "VDI Heat Atlas \u2014 v\u00e1lcov\u00e9 geometrie, kritick\u00fd polom\u011br", is_last=True)

    save_and_export(doc, "11-vedeni-tepla-valec")


if __name__ == "__main__":
    generate()
