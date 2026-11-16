# A1 HDMI schematic audit - 2026-11-16

Status: native KiCad A1_HDMI_TX.kicad_sch linked as page 13, **not yet ERC-validated or fabrication released**.

- J201: Type-D Micro-HDMI connector; Molex 46765 family, footprint candidate.
- R201..R208: 2.2-ohm series on eight native RK3568 TX PHY TMDS lines.
- U201/U202: ESD5344D four-line clamps; must verify ESD parasitic capacitance <0.4pF for TMDS and mechanical proximity to connector.
- R209: HDMI_TX_REXT=1.62k-ohm ±1% to GND.
- HPD: R210 1k series, R211 100k pulldown, C201 100nF debounce.
- Q201 + R212: CEC MOS isolation with 27k-ohm low-side pullup.
- Q202/Q203 and R213..R216: 2SK3018 bidirectional DDC open-drain translators 3.3V/5V.
- D201 + C202: anti-backfeed Schottky, connector-side 1uF.
- C203..C208: 4.7uF+100nF at HDMI PHY supply balls, using previously corrected VDDA0V9_IMAGE and VCCA1V8_IMAGE.

**Open blockers**
1. D201 drop may violate HDMI +5V minimum 4.8V at connector; verify under full sink loading and 5V_SYS tolerance, or revise with a qualified reverse-blocking low-loss solution.
2. Confirm Type-D 19-pin shield pad and footprint mapping against the exact connector orderable MPN; check ESD TVS datasheet and CEC/DDC circuit against EVB.
3. HDMI controlled impedance 100-ohm differential, return paths, pair spacing, crosstalk and mechanical are not PCB-reviewed.
4. PMIC enable/register programming for RK809 LDO1=0.9V/LDO9=1.8V remains unverified.
5. Native KiCad load/ERC/netlist export/visual review/DRC have **not** been run.

Primary reference: https://dl.xkwy2018.com/downloads/RK3568/RK356X/Hardware/Rockchip_RK3568_Hardware_Design_Guide_V1.2_EN.pdf
