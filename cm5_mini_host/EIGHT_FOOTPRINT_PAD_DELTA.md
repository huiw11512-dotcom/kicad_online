# High-priority footprint geometry differences (8 components)

**Source:** verified 50-component KiCad 10 mismatch inventory on MiniHost Rev.A.
Actual KiCad PCB-internal footprints compared to the exact named local/stock library (read-only).
The report compares local pad positions, dimensions, drill and pad type. It does NOT automatically replace any pads, mounts or net routing.

## U703 — Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm

- Actual board pad count: **4**; library pad count: **4**
- Changed individual pad-number groups: **4**
- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review

| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |
|---|---|---|---|---|---|
| pad 1 | -1.10000,0.85000 | -1.10000,0.85000 | 1.40000×1.20000; drill 0.00000×0.00000 | 1.40000×1.20000; drill 0.00000×0.00000 | pad shape differs |
| pad 2 | 1.10000,0.85000 | 1.10000,0.85000 | 1.40000×1.20000; drill 0.00000×0.00000 | 1.40000×1.20000; drill 0.00000×0.00000 | pad shape differs |
| pad 3 | 1.10000,-0.85000 | 1.10000,-0.85000 | 1.40000×1.20000; drill 0.00000×0.00000 | 1.40000×1.20000; drill 0.00000×0.00000 | pad shape differs |
| pad 4 | -1.10000,-0.85000 | -1.10000,-0.85000 | 1.40000×1.20000; drill 0.00000×0.00000 | 1.40000×1.20000; drill 0.00000×0.00000 | pad shape differs |

## U602 — Package_TO_SOT_SMD:SOT-353_SC-70-5

- Actual board pad count: **5**; library pad count: **5**
- Changed individual pad-number groups: **5**
- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review

| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |
|---|---|---|---|---|---|
| pad 1 | -0.95000,-0.65000 | -0.83750,-0.65000 | 0.65000×0.40000; drill 0.00000×0.00000 | 1.02500×0.35000; drill 0.00000×0.00000 | local position differs, copper size differs |
| pad 2 | -0.95000,0.00000 | -0.83750,0.00000 | 0.65000×0.40000; drill 0.00000×0.00000 | 1.02500×0.35000; drill 0.00000×0.00000 | local position differs, copper size differs |
| pad 3 | -0.95000,0.65000 | -0.83750,0.65000 | 0.65000×0.40000; drill 0.00000×0.00000 | 1.02500×0.35000; drill 0.00000×0.00000 | local position differs, copper size differs |
| pad 4 | 0.95000,0.65000 | 0.83750,0.65000 | 0.65000×0.40000; drill 0.00000×0.00000 | 1.02500×0.35000; drill 0.00000×0.00000 | local position differs, copper size differs |
| pad 5 | 0.95000,-0.65000 | 0.83750,-0.65000 | 0.65000×0.40000; drill 0.00000×0.00000 | 1.02500×0.35000; drill 0.00000×0.00000 | local position differs, copper size differs |

## C702 — Capacitor_Tantalum_SMD:CP_EIA-3528-21_Kemet-B

- Actual board pad count: **2**; library pad count: **2**
- Changed individual pad-number groups: **2**
- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review

| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |
|---|---|---|---|---|---|
| pad 1 | -1.53750,0.00000 | -1.54000,0.00000 | 1.32500×2.35000; drill 0.00000×0.00000 | 1.34000×2.39000; drill 0.00000×0.00000 | local position differs, copper size differs |
| pad 2 | 1.53750,0.00000 | 1.54000,0.00000 | 1.32500×2.35000; drill 0.00000×0.00000 | 1.34000×2.39000; drill 0.00000×0.00000 | local position differs, copper size differs |

## R702 — Resistor_SMD:R_0402_1005Metric

- Actual board pad count: **2**; library pad count: **2**
- Changed individual pad-number groups: **0**
- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review

| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |
|---|---|---|---|---|---|

## R703 — Resistor_SMD:R_0402_1005Metric

- Actual board pad count: **2**; library pad count: **2**
- Changed individual pad-number groups: **0**
- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review

| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |
|---|---|---|---|---|---|

## U1 — Package_LGA:LGA-16_3x3mm_P0.5mm_LayoutBorder3x5y

- Actual board pad count: **16**; library pad count: **16**
- Changed individual pad-number groups: **14**
- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review

| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |
|---|---|---|---|---|---|
| pad 1 | -1.22500,1.00000 | -1.22500,-1.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | local position differs |
| pad 10 | 1.22500,-0.50000 | 1.22500,0.50000 | 0.55000×0.35000; drill 0.00000×0.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | local position differs |
| pad 12 | 1.22500,0.50000 | 1.22500,-0.50000 | 0.55000×0.35000; drill 0.00000×0.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | local position differs |
| pad 13 | 1.22500,1.00000 | 1.22500,-1.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | local position differs |
| pad 14 | 0.50000,1.22500 | 0.50000,-1.22500 | 0.35000×0.55000; drill 0.00000×0.00000 | 0.35000×0.55000; drill 0.00000×0.00000 | local position differs |
| pad 15 | 0.00000,1.22500 | 0.00000,-1.22500 | 0.35000×0.55000; drill 0.00000×0.00000 | 0.35000×0.55000; drill 0.00000×0.00000 | local position differs |
| pad 16 | -0.50000,1.22500 | -0.50000,-1.22500 | 0.35000×0.55000; drill 0.00000×0.00000 | 0.35000×0.55000; drill 0.00000×0.00000 | local position differs |
| pad 2 | -1.22500,0.50000 | -1.22500,-0.50000 | 0.55000×0.35000; drill 0.00000×0.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | local position differs |
| pad 4 | -1.22500,-0.50000 | -1.22500,0.50000 | 0.55000×0.35000; drill 0.00000×0.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | local position differs |
| pad 5 | -1.22500,-1.00000 | -1.22500,1.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | local position differs |
| pad 6 | -0.50000,-1.22500 | -0.50000,1.22500 | 0.35000×0.55000; drill 0.00000×0.00000 | 0.35000×0.55000; drill 0.00000×0.00000 | local position differs |
| pad 7 | 0.00000,-1.22500 | 0.00000,1.22500 | 0.35000×0.55000; drill 0.00000×0.00000 | 0.35000×0.55000; drill 0.00000×0.00000 | local position differs |
| pad 8 | 0.50000,-1.22500 | 0.50000,1.22500 | 0.35000×0.55000; drill 0.00000×0.00000 | 0.35000×0.55000; drill 0.00000×0.00000 | local position differs |
| pad 9 | 1.22500,-1.00000 | 1.22500,1.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | 0.55000×0.35000; drill 0.00000×0.00000 | local position differs |

## J701 — CM5IO:M.2 M Key socket_2230_2242

- Actual board pad count: **71**; library pad count: **73**
- Changed individual pad-number groups: **2**
- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review

| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |
|---|---|---|---|---|---|
| pad M1 | — | 0.00000,28.25000 | — | 5.80000×5.80000; drill 3.70000×3.70000 | unmatched local pad definition (often non-electrical NPTH) |
| pad M2 | — | 0.00000,40.25000 | — | 5.80000×5.80000; drill 3.70000×3.70000 | unmatched local pad definition (often non-electrical NPTH) |

## Module301 — CM5IO:Raspberry-Pi-5-Compute-Module_GPIO

- Actual board pad count: **102**; library pad count: **104**
- Changed individual pad-number groups: **102**
- Difference category is determined only from pad geometry; actual part datasheet and assembly height still need review

**Caution:** 106 pad-level comparisons differ from the library for Module301; only the first 20 are displayed. This can indicate a different coordinate frame or an alternate footprint revision. Do not assume these are all independent copper errors. Compare connector orientation and physical manufacturer pin map before editing.

| Pad | Board x,y (mm) | Library x,y (mm) | Board size / drill (mm) | Library size / drill (mm) | Notes |
|---|---|---|---|---|---|
| PCB-only unnamed NPTH / mechanical | 0.00000,0.00000 | — | 2.70000×2.70000; drill 2.70000×2.70000 | — | unmatched local pad definition (often non-electrical NPTH) |
| PCB-only unnamed NPTH / mechanical | 0.00000,48.00000 | — | 2.70000×2.70000; drill 2.70000×2.70000 | — | unmatched local pad definition (often non-electrical NPTH) |
| Library unnamed NPTH / mechanical | — | 0.00000,-48.00000 | — | 2.70000×2.70000; drill 2.70000×2.70000 | unmatched local pad definition (often non-electrical NPTH) |
| Library unnamed NPTH / mechanical | — | 0.00000,0.00000 | — | 2.70000×2.70000; drill 2.70000×2.70000 | unmatched local pad definition (often non-electrical NPTH) |
| Library unnamed NPTH / mechanical | — | 33.00000,-48.00000 | — | 2.70000×2.70000; drill 2.70000×2.70000 | unmatched local pad definition (often non-electrical NPTH) |
| Library unnamed NPTH / mechanical | — | 33.00000,0.00000 | — | 2.70000×2.70000; drill 2.70000×2.70000 | unmatched local pad definition (often non-electrical NPTH) |
| pad 1 | -2.04000,31.30000 | -2.04000,-31.30000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 10 | 1.04000,29.70000 | 1.04000,-29.70000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 100 | 1.04000,11.70000 | 1.04000,-11.70000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 11 | -2.04000,29.30000 | -2.04000,-29.30000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 12 | 1.04000,29.30000 | 1.04000,-29.30000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 13 | -2.04000,28.90000 | -2.04000,-28.90000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 14 | 1.04000,28.90000 | 1.04000,-28.90000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 15 | -2.04000,28.50000 | -2.04000,-28.50000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 16 | 1.04000,28.50000 | 1.04000,-28.50000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 17 | -2.04000,28.10000 | -2.04000,-28.10000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 18 | 1.04000,28.10000 | 1.04000,-28.10000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 19 | -2.04000,27.70000 | -2.04000,-27.70000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 2 | 1.04000,31.30000 | 1.04000,-31.30000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |
| pad 20 | 1.04000,27.70000 | 1.04000,-27.70000 | 0.20000×0.70000; drill 0.00000×0.00000 | 0.20000×0.70000; drill 0.00000×0.00000 | local position differs |

## Safe decision rule

- A change solely to unnumbered NPTH may be fixable by restoring local-library consistency **after** the fabrication drill drawing is confirmed.
- Signal pad offsets and dimensions must match the actually purchased device's recommended land pattern, not the newest KiCad default by assumption.
- No KiCad DRC warning should be ignored solely because the parts appear correctly connected; physical component pads can differ while the netlist remains unchanged.
