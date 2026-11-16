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


## Per-sheet netlist diagnosis

The workflow now exports the assembled root netlist and a separate standalone netlist for every `A1_*.kicad_sch` child page. Review `per-sheet-summary.csv` and `per-sheet/exit-codes.csv` in the latest artifact:

- If a child page's standalone netlist contains its components but the root netlist does not, investigate the parent sheet UUID, project instance path, page references and duplicate UUIDs.
- If a standalone page netlist is also empty, inspect that page's placed-symbol instances, library cache, reference/unit fields and `in_bom/on_board` flags.
- A successful export command does not imply complete connectivity. Compare component references and named nets against the schematic/BOM, then resolve ERC violations.

The GPIO page's duplicate UUID namespace was repaired in commit `91a2334`; the page's 3.3V pinmux and external 5V protection remain open design gates. Page 17 adds measurement-only pogo arrays; it is not a populated connector.
