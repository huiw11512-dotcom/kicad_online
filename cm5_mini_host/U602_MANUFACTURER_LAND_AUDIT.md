# U602 final vendor pad pattern

Native KiCad before: {'erc': 0, 'hard': 0, 'parity': 0, 'unrouted': 0, 'total': 81, 'u602_mismatch': True}

After: {'erc': 0, 'hard': 0, 'parity': 0, 'unrouted': 0, 'total': 80, 'u602_mismatch': False}

Diodes 74LVC1G07SE-7 SOT353 0.65mm pitch, pad row center separation C1=1.9mm, recommended land 0.60 x 0.42mm. The previous board footprint used 0.65 x 0.40mm, same pad centers. Only U602 land length and width were corrected, with all pad nets/centers, traces, vias and footprints preserved. A project-local CM5IO vendor-specific PCB footprint was exported by pcbnew and referenced by the schematic symbol. KiCad's actual local library check now matches the board. Vendor: https://www.diodes.com/datasheet/download/74LVC1G07.pdf (DS32274 Rev12 page 13); JLC C67531: https://jlcpcb.com/partdetail/DiodesIncorporated-74LVC1G07SE7/C67531 .

Functional LED polarity / assembly should still be tested in hardware; neither ERC nor DRC verifies board boot.
