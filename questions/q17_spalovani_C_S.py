# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 17: Statika spalov\u00e1n\u00ed uhl\u00edku a s\u00edry.
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

def generate_c_reactions():
    """Comparison of complete vs incomplete combustion of carbon."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))

    from matplotlib.patches import FancyBboxPatch

    for ax, title, eq, products, energy, color, y_label in [
        (ax1, "\u00daPLN\u00c9 spalov\u00e1n\u00ed (dostatek O\u2082)",
         "C + O\u2082 \u2192 CO\u2082", "CO\u2082", "393,5 kJ/mol (32,8 MJ/kg C)", "#16A34A", "Q = 32,8 MJ/kg"),
        (ax2, "NE\u00daPLN\u00c9 spalov\u00e1n\u00ed (nedostatek O\u2082)",
         "2C + O\u2082 \u2192 2CO", "CO (jedovat\u00fd!)", "110,5 kJ/mol (9,2 MJ/kg C)", "#DC2626", "Q = 9,2 MJ/kg"),
    ]:
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 2)
        ax.axis("off")

        # Title
        ax.text(0.2, 1.5, title, fontsize=10, fontweight="bold", color=color, va="center")

        # Equation box
        box = FancyBboxPatch((0.2, 0.3), 5, 0.9, boxstyle="round,pad=0.15",
                              facecolor="white", edgecolor=color, lw=2)
        ax.add_patch(box)
        ax.text(2.7, 0.75, eq, fontsize=14, ha="center", va="center", fontweight="bold", color=color)

        # Energy
        ebox = FancyBboxPatch((6, 0.3), 5.5, 0.9, boxstyle="round,pad=0.15",
                               facecolor="#FEF3C7", edgecolor="#D97706", lw=1.5)
        ax.add_patch(ebox)
        ax.text(8.75, 0.75, y_label, fontsize=11, ha="center", va="center",
                fontweight="bold", color="#D97706")

    fig.suptitle("Spalov\u00e1n\u00ed uhl\u00edku: \u00fapln\u00e9 vs. ne\u00fapln\u00e9", fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q17_c_reactions.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_combustion_comparison():
    """Bar chart comparing O2 needs and products for C, H, S combustion."""
    fig, ax = plt.subplots(figsize=(9, 5))

    elements = ["C \u2192 CO\u2082", "H\u2082 \u2192 H\u2082O", "S \u2192 SO\u2082"]
    O2_need = [2.67, 8.0, 1.0]  # kg O2 per kg element
    product = [3.67, 9.0, 2.0]  # kg product per kg element
    Q_vals = [32.8, 120.0, 9.3]  # MJ/kg

    x = np.arange(len(elements))
    w = 0.25

    ax.bar(x - w, O2_need, w, label="Pot\u0159eba O\u2082 [kg/kg]", color=COLORS[0])
    ax.bar(x, product, w, label="Produkt [kg/kg]", color=COLORS[1])
    ax.bar(x + w, [q/10 for q in Q_vals], w, label="V\u00fdh\u0159evnost [MJ/kg] / 10", color=COLORS[3])

    # Values on bars
    for i, (o, p, q) in enumerate(zip(O2_need, product, Q_vals)):
        ax.text(i - w, o + 0.15, f"{o:.2f}", ha="center", fontsize=8, fontweight="bold")
        ax.text(i, p + 0.15, f"{p:.2f}", ha="center", fontsize=8, fontweight="bold")
        ax.text(i + w, q/10 + 0.15, f"{q:.1f}", ha="center", fontsize=8, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(elements, fontsize=11)
    ax.set_ylabel("Hodnota [kg/kg nebo MJ/kg/10]", fontsize=10)
    ax.set_title("Porovn\u00e1n\u00ed spalov\u00e1n\u00ed C, H\u2082 a S", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q17_comparison.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_c = generate_c_reactions()
    img_cmp = generate_combustion_comparison()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="17. Statika spalov\u00e1n\u00ed uhl\u00edku a s\u00edry.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Napi\u0161te stechiometrick\u00e9 rovnice spalov\u00e1n\u00ed uhl\u00edku (\u00fapln\u00e9ho a ne\u00fapln\u00e9ho) "
        "a s\u00edry. Vypo\u010dt\u011bte pot\u0159ebn\u00e9 mno\u017estv\u00ed kysl\u00edku a mno\u017estv\u00ed produkt\u016f "
        "na 1 kg prvku.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    # -- 1.1 Uhlik --
    add_heading(doc, "1.1 Spalov\u00e1n\u00ed uhl\u00edku", level=3)

    add_para(doc, "a) \u00dapln\u00e9 spalov\u00e1n\u00ed (dostatek kysl\u00edku):", bold=True, keep_with_next=True)
    add_equation(doc, r"\text{C} + \text{O}_2 \rightarrow \text{CO}_2 + 393{,}5 \text{ kJ/mol}", label="1")

    add_para(doc, "Hmotnostn\u00ed bilance na 1 kg C:", keep_with_next=True)
    add_equation(doc, r"m_{O_2} = \frac{M_{O_2}}{M_C} = \frac{32}{12} = 2{,}667 \text{ kg O}_2 / \text{kg C}", label="2")
    add_equation(doc, r"m_{CO_2} = \frac{M_{CO_2}}{M_C} = \frac{44}{12} = 3{,}667 \text{ kg CO}_2 / \text{kg C}", label="3")

    add_para(doc, "b) Ne\u00fapln\u00e9 spalov\u00e1n\u00ed (nedostatek kysl\u00edku):", bold=True, keep_with_next=True)
    add_equation(doc, r"2\text{C} + \text{O}_2 \rightarrow 2\text{CO} + 221 \text{ kJ}", label="4")

    add_para(doc, "Na 1 kg C:", keep_with_next=True)
    add_equation(doc, r"m_{O_2} = \frac{16}{12} = 1{,}333 \text{ kg O}_2 / \text{kg C}", label="5")
    add_equation(doc, r"m_{CO} = \frac{28}{12} = 2{,}333 \text{ kg CO / kg C}", label="6")

    add_image(doc, img_c, width_cm=14,
              caption="Obr. 1: \u00dapln\u00e9 vs. ne\u00fapln\u00e9 spalov\u00e1n\u00ed uhl\u00edku \u2014 rozd\u00edl v energii a produktech")

    add_warning_box(doc,
        "Ne\u00fapln\u00e9 spalov\u00e1n\u00ed (C \u2192 CO) uvoln\u00ed pouze 28 % energie \u00fapln\u00e9ho spalov\u00e1n\u00ed "
        "a vytv\u00e1\u0159\u00ed jedovat\u00fd oxid uhelnat\u00fd CO. V praxi je ne\u017e\u00e1douc\u00ed \u2014 "
        "zaji\u0161\u0165uje se dostate\u010dn\u00fd p\u0159\u00edsun vzduchu a dobr\u00e9 prom\u00edch\u00e1n\u00ed.")

    add_para(doc, "Doho\u0159\u00edv\u00e1n\u00ed CO:", bold=True, keep_with_next=True)
    add_equation(doc, r"2\text{CO} + \text{O}_2 \rightarrow 2\text{CO}_2 + 566 \text{ kJ}", label="7")
    add_para(doc, "Celkov\u00e1 energie: 221 + 566 = 787 kJ (= 2 \u00d7 393,5 kJ) \u2014 z\u00e1kon zachov\u00e1n\u00ed energie.")

    # -- 1.2 Sira --
    add_page_break(doc)
    add_heading(doc, "1.2 Spalov\u00e1n\u00ed s\u00edry", level=3)

    add_equation(doc, r"\text{S} + \text{O}_2 \rightarrow \text{SO}_2 + 297 \text{ kJ/mol}", label="8")

    add_para(doc, "Na 1 kg S:", keep_with_next=True)
    add_equation(doc, r"m_{O_2} = \frac{32}{32} = 1{,}000 \text{ kg O}_2 / \text{kg S}", label="9")
    add_equation(doc, r"m_{SO_2} = \frac{64}{32} = 2{,}000 \text{ kg SO}_2 / \text{kg S}", label="10")

    add_para(doc, "\u010c\u00e1ste\u010dn\u00e1 oxidace na SO\u2083 (katalyticky, v kotl\u00edch ~1\u20135 %):", keep_with_next=True)
    add_equation(doc, r"2\text{SO}_2 + \text{O}_2 \rightleftharpoons 2\text{SO}_3", label="11")

    add_warning_box(doc,
        "SO\u2082 a SO\u2083 jsou hlavn\u00ed p\u0159\u00ed\u010dinou kysel\u00fdch de\u0161\u0165\u016f a koroze spalinov\u00fdch cest. "
        "SO\u2083 s vodou tvo\u0159\u00ed H\u2082SO\u2084 \u2014 kyselinov\u00fd rosn\u00fd bod spalin m\u016f\u017ee b\u00fdt a\u017e 150 \u00b0C! "
        "Odsi\u0159ov\u00e1n\u00ed: v\u00e1pencov\u00e1 vyp\u00edrka, such\u00e9 metody.")

    # -- 1.3 Souhrn --
    add_heading(doc, "1.3 Souhrnná tabulka", level=3)

    add_styled_table(doc,
        headers=["Reakce", "O\u2082 [kg/kg]", "Produkt [kg/kg]", "Q [MJ/kg]", "Q [kJ/mol]"],
        data=[
            ["C + O\u2082 \u2192 CO\u2082", "2,667", "3,667 CO\u2082", "32,8", "393,5"],
            ["2C + O\u2082 \u2192 2CO", "1,333", "2,333 CO", "9,2", "110,5"],
            ["S + O\u2082 \u2192 SO\u2082", "1,000", "2,000 SO\u2082", "9,3", "297"],
            ["H\u2082 + 0,5O\u2082 \u2192 H\u2082O", "8,000", "9,000 H\u2082O", "120,0", "242"],
        ],
    )

    add_image(doc, img_cmp, width_cm=13,
              caption="Obr. 2: Porovn\u00e1n\u00ed pot\u0159eby O\u2082 a produkt\u016f p\u0159i spalov\u00e1n\u00ed C, H\u2082 a S")

    # -- 1.4 Objemova bilance --
    add_page_break(doc)
    add_heading(doc, "1.4 Objemov\u00e1 bilance (norm\u00e1ln\u00ed podm\u00ednky)", level=3)

    add_para(doc, "\u00dapln\u00e9 spalov\u00e1n\u00ed uhl\u00edku:", bold=True, keep_with_next=True)
    add_equation(doc, r"V_{O_2} = \frac{1}{12} \times 22{,}414 = 1{,}868 \text{ m}^3_N / \text{kg C}", label="12")
    add_equation(doc, r"V_{CO_2} = \frac{1}{12} \times 22{,}414 = 1{,}868 \text{ m}^3_N / \text{kg C}", label="13")
    add_para(doc, "Pozn.: V_{O\u2082} = V_{CO\u2082} \u2014 1 mol plynu nahrad\u00ed 1 mol (objem se nem\u011bn\u00ed).")

    add_para(doc, "Spalov\u00e1n\u00ed s\u00edry:", bold=True, keep_with_next=True)
    add_equation(doc, r"V_{O_2} = \frac{1}{32} \times 22{,}414 = 0{,}700 \text{ m}^3_N / \text{kg S}", label="14")
    add_equation(doc, r"V_{SO_2} = \frac{1}{32} \times 22{,}414 = 0{,}700 \text{ m}^3_N / \text{kg S}", label="15")

    add_info_box(doc,
        "Obecn\u00fd vzorec pro pot\u0159ebu O\u2082",
        "Pro spalov\u00e1n\u00ed 1 kg prvku X s molovou hmotnost\u00ed M_X, kde na 1 mol X "
        "p\u0159ipad\u00e1 n mol O\u2082:\n"
        "m_{O\u2082} = n \u00d7 32 / M_X [kg/kg]\n"
        "V_{O\u2082} = n \u00d7 22,414 / M_X [m\u00b3_N/kg]")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 V\u00fdznam ne\u00fapln\u00e9ho spalov\u00e1n\u00ed", level=3)
    add_bullet(doc, "Ztráta chemick\u00fdm nedop\u00e1lem (CO ve spalin\u00e1ch) \u2014 a\u017e 72 % energie C je ztracena")
    add_bullet(doc, "CO je jedovat\u00fd (limit: 26 ppm pro 8h expozici)")
    add_bullet(doc, "Indik\u00e1tor \u0161patn\u00e9ho spalov\u00e1n\u00ed \u2014 m\u011b\u0159en\u00ed CO ve spalin\u00e1ch je z\u00e1kladn\u00ed diagnostika")
    add_bullet(doc, "P\u0159\u00ed\u010diny: nedostatek vzduchu, \u0161patn\u00e9 m\u00edsen\u00ed, n\u00edzk\u00e1 teplota, kr\u00e1tk\u00fd pobyt", is_last=True)

    add_heading(doc, "2.2 V\u00fdznam s\u00edry v palivu", level=3)
    add_styled_table(doc,
        headers=["Probl\u00e9m", "P\u0159\u00ed\u010dina", "\u0158e\u0161en\u00ed"],
        data=[
            ["Kysel\u00e9 de\u0161t\u011b", "SO\u2082 + H\u2082O \u2192 H\u2082SO\u2083", "Odsi\u0159ov\u00e1n\u00ed spalin (FGD)"],
            ["N\u00edzkoteplotn\u00ed koroze", "SO\u2083 + H\u2082O \u2192 H\u2082SO\u2084 (rosn\u00fd bod)", "Vy\u0161\u0161\u00ed T spalin na v\u00fdstupu"],
            ["Emise", "Limit SO\u2082: 200 mg/m\u00b3_N (velk\u00e9 zdroje)", "V\u00e1pencov\u00e1 vyp\u00edrka, such\u00e9 metody"],
        ],
    )

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Spalov\u00e1n\u00ed uhl\u00edku se vzduchem", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Spo\u010dt\u011bte mno\u017estv\u00ed vzduchu a spalin p\u0159i \u00fapln\u00e9m sp\u00e1len\u00ed "
        "1 kg \u010dist\u00e9ho uhl\u00edku se stechiometrick\u00fdm vzduchem.", bold=True)

    add_para(doc, "Krok 1: Pot\u0159eba O\u2082 a vzduchu", bold=True)
    add_equation(doc, r"m_{O_2} = 2{,}667 \text{ kg}")
    add_equation(doc, r"m_{vz,min} = \frac{2{,}667}{0{,}232} = 11{,}50 \text{ kg vzduchu}")

    add_para(doc, "Krok 2: Spaliny", bold=True)
    add_equation(doc, r"m_{CO_2} = 3{,}667 \text{ kg}")
    add_equation(doc, r"m_{N_2} = 11{,}50 - 2{,}667 = 8{,}833 \text{ kg}")
    add_equation(doc, r"m_{sp,min} = 3{,}667 + 8{,}833 = 12{,}50 \text{ kg}")

    add_para(doc, "Krok 3: Kontrola bilance", bold=True)
    add_equation(doc, r"1{,}0 + 11{,}50 = 12{,}50 \quad \checkmark")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Na 1 kg C: 11,50 kg vzduchu, 12,50 kg spalin\n"
        "Slo\u017een\u00ed spalin: 29,3 % CO\u2082, 70,7 % N\u2082 (hmotnostn\u011b)\n"
        "Objemov\u011b: 21 % CO\u2082, 79 % N\u2082 (proto\u017ee V_{CO\u2082} = V_{O\u2082})")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Jak\u00fd je rozd\u00edl mezi \u00fapln\u00fdm a ne\u00fapln\u00fdm spalov\u00e1n\u00edm uhl\u00edku?",
         "\u00dapln\u00e9: C + O\u2082 \u2192 CO\u2082, uvoln\u00ed 32,8 MJ/kg. Ne\u00fapln\u00e9: 2C + O\u2082 \u2192 2CO, "
         "uvoln\u00ed jen 9,2 MJ/kg (28 %). Rozd\u00edl v energii p\u0159edstavuje ztrátu "
         "chemick\u00fdm nedop\u00e1lem. CO je nav\u00edc jedovat\u00fd a v\u00fdbu\u0161n\u00fd."),

        ("Pro\u010d p\u0159i \u00fapln\u00e9m spalov\u00e1n\u00ed C plat\u00ed V_{O\u2082} = V_{CO\u2082}?",
         "Z rovnice C + O\u2082 \u2192 CO\u2082: 1 mol O\u2082 se spot\u0159ebuje a vznikne 1 mol CO\u2082. "
         "Podle Avogadrova z\u00e1kona maj\u00ed stejn\u00e9 mno\u017estv\u00ed mol\u016f plyn\u016f stejn\u00fd objem "
         "p\u0159i stejn\u00fdch podm\u00ednk\u00e1ch. Proto se celkov\u00fd objem spalin nem\u011bn\u00ed (p\u0159i such\u00fdch spalin\u00e1ch)."),

        ("Pro\u010d je spalov\u00e1n\u00ed s\u00edry v palivech ne\u017e\u00e1douc\u00ed?",
         "V\u00fdh\u0159evnost s\u00edry je n\u00edzk\u00e1 (9,3 MJ/kg). Produkty SO\u2082/SO\u2083 zp\u016fsobuj\u00ed "
         "kysel\u00e9 de\u0161t\u011b, n\u00edzkoteplotn\u00ed korozi (H\u2082SO\u2084 na st\u011bn\u00e1ch spalinov\u00fdch cest) "
         "a vy\u017eaduj\u00ed n\u00e1kladn\u00e9 odsi\u0159ov\u00e1n\u00ed."),

        ("Kolik kg O\u2082 pot\u0159ebujete na sp\u00e1len\u00ed 1 kg C, H\u2082 a S?",
         "C: 2,667 kg O\u2082 (32/12). H\u2082: 8,000 kg O\u2082 (16/2). S: 1,000 kg O\u2082 (32/32). "
         "Vod\u00edk pot\u0159ebuje nejv\u00edce O\u2082 na kg, proto\u017ee m\u00e1 nejvy\u0161\u0161\u00ed v\u00fdh\u0159evnost."),

        ("Co je chemick\u00fd nedop\u00e1l a jak se m\u011b\u0159\u00ed?",
         "Ztráta energie v d\u016fsledku ne\u00fapln\u00e9ho sp\u00e1len\u00ed \u2014 p\u0159\u00edtomnost CO (a nespálen\u00fdch "
         "uhlovod\u00edk\u016f) ve spalin\u00e1ch. M\u011b\u0159\u00ed se analyzátory spalin (NDIR pro CO, "
         "FID pro uhlovod\u00edky). Typick\u00e9 hodnoty: CO < 100 ppm u dobr\u00e9ho spalov\u00e1n\u00ed."),

        ("Vysv\u011btlete kyselinov\u00fd rosn\u00fd bod spalin.",
         "Teplota, p\u0159i kter\u00e9 kondenzuje H\u2082SO\u2084 ze SO\u2083 a H\u2082O ve spalin\u00e1ch. "
         "Le\u017e\u00ed v rozmez\u00ed 90\u2013150 \u00b0C (z\u00e1vis\u00ed na obsahu S v palivu). "
         "Teplota spalin na v\u00fdstupu z kotle mus\u00ed b\u00fdt vy\u0161\u0161\u00ed, jinak hroz\u00ed koroze \u2014 "
         "to omezuje vyu\u017eit\u00ed tepla a sni\u017euje \u00fa\u010dinnost."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M. a kol.: Spalov\u00e1n\u00ed a spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "Turns, S.R.: An Introduction to Combustion")
    add_bullet(doc, "Glassman, I., Yetter, R.A.: Combustion, 5th Ed.")
    add_bullet(doc, "\u010cSN EN 14792 \u2014 Stanoven\u00ed NOx, SO\u2082 ve spalin\u00e1ch", is_last=True)

    save_and_export(doc, "17-spalovani-C-S")


if __name__ == "__main__":
    generate()
