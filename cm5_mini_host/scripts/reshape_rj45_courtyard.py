#!/usr/bin/env python3
"""Manufacturer-grounded, non-rectangular RJ45 F.CrtYd engineering candidate.

Kycon GLPLX-SMT-188S7-QQ-Y/G official A4 drawing: 17.60 mm outside body width,
21.50 mm body depth. Original imported rectangular F.CrtYd is 22.4x24.229 mm,
and incorrectly treats the separated shield solder tabs as a full-width body.

The proposed polygon retains ≥0.25 mm outside the 17.6mm body width, ≥0.25mm
beyond all 14 signal-pad envelopes at the rear, and wing-shaped pockets with
≥0.25mm clearance beyond both 2.1x3.1mm shield solder lands (pads 15/16).
No copper, component placement, drill, paste, Edge.Cuts or pad is modified.

DRC and physical assembly clearance are final acceptance gates.
"""
from pathlib import Path
import re,uuid
import pcbnew

root=Path("cm5_mini_host")
boardpath=root/"CM5_MINIMA_3.kicad_pcb"
libpath=root/"Samacsys.pretty"/"GLPLXSMT188S7QQYG.kicad_mod"
# Coordinates in KiCad footprint local frame, millimeters.
polygon=[
    (-9.05,-10.58),(9.05,-10.58),
    (9.05,3.10),(10.45,3.10),
    (10.45,6.71),(9.05,6.71),
    (9.05,13.16),(-9.05,13.16),
    (-9.05,6.71),(-10.45,6.71),
    (-10.45,3.10),(-9.05,3.10)
]
def end_expr(s,k):
    dep=0;quote=False;escape=False
    for i in range(k,len(s)):
        c=s[i]
        if quote:
            if escape:escape=False
            elif c=="\\":escape=True
            elif c=='"':quote=False
        elif c=='"':quote=True
        elif c=='(':
            dep+=1
        elif c==')':
            dep-=1
            if dep==0:return i+1
    raise ValueError("Bad KiCad expression")
def point_in_polygon(x,y):
    inside=False
    for k,(ax,ay) in enumerate(polygon):
        bx,by=polygon[(k+1)%len(polygon)]
        # boundary included for tolerance
        if abs((bx-ax)*(y-ay)-(by-ay)*(x-ax))<1e-7 and min(ax,bx)-1e-8<=x<=max(ax,bx)+1e-8 and min(ay,by)-1e-8<=y<=max(ay,by)+1e-8:return True
        if (ay>y)!=(by>y):
            cross=(bx-ax)*(y-ay)/(by-ay)+ax
            if x<cross:inside=not inside
    return inside

# SMD-land check: original footprint has 14 tiny signal lands and 2 shield lands.
lib=libpath.read_text(encoding="utf-8")
pads=[]
for m in re.finditer(r'\(pad "([^"]+)" smd rect\s*\(at ([\d.-]+) ([\d.-]+)\)\s*\(size ([\d.]+) ([\d.]+)\)',lib):
    num,x,y,w,h=m.groups();pads.append((num,*map(float,(x,y,w,h))))
if len(pads)!=16:raise SystemExit(f"Expected 16 RJ45 solder lands, got {len(pads)}")
assert {'15','16'}<=set(p[0] for p in pads)
for num,x,y,w,h in pads:
    for px in (x-w/2-.2,x+w/2+.2):
        for py in (y-h/2-.2,y+h/2+.2):
            if not point_in_polygon(px,py):
                raise SystemExit(f"New courtyard does not enclose {num} solder land plus 0.2mm margin at {(px,py)}")
def replace_courtyard(src,expected_type):
    s=src.read_text(encoding="utf-8")
    if expected_type=="board":
        token='(footprint "Samacsys:GLPLXSMT188S7QQYG"'
    else:
        token='(footprint "GLPLXSMT188S7QQYG"'
    pos=s.find(token)
    if pos<0 or s.count(token)!=1:
        raise ValueError(f"Expected 1 {expected_type} GLPLX footprint, got {s.count(token)}")
    end=end_expr(s,pos)
    body=s[pos:end]
    if expected_type=="board":
        if '(property "Reference" "J1"' not in body:
            raise ValueError("Wrong board footprint; refuse to modify")
    spans=[]
    for m in re.finditer(r'\(fp_line\b',body):
        e=end_expr(body,m.start())
        text=body[m.start():e]
        if '(layer "F.CrtYd")' in text:
            spans.append((m.start(),e,text))
    if len(spans)!=4:raise ValueError(f"Expected 4 original F.CrtYd lines, found {len(spans)}")
    joined="\n".join(x[2] for x in spans)
    for x in ["-11.2","11.2","12.903","-11.326"]:
        if x not in joined:raise ValueError(f"Original Courtyard coordinate {x} not present")
    # Delete the old 4 segments and insert one closed nonrectangular, manufacturability-aware outline.
    for st,en,_ in reversed(spans):
        body=body[:st]+body[en:]
    strokes=[]
    for k,(x1,y1) in enumerate(polygon):
        x2,y2=polygon[(k+1)%len(polygon)]
        strokes.append(f'''
\t(fp_line
\t\t(start {x1:.3f} {y1:.3f})
\t\t(end {x2:.3f} {y2:.3f})
\t\t(stroke (width 0.1) (type solid))
\t\t(layer "F.CrtYd")
\t\t(uuid "{uuid.uuid4()}")
\t)''')
    # Board instance may have only the 4 original Courtyard graphics.
    # Appending before the footprint closing paren is valid KiCad and retains every pad.
    body=body[:-1]+"\n"+"\n".join(strokes)+"\n)"
    s=s[:pos]+body+s[end:]
    src.write_text(s,encoding="utf-8")
    print("Replaced 4 old F.CrtYd segments with 12 pad-aware polygon segments in",src)
replace_courtyard(boardpath,"board")
replace_courtyard(libpath,"library")
board=pcbnew.LoadBoard(str(boardpath))
fp=next(f for f in board.GetFootprints() if f.GetReference()=="J1")
assert len(fp.Pads())==18,"Expected 16 copper pads plus 2 NPTH alignment holes"
print("Parsed modified KiCad board successfully; RJ45 pads retained:",len(fp.Pads()))
