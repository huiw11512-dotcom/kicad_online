#!/usr/bin/env python3
"""Snapshot embedded schematic symbols into local project libraries.
The cache is retained; mechanical switch/connector pins are typed passive.
"""
from pathlib import Path
from collections import defaultdict
import re, hashlib

root=Path("cm5_mini_host")
files=sorted(root.glob("*.kicad_sch"))
if not files: raise SystemExit("No hierarchical schematics found")

def expr_end(s,k):
    d=0; q=False; e=False
    for i in range(k,len(s)):
        c=s[i]
        if q:
            if e:e=False
            elif c=="\\":e=True
            elif c=='"':q=False
        elif c=='"':q=True
        elif c=="(":d+=1
        elif c==")":
            d-=1
            if d==0:return i+1
    raise ValueError(f"Unbalanced S-expression at {k}")

def children(s,start,end):
    i=s.find("\n",start)+1
    while i<end-1:
        while i<end-1 and s[i].isspace():i+=1
        if i>=end-1:break
        if s[i]!="(":raise ValueError(f"Unexpected token at {i}")
        j=expr_end(s,i)
        yield i,j,s[i:j]
        i=j

passive={"MK-11C04-G013","TS-1010A-B","SM02B-SRSS-TB(LF)(SN)"}
def passive_base(cache_name):
    for target in passive:
        if cache_name==target or cache_name.startswith(target+"_"):
            return target
    return None
libs=defaultdict(dict)
pin_fixes=[]
for path in files:
    original=path.read_text(encoding="utf-8")
    src=original
    cache_defs={}
    for m in reversed(list(re.finditer(r"\(lib_symbols\b",src))):
        start=m.start(); end=expr_end(src,start); rebuilt=[]
        for a,b,expr in children(src,start,end):
            sm=re.match(r'\(symbol\s+"([^"]+)"',expr)
            if not sm:
                rebuilt.append(expr); continue
            cache_name=sm.group(1)
            if passive_base(cache_name):
                n=expr.count("(pin unspecified line")
                if n:
                    expr=expr.replace("(pin unspecified line","(pin passive line")
                    pin_fixes.append((path.name,"embedded",cache_name,n))
            cache_defs[cache_name]=expr
            if ":" in cache_name:
                nick,name=cache_name.split(":",1)
                library_expr=expr.replace(f'(symbol "{cache_name}"',f'(symbol "{name}"',1)
                digest=hashlib.sha256(library_expr.encode()).hexdigest()
                old=libs[nick].get(name)
                if old and hashlib.sha256(old.encode()).hexdigest()!=digest:
                    raise SystemExit(f"Conflicting cached symbol definitions: {nick}:{name}")
                libs[nick][name]=library_expr
            # Keep the cached symbol's original name in the schematic.
            rebuilt.append(expr)
        new="(lib_symbols\n"+"\n".join("\t\t"+x.replace("\n","\n\t\t") for x in rebuilt)+"\n\t)"
        src=src[:start]+new+src[end:]

    # Legacy symbols can have an unqualified cache name and a separate lib_name alias.
    for im in re.finditer(r'\(lib_id "([^"]+)"\)',original):
        libid=im.group(1)
        if ":" not in libid: continue
        nick,name=libid.split(":",1)
        inst_start=original.rfind("\n\t(symbol",0,im.start())+2
        if inst_start<2: continue
        inst_end=expr_end(original,inst_start)
        instance=original[inst_start:inst_end]
        lm=re.search(r'\(lib_name "([^"]+)"\)',instance)
        if not lm: continue
        cache_name=lm.group(1)
        cached=cache_defs.get(cache_name)
        if cached is None: continue
        # Rename both the top-level symbol and all unit/body symbol identifiers.
        pattern=re.compile(r'(\\(symbol\\s+")'+re.escape(cache_name)+r'(?=[_"])')
        library_expr=pattern.sub(lambda m:m.group(1)+name,cached)
        digest=hashlib.sha256(library_expr.encode()).hexdigest()
        old=libs[nick].get(name)
        # Prefer an already fully-qualified cache definition. Only use the alias
        # when the corresponding library symbol is otherwise absent.
        if old is None:
            libs[nick][name]=library_expr

    path.write_text(src,encoding="utf-8")

out=root/"EmbeddedSymbols"; out.mkdir(exist_ok=True)
rows=[]
for nick,symbols in sorted(libs.items()):
    safe=re.sub(r"[^A-Za-z0-9_.-]+","_",nick)
    body='(kicad_symbol_lib\n\t(version 20231120)\n\t(generator "kicad_symbol_editor")\n\t(generator_version "10.0")\n'
    for name,expr in sorted(symbols.items()):
        body+="\t"+expr.replace("\n","\n\t")+"\n"
    body+=")\n"
    (out/f"{safe}.kicad_sym").write_text(body,encoding="utf-8")
    rows.append(f'\t(lib (name "{nick}")(type "KiCad")(uri "${{KIPRJMOD}}/EmbeddedSymbols/{safe}.kicad_sym")(options "")(descr "Exact project-local snapshot of embedded schematic symbols"))')
(root/"sym-lib-table").write_text("(sym_lib_table\n"+"\n".join(rows)+"\n)\n",encoding="utf-8")
(root/"SYMBOL_SNAPSHOT_REV_B_AUDIT.md").write_text(
    "# Rev.B embedded-symbol library snapshot\n\n"
    f"- Local symbol libraries: {len(libs)}\n"
    f"- Cached symbol definitions: {sum(len(x) for x in libs.values())}\n"
    f"- Passive-contact pin type corrections: {sum(x[3] for x in pin_fixes)} pins in {len(pin_fixes)} symbol instances\n\n"
    "The libraries preserve the symbols cached by the source schematic. Mechanical switch contacts and the two-pin JST connector are typed passive to reflect their physical electrical behavior. This is not a substitute for checking the connector pin map or switch truth table.\n\n"
    + "\n".join(f"- {f}: {lib}:{name}, {n} pins" for f,lib,name,n in pin_fixes)+"\n",encoding="utf-8")
print(f"Created {len(libs)} local symbol libraries / {sum(len(x) for x in libs.values())} symbols; passive pin corrections={sum(x[3] for x in pin_fixes)}.")
