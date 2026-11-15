#!/usr/bin/env python3
"""Populate verified Rev.B manufacturer/LCSC identifiers and correct stale BOM fields."""
from pathlib import Path
import re

root=Path("cm5_mini_host")
pcb=root/"CM5_MINIMA_3.kicad_pcb"
src=pcb.read_text(encoding="utf-8",errors="replace")

def blocks(src,tag):
    needle="("+tag;pos=0
    while True:
        st=src.find(needle,pos)
        if st<0:return
        after=st+len(needle)
        if after<len(src) and not src[after].isspace() and src[after]!=")":pos=after;continue
        depth=0;quoted=False;escaped=False;end=None
        for i in range(st,len(src)):
            ch=src[i]
            if quoted:
                if escaped:escaped=False
                elif ch=="\\":escaped=True
                elif ch=='"':quoted=False
            else:
                if ch=='"':quoted=True
                elif ch=="(":depth+=1
                elif ch==")":
                    depth-=1
                    if depth==0:end=i+1;break
        if end is None:raise SystemExit(f"Malformed {tag} block")
        yield st,end,src[st:end]
        pos=end

def quote(s):
    return '"'+s.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n")+'"'

def setprop(block,name,value):
    pat=re.compile(r'(\(property\s+"'+re.escape(name)+r'"\s+)"((?:\\.|[^"\\])*)"')
    if pat.search(block):
        return pat.sub(lambda m:m.group(1)+quote(value),block,count=1)
    add=f'\n\t\t(property "{name}" {quote(value)} (at 0 0 0) (layer "F.Fab") (hide yes))\n'
    return block[:block.rfind(")")]+add+block[block.rfind(")"):]

# Ref -> manufacturer, MPN, LCSC, short specification.
parts={}
def add(refs,mfr,mpn,lcsc,desc):
    for ref in refs.split():parts[ref]=(mfr,mpn,lcsc,desc)

add("R101 R501 R502 R605 R606 R706","UNI-ROYAL","0402WGF2201TCE","C25879","2.2kΩ ±1%, 62.5mW, 0402, 50V")
add("R103 R403","UNI-ROYAL","0402WGF0000TCE","C17168","0Ω, 0402, 62.5mW")
add("R107 R108","UNI-ROYAL","0402WGF1002TCE","C25744","10kΩ ±1%, 62.5mW, 0402")
add("R701","UNI-ROYAL","0402WGF3902TCE","C25783","39kΩ ±1%, 62.5mW, 0402")
add("R702 R703","UNI-ROYAL","0402WGF5602TCE","C25796","56kΩ ±1%, 62.5mW, 0402")
add("R707","UNI-ROYAL","0402WGF2201TCE","C25879","2.2kΩ ±1%, 62.5mW, 0402")
add("R102","UNI-ROYAL","0402WGF0000TCE","C17168","0Ω, 0402, 62.5mW")
add("C707","FH","0402B472K500NT","C1538","4.7nF, 50V, X7R ±10%, 0402")
add("D605 D606 D702","LITEON","LTST-C190KGKT","C125094","Yellow-green LED, 0603, Vf 2.0V")
add("J501","G-Switch","GT-HD001B-CNNG1","C27636747","HDMI-A 19P female, right-angle SMT")
add("J502 J601","JST","BM04B-SRSS-TB(LF)(SN)","C160390","JST SH, 4P, 1.0mm pitch, SMT")
add("J503","JST","BM10B-SURS-TF(LF)(SN)","C5306166","JST SUR, 10P, 0.8mm pitch, SMT; LCSC listing currently out of stock")
add("U1","ST","LIS3DHTR","C15134","3-axis accelerometer, LGA-16 3x3mm")
add("D101 D502 D701","Semtech","RClamp0502BATCT","","2-line ultra-low-capacitance TVS, SOT-523; external procurement")

# The eight 10uF 0805 positions had a Murata MPN but an LCSC code for a different
# Samsung part. Keep the actual populated LCSC part and make the MPN/manufacturer agree.
add("C701 C703 C704 C705 C708 C709 C710 C711","Samsung Electro-Mechanics","CL21A106KAYNNNE","C15850","10uF, 25V, X5R, 0805; check DC-bias effective capacitance against regulator minimum")

def getref(block):
    m=re.search(r'\(property\s+"Reference"\s+"((?:\\.|[^"\\])*)"',block)
    return m.group(1) if m else ""

