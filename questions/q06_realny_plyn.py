"""
Státnicová otázka 6: Reálný plyn, zjednodušený výpočet reálných plynů.
Směsi plynů. Adiabatické míšení v proudu.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# Ensure project root is on sys.path so we can import docx_engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from docx_engine import (
    create_document, save_and_export, add_heading, add_para,
    add_equation, add_bullet, add_image, add_info_box,
    add_warning_box, add_page_break, add_styled_table,
    add_exam_questions, COLORS, IMG_DIR,
)

# ═════════════════════════════════════════════════════════════════════════════
# GRAFY SPECIFICKÉ PRO OTÁZKU 6
# ═════════════════════════════════════════════════════════════════════════════


def generate_pv_diagram():
    """Generate p-V diagram comparing ideal vs van der Waals isotherms."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    R = 8.314
    Tc, Pc = 304.2, 73.8e5  # CO2
    a = 27 * R**2 * Tc**2 / (64 * Pc)
    b = R * Tc / (8 * Pc)

    temps = [250, 304.2, 350, 450]
    temp_labels = ["250 K (pod Tk)", "304,2 K (Tk)", "350 K", "450 K"]

    for i, (T, lbl) in enumerate(zip(temps, temp_labels)):
        V_ideal = np.linspace(0.00008, 0.001, 500)
        p_ideal = R * T / V_ideal
        ax.plot(V_ideal * 1e6, p_ideal / 1e6, "--", color=COLORS[i], alpha=0.4, linewidth=1)

        V_vdw = np.linspace(b * 1.05, 0.001, 2000)
        p_vdw = R * T / (V_vdw - b) - a / V_vdw**2
        mask = (p_vdw > 0) & (p_vdw < 300e6)
        ax.plot(V_vdw[mask] * 1e6, p_vdw[mask] / 1e6, "-", color=COLORS[i],
                linewidth=2, label=lbl)

    Vc = 3 * b
    ax.plot(Vc * 1e6, Pc / 1e6, "ko", markersize=10, zorder=5)
    ax.annotate("Kritický bod\n(Tk, pk, vk)", xy=(Vc * 1e6, Pc / 1e6),
                xytext=(Vc * 1e6 + 120, Pc / 1e6 + 15),
                fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    ax.set_xlabel("Molární objem V [cm³/mol]", fontsize=11)
    ax.set_ylabel("Tlak p [MPa]", fontsize=11)
    ax.set_title("p-V diagram: Ideální plyn (čárkovaně) vs. van der Waals (plně) — CO₂",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(50, 800)
    ax.set_ylim(0, 150)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "pv_diagram.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_z_factor_chart():
    """Generate generalized compressibility chart Z(pr) for various Tr."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    Tr_values = [1.0, 1.2, 1.5, 2.0, 3.0, 5.0]
    pr_range = np.linspace(0.01, 7, 500)

    for i, Tr in enumerate(Tr_values):
        Z_vals = []
        for pr in pr_range:
            Ap = 27 * pr / (64 * Tr**2)
            Bp = pr / (8 * Tr)
            coeffs = [1, -(1 + Bp), Ap, -Ap * Bp]
            roots = np.roots(coeffs)
            real_roots = [r.real for r in roots if abs(r.imag) < 1e-6 and r.real > 0]
            Z_vals.append(max(real_roots) if real_roots else np.nan)
        ax.plot(pr_range, Z_vals, color=COLORS[i % len(COLORS)], linewidth=2,
                label=f"Tr = {Tr:.1f}")

    ax.axhline(y=1.0, color="gray", linestyle=":", linewidth=1, alpha=0.7)
    ax.annotate("Z = 1 (ideální plyn)", xy=(5.5, 1.01), fontsize=8, color="gray")

    ax.fill_between([0, 7], [0], [1], alpha=0.05, color="blue")
    ax.text(5.0, 0.45, "Z < 1\npřitažlivé síly\ndominují",
            fontsize=8, ha="center", style="italic", color="#2563EB")
    ax.text(5.0, 1.35, "Z > 1\nodpudivé síly\ndominují",
            fontsize=8, ha="center", style="italic", color="#DC2626")

    ax.set_xlabel("Redukovaný tlak pr = p/pk", fontsize=11)
    ax.set_ylabel("Kompresibilitní faktor Z", fontsize=11)
    ax.set_title("Generalizovaný diagram kompresibilitního faktoru Z",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(0, 7)
    ax.set_ylim(0.2, 1.8)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "z_factor.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_mixing_schema():
    """Generate a schematic of adiabatic mixing chamber."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 5.5)
    ax.set_aspect("equal")
    ax.axis("off")

    chamber = FancyBboxPatch((3, 0.5), 4, 3.5, boxstyle="round,pad=0.2",
                              facecolor="#E8F0FE", edgecolor="#2563EB", linewidth=2.5)
    ax.add_patch(chamber)
    ax.text(5, 2.25, "SMĚŠOVACÍ\nKOMORA", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#1A478A")

    # Stream 1 (hot)
    ax.annotate("", xy=(3, 3.2), xytext=(0.5, 3.2),
                arrowprops=dict(arrowstyle="-|>", color="#DC2626", lw=3))
    box1 = FancyBboxPatch((-0.8, 3.8), 2.8, 1.3, boxstyle="round,pad=0.15",
                           facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=1.5)
    ax.add_patch(box1)
    ax.text(0.6, 4.7, "Proud 1 (horký)", ha="center", va="center",
            fontsize=9, fontweight="bold", color="#DC2626")
    ax.text(0.6, 4.2, "ṁ₁ = 2 kg/s\nT₁ = 150 °C", ha="center", va="center",
            fontsize=8, color="#991B1B")

    # Stream 2 (cold)
    ax.annotate("", xy=(3, 1.3), xytext=(0.5, 1.3),
                arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=3))
    box2 = FancyBboxPatch((-0.8, -0.6), 2.8, 1.3, boxstyle="round,pad=0.15",
                           facecolor="#DBEAFE", edgecolor="#2563EB", linewidth=1.5)
    ax.add_patch(box2)
    ax.text(0.6, 0.3, "Proud 2 (studený)", ha="center", va="center",
            fontsize=9, fontweight="bold", color="#2563EB")
    ax.text(0.6, -0.2, "ṁ₂ = 3 kg/s\nT₂ = 20 °C", ha="center", va="center",
            fontsize=8, color="#1E40AF")

    # Stream 3 (output)
    ax.annotate("", xy=(10, 2.25), xytext=(7, 2.25),
                arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=3))
    box3 = FancyBboxPatch((8.5, 1.3), 2.8, 1.9, boxstyle="round,pad=0.15",
                           facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(box3)
    ax.text(9.9, 2.55, "Proud 3 (výstup)", ha="center", va="center",
            fontsize=9, fontweight="bold", color="#16A34A")
    ax.text(9.9, 1.85, "ṁ₃ = 5 kg/s\nT₃ = 72 °C = ?", ha="center", va="center",
            fontsize=8, color="#166534")

    ax.text(5, -0.3, "Q = 0 (adiabatický)  |  W = 0  |  p = konst.",
            ha="center", fontsize=9, style="italic", color="#555555")

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "mixing_schema.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_mixing_temperature_chart():
    """Generate chart showing output temperature vs mass flow ratio."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    T1, T2 = 150, 20  # °C
    m_total = 5.0
    m1_range = np.linspace(0.01, 4.99, 200)
    m2_range = m_total - m1_range
    T3 = (m1_range * (T1 + 273.15) + m2_range * (T2 + 273.15)) / m_total - 273.15

    ax.plot(m1_range, T3, color=COLORS[0], linewidth=2.5, label="T₃ výstupní")
    ax.axhline(y=T1, color=COLORS[1], linestyle="--", linewidth=1, alpha=0.6, label=f"T₁ = {T1} °C")
    ax.axhline(y=T2, color=COLORS[2], linestyle="--", linewidth=1, alpha=0.6, label=f"T₂ = {T2} °C")

    ax.plot(2, 72, "ko", markersize=10, zorder=5)
    ax.annotate("Náš příklad\nṁ₁=2, T₃=72 °C", xy=(2, 72), xytext=(2.8, 50),
                fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    ax.fill_between(m1_range, T2, T3, alpha=0.08, color=COLORS[0])

    ax.set_xlabel("Hmotnostní průtok horkého proudu ṁ₁ [kg/s]", fontsize=11)
    ax.set_ylabel("Výstupní teplota T₃ [°C]", fontsize=11)
    ax.set_title("Závislost výstupní teploty na poměru průtoků\n(ṁ₁ + ṁ₂ = 5 kg/s, T₁ = 150 °C, T₂ = 20 °C)",
                 fontsize=11, fontweight="bold")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 170)
    ax.legend(loc="upper left", fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "mixing_temperature.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_equation_comparison_chart():
    """Bar chart comparing accuracy of different equations of state."""
    fig, ax = plt.subplots(figsize=(7, 4))

    equations = ["Ideální plyn", "Van der Waals", "Redlich-Kwong", "Peng-Robinson", "Virialová (B,C)"]
    errors = [15, 8, 3.5, 1.5, 0.5]
    colors = ["#DC2626", "#D97706", "#2563EB", "#16A34A", "#059669"]

    bars = ax.barh(equations, errors, color=colors, edgecolor="white", height=0.6)

    for bar, err in zip(bars, errors):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{err} %", va="center", fontsize=10, fontweight="bold")

    ax.set_xlabel("Typická chyba při středních tlacích [%]", fontsize=11)
    ax.set_title("Srovnání přesnosti stavových rovnic", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 20)
    ax.invert_yaxis()

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "equation_comparison.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_dalton_schema():
    """Visual representation of Dalton's law."""
    fig, axes = plt.subplots(1, 4, figsize=(10, 3.5))

    gases = [
        ("N₂", 0.78, "#2563EB"),
        ("O₂", 0.21, "#DC2626"),
        ("Ar", 0.01, "#16A34A"),
    ]

    for i, (name, frac, color) in enumerate(gases):
        ax = axes[i]
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        box = FancyBboxPatch((0.05, 0.05), 0.9, 0.9, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor="black", alpha=0.15, linewidth=1.5)
        ax.add_patch(box)
        ax.text(0.5, 0.65, name, ha="center", va="center", fontsize=16, fontweight="bold", color=color)
        ax.text(0.5, 0.4, f"xi = {frac}", ha="center", va="center", fontsize=10)
        ax.text(0.5, 0.25, f"pi = {frac}p", ha="center", va="center", fontsize=10, style="italic")
        ax.set_title(f"Složka {i+1}", fontsize=9)
        ax.axis("off")

    ax = axes[3]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    for j, (_, _, color) in enumerate(gases):
        box = FancyBboxPatch((0.05 + j*0.02, 0.05 + j*0.02), 0.9 - j*0.04, 0.9 - j*0.04,
                              boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor="black", alpha=0.1, linewidth=1)
        ax.add_patch(box)
    ax.text(0.5, 0.6, "SMĚS", ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(0.5, 0.4, "p = Σ pi", ha="center", va="center", fontsize=11, style="italic")
    ax.set_title("Celková směs", fontsize=9)
    ax.axis("off")

    fig.suptitle("Daltonův zákon parciálních tlaků (příklad: vzduch)",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "dalton_law.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ═════════════════════════════════════════════════════════════════════════════
# OBSAH DOKUMENTU
# ═════════════════════════════════════════════════════════════════════════════

def generate():
    print("Generuji diagramy...")
    img_pv = generate_pv_diagram()
    img_z = generate_z_factor_chart()
    img_mixing = generate_mixing_schema()
    img_temp = generate_mixing_temperature_chart()
    img_eq_cmp = generate_equation_comparison_chart()
    img_dalton = generate_dalton_schema()
    print("Diagramy hotové. Generuji .docx...")

    doc = create_document(
        title="6. Reálný plyn, zjednodušený výpočet reálných plynů.\n"
              "    Směsi plynů. Adiabatické míšení v proudu.",
        okruh="Termodynamika",
    )

    # ── ZADÁNÍ ──
    add_heading(doc, "Zadání", level=2)
    add_para(doc,
        "Vysvětlete chování reálného plynu a jeho odchylky od modelu ideálního plynu. "
        "Popište základní stavové rovnice pro reálné plyny a zjednodušené metody jejich výpočtu. "
        "Vysvětlete principy popisu směsí plynů a proces adiabatického míšení v proudu.")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 1: TEORETICKÝ ROZBOR
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 1: Teoretický rozbor", level=2)

    # ── 1.1 ──
    add_heading(doc, "1.1 Ideální plyn a jeho omezení", level=3)

    add_info_box(doc,
        "Definice: Ideální plyn",
        "Teoretický model plynu, jehož molekuly jsou hmotné body bez vlastního objemu, "
        "mezi nimiž nepůsobí žádné mezimolekulární síly a jejichž srážky jsou dokonale pružné.")

    add_para(doc, "Stavová rovnice ideálního plynu:", keep_with_next=True)
    add_equation(doc, r"pV = nRT", label="1")

    add_para(doc,
        "kde p je tlak [Pa], V objem [m³], n látkové množství [mol], "
        "R = 8,314 J/(mol·K) univerzální plynová konstanta a T termodynamická teplota [K].")

    add_para(doc, "Pro měrné veličiny (na jednotku hmotnosti):", keep_with_next=True)
    add_equation(doc, r"pv = r T", label="2")

    add_para(doc,
        "kde v je měrný objem [m³/kg] a r = R/M je měrná plynová konstanta [J/(kg·K)].")

    add_warning_box(doc,
        "Model ideálního plynu je dostatečně přesný pouze při nízkých tlacích a vysokých teplotách "
        "(daleko od kritického bodu). Při vyšších tlacích a nižších teplotách selhává!")

    # ── 1.2 ──
    add_heading(doc, "1.2 Reálný plyn a kompresibilitní faktor", level=3)
    add_para(doc, "Reálný plyn se od ideálního liší ve dvou zásadních ohledech:", keep_with_next=True)
    add_bullet(doc, "Molekuly mají konečný vlastní objem (kovolum b) — při vysokém tlaku nelze objem stlačit na nulu")
    add_bullet(doc, "Mezi molekulami působí mezimolekulární síly (van der Waalsovy) — přitažlivé na střední vzdálenosti, odpudivé na velmi krátké", is_last=True)

    add_info_box(doc,
        "Klíčová veličina: Kompresibilitní faktor Z",
        "Bezrozměrná veličina vyjadřující míru odchylky od ideálního chování.\n"
        "Z = 1 → ideální plyn  |  Z < 1 → přitažlivé síly dominují  |  Z > 1 → odpudivé síly dominují")

    add_para(doc, "Kompresibilitní faktor je definován jako:", keep_with_next=True)
    add_equation(doc, r"Z = \frac{pv}{rT} = \frac{pV}{nRT}", label="3")

    add_image(doc, img_z, width_cm=14,
              caption="Obr. 1: Generalizovaný diagram kompresibilitního faktoru Z v závislosti na redukovaném tlaku pr pro různé redukované teploty Tr")

    # ── 1.3 ──
    add_page_break(doc)
    add_heading(doc, "1.3 Van der Waalsova stavová rovnice", level=3)
    add_para(doc,
        "Historicky první a nejznámější korekce ideální stavové rovnice. "
        "Zavádí dva korekční parametry a, b specifické pro každý plyn:")
    add_equation(doc, r"\left(p + \frac{a}{v^2}\right)(v - b) = rT", label="4")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "a — parametr zohledňující mezimolekulární přitažlivé síly [Pa·m⁶/kg²]")
    add_bullet(doc, "b — kovolum, vlastní objem molekul [m³/kg]", is_last=True)

    add_para(doc, "Parametry a, b se určují z kritického bodu:", keep_with_next=True)
    add_equation(doc, r"a = \frac{27 r^2 T_k^2}{64 p_k}", label="5")
    add_equation(doc, r"b = \frac{r T_k}{8 p_k}", label="6")

    add_image(doc, img_pv, width_cm=14,
              caption="Obr. 2: p-V diagram pro CO₂ — srovnání izoterem ideálního plynu (čárkovaně) a van der Waalsova modelu (plně). Pod kritickou teplotou Tk se na van der Waalsových izotermách objevují inflexní body.")

    # ── 1.4 ──
    add_page_break(doc)
    add_heading(doc, "1.4 Další stavové rovnice reálných plynů", level=3)

    add_para(doc,
        "Redlich-Kwongova rovnice — zpřesnění s teplotní závislostí parametru a:",
        keep_with_next=True)
    add_equation(doc, r"p = \frac{rT}{v - b} - \frac{a}{T^{0{,}5} \cdot v(v + b)}", label="7")

    add_para(doc,
        "Peng-Robinsonova rovnice — nejpoužívanější v průmyslu, přesnější pro kapaliny:",
        keep_with_next=True)
    add_equation(doc, r"p = \frac{rT}{v - b} - \frac{a(T)}{v(v + b) + b(v - b)}", label="8")

    add_para(doc, "Virialová stavová rovnice — rozvoj Z v řadu:", keep_with_next=True)
    add_equation(doc, r"Z = 1 + \frac{B}{v} + \frac{C}{v^2} + \ldots", label="9")

    add_para(doc,
        "kde B, C jsou viriální koeficienty s přímým fyzikálním významem "
        "(B — párové interakce, C — trojice).")

    add_image(doc, img_eq_cmp, width_cm=13,
              caption="Obr. 3: Srovnání typické chyby stavových rovnic při středních tlacích")

    # ── 1.5 ──
    add_page_break(doc)
    add_heading(doc, "1.5 Zákon korespondujících stavů", level=3)
    add_para(doc,
        "Princip korespondujících stavů: všechny plyny se chovají podobně, "
        "jsou-li stavové veličiny vyjádřeny v redukovaném tvaru:")
    add_equation(doc, r"p_r = \frac{p}{p_k}, \quad T_r = \frac{T}{T_k}, \quad v_r = \frac{v}{v_k}", label="10")

    add_para(doc, "Z je pak univerzální funkcí redukovaných veličin:")
    add_equation(doc, r"Z = Z(p_r, T_r)", label="11")

    add_para(doc, "Zpřesnění Pitzerovou korelací s acentrickým faktorem ω:", keep_with_next=True)
    add_equation(doc, r"Z = Z^{(0)}(p_r, T_r) + \omega \cdot Z^{(1)}(p_r, T_r)", label="12")

    add_info_box(doc,
        "Praktický přínos",
        "Pro zjednodušený výpočet reálného plynu stačí znát pouze tři parametry: "
        "kritický tlak pk, kritickou teplotu Tk a acentrický faktor ω. "
        "Z generalizovaného diagramu (Obr. 1) pak odečteme Z a dosadíme do pv = ZrT.")

    add_para(doc, "Kritické konstanty vybraných plynů:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["Plyn", "Tk [K]", "pk [MPa]", "vk [cm³/mol]", "ω [–]"],
        data=[
            ["Vzduch", "132,5", "3,77", "92,4", "0,035"],
            ["CO₂", "304,2", "7,38", "94,0", "0,225"],
            ["H₂O", "647,1", "22,06", "55,9", "0,344"],
            ["N₂", "126,2", "3,39", "89,2", "0,037"],
            ["CH₄", "190,6", "4,60", "98,6", "0,011"],
            ["O₂", "154,6", "5,04", "73,4", "0,022"],
        ],
    )

    # ── 1.6 ──
    add_page_break(doc)
    add_heading(doc, "1.6 Směsi plynů", level=3)
    add_para(doc, "Složení směsi se popisuje molárními nebo hmotnostními zlomky:", keep_with_next=True)
    add_equation(doc, r"x_i = \frac{n_i}{n_{celk}}, \quad w_i = \frac{m_i}{m_{celk}}", label="13")

    add_info_box(doc,
        "Daltonův zákon parciálních tlaků",
        "Celkový tlak směsi ideálních plynů je roven součtu parciálních tlaků: p = Σ pi = Σ xi·p")

    add_equation(doc, r"p = \sum_{i=1}^{k} p_i, \quad p_i = x_i \cdot p", label="14")

    add_image(doc, img_dalton, width_cm=14,
              caption="Obr. 4: Vizualizace Daltonova zákona na příkladu vzduchu")

    add_para(doc, "Amagatův zákon — celkový objem je součet parciálních objemů:", keep_with_next=True)
    add_equation(doc, r"V = \sum_{i=1}^{k} V_i, \quad V_i = x_i \cdot V", label="15")

    add_para(doc, "Zdánlivá molární hmotnost a měrná plynová konstanta směsi:", keep_with_next=True)
    add_equation(doc, r"M_{sm} = \sum_{i=1}^{k} x_i M_i", label="16")
    add_equation(doc, r"r_{sm} = \frac{R}{M_{sm}} = \sum_{i=1}^{k} w_i r_i", label="17")

    add_para(doc,
        "Pro reálné směsi se parametry stavových rovnic určují směšovacími pravidly "
        "(mixing rules), nejčastěji van der Waalsovým kvadratickým míšením:")
    add_equation(doc, r"a_{sm} = \sum_i \sum_j x_i x_j \sqrt{a_i a_j}", label="18")
    add_equation(doc, r"b_{sm} = \sum_i x_i b_i", label="19")

    # ── 1.7 ──
    add_page_break(doc)
    add_heading(doc, "1.7 Adiabatické míšení v proudu", level=3)

    add_info_box(doc,
        "Definice: Adiabatické míšení",
        "Nevratný proces, při kterém se dva nebo více proudů plynu o různých teplotách, "
        "tlacích a složeních mísí bez výměny tepla s okolím (Q = 0). "
        "Entropie soustavy vždy roste.")

    add_image(doc, img_mixing, width_cm=14,
              caption="Obr. 5: Schéma adiabatické směšovací komory se dvěma vstupy")

    add_para(doc, "Bilance hmotnosti:", keep_with_next=True)
    add_equation(doc, r"\dot{m}_1 + \dot{m}_2 = \dot{m}_3", label="20")

    add_para(doc,
        "Bilance energie (1. zákon TD, Q = 0, W = 0, zanedbána kinetická a potenciální energie):",
        keep_with_next=True)
    add_equation(doc, r"\dot{m}_1 h_1 + \dot{m}_2 h_2 = \dot{m}_3 h_3", label="21")

    add_para(doc, "Pro ideální plyny s konstantním cp a míšení stejných plynů:", keep_with_next=True)
    add_equation(doc, r"T_3 = \frac{\dot{m}_1 T_1 + \dot{m}_2 T_2}{\dot{m}_1 + \dot{m}_2}", label="22")

    add_para(doc, "Při míšení různých plynů, složení výstupního proudu:", keep_with_next=True)
    add_equation(doc, r"w_{i,3} = \frac{\dot{m}_1 w_{i,1} + \dot{m}_2 w_{i,2}}{\dot{m}_3}", label="23")

    add_para(doc, "Bilance entropie a entropie míšení:", keep_with_next=True)
    add_equation(doc, r"\dot{S}_{gen} = \dot{m}_3 s_3 - \dot{m}_1 s_1 - \dot{m}_2 s_2 \geq 0", label="24")
    add_equation(doc, r"\Delta S_{mix} = -nR \sum_{i=1}^{k} x_i \ln x_i > 0", label="25")

    add_para(doc,
        "Entropie míšení je vždy kladná (xi < 1, ln xi < 0), což potvrzuje nevratnost procesu.")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 2: PRAKTICKÝ ROZBOR
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 2: Praktický rozbor", level=2)

    add_heading(doc, "2.1 Kdy nelze použít model ideálního plynu", level=3)

    add_styled_table(doc,
        headers=["Podmínka", "Model", "Typická chyba"],
        data=[
            ["Tr > 2 a pr < 1", "Ideální plyn stačí", "< 1 %"],
            ["Tr = 1,0–1,5 a pr > 0,5", "Nutný reálný model", "5–15 %"],
            ["Tr ≈ 1, pr ≈ 1 (blízko krit. bodu)", "Ideální model selhává", "> 20 %"],
        ],
    )

    add_para(doc, "Typické situace vyžadující reálný model:", keep_with_next=True)
    add_bullet(doc, "Vysokotlaké procesy — kompresory, expanzní turbíny, vysokotlaké reaktory")
    add_bullet(doc, "Zkapalňování plynů — LNG terminály, průmyslové plyny (O₂, N₂, Ar)")
    add_bullet(doc, "Nadkritické procesy — extrakce nadkritickým CO₂, nadkritická voda v elektrárnách")
    add_bullet(doc, "Parní turbíny pracující blízko oblasti mokré páry", is_last=True)

    add_heading(doc, "2.2 Volba stavové rovnice v praxi", level=3)

    add_styled_table(doc,
        headers=["Rovnice", "Typické použití", "Přesnost", "Výhody / Nevýhody"],
        data=[
            ["Van der Waals", "Výuka, kvalitativní", "5–15 %", "Jednoduchá / nepřesná"],
            ["Redlich-Kwong", "Plyny, uhlovodíky", "2–5 %", "Lepší pro plynnou fázi"],
            ["Peng-Robinson", "Ropný průmysl", "1–3 %", "Nejlepší pro kapaliny / složitější"],
            ["Virialová", "Přesné výpočty", "< 1 %", "Fyzikálně podložená / pomalá konvergence"],
        ],
    )

    add_heading(doc, "2.3 Adiabatické míšení — praktické aplikace", level=3)
    add_bullet(doc, "HVAC systémy — míšení čerstvého a recirkulovaného vzduchu v klimatizaci")
    add_bullet(doc, "Spalovací komory — míšení paliva a vzduchu v turbínách a kotlích")
    add_bullet(doc, "Chemické reaktory — míšení reaktantů o různých teplotách")
    add_bullet(doc, "Plynárenství — míšení zemního plynu z různých zdrojů (různé výhřevnosti)")
    add_bullet(doc, "Tepelné výměníky — kontaktní (směšovací) výměníky", is_last=True)

    add_warning_box(doc,
        "U reálných plynů při expanzi/kompresi dochází k Jouleovu-Thomsonovu efektu "
        "(změna teploty při izoentalpické expanzi). U ideálního plynu je tento efekt nulový.")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 3: ILUSTRAČNÍ PŘÍKLAD
    # ═══════════════════════════════════════════════════════════════════════
    add_page_break(doc)
    add_heading(doc, "Část 3: Ilustrační příklad", level=2)
    add_heading(doc, "Příklad: Adiabatické míšení dvou proudů vzduchu", level=3)

    add_para(doc,
        "Zadání: Ve směšovací komoře se adiabaticky mísí dva proudy vzduchu. "
        "Proud 1: ṁ₁ = 2 kg/s, T₁ = 150 °C. Proud 2: ṁ₂ = 3 kg/s, T₂ = 20 °C. "
        "Tlak je konstantní 100 kPa. Vzduch uvažujeme jako ideální plyn s cp = 1,005 kJ/(kg·K). "
        "Určete výstupní teplotu směsi.", bold=True)

    add_para(doc, "Krok 1: Kontrola oprávněnosti modelu ideálního plynu", bold=True)
    add_para(doc,
        "Vzduch: pk = 3,77 MPa, Tk = 132,5 K. Při p = 100 kPa: "
        "pr = 0,1/3,77 = 0,027. Při T = 293–423 K: Tr = 2,2–3,2. "
        "Podmínka Tr > 2, pr < 1 je splněna → ideální plyn je oprávněný.")

    add_para(doc, "Krok 2: Bilance hmotnosti", bold=True)
    add_equation(doc, r"\dot{m}_3 = \dot{m}_1 + \dot{m}_2 = 2 + 3 = 5 \text{ kg/s}")

    add_para(doc, "Krok 3: Bilance energie → výstupní teplota", bold=True)
    add_equation(doc, r"T_3 = \frac{\dot{m}_1 T_1 + \dot{m}_2 T_2}{\dot{m}_3}")
    add_equation(doc, r"T_3 = \frac{2 \times 423{,}15 + 3 \times 293{,}15}{5} = \frac{846{,}3 + 879{,}45}{5}")
    add_equation(doc, r"T_3 = 345{,}15 \text{ K} = 72 \text{ °C}")

    add_info_box(doc,
        "Výsledek: T₃ = 72 °C",
        "Výstupní teplota leží mezi teplotami obou proudů, blíže k teplotě studeného proudu "
        "(který má větší hmotnostní průtok). Proud s větší tepelnou kapacitou (ṁ × cp) "
        "má větší vliv na výslednou teplotu — to odpovídá fyzikální intuici.")

    add_image(doc, img_temp, width_cm=13,
              caption="Obr. 6: Závislost výstupní teploty T₃ na hmotnostním průtoku horkého proudu ṁ₁ (při celkovém průtoku 5 kg/s)")

    # ═══════════════════════════════════════════════════════════════════════
    # ČÁST 4: TYPICKÉ ZKOUŠKOVÉ OTÁZKY
    # ═══════════════════════════════════════════════════════════════════════
    add_exam_questions(doc, [
        ("Pro\u010d nelze pou\u017e\u00edt model ide\u00e1ln\u00edho plynu bl\u00edzko kritick\u00e9ho bodu?",
         "Bl\u00edzko kritick\u00e9ho bodu jsou mezimolekul\u00e1rn\u00ed s\u00edly a vlastn\u00ed objem molekul srovnateln\u00e9 "
         "s termodynamick\u00fdmi veli\u010dinami \u2014 p\u0159ita\u017eliv\u00e9 s\u00edly zp\u016fsobuj\u00ed v\u00fdrazn\u00e9 odchylky tlaku a objemu "
         "od predikce pv = rT. Kompresibilitn\u00ed faktor Z se m\u016f\u017ee odch\u00fdlit o des\u00edtky procent od jedni\u010dky."),

        ("Jak\u00fd je fyzik\u00e1ln\u00ed v\u00fdznam kompresibilitn\u00edho faktoru Z a kdy je Z < 1 vs. Z > 1?",
         "Z = pv/(rT) vyjad\u0159uje m\u00edru odchylky od ide\u00e1ln\u00edho chov\u00e1n\u00ed. Z < 1 znamen\u00e1, \u017ee p\u0159ita\u017eliv\u00e9 "
         "mezimolekul\u00e1rn\u00ed s\u00edly dominuj\u00ed (plyn je stla\u010diteln\u011bj\u0161\u00ed ne\u017e ide\u00e1ln\u00ed) \u2014 typicky p\u0159i st\u0159edn\u00edch "
         "tlac\u00edch. Z > 1 nast\u00e1v\u00e1 p\u0159i vysok\u00fdch tlac\u00edch, kdy dominuje odpudiv\u00fd vlastn\u00ed objem molekul."),

        ("Vysv\u011btlete rozd\u00edl mezi van der Waalsovou a Peng-Robinsonovou stavovou rovnic\u00ed.",
         "Van der Waalsova rovnice je historicky prvn\u00ed dvoukonstantov\u00e1 korekce (parametry a, b). "
         "Je jednoduch\u00e1, ale nep\u0159esn\u00e1 (chyba 5\u201315 %). Peng-Robinsonova rovnice zav\u00e1d\u00ed teplotn\u00ed "
         "z\u00e1vislost parametru a pomoc\u00ed acentrick\u00e9ho faktoru \u03c9 a modifikovan\u00fd \u010dlen pro objem, "
         "\u010d\u00edm\u017e dosahuje chyby 1\u20133 % \u2014 je standardem v ropn\u00e9m a chemick\u00e9m pr\u016fmyslu."),

        ("Co je z\u00e1kon koresponduj\u00edc\u00edch stav\u016f a k \u010demu slou\u017e\u00ed?",
         "Princip, \u017ee v\u0161echny plyny se chovaj\u00ed podobn\u011b, jsou-li stavov\u00e9 veli\u010diny vyj\u00e1d\u0159eny "
         "v redukovan\u00e9m tvaru (p_r = p/p_k, T_r = T/T_k). D\u00edky tomu sta\u010d\u00ed jeden generalizovan\u00fd "
         "diagram Z(p_r, T_r) pro jak\u00fdkoliv plyn \u2014 pot\u0159ebujeme zn\u00e1t jen kritick\u00e9 konstanty."),

        ("Jak se li\u0161\u00ed Dalton\u016fv a Amagat\u016fv z\u00e1kon pro sm\u011bsi plyn\u016f?",
         "Dalton\u016fv z\u00e1kon: celkov\u00fd tlak je sou\u010det parci\u00e1ln\u00edch tlak\u016f slo\u017eek (p = \u03a3 p_i), plat\u00ed "
         "p\u0159i spole\u010dn\u00e9m objemu a teplot\u011b. Amagat\u016fv z\u00e1kon: celkov\u00fd objem je sou\u010det parci\u00e1ln\u00edch "
         "objem\u016f (V = \u03a3 V_i), plat\u00ed p\u0159i spole\u010dn\u00e9m tlaku a teplot\u011b. Pro ide\u00e1ln\u00ed plyny jsou oba "
         "ekvivalentn\u00ed, pro re\u00e1ln\u00e9 plyny d\u00e1vaj\u00ed m\u00edrn\u011b odli\u0161n\u00e9 v\u00fdsledky."),

        ("Pro\u010d je adiabatick\u00e9 m\u00ed\u0161en\u00ed nevratn\u00fd proces, i kdy\u017e Q = 0?",
         "Proto\u017ee doch\u00e1z\u00ed ke spont\u00e1nn\u00edmu vyrovn\u00e1v\u00e1n\u00ed teplot (a p\u0159\u00edpadn\u011b slo\u017een\u00ed) mezi proudy, "
         "co\u017e je typick\u00fd nevratn\u00fd proces. Entropie soustavy v\u017edy roste \u2014 entropie m\u00ed\u0161en\u00ed "
         "\u0394S_mix = \u2212nR \u03a3 x_i ln x_i > 0, proto\u017ee x_i < 1 a ln x_i < 0."),

        ("Jak experiment\u00e1ln\u011b ur\u010d\u00edte, zda je pro dan\u00fd plyn opr\u00e1vn\u011bn\u00e9 pou\u017e\u00edt model ide\u00e1ln\u00edho plynu?",
         "Spo\u010d\u00edt\u00e1me redukovan\u00e9 veli\u010diny T_r = T/T_k a p_r = p/p_k. Pokud T_r > 2 a p_r < 1, "
         "je model ide\u00e1ln\u00edho plynu dostate\u010dn\u011b p\u0159esn\u00fd (chyba < 1 %). Alternativn\u011b ode\u010dteme Z "
         "z generalizovan\u00e9ho diagramu \u2014 pokud |Z \u2212 1| < 0,01, ide\u00e1ln\u00ed model sta\u010d\u00ed."),
    ])

    # ── Zápatí: Zdroje ──
    doc.add_paragraph()
    doc.add_paragraph("─" * 60)
    add_para(doc, "Zdroje a doporučená literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Çengel, Y.A., Boles, M.A.: Thermodynamics — An Engineering Approach, 9th Ed.")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "Atkins, P., de Paula, J.: Physical Chemistry, 11th Ed.")
    add_bullet(doc, "NIST Chemistry WebBook — kritické konstanty a viriální koeficienty")
    add_bullet(doc, "Perry's Chemical Engineers' Handbook — směšovací pravidla, Z-faktor tabulky", is_last=True)

    # ── Save ──
    save_and_export(doc, "06-realny-plyn-smesi-plynu")


if __name__ == "__main__":
    generate()
