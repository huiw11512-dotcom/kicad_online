# A1 hierarchical schematic plan — Rev 0.2

The first KiCad release is a project shell and page plan. It is not yet a complete schematic.

| Sheet | Block | Main review gate |
|---|---|---|
| 01 | USB-C PD input and protection | PD contract, current limit, connector CC and protection |
| 02 | Main 5V/3V3 rails | Load budget, regulator SOA, inrush, thermal |
| 03 | RK809-5 PMIC and SoC rails | Exact RK809-5 variant, rail map, OTP and power sequence |
| 04 | RK3568 SoC, clocks, reset and boot straps | Official ball map, power domains, decoupling and boot mode |
| 05 | LPDDR4X | Exact memory/template/BIN match; point-to-point topology |
| 06 | eMMC and MicroSD | Exact eMMC package/ball map, voltage and HS mode |
| 07 | GMAC0 Ethernet PHY and RJ45 | RGMII pinmux, delay strategy, PHY straps and magnetics |
| 08 | USB3/USB2 | Multi-PHY resource map, host/DRD role, VBUS protection |
| 09 | HDMI | TMDS pairs, DDC, HPD, CEC, PHY rails and ESD |
| 10 | Wi-Fi/Bluetooth | Exact module pinout, SDIO/UART, power, antenna keepout |
| 11 | GPIO, debug and controls | 40-pin pinmux, bank voltages, UART, reset/recovery |

## Schematic conventions

- Use the manufacturer signal names and ball numbers from the exact RK3568 datasheet revision.
- Every power pin and ground pin must be represented; do not use guessed generic power symbols.
- Every unused pin must be intentionally marked NC or documented as reserved.
- Every IO bank must have one verified voltage assignment; do not mix 1.8V and 3.3V signals within a bank.
- All high-speed ports must have an explicit reference plane and routing constraint before PCB placement.
- Use hierarchical labels for cross-sheet connections and global labels only for genuine global nets.
- Keep power sequencing and reset dependencies explicit.
- Record every provisional part as DNP/ALT or candidate in the BOM; do not silently substitute parts.

## KiCad shell

- Project: `hardware/kicad/A1.kicad_pro`
- Root schematic: `hardware/kicad/A1.kicad_sch`
- Library files are added only after the SoC symbol and footprint pass native KiCad parsing and ball-map validation.
