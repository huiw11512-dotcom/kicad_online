# A1 Wi-Fi / Bluetooth pinmux and electrical baseline — Rev1

**Date:** 2026-11-16  
**Status:** provisional pinmux allocation committed; module schematic and electrical implementation are not complete. Do not treat this as a fabrication release.

## 1. Pin-mux conflict found and resolved at the host allocation level

The A1 Ethernet implementation uses RK3568 GMAC0 in RGMII mode. The selected GMAC0 RGMII balls overlap the SDMMC1 alternate-function group. Rockchip's RK3568 Hardware Design Guide describes SDMMC1 as the default SDIO-Wi-Fi controller, but the same physical balls cannot simultaneously carry GMAC0 RGMII and SDMMC1 SDIO.

**Rev1 allocation:** retain GMAC0 RGMII for Gigabit Ethernet and move Wi-Fi SDIO to **SDMMC2 M0**, which is the VCCIO6 group. Do not route Wi-Fi to SDMMC1.

## 2. Provisional module candidate

- Module candidate: **AMPAK AP6275S**, 2T2R Wi-Fi 6 + Bluetooth combo, 50-pad stamp module, nominal outline 15 × 13 mm.
- Wi-Fi host interface: 4-bit SDIO.
- Bluetooth host interface: HCI UART; PCM remains unused in Rev1.
- Candidate orderable listing: LCSC C2918717. Confirm exact revision, origin and current stock before BOM release.
- Current AMPAK datasheet revision 2.7 is dated 2026-05-20.

**Important part-revision discrepancy — do not freeze the module footprint yet:** the current AMPAK Rev.2.7 pin table assigns pin 33=WL_GPIO_10, pin 35=WL_GPIO_11 and pin 48=NC. The older LCSC C2918717-hosted datasheet assigns pin 33=NC, pin 35=NC and pin 48=BT_ANT. This changes the Bluetooth RF/antenna interface. The SoC-side SDMMC2/UART pin allocation remains a valid host-side reservation, but the AP6275S module padout, antenna topology and native footprint are **not released** until the exact purchased module revision is confirmed by AMPAK/LCSC. Do not combine the Rev.2.7 pinout with the older C2918717 footprint.

## 3. RK3568 pin allocation

### Wi-Fi SDIO — SDMMC2 M0 / VCCIO6 = 1.8 V

| RK3568 ball | SDMMC2 M0 function | A1 net | Module function |
|---|---|---|---|
| AC5 | SDMMC2_D0_M0 | WIFI_SDIO_D0 | SDIO_DATA_0 |
| AA6 | SDMMC2_D1_M0 | WIFI_SDIO_D1 | SDIO_DATA_1 |
| AB5 | SDMMC2_D2_M0 | WIFI_SDIO_D2 | SDIO_DATA_2 |
| AB1 | SDMMC2_D3_M0 | WIFI_SDIO_D3 | SDIO_DATA_3 |
| Y7 | SDMMC2_CMD_M0 | WIFI_SDIO_CMD | SDIO_DATA_CMD |
| AC1 | SDMMC2_CLK_M0 | WIFI_SDIO_CLK | SDIO_DATA_CLK |
| AA1 | GPIO3_D4 / SDMMC2_DET_M0 | WIFI_HOST_WAKE | WL_HOST_WAKE (provisional) |
| AA5 | GPIO3_D5 / SDMMC2_PWREN_M0 | WIFI_REG_ON | WL_REG_ON (provisional) |

All six SDMMC2 M0 data/clock/command signals are in the VCCIO6 domain. A1 currently supplies VCCIO6 from VCC_1V8, matching the AP6275S VDDIO requirement.

### Bluetooth UART — UART8 M0 / VCCIO4 = 1.8 V

| RK3568 ball | UART8 M0 function | A1 net | Module function |
|---|---|---|---|
| F26 | UART8_TX_M0 | BT_UART8_TX | BT_UART_RXD |
| E26 | UART8_RX_M0 | BT_UART8_RX | BT_UART_TXD |
| D26 | UART8_RTSn_M0 | BT_UART8_RTS_N | BT_UART_CTS_N |
| E25 | UART8_CTSn_M0 | BT_UART8_CTS_N | BT_UART_RTS_N |

UART signals are named from the host perspective; TX/RX and RTS/CTS cross to the corresponding module input/output pins. VCCIO4 is currently 1.8 V, matching module VDDIO.

The pin labels and the 636-row SoC pin assignment CSV have been updated together. The current static coordinate audit reports 636 unique balls, 610 assigned nets, 26 explicit NC balls, and zero net-label/CSV mismatches. This is a source consistency check, not a native KiCad ERC.

## 4. SDIO clock-mode limit

