# MiniHost Rev.A — latest 85-item KiCad DRC triage (2026-11-14)

**Verified actual KiCad run:** [USB D+ single-via removal no-regression check](https://github.com/huiw11512-dotcom/kicad_online/actions/runs/43600307395).

Native KiCad 10.0.8 on GitHub Actions now reports **85 total PCB DRC violations = 2 hard errors + 83 warnings**, **ERC 0 hard errors**, **0 PCB unconnected pads**, **0 schematic/footprint parity issues**. The initial standardized cloud report was **230**, and controlled PCB edits have reduced it to 85. No mask-rule, hard DRC or global rule disabling was used. The board remains **NOT manufacturing released**.

| Current category (actual DRC code) | Count | Technical disposition |
| --- | ---: | --- |
| `copper_edge_clearance` | **2 hard** | Kycon J1 shield pads 15 and 16 to routed board-edge cutout, actual 0.2164 mm and 0.1914 mm against 0.372 mm design rule; keep as explicit fab blockers until board aperture and mechanical overhang are validated |
| `lib_footprint_mismatch` | 50 warnings | Library metadata/silk/geometry differs from installed stock KiCad 10. **Do not auto-update all libraries:** must compare pad coordinates, aperture, pin numbering and drills against BOM and datasheets first |
| `silk_edge_clearance` | 15 warnings | Edge-cut silk likely trimmed by fab. Move or shorten only nonessential silk graphics with manufacturer fit and board-edge check |
| `silk_overlap` | 8 warnings | Remaining custom label polygons near M.2 and small parts; do not delete readable critical I/O labels solely to reduce count |
| `silk_over_copper` | 7 warnings | Text/graphics intersect solder-mask openings; inspect fab layers and reposition or clip only genuine offending graphics |
| `via_dangling` | 2 warnings | PWR_BUT at (130.9594,65.5595) and +BATT at (81.45,72.50) mm: removing vias alone creates two dangling trace ends, so preserve pending segment-level route correction |
| `isolated_copper` | 1 warning | GND isolated pour near (74.99,20.22) mm; inspect zone island and high-speed return continuity before removing |
| **Total** | **85** | **2 hard, 83 warnings** |

## Measured reductions (independently checked and committed)

| Native project edit | Before → After total | No change to |
| --- | ---: | --- |
| Remove duplicated HSS CM5 outer silkscreen outlines | **230 → 198** | pads, copper, track/vias, zone nets |
| Hide tiny KiBuzzard generated `Reference` placeholders, retain printed label polygons | **198 → 140** | pads, tracks, visual labels |
| M.2 J701 SMT pads: mask expansion 0.102 mm to 0.020 mm, nominal mask web 0.16 mm | **140 → 86** | 0.5 mm pitch, 0.3 mm copper lands, net mapping, local library pad geometry |
| Remove one USB_C.D_P unused via attached to F.Cu traces | **86 → 85** | complete netlist, all pads, all other tracks, zone topology |

The J701 change is based on JLCPCB **six-layer, 1oz outer copper, green LDI soldermask** envelope and its published 0.10 mm mask-web minimum. This **does not certify** the 0.16 mm nominal ink wall against production registration, alternative copper weights, mask color or supplier without DFM signoff. Source: https://jlcpcb.com/capabilities/Capabilities .

The remaining two RJ45 hard errors are **not resolved**, and the edge clearance cannot be made safe merely by suppressing DRC or shrinking the manufacturer's solder shield lands. The official A4 connector drawing allows customer-selected PCB overhang, but the board cutout and housing/interference constraints must be resolved together: https://www.kycon.com/Pub_Eng_Draw/GLPLX-SMT-188S7-QQ-YG.pdf .

## Important negative trial (not merged)

Removing all three dangling vias caused `via_dangling` to go **3 → 0** but introduced `track_dangling` **0 → 2**. The automated DRC guard correctly rejected it. Only the independently verified USB D+ via removal was merged; two vias remain for subsequent topology review.

## Release prerequisites

1. RJ45 copper-edge clearance must pass with a confirmed physical/PCB stack and connector cutout.
2. M.2 0.16mm mask web and copper pads must pass chosen fab DFM for actual color and outer copper weight.
3. Inspect 50 footprint-library mismatches before any footprint replacement; distinguish graphical version changes from pad/drill differences.
4. Resolve two flagged signal tail vias and isolated copper without breaking return paths.
5. Clean remaining 30 silkscreen-related warnings using position-aware edits; no global DRC disabling.
6. Recalculate PCIe/HDMI/USB controlled differential impedance using actual six-layer fab dielectric constants and copper weights; formal board power and boot/thermal test required.

---

## Archived earlier 230-item warning classification

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
