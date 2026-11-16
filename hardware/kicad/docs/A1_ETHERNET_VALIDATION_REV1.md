# A1 Ethernet PHY review — 2026-11-16

Status: schematic page exists; electrical sign-off is NOT complete. This review records the checks required before PCB placement/routing. It does not claim that native KiCad ERC or hardware validation has passed.

## Design under review

- PHY: Realtek RTL8211F-CG, 10/100/1000BASE-T, RGMII.
- Connector/magnetics: HR911130A MagJack (verify exact manufacturer's pinout and LED/common-mode network against the purchased revision).
- SoC interface labels present on both pages: GMAC0_TXD[3:0], GMAC0_TXEN, GMAC0_TXCLK, GMAC0_RXD[3:0], GMAC0_RXDV, GMAC0_RXCLK, GMAC0_MDC, GMAC0_MDIO and ETH0_REFCLKO_25M.
- PHY-side labels present: PHY_TXD[3:0], PHY_TXCTL, PHY_TXC, PHY_RXD[3:0], PHY_RXCTL, PHY_RXC, PHY_MDC, PHY_MDIO, PHY_RESET_N and PHY_INT_N.
- Local power/reference labels present: VCC3V3_SYS, VCC_1V8, PHY_1V0, PHY_REG_OUT, PHY_DVDD_RG, PHY_25M_CLK and PHY_RSET.

## Mandatory checks before declaring Ethernet complete

1. **PHY configuration straps.** RTL8211F samples RXD3, RXC, RXCTL, RXD2, RXD1 and RXD0 for PHY address, PLL-off behavior, RGMII TX/RX clock-delay selection and related configuration. Verify each strap resistor value and polarity against the exact RTL8211F-CG datasheet table, and confirm that the same nets still reach the RK3568 after strap sampling. Do not rely on net names alone.
2. **RGMII timing mode.** Choose exactly one clock-delay strategy: PHY internal delay or PCB-added delay. The datasheet describes approximately 2 ns internal delay options and requires controlled skew when delay is provided on the PCB. Record the chosen TX and RX modes, then route TXC/RXC and their data/control groups to the matching timing budget. Do not blindly add long serpentine delays if the PHY straps already enable internal delay.
3. **Reference clock.** Confirm the 25 MHz crystal/oscillator circuit, load capacitors (if crystal), drive level, and whether ETH0_REFCLKO_25M is an output to the MAC or an input/reference in the selected RK3568 pinmux configuration. Check no unintended clock-output contention exists.
4. **Power tree.** Confirm the RTL8211F-CG switching-regulator topology: REG_OUT must feed only the PHY's specified 1.0 V domains (DVDD10/AVDD10) through the recommended inductor/filter arrangement; it must not be treated as a general 1.0 V board rail. Verify all AVDD33, DVDD_RG, I/O and analog supply pins, decoupling placement and power-up sequence against the datasheet and layout guide.
5. **RSET and analog front end.** Verify the RSET resistor value/tolerance and ground return, all MDI differential pairs, center-tap/bias network, Bob Smith termination if required by the selected MagJack/reference design, and ESD placement. Keep the PHY-to-MagJack analog path short and symmetric.
6. **Reset/management.** Confirm PHYRSTB polarity, pull-up/down and reset timing; MDIO pull-up voltage must match the selected RGMII I/O voltage. Confirm MDC/MDIO are mapped to the intended RK3568 GMAC0 pins and PHY address agrees with the Linux device tree.
7. **MagJack.** Check HR911130A pin numbers against the actual vendor drawing, including MDI pairs, center taps, LED anodes/cathodes and shield. Confirm LED resistor polarity/current and chassis/shield strategy.
8. **SoC pinmux and software.** Cross-check every GMAC0 signal against the RK3568 datasheet/pinmux and the chosen GMAC controller instance. The device tree must use the same interface mode, PHY address, reset GPIO, clock direction and delay settings as the hardware.

## PCB constraints to carry forward

- Treat RGMII as a timing-critical interface; maintain a continuous reference plane and avoid stubs.
- Route each RGMII data/control group with the clock according to the selected internal/PCB delay strategy and the Rockchip/Realtek timing budgets.
- Route the four MDI pairs as controlled-impedance differential pairs with consistent geometry, pair symmetry and minimal via count. Keep them away from switching nodes, crystal and high-current power loops.
- Place PHY decoupling at the associated supply pins; keep REG_OUT/inductor/capacitor loop compact and follow Realtek's layout guide.
- Place ESD protection at the connector side, without long unprotected traces between connector and protection device.

## Release gate

Ethernet may be marked complete only after all of the following are attached to the project:
- Exact RTL8211F-CG datasheet revision and HR911130A manufacturer drawing.
- Pin-by-pin strap/power/clock/reset audit table.
- KiCad native ERC report and exported netlist cross-check.
- Confirmed RK3568 GMAC0 pinmux + Linux device-tree configuration.
- PCB impedance/timing review and first-board link tests at 10/100/1000 Mb/s.

## References

- Realtek product page: https://www.realtek.com/Product/Index?cate_id=194&id=3975&menu_id=291
- RTL8211F(I)-CG datasheet (LCSC-hosted PDF): https://datasheet.lcsc.com/datasheet/pdf/7023c5bb6713a670a415e3c449e0d974.pdf?productCode=C187932
- RTL8211F(I)-CG datasheet, RGMII timing/strap details: https://files.pine64.org/doc/datasheet/rock64/RTL8211F-CG-Realtek.pdf
