# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 14: Paliva, rozd\u011blen\u00ed paliv, charakteristiky a slo\u017een\u00ed paliv.
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

def generate_fuel_classification():
    """Tree diagram of fuel classification."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

    from matplotlib.patches import FancyBboxPatch

    # Root
    root = FancyBboxPatch((3.5, 7), 3, 0.7, boxstyle="round,pad=0.15",
                           facecolor="#E8F0FE", edgecolor="#2563EB", lw=2)
    ax.add_patch(root)
    ax.text(5, 7.35, "PALIVA", ha="center", va="center", fontsize=13, fontweight="bold", color="#2563EB")

    # Level 1: Tuh\u00e1, Kapaln\u00e1, Plynn\u00e1
    l1 = [
        (1, 5.5, "TUH\u00c1", "#FEE2E2", "#DC2626"),
        (4, 5.5, "KAPALN\u00c1", "#FEF3C7", "#D97706"),
        (7, 5.5, "PLYNN\u00c1", "#DCFCE7", "#16A34A"),
    ]
    for x, y, label, fc, ec in l1:
        box = FancyBboxPatch((x, y), 2, 0.7, boxstyle="round,pad=0.1",
                              facecolor=fc, edgecolor=ec, lw=2)
        ax.add_patch(box)
        ax.text(x + 1, y + 0.35, label, ha="center", va="center", fontsize=10,
                fontweight="bold", color=ec)
        ax.plot([5, x + 1], [7, y + 0.7], color="gray", lw=1)

    # Level 2: sub-categories
    l2_tuha = [
        (0, 4, "Uhl\u00ed (hn\u011bd\u00e9,\n\u010dern\u00e9, antracit)"),
        (0, 2.8, "D\u0159evo, biomasa"),
        (0, 1.6, "Ra\u0161elina, koks"),
    ]
    l2_kapal = [
        (3.5, 4, "Ropn\u00e9 produkty\n(benzin, nafta, TO)"),
        (3.5, 2.8, "Bioliq. (bionafta,\nbioethanol)"),
        (3.5, 1.6, "Dehty, oleje"),
    ]
    l2_plyn = [
        (7, 4, "Zemn\u00ed plyn (CH\u2084)"),
        (7, 2.8, "Propan-butan\n(LPG)"),
        (7, 1.6, "Vod\u00edk, bioplyn,\nsvítiplyn"),
    ]

    for items, parent_x, ec in [(l2_tuha, 2, "#DC2626"), (l2_kapal, 5, "#D97706"), (l2_plyn, 8, "#16A34A")]:
        for x, y, label in items:
            ax.text(x + 1.2, y + 0.35, label, fontsize=8, ha="center", va="center", color="#333")
            box = FancyBboxPatch((x + 0.1, y), 2.2, 0.7, boxstyle="round,pad=0.08",
                                  facecolor="white", edgecolor=ec, lw=1, alpha=0.7)
            ax.add_patch(box)
            ax.plot([parent_x, x + 1.2], [5.5, y + 0.7], color=ec, lw=0.8, alpha=0.5)

    fig.suptitle("Rozd\u011blen\u00ed paliv podle skupenstv\u00ed", fontsize=12, fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q14_classification.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_heating_values():
    """Bar chart comparing heating values of different fuels."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    fuels = [
        "Vod\u00edk (H\u2082)", "Zemn\u00ed plyn", "Propan (LPG)",
        "Benzin", "Motorov\u00e1 nafta", "T\u011b\u017ek\u00fd TO",
        "\u010cern\u00e9 uhl\u00ed", "Hn\u011bd\u00e9 uhl\u00ed", "D\u0159evo (such\u00e9)",
        "Biomasa (st\u00e9bla)", "Ra\u0161elina"
    ]
    Qi = [120.0, 34.0, 46.4, 43.5, 42.5, 40.0, 29.0, 17.0, 15.0, 14.0, 9.0]
    colors_bar = (
        [COLORS[2]] * 3 +  # plynn\u00e1/vod\u00edk
        [COLORS[3]] * 3 +  # kapaln\u00e1
        [COLORS[1]] * 2 +  # uhl\u00ed
        [COLORS[2]] * 2 +  # biomasa
        ["#7C3AED"]        # ra\u0161elina
    )

    bars = ax.barh(fuels, Qi, color=colors_bar, edgecolor="white", height=0.6)

    for bar, val in zip(bars, Qi):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{val} MJ/kg", va="center", fontsize=9, fontweight="bold")

    ax.set_xlabel("V\u00fdh\u0159evnost Q\u1d62 [MJ/kg]", fontsize=11)
    ax.set_title("V\u00fdh\u0159evnost vybran\u00fdch paliv", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 135)
    ax.invert_yaxis()

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q14_heating_values.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_coal_composition():
    """Stacked bar chart showing composition of different coal types."""
    fig, ax = plt.subplots(figsize=(8, 5))

    coals = ["Ra\u0161elina", "Hn\u011bd\u00e9 uhl\u00ed", "\u010cern\u00e9 uhl\u00ed", "Antracit"]
    C = [55, 65, 80, 93]
    H = [6, 5, 5, 2]
    O = [33, 25, 10, 2]
    N_S = [2, 2, 2, 1]
    W_A = [4, 3, 3, 2]  # vlhkost + popel (zjednodu\u0161en\u011b)

    x = np.arange(len(coals))
    w = 0.5

    ax.bar(x, C, w, label="Uhl\u00edk C", color=COLORS[0])
    ax.bar(x, H, w, bottom=C, label="Vod\u00edk H", color=COLORS[2])
    bottom2 = [c + h for c, h in zip(C, H)]
    ax.bar(x, O, w, bottom=bottom2, label="Kysl\u00edk O", color=COLORS[3])
    bottom3 = [b + o for b, o in zip(bottom2, O)]
    ax.bar(x, N_S, w, bottom=bottom3, label="N + S", color="#7C3AED")
    bottom4 = [b + n for b, n in zip(bottom3, N_S)]
    ax.bar(x, W_A, w, bottom=bottom4, label="Vl. + popel", color="gray")

    ax.set_xticks(x)
    ax.set_xticklabels(coals)
    ax.set_ylabel("Slo\u017een\u00ed [% hm.]", fontsize=11)
    ax.set_title("Prvkov\u00e9 slo\u017een\u00ed r\u016fzn\u00fdch typ\u016f uhl\u00ed (ho\u0159lavina)", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9, loc="upper right")
    ax.set_ylim(0, 105)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q14_coal_composition.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH DOKUMENTU
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_class = generate_fuel_classification()
    img_hv = generate_heating_values()
    img_coal = generate_coal_composition()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="14. Paliva, rozd\u011blen\u00ed paliv, charakteristiky a slo\u017een\u00ed paliv.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Vysv\u011btlete pojem palivo, uve\u010fte z\u00e1kladn\u00ed rozd\u011blen\u00ed paliv, jejich hlavn\u00ed "
        "charakteristiky a zp\u016fsoby popisu slo\u017een\u00ed tuh\u00fdch, kapaln\u00fdch a plynn\u00fdch paliv.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Definice paliva", level=3)

    add_info_box(doc,
        "Definice: Palivo",
        "L\u00e1tka, kter\u00e1 p\u0159i chemick\u00e9 reakci se vzdu\u0161n\u00fdm kysl\u00edkem (spalov\u00e1n\u00ed) "
        "uvol\u0148uje tepelnou energii vyu\u017eitelnou pro technick\u00e9 \u00fa\u010dely. "
        "Z\u00e1kladn\u00ed ho\u0159lav\u00e9 prvky: uhl\u00edk C, vod\u00edk H, s\u00edra S.")

    add_heading(doc, "1.2 Rozd\u011blen\u00ed paliv", level=3)

    add_image(doc, img_class, width_cm=14,
              caption="Obr. 1: Rozd\u011blen\u00ed paliv podle skupenstv\u00ed")

    add_para(doc, "Rozd\u011blen\u00ed podle p\u016fvodu:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["P\u016fvod", "P\u0159\u00edklady"],
        data=[
            ["P\u0159\u00edrodn\u00ed (fosiln\u00ed)", "Uhl\u00ed, ropa, zemn\u00ed plyn, ra\u0161elina"],
            ["P\u0159\u00edrodn\u00ed (obnoviteln\u00e1)", "D\u0159evo, biomasa, bioplyn"],
            ["Um\u011bl\u00e1 (zpracovan\u00e1)", "Koks, brikety, benzin, nafta, svítiplyn, vod\u00edk"],
            ["Jadern\u00e1", "Uran, thorium, plutonium"],
        ],
    )

    # -- 1.3 Slo\u017een\u00ed --
    add_page_break(doc)
    add_heading(doc, "1.3 Slo\u017een\u00ed tuh\u00fdch a kapaln\u00fdch paliv", level=3)

    add_info_box(doc,
        "T\u0159i slo\u017eky paliva",
        "1) Ho\u0159lavina (h) \u2014 uhl\u00edk C, vod\u00edk H, s\u00edra S, (kysl\u00edk O, dus\u00edk N \u2014 v ho\u0159lavin\u011b)\n"
        "2) Popelovina (A) \u2014 miner\u00e1ln\u00ed l\u00e1tky, kter\u00e9 tvo\u0159\u00ed popel\n"
        "3) Voda (W) \u2014 vlhkost paliva")

    add_para(doc, "Bilance slo\u017een\u00ed (hmotnostn\u00ed zlomky):", keep_with_next=True)
    add_equation(doc, r"C^r + H^r + S^r + O^r + N^r + A^r + W^r = 1", label="1")

    add_para(doc, "kde horn\u00ed index r ozna\u010duje surov\u00e9 (raw) palivo.", keep_with_next=True)

    add_para(doc, "Zp\u016fsoby vyj\u00e1d\u0159en\u00ed slo\u017een\u00ed:", bold=True, keep_with_next=True)
    add_styled_table(doc,
        headers=["Ozna\u010den\u00ed", "Stav paliva", "Vztah"],
        data=[
            ["Surov\u00e9 (r)", "Jak p\u0159ich\u00e1z\u00ed \u2014 s vodou i popelem", "C\u02b3 + H\u02b3 + ... + A\u02b3 + W\u02b3 = 1"],
            ["Such\u00e9 (d)", "Bez vody (W = 0)", "p\u0159epo\u010det: X\u1d48 = X\u02b3/(1 \u2212 W\u02b3)"],
            ["Ho\u0159lavina (daf)", "Bez vody a popela", "p\u0159epo\u010det: X\u1d48\u1d43\u1da0 = X\u02b3/((1 \u2212 W\u02b3)(1 \u2212 A\u1d48))"],
        ],
    )

    add_image(doc, img_coal, width_cm=13,
              caption="Obr. 2: Prvkov\u00e9 slo\u017een\u00ed r\u016fzn\u00fdch typ\u016f uhl\u00ed \u2014 s rostouc\u00edm st\u00e1\u0159\u00edm roste pod\u00edl C")

    # -- 1.4 Slo\u017een\u00ed plynn\u00fdch --
    add_page_break(doc)
    add_heading(doc, "1.4 Slo\u017een\u00ed plynn\u00fdch paliv", level=3)

    add_para(doc,
        "Plynn\u00e1 paliva se popisuj\u00ed objemov\u00fdmi (mol\u00e1rn\u00edmi) zlomky slo\u017eek:", keep_with_next=True)
    add_equation(doc, r"\text{CH}_4 + \text{C}_2\text{H}_6 + \text{C}_3\text{H}_8 + \text{CO} + \text{H}_2 + \text{CO}_2 + \text{N}_2 + \ldots = 1", label="2")

    add_styled_table(doc,
        headers=["Plyn", "Hlavn\u00ed slo\u017eka", "Q\u1d62 [MJ/m\u00b3]"],
        data=[
            ["Zemn\u00ed plyn", "CH\u2084 (90\u201398 %)", "34\u201336"],
            ["Propan-butan (LPG)", "C\u2083H\u2088 + C\u2084H\u2081\u2080", "90\u2013120"],
            ["Svítiplyn", "H\u2082 (50 %) + CO + CH\u2084", "16\u201318"],
            ["Bioplyn", "CH\u2084 (55\u201370 %) + CO\u2082", "20\u201325"],
            ["Vysokopecn\u00ed plyn", "CO (20\u201328 %) + N\u2082 + CO\u2082", "3\u20134"],
        ],
    )

    # -- 1.5 Charakteristiky --
    add_heading(doc, "1.5 Z\u00e1kladn\u00ed charakteristiky paliv", level=3)

    add_para(doc, "V\u00fdh\u0159evnost a spaln\u00e9 teplo:", bold=True, keep_with_next=True)
    add_bullet(doc, "Spaln\u00e9 teplo Q\u209b [MJ/kg] \u2014 teplo uvoln\u011bn\u00e9 \u00fapln\u00fdm sp\u00e1len\u00edm 1 kg paliva, "
               "v\u010detn\u011b kondenza\u010dn\u00edho tepla vodn\u00ed p\u00e1ry ve spalin\u00e1ch")
    add_bullet(doc, "V\u00fdh\u0159evnost Q\u1d62 [MJ/kg] \u2014 spaln\u00e9 teplo m\u00ednus kondenza\u010dn\u00ed teplo "
               "vodn\u00ed p\u00e1ry (p\u00e1ra odch\u00e1z\u00ed jako plyn, nekondenzuje)")
    add_bullet(doc, "Vztah: Q\u1d62 = Q\u209b \u2212 r\u00b7(9H\u02b3 + W\u02b3), kde r = 2,454 MJ/kg je v\u00fdparn\u00e9 teplo vody p\u0159i 25 \u00b0C", is_last=True)

    add_equation(doc, r"Q_i^r = Q_s^r - r(9H^r + W^r)", label="3")

    add_image(doc, img_hv, width_cm=14,
              caption="Obr. 3: V\u00fdh\u0159evnost vybran\u00fdch paliv")

    add_page_break(doc)
    add_para(doc, "Dal\u0161\u00ed d\u016fle\u017eit\u00e9 charakteristiky:", bold=True, keep_with_next=True)

    add_styled_table(doc,
        headers=["Charakteristika", "Jednotka", "V\u00fdznam"],
        data=[
            ["Vlhkost W\u02b3", "%", "Sni\u017euje v\u00fdh\u0159evnost, zvy\u0161uje objem spalin"],
            ["Popel A\u02b3", "%", "Tvo\u0159\u00ed strusku, \u0161kv\u00e1ru; eroze povrch\u016f"],
            ["Prchav\u00e1 ho\u0159lavina V\u1d48\u1d43\u1da0", "%", "Snadn\u00e9 vzn\u00edcen\u00ed; d\u0159evo 80 %, antracit 5 %"],
            ["Bod m\u011bknut\u00ed popela", "\u00b0C", "Ur\u010duje typ ohni\u0161t\u011b (v\u00fdtavn\u00e9 vs. granula\u010dn\u00ed)"],
            ["S\u00edra S\u02b3", "%", "Koroze, emise SO\u2082, kyselinov\u00fd rosn\u00fd bod"],
            ["Teplota vzn\u00edcen\u00ed", "\u00b0C", "Min. T pro samovoln\u00e9 vzn\u00edcen\u00ed na vzduchu"],
        ],
    )

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Srovn\u00e1n\u00ed typ\u016f uhl\u00ed", level=3)
    add_styled_table(doc,
        headers=["Parametr", "Hn\u011bd\u00e9 uhl\u00ed", "\u010cern\u00e9 uhl\u00ed", "Antracit"],
        data=[
            ["St\u00e1\u0159\u00ed [mil. let]", "30\u201360", "60\u2013300", "300+"],
            ["C\u1d48\u1d43\u1da0 [%]", "60\u201370", "75\u201390", "90\u201396"],
            ["V\u1d48\u1d43\u1da0 [%]", "45\u201355", "20\u201340", "3\u20138"],
            ["Q\u1d62\u02b3 [MJ/kg]", "10\u201320", "24\u201332", "30\u201335"],
            ["W\u02b3 [%]", "25\u201355", "3\u201315", "2\u20135"],
        ],
    )

    add_heading(doc, "2.2 Ur\u010dov\u00e1n\u00ed v\u00fdh\u0159evnosti", level=3)
    add_para(doc, "Metody:", keep_with_next=True)
    add_bullet(doc, "Kalorimetrick\u00e1 bomba \u2014 p\u0159\u00edm\u00e9 m\u011b\u0159en\u00ed spaln\u00e9ho tepla Q\u209b")
    add_bullet(doc, "V\u00fdpo\u010det z prvkov\u00e9ho rozboru \u2014 Mendělejevova rovnice:")
    add_equation(doc, r"Q_i^r = 33{,}91 C^r + 103{,}0 H^r - 10{,}89 (O^r - S^r) - 2{,}51 W^r \quad [\text{MJ/kg}]", label="4")
    add_bullet(doc, "Tabelov\u00e9 hodnoty pro standardn\u00ed paliva", is_last=True)

    add_heading(doc, "2.3 Trendy a ekologie", level=3)
    add_bullet(doc, "P\u0159echod od uhl\u00ed k zemn\u00edmu plynu (ni\u017e\u0161\u00ed emise CO\u2082 na jednotku energie)")
    add_bullet(doc, "Biomasa jako CO\u2082-neutr\u00e1ln\u00ed palivo (v r\u00e1mci \u017eivotn\u00edho cyklu)")
    add_bullet(doc, "Vod\u00edk jako palivo budoucnosti (nulov\u00e9 emise CO\u2082, ale v\u00fdroba?)")
    add_bullet(doc, "Spolusp\u00e1len\u00ed biomasy s uhl\u00edm (co-firing) \u2014 sni\u017eov\u00e1n\u00ed emis\u00ed", is_last=True)

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: V\u00fdpo\u010det v\u00fdh\u0159evnosti z prvkov\u00e9ho rozboru", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: \u010cern\u00e9 uhl\u00ed m\u00e1 surov\u00e9 slo\u017een\u00ed: C\u02b3 = 65 %, H\u02b3 = 4,5 %, "
        "O\u02b3 = 8 %, N\u02b3 = 1,2 %, S\u02b3 = 0,8 %, A\u02b3 = 12 %, W\u02b3 = 8,5 %. "
        "Ur\u010dete v\u00fdh\u0159evnost Mendělejevovou rovnic\u00ed.", bold=True)

    add_para(doc, "Krok 1: Kontrola bilance", bold=True)
    add_equation(doc, r"65 + 4{,}5 + 8 + 1{,}2 + 0{,}8 + 12 + 8{,}5 = 100{,}0 \% \quad \checkmark")

    add_para(doc, "Krok 2: Mend\u011blejevova rovnice", bold=True)
    add_equation(doc, r"Q_i^r = 33{,}91 \times 0{,}65 + 103{,}0 \times 0{,}045 - 10{,}89 \times (0{,}08 - 0{,}008) - 2{,}51 \times 0{,}085")
    add_equation(doc, r"Q_i^r = 22{,}04 + 4{,}64 - 0{,}78 - 0{,}21 = 25{,}69 \text{ MJ/kg}")

    add_para(doc, "Krok 3: Spaln\u00e9 teplo", bold=True)
    add_equation(doc, r"Q_s^r = Q_i^r + r(9H^r + W^r) = 25{,}69 + 2{,}454 \times (9 \times 0{,}045 + 0{,}085)")
    add_equation(doc, r"Q_s^r = 25{,}69 + 2{,}454 \times 0{,}49 = 25{,}69 + 1{,}20 = 26{,}89 \text{ MJ/kg}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "V\u00fdh\u0159evnost: Q\u1d62\u02b3 = 25,69 MJ/kg\n"
        "Spaln\u00e9 teplo: Q\u209b\u02b3 = 26,89 MJ/kg\n"
        "Rozd\u00edl Q\u209b \u2212 Q\u1d62 = 1,20 MJ/kg (kondenza\u010dn\u00ed teplo vodn\u00ed p\u00e1ry)\n\n"
        "Hodnoty odpov\u00eddaj\u00ed kvalitn\u00edmu \u010dern\u00e9mu uhl\u00ed. "
        "Rozd\u00edl Q\u209b \u2212 Q\u1d62 je mal\u00fd (4,5 %), proto\u017ee uhl\u00ed m\u00e1 relativn\u011b m\u00e1lo H a W.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Jak\u00fd je rozd\u00edl mezi spaln\u00fdm teplem a v\u00fdh\u0159evnost\u00ed?",
         "Spaln\u00e9 teplo Q\u209b zahrnuje kondenza\u010dn\u00ed teplo vodn\u00ed p\u00e1ry ve spalin\u00e1ch "
         "(p\u00e1ra zkondenzuje na kapalinu). V\u00fdh\u0159evnost Q\u1d62 toto teplo nezahrnuje "
         "(p\u00e1ra z\u016fst\u00e1v\u00e1 v plynn\u00e9 f\u00e1zi). V praxi se pou\u017e\u00edv\u00e1 Q\u1d62, "
         "proto\u017ee spaliny b\u011b\u017en\u011b nekondenzuj\u00ed (T > rosn\u00fd bod)."),

        ("Pro\u010d m\u00e1 vod\u00edk nejvy\u0161\u0161\u00ed v\u00fdh\u0159evnost na kg, ale ne na m\u00b3?",
         "Vod\u00edk m\u00e1 extr\u00e9mn\u011b n\u00edzkou hustotu (0,09 kg/m\u00b3 p\u0159i NTP). "
         "Na kg: Q\u1d62 = 120 MJ/kg (nejvy\u0161\u0161\u00ed). Na m\u00b3: Q\u1d62 = 10,8 MJ/m\u00b3 "
         "(ni\u017e\u0161\u00ed ne\u017e zemn\u00ed plyn 36 MJ/m\u00b3). Proto je skladov\u00e1n\u00ed H\u2082 probl\u00e9m."),

        ("Co jsou prchav\u00e9 ho\u0159laviny a jak ovliv\u0148uj\u00ed spalov\u00e1n\u00ed?",
         "L\u00e1tky uvol\u0148ovan\u00e9 z paliva p\u0159i zah\u0159\u00e1t\u00ed na 850\u2013900 \u00b0C bez p\u0159\u00edstupu vzduchu "
         "(uhlovod\u00edky, H\u2082, CO, dehty). Vysok\u00fd obsah (d\u0159evo 80 %) znamen\u00e1 snadn\u00e9 "
         "vzn\u00edcen\u00ed, ale i riziko p\u0159ilo\u017een\u00ed na p\u0159\u00edvod vzduchu. Antracit (V\u1d48\u1d43\u1da0 < 8 %) ho\u0159\u00ed pomalu."),

        ("Vysv\u011btlete t\u0159i zp\u016fsoby vyj\u00e1d\u0159en\u00ed slo\u017een\u00ed paliva (r, d, daf).",
         "r (raw/surov\u00e9) = skute\u010dn\u00fd stav v\u010detn\u011b vlhkosti a popela. "
         "d (dry/such\u00e9) = p\u0159epo\u010dten\u00e9 na bezvodn\u00fd stav. "
         "daf (dry ash-free) = pouze ho\u0159lavina bez vody a popela. "
         "P\u0159epo\u010dty: X\u1d48 = X\u02b3/(1 \u2212 W\u02b3), X\u1d48\u1d43\u1da0 = X\u1d48/(1 \u2212 A\u1d48)."),

        ("Pro\u010d je s\u00edra v palivu ne\u017e\u00e1douc\u00ed?",
         "S\u00edra p\u0159i spalov\u00e1n\u00ed tvo\u0159\u00ed SO\u2082 (a \u010d\u00e1ste\u010dn\u011b SO\u2083), "
         "kter\u00fd zp\u016fsobuje kysel\u00e9 de\u0161t\u011b. SO\u2083 s vodou tvo\u0159\u00ed H\u2082SO\u2084 \u2014 "
         "zvy\u0161uje kyselinov\u00fd rosn\u00fd bod spalin (a\u017e 150 \u00b0C), co\u017e vynucuje "
         "vy\u0161\u0161\u00ed teplotu spalin na v\u00fdstupu a sni\u017euje \u00fa\u010dinnost kotle."),

        ("Jak\u00fd je trend v energetice ohledn\u011b paliv?",
         "Od uhl\u00ed k plynu (ni\u017e\u0161\u00ed emise CO\u2082/kWh, \u017e\u00e1dn\u00e1 \u0161kv\u00e1ra). "
         "R\u016fst biomasy a odpadu jako paliv (co-firing, spalovny). "
         "Vod\u00edk jako potenci\u00e1ln\u00ed bezuhl\u00edkov\u00e9 palivo. "
         "Kondenza\u010dn\u00ed kotle vyu\u017e\u00edvaj\u00ed Q\u209b (ne jen Q\u1d62) \u2014 \u00fa\u010dinnost > 100 % dle Q\u1d62."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M. a kol.: Spalov\u00e1n\u00ed a spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cSN ISO 1928 \u2014 Stanoven\u00ed spaln\u00e9ho tepla")
    add_bullet(doc, "Perry's Chemical Engineers' Handbook \u2014 Properties of Fuels")
    add_bullet(doc, "IEA World Energy Outlook \u2014 statistiky spot\u0159eby paliv", is_last=True)

    save_and_export(doc, "14-paliva")


if __name__ == "__main__":
    generate()
