# KiCad 10 footprint-library mismatch pad audit

Source: current cm5_mini_host KiCad 10 DRC (50 lib_footprint_mismatch warnings).

**This is a comparative audit, not an instruction to replace footprints.**
The audit checks native KiCad 10 pad numbers, local positions, pad shapes/sizes, drill and pad-level mask/paste margins where the API allows it. A visual 3D enclosure and mechanical manufacturer drawing check is still mandatory.

## Classifications

- **LIBRARY_LOAD_ERROR**: 50

## Per-footprint differences

| Ref | Class | Embedded footprint ID | Pads board/lib | Finding |
|---|---|---|---|---|
| U405 | LIBRARY_LOAD_ERROR | Package_TO_SOT_SMD:SOT-23-5 |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R704 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| J502 | LIBRARY_LOAD_ERROR | Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.00mm_Vertical |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C705 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R606 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C708 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C502 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| U701 | LIBRARY_LOAD_ERROR | Package_TO_SOT_SMD:SOT-23-6 |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R101 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R402 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R401 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| L701 | LIBRARY_LOAD_ERROR | Inductor_SMD:L_Coilcraft_XAL5030-XXX |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| U703 | LIBRARY_LOAD_ERROR | Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C704 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R707 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C709 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C701 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R706 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| J601 | LIBRARY_LOAD_ERROR | Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.00mm_Vertical |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C703 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| U602 | LIBRARY_LOAD_ERROR | Package_TO_SOT_SMD:SOT-353_SC-70-5 |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| J503 | LIBRARY_LOAD_ERROR | Connector_JST:JST_SUR_BM10B-SURS-TF_1x10-1MP_P0.80mm_Vertical |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C401 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C702 | LIBRARY_LOAD_ERROR | Capacitor_Tantalum_SMD:CP_EIA-3528-21_Kemet-B |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R702 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R705 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R501 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| J701 | LIBRARY_LOAD_ERROR | CM5IO:M.2 M Key socket_2230_2242 |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C711 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C712 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C501 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C710 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R701 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C706 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C102 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C101 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C601 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0805_2012Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R703 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C707 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R502 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R605 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| Module301 | LIBRARY_LOAD_ERROR | CM5IO:Raspberry-Pi-5-Compute-Module_GPIO |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R103 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R108 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R102 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| U1 | LIBRARY_LOAD_ERROR | Package_LGA:LGA-16_3x3mm_P0.5mm_LayoutBorder3x5y |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R403 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R107 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| C503 | LIBRARY_LOAD_ERROR | Capacitor_SMD:C_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |
| R104 | LIBRARY_LOAD_ERROR | Resistor_SMD:R_0402_1005Metric |  | TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType' |

## DFM interpretation

- PAD_NUMBER_OR_COUNT / PAD_GEOMETRY are high priority; confirm datasheet pinout and exact purchased reel before any PCB order.
- MASK_PASTE_MARGIN differences require manufacturing process signoff; do not copy stock values blindly, especially J701 0.16mm mask dam.
- NON_PAD_VERSION_OR_GRAPHICS does **not** mean safe: may still change 3D envelope, courtyard, polarity mark or exposed copper wording; review the vendor's mechanical drawing.
- This report did not modify any design files, PCB copper or circuit values.
