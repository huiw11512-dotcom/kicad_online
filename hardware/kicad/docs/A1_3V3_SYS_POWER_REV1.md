# Pre-PMIC VCC3V3_SYS buck — A1 Rev1

Date: 2026-11-15  
Status: schematic and BOM committed; not a fabrication release.

## 1. Function

Generate the pre-PMIC 3.3V system rail from 5V_SYS. This is the input supply for RK809-5 pins VCC1–VCC9 and VCC_RTC. It is a different net from the RK809 downstream SWOUT1 rail VCC_3V3.

## 2. Selected topology

- U6: TI TPS62132RGTT, fixed 3.3V, 3A synchronous buck, 3V–17V input, 2.5MHz.
- L8: APV ANR5040T2R2M, 2.2uH, 4.3A heat-rating current, 5.6A saturation current, 5×5mm.
- CIN: C52 10uF/25V X5R 0805 plus C53 100nF/16V X7R 0603.
- COUT: C54+C55, each 22uF/10V X7R 1206, in parallel.
- Soft start: C56 3.3nF from SS/TR to GND.
- EN is tied to 5V_SYS.
- DEF=GND selects nominal fixed 3.3V; FSW=GND selects 2.5MHz.
- On the fixed-output TPS62132, FB is connected to AGND as recommended by TI. AGND, PGND and exposed pad 17 join the GND plane.
- PG is unused and marked NC.

## 3. Component sourcing

All six BOM lines have an LCSC part number:
- U6 TPS62132RGTT — C2070674.
- L8 APV ANR5040T2R2M — C7427127.
- C52 Samsung CL21A106KAYNNNE — C15850.
- C53 Yageo CC0603KRX7R7BB104 — C108079.
- C54/C55 CCTC TCC1206X7R226M100HT — C7393991.
- C56 Yageo CC0603KRX7R9BB332 — C107088.

The APV ANR5040 land pattern follows the manufacturer drawing: two 2.3×1.4mm pads with 4.2mm center spacing. The custom footprint is A1_POWER:APV_ANR5040_5x5mm.

## 4. Electrical checks

- 5V_SYS is within TPS62132's 3V–17V operating range.
- The 3A rating is the converter's maximum capability, not a guarantee of 3A at any board temperature. Verify IC junction temperature and inductor temperature rise on the actual 6-layer PCB.
- C54/C55 must retain at least the datasheet-required effective output capacitance after DC-bias derating at 3.3V. Check the selected CCTC datasheet curve; increase capacitance or package size if required.
- Confirm input/output ripple, startup overshoot, load-step response and current-limit behavior at 0A, nominal PMIC load and 3A.
- Keep PVIN/AVIN bypass capacitors close to the IC; minimize the SW–L8–COUT hot loop. Connect the exposed pad to GND with thermal vias and solid copper.
- The schematic page is logically connected with global labels. Native KiCad load/ERC/netlist export has not yet been run in this environment.

## 5. References

- TI TPS6213x datasheet, Figure 9-44 (3.3V/3A power supply): https://www.ti.com/lit/ds/symlink/tps62132.pdf
- APV ANR Series datasheet, ANR5040 dimensions/land pattern and current table: https://datasheet.lcsc.com/lcsc/2309201138_APV-ANR3012T330M_C6364785.pdf
- LCSC U6: https://www.lcsc.com/product-detail/C2070674.html
- LCSC L8: https://www.lcsc.com/product-detail/C7427127.html
