# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 15: V\u00fdh\u0159evnost a spaln\u00e9 teplo, zp\u016fsoby stanoven\u00ed, p\u0159epo\u010dty.
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

def generate_qs_qi_diagram():
    """Diagram showing relationship between Qs and Qi."""
    fig, ax = plt.subplots(figsize=(8, 5))

    fuels = ["Vod\u00edk", "Zemn\u00ed plyn", "Propan", "Benzin", "\u010cern\u00e9 uhl\u00ed", "Hn\u011bd\u00e9 uhl\u00ed", "D\u0159evo"]
    Qi = [120.0, 34.0, 46.4, 43.5, 25.7, 17.0, 15.0]
    Qs = [142.0, 37.8, 50.4, 47.3, 26.9, 18.5, 17.2]

    x = np.arange(len(fuels))
    w = 0.35

    bars1 = ax.bar(x - w/2, Qs, w, label="Spaln\u00e9 teplo $Q_s$ (HHV)", color=COLORS[1], edgecolor="white")
    bars2 = ax.bar(x + w/2, Qi, w, label="V\u00fdh\u0159evnost $Q_i$ (LHV)", color=COLORS[0], edgecolor="white")

    # Difference annotation on first bar
    ax.annotate("", xy=(x[0] - w/2, Qi[0]), xytext=(x[0] - w/2, Qs[0]),
                arrowprops=dict(arrowstyle="<->", color="#D97706", lw=2))
    ax.text(x[0] - w/2 - 0.35, (Qs[0] + Qi[0]) / 2, "$\\Delta Q$\n(kond.\nteplo)", fontsize=7,
            color="#D97706", ha="center", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(fuels, fontsize=9, rotation=15)
    ax.set_ylabel("Teplo [MJ/kg]", fontsize=11)
    ax.set_title("Spaln\u00e9 teplo (HHV) vs. v\u00fdh\u0159evnost (LHV)", fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_ylim(0, 155)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q15_qs_qi.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_calorimeter_schema():
    """Simplified calorimetric bomb schema."""
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

    from matplotlib.patches import FancyBboxPatch, Circle

    # Water jacket
    jacket = FancyBboxPatch((1.5, 1), 7, 5.5, boxstyle="round,pad=0.3",
                             facecolor="#DBEAFE", edgecolor="#2563EB", lw=2)
    ax.add_patch(jacket)
    ax.text(5, 6.8, "VODN\u00cd L\u00c1ZE\u0147 (m\u2096, c\u2096, \u0394T)", fontsize=10, ha="center",
            fontweight="bold", color="#2563EB")

    # Bomb
    bomb = FancyBboxPatch((3, 2), 4, 3.5, boxstyle="round,pad=0.2",
                           facecolor="#FEE2E2", edgecolor="#DC2626", lw=2.5)
    ax.add_patch(bomb)
    ax.text(5, 4.2, "KALORIMETRICK\u00c1\nBOMBA", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#DC2626")
    ax.text(5, 3.2, "vzorek paliva\n+ O\u2082 (3 MPa)", ha="center", va="center",
            fontsize=9, color="#991B1B")

    # Thermometer
    ax.text(8.5, 4, "Teplom\u011br\n(\u0394T)", fontsize=9, ha="center", color="#555",
            fontweight="bold")
    ax.annotate("", xy=(7.2, 4), xytext=(8.2, 4),
                arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.5))

    # Ignition
    ax.text(1, 4, "Zapalov\u00e1n\u00ed\n(el. dr\u00e1tek)", fontsize=9, ha="center", color="#D97706",
            fontweight="bold")
    ax.annotate("", xy=(2.8, 4), xytext=(1.8, 4),
                arrowprops=dict(arrowstyle="-|>", color="#D97706", lw=1.5))

    # Equation
    ax.text(5, 0.5, "$Q_s = \\frac{(m_w c_w + C_{kal}) \\cdot \\Delta T}{m_{paliva}}$",
            fontsize=12, ha="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF3C7", edgecolor="#D97706"))

    fig.suptitle("Sch\u00e9ma kalorimetrick\u00e9 bomby", fontsize=12, fontweight="bold", y=0.98)
    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q15_calorimeter.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_moisture_effect():
    """Effect of moisture content on heating value."""
    fig, ax = plt.subplots(figsize=(7, 5))

    W = np.linspace(0, 60, 100)  # moisture %
    Qi_daf = 20.0  # MJ/kg for dry ash-free coal
    A_d = 15  # ash on dry basis %

    # Q_i^r = Q_i^daf * (1 - W/100) * (1 - A_d/100/(1-W/100)) - 2.454 * W/100
    # Simplified: Q_i^r = Q_i^daf * (100 - W - A*(100-W)/100) / 100 - 2.454*W/100
    Qi_r = Qi_daf * (1 - W/100) * (1 - A_d/100) - 2.454 * W/100

    ax.plot(W, Qi_r, color=COLORS[0], linewidth=2.5, label="$Q_i^r$")
    ax.axhline(y=0, color="gray", linewidth=0.8, linestyle=":")

    # Self-sustaining combustion limit
    ax.axhline(y=4, color=COLORS[1], linewidth=1.5, linestyle="--", alpha=0.7)
    ax.text(55, 4.5, "Hranice samoudr\u017eiteln\u00e9ho\nspalov\u00e1n\u00ed (~4 MJ/kg)", fontsize=8,
            color=COLORS[1])

    # Mark typical values
    for w_val, label in [(8, "\u010cern\u00e9 uhl\u00ed"), (35, "Hn\u011bd\u00e9 uhl\u00ed"), (50, "K\u016fra")]:
        qi_val = Qi_daf * (1 - w_val/100) * (1 - A_d/100) - 2.454 * w_val/100
        ax.plot(w_val, qi_val, "ko", markersize=7, zorder=5)
        ax.annotate(f"{label}\n({qi_val:.1f} MJ/kg)", xy=(w_val, qi_val),
                    xytext=(w_val + 3, qi_val + 1.5), fontsize=8,
                    arrowprops=dict(arrowstyle="->", lw=1))

    ax.set_xlabel("Vlhkost paliva W\u02b3 [%]", fontsize=11)
    ax.set_ylabel("V\u00fdh\u0159evnost $Q_i^r$ [MJ/kg]", fontsize=11)
    ax.set_title("Vliv vlhkosti na v\u00fdh\u0159evnost paliva\n($Q_i^{daf}$ = 20 MJ/kg, $A^d$ = 15 %)",
                 fontsize=11, fontweight="bold")
    ax.set_xlim(0, 65)
    ax.legend(fontsize=9)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q15_moisture.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH DOKUMENTU
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_qs_qi = generate_qs_qi_diagram()
    img_cal = generate_calorimeter_schema()
    img_moist = generate_moisture_effect()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="15. V\u00fdh\u0159evnost a spaln\u00e9 teplo, zp\u016fsoby stanoven\u00ed, p\u0159epo\u010dty.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Definujte v\u00fdh\u0159evnost a spaln\u00e9 teplo paliva. Vysv\u011btlete zp\u016fsoby jejich stanoven\u00ed "
        "(experiment\u00e1ln\u00ed, v\u00fdpo\u010detn\u00ed). Odvo\u010fte p\u0159epo\u010dty mezi r\u016fzn\u00fdmi stavy paliva "
        "(surov\u00e9, such\u00e9, ho\u0159lavina).")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Definice", level=3)

    add_info_box(doc,
        "Spaln\u00e9 teplo Q\u209b (HHV \u2014 Higher Heating Value)",
        "Mno\u017estv\u00ed tepla uvoln\u011bn\u00e9 \u00fapln\u00fdm sp\u00e1len\u00edm 1 kg paliva p\u0159i ochlažen\u00ed "
        "spalin na 25 \u00b0C, p\u0159i\u010dem\u017e vodn\u00ed p\u00e1ra ve spalin\u00e1ch ZKONDENZUJE na kapalnou vodu. "
        "Zahrnuje kondenza\u010dn\u00ed teplo.")

    add_info_box(doc,
        "V\u00fdh\u0159evnost Q\u1d62 (LHV \u2014 Lower Heating Value)",
        "Mno\u017estv\u00ed tepla uvoln\u011bn\u00e9 \u00fapln\u00fdm sp\u00e1len\u00edm 1 kg paliva p\u0159i ochlažen\u00ed "
        "spalin na 25 \u00b0C, p\u0159i\u010dem\u017e vodn\u00ed p\u00e1ra z\u016fst\u00e1v\u00e1 V PLYNN\u00c9 F\u00c1ZI. "
        "Nezahrnuje kondenza\u010dn\u00ed teplo. V Evrop\u011b standardn\u011b pou\u017e\u00edvan\u00e1 veli\u010dina.")

    add_para(doc, "Vztah mezi Q\u209b a Q\u1d62:", keep_with_next=True)
    add_equation(doc, r"Q_i^r = Q_s^r - r \cdot (9H^r + W^r)", label="1")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "r = 2,454 MJ/kg \u2014 v\u00fdparn\u00e9 teplo vody p\u0159i 25 \u00b0C")
    add_bullet(doc, "9H\u02b3 \u2014 hmotnost vody vznikl\u00e9 sp\u00e1len\u00edm vod\u00edku (2H\u2082 + O\u2082 \u2192 2H\u2082O; "
               "M_H\u2082O/M_H\u2082 = 18/2 = 9)")
    add_bullet(doc, "W\u02b3 \u2014 vlhkost paliva (voda, kter\u00e1 se odpa\u0159\u00ed)", is_last=True)

    add_image(doc, img_qs_qi, width_cm=14,
              caption="Obr. 1: Srovn\u00e1n\u00ed spaln\u00e9ho tepla (HHV) a v\u00fdh\u0159evnosti (LHV) pro r\u016fzn\u00e1 paliva")

    add_warning_box(doc,
        "U vod\u00edku je rozd\u00edl Q\u209b \u2212 Q\u1d62 obrovsk\u00fd (22 MJ/kg = 18 %), proto\u017ee ve\u0161ker\u00fd "
        "produkt spalov\u00e1n\u00ed je voda. U uhl\u00ed je rozd\u00edl mal\u00fd (1\u20132 MJ/kg = 4\u20138 %), "
        "proto\u017ee hlavn\u00ed ho\u0159lavinou je uhl\u00edk (produkt CO\u2082).")

    # -- 1.2 Stanoven\u00ed --
    add_page_break(doc)
    add_heading(doc, "1.2 Zp\u016fsoby stanoven\u00ed", level=3)

    add_heading(doc, "a) Experiment\u00e1ln\u00ed \u2014 kalorimetrick\u00e1 bomba", level=3)

    add_image(doc, img_cal, width_cm=12,
              caption="Obr. 2: Sch\u00e9ma kalorimetrick\u00e9 bomby pro stanoven\u00ed spaln\u00e9ho tepla")

    add_para(doc, "Princip:", keep_with_next=True)
    add_bullet(doc, "Vzorek paliva se sp\u00e1l\u00ed v tlakov\u00e9 n\u00e1dob\u011b (bomb\u011b) napln\u011bn\u00e9 kysl\u00edkem (3 MPa)")
    add_bullet(doc, "Bomba je pono\u0159ena ve vodn\u00ed l\u00e1zni o zn\u00e1m\u00e9 hmotnosti a teplot\u011b")
    add_bullet(doc, "M\u011b\u0159\u00ed se n\u00e1r\u016fst teploty \u0394T vodn\u00ed l\u00e1zn\u011b")
    add_bullet(doc, "V\u00fdsledek: spaln\u00e9 teplo Q\u209b (p\u00e1ra zkondenzuje p\u0159i ochlažen\u00ed na T l\u00e1zn\u011b)", is_last=True)

    add_equation(doc, r"Q_s = \frac{(m_w c_w + C_{kal}) \cdot \Delta T - Q_{dr\acute{a}tek}}{m_{paliva}}", label="2")

    add_para(doc, "kde C_kal je tepeln\u00e1 kapacita kalorimetru (vodn\u00ed ekvivalent).")

    add_heading(doc, "b) V\u00fdpo\u010detn\u00ed \u2014 z prvkov\u00e9ho rozboru", level=3)

    add_para(doc, "Mend\u011blejevova empirick\u00e1 rovnice:", keep_with_next=True)
    add_equation(doc, r"Q_i^r = 33{,}91 C^r + 103{,}0 H^r - 10{,}89 (O^r - S^r) - 2{,}51 W^r \quad [\text{MJ/kg}]", label="3")

    add_para(doc, "Dulongova rovnice (alternativa):", keep_with_next=True)
    add_equation(doc, r"Q_s^r = 33{,}83 C^r + 144{,}3 \left(H^r - \frac{O^r}{8}\right) + 9{,}42 S^r \quad [\text{MJ/kg}]", label="4")

    # -- 1.3 P\u0159epo\u010dty --
    add_page_break(doc)
    add_heading(doc, "1.3 P\u0159epo\u010dty mezi stavy paliva", level=3)

    add_para(doc, "P\u0159epo\u010det z surov\u00e9ho na such\u00e9:", keep_with_next=True)
    add_equation(doc, r"Q_i^d = \frac{Q_i^r + 2{,}454 \cdot W^r}{1 - W^r}", label="5")

    add_para(doc, "P\u0159epo\u010det z such\u00e9ho na ho\u0159lavinu:", keep_with_next=True)
    add_equation(doc, r"Q_i^{daf} = \frac{Q_i^d}{1 - A^d}", label="6")

    add_para(doc, "P\u0159epo\u010det z ho\u0159laviny na surov\u00e9 (zp\u011bt):", keep_with_next=True)
    add_equation(doc, r"Q_i^r = Q_i^{daf} (1 - A^d)(1 - W^r) - 2{,}454 \cdot W^r", label="7")

    add_image(doc, img_moist, width_cm=13,
              caption="Obr. 3: Vliv vlhkosti na v\u00fdh\u0159evnost paliva \u2014 p\u0159i ~55 % vlhkosti kles\u00e1 Q\u1d62 pod hranici samoudr\u017eiteln\u00e9ho spalov\u00e1n\u00ed")

    add_info_box(doc,
        "Praktick\u00e9 d\u016fsledky vlhkosti",
        "Ka\u017ed\u00e9 % vlhkosti sn\u00ed\u017e\u00ed Q\u1d62 dvoj\u00edm zp\u016fsobem:\n"
        "1) Zmen\u0161uje pod\u00edl ho\u0159laviny (m\u00e9n\u011b paliva na kg)\n"
        "2) Spot\u0159ebov\u00e1v\u00e1 teplo na odpa\u0159en\u00ed (2,454 MJ/kg vody)\n"
        "Proto je su\u0161en\u00ed paliva \u010dasto ekonomicky v\u00fdhodn\u00e9.")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Normy", level=3)
    add_styled_table(doc,
        headers=["Norma", "P\u0159edm\u011bt"],
        data=[
            ["\u010cSN ISO 1928", "Stanoven\u00ed spaln\u00e9ho tepla kalorimetrickou bombou"],
            ["\u010cSN EN 14918", "Biomasa \u2014 stanoven\u00ed spaln\u00e9ho tepla"],
            ["\u010cSN EN ISO 6976", "Zemn\u00ed plyn \u2014 v\u00fdpo\u010det spaln\u00e9ho tepla ze slo\u017een\u00ed"],
            ["\u010cSN 44 1352", "Stanoven\u00ed v\u00fdh\u0159evnosti tuh\u00fdch paliv"],
        ],
    )

    add_heading(doc, "2.2 HHV vs. LHV v r\u016fzn\u00fdch zem\u00edch", level=3)
    add_para(doc,
        "V Evrop\u011b se standardn\u011b pou\u017e\u00edv\u00e1 v\u00fdh\u0159evnost Q\u1d62 (LHV) \u2014 spaliny nekondenzuj\u00ed. "
        "V Severn\u00ed Americe se historicky pou\u017e\u00edv\u00e1 spaln\u00e9 teplo Q\u209b (HHV). "
        "Modern\u00ed kondenza\u010dn\u00ed kotle (plynov\u00e9) vyu\u017e\u00edvaj\u00ed i kondenza\u010dn\u00ed teplo \u2014 "
        "jejich \u00fa\u010dinnost m\u016f\u017ee p\u0159ekro\u010dit 100 % (pokud je referen\u010dn\u00ed hodnotou Q\u1d62).")

    add_heading(doc, "2.3 V\u00fdh\u0159evnost plynn\u00fdch paliv", level=3)
    add_para(doc,
        "U plynn\u00fdch paliv se v\u00fdh\u0159evnost ud\u00e1v\u00e1 v MJ/m\u00b3 (p\u0159i norm\u00e1ln\u00edch podm\u00ednk\u00e1ch "
        "0 \u00b0C, 101,325 kPa). V\u00fdpo\u010det ze slo\u017een\u00ed:", keep_with_next=True)
    add_equation(doc, r"Q_i = \sum_j y_j \cdot Q_{i,j}", label="8")
    add_para(doc, "kde y_j je objemov\u00fd zlomek a Q_{i,j} v\u00fdh\u0159evnost j-t\u00e9 slo\u017eky.")

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: P\u0159epo\u010det v\u00fdh\u0159evnosti p\u0159i zm\u011bn\u011b vlhkosti", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Hn\u011bd\u00e9 uhl\u00ed m\u00e1 v surov\u00e9m stavu v\u00fdh\u0159evnost Q\u1d62\u02b3 = 12,5 MJ/kg, "
        "vlhkost W\u02b3 = 35 %, popel A\u02b3 = 20 %. "
        "Uhl\u00ed se vysu\u0161\u00ed na W = 10 %. Ur\u010dete novou v\u00fdh\u0159evnost.", bold=True)

    add_para(doc, "Krok 1: P\u0159epo\u010det na ho\u0159lavinu", bold=True)
    add_equation(doc, r"A^d = \frac{A^r}{1 - W^r} = \frac{0{,}20}{1 - 0{,}35} = 0{,}3077 = 30{,}8 \%")
    add_equation(doc, r"Q_i^d = \frac{Q_i^r + 2{,}454 \times W^r}{1 - W^r} = \frac{12{,}5 + 2{,}454 \times 0{,}35}{1 - 0{,}35} = \frac{13{,}36}{0{,}65} = 20{,}55 \text{ MJ/kg}")
    add_equation(doc, r"Q_i^{daf} = \frac{Q_i^d}{1 - A^d} = \frac{20{,}55}{1 - 0{,}308} = \frac{20{,}55}{0{,}692} = 29{,}70 \text{ MJ/kg}")

    add_para(doc, "Krok 2: P\u0159epo\u010det zp\u011bt na nov\u00fd surov\u00fd stav (W = 10 %)", bold=True)
    add_equation(doc, r"Q_i^{r,nov\acute{e}} = Q_i^{daf}(1 - A^d)(1 - W^{r,nov\acute{e}}) - 2{,}454 \cdot W^{r,nov\acute{e}}")
    add_equation(doc, r"Q_i^{r,nov\acute{e}} = 29{,}70 \times 0{,}692 \times (1 - 0{,}10) - 2{,}454 \times 0{,}10")
    add_equation(doc, r"Q_i^{r,nov\acute{e}} = 29{,}70 \times 0{,}692 \times 0{,}90 - 0{,}245 = 18{,}24 \text{ MJ/kg}")

    add_info_box(doc,
        "V\u00fdsledky:",
        "P\u016fvodn\u00ed: Q\u1d62\u02b3 = 12,5 MJ/kg (W = 35 %)\n"
        "Po vysu\u0161en\u00ed: Q\u1d62\u02b3 = 18,24 MJ/kg (W = 10 %)\n\n"
        "Zv\u00fd\u0161en\u00ed o 46 %! Vysu\u0161en\u00ed z 35 % na 10 % v\u00fdrazn\u011b zvy\u0161uje "
        "v\u00fdh\u0159evnost a sni\u017euje spot\u0159ebu paliva. V praxi se hn\u011bd\u00e9 uhl\u00ed \u010dasto su\u0161\u00ed "
        "odpadn\u00edm teplem spalin.")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d se v Evrop\u011b pou\u017e\u00edv\u00e1 Q\u1d62 a v Americe Q\u209b?",
         "Historick\u00e1 konvence. V praxi spaliny obvykle nekondenzuj\u00ed (T > rosn\u00fd bod), "
         "tak\u017ee Q\u1d62 l\u00e9pe odpov\u00edd\u00e1 skute\u010dn\u011b vyu\u017eiteln\u00e9mu teplu. "
         "Americk\u00e1 konvence Q\u209b je v\u00fdhodn\u00e1 pro kondenza\u010dn\u00ed technologie, "
         "kde se \u010d\u00e1st kondenza\u010dn\u00edho tepla skute\u010dn\u011b vyu\u017eije."),

        ("Pro\u010d m\u016f\u017ee kondenza\u010dn\u00ed kotel m\u00edt \u00fa\u010dinnost nad 100 %?",
         "Proto\u017ee referen\u010dn\u00ed hodnotou je Q\u1d62, kter\u00e1 nezahrnuje kondenza\u010dn\u00ed teplo. "
         "Kondenza\u010dn\u00ed kotel vyu\u017e\u00edv\u00e1 i \u010d\u00e1st kondenza\u010dn\u00edho tepla p\u00e1ry ve spalin\u00e1ch, "
         "tak\u017ee z\u00edsk\u00e1 v\u00edce tepla ne\u017e Q\u1d62. Skute\u010dn\u00e1 \u00fa\u010dinnost v\u016f\u010di Q\u209b je v\u017edy < 100 %."),

        ("Vysv\u011btlete, pro\u010d se v\u00fdh\u0159evnost m\u011b\u0159\u00ed v kalorimetrick\u00e9 bomb\u011b a ne v otev\u0159en\u00e9m oh\u0159\u00edva\u010di.",
         "Bomba zaji\u0161\u0165uje \u00fapln\u00e9 sp\u00e1len\u00ed (p\u0159ebytek O\u2082, vysok\u00fd tlak), "
         "izolovan\u00fd syst\u00e9m (p\u0159esn\u00e9 m\u011b\u0159en\u00ed \u0394T) a kondenzaci p\u00e1ry "
         "(v\u00fdsledek je Q\u209b, ze kter\u00e9ho se dopo\u010dte Q\u1d62)."),

        ("Pro\u010d vlhkost sni\u017euje v\u00fdh\u0159evnost dvoj\u00edm zp\u016fsobem?",
         "1) Zmen\u0161uje pod\u00edl ho\u0159laviny na kg paliva (z\u0159e\u010f\u016fvac\u00ed efekt). "
         "2) Na odpa\u0159en\u00ed vody se spot\u0159ebuje 2,454 MJ/kg. "
         "Oba efekty se s\u010d\u00edtaj\u00ed \u2014 proto ka\u017ed\u00e9 procento vlhkosti sn\u00ed\u017e\u00ed Q\u1d62 v\u00edce, "
         "ne\u017e by odpov\u00eddalo prost\u00e9mu z\u0159ed\u011bn\u00ed."),

        ("Jak\u00e1 je minim\u00e1ln\u00ed v\u00fdh\u0159evnost pro samoudr\u017eiteln\u00e9 spalov\u00e1n\u00ed?",
         "Cca 4\u20136 MJ/kg. Pod touto hranic\u00ed nestačí teplo ze spalov\u00e1n\u00ed na odpa\u0159en\u00ed "
         "vlhkosti a oh\u0159ev paliva na teplotu vzn\u00edcen\u00ed. V praxi se p\u0159id\u00e1v\u00e1 "
         "podp\u016frn\u00e9 palivo (zemn\u00ed plyn) nebo se palivo p\u0159edsu\u0161uje."),

        ("Jak vypo\u010d\u00edt\u00e1te v\u00fdh\u0159evnost zemn\u00edho plynu ze slo\u017een\u00ed?",
         "Sou\u010det sou\u010din\u016f objemov\u00fdch zlomk\u016f a v\u00fdh\u0159evnost\u00ed slo\u017eek: "
         "Q\u1d62 = \u03a3 y_j Q_{i,j}. Nap\u0159. pro 95 % CH\u2084 + 3 % C\u2082H\u2086 + 2 % N\u2082: "
         "Q\u1d62 = 0,95\u00d735,9 + 0,03\u00d764,4 + 0 = 36,0 MJ/m\u00b3."),
    ])

    # -- Zapati --
    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "Bal\u00e1\u0161, M. a kol.: Spalov\u00e1n\u00ed a spalovac\u00ed za\u0159\u00edzen\u00ed, VUT Brno")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "\u010cSN ISO 1928 \u2014 Stanoven\u00ed spaln\u00e9ho tepla")
    add_bullet(doc, "\u010cSN EN 14918 \u2014 Biomasa, stanoven\u00ed spaln\u00e9ho tepla")
    add_bullet(doc, "Perry's Chemical Engineers' Handbook \u2014 Combustion", is_last=True)

    save_and_export(doc, "15-vyhrevnost")


if __name__ == "__main__":
    generate()
