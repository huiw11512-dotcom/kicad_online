#!/usr/bin/env python3
"""Remove one verified dangling 2.54 mm schematic wire spur; no net endpoints/pins are moved."""
from pathlib import Path
root=Path("cm5_mini_host")
p=root/"PCIe-M2.kicad_sch"
s=p.read_text(encoding="utf-8")
uuid='(uuid "45bd3ceb-a5c3-48b0-a48c-20c7d9db246e")'
if s.count(uuid)!=1:raise SystemExit("Expected exactly one audited orphan wire UUID")
pos=s.index(uuid); start=s.rfind("\n\t(wire",0,pos)+2
if start<2:raise SystemExit("Cannot locate dangling wire block")
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
if end is None:raise SystemExit("Malformed wire expression")
block=s[start:end]
if "(xy 180.34 119.38) (xy 180.34 121.92)" not in block or "(stroke" not in block:
    raise SystemExit("Audited wire geometry no longer matches; refusing deletion")
# The endpoint (180.34,119.38) has no pin, label, junction or no-connect marker;
# the other end joins an existing net at (180.34,121.92). Remove only the 2.54mm spur.
s=s[:start]+s[end:]
p.write_text(s,encoding="utf-8")
(root/"ORPHAN_WIRE_CLEANUP_REV_B.md").write_text(
    "# Rev.B schematic orphan-wire cleanup\n\n"
    "Removed PCIe-M2.kicad_sch wire UUID 45bd3ceb-a5c3-48b0-a48c-20c7d9db246e, "
    "the isolated 2.54 mm vertical spur from (180.34,119.38) to the existing net junction at (180.34,121.92). "
    "No symbol pin, label, junction or no-connect object was moved or deleted; only the dangling wire segment was removed.\n",encoding="utf-8")
print("Removed the exact audited 2.54 mm dangling schematic wire spur.")
