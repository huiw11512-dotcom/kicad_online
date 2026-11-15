#!/usr/bin/env python3
"""Build a trustworthy SMT BOM from the PCB's actual footprint properties.

The previous export requested only a schematic field literally named P/N.
That omitted valid LCSC, LCSC Part, Manufacturer_Part_Number and Field6 fields.
This script keeps distributor SKUs separate from manufacturer part numbers and
fails closed on known value/package contradictions.
"""
from pathlib import Path
import csv,re,sys,json

board=Path(sys.argv[1])
out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
text=board.read_text(encoding="utf-8",errors="replace")

def iter_blocks(src,tag):
    needle="("+tag
    pos=0
    while True:
        start=src.find(needle,pos)
        if start<0:return
        # Ensure tag boundary.
        after=start+len(needle)
        if after<len(src) and not src[after].isspace() and src[after]!=")":pos=after;continue
        depth=0;quoted=False;escaped=False;end=None
        for i in range(start,len(src)):
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
        if end is None:raise SystemExit(f"Malformed {tag} expression at {start}")
        yield src[start:end]
        pos=end

def unq(s):
    return s.replace(r'\"','"').replace(r'\\','\\').replace(r'\n','\n').replace(r'\t','\t')

def getprops(block):
    return {unq(m.group(1)):unq(m.group(2)) for m in re.finditer(
        r'\(property\s+"((?:\\.|[^"\\])*)"\s+"((?:\\.|[^"\\])*)"',block)}

def norm(s):return re.sub(r'\s+',' ',(s or '').strip())

def resistor_ohms(s):
    v=(s or "").strip().lower().replace("ω","r")
    if v in {"0r","0","0ohm","0 ohm"}:return 0.0
    m=re.fullmatch(r'(\d+(?:\.\d+)?)([rk])(\d+)?',v)
    if not m:return None
    a=float(m.group(1));unit=m.group(2);tail=m.group(3)
    if tail:
        return float(f"{m.group(1)}.{tail}")*(1000 if unit=="k" else 1)
    return a*(1000 if unit=="k" else 1)

