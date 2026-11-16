# Linux MiniHost A1 RK3568 SoC — 636-ball integration audit
Date: 2026-11-16

## Native schematic state
- U7 RK3568 represented as 17 editable unit instances on A1_RK3568_SOC.kicad_sch.
- All 636 ball positions are explicitly accounted for: 607 net-labeled pins and 29 no-connect markers.
- Original ball names and primary functions are retained in A1_RK3568_PINNETS.csv; each ball is assigned either a named net or explicit NC status.
- Power and ground nets have been mapped provisionally. Every signal without verified final mux or peripheral mapping has a *unique* SOC_<ball>_<function> net, preventing accidental short-circuit by a common unknown net.
- Per-ball net labeling is **not** equivalent to completion of the peripheral schematic or ERC success.

## Important electrical decisions and flags
- RK3568 LPDDR4X DDRPHY_VDDQ pins → VCC_DDR_1V1.
- RK3568 LPDDR4X DDRPHY_VDDQL pins → VCC0V6_DDR (NOT 1.1V).
- RK3568 DDR_RZQ ball H7 → R41 120Ω ±1% → VCC_DDR_1V1 (1.1V), per Hardware Design Guide Rev1.2 §2.1.7.2. This SoC reference resistor is distinct from DRAM U10 ZQ0 R40 240Ω ±1% to VCC0V6_DDR.
- VDD_CPU balls → VDD_CPU from a separately controlled dynamic CPU Buck (not yet drawn).
- VDD_CPU_COM has its own VDD_CPU_REMOTE_SENSE net, **do not short** to GND or 3.3V; check the chosen regulator's remote-sense arrangement.
- PMUIO1/2, VCCIO1..7 are provisionally mapped to 3.3V/1.8V domains per RK3568 IO-domain examples. Verify pinmux and DTS io-domain regulator supplies **before PCB layout**.
- VCCIO2=1.8V requires FLASH_VOL_SEL pulled high to a matching 1.8V rail, before boot; the pull-up is not yet placed.
- Critical PMIC I2C0 lines, PMIC interrupt GPIO0_A3, PMIC_SLEEP and CLK32K_IN have net names matching the RK809-5 page.
- 0.9V/1.8V/3.3V analog PHY balls are provisionally tied to named supply networks; local filtering and decoupling still need to be added.
- Unassigned peripheral signals keep unique ball names until exact pinmux and connectors are confirmed.
- 0 balls remain flagged POWER_BALL_REQUIRES_VERIFICATION in this mapping.

## Verification performed
- Source symbol has 17 logical units and 636 distinct ball numbers.
- Source footprint contains 636 distinct pad numbers (from preceding repository audit).
- Each source pin is represented exactly once as a placed schematic pin; 607 pins have global net labels and 29 have explicit no-connect markers.
- File assembled as balanced KiCad S-expressions by generator; **KiCad CLI has not been run**.
- Mark as DESIGN-IN-PROGRESS, NOT FABRICATION READY.

## Reference
- Rockchip RK3568 Hardware Design Guide Rev 1.2, section 2.1.7.5, LPDDR4X DDRPHY rails.
- RK3568 Datasheet Rev 2.1, package / pin list.
- RK3568 EVB IO voltage domain checklist and Linux RK3568 device-tree IO power domain definitions.
