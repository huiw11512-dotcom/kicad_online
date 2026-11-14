# MiniHost engineering specification — draft v0.1

## Functional target

* Compute: Raspberry Pi CM5 with **4–8 GB RAM** and optional onboard eMMC. A Lite CM5 needs an alternate validated boot medium.
* Storage: PCIe Gen 2 x1 NVMe through M.2 Key-M connector, with board-side 3.3 V and correct reset / request signaling.
* Display: one HDMI 2.0 output (interface requirements and HPD/DDC/ESD are mandatory).
* Network: one 1000BASE-T RJ45 with isolation magnetics and ESD.
* External IO: USB 2.0 host interface for basic keyboard/mouse plus optional CM5 wireless.
* Power: external regulated 5 V supply; design for 5 A capability or explicitly constrain the peripheral budget. No mains on the PCB.
* Mechanical: target below 70 × 70 mm; six-layer controlled impedance stackup; CM5 socket and cooling keep-outs per manufacturer.
* Clock/signaling: based on CM5 official electrical interfaces, not arbitrary GPIO mappings.

## Six-layer routing intent (verify against actual board stackup)

1. L1 Top: components and controlled-impedance high-speed microstrips.
2. L2: continuous GND reference.
3. L3: local signal/power.
4. L4: power distribution, split carefully without crossing high-speed reference paths.
5. L5: continuous GND reference.
6. L6 Bottom: limited high-speed with adjacent L5 GND, power/low-speed as needed.

The actual inherited board stackup and fabrication data take precedence until the revision is formally updated.

## Interface constraints from CM5 documentation

| Interface | Target differential impedance | P/N intra-pair tolerance | Notes |
|---|---:|---:|---|
| PCIe Gen 2 | 90 Ω | ideally ≤0.10 mm | Keep PCIe CLK_REQ and RST correct; AC-couple external PCIe RX as specified |
| USB 3 (if added) | 90 Ω | ideally ≤0.10 mm | Do not use this row to claim USB 3 ports are on the current reference |
| USB 2 | 90 Ω | ideally ≤0.15 mm | Do not swap D+/D− |
| HDMI | 100 Ω | aim ≤0.15 mm | Board-to-board mismatch managed per CM5 datasheet; preserve return path |

**Widths and gaps are not fixed at this stage**. They require the chosen laminate, copper weight, trace-to-reference thickness and fab impedance coupon data. Via stubs, ESD return paths, connector insertion loss, common-mode choke choices and launch quality must be reviewed.

## Verification gates

- [ ] KiCad parses all hierarchical schematic sheets.
- [ ] ERC 0 errors after engineering review (warnings individually waived or fixed).
- [ ] DRC 0 errors after board zone refill, netclass/clearance review.
- [ ] Pair maps: CM5→SSD; CM5→HDMI; CM5→RJ45; USB host.
- [ ] Power map: CM5 5 V input, NVMe 3.3 V transient budget, PD startup and USB VBUS switches.
- [ ] CM5 socket footprint exact approved manufacturer connector/housing height.
- [ ] Impedance check by fabricator; P/N length report checked for all routed pairs.
- [ ] PCB mechanical and assembly verification, then prototype bring-up.

## Reference source

* CM5 official documentation: https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008180-DS-7-cm5-datasheet.pdf
* Official IO board KiCad: https://pip.raspberrypi.com/categories/1098-design-files
* Derived open-hardware baseline: https://github.com/piecol/CM5_MINIMA_REV3

This specification is an original project planning document; it does not certify the baseline design for manufacturing.