updates=[];seen=set()
for st,en,block in blocks(src,"footprint"):
    ref=getref(block)
    if ref not in parts:continue
    mfr,mpn,lcsc,desc=parts[ref]
    block=setprop(block,"Manufacturer_Part_Number",mpn)
    block=setprop(block,"Manufacturer_Name",mfr)
    block=setprop(block,"Part Description",desc)
    if lcsc:block=setprop(block,"LCSC",lcsc)
    # Keep legacy fields coherent where they were previously used.
    if re.search(r'\(property\s+"Field6"\s+',block):block=setprop(block,"Field6",mpn)
    if re.search(r'\(property\s+"Field7"\s+',block):block=setprop(block,"Field7",mfr)
    if re.search(r'\(property\s+"Field4"\s+',block) and ref in {"R701","R707","R102"}:block=setprop(block,"Field4","")
    if re.search(r'\(property\s+"Field5"\s+',block) and ref in {"R701","R707","R102"}:block=setprop(block,"Field5","")
    # Correct the Semtech package designation and align pad geometry with the
    # standard SOT-523 footprint (same three-pad pin order, smaller recommended pads).
    if ref in {"D101","D502","D701"}:
        block=block.replace('footprint "Package_TO_SOT_SMD:SOT-416"','footprint "Package_TO_SOT_SMD:SOT-523"',1)
        block=block.replace('"SOT-416"','"SOT-523"')
        block=block.replace('SOT?416*','SOT?523*')
        block=block.replace('(size 0.6 0.5)','(size 0.51 0.4)')
        block=re.sub(r'\(at -0\.65 (-?0\.5 270)\)',r'(at -0.645 \1)',block)
        block=re.sub(r'\(at 0\.65 (0 270)\)',r'(at 0.645 \1)',block)
        # Change only pad shape; remove roundrect-only ratio tokens from rectangular pads.
        block=re.sub(r'(\(pad\s+"?\d+"?\s+smd\s+)roundrect\b',r'\1rect',block)
        block=re.sub(r'\s*\(roundrect_rratio [^)]+\)','',block)
        block=block.replace('SOT-416, https://www.nxp.com/docs/en/package-information/SOT416.pdf','SOT-523 package for Semtech RClamp0502BA')
        block=block.replace('Package_TO_SOT_SMD.3dshapes/SOT-416.wrl','Package_TO_SOT_SMD.3dshapes/SOT-523.wrl')
        block=setprop(block,"Footprint","Package_TO_SOT_SMD:SOT-523")
    updates.append((st,en,block));seen.add(ref)

missing=set(parts)-seen
if missing:raise SystemExit(f"Could not find PCB footprints for {sorted(missing)}")
for st,en,block in reversed(updates):
    src=src[:st]+block+src[en:]
pcb.write_text(src,encoding="utf-8")

# Update placed-symbol footprint properties in every sheet and the embedded library
# symbol definition so the next schematic/PCB sync retains SOT-523.
for sch in root.glob("*.kicad_sch"):
    s=sch.read_text(encoding="utf-8",errors="replace")
    for ref in ("D101","D502","D701"):
        token=f'(property "Reference" "{ref}"'
        p=s.find(token)
        if p>=0:
            st=s.rfind("\n\t(symbol",0,p)+2
            if st>=2:
                depth=0;quoted=False;escaped=False;end=None
                for i in range(st,len(s)):
                    ch=s[i]
                    if quoted:
                        if escaped:escaped=False
                        elif ch=="\\":escaped=True
                        elif ch=='"':quoted=False
                    else:
                        if ch=='"':quoted=True
                        elif ch=="(":depth+=1
                        elif ch==")":
                            depth-=1
                            if depth==0:end=i+1;break
                if end:
                    b=s[st:end]
                    b=setprop(b,"Footprint","Package_TO_SOT_SMD:SOT-523")
                    s=s[:st]+b+s[end:]
    # Update the embedded library definition only when it is the RClamp0502BA symbol.
    token='(symbol "RCLAMP0502BA"'
    p=s.find(token)
    if p>=0:
        depth=0;quoted=False;escaped=False;end=None
        for i in range(p,len(s)):
            ch=s[i]
            if quoted:
                if escaped:escaped=False
                elif ch=="\\":escaped=True
                elif ch=='"':quoted=False
            else:
                if ch=='"':quoted=True
                elif ch=="(":depth+=1
                elif ch==")":
                    depth-=1
                    if depth==0:end=i+1;break
        if end:
            b=s[p:end]
            b=setprop(b,"Footprint","Package_TO_SOT_SMD:SOT-523")
            s=s[:p]+b+s[end:]
    sch.write_text(s,encoding="utf-8")

(root/"SMT_BOM_FIELD_COMPLETION_REV_B.md").write_text(
"# Rev.B SMT identifier corrections\n\n"
"Populated manufacturer MPN, manufacturer and LCSC fields for the 21 previously unnumbered references; "
"corrected the stale value/MPN/LCSC mappings on R102, R701, R702, R703 and R707; "
"and aligned the eight 10uF capacitors with the Samsung MPN corresponding to their C15850 LCSC code. "
"Semtech RClamp0502BATCT remains an external-procurement item. J503 uses JST BM10B-SURS-TF(LF)(SN), "
"but the LCSC listing C5306166 was out of stock at the last catalog check. "
"The Semtech ESD parts were changed to the SOT-523 package and the board pad geometry was updated to the standard SOT-523 footprint. "
"Catalog stock, alternates, solder paste/land-pattern fit and the effective capacitance of the 10uF X5R parts under DC bias remain to be checked before PCBA release.\n",
encoding="utf-8")
print(f"Populated SMT identifiers for {len(seen)} references; updated RClamp footprint to SOT-523.")
