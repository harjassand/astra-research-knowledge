"""Exact finite generalized spectra for flat references; no extrapolation proof.

Builds character blocks rather than the full co-Choi matrix. The reference
is u=sum_{j<r}|jj> in C^r tensor C^r. Uses the analytic reference inverse
A^-1=I/(r-1)-uu*/((r-1)(5r-4)).
"""
from collections import defaultdict
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse,json,time
import sympy as sp


def phase(a,b,c,d,r):
    w=[0]*r;w[a]+=1;w[c]+=1;w[b]-=1;w[d]-=1
    return tuple(w)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--rank',type=int,default=3)
    r=parser.parse_args().rank;assert r>=2
    start=time.perf_counter()
    basis=list(product(range(r),repeat=2))
    @lru_cache(None)
    def row(i,z):
        a,b=i;c,d=z;v=defaultdict(lambda:sp.Rational(0))
        if a==b:v[c,d]+=1
        if c==a:v[b,d]-=sp.Rational(1,2)
        if d==b:v[c,a]-=sp.Rational(1,2)
        if c==a and d==b:
            for k in range(r):v[k,k]+=sp.Rational(1,4)
        return {k:v for k,v in v.items() if v}
    @lru_cache(None)
    def sentry(i,z,j,w):
        x=row(j,z);y=row(i,w)
        return (sp.Rational(1,r-1)*sum(v*y.get(k,0) for k,v in x.items())
                -sp.Rational(1,(r-1)*(5*r-4))*sum(v for k,v in x.items() if k[0]==k[1])*sum(v for k,v in y.items() if k[0]==k[1]))
    def cinv_entry(i,z,j,w):
        a,b=i;c,d=z;e,f=j;g,h=w
        return sp.Rational(4,9)*(2*int(a==e and c==g)+int(a==g and c==e))*(2*int(b==f and d==h)+int(b==h and d==f))
    parts=defaultdict(list)
    for i,z in product(basis,repeat=2):parts[phase(*i,*z,r)].append((i,z))
    seen={};types=[]
    for weight,labels in sorted(parts.items()):
        S=sp.Matrix([[sentry(i,z,j,w) for j,w in labels] for i,z in labels])
        Ci=sp.Matrix([[cinv_entry(i,z,j,w) for j,w in labels] for i,z in labels])
        signature=tuple(S)+tuple(Ci)
        if signature in seen:
            types[seen[signature]]['multiplicity']+=1
            continue
        seen[signature]=len(types)
        P=Ci*S
        assert P==P.applyfunc(sp.Rational)
        cp=P.charpoly().as_expr();factored=sp.factor(cp)
        types.append({'dimension':len(labels),'multiplicity':1,'weight':weight,
                      'generalized_characteristic_polynomial':str(factored)})
        print('newtype',len(types)-1,'dim',len(labels),'poly',factored,flush=True)
    out={'status':'EXACT_FINITE_FLAT_REFERENCE_SPECTRA_NO_GENERAL_RANK_PROOF',
         'rank':r,'dims':[r,r],'reference':'sum_i |ii>','phase_block_count':len(parts),
         'types':types,'elapsed_code_seconds':time.perf_counter()-start}
    Path(__file__).with_name(f'flat_rank_{r}.json').write_text(json.dumps(out,indent=2)+'\n')
    print('saved rank',r,'seconds',out['elapsed_code_seconds'])


if __name__=='__main__':main()
