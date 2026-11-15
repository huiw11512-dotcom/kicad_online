# A1 CPU dynamic Buck — TCS4525_WT (initial schematic)
Date: 2026-11-16
## Function
U8 TCS4525_WT provides RK3568 VDD_CPU through a 0.47uH 3MHz Buck stage, input 5V_SYS, output target 1.025V at boot (VSEL=0, defaults); I2C dynamic voltage scaling supported.
Datasheet: https://atta.szlcsc.com/upload/public/pdf/source/20250224/61B4304C265F1C8D7235B80D248DF251.pdf
Reference schematic: Radxa ROCK3A V1.3 Power_CPU_RTC, page 31.

## Pin mapping (manufacturer 5x4 top view)
- A1 VSEL → CPU_BUCK_VSEL
- A2 EN → CPU_BUCK_EN
- A3 SCL → PMIC_I2C1_SCL
- A4 FB → VDD_CPU_REMOTE_SENSE
- B1 SDA → PMIC_I2C1_SDA
- B2 PGND → GND
- B3 PGND_PG → GND
- B4 AGND → GND
- C1 PGND → GND
- C2 PGND → GND
- C3 PGND → GND
- C4 PGND → GND
- D1 AVIN → 5V_SYS
- D2 PVIN → 5V_SYS
- D3 SW → CPU_SW
- D4 SW → CPU_SW
- E1 PVIN → 5V_SYS
- E2 PVIN → 5V_SYS
- E3 SW → CPU_SW
- E4 SW → CPU_SW

The TCS4525 datasheet explicitly says A4 is **FB** (not VOUT). B3 is an optional open-drain PG output; grounded if unused. The remote sense is connected to RK3568 VDD_CPU_COM through the VDD_CPU_REMOTE_SENSE net, not shorted to GND. R20=100k between VDD_CPU and remote-sense net gives a fail-safe bias path; actual recommended remote-sense resistor must be confirmed against the chosen Rockchip design revision.

## Hardware
- Input: two 22uF/10V bulk caps and one 100nF/10V high-frequency bypass cap.
- L9: TDK SPM5030T-R47M-HZ, 0.47uH. Manufacturer datasheet selection and board-thermal check required.
- Output: four 22uF/6.3V caps and one 100nF/10V cap. Verify effective capacitance at 1V and ripple/thermal.
- EN: CPU_BUCK_EN from RK809-5 EXT_EN.
- VSEL: R21 100k to GND, boots default ~1.025V until I2C config; verifies if 1.025V within SOC startup recommendations.
- I2C: common I2C0 PMIC bus (PMIC_I2C1_SCL/SDA), regulator nominal address 0x1c.
- Package: WCSP-20, 2.0×1.6mm, 0.4mm pitch. **The preliminary 0.23mm solder land is NOT manufacturing-verified**.
- The main 5V_SYS converter has a 5A output rating: CPU dynamic load + all other board loads must remain within 5V input power budget.

## Gates before fabrication
1. Confirm exact ordering code (TCS4525_WT) and lead-free WCSP ball land / paste pattern with assembly house.
2. Confirm CPU startup enable timing relative to RK809 RESETB, BUCK1/2/3/5, DDR and external PHY.
3. Confirm all 20 symbol-to-pad ball positions with manufacturer datasheet.
4. Perform native KiCad ERC + PCB DRC (not run in this environment).
