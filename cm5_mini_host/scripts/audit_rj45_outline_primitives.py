#!/usr/bin/env python3
"""Read-only exact KiCad Edge.Cuts primitive inventory around RJ45 opening."""
from pathlib import Path
import re
s=Path('cm5_mini_host/CM5_MINIMA_3.kicad_pcb').read_text(encoding='utf-8')
def expr_end(s,k):
    dep=0;q=False;esc=False
    for j in range(k,len(s)):
        c=s[j]
        if q:
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':q=False
        else:
            if c=='"':q=True
            elif c=='(':dep+=1
            elif c==')':
                dep-=1
                if dep==0:return j+1
    raise Exception('Invalid KiCad PCB expression')
rows=[]
for m in re.finditer(r'\(gr_(?:line|arc|poly|rect)\b',s):
    block=s[m.start():expr_end(s,m.start())]
    if '(layer "Edge.Cuts")' not in block:continue
    coords=re.findall(r'\((start|mid|end|xy)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\)',block)
    vals=[(a,float(b),float(c)) for a,b,c in coords]
    if vals and any(76<x<91 and 26<y<47 for _,x,y in vals):
        rows.append((m.group(0),vals,(re.search(r'\(uuid "([^"]+)"',block) or ['',''])[1]))
out=['# Exact RJ45 Edge.Cuts geometry near the shield-solder lands','','Source: native KiCad PCB edge primitives; no board changes.','', 'Current Kycon center 88.900,36.150 mm, shield pad centers at (83.996,27.0) and (83.996,45.3).','']
for shape,coords,uid in rows:out.append(f'- {shape}: {coords}, uuid={uid}')
text='\n'.join(out)+'\n'
print(text)
p=Path('cm5_mini_host/RJ45_EDGE_PRIMITIVE_INVENTORY.md')
p.write_text(text,encoding='utf-8')
