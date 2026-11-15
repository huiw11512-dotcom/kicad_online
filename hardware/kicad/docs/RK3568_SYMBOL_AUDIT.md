# RK3568 symbol and footprint audit — Rev 0.1

## Source and cross-check

- Symbol ball names and numbers were taken from a 636-pin RK3568 KiCad symbol source and checked against Rockchip RK3568 Datasheet Rev 2.1 Table 2-1 spot checks.
- Package: FCBGA636L, 19.00 mm nominal body, 0.65 mm pitch, nominal ball diameter 0.36 mm.
- Footprint source contains 636 unique pads; pad numbers match the symbol ball numbers one-to-one.
- A1 ball is mapped to pad A1 at local coordinate (-8.770, +8.770) mm in the source footprint orientation.
- The symbol is split into functional units. Pin names displayed in the symbol use the primary mux function (LPDDR4 alternative preferred when present); complete mux strings are retained in A1_SOC_BALLMAP.csv.
- Power and ground balls are typed as power_in. All other signal balls are passive because the full mux direction is mode-dependent; this avoids false ERC direction conflicts but means ERC cannot validate signal direction.

## Library registration\n\nThe project-local symbol library is registered as `A1_SOC` in `sym-lib-table`; the footprint library is registered as `A1_SOC` in `fp-lib-table`.\n\n## Footprint caveat

- Candidate footprint uses 636 circular 0.350 mm pads on a 0.65 mm grid and the 28 × 28 ball map with 636 populated positions.
- Rockchip Datasheet Rev 2.1 specifies package body and ball geometry, but the exact PCB land pattern / solder-mask / paste geometry still requires confirmation against the Rockchip assembly recommendation or the selected assembly house.
- Do not treat this footprint as fabrication-approved until that land-pattern check and a BGA escape/assembly review are complete.

## Files

- A1_SOC.kicad_sym — grouped 636-ball symbol.
- A1_SOC.pretty/BGA-636_L19.0-W19.0-P0.65-BL.kicad_mod — candidate footprint.
- A1_SOC_BALLMAP.csv — complete ball-to-function map and pad coordinates.

## References

- Rockchip RK3568 Datasheet Rev 2.1, Table 2-1 and FCBGA636L package drawing: https://www.boardcon.com/download/Rockchip_RK3568_Datasheet_V2.1-20240621.pdf
