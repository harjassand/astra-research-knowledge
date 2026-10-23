"""Construct a finite all-depth star-four certificate with two module classes.
The exact local port lemma is proved in PROOF.md. No solver is used.
"""
from itertools import product, permutations, combinations_with_replacement
from pathlib import Path
from time import perf_counter, process_time
import json, resource

COLORS=range(4)
PERMS=tuple(permutations(COLORS))
L=((0,0,1,1,1,1),(0,1,2,2,0,0))
N=((0,0,1,2,0,0),(0,0,1,2,1,1),(0,1,1,0,0,0),
   (0,1,1,2,0,0),(0,1,1,2,1,0),(0,1,2,0,0,0),
   (0,1,2,0,0,1),(0,1,2,3,0,1),(0,1,2,3,1,0))
FAMILIES={'L':L,'N':N}

def canonical_map(sig):
    used=[]
    for c in sig[:4]:
        if c not in used:used.append(c)
    used += [c for c in COLORS if c not in used]
    return tuple(used.index(c) for c in COLORS)

def transform(sig,p):
    return tuple(p[c] for c in sig[:4])+tuple(sig[4:])

def canonical(sig):
    return transform(sig,canonical_map(sig))

def output_family(kind,children):
    return 'L' if kind=='P' and children==('N','N','N') else 'N'

def candidates(kind,classes,families=None):
    table=FAMILIES if families is None else families
    for raw in product(*(table[c] for c in classes)):
        first=raw[0]
        if kind=='S':
            aligned={transform(raw[1],p) for p in PERMS if p[raw[1][0]]==first[1]}
            for last in sorted(aligned):
                if first[3]==last[2] and (first[5] or last[4]):continue
                out=(first[0],last[1],first[2],last[3],first[4],last[5])
                p=canonical_map(out)
                yield canonical(out),[transform(first,p),transform(last,p)]
        else:
            c,d=first[:2]
            aligned=[sorted({transform(s,p) for p in PERMS if p[s[0]]==c and p[s[1]]==d}) for s in raw[1:]]
            for tail in product(*aligned):
                child=(first,)+tail
                left=[s[2] for s in child];right=[s[3] for s in child]
                if any(s[4] and left.count(s[2])>1 for s in child):continue
                if any(s[5] and right.count(s[3])>1 for s in child):continue
                for a,b in product(COLORS,repeat=2):
                    if a==c or b==d:continue
                    if any(s[4] and s[2]==a for s in child):continue
                    if any(s[5] and s[3]==b for s in child):continue
                    out=(a,b,c,d,int(a in left),int(b in right))
                    p=canonical_map(out)
                    yield canonical(out),[transform(s,p) for s in child]

def construct():
    rows=[]
    cases=[('S',x) for x in product(('L','N'),repeat=2)]
    cases += [('P',x) for k in (2,3) for x in combinations_with_replacement(('L','N'),k)]
    for kind,classes in cases:
        parent=output_family(kind,classes)
        targets=set(FAMILIES[parent]);witness={}
        for out,children in candidates(kind,classes):
            if out in targets and out not in witness:
                witness[out]={'parent_signature':out,'child_signatures':children}
                if len(witness)==len(targets):break
        if set(witness)!=targets:raise AssertionError((kind,classes,targets-set(witness)))
        rows.append({'kind':kind,'child_classes':classes,'parent_class':parent,
                     'witnesses':[witness[s] for s in FAMILIES[parent]]})
    return {'schema':'astra-star-four-two-family-certificate/v1',
            'palette_size':4,'signature_order':['s','t','neighbor_s','neighbor_t','left_flag','right_flag'],
            'leaf':'two-edge path','families':FAMILIES,'transitions':rows,
            'case_count':len(rows),'witness_count':sum(len(x['witnesses']) for x in rows)}

if __name__=='__main__':
    t=perf_counter();cpu=process_time()
    cert=construct()
    elapsed=perf_counter()-t
    out=Path(__file__).resolve().parents[1]/'results'
    out.mkdir(exist_ok=True)
    (out/'star_four_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    cost={'wall_seconds':elapsed,'cpu_seconds':process_time()-cpu,
          'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
          'case_count':cert['case_count'],'witness_count':cert['witness_count'],
          'scope':'Wall interval: exact witness construction, excluding serialization/startup. CPU interval additionally includes certificate serialization. Inference and proof preparation unknown.'}
    (out/'certificate_construction_cost.json').write_text(json.dumps(cost,indent=2)+'\n')
    print(json.dumps(cost))

