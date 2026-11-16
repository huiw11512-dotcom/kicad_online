# A1 Production Test / Recovery page Rev1

Native child page 17: `A1_TEST_RECOVERY.kicad_sch`. Two bare-copper pogo arrays are included; no physical connector is fitted.

## TP1701 — power rail array (2x5, 1.27mm pitch)

| Pin | Net | Purpose | Voltage |
|---:|---|---|---|
| 1 | GND | Ground | 0V |
| 2 | PD_15V_IN | USB-C PD input | 15V max |
| 3 | 5V_SYS | Main system rail | 5V |
| 4 | VCC3V3_SYS | Pre-PMIC 3.3V | 3.3V |
| 5 | VCC3V3_PMU | PMU 3.3V | 3.3V |
| 6 | VDD_CPU | Dynamic CPU rail | Variable |
| 7 | VCC_DDR_1V1 | DDR rail | 1.1V |
| 8 | VCC0V6_DDR | DDR rail | 0.6V |
| 9 | VCC1V8_DDR | DDR rail | 1.8V |
| 10 | VCCIO_SD | SD IO rail | 1.8V/3.3V switchable |

## TP1702 — debug / recovery array (2x7, 1.27mm pitch)

| Pin | Net | Purpose |
|---:|---|---|
| 1 | GND | Ground |
| 2 | VCC3V3_PMU | Reference rail |
| 3 | DEBUG_UART2_TX | 3.3V TTL UART2 TX |
| 4 | DEBUG_UART2_RX | 3.3V TTL UART2 RX |
| 5 | PMIC_RESETB_N | PMIC reset |
| 6 | PMIC_PWRON_N | PMIC power-on control |
| 7 | ADC_RECOVERY | Recovery ADC input; probe only |
| 8 | RECOVERY_SW | Recovery switch net; probe only |
| 9 | HDR_I2C1_SDA | MCU_JTAG_TCK mux (GPIO header pin 27) |
| 10 | HDR_GPIO0_C2 | MCU_JTAG_TMS mux (GPIO header pin 33) |
| 11 | HDR_UART0_TX | MCU_JTAG_TDI mux (GPIO header pin 8) |
| 12 | HDR_I2C1_SCL | MCU_JTAG_TDO mux (GPIO header pin 28) |
| 13 | HDR_GPIO0_C3 | MCU_JTAG_TRSTn mux (GPIO header pin 35) |
| 14 | PMIC_INT_N | PMIC interrupt |

**Important:** MCU_JTAG mux functions share existing 40-pin GPIO/I2C1/UART0 nets. Configure the correct RK3568 pinmux before using JTAG; these pads are not the dedicated ARMJTAG CPU debug interface. GPIO header functions on the shared nets are unavailable while JTAG is active. UART2 is 3.3V TTL. ADC_RECOVERY and RECOVERY_SW are probe-only; do not drive them from a fixture. All rail pads are measurement-only; do not inject external voltage. TP1701 pin 2 is 15V.

Footprints `A1_TEST:TP_ARRAY_2X5_P1.27mm` and `A1_TEST:TP_ARRAY_2X7_P1.27mm` use 1.0mm exposed copper pads at 1.27mm pitch with no solder paste. Verify pogo fixture pin alignment and mask registration with the PCB fabricator.
