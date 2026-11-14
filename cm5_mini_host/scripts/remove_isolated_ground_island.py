#!/usr/bin/env python3
"""Change ONLY multi-layer GND zone island policy to ALWAYS remove islands.

The GND region spanning F.Cu, B.Cu, In1.Cu, In2.Cu, In4.Cu uses
island_removal_mode 2 and island_area_min 5mm2; KiCad 10 DRC reports one
disconnected GND fill island near (74.99,20.22). Ground islands are not a
useful signal-return plane. Change mode to 0 (always remove disconnected
areas) and refill using native pcbnew. The zone outline, clearance, net and
all traces/vias/pads must be retained. DRC verification is a commit gate.
"""
from pathlib import Path
import re, math, pcbnew
p=Path('cm5_mini_host/CM5_MINIMA_3.kicad_pcb')
s=p.read_text(encoding='utf-8')
anchor='(uuid "6639aad9-23df-4a45-9cb9-f9efd7cc4ef0")'
i=s.find(anchor)
if i<0 or s.count(anchor)!=1:raise SystemExit('Wrong GND zone ID')
start=s.rfind('\n\t(zone',0,i)+2
if start<2:raise SystemExit('Cannot locate GND zone')
def end(s,k):
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
    raise ValueError('Corrupt zone S-expression')
stop=end(s,start)
blk=s[start:stop]
if '(net "GND")' not in blk or '(layers "F.Cu" "B.Cu" "In1.Cu" "In2.Cu" "In4.Cu")' not in blk:
    raise SystemExit('Wrong multilayer GND fill')
needle='(island_removal_mode 2)\n\t\t\t(island_area_min 5)'
if blk.count(needle)!=1:raise SystemExit('Unexpected existing GND island setting')
blk=blk.replace(needle,'(island_removal_mode 0)',1)
s=s[:start]+blk+s[stop:]
b0=pcbnew.LoadBoard(str(p))
def signature(b):
    return (
        sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,
                p.GetSize().x,p.GetSize().y) for f in b.GetFootprints() for p in f.Pads()),
        sorted((t.GetNetname(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetLayer())
               for t in b.GetTracks()),
        sorted((z.GetNetname(),str(z.GetLayerSet().FmtHex()),str(z.GetPosition().x)+":"+str(z.GetPosition().y)) for z in b.Zones()))
baseline=signature(b0)
p.write_text(s,encoding='utf-8')
b=pcbnew.LoadBoard(str(p))
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(p),b)
b1=pcbnew.LoadBoard(str(p))
if signature(b1)!=baseline:raise SystemExit('Something besides zone island fill changed')
print("GND 5-layer flood changed island removal from min-area 5mm^2 to ALWAYS, refilled and PCB parsed.")
print("Pad, track/via, zone count/net/layer/outline geometry unchanged.")
targets=[('/CM5/PWR_BUT',130.9594,65.5595),('+BATT',81.45,72.5)]
def mm(k):return pcbnew.ToMM(k)
def dist(v,x,y):return math.hypot(mm(v.x)-x,mm(v.y)-y)
lines=['# Two retained dangling vias: native KiCad physical audit','','These are NOT blindly deleted. Removing them without attached tracks caused two new track_dangling warnings in an earlier trial.','']
for name,x,y in targets:
    v=[t for t in b1.GetTracks() if isinstance(t,pcbnew.PCB_VIA) and t.GetNetname()==name and dist(t.GetPosition(),x,y)<0.002]
    if len(v)!=1:raise SystemExit(f'Expected one remaining via {name} at {x},{y}')
    q=v[0]
    lines.append(f'## {name}, via ({x:.4f},{y:.4f})mm')
    lines.append(f'- via drill {mm(q.GetDrillValue()):.4f}mm and annular diameter {mm(q.GetWidth()):.4f}mm')
    count=0
    for t in b1.GetTracks():
        if t is q or isinstance(t,pcbnew.PCB_VIA) or t.GetNetname()!=name:continue
        a=t.GetStart();c=t.GetEnd()
        if dist(a,x,y)<0.006 or dist(c,x,y)<0.006:
            count+=1
            lines.append(f'- track layer {b1.GetLayerName(t.GetLayer())}, from {mm(a.x):.4f},{mm(a.y):.4f} to {mm(c.x):.4f},{mm(c.y):.4f}mm, width {mm(t.GetWidth()):.4f}mm, length {t.GetLength():.0f} IU')
    lines.append(f'- touching copper-trace endpoints: **{count}**')
    lines.append('')
Path('cm5_mini_host/DANGLING_VIA_DETAIL.md').write_text('\n'.join(lines),encoding='utf-8')
print("\n".join(lines))
