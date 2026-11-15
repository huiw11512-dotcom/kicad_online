# Linux MiniHost A1 — Master Hardware Baseline Rev 1.0

Date: 2026-11-15  
Status: design baseline frozen for schematic development; not a fabrication release.

This file is the single source of truth for Rev 1. If older planning notes conflict with this file, this file takes precedence until those notes are updated.

## 1. Product definition

An independently designed RK3568 ARM64 Linux single-board computer. The functional target is a compact Raspberry Pi 4B-class Linux board: boot Linux from onboard eMMC, provide HDMI, Gigabit Ethernet, USB, Wi-Fi/Bluetooth and a 40-pin GPIO header. It is not a CM5 carrier and is not a copy of another SBC.

Performance note: RK3568 uses four Cortex-A55 cores; Raspberry Pi 4B uses Cortex-A72. A1 targets a similar application class and interface set, not identical CPU benchmark performance.

## 2. Rev 1 architecture — frozen decisions

| Block | Rev 1 decision | Freeze status |
|---|---|---|
| SoC | Rockchip RK3568, FCBGA636L, 19 × 19 mm | Device selected; ball map and land pattern verification required |
| RAM | 4 GB LPDDR4X, 32-bit | Capacity frozen; exact part/template/BIN pairing open |
| Boot storage | 32 GB eMMC 5.1, 8-bit | Capacity/interface frozen; exact part open |
| Removable storage | MicroSD, SDMMC0 4-bit | Interface frozen |
| PMIC | RK809-5 | Selected; full EVB rail-by-rail implementation open |
| CPU rail | Separate dynamic Buck, ≥4 A design capability | Architecture frozen; exact regulator and compensation open |
| Display | 1 × HDMI 2.0a | Frozen |
| Ethernet | 1 × Gigabit Ethernet, GMAC0 RGMII + external PHY | Frozen; exact PHY/strap/clock details open |
| USB Type-A | 1 × USB 3.x Host1 + 2 × USB 2.0 Host2/Host3 | Frozen |
| Service/download | 1 × Micro-USB on USB3_OTG0_DP/DM, device/download mode | Reserved per Rockchip requirement |
| Wireless | 1 soldered Wi-Fi/Bluetooth combo module, SDIO + UART | Architecture frozen; exact module open |
| GPIO | 40-pin, 2.54 mm header | Frozen as a feature; final pinout subject to pinmux and voltage-domain audit |
| Debug | 3-pin 3.3 V UART + Recovery/MaskROM access | Frozen |
| Input | USB-C PD 15 V / 3 A (45 W) | Frozen for Rev 1 |
| Main rail | 15 V_IN → 5 V_SYS, 5 A maximum converter target | Topology frozen; power/thermal validation open |
| PCB | 6-layer FR-4, 1.6 mm starting thickness | Starting target; stackup/impedance must be confirmed with fabricator |
| Outline | 85 × 56 mm target | Mechanical target only; freeze after connector and DDR placement |

### USB resource allocation

- USB3_HOST1 + MULTI_PHY1 → one USB 3.x Type-A Host port.
- USB2_HOST2 → one USB 2.0 Type-A Host port.
- USB2_HOST3 → one USB 2.0 Type-A Host port.
- USB3_OTG0_DP/DM → dedicated Micro-USB service/download port. The OTG0 SuperSpeed pair is not routed to a user port in Rev 1; MULTI_PHY0 is not allocated to SATA/PCIe.
- USB3_OTG0_VBUSDET must be connected as required by Rockchip. Keep the service port accessible for MaskROM/Loader/ADB and production flashing.
- Each Type-A VBUS gets its own current-limited load switch and connector-side ESD. Initial system VBUS budget: 0.9 A + 0.5 A + 0.5 A = 1.9 A total.

This deliberately prioritizes reliable recovery and a simple first board over maximizing the number of USB3 sockets.

## 3. Power baseline

1. USB-C PD Sink negotiates 15 V / 3 A. HUSB238 remains the selected controller candidate.
2. HUSB238 resistor targets from Hynetek's reference-design guide: RVSET = 14 kΩ for 15 V; RISET = 22.6 kΩ for 3.0 A.
3. Protected 15 V_IN feeds the main synchronous Buck.
4. LM76005 is the current 5 V / 5 A converter candidate. 5 V_SYS is the source for RK809-5 and the downstream regulators/loads.
5. The 5 V converter's 5 A output limit is the binding board-level power limit (25 W nominal), not the 45 W PD contract. The power budget must include conversion losses, SoC/DDR/PHY, Wi-Fi, HDMI, and up to 1.9 A USB VBUS. USB ports must be current-limited and total load managed.
6. RK809-5 input is 2.7–5.5 V; it must only receive 5 V_SYS, never 15 V_IN.
7. VDD_CPU uses an independent dynamic Buck with ≥4 A capability and remote feedback to VDD_CPU_COM.
8. RK809-5 rails and fixed power-on sequence must follow the complete RK3568 EVB reference schematic and the RK3568 Hardware Design Guide, not a simplified block diagram.
9. LPDDR4X SoC PHY rails and DRAM VDD1/VDD2/VDDQ are separate networks. Values are set only after the exact DRAM part and Rockchip template are paired.

### Existing input-stage review flags

