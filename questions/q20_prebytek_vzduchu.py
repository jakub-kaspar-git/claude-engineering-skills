# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 20: P\u0159ebytek spalovac\u00edho vzduchu.
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

def generate_excess_air_effects():
    """Effect of excess air on efficiency, CO, NOx."""
    fig, ax1 = plt.subplots(figsize=(8, 5.5))

    n = np.linspace(0.8, 2.0, 200)

    # Efficiency curve (peak around n=1.1-1.2)
    eta = 92 - 5 * (n - 1.15)**2 * 100 - np.where(n < 1.0, 30 * (1 - n)**2 * 100, 0)
    eta = np.clip(eta, 50, 93)

    ax1.plot(n, eta, color=COLORS[0], linewidth=2.5, label="\u00da\u010dinnost kotle \u03b7 [%]")
    ax1.set_xlabel("P\u0159ebytek vzduchu n [-]", fontsize=11)
    ax1.set_ylabel("\u00da\u010dinnost \u03b7 [%]", fontsize=11, color=COLORS[0])
    ax1.tick_params(axis="y", labelcolor=COLORS[0])

    # CO and NOx on secondary axis
    ax2 = ax1.twinx()

    # CO: high at n<1, drops sharply to near-zero at n>1.05
    CO = np.where(n < 1.0, 5000 * (1 - n), 50 * np.exp(-10 * (n - 1)))
    CO = np.clip(CO, 0, 6000)

    # NOx: increases with n (more N2 at higher T)
    NOx = 100 + 200 * (n - 1) + 50 * n**2

    ax2.plot(n, CO, color=COLORS[1], linewidth=2, linestyle="--", label="CO [ppm]")
    ax2.plot(n, NOx, color="#7C3AED", linewidth=2, linestyle="-.", label="NOx [mg/m\u00b3]")
    ax2.set_ylabel("CO [ppm] / NOx [mg/m\u00b3]", fontsize=11, color="#555")

    # Optimal zone
    ax1.axvspan(1.1, 1.25, alpha=0.1, color=COLORS[2])
    ax1.text(1.175, 60, "Optim\u00e1ln\u00ed\nz\u00f3na", fontsize=10, ha="center",
             fontweight="bold", color=COLORS[2])

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc="lower left")

    ax1.set_title("Vliv p\u0159ebytku vzduchu na \u00fa\u010dinnost, CO a NOx",
                  fontsize=12, fontweight="bold")
    ax1.set_xlim(0.8, 2.0)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q20_excess_effects.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_o2_co2_vs_n():
    """O2 and CO2 concentration vs excess air coefficient."""
    fig, ax = plt.subplots(figsize=(7, 5))

    n = np.linspace(1.0, 2.5, 100)
    CO2_max = 18.5  # for coal

    CO2 = CO2_max / n  # approximate
    O2 = 21 * (1 - 1/n)

    ax.plot(n, CO2, color=COLORS[1], linewidth=2.5, label="CO\u2082 [%]")
    ax.plot(n, O2, color=COLORS[0], linewidth=2.5, label="O\u2082 [%]")

    ax.axhline(y=CO2_max, color=COLORS[1], linewidth=1, linestyle=":", alpha=0.5)
    ax.text(2.3, CO2_max + 0.3, f"CO\u2082_max = {CO2_max} %", fontsize=8, color=COLORS[1])

    ax.set_xlabel("P\u0159ebytek vzduchu n [-]", fontsize=11)
    ax.set_ylabel("Koncentrace v such\u00fdch spalin\u00e1ch [%]", fontsize=11)
    ax.set_title("CO\u2082 a O\u2082 v z\u00e1vislosti na p\u0159ebytku vzduchu\n(\u010dern\u00e9 uhl\u00ed, CO\u2082_max = 18,5 %)",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(1, 2.5)
    ax.set_ylim(0, 22)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q20_o2_co2.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_effects = generate_excess_air_effects()
    img_o2co2 = generate_o2_co2_vs_n()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="20. P\u0159ebytek spalovac\u00edho vzduchu.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Definujte p\u0159ebytek spalovac\u00edho vzduchu. Vysv\u011btlete jeho vliv na spalov\u00e1n\u00ed "
        "a \u00fa\u010dinnost kotle. Uve\u010fte zp\u016fsoby jeho stanoven\u00ed z anal\u00fdzy spalin.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Definice p\u0159ebytku vzduchu", level=3)

    add_info_box(doc,
        "P\u0159ebytek vzduchu n (sou\u010dinitel p\u0159ebytku vzduchu)",
        "Pom\u011br skute\u010dn\u00e9ho mno\u017estv\u00ed vzduchu ku stechiometrick\u00e9mu:\n"
        "n = V_vz / V_{vz,min} = m_vz / m_{vz,min}\n"
        "n = 1: stechiometrick\u00e9 spalov\u00e1n\u00ed | n > 1: p\u0159ebytek | n < 1: nedostatek")

    add_equation(doc, r"n = \frac{V_{vz}}{V_{vz,min}} = \frac{m_{vz}}{m_{vz,min}}", label="1")

    add_para(doc, "P\u0159ebytek vzduchu v procentech:", keep_with_next=True)
    add_equation(doc, r"e = (n - 1) \times 100 \quad [\%]", label="2")

    # -- 1.2 Stanoveni z analyzy --
    add_heading(doc, "1.2 Stanoven\u00ed p\u0159ebytku z anal\u00fdzy spalin", level=3)

    add_para(doc, "a) Z koncentrace O\u2082 v such\u00fdch spalin\u00e1ch:", bold=True, keep_with_next=True)
    add_equation(doc, r"n = \frac{21}{21 - O_2} \quad [\text{O}_2 \text{ v \%}]", label="3")

    add_para(doc, "b) Z koncentrace CO\u2082 v such\u00fdch spalin\u00e1ch:", bold=True, keep_with_next=True)
    add_equation(doc, r"n = \frac{CO_{2,max}}{CO_2}", label="4")

    add_para(doc, "kde CO\u2082_max je maxim\u00e1ln\u00ed koncentrace CO\u2082 p\u0159i n = 1 (z\u00e1vis\u00ed na palivu).")

    add_image(doc, img_o2co2, width_cm=12,
              caption="Obr. 1: Z\u00e1vislost CO\u2082 a O\u2082 na p\u0159ebytku vzduchu \u2014 inverzn\u00ed pr\u016fb\u011bh")

    add_styled_table(doc,
        headers=["P\u0159ebytek n", "O\u2082 [%]", "CO\u2082 [%] (uhl\u00ed)"],
        data=[
            ["1,00", "0,0", "18,5"],
            ["1,10", "1,9", "16,8"],
            ["1,20", "3,5", "15,4"],
            ["1,30", "4,9", "14,2"],
            ["1,50", "7,0", "12,3"],
            ["2,00", "10,5", "9,3"],
        ],
    )

    # -- 1.3 Vliv --
    add_page_break(doc)
    add_heading(doc, "1.3 Vliv p\u0159ebytku vzduchu na provoz", level=3)

    add_image(doc, img_effects, width_cm=14,
              caption="Obr. 2: Vliv p\u0159ebytku vzduchu na \u00fa\u010dinnost kotle, emise CO a NOx")

    add_para(doc, "P\u0159\u00edli\u0161 n\u00edzk\u00fd p\u0159ebytek (n < 1):", bold=True, keep_with_next=True)
    add_bullet(doc, "Ne\u00fapln\u00e9 spalov\u00e1n\u00ed \u2192 CO, saze, nespálen\u00e9 uhlovod\u00edky")
    add_bullet(doc, "Ztráta chemick\u00fdm nedop\u00e1lem (a\u017e des\u00edtky % energie)")
    add_bullet(doc, "Nebezpe\u010d\u00ed v\u00fdbuchu (ho\u0159lav\u00e9 plyny ve spalinov\u00e9m traktu)", is_last=True)

    add_para(doc, "P\u0159\u00edli\u0161 vysok\u00fd p\u0159ebytek (n >> 1):", bold=True, keep_with_next=True)
    add_bullet(doc, "Ztráta citelnou heat\u016f spalin (v\u011bt\u0161\u00ed objem spalin = v\u00edce tepla odch\u00e1z\u00ed kom\u00ednem)")
    add_bullet(doc, "Zvy\u0161uje se tvorba NOx (v\u00edce N\u2082 p\u0159i vysok\u00e9 T)")
    add_bullet(doc, "Ochlazov\u00e1n\u00ed oh\u0159ívacího prostoru (sn\u00ed\u017een\u00ed teploty plamene)")
    add_bullet(doc, "Vy\u0161\u0161\u00ed v\u00fdkon ventil\u00e1toru (vy\u0161\u0161\u00ed pr\u016ftok vzduchu)", is_last=True)

    add_info_box(doc,
        "Optim\u00e1ln\u00ed p\u0159ebytek vzduchu",
        "Kompromis mezi ne\u00fapln\u00fdm spalov\u00e1n\u00edm (n p\u0159\u00edli\u0161 n\u00edzk\u00e9) a ztr\u00e1tou "
        "citelným teplem spalin (n p\u0159\u00edli\u0161 vysok\u00e9). Optim\u00e1ln\u00ed n le\u017e\u00ed v\u011bt\u0161inou "
        "v rozmez\u00ed 1,05\u20131,30 podle typu ho\u0159\u00e1ku a paliva.")

    # -- 1.4 Ztráty --
    add_heading(doc, "1.4 Ztráta citelným teplem spalin", level=3)

    add_equation(doc, r"q_{sp} = \frac{V_{sp} \cdot c_{p,sp} \cdot (T_{sp} - T_{vz})}{Q_i^r} \times 100 \quad [\%]", label="5")

    add_para(doc,
        "kde T_sp je teplota spalin na v\u00fdstupu z kotle a T_vz teplota vzduchu. "
        "Ka\u017ed\u00fdch 20 \u00b0C nav\u00fd\u0161en\u00ed T_sp zvy\u0161uje ztrátu o ~1 procentn\u00ed bod.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Typick\u00e9 hodnoty p\u0159ebytku", level=3)
    add_styled_table(doc,
        headers=["Spalovac\u00ed za\u0159\u00edzen\u00ed", "n", "O\u2082 [%]"],
        data=[
            ["Plynov\u00fd ho\u0159\u00e1k (premix)", "1,05\u20131,10", "1\u20132"],
            ["Pr\u00e1\u0161kov\u00fd uhl\u00edkov\u00fd ho\u0159\u00e1k", "1,15\u20131,25", "3\u20135"],
            ["Ro\u0161tov\u00e9 oh\u0159ívací (uhl\u00ed)", "1,30\u20131,50", "5\u20138"],
            ["Fluidn\u00ed kotel", "1,15\u20131,25", "3\u20135"],
            ["Spalovna odpadu", "1,50\u20132,00", "8\u201312"],
            ["Plynov\u00e1 turbína", "2,0\u20133,5", "12\u201316"],
        ],
    )

    add_heading(doc, "2.2 M\u011b\u0159en\u00ed a regulace", level=3)
    add_bullet(doc, "Lambda sonda (ZrO\u2082) \u2014 kontinuální m\u011b\u0159en\u00ed O\u2082 ve spalin\u00e1ch")
    add_bullet(doc, "NDIR analyz\u00e1tor \u2014 m\u011b\u0159en\u00ed CO, CO\u2082")
    add_bullet(doc, "Automatick\u00e1 regulace \u2014 \u0159\u00eddic\u00ed syst\u00e9m udr\u017euje O\u2082 v optim\u00e1ln\u00edm rozmez\u00ed")
    add_bullet(doc, "K\u0159\u00ed\u017eov\u00e1 regulace \u2014 pom\u011br palivo/vzduch se m\u011bn\u00ed s v\u00fdkonem", is_last=True)

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Ur\u010den\u00ed p\u0159ebytku vzduchu z anal\u00fdzy spalin", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Anal\u00fdza such\u00fdch spalin \u010dern\u00e9ho uhl\u00ed uk\u00e1zala: O\u2082 = 4,5 %, "
        "CO\u2082 = 14,8 %. CO\u2082_max pro dan\u00e9 uhl\u00ed je 18,5 %. "
        "Ur\u010dete p\u0159ebytek vzduchu ob\u011bma metodami.", bold=True)

    add_para(doc, "Metoda 1: Z O\u2082", bold=True)
    add_equation(doc, r"n = \frac{21}{21 - O_2} = \frac{21}{21 - 4{,}5} = \frac{21}{16{,}5} = 1{,}273")

    add_para(doc, "Metoda 2: Z CO\u2082", bold=True)
    add_equation(doc, r"n = \frac{CO_{2,max}}{CO_2} = \frac{18{,}5}{14{,}8} = 1{,}250")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Z O\u2082: n = 1,273 | Z CO\u2082: n = 1,250\n"
        "Shoda je dobr\u00e1 (rozd\u00edl 2 %). Mal\u00e1 odchylka m\u016f\u017ee b\u00fdt zp\u016fsobena "
        "m\u00edrn\u00fdm ne\u00fapln\u00fdm spalov\u00e1n\u00edm (CO ve spalin\u00e1ch), "
        "nep\u0159esnost\u00ed CO\u2082_max nebo m\u011b\u0159ení.\n\n"
        "P\u0159ebytek vzduchu e = (1,27 \u2212 1) \u00d7 100 = 27 % \u2014 odpov\u00edd\u00e1 "
        "pr\u00e1\u0161kov\u00e9mu spalov\u00e1n\u00ed uhl\u00ed.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d nelze spalovat p\u0159esn\u011b se stechiometrick\u00fdm vzduchem (n = 1)?",
         "V praxi nen\u00ed mo\u017en\u00e9 dokonale prom\u00edchat palivo se vzduchem. "
         "Lok\u00e1ln\u011b by vznikaly z\u00f3ny s nedostatkem O\u2082 \u2192 CO, saze, ne\u00fapln\u00e9 spalov\u00e1n\u00ed. "
         "P\u0159ebytek zaji\u0161\u0165uje, \u017ee v\u0161ude je dostatek O\u2082."),

        ("Jak p\u0159ebytek vzduchu ovliv\u0148uje teplotu plamene?",
         "P\u0159ebyte\u010dn\u00fd vzduch se oh\u0159\u00edv\u00e1, ale s\u00e1m nedod\u00e1v\u00e1 teplo \u2192 sni\u017euje "
         "adiabatickou teplotu plamene. P\u0159i n = 2 klesne teplota plamene o stovky \u00b0C. "
         "To zhor\u0161uje p\u0159estup tepla s\u00e1l\u00e1n\u00edm (E ~ T\u2074)."),

        ("Pro\u010d d\u00e1v\u00e1 metoda z O\u2082 a z CO\u2082 m\u00edrn\u011b odli\u0161n\u00e9 v\u00fdsledky?",
         "P\u0159i ne\u00fapln\u00e9m spalov\u00e1n\u00ed \u010d\u00e1st C p\u0159ejde na CO m\u00edsto CO\u2082 \u2014 "
         "CO\u2082 je ni\u017e\u0161\u00ed ne\u017e by odpov\u00eddalo dan\u00e9mu n. Metoda z O\u2082 "
         "je v tomto p\u0159\u00edpad\u011b p\u0159esn\u011bj\u0161\u00ed. Proto se v praxi pou\u017e\u00edv\u00e1 O\u2082 sonda."),

        ("Co je lambda sonda a jak pracuje?",
         "Elektro-chemick\u00fd sn\u00edma\u010d na b\u00e1zi ZrO\u2082, kter\u00fd m\u011b\u0159\u00ed parci\u00e1ln\u00ed tlak O\u2082 "
         "ve spalin\u00e1ch. P\u0159i rozd\u00edln\u00e9m tlaku O\u2082 na obou stran\u00e1ch keramiky "
         "vznik\u00e1 elektrick\u00e9 nap\u011bt\u00ed (Nernst\u016fv princip). Pracuje p\u0159i ~600 \u00b0C."),

        ("Pro\u010d spalovny odpadu pracuj\u00ed s velk\u00fdm p\u0159ebytkem vzduchu?",
         "Odpad m\u00e1 prom\u011bnliv\u00e9 slo\u017een\u00ed, nerovnom\u011brn\u00e9 ho\u0159en\u00ed a vysok\u00fd obsah "
         "vlhkosti. Vysok\u00fd p\u0159ebytek (n = 1,5\u20132,0) zaji\u0161\u0165uje \u00fapln\u00e9 sp\u00e1len\u00ed "
         "i za nep\u0159\u00edzniv\u00fdch podm\u00ednek. Z\u00e1rove\u0148 sni\u017euje teplotu (ochrana ro\u0161tu)."),

        ("Jak ovliv\u0148uje p\u0159ebytek vzduchu tvorbu NOx?",
         "M\u00edrn\u00fd p\u0159ebytek (n = 1,1\u20131,3) zvy\u0161uje NOx (v\u00edce O\u2082 + vysok\u00e1 T). "
         "Velk\u00fd p\u0159ebytek (n > 1,5) sni\u017euje NOx (ni\u017e\u0161\u00ed teplota plamene). "
         "Optim\u00e1ln\u00ed NOx\u2193 je p\u0159i chud\u00e9 sm\u011bsi (lean premix, DLN ho\u0159\u00e1ky)."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M. a kol.: Spalov\u00e1n\u00ed a spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cSN EN 14181 \u2014 Emisn\u00ed m\u011b\u0159en\u00ed")
    add_bullet(doc, "Turns, S.R.: An Introduction to Combustion")
    add_bullet(doc, "Testo \u2014 P\u0159\u00edru\u010dka pro m\u011b\u0159en\u00ed spalin", is_last=True)

    save_and_export(doc, "20-prebytek-vzduchu")


if __name__ == "__main__":
    generate()
