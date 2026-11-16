# A1 Ethernet PHY review — 2026-11-16

**Status:** preliminary schematic page exists; strap topology and clock path have been decoded from the current source. Native ERC, full netlist audit, PCB review and hardware validation are still open. Do not release for fabrication.

## 1. Design under review

- PHY: Realtek RTL8211F-CG, 10/100/1000BASE-T, RGMII.
- Connector/magnetics: HR911130A MagJack, LCSC C54408.
- SoC interface: RK3568 GMAC0 RGMII.
- Schematic: `hardware/kicad/A1_ETHERNET.kicad_sch`.
- RGMII series resistors: R120–R134, 22 Ω each.
- PHY internal 1.0 V switching regulator: REG_OUT → L20 4.7 µH → PHY_1V0.

## 2. Strap values decoded from the current schematic

The following are the actual resistor connections currently present in `A1_ETHERNET.kicad_sch`. The logic values below are derived from the Realtek RTL8211F(I)-CG Rev.1.4 strap table.

| PHY strap | Pin | Resistor / connection | Sampled value | Meaning |
|---|---:|---|---:|---|
| PHYAD0 | RXD3 / 22 | R139 4.7 kΩ to PHY_DVDD_RG | 1 | PHY address bit 0 |
| PHYAD1 | RXC / 27 | R140 4.7 kΩ to GND | 0 | PHY address bit 1 |
| PHYAD2 | RXCTL / 26 | R141 4.7 kΩ to GND | 0 | PHY address bit 2 |
| PLLOFF | RXD2 / 23 | R142 4.7 kΩ to GND | 0 | Keep PLL running in ALDPS |
| TXDLY | RXD1 / 24 | R143 4.7 kΩ to PHY_DVDD_RG | 1 | Add 2 ns internal TXC delay |
| RXDLY | RXD0 / 25 | R144 4.7 kΩ to PHY_DVDD_RG | 1 | Add 2 ns internal RXC delay |
| CFG_EXT | LED0 / 32 | R145 4.7 kΩ to GND | 0 | Use the PHY's internal RGMII I/O LDO |
| CFG_LDO0 | LED1 / 33 | R146 4.7 kΩ to GND | 0 | LDO voltage select bit 0 |
| CFG_LDO1 | LED2 / 34 | R147 4.7 kΩ to VCC3V3_SYS | 1 | LDO voltage select bit 1 |

**Decoded result:**

- PHY address = `001b` = **1**. Linux device tree must use PHY address 1.
- CFG_EXT=0 and CFG_LDO[1:0]=10 select the internal **1.8 V RGMII I/O LDO**, matching RK3568 VCCIO4=1.8 V.
- TXDLY=1 and RXDLY=1 enable approximately 2 ns internal delay on both directions. The RK3568 MAC/device-tree must not add another TX/RX delay. Use the no-extra-delay RGMII mode and verify the actual Rockchip driver configuration.
- R139/R143/R144 pull to PHY_DVDD_RG, which is the PHY's internal 1.8 V RGMII LDO output in this strap mode. Do not externally drive PHY_DVDD_RG from VCC_1V8 while CFG_EXT=0.

Other decoded support parts:
- R138 = 1.5 kΩ MDIO pull-up to VCC_1V8, matching the 1.8 V management I/O domain.
- R136 = 10 kΩ PHYRSTB pull-up to VCC3V3_SYS.
- R137 = 4.7 kΩ PHY_INT_N pull-up to VCC3V3_SYS.
- R148 = 2.49 kΩ RSET to GND.
- R135 = 4.7 kΩ default pull-down on GMAC0_TXEN; verify SoC output drive and reset behavior in the final netlist.

## 3. Reference clock — current topology is an external-clock input

The current circuit is not a crystal network:

- RK3568 `ETH0_REFCLKO_25M` output → R134 (22 Ω) → `PHY_25M_CLK`.
- `PHY_25M_CLK` connects to RTL8211F pin 37, `XTAL_OUT/EXT_CLK`.
- RTL8211F pin 36, `XTAL_IN`, is tied to GND, as required when an external 25 MHz clock drives pin 37.
- RK3568 G23 is in the 1.8 V VCCIO4 domain. This is compatible with the Realtek external-clock input thresholds (VIH ≥ 1.4 V, VIL ≤ 0.4 V); it is not necessary to force this clock to 3.3 V.

Before release, measure/confirm the SoC clock output at the PHY pin:
- Frequency: 25 MHz, tolerance within ±50 ppm.
- Duty cycle: 40–60%.
- Broadband peak-to-peak jitter: ≤200 ps.
- Rise/fall time: ≤10 ns.
- Ensure the clock is not stopped while the PHY remains powered. If the SoC clock cannot meet these requirements, replace this path with a compliant low-jitter oscillator and revise the pin36/pin37 topology; do not add a second clock source while R134 is populated.