rows=[]
for block in iter_blocks(text,"footprint"):
    props=getprops(block)
    ref=props.get("Reference","").strip()
    if not ref or ref.startswith("kibuzzard-") or re.fullmatch(r"H\d+",ref) or re.fullmatch(r"TP\d+",ref) or ref in {"M701","M702","Module301","Module302"}:
        continue
    value=norm(props.get("Value",""))
    fp=(re.match(r'\(footprint\s+"((?:\\.|[^"\\])*)"',block) or [None,""])[1]
    fp=unq(fp)
    dnp=bool(re.search(r'\(attr\s+dnp\)',block)) or props.get("DNP","").lower() in {"yes","true","1"}
    manufacturer=norm(props.get("Manufacturer_Name") or props.get("Manufacturer") or props.get("Field7") or "")
    lcsc=norm(props.get("LCSC") or props.get("LCSC Part") or "")
    direct_mpn=norm(props.get("Manufacturer_Part_Number") or props.get("MPN") or props.get("P/N") or "")
    f6=norm(props.get("Field6",""))
    f5=norm(props.get("Field5",""))
    distributor=norm(props.get("Field4",""))
    distributor_pn=f5 if distributor else ""
    candidate=direct_mpn
    source="explicit MPN field" if direct_mpn else ""
    notes=[]
    if not candidate and f6 and manufacturer:
        candidate=f6;source="Field6 + Manufacturer"
    elif not candidate and f6 and not manufacturer:
        candidate=f6;source="Field6 (manufacturer blank)"
        notes.append("Confirm manufacturer identity; Field6 is not independently verified")
    elif not candidate and f5 and not distributor:
        candidate=f5;source="Field5-only candidate"
        notes.append("Verify Field5 is manufacturer MPN, not distributor SKU")
    desc=norm(props.get("Part Description") or props.get("Description") or "")
    datasheet=norm(props.get("Datasheet",""))
    # Detect stale resistor BOM fields against the current PCB value.
    r_value=resistor_ohms(value)
    if r_value is not None and desc:
        dm=re.search(r'(\d+(?:\.\d+)?)\s*(k|ohm|r)\b',desc.lower())
        if dm:
            expected=float(dm.group(1))*(1000 if dm.group(2)=="k" else 1)
            if abs(expected-r_value)>max(0.01,0.001*r_value):
                notes.append(f"STALE RESISTOR DESCRIPTION: PCB value {value} conflicts with description {dm.group(0)}")
    if re.search(r'R_0402|C_0402|1005Metric',fp) and re.search(r'\bM2012\b|2012\s*\(2012 Metric\)',desc,re.I):
        notes.append("PACKAGE MISMATCH: description says 2012/0805 while PCB footprint is 0402/1005")
    if re.search(r'R_0805|C_0805|2012Metric',fp) and re.search(r'\bM1005\b|1005\s*\(1005 Metric\)',desc,re.I):
        notes.append("PACKAGE MISMATCH: description says 1005/0402 while PCB footprint is 0805/2012")
    conflict=any(x.startswith(("STALE","PACKAGE MISMATCH")) for x in notes)
    if conflict:
        status="BLOCKED_CONFLICT"
    elif dnp:
        status="DNP"
    elif candidate or lcsc:
        status="IDENTIFIER_PRESENT_REQUIRES_CATALOG_CHECK"
    else:
        status="MISSING_MPN_AND_LCSC"
    rows.append({
        "Reference":ref,"Qty":1,"Value":value,"Footprint":fp,
        "Manufacturer":manufacturer,"ManufacturerPart":candidate,
        "MPN_source":source,"LCSC":lcsc,"Distributor":distributor,
        "DistributorPart":distributor_pn,"Description":desc,
        "Datasheet":datasheet,"DNP":"YES" if dnp else "NO",
        "Status":status,"ReviewNotes":"; ".join(notes)
    })

rows.sort(key=lambda x:x["Reference"])
fields=list(rows[0].keys()) if rows else []
def write(name,data,cols):
    with (out/name).open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore")
        w.writeheader();w.writerows(data)

write("BOM_RefDes_Audit.csv",rows,fields)
active=[r for r in rows if r["DNP"]!="YES"]
bom=[r for r in active if r["Status"]!="BLOCKED_CONFLICT"]
missing=[r for r in active if r["Status"]=="MISSING_MPN_AND_LCSC"]
conflicts=[r for r in active if r["Status"]=="BLOCKED_CONFLICT"]
write("BOM_Parts.csv",bom,["Reference","Qty","Value","Footprint","Manufacturer","ManufacturerPart","LCSC","Description"])
write("BOM_Missing_ManufacturerPart.csv",missing,fields)
write("BOM_MPN_Conflicts.csv",conflicts,fields)
facts={
 "board_footprint_count":len(rows),
 "active_assembly_refs":len(active),
 "dnp_refs":sum(r["DNP"]=="YES" for r in rows),
 "refs_with_candidate_mpn_or_lcsc":sum(bool(r["ManufacturerPart"] or r["LCSC"]) for r in active),
 "refs_missing_both_mpn_and_lcsc":len(missing),
 "refs_with_known_value_or_package_conflicts":len(conflicts),
 "assembly_bom_complete":not missing and not conflicts,
 "note":"Candidate identifiers are not equivalent to catalog-verified availability. See BOM_RefDes_Audit.csv."
}
(out/"bom_audit_summary.json").write_text(json.dumps(facts,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(facts,ensure_ascii=False))
for r in conflicts:print("CONFLICT",r["Reference"],r["Value"],r["ManufacturerPart"],r["ReviewNotes"])
for r in missing:print("MISSING",r["Reference"],r["Value"],r["Footprint"])
