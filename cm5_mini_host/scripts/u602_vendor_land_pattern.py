#!/usr/bin/env python3
"""Vendor-correct Diodes 74LVC1G07SE-7 SOT-353 pad land locking.

Diodes datasheet DS32274 Rev12 (page 13): SOT353 center spacing
C1=1.900 mm, transverse pitch C=0.650 mm, recommended pad Y=0.600mm
radial length, X=0.420mm lateral width.
Existing five U602 board copper pad centers are +-0.95 X and 0.65 Y
pitch but land size was 0.650x0.400mm. Set size to 0.600x0.420mm
at unchanged centers. Save identical native board footprint to locally
versioned CM5IO:Diodes_74LVC1G07SE7_SOT353 library. Update the U602
IO.kicad_sch instance footprint property. No other footprint/pad changed.
"""
from pathlib import Path
import re,pcbnew
root=Path('cm5_mini_host')
pcb=root/'CM5_MINIMA_3.kicad_pcb'
sch=root/'IO.kicad_sch'
libdir=root/'CM5IO.pretty'
oldid='Package_TO_SOT_SMD:SOT-353_SC-70-5'
newname='Diodes_74LVC1G07SE7_SOT353'
newid='CM5IO:'+newname
libfile=libdir/(newname+'.kicad_mod')
if libfile.exists():raise SystemExit('Refuse overwrite of existing vendor land-pattern footprint')
def expr_end(s,k):
    depth=0;q=False;esc=False
    for j in range(k,len(s)):
        c=s[j]
        if q:
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':q=False
        else:
            if c=='"':q=True
            elif c=='(':depth+=1
            elif c==')':
                depth-=1
                if depth==0:return j+1
    raise ValueError('KiCad S-expression corrupted')
def extract_fp(s):
    idx=s.find('(property "Reference" "U602"')
    if idx<0 or s.count('(property "Reference" "U602"')!=1:
        raise SystemExit('U602 board footprint not unique')
    st=s.rfind('\n\t(footprint',0,idx)+2
    if st<2:raise SystemExit('U602 board footprint delimiter missing')
    en=expr_end(s,st)
    return st,en,s[st:en]
b0=pcbnew.LoadBoard(str(pcb))
f0=next(f for f in b0.GetFootprints() if f.GetReference()=='U602')
before=sorted((p.GetNumber(),p.GetPosition().x,p.GetPosition().y,p.GetNetname(),p.GetSize().x,p.GetSize().y) for p in f0.Pads())
if len(before)!=5 or any(abs(pcbnew.ToMM(x[4])-0.65)>.0001 or abs(pcbnew.ToMM(x[5])-0.4)>.0001 for x in before):
    raise SystemExit('U602 pad baseline not matching expected 5 rectangles 0.65x0.4mm')
trackcount=len(b0.GetTracks());netcount=b0.GetNetCount();zones=len(b0.Zones())
s=pcb.read_text(encoding='utf-8')
st,en,block=extract_fp(s)
oldheader='(footprint "'+oldid+'"'
if block.count(oldheader)!=1:raise SystemExit('Wrong U602 existing footprint ID')
block=block.replace(oldheader,'(footprint "'+newid+'"',1)
oldprop='(property "Footprint" "'+oldid+'"'
if block.count(oldprop)==1:
    block=block.replace(oldprop,'(property "Footprint" "'+newid+'"',1)
padcount=0
spans=[]
for m in re.finditer(r'\(pad "[^"]*" smd (?:rect|roundrect)\b',block):
    stop=expr_end(block,m.start())
    p=block[m.start():stop]
    if '(size 0.65 0.4)' not in p:
        raise SystemExit('Unexpected U602 pad copper size')
    spans.append((m.start(),stop,p.replace('(size 0.65 0.4)','(size 0.6 0.42)',1)))
    padcount+=1
if padcount!=5:raise SystemExit(f'Expected 5 U602 solder pads, got {padcount}')
for a,z,repl in reversed(spans):block=block[:a]+repl+block[z:]
pcb.write_text(s[:st]+block+s[en:],encoding='utf-8')
sym=sch.read_text(encoding='utf-8')
k=sym.index('(property "Reference" "U602"')
a=sym.rfind('\n\t(symbol',0,k)+2
if a<2:raise SystemExit('Cannot locate U602 schematic symbol')
z=expr_end(sym,a);blk=sym[a:z]
if blk.count('(property "Footprint" "'+oldid+'"')!=1:raise SystemExit('Unexpected U602 schematic land assignment')
blk=blk.replace('(property "Footprint" "'+oldid+'"','(property "Footprint" "'+newid+'"',1)
sch.write_text(sym[:a]+blk+sym[z:],encoding='utf-8')
b=pcbnew.LoadBoard(str(pcb))
f=next(f for f in b.GetFootprints() if f.GetReference()=='U602')
assert f.GetFPID().GetLibNickname()=='CM5IO' and f.GetFPID().GetLibItemName()==newname
newpads=sorted((p.GetNumber(),p.GetPosition().x,p.GetPosition().y,p.GetNetname(),p.GetSize().x,p.GetSize().y) for p in f.Pads())
assert len(newpads)==5
assert [(x[0],x[1],x[2],x[3]) for x in newpads]==[(x[0],x[1],x[2],x[3]) for x in before]
assert all(abs(pcbnew.ToMM(x[4])-.6)<.00001 and abs(pcbnew.ToMM(x[5])-.42)<.00001 for x in newpads)
assert len(b.GetTracks())==trackcount and b.GetNetCount()==netcount and len(b.Zones())==zones
# Store exact geometry from board footprint via KiCad native serialiser.
io=pcbnew.PCB_IO_KICAD_SEXPR()
io.FootprintSave(str(libdir),f)
if not libfile.exists():raise SystemExit('KiCad did not produce local footprint file')
fl=io.FootprintLoad(str(libdir),newname)
assert fl is not None and len(list(fl.Pads()))==5
def geom(fp):
    return sorted((p.GetNumber(),p.GetFPRelativePosition().x,p.GetFPRelativePosition().y,
                   p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y) for p in fp.Pads())
if geom(fl)!=geom(f):
    raise SystemExit('Locally saved vendor footprint differs from board solder lands')
print("Five U602 solder lands adjusted to vendor 0.600x0.420mm, C1=1.9mm and pitch0.65mm retained.")
print("Native PCB custom footprint+local project library saved; all other physical pad centers, vias, tracks, nets unchanged.")
