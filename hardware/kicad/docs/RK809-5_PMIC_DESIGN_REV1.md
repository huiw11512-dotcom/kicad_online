# RK809-5 PMIC page — A1 Rev1 implementation notes

Date: 2026-11-15  
Status: native editable KiCad page committed; not a fabrication release.

## 1. Selected device and package

- U3: Rockchip RK809-5.
- Package: QFN68, 7.0 × 7.0 mm, 0.35 mm lead pitch.
- Exposed pad: 5.49 × 5.49 mm nominal.
- Local candidate footprint: `A1_PMIC:RK809_QFN-68-1EP_7x7mm_P0.35mm_EP5.49x5.49mm`.
- Footprint contains 68 numbered perimeter lands plus EP pad 69. The source geometry matches the package dimensions in RK809 Datasheet Rev 2.5; the exact land pattern and stencil/thermal-via strategy still require assembly-house confirmation.

## 2. PMIC input distribution

| Pins | Name | A1 net | Decoupling |
|---|---|---|---|
| 10, 11, 24, 66 | VCC2/VCC1/VCC3/VCC4 | 5V_SYS | 10uF each |
| 22, 30, 4 | VCC5/VCC6/VCC7 | 5V_SYS | 10uF each |
| 57, 54 | VCC8/VCC9 | 5V_SYS | 10uF each |
| 45 | VCC_RTC | 5V_SYS | 1uF local |
| 44, 48 | VCC_1P8A/VCC_1P8D | PMIC_BUCK5_1V8 | 1uF each |
| 33 | VCC_SPK_HP | PMIC_SPK_HP_5V | 1uH filter + 10uF/100nF |

VCC_RTC is tied to the same 5V_SYS source as VCC9, meeting Rockchip's requirement that VCC_RTC be the highest PMIC supply (or within 0.3V of it) and not be powered later.

## 3. Buck power stages

| Channel | Default RK809-5 setting | A1 implementation | State |
|---|---:|---|---|
| BUCK1 | 0.9V | 0.47uH, 2×47uF, output net PMIC_BUCK1_0V9_TBD | Voltage/load mapping to SoC pending |
| BUCK2 | 0.9V | 0.47uH, 2×47uF, output net PMIC_BUCK2_0V9_TBD | Voltage/load mapping to SoC pending |
| BUCK3 | external resistor setting | 0.47uH, 2×47uF, external RH/RL placeholders | Must be set from final DRAM rail |
| BUCK4 | 0.5V, OFF | 0.47uH + 2×47uF stage populated; output reserved | Hardware retained; OTP-default OFF |
| BUCK5 | 1.8V | 0.47uH, 2×47uF; supplies internal 1.8V PMIC rails | 1.8V default retained |

Rockchip's RK3568 guide specifies 0.47uH inductors with saturation current above 3.5A and DCR below 50mOhm (preferably below 20mOhm). It specifies more than 30uF output capacitance for BUCK1/2/3/4 and more than 33uF for BUCK5. The schematic uses 2×47uF nominal per active buck as a conservative starting point; effective capacitance under DC bias must be checked against the selected capacitor datasheet.

BUCK3 uses an external divider referenced to 0.8V. The guide gives:
`RH = (VBUCK3 - 0.8) × RL / 0.8`.
RH/RL remain DNP/TBD until the exact LPDDR4X device and rail requirement are frozen. Do not populate guessed values.

## 4. LDO and switch channels

The RK809-5 OTP defaults from Datasheet Rev 2.5 are retained as the initial state:

| Output | Default | Startup sequence | A1 treatment |
|---|---:|---:|---|
| LDO1 | 0.6V OFF | OFF | NC |
| LDO2 | 0.9V | 1 | 1uF; output net reserved |
| LDO3 | 0.9V | 1 (about 200us after LDO2) | 1uF; output net reserved |
| LDO4 | 0.6V OFF | OFF | NC |
| LDO5 | 3.3V | 4 | 1uF; output net reserved |
| LDO6 | 3.3V | 2 | 1uF; output net reserved |
| LDO7 | 1.8V | 2 | 1uF; output net reserved |
| LDO8 | 1.8V | 2 | 1uF; output net reserved |
| LDO9 | 0.6V OFF | OFF | NC |
| SWOUT1/2 | 3.3V | 4 | 1uF each; outputs reserved |

