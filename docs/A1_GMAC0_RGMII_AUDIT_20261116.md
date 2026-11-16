# A1 Gigabit Ethernet GMAC0 / RTL8211F audit — 2026-11-16

**Native KiCad page 14 generated; structurally checked but NOT KiCad-CLI loaded, NOT ERC-clean, NOT board-release approved.**

## Pinmux assignment

| RK3568 BGA | Net | RTL8211F pin | VCCIO |
|---|---|---:|---|
| F24 | GMAC0_RXDV_CRS | 26 | 1.8V |
| H25 | GMAC0_RXD1 | 24 | 1.8V |
| H24 | GMAC0_MDC | 13 | 1.8V |
| H23 | GMAC0_MDIO | 22-ohm series to PHY | 1.8V |
| B28 | GMAC0_RXCLK | 27 | 1.8V |
| C27 | GMAC0_TXD2 | 16 | 1.8V |
| C28 | GMAC0_TXD3 | 15 | 1.8V |
| D27 | GMAC0_TXCLK | 20 | 1.8V |
| E27 | GMAC0_RXD2 | 23 | 1.8V |
| E28 | GMAC0_RXD3 | 22 | 1.8V |

- Existing GMAC0 native signal nets F27=RXD0 F28=TXD0 G27=TXD1 G28=TXEN preserved.
- GPIO0_D4 ball AB23 assigned ETH_PHY_RST_N as fixed PMUIO1 3.3V; per Rockchip RTL8211F reset only supports 3.3V and >10ms low.
- SDMMC1 is consumed by GMAC0 on B28/C27/C28/D27/E27/E28; **Wi-Fi must use SDMMC2 or alternate interface, not SDMMC1**.
- All 12 RGMII data/control/clock nets have 22-ohm placement near signal driver, with GMAC0_MDC series resistor 22R, MDIO pullup 1.5k to 1.8V.

## Realtek 40-pin native symbol
- QFN40 (+ exposed pad 41) 41 numbered pins match Realtek Rev1.4 pin assignments page 6.
- RTL8211F 3.3V AVDD33/DVDD33; external 1.8V RGMII DVDD_RG on pin 28; internal 1.0V regulator REG_OUT pin 30 via L301=2.2uH feeds PHY-only 1.0V AVDD10 and DVDD10.
- PHY 25MHz external crystal Y301; C308/C309 18pF **tentative** and must recalc after crystal selection.
- CFG_EXT=1, CFG_LDO1/0=10 (1.8V external RGMII); strap resistors R317..R319 must be confirmed with LED function before release.
- R315=2.49kΩ/1% for RSET, R316=10kΩ reset pullup, C301=100nF at reset pin.
- J301 LPJG16414A4NL Gigabit integrated magnetics RJ45 pin map follows TI TIDEP-01030 reference; actual supplier mechanical footprint remains **UNASSIGNED** (blocker); MagJack LED polarity and center-tap power are provisional until vendor schematic checked.
- CHASSIS ground via C310=1nF 2kV to GND is **provisional**, safety/EMC isolation must be reviewed.

## Critical unclosed gates
1. Confirm U301 QFN exposed pad/footprint dimensions using manufacturer mechanical drawing; its A1_ETH footprint is a **candidate**.
2. J301 has no footprint by design; **cannot fabricate** until exact MPN and copper/drill map verified. Magnetics LED polarity, shields and center taps must be validated from vendor PDF.
3. RTL8211F CFG straps (incl PHY address and TX/RX delay) and Linux DTS phy-mode (rgmii-id/rxid/txid), GMAC0 clocking, reset GPIO and timing require actual register/mux audit.
4. REG_OUT 1.0V loop and L301 current/ripple, 3.3V/1.8V sequencing, cable-side ESD and termination must pass vendor/layout review.
5. **No native KiCad load, ERC, netlist, PCB DRC or Linux bring-up has been executed.**

Sources: [Realtek RTL8211F datasheet Rev1.4](https://evelta.com/content/datasheets/429-RTL8211F-CG.pdf), [Rockchip RK3568 Hardware Design Guide](https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf), [TI Ethernet integrated MagJack reference](https://www.ti.com.cn/cn/lit/df/tidmco9/tidmco9.pdf).
