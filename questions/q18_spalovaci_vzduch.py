# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 18: V\u00fdpo\u010det mno\u017estv\u00ed spalovac\u00edho vzduchu pro spalov\u00e1n\u00ed tuh\u00fdch paliv.
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

def generate_air_need_chart():
    """Bar chart of stoichiometric air need for different fuels."""
    fig, ax = plt.subplots(figsize=(8, 5))

    fuels = ["Vod\u00edk", "Zemn\u00ed plyn", "T\u011b\u017ek\u00fd TO", "Benzin",
             "\u010cern\u00e9 uhl\u00ed", "Hn\u011bd\u00e9 uhl\u00ed", "D\u0159evo", "Ra\u0161elina"]
    Vvz = [26.7, 9.5, 10.8, 11.6, 7.5, 4.5, 3.8, 2.5]  # m3_N/kg

    colors_bar = [COLORS[2]] + [COLORS[3]] * 3 + [COLORS[1]] * 2 + [COLORS[2]] * 2

    bars = ax.barh(fuels, Vvz, color=colors_bar, edgecolor="white", height=0.6)
    for bar, val in zip(bars, Vvz):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
                f"{val:.1f} m\u00b3_N/kg", va="center", fontsize=9, fontweight="bold")

    ax.set_xlabel("Stechiometrick\u00fd objem vzduchu $V_{vz,min}$ [m\u00b3_N/kg]", fontsize=11)
    ax.set_title("Pot\u0159eba vzduchu pro spalov\u00e1n\u00ed r\u016fzn\u00fdch paliv", fontsize=12, fontweight="bold")
    ax.set_xlim(0, 30)
    ax.invert_yaxis()

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q18_air_need.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_air_vs_heating_value():
    """Correlation between air need and heating value."""
    fig, ax = plt.subplots(figsize=(7, 5))

    Qi = np.array([120, 34, 42, 43.5, 25.7, 17, 15, 9])
    Vvz = np.array([26.7, 9.5, 10.8, 11.6, 7.5, 4.5, 3.8, 2.5])
    labels = ["H\u2082", "ZP", "TO", "Benzin", "\u010cU", "HU", "D\u0159evo", "Ra\u0161."]

    ax.scatter(Qi, Vvz, s=100, c=COLORS[0], zorder=5)
    for x, y, lbl in zip(Qi, Vvz, labels):
        ax.annotate(lbl, (x, y), textcoords="offset points", xytext=(5, 5), fontsize=9)

    # Linear fit (exclude H2 as outlier)
    mask = Qi < 50
    z = np.polyfit(Qi[mask], Vvz[mask], 1)
    x_fit = np.linspace(5, 50, 100)
    ax.plot(x_fit, np.polyval(z, x_fit), "--", color="gray", linewidth=1.5, alpha=0.6,
            label=f"Trend: V$_{{vz}}$ \u2248 {z[0]:.2f}\u00b7Q$_i$ {z[1]:+.1f}")

    ax.set_xlabel("V\u00fdh\u0159evnost $Q_i^r$ [MJ/kg]", fontsize=11)
    ax.set_ylabel("$V_{vz,min}$ [m\u00b3_N/kg]", fontsize=11)
    ax.set_title("Korelace mezi v\u00fdh\u0159evnost\u00ed a pot\u0159ebou vzduchu",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q18_air_vs_qi.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_air = generate_air_need_chart()
    img_corr = generate_air_vs_heating_value()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="18. V\u00fdpo\u010det mno\u017estv\u00ed spalovac\u00edho vzduchu pro spalov\u00e1n\u00ed tuh\u00fdch paliv.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Odvo\u010fte vztahy pro v\u00fdpo\u010det minim\u00e1ln\u00edho (stechiometrick\u00e9ho) mno\u017estv\u00ed "
        "spalovac\u00edho vzduchu z prvkov\u00e9ho rozboru tuh\u00e9ho paliva. Uve\u010fte hmotnostní "
        "i objemov\u00e9 vyj\u00e1d\u0159en\u00ed.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 V\u00fdchoz\u00ed \u00favahy", level=3)

    add_info_box(doc,
        "Princip v\u00fdpo\u010dtu",
        "Stechiometrick\u00e9 mno\u017estv\u00ed vzduchu se ur\u010d\u00ed s\u010dten\u00edm pot\u0159eb kysl\u00edku "
        "pro sp\u00e1len\u00ed ka\u017ed\u00e9ho ho\u0159lav\u00e9ho prvku (C, H, S), p\u0159i\u010dem\u017e se ode\u010dte "
        "kysl\u00edk ji\u017e obsa\u017een\u00fd v palivu (O\u02b3).")

    add_para(doc, "Stechiometrick\u00e9 rovnice (z Q16 a Q17):", keep_with_next=True)
    add_styled_table(doc,
        headers=["Prvek", "Rovnice", "O\u2082 [kg/kg prvku]", "O\u2082 [m\u00b3_N/kg prvku]"],
        data=[
            ["C", "C + O\u2082 \u2192 CO\u2082", "2,667 (= 32/12)", "1,868"],
            ["H", "2H\u2082 + O\u2082 \u2192 2H\u2082O", "8,000 (= 16/2)", "5,600"],
            ["S", "S + O\u2082 \u2192 SO\u2082", "1,000 (= 32/32)", "0,700"],
        ],
    )

    # -- 1.2 Hmotnostni --
    add_heading(doc, "1.2 Hmotnostn\u00ed mno\u017estv\u00ed kysl\u00edku a vzduchu", level=3)

    add_para(doc, "Minim\u00e1ln\u00ed pot\u0159eba kysl\u00edku na 1 kg surov\u00e9ho paliva:", keep_with_next=True)
    add_equation(doc, r"m_{O_2,min} = 2{,}667 C^r + 8 H^r + S^r - O^r", label="1")

    add_para(doc,
        "kde C\u02b3, H\u02b3, S\u02b3, O\u02b3 jsou hmotnostn\u00ed pod\u00edly ho\u0159lav\u00fdch prvk\u016f a kysl\u00edku "
        "v surov\u00e9m palivu. Ode\u010dten\u00ed O\u02b3 proto\u017ee tento kysl\u00edk je ji\u017e v palivu "
        "a nemus\u00ed se dod\u00e1vat ze vzduchu.")

    add_para(doc, "Minim\u00e1ln\u00ed mno\u017estv\u00ed vzduchu:", keep_with_next=True)
    add_equation(doc, r"m_{vz,min} = \frac{m_{O_2,min}}{0{,}232}", label="2")

    add_para(doc, "kde 0,232 je hmotnostn\u00ed pod\u00edl O\u2082 v such\u00e9m vzduchu.")

    # -- 1.3 Objemove --
    add_page_break(doc)
    add_heading(doc, "1.3 Objemov\u00e9 mno\u017estv\u00ed kysl\u00edku a vzduchu", level=3)

    add_para(doc, "P\u0159i norm\u00e1ln\u00edch podm\u00ednk\u00e1ch (0 \u00b0C, 101,325 kPa):", keep_with_next=True)
    add_equation(doc, r"V_{O_2,min} = 1{,}868 C^r + 5{,}6 H^r + 0{,}7 S^r - 0{,}7 O^r \quad [\text{m}^3_N / \text{kg}]", label="3")

    add_para(doc, "Minim\u00e1ln\u00ed objem vzduchu:", keep_with_next=True)
    add_equation(doc, r"V_{vz,min} = \frac{V_{O_2,min}}{0{,}21} \quad [\text{m}^3_N / \text{kg}]", label="4")

    add_para(doc, "kde 0,21 je objemov\u00fd pod\u00edl O\u2082 v such\u00e9m vzduchu.")

    add_info_box(doc,
        "Zjednodu\u0161en\u00fd odhad (Rosinova formule)",
        "Pro tuh\u00e1 paliva existuje p\u0159ibli\u017en\u00fd vztah:\n"
        "V_{vz,min} \u2248 0,260 \u00d7 Q\u1d62\u02b3 [m\u00b3_N/kg]\n"
        "kde Q\u1d62\u02b3 je v\u00fdh\u0159evnost v MJ/kg. Chyba < 5 % pro b\u011b\u017en\u00e1 tuh\u00e1 paliva.")

    # -- 1.4 Skutecne mnozstvi --
    add_heading(doc, "1.4 Skute\u010dn\u00e9 mno\u017estv\u00ed vzduchu", level=3)

    add_para(doc, "Se zapo\u010dten\u00edm p\u0159ebytku vzduchu n:", keep_with_next=True)
    add_equation(doc, r"V_{vz} = n \cdot V_{vz,min}", label="5")
    add_equation(doc, r"m_{vz} = n \cdot m_{vz,min}", label="6")

    add_styled_table(doc,
        headers=["Typ spalov\u00e1n\u00ed", "Typick\u00fd p\u0159ebytek n"],
        data=[
            ["Pr\u00e1\u0161kov\u00e9 spalov\u00e1n\u00ed uhl\u00ed", "1,15\u20131,25"],
            ["Ro\u0161tov\u00e9 spalov\u00e1n\u00ed uhl\u00ed", "1,30\u20131,50"],
            ["Fluidn\u00ed spalov\u00e1n\u00ed", "1,15\u20131,25"],
            ["Spalov\u00e1n\u00ed zemn\u00edho plynu", "1,05\u20131,15"],
            ["Spalov\u00e1n\u00ed oleje", "1,10\u20131,20"],
        ],
    )

    add_image(doc, img_air, width_cm=13,
              caption="Obr. 1: Stechiometrick\u00e9 mno\u017estv\u00ed vzduchu pro r\u016fzn\u00e1 paliva")

    add_image(doc, img_corr, width_cm=12,
              caption="Obr. 2: Korelace mezi v\u00fdh\u0159evnost\u00ed a pot\u0159ebou vzduchu \u2014 p\u0159ibli\u017en\u011b line\u00e1rn\u00ed z\u00e1vislost")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Vliv vlhkosti vzduchu", level=3)
    add_para(doc,
        "Sku\u010dte\u010dn\u00fd vzduch obsahuje vodní p\u00e1ru. P\u0159i v\u00fdpo\u010dtu se m\u016f\u017ee vlhkost "
        "zohlednit korekc\u00ed:", keep_with_next=True)
    add_equation(doc, r"V_{vz,vlhk\acute{y}} = V_{vz,such\acute{y}} (1 + 1{,}61 x)", label="7")
    add_para(doc, "kde x je m\u011brn\u00e1 vlhkost vzduchu [kg/kg s.v.]. "
             "Typicky x = 0,01 kg/kg \u2192 korekce +1,6 %.")

    add_heading(doc, "2.2 V\u011btr\u00e1n\u00ed paliva", level=3)
    add_para(doc,
        "Kysl\u00edk obsa\u017een\u00fd v palivu (O\u02b3) sni\u017euje pot\u0159ebu vzduchu. "
        "D\u0159evo a biomasa maj\u00ed vysok\u00fd O\u02b3 (35\u201345 %) \u2014 proto pot\u0159ebuj\u00ed "
        "m\u00e9n\u011b vzduchu ne\u017e uhl\u00ed p\u0159i stejn\u00e9 v\u00fdh\u0159evnosti.")

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: V\u00fdpo\u010det pot\u0159eby vzduchu pro \u010dern\u00e9 uhl\u00ed", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: \u010cern\u00e9 uhl\u00ed m\u00e1 slo\u017een\u00ed: C\u02b3 = 65 %, H\u02b3 = 4,5 %, "
        "O\u02b3 = 8 %, N\u02b3 = 1,2 %, S\u02b3 = 0,8 %, A\u02b3 = 12 %, W\u02b3 = 8,5 %. "
        "P\u0159ebytek vzduchu n = 1,3. Ur\u010dete stechiometrick\u00fd a skute\u010dn\u00fd objem vzduchu.",
        bold=True)

    add_para(doc, "Krok 1: Stechiometrick\u00fd objem O\u2082", bold=True)
    add_equation(doc, r"V_{O_2,min} = 1{,}868 \times 0{,}65 + 5{,}6 \times 0{,}045 + 0{,}7 \times 0{,}008 - 0{,}7 \times 0{,}08")
    add_equation(doc, r"V_{O_2,min} = 1{,}214 + 0{,}252 + 0{,}006 - 0{,}056 = 1{,}416 \text{ m}^3_N / \text{kg}")

    add_para(doc, "Krok 2: Stechiometrick\u00fd objem vzduchu", bold=True)
    add_equation(doc, r"V_{vz,min} = \frac{1{,}416}{0{,}21} = 6{,}743 \text{ m}^3_N / \text{kg}")

    add_para(doc, "Krok 3: Skute\u010dn\u00fd objem vzduchu", bold=True)
    add_equation(doc, r"V_{vz} = 1{,}3 \times 6{,}743 = 8{,}766 \text{ m}^3_N / \text{kg}")

    add_para(doc, "Krok 4: Kontrola Rosinovou formulí", bold=True)
    add_equation(doc, r"V_{vz,min} \approx 0{,}260 \times Q_i^r = 0{,}260 \times 25{,}7 = 6{,}68 \text{ m}^3_N / \text{kg}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "V_{O\u2082,min} = 1,416 m\u00b3_N/kg\n"
        "V_{vz,min} = 6,74 m\u00b3_N/kg (stechiometrick\u00fd)\n"
        "V_{vz} = 8,77 m\u00b3_N/kg (s p\u0159ebytkem n = 1,3)\n\n"
        "Rosinova formule d\u00e1v\u00e1 6,68 m\u00b3_N/kg \u2014 shoda s p\u0159esn\u00fdm v\u00fdpo\u010dtem do 1 %.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d se od pot\u0159eby O\u2082 ode\u010d\u00edt\u00e1 kysl\u00edk obsa\u017een\u00fd v palivu?",
         "Kysl\u00edk v palivu O\u02b3 je ji\u017e v\u00e1z\u00e1n v ho\u0159lavin\u011b a \u010d\u00e1ste\u010dn\u011b pokr\u00fdv\u00e1 "
         "pot\u0159ebu O\u2082 pro oxidaci. Nemus\u00ed se dod\u00e1vat ze vzduchu. "
         "D\u0159evo (O\u02b3 \u2248 40 %) pot\u0159ebuje v\u00fdrazn\u011b m\u00e9n\u011b vzduchu ne\u017e uhl\u00ed (O\u02b3 \u2248 5\u201310 %)."),

        ("Vysv\u011btlete Rosinovu p\u0159ibli\u017enou formuli V_{vz,min} \u2248 0,260 Q\u1d62.",
         "Empirick\u00e1 korelace zalo\u017een\u00e1 na tom, \u017ee paliva s vy\u0161\u0161\u00ed v\u00fdh\u0159evnost\u00ed "
         "pot\u0159ebuj\u00ed v\u00edce vzduchu p\u0159ibli\u017en\u011b line\u00e1rn\u011b. Funguje dob\u0159e pro "
         "b\u011b\u017en\u00e1 tuh\u00e1 a kapaln\u00e1 paliva (chyba < 5 %). "
         "Nehodí se pro H\u2082 a neobvykl\u00e1 paliva."),

        ("Pro\u010d se v praxi spaluje s p\u0159ebytkem vzduchu?",
         "P\u0159i n = 1 by nedokonalost m\u00edsen\u00ed paliva se vzduchem vedla k lok\u00e1ln\u00edmu "
         "nedostatku O\u2082 a ne\u00fapln\u00e9mu sp\u00e1len\u00ed (CO, saze). P\u0159ebytek zaji\u0161\u0165uje, "
         "\u017ee ka\u017ed\u00e1 \u010d\u00e1stice paliva m\u00e1 dostatek O\u2082."),

        ("Jak\u00fd je rozd\u00edl mezi such\u00fdm a vlhk\u00fdm vzduchem ve v\u00fdpo\u010dtu?",
         "Such\u00fd vzduch: 21 % O\u2082 + 79 % N\u2082 (objemov\u011b). "
         "Vlhk\u00fd vzduch obsahuje vodn\u00ed p\u00e1ru \u2014 z\u0159e\u010fuje O\u2082 a N\u2082, "
         "tak\u017ee na stejn\u00e9 mno\u017estv\u00ed O\u2082 pot\u0159ebujeme o ~1\u20132 % v\u011bt\u0161\u00ed objem vzduchu."),

        ("Pro\u010d ro\u0161tov\u00e9 oh\u0159ívače pot\u0159ebuj\u00ed v\u011bt\u0161\u00ed p\u0159ebytek vzduchu ne\u017e pr\u00e1\u0161kov\u00e9?",
         "U pr\u00e1\u0161kov\u00e9ho spalov\u00e1n\u00ed je palivo jemn\u011b namlet\u00e9 \u2014 velk\u00fd povrch, "
         "dobr\u00e9 m\u00edsen\u00ed se vzduchem. U ro\u0161tu ho\u0159\u00ed kusy uhl\u00ed \u2014 hor\u0161\u00ed kontakt "
         "s O\u2082, proto n = 1,3\u20131,5 vs. 1,15\u20131,25 u pr\u00e1\u0161ku."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M. a kol.: Spalov\u00e1n\u00ed a spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cSN 07 0302 \u2014 V\u00fdpo\u010det spalov\u00e1n\u00ed tuh\u00fdch paliv")
    add_bullet(doc, "Kozub\u00edk, T.: Spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Glassman, I.: Combustion, 5th Ed.", is_last=True)

    save_and_export(doc, "18-spalovaci-vzduch")


if __name__ == "__main__":
    generate()
