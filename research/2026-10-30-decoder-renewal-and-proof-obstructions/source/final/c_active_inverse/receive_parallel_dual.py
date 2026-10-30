"""Read-only exact intake of ROOT's SAME two-parallel-query dual certificate.

Reconstructs all six Gram-congruent blocks and source-input bounds using
stdlib Fractions; no root imports/solver/model/RNG or source execution.
"""

from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib,json,time


PP=tuple(permutations(range(3)))


def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))


def inv(p):return tuple(p.index(i) for i in range(len(p)))


def cycles(p):
    seen=set();n=0
    for i in range(len(p)):
        if i in seen:continue
        n+=1;j=i
        while j not in seen:seen.add(j);j=p[j]
    return n


def mm(a,b):
    return [[sum(a[i][h]*b[h][j] for h in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def kron(a,b):
    return [[a[i][j]*b[h][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for h in range(len(b))]


def inverse(a):
    n=len(a);b=[[F(v) for v in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        k=next(i for i in range(j,n) if b[i][j]);b[j],b[k]=b[k],b[j]
        z=b[j][j];b[j]=[x/z for x in b[j]]
        for i in range(n):
            if i==j:continue
            z=b[i][j];b[i]=[x-z*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]


def reps():
    out={'trivial':([[[F(1)]] for _ in PP],[[F(1)]]),
         'sign':([[[F((-1)**(3-cycles(p)))]] for p in PP],[[F(1)]])}
    matrices=[]
    for p in PP:
        cols=[]
        for j in range(2):
            v=[0,0,0];v[p[j]]+=1;v[p[2]]-=1;cols.append(v[:2])
        matrices.append([[F(cols[j][i]) for j in range(2)] for i in range(2)])
    out['standard']=(matrices,[[F(2),F(1)],[F(1),F(2)]])
    for matrices,_ in out.values():
        for i,p in enumerate(PP):
            for j,q in enumerate(PP):assert mm(matrices[i],matrices[j])==matrices[PP.index(compose(p,q))]
    return out


def ldl(a):
    n=len(a);L=[[F(0)]*n for _ in range(n)];d=[]
    assert all(a[i][j]==a[j][i] for i in range(n) for j in range(n))
    for j in range(n):
        L[j][j]=1;z=a[j][j]-sum(L[j][h]**2*d[h] for h in range(j));assert z>0;d.append(z)
        for i in range(j+1,n):L[i][j]=(a[i][j]-sum(L[i][h]*L[j][h]*d[h] for h in range(j)))/z
    return d


def main():
    start=time.perf_counter();base=Path(__file__).parent;root=base.parent/'root_comb'
    raw=(root/'PARALLEL_DUAL_CERTIFICATE.json').read_bytes();x=json.loads(raw)
    assert (x['k'],x['r'],x['D'],x['source_queries_in_strategy'])==(2,2,4,2)
    y=[[F(v) for v in row] for row in x['dual_coefficients']]
    gram=[[F(4**cycles(compose(inv(p),q))) for q in PP] for p in PP];gi=inverse(gram)
    rr=reps();records=[]
    for la in ('trivial','standard'):
        aa,ga=rr[la]
        for lb in ('trivial','standard','sign'):
            bb,gb=rr[lb];g=kron(ga,gb);n=len(g);slack=[[F(0)]*n for _ in range(n)]
            for i,p in enumerate(PP):
                for j,q in enumerate(PP):
                    value=-gi[j][i]*F(2)**(cycles(p)-3)/4
                    if i in (0,1):value+=y[i][j] # embedded permutations fix logical output0
                    block=mm(g,kron(aa[i],bb[j]))
                    for a in range(n):
                        for b in range(n):slack[a][b]+=value*block[a][b]
            d=ldl(slack)
            saved=next(z for z in x['positive_blocks'] if z['logical_irrep']==la and z['physical_irrep']==lb)
            assert slack==[[F(v) for v in row] for row in saved['metric_dual_block']]
            assert d==list(map(F,saved['exact_LDL_positive_pivots']))
            records.append({'logical':la,'physical':lb,'all_entries_and_pivots_match':True})
    norms=[sum(4**cycles(p)*(y[0][i]+s*y[1][i]) for i,p in enumerate(PP)) for s in(1,-1)]
    upper=max(norms);assert upper==F(x['parallel_Bell_fidelity_upper'])
    lower=F(json.loads((base/'COHERENT_FEEDBACK.json').read_text())['qualified_feasible_Bell_fidelity'])
    assert lower-upper>F(1,80)
    out={'scope':'exact reconstruction of root SAME k2,r2,D4 all-parallel dual plus saved adaptive lower; no new model/solve',
         'root_certificate_sha256':hashlib.sha256(raw).hexdigest(),'six_reconstructed_blocks':records,
         'input_normalization_values':list(map(str,norms)),
         'parallel_Bell_fidelity_upper':str(upper),'adaptive_CPTP_lower':str(lower),
         'exact_gap':str(lower-upper),'gap_greater_than_1_over_80':True,
         'no_source_model_solver_or_RNG_calls':True,'seconds_after_imports':time.perf_counter()-start}
    (base/'PARALLEL_INTAKE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
