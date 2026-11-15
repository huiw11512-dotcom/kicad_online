# Linux SBC A1 — KiCad working project

This is the first actual electrical subcircuit in the A1 native KiCad project:
- USB-C PD sink using Hynetek HUSB238_003DD
- 15V / 3A request configuration (RVSET=14k, RISET=22.6k)
- P-channel high-side input switch AO4407A
- HUSB238 VIN bypass capacitor
- CC1/CC2 and D+/D- wiring

Files:
- `A1.kicad_pro` — KiCad project
- `A1.kicad_sch` — current root schematic containing the USB-C PD input page
- `A1_CUSTOM.kicad_sym` — custom symbols
- `sym-lib-table` — local symbol library table
- `fp-lib-table` — standard footprint library references
- `A1_PD_INPUT_BOM.csv` — subcircuit BOM
- `A1_PD_INPUT_NETS.csv` — explicit net membership

## Engineering status

This is **not yet the complete SBC schematic**. The PD input subcircuit is drafted from Hynetek HUSB238 datasheet Figures 4 and its VSET/ISET tables. No KiCad CLI is installed in the authoring environment, so the file has not yet passed native Eeschema load, ERC, or netlist export. Do not fabricate from this page yet.

Before release:
1. Verify USB-C receptacle exact manufacturer pad numbering against selected footprint.
2. Verify AO4407A SO-8 pin numbering (pins 1–3 source, 4 gate, 5–8 drain) against the exact manufacturer package drawing.
3. Confirm HUSB238_003DD procurement and OTP option.
4. Add connector-side ESD and input protection after exact TVS/fuse selection.
5. Add the 15V-to-5V converter and its power-good/undervoltage sequencing.