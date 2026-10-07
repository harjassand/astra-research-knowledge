import json
from itertools import product

def spectrum(L,s):
    n=L*L
    edges=[(r*L+c,r*L+c+1) for r in range(L) for c in range(L-1)]+[(r*L+c,(r+1)*L+c) for r in range(L-1) for c in range(L)]
    counts={}
    ground=[]
    for bits in product((0,1),repeat=n):
        energy=sum(bits[u]!=bits[v] for u,v in edges)+(bits[0]!=s)
        counts[energy]=counts.get(energy,0)+1
        if energy==0: ground.append(bits)
    return {"L":L,"pin":s,"ground_degeneracy":counts[0],"gap":min(e for e in counts if e>0),"ground_configuration":ground[0],"energy_multiplicities":counts}

if __name__=="__main__":
    records=[spectrum(L,s) for L in (2,3) for s in (0,1)]
    print(json.dumps({"records":records,"proof_scope":"Finite enumeration diagnoses the explicit family; general claims follow from integer penalties and graph connectedness in REPORT.md."},indent=2))
