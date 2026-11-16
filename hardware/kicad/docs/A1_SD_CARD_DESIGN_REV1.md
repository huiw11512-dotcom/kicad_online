# microSD / SDMMC0 interface — A1 Rev1

Status: editable schematic and local symbol/footprint libraries added. Native KiCad ERC/DRC and physical assembly validation remain open.

## Interface topology

- RK3568 controller: SDMMC0, 4-bit bus.
- Connector: J4 TFP09-2-12B push-push microSD socket with card detect.
- Data/CMD/CLK series resistors: R50–R55 = 22Ω, 0402, 1%.
- Card-detect series resistor: R56 = 100Ω, 0402, 1%.
- Card-detect pull-up: R58 = 10kΩ, 0402, 1%, to VCCIO_SD.
- ESD: D20–D26, TECH PUBLIC ESD5341N, 0.35pF typical, DFN1006-2, one per DAT[3:0], CMD, CLK and DET.
- Card VDD: 3.3V from RK809-5 SWOUT2 output VCC3V3_SD (power-sequence slot 4). Rockchip RK3568 EVB User Guide Rev1.2 specifies Switch2 for VCC3V3_SD / MicroSD, 2.1A max and 100mΩ RDS(on).
- R57 is a 0Ω optional bypass from VCC3V3_SYS to VCC3V3_SD and is DNP for Rev1. Do not populate it: doing so bypasses the PMIC SWOUT2 switch.
- Decoupling: C80=10µF/10V/X5R/0603 and C81=100nF/10V/X7R/0402.
- SDMMC0_PWREN is intentionally NC; card VDD is supplied by SWOUT2 after PMIC power-sequence slot 4. The SD card is not independently power-gated by the SoC PWREN pin.

## RK3568 ball assignment

| RK3568 ball | Signal | J4 pin |
|---|---|---:|
| H26 | SDMMC0_D2 | 1 DAT2 |
| J23 | SDMMC0_D3 | 2 DAT3 |
| H27 | SDMMC0_CMD | 3 CMD |
| H28 | SDMMC0_CLK | 5 CLK |
| J25 | SDMMC0_D0 | 7 DAT0 |
| J24 | SDMMC0_D1 | 8 DAT1 |
| Y22 | SDMMC0_DET | 9 card detect |
| AF25 | SDMMC0_PWREN | NC |

J4 pin 4 is VDD (VCC3V3_SD); pin 6 is VSS; pin 10 is the shell ground pad number used by four physical shell pads.

## Voltage domains

- Card VDD is sourced from RK809-5 SWOUT2 on VCC3V3_SD; R57 bypass to VCC3V3_SYS remains DNP.
- RK3568 VCCIO3 is supplied by VCCIO_SD from RK809 LDO5.
- VCCIO_SD must be configured to 3.3V for initial SD negotiation and switched to 1.8V for UHS-I modes. The device tree should provide VCC3V3_SD as `vmmc-supply` and VCCIO_SD as `vqmmc-supply`; enable UHS modes only after the PMIC LDO5 transition and signal integrity are validated.
- SDMMC0 DAT[3:0] and CMD use the SoC internal pull-ups; no additional external pull-ups are fitted.
- Card-detect switch is normally open and closes to GND when a card is inserted. R58 pulls the SoC-side detect node up to VCCIO_SD.

## Footprint notes

- Local footprint: `A1_IO.pretty/TFP09-2-12B_microSD.kicad_mod`.
- J4 has pads 1–9 for the eight SD signals plus card detect; pad 10 is repeated on four shell-ground pads. Two NPTH locating holes are included.
- Pin 1 is placed according to the published TFP09-2-12B board-land-pattern view. Confirm the supplier drawing orientation before fabrication.
- Local ESD footprint: `A1_IO.pretty/ESD5341N_DFN1006-2L.kicad_mod`. Confirm the exact land pattern against the selected ESD5341N manufacturer's package drawing.

## Sourcing

- J4: TFP09-2-12B, LCSC C2911421; currently listed out of stock. JLC assembly extended part C2887880 is listed as the alternative route; verify orderability before BOM freeze.
- D20–D26: TECH PUBLIC ESD5341N, LCSC C3021106.
- R50–R55: Yageo RC0402FR-0722RL, C106260.
- R56: Yageo RC0402FR-07100RL, C106232.
- R57: UNI-ROYAL 0402WGF0000TCE, C17168, DNP in Rev1 (optional bypass only).
- R58: UNI-ROYAL 0402WGF1002TCE, C25744.
- C80: CCTC TCC0603X5R106K100CT, C380314.
- C81: C387941 (100nF, 10V, X7R, 0402); confirm current stock and exact MPN before purchase.

## Validation still required

1. Verify J4 pin-1 orientation and the 13 copper-pad pattern plus two NPTH locating holes against the supplier's latest drawing.
2. Confirm current orderability of the TFP09-2-12B and all seven ESD5341N devices.
3. Check VCCIO_SD LDO5 output range, boot default, PMIC register configuration and 3.3V↔1.8V transition timing.
4. Run native KiCad ERC/netlist/DRC and inspect the page in the KiCad GUI.
5. Validate card insertion/removal, detect polarity, 4-bit enumeration, UHS-I voltage switching and sustained read/write.


## Reference

- Rockchip RK3568 EVB User Guide Rev1.2, Power Diagram (p.12): SWOUT2 / Switch2 supplies VCC3V3_SD for MicroSD, 2.1A maximum, 100mΩ RDS(on): https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_EVB_User_Guide_V1.2_EN.pdf
