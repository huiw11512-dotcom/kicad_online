# RK3568 A1 minimum boot clock / reset / recovery
Date: 2026-11-16

## 24 MHz clock (RK3568 XIN24M AF28, XOUT24M AF27)
- Y2 4-pin SMD 24MHz crystal, ±20 ppm candidate; final crystal CL and ESR not selected.
- R35 22Ω in series with XOUT24M, mandatory Rockchip recommendation.
- R36 1MΩ between XIN24M and crystal-side XOUT24M, mandatory Rockchip recommendation.
- C75/C76 18pF C0G 0402 to ground. Rockchip gives these as values for *its chosen crystal*, not universal; must match final Y2 CL and stray capacitance.
- Crystal pins 2/4 grounded. Keep crystal close to RK3568, away from switching power.
- Technical reference: Rockchip RK3568 Hardware Design Guide Rev1.2 §2.1.1.

## Reset and boot voltage
- RK3568 nPOR ball AH27 is globally named PMIC_RESETB_N, connecting to RK809-5 open-drain reset output.
- RK3568 FLASH_VOL_SEL ball AG25 10k pullup to VCC3V3_PMU (R37): VCCIO2/eMMC interface uses 1.8V.
- RX/TX debug UART2 M0 on AH24/AC20 to 3pin connector J2; ensure correct 3.3V TTL IO level from PMUIO (never RS232 level).
- Recovery: SARADC_VIN0 ball B27 is ADC_RECOVERY, 10k pullup to VCCA_1V8, 100R input series and SW2 momentary to GND. Check DTS key ladder and ADC thresholds in U-Boot.
- USB OTG service/download connector is not yet drawn; debug UART and recovery key alone do not complete flashing path.

## Fabrication gates
- Select real 24MHz crystal with 4-pin matching footprint. Adjust two capacitors per measured board/CL and Rockchip design requirement.
- Confirm recovery key input and reset release timing against Rockchip EVB schematic.
- Native KiCad ERC and PCB signal-integrity validation have not been run.


## 2026-11-16 strap IO correction
R37 FLASH_VOL_SEL logic-high strap was corrected from VCC_1V8 to VCC3V3_PMU. The strap GPIO0_A7 is in 3.3V PMUIO; the selected VCCIO2 for eMMC remains 1.8V. Do not confuse strap logic-high supply with eMMC VCCQ voltage. Confirm with Rockchip package IO-domain checklist and board power-on sequencing.