## 4. RGMII timing

The PHY straps currently enable 2 ns internal delay on both TX and RX. Therefore:
- Keep the MAC/SoC-side additional delay disabled.
- Do not use a device-tree mode that also requests PHY internal delay without checking the RTL8211F driver behavior.
- Route TXC/RXC with their associated data/control groups, continuous reference plane and controlled impedance.
- Check the RK3568 GMAC0 timing requirements and the Realtek RGMII timing tables together; do not add arbitrary serpentine delay.

## 5. Power tree

- AVDD33/DVDD33: VCC3V3_SYS.
- REG_OUT: PHY internal switching regulator output; L20=4.7 µH feeds PHY_1V0. This is within the Realtek recommended 2.2/4.7 µH options.
- AVDD10/DVDD10: PHY_1V0 only; do not use it as a general board rail.
- DVDD_RG: internal 1.8 V RGMII I/O LDO output in the current CFG_EXT=0 mode.
- Check all local bypass capacitors and keep the REG_OUT/inductor/output-capacitor loop compact.
- Follow Realtek's 3.3 V / internal 1.0 V regulator power sequence. Do not repeatedly toggle the PHY 3.3 V source without allowing the specified discharge interval.

## 6. Reset, management and interrupt

- PHYRSTB is active low and must be held low for at least 10 ms for a complete hardware reset.
- R136 provides a 10 kΩ pull-up to VCC3V3_SYS; confirm the SoC reset GPIO can pull it low and that reset release occurs only after required supplies and clock are stable.
- MDIO uses R138=1.5 kΩ to VCC_1V8; keep the SoC management I/O voltage at 1.8 V.
- PHY_INT_N uses R137=4.7 kΩ to VCC3V3_SYS; confirm the RK3568 GPIO input is 3.3 V tolerant or add level translation if not.
- Set PHY address 1 in the Linux device tree.

## 7. HR911130A LED and connector wiring

- Green LED polarity has been corrected in the schematic: pin 11 (LED_GREEN_A) now connects through R149=510 Ω to PHY_CFG_LDO0_LED1; pin 12 (LED_GREEN_K) connects to GND. This matches CFG_LDO0=0, for which LED1 is active high.
- Yellow LED: pin 14 (LED_YELLOW_A) connects through R150=510 Ω to VCC3V3_SYS; pin 13 (LED_YELLOW_K) connects to PHY_CFG_LDO1_LED2. This matches CFG_LDO1=1, for which LED2 is active low.
- Recheck pin 10 (P10/CM), pin 1 (TCT), shield pins 15/16 and the 0 Ω / 1 MΩ shield network against the exact HR911130A manufacturer drawing and the purchased revision.
- Verify the integrated magnetics/common-mode termination before adding any external Bob Smith network; avoid duplicating internal termination.
- Add connector-side ESD protection and confirm the shield/chassis return strategy.

## 8. SoC pinmux and PCB constraints

- GMAC0 RGMII uses the selected RK3568 GMAC0 pinmux and shares physical balls with SDMMC1 alternate functions. Wi-Fi has therefore been moved to SDMMC2 M0; do not reassign SDMMC1 to Wi-Fi.
- Maintain a continuous reference plane and avoid stubs on RGMII.
- Route four MDI pairs as controlled-impedance differential pairs with consistent geometry, pair symmetry and minimal via count. Keep them away from switching nodes, clock and high-current power loops.
- Place PHY decoupling at the associated supply pins; keep REG_OUT/inductor/capacitor loop compact.
- Place ESD protection at the connector side.

## Release gate

Ethernet may be marked complete only after all of the following are attached to the project:
- Exact RTL8211F-CG datasheet revision and HR911130A manufacturer drawing.
- Native KiCad ERC report and exported netlist cross-check.
- Confirmed RK3568 GMAC0 pinmux, 1.8 V VCCIO4, PHY address 1, and no-extra-delay RGMII device-tree configuration.
- Measured/verified 25 MHz clock waveform at pin 37.
- PCB impedance/timing review and first-board link tests at 10/100/1000 Mb/s.

## References

- Realtek RTL8211F(I)-CG datasheet Rev.1.4 (pin descriptions, strap table, LDO selection, clock requirements and RGMII timing): https://robu-prod-media.s3.ap-south-1.amazonaws.com/uploads/2025/08/C187932.pdf
- Realtek product page: https://www.realtek.com/Product/Index?cate_id=194&id=3975&menu_id=291
- HR911130A datasheet, LCSC C54408: https://lcsc.com/datasheet/lcsc_datasheet_2411121131_HANRUN-Zhongshan-HanRun-Elec-HR911130A_C54408.pdf
