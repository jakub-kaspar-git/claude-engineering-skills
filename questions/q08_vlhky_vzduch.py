"""
Státnicová otázka 8: Vlhký vzduch a vlhké technické plyny.
Absolutní, relativní a měrná vlhkost vzduchu.
Entalpie vlhkého vzduchu a jeho tepelný diagram, vlhčení.
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


# ═════════════════════════════════════════════════════════════════════════════
# GRAFY
# ═════════════════════════════════════════════════════════════════════════════

def generate_mollier_hx():
    """Generate simplified Mollier h-x diagram for moist air at 101.325 kPa."""
    fig, ax = plt.subplots(figsize=(9, 7))

    # x axis: měrná vlhkost x [g/kg s.v.], range 0–30
    # y axis: entalpie h [kJ/kg s.v.]
    x_range = np.linspace(0, 30, 300)  # g/kg

    # Isotherms: h = cp_a * t + x * (l_0 + cp_v * t)
    # cp_a = 1.006 kJ/(kg·K), cp_v = 1.84 kJ/(kg·K), l_0 = 2501 kJ/kg
    cp_a = 1.006
    cp_v = 1.84
    l_0 = 2501.0

    temps = [-10, 0, 10, 20, 30, 40, 50]
    for i, t in enumerate(temps):
        h = cp_a * t + (x_range / 1000) * (l_0 + cp_v * t)
        color = plt.cm.RdYlBu_r((t + 10) / 60)
        ax.plot(x_range, h, color=color, linewidth=1.5, alpha=0.8)
        # Label at the right end
        ax.text(x_range[-1] + 0.5, h[-1], f"{t} °C", fontsize=8, va="center", color=color)

    # Saturation curve (phi = 100%)
    # Antoine equation for water: log10(p_s) = A - B/(C+T)
    # Simplified: p_s(T) in Pa
    def p_sat(T_C):
        return 610.78 * np.exp(17.27 * T_C / (T_C + 237.3))

    p_atm = 101325.0
    t_sat_range = np.linspace(-10, 50, 300)
    x_sat = np.zeros_like(t_sat_range)
    h_sat = np.zeros_like(t_sat_range)
    for i, t in enumerate(t_sat_range):
        ps = p_sat(t)
        x_sat[i] = 622 * ps / (p_atm - ps)  # g/kg
        h_sat[i] = cp_a * t + (x_sat[i] / 1000) * (l_0 + cp_v * t)

    mask = x_sat <= 30
    ax.plot(x_sat[mask], h_sat[mask], color="black", linewidth=2.5, label="φ = 100 % (křivka sytosti)")

    # Relative humidity lines: phi = 20%, 40%, 60%, 80%
    for phi_pct in [20, 40, 60, 80]:
        phi = phi_pct / 100
        x_phi = np.zeros_like(t_sat_range)
        h_phi = np.zeros_like(t_sat_range)
        for i, t in enumerate(t_sat_range):
            ps = p_sat(t)
            pp = phi * ps
            x_phi[i] = 622 * pp / (p_atm - pp)  # g/kg
            h_phi[i] = cp_a * t + (x_phi[i] / 1000) * (l_0 + cp_v * t)
        mask_phi = x_phi <= 30
        ax.plot(x_phi[mask_phi], h_phi[mask_phi], color="gray", linewidth=1,
                linestyle="--", alpha=0.6)
        # Label
        idx = len(x_phi[mask_phi]) - 1
        if idx > 0:
            ax.text(x_phi[mask_phi][idx] + 0.3, h_phi[mask_phi][idx],
                    f"φ={phi_pct}%", fontsize=7, color="gray", va="center")

    # Region labels
    ax.text(5, 60, "Nenasycený\nvlhký vzduch\n(φ < 100 %)", fontsize=10,
            ha="center", style="italic", color=COLORS[0], alpha=0.7)
    ax.text(22, 20, "Oblast mlhy\n(φ = 100 %,\npřebytek kondenzátu)", fontsize=9,
            ha="center", style="italic", color=COLORS[1], alpha=0.7)

    ax.set_xlabel("Měrná vlhkost x [g/kg suchého vzduchu]", fontsize=11)
    ax.set_ylabel("Měrná entalpie h [kJ/kg suchého vzduchu]", fontsize=11)
    ax.set_title("h-x diagram vlhkého vzduchu (Mollierův diagram)\np = 101,325 kPa",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(0, 32)
    ax.set_ylim(-15, 120)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q08_mollier_hx.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_humidity_types():
    """Visual comparison of absolute, relative and specific humidity."""
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")

    # 1. Absolutní vlhkost
    ax = axes[0]
    box = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.05",
                          facecolor="#DBEAFE", edgecolor="#2563EB", linewidth=2)
    ax.add_patch(box)
    ax.text(0.5, 0.8, "Absolutní vlhkost", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#2563EB")
    ax.text(0.5, 0.55, r"$\rho_v = \frac{m_v}{V}$", ha="center", va="center",
            fontsize=14, color="#1E40AF")
    ax.text(0.5, 0.35, "[kg/m³]", ha="center", va="center", fontsize=10, color="#555")
    ax.text(0.5, 0.15, "Hmotnost vodní páry\nna jednotku objemu", ha="center", va="center",
            fontsize=8, color="#555")

    # 2. Relativní vlhkost
    ax = axes[1]
    box = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.05",
                          facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2)
    ax.add_patch(box)
    ax.text(0.5, 0.8, "Relativní vlhkost", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#DC2626")
    ax.text(0.5, 0.55, r"$\varphi = \frac{p_p}{p_s(T)}$", ha="center", va="center",
            fontsize=14, color="#991B1B")
    ax.text(0.5, 0.35, "[%, –]", ha="center", va="center", fontsize=10, color="#555")
    ax.text(0.5, 0.15, "Poměr parciálního tlaku\nku tlaku nasycených par", ha="center", va="center",
            fontsize=8, color="#555")

    # 3. Měrná vlhkost
    ax = axes[2]
    box = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.05",
                          facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=2)
    ax.add_patch(box)
    ax.text(0.5, 0.8, "Měrná vlhkost", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#16A34A")
    ax.text(0.5, 0.55, r"$x = \frac{m_v}{m_a}$", ha="center", va="center",
            fontsize=14, color="#166534")
    ax.text(0.5, 0.35, "[kg/kg s.v.] nebo [g/kg]", ha="center", va="center", fontsize=10, color="#555")
    ax.text(0.5, 0.15, "Hmotnost vodní páry\nna 1 kg suchého vzduchu", ha="center", va="center",
            fontsize=8, color="#555")

    fig.suptitle("Tři způsoby vyjádření vlhkosti vzduchu", fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q08_humidity_types.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_processes_hx():
    """Generate h-x diagram with typical HVAC processes."""
    fig, ax = plt.subplots(figsize=(9, 6))

    cp_a = 1.006
    cp_v = 1.84
    l_0 = 2501.0
    p_atm = 101325.0

    def p_sat(T_C):
        return 610.78 * np.exp(17.27 * T_C / (T_C + 237.3))

    def h_from_tx(t, x_gkg):
        return cp_a * t + (x_gkg / 1000) * (l_0 + cp_v * t)

    # Saturation curve
    t_range = np.linspace(-5, 45, 300)
    x_sat = np.array([622 * p_sat(t) / (p_atm - p_sat(t)) for t in t_range])
    h_sat_vals = np.array([h_from_tx(t, x) for t, x in zip(t_range, x_sat)])
    mask = x_sat <= 25
    ax.plot(x_sat[mask], h_sat_vals[mask], "k-", linewidth=2, label="φ = 100 %")

    # Light isotherms
    for t in [0, 10, 20, 30, 40]:
        x_iso = np.linspace(0, 25, 100)
        h_iso = np.array([h_from_tx(t, xi) for xi in x_iso])
        ax.plot(x_iso, h_iso, color="gray", linewidth=0.5, alpha=0.4)
        ax.text(0.3, h_from_tx(t, 0) + 1, f"{t}°C", fontsize=7, color="gray")

    # Process 1: Ohřev (heating) — horizontální (x = const)
    x_A, t_A = 5.0, 5.0
    t_B = 35.0
    h_A = h_from_tx(t_A, x_A)
    h_B = h_from_tx(t_B, x_A)
    ax.annotate("", xy=(x_A, h_B), xytext=(x_A, h_A),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[1], lw=2.5))
    ax.plot(x_A, h_A, "o", color=COLORS[1], markersize=8, zorder=5)
    ax.plot(x_A, h_B, "s", color=COLORS[1], markersize=8, zorder=5)
    ax.text(x_A + 0.5, (h_A + h_B) / 2, "Ohřev\n(x = konst.)", fontsize=8,
            color=COLORS[1], fontweight="bold")

    # Process 2: Adiabatické vlhčení — h ≈ const (along isotherm of wet bulb)
    x_C, t_C = 5.0, 20.0
    x_D = 14.0
    h_C = h_from_tx(t_C, x_C)
    h_D = h_C  # adiabatic
    ax.annotate("", xy=(x_D, h_D), xytext=(x_C, h_C),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[2], lw=2.5))
    ax.plot(x_C, h_C, "o", color=COLORS[2], markersize=8, zorder=5)
    ax.plot(x_D, h_D, "s", color=COLORS[2], markersize=8, zorder=5)
    ax.text((x_C + x_D) / 2, h_C + 3, "Adiabatické vlhčení\n(h ≈ konst.)", fontsize=8,
            color=COLORS[2], fontweight="bold", ha="center")

    # Process 3: Chlazení s odvlhčením — podél φ=100% dolů
    x_E, t_E = 12.0, 30.0
    t_F = 10.0
    h_E = h_from_tx(t_E, x_E)
    ps_F = p_sat(t_F)
    x_F = 622 * ps_F / (p_atm - ps_F)
    h_F = h_from_tx(t_F, x_F)
    ax.annotate("", xy=(x_F, h_F), xytext=(x_E, h_E),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=2.5))
    ax.plot(x_E, h_E, "o", color=COLORS[0], markersize=8, zorder=5)
    ax.plot(x_F, h_F, "s", color=COLORS[0], markersize=8, zorder=5)
    ax.text(x_E + 0.5, h_E - 5, "Chlazení\ns odvlhčením", fontsize=8,
            color=COLORS[0], fontweight="bold")

    # Process 4: Směšování dvou proudů
    x_G, t_G = 3.0, 0.0
    x_H, t_H = 10.0, 25.0
    h_G = h_from_tx(t_G, x_G)
    h_H = h_from_tx(t_H, x_H)
    x_M = (x_G + x_H) / 2
    h_M = (h_G + h_H) / 2
    ax.plot([x_G, x_H], [h_G, h_H], "--", color=COLORS[3], linewidth=2)
    ax.plot(x_G, h_G, "o", color=COLORS[3], markersize=8, zorder=5)
    ax.plot(x_H, h_H, "o", color=COLORS[3], markersize=8, zorder=5)
    ax.plot(x_M, h_M, "D", color=COLORS[3], markersize=10, zorder=5)
    ax.text(x_M + 0.5, h_M + 3, "Směšování\n(M na úsečce)", fontsize=8,
            color=COLORS[3], fontweight="bold")

    ax.set_xlabel("Měrná vlhkost x [g/kg s.v.]", fontsize=11)
    ax.set_ylabel("Měrná entalpie h [kJ/kg s.v.]", fontsize=11)
    ax.set_title("Základní procesy úpravy vlhkého vzduchu v h-x diagramu",
                 fontsize=11, fontweight="bold")
    ax.set_xlim(0, 26)
    ax.set_ylim(-10, 90)
    ax.legend(loc="upper left", fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q08_processes_hx.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_saturation_pressure():
    """Plot saturation pressure of water vs temperature."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    T = np.linspace(-10, 60, 300)
    ps = 610.78 * np.exp(17.27 * T / (T + 237.3))

    ax.plot(T, ps / 1000, color=COLORS[0], linewidth=2.5, label="p_s(T)")
    ax.fill_between(T, 0, ps / 1000, alpha=0.08, color=COLORS[0])

    # Mark typical indoor conditions
    ax.axvline(x=20, color="gray", linestyle=":", linewidth=1)
    ax.axvline(x=35, color="gray", linestyle=":", linewidth=1)
    ps_20 = 610.78 * np.exp(17.27 * 20 / (20 + 237.3)) / 1000
    ps_35 = 610.78 * np.exp(17.27 * 35 / (35 + 237.3)) / 1000
    ax.plot(20, ps_20, "ko", markersize=8, zorder=5)
    ax.plot(35, ps_35, "ko", markersize=8, zorder=5)
    ax.annotate(f"20 °C: {ps_20:.2f} kPa", xy=(20, ps_20), xytext=(25, ps_20 - 0.5),
                fontsize=9, arrowprops=dict(arrowstyle="->", lw=1))
    ax.annotate(f"35 °C: {ps_35:.2f} kPa", xy=(35, ps_35), xytext=(40, ps_35 - 1),
                fontsize=9, arrowprops=dict(arrowstyle="->", lw=1))

    ax.set_xlabel("Teplota T [°C]", fontsize=11)
    ax.set_ylabel("Tlak nasycených par p_s [kPa]", fontsize=11)
    ax.set_title("Závislost tlaku nasycených vodních par na teplotě",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(-10, 60)
    ax.set_ylim(0, 22)
    ax.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q08_saturation_pressure.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_dewpoint_schema():
    """Schematic showing dew point concept."""
    fig, ax = plt.subplots(figsize=(8, 4))

    cp_a = 1.006
    cp_v = 1.84
    l_0 = 2501.0
    p_atm = 101325.0

    def p_sat(T_C):
        return 610.78 * np.exp(17.27 * T_C / (T_C + 237.3))

    # Plot saturation curve as T vs x
    T_range = np.linspace(-5, 40, 200)
    x_sat = np.array([622 * p_sat(t) / (p_atm - p_sat(t)) for t in T_range])

    ax.plot(x_sat, T_range, "k-", linewidth=2, label="Křivka sytosti (φ=100%)")

    # Point A: air at 25°C, x=10 g/kg (phi ≈ 50%)
    x_A = 10.0
    T_A = 25.0
    ax.plot(x_A, T_A, "o", color=COLORS[1], markersize=12, zorder=5)
    ax.annotate("Stav vzduchu A\n(25 °C, x=10 g/kg, φ≈50%)",
                xy=(x_A, T_A), xytext=(x_A + 4, T_A + 3),
                fontsize=9, fontweight="bold", color=COLORS[1],
                arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=1.5))

    # Dew point: cool at x=const until hitting saturation
    T_dew = np.interp(x_A, x_sat, T_range)
    ax.plot(x_A, T_dew, "s", color=COLORS[0], markersize=12, zorder=5)
    ax.annotate(f"Rosný bod\nT_r = {T_dew:.1f} °C",
                xy=(x_A, T_dew), xytext=(x_A + 4, T_dew - 3),
                fontsize=9, fontweight="bold", color=COLORS[0],
                arrowprops=dict(arrowstyle="->", color=COLORS[0], lw=1.5))

    # Arrow down from A to dew point
    ax.annotate("", xy=(x_A, T_dew + 0.5), xytext=(x_A, T_A - 0.5),
                arrowprops=dict(arrowstyle="-|>", color=COLORS[0], lw=2, linestyle="--"))
    ax.text(x_A - 1.5, (T_A + T_dew) / 2, "Chlazení\n(x = konst.)", fontsize=8,
            color=COLORS[0], ha="center")

    ax.set_xlabel("Měrná vlhkost x [g/kg s.v.]", fontsize=11)
    ax.set_ylabel("Teplota T [°C]", fontsize=11)
    ax.set_title("Rosný bod — ochlazení vzduchu při konstantní vlhkosti x",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(0, 25)
    ax.set_ylim(-5, 40)
    ax.legend(loc="upper left", fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q08_dewpoint.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ═════════════════════════════════════════════════════════════════════════════
# OBSAH DOKUMENTU
# ═════════════════════════════════════════════════════════════════════════════

def generate():
    print("Generuji diagramy...")
    img_mollier = generate_mollier_hx()
    img_humidity = generate_humidity_types()
    img_processes = generate_processes_hx()
    img_psat = generate_saturation_pressure()
    img_dewpoint = generate_dewpoint_schema()
    print("Diagramy hotové. Generuji .docx...")

    doc = create_document(
        title="8. Vlhký vzduch a vlhké technické plyny.\n"
              "    Absolutní, relativní a měrná vlhkost vzduchu.\n"
              "    Entalpie vlhkého vzduchu a jeho tepelný diagram, vlhčení.",
        okruh="Termomechanika a spalování",
    )

    # ── ZADÁNÍ ──
    add_heading(doc, "Zadání", level=2)
    add_para(doc,
        "Vysvětlete pojmy vlhký vzduch a vlhké technické plyny. Definujte absolutní, "
        "relativní a měrnou vlhkost vzduchu a vztahy mezi nimi. Odvoďte entalpii vlhkého "
        "vzduchu, popište jeho tepelný diagram (h-x diagram) a vysvětlete proces vlhčení.")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 1: TEORETICKÝ ROZBOR
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 1: Teoretický rozbor", level=2)

    # ── 1.1 ──
    add_heading(doc, "1.1 Vlhký vzduch — definice a model", level=3)

    add_info_box(doc,
        "Definice: Vlhký vzduch",
        "Směs suchého vzduchu a vodní páry. Suchý vzduch se chová jako ideální plyn "
        "(M_a = 28,964 kg/kmol, r_a = 287,1 J/(kg·K)). Vodní pára při atmosférickém tlaku "
        "má parciální tlak řádově stovky Pa až jednotky kPa — splňuje podmínky ideálního plynu "
        "(M_v = 18,015 kg/kmol, r_v = 461,5 J/(kg·K)).")

    add_para(doc, "Předpoklady modelu:", keep_with_next=True)
    add_bullet(doc, "Suchý vzduch i vodní pára se chovají jako ideální plyny")
    add_bullet(doc, "Platí Daltonův zákon: p = p_a + p_p (celkový tlak = parciální tlak vzduchu + parciální tlak páry)")
    add_bullet(doc, "Při kontaktu s vodou/ledem je v rovnováze nasycený vlhký vzduch (φ = 100 %)")
    add_bullet(doc, "Vlhké technické plyny (spaliny, procesní plyny) se modelují analogicky", is_last=True)

    add_para(doc, "Daltonův zákon pro vlhký vzduch:", keep_with_next=True)
    add_equation(doc, r"p = p_a + p_p", label="1")
    add_para(doc,
        "kde p je celkový (barometrický) tlak, p_a parciální tlak suchého vzduchu "
        "a p_p parciální tlak vodní páry.")

    # ── 1.2 ──
    add_page_break(doc)
    add_heading(doc, "1.2 Způsoby vyjádření vlhkosti", level=3)

    add_image(doc, img_humidity, width_cm=14,
              caption="Obr. 1: Tři základní způsoby vyjádření vlhkosti vzduchu")

    add_heading(doc, "Absolutní vlhkost", level=3)
    add_para(doc,
        "Hmotnost vodní páry obsažené v jednotkovém objemu vlhkého vzduchu. "
        "Numericky se rovná hustotě vodní páry ve směsi:", keep_with_next=True)
    add_equation(doc, r"\rho_v = \frac{m_v}{V} = \frac{p_p}{r_v T}", label="2")
    add_para(doc, "kde r_v = 461,5 J/(kg·K) je měrná plynová konstanta vodní páry.")

    add_heading(doc, "Relativní vlhkost φ", level=3)
    add_info_box(doc,
        "Relativní vlhkost φ",
        "Poměr parciálního tlaku vodní páry k tlaku nasycených par při téže teplotě. "
        "Vyjadřuje stupeň nasycení vzduchu vodní parou.\n"
        "φ = 0 → absolutně suchý vzduch | φ = 1 (100 %) → nasycený vzduch")

    add_equation(doc, r"\varphi = \frac{p_p}{p_s(T)}", label="3")

    add_para(doc,
        "kde p_s(T) je tlak nasycených (sytých) vodních par při teplotě T. "
        "Hodnotu p_s(T) lze určit z parních tabulek nebo z Antoineovy/Magnusovy rovnice.")

    add_image(doc, img_psat, width_cm=13,
              caption="Obr. 2: Závislost tlaku nasycených vodních par na teplotě — exponenciální růst")

    add_page_break(doc)
    add_heading(doc, "Měrná vlhkost x (humidity ratio)", level=3)

    add_info_box(doc,
        "Měrná vlhkost x",
        "Hmotnost vodní páry připadající na 1 kg suchého vzduchu. "
        "Klíčová veličina pro výpočty — zůstává konstantní při ohřevu/chlazení "
        "bez kondenzace nebo přidávání vlhkosti.")

    add_equation(doc, r"x = \frac{m_v}{m_a} = 0{,}622 \cdot \frac{p_p}{p - p_p}", label="4")

    add_para(doc,
        "Konstanta 0,622 = M_v / M_a = 18,015 / 28,964 je poměr molárních hmotností. "
        "Měrná vlhkost se uvádí v kg/kg s.v. nebo častěji v g/kg s.v.")

    add_para(doc, "Vyjádření x pomocí relativní vlhkosti φ:", keep_with_next=True)
    add_equation(doc, r"x = 0{,}622 \cdot \frac{\varphi \cdot p_s(T)}{p - \varphi \cdot p_s(T)}", label="5")

    add_para(doc, "Vzájemné vztahy mezi veličinami vlhkosti:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["Převod", "Vztah"],
        data=[
            ["φ → x", "x = 0,622 · φ·p_s / (p − φ·p_s)"],
            ["x → φ", "φ = x·p / ((0,622 + x)·p_s)"],
            ["x → p_p", "p_p = x·p / (0,622 + x)"],
            ["ρ_v → x", "x = ρ_v · r_v · T / (p − ρ_v · r_v · T) · (M_v/M_a)"],
        ],
    )

    # ── 1.3 Rosný bod ──
    add_heading(doc, "1.3 Rosný bod (teplota rosného bodu)", level=3)

    add_info_box(doc,
        "Rosný bod T_r",
        "Teplota, na kterou je třeba ochladit vlhký vzduch (při konstantní měrné vlhkosti x), "
        "aby dosáhl stavu nasycení (φ = 100 %). Při dalším ochlazení začíná kondenzace.")

    add_para(doc, "Rosný bod je definován podmínkou:", keep_with_next=True)
    add_equation(doc, r"p_s(T_r) = p_p = \frac{x \cdot p}{0{,}622 + x}", label="6")

    add_image(doc, img_dewpoint, width_cm=13,
              caption="Obr. 3: Rosný bod — ochlazení vzduchu při konstantní vlhkosti x do stavu nasycení")

    # ── 1.4 Entalpie ──
    add_page_break(doc)
    add_heading(doc, "1.4 Entalpie vlhkého vzduchu", level=3)

    add_para(doc,
        "Entalpie vlhkého vzduchu se vztahuje na 1 kg suchého vzduchu (ne na 1 kg směsi!). "
        "Tím je zajištěno, že hmotnostní základ zůstává konstantní i při změnách vlhkosti.")

    add_para(doc, "Měrná entalpie vlhkého vzduchu:", keep_with_next=True)
    add_equation(doc, r"h = h_a + x \cdot h_v", label="7")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "h_a = c_{p,a} · t = 1,006 · t [kJ/kg] — entalpie suchého vzduchu")
    add_bullet(doc, "h_v = l_0 + c_{p,v} · t = 2501 + 1,84 · t [kJ/kg] — entalpie vodní páry", is_last=True)

    add_para(doc, "Po dosazení:", keep_with_next=True)
    add_equation(doc, r"h = c_{p,a} \cdot t + x \cdot (l_0 + c_{p,v} \cdot t)", label="8")
    add_equation(doc, r"h = 1{,}006 \cdot t + x \cdot (2501 + 1{,}84 \cdot t) \quad [\text{kJ/kg s.v.}]", label="9")

    add_para(doc,
        "kde t je teplota [°C], c_{p,a} = 1,006 kJ/(kg·K), c_{p,v} = 1,84 kJ/(kg·K), "
        "l_0 = 2501 kJ/kg je výparné teplo vody při 0 °C.")

    add_warning_box(doc,
        "Referenční stav: t = 0 °C, kapalná voda. Entalpie suchého vzduchu při 0 °C je nulová, "
        "entalpie vodní páry při 0 °C je rovna výparnému teplu l₀ = 2501 kJ/kg.")

    # ── 1.5 h-x diagram ──
    add_page_break(doc)
    add_heading(doc, "1.5 Tepelný diagram vlhkého vzduchu (Mollierův h-x diagram)", level=3)

    add_info_box(doc,
        "Mollierův h-x diagram",
        "Grafická reprezentace stavů vlhkého vzduchu při konstantním celkovém tlaku "
        "(typicky p = 101,325 kPa). Osa x: měrná vlhkost x [g/kg s.v.], "
        "osa y: měrná entalpie h [kJ/kg s.v.]. V technické praxi se často kreslí "
        "se šikmo orientovanou osou x (kosý diagram).")

    add_para(doc, "Prvky diagramu:", keep_with_next=True)
    add_bullet(doc, "Izotermy — přímky (mírně se rozbíhající od osy h) s předpisem h = f(x) při t = konst.")
    add_bullet(doc, "Křivka sytosti (φ = 100 %) — odděluje oblast nenasyceného vzduchu od oblasti mlhy")
    add_bullet(doc, "Izogramy relativní vlhkosti (φ = konst.) — křivky mezi osou h a křivkou sytosti")
    add_bullet(doc, "Oblast nad křivkou sytosti — nenasycený vzduch (pára + vzduch)")
    add_bullet(doc, "Oblast pod křivkou sytosti — přesycený stav (mlha, kapky kondenzátu)", is_last=True)

    add_image(doc, img_mollier, width_cm=14,
              caption="Obr. 4: Mollierův h-x diagram vlhkého vzduchu s izotermami a křivkami konstantní relativní vlhkosti")

    # ── 1.6 Procesy v h-x diagramu ──
    add_page_break(doc)
    add_heading(doc, "1.6 Základní procesy úpravy vlhkého vzduchu", level=3)

    add_image(doc, img_processes, width_cm=14,
              caption="Obr. 5: Základní procesy úpravy vzduchu znázorněné v h-x diagramu")

    add_styled_table(doc,
        headers=["Proces", "Směr v h-x", "x", "h", "Příklad"],
        data=[
            ["Ohřev (suchý)", "Svisle nahoru", "konst.", "roste", "Radiátor, ohřívač"],
            ["Chlazení (suchý)", "Svisle dolů", "konst.", "klesá", "Chladič bez kondenzace"],
            ["Adiabatické vlhčení", "Vodorovně vpravo", "roste", "≈ konst.", "Pračka vzduchu"],
            ["Vlhčení parou", "Šikmo vpravo nahoru", "roste", "roste", "Parní zvlhčovač"],
            ["Chlazení s odvlhčením", "Šikmo vlevo dolů", "klesá", "klesá", "Klimatizace"],
            ["Směšování", "Úsečka mezi body", "podle poměru", "podle poměru", "Směšovací komora"],
        ],
    )

    # ── 1.7 Vlhčení ──
    add_heading(doc, "1.7 Vlhčení vzduchu", level=3)

    add_para(doc, "Rozlišujeme dva základní způsoby vlhčení:", keep_with_next=True)

    add_para(doc, "a) Adiabatické vlhčení (vodou):", bold=True, keep_with_next=True)
    add_para(doc,
        "Voda se rozprašuje nebo odpařuje do proudu vzduchu. Teplo potřebné na odpaření "
        "se odebírá ze vzduchu → teplota klesá, vlhkost roste, entalpie přibližně konstantní "
        "(h ≈ konst.). Teplota se blíží teplotě mokrého teploměru.")
    add_equation(doc, r"\Delta h \approx 0 \quad \Rightarrow \quad c_{p,a} \cdot \Delta t \approx -\Delta x \cdot l_0", label="10")

    add_para(doc, "b) Vlhčení parou:", bold=True, keep_with_next=True)
    add_para(doc,
        "Sytá nebo přehřátá pára se přivádí do proudu vzduchu. Entalpie páry je vysoká → "
        "vzduch se ohřívá a zvlhčuje současně. V h-x diagramu se bod stavu pohybuje "
        "šikmo nahoru-vpravo.")
    add_equation(doc, r"\Delta h = \Delta x \cdot h_{pára}", label="11")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 2: PRAKTICKÝ ROZBOR
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 2: Praktický rozbor", level=2)

    add_heading(doc, "2.1 Komfortní parametry vnitřního prostředí", level=3)

    add_styled_table(doc,
        headers=["Parametr", "Zima", "Léto"],
        data=[
            ["Teplota", "20–24 °C", "23–26 °C"],
            ["Relativní vlhkost", "30–50 %", "40–60 %"],
            ["Měrná vlhkost", "~6–9 g/kg", "~9–13 g/kg"],
            ["Rychlost proudění", "0,1–0,2 m/s", "0,15–0,25 m/s"],
        ],
    )

    add_heading(doc, "2.2 Rosný bod v praxi", level=3)
    add_bullet(doc, "Kondenzace na oknech — povrchová teplota < T_r vnitřního vzduchu")
    add_bullet(doc, "Tepelné mosty — místa s nízkou povrchovou teplotou → kondenzace, plísně")
    add_bullet(doc, "Průmyslové sušení — řízení rosného bodu pro kontrolu kvality")
    add_bullet(doc, "Letecký průmysl — námraza na křídlech při T < T_r okolního vzduchu", is_last=True)

    add_heading(doc, "2.3 Vlhké technické plyny", level=3)
    add_para(doc,
        "Analogicky k vlhkému vzduchu se modelují i jiné technické plyny obsahující vodní páru:")
    add_bullet(doc, "Spaliny — směs CO₂, N₂, H₂O, O₂; rosný bod spalin 45–60 °C (závisí na palivu)")
    add_bullet(doc, "Zemní plyn — obsahuje vodní páru; nutné sušení před transportem")
    add_bullet(doc, "Stlačený vzduch — při kompresi roste parciální tlak páry → kondenzace v rozvodech")
    add_bullet(doc, "Procesní plyny — sušárny, chemický průmysl", is_last=True)

    add_warning_box(doc,
        "U spalin je rosný bod kritický: při spalování sirnatých paliv vzniká SO₃, "
        "který s vodní parou tvoří H₂SO₄. Kyselinový rosný bod spalin může být 120–150 °C! "
        "Teplota spalin na výstupu z kotle musí být nad touto hodnotou.")

    add_heading(doc, "2.4 Měření vlhkosti", level=3)
    add_styled_table(doc,
        headers=["Metoda", "Princip", "Přesnost"],
        data=[
            ["Psychrometr (suchý/mokrý teploměr)", "Rozdíl teplot → φ z tabulek", "±2–3 %"],
            ["Kapacitní snímač", "Změna kapacity polymeru s vlhkostí", "±1–2 %"],
            ["Rosný bod (zrcátkový)", "Ochlazení povrchu do kondenzace", "±0,2 °C"],
            ["Absorpční (LiCl)", "Rovnovážná teplota LiCl roztoku", "±1,5 %"],
        ],
    )

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 3: ILUSTRAČNÍ PŘÍKLAD
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 3: Ilustrační příklad", level=2)
    add_heading(doc, "Příklad: Určení parametrů vlhkého vzduchu", level=3)

    add_para(doc,
        "Zadání: Vlhký vzduch má teplotu t = 30 °C a relativní vlhkost φ = 60 %. "
        "Celkový (barometrický) tlak je p = 101,325 kPa. "
        "Určete: měrnou vlhkost x, parciální tlak vodní páry p_p, rosný bod T_r "
        "a měrnou entalpii h.", bold=True)

    add_para(doc, "Krok 1: Tlak nasycených par při 30 °C", bold=True)
    add_equation(doc, r"p_s(30) = 610{,}78 \cdot \exp\!\left(\frac{17{,}27 \times 30}{30 + 237{,}3}\right) = 4243 \text{ Pa} = 4{,}243 \text{ kPa}")

    add_para(doc, "Krok 2: Parciální tlak vodní páry", bold=True)
    add_equation(doc, r"p_p = \varphi \cdot p_s = 0{,}60 \times 4{,}243 = 2{,}546 \text{ kPa}")

    add_para(doc, "Krok 3: Měrná vlhkost", bold=True)
    add_equation(doc, r"x = 0{,}622 \cdot \frac{p_p}{p - p_p} = 0{,}622 \cdot \frac{2{,}546}{101{,}325 - 2{,}546} = 0{,}01603 \text{ kg/kg}")
    add_equation(doc, r"x = 16{,}03 \text{ g/kg suchého vzduchu}")

    add_para(doc, "Krok 4: Rosný bod", bold=True)
    add_para(doc, "Hledáme teplotu T_r, při které p_s(T_r) = p_p = 2,546 kPa:", keep_with_next=True)
    add_equation(doc, r"T_r = \frac{237{,}3 \cdot \ln(p_p / 610{,}78)}{17{,}27 - \ln(p_p / 610{,}78)}")
    add_equation(doc, r"T_r = \frac{237{,}3 \cdot \ln(2546 / 610{,}78)}{17{,}27 - \ln(2546 / 610{,}78)} = 21{,}4 \text{ °C}")

    add_para(doc, "Krok 5: Měrná entalpie", bold=True)
    add_equation(doc, r"h = 1{,}006 \times 30 + 0{,}01603 \times (2501 + 1{,}84 \times 30)")
    add_equation(doc, r"h = 30{,}18 + 0{,}01603 \times 2556{,}2 = 30{,}18 + 40{,}98")
    add_equation(doc, r"h = 71{,}16 \text{ kJ/kg suchého vzduchu}")

    add_info_box(doc,
        "Výsledky:",
        "Měrná vlhkost: x = 16,03 g/kg s.v.\n"
        "Parciální tlak páry: p_p = 2,546 kPa\n"
        "Rosný bod: T_r = 21,4 °C\n"
        "Měrná entalpie: h = 71,16 kJ/kg s.v.\n\n"
        "Interpretace: Pokud tento vzduch přijde do styku s povrchem chladnějším než 21,4 °C, "
        "začne na něm kondenzovat vodní pára (rosení oken, tepelné mosty).")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 4: TYPICKÉ ZKOUŠKOVÉ OTÁZKY
    # ═══════════════════════════════════════════════════════════════════════
    add_exam_questions(doc, [
        ("Jaký je rozdíl mezi absolutní, relativní a měrnou vlhkostí? Která je nejužitečnější pro výpočty?",
         "Absolutní vlhkost ρ_v [kg/m³] je hustota vodní páry v objemu. Relativní vlhkost φ [%] "
         "je poměr parciálního tlaku páry ku tlaku nasycení — udává stupeň nasycení. Měrná vlhkost "
         "x [g/kg s.v.] je hmotnost páry na 1 kg suchého vzduchu — nejužitečnější pro výpočty, "
         "protože zůstává konstantní při ohřevu/chlazení bez kondenzace (hmotnostní základ se nemění)."),

        ("Proč se entalpie vlhkého vzduchu vztahuje na 1 kg suchého vzduchu, ne na 1 kg směsi?",
         "Protože při procesech úpravy vzduchu (vlhčení, odvlhčování) se mění množství vodní páry, "
         "ale množství suchého vzduchu zůstává konstantní. Vztažením na suchý vzduch zajistíme "
         "stálý hmotnostní základ pro energetické bilance."),

        ("Co je rosný bod a jak ho prakticky určíte?",
         "Rosný bod T_r je teplota, na kterou musíme vzduch ochladit při konstantní vlhkosti x, "
         "aby nastal stav nasycení (φ = 100 %). Prakticky: z parciálního tlaku páry p_p najdeme "
         "teplotu, při které p_s(T_r) = p_p. Měří se zrcátkovým hygrometrem — ochlazujeme "
         "zrcátko, až na něm začne kondenzace."),

        ("Vysvětlete rozdíl mezi adiabatickým vlhčením vodou a vlhčením parou v h-x diagramu.",
         "Adiabatické vlhčení vodou: teplo na odpaření se odebírá ze vzduchu → teplota klesá, "
         "x roste, h ≈ konst. (vodorovný pohyb v h-x diagramu). Vlhčení parou: pára přináší "
         "vlastní entalpii (≈ 2675 kJ/kg) → teplota i x rostou, h roste (šikmý pohyb nahoru-vpravo)."),

        ("Proč je při kompresi vzduchu nutné odvlhčování?",
         "Při kompresi roste parciální tlak vodní páry úměrně celkovému tlaku, ale tlak nasycení "
         "p_s(T) závisí jen na teplotě. Při kompresi na např. 8 bar se p_p zvýší 8×, čímž snadno "
         "překročí p_s → pára kondenzuje v rozvodech. Kondenzát způsobuje korozi a poruchy "
         "pneumatických zařízení, proto se stlačený vzduch suší."),

        ("Co je kyselinový rosný bod spalin a proč je nebezpečný?",
         "Při spalování sirnatých paliv vzniká SO₃, který s vodní parou tvoří H₂SO₄. Kyselinový "
         "rosný bod (120–150 °C) je teplota, pod kterou kondenzuje kyselina sírová na stěnách "
         "spalinových cest. Způsobuje silnou korozi — teplota spalin na výstupu z kotle musí být "
         "nad touto hodnotou, což omezuje využití tepla a snižuje účinnost."),

        ("Jak v h-x diagramu znázorníte směšování dvou proudů vzduchu?",
         "Bod výsledného stavu M leží na úsečce spojující body stavů obou proudů (1 a 2). "
         "Poloha M dělí úsečku v poměru hmotnostních průtoků suchého vzduchu: "
         "úsek 1–M / úsek M–2 = ṁ_a2 / ṁ_a1. Pokud M padne pod křivku sytosti, "
         "dochází ke kondenzaci (mlha) — typický problém při míšení studeného a teplého vlhkého vzduchu."),
    ])

    # ── Zápatí: Zdroje ──
    doc.add_paragraph()
    doc.add_paragraph("─" * 60)
    add_para(doc, "Zdroje a doporučená literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Çengel, Y.A., Boles, M.A.: Thermodynamics — An Engineering Approach, 9th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "Chyský, J., Hemzal, K.: Větrání a klimatizace, Bolit")
    add_bullet(doc, "ASHRAE Handbook — Fundamentals (psychrometrics)")
    add_bullet(doc, "ČSN EN ISO 7730 — Tepelné prostředí", is_last=True)

    # ── Save ──
    save_and_export(doc, "08-vlhky-vzduch")


if __name__ == "__main__":
    generate()
