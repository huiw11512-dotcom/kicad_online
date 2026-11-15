# Linux SBC A1 — KiCad workspace

This directory contains the native KiCad project shell for the independently designed RK3568 SBC.

## Open the project

Open `A1.kicad_pro` in KiCad. The root schematic is currently an intentionally empty project sheet. It is not an electrical design and contains no released components or nets yet.

## Planned hierarchy

See `../../docs/SCHEMATIC_PLAN.md` for the 11-sheet design plan and review gates.

## Library release policy

The RK3568 symbol and FCBGA636L footprint are not released until all 636 ball identifiers, ball coordinates, A1 orientation, package dimensions and KiCad parser compatibility have been independently checked against the exact manufacturer package drawing. A generated footprint with an assumed pad size is not sufficient for fabrication.

## Current state

- Native project shell: created.
- Root schematic: empty placeholder.
- SoC symbol: not released.
- BGA footprint: not released.
- Full schematic: not started.
- PCB: not started.
- ERC/DRC: not run.

Do not use this shell as a fabrication release.
