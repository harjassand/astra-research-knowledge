#!/usr/bin/env python3
"""Audit a proposed covalent, chemically specified E. coli 23S construction.

This computes sequences, bookkeeping and an explicitly conditional yield model.
It does NOT simulate ribosome folding, ligation yield, fidelity, or translation.
Uses only Python's standard library and the captured public input files.
"""
from pathlib import Path
import ast
import csv
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
SRC = ROOT / "sources"

MODS = [
    (745,"G","m1G","1MG"),(746,"U","Psi","PSU"),(747,"U","m5U","5MU"),
    (955,"U","Psi","PSU"),(1618,"A","m6A","6MZ"),(1835,"G","m2G","2MG"),
    (1911,"U","Psi","PSU"),(1915,"U","m3Psi","3TD"),(1917,"U","Psi","PSU"),
    (1939,"U","m5U","5MU"),(1962,"C","m5C","5MC"),(2030,"A","m6A","6MZ"),
    (2069,"G","m7G","G7M"),(2251,"G","Gm","OMG"),(2445,"G","m2G","2MG"),
    (2449,"U","D",None),(2457,"U","Psi","PSU"),(2498,"C","Cm","OMC"),
    (2501,"C","ho5C",None),(2503,"A","m2A","2MA"),(2504,"U","Psi","PSU"),
    (2552,"U","Um","OMU"),(2580,"U","Psi","PSU"),(2604,"U","Psi",None),
    (2605,"U","Psi","PSU")
]
# Structural deposition represents 22 sites. The other three are independently
# documented in Ero et al. 2024 Table 1; an omitted PDB modification is NOT absence.
ENZYME_POS = {2069, 2445}
MOD_MAP = {p: dict(position=p, canonical=b, modification=m, pdb_code=c,
                  installation="RlmKL_plus_SAM" if p in ENZYME_POS else "synthetic_patch",
                  evidence="4YBB_entity22" if c else "Ero2024_Table1",
                  occupancy_note="variable occupancy; compare 0 and 1 target variants" if p==2501 else
                  "measure actual enzymatic occupancy" if p in ENZYME_POS else "target 1.0; verify chemically")
           for p,b,m,c in MODS}

embl = (SRC / "V00331.embl").read_text()
seq = re.sub("[^acgt]", "", embl.split("SQ   Sequence",1)[1].split("\n",1)[1]).upper().replace("T","U")
entity = json.loads((SRC / "4YBB_22.json").read_text())
poly = entity["entity_poly"]
assert len(seq) == 2904
assert seq == poly["pdbx_seq_one_letter_code_can"].replace("\n","").replace("X","U")
tokens = re.findall(r"\([A-Z0-9]+\)|[ACGUX]", poly["pdbx_seq_one_letter_code"].replace("\n",""))
assert len(tokens) == 2904
assert len(MODS) == 25 and len(MOD_MAP) == 25
for p,b,m,c in MODS:
    assert seq[p-1] == b, (p,seq[p-1],b)
    if c:
        assert tokens[p-1] == "("+c+")", (p,tokens[p-1],c)
assert sum(t.startswith("(") for t in tokens) == 22

def sha(data):
    return hashlib.sha256(data).hexdigest()

def fasta(path, records):
    with path.open("w") as f:
        for name,s in records:
            f.write(">"+name+"\n")
            for i in range(0,len(s),80): f.write(s[i:i+80]+"\n")

def csvout(path, rows):
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def intervals(positions, max_length=80, margin=12):
    """Greedy equal-cost interval cover with required flanks; minimal count.
    The first uncovered modified site fixes the leftmost permitted interval.
    Taking every next site that fits cannot worsen the number of intervals.
    This is combinatorial coverage, not a chemistry/yield optimization.
    """
    pending=sorted(positions); ans=[]
    while pending:
        start=pending[0]-margin
        chosen=[]
        while pending and pending[0]+margin-start+1 <= max_length:
            chosen.append(pending.pop(0))
        assert chosen
        ans.append((start,chosen[-1]+margin,chosen))
    return ans

