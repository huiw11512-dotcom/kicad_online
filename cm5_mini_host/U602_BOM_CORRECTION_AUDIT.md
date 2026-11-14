# U602 logic/BOM mismatch correction

ERC/hard-DRC/parity/unconnected/total: (0, 2, 0, 0, 85) → (0, 2, 0, 0, 85)

U602 revised from incorrectly assigned UMW SN74LVC1G14DBVR Schmitt-trigger inverter (SOT-23 DBV) to Diodes Incorporated 74LVC1G07SE-7 (JLCPCB/LCSC C67531) **non-inverting open-drain buffer**. Pin 2 is nPWR_LED and pin 4 sinks the D605/R605 5V indicator branch; an open-drain buffer matches the original symbolic intended function. The preexisting 5-pin SC70/SOT-353 PCB footprint's pad geometry, nets, vias and tracks were NOT changed. **The exact Diodes SOT353 recommended land pattern and first power-on LED logic still require physical review before production.**

Source schematic: IO.kicad_sch; prior root analysis U602_COMPONENT_MISMATCH_REVIEW.md; Diodes datasheet: https://www.diodes.com/datasheet/download/74LVC1G07.pdf ; JLC supplier part: https://jlcpcb.com/partdetail/DiodesIncorporated-74LVC1G07SE7/C67531 .
