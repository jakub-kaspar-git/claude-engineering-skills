# -*- coding: utf-8 -*-
"""
St\u00e1tnicov\u00e1 ot\u00e1zka 5: Stroje na stla\u010dov\u00e1n\u00ed a dopravu vzdu\u0161in, rozd\u011blen\u00ed.
Jednostup\u0148ov\u00e1 a v\u00edcestup\u0148ov\u00e1 komprese. Vliv \u0161kodliv\u00e9ho prostoru,
d\u016fvody v\u00edcestup\u0148ov\u00e9 komprese, p\u0159\u00edkon kompresoru.
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

def generate_pv_compression():
    """p-v diagram comparing isothermal, polytropic, isentropic compression."""
    fig, ax = plt.subplots(figsize=(8, 5.5))
    kappa = 1.4

    p1 = 100  # kPa
    v1 = 1.0
    p2 = 800  # kPa

    v_range = np.linspace(0.05, 1.1, 500)

    # Isothermal (n=1)
    p_iso = p1 * v1 / v_range
    ax.plot(v_range, p_iso, color=COLORS[0], linewidth=2.5, label="Izotermick\u00e1 (n=1) \u2014 minim\u00e1ln\u00ed pr\u00e1ce")

    # Polytropic (n=1.25)
    n_poly = 1.25
    p_poly = p1 * (v1 / v_range)**n_poly
    ax.plot(v_range, p_poly, color="#7C3AED", linewidth=2.5, linestyle="--",
            label="Polytropick\u00e1 (n=1,25)")

    # Isentropic (n=kappa)
    p_isen = p1 * (v1 / v_range)**kappa
    ax.plot(v_range, p_isen, color=COLORS[1], linewidth=2.5, label="Izoentropick\u00e1 (n=\u03ba=1,4) \u2014 maxim\u00e1ln\u00ed pr\u00e1ce")

    # Highlight work areas
    v2_iso = p1 * v1 / p2
    v2_isen = v1 * (p1 / p2)**(1/kappa)

    ax.axhline(y=p1, color="gray", linewidth=0.5, linestyle=":")
    ax.axhline(y=p2, color="gray", linewidth=0.5, linestyle=":")
    ax.text(1.05, p1, "$p_1$", fontsize=10, color="gray")
    ax.text(1.05, p2, "$p_2$", fontsize=10, color="gray")

    # Starting point
    ax.plot(v1, p1, "ko", markersize=10, zorder=5)
    ax.annotate("1", xy=(v1, p1), xytext=(v1 + 0.05, p1 + 30),
                fontsize=12, fontweight="bold")

    ax.set_xlabel("M\u011brn\u00fd objem v", fontsize=11)
    ax.set_ylabel("Tlak p [kPa]", fontsize=11)
    ax.set_title("p-v diagram: srovn\u00e1n\u00ed typ\u016f komprese\n(izotermick\u00e1 vy\u017eaduje nejm\u00e9n\u011b pr\u00e1ce)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(0, 1.15)
    ax.set_ylim(0, 1000)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q05_pv_compression.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_clearance_effect():
    """Effect of clearance volume on volumetric efficiency."""
    fig, ax = plt.subplots(figsize=(8, 5.5))
    kappa = 1.4

    pi = np.linspace(1, 10, 200)  # pressure ratio

    for c, color, label in [(0, COLORS[2], "c = 0 (ide\u00e1ln\u00ed)"),
                             (0.04, COLORS[0], "c = 4 %"),
                             (0.08, COLORS[1], "c = 8 %"),
                             (0.12, COLORS[3], "c = 12 %")]:
        eta_v = 1 - c * (pi**(1/kappa) - 1)
        eta_v = np.clip(eta_v, 0, 1)
        ax.plot(pi, eta_v * 100, color=color, linewidth=2.5, label=label)

    ax.set_xlabel("Tlakov\u00fd pom\u011br \u03c0 = p\u2082/p\u2081 [-]", fontsize=11)
    ax.set_ylabel("Objemov\u00e1 \u00fa\u010dinnost \u03b7_v [%]", fontsize=11)
    ax.set_title("Vliv \u0161kodliv\u00e9ho prostoru na objemovou \u00fa\u010dinnost\n(\u03ba = 1,4)",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=9)
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 105)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q05_clearance.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_multistage():
    """p-v diagram of two-stage compression with intercooling."""
    fig, ax = plt.subplots(figsize=(8, 5.5))
    kappa = 1.4
    n = 1.3

    p1 = 100  # kPa
    v1 = 1.0
    p3 = 900  # final pressure
    p2 = np.sqrt(p1 * p3)  # optimal intermediate pressure

    v_range = np.linspace(0.05, 1.1, 500)

    # Single stage (polytropic)
    p_single = p1 * (v1 / v_range)**n
    ax.plot(v_range, p_single, color=COLORS[1], linewidth=2, linestyle="--", alpha=0.6,
            label="Jednostup\u0148ov\u00e1 (v\u00edce pr\u00e1ce)")

    # Stage 1: p1 -> p2
    p_s1 = p1 * (v1 / v_range)**n
    mask1 = p_s1 <= p2
    ax.plot(v_range[mask1], p_s1[mask1], color=COLORS[0], linewidth=2.5)

    # Intercooling at p2 (isobaric, T back to T1 -> v back to v at p2 isothermal)
    v2_hot = v1 * (p1 / p2)**(1/n)
    v2_cool = v1 * p1 / p2  # isothermal: same T -> pv = p1*v1
    ax.plot([v2_hot, v2_cool], [p2, p2], color=COLORS[2], linewidth=2.5)

    # Stage 2: p2 -> p3
    p_s2 = p2 * (v2_cool / v_range)**n
    mask2 = (p_s2 >= p2) & (p_s2 <= p3)
    ax.plot(v_range[mask2], p_s2[mask2], color=COLORS[0], linewidth=2.5)

    # Labels
    ax.axhline(y=p1, color="gray", linewidth=0.5, linestyle=":")
    ax.axhline(y=p2, color="gray", linewidth=0.5, linestyle=":")
    ax.axhline(y=p3, color="gray", linewidth=0.5, linestyle=":")
    ax.text(1.05, p1, "$p_1$", fontsize=10, color="gray")
    ax.text(1.05, p2, f"$p_2 = \\sqrt{{p_1 p_3}}$ = {p2:.0f}", fontsize=9, color="gray")
    ax.text(1.05, p3, "$p_3$", fontsize=10, color="gray")

    # Intercooling annotation
    ax.annotate("Mezichladi\u010d\n(T \u2192 T\u2081)", xy=((v2_hot + v2_cool) / 2, p2),
                xytext=(0.6, p2 + 100), fontsize=9, fontweight="bold", color=COLORS[2],
                arrowprops=dict(arrowstyle="->", color=COLORS[2], lw=1.5))

    # Shaded area = saved work
    ax.fill_between(v_range[mask1], p_s1[mask1], alpha=0.05, color=COLORS[0])
    ax.text(0.3, 500, "\u00daSPORA\nPR\u00c1CE", fontsize=10, fontweight="bold",
            color=COLORS[2], ha="center", alpha=0.7)

    ax.plot(v1, p1, "ko", markersize=10, zorder=5)
    ax.set_xlabel("M\u011brn\u00fd objem v", fontsize=11)
    ax.set_ylabel("Tlak p [kPa]", fontsize=11)
    ax.set_title("Dvoustup\u0148ov\u00e1 komprese s mezichlazen\u00edm\n\u00faspora pr\u00e1ce oproti jednostup\u0148ov\u00e9",
                 fontsize=11, fontweight="bold")
    ax.legend(fontsize=9, loc="upper right")
    ax.set_xlim(0, 1.15)
    ax.set_ylim(0, 1050)

    fig.tight_layout()
    path = os.path.join(IMG_DIR, "q05_multistage.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


# ======================================================================
# OBSAH
# ======================================================================

def generate():
    print("Generuji diagramy...")
    img_pv = generate_pv_compression()
    img_clear = generate_clearance_effect()
    img_multi = generate_multistage()
    print("Diagramy hotov\u00e9. Generuji .docx...")

    doc = create_document(
        title="5. Stroje na stla\u010dov\u00e1n\u00ed a dopravu vzdu\u0161in, rozd\u011blen\u00ed.\n"
              "    Jednostup\u0148ov\u00e1 a v\u00edcestup\u0148ov\u00e1 komprese. \u0160kodliv\u00fd prostor, p\u0159\u00edkon.",
        okruh="Termomechanika a spalov\u00e1n\u00ed",
    )

    add_heading(doc, "Zad\u00e1n\u00ed", level=2)
    add_para(doc,
        "Rozd\u011blte stroje na stla\u010dov\u00e1n\u00ed a dopravu vzdu\u0161in. Vysv\u011btlete jednostup\u0148ovou "
        "a v\u00edcestup\u0148ovou kompresi, vliv \u0161kodliv\u00e9ho prostoru na v\u00fdkonnost kompresoru, "
        "d\u016fvody v\u00edcestup\u0148ov\u00e9 komprese a v\u00fdpo\u010det p\u0159\u00edkonu.")

    # ==================================================================
    # CAST 1
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 1: Teoretick\u00fd rozbor", level=2)

    add_heading(doc, "1.1 Rozd\u011blen\u00ed stroj\u016f", level=3)

    add_styled_table(doc,
        headers=["Skupina", "Typ", "Princip", "\u03c0 typick\u00e9"],
        data=[
            ["Objemov\u00e9", "P\u00edstov\u00fd", "Zm\u011bna objemu v\u00e1lce", "2\u201310 (stupe\u0148)"],
            ["Objemov\u00e9", "Lamelové, \u0161roubov\u00e9", "Rotační objemov\u00e9 \u010derp\u00e1n\u00ed", "3\u201315"],
            ["Rychlostn\u00ed", "Radi\u00e1ln\u00ed (turbo)", "Odst\u0159ediv\u00e1 s\u00edla", "2\u20138 (stupe\u0148)"],
            ["Rychlostn\u00ed", "Axi\u00e1ln\u00ed (turbo)", "Odklon proud\u011bn\u00ed lopatkami", "1,1\u20131,4 (st.)"],
            ["Proud\u011bn\u00edm", "Ejektory", "Hn\u00e1n\u00ed vysoko-tl. proudem", "< 2"],
        ],
    )

    add_para(doc, "Podle dosa\u017een\u00e9ho tlaku:", bold=True, keep_with_next=True)
    add_bullet(doc, "Ventil\u00e1tory: \u03c0 < 1,1 (p\u0159etlak < 10 kPa)")
    add_bullet(doc, "Dmychadla: \u03c0 = 1,1\u20133")
    add_bullet(doc, "Kompresory: \u03c0 > 3 (a\u017e stovky)", is_last=True)

    # -- 1.2 Jednostupnova --
    add_heading(doc, "1.2 Jednostup\u0148ov\u00e1 komprese", level=3)

    add_para(doc, "Technick\u00e1 pr\u00e1ce kompresoru (pr\u00e1ce dodan\u00e1 plynu):", keep_with_next=True)
    add_equation(doc, r"w_t = -\int_1^2 v \, dp", label="1")

    add_para(doc, "Pro polytropickou kompresi (pv\u207f = konst.):", keep_with_next=True)
    add_equation(doc, r"w_t = \frac{n}{n-1} p_1 v_1 \left[\left(\frac{p_2}{p_1}\right)^{\frac{n-1}{n}} - 1\right]", label="2")

    add_para(doc, "Pro izotermickou kompresi (n = 1):", keep_with_next=True)
    add_equation(doc, r"w_{t,izo} = p_1 v_1 \ln\frac{p_2}{p_1} = r T_1 \ln\frac{p_2}{p_1}", label="3")

    add_image(doc, img_pv, width_cm=14,
              caption="Obr. 1: Srovn\u00e1n\u00ed izotermick\u00e9, polytropick\u00e9 a izoentropick\u00e9 komprese v p-v diagramu")

    add_info_box(doc,
        "Izotermick\u00e1 komprese = nejm\u00e9n\u011b pr\u00e1ce",
        "Proto\u017ee teplo vznikl\u00e9 kompres\u00ed se pr\u016fb\u011b\u017en\u011b odv\u00e1d\u00ed chlazením. "
        "V praxi se j\u00ed p\u0159ibli\u017eujeme v\u00edcestup\u0148ovou kompres\u00ed s mezichlazením.")

    # -- 1.3 Skodlivy prostor --
    add_page_break(doc)
    add_heading(doc, "1.3 \u0160kodliv\u00fd prostor", level=3)

    add_info_box(doc,
        "\u0160kodliv\u00fd prostor",
        "Objem v\u00e1lce, kter\u00fd z\u016fst\u00e1v\u00e1 napln\u011bn stla\u010den\u00fdm plynem i v horn\u00ed \u00favrati p\u00edstu. "
        "Pom\u011brn\u00fd \u0161kodliv\u00fd prostor: c = V_0 / V_z (typicky 3\u201312 %).")

    add_para(doc, "Objemov\u00e1 \u00fa\u010dinnost (volumetrick\u00e1):", keep_with_next=True)
    add_equation(doc, r"\eta_v = 1 - c \left[\left(\frac{p_2}{p_1}\right)^{1/n} - 1\right]", label="4")

    add_para(doc, "D\u016fsledky:", keep_with_next=True)
    add_bullet(doc, "S rostouc\u00edm \u03c0 kles\u00e1 \u03b7_v \u2014 kompresor dopravuje m\u00e9n\u011b plynu")
    add_bullet(doc, "P\u0159i ur\u010dit\u00e9m \u03c0_{max} klesne \u03b7_v na 0 (kompresor ned\u00e1v\u00e1 \u017e\u00e1dn\u00fd v\u00fdkon)")
    add_bullet(doc, "Men\u0161\u00ed c \u2192 vy\u0161\u0161\u00ed \u03b7_v (lep\u0161\u00ed konstrukce)", is_last=True)

    add_image(doc, img_clear, width_cm=13,
              caption="Obr. 2: Vliv \u0161kodliv\u00e9ho prostoru na objemovou \u00fa\u010dinnost")

    # -- 1.4 Vicestupnova --
    add_page_break(doc)
    add_heading(doc, "1.4 V\u00edcestup\u0148ov\u00e1 komprese s mezichlazením", level=3)

    add_para(doc, "D\u016fvody pro v\u00edcestup\u0148ovou kompresi:", bold=True, keep_with_next=True)
    add_bullet(doc, "Sn\u00ed\u017een\u00ed pr\u00e1ce (p\u0159ibli\u017eujeme se izotermick\u00e9 kompresi)")
    add_bullet(doc, "Omezen\u00ed v\u00fdstupn\u00ed teploty (maz\u00e1n\u00ed, t\u011bsn\u011bn\u00ed, bezpe\u010dnost)")
    add_bullet(doc, "Zv\u00fd\u0161en\u00ed objemov\u00e9 \u00fa\u010dinnosti (ni\u017e\u0161\u00ed \u03c0 na stupe\u0148)")
    add_bullet(doc, "Konstruk\u010dn\u00ed d\u016fvody (men\u0161\u00ed s\u00edly na p\u00edst)", is_last=True)

    add_para(doc, "Optim\u00e1ln\u00ed rozd\u011blen\u00ed tlak\u016f pro z stup\u0148\u016f:", keep_with_next=True)
    add_equation(doc, r"\pi_i = \left(\frac{p_{konec}}{p_{za\check{c}}}\right)^{1/z} = \text{konst.}", label="5")

    add_para(doc, "Pro 2 stupn\u011b:", keep_with_next=True)
    add_equation(doc, r"p_2 = \sqrt{p_1 \cdot p_3}", label="6")

    add_image(doc, img_multi, width_cm=14,
              caption="Obr. 3: Dvoustup\u0148ov\u00e1 komprese s mezichlazením \u2014 \u00faspora pr\u00e1ce")

    add_para(doc, "\u00daspora pr\u00e1ce p\u0159i z stup\u0148\u00edch vs. 1 stupe\u0148:", keep_with_next=True)
    add_equation(doc, r"w_{z\text{-}st} = z \cdot \frac{n}{n-1} p_1 v_1 \left[\left(\frac{p_{konec}}{p_{za\check{c}}}\right)^{\frac{n-1}{nz}} - 1\right]", label="7")

    # -- 1.5 Prikon --
    add_heading(doc, "1.5 P\u0159\u00edkon kompresoru", level=3)

    add_equation(doc, r"P = \frac{\dot{m} \cdot w_t}{\eta_{mech} \cdot \eta_{el}}", label="8")

    add_para(doc, "kde:", keep_with_next=True)
    add_bullet(doc, "m\u0307 \u2014 hmotnostn\u00ed pr\u016ftok [kg/s]")
    add_bullet(doc, "w_t \u2014 m\u011brn\u00e1 technick\u00e1 pr\u00e1ce [J/kg]")
    add_bullet(doc, "\u03b7_{mech} \u2014 mechanick\u00e1 \u00fa\u010dinnost (t\u0159en\u00ed, ~95 %)")
    add_bullet(doc, "\u03b7_{el} \u2014 \u00fa\u010dinnost el. motoru (~90\u201395 %)", is_last=True)

    add_para(doc, "Izoentropick\u00e1 \u00fa\u010dinnost kompresoru:", keep_with_next=True)
    add_equation(doc, r"\eta_{is} = \frac{w_{t,is}}{w_{t,skut}} = \frac{h_{2s} - h_1}{h_2 - h_1}", label="9")

    # ==================================================================
    # CAST 2
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 2: Praktick\u00fd rozbor", level=2)

    add_heading(doc, "2.1 Typick\u00e9 parametry", level=3)
    add_styled_table(doc,
        headers=["Typ", "\u03c0 (stupe\u0148)", "V\u0307 [m\u00b3/h]", "\u03b7_{is}"],
        data=[
            ["P\u00edstov\u00fd", "2\u201310", "1\u20131000", "70\u201385 %"],
            ["\u0160roubov\u00fd", "3\u201315", "100\u201310000", "70\u201388 %"],
            ["Radi\u00e1ln\u00ed turbo", "2\u20138", "1000\u2013100000", "78\u201385 %"],
            ["Axi\u00e1ln\u00ed turbo", "1,1\u20131,4/st.", "10000+", "85\u201392 %"],
        ],
    )

    add_heading(doc, "2.2 Omezen\u00ed v\u00fdstupn\u00ed teploty", level=3)
    add_para(doc,
        "P\u0159i polytropick\u00e9 kompresi roste teplota: T\u2082 = T\u2081\u00b7\u03c0^((n-1)/n). "
        "P\u0159i \u03c0 = 8, n = 1,3, T\u2081 = 20 \u00b0C: T\u2082 \u2248 220 \u00b0C. "
        "P\u0159i \u03c0 = 8, n = 1,4: T\u2082 \u2248 270 \u00b0C. "
        "Omezen\u00ed: maz\u00e1n\u00ed (< 180 \u00b0C), bezpe\u010dnost (< 200 \u00b0C pro vzduch). "
        "Proto se pou\u017e\u00edv\u00e1 v\u00edcestup\u0148ov\u00e1 komprese s mezichlazením.")

    # ==================================================================
    # CAST 3
    # ==================================================================
    add_page_break(doc)
    add_heading(doc, "\u010c\u00e1st 3: Ilustra\u010dn\u00ed p\u0159\u00edklad", level=2)
    add_heading(doc, "P\u0159\u00edklad: Dvoustup\u0148ov\u00e1 komprese vzduchu", level=3)

    add_para(doc,
        "Zad\u00e1n\u00ed: Vzduch (\u03ba = 1,4, r = 287,1 J/(kg\u00b7K)) se komprimuje z p\u2081 = 100 kPa, "
        "T\u2081 = 20 \u00b0C na p\u2083 = 900 kPa dvoustup\u0148ov\u011b s mezichlazením na T\u2081. "
        "Polytropick\u00fd exponent n = 1,3. Ur\u010dete optim\u00e1ln\u00ed p\u2082, pr\u00e1ci a \u00fasporu oproti 1 stupni.",
        bold=True)

    add_para(doc, "Krok 1: Optim\u00e1ln\u00ed mezitlak", bold=True)
    add_equation(doc, r"p_2 = \sqrt{p_1 \cdot p_3} = \sqrt{100 \times 900} = 300 \text{ kPa}")

    add_para(doc, "Krok 2: Pr\u00e1ce jednoho stupn\u011b (\u03c0 = 3)", bold=True)
    add_equation(doc, r"w_1 = \frac{n}{n-1} r T_1 \left[\pi^{\frac{n-1}{n}} - 1\right] = \frac{1{,}3}{0{,}3} \times 287{,}1 \times 293{,}15 \times \left[3^{0{,}231} - 1\right]")
    add_equation(doc, r"w_1 = 4{,}333 \times 287{,}1 \times 293{,}15 \times (1{,}291 - 1) = 4{,}333 \times 84\,172 \times 0{,}291")
    add_equation(doc, r"w_1 = 106\,200 \text{ J/kg} = 106{,}2 \text{ kJ/kg}")

    add_para(doc, "Krok 3: Celkov\u00e1 pr\u00e1ce 2 stup\u0148\u016f (po mezichlazení w\u2082 = w\u2081)", bold=True)
    add_equation(doc, r"w_{2st} = 2 \times 106{,}2 = 212{,}4 \text{ kJ/kg}")

    add_para(doc, "Krok 4: Pr\u00e1ce p\u0159i jednostup\u0148ov\u00e9 kompresi (\u03c0 = 9)", bold=True)
    add_equation(doc, r"w_{1st} = \frac{1{,}3}{0{,}3} \times 287{,}1 \times 293{,}15 \times \left[9^{0{,}231} - 1\right] = 364\,711 \times (1{,}697 - 1)")
    add_equation(doc, r"w_{1st} = 364\,711 \times 0{,}697 = 254\,200 \text{ J/kg} = 254{,}2 \text{ kJ/kg}")

    add_para(doc, "Krok 5: \u00daspora", bold=True)
    add_equation(doc, r"\Delta w = w_{1st} - w_{2st} = 254{,}2 - 212{,}4 = 41{,}8 \text{ kJ/kg}")
    add_equation(doc, r"\text{\u00daspora} = \frac{41{,}8}{254{,}2} \times 100 = 16{,}4 \%")

    add_info_box(doc,
        "V\u00fdsledky:",
        "Optim\u00e1ln\u00ed mezitlak: p\u2082 = 300 kPa\n"
        "Pr\u00e1ce 2 stupn\u011b: 212,4 kJ/kg\n"
        "Pr\u00e1ce 1 stupe\u0148: 254,2 kJ/kg\n"
        "\u00daspora: 41,8 kJ/kg = 16,4 %\n\n"
        "Nav\u00edc: v\u00fdstupn\u00ed T p\u0159i 1 stupni: T\u2082 = 293\u00d79^{0,231} = 498 K = 225 \u00b0C (nebezpe\u010dn\u00e9!)\n"
        "P\u0159i 2 stup\u0148\u00edch: max T = 293\u00d73^{0,231} = 378 K = 105 \u00b0C (bezpe\u010dn\u00e9)")

    # ==================================================================
    # CAST 4
    # ==================================================================
    add_exam_questions(doc, [
        ("Pro\u010d je izotermick\u00e1 komprese energeticky nejv\u00fdhodn\u011bj\u0161\u00ed?",
         "Proto\u017ee ve\u0161ker\u00e9 teplo vznikl\u00e9 kompres\u00ed se pr\u016fb\u011b\u017en\u011b odv\u00e1d\u00ed chlazením. "
         "Plyn se neoh\u0159\u00edv\u00e1, tak\u017ee m\u011brn\u00fd objem kles\u00e1 nejrychleji a plocha pod "
         "k\u0159ivkou v p-v (\u2248 pr\u00e1ce) je nejmen\u0161\u00ed."),

        ("Co je \u0161kodliv\u00fd prostor a pro\u010d sni\u017euje v\u00fdkonnost?",
         "Objem v\u00e1lce, kter\u00fd nelze vypr\u00e1zdnit (ventily, v\u016fle p\u00edstu). "
         "Stla\u010den\u00fd plyn v n\u011bm se p\u0159i expanzi rozpíná zp\u011bt, \u010d\u00edm\u017e zab\u00edr\u00e1 \u010d\u00e1st zdvihu. "
         "P\u0159i vysok\u00e9m \u03c0 m\u016f\u017ee \u03b7_v klesnout na 0 \u2014 p\u00edst se jen pohybuje sem a tam."),

        ("Pro\u010d je optim\u00e1ln\u00ed mezitlak geometrick\u00fdm pr\u016fm\u011brem?",
         "Minim\u00e1ln\u00ed pr\u00e1ce p\u0159i dvoustup\u0148ov\u00e9 kompresi s mezichlazením na T\u2081 nastane, "
         "kdy\u017e jsou tlakov\u00e9 pom\u011bry na obou stup\u0148\u00edch stejn\u00e9. "
         "To vede na p\u2082/p\u2081 = p\u2083/p\u2082, tedy p\u2082 = \u221a(p\u2081\u00b7p\u2083)."),

        ("Jak\u00e9 jsou d\u016fvody pro v\u00edcestup\u0148ovou kompresi?",
         "1) \u00daspora pr\u00e1ce (mezichlazení p\u0159ibli\u017euje izotermick\u00e9 kompresi). "
         "2) Sn\u00ed\u017een\u00ed v\u00fdstupn\u00ed teploty (maz\u00e1n\u00ed, t\u011bsn\u011bn\u00ed, bezpe\u010dnost). "
         "3) Zv\u00fd\u0161en\u00ed \u03b7_v (ni\u017e\u0161\u00ed \u03c0 na stupe\u0148). "
         "4) Men\u0161\u00ed konstruk\u010dn\u00ed nam\u00e1h\u00e1n\u00ed."),

        ("Jak\u00fd je rozd\u00edl mezi ventil\u00e1torem, dmychadlem a kompresorem?",
         "Ventil\u00e1tor: \u03c0 < 1,1 (p\u0159etlak < 10 kPa), z\u00e1kladní \u010derp\u00e1n\u00ed vzduchu. "
         "Dmychadlo: \u03c0 = 1,1\u20133, dopravn\u00ed pneumatika, spalovac\u00ed vzduch. "
         "Kompresor: \u03c0 > 3, stla\u010den\u00fd vzduch pro pneumatiku, chlazen\u00ed, plyny."),

        ("Co je izoentropick\u00e1 \u00fa\u010dinnost kompresoru?",
         "Pom\u011br ide\u00e1ln\u00ed (izoentropick\u00e9) pr\u00e1ce ku skute\u010dn\u00e9: \u03b7_is = w_{is}/w_{skut}. "
         "U kompresoru je w_{is} < w_{skut} (\u03b7_is < 1), proto\u017ee nevratnosti "
         "(t\u0159en\u00ed, v\u00edry) vy\u017eaduj\u00ed v\u00edce pr\u00e1ce. Typicky 70\u201390 %."),
    ])

    doc.add_paragraph()
    doc.add_paragraph("\u2500" * 60)
    add_para(doc, "Zdroje a doporu\u010den\u00e1 literatura:", bold=True, size=10, keep_with_next=True)
    add_bullet(doc, "\u010cengel, Y.A., Boles, M.A.: Thermodynamics \u2014 An Engineering Approach")
    add_bullet(doc, "Pavelek, M. a kol.: Termomechanika, CERM Brno")
    add_bullet(doc, "Kadrnožka, J.: Kompresory, SNTL")
    add_bullet(doc, "Bl\u00e1ha, J., Brada, K.: P\u0159\u00edru\u010dka \u010derpac\u00ed techniky, \u010cVUT Praha")
    add_bullet(doc, "ISO 1217 \u2014 Objemov\u00e9 kompresory, p\u0159ej\u00edmac\u00ed zkou\u0161ky", is_last=True)

    save_and_export(doc, "05-kompresory")


if __name__ == "__main__":
    generate()
