# KiCad 10 Rev.A DRC warning triage — 2026-11-14

**Original 234-item reference run:** https://github.com/huiw11512-dotcom/kicad_online/actions/runs/43596487428

**Latest confirmed actual report:** https://github.com/huiw11512-dotcom/kicad_online/actions/runs/43596928117 — total **230** DRC violations after CM5 duplicate nonplated drill cleanup; **0 ERC hard errors / 2 PCB hard errors / 0 schematic footprint parity / 0 unconnected**. The 2.7 mm M2.5-compatible physical holes remain in Module301, two duplicate 3.0 mm holes in Module302 were deleted. Compare `CM5_ALIGNMENT_HOLE_AUDIT.md`.

The GitHub Actions KiCad 10.0.8 runner now initializes the official **KiCad 10 standard footprint/symbol library tables** (previously uninitialized). This removed 65 `lib_footprint_issues` false missing-library warnings. **It did not imply the 234 remaining items are safe.** The report retains *2 hard board-edge copper-clearance errors*. The 234 DRC violations are independently of the ERC count; ERC 0 errors still has warnings.

## Historical 234-item group counts before CM5 NPTH de-duplication

| DRC code | Count | Disposition |
|---|---:|---|
| `solder_mask_bridge` | 54 | **FAB REVIEW**: verify mask-web technology and intentionally mask-open closely spaced pads, especially fine-pitch connectors; do not automatically increase mask clearance |
| `lib_footprint_mismatch` | 51 | **LIBRARY REVIEW**: KiCad-9 embedded footprints vs current KiCad-10 stock revisions plus custom footprints; check pad drill/size before any library update |
| `silk_overlap` | 33 | Silkscreen production cleanup required |
| `text_thickness` | 27 | Silkscreen/text manufacturability |
| `text_height` | 27 | Silkscreen/text manufacturability |
| `silk_over_copper` | 17 | Silkscreen-to-pad masking and readability |
| `silk_edge_clearance` | 17 | Board-edge silkscreen cleanup |
| `via_dangling` | 3 | **ELECTRICAL REVIEW**: /USB_C.D_P at (85.848,48.5204), /CM5/PWR_BUT at (130.9594,65.5595), +BATT at (81.45,72.5) — investigate whether single-layer vias are unnecessary or need connection |
| `copper_edge_clearance` | 2 | **HARD ERROR / FAB BLOCK**: RJ45 J1 pads 15,16 vs PCB notch edges; 0.2164 mm and 0.1914 mm vs 0.3720 mm design rule |
| `holes_co_located` | 2 | **DRILL REVIEW**: duplicated unnumbered NPTHs on Module301/Module302 (CM5 same physical hole). Must compare exact drill and pad geometry before removing duplicate |
| `isolated_copper` | 1 | **RETURN PATH REVIEW**: GND isolated copper island around (74.990,20.220), copper zone fill should be examined |

**Historical counts sum to 234.** The current 230-item report differs only as follows:
- `holes_co_located`: **2→0**.
- `lib_footprint_mismatch`: **51→50** (board-embedded HSS footprint and project library now aligned).
- `silk_over_copper`: **17→16** (the duplicate mechanical pad graphics were removed).
- All other categories remain unchanged, including the **two hard copper-edge errors**.

All counts were extracted from actual GitHub Actions `drc.rpt` artifacts, not inferred from the 3D preview.

## Priorities for engineering release

1. **Preserve real mechanical and high-speed geometry:** J1 manufacturer [A4 layout](https://www.kycon.com/Pub_Eng_Draw/GLPLX-SMT-188S7-QQ-YG.pdf) sets part outline and the PCB overhang is a customer design decision. Do not “fix” edge copper gaps by arbitrarily shrinking shield pads or weakening global DRC.
2. **Validate real manufacturing risk:** 54 solder-mask bridges and critical high-speed connectors against selected fab's minimum mask web, trace-to-pad geometry and ENIG finish; verify original footprint placement accuracy, not just KiCad-10 parity.
3. **Investigate 3 disconnected/dangling via warnings** and 1 isolated ground island. If truly redundant, remove only after connectivity/DRC proof and high-speed return path inspection.
4. **Resolve mechanical duplicate holes** through model inspection, not by removing drilling definitions from both logical CM5 half-footprints.
5. **Only after electrical/DFM:** bulk silkscreen cleanup and stock-library migration with an explicit per-footprint pad and drill match.

## Already verified

- ERC hard errors 0; PCB schematic footprint parity 0; board unconnected 0.
- USB power Rp/ILIM resistors revised and native net/pad/track checks passed.
- KiCad RJ45 Courtyard replaced by manufacturer-body/pad-aware outline: hard errors 4→2; courtyard overlaps 2→0, no copper and pad changes.
- 8 recovered custom footprints load in current KiCad.

**No manufacturing Gerbers are authorized by this document.** Real impedance and assembly checks remain open.
