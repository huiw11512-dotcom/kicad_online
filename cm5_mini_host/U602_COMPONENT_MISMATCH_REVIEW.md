# Manufacturing blocker: U602 **symbol / function / package** conflict

**Reviewed 2026-11-14. Status: HIGH PRIORITY — do not fabricate or assemble until resolved.**

This problem was found by comparing the actual `cm5_mini_host/IO.kicad_sch` instance, the PCB footprint-library mismatch analysis, and manufacturer datasheets. A **zero-error ERC is not sufficient** to detect a part with the right pin numbers but wrong logic and package.

## Three incompatible data points in the actual source

| Field | Actual reference design | Implication |
| --- | --- | --- |
| U602 value / P/N | `SN74LVC1G14DBVR` | UMW C434069 (as linked in project), a **Schmitt-trigger inverter**, **SOT-23-5 (DBV)** |
| Schematic library symbol | `CM4IO:74LVC1G07_copy` | Symbol describes an **open-drain non-inverting buffer**, output pin 4 electrical type `open_collector`, opposite function/output stage to SN74LVC1G14 |
| PCB and schematic footprint ID | `Package_TO_SOT_SMD:SOT-353_SC-70-5` | **SC-70-5 / DCK**, physically smaller than SOT-23-5 / DBV; current board pad footprint 0.65×0.40 mm with 0.95 mm pad X center; stock KiCad 10 DCK pad 1.025×0.35 mm center x≈0.8375 mm. Neither equals a confirmed SOT-23 DBV land pattern |

Primary part source: [JLCPCB part C434069](https://jlcpcb.com/partdetail/SN74LVC1G14DBVR/C434069), explicitly UMW/Youtai and SOT-23-5 inverter.
Datasheets: [UMW SN74LVC1G14](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/5338/SN74LVC1G14.pdf); [TI SN74LVC1G14 DBV vs DCK](https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf); [TI SN74LVC1G07 (open-drain buffer)](https://www.ti.com/product/SN74LVC1G07).

## Input/output nets

U602 pin 2 is connected to hierarchical signal `nPWR_LED` in `IO.kicad_sch`; pin 4 drives the downstream indicator circuit (trace goes toward x=88.90 mm on the schematic). The inverter-versus-noninverting decision must be made against intended active-low LED behavior and pull-up/LED resistor wiring. Do not choose merely by the old symbol name or because ERC passes.

**Common physical pin map:** both listed 5-pin devices use 1 NC, 2 A, 3 GND, 4 Y, 5 VCC (confirm exact chosen manufacturer). Therefore an electrical netlist can still look correct even when function and land pattern are wrong.

## Required design decision before PCB modification

**Option A — keep UMW C434069 / SN74LVC1G14DBVR:** First verify that inverting, push-pull Schmitt output is the desired response to `nPWR_LED`. Replace the cached buffer symbol with electrically correct inverter symbol and change U602 to datasheet-confirmed **SOT-23-5 (DBV)** land pattern; reroute all five affected pads and check copper clearances, silkscreen and polarity. Full KiCad ERC/DRC and circuit-level function review must pass.

**Option B — preserve non-inverting open-drain function:** Change the BOM to a genuine `SN74LVC1G07`-type open-drain buffer whose package variant matches a *validated* footprint; recheck whether the LED needs a pull-up or whether the output is already correctly current-limited. A DCKR variant can be SC-70 but requires verifying the existing pad arrangement against its exact datasheet. Do **not** simply change the component name and call it fixed.

**Decision NOT made:** Which function is intended has not yet been electrically confirmed; this report is not a manufacturing release and does not authorize either option. U602 currently remains UNCHANGED in the PCB to avoid silently reversing the indicator function or creating an unmanufacturable SOT-23 mismatch.

## Other eight-footprint audit findings

See [EIGHT_FOOTPRINT_PAD_DELTA.md](EIGHT_FOOTPRINT_PAD_DELTA.md):
- U703: 4 pads have same XY and size, but KiCad pad shape definition differs.
- C702: slight tantalum land pattern dimensional adjustment vs stock library; verify Kemet variant.
- U1: **LIS3DH accelerometer**, board local Y vs library is mirrored due bottom-layer placement/coordinate frame; do not interpret as literal 2 mm mechanical relocation without transformed-coordinate comparison and pin-1 orientation.
- J701 M.2: board 71 pads vs 73 library, extra `M1/M2` are alternate SSD board mounting holes rather than M.2 contact pads. Already has separate mounting holes. Validate actual SSD standoff pattern.
- Module301 CM5: two board NPTH drills vs four in project-local library; the extracted coordinate frames also reflect mirroring and must be normalized before interpreting signal pad positions.
- R702/R703: a first raw geometry comparison labeled mismatch, but rounded five-decimal actual XY/size comparison finds no numerical difference; treat as an **audit-method precision question**, not evidence of bad copper pads.

## Release gates

- [ ] Select one U602 electrical function (inverting Schmitt vs non-inverting open-drain) after pin-level LED circuitry review.
- [ ] Lock manufacturer part number and correct 5-pin land pattern with actual datasheet, then modify PCB or BOM.
- [ ] Review actual U1 LIS3DH accelerometer bottom-side orientation and pin 1.
- [ ] Close remaining 2 hard RJ45 copper-edge clearance violations with validated official cutout and shield land dimensions.
- [ ] Confirm factory six-layer impedance/mask/copper process and full enclosure cooling and CM5 mounting design.

**Conclusion:** The project is editable and DRC has improved, but U602 is an additional *functional/manufacturing block* that DRC cannot flag; the release remains blocked even if the remaining two geometry errors are resolved.
