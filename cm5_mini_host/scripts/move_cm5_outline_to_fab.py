#!/usr/bin/env python3
"""Move one CM5 body-outline stroke from bottom silkscreen to bottom fabrication.

Module301 GPIO is a logical half of the CM5 but its 48 mm long body outline
at x130.75 passes straight across the PCB's onboard switches SW101/SW501.
That line is an assembly mechanical outline, not an electrical or user-readable
label; keep it on Fab to document geometry without sending it to silkscreen.
The six real soldermask collisions are native KiCad DRC findings.
Exactly the same local-body segment is changed in CM5IO.pretty F.Fab.
"""
from pathlib import Path
import re,pcbnew
root=Path('cm5_mini_host')
pb=root/'CM5_MINIMA_3.kicad_pcb'
lib=root/'CM5IO.pretty'/'Raspberry-Pi-5-Compute-Module_GPIO.kicad_mod'
def end(s,k):
    d=0;q=False;escape=False
    for j in range(k,len(s)):
        c=s[j]
        if q:
            if escape:escape=False
            elif c=="\\":escape=True
            elif c=='"':q=False
        else:
            if c=='"':q=True
            elif c=='(':d+=1
            elif c==')':
                d-=1
                if d==0:return j+1
    raise ValueError("Invalid KiCad S-expression")
def move(path,token,layer,dest,geom,ref):
    s=path.read_text(encoding='utf-8')
    a=s.find(token)
    if a<0 or s.count(token)!=1:raise SystemExit(f'Expected one Module301 footprint in {path}')
    z=end(s,a);b=s[a:z]
    if ref and '(property "Reference" "Module301"' not in b:raise SystemExit('Wrong logical CM5 board footprint')
    matches=[]
    for m in re.finditer(r'\(fp_line\b',b):
        f=end(b,m.start());g=b[m.start():f]
        if geom in re.sub(r'\s+',' ',g) and '(layer "'+layer+'")' in g:
            matches.append((m.start(),f,g))
    if len(matches)!=1:raise SystemExit(f'Expected one outer silkscreen stroke in {path} but got {len(matches)}')
    st,stop,old=matches[0]
    new=old.replace('(layer "'+layer+'")','(layer "'+dest+'")',1)
    b=b[:st]+new+b[stop:]
    path.write_text(s[:a]+b+s[z:],encoding='utf-8')
    print(path, ': moved only one original physical CM5 body-stroke from',layer,'to',dest)
    return old,new
b0=pcbnew.LoadBoard(str(pb))
tracks=len(b0.GetTracks());zones=len(b0.Zones());nets=b0.GetNetCount()
def footprints(b):
    return sorted((f.GetReference(),sorted((p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,
                  p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y) for p in f.Pads()))
                  for f in b.GetFootprints())
pads=footprints(b0)
old,new=move(pb,'(footprint "CM5IO:Raspberry-Pi-5-Compute-Module_GPIO"','B.SilkS','B.Fab','(start -3.5 0) (end -3.5 48)',True)
move(lib,'(footprint "Raspberry-Pi-5-Compute-Module_GPIO"','F.SilkS','F.Fab','(start -3.5 -48) (end -3.5 0)',False)
b1=pcbnew.LoadBoard(str(pb))
assert footprints(b1)==pads and len(b1.GetTracks())==tracks and len(b1.Zones())==zones and b1.GetNetCount()==nets
print('Native KiCad board parser and board electrical geometry untouched.')
