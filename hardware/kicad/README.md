# Linux MiniHost A1 — native KiCad working project

## Project hierarchy

- `A1.kicad_pro` — KiCad project.
- `A1.kicad_sch` — root sheet (page 1): USB-C PD input and 15V-to-5V_SYS main buck; links the RK809-5 page.
- `A1_RK809_PMIC.kicad_sch` — PMIC and power-sequencing page (page 2).\n- `A1_DDR_POWER.kicad_sch` — separate LPDDR4X 0.6V and 1.8V power rails (page 3).
- `A1_CUSTOM.kicad_sym` — HUSB238, USB-C, AO4407A, LM76005, R/C/L, pushbutton and crystal symbols.
- `A1_PMIC.kicad_sym` — RK809-5 69-pin symbol.
- `A1_SOC.kicad_sym` — RK3568 636-ball grouped symbol.
- `sym-lib-table`, `fp-lib-table` — project-local library registration.

## Current electrical pages

### Page 1 — USB-C PD and main power
- HUSB238_003DD, 15V/3A request, input path switch and PD configuration.
- LM76005RNPR, 15V to 5V_SYS, 5A design target.
- This page is an initial design implementation; native KiCad ERC and bench validation are still pending.

### Page 2 — RK809-5 PMIC
- U3 RK809-5 QFN68, all 68 pins plus exposed pad represented.
- All PMIC pins have a named net or explicit no-connect marker.
- Five buck stages represented; BUCK4 hardware populated but OTP-default OFF are represented with 0.47uH inductors and nominal 2×47uF output capacitors.
- BUCK3 feedback divider is explicitly TBD until the LPDDR4X rail is finalized.
- VDC divider, PWRON switch, SLEEP pulldown, I2C/open-drain pull-ups, RESETB 100nF, 32.768kHz crystal, charge-pump bypass and all PMIC decoupling are represented.
- RK809-5 output rail map now follows the Rockchip EVB reference (BUCK1=VDD_LOGIC, BUCK2=VDD_GPU, BUCK3=VCC_DDR, BUCK4=VDD_NPU, BUCK5=VCC_1V8; LDO/SWOUT rails assigned). LPDDR4X still needs separate 0.6V and 1.8V DDR rails. Buck inductors use TDK SPM5030T family; local land pattern follows TDK's recommended 1.5×2.2mm pads and 2.7mm gap.

### LPDDR4X DDR power page\n- U4 SY8089AAAC generates VCC0V6_DDR from VCC_3V3.\n- U5 AP2112K-1.8TRG1 generates VCC1V8_DDR from VCC3V3_PMU.\n- VCC_DDR_1V1 comes from RK809 BUCK3 with 37.4k/100k divider.\n- Final DRAM part/template and rail current/ramp verification remain open.\n\n## RK3568 library
- `A1_SOC.kicad_sym` — 636-ball grouped symbol.
- `A1_SOC.pretty/BGA-636_L19.0-W19.0-P0.65-BL.kicad_mod` — candidate 636-pad footprint.
- `A1_SOC_BALLMAP.csv` — full ball map and mux strings.
- SoC footprint remains a candidate until land pattern and assembly review are complete.

## PMIC files
- `A1_RK809_PMIC_PINMAP.csv` — pin-by-pin net/status map.
- `A1_RK809_PMIC_BOM.csv` — PMIC page BOM.
- `A1_PMIC.pretty/RK809_QFN-68-1EP_7x7mm_P0.35mm_EP5.49x5.49mm.kicad_mod` — candidate footprint.
- `docs/RK809-5_PMIC_DESIGN_REV1.md` — PMIC design notes and unresolved gates.

## Verification state

- Parent/child schematic S-expressions and symbol/footprint pad counts have been structurally checked.
- RK809-5 symbol has 69 unique pin numbers; PMIC footprint has 69 numbered pads (68 perimeter + EP).
- All 69 PMIC pins are assigned to a net or explicit NC.
- Native KiCad load, ERC, netlist export and visual review have **not** yet been executed; KiCad CLI is not installed in the authoring environment.
- No PCB placement/routing, DRC or hardware bring-up has been completed.
- Do not fabricate from this revision.
