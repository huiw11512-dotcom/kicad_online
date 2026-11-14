#!/usr/bin/env python3
"""Add a PWR_FLAG to the CM5_3.3V supply source net feeding U602."""
from pathlib import Path
import re,uuid
p=Path("cm5_mini_host/IO.kicad_sch")
s=p.read_text(encoding="utf-8")
if '(property "Reference" "#FLG0999"' in s: raise SystemExit("U602 PWR_FLAG already exists; refusing duplicate")
token='(property "Reference" "#FLG0102"'
if s.count(token)!=1: raise SystemExit("Expected exactly one reusable PWR_FLAG template")
pos=s.index(token); start=s.rfind("\n\t(symbol",0,pos)+2
if start<2: raise SystemExit("Cannot locate PWR_FLAG symbol instance")
d=0;q=False;e=False;end=None
for i in range(start,len(s)):
    c=s[i]
    if q:
        if e:e=False
        elif c=="\\":e=True
        elif c=='"':q=False
    elif c=='"':q=True
    elif c=="(":d+=1
    elif c==")":
        d-=1
        if d==0:end=i+1;break
if end is None: raise SystemExit("Malformed PWR_FLAG template")
block=s[start:end]
if '(lib_id "power:PWR_FLAG")' not in block: raise SystemExit("Template is not PWR_FLAG")
oldx,oldy,newx,newy=63.5,59.69,76.2,22.86
dx,dy=newx-oldx,newy-oldy
def move(m):
    x,y,a=float(m.group(1)),float(m.group(2)),m.group(3)
    return f'(at {x+dx:.4f} {y+dy:.4f} {a})'
block=re.sub(r'\(at (-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?) ([^)]+)\)',move,block)
block=block.replace('#FLG0102','#FLG0999')
block=block.replace('reference "#FLG0102"','reference "#FLG0999"')
block=re.sub(r'\(uuid "[^"]+"\)',lambda m:f'(uuid "{uuid.uuid4()}")',block)
# Keep the flag orientation but put its pin exactly on the U602 VCC net's +3V3_PI source node.
s=s[:end]+ "\n\t"+block + s[end:]
p.write_text(s,encoding="utf-8")
Path("cm5_mini_host/U602_3V3_PI_PWR_FLAG_AUDIT.md").write_text(
"# U602 3.3V ERC power-source flag\n\n"
"Added a PWR_FLAG at (76.20,22.86) mm on the +3V3_PI wire feeding U602 VCC pin 5. This tells ERC that the rail is driven by the CM5 module's regulated 3.3V output, rather than treating the rail's power-input symbols as a source. It does not add a physical component or change PCB copper. The CM5 pins 84/86 remain the physical source; the board route to pin 84 is audited separately.\n",encoding="utf-8")
print("Added PWR_FLAG to U602 +3V3_PI supply node.")
