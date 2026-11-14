# KiCad Web Pilot — 5 V filter board

A small native KiCad project created to test **ChatGPT → GitHub → ZiroEDA** engineering workflows.

Open in the browser: https://designer.ziroeda.com/gh/huiw11512-dotcom/kicad_online

## Project files

- `KiCad_Web_Pilot.kicad_pro` — KiCad project settings
- `KiCad_Web_Pilot.kicad_sch` — editable schematic, five symbols
- `KiCad_Web_Pilot.kicad_pcb` — routed 42 × 26 mm, two-layer PCB
- `Pilot.kicad_sym` and `sym-lib-table` — project-local symbol library
- `.github/workflows/kicad-check.yml` — example CLI checks on GitHub Actions

## Circuit

J1: pin 1 VIN, pin 2 GND.
FB1: 600 Ω @ 100 MHz nominal ferrite bead (placeholder specification).
C1: 100 nF, C2: 10 µF, both from the filtered supply to GND.
J2: pin 1 5V_FILT, pin 2 GND.

Footprints: J1/J2 2.54 mm through-hole headers; FB1 0603; C1/C2 0805. Board nominal thickness 1.6 mm. Includes top/bottom traces, vias and a B.Cu ground zone.

**Only a low-voltage test project, not a production-ready EMC design. Do not connect it to mains.**

## How to test

1. Visit [Open KiCad project in ZiroEDA](https://designer.ziroeda.com/gh/huiw11512-dotcom/kicad_online).
2. If automatic opening fails, visit https://designer.ziroeda.com and use File → Open from GitHub, then enter `huiw11512-dotcom/kicad_online`.
3. Inspect both the schematic and PCB. Expected references: J1, FB1, C1, C2 and J2; nets: VIN, 5V_FILT and GND.
4. Refill ground zone if the editor requests it, and try ERC / DRC.
5. Report any import, library or connectivity errors for subsequent iteration.

## Verification status

The files were generated and structurally checked, but **have not yet been successfully opened by a native KiCad installation or by ZiroEDA in this conversation**. A passing GitHub Actions check, if it occurs, still does not replace inspection of the rendered schematic/PCB, actual copper connectivity and fabrication clearance rules. The local symbol library uses the name `Pilot`.

This repository is a portability and toolchain pilot; manufacturing readiness is not claimed.
