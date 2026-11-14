#!/usr/bin/env python3
"""Remove unavailable footprint assignment from the DNP/off-board TP701 placeholder."""
from pathlib import Path
p=Path("cm5_mini_host/PCIe-M2.kicad_sch")
s=p.read_text(encoding="utf-8")
token='(property "Reference" "TP701"'
if s.count(token)!=1:raise SystemExit("Expected exactly one TP701")
at=s.index(token)
start=s.rfind("\n\t(symbol",0,at)+2
if start<2:raise SystemExit("TP701 instance not found")
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
if end is None:raise SystemExit("Malformed TP701 instance")
block=s[start:end]
if '(on_board no)' not in block or '(dnp yes)' not in block:
    raise SystemExit("TP701 not explicitly DNP/off-board; refuse change")
old='(property "Footprint" "TestPoint:TestPoint_Pad_2.0x2.0mm"'
if block.count(old)!=1:
    raise SystemExit("Expected footprint assignment not found")
block=block.replace(old,'(property "Footprint" ""',1)
p.write_text(s[:start]+block+s[end:],encoding="utf-8")
Path("cm5_mini_host/TP701_DNP_FOOTPRINT_CLEANUP.md").write_text(
    "# TP701 DNP test-point placeholder\n\n"
    "Cleared an unavailable library footprint from the PCIe-M2 sheet's TP701 "
    "symbol, which is explicitly (dnp yes) and (on_board no). "
    "No PCB pads, tracks, nets, or fitted components were altered. "
    "Native KiCad ERC must confirm the missing-footprint warning is removed.\n",
    encoding="utf-8")
print("Cleared obsolete footprint link from DNP/off-board TP701.")
