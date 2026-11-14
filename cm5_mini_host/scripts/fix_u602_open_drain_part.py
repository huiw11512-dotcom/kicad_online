#!/usr/bin/env python3
"""Correct U602 part identity to match its existing open-drain schematic logic.

The real U602 circuit takes nPWR_LED through pin 2; pin 4 sinks D605/R605
to light the power LED. The schematic symbol is the non-inverting, open-drain
74LVC1G07, but the instance value incorrectly specified UMW
SN74LVC1G14DBVR (SOT-23 Schmitt inverter).
Select Diodes 74LVC1G07SE-7, JLCPCB C67531, SOT-353, matching intended
logic and nominal package family. This changes only the schematic instance
part value+P/N+datasheet and the PCB value text. It does NOT silently assume
the original SOT-353 copper lands are vendor-approved.
"""
from pathlib import Path
import pcbnew

root=Path("cm5_mini_host")
schematic=root/"IO.kicad_sch"
boardfile=root/"CM5_MINIMA_3.kicad_pcb"
oldpart="SN74LVC1G14DBVR"
newpart="74LVC1G07SE-7"
datasheet="https://www.diodes.com/datasheet/download/74LVC1G07.pdf"
oldurl="https://www.lcsc.com/datasheet/lcsc_datasheet_2405141143_UMW-Youtai-Semiconductor-Co---Ltd--SN74LVC1G14DBVR_C434069.pdf"
s=schematic.read_text(encoding="utf-8")
needle='(property "Reference" "U602"'
if s.count(needle)!=1:raise SystemExit("Not exactly one U602 schematic instance")
i=s.index(needle)
begin=s.rfind("\n\t(symbol",0,i)+2
if begin<2 or '(lib_id "CM4IO:74LVC1G07_copy")' not in s[begin:i]:
    raise SystemExit("U602 is not expected open-drain buffer symbol")
def end(s,k):
    depth=0;quoted=False;escaped=False
    for j in range(k,len(s)):
        c=s[j]
        if quoted:
            if escaped:escaped=False
            elif c=="\\":escaped=True
            elif c=='"':quoted=False
        else:
            if c=='"':quoted=True
            elif c=='(':depth+=1
            elif c==')':
                depth-=1
                if depth==0:return j+1
    raise ValueError("Malformed KiCad S-expression")
fin=end(s,begin)
block=s[begin:fin]
oldvalues=[
    ('(property "Value" "'+oldpart+'"','(property "Value" "'+newpart+'"'),
    ('(property "P/N" "'+oldpart+'"','(property "P/N" "'+newpart+'"'),
    ('(property "Datasheet" "'+oldurl+'"','(property "Datasheet" "'+datasheet+'"')
]
for original,repl in oldvalues:
    if block.count(original)!=1:raise SystemExit("Missing expected U602 field "+original)
    block=block.replace(original,repl,1)
updated=s[:begin]+block+s[fin:]
assert updated.count(needle)==1
schematic.write_text(updated,encoding="utf-8")
print("U602 schematic: value and P/N =>",newpart,"Diodes SOT353 open drain. Datasheet corrected.")

b=pcbnew.LoadBoard(str(boardfile))
fp=[f for f in b.GetFootprints() if f.GetReference()=="U602"]
if len(fp)!=1:raise SystemExit("U602 board footprint missing")
f=fp[0]
if f.GetValue()!=oldpart:raise SystemExit(f"Unexpected PCB U602 value {f.GetValue()}")
if str(f.GetFPID().GetLibItemName())!="SOT-353_SC-70-5":
    raise SystemExit("Physical U602 footprint not SC70-5; verify before change")
pad=lambda z:sorted((p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,
                      p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y) for p in z.Pads())
before=pad(f)
if len(before)!=5:raise SystemExit("U602 needs exactly five pads")
trackcount=len(b.GetTracks());zones=len(b.Zones());nets=b.GetNetCount()
f.SetValue(newpart)
pcbnew.SaveBoard(str(boardfile),b)

# KiCad footprint also stores a user-defined P/N field, separately from Value.
# Changing Value alone creates footprint_symbol_field_mismatch, so update
# precisely this U602 footprint's P/N property in the serialized native board.
raw=boardfile.read_text(encoding="utf-8")
pnpos=raw.find('(property "Reference" "U602"')
if pnpos<0 or raw.count('(property "Reference" "U602"')!=1:
    raise SystemExit("No unique PCB U602 footprint reference")
fbeg=raw.rfind("\n\t(footprint",0,pnpos)+2
if fbeg<2:raise SystemExit("Cannot locate U602 footprint record")
fend=end(raw,fbeg)
ft=raw[fbeg:fend]
old_field='(property "P/N" "'+oldpart+'"'
new_field='(property "P/N" "'+newpart+'"'
if ft.count(old_field)!=1:
    raise SystemExit("U602 P/N field is not the expected old part")
ft=ft.replace(old_field,new_field,1)
old_ds='(property "Datasheet" "'+oldurl+'"'
if old_ds in ft:
    ft=ft.replace(old_ds,'(property "Datasheet" "'+datasheet+'"',1)
raw=raw[:fbeg]+ft+raw[fend:]
boardfile.write_text(raw,encoding="utf-8")

b2=pcbnew.LoadBoard(str(boardfile))
p2=next(x for x in b2.GetFootprints() if x.GetReference()=="U602")
assert p2.GetValue()==newpart and pad(p2)==before
assert len(b2.GetTracks())==trackcount and len(b2.Zones())==zones and b2.GetNetCount()==nets
print("KiCad roundtrip: U602 PCB footprint value updated; five pads, nets, copper traces, zones unchanged.")
