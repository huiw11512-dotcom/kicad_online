#!/usr/bin/env python3
"""Align KiCad six-layer mechanical stackup to JLC06161H-3313 1.6-mm nominal build."""
from pathlib import Path
import re
root=Path("cm5_mini_host")
p=root/"CM5_MINIMA_3.kicad_pcb"
s=p.read_text(encoding="utf-8")
m=re.search(r'\(\s*stackup\s*\n([\s\S]*?)\n\t\t\)',s)
if not m:raise SystemExit("KiCad board setup stackup not found")
stack=m.group(0)
def set_layer(n,thickness,material,epsilon):
    global stack
    pat=r'(\(layer "dielectric '+str(n)+r'"\s*\n)([\s\S]*?)(\n\t\t\t\))'
    hits=list(re.finditer(pat,stack))
    if len(hits)!=1:raise SystemExit(f"Expected one dielectric {n}, found {len(hits)}")
    h=hits[0]; body=h.group(2)
    body,nt=re.subn(r'(\(thickness\s+)([\d.]+)(\))',lambda m:m.group(1)+str(thickness)+m.group(3),body,count=1)
    body,nm=re.subn(r'(\(material\s+")([^"]+)("\))',lambda m:m.group(1)+material+m.group(3),body,count=1)
    body,ne=re.subn(r'(\(epsilon_r\s+)([\d.]+)(\))',lambda m:m.group(1)+str(epsilon)+m.group(3),body,count=1)
    if (nt,nm,ne)!=(1,1,1):raise SystemExit(f"Incomplete dielectric {n} fields: thickness={nt} material={nm} er={ne}")
    stack=stack[:h.start()]+h.group(1)+body+h.group(3)+stack[h.end():]
set_layer(1,0.0994,"3313",4.1)
set_layer(2,0.55,"Core",4.6)
set_layer(3,0.1088,"2116",4.16)
set_layer(4,0.55,"Core",4.6)
set_layer(5,0.0994,"3313",4.1)
s=s[:m.start()]+stack+s[m.end():]
old='(thickness 1.5296)'
old='(thickness 1.5584)'
if s.count(old)!=1:raise SystemExit("Previous provisional 1.5584mm thickness missing or altered")
s=s.replace(old,'(thickness 1.6)',1)
p.write_text(s,encoding="utf-8")
(root/"JLC06161H_3313_STACKUP_REV_B.md").write_text(
    "# Rev.B proposed fabrication stackup\n\n"
    "Factory: JLCPCB. Nominal finished board thickness **1.6 mm**, 6 copper layers; "
    "manufacturer reference **JLC06161H-3313** (1 oz finished external copper, 0.5 oz internal copper). "
    "KiCad calculated dielectric/mask/copper sum is 1.5584 mm, a pressed-up nominal value before manufacturing tolerance. "
    "Outer L1-L2 and L5-L6 prepreg 3313, 0.0994 mm each, dielectric estimate 4.1; "
    "L2-L3 and L4-L5 cores 0.55 mm NP-155F each, dielectric estimate 4.6; "
    "L3-L4 prepreg 2116, 0.1088 mm, dielectric estimate 4.16. "
    "External copper 0.035 mm, internal copper 0.0152 mm each, soldermask 0.01 mm each. "
    "Stackup values are from the JLCPCB published impedance stackup family, not a factory-approved controlled-impedance order. "
    "Do not mark the high-speed 90/100 ohm routing as compliant until manufacturer DFM/impedance analysis accepts the actual line widths, spacings and via/pad launches.\n\n"
    "Reference: https://jlcpcb.com/impedance\n",encoding="utf-8")
print("Updated KiCad stackup to JLCPCB published JLC06161H-3313; nominal finished thickness 1.6mm.")
