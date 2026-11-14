# CM5 MiniHost — high-speed carrier development

**Stage:** V0.1 project baseline. The KiCad schematic/PCB in this directory are a sourced open-hardware baseline, **not a newly completed or electrically verified custom PCB**.

## Goal

A genuinely Linux-capable small computer using the **Raspberry Pi Compute Module 5**. Features to retain in our eventual custom revision:

- USB-C external 5 V supply and safe power sequencing
- HDMI display output
- Gigabit Ethernet
- PCIe Gen 2 ×1 to M.2 Key-M NVMe SSD
- USB 2.0 host/user interface (plus Wi-Fi/Bluetooth when the fitted CM5 supports it)
- Boot/service access, status indicators and thermal provisions

Unlike a microcontroller demo, CM5 includes CPU, RAM, and optional eMMC and can run Raspberry Pi OS.

## Origin and licensing

The starting electronic design is **CM5 MINIMA REV3** by Pierluigi Colangeli, source: https://github.com/piecol/CM5_MINIMA_REV3

Source snapshot commit: `6d77314dbbc26c8f5735add30ccb0588816cb71a`.

The original is open hardware under **CERN-OHL-S-2.0**. We retain the upstream license and identify changes in version history. Do not describe the baseline as independently designed or verified in this repository. See `SOURCE_README.md` after import.

## Work so far

1. Selected CM5 for a compact but practical Linux mini-computer.
2. Verified high-speed design guidance against CM5 official documentation.
3. Added a reproducible, attributed KiCad source import and cloud review.
4. **Next engineering work:** validate ERC/DRC, map the power and boot nets, verify M.2/HDMI/Ethernet pin connectivity, design own functional revision, review the mechanical stack, source BOM, and fabricate/test.

## Open in ZiroEDA

https://designer.ziroeda.com/gh/huiw11512-dotcom/kicad_online/tree/main/cm5_mini_host

If the deep link fails, use ZiroEDA → File → Open from GitHub, select `huiw11512-dotcom/kicad_online` → `cm5_mini_host` → `CM5_MINIMA_3.kicad_pro`.

This baseline includes complete routed source files; 3D manufacturer models may be omitted where large. Missing external 3D models do not affect native copper geometry.

## Important

Do **not** order boards based solely on a successful web import. Proper fabrication release requires electrical design review, pin-map and component-footprint verification, stackup and impedance calculation from the board fabricator, complete DRC/ERC closure, Gerber/NC drill and stencil review, and bench bring-up.
