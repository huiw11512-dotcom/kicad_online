#!/usr/bin/env python3
"""Fail closed if USB type-C connections disagree between the schematic netlist
and PCB pad-net assignments. Important: full project parity still requires KiCad DRC.
"""
from pathlib import Path
import re,sys
import pcbnew

netfile=Path("reports/cm5.net")
s=netfile.read_text(errors="replace")
tok=re.findall(r'\s*(\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+)',s)
i=0
def parse():
    global i
    t=tok[i];i+=1
    if t!='(':return t.strip('"')
    a=[]
    while i<len(tok) and tok[i]!=')': a.append(parse())
    if i>=len(tok):raise ValueError("Unbalanced schematic netlist")
    i+=1
    return a
root=parse()
def walk(v):
    if isinstance(v,list):
        if v and v[0]=='net':yield v
        for x in v:yield from walk(x)
def field(v,k):
    for x in v:
        if isinstance(x,list) and x and x[0]==k and len(x)>1:return x[1]
    return ""
schematic={}
for net in walk(root):
    name=field(net,"name")
    for node in net:
        if isinstance(node,list) and node and node[0]=="node":
            ref=field(node,"ref");pin=field(node,"pin")
            if ref and pin:
                if (ref,pin) in schematic and schematic[(ref,pin)]!=name:
                    raise ValueError(f"Ambiguous schematic pin {ref}.{pin}")
                schematic[(ref,pin)]=name
board=pcbnew.LoadBoard("cm5_mini_host/CM5_MINIMA_3.kicad_pcb")
pcb={}
for fp in board.GetFootprints():
    for p in fp.Pads():
        if p.GetNumber():pcb[(fp.GetReference(),p.GetNumber())]=p.GetNetname()
expected={
"J101 USB-C data P":[("Module302","105"),("J101","A6"),("J101","B6"),("D101","1")],
"J101 USB-C data N":[("Module302","103"),("J101","A7"),("J101","B7"),("D101","2")],
"USB701 host data P":[("Module302","134"),("USB701","A6"),("USB701","B6"),("D701","1")],
"USB701 host data N":[("Module302","136"),("USB701","A7"),("USB701","B7"),("D701","2")],
}
results=["# Native KiCad schematic-vs-PCB USB pin parity", ""]
bad=0
for label, pins in expected.items():
    sn={schematic.get(p,"<MISSING>") for p in pins}
    pn={pcb.get(p,"<MISSING>") for p in pins}
    both=sn==pn and len(sn)==1 and "<MISSING>" not in sn
    if not both:bad+=1
    results.append(f"- {label}: {'MATCH' if both else 'MISMATCH'}; schematic={sorted(sn)}, PCB={sorted(pn)}")
    for p in pins:results.append(f"  - {p[0]}.{p[1]}: schematic {schematic.get(p,'<MISSING>')}; PCB {pcb.get(p,'<MISSING>')}")
results += ["",f"Mismatch group count: {bad}",""]
out=Path("reports/usb_sch_pcb_parity.md")
out.write_text("\n".join(results),encoding="utf-8")
print(out.read_text())
if bad: sys.exit(f"BLOCKED: {bad} USB groups don't match between schematic and actual PCB")
