# A1 USB2 HOST2 / HOST3 interface — Rev1

**Status:** schematic page added to the working branch; source-level pin and connectivity checks pending native KiCad ERC. Not a fabrication release.

## 1. RK3568 pin allocation

| Function | RK3568 ball | A1 net | Use |
|---|---:|---|---|
| USB2 HOST2 DM | R1 | USB2_HOST2_DM | Port J7 D− |
| USB2 HOST2 DP | R2 | USB2_HOST2_DP | Port J7 D+ |
| USB2 HOST3 DM | T1 | USB2_HOST3_DM | Port J8 D− |
| USB2 HOST3 DP | T2 | USB2_HOST3_DP | Port J8 D+ |
| HOST2 VBUS enable | AF8 / GPIO4_C2 | USB2_HOST2_PWR_EN | U13 EN, active high |
| HOST3 VBUS enable | AB9 / GPIO4_D2 | USB2_HOST3_PWR_EN | U14 EN, active high |

The two enable GPIOs are in the VCCIO7 domain. The current SoC power map ties VCCIO7 to VCC_3V3, so both control signals are 3.3V logic. They are reserved for the USB port regulators and must not be assigned to other pinmux functions.

## 2. Per-port data circuit

Each port follows the RK3568 Hardware Design Guide Rev1.2 §2.3.4:

1. SoC DP and DM each pass through a 2.2Ω ±1% 0402 resistor.
2. Each connector-side DP/DM net has one TECH PUBLIC ESD5341N, nominal capacitance 0.35pF, to GND. This is below the guide's 3pF maximum.
3. Route DP/DM as a 90Ω differential pair, target ±10%, length matched and continuous reference plane maintained.
4. Place the ESD device adjacent to the Type-A connector. Place the 2.2Ω resistors near the SoC PHY side.
5. No common-mode choke is fitted in Rev1. If EMC testing requires one, reserve a CMC footprint while retaining the 2.2Ω series resistors.

## 3. Per-port VBUS power switch

- U13/U14: TI TPS2553DBVR, LCSC C55266, SOT-23-6.
- IN: 5V_SYS.
- OUT: USB2_HOST2_VBUS / USB2_HOST3_VBUS.
- EN: USB2_HOST2_PWR_EN / USB2_HOST3_PWR_EN, active high.
- R86/R87: 100kΩ pull-down on EN. Ports remain disabled while GPIOs are high-impedance during reset.
- ILIM: R84/R85 = 47kΩ ±1% to GND.
- FAULT: left NC in Rev1.
- Input bypass: 1uF X7R at each switch.
- Output bulk: Panasonic 16SVPC100M, 100uF/16V polymer, plus 100nF X7R per port.

The 47kΩ ILIM choice is intended to keep the minimum current-limit threshold above 500mA. Using the TPS2553 datasheet min/typ/max equations gives approximately 0.505A / 0.557A / 0.616A. This is a protection threshold, not a precision 500mA regulator. Reserve up to 0.62A per port in the 5V budget and confirm the actual TPS2553 ordering suffix and datasheet limits before release.

The USB3 HOST1 port is already designed for approximately 0.9A nominal current limit. The combined HOST1 + HOST2 + HOST3 VBUS design allowance is therefore about 2.14A; use **2.2A** as the board-level 5V USB-port budget until the exact switch tolerance and load profile are closed.

## 4. Connector allocation

J7 and J8 use the same HC-USB3.0-L168-WP / LCSC C7501850 Type-A receptacle already used by the USB3 HOST1 port. On these two ports only USB2 VBUS, D−, D+, GND and shield are connected. SuperSpeed contacts 5, 6, 8 and 9 are explicitly NC; these are USB2-only ports despite the 9-contact receptacle.

## 5. Linux / device-tree requirements

- Configure GPIO4_C2 (AF8) and GPIO4_D2 (AB9) as GPIO outputs.
- Define one fixed regulator for each VBUS switch, active-high enable, with 5V output.
- Associate each USB2 host controller's VBUS supply with its regulator node.
- Do not set regulator-always-on in the first spin. Enable VBUS only when the corresponding host port is enabled by the OS.
- Verify the correct controller/regulator phandle mapping against the final RK3568 kernel DTS and bootloader tree.

## 6. Files

- Schematic: `hardware/kicad/A1_USB2_HOST23.kicad_sch`
- BOM: `hardware/kicad/A1_USB2_HOST23_BOM.csv`
- SoC page: `hardware/kicad/A1_RK3568_SOC.kicad_sch`
- Ball/net audit: `hardware/kicad/A1_RK3568_PINNETS.csv`

## 7. Release checks still required

1. Open the project in the target KiCad version and run ERC; confirm all direct global labels attach to the intended symbol pin endpoints.
2. Export the netlist and verify R1/R2/T1/T2, both EN GPIOs, both ILIM resistors, VBUS capacitors, ESD and connector pins.
3. Check the Panasonic polymer capacitor land pattern/polarity and connector mechanical footprint against the manufacturer drawings.
4. Verify TPS2553 current-limit resistor selection against the exact device datasheet revision and perform hot-plug/inrush tests.
5. Confirm the kernel DTS enables each regulator before USB enumeration.
6. PCB route the two DP/DM pairs at 90Ω differential, matched length, with ESD adjacent to the connector and no stubs.

## 8. References

- Rockchip RK3568 Hardware Design Guide Rev1.2, §§2.3.4, Figures 2-81 to 2-88 and Table 2-18: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- TI TPS2553 datasheet: https://www.ti.com/lit/ds/symlink/tps2553.pdf
- XUNPU HC-USB3.0-L168-WP / LCSC C7501850: https://www.lcsc.com/product-detail/C7501850.html
- TECH PUBLIC ESD5341N / LCSC C3021106: https://www.lcsc.com/product-detail/C3021106.html
- Panasonic 16SVPC100M / LCSC C136275: https://www.lcsc.com/product-detail/C136275.html
- YAGEO RC0402FR-072R2L / LCSC C327251: https://www.lcsc.com/product-detail/C327251.html
