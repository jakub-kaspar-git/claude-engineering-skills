---
name: pump-design
description: "Comprehensive pump design workflow — from selection through cavitation analysis to system integration"
category: thinking
domain: mechanical
complexity: advanced
dependencies:
  - numpy
  - scipy
  - matplotlib
  - CoolProp
---

# Pump Design — Zastřešující skill

## Overview

Komplexní workflow pro návrh, analýzu a optimalizaci čerpadlových systémů. Tento skill zastřešuje 6 specializovaných sub-skillů, které pokrývají celý životní cyklus návrhu čerpadla.

## Sub-skilly

| Sub-skill | Zaměření | Kdy použít |
|---|---|---|
| [centrifugal-pumps](centrifugal-pumps/SKILL.md) | Eulerovy rovnice, rychlostní trojúhelníky, specifická rychloběžnost | Návrh nového odstředivého čerpadla |
| [positive-displacement-pumps](positive-displacement-pumps/SKILL.md) | Zubová, pístová, šroubová čerpadla, objemová účinnost | Návrh objemových čerpadel |
| [cavitation-analysis](cavitation-analysis/SKILL.md) | NPSH výpočty, kavitační riziko, ochranná opatření | Ověření kavitační bezpečnosti |
| [performance-curves](performance-curves/SKILL.md) | H-Q křivky, afinní zákony, mimo-návrhový provoz | Analýza provozních charakteristik |
| [efficiency-optimization](efficiency-optimization/SKILL.md) | Optimalizace účinnosti, provozní strategie | Zvýšení účinnosti existujícího systému |
| [system-integration](system-integration/SKILL.md) | Potrubní sítě, regulace, paralelní/sériové zapojení | Návrh kompletního čerpadlového systému |

## Typický workflow návrhu

```
1. VÝBĚR TYPU
   → helpers/pump-selection-helper
   → centrifugal-pumps NEBO positive-displacement-pumps

2. HYDRAULICKÝ NÁVRH
   → centrifugal-pumps (Euler, velocity triangles, ns)
   → performance-curves (H-Q, η-Q, P-Q)

3. KAVITAČNÍ ANALÝZA
   → cavitation-analysis (NPSH_A vs NPSH_R)
   → databases/cavitation-risk-db

4. OPTIMALIZACE
   → efficiency-optimization
   → packages/scipy-optimization

5. SYSTÉMOVÁ INTEGRACE
   → system-integration (piping, controls, parallel/series)
   → databases/hydraulic-components-db
```

## Mapování na státnicové okruhy

- **Čerpadla a hydraulické stroje** — všechny sub-skilly
- **Mechanika tekutin** — cavitation-analysis, performance-curves
- **Návrh a optimalizace** — efficiency-optimization, system-integration

## Souvisící skilly

- `databases/pump-performance-db` — výrobcovské křivky (Grundfos, KSB, Flowserve)
- `databases/cavitation-risk-db` — tenze par, NPSH korelace
- `databases/hydraulic-components-db` — ztráty v potrubí a armaturách
- `helpers/pump-selection-helper` — rozhodovací strom pro výběr typu čerpadla
- `packages/fluids-package` — výpočty proudění v potrubí

## Normy a standardy

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
- **HI Standards** — Hydraulic Institute (NPSH, vibrace, hluk)
- **ISO 9906** — Rotodynamic pumps — Hydraulic performance acceptance tests
- **ISO 5199** — Technical specifications for centrifugal pumps
- **ASME B73.1** — Specification for Horizontal End Suction Centrifugal Pumps