These are the RK809-5 OTP defaults, not the final SoC rail map. Do not connect these outputs to RK3568 power balls until the Rockchip EVB power tree and the selected memory configuration are checked pin-by-pin.

## 5. Startup and control

- VDC divider: 100k/33k from 5V_SYS gives approximately 1.24V, above the 0.55V startup threshold and close to Rockchip's recommended 1.2V.
- VCC_RTC must be above 3.0V before VDC or PWRON starts the sequence.
- After EXT_EN rises, VCC9 must already be above 3.0V within 1.5ms. A1 supplies VCC9 and VCC_RTC from the pre-existing 5V_SYS rail.
- EXT_EN drives the external VDD_CPU regulator enable.
- PWRON is active low with an internal 17k pull-up to VCC_RTC; SW1 must hold it low for more than 500ms to trigger power-on.
- SLEEP is held low through 100k for normal operation.
- RESETB is open drain and has the required 100nF capacitor; its pull-up is to the 1.8V logic domain, not 5V.
- SCL/SDA/INT/RESETB/CLK32K are treated as open-drain signals and pulled up to the 1.8V domain.
- RTC crystal: 32.768kHz, CL=12.5pF candidate; two 22pF load capacitors follow the Rockchip guide's recommended value. Confirm the final crystal CL and parasitic capacitance.
- BATDIV, SNSP and SNSN are grounded because the fuel gauge is not used.

## 6. Explicitly unused functions

A1 Rev1 does not include the RK809 audio codec, headphone amplifier, microphone inputs, speaker output, or I2S/PDM audio. Pins 14–19 and 32–43 are marked NC, except VCC_SPK_HP which retains its filtered supply network per Rockchip's hardware guide. Fuel-gauge pins are grounded as specified above.

## 7. Unclosed gates

1. Map BUCK1/2/3, BUCK5, LDO2/3/5/6/7/8 and SWOUT1/2 to the RK3568 power tree using the full EVB schematic, not only the block diagram.
2. Confirm whether any unused channel requires a specific termination in the RK809-5 reference schematic.
3. Finalize BUCK3 divider after exact LPDDR4X voltage is known.
4. Select exact 0.47uH and 1uH inductor MPNs with saturation current, DCR and temperature rise verified.
5. Verify capacitor effective capacitance under DC bias, ESR and package size.
6. Confirm QFN68 land pattern, EP solder paste segmentation and thermal via strategy with assembly house.
7. Run native KiCad load, ERC and netlist export; this environment has not executed KiCad CLI.

## References

- Rockchip RK809 Datasheet Rev 2.5, Apr. 2025: https://www.boardcon.com/download/Rockchip_RK809_Datasheet_V2.5-20250407.pdf
- Rockchip RK3568 Hardware Design Guide Rev 1.2, sections 2.2.3.3–2.2.3.5: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
- Rockchip RK3568 EVB User Guide Rev 1.2: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_EVB_User_Guide_V1.2_EN.pdf
- Rockchip RK3568 DDR template/BIN compatibility table: https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md


## Selected power-inductor parts and footprint

- BUCK1/2/3/4/5: TDK SPM5030T-R47M-HZ, 0.47uH, Isat 11A typ, Itemp 14A typ, DCR 5.39mOhm max, 5.2×5.0×3.0mm.
- Speaker/charge-pump supply filter: TDK SPM5030T-1R0M-HZ, 1.0uH, Isat 8A typ, Itemp 10.4A typ, DCR 11.5mOhm max.
- Local footprint `A1_PMIC:TDK_SPM5030T_5.2x5.0mm` uses TDK's recommended two-pad land pattern: 1.5×2.2mm pads, 2.7mm gap.
- Crystal: Epson Q13FC13500004, FC-135, 32.768kHz, CL=12.5pF, ±20ppm, 3.2×1.5mm.
- Power key: Omron B3U-1000P, momentary SMD tact switch.
