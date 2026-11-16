# A1 root netlist component coverage diagnosis — 2026-11-16

## Current observation

The KiCad 9 root export for the 17-page project produced 99 component records. The parsed records currently belong to the root sheet and the Ethernet, Wi-Fi/BT, GPIO and production-test pages. The root export does not currently show components from the RK809, DDR power, 3V3 power, RK3568 SoC, CPU power, eMMC, boot/debug, LPDDR4X, SD card, USB ports, USB2 HOST2/HOST3 or HDMI pages.

This is an observed discrepancy, not yet a proven cause.

## Important correction to earlier diagnostic

A child sheet such as `A1_RK809_PMIC.kicad_sch` is not a standalone root schematic. Running `kicad-cli sch export netlist` directly against a child file returns `Failed to load schematic`; that is expected for a hierarchical child and does **not** establish that the child page is malformed.

The workflow now exports only from `A1.kicad_sch` and archives:
- `A1.net` — hierarchical root netlist
- `A1-BOM.csv` — root BOM
- `A1-Schematic.pdf` — all 17 sheets
- `A1-erc.json` — native ERC report
- `netlist-bom-summary.txt` — component count comparison

## Next investigation

1. Compare root BOM row count and component references with the root netlist component records.
2. If BOM also omits the legacy sheets, inspect child sheet references, component annotation instances, library resolution and project load.
3. If BOM includes those components but netlist does not, inspect the placed-symbol electrical pin data and netlist connectivity.
4. Inspect the exported full PDF to confirm all child sheets load and render.
5. Do not change electrical designators or sheet UUIDs speculatively. Use the artifact evidence first.

## Related integrity fix

GPIO page 16 UUID collisions were repaired in commit `91a2334`; the production-test page 17 was added in the same change set. The current branch includes both changes after restoration on the latest baseline.
