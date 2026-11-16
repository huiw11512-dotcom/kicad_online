# A1 AP6256 Wi-Fi + Bluetooth SDMMC2 - 2026-11-16

**Page 15 committed as editable KiCad schematic, but not ERC clean / NOT yet hardware release.**

## Critical RK3568 mux and domain decisions
- SDMMC2 M0 from VCCIO6=1.8V: AC5=D0, AA6=D1, AB5=D2, AB1=D3, Y7=CMD, AC1=CLK; six 22Ω series footprints near SoC; five 47kΩ pulls to 1.8V on CMD/D0-3.
- AA5/GPIO3_D5=WL_REG_ON, AA1/GPIO3_D4=WL_HOST_WAKE, Y6/GPIO3_D6=BT_REG_ON, Y5/GPIO3_D7=BT_HOST_WAKE, AA7/GPIO3_C2=BT_WAKE. All 1.8V GPIO bank VCCIO6.
- UART4 M0 uses VCCIO1=3.3V: F18 RX<-BT UART_TXD, C20 TX->BT UART_RXD, B20 CTS<-BT UART_RTS, A20 RTS->BT UART_CTS. TXB0104PWR level translates A-side 1.8V and B-side 3.3V, with OE delayed by RC bias.
- AP6256 VDDIO=VCC_1V8, SDIO_VSEL=1.8V HIGH; VBAT via 0Ω link from VCC3V3_SYS, bulk capacitor 22uF; verify 3.3V peak power >1A including regulator derating.
- PMIC_CLK32K feeds AP6256 LPO, 32.768kHz output amplitude/drive >1.6Vpp must be measured/verified against PMIC output.
- AP6256 module pin10/11: 37.4MHz external crystal Y401; 1pF/18pF tuning caps are placeholders from reference, final vendor crystal load capacitance must be computed.
- AP6256 21 VIN_LDO_OUT -> L401 4.7uH -> 23 VIN_LDO, 4.7uF output cap; verify vendor exact buck topology and inductor current before design signoff.
- RF port 2 to U.FL J401, 50Ω line, antenna keepout. Matching network may need 3-element pi option after antenna measurements.
- GPIO PCM pins 25-28, reserved GPIO 37-40 and test pads 45-47 intentionally NC; do not ground NC.

## Important design blockers
1. 47-pad candidate AP6256 footprint and center NC pads must be measured against SparkLAN Rev1.4 mechanical drawing & stencil recommendations. Symbol pin count 47, reference shows 44 perimeter + 3 center NC.
2. TXB0104 logic translator requires short traces, no strong UART pullups (<50kΩ), and 1.8V/3.3V sequencing validation; radio firmware must support hardware flow control at selected UART4 mode.
3. AP6256 37.4MHz oscillator and 32k LPO input, internal 4.7uH buck current and Pi-antenna match are unqualified until real module tests.
4. Linux device-tree SDMMC2 pinctrl, vmmc/vqmmc supplies, BT UART4 pinctrl and rfkill, firmware driver compatibility need software build + actual bring-up.
5. No KiCad native ERC/netlist/DRC or actual RF/SDIO validation executed.

Datasheets: https://varitec.co.jp/wp/wp-content/uploads/2024/03/AP6256_datasheet-ver1.4_20230502.pdf , https://datasheet.lcsc.com/lcsc/1810151620_Texas-Instruments-TXB0104PWR_C60708.pdf , Rockchip reference https://download.t-firefly.com/product/Board/RK356X/Document/Hardware/ROC-RK3568-PC/SCH/V1.1/ROC-RK3568-PC-V11-20211028.pdf

## 2026-11-16 bank mismatch correction
- Critical: original draft incorrectly connected `BT_WAKE_1V8` to Y2/GPIO4_A4, which is VCCIO7 3.3V. This was **unsafe for AP6256 1.8V IO**.
- The BT_WAKE_1V8 SoC signal is now assigned AA7/GPIO3_C2 (VCCIO6 1.8V); Y2 is restored to its unassigned CIF_D14 net.
- Actual RTL3 pinmux and power-bank confirmation and KiCad netlist are still required before hardware release.
