# U602 LED_nPWR buffer supply correction

U602 (Diodes 74LVC1G07SE-7, LCSC C67531) now uses CM5_3.3V (+3V3_PI) on VCC pin 5 instead of +5V. The CM5 datasheet identifies LED_nPWR as a 3.3 V active-low output that requires buffering. At VCC=3.0–3.6 V, the 74LVC1G07 VIH requirement is 2.0 V, providing guaranteed compatibility with the CM5 3.3 V signal. Its open-drain output is rated for 0–5.5 V operation, so the existing 5 V LED pull-up through R605=2.2 kΩ is retained. The LED branch current is approximately 1.3 mA assuming a 2.0 V LED drop and 0.1 V low-level output. CM5_3.3V is available from CM5 pins 84/86; U602 supply current is negligible relative to the 600 mA module rail budget.

No PCB pad, track, footprint, or LED resistor geometry is changed. Validate the LED behavior during first prototype bring-up.
