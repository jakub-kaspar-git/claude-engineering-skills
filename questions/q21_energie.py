# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 21: Energie (pojem, v\u00fdznam, jednotky, zdroje na Zemi).
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

def generate_energy_sources_pie():
    """World primary energy mix."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # World
    labels_w = ["Ropa", "Zemn\u00ed plyn", "Uhl\u00ed", "Jadern\u00e1", "Vodn\u00ed", "OZE\n(sol.,v\u00edtr,bio)"]
    vals_w = [31, 24, 27, 4, 7, 7]
    colors_w = ["#1E40AF", COLORS[2], "#555", "#7C3AED", COLORS[0], COLORS[2]]
    ax1.pie(vals_w, labels=labels_w, autopct="%1.0f%%", colors=colors_w, startangle=90,
            textprops={"fontsize": 9})
    ax1.set_title("SV\u011aT (2023)", fontsize=12, fontweight="bold")

    # Czech Republic
    labels_cz = ["Uhl\u00ed", "Jadern\u00e1", "Zemn\u00ed plyn", "Ropa", "OZE", "Ostatn\u00ed"]
    vals_cz = [35, 19, 17, 18, 8, 3]
    colors_cz = ["#555", "#7C3AED", COLORS[2], "#1E40AF", COLORS[2], "gray"]
    ax2.pie(vals_cz, labels=labels_cz, autopct="%1.0f%%", colors=colors_cz, startangle=90,
            textprops={"fontsize": 9})
    ax2.set_title("\u010cESK\u00c1 REPUBLIKA (2023)", fontsize=12, fontweight="bold")

    fig.suptitle("Prim\u00e1rn\u00ed energetick\u00fd mix", fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q21_energy_mix.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_energy_forms():
    """Diagram of energy forms and conversions."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    from matplotlib.patches import FancyBboxPatch

    forms = [
        (1, 5, "Kinetick\u00e1\n$E_k = \\frac{1}{2}mv^2$", "#DC2626"),
        (5, 5, "Potenci\u00e1ln\u00ed\n$E_p = mgh$", "#2563EB"),
        (9, 5, "Tepeln\u00e1\n$Q = mc\\Delta T$", "#D97706"),
        (1, 2, "Elektrick\u00e1\n$W = UIt$", "#16A34A"),
        (5, 2, "Chemick\u00e1\n(paliva, baterie)", "#7C3AED"),
        (9, 2, "Jadern\u00e1\n$E = mc^2$", "#DC2626"),
    ]

    for x, y, label, color in forms:
        box = FancyBboxPatch((x - 1.2, y - 0.8), 2.4, 1.6, boxstyle="round,pad=0.15",
                              facecolor="white", edgecolor=color, lw=2)
        ax.add_patch(box)
        ax.text(x, y, label, ha="center", va="center", fontsize=9, fontweight="bold", color=color)

    # Central label
    ax.text(5, 3.7, "P\u0158EM\u011aNY ENERGIE\n(z\u00e1kon zachov\u00e1n\u00ed)", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#555",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF3C7", edgecolor="#D97706"))

    # Arrows between forms
    for x1, y1, x2, y2 in [(2.2, 5, 3.8, 5), (6.2, 5, 7.8, 5), (2.2, 2, 3.8, 2),
                            (6.2, 2, 7.8, 2), (1, 4.2, 1, 2.8), (9, 4.2, 9, 2.8)]:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<->", color="gray", lw=1, alpha=0.5))

    fig.suptitle("Formy energie a jejich p\u0159em\u011bny", fontsize=13, fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q21_energy_forms.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_reserves_chart():
    """Estimated reserves of fossil fuels in years."""
    fig, ax = plt.subplots(figsize=(7, 4))

    resources = ["Ropa", "Zemn\u00ed plyn", "Uhl\u00ed", "Uran"]
    years = [50, 55, 130, 80]
    colors_bar = ["#1E40AF", COLORS[2], "#555", "#7C3AED"]

    bars = ax.bar(resources, years, color=colors_bar, edgecolor="white", width=0.5)
    for bar, val in zip(bars, years):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                f"~{val} let", ha="center", fontsize=11, fontweight="bold")

    ax.set_ylabel("Odhadovan\u00e1 \u017eivotnost z\u00e1sob [roky]", fontsize=11)
    ax.set_title("Odhadovan\u00e9 z\u00e1soby neobnoviteln\u00fdch zdroj\u016f\n(p\u0159i sou\u010dasn\u00e9 spot\u0159eb\u011b)",
                 fontsize=12, fontweight="bold")
    ax.set_ylim(0, 160)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q21_reserves.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_mix = generate_energy_sources_pie()
    img_forms = generate_energy_forms()
    img_res = generate_reserves_chart()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="21. Energie (pojem, v\u00fdznam, jednotky, zdroje na Zemi).",
        okruh="Provoz energetick\u00fdch za\u0159\u00edzen\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Definujte pojem energie, vysv\u011btlete jej\u00ed v\u00fdznam v technice a spole\u010dnosti. "
        "Uve\u010fte jednotky energie a v\u00fdkonu. Pop\u00ed\u0161te hlavn\u00ed zdroje energie na Zemi "
        "(obnoviteln\u00e9 i neobnoviteln\u00e9).")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Pojem energie", level=3)

    add_info_box(doc,
        "Definice: Energie",
        "Schopnost soustavy konat pr\u00e1ci nebo sd\u011blovat teplo. "
        "Energie se nem\u016f\u017ee vytvo\u0159it ani zni\u010dit, pouze p\u0159em\u011bnit "
        "z jedn\u00e9 formy na jinou (1. z\u00e1kon termodynamiky).")

    add_image(doc, img_forms, width_cm=14,
              caption="Obr. 1: Z\u00e1kladn\u00ed formy energie a jejich vz\u00e1jemn\u00e9 p\u0159em\u011bny")

    add_heading(doc, "1.2 Jednotky energie a v\u00fdkonu", level=3)

    add_styled_table(doc,
        headers=["Veli\u010dina", "Jednotka SI", "Dal\u0161\u00ed jednotky"],
        data=[
            ["Energie", "J (joule) = kg\u00b7m\u00b2/s\u00b2", "kWh, cal, BTU, toe, eV"],
            ["V\u00fdkon", "W (watt) = J/s", "kW, MW, GW, HP (kon\u011b)"],
            ["Teplo", "J", "kJ, MJ, GJ, cal, kcal"],
            ["V\u00fdh\u0159evnost", "J/kg nebo J/m\u00b3", "MJ/kg, kWh/m\u00b3"],
        ],
    )

    add_para(doc, "P\u0159evodn\u00ed vztahy:", bold=True, keep_with_next=True)
    add_bullet(doc, "1 kWh = 3,6 MJ = 3 600 kJ")
    add_bullet(doc, "1 cal = 4,186 J")
    add_bullet(doc, "1 toe (tuna ekvivalentu ropy) = 41,868 GJ = 11,63 MWh")
    add_bullet(doc, "1 BTU = 1 055 J")
    add_bullet(doc, "1 HP = 745,7 W", is_last=True)

    # -- 1.3 Zdroje --
    add_page_break(doc)
    add_heading(doc, "1.3 Zdroje energie na Zemi", level=3)

    add_para(doc, "Neobnoviteln\u00e9 zdroje:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["Zdroj", "Forma", "V\u00fdhody", "Nev\u00fdhody"],
        data=[
            ["Uhl\u00ed", "Tuh\u00e9 fosiln\u00ed", "Velk\u00e9 z\u00e1soby, levn\u00e9", "Emise CO\u2082, \u010d\u00e1stice, S"],
            ["Ropa", "Kapaln\u00e9 fosiln\u00ed", "Vysok\u00e1 Q\u1d62, doprava", "Vy\u010derpatelnost, ekologie"],
            ["Zemn\u00ed plyn", "Plynn\u00e9 fosiln\u00ed", "Ni\u017e\u0161\u00ed emise CO\u2082", "Metan = sklen\u00edk. plyn"],
            ["Uran", "Jadern\u00e9 \u0161t\u011bpen\u00ed", "Obrovsk\u00e1 E/kg, bez CO\u2082", "Odpad, bezpe\u010dnost"],
        ],
    )

    add_para(doc, "Obnoviteln\u00e9 zdroje:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["Zdroj", "Princip", "Potenci\u00e1l \u010cR"],
        data=[
            ["Sol\u00e1rn\u00ed", "Fotovoltaika, sol. kol.", "1000\u20131100 kWh/m\u00b2/rok"],
            ["V\u011btrn\u00e1", "V\u011btrn\u00e9 turb\u00edny", "Omezen\u00fd (n\u00ed\u017einnat\u00e1 zem\u011b)"],
            ["Vodn\u00ed", "Turb\u00edny na toc\u00edch", "Vyu\u017eit\u00fd z velk\u00e9 \u010d\u00e1sti"],
            ["Biomasa", "Spalov\u00e1n\u00ed, bioplyn", "V\u00fdznamn\u00fd (lesy, zem\u011bd.)"],
            ["Geotermální", "Teplo zemsk\u00e9 k\u016fry", "Omezen\u00fd (T\u010c, l\u00e1zn\u011b)"],
        ],
    )

    add_image(doc, img_mix, width_cm=14,
              caption="Obr. 2: Prim\u00e1rn\u00ed energetick\u00fd mix \u2014 sv\u011bt vs. \u010cR")

    # -- 1.4 Zasoby --
    add_page_break(doc)
    add_heading(doc, "1.4 Z\u00e1soby a udr\u017eitelnost", level=3)

    add_image(doc, img_res, width_cm=12,
              caption="Obr. 3: Odhadovan\u00e1 \u017eivotnost z\u00e1sob neobnoviteln\u00fdch zdroj\u016f")

    add_warning_box(doc,
        "Uhl\u00ed m\u00e1 nejv\u011bt\u0161\u00ed z\u00e1soby (~130 let), ale nejvy\u0161\u0161\u00ed emise CO\u2082/kWh. "
        "Energetick\u00e1 transformace sm\u011b\u0159uje od uhl\u00ed k plynu a OZE. "
        "\u010cR: uhl\u00ed st\u00e1le 35 % mixu, ale kles\u00e1; roste pod\u00edl sol\u00e1ru a jadra.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Energetick\u00e1 bilance \u010cR", level=3)
    add_bullet(doc, "Spot\u0159eba prim\u00e1rn\u00ed energie: ~1 700 PJ/rok (~40 Mtoe/rok)")
    add_bullet(doc, "Elektrick\u00e1 energie: ~85 TWh/rok (v\u00fdroba), ~60 TWh/rok (spot\u0159eba)")
    add_bullet(doc, "\u010cR je \u010dist\u00fdm export\u00e9rem elekt\u0159iny")
    add_bullet(doc, "Jadern\u00e9 elektr\u00e1rny (Dukovany, Temel\u00edn): ~35 % v\u00fdroby elekt\u0159iny", is_last=True)

    add_heading(doc, "2.2 Energetick\u00e1 \u00fa\u010dinnost p\u0159em\u011bn", level=3)
    add_styled_table(doc,
        headers=["P\u0159em\u011bna", "\u00da\u010dinnost"],
        data=[
            ["Uhl\u00ed \u2192 elekt\u0159ina (klasika)", "33\u201338 %"],
            ["Zemn\u00ed plyn \u2192 el. (paroplyn)", "55\u201362 %"],
            ["Jad. reaktor \u2192 el.", "33\u201337 %"],
            ["Fotovoltaika", "18\u201323 %"],
            ["V\u011btrn\u00e1 turb\u00edna", "35\u201350 %"],
            ["Vodn\u00ed turb\u00edna", "85\u201393 %"],
        ],
    )

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: P\u0159evody energetick\u00fdch jednotek", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Elektr\u00e1rna o v\u00fdkonu 500 MW pracuje 7000 hodin za rok "
        "s \u00fa\u010dinnost\u00ed 38 %. Ur\u010dete: ro\u010dn\u00ed v\u00fdrobu elekt\u0159iny, pot\u0159ebu prim\u00e1rn\u00ed "
        "energie a spot\u0159ebu uhl\u00ed (Q\u1d62 = 20 MJ/kg).", bold=True)

    add_para(doc, "Krok 1: Ro\u010dn\u00ed v\u00fdroba elekt\u0159iny", bold=True)
    add_equation(doc, r"E_{el} = P \times t = 500 \times 7000 = 3{,}5 \times 10^6 \text{ MWh} = 3{,}5 \text{ TWh}")

    add_para(doc, "Krok 2: Prim\u00e1rn\u00ed energie (palivo)", bold=True)
    add_equation(doc, r"E_{prim} = \frac{E_{el}}{\eta} = \frac{3{,}5 \text{ TWh}}{0{,}38} = 9{,}21 \text{ TWh} = 33{,}16 \text{ PJ}")

    add_para(doc, "Krok 3: Spot\u0159eba uhl\u00ed", bold=True)
    add_equation(doc, r"m_{uhli} = \frac{E_{prim}}{Q_i} = \frac{33{,}16 \times 10^{9} \text{ kJ}}{20 \times 10^3 \text{ kJ/kg}} = 1{,}658 \times 10^6 \text{ t} = 1{,}66 \text{ Mt}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "V\u00fdroba: 3,5 TWh/rok\n"
        "Prim\u00e1rn\u00ed energie: 33,16 PJ/rok\n"
        "Spot\u0159eba uhl\u00ed: 1,66 Mt/rok (~4 550 t/den)\n\n"
        "Pro srovn\u00e1n\u00ed: cel\u00e1 \u010cR spot\u0159ebov\u00e1v\u00e1 ~35 Mt uhl\u00ed za rok.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Jak\u00fd je rozd\u00edl mezi prim\u00e1rn\u00ed a kone\u010dnou energi\u00ed?",
         "Prim\u00e1rn\u00ed: energie obsa\u017een\u00e1 ve zdroji (uhl\u00ed, ropa, slunce). "
         "Kone\u010dn\u00e1: energie doru\u010den\u00e1 spot\u0159ebiteli (elekt\u0159ina, teplo, plyn). "
         "Rozd\u00edl = ztráty p\u0159i p\u0159em\u011bn\u011b, p\u0159enosu a distribuci (typicky 50\u201370 %)."),

        ("Pro\u010d m\u00e1 \u010cR tak vysok\u00fd pod\u00edl uhl\u00ed v energetick\u00e9m mixu?",
         "Historick\u00e9 d\u011bdictv\u00ed: velk\u00e9 z\u00e1soby hn\u011bd\u00e9ho uhl\u00ed (severní \u010cechy, Sokolovsko). "
         "Infrastruktura (uheln\u00e9 elektr\u00e1rny, tepln\u00e9 s\u00edt\u011b, pracovn\u00ed m\u00edsta). "
         "Postupn\u011b kles\u00e1 \u2014 r\u016fst jadra, sol\u00e1ru a plynu."),

        ("Co je toe a pro\u010d se pou\u017e\u00edv\u00e1?",
         "Tuna ropn\u00e9ho ekvivalentu (toe) = 41,868 GJ = 11,63 MWh. "
         "Umo\u017e\u0148uje porovn\u00e1vat r\u016fzn\u00e9 zdroje energie na spole\u010dn\u00e9m z\u00e1klad\u011b "
         "(kolik tun ropy by dalo stejn\u00e9 mno\u017estv\u00ed energie)."),

        ("Jak\u00e9 jsou hlavn\u00ed v\u00fdhody a nev\u00fdhody jadern\u00e9 energie?",
         "V\u00fdhody: obrovsk\u00e1 hustota energie (1 kg U-235 \u2248 80 TJ \u2248 2700 t uhl\u00ed), "
         "\u017e\u00e1dn\u00e9 emise CO\u2082 p\u0159i provozu, stabiln\u00ed v\u00fdroba. "
         "Nev\u00fdhody: radioaktivn\u00ed odpad, riziko hav\u00e1rie, vysok\u00e9 investi\u010dn\u00ed n\u00e1klady, "
         "dlouh\u00e1 v\u00fdstavba."),

        ("Pro\u010d je \u00fa\u010dinnost fotovoltaiky jen 18\u201323 %, ale vodn\u00ed turb\u00edny 90 %?",
         "Fotovoltaika: omezena termodynamick\u00fdm limitem p\u0159em\u011bny sv\u011btla (Shockley-Queisser "
         "limit ~33 % pro Si), plus optick\u00e9 a elektrick\u00e9 ztráty. "
         "Vodn\u00ed turb\u00edna: mechanick\u00e1 p\u0159em\u011bna (potenci\u00e1ln\u00ed \u2192 kinetick\u00e1 \u2192 el.), "
         "bez termodynamick\u00e9ho limitu, ztráty jen t\u0159en\u00edm."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "IEA World Energy Outlook 2023")
    add_bullet(doc, "ERU \u2014 Ro\u010dn\u00ed zpr\u00e1va o provozu ES \u010cR")
    add_bullet(doc, "MPO \u010cR \u2014 St\u00e1tn\u00ed energetick\u00e1 koncepce")
    add_bullet(doc, "\u010cengel, Y.A.: Energy, Efficiency, and Sustainability")
    add_bullet(doc, "BP Statistical Review of World Energy", is_last=True)

    save_and_export(doc, "21-energie")


if __name__ == "__main__":
    generate()
