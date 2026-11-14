#!/usr/bin/env python3
"""Power the CM5 LED_nPWR open-drain buffer from CM5_3.3V, not +5V."""
from pathlib import Path
root=Path("cm5_mini_host")
p=root/"IO.kicad_sch"
s=p.read_text(encoding="utf-8")
uid='(uuid "2416617e-ff59-4026-9fb9-debfca7c0256")'
if s.count(uid)!=1:raise SystemExit("Expected one U602 VCC power symbol")
pos=s.index(uid); start=s.rfind("\n\t(symbol",0,pos)+2
if start<2:raise SystemExit("Cannot locate U602 VCC power symbol")
d=0;q=False;e=False;end=None
for i in range(start,len(s)):
    c=s[i]
    if q:
        if e:e=False
        elif c=="\\":e=True
        elif c=='"':q=False
    elif c=='"':q=True
    elif c=='(':d+=1
    elif c==')':
        d-=1
        if d==0:end=i+1;break
if end is None:raise SystemExit("Malformed power symbol block")
block=s[start:end]
if '(lib_id "power:+5V")' not in block or '(property "Value" "+5V"' not in block:
    raise SystemExit("U602 VCC power symbol is no longer +5V; manual review required")
if '(at 76.2 22.86 0)' not in block:raise SystemExit("U602 VCC coordinate changed")
block=block.replace('(property "Value" "+5V"','(property "Value" "+3V3_PI"',1)
block=block.replace('Power symbol creates a global label with name \\"+5V\\"','Power symbol creates a global label with name \\"+3V3_PI\\"',1)
p.write_text(s[:start]+block+s[end:],encoding="utf-8")
(root/"U602_3V3_PI_SUPPLY_AUDIT.md").write_text(
    "# U602 LED_nPWR buffer supply correction\n\n"
    "U602 (Diodes 74LVC1G07SE-7, LCSC C67531) now uses CM5_3.3V (+3V3_PI) on VCC pin 5 instead of +5V. "
    "The CM5 datasheet identifies LED_nPWR as a 3.3 V active-low output that requires buffering. "
    "At VCC=3.0–3.6 V, the 74LVC1G07 VIH requirement is 2.0 V, providing guaranteed compatibility with the CM5 3.3 V signal. "
    "Its open-drain output is rated for 0–5.5 V operation, so the existing 5 V LED pull-up through R605=2.2 kΩ is retained. "
    "The LED branch current is approximately 1.3 mA assuming a 2.0 V LED drop and 0.1 V low-level output. "
    "CM5_3.3V is available from CM5 pins 84/86; U602 supply current is negligible relative to the 600 mA module rail budget.\n\n"
    "No PCB pad, track, footprint, or LED resistor geometry is changed. Validate the LED behavior during first prototype bring-up.\n",encoding="utf-8")
print("U602 VCC changed from +5V to CM5_3.3V (+3V3_PI); 5V open-drain LED pull-up retained.")
