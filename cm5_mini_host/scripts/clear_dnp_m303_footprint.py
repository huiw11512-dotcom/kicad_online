#!/usr/bin/env python3
"""Remove an unavailable footprint link from a DNP, off-board mechanical reference."""
from pathlib import Path
root=Path("cm5_mini_host")
p=root/"CM5.kicad_sch"
s=p.read_text(encoding="utf-8")
token='(property "Reference" "M303"'
if s.count(token)!=1:raise SystemExit("Expected one M303 symbol instance")
pos=s.index(token); start=s.rfind("\n\t(symbol",0,pos)+2
if start<2:raise SystemExit("Cannot locate M303 symbol block")
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
if end is None:raise SystemExit("Malformed M303 symbol")
block=s[start:end]
if '(on_board no)' not in block or '(dnp yes)' not in block:
    raise SystemExit("M303 is not the expected DNP/off-board mechanical placeholder")
old='(property "Footprint" "Antmicro-footprints:Compute-Module-4_H1.5mm"'
if block.count(old)!=1:raise SystemExit("M303 footprint link changed; manual review required")
block=block.replace(old,'(property "Footprint" ""',1)
p.write_text(s[:start]+block+s[end:],encoding="utf-8")
(root/"M303_DNP_FOOTPRINT_CLEANUP.md").write_text(
    "# M303 DNP mechanical placeholder\n\n"
    "Cleared the unresolved Antmicro footprint-library assignment from M303 only. "
    "The symbol instance is explicitly (on_board no) and (dnp yes), so it does not represent a fitted PCB component. "
    "No board footprint, net, pad or placement is changed.\n",encoding="utf-8")
print("Cleared obsolete footprint link from DNP/off-board M303 placeholder.")
