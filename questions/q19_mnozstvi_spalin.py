# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 19: V\u00fdpo\u010det mno\u017estv\u00ed spalin pro spalov\u00e1n\u00ed tuh\u00fdch paliv.
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

def generate_flue_gas_composition():
    """Pie chart of flue gas composition for typical coal combustion."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # Stoichiometric (n=1)
    labels1 = ["CO\u2082", "H\u2082O", "SO\u2082", "N\u2082"]
    vals1 = [14.5, 5.5, 0.2, 79.8]
    colors1 = [COLORS[1], COLORS[0], "#D97706", "#7C3AED"]
    ax1.pie(vals1, labels=labels1, autopct="%1.1f%%", colors=colors1, startangle=90,
            textprops={"fontsize": 10})
    ax1.set_title("Stechiometrick\u00e9 (n = 1)", fontsize=11, fontweight="bold")

    # With excess air (n=1.3)
    labels2 = ["CO\u2082", "H\u2082O", "SO\u2082", "O\u2082", "N\u2082"]
    vals2 = [11.8, 4.5, 0.15, 4.55, 79.0]
    colors2 = [COLORS[1], COLORS[0], "#D97706", COLORS[2], "#7C3AED"]
    ax2.pie(vals2, labels=labels2, autopct="%1.1f%%", colors=colors2, startangle=90,
            textprops={"fontsize": 10})
    ax2.set_title("S p\u0159ebytkem (n = 1,3)", fontsize=11, fontweight="bold")

    fig.suptitle("Objemov\u00e9 slo\u017een\u00ed spalin \u010dern\u00e9ho uhl\u00ed", fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q19_flue_composition.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_flue_gas_volume():
    """Flue gas volume vs excess air coefficient."""
    fig, ax = plt.subplots(figsize=(7, 5))

    n = np.linspace(1.0, 2.0, 100)
    # Typical coal: V_sp_min ~ 7.0 m3/kg, V_vz_min ~ 6.74 m3/kg
    V_sp_min = 7.0
    V_vz_min = 6.74
    V_sp = V_sp_min + (n - 1) * V_vz_min

    ax.plot(n, V_sp, color=COLORS[0], linewidth=2.5, label="$V_{sp}$ (celkov\u00e9 spaliny)")
    ax.axhline(y=V_sp_min, color=COLORS[2], linewidth=1.5, linestyle="--", alpha=0.6,
               label=f"$V_{{sp,min}}$ = {V_sp_min:.1f} m\u00b3/kg")

    # Fill excess
    ax.fill_between(n, V_sp_min, V_sp, alpha=0.1, color=COLORS[0])
    ax.text(1.5, V_sp_min + 1.5, "P\u0159ebyte\u010dn\u00fd\nvzduch", fontsize=10,
            ha="center", style="italic", color=COLORS[0])

    ax.set_xlabel("P\u0159ebytek vzduchu n [-]", fontsize=11)
    ax.set_ylabel("Objem spalin $V_{sp}$ [m\u00b3_N/kg]", fontsize=11)
    ax.set_title("Z\u00e1vislost objemu spalin na p\u0159ebytku vzduchu",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(1, 2)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q19_flue_volume.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_comp = generate_flue_gas_composition()
    img_vol = generate_flue_gas_volume()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="19. V\u00fdpo\u010det mno\u017estv\u00ed spalin pro spalov\u00e1n\u00ed tuh\u00fdch paliv.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Odvo\u010fte vztahy pro v\u00fdpo\u010det mno\u017estv\u00ed a slo\u017een\u00ed spalin p\u0159i spalov\u00e1n\u00ed "
        "tuh\u00fdch paliv. Rozli\u0161te such\u00e9 a vlhk\u00e9 spaliny, stechiometrick\u00e9 a se skute\u010dn\u00fdm "
        "p\u0159ebytkem vzduchu.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Slo\u017eky spalin", level=3)

    add_info_box(doc,
        "Slo\u017een\u00ed spalin p\u0159i \u00fapln\u00e9m spalov\u00e1n\u00ed",
        "CO\u2082 (z uhl\u00edku) + H\u2082O (z vod\u00edku a vlhkosti) + SO\u2082 (ze s\u00edry) + "
        "N\u2082 (ze vzduchu a paliva) + p\u0159\u00edpadn\u011b O\u2082 (p\u0159ebyte\u010dn\u00fd)")

    add_para(doc, "Rozd\u011blen\u00ed:", keep_with_next=True)
    add_bullet(doc, "Such\u00e9 spaliny = CO\u2082 + SO\u2082 + N\u2082 + O\u2082 (bez H\u2082O)")
    add_bullet(doc, "Vlhk\u00e9 spaliny = such\u00e9 spaliny + H\u2082O", is_last=True)

    # -- 1.2 Stechiometricke --
    add_heading(doc, "1.2 Stechiometrick\u00e9 objemy jednotliv\u00fdch slo\u017eek", level=3)

    add_para(doc, "Objem CO\u2082:", keep_with_next=True)
    add_equation(doc, r"V_{CO_2} = 1{,}868 \, C^r \quad [\text{m}^3_N / \text{kg}]", label="1")

    add_para(doc, "Objem SO\u2082:", keep_with_next=True)
    add_equation(doc, r"V_{SO_2} = 0{,}700 \, S^r \quad [\text{m}^3_N / \text{kg}]", label="2")

    add_para(doc, "Objem N\u2082 (ze vzduchu + z paliva):", keep_with_next=True)
    add_equation(doc, r"V_{N_2} = 0{,}79 \, V_{vz,min} + 0{,}800 \, N^r \quad [\text{m}^3_N / \text{kg}]", label="3")

    add_para(doc, "Objem H\u2082O (z vod\u00edku + z vlhkosti + z vlhkosti vzduchu):", keep_with_next=True)
    add_equation(doc, r"V_{H_2O} = 11{,}2 \, H^r + 1{,}244 \, W^r + 1{,}61 \, x \, V_{vz,min}", label="4")

    add_para(doc, "kde x je m\u011brn\u00e1 vlhkost vzduchu [kg/kg s.v.], typicky x \u2248 0,01.")

    add_para(doc, "Celkov\u00fd objem stechiometrick\u00fdch spalin:", bold=True, keep_with_next=True)

    add_para(doc, "Such\u00e9:", keep_with_next=True)
    add_equation(doc, r"V_{sp,min}^{such\acute{e}} = V_{CO_2} + V_{SO_2} + V_{N_2}", label="5")

    add_para(doc, "Vlhk\u00e9:", keep_with_next=True)
    add_equation(doc, r"V_{sp,min}^{vlhk\acute{e}} = V_{sp,min}^{such\acute{e}} + V_{H_2O}", label="6")

    # -- 1.3 Se skutecnym prebytkem --
    add_page_break(doc)
    add_heading(doc, "1.3 Spaliny p\u0159i skute\u010dn\u00e9m p\u0159ebytku vzduchu", level=3)

    add_para(doc, "P\u0159i p\u0159ebytku n > 1 se ve spalin\u00e1ch objev\u00ed p\u0159ebyte\u010dn\u00fd O\u2082 a dal\u0161\u00ed N\u2082:", keep_with_next=True)

    add_equation(doc, r"V_{sp}^{such\acute{e}} = V_{sp,min}^{such\acute{e}} + (n - 1) \, V_{vz,min}", label="7")
    add_equation(doc, r"V_{sp}^{vlhk\acute{e}} = V_{sp,min}^{vlhk\acute{e}} + (n - 1) \, V_{vz,min} (1 + 1{,}61 x)", label="8")

    add_para(doc, "P\u0159ebyte\u010dn\u00fd kysl\u00edk:", keep_with_next=True)
    add_equation(doc, r"V_{O_2} = 0{,}21 (n - 1) V_{vz,min}", label="9")

    add_image(doc, img_vol, width_cm=13,
              caption="Obr. 1: Objem spalin line\u00e1rn\u011b roste s p\u0159ebytkem vzduchu")

    # -- 1.4 Koncentrace slozek --
    add_heading(doc, "1.4 Objemov\u00e9 koncentrace slo\u017eek spalin", level=3)

    add_equation(doc, r"c_{CO_2} = \frac{V_{CO_2}}{V_{sp}^{such\acute{e}}} \times 100 \quad [\%]", label="10")

    add_para(doc,
        "Maxim\u00e1ln\u00ed koncentrace CO\u2082 (p\u0159i n = 1) se ozna\u010duje CO\u2082_max a z\u00e1vis\u00ed "
        "na palivu. Pro \u010dern\u00e9 uhl\u00ed: CO\u2082_max \u2248 18\u201319 %, pro zemn\u00ed plyn \u2248 11\u201312 %.")

    add_image(doc, img_comp, width_cm=14,
              caption="Obr. 2: Objemov\u00e9 slo\u017een\u00ed spalin \u010dern\u00e9ho uhl\u00ed \u2014 stechiometrick\u00e9 vs. s p\u0159ebytkem")

    # -- 1.5 Hmotnostni --
    add_page_break(doc)
    add_heading(doc, "1.5 Hmotnostn\u00ed bilance spalin", level=3)

    add_para(doc, "Alternativn\u011b lze po\u010d\u00edtat hmotnostn\u011b:", keep_with_next=True)
    add_equation(doc, r"m_{sp,min} = m_{CO_2} + m_{SO_2} + m_{N_2} + m_{H_2O}", label="11")
    add_equation(doc, r"m_{sp,min} = 3{,}667 C^r + 2 S^r + 0{,}768 m_{vz,min} + 9 H^r + W^r", label="12")

    add_info_box(doc,
        "Kontrola: z\u00e1kon zachov\u00e1n\u00ed hmotnosti",
        "m_{palivo} + m_{vzduch} = m_{spaliny} + m_{popel}\n"
        "Tato rovnice mus\u00ed v\u017edy platit. Je to z\u00e1kladn\u00ed kontrola spr\u00e1vnosti v\u00fdpo\u010dtu.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 CO\u2082_max pro r\u016fzn\u00e1 paliva", level=3)
    add_styled_table(doc,
        headers=["Palivo", "CO\u2082_max [%]"],
        data=[
            ["Uhl\u00edk (\u010dist\u00fd C)", "21,0"],
            ["\u010cern\u00e9 uhl\u00ed", "18\u201319"],
            ["Hn\u011bd\u00e9 uhl\u00ed", "17\u201319"],
            ["T\u011b\u017ek\u00fd topn\u00fd olej", "15\u201316"],
            ["Zemn\u00ed plyn (CH\u2084)", "11\u201312"],
            ["Vod\u00edk (H\u2082)", "0 (!)"],
        ],
    )

    add_heading(doc, "2.2 Rosn\u00fd bod spalin", level=3)
    add_para(doc,
        "Vodn\u00ed p\u00e1ra ve spalin\u00e1ch m\u00e1 ur\u010dit\u00fd parci\u00e1ln\u00ed tlak. Rosn\u00fd bod spalin "
        "z\u00e1vis\u00ed na obsahu H\u2082O a S (kyselinov\u00fd rosn\u00fd bod). "
        "Typick\u00e9 hodnoty:", keep_with_next=True)
    add_bullet(doc, "Zemn\u00ed plyn (bezs\u00edr\u00fd): T_r \u2248 55 \u00b0C")
    add_bullet(doc, "\u010cern\u00e9 uhl\u00ed (S < 1 %): T_r \u2248 45 \u00b0C, kyselinov\u00fd T_r \u2248 110\u2013130 \u00b0C")
    add_bullet(doc, "T\u011b\u017ek\u00fd TO (S > 2 %): kyselinov\u00fd T_r \u2248 140\u2013150 \u00b0C", is_last=True)

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Spaliny \u010dern\u00e9ho uhl\u00ed", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: \u010cern\u00e9 uhl\u00ed (C\u02b3=65%, H\u02b3=4,5%, O\u02b3=8%, N\u02b3=1,2%, S\u02b3=0,8%, "
        "A\u02b3=12%, W\u02b3=8,5%). V_{vz,min} = 6,74 m\u00b3_N/kg (z Q18). "
        "P\u0159ebytek n = 1,3. Ur\u010dete objem a slo\u017een\u00ed such\u00fdch spalin.",
        bold=True)

    add_para(doc, "Krok 1: Slo\u017eky stechiometrick\u00fdch spalin", bold=True)
    add_equation(doc, r"V_{CO_2} = 1{,}868 \times 0{,}65 = 1{,}214 \text{ m}^3_N/\text{kg}")
    add_equation(doc, r"V_{SO_2} = 0{,}700 \times 0{,}008 = 0{,}006 \text{ m}^3_N/\text{kg}")
    add_equation(doc, r"V_{N_2} = 0{,}79 \times 6{,}74 + 0{,}800 \times 0{,}012 = 5{,}325 + 0{,}010 = 5{,}335 \text{ m}^3_N/\text{kg}")

    add_para(doc, "Krok 2: Stechiometrick\u00e9 such\u00e9 spaliny", bold=True)
    add_equation(doc, r"V_{sp,min}^{s} = 1{,}214 + 0{,}006 + 5{,}335 = 6{,}555 \text{ m}^3_N/\text{kg}")

    add_para(doc, "Krok 3: Skute\u010dn\u00e9 such\u00e9 spaliny (n = 1,3)", bold=True)
    add_equation(doc, r"V_{sp}^{s} = 6{,}555 + (1{,}3 - 1) \times 6{,}74 = 6{,}555 + 2{,}022 = 8{,}577 \text{ m}^3_N/\text{kg}")

    add_para(doc, "Krok 4: Slo\u017een\u00ed such\u00fdch spalin", bold=True)
    add_styled_table(doc,
        headers=["Slo\u017eka", "Objem [m\u00b3_N/kg]", "Pod\u00edl [%]"],
        data=[
            ["CO\u2082", "1,214", "14,2"],
            ["SO\u2082", "0,006", "0,1"],
            ["N\u2082", "5,335 + 0,79\u00d72,022 = 6,932", "80,8"],
            ["O\u2082", "0,21\u00d72,022 = 0,425", "5,0"],
            ["Celkem", "8,577", "100,0"],
        ],
    )

    add_info_box(doc,
        "V\u00fdsledky:",
        "V_{sp,min}(such\u00e9) = 6,56 m\u00b3_N/kg | V_{sp}(such\u00e9, n=1,3) = 8,58 m\u00b3_N/kg\n"
        "CO\u2082 = 14,2 % (< CO\u2082_max = 18,5 %, proto\u017ee n > 1)\n"
        "O\u2082 = 5,0 % (potvrzuje p\u0159ebytek vzduchu)")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Jak\u00fd je rozd\u00edl mezi such\u00fdmi a vlhk\u00fdmi spalinami?",
         "Such\u00e9 spaliny neobsahuj\u00ed vodn\u00ed p\u00e1ru: CO\u2082 + SO\u2082 + N\u2082 + O\u2082. "
         "Vlhk\u00e9 spaliny zahrnuj\u00ed i H\u2082O. Such\u00e9 spaliny se pou\u017e\u00edvaj\u00ed pro anal\u00fdzu "
         "(analyzátory pracuj\u00ed se such\u00fdm vzorkem), vlhk\u00e9 pro objemov\u00e9 v\u00fdpo\u010dty."),

        ("Pro\u010d kles\u00e1 koncentrace CO\u2082 s rostouc\u00edm p\u0159ebytkem vzduchu?",
         "Mno\u017estv\u00ed CO\u2082 je d\u00e1no palivem a nem\u011bn\u00ed se s n. Ale celkov\u00fd objem spalin "
         "roste (p\u0159\u00eddavn\u00fd vzduch). Zlomek V_{CO\u2082}/V_{sp} proto kles\u00e1. "
         "CO\u2082_max nastane p\u0159i n = 1."),

        ("Co znamen\u00e1 CO\u2082_max a jak se pou\u017e\u00edv\u00e1?",
         "Maxim\u00e1ln\u00ed mo\u017en\u00e1 koncentrace CO\u2082 v such\u00fdch spalin\u00e1ch (p\u0159i n = 1). "
         "Z\u00e1vis\u00ed na palivu (uhl\u00ed ~19 %, ZP ~12 %). Pou\u017e\u00edv\u00e1 se pro ur\u010den\u00ed "
         "p\u0159ebytku vzduchu z m\u011b\u0159en\u00e9 koncentrace CO\u2082."),

        ("Jak z anal\u00fdzy spalin ur\u010d\u00edte p\u0159ebytek vzduchu?",
         "Z koncentrace O\u2082 v such\u00fdch spalin\u00e1ch: n = 21/(21 \u2212 O\u2082[%]). "
         "Alternativn\u011b z CO\u2082: n = CO\u2082_max/CO\u2082. Ob\u011b metody by m\u011bly d\u00e1t "
         "stejn\u00fd v\u00fdsledek (za p\u0159edpokladu \u00fapln\u00e9ho sp\u00e1len\u00ed)."),

        ("Pro\u010d je zn\u00e1m\u00fd rosn\u00fd bod spalin d\u016fle\u017eit\u00fd pro n\u00e1vrh kotle?",
         "Teplota spalin na v\u00fdstupu mus\u00ed b\u00fdt vy\u0161\u0161\u00ed ne\u017e rosn\u00fd bod, "
         "jinak kondenzuje voda (a p\u0159\u00edpadn\u011b H\u2082SO\u2084) na st\u011bn\u00e1ch spalinov\u00e9ho traktu. "
         "To omezuje vyu\u017eit\u00ed tepla spalin a sni\u017euje \u00fa\u010dinnost kotle."),

        ("Pro\u010d vod\u00edk nem\u00e1 CO\u2082_max?",
         "Proto\u017ee spalov\u00e1n\u00edm H\u2082 nevznik\u00e1 \u017e\u00e1dn\u00fd CO\u2082 \u2014 produktem je jen H\u2082O. "
         "Such\u00e9 spaliny obsahuj\u00ed pouze N\u2082 (a p\u0159\u00edpadn\u011b p\u0159ebyte\u010dn\u00fd O\u2082). "
         "CO\u2082_max = 0 %."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M. a kol.: Spalov\u00e1n\u00ed a spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cSN 07 0302 \u2014 V\u00fdpo\u010det spalov\u00e1n\u00ed tuh\u00fdch paliv")
    add_bullet(doc, "Glassman, I.: Combustion, 5th Ed.")
    add_bullet(doc, "VDI 2066 \u2014 M\u011b\u0159en\u00ed spalin", is_last=True)

    save_and_export(doc, "19-mnozstvi-spalin")


if __name__ == "__main__":
    generate()
