# Linux SBC A1 — native KiCad working schematic

The root schematic now contains two actual electrical subcircuits:

1. USB-C PD sink input: HUSB238_003DD, 15V/3A request, AO4407A high-side P-MOSFET switch, VSET/ISET configuration and VIN bypass.
2. 15V-to-5V_SYS main buck: LM76005RNPR 5V/5A design target, 400kHz default, input/output filters, bootstrap, feedback, BIAS/VCC decoupling, PGOOD pull-up and 10V EN UVLO divider.

## Project files

- `A1.kicad_pro` — KiCad project
- `A1.kicad_sch` — current native root schematic with PD input and main 5V buck circuits
- `A1_CUSTOM.kicad_sym` — custom symbol library (USB-C connector, HUSB238, passives, AO4407A, LM76005, inductor)
- `sym-lib-table` — local symbol library registration
- `A1_PD_INPUT_BOM.csv` — PD input BOM
- `A1_PD_INPUT_NETS.csv` — PD input net membership
- `A1_POWER_BOM.csv` — main buck BOM
- `A1_POWER_NETS.csv` — main buck net membership

## RK3568 SoC library\n\n- `A1_SOC.kicad_sym` — 636-ball multi-unit RK3568 symbol.\n- `A1_SOC.pretty/BGA-636_L19.0-W19.0-P0.65-BL.kicad_mod` — candidate 636-pad footprint.\n- `A1_SOC_BALLMAP.csv` — complete ball map, full mux names and pad coordinates.\n- `docs/RK3568_SYMBOL_AUDIT.md` — validation scope and footprint caveat.\n- The symbol displays primary mux functions; full alternatives remain in the CSV. All non-power signal pins are passive pending mode-specific pin-direction review.\n- The 0.35 mm pad diameter is provisional; the footprint is not fabrication-approved until land-pattern and assembly-house confirmation.\n\n## Electrical decisions

### USB-C PD input
- HUSB238_003DD, DFN-10L.
- RVSET=14k requests 15V.
- RISET=22.6k limits requested current to 3.0A.
- Q1 AO4407A P-channel switch: pins 1–3 source, pin 4 gate, pins 5–8 drain.
- R3=5.1k GATE series; R4=49.9k gate pull-up to VBUS.
- C1=1uF VIN bypass.

### Main buck
- U2 LM76005RNPR, WQFN RNP 30-pin, 6mm × 4mm.
- 15V input to 5V_SYS, 5A maximum design target.
- 400kHz default frequency (RT left open).
- L1=6.8uH, Isat >8A.
- COUT=3×47uF, 10V X7R.
- RFBT=100k, RFBB=24.9k, CFF=47pF.
- CBOOT=470nF; CVCC=2.2uF; CBIAS=1uF; BIAS tied to 5V_SYS.
- EN divider 732k/100k gives approximately 10V rising threshold so the converter does not start on the USB-C default 5V before PD negotiation reaches the 15V contract.
- PGOOD pulled up to 5V_SYS through 10k.

## Verification state

- S-expression syntax and balanced parentheses checked.
- All 30 LM76005 pins and all other placed symbol pin endpoints have a wire, net label, or explicit no-connect marker in the generated source.
- Native KiCad Eeschema load, ERC, netlist export and visual review have **not** been run because KiCad CLI is not installed in the authoring environment.
- LM76005 footprint is intentionally left unassigned until the exact TI RNP WQFN land pattern is obtained and checked.
- The project is not a complete SBC schematic yet. RK809-5, RK3568 SoC, LPDDR4X, eMMC, Ethernet, USB, HDMI, Wi-Fi/BT and GPIO circuits remain to be added.
- Do not fabricate from the current revision.

## Primary datasheets

- Hynetek HUSB238: https://www.hynetek.com/uploadfiles/site/219/news/aabbbbdb-48c9-4a44-a6dc-2c15f53282e6.pdf
- TI LM76005: https://www.ti.com/lit/ds/symlink/lm76005.pdf