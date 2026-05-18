# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 22: Spalovac\u00ed za\u0159\u00edzen\u00ed pro r\u016fzn\u00e9 druhy paliv, princip a popis.
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


def generate_furnace_types():
    """Overview of furnace types for different fuels."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # Root
    root = FancyBboxPatch((3, 6), 4, 0.7, boxstyle="round,pad=0.15",
                           facecolor="#E8F0FE", edgecolor="#2563EB", lw=2)
    ax.add_patch(root)
    ax.text(5, 6.35, "SPALOVAC\u00cd ZA\u0158\u00cdZEN\u00cd", ha="center", fontsize=12,
            fontweight="bold", color="#2563EB")

    categories = [
        (1, 4, "TUH\u00c1 PALIVA", "#DC2626",
         ["Ro\u0161tov\u00e1 oh\u0159i\u0161t\u011b", "Pr\u00e1\u0161kov\u00e9 ho\u0159\u00e1ky", "Fluidn\u00ed kotle", "Spalovny odpadu"]),
        (5, 4, "KAPALN\u00c1", "#D97706",
         ["Tlakov\u00e9 ho\u0159\u00e1ky", "Rotacn\u00ed ho\u0159\u00e1ky", "Odpakov\u00e1n\u00ed"]),
        (9, 4, "PLYNN\u00c1", "#16A34A",
         ["Difuzn\u00ed ho\u0159\u00e1ky", "Premix ho\u0159\u00e1ky", "DLN ho\u0159\u00e1ky", "Katalytick\u00e9"]),
    ]

    for x, y, title, color, items in categories:
        box = FancyBboxPatch((x - 1.3, y - 0.4), 2.6, 0.8, boxstyle="round,pad=0.1",
                              facecolor="white", edgecolor=color, lw=2)
        ax.add_patch(box)
        ax.text(x, y, title, ha="center", fontsize=10, fontweight="bold", color=color)
        ax.plot([5, x], [6, y + 0.4], color="gray", lw=1)

        for i, item in enumerate(items):
            yi = y - 1.0 - i * 0.6
            ax.text(x, yi, item, ha="center", fontsize=8, color="#333")
            bx = FancyBboxPatch((x - 1.2, yi - 0.25), 2.4, 0.5, boxstyle="round,pad=0.05",
                                 facecolor="white", edgecolor=color, lw=0.8, alpha=0.5)
            ax.add_patch(bx)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q22_furnace_types.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate():
    print("Generuji diagramy...")
    img_types = generate_furnace_types()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="22. Spalovac\u00ed za\u0159\u00edzen\u00ed pro r\u016fzn\u00e9 druhy paliv, princip a popis.",
        okruh="Provoz energetick\u00fdch za\u0159\u00edzen\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Popi\u0161te z\u00e1kladn\u00ed typy spalovac\u00edch za\u0159\u00edzen\u00ed pro tuh\u00e1, kapaln\u00e1 a plynn\u00e1 paliva. "
        "Vysv\u011btlete princip \u010dinnosti, hlavn\u00ed \u010d\u00e1sti a oblasti pou\u017eit\u00ed.")

    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_image(doc, img_types, width_cm=14,
              caption="Obr. 1: P\u0159ehled spalovac\u00edch za\u0159\u00edzen\u00ed podle druhu paliva")

    # -- Tuha paliva --
    add_heading(doc, "1.1 Spalovac\u00ed za\u0159\u00edzen\u00ed pro tuh\u00e1 paliva", level=3)

    add_styled_table(doc,
        headers=["Typ", "Princip", "V\u00fdkon", "Palivo"],
        data=[
            ["Ro\u0161tov\u00e9 oh\u0159i\u0161t\u011b", "Palivo ho\u0159\u00ed na pohybliv\u00e9m/pevn\u00e9m ro\u0161tu, vzduch zespodu", "1\u201350 MW", "Kusov\u00e9 uhl\u00ed, d\u0159evo, biomasa"],
            ["Pr\u00e1\u0161kov\u00e9 oh\u0159i\u0161t\u011b", "Jemn\u011b mlet\u00e9 palivo (< 0,1 mm) ho\u0159\u00ed v letu", "50\u20131000 MW", "Uhl\u00ed, biomasa"],
            ["Fluidn\u00ed kotle (BFB/CFB)", "Inert. l\u016f\u017eko fluidizov\u00e1no vzduchem, palivo v n\u011bm ho\u0159\u00ed", "10\u2013500 MW", "Uhl\u00ed, biomasa, odpad, kaly"],
            ["Spalovny TKO", "Ro\u0161t + doho\u0159\u00edv\u00e1n\u00ed, \u010di\u0161t\u011bn\u00ed spalin", "5\u201350 MW", "Komun\u00e1ln\u00ed odpad"],
        ],
    )

    add_info_box(doc,
        "Fluidn\u00ed spalov\u00e1n\u00ed \u2014 v\u00fdhody",
        "Ni\u017e\u0161\u00ed teplota spalov\u00e1n\u00ed (800\u2013900 \u00b0C) \u2192 m\u00e9n\u011b NOx. "
        "Mo\u017enost dod\u00e1v\u00e1n\u00ed v\u00e1pence do lo\u017ee \u2192 odsi\u0159ov\u00e1n\u00ed p\u0159\u00edmo v oh\u0159i\u0161ti. "
        "Spaluje i nekvalitní paliva (vysok\u00fd popel, vlhkost).")

    # -- Kapalna --
    add_page_break(doc)
    add_heading(doc, "1.2 Spalovac\u00ed za\u0159\u00edzen\u00ed pro kapaln\u00e1 paliva", level=3)

    add_styled_table(doc,
        headers=["Typ ho\u0159\u00e1ku", "Princip", "Pou\u017eit\u00ed"],
        data=[
            ["Tlakov\u00fd (mechanic.)", "Palivo rozprá\u0161eno tlakem (10\u201330 bar) tryskou", "TO, lehk\u00fd i t\u011b\u017ek\u00fd"],
            ["Rota\u010dn\u00ed", "Palivo rozprá\u0161eno rotuj\u00edc\u00edm kotouc\u00edkem", "Visk\u00f3zn\u00ed paliva"],
            ["Parn\u00ed/vzdu\u0161n\u00fd", "Atomizace pomoc\u00ed p\u00e1ry nebo stla\u010d. vzduchu", "T\u011b\u017ek\u00fd TO, odpadn\u00ed oleje"],
        ],
    )

    add_para(doc, "Kl\u00ed\u010dov\u00e9: kvalitn\u00ed atomizace (mal\u00e9 kapky = velk\u00fd povrch = rychl\u00e9 ho\u0159en\u00ed).")

    # -- Plynna --
    add_heading(doc, "1.3 Spalovac\u00ed za\u0159\u00edzen\u00ed pro plynn\u00e1 paliva", level=3)

    add_styled_table(doc,
        headers=["Typ ho\u0159\u00e1ku", "Princip", "V\u00fdhody"],
        data=[
            ["Difuzn\u00ed", "Plyn a vzduch se m\u00eds\u00ed a\u017e v plameni", "Stabiln\u00ed, bezpe\u010dn\u00fd, \u0161irok\u00fd regulac. rozsah"],
            ["Premix", "Plyn a vzduch se p\u0159edm\u00eds\u00ed p\u0159ed plamenem", "Ni\u017e\u0161\u00ed emise, vy\u0161\u0161\u00ed \u03b7"],
            ["DLN (Dry Low NOx)", "Chud\u00e1 p\u0159edm\u00edsen\u00e1 sm\u011bs, rozpt\u00fdlen\u00fd plamen", "Velmi n\u00edzk\u00e9 NOx (< 25 ppm)"],
            ["Katalytick\u00fd", "Spalov\u00e1n\u00ed na povrchu katalyz\u00e1toru p\u0159i n\u00edzk\u00e9 T", "Ultra-n\u00edzk\u00e9 emise, < 400 \u00b0C"],
        ],
    )

    add_warning_box(doc,
        "U plynov\u00fdch ho\u0159\u00e1k\u016f premix je riziko zp\u011btn\u00e9ho pro\u0161lehnut\u00ed plamene (flashback). "
        "Vy\u017eaduje pe\u010dliv\u00fd n\u00e1vrh rychlosti proud\u011bn\u00ed > rychlost \u0161\u00ed\u0159en\u00ed plamene.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Volba spalovac\u00edho za\u0159\u00edzen\u00ed", level=3)
    add_styled_table(doc,
        headers=["Krit\u00e9rium", "Ro\u0161tov\u00e9", "Pr\u00e1\u0161kov\u00e9", "Fluidn\u00ed"],
        data=[
            ["V\u00fdkon", "1\u201350 MW", "50\u20131000 MW", "10\u2013500 MW"],
            ["N\u00e1roky na palivo", "N\u00edzk\u00e9 (kusy)", "Vysok\u00e9 (mlet\u00ed)", "N\u00edzk\u00e9 (i nekvalit.)"],
            ["Emisní limity", "H\u016f\u0159e splnit.", "Splniteln\u00e9", "Nejsnadn\u011bji"],
            ["Investi\u010dn\u00ed n\u00e1klady", "Nejni\u017e\u0161\u00ed", "Vysok\u00e9", "St\u0159edn\u00ed"],
            ["Regulace v\u00fdkonu", "Pomal\u00e1", "Dobr\u00e1", "Dobr\u00e1"],
        ],
    )

    add_heading(doc, "2.2 Emisn\u00ed limity (\u010cR, velk\u00e9 zdroje > 50 MW)", level=3)
    add_styled_table(doc,
        headers=["L\u00e1tka", "Limit [mg/m\u00b3_N]", "Metoda sn\u00ed\u017een\u00ed"],
        data=[
            ["TZL (prach)", "20", "Elektrostatick\u00fd filtr, l\u00e1tkov\u00fd filtr"],
            ["SO\u2082", "200", "V\u00e1pencov\u00e1 vyp\u00edrka (FGD), fluidn\u00ed"],
            ["NOx", "200", "SCR/SNCR, DLN, n\u00edzko-NOx ho\u0159\u00e1ky"],
            ["CO", "250", "Dostate\u010dn\u00fd p\u0159ebytek vzduchu, doho\u0159\u00edv\u00e1n\u00ed"],
        ],
    )

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Volba spalovac\u00edho za\u0159\u00edzen\u00ed", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: M\u00e1te spalovat sm\u011bs hn\u011bd\u00e9ho uhl\u00ed a biomasy (20 % hm.) o celkov\u00e9m "
        "v\u00fdkonu 80 MW. Palivo m\u00e1 prom\u011bnliv\u00fd obsah vlhkosti (25\u201345 %) a popela (10\u201325 %). "
        "Jak\u00fd typ oh\u0159i\u0161t\u011b zvol\u00edte?", bold=True)

    add_para(doc, "Rozbor:", bold=True, keep_with_next=True)
    add_bullet(doc, "V\u00fdkon 80 MW \u2014 ro\u0161tov\u00e9 (max ~50 MW) nevyhovuje, pr\u00e1\u0161kov\u00e9 nebo fluidn\u00ed")
    add_bullet(doc, "Prom\u011bnliv\u00e1 vlhkost a popel \u2014 pr\u00e1\u0161kov\u00e9 vy\u017eaduje stabiln\u00ed kvalitu paliva")
    add_bullet(doc, "Spolusp\u00e1len\u00ed biomasy \u2014 fluidn\u00ed zvl\u00e1dne r\u016fznorod\u00e1 paliva l\u00e9pe")
    add_bullet(doc, "Emisn\u00ed limity \u2014 fluidn\u00ed: mo\u017enost odsi\u0159ov\u00e1n\u00ed v lo\u017ei", is_last=True)

    add_info_box(doc,
        "Doporu\u010den\u00ed: Fluidn\u00ed kotel (CFB)",
        "Atmosf\u00e9rick\u00fd cirkuluj\u00edc\u00ed fluidn\u00ed kotel (CFB) je optim\u00e1ln\u00ed volba:\n"
        "- Zvl\u00e1dne prom\u011bnlivou kvalitu paliva\n"
        "- Spalov\u00e1n\u00ed p\u0159i 850 \u00b0C (n\u00edzk\u00e9 NOx)\n"
        "- Odsi\u0159ov\u00e1n\u00ed v\u00e1pencem p\u0159\u00edmo v lo\u017ei\n"
        "- V\u00fdkon 80 MW je v optim\u00e1ln\u00edm rozsahu")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Jak\u00fd je rozd\u00edl mezi ro\u0161tov\u00fdm a pr\u00e1\u0161kov\u00fdm oh\u0159i\u0161t\u011bm?",
         "Ro\u0161tov\u00e9: palivo ho\u0159\u00ed v kusech na ro\u0161tu, vzduch proud\u00ed zespodu. "
         "Pr\u00e1\u0161kov\u00e9: palivo se jemn\u011b semele (< 0,1 mm) a ho\u0159\u00ed v letu. "
         "Pr\u00e1\u0161kov\u00e9 m\u00e1 vy\u0161\u0161\u00ed v\u00fdkon, lep\u0161\u00ed regulaci, ale vy\u017eaduje mlec\u00ed za\u0159\u00edzen\u00ed."),

        ("Pro\u010d je fluidn\u00ed spalov\u00e1n\u00ed v\u00fdhodn\u00e9 z hlediska emis\u00ed?",
         "Ni\u017e\u0161\u00ed teplota spalov\u00e1n\u00ed (800\u2013900 \u00b0C vs. 1200\u20131500 \u00b0C u pr\u00e1\u0161ku) "
         "sni\u017euje tvorbu termick\u00e9ho NOx. Mo\u017enost p\u0159id\u00e1vat v\u00e1penec do lo\u017ee "
         "pro z\u00e1chyt SO\u2082 p\u0159\u00edmo p\u0159i spalov\u00e1n\u00ed (bez extern\u00edho FGD)."),

        ("Co je atomizace a pro\u010d je d\u016fle\u017eit\u00e1 u kapaln\u00fdch paliv?",
         "Rozpr\u00e1\u0161en\u00ed kapek paliva na jemn\u00e9 kapky (10\u2013200 \u03bcm). "
         "Men\u0161\u00ed kapky = v\u011bt\u0161\u00ed povrch = rychlej\u0161\u00ed odpa\u0159en\u00ed a ho\u0159en\u00ed. "
         "\u0160patn\u00e1 atomizace \u2192 velk\u00e9 kapky \u2192 ne\u00fapln\u00e9 spalov\u00e1n\u00ed, saze, CO."),

        ("Co je DLN ho\u0159\u00e1k a jak sni\u017euje NOx?",
         "Dry Low NOx: p\u0159edm\u00edsen\u00e1 chud\u00e1 sm\u011bs (n >> 1) ho\u0159\u00ed s ni\u017e\u0161\u00ed teplotou "
         "plamene. Ni\u017e\u0161\u00ed T \u2192 m\u00e9n\u011b termick\u00e9ho NOx. NOx < 25 ppm "
         "(vs. 100\u2013300 ppm u konven\u010dn\u00edch difuzn\u00edch ho\u0159\u00e1k\u016f)."),

        ("Pro\u010d se spalovny odpadu navrhuj\u00ed s velk\u00fdm p\u0159ebytkem vzduchu?",
         "Odpad m\u00e1 prom\u011bnliv\u00e9 slo\u017een\u00ed a vlhkost. Velk\u00fd p\u0159ebytek (n = 1,5\u20132) "
         "zaji\u0161\u0165uje \u00fapln\u00e9 sp\u00e1len\u00ed i za nep\u0159\u00edzniv\u00fdch podm\u00ednek. "
         "Z\u00e1kon vy\u017eaduje T > 850 \u00b0C po dobu > 2 s (zni\u010den\u00ed dioxin\u016f)."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M.: Spalov\u00e1n\u00ed a spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Balas, M.: Kotle a v\u00fdm\u011bn\u00edky tepla, VUT Brno")
    add_bullet(doc, "Turns, S.R.: An Introduction to Combustion")
    add_bullet(doc, "Sm\u011brnice 2010/75/EU o pr\u016fmyslov\u00fdch emis\u00edch (IED)")
    add_bullet(doc, "\u010cSN EN 303 \u2014 Kotle pro \u00fast\u0159edn\u00ed vyt\u00e1p\u011bn\u00ed", is_last=True)

    save_and_export(doc, "22-spalovaci-zarizeni")


if __name__ == "__main__":
    generate()