- The current KiCad prototype requests 15 V / 3 A and uses AO4407A (30 V VDS) as the P-MOS path switch. The 30 V rating is not automatically accepted for production: TVS/clamp voltage, cable/transient conditions, MOSFET SOA and thermal margin must be checked. Keep Q1 as a candidate until that check closes.
- The current LM76005 5 V / 5 A values, inductor and capacitor bank remain provisional until the TI datasheet design equations, DC-bias derating, ripple, loop stability and thermal rise are checked.
- Add/verify input fuse or eFuse, TVS, reverse-current behavior, input bulk capacitance, and test points before freezing the input page.

## 4. Memory and boot decisions

### LPDDR4X

- Target: 4 GB, 32-bit.
- Candidate: Micron MT53E1G32D2FW-046 WT:C, not yet approved for A1.
- Must close all of: exact ordering code and datasheet revision, package ball map, Rockchip AVL row/application note, exact PCB template, exact DDR initialization BIN/version, WDQS requirement, SoC-to-DRAM DQ/DQS/CA/CK/CS mapping, and rail mapping.
- If the single x32 candidate cannot be proven compatible, switch to a Rockchip-supported two-device x16 organization. Do not force an unverified device into a convenient template.

### eMMC / MicroSD

- eMMC: 32 GB, 8-bit, HS200-capable target. Exact ordering code and VCC/VCCQ requirements remain open.
- MicroSD: SDMMC0 4-bit, with 3.3 V I/O as the initial plan, subject to VCCIO3 and pinmux confirmation.
- Recovery: preserve USB OTG0 firmware-download path and UART console.

## 5. Schematic page plan

1. USB-C_PD_INPUT — receptacle, HUSB238, input protection, PD status, input test points.
2. MAIN_POWER — 15 V to 5 V_SYS Buck, feedback, EN/PGOOD, protection, current/thermal budget.
3. RK809_PMIC — complete RK809-5 pinout, all Buck/LDO/SW rails, VCC input domains, RTC, crystal, I2C, PWRON, RESETB and unused-pin handling.
4. CPU_GPU_LOGIC_POWER — CPU dynamic Buck, feedback, GPU/logic/DDR-related power rails, sequencing and decoupling.
5. RK3568_SOC — all 636 balls, power/ground, clocks, reset, boot straps, UART, I2C and service/download signals.
6. LPDDR4X_4GB — exact matched DRAM device and complete bus/power wiring.
7. EMMC_MICROSD — eMMC 8-bit and MicroSD 4-bit.
8. GIGABIT_ETHERNET — RGMII, PHY, clock, straps, magnetics/RJ45 and ESD.
9. USB3_USB2 — one USB3 Host, two USB2 Host ports, VBUS switches and ESD.
10. HDMI — HDMI TX, DDC, HPD, CEC, +5 V and ESD.
11. WIFI_BT_GPIO — combo module, antenna keepout, 40-pin header, LEDs and buttons.
12. TEST_RECOVERY — UART, MaskROM/Recovery, JTAG/test pads and rail test points.

## 6. Hard gates before fabrication

- Gate A — SoC: verify all 636 ball numbers and names against Rockchip RK3568 Datasheet Rev 2.1 Table 2-1; verify BGA footprint origin, A1 orientation, pitch and land dimensions against the package drawing and assembly recommendation.
- Gate B — DDR: exact DRAM ↔ AVL ↔ PCB template ↔ DDR BIN compatibility proven; then verify all bus lanes and rails.
- Gate C — PMIC/power: transcribe the full EVB RK809-5 implementation pin-by-pin; calculate startup sequence, steady-state and transient current, DC drop, ripple and thermal rise.
- Gate D — interfaces: finalize SoC pinmux, IO-bank voltages, USB Multi-PHY allocation, PHY straps and ESD parts.
- Gate E — PCB: 6-layer stackup and impedance controlled by fabricator; DDR placement/routing must follow the matched Rockchip template; complete ERC/DRC and netlist review.

No board fabrication is authorized until all gates are closed and the native KiCad ERC/DRC reports have been reviewed.

## 7. Primary references

- Rockchip RK3568 Datasheet Rev 2.1 (2024-06-21), especially Table 2-1 Pin Number List, Table 2-2 Power/Ground IO, and package drawing: https://www.boardcon.com/download/Rockchip_RK3568_Datasheet_V2.1-20240621.pdf
- Rockchip RK3568 Hardware Design Guide Rev 1.2: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Hynetek HUSB238 Sink Reference Design Guide, RVSET/RISET resistor tables: https://en.hynetek.com/2525.html
- Rockchip RK3568 DDR template/BIN configuration table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md
- RK3568 public reference hardware index: https://github.com/hqnicolas/RK3568-hardware-design

## 8. Current implementation status

- Native KiCad root schematic contains the USB-C PD input and 15 V to 5 V main Buck prototype, and links the RK809-5 PMIC page 2.
- RK809-5 has a complete 69-pin symbol and 68+EP candidate footprint; its output-to-SoC rail allocation is not frozen.
- RK3568 symbol library exists, but the SoC has not yet been placed in the root schematic. LPDDR4X, eMMC and external interfaces are not yet drawn.
- The project has not passed native KiCad load, ERC, netlist export, visual review, PCB DRC or hardware bring-up.
- This baseline resolves architecture conflicts; it does not represent a completed schematic or fabrication-ready design.
