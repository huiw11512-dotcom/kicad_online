#!/usr/bin/env python3
"""MiniHost USB2 host power-source default-current variant.
R702/R703 Rp: 22k -> 56k, advertised 1.5A -> USB default (5V/500mA for USB2).
R701 AP22653 ILIM: 15k -> 39k, nominal threshold ~0.64A.

All resistors retain their exact pad positions and 0402 footprints.
Changes are made only after validating netlist-derived old reference values.
Actual current advertisement depends on the type-C standard and wiring, not DRC.
"""
from pathlib import Path
import pcbnew

root=Path("cm5_mini_host")
schematic=root/"USB.kicad_sch"
pcb=root/"CM5_MINIMA_3.kicad_pcb"
target={"R701":("15k","39k"),"R702":("22k","56k"),"R703":("22k","56k")}
s=schematic.read_text(encoding="utf-8")
def end_expr(text,at):
    depth=0;quoted=False;escaped=False
    for i in range(at,len(text)):
        c=text[i]
        if quoted:
            if escaped:escaped=False
            elif c=="\\":escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c=='(':depth+=1
        elif c==')':
            depth-=1
            if depth==0:return i+1
    raise RuntimeError("Malformed KiCad S-expression")
for ref,(old,new) in target.items():
    needle=f'(property "Reference" "{ref}"'
    if s.count(needle)!=1:raise RuntimeError(f"{ref}: expected one reference property")
    ix=s.index(needle)
    beginning=s.rfind("\n\t(symbol",0,ix)+2
    if beginning<2:raise RuntimeError("Instance block not found")
    ending=end_expr(s,beginning)
    body=s[beginning:ending]
    assert needle in body and '(lib_id "Device:R")' in body, f"unexpected instance {ref}"
    val=f'(property "Value" "{old}"'
    if body.count(val)!=1:raise RuntimeError(f"{ref}: expected one old value {old}")
    body=body.replace(val,f'(property "Value" "{new}"',1)
    s=s[:beginning]+body+s[ending:]
    print(f"{ref} schematic: {old}->{new}")
schematic.write_text(s,encoding="utf-8")

b=pcbnew.LoadBoard(str(pcb))
track_count=len(b.GetTracks())
def geom(board):
    pads=[]
    for fp in board.GetFootprints():
        for p in fp.Pads():
            pads.append((fp.GetReference(),p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,
                         p.GetSize().x,p.GetSize().y))
    return sorted(pads)
pads_before=geom(b)
for ref,(old,new) in target.items():
    fps=[f for f in b.GetFootprints() if f.GetReference()==ref]
    if len(fps)!=1:raise RuntimeError(f"Expected one PCB footprint {ref}")
    f=fps[0]
    if f.GetValue()!=old:raise RuntimeError(f"{ref}: board current value is {f.GetValue()}, expected {old}")
    if len(f.Pads())!=2:raise RuntimeError(f"{ref}: not a 2-pad resistor")
    f.SetValue(new)
    print(f"{ref} PCB: {old}->{new}")
assert len(b.GetTracks())==track_count and geom(b)==pads_before
pcbnew.SaveBoard(str(pcb),b)
check=pcbnew.LoadBoard(str(pcb))
assert len(check.GetTracks())==track_count and geom(check)==pads_before
for ref,(_,new) in target.items():
    assert next(f for f in check.GetFootprints() if f.GetReference()==ref).GetValue()==new
print("Roundtrip check passed: no pads, coordinates, nets or tracks were modified.")
