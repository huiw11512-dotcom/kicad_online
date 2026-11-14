#!/usr/bin/env python3
"""Remove only the duplicated CM5 *module-outline* silkscreen in logical HSS half.

CM5 is represented as two KiCad logical footprints Module301 GPIO and Module302
HSS; both draw the same large external B.SilkS perimeter. Keep complete GPIO
perimeter; keep HSS's six connector-specific silk strokes. Remove four long
outer lines + four corner arcs from HSS board instance and its local .pretty.
No pad, fab, courtyard, copper, hole or net data changes.
"""
from pathlib import Path
import re, math, pcbnew

folder=Path("cm5_mini_host")
pcbpath=folder/"CM5_MINIMA_3.kicad_pcb"
libpath=folder/"CM5IO.pretty"/"Raspberry-Pi-5-Compute-Module_HSS.kicad_mod"

def sexpr_end(s,k):
    depth=0;quote=False;escape=False
    for j in range(k,len(s)):
        c=s[j]
        if quote:
            if escape:escape=False
            elif c=="\\":escape=True
            elif c=='"':quote=False
        else:
            if c=='"':quote=True
            elif c=='(':depth+=1
            elif c==')':
                depth-=1
                if depth==0:return j+1
    raise ValueError("unbalanced native KiCad expression")

def edit(path,token,need_ref,layer):
    s=path.read_text(encoding="utf-8")
    k=s.find(token)
    if k<0 or s.count(token)!=1:raise ValueError(f"Expected unique {token} in {path}")
    en=sexpr_end(s,k)
    block=s[k:en]
    if need_ref and '(property "Reference" "Module302"' not in block:
        raise ValueError("Footprint is not the HSS half Module302")
    spans=[]
    for m in re.finditer(r'\(fp_(?:line|arc)\b',block):
        stop=sexpr_end(block,m.start())
        val=block[m.start():stop]
        if f'(layer "{layer}")' not in val:continue
        st=re.search(r'\(start\s+(-?[\d.]+)\s+(-?[\d.]+)\)',val)
        ed=re.search(r'\(end\s+(-?[\d.]+)\s+(-?[\d.]+)\)',val)
        if not st or not ed:continue
        xs,ys=map(float,st.groups());xe,ye=map(float,ed.groups())
        length=math.hypot(xe-xs,ye-ys)
        outer_line=val.startswith("(fp_line") and length>=30.0
        outer_arc=val.startswith("(fp_arc") and (
            any(abs(v-a)<0.01 for v in (xs,xe) for a in (-3.5,0,33,36.5))
            and (abs(xs-xe)>2 or abs(ys-ye)>2)
        )
        if outer_line or outer_arc:
            spans.append((m.start(),stop,"arc" if outer_arc else "line",(xs,ys),(xe,ye)))
    if len(spans)!=8 or sum(x[2]=="line" for x in spans)!=4 or sum(x[2]=="arc" for x in spans)!=4:
        raise ValueError(f"Expected exactly 4 long lines + 4 corner arcs, got {spans}")
    for st,en,*rest in reversed(spans):block=block[:st]+block[en:]
    result=s[:k]+block+s[sexpr_end(s,k):]
    path.write_text(result,encoding="utf-8")
    print(path,": removed 8 redundant CM5 outline primitives; kept all connector silkscreen.")
    return result

b=pcbnew.LoadBoard(str(pcbpath))
old_fp={x.GetReference():(len(x.Pads()),x.GetValue()) for x in b.GetFootprints()}
old_tracks=len(b.GetTracks())
old_nets=b.GetNetCount()
old_zones=len(b.Zones())
edit(pcbpath,'(footprint "CM5IO:Raspberry-Pi-5-Compute-Module_HSS"',True,"B.SilkS")
edit(libpath,'(footprint "Raspberry-Pi-5-Compute-Module_HSS"',False,"F.SilkS")
b2=pcbnew.LoadBoard(str(pcbpath))
assert {x.GetReference():(len(x.Pads()),x.GetValue()) for x in b2.GetFootprints()}==old_fp
assert len(b2.GetTracks())==old_tracks and b2.GetNetCount()==old_nets and len(b2.Zones())==old_zones
assert len(next(f for f in b2.GetFootprints() if f.GetReference()=="Module302").Pads())>90
print("Native KiCad PCB roundtrip passed: pad counts, nets, tracks and zones unchanged")