Rockchip's RK3568 Hardware Design Guide states that SDMMC2 supports up to 150 MHz. The AP6275S supports 1.8 V 4-bit SDIO modes including SDR50 (100 MHz), SDR104 (208 MHz) and DDR50 (50 MHz).

**Rev1 target: SDR50 at 100 MHz.** Do not claim SDR104 operation at 208 MHz on SDMMC2. The controller's 150 MHz ceiling is below the module's SDR104 clock requirement. Confirm the actual RK3568 driver/clock configuration and module firmware during bring-up.

## 5. Power and clock requirements to implement

- **VBAT:** 3.0–3.8 V, nominal 3.3 V. AMPAK lists 1.2 A peak consumption at VBAT=3.3 V. Reserve at least 1.5 A transient headroom on the 3.3 V source pending a complete board power budget.
- **VDDIO:** 1.68–1.98 V, nominal 1.8 V. Connect to a verified 1.8 V rail; do not drive the module I/O from 3.3 V.
- **LPO:** external 32.768 kHz clock, 1.8 V amplitude. A1's PMIC/SoC 32.768 kHz net is in the 3.3 V PMUIO2 domain; it must not be connected directly to the module LPO. Add a suitable 1.8 V clock buffer/level translation or a dedicated 1.8 V oscillator.
- **Reference clock:** external 37.4 MHz crystal; ±10 ppm frequency tolerance, 18 pF load capacitance and ESR≤60 Ω. Add the oscillator network to the Wi-Fi page and verify crystal ESR/load.
- **Power-up sequence:** VBAT must be present before or at the same time as VDDIO; its rise time must be 40 µs to 100 ms. Keep WL_REG_ON and BT_REG_ON low until approximately two LPO cycles after the supplies rise. BT_REG_ON must never float.
- **RF:** reserve both antenna feed paths and the module's keep-out area; antenna matching and enclosure clearance require mechanical review.

## 6. Wake and standby limitation

AA1 and AA5 are provisional control allocations in VCCIO6. Rockchip warns that VCCIO1–VCCIO7 GPIO states are not retained when VDD_LOGIC is powered off; SDIO Wi-Fi control signals that must wake the host should be moved to a PMUIO domain.

Before adding the module schematic, choose one:
1. Rev1 explicitly does not support deep-suspend wake from Wi-Fi; retain the provisional VCCIO6 controls; or
2. Move required wake/control signals to an always-on PMUIO domain and add level translation to the module's 1.8 V VDDIO domain.

BT_REG_ON, BT_WAKE and BT_HOST_WAKE are not yet allocated. Their retention and voltage-level requirements remain open. Do not leave BT_REG_ON floating.

## 7. Release gates

- Resolve the AMPAK Rev.2.7 versus LCSC C2918717 pin-33/pin-35/pin-48 discrepancy and obtain the exact purchased module revision. Only then create the native symbol and 50-pad footprint; verify pin-1 orientation, paste apertures, RF port count and assembly capability.
- Add VBAT/VDDIO decoupling, local VBAT filtering and a 1.5 A transient power budget. Confirm the required external network for CBUCK_0P9/CSR_VLX and ASR_VLX/ABUCK_1P12 against the matching module-revision reference schematic; these pins must not be left floating or grounded by guesswork.
- Add 37.4 MHz crystal and a valid 1.8 V 32.768 kHz LPO source/translator; keep NC pins floating exactly as specified by the confirmed module revision.
- Complete WL_REG_ON, BT_REG_ON, WL_HOST_WAKE, BT_WAKE and BT_HOST_WAKE allocation with the chosen standby policy.
- Add the module page and BOM; run native KiCad ERC and netlist cross-check.
- Confirm the RK3568 device tree selects SDMMC2 M0, 1.8 V VCCIO6, SDR50/100 MHz and UART8 M0; validate firmware and Wi-Fi/BT enumeration on the first board.

## References

- Rockchip RK3568 Hardware Design Guide V1.2, §2.3.1: SDMMC1/2 domains and SDMMC2 150 MHz maximum; §2.3.1.4: SDIO Wi-Fi standby-control requirement.  
  https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- AMPAK AP6275S Datasheet Rev. 2.7, 2026-05-20: power rails, pin assignment, 32.768 kHz LPO, 37.4 MHz reference and SDIO timing.  
  https://www.ampak.com.tw/uploads/files/shares/DataSheet/Stamp_Type_2T2R/AP6275S%20datasheet_EN.pdf
- AMPAK AP6275S product page.  
  https://www.ampak.com.tw/product/WiFi-Bluetooth/Stamp-Type-2T2R/AP6275S
- LCSC AP6275S listing, C2918717.  
  https://www.lcsc.com/product-detail/C2918717.html
