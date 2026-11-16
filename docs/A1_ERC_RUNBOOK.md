# Running native KiCad ERC for Linux MiniHost A1

The GitHub Actions workflow `.github/workflows/a1-native-kicad-erc.yml` installs KiCad 9 on Ubuntu 24.04 and attempts schematic netlist export and native ERC. Generated netlist, ERC JSON, terminal logs and exit codes are uploaded as `A1-KiCad9-ERC` (when workflow is permitted to execute).

The workflow being present **does not establish that ERC has run or passed**. Review the actual GitHub Actions run, logs and ERC JSON before treating any schematic as validated.

To reproduce on a local KiCad 9 installation:

```sh
cd hardware/kicad
kicad-cli sch export netlist --output A1.net A1.kicad_sch
kicad-cli sch erc --format json --output A1-erc.json --exit-code-violations A1.kicad_sch
```

Do not waive global net mismatches, duplicate pin positions or missing footprints without inspecting the schematic and BOM. PCB design is not begun. RTL8211F Ethernet MagJack footprint, AP6256 candidate footprint, DDR template/BIN, RK809 power sequencing and HDMI 5V requirement are hard gates.
