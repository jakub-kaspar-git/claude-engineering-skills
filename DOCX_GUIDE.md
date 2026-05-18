# Průvodce generováním .docx dokumentů

Tento dokument obsahuje detailní instrukce pro generování státnicových otázek do formátu .docx s OMML rovnicemi a vizuálními prvky.

## Výstupní formát: .docx

Výstupem zpracování každé otázky je soubor **.docx** (Microsoft Word). Pro generování použij `docx_engine.py` (sdílený toolkit) a per-question skript v `questions/`.

### Workflow

```
1. Uživatel zadá státnicovou otázku
2. Claude načte příslušné skilly z skills/thinking/ a skills/databases/
3. Claude napíše questions/qXX_nazev.py importující z docx_engine
4. Claude spustí skript → hotový .docx + .pdf v output/
```

### Příklad per-question skriptu

```python
from docx_engine import (
    create_document, save_and_export, add_heading, add_para,
    add_equation, add_bullet, add_image, add_info_box,
    add_warning_box, add_page_break, add_styled_table,
    COLORS, IMG_DIR,
)

def generate():
    doc = create_document(
        title="12. Bernoulliho rovnice",
        okruh="Mechanika tekutin",
    )
    # ... obsah otázky ...
    save_and_export(doc, "12-bernoulliho-rovnice")

if __name__ == "__main__":
    generate()
```

## Rovnice — OMML formát

- Používej `docx_engine.add_equation(doc, latex_str, label=None)`
- Rovnice se převádí LaTeX → MathML → OMML (Office Math Markup Language)
- Rovnice NESMÍ být jako prostý text ani jako obrázky — musí být editovatelné Word equations
- Každá rovnice má být na samostatném řádku jako Word equation objekt

## Vizuální prvky — POVINNÉ v každém dokumentu

Dokument musí být vizuálně bohatý a srozumitelný. Ke každé otázce generuj co nejvíce relevantních vizuálních prvků:

### 1. Diagramy a grafy (matplotlib → PNG → vložit do .docx)
- p-V, T-s, h-s diagramy pro termodynamické děje
- Charakteristiky čerpadel (H-Q, η-Q, P-Q křivky)
- Proudová pole, rychlostní profily
- Moodyho diagram, závislosti součinitelů
- Fázové diagramy, oblasti stavů
- Generuj pomocí matplotlib, ulož jako PNG do `output/img/`, vlož přes `add_image(doc, path)`

### 2. Schémata a blokové diagramy (matplotlib / tabulky)
- Schémata systémů (směšovací komory, cykly, obvody)
- Kontrolní objemy s vyznačenými toky a bilancemi
- Blokové diagramy procesů
- Kreslí se pomocí matplotlib (patches, arrows, annotate) nebo jako formátované tabulky

### 3. Srovnávací a přehledové tabulky (python-docx tabulky)
- Srovnání metod, rovnic, modelů
- Přehledy vlastností, parametrů, konstant
- Rozhodovací matice (kdy použít co)
- Použij `add_styled_table(doc, headers, data)`

### 4. Barevné rámečky a zvýraznění
- Klíčové definice: `add_info_box(doc, title, text)` (modrý rámeček)
- Varování: `add_warning_box(doc, text)` (žlutý rámeček)
- Důležité rovnice odsaď a očísluj pomocí `label` parametru

## Struktura .docx dokumentu

- Záhlaví: název otázky, okruh, datum (automaticky přes `create_document()`)
- Část 1: Teoretický rozbor (hlavní obsah, ~55 % dokumentu) — s diagramy, schématy, přehledovými tabulkami
- Část 2: Praktický rozbor (~25 % dokumentu) — se srovnávacími tabulkami, příklady z praxe
- Část 3: Ilustrační příklad (~15 % dokumentu) — s grafem výsledků
- Část 4: Typické zkouškové otázky (~10 % dokumentu) — 5–8 otázek s odpověďmi
- Zápatí: odkazy na normy a zdroje

## Stránkování a rozložení — POVINNÉ

Dokument musí být čitelný a logicky členěný po stránkách:

### Page breaks před hlavními celky
- Vždy vlož `add_page_break(doc)` před Část 1, Část 2, Část 3
- Page break před každou novou podkapitolou (1.3, 1.5, 1.6, 1.7...) pokud by předchozí obsah přesáhl stránku
- Cíl: každý logický celek začíná na nové stránce

### Keep with next (nadpis + první odstavec)
- Nadpisy vždy zůstanou na stejné stránce jako následující odstavec (automaticky v `add_heading()`)
- Text před rovnicí musí zůstat na stejné stránce jako rovnice (`keep_with_next=True`)
- Popisek tabulky/obrázku zůstane s tabulkou/obrázkem

### Keep together (nedělit odstavce)
- Žádný odstavec se nesmí rozdělit mezi dvě stránky (automaticky v `add_para()`)
- Odrážkové seznamy zůstanou pohromadě — všechny odrážky kromě poslední mají `keepNext` (automaticky v `add_bullet()`)
- Info boxy a warning boxy se nesmí rozdělit (automaticky v `add_info_box()`, `add_warning_box()`)

### Obrázky + popisek
- Obrázek a jeho caption zůstanou vždy na stejné stránce (automaticky v `add_image()`)

## PDF export — POVINNÝ

Po uložení .docx se automaticky vygeneruje PDF kopie do `output/pdf/`. Řeší `save_and_export()`.

- Konverze přes Microsoft Word COM (Windows) pomocí `comtypes`
- Pokud Word COM není dostupný, vypíše varování a přeskočí PDF export

## docx_engine.py — API reference

| Funkce | Účel |
|---|---|
| `create_document(title, okruh)` | Nový Document se záhlavím |
| `save_and_export(doc, filename)` | Uloží .docx + PDF, vrátí cesty |
| `add_heading(doc, text, level)` | Stylovaný nadpis |
| `add_para(doc, text, bold, italic, size, keep_with_next)` | Odstavec |
| `add_equation(doc, latex_str, label)` | OMML rovnice |
| `add_bullet(doc, text, level, is_last)` | Odrážka |
| `add_image(doc, path, width_cm, caption)` | Obrázek s popiskem |
| `add_info_box(doc, title, text)` | Modrý info rámeček |
| `add_warning_box(doc, text)` | Žlutý warning rámeček |
| `add_exam_questions(doc, questions)` | Sekce zkouškových Q&A (list of (q, a) tuples) |
| `add_styled_table(doc, headers, data, style)` | Tabulka s formátovaným záhlavím |
| `add_page_break(doc)` | Konec stránky |
| `latex_to_omml(latex_str)` | LaTeX → OMML element |
| `docx_to_pdf(docx_path, pdf_path)` | Word COM PDF export |

## Python závislosti

```
python-docx lxml latex2mathml    # generování .docx s rovnicemi
comtypes                         # PDF export přes Word COM (Windows)
numpy scipy sympy pint           # ilustrační výpočty
fluids thermo CoolProp           # inženýrská data
matplotlib                       # vizualizace
```