def make_design(name, positions):
    chem=sorted(set(positions)-ENZYME_POS)
    patches=intervals(chem)
    pieces=[];last=0
    for lo,hi,marks in patches:
        if lo>last+1:
            pieces.append(dict(start=last+1,end=lo-1,method="IVT_plus_exact_end_processing",marks=[]))
        pieces.append(dict(start=lo,end=hi,method="chemical_synthesis",marks=marks))
        last=hi
    if last<len(seq): pieces.append(dict(start=last+1,end=len(seq),method="IVT_plus_exact_end_processing",marks=[]))
    for i,p in enumerate(pieces,1):
        p.update(id=f"{name}_F{i:02d}",length=p["end"]-p["start"]+1,
                 canonical_sequence=seq[p["start"]-1:p["end"]],
                 terminal_chemistry="5prime_monophosphate__3prime_hydroxyl")
        p["modified_sequence"]="".join("["+MOD_MAP[k]["modification"]+"]" if k in p["marks"] else seq[k-1]
                                      for k in range(p["start"],p["end"]+1))
    assert "".join(p["canonical_sequence"] for p in pieces)==seq
    assert sorted(k for p in pieces for k in p["marks"])==chem
    design=dict(name=name, intended_final_marks=sorted(positions),
                chemical_marks=chem, enzyme_marks=sorted(set(positions)&ENZYME_POS),
                patches=len(patches), fragments=len(pieces), junctions=len(pieces)-1,
                chemical_nt=sum(p["length"] for p in pieces if p["method"]=="chemical_synthesis"),
                pieces=pieces)
    (DATA/(name+".json")).write_text(json.dumps(design,indent=2)+"\n")
    fasta(DATA/(name+"_fragments.fasta"),[(p["id"]+f"__{p['start']}_{p['end']}__"+p["method"],p["canonical_sequence"])for p in pieces])
    csvout(DATA/(name+"_fragments.csv"),[{**p,"marks":";".join(str(x) for x in p["marks"])}for p in pieces])
    return design

full = make_design("full25", MOD_MAP)
# Small designs are comparisons, NOT earned minima for full translation.
core = make_design("core_plus_RlmKL", {2069,2445,2449,2457,2498,2501,2503,2504})
ptc = make_design("ptc13", {2069,2251,2445,2449,2457,2498,2501,2503,2504,2552,2580,2604,2605})
assert full["patches"]==9 and full["fragments"]==19 and full["junctions"]==18
assert full["chemical_nt"]==386

# Copy parameter data from the captured, versioned public Biopython implementation
# without importing or executing that downloaded module.
tree=ast.parse((SRC/"Biopython_1_86_MeltingTemp.py").read_text())
nn=None
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="R_DNA_NN1" for t in node.targets):
        nn=ast.literal_eval(node.value)
assert nn and len([k for k in nn if "/" in k and not k.startswith("init")])==16
comp=str.maketrans("ACGTU","TGCAA")

def nn_hybrid_diagnostic(rna):
    """Unmodified isolated duplex at tabulated reference conditions only.
    No salt/Mg/crowding correction, no RNA unfolding cost, no modified bases.
    Therefore dG is NOT the free energy of splint invasion or rRNA assembly.
    """
    s=rna.replace("U","T");t=s.translate(comp)
    dh,ds=nn["init"]
    for i in range(len(s)-1):
        h,e=nn[s[i:i+2]+"/"+t[i:i+2]];dh+=h;ds+=e
    return {"dH_kcal_mol":round(dh,3),"dS_cal_mol_K":round(ds,3),
            "dG37_kcal_mol_reference_only":round(dh-310.15*ds/1000,3)}

junctions=[]
for p in full["pieces"][:-1]:
    j=p["end"];window=seq[j-12:j+12]
    # Flanks exclude every modification installed BEFORE ligation.
    # G2445 is still canonical here; RlmKL acts only after DNA removal.
    assert not (set(range(j-11,j+13)) & (set(MOD_MAP)-ENZYME_POS))
    splint=window.translate(comp)[::-1]
    assert seq.count(window)==1
    junctions.append(dict(after_position=j,left_id=p["id"],local_rna24=window,
                          diagnostic_dna24_5to3=splint,exact_occurrences=seq.count(window),
                          **nn_hybrid_diagnostic(window)))
csvout(DATA/"full25_junction_diagnostics.csv",junctions)
fasta(DATA/"full25_junction_diagnostics.fasta",[(f"J{j['after_position']}__DNA_24nt_local_diagnostic_NOT_DALI_splint",j["diagnostic_dna24_5to3"])for j in junctions])

