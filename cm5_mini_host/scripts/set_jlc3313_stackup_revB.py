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
old='(thickness 1.5584)'
if s.count(old)!=1:raise SystemExit("Previous provisional 1.5584mm thickness missing or altered")
s=s.replace(old,'(thickness 1.6)',1)
p.write_text(s,encoding="utf-8")
(root/"JLC06161H_3313_STACKUP_REV_B.md").write_text(
    "# Rev.B proposed fabrication stackup\n\n"
    "Factory reference: **JLCPCB JLC06161H-3313**, six copper layers, nominal finished thickness **1.6 mm**, outer copper 1 oz and inner copper 0.5 oz.\n\n"
    "| From top | Layer/material | Thickness |\n"
    "|---|---|---:|\n"
    "| L1 | External copper | 0.035 mm |\n"
    "| Dielectric | 3313 prepreg | 0.0994 mm |\n"
    "| L2 | Internal copper | 0.0152 mm |\n"
    "| Dielectric | Core, Dk 4.6 | 0.55 mm |\n"
    "| L3 | Internal copper | 0.0152 mm |\n"
    "| Dielectric | 2116 prepreg | 0.1088 mm |\n"
    "| L4 | Internal copper | 0.0152 mm |\n"
    "| Dielectric | Core, Dk 4.6 | 0.55 mm |\n"
    "| L5 | Internal copper | 0.0152 mm |\n"
    "| Dielectric | 3313 prepreg | 0.0994 mm |\n"
    "| L6 | External copper | 0.035 mm |\n\n"
    "JLCPCB publishes Dk values of 4.1 for 3313 prepreg, 4.16 for 2116 prepreg and 4.6 for core. Its impedance page specifies solder-mask dielectric constant 3.8, 1.2 mil coating above substrate, 0.6 mil above copper traces and 1.2 mil between traces.\n\n"
    "**Important:** this selects a real published factory stackup; it does not constitute an impedance sign-off. The actual USB 90-ohm and any other controlled-impedance geometries still require the manufacturer's calculator/field-solver using the final copper weights, solder mask, reference plane and trace geometry, followed by factory confirmation. Do not claim controlled impedance until JLCPCB accepts the order's impedance settings.\n\n"
    "Reference: https://jlcpcb.com/impedance\n",encoding="utf-8")

print("Updated KiCad stackup to JLCPCB published JLC06161H-3313; nominal finished thickness 1.6mm.")
