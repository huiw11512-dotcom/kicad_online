# A1 40-pin GPIO header Rev1 - 2026-11-16

Native KiCad page16 `A1_GPIO_40PIN.kicad_sch` wired to root. 40 numbered pads, 28 separate SoC 3.3V pinmux assignments, 12 power/ground pins. **This is not certified pin-compatible electrically or in Linux GPIO numbering with Raspberry Pi 4B.**

## Physical pinout

| Pin | Net | SoC ball |
|---:|---|---|
| 1 | VCC_3V3 | — |
| 2 | GPIO_HDR_5V_FUSED | — |
| 3 | HDR_I2C2_SDA | AA20 |
| 4 | GPIO_HDR_5V_FUSED | — |
| 5 | HDR_I2C2_SCL | AC22 |
| 6 | GND | — |
| 7 | HDR_GPIO3_A0 | AH4 |
| 8 | HDR_UART0_TX | AF23 |
| 9 | GND | — |
| 10 | HDR_UART0_RX | AD22 |
| 11 | HDR_GPIO3_A1 | AB8 |
| 12 | HDR_GPIO3_A2 | AE5 |
| 13 | HDR_GPIO3_A3 | AG4 |
| 14 | GND | — |
| 15 | HDR_GPIO3_A4 | AF4 |
| 16 | HDR_GPIO3_A5 | AH3 |
| 17 | VCC_3V3 | — |
| 18 | HDR_GPIO3_A6 | AG3 |
| 19 | HDR_GPIO3_A7 | AH2 |
| 20 | GND | — |
| 21 | HDR_GPIO3_B0 | AG2 |
| 22 | HDR_GPIO3_B1 | AG1 |
| 23 | HDR_GPIO3_B2 | AF2 |
| 24 | HDR_GPIO3_B3 | AF1 |
| 25 | GND | — |
| 26 | HDR_GPIO3_B4 | AE1 |
| 27 | HDR_I2C1_SDA | AB20 |
| 28 | HDR_I2C1_SCL | AG24 |
| 29 | HDR_GPIO3_B5 | AE2 |
| 30 | GND | — |
| 31 | HDR_GPIO3_B6 | AE3 |
| 32 | HDR_GPIO3_B7 | AD4 |
| 33 | HDR_GPIO0_C2 | AG23 |
| 34 | GND | — |
| 35 | HDR_GPIO0_C3 | AE23 |
| 36 | HDR_GPIO0_C4 | AD21 |
| 37 | HDR_GPIO0_C5 | AC21 |
| 38 | HDR_GPIO0_C6 | AD20 |
| 39 | GND | — |
| 40 | HDR_GPIO0_C7 | AH25 |

- Pin 1,17: VCC_3V3; pin 2,4: 5V_SYS via resettable PTC F501=1.1A holding-current candidate; pins 6,9,14,20,25,30,34,39: GND.
- GPIO3_A0..B7: VCCIO5 fixed 3.3V; GPIO0_C0..C7 and I2C1/2: PMUIO2 fixed 3.3V as current SoC power-net plan; confirm PMUIO2 startup and pullups.
- R501..R504: 4.7k pullups to VCC3V3_PMU on two I2C buses. Pin labels are A1-specific.
- All IO **3.3V only, NOT 5V-tolerant**; never attach 5V logic to IO pins.
- No multiplexed pin is assigned to GMAC0 Ethernet, HDMI CEC M0, UART4 Bluetooth, SDMMC2 WiFi, eMMC, MicroSD, USB2 power enable or UART2 debug.

## Unclosed
- Confirm header footprint orientation (pin 1 upper left physically), mechanical enclosure space, PTC thermal trip, 3.3V GPIO current and PMUIO2 domain limits.
- GPIO header ESD and external 5V reverse injection remain OPEN; fused output is not anti-backfeed protection.
- Validate Linux DTS pinctrl/pad drive before software; no native KiCad/ERC/PCB execution in this commit.
- Board not ready for fabrication or release.