# A concrete three-tier synthesis tree. Only purified covalent products advance.
# This is an operation graph, not an assumption of perfect substrate recognition.
nodes=[dict(id=p["id"],start=p["start"],end=p["end"],depth=0,children=[])for p in full["pieces"]]
operations=[];tier=0
while len(nodes)>1:
    tier+=1;new=[]
    for i in range(0,len(nodes),3):
        children=nodes[i:i+3]
        if len(children)==1: new.append(children[0]);continue
        node=dict(id=f"T{tier}_B{i//3+1}",start=children[0]["start"],end=children[-1]["end"],
                  depth=max(c["depth"]for c in children)+1,children=[c["id"]for c in children])
        operations.append(node);new.append(node)
    nodes=new
assert sum(len(n["children"])-1 for n in operations)==18
assert len(operations)==9 and nodes[0]["depth"]==3
(DATA/"full25_assembly_tree.json").write_text(json.dumps(operations,indent=2)+"\n")
fasta(DATA/"full25_long_dna_splints.fasta",[(n["id"]+"__sense_DNA",seq[n["start"]-1:n["end"]].replace("U","T"))for n in operations])
# The FASTA defines one strand of each dsDNA splint; complementary strand implied.

yield_rows=[]
for q in [0.10,0.272,0.50,0.80]:
    for recovery in [0.5,0.8,1.0]:
        amounts={p["id"]:1.0 for p in full["pieces"]}
        for n in operations:
            amounts[n["id"]]=min(amounts[c] for c in n["children"])*q*recovery
        y=amounts[operations[-1]["id"]]
        yield_rows.append(dict(three_piece_ligation_yield_assumed=q,purification_recovery_assumed=recovery,
                              full_length_mol_per_equal_input_mol=round(y,9),
                              input_mol_of_each_fragment_per_output_mol=round(1/y,3),
                              source_note="q=0.272 measured for one unrelated DALI mRNA; NOT an rRNA prediction" if q==0.272 else "hypothetical scenario"))
csvout(DATA/"yield_scenarios.csv",yield_rows)

frontier=[]
for length in [40,60,80,100,150,200]:
    patches=intervals(set(MOD_MAP)-ENZYME_POS,max_length=length)
    frontier.append(dict(max_chemical_patch_nt=length,number_of_patches=len(patches),
                         chemical_nt=sum(hi-lo+1 for lo,hi,_ in patches),
                         fragments=2*len(patches)+1,junctions=2*len(patches),
                         interpretation="combinatorial cover only; chemistry compatibility not scored"))
csvout(DATA/"patch_size_frontier.csv",frontier)

fasta(DATA/"reference_23S_V00331_1.fasta",[("ENA_V00331.1_E_coli_rrnB_23S__RNA__2904nt",seq)])
(DATA/"modification_map.json").write_text(json.dumps(list(MOD_MAP.values()),indent=2)+"\n")
csvout(DATA/"modification_map.csv",list(MOD_MAP.values()))
summary=dict(status="COMPUTED_CONSTRUCTION_ONLY__NO_NEW_EXPERIMENTAL_DEMONSTRATION",
             reference_length_nt=len(seq),reference_sha256=sha(seq.encode()),
             reference_equals_4YBB_entity22=True,structurally_crosschecked_marks=22,
             additional_literature_marks=[2449,2501,2604],target_marks=25,
             chemically_installed_marks=23,enzymatically_installed_marks=2,
             patch_count=9,patch_nt=386,IVT_nt=2518,fragment_count=19,junction_count=18,
             ligation_operations=len(operations),max_purified_ligation_tiers=3,
             isolated_junction_dG37_range_kcal_mol=[min(j["dG37_kcal_mol_reference_only"]for j in junctions),
                                                  max(j["dG37_kcal_mol_reference_only"]for j in junctions)],
             hypothetical_full_length_yield_at_q_0272_recovery_080=round((.272*.8)**3,9),
             absolute_lower_bound_ligation_ATP_per_final_RNA=18,
             absolute_lower_bound_SAM_per_final_RNA=2,
             exact_reference_sequence_reconstructed=True,
             limitations=["No predicted ligation probability or folding pathway", "No claim of native modification occupancies",
                          "No demonstrated full translation, fidelity, usable lifetime or renewable chemistry",
                          "DALI transfer to 2904-nt rRNA and mixed modification patches is untested",
                          "NN diagnostic excludes rRNA unfolding, tertiary interactions, proteins and Mg2+"])
(DATA/"audit_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
