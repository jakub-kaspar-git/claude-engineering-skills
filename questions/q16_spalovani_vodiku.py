# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 16: Statika spalov\u00e1n\u00ed vod\u00edku.
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

def generate_h2_reaction_schema():
    """Schematic of hydrogen combustion reaction."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")

    from matplotlib.patches import FancyBboxPatch

    # Reactants
    r1 = FancyBboxPatch((0.3, 1.2), 2.2, 1.6, boxstyle="round,pad=0.15",
                         facecolor="#DCFCE7", edgecolor="#16A34A", lw=2)
    ax.add_patch(r1)
    ax.text(1.4, 2.3, "2 H\u2082", fontsize=16, ha="center", va="center",
            fontweight="bold", color="#16A34A")
    ax.text(1.4, 1.6, "Vod\u00edk", fontsize=9, ha="center", color="#166534")

    ax.text(3, 2, "+", fontsize=18, ha="center", va="center", fontweight="bold")

    r2 = FancyBboxPatch((3.5, 1.2), 2.2, 1.6, boxstyle="round,pad=0.15",
                         facecolor="#DBEAFE", edgecolor="#2563EB", lw=2)
    ax.add_patch(r2)
    ax.text(4.6, 2.3, "O\u2082", fontsize=16, ha="center", va="center",
            fontweight="bold", color="#2563EB")
    ax.text(4.6, 1.6, "Kysl\u00edk", fontsize=9, ha="center", color="#1E40AF")

    # Arrow
    ax.annotate("", xy=(7.3, 2), xytext=(6.2, 2),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=3))
    ax.text(6.75, 2.8, "Spalov\u00e1n\u00ed", fontsize=10, ha="center", color="#D97706", fontweight="bold")
    ax.text(6.75, 0.8, "Q = 286 kJ/mol", fontsize=9, ha="center", color="#D97706", style="italic")

    # Product
    p1 = FancyBboxPatch((7.5, 1.2), 2.8, 1.6, boxstyle="round,pad=0.15",
                         facecolor="#FEE2E2", edgecolor="#DC2626", lw=2)
    ax.add_patch(p1)
    ax.text(8.9, 2.3, "2 H\u2082O", fontsize=16, ha="center", va="center",
            fontweight="bold", color="#DC2626")
    ax.text(8.9, 1.6, "Vodn\u00ed p\u00e1ra", fontsize=9, ha="center", color="#991B1B")

    fig.suptitle("Stechiometrick\u00e1 rovnice spalov\u00e1n\u00ed vod\u00edku", fontsize=12, fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q16_h2_reaction.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_h2_mass_balance():
    """Sankey-style mass balance for H2 combustion."""
    fig, ax = plt.subplots(figsize=(8, 5))

    categories = ["Vod\u00edk H\u2082\n(palivo)", "Kysl\u00edk O\u2082\n(ze vzduchu)", "Dus\u00edk N\u2082\n(ze vzduchu)",
                  "Vodn\u00ed p\u00e1ra H\u2082O\n(produkt)", "Dus\u00edk N\u2082\n(ve spalin\u00e1ch)"]
    values = [1.0, 8.0, 26.3, 9.0, 26.3]
    colors_bar = [COLORS[2], COLORS[0], "#7C3AED", COLORS[1], "#7C3AED"]

    # Split into inputs and outputs
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    # Inputs
    inputs = ["H\u2082 (palivo)", "O\u2082 (vzduch)", "N\u2082 (vzduch)"]
    in_vals = [1.0, 8.0, 26.3]
    in_colors = [COLORS[2], COLORS[0], "#7C3AED"]
    bars1 = ax1.barh(inputs, in_vals, color=in_colors, edgecolor="white", height=0.5)
    for bar, val in zip(bars1, in_vals):
        ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val:.1f} kg", va="center", fontsize=10, fontweight="bold")
    ax1.set_xlabel("Hmotnost [kg]", fontsize=11)
    ax1.set_title("VSTUPY (na 1 kg H\u2082)", fontsize=12, fontweight="bold")
    ax1.set_xlim(0, 35)
    ax1.invert_yaxis()

    # Outputs
    outputs = ["H\u2082O (spaliny)", "N\u2082 (spaliny)"]
    out_vals = [9.0, 26.3]
    out_colors = [COLORS[1], "#7C3AED"]
    bars2 = ax2.barh(outputs, out_vals, color=out_colors, edgecolor="white", height=0.5)
    for bar, val in zip(bars2, out_vals):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val:.1f} kg", va="center", fontsize=10, fontweight="bold")
    ax2.set_xlabel("Hmotnost [kg]", fontsize=11)
    ax2.set_title("V\u00ddSTUPY (spaliny)", fontsize=12, fontweight="bold")
    ax2.set_xlim(0, 35)
    ax2.invert_yaxis()

    fig.suptitle("Hmotnostn\u00ed bilance spalov\u00e1n\u00ed 1 kg vod\u00edku (stechiomet. se vzduchem)",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q16_h2_balance.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_excess_air_effect():
    """Effect of excess air on flue gas composition for H2 combustion."""
    fig, ax = plt.subplots(figsize=(8, 5))

    n_vals = np.linspace(1.0, 3.0, 100)  # excess air coefficient

    # For 1 kg H2: stoichiometric O2 = 8 kg, N2 = 26.32 kg, H2O = 9 kg
    O2_stoich = 8.0
    N2_stoich = 26.32
    H2O = 9.0

    O2_excess = O2_stoich * (n_vals - 1)
    N2_total = N2_stoich * n_vals
    total = H2O + O2_excess + N2_total

    y_H2O = H2O / total * 100
    y_O2 = O2_excess / total * 100
    y_N2 = N2_total / total * 100

    ax.plot(n_vals, y_H2O, color=COLORS[1], linewidth=2.5, label="H\u2082O [%]")
    ax.plot(n_vals, y_O2, color=COLORS[0], linewidth=2.5, label="O\u2082 [%]")
    ax.plot(n_vals, y_N2, color="#7C3AED", linewidth=2.5, label="N\u2082 [%]")

    ax.axvline(x=1.0, color="gray", linestyle=":", linewidth=1)
    ax.text(1.02, 5, "n = 1\n(stechiomet.)", fontsize=8, color="gray")

    ax.set_xlabel("P\u0159ebytek vzduchu n [-]", fontsize=11)
    ax.set_ylabel("Hmotnostn\u00ed pod\u00edl ve spalin\u00e1ch [%]", fontsize=11)
    ax.set_title("Slo\u017een\u00ed spalin p\u0159i spalov\u00e1n\u00ed H\u2082 v z\u00e1vislosti na p\u0159ebytku vzduchu",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(1, 3)
    ax.set_ylim(0, 85)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q16_excess_air.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH DOKUMENTU
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_reaction = generate_h2_reaction_schema()
    img_balance = generate_h2_mass_balance()
    img_excess = generate_excess_air_effect()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="16. Statika spalov\u00e1n\u00ed vod\u00edku.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Napi\u0161te stechiometrickou rovnici spalov\u00e1n\u00ed vod\u00edku. Vypo\u010dt\u011bte pot\u0159ebn\u00e9 "
        "mno\u017estv\u00ed kysl\u00edku a vzduchu pro sp\u00e1len\u00ed 1 kg vod\u00edku. Ur\u010dete mno\u017estv\u00ed "
        "a slo\u017een\u00ed spalin.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Stechiometrick\u00e1 rovnice", level=3)

    add_image(doc, img_reaction, width_cm=14,
              caption="Obr. 1: Stechiometrick\u00e1 rovnice spalov\u00e1n\u00ed vod\u00edku")

    add_para(doc, "Mol\u00e1rn\u00ed z\u00e1pis:", keep_with_next=True)
    add_equation(doc, r"2\text{H}_2 + \text{O}_2 \rightarrow 2\text{H}_2\text{O}", label="1")

    add_para(doc, "Zjednodu\u0161en\u011b pro 1 mol H\u2082:", keep_with_next=True)
    add_equation(doc, r"\text{H}_2 + \frac{1}{2}\text{O}_2 \rightarrow \text{H}_2\text{O}", label="2")

    add_info_box(doc,
        "Kl\u00ed\u010dov\u00e9 mol\u00e1rn\u00ed hmotnosti",
        "H\u2082: M = 2 g/mol | O\u2082: M = 32 g/mol | H\u2082O: M = 18 g/mol | N\u2082: M = 28 g/mol\n"
        "Vzduch: 21 % O\u2082 + 79 % N\u2082 (objemov\u011b) \u2192 pom\u011br N\u2082/O\u2082 = 79/21 = 3,762")

    # -- 1.2 Hmotnostn\u00ed bilance --
    add_heading(doc, "1.2 Hmotnostn\u00ed bilance na 1 kg H\u2082", level=3)

    add_para(doc, "Z rovnice (2): 1 mol H\u2082 pot\u0159ebuje 0,5 mol O\u2082:", keep_with_next=True)

    add_para(doc, "Pot\u0159eba kysl\u00edku:", bold=True, keep_with_next=True)
    add_equation(doc, r"m_{O_2} = \frac{0{,}5 \times 32}{2} \times 1 = 8 \text{ kg O}_2 \text{ / kg H}_2", label="3")

    add_para(doc, "Pot\u0159eba stechiometrick\u00e9ho vzduchu:", bold=True, keep_with_next=True)
    add_equation(doc, r"m_{vz,min} = \frac{m_{O_2}}{0{,}232} = \frac{8}{0{,}232} = 34{,}48 \text{ kg vzduchu / kg H}_2", label="4")

    add_para(doc, "kde 0,232 je hmotnostn\u00ed pod\u00edl O\u2082 ve vzduchu (23,2 %).", keep_with_next=True)

    add_para(doc, "Objemov\u011b (p\u0159i norm\u00e1ln\u00edch podm\u00ednk\u00e1ch):", bold=True, keep_with_next=True)
    add_equation(doc, r"V_{O_2,min} = \frac{0{,}5}{1} \times 22{,}414 = \frac{0{,}5 \times 22{,}414}{2/M_{H_2}}", label="5")

    add_para(doc, "Zjednodu\u0161en\u011b pro 1 kg H\u2082 (500 mol):", keep_with_next=True)
    add_equation(doc, r"V_{O_2,min} = 500 \times 0{,}5 \times 22{,}414 \times 10^{-3} = 5{,}6 \text{ m}^3_N \text{ / kg H}_2")
    add_equation(doc, r"V_{vz,min} = \frac{V_{O_2,min}}{0{,}21} = \frac{5{,}6}{0{,}21} = 26{,}67 \text{ m}^3_N \text{ / kg H}_2", label="6")

    # -- 1.3 Mno\u017estv\u00ed spalin --
    add_page_break(doc)
    add_heading(doc, "1.3 Mno\u017estv\u00ed a slo\u017een\u00ed spalin", level=3)

    add_para(doc, "Produkt spalov\u00e1n\u00ed: vodn\u00ed p\u00e1ra H\u2082O:", keep_with_next=True)
    add_equation(doc, r"m_{H_2O} = \frac{1 \times 18}{2} = 9 \text{ kg H}_2\text{O / kg H}_2", label="7")

    add_para(doc, "Dus\u00edk ze vzduchu (proch\u00e1z\u00ed beze zm\u011bny):", keep_with_next=True)
    add_equation(doc, r"m_{N_2} = m_{vz,min} - m_{O_2} = 34{,}48 - 8{,}0 = 26{,}48 \text{ kg N}_2 \text{ / kg H}_2", label="8")

    add_para(doc, "Celkov\u00e9 mno\u017estv\u00ed spalin (stechiometrick\u00e9):", keep_with_next=True)
    add_equation(doc, r"m_{sp,min} = m_{H_2O} + m_{N_2} = 9{,}0 + 26{,}48 = 35{,}48 \text{ kg / kg H}_2", label="9")

    add_image(doc, img_balance, width_cm=14,
              caption="Obr. 2: Hmotnostn\u00ed bilance spalov\u00e1n\u00ed 1 kg vod\u00edku se stechiometrick\u00fdm vzduchem")

    add_warning_box(doc,
        "Spaliny z vod\u00edku neobsahuj\u00ed CO\u2082! Jedin\u00fdm produktem (krom\u011b N\u2082 ze vzduchu) "
        "je vodn\u00ed p\u00e1ra. Proto je vod\u00edk pova\u017eov\u00e1n za bezemisn\u00ed palivo (z hlediska CO\u2082).")

    # -- 1.4 P\u0159ebytek vzduchu --
    add_heading(doc, "1.4 Spalov\u00e1n\u00ed s p\u0159ebytkem vzduchu", level=3)

    add_para(doc, "Skute\u010dn\u00e9 mno\u017estv\u00ed vzduchu p\u0159i p\u0159ebytku n:", keep_with_next=True)
    add_equation(doc, r"m_{vz} = n \cdot m_{vz,min}", label="10")

    add_para(doc, "Slo\u017een\u00ed spalin p\u0159i p\u0159ebytku vzduchu:", keep_with_next=True)
    add_equation(doc, r"m_{sp} = m_{H_2O} + m_{N_2} \cdot n + m_{O_2}(n - 1)", label="11")

    add_para(doc,
        "Ve spalin\u00e1ch se objev\u00ed p\u0159ebyte\u010dn\u00fd kysl\u00edk O\u2082 a dal\u0161\u00ed dus\u00edk N\u2082.")

    add_image(doc, img_excess, width_cm=13,
              caption="Obr. 3: Slo\u017een\u00ed spalin v z\u00e1vislosti na p\u0159ebytku vzduchu")

    # -- 1.5 Objemov\u00e1 bilance --
    add_page_break(doc)
    add_heading(doc, "1.5 Objemov\u00e1 bilance (norm\u00e1ln\u00ed podm\u00ednky)", level=3)

    add_styled_table(doc,
        headers=["Veli\u010dina", "Hmotnostn\u011b [kg/kg H\u2082]", "Objemov\u011b [m\u00b3_N/kg H\u2082]"],
        data=[
            ["O\u2082 pot\u0159eba (min)", "8,00", "5,60"],
            ["Vzduch (min)", "34,48", "26,67"],
            ["H\u2082O (produkt)", "9,00", "11,20"],
            ["N\u2082 (ve spalin\u00e1ch)", "26,48", "21,15"],
            ["Spaliny (min)", "35,48", "32,35"],
        ],
    )

    add_info_box(doc,
        "Kontrola: z\u00e1kon zachov\u00e1n\u00ed hmotnosti",
        "Vstupy: 1,0 (H\u2082) + 34,48 (vzduch) = 35,48 kg\n"
        "V\u00fdstupy: 9,0 (H\u2082O) + 26,48 (N\u2082) = 35,48 kg \u2714")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Vod\u00edk jako palivo", level=3)
    add_bullet(doc, "Nejvy\u0161\u0161\u00ed v\u00fdh\u0159evnost na kg (120 MJ/kg), ale nejni\u017e\u0161\u00ed hustota")
    add_bullet(doc, "Bezemisn\u00ed spalov\u00e1n\u00ed (produkt jen H\u2082O)")
    add_bullet(doc, "Velmi \u0161irok\u00e9 meze v\u00fdbu\u0161nosti (4\u201375 % obj. ve vzduchu)")
    add_bullet(doc, "Vysok\u00e1 rychlost ho\u0159en\u00ed, n\u00edzk\u00e1 z\u00e1paln\u00e1 energie")
    add_bullet(doc, "Skladov\u00e1n\u00ed: vysok\u00fd tlak (350\u2013700 bar), zkapaln\u011bn\u00ed (\u221225 3\u00b0C), hydridy kov\u016f", is_last=True)

    add_heading(doc, "2.2 Emise NOx", level=3)
    add_para(doc,
        "P\u0159esto\u017ee spalov\u00e1n\u00ed H\u2082 nevytv\u00e1\u0159\u00ed CO\u2082, p\u0159i vysok\u00fdch teplot\u00e1ch "
        "(> 1500 \u00b0C) vznik\u00e1 termick\u00fd NOx z dus\u00edku vzduchu. "
        "Sni\u017eov\u00e1n\u00ed: chud\u00e9 sm\u011bsi (n >> 1), vstrikování vody, DLN ho\u0159\u00e1ky.")

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Spalov\u00e1n\u00ed H\u2082 s 20 % p\u0159ebytkem vzduchu", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Spo\u010dt\u011bte mno\u017estv\u00ed vzduchu a slo\u017een\u00ed spalin p\u0159i spalov\u00e1n\u00ed "
        "1 kg vod\u00edku s p\u0159ebytkem vzduchu n = 1,2.", bold=True)

    add_para(doc, "Krok 1: Skute\u010dn\u00e9 mno\u017estv\u00ed vzduchu", bold=True)
    add_equation(doc, r"m_{vz} = n \cdot m_{vz,min} = 1{,}2 \times 34{,}48 = 41{,}38 \text{ kg}")

    add_para(doc, "Krok 2: Slo\u017een\u00ed spalin", bold=True)
    add_equation(doc, r"m_{H_2O} = 9{,}0 \text{ kg (nem\u011bn\u00ed se)}")
    add_equation(doc, r"m_{N_2} = 26{,}48 \times 1{,}2 = 31{,}78 \text{ kg}")
    add_equation(doc, r"m_{O_2,p\v{r}eb} = 8{,}0 \times (1{,}2 - 1) = 1{,}60 \text{ kg}")
    add_equation(doc, r"m_{sp} = 9{,}0 + 31{,}78 + 1{,}60 = 42{,}38 \text{ kg}")

    add_para(doc, "Krok 3: Hmotnostn\u00ed pod\u00edly ve spalin\u00e1ch", bold=True)
    add_styled_table(doc,
        headers=["Slo\u017eka", "Hmotnost [kg]", "Pod\u00edl [%]"],
        data=[
            ["H\u2082O", "9,00", "21,2"],
            ["N\u2082", "31,78", "75,0"],
            ["O\u2082", "1,60", "3,8"],
            ["Celkem", "42,38", "100,0"],
        ],
    )

    add_info_box(doc,
        "V\u00fdsledky:",
        "Pot\u0159eba vzduchu: 41,38 kg / kg H\u2082 (p\u0159i n = 1,2)\n"
        "Spaliny: 42,38 kg / kg H\u2082\n"
        "Ve spalin\u00e1ch: 21,2 % H\u2082O, 75,0 % N\u2082, 3,8 % O\u2082\n"
        "\u017d\u00e1dn\u00e9 CO\u2082!")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Jak\u00e9 jsou produkty spalov\u00e1n\u00ed vod\u00edku a pro\u010d je H\u2082 bezemisn\u00ed palivo?",
         "Jedin\u00fdm produktem spalov\u00e1n\u00ed je vodn\u00ed p\u00e1ra H\u2082O (a N\u2082 ze vzduchu). "
         "Nevznik\u00e1 CO\u2082 ani tuh\u00e9 \u010d\u00e1stice. Proto je H\u2082 pova\u017eov\u00e1n za bezemisn\u00ed \u2014 "
         "ov\u0161em pouze z hlediska spalov\u00e1n\u00ed, ne v\u00fdroby (zelen\u00fd vs. \u0161ed\u00fd H\u2082)."),

        ("Kolik kg vzduchu pot\u0159ebujete na sp\u00e1len\u00ed 1 kg H\u2082?",
         "Stechiometricky 34,48 kg (8 kg O\u2082 + 26,48 kg N\u2082). "
         "To je velmi mnoho ve srovn\u00e1n\u00ed s uhl\u00edm (~11 kg/kg) nebo zemn\u00edm plynem (~17 kg/kg), "
         "proto\u017ee H\u2082 m\u00e1 nejvy\u0161\u0161\u00ed v\u00fdh\u0159evnost na kg."),

        ("Pro\u010d p\u0159i spalov\u00e1n\u00ed H\u2082 vznik\u00e1 9 kg vody na 1 kg paliva?",
         "Z rovnice H\u2082 + 0,5 O\u2082 \u2192 H\u2082O: pom\u011br M_{H\u2082O}/M_{H\u2082} = 18/2 = 9. "
         "Ka\u017ed\u00fd kg vod\u00edku v\u00e1\u017ee 8 kg kysl\u00edku a vytvo\u0159\u00ed 9 kg vody. "
         "Proto je rozd\u00edl Q\u209b \u2212 Q\u1d62 u H\u2082 tak velk\u00fd (22 MJ/kg kondenza\u010dn\u00edho tepla)."),

        ("Pro\u010d vznik\u00e1 NOx i p\u0159i spalov\u00e1n\u00ed \u010dist\u00e9ho H\u2082?",
         "Termick\u00fd NOx vznik\u00e1 z dus\u00edku a kysl\u00edku ve vzduchu p\u0159i T > 1500 \u00b0C "
         "(Zeldovi\u010d\u016fv mechanismus). Vod\u00edk ho\u0159\u00ed s velmi vysokou teplotou plamene "
         "(~2100 \u00b0C), co\u017e tvorbu NOx zvy\u0161uje. \u0158e\u0161en\u00ed: chud\u00e9 sm\u011bsi, DLN ho\u0159\u00e1ky."),

        ("Vysv\u011btlete pojem stechiometrick\u00e9ho vzduchu.",
         "Minim\u00e1ln\u00ed mno\u017estv\u00ed vzduchu pot\u0159ebn\u00e9 pro \u00fapln\u00e9 sp\u00e1len\u00ed paliva "
         "(\u017e\u00e1dn\u00fd zbytek O\u2082 ve spalin\u00e1ch). V praxi se spaluje s p\u0159ebytkem (n > 1), "
         "proto\u017ee p\u0159i n = 1 by nedokonalost m\u00edsen\u00ed vedla k nedokonalému sp\u00e1len\u00ed."),

        ("Pro\u010d m\u00e1 vod\u00edk tak \u0161irok\u00e9 meze v\u00fdbu\u0161nosti (4\u201375 %)?",
         "Mal\u00e1 molekula H\u2082 m\u00e1 vysokou difuzivitu a n\u00edzkou z\u00e1palnou energii. "
         "Rychlost \u0161\u00ed\u0159en\u00ed plamene je 8\u00d7 vy\u0161\u0161\u00ed ne\u017e u metanu. "
         "D\u00edky tomu ho\u0159\u00ed i velmi chud\u00e9 (4 %) i velmi bohat\u00e9 (75 %) sm\u011bsi, "
         "co\u017e klade vysok\u00e9 n\u00e1roky na bezpe\u010dnost."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M. a kol.: Spalov\u00e1n\u00ed a spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "Turns, S.R.: An Introduction to Combustion, 3rd Ed.")
    add_bullet(doc, "IEA Hydrogen Reports \u2014 vod\u00edkov\u00e9 technologie")
    add_bullet(doc, "\u010cSN EN 14522 \u2014 Teploty samovzn\u00edcen\u00ed plyn\u016f a par", is_last=True)

    save_and_export(doc, "16-spalovani-vodiku")


if __name__ == "__main__":
    generate()
