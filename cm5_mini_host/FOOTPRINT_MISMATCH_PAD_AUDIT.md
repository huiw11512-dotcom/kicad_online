# KiCad 10 footprint-library mismatch pad audit

Source: current cm5_mini_host KiCad 10 DRC (50 lib_footprint_mismatch warnings).

**This is a comparative audit, not an instruction to replace footprints.**
The audit checks native KiCad 10 pad numbers, local positions, pad shapes/sizes, drill and pad-level mask/paste margins where the API allows it. A visual 3D enclosure and mechanical manufacturer drawing check is still mandatory.

## Classifications

- **NON_PAD_VERSION_OR_GRAPHICS**: 42
- **PAD_GEOMETRY**: 6
- **PAD_NUMBER_OR_COUNT**: 2

## Per-footprint differences

| Ref | Class | Embedded footprint ID | Pads board/lib | Finding |
|---|---|---|---|---|
| U405 | NON_PAD_VERSION_OR_GRAPHICS | Package_TO_SOT_SMD:SOT-23-5 | 5/5 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R704 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| J502 | NON_PAD_VERSION_OR_GRAPHICS | Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.00mm_Vertical | 6/6 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C705 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R606 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C708 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C502 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| U701 | NON_PAD_VERSION_OR_GRAPHICS | Package_TO_SOT_SMD:SOT-23-6 | 6/6 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R101 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R402 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R401 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| L701 | NON_PAD_VERSION_OR_GRAPHICS | Inductor_SMD:L_Coilcraft_XAL5030-XXX | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| U703 | PAD_GEOMETRY | Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm | 4/4 | Pad attr, XY, size, shape or drill differs in 4 sorted entries |
| C704 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R707 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C709 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C701 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R706 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| J601 | NON_PAD_VERSION_OR_GRAPHICS | Connector_JST:JST_SH_BM04B-SRSS-TB_1x04-1MP_P1.00mm_Vertical | 6/6 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C703 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| U602 | PAD_GEOMETRY | Package_TO_SOT_SMD:SOT-353_SC-70-5 | 5/5 | Pad attr, XY, size, shape or drill differs in 5 sorted entries |
| J503 | NON_PAD_VERSION_OR_GRAPHICS | Connector_JST:JST_SUR_BM10B-SURS-TF_1x10-1MP_P0.80mm_Vertical | 12/12 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C401 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C702 | PAD_GEOMETRY | Capacitor_Tantalum_SMD:CP_EIA-3528-21_Kemet-B | 2/2 | Pad attr, XY, size, shape or drill differs in 2 sorted entries |
| R702 | PAD_GEOMETRY | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad attr, XY, size, shape or drill differs in 2 sorted entries |
| R705 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R501 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| J701 | PAD_NUMBER_OR_COUNT | CM5IO:M.2 M Key socket_2230_2242 | 71/73 | PCB 71 pads vs library 73 pads |
| C711 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C712 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C501 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C710 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R701 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C706 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C102 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C101 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C601 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0805_2012Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R703 | PAD_GEOMETRY | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad attr, XY, size, shape or drill differs in 2 sorted entries |
| C707 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R502 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R605 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| Module301 | PAD_NUMBER_OR_COUNT | CM5IO:Raspberry-Pi-5-Compute-Module_GPIO | 102/104 | PCB 102 pads vs library 104 pads |
| R103 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R108 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R102 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| U1 | PAD_GEOMETRY | Package_LGA:LGA-16_3x3mm_P0.5mm_LayoutBorder3x5y | 16/16 | Pad attr, XY, size, shape or drill differs in 14 sorted entries |
| R403 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R107 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| C503 | NON_PAD_VERSION_OR_GRAPHICS | Capacitor_SMD:C_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |
| R104 | NON_PAD_VERSION_OR_GRAPHICS | Resistor_SMD:R_0402_1005Metric | 2/2 | Pad number/shape/local XY/size/drill + local mask/paste matching; compare silk, fab/courtyard, 3D, metadata |

## DFM interpretation

- PAD_NUMBER_OR_COUNT / PAD_GEOMETRY are high priority; confirm datasheet pinout and exact purchased reel before any PCB order.
- MASK_PASTE_MARGIN differences require manufacturing process signoff; do not copy stock values blindly, especially J701 0.16mm mask dam.
- NON_PAD_VERSION_OR_GRAPHICS does **not** mean safe: may still change 3D envelope, courtyard, polarity mark or exposed copper wording; review the vendor's mechanical drawing.
- This report did not modify any design files, PCB copper or circuit values.
