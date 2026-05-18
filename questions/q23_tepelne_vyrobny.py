# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 23: Tepeln\u011b energetick\u00e9 v\u00fdrobny, druhy, v\u00fdkony, \u00fa\u010dinnosti a vybaven\u00ed.
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


def generate_efficiency_comparison():
    """Comparison of efficiencies for different power plant types."""
    fig, ax = plt.subplots(figsize=(9, 5))

    types = [
        "Uheln\u00e1\n(subkritick\u00e1)", "Uheln\u00e1\n(nadkritick\u00e1)",
        "Paroplyn.\n(CCGT)", "Jadern\u00e1",
        "Tepl\u00e1rna\n(CHP, cel.)", "Plynov\u00e1\nturbina"
    ]
    eta_el = [36, 44, 60, 34, 30, 38]
    eta_celk = [36, 44, 60, 34, 85, 38]

    x = np.arange(len(types))
    w = 0.35

    bars1 = ax.bar(x - w/2, eta_el, w, label="\u00da\u010dinnost elektrick\u00e1 $\\eta_{el}$",
                   color=COLORS[0], edgecolor="white")
    bars2 = ax.bar(x + w/2, eta_celk, w, label="\u00da\u010dinnost celkov\u00e1 (v\u010d. tepla)",
                   color=COLORS[2], edgecolor="white", alpha=0.7)

    for bar, val in zip(bars1, eta_el):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"{val}%", ha="center", fontsize=9, fontweight="bold")

    # CHP highlight
    ax.annotate("Tepl\u00e1rna:\n\u03b7_{el}=30%\n\u03b7_{celk}=85%!", xy=(4 + w/2, 85),
                xytext=(4.8, 75), fontsize=8, fontweight="bold", color=COLORS[2],
                arrowprops=dict(arrowstyle="->", lw=1))

    ax.set_xticks(x)
    ax.set_xticklabels(types, fontsize=9)
    ax.set_ylabel("\u00da\u010dinnost [%]", fontsize=11)
    ax.set_title("Srovn\u00e1n\u00ed \u00fa\u010dinnost\u00ed energetick\u00fdch v\u00fdroben", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 100)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q23_efficiency.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate():
    print("Generuji diagramy...")
    img_eff = generate_efficiency_comparison()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="23. Tepeln\u011b energetick\u00e9 v\u00fdrobny, druhy, v\u00fdkony, \u00fa\u010dinnosti a vybaven\u00ed.",
        okruh="Provoz energetick\u00fdch za\u0159\u00edzen\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Popi\u0161te z\u00e1kladn\u00ed druhy tepeln\u011b energetick\u00fdch v\u00fdroben, jejich typick\u00e9 v\u00fdkony, "
        "\u00fa\u010dinnosti a hlavn\u00ed technologick\u00e9 vybaven\u00ed.")

    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Rozd\u011blen\u00ed tepeln\u00fdch elektr\u00e1ren", level=3)

    add_info_box(doc,
        "Z\u00e1kladn\u00ed d\u011blen\u00ed",
        "Podle zp\u016fsobu v\u00fdroby: kondenza\u010dn\u00ed elektr\u00e1rna (jen el.), tepl\u00e1rna/CHP "
        "(el. + teplo), v\u00fdtopna (jen teplo). Podle paliva: uheln\u00e1, plynov\u00e1, jadern\u00e1, "
        "na biomasu, spalovna.")

    add_styled_table(doc,
        headers=["Typ", "V\u00fdkon", "\u03b7_{el}", "\u03b7_{celk}", "Palivo"],
        data=[
            ["Uheln\u00e1 kondenz.", "100\u20131000 MW", "33\u201344 %", "33\u201344 %", "Uhl\u00ed"],
            ["Paroplyn. (CCGT)", "100\u2013600 MW", "55\u201362 %", "55\u201362 %", "Zemn\u00ed plyn"],
            ["Jadern\u00e1", "500\u20131200 MW", "33\u201337 %", "33\u201337 %", "Uran"],
            ["Tepl\u00e1rna (CHP)", "10\u2013200 MW_el", "25\u201335 %", "80\u201390 %", "Uhl\u00ed, plyn, biomasa"],
            ["Spalovna TKO", "5\u201350 MW_el", "15\u201325 %", "60\u201380 %", "Komun\u00e1ln\u00ed odpad"],
            ["Plynov\u00e1 turb\u00edna", "20\u2013300 MW", "30\u201340 %", "30\u201340 %", "ZP, kerosin"],
        ],
    )

    add_image(doc, img_eff, width_cm=14,
              caption="Obr. 1: Srovn\u00e1n\u00ed \u00fa\u010dinnost\u00ed r\u016fzn\u00fdch typ\u016f energetick\u00fdch v\u00fdroben")

    add_page_break(doc)
    add_heading(doc, "1.2 Hlavn\u00ed technologick\u00e9 celky", level=3)

    add_para(doc, "Uheln\u00e1 elektr\u00e1rna:", bold=True, keep_with_next=True)
    add_bullet(doc, "Z\u00e1sobov\u00e1n\u00ed palivem: skl\u00e1dka uhl\u00ed, podava\u010de, ml\u00fdny")
    add_bullet(doc, "Kotel (parogener\u00e1tor): spalov\u00e1n\u00ed, v\u00fdroba p\u00e1ry")
    add_bullet(doc, "Turb\u00edna: expanze p\u00e1ry, v\u00fdroba mechanick\u00e9 pr\u00e1ce")
    add_bullet(doc, "Gener\u00e1tor: p\u0159em\u011bna mech. pr\u00e1ce na elekt\u0159inu")
    add_bullet(doc, "Kondenz\u00e1tor: chlazení, kondenzace p\u00e1ry")
    add_bullet(doc, "\u010ci\u0161t\u011bn\u00ed spalin: odlu\u010dova\u010d prachu, odsi\u0159ov\u00e1n\u00ed (FGD), DeNOx")
    add_bullet(doc, "Chladicí syst\u00e9m: chladicí v\u011b\u017ee nebo pr\u016fto\u010dn\u00e9 chlazení", is_last=True)

    add_para(doc, "Paroplynov\u00e1 elektr\u00e1rna (CCGT):", bold=True, keep_with_next=True)
    add_bullet(doc, "Plynov\u00e1 turb\u00edna (Brayton\u016fv cyklus): spalov\u00e1n\u00ed ZP, T_{in} ~ 1400 \u00b0C")
    add_bullet(doc, "Spalinov\u00fd kotel (HRSG): vyu\u017eit\u00ed odpadn\u00edho tepla spalin")
    add_bullet(doc, "Parn\u00ed turb\u00edna (Rankine\u016fv cyklus): dal\u0161\u00ed v\u00fdroba elekt\u0159iny")
    add_bullet(doc, "V\u00fdsledek: \u03b7 = 55\u201362 % (\u0161pi\u010dka v energetice)", is_last=True)

    add_heading(doc, "1.3 Tepl\u00e1rna (CHP)", level=3)

    add_info_box(doc,
        "Kombinovan\u00e1 v\u00fdroba elekt\u0159iny a tepla (KVET/CHP)",
        "Teplo, kter\u00e9 by v kondenza\u010dn\u00ed elektr\u00e1rn\u011b ode\u0161lo do chladic\u00ed v\u011b\u017ee, "
        "se vyu\u017e\u00edv\u00e1 pro vyt\u00e1p\u011bn\u00ed. Celkov\u00e1 \u00fa\u010dinnost vyu\u017eit\u00ed paliva: 80\u201390 %. "
        "Sni\u017euje el. \u00fa\u010dinnost (men\u0161\u00ed sp\u00e1d na turb\u00edn\u011b), ale celkov\u011b je efektivn\u011bj\u0161\u00ed.")

    add_equation(doc, r"\eta_{celk} = \frac{P_{el} + \dot{Q}_{teplo}}{\dot{Q}_{palivo}}", label="1")

    add_para(doc, "Parametr modu teplo/elekt\u0159ina:", keep_with_next=True)
    add_equation(doc, r"\sigma = \frac{\dot{Q}_{teplo}}{P_{el}}", label="2")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Energetick\u00e9 v\u00fdrobny v \u010cR", level=3)
    add_styled_table(doc,
        headers=["V\u00fdrobna", "V\u00fdkon [MW]", "Typ"],
        data=[
            ["Dukovany (JETE)", "4 \u00d7 510", "Jadern\u00e1 (VVER 440)"],
            ["Temel\u00edn (JETE)", "2 \u00d7 1078", "Jadern\u00e1 (VVER 1000)"],
            ["Prunéřov II", "3 \u00d7 250", "Uheln\u00e1 (hn\u011bd\u00e9 uhl\u00ed)"],
            ["Tu\u0161imice II", "4 \u00d7 200", "Uheln\u00e1 (hn\u011bd\u00e9 uhl\u00ed)"],
            ["Prost\u011bjov CCGT", "1 \u00d7 100", "Paroplyn (ZP)"],
            ["Hodon\u00edn (biomasa)", "1 \u00d7 30", "Biomasa + uhl\u00ed"],
        ],
    )

    add_heading(doc, "2.2 Trendy", level=3)
    add_bullet(doc, "Postupn\u00e9 odstavov\u00e1n\u00ed uheln\u00fdch elektr\u00e1ren (2030\u20132050)")
    add_bullet(doc, "V\u00fdstavba nov\u00e9ho jadernho bloku (Dukovany 5)")
    add_bullet(doc, "R\u016fst paroplyn. zdroj\u016f a OZE (sol\u00e1r, v\u00edtr)")
    add_bullet(doc, "Decentralizace \u2014 FVE na st\u0159ech\u00e1ch, mal\u00e9 kogenerace", is_last=True)

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: CHP vs. odd\u011blen\u00e1 v\u00fdroba", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Pot\u0159eba 100 MW tepla a 50 MW elekt\u0159iny. Porovnejte spot\u0159ebu paliva "
        "p\u0159i a) odd\u011blen\u00e9 v\u00fdrob\u011b (elektr\u00e1rna \u03b7_el=38%, v\u00fdtopna \u03b7_t=90%) "
        "a b) CHP (\u03b7_{celk}=85%, \u03c3=2).", bold=True)

    add_para(doc, "a) Odd\u011blen\u00e1 v\u00fdroba:", bold=True)
    add_equation(doc, r"Q_{pal,el} = \frac{P_{el}}{\eta_{el}} = \frac{50}{0{,}38} = 131{,}6 \text{ MW}")
    add_equation(doc, r"Q_{pal,t} = \frac{\dot{Q}_t}{\eta_t} = \frac{100}{0{,}90} = 111{,}1 \text{ MW}")
    add_equation(doc, r"Q_{pal,celk} = 131{,}6 + 111{,}1 = 242{,}7 \text{ MW}")

    add_para(doc, "b) CHP:", bold=True)
    add_equation(doc, r"Q_{pal,CHP} = \frac{P_{el} + \dot{Q}_t}{\eta_{celk}} = \frac{50 + 100}{0{,}85} = 176{,}5 \text{ MW}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Odd\u011blen\u00e1 v\u00fdroba: 242,7 MW paliva\n"
        "CHP: 176,5 MW paliva\n"
        "\u00daspora: 66,2 MW = 27,3 % paliva!\n\n"
        "CHP je v\u00fdrazn\u011b efektivn\u011bj\u0161\u00ed, proto\u017ee vyu\u017e\u00edv\u00e1 odpadn\u00ed teplo turb\u00edny.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Vysv\u011btlete rozd\u00edl mezi kondenza\u010dn\u00ed elektr\u00e1rnou a tepl\u00e1rnou.",
         "Kondenza\u010dn\u00ed: ve\u0161ker\u00e1 p\u00e1ra expanduje v turb\u00edn\u011b na vakuum, "
         "teplo odch\u00e1z\u00ed do chladic\u00ed v\u011b\u017ee. \u03b7_{el} maxim\u00e1ln\u00ed, ale \u03b7_{celk} = \u03b7_{el}. "
         "Tepl\u00e1rna: \u010d\u00e1st p\u00e1ry se odeb\u00edr\u00e1 pro vyt\u00e1p\u011bn\u00ed \u2192 \u03b7_{el} ni\u017e\u0161\u00ed, "
         "ale \u03b7_{celk} = 80\u201390 %."),

        ("Pro\u010d m\u00e1 paroplyn. elektr\u00e1rna nejvy\u0161\u0161\u00ed \u03b7_{el}?",
         "Kombinuje Brayton (GT, T_in ~1400 \u00b0C) a Rankine (parn\u00ed turb\u00edna). "
         "Horn\u00ed cyklus pracuje p\u0159i velmi vysok\u00e9 T_H, doln\u00ed vyu\u017e\u00edv\u00e1 odpadn\u00ed teplo. "
         "\u03b7 = \u03b7_GT + (1\u2212\u03b7_GT)\u00b7\u03b7_ST \u2248 60 %."),

        ("Pro\u010d m\u00e1 jadern\u00e1 elektr\u00e1rna ni\u017e\u0161\u00ed \u03b7 ne\u017e uheln\u00e1?",
         "JE pracuje s ni\u017e\u0161\u00edmi parametry p\u00e1ry (Temel\u00edn: 260 \u00b0C, 6,2 MPa vs. "
         "uheln\u00e1: 540 \u00b0C, 18 MPa). Ni\u017e\u0161\u00ed T_H \u2192 ni\u017e\u0161\u00ed \u03b7_Carnot \u2192 ni\u017e\u0161\u00ed \u03b7_{el}. "
         "D\u016fvod: materi\u00e1lov\u00e9 omezen\u00ed palivov\u00fdch \u010dl\u00e1nk\u016f."),

        ("Co je HRSG a jak funguje?",
         "Heat Recovery Steam Generator \u2014 spalinov\u00fd kotel v paroplynov\u00e9 elektr\u00e1rn\u011b. "
         "Hor\u00e9c\u00ed spaliny z plynov\u00e9 turb\u00edny (~550 \u00b0C) proch\u00e1z\u00ed teplosm\u011bnn\u00fdmi "
         "plochami a oh\u0159\u00edvaj\u00ed vodu/p\u00e1ru pro parn\u00ed turb\u00ednu."),

        ("Pro\u010d je CHP v\u00fdhodn\u011bj\u0161\u00ed ne\u017e odd\u011blen\u00e1 v\u00fdroba?",
         "P\u0159i odd\u011blen\u00e9 v\u00fdrob\u011b se teplo z kondenz\u00e1toru mar\u00ed (chladic\u00ed v\u011b\u017e). "
         "CHP toto teplo vyu\u017e\u00edv\u00e1 pro vyt\u00e1p\u011bn\u00ed \u2192 celkov\u00e1 \u00fa\u010dinnost 80\u201390 %. "
         "\u00daspora paliva: typicky 20\u201330 % oproti odd\u011blen\u00e9 v\u00fdrob\u011b."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Kadrnožka, J.: Tepeln\u00e9 elektr\u00e1rny a tepl\u00e1rny")
    add_bullet(doc, "ERU \u2014 Ro\u010dn\u00ed zpr\u00e1va o provozu ES \u010cR")
    add_bullet(doc, "\u010cengel, Y.A.: Thermodynamics \u2014 Power Plant Cycles")
    add_bullet(doc, "Sm\u011brnice 2012/27/EU o energetick\u00e9 \u00fa\u010dinnosti")
    add_bullet(doc, "COGEN Europe \u2014 Combined Heat and Power", is_last=True)

    save_and_export(doc, "23-tepelne-vyrobny")


if __name__ == "__main__":
    generate()
