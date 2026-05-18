# Spec: Refactoring docx_engine — oddělení enginu od obsahu

## Objective

Rozdělit monolitický `generate_question.py` (875 řádků) na:

1. **`docx_engine.py`** — sdílený toolkit pro generování .docx dokumentů s OMML rovnicemi, vizuálními prvky a PDF exportem
2. **`questions/q06_realny_plyn.py`** — per-question skript obsahující pouze obsah a specifické grafy, importující z `docx_engine`

**Proč:** Každá nová státnicová otázka vyžaduje psát celý skript od nuly. Po refactoringu stačí napsat jen obsah a grafy (~400 řádků místo ~875), zbytek dodá engine.

**Kdo to používá:** Student (autor) zadává Claude otázku → Claude napíše per-question skript → spustí ho → dodá hotový .docx + .pdf.

### Success Criteria

- [ ] `python questions/q06_realny_plyn.py` vygeneruje funkční `output/06-realny-plyn-smesi-plynu.docx`
- [ ] Výstupní .docx má stejnou strukturu a obsah jako původní (rovnice, grafy, tabulky, info boxy)
- [ ] PDF export funguje (pokud je dostupný Word COM)
- [ ] `generate_question.py` zůstává netknutý (zachován jako reference)
- [ ] Nový per-question skript je kratší a čitelnější než originál

## Tech Stack

- Python 3.10+
- `python-docx`, `lxml`, `latex2mathml` — generování .docx s OMML rovnicemi
- `matplotlib`, `numpy` — vizualizace
- `comtypes` — PDF export přes Word COM (Windows only)

## Commands

```
Install deps:    pip install python-docx lxml latex2mathml matplotlib numpy comtypes
Run question:    python questions/q06_realny_plyn.py
Run old script:  python generate_question.py
```

## Project Structure

```
project/
├── CLAUDE.md                    # Instrukce pro Claude (existující)
├── SPEC.md                      # Tato specifikace
├── generate_question.py         # Původní monolitický skript (NEMĚNIT)
├── docx_engine.py               # NOVÝ: sdílený toolkit
├── questions/                   # NOVÝ: per-question skripty
│   ├── __init__.py
│   └── q06_realny_plyn.py       # Obsah otázky 6
├── output/                      # Generované dokumenty
│   ├── *.docx
│   ├── img/                     # Generované PNG diagramy
│   └── pdf/                     # Exportované PDF
└── skills/                      # Engineering skills (existující)
```

## API Design: docx_engine.py

### Exportované funkce

```python
# ── Paths ──
BASE_DIR: str       # Kořen projektu (dirname tohoto souboru)
OUTPUT_DIR: str     # output/
IMG_DIR: str        # output/img/

# ── OMML ──
latex_to_omml(latex_str: str) -> etree._Element

# ── Document helpers ──
add_equation(doc, latex_str, label=None) -> Paragraph
add_heading(doc, text, level=1) -> Paragraph
add_para(doc, text, bold=False, italic=False, size=11, keep_with_next=False) -> Paragraph
add_bullet(doc, text, level=0, is_last=False) -> Paragraph
add_image(doc, path, width_cm=14, caption=None) -> Paragraph
add_info_box(doc, title, text) -> None
add_warning_box(doc, text) -> None
add_page_break(doc) -> Paragraph

# ── Styled table ──
add_styled_table(doc, headers: list[str], data: list[list[str]],
                 style="Light Grid Accent 1") -> Table

# ── Document lifecycle ──
create_document(title: str, okruh: str) -> Document
    # Vytvoří Document s Calibri 11pt, záhlaví (název, okruh, datum)

save_and_export(doc, filename: str) -> tuple[str, str | None]
    # Uloží .docx do output/, exportuje PDF do output/pdf/
    # Vrátí (docx_path, pdf_path_or_None)

# ── PDF ──
docx_to_pdf(docx_path, pdf_path) -> None

# ── Matplotlib ──
COLORS: list[str]   # Standardní barevná paleta
# plt.rcParams se nastaví při importu
```

### Nové convenience funkce (oproti originálu)

| Funkce | Důvod |
|---|---|
| `create_document(title, okruh)` | Každá otázka opakuje stejný setup (styl, záhlaví, datum) |
| `save_and_export(doc, filename)` | Každá otázka opakuje stejný save + PDF export boilerplate |
| `add_styled_table(doc, headers, data)` | Tabulky s formátovaným záhlavím se opakují 4× v q06 |

### Co engine NEOBSAHUJE

- Žádné `generate_*` funkce (specifické grafy)
- Žádný textový obsah otázek
- Žádnou `main()` / `generate()` funkci

## Code Style

```python
# Pojmenování: snake_case pro funkce/proměnné, UPPER_CASE pro konstanty
# Docstringy: jednořádkové pro helper funkce
# Type hints: ano pro public API, ne pro interní helpery
# Importy: seskupené (stdlib / third-party / local), sorted

# Příklad per-question skriptu:
from docx_engine import (
    create_document, save_and_export, add_heading, add_para,
    add_equation, add_bullet, add_image, add_info_box,
    add_warning_box, add_page_break, add_styled_table,
    COLORS, IMG_DIR,
)

def generate():
    doc = create_document(
        title="6. Reálný plyn, zjednodušený výpočet reálných plynů.\n"
              "    Směsi plynů. Adiabatické míšení v proudu.",
        okruh="Termodynamika",
    )
    # ... obsah ...
    save_and_export(doc, "06-realny-plyn-smesi-plynu")

if __name__ == "__main__":
    generate()
```

## Testing Strategy

- **Manuální test:** Spustit `python questions/q06_realny_plyn.py`, otevřít výstupní .docx ve Wordu, zkontrolovat rovnice, grafy, tabulky, stránkování
- **Smoke test:** Importovat `docx_engine` a zavolat `create_document()` — musí vrátit Document bez chyby
- **Regression:** Porovnat počet stránek a vizuálních prvků s původním výstupem

## Boundaries

- **Always:** Zachovat přesně stejné API helper funkcí (parametry, návratové hodnoty)
- **Always:** `generate_question.py` zůstává nezměněn
- **Ask first:** Přidání nových závislostí
- **Never:** Měnit existující soubory v `skills/`

## Open Questions

*Žádné — předpoklady odsouhlaseny.*
