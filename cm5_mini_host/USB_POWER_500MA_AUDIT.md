# Default-current USB2 host power variant

**Implementation:** R702=R703=56kΩ from +5V to CC1/CC2 (USB Type-C source advertises default USB current, i.e. 500mA for the USB2 interface); R701=39kΩ from AP22653 ILIM to GND.

Estimated AP22653 current-limit min/typ/max at 39k (Diodes best-fit equation): 0.564/0.636/0.710 A, excluding external resistor tolerance.

KiCad ERC/hard DRC/footprint parity/unrouted: (0, 4, 0, 0) -> (0, 4, 0, 0).

**Design allocation:** 5V/500mA at the USB-C host port = 2.5W. This allocation is not an assurance of CM5 and SSD peak load. Full-system power and thermals still require measurement.

**Caveat:** a fixed Rp pair is not a complete USB-C source-controller implementation; review attach/detach, VBUS_EN timing and inrush against source requirements. AP22653 limit is protective, not a guarantee of available power.

Datasheets: https://www.diodes.com/datasheet/download/AP3441.pdf , https://www.diodes.com/part/view/AP22653 ; CC Rp reference https://www.st.com/resource/en/technical_article/ta0357-overview-of-usb-typec-and-power-delivery-technologies-stmicroelectronics.pdf .
