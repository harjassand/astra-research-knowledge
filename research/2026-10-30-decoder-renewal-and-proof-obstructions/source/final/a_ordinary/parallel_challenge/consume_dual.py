"""Independent stdlib/Fraction consumption of root's saved two-query dual.

No producer imports, solver, source queries, Haar samples or quantum execution.
Reconstructs the complete S3 Gram, sparse native Choi moments, rational irreps,
six operator blocks, LDL pivots and two input normalization sectors.
"""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import hashlib
import json
import time


def zero(n,m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def eye(n):
    a=zero(n)
    for i in range(n): a[i][i]=F(1)
    return a


def mul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def trans(a): return list(map(list,zip(*a)))


def kron(a,b):
    return [[x*y for x in ra for y in rb] for ra in a for rb in b]


def add_scaled(a,b,s):
    for i,row in enumerate(b):
        for j,v in enumerate(row): a[i][j]+=s*v


def inverse(a):
    n=len(a);v=[row[:]+e for row,e in zip(a,eye(n))]
    for j in range(n):
        p=next(i for i in range(j,n) if v[i][j])
        v[p],v[j]=v[j],v[p]
        c=v[j][j];v[j]=[x/c for x in v[j]]
        for i in range(n):
            if i==j: continue
            c=v[i][j];v[i]=[x-c*y for x,y in zip(v[i],v[j])]
    out=[row[n:] for row in v]
    assert mul(a,out)==eye(n)
    return out


def compose(p,q): return tuple(p[x] for x in q)


def inv(p): return tuple(p.index(i) for i in range(len(p)))


def cycles(p):
    seen=set();c=0
    for i in range(len(p)):
        if i in seen: continue
        c+=1
        while i not in seen:
            seen.add(i);i=p[i]
    return c


def action(p,x):
    y=[None]*len(p)
    for i in range(len(p)): y[p[i]]=x[i]
    return tuple(y)


def reps(pp):
    standard=[]
    # Columns of e_p(j)-e_p(2), expressed in (e0-e2,e1-e2).
    for p in pp:
        a=zero(2)
        for j in range(2):
            v=[0,0,0];v[p[j]]+=1;v[p[2]]-=1
            for i in range(2): a[i][j]=F(v[i])
        standard.append(a)
    out={'trivial':([[[F(1)]] for p in pp],[[F(1)]]),
         'standard':(standard,[[F(2),F(1)],[F(1),F(2)]]),
         'sign':([[[F((-1)**(3-cycles(p)))]] for p in pp],[[F(1)]])}
    for rr,g in out.values():
        for i,p in enumerate(pp):
            assert mul(mul(trans(rr[i]),g),rr[i])==g
            for j,q in enumerate(pp):
                assert mul(rr[i],rr[j])==rr[pp.index(compose(p,q))]
    return out


def ldl(a):
    assert trans(a)==a
    n=len(a);l=eye(n);d=[]
    for j in range(n):
        z=a[j][j]-sum(l[j][i]**2*d[i] for i in range(j))
        assert z>0
        d.append(z)
        for i in range(j+1,n):
            l[i][j]=(a[i][j]-sum(l[i][h]*l[j][h]*d[h] for h in range(j)))/z
    dd=zero(n)
    for i,v in enumerate(d): dd[i][i]=v
    assert mul(mul(l,dd),trans(l))==a
    return d


def native_moment(s,t,k=2,r=2):
    # Direct sparse trace(P_s^A tensor P_t^B J_N^tensor3)/k^2 for U=I.
    # One native Choi entry: row(a,a*r+f), col(c,c*r+f), coefficient1/r.
    total=0
    for a in product(range(k),repeat=3):
        ap=action(s,a)
        for f in product(range(r),repeat=3):
            b=tuple(a[i]*r+f[i] for i in range(3))
            bp=tuple(ap[i]*r+f[i] for i in range(3))
            if action(t,b)==bp: total+=1
    return F(total,r**3*k**2)


def main():
    start=time.perf_counter()
    folder=Path(__file__).resolve().parent
    source=folder.parent.parent/'root_comb/PARALLEL_DUAL_CERTIFICATE.json'
    raw=source.read_bytes();cert=json.loads(raw)
    assert (cert['k'],cert['r'],cert['D'],cert['source_queries_in_strategy'])==(2,2,4,2)
    pp=list(permutations(range(3)));aa=list(permutations(range(2)))
    gram=[[F(4**cycles(compose(inv(p),q))) for q in pp] for p in pp]
    gi=inverse(gram)
    omega=[[gi[j][i]*F(2)**(cycles(s)-3)/4 for j in range(6)] for i,s in enumerate(pp)]
    moment_count=0
    for s in pp:
        for t in pp:
            got=native_moment(s,t)
            wanted=F(2**cycles(compose(s,inv(t))))*F(2)**(cycles(t)-3)/4
            assert got==wanted
            moment_count+=1
    # Physical twirl/full transpose leaves this exact coefficient tensor fixed.
    for i,p in enumerate(pp):
        for j,q in enumerate(pp):
            assert omega[i][j]==omega[pp.index(inv(p))][pp.index(inv(q))]
    y=[[F(v) for v in row] for row in cert['dual_coefficients']]
    for row in y:
        for j,p in enumerate(pp): assert row[j]==row[pp.index(inv(p))]
    rr=reps(pp);records=[]
    for aname in ('trivial','standard'):
        ra,ga=rr[aname]
        for bname in ('trivial','standard','sign'):
            rb,gb=rr[bname];metric=kron(ga,gb);block=zero(len(metric))
            for i in range(6):
                for j in range(6):
                    add_scaled(block,mul(metric,kron(ra[i],rb[j])),-omega[i][j])
            for a,row in zip(aa,y):
                embed=(0,a[0]+1,a[1]+1);i=pp.index(embed)
                for j,v in enumerate(row):
                    add_scaled(block,mul(metric,kron(ra[i],rb[j])),v)
            pivots=ldl(block)
            saved=next(z for z in cert['positive_blocks'] if
                       (z['logical_irrep'],z['physical_irrep'])==(aname,bname))
            assert block==[[F(v) for v in row] for row in saved['metric_dual_block']]
            assert pivots==list(map(F,saved['exact_LDL_positive_pivots']))
            records.append(dict(logical=aname,physical=bname,size=len(block),
                                positive_pivots=list(map(str,pivots))))
    sectors=[sum(F(4**cycles(p))*(y[0][j]+sign*y[1][j]) for j,p in enumerate(pp))
             for sign in (1,-1)]
    upper=F(cert['parallel_Bell_fidelity_upper'])
    assert sectors==list(map(F,cert['input_symmetry_sector_values']))
    assert all(z<=upper for z in sectors)
    adaptive=F(55716029295809,123760695281664)
    assert adaptive>upper
    receipt=dict(status='PASS_EXACT_INDEPENDENT_CONSUMER',
                 source=str(source),source_sha256=hashlib.sha256(raw).hexdigest(),
                 consumer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 native_sparse_choi_moments=moment_count,
                 transpose_coefficient_identity=True,group_multiplication_and_metric=True,
                 complete_positive_blocks=records,input_sector_values=list(map(str,sectors)),
                 parallel_upper=str(upper),conditional_adaptive_comparison_gap=str(adaptive-upper),
                 mathematical_model_scope='whole model challenged separately in REVIEW.md',
                 source_queries=0,quantum_runs=0,optimizer_runs=0,
                 producer_imports=False,seconds=time.perf_counter()-start)
    (folder/'EXACT_CONSUMPTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ('status','native_sparse_choi_moments',
          'parallel_upper','conditional_adaptive_comparison_gap','seconds')},indent=2))


if __name__=='__main__': main()
