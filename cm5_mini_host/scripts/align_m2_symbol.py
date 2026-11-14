#!/usr/bin/env python3
"""Correct CM5 MINIMA's M.2 symbol variant to match the actual 2230/2242 footprint.

Original symbol has four alternative SSD mounting-hole pins M1..M4
(GND2230, GND2242, GND2260, GND2280); NONE exist in the J701 physical
footprint used by the routed board. Actual SSD fixing holes are represented
separately as M701/M702, and shield pins S1/S2 remain present.

This is a narrowly scoped KiCad S-expression modification; CI must confirm
ERC and schematic-vs-PCB parity before committing any result.
"""
from pathlib import Path
import re

src=Path("cm5_mini_host/PCIe-M2.kicad_sch")
s=src.read_text(encoding="utf-8")

def end_of_expr(text,at):
    if text[at]!='(':
        raise ValueError("expression must start with (")
    depth=0; quote=False; esc=False
    for j in range(at,len(text)):
        c=text[j]
        if quote:
            if esc:esc=False
            elif c=="\\":esc=True
            elif c=='"':quote=False
        elif c=='"':quote=True
        elif c=='(':
            depth+=1
        elif c==')':
            depth-=1
            if depth==0:return j+1
    raise ValueError("unbalanced S-expression")

label='(symbol "CM5IO:Bus_M.2_Socket_M"'
a=s.find(label)
assert a>=0, "M.2 cached library symbol not found"
b=end_of_expr(s,a)
lib=s[a:b]
for number in ("M1","M2","M3","M4"):
    matches=[]
    # Pin definitions start with "(pin electrical_type line" and must contain the expected number.
    for m in re.finditer(r'\(pin (?:no_connect|power_in|passive|input|output|bidirectional) line',lib):
        z=end_of_expr(lib,m.start())
        body=lib[m.start():z]
        if re.search(r'\(number "'+number+r'"',body):
            matches.append((m.start(),z,body))
    if len(matches)!=1:
        raise ValueError(f"Expected exactly one physical mounting pin definition {number}, got {len(matches)}")
    aa,bb,body=matches[0]
    if not re.search(r'\(name "GND(?:2230|2242|2260|2280)"',body):
        raise ValueError(f"Unexpected M.2 symbol pin {number}; refusing to remove")
    lib=lib[:aa]+lib[bb:]
    print("Removed stale physical socket mounting pin definition",number)
s=s[:a]+lib+s[b:]

# Remove matching pin instances ONLY from J701, never similarly numbered pins elsewhere.
key='(lib_id "CM5IO:Bus_M.2_Socket_M")'
at=s.index(key)
a=s.rfind("\n\t(symbol",0,at)+2
b=end_of_expr(s,a)
inst=s[a:b]
assert '(property "Reference" "J701"' in inst, "Expected J701 instance not found"
for number in ("M1","M2","M3","M4"):
    exp=r'\s*\(pin "'+number+r'"\s*\(uuid "[0-9a-f-]+"\)\s*\)'
    inst,n=re.subn(exp,"",inst)
    if n!=1:raise ValueError(f"Expected one J701 pin instance {number}, got {n}")
s=s[:a]+inst+s[b:]
for number in ("M1","M2","M3","M4"):
    assert '(number "'+number+'"' not in s[s.index(label):end_of_expr(s,s.index(label))]
    assert '(pin "'+number+'"' not in s[s.index(key):end_of_expr(s,s.rfind("\n\t(symbol",0,s.index(key))+2)]
# Mounting hole symbol objects and the copper board are NOT modified.
assert "M.2_Screw" in s and '"S1"' in s and '"S2"' in s
src.write_text(s,encoding="utf-8")
print("Saved",src,"— 4 obsolete mount pins removed; actual connector electrical pads unchanged")
