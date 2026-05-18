"""
Státnicová otázka 7: Páry, základní pojmy. Jednoduchý ideální parní cyklus, schéma, T-s diagram.
Zvyšování účinnosti cyklu přihříváním páry a regenerativním ohřevem napájecí vody.
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


# ═════════════════════════════════════════════════════════════════════════════
# GRAFY
# ═════════════════════════════════════════════════════════════════════════════

def generate_pv_diagram_water():
    """Generate p-v diagram of water with phase regions."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    # Simplified saturation curve for water (schematic)
    # Critical point: Tc=647.1 K, pc=22.06 MPa, vc=0.003155 m³/kg
    T_sat = np.linspace(373.15, 647.1, 200)

    # Approximate saturated liquid and vapor specific volumes
    v_f = 0.001 * np.exp(0.0015 * (T_sat - 373.15))
    v_g = 1.673 * np.exp(-0.012 * (T_sat - 373.15))

    # Convert to pressure via Clausius-Clapeyron approximation
    p_sat = 101325 * np.exp(13.7 * (1 - 373.15 / T_sat))

    ax.plot(v_f * 1e3, p_sat / 1e6, color=COLORS[0], linewidth=2.5, label="Mezní křivka kapaliny (x=0)")
    ax.plot(v_g * 1e3, p_sat / 1e6, color=COLORS[1], linewidth=2.5, label="Mezní křivka sytosti (x=1)")

    # Critical point
    ax.plot(3.155, 22.06, "ko", markersize=12, zorder=5)
    ax.annotate("Kritický bod K\n(374,15 °C; 22,06 MPa)",
                xy=(3.155, 22.06), xytext=(15, 18),
                fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    # Region labels
    ax.text(0.3, 10, "Kapalina\n(pod-\nchlazená)", fontsize=10, ha="center",
            style="italic", color=COLORS[0])
    ax.text(5, 8, "Mokrá pára\n(dvoufázová\noblast)", fontsize=10, ha="center",
            style="italic", color="#7C3AED")
    ax.text(60, 5, "Přehřátá\npára", fontsize=10, ha="center",
            style="italic", color=COLORS[1])

    # Isobars
    for p_val, t_label in [(0.1, "0,1 MPa"), (1.0, "1 MPa"), (10.0, "10 MPa")]:
        ax.axhline(y=p_val, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
        ax.text(100, p_val * 1.05, t_label, fontsize=7, color="gray")

    ax.set_xlabel("Měrný objem v [dm³/kg]", fontsize=11)
    ax.set_ylabel("Tlak p [MPa]", fontsize=11)
    ax.set_title("p-v diagram vody — fázové oblasti", fontsize=12, fontweight="bold")
    ax.set_xscale("log")
    ax.set_xlim(0.1, 200)
    ax.set_ylim(0, 25)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q07_pv_water.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_ts_diagram_water():
    """Generate T-s diagram of water with saturation dome and Rankine cycle."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Schematic saturation dome
    s_f = np.array([0.0, 0.3, 0.65, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0, 3.36])
    T_f = np.array([273, 300, 330, 360, 380, 400, 420, 440, 460, 474])

    s_g = np.array([3.36, 3.8, 4.5, 5.5, 6.0, 6.5, 7.0, 7.36, 7.5, 8.0, 8.5, 9.0])
    T_g = np.array([474, 460, 440, 400, 380, 360, 340, 320, 310, 290, 275, 260])

    # Shift to realistic kJ/(kg·K) scale
    ax.plot(s_f, T_f - 273.15, color=COLORS[0], linewidth=2.5, label="Mezní křivka kapaliny")
    ax.plot(s_g, T_g - 273.15, color=COLORS[1], linewidth=2.5, label="Mezní křivka syté páry")

    # Critical point
    ax.plot(3.36, 374.15 - 273.15 + 100, "ko", markersize=10, zorder=5)
    ax.annotate("Kritický\nbod K", xy=(3.36, 201), xytext=(4.0, 220),
                fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    # Simple Rankine cycle (schematic)
    # Points: 1(after condenser, sat liquid) → 2(after pump) → 3(after boiler, sat/superheat) → 4(after turbine)
    # State 1: condenser exit, ~40°C, s≈0.57
    # State 2: pump exit, ~41°C, s≈0.57 (isentropic pump)
    # State 3: boiler exit, superheat 400°C, s≈6.8
    # State 4: turbine exit, ~40°C, s≈6.8 (isentropic), in wet region

    s1, T1 = 0.57, 40
    s2, T2 = 0.57, 42  # Nearly same (pump work is tiny)
    s3, T3 = 6.8, 400
    s4, T4 = 6.8, 40

    # Draw cycle
    # 1→2 (pump, nearly vertical line up — but ΔT is tiny, show as dot)
    ax.plot([s1, s2], [T1, T2], color="#7C3AED", linewidth=3, zorder=4)
    # 2→3 (boiler: heating, vaporization, superheating)
    s_boiler = [s2, 0.57, 1.3, 2.0, 3.36, 4.5, 5.5, 6.0, 6.5, s3]
    T_boiler = [T2, 100, 100, 100, 100, 100, 100, 100, 200, T3]
    # More realistic: isobar in boiler
    s_boiler = np.array([s2, 1.3, 1.3, 6.8, s3])
    T_boiler = np.array([T2, 100, 180, 180, T3])
    # Simplify: just show the path as a curve along the isobar
    s_b = np.array([s2, 0.8, 1.3, 2.5, 6.5, s3])
    T_b = np.array([T2, 80, 180, 180, 180, T3])
    ax.plot(s_b, T_b, color="#7C3AED", linewidth=3, zorder=4)
    # 3→4 (turbine, isentropic expansion — vertical line down)
    ax.plot([s3, s4], [T3, T4], color="#7C3AED", linewidth=3, zorder=4)
    # 4→1 (condenser, isobar/isotherm — horizontal line left)
    ax.plot([s4, s1], [T4, T1], color="#7C3AED", linewidth=3, zorder=4)

    # Label points
    offset = 8
    ax.plot(s1, T1, "o", color="#7C3AED", markersize=10, zorder=5)
    ax.annotate("1", xy=(s1, T1), xytext=(s1 - 0.4, T1 + offset), fontsize=12, fontweight="bold", color="#7C3AED")
    ax.plot(s2, T2, "o", color="#7C3AED", markersize=10, zorder=5)
    ax.annotate("2", xy=(s2, T2), xytext=(s2 - 0.4, T2 + 15), fontsize=12, fontweight="bold", color="#7C3AED")
    ax.plot(s3, T3, "o", color="#7C3AED", markersize=10, zorder=5)
    ax.annotate("3", xy=(s3, T3), xytext=(s3 + 0.2, T3 + offset), fontsize=12, fontweight="bold", color="#7C3AED")
    ax.plot(s4, T4, "o", color="#7C3AED", markersize=10, zorder=5)
    ax.annotate("4", xy=(s4, T4), xytext=(s4 + 0.2, T4 + offset), fontsize=12, fontweight="bold", color="#7C3AED")

    # Process labels
    ax.annotate("Čerpadlo\n1→2", xy=(0.2, 80), fontsize=8, color="#555", ha="center")
    ax.annotate("Kotel (izobarický ohřev)\n2→3", xy=(3.5, 320), fontsize=8, color="#555", ha="center")
    ax.annotate("Turbína\n(izoentropická\nexpanze)\n3→4", xy=(7.5, 220), fontsize=8, color="#555", ha="center")
    ax.annotate("Kondenzátor\n(izobarické chlazení)\n4→1", xy=(3.5, 15), fontsize=8, color="#555", ha="center")

    # Fill cycle area (represents net work)
    s_fill = np.concatenate([[s1], s_b, [s4, s1]])
    T_fill = np.concatenate([[T1], T_b, [T4, T1]])
    ax.fill(s_fill, T_fill, alpha=0.08, color="#7C3AED")

    ax.set_xlabel("Měrná entropie s [kJ/(kg·K)]", fontsize=11)
    ax.set_ylabel("Teplota T [°C]", fontsize=11)
    ax.set_title("T-s diagram: Rankineův cyklus (ideální) s přehřátou parou", fontsize=12, fontweight="bold")
    ax.set_xlim(-0.5, 10)
    ax.set_ylim(-10, 450)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q07_ts_rankine.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_rankine_schema():
    """Generate schematic of simple Rankine cycle components."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-1, 13)
    ax.set_ylim(-1, 7)
    ax.set_aspect("equal")
    ax.axis("off")

    # Kotel
    kotel = FancyBboxPatch((0.5, 4), 3, 2, boxstyle="round,pad=0.2",
                            facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2)
    ax.add_patch(kotel)
    ax.text(2, 5, "KOTEL", ha="center", va="center", fontsize=12, fontweight="bold", color="#DC2626")
    ax.text(2, 4.4, "(parogenerátor)", ha="center", va="center", fontsize=8, color="#991B1B")

    # Turbína
    turb = FancyBboxPatch((5.5, 4), 3, 2, boxstyle="round,pad=0.2",
                           facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=2)
    ax.add_patch(turb)
    ax.text(7, 5, "TURBÍNA", ha="center", va="center", fontsize=12, fontweight="bold", color="#16A34A")
    ax.text(7, 4.4, "(W_T > 0)", ha="center", va="center", fontsize=8, color="#166534")

    # Kondenzátor
    kond = FancyBboxPatch((5.5, 0.5), 3, 2, boxstyle="round,pad=0.2",
                           facecolor="#DBEAFE", edgecolor="#2563EB", linewidth=2)
    ax.add_patch(kond)
    ax.text(7, 1.5, "KONDENZÁTOR", ha="center", va="center", fontsize=12, fontweight="bold", color="#2563EB")
    ax.text(7, 0.9, "(Q_out)", ha="center", va="center", fontsize=8, color="#1E40AF")

    # Čerpadlo
    cerp = FancyBboxPatch((0.5, 0.5), 3, 2, boxstyle="round,pad=0.2",
                           facecolor="#FEF3C7", edgecolor="#D97706", linewidth=2)
    ax.add_patch(cerp)
    ax.text(2, 1.5, "ČERPADLO", ha="center", va="center", fontsize=12, fontweight="bold", color="#D97706")
    ax.text(2, 0.9, "(W_P < 0)", ha="center", va="center", fontsize=8, color="#92400E")

    # Arrows: Kotel → Turbína (top)
    ax.annotate("", xy=(5.5, 5), xytext=(3.5, 5),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=3))
    ax.text(4.5, 5.5, "3: přehřátá pára\np₃, T₃", ha="center", fontsize=8, color="#555")

    # Turbína → Kondenzátor (right)
    ax.annotate("", xy=(7, 2.5), xytext=(7, 4),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=3))
    ax.text(8.8, 3.3, "4: mokrá pára\np₄, x₄", ha="center", fontsize=8, color="#555")

    # Kondenzátor → Čerpadlo (bottom)
    ax.annotate("", xy=(3.5, 1.5), xytext=(5.5, 1.5),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=3))
    ax.text(4.5, 0.2, "1: sytá kapalina\np₁, x=0", ha="center", fontsize=8, color="#555")

    # Čerpadlo → Kotel (left)
    ax.annotate("", xy=(2, 4), xytext=(2, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=3))
    ax.text(-0.2, 3.3, "2: podchlazen. kap.\np₂ ≈ p₃", ha="center", fontsize=8, color="#555")

    # Heat input/output arrows
    ax.annotate("Q_in", xy=(2, 6.3), fontsize=11, fontweight="bold", color="#DC2626", ha="center")
    ax.annotate("", xy=(2, 6.1), xytext=(2, 6.8),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=2))

    # Generator symbol
    ax.annotate("W_net", xy=(10.5, 5), fontsize=11, fontweight="bold", color="#16A34A", ha="center")
    ax.annotate("", xy=(10.5, 5), xytext=(8.5, 5),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=2))

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q07_rankine_schema.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_reheat_ts():
    """Generate T-s diagram comparing simple Rankine vs reheat cycle."""
    fig, ax = plt.subplots(figsize=(8, 6))

    # Saturation dome (simplified)
    s_f = np.array([0.0, 0.3, 0.65, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0, 3.36])
    T_f = np.array([0, 27, 57, 87, 107, 127, 147, 167, 187, 201])
    s_g = np.array([3.36, 3.8, 4.5, 5.5, 6.0, 6.5, 7.0, 7.36, 7.5, 8.0, 8.5, 9.0])
    T_g = np.array([201, 187, 167, 127, 107, 87, 67, 47, 37, 17, 2, -13])

    ax.plot(s_f, T_f, color="gray", linewidth=2, alpha=0.5)
    ax.plot(s_g, T_g, color="gray", linewidth=2, alpha=0.5)
    ax.fill_betweenx(np.linspace(-13, 201, 100),
                     np.interp(np.linspace(-13, 201, 100), T_f, s_f),
                     np.interp(np.linspace(-13, 201, 100), T_g[::-1], s_g[::-1]),
                     alpha=0.03, color="gray")

    # Simple Rankine (lighter)
    s_simple = [0.57, 0.8, 1.3, 2.5, 6.5, 6.8, 6.8, 0.57]
    T_simple = [40, 80, 180, 180, 180, 400, 40, 40]
    ax.plot(s_simple, T_simple, color=COLORS[0], linewidth=2, linestyle="--", alpha=0.6,
            label="Jednoduchý Rankine")

    # Reheat cycle
    # 1→2: pump
    # 2→3: boiler to HP superheat (10 MPa, 500°C)
    # 3→4: HP turbine expansion (to ~1 MPa, ~200°C)
    # 4→5: reheat in boiler (1 MPa, back to 500°C)
    # 5→6: LP turbine expansion (to condenser, ~40°C)
    # 6→1: condenser
    s_rh = [0.57, 0.8, 1.3, 2.5, 6.2, 6.6, 6.6, 5.0, 5.0, 7.5, 7.5, 0.57]
    T_rh = [40, 80, 180, 180, 180, 500, 200, 200, 500, 500, 40, 40]
    ax.plot(s_rh, T_rh, color=COLORS[1], linewidth=2.5,
            label="Rankine s přihříváním")

    # Labels
    ax.annotate("HP\nturbína", xy=(6.5, 350), fontsize=8, color=COLORS[1], ha="center")
    ax.annotate("Přihřívání\n4→5", xy=(5.0, 370), fontsize=8, color=COLORS[1], ha="center",
                fontweight="bold")
    ax.annotate("LP\nturbína", xy=(7.2, 270), fontsize=8, color=COLORS[1], ha="center")

    ax.set_xlabel("Měrná entropie s [kJ/(kg·K)]", fontsize=11)
    ax.set_ylabel("Teplota T [°C]", fontsize=11)
    ax.set_title("T-s diagram: Srovnání jednoduchého Rankineova cyklu a cyklu s přihříváním",
                 fontsize=11, fontweight="bold")
    ax.set_xlim(-0.5, 10)
    ax.set_ylim(-20, 550)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q07_reheat_ts.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_regenerative_schema():
    """Generate schematic of regenerative Rankine cycle with open feedwater heater."""
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1, 8)
    ax.set_aspect("equal")
    ax.axis("off")

    # Components
    components = [
        ("KOTEL", 1, 5.5, 2.5, 1.8, "#FEE2E2", "#DC2626"),
        ("TURBÍNA\n(HP)", 5, 5.5, 2, 1.8, "#DCFCE7", "#16A34A"),
        ("TURBÍNA\n(LP)", 8.5, 5.5, 2, 1.8, "#DCFCE7", "#16A34A"),
        ("KONDENZÁTOR", 8.5, 0.5, 2.5, 1.8, "#DBEAFE", "#2563EB"),
        ("ODPLYŇOVÁK\n(OFW heater)", 4, 0.5, 3, 1.8, "#F3E8FF", "#7C3AED"),
        ("ČERP. 1", 12, 0.5, 1.5, 1.8, "#FEF3C7", "#D97706"),
        ("ČERP. 2", 1, 0.5, 1.5, 1.8, "#FEF3C7", "#D97706"),
    ]

    for label, x, y, w, h, fc, ec in components:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                              facecolor=fc, edgecolor=ec, linewidth=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, label, ha="center", va="center",
                fontsize=9, fontweight="bold", color=ec)

    # Arrows (simplified flow)
    arrows = [
        (3.5, 6.4, 5, 6.4, "#DC2626"),      # Kotel → HP turbína
        (7, 6.4, 8.5, 6.4, "#16A34A"),       # HP → LP turbína
        (9.75, 5.5, 9.75, 2.3, "#16A34A"),   # LP turbína → Kondenzátor
        (9.75, 0.5, 9.75, -0.3, "#2563EB"),  # ... not needed, use horizontal
        (11, 1.4, 12, 1.4, "#2563EB"),       # Kondenzátor → Čerpadlo 1
        (6.5, 5.5, 5.5, 2.3, "#7C3AED"),     # HP turbine bleed → OFW heater
        (4, 1.4, 2.5, 1.4, "#7C3AED"),       # OFW → Čerpadlo 2
        (1.75, 2.3, 1.75, 5.5, "#D97706"),   # Čerpadlo 2 → Kotel
    ]

    for x1, y1, x2, y2, color in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.5))

    # Bleed steam label
    ax.text(5.3, 4.0, "Odběr páry\n(bleeding)\ny·ṁ", ha="center", fontsize=8,
            color="#7C3AED", fontweight="bold")

    # Main flow label
    ax.text(13.5, 1.4, "ṁ", fontsize=10, fontweight="bold", color="#555")

    fig.suptitle("Schéma regenerativního Rankineova cyklu s otevřeným ohřívákem napájecí vody",
                 fontsize=11, fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q07_regenerative_schema.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_efficiency_comparison():
    """Bar chart comparing thermal efficiencies of different cycle modifications."""
    fig, ax = plt.subplots(figsize=(8, 4.5))

    cycles = [
        "Jednoduchý Rankine\n(bez přehřátí)",
        "Rankine\ns přehřátím",
        "Rankine\ns přihříváním",
        "Rankine\nregenerativní",
        "Kombinovaný\n(přihřívání +\nregenerace)",
    ]
    efficiencies = [30, 36, 40, 42, 46]
    colors_bar = [COLORS[0], COLORS[3], COLORS[1], COLORS[2], "#7C3AED"]

    bars = ax.bar(cycles, efficiencies, color=colors_bar, edgecolor="white", width=0.65)

    for bar, eff in zip(bars, efficiencies):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f"{eff} %", ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.axhline(y=100 * (1 - (40 + 273.15)/(540 + 273.15)), color="gray", linestyle=":",
               linewidth=1.5, alpha=0.7)
    eta_carnot = 100 * (1 - (40 + 273.15)/(540 + 273.15))
    ax.text(4.6, eta_carnot + 1, f"Carnot (η = {eta_carnot:.0f} %)", fontsize=8, color="gray")

    ax.set_ylabel("Termická účinnost η_t [%]", fontsize=11)
    ax.set_title("Srovnání termických účinností parních cyklů\n(typické hodnoty pro moderní elektrárny)",
                 fontsize=11, fontweight="bold")
    ax.set_ylim(0, 70)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q07_efficiency_comparison.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ═════════════════════════════════════════════════════════════════════════════
# OBSAH DOKUMENTU
# ═════════════════════════════════════════════════════════════════════════════

def generate():
    print("Generuji diagramy...")
    img_pv = generate_pv_diagram_water()
    img_ts = generate_ts_diagram_water()
    img_schema = generate_rankine_schema()
    img_reheat = generate_reheat_ts()
    img_regen = generate_regenerative_schema()
    img_eff = generate_efficiency_comparison()
    print("Diagramy hotové. Generuji .docx...")

    doc = create_document(
        title="7. Páry, základní pojmy. Jednoduchý ideální parní cyklus, schéma, T-s diagram.\n"
              "    Zvyšování účinnosti cyklu přihříváním páry a regenerativním ohřevem napájecí vody.",
        okruh="Termomechanika a spalování",
    )

    # ── ZADÁNÍ ──
    add_heading(doc, "Zadání", level=2)
    add_para(doc,
        "Vysvětlete základní pojmy z oblasti par (sytá kapalina, mokrá pára, přehřátá pára, "
        "suchost). Popište jednoduchý ideální parní cyklus (Rankineův), jeho schéma a T-s diagram. "
        "Vysvětlete principy zvyšování účinnosti cyklu přihříváním páry a regenerativním "
        "ohřevem napájecí vody.")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 1: TEORETICKÝ ROZBOR
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 1: Teoretický rozbor", level=2)

    # ── 1.1 Základní pojmy ──
    add_heading(doc, "1.1 Páry — základní pojmy a fázové přeměny", level=3)

    add_info_box(doc,
        "Definice: Pára",
        "Pára je plyn, který se nachází v blízkosti svého stavu nasycení — tj. blízko podmínek, "
        "při nichž dochází ke kondenzaci. Na rozdíl od ideálního plynu nelze chování páry popsat "
        "jednoduchou stavovou rovnicí pv = rT; je nutné používat parní tabulky nebo software (CoolProp, REFPROP).")

    add_para(doc, "Klíčové pojmy fázových přeměn:", bold=True, keep_with_next=True)

    add_bullet(doc, "Sytá (vařící) kapalina — kapalina na mezi varu při daném tlaku; "
               "jakékoliv dodání tepla způsobí var (značíme čárkou: h', s', v')")
    add_bullet(doc, "Sytá (suchá) pára — pára na mezi kondenzace při daném tlaku; "
               "jakékoliv odebrání tepla způsobí kondenzaci (značíme dvěma čárkami: h'', s'', v'')")
    add_bullet(doc, "Mokrá pára — dvoufázová směs kapaliny a páry; "
               "stav popsán suchostí x")
    add_bullet(doc, "Přehřátá pára — pára ohřátá nad teplotu sytosti při daném tlaku; "
               "jednofázový stav")
    add_bullet(doc, "Podchlazená kapalina — kapalina ochlazená pod teplotu sytosti; "
               "jednofázový stav", is_last=True)

    add_info_box(doc,
        "Suchost (kvalita páry) x",
        "Hmotnostní podíl suché syté páry ve směsi mokré páry:\n"
        "x = m_pára / (m_kapalina + m_pára)\n"
        "x = 0 → sytá kapalina | x = 1 → sytá pára | 0 < x < 1 → mokrá pára")

    add_para(doc, "Vlastnosti mokré páry se určují lineární interpolací:", keep_with_next=True)
    add_equation(doc, r"h = h' + x \cdot (h'' - h') = h' + x \cdot l", label="1")
    add_equation(doc, r"s = s' + x \cdot (s'' - s')", label="2")
    add_equation(doc, r"v = v' + x \cdot (v'' - v')", label="3")

    add_para(doc, "kde l = h'' − h' je měrné výparné (skupenské) teplo [kJ/kg].")

    # p-v diagram
    add_image(doc, img_pv, width_cm=14,
              caption="Obr. 1: p-v diagram vody — fázové oblasti a mezní křivky")

    # ── 1.2 Kritický bod ──
    add_page_break(doc)
    add_heading(doc, "1.2 Kritický bod a Triplex bod", level=3)

    add_info_box(doc,
        "Kritický bod",
        "Stav, při kterém se sytá kapalina a sytá pára stávají nerozlišitelnými. "
        "Nad kritickým bodem existuje pouze nadkritická tekutina — nelze definovat fázový přechod.\n"
        "Voda: T_k = 374,15 °C, p_k = 22,064 MPa, v_k = 0,003155 m³/kg")

    add_para(doc, "Vlastnosti kritického bodu:", keep_with_next=True)
    add_bullet(doc, "Výparné teplo l → 0 (kapalina a pára splývají)")
    add_bullet(doc, "Měrné objemy v' a v'' se vyrovnávají")
    add_bullet(doc, "Mezní křivky kapaliny a páry se stýkají")
    add_bullet(doc, "Nad kritickým tlakem nelze rozlišit var a kondenzaci", is_last=True)

    add_para(doc, "Trojný bod (triplex bod) vody: T_tr = 0,01 °C, p_tr = 611,73 Pa — "
             "jediný stav, kde koexistují všechny tři fáze (led, kapalina, pára) v rovnováze.")

    add_styled_table(doc,
        headers=["Veličina", "Trojný bod", "Kritický bod"],
        data=[
            ["Teplota", "0,01 °C (273,16 K)", "374,15 °C (647,3 K)"],
            ["Tlak", "611,73 Pa (0,006 bar)", "22,064 MPa (220,64 bar)"],
            ["Měrný objem v'", "0,001000 m³/kg", "0,003155 m³/kg"],
            ["Měrný objem v''", "206,1 m³/kg", "0,003155 m³/kg"],
            ["Výparné teplo l", "2501 kJ/kg", "0 kJ/kg"],
        ],
    )

    # ── 1.3 Rankineův cyklus ──
    add_page_break(doc)
    add_heading(doc, "1.3 Jednoduchý ideální Rankineův cyklus", level=3)

    add_info_box(doc,
        "Rankineův cyklus",
        "Základní termodynamický oběh parních elektráren. Pracovní látkou je voda/pára. "
        "Skládá se ze čtyř ideálních dějů: izoentropická komprese (čerpadlo), "
        "izobarický ohřev (kotel), izoentropická expanze (turbína), izobarické chlazení (kondenzátor).")

    add_para(doc, "Schéma cyklu:", bold=True, keep_with_next=True)
    add_image(doc, img_schema, width_cm=14,
              caption="Obr. 2: Schéma jednoduchého Rankineova cyklu — čtyři základní komponenty")

    add_page_break(doc)
    add_para(doc, "Děje v Rankineově cyklu:", bold=True, keep_with_next=True)

    add_styled_table(doc,
        headers=["Děj", "Úsek", "Komponenta", "Popis"],
        data=[
            ["1→2", "Izoentropická komprese", "Čerpadlo", "s₁ = s₂, zvýšení tlaku kapaliny"],
            ["2→3", "Izobarický ohřev", "Kotel", "p₂ = p₃, ohřev + var + přehřátí"],
            ["3→4", "Izoentropická expanze", "Turbína", "s₃ = s₄, expanze páry → práce"],
            ["4→1", "Izobarické chlazení", "Kondenzátor", "p₄ = p₁, kondenzace páry"],
        ],
    )

    add_para(doc, "T-s diagram Rankineova cyklu:", bold=True, keep_with_next=True)
    add_image(doc, img_ts, width_cm=14,
              caption="Obr. 3: T-s diagram ideálního Rankineova cyklu s přehřátou parou")

    # ── 1.4 Energetická bilance ──
    add_page_break(doc)
    add_heading(doc, "1.4 Energetická bilance Rankineova cyklu", level=3)

    add_para(doc, "Přivedené teplo v kotli (izobarický ohřev):", keep_with_next=True)
    add_equation(doc, r"q_{in} = h_3 - h_2", label="4")

    add_para(doc, "Odvedené teplo v kondenzátoru:", keep_with_next=True)
    add_equation(doc, r"q_{out} = h_4 - h_1", label="5")

    add_para(doc, "Měrná práce turbíny:", keep_with_next=True)
    add_equation(doc, r"w_T = h_3 - h_4", label="6")

    add_para(doc, "Měrná práce čerpadla:", keep_with_next=True)
    add_equation(doc, r"w_P = h_2 - h_1 \approx v_1 (p_2 - p_1)", label="7")

    add_para(doc,
        "Aproximace v rovnici (7) platí pro nestlačitelnou kapalinu — "
        "čerpadlová práce je výrazně menší než práce turbíny (typicky 1–3 % w_T).")

    add_para(doc, "Čistá práce cyklu:", keep_with_next=True)
    add_equation(doc, r"w_{net} = w_T - w_P = (h_3 - h_4) - (h_2 - h_1)", label="8")

    add_para(doc, "Termická účinnost cyklu:", keep_with_next=True)
    add_equation(doc, r"\eta_t = \frac{w_{net}}{q_{in}} = 1 - \frac{q_{out}}{q_{in}} = 1 - \frac{h_4 - h_1}{h_3 - h_2}", label="9")

    add_warning_box(doc,
        "Termická účinnost Rankineova cyklu je vždy nižší než účinnost Carnotova cyklu "
        "pracujícího mezi stejnými teplotami, protože přívod tepla v kotli není izotermický "
        "(ohřev kapaliny + var + přehřátí probíhá při různých teplotách).")

    # ── 1.5 Přehřátí páry ──
    add_page_break(doc)
    add_heading(doc, "1.5 Zvyšování účinnosti — přehřátí páry", level=3)

    add_para(doc,
        "Přehřátí páry nad teplotu sytosti zvyšuje střední teplotu přívodu tepla, "
        "a tím zvyšuje termickou účinnost cyklu (přibližuje se Carnotovu cyklu).")

    add_para(doc, "Výhody přehřátí:", keep_with_next=True)
    add_bullet(doc, "Zvýšení termické účinnosti o 3–5 procentních bodů")
    add_bullet(doc, "Zvýšení suchosti páry na výstupu z turbíny (méně eroze lopatek)")
    add_bullet(doc, "Zvýšení měrné práce turbíny (větší výkon při stejném průtoku)", is_last=True)

    add_warning_box(doc,
        "Teplota přehřátí je omezena žárupevností materiálů. Moderní elektrárny: "
        "T₃ = 540–620 °C (austenitické oceli), experimentálně až 700 °C (niklové slitiny).")

    # ── 1.6 Přihřívání ──
    add_heading(doc, "1.6 Zvyšování účinnosti — přihřívání páry (reheat)", level=3)

    add_info_box(doc,
        "Princip přihřívání",
        "Pára se po částečné expanzi v HP turbíně vrací do kotle, kde se znovu ohřeje "
        "na vysokou teplotu. Poté expanduje v LP turbíně. Přihřívání zvyšuje střední teplotu "
        "přívodu tepla a zároveň zabraňuje nadměrné vlhkosti na výstupu LP turbíny.")

    add_para(doc, "Modifikace energetické bilance:", keep_with_next=True)
    add_equation(doc, r"q_{in} = (h_3 - h_2) + (h_5 - h_4)", label="10")
    add_equation(doc, r"w_{net} = (h_3 - h_4) + (h_5 - h_6) - w_P", label="11")
    add_equation(doc, r"\eta_t = \frac{w_{net}}{q_{in}}", label="12")

    add_image(doc, img_reheat, width_cm=14,
              caption="Obr. 4: T-s diagram — srovnání jednoduchého Rankineova cyklu a cyklu s přihříváním páry")

    # ── 1.7 Regenerace ──
    add_page_break(doc)
    add_heading(doc, "1.7 Zvyšování účinnosti — regenerativní ohřev napájecí vody", level=3)

    add_info_box(doc,
        "Princip regenerace",
        "Část páry se odebírá (bleeding) z turbíny v průběhu expanze a používá se k předehřevu "
        "napájecí vody v ohříváku. Tím se zvyšuje střední teplota přívodu tepla (teplo se přivádí "
        "při vyšší teplotě) a účinnost cyklu roste.")

    add_para(doc, "Typy ohříváků napájecí vody:", keep_with_next=True)
    add_bullet(doc, "Otevřený (směšovací, odplyňovák) — pára se mísí přímo s napájecí vodou; "
               "jednodušší, levnější, zároveň odplyňuje")
    add_bullet(doc, "Uzavřený (povrchový) — teplo se předává přes teplosměnnou plochu; "
               "pára a voda se nemísí, složitější zapojení", is_last=True)

    add_image(doc, img_regen, width_cm=14,
              caption="Obr. 5: Schéma regenerativního Rankineova cyklu s otevřeným ohřívákem napájecí vody (odplyňovákem)")

    add_para(doc, "Bilance otevřeného ohříváku:", keep_with_next=True)
    add_equation(doc, r"y \cdot h_{odb} + (1 - y) \cdot h_{kond} = 1 \cdot h_{out}", label="13")

    add_para(doc,
        "kde y je podíl odběrového hmotnostního průtoku z celkového průtoku turbínou. "
        "Optimální počet regenerativních ohřevů v reálných elektrárnách: 5–8 (závisí na výkonu).")

    add_para(doc, "Vliv regenerace na účinnost:", keep_with_next=True)
    add_bullet(doc, "Každý regenerativní ohřev zvyšuje η_t o 1–2 procentní body")
    add_bullet(doc, "Nad ~8 stupňů se přínos zmenšuje (zákon klesajících výnosů)")
    add_bullet(doc, "Moderní elektrárny: 6–8 regenerativních ohřevů, η_t ≈ 42–46 %", is_last=True)

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 2: PRAKTICKÝ ROZBOR
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 2: Praktický rozbor", level=2)

    add_heading(doc, "2.1 Srovnání účinností parních cyklů", level=3)

    add_image(doc, img_eff, width_cm=14,
              caption="Obr. 6: Srovnání typických termických účinností různých konfigurací parních cyklů")

    add_heading(doc, "2.2 Parametry moderních parních elektráren", level=3)

    add_styled_table(doc,
        headers=["Parametr", "Subkritická", "Nadkritická (USC)"],
        data=[
            ["Tlak admisní páry", "16–18 MPa", "25–30 MPa"],
            ["Teplota admisní páry", "540 °C", "600–620 °C"],
            ["Přihřívání", "1×, 540 °C", "1–2×, 620 °C"],
            ["Regenerace", "6–7 stupňů", "8–10 stupňů"],
            ["Termická účinnost", "38–42 %", "45–48 %"],
            ["Celková účinnost (brutto)", "33–37 %", "40–44 %"],
        ],
    )

    add_heading(doc, "2.3 Praktická omezení a problémy", level=3)

    add_para(doc, "Vlhkost páry na výstupu z turbíny:", bold=True, keep_with_next=True)
    add_bullet(doc, "Maximální přípustná vlhkost: x₄ ≥ 0,88 (suchost ≥ 88 %)")
    add_bullet(doc, "Při vyšší vlhkosti hrozí eroze lopatek kapkami kondenzátu")
    add_bullet(doc, "Přehřátí a přihřívání zvyšují suchost na výstupu", is_last=True)

    add_para(doc, "Materiálová omezení:", bold=True, keep_with_next=True)
    add_bullet(doc, "Feritické oceli: max ~580 °C")
    add_bullet(doc, "Austenitické oceli: max ~620 °C")
    add_bullet(doc, "Niklové slitiny (experimentálně): ~700 °C")
    add_bullet(doc, "Vyšší parametry → dražší materiály, kratší životnost", is_last=True)

    add_warning_box(doc,
        "Carnotova účinnost pro moderní parametry (T_H = 600 °C, T_C = 30 °C) je η_C = 65 %. "
        "Reálné elektrárny dosahují 40–48 %, tj. 60–75 % Carnotovy účinnosti. "
        "Ztráty jsou způsobeny nevratnostmi v turbíně, kotli, potrubí a vlastní spotřebou.")

    add_heading(doc, "2.4 Parní tabulky a software", level=3)
    add_para(doc,
        "Pro výpočty parních cyklů jsou nezbytné přesné hodnoty termodynamických vlastností "
        "vody/páry. Používají se:")
    add_bullet(doc, "Parní tabulky — IAPWS-IF97 (tabelární hodnoty h, s, v pro sytou kapalinu/páru a přehřátou páru)")
    add_bullet(doc, "CoolProp — open-source software, Python: from CoolProp.CoolProp import PropsSI")
    add_bullet(doc, "NIST REFPROP — komerční, vyšší přesnost")
    add_bullet(doc, "XSteam — jednoduchý Excel/Matlab nástroj pro vlastnosti vodní páry", is_last=True)

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 3: ILUSTRAČNÍ PŘÍKLAD
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 3: Ilustrační příklad", level=2)
    add_heading(doc, "Příklad: Ideální Rankineův cyklus s přehřátou parou", level=3)

    add_para(doc,
        "Zadání: Jednoduchý ideální Rankineův cyklus pracuje s vodní parou. Pára vstupuje "
        "do turbíny při tlaku p₃ = 6 MPa a teplotě T₃ = 500 °C. V kondenzátoru je tlak "
        "p₁ = 10 kPa. Určete termickou účinnost cyklu a suchost páry na výstupu z turbíny.",
        bold=True)

    add_para(doc, "Krok 1: Určení stavových veličin v bodech cyklu", bold=True)
    add_para(doc, "Bod 1 (výstup kondenzátoru) — sytá kapalina při p₁ = 10 kPa:", keep_with_next=True)
    add_equation(doc, r"h_1 = h'(10 \text{ kPa}) = 191{,}8 \text{ kJ/kg}")
    add_equation(doc, r"s_1 = s'(10 \text{ kPa}) = 0{,}6493 \text{ kJ/(kg\cdot K)}")
    add_equation(doc, r"v_1 = 0{,}001010 \text{ m}^3/\text{kg}")

    add_para(doc, "Bod 2 (výstup čerpadla) — izoentropická komprese:", keep_with_next=True)
    add_equation(doc, r"w_P = v_1 (p_2 - p_1) = 0{,}001010 \times (6000 - 10) = 6{,}05 \text{ kJ/kg}")
    add_equation(doc, r"h_2 = h_1 + w_P = 191{,}8 + 6{,}05 = 197{,}85 \text{ kJ/kg}")

    add_para(doc, "Bod 3 (vstup turbíny) — přehřátá pára při 6 MPa, 500 °C:", keep_with_next=True)
    add_equation(doc, r"h_3 = 3422{,}2 \text{ kJ/kg}")
    add_equation(doc, r"s_3 = 6{,}8803 \text{ kJ/(kg\cdot K)}")

    add_para(doc, "Bod 4 (výstup turbíny) — izoentropická expanze, s₄ = s₃:", keep_with_next=True)
    add_equation(doc, r"s_4 = s_3 = 6{,}8803 \text{ kJ/(kg\cdot K)}")
    add_para(doc, "Při p₄ = 10 kPa: s' = 0,6493, s'' = 8,1502 kJ/(kg·K)", keep_with_next=True)
    add_equation(doc, r"x_4 = \frac{s_4 - s'}{s'' - s'} = \frac{6{,}8803 - 0{,}6493}{8{,}1502 - 0{,}6493} = 0{,}831")
    add_equation(doc, r"h_4 = h' + x_4 \cdot l = 191{,}8 + 0{,}831 \times 2392{,}8 = 2180{,}2 \text{ kJ/kg}")

    add_para(doc, "Krok 2: Výpočet účinnosti", bold=True)
    add_equation(doc, r"q_{in} = h_3 - h_2 = 3422{,}2 - 197{,}85 = 3224{,}35 \text{ kJ/kg}")
    add_equation(doc, r"w_T = h_3 - h_4 = 3422{,}2 - 2180{,}2 = 1242{,}0 \text{ kJ/kg}")
    add_equation(doc, r"w_{net} = w_T - w_P = 1242{,}0 - 6{,}05 = 1235{,}95 \text{ kJ/kg}")
    add_equation(doc, r"\eta_t = \frac{w_{net}}{q_{in}} = \frac{1235{,}95}{3224{,}35} = 0{,}383 = 38{,}3 \%")

    add_info_box(doc,
        "Výsledky:",
        "Termická účinnost: η_t = 38,3 %\n"
        "Suchost na výstupu z turbíny: x₄ = 0,831 (83,1 %)\n\n"
        "Poznámka: Suchost x₄ = 83,1 % je pod přípustnou mezí 88 % → v praxi by se použilo "
        "přihřívání páry ke zvýšení suchosti na výstupu.")

    add_para(doc, "Krok 3: Srovnání s Carnotovým cyklem", bold=True)
    add_equation(doc, r"\eta_{Carnot} = 1 - \frac{T_C}{T_H} = 1 - \frac{318{,}95}{773{,}15} = 0{,}587 = 58{,}7 \%")
    add_para(doc,
        "Rankineův cyklus dosahuje 65 % Carnotovy účinnosti. Rozdíl je dán hlavně tím, "
        "že přívod tepla v kotli není izotermický (ohřev kapaliny probíhá při teplotě nižší "
        "než je teplota varu).")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 4: TYPICKÉ ZKOUŠKOVÉ OTÁZKY
    # ═══════════════════════════════════════════════════════════════════════
    add_exam_questions(doc, [
        ("Proč je termická účinnost Rankineova cyklu nižší než Carnotova cyklu mezi stejnými teplotami?",
         "Protože přívod tepla v kotli není izotermický — ohřev kapaliny od teploty kondenzátoru "
         "do teploty varu probíhá při teplotě výrazně nižší než maximální teplota cyklu. "
         "Střední termodynamická teplota přívodu tepla je proto nižší než T_H u Carnota."),

        ("Co je suchost páry a proč je důležitá na výstupu z turbíny?",
         "Suchost x je hmotnostní podíl suché syté páry v mokré páře (x = m_pára/m_celk). "
         "Na výstupu z turbíny musí být x ≥ 0,88 (suchost ≥ 88 %), jinak kapky kondenzátu "
         "erodují lopatky turbíny a snižují její životnost a účinnost."),

        ("Jak přihřívání páry zvyšuje účinnost cyklu a zároveň řeší problém vlhkosti?",
         "Přihříváním se zvyšuje střední teplota přívodu tepla (přidává se teplo při vysoké "
         "teplotě po částečné expanzi). Současně se pára na vstupu do LP turbíny dostává "
         "zpět do přehřáté oblasti, takže na výstupu z LP turbíny má vyšší suchost."),

        ("Vysvětlete princip regenerativního ohřevu napájecí vody. Proč zvyšuje účinnost?",
         "Část páry se odebírá z turbíny a ohřívá napájecí vodu před vstupem do kotle. "
         "Tím se eliminuje přívod tepla při nejnižších teplotách (ohřev studené vody), "
         "což zvyšuje střední teplotu přívodu tepla a přibližuje cyklus Carnotovu."),

        ("Jaký je rozdíl mezi otevřeným a uzavřeným ohřívákem napájecí vody?",
         "Otevřený (směšovací): pára se mísí přímo s vodou — jednoduchý, levný, zároveň "
         "odplyňuje (odstraňuje rozpuštěné plyny). Uzavřený (povrchový): teplo se předává "
         "přes teplosměnnou plochu, proudy se nemísí — složitější, ale umožňuje více stupňů "
         "regenerace bez kaskády čerpadel."),

        ("Proč se v moderních elektrárnách používá nadkritický tlak páry?",
         "Nad kritickým tlakem (22,06 MPa) neexistuje fázový přechod kapalina–pára, celý ohřev "
         "probíhá v jednofázové oblasti. Střední teplota přívodu tepla je vyšší, protože "
         "odpadá izoterma varu. Nadkritické bloky dosahují η_t = 45–48 % vs. 38–42 % u subkritických."),

        ("Jak byste z parních tabulek určili stav páry na výstupu z turbíny při izoentropické expanzi?",
         "Známe s₃ = s₄ (izoentropická expanze). Při tlaku kondenzátoru p₄ porovnáme s₄ s hodnotami "
         "s' a s'' z tabulek sytosti. Pokud s' < s₄ < s'', jde o mokrou páru a suchost určíme "
         "jako x₄ = (s₄ − s')/(s'' − s'). Entalpii pak h₄ = h' + x₄·(h'' − h')."),
    ])

    # ── Zápatí: Zdroje ──
    doc.add_paragraph()
    doc.add_paragraph("─" * 60)
    add_para(doc, "Zdroje a doporučená literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Çengel, Y.A., Boles, M.A.: Thermodynamics — An Engineering Approach, 9th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "Kadrnožka, J.: Tepelné elektrárny a teplárny, SNTL")
    add_bullet(doc, "IAPWS-IF97: Mezinárodní asociace pro vlastnosti vody a páry")
    add_bullet(doc, "CoolProp — open-source databáze termodynamických vlastností", is_last=True)

    # ── Save ──
    save_and_export(doc, "07-pary-parni-cyklus")


if __name__ == "__main__":
    generate()
