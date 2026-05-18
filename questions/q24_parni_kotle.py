# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 24: Parn\u00ed kotle \u2013 typy, hlavn\u00ed \u010d\u00e1sti, transformace energie, \u00fa\u010dinnost.
"""

import os, sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from docx_engine import (
    create_document, save_and_export, add_heading, add_para,
    add_equation, add_bullet, add_image, add_info_box,
    add_warning_box, add_page_break, add_styled_table,
    add_exam_questions, COLORS, IMG_DIR,
)

def generate_boiler_efficiency():
    fig, ax = plt.subplots(figsize=(8, 5))
    losses = ["Ztr\u00e1ta\nspalinami", "Ztr\u00e1ta\nnedop\u00e1lem", "Ztr\u00e1ta\ns\u00e1l\u00e1n\u00edm", "Ztr\u00e1ta\npopelem", "Ztr\u00e1ta\nfyz. teplem\npaliva", "\u00da\u010dinnost\nkotle"]
    vals = [5.5, 0.5, 0.3, 0.5, 0.2, 93.0]
    colors_bar = [COLORS[1]]*5 + [COLORS[2]]
    bars = ax.bar(losses, vals, color=colors_bar, edgecolor="white", width=0.6)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val}%", ha="center", fontsize=10, fontweight="bold")
    ax.set_ylabel("[%]", fontsize=11)
    ax.set_title("\u00da\u010dinnost parn\u00edho kotle \u2014 nep\u0159\u00edm\u00e1 metoda\n(100 % \u2212 \u03a3 ztr\u00e1t = \u03b7)",
                 fontsize=12, fontweight="bold")
    ax.set_ylim(0, 100)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q24_boiler_eff.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path

def generate():
    print("Generuji diagramy...")
    img_eff = generate_boiler_efficiency()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="24. Parn\u00ed kotle \u2013 typy, hlavn\u00ed \u010d\u00e1sti, transformace energie, \u00fa\u010dinnost.",
        okruh="Provoz energetick\u00fdch za\u0159\u00edzen\u00ed",
    )
    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc, "Popi\u0161te z\u00e1kladn\u00ed typy parn\u00edch kotl\u016f, jejich hlavn\u00ed \u010d\u00e1sti, "
        "transformaci energie a zp\u016fsoby ur\u010dov\u00e1n\u00ed \u00fa\u010dinnosti.")

    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Rozd\u011blen\u00ed parn\u00edch kotl\u016f", level=3)
    add_styled_table(doc,
        headers=["Krit\u00e9rium", "Typy"],
        data=[
            ["Podle ob\u011bhu vody", "P\u0159irozen\u00fd ob\u011bh / nucen\u00fd ob\u011bh / pr\u016fto\u010dn\u00fd (Benson)"],
            ["Podle tlaku", "N\u00edzkotlak\u00fd (< 4 MPa) / st\u0159edotlak\u00fd / vysokotlak\u00fd / nadkritick\u00fd (> 22 MPa)"],
            ["Podle paliva", "Uheln\u00fd / plynov\u00fd / olejov\u00fd / na biomasu"],
            ["Podle oh\u0159i\u0161t\u011b", "Ro\u0161tov\u00fd / pr\u00e1\u0161kov\u00fd / fluidn\u00ed"],
        ],
    )

    add_heading(doc, "1.2 Hlavn\u00ed \u010d\u00e1sti parn\u00edho kotle", level=3)
    add_info_box(doc,
        "Teplosm\u011bnn\u00e9 plochy kotle",
        "Oh\u0159ev vody a v\u00fdroba p\u00e1ry prob\u00edh\u00e1 v n\u011bkolika stup\u0148\u00edch, "
        "ka\u017ed\u00fd s vlastn\u00ed teplosm\u011bnnou plochou.")

    add_styled_table(doc,
        headers=["\u010c\u00e1st", "Funkce", "T vody/p\u00e1ry"],
        data=[
            ["Ekonomiz\u00e9r (oh\u0159\u00edv\u00e1k vody)", "Oh\u0159ev nap\u00e1jec\u00ed vody na teplotu bl\u00edzkou varu", "~105 \u2192 ~300 \u00b0C"],
            ["V\u00fdparn\u00edk (oh\u0159i\u0161t\u011b)", "Var vody, v\u00fdroba syt\u00e9 p\u00e1ry", "T_sat p\u0159i p_kotle"],
            ["P\u0159eh\u0159\u00edv\u00e1k", "P\u0159eh\u0159\u00e1t\u00ed p\u00e1ry na po\u017eadovanou T", "T_sat \u2192 540\u2013620 \u00b0C"],
            ["P\u0159ih\u0159\u00edv\u00e1k", "Druh\u00e9 p\u0159eh\u0159\u00e1t\u00ed (po \u010d\u00e1ste\u010dn\u00e9 expanzi v turb\u00edn\u011b)", "~350 \u2192 540 \u00b0C"],
            ["Oh\u0159\u00edv\u00e1k vzduchu (LUVO)", "P\u0159edeh\u0159ev spalovac\u00edho vzduchu", "20 \u2192 250\u2013350 \u00b0C"],
        ],
    )

    add_para(doc, "Transformace energie v kotli:", bold=True, keep_with_next=True)
    add_equation(doc, r"\text{Chemick\u00e1 E paliva} \xrightarrow{\text{spalov\u00e1n\u00ed}} \text{Teplo spalin} \xrightarrow{\text{p\u0159estup}} \text{Entalpie p\u00e1ry}")

    add_page_break(doc)
    add_heading(doc, "1.3 \u00da\u010dinnost kotle", level=3)

    add_para(doc, "P\u0159\u00edm\u00e1 metoda:", bold=True, keep_with_next=True)
    add_equation(doc, r"\eta_{kotle} = \frac{\dot{m}_p (h_{out} - h_{in})}{\dot{m}_{pal} \cdot Q_i^r}", label="1")

    add_para(doc, "Nep\u0159\u00edm\u00e1 metoda (ze ztr\u00e1t):", bold=True, keep_with_next=True)
    add_equation(doc, r"\eta_{kotle} = 1 - (q_{sp} + q_{chem} + q_{mech} + q_{s\acute{a}l} + q_{fyz})", label="2")

    add_image(doc, img_eff, width_cm=13,
              caption="Obr. 1: Rozlo\u017een\u00ed ztr\u00e1t a \u00fa\u010dinnost parn\u00edho kotle (nep\u0159\u00edm\u00e1 metoda)")

    add_styled_table(doc,
        headers=["Ztr\u00e1ta", "Symbol", "Typick\u00e1 hodnota", "P\u0159\u00ed\u010dina"],
        data=[
            ["Komínov\u00e1 (spalinami)", "q_{sp}", "4\u20138 %", "Hor\u00e9c\u00e9 spaliny odch\u00e1z\u00ed kom\u00ednem"],
            ["Chemick\u00fdm nedop\u00e1lem", "q_{chem}", "0\u20131 %", "CO, nespálen\u00e9 uhlovod\u00edky"],
            ["Mechanick\u00fdm nedop\u00e1lem", "q_{mech}", "0,5\u20132 %", "Nespálen\u00e9 \u010d\u00e1stice v popelu/strusce"],
            ["S\u00e1l\u00e1n\u00edm", "q_{s\u00e1l}", "0,2\u20130,5 %", "Teplo p\u0159es st\u011bny kotle do okol\u00ed"],
            ["Fyz. teplem paliva", "q_{fyz}", "0\u20130,5 %", "Teplo v tuh\u00e9m zbytku (struska)"],
        ],
    )

    add_warning_box(doc,
        "Nejv\u011bt\u0161\u00ed ztr\u00e1tou je KOMÍNOV\u00c1 (4\u20138 %). Sn\u00ed\u017een\u00ed: "
        "sn\u00ed\u017een\u00ed teploty spalin na v\u00fdstupu (omezeno rosn\u00fdm bodem!), "
        "p\u0159edeh\u0159ev vzduchu (LUVO), ekonomiz\u00e9r.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Typick\u00e9 parametry kotl\u016f", level=3)
    add_styled_table(doc,
        headers=["Parametr", "St\u0159edotlak\u00fd", "Vysokotlak\u00fd", "Nadkritick\u00fd"],
        data=[
            ["Tlak p\u00e1ry", "4\u20138 MPa", "14\u201318 MPa", "25\u201330 MPa"],
            ["Teplota p\u00e1ry", "450\u2013500 \u00b0C", "540 \u00b0C", "600\u2013620 \u00b0C"],
            ["V\u00fdkon (parn\u00ed)", "10\u201350 t/h", "100\u2013500 t/h", "500\u20132000 t/h"],
            ["\u00da\u010dinnost", "85\u201390 %", "90\u201393 %", "92\u201395 %"],
        ],
    )

    add_heading(doc, "2.2 Pr\u016fto\u010dn\u00fd (Benson\u016fv) kotel", level=3)
    add_para(doc,
        "U nadkritick\u00fdch kotl\u016f neexistuje fázov\u00fd p\u0159echod kapalina\u2013p\u00e1ra "
        "(p > 22,06 MPa). Voda se postupn\u011b oh\u0159\u00edv\u00e1 na nadkritick\u00fd stav \u2014 "
        "nen\u00ed pot\u0159eba buben (separator). Proto se naz\u00fdv\u00e1 pr\u016fto\u010dn\u00fd kotel.")

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: V\u00fdpo\u010det \u00fa\u010dinnosti kotle", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Kotel spaluje hn\u011bd\u00e9 uhl\u00ed (Q\u1d62 = 15 MJ/kg, m\u0307_{pal} = 20 kg/s). "
        "Vyr\u00e1b\u00ed p\u00e1ru o parametrech h_{out} = 3400 kJ/kg z nap\u00e1jec\u00ed vody "
        "h_{in} = 600 kJ/kg. Pr\u016ftok p\u00e1ry m\u0307_p = 80 kg/s. Ur\u010dete \u00fa\u010dinnost.", bold=True)

    add_equation(doc, r"\eta = \frac{\dot{m}_p(h_{out} - h_{in})}{\dot{m}_{pal} \cdot Q_i^r} = \frac{80 \times (3400 - 600)}{20 \times 15000} = \frac{224\,000}{300\,000} = 0{,}747 = 74{,}7\%")

    add_info_box(doc,
        "V\u00fdsledek:",
        "\u03b7 = 74,7 % \u2014 relativn\u011b n\u00edzk\u00e1 \u00fa\u010dinnost (hn\u011bd\u00e9 uhl\u00ed, vysok\u00e1 vlhkost). "
        "Moderní kotle na kvalitn\u00ed uhl\u00ed dosahuj\u00ed 90\u201395 %.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Vysv\u011btlete rozd\u00edl mezi p\u0159\u00edmou a nep\u0159\u00edmou metodou ur\u010den\u00ed \u00fa\u010dinnosti.",
         "P\u0159\u00edm\u00e1: m\u011b\u0159\u00ed se v\u00fdkon (m\u0307_p, h) a p\u0159\u00edkon (m\u0307_{pal}, Q\u1d62), \u03b7 = v\u00fdkon/p\u0159\u00edkon. "
         "Nep\u0159\u00edm\u00e1: m\u011b\u0159\u00ed se jednotliv\u00e9 ztráty, \u03b7 = 1 \u2212 \u03a3q_i. "
         "Nep\u0159\u00edm\u00e1 je p\u0159esn\u011bj\u0161\u00ed (ztráty jsou mal\u00e9, m\u011b\u0159\u00ed se p\u0159esn\u011b)."),

        ("Pro\u010d je kom\u00ednov\u00e1 ztráta nejv\u011bt\u0161\u00ed a jak ji sn\u00ed\u017eit?",
         "Hor\u00e9c\u00e9 spaliny (T \u2248 120\u2013200 \u00b0C) odch\u00e1z\u00ed kom\u00ednem a odnášej\u00ed teplo. "
         "Sn\u00ed\u017een\u00ed: p\u0159id\u00e1n\u00edm ekonomiz\u00e9ru a LUVO (oh\u0159\u00edv\u00e1k vzduchu), "
         "ale T_{sp} nesm\u00ed klesnout pod rosn\u00fd bod (~90\u2013150 \u00b0C)."),

        ("Co je ekonomiz\u00e9r a jak\u00e9 plní funkce?",
         "V\u00fdm\u011bn\u00edk za kotlem, kde spaliny oh\u0159\u00edvaj\u00ed nap\u00e1jec\u00ed vodu. "
         "Funkce: sni\u017euje kom\u00ednovou ztrátu (chlad\u00ed spaliny), zvy\u0161uje \u03b7 kotle, "
         "p\u0159edeh\u0159\u00edv\u00e1 vodu a odleh\u010duje v\u00fdparn\u00edku."),

        ("Pro\u010d nadkritick\u00fd kotel nepot\u0159ebuje buben?",
         "Nad kritick\u00fdm tlakem (22,06 MPa) neexistuje fázov\u00fd p\u0159echod \u2014 "
         "nen\u00ed pot\u0159eba separovat kapalinu od p\u00e1ry. Voda se plynule m\u011bn\u00ed "
         "v nadkritickou tekutinu. Kotel je pr\u016fto\u010dn\u00fd (Benson)."),

        ("Jak\u00fd v\u00fdznam m\u00e1 p\u0159eh\u0159\u00edv\u00e1k a p\u0159ih\u0159\u00edv\u00e1k?",
         "P\u0159eh\u0159\u00edv\u00e1k: zvy\u0161uje T p\u00e1ry nad T_sat \u2192 vy\u0161\u0161\u00ed \u03b7 cyklu, "
         "vy\u0161\u0161\u00ed suchost na v\u00fdstupu z turb\u00edny. P\u0159ih\u0159\u00edv\u00e1k: znovu oh\u0159eje "
         "p\u00e1ru po \u010d\u00e1ste\u010dn\u00e9 expanzi \u2014 dal\u0161\u00ed zv\u00fd\u0161en\u00ed \u03b7 a suchosti."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M.: Kotle a v\u00fdm\u011bn\u00edky tepla, VUT Brno")
    add_bullet(doc, "Kadrnožka, J.: Tepeln\u00e9 elektr\u00e1rny a tepl\u00e1rny")
    add_bullet(doc, "\u010cSN EN 12952 \u2014 Vodn\u00ed trubkov\u00e9 kotle")
    add_bullet(doc, "Babcock & Wilcox: Steam, Its Generation and Use")
    add_bullet(doc, "VGB PowerTech \u2014 Thermal Power Plants", is_last=True)

    save_and_export(doc, "24-parni-kotle")

if __name__ == "__main__":
    generate()
