# A1 eMMC interface rev 0.1
Date 2026-11-16
U9: Samsung KLMBG2JETD-B041, 32GB eMMC 5.1, LCSC C5821038 (stock requires live confirmation).
Samsung datasheet: https://datasheet.lcsc.com/lcsc/2202131900_Samsung-KLMBG2JETD-B041_C2803245.pdf

Power:
- VDDF/VCC flash array: VCC_3V3 (E6 F5 J10 K9).
- VDD/VCCQ interface: VCC_1V8 (C6 M4 N4 P3 P5).
- VDDI internal controller rail: C2 → EMMC_VDDI, 1uF to GND; NEVER connect externally to 3.3V or 1.8V.
- Ground: A6 C4 E7 G5 H10 J5 K8 N2 N5 P4 P6.
- VCCIO2 on RK3568 = 1.8V. FLASH_VOL_SEL must be pulled HIGH to 1.8V before boot; the actual strap resistor must be added to the boot-control page.

Signals:
- CLK M6, CMD M5, DAT0 A3, DAT1 A4, DAT2 A5, DAT3 B2, DAT4 B3, DAT5 B4, DAT6 B5, DAT7 B6, HS400 DataStrobe H5, RSTN K5.
- R31 22Ω serial clock damping, a design candidate; target HS200 first, HS400 only after eye-diagram validation.
- R32 CMD and R33 DAT0 10k pullups to 1.8V; R34 10k RSTN pullup to 1.8V. Confirm actual SoC boot strap and eMMC reset timing.
- Pinout and all 153 candidate pads in A1_EMMC_PINMAP.csv. Unused NC/RFU pins marked no_connect in KiCad; REF and reserved flags require cross-check.

Hard gates:
1. Check full 153-ball package coordinates and TOP vs BALL-SIDE-DOWN orientation using Samsung mechanical drawing. Current footprint dimensions/pad diameters are intentionally preliminary and not production approved.
2. Check eMMC 5.1 VDD(VCCQ) signal levels, HS200 drive strengths, trace impedance/lengths.
3. Check eMMC boot order with SD card and USB maskROM, 32GB device availability, valid SPL/loader.
4. Run KiCad ERC, netlist and PCB DRC; no native KiCad invocation has been executed here.
