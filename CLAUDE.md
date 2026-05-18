# Claude Engineering Skills Library

## Popis projektu

Knihovna inženýrských Agent Skills pro zpracování vysokoškolských státnicových otázek z oblastí strojního inženýrství, leteckého inženýrství, mechaniky tekutin a návrhu čerpadel.

## Hlavní účel

Tento repozitář slouží jako znalostní báze pro přípravu a zpracování **státnicových otázek**. Claude používá skilly z `skills/` k:

1. **Rozboru otázky** - identifikace tématu, podoblasti a požadované hloubky
2. **Teoretickému výkladu** - fyzikální principy, definice, odvození klíčových vztahů
3. **Strukturované odpovědi** - odvození řešení s využitím příslušných vzorců, dat a metodologií
4. **Praktickému rozboru** - reálné aplikace, inženýrská praxe, typické problémy a řešení
5. **Vizualizaci** - generování grafů, diagramů a schémat kde je to přínosné
6. **Ilustračním příkladům** - výpočty pro pochopení teorie (doplňková část, ne hlavní důraz)

## Struktura skillů

```
skills/
├── databases/       # Materiálové a termodynamické databáze (CoolProp, REFPROP, kavitace)
├── helpers/         # Převody jednotek, výběr čerpadel, kalkulátor vlastností
├── integrations/    # OpenFOAM, ANSYS, SolidWorks, COMSOL
├── packages/        # NumPy, SciPy, Matplotlib, Pint, Fluids, Thermo
└── thinking/        # Analytické postupy: mechanika tekutin, termodynamika, FEA, čerpadla
```

## Mapování na státnicové okruhy

| Státnicový okruh | Relevantní skilly |
|---|---|
| Mechanika tekutin | `thinking/fluid-dynamics`, `databases/coolprop-db`, `packages/fluids-package` |
| Termodynamika | `thinking/thermodynamics`, `databases/coolprop-db`, `databases/nist-refprop` |
| Čerpadla a hydraulické stroje | `thinking/pump-design/*`, `databases/pump-performance-db`, `databases/cavitation-risk-db` |
| Pevnostní analýza (FEA) | `thinking/structural-analysis`, `integrations/ansys-simulation`, `integrations/comsol-multiphysics` |
| CFD a modelování proudění | `thinking/fluid-dynamics`, `integrations/openfoam-cfd`, `databases/turbulence-models-db` |
| Materiálové vlastnosti | `databases/material-properties-db`, `packages/thermo-package` |
| Návrh a optimalizace | `packages/scipy-optimization`, `thinking/pump-design/efficiency-optimization` |

## Jak zpracovávat státnicové otázky

### Postup pro každou otázku

1. **Klasifikace** — urči okruh (mechanika tekutin / termodynamika / čerpadla / pevnostní analýza / CFD)
2. **Aktivace skillů** — načti příslušné SKILL.md soubory z `skills/thinking/` pro metodologii a z `skills/databases/` pro data
3. **Teoretický výklad** (HLAVNÍ ČÁST) — fyzikální princip, definice pojmů, odvození klíčových vztahů, předpoklady a omezení platnosti
4. **Praktický rozbor** — kde se to uplatňuje v praxi, typické inženýrské problémy, reálné aplikace, souvislosti s dalšími tématy
5. **Ilustrační příklady** (DOPLŇKOVÁ ČÁST) — jednoduchý výpočet pro lepší pochopení teorie, ne jako hlavní obsah

### Výstupní formát: .docx

Výstup je soubor .docx generovaný přes `docx_engine.py` + per-question skript v `questions/`.

**Kompletní instrukce pro generování .docx viz [`DOCX_GUIDE.md`](DOCX_GUIDE.md).**

### Jazyk a notace

- Odpovědi piš **česky**, pokud není požadována angličtina
- Používej **SI jednotky** (skill `helpers/unit-converter` pro převody)
- Rovnice formátuj jako Word Equation objekty (OMML), ne jako prostý text
- Veličiny značí podle českých a ISO norem (p — tlak, T — teplota, v — rychlost, Q — průtok, H — dopravní výška)

## Aktivace skillů

Při každém dotazu:

1. Načti příslušný `SKILL.md` z `skills/thinking/` pro analytický postup
2. Pro vlastnosti tekutin použij `skills/databases/coolprop-db/SKILL.md`
3. Pro výpočty s jednotkami použij `skills/helpers/unit-converter/SKILL.md`
4. Pro vizualizaci použij `skills/packages/matplotlib-visualization/SKILL.md`

Plný obsah skillů načítej on-demand, ne všechny najednou.

## Pravidla

- Důraz na teorii a pochopení, ne na výpočty - výpočty jsou pouze ilustrační
- Vždy uveď fyzikální předpoklady a omezení platnosti vzorců
- Vysvětluj "proč", ne jen "jak" - student musí pochopit princip
- Pokud otázka přesahuje rozsah dostupných skillů, řekni to explicitně
- U kavitačních výpočtů vždy zahrnuj bezpečnostní rezervu (NPSH_available > NPSH_required)
- Odkazy na normy (ASME, API, ISO, HI) uvádej kde je to relevantní
- Všechny .docx soubory ukládej do složky `output/`, PDF kopie do `output/pdf/`

## Python závislosti

```
python-docx lxml latex2mathml    # generování .docx s rovnicemi
comtypes                         # PDF export přes Word COM (Windows)
numpy scipy sympy pint           # ilustrační výpočty
fluids thermo CoolProp           # inženýrská data
matplotlib                       # vizualizace
```
