"""Exact symbolic rank-two grouped co-Choi certificates, no dense co-Choi.

Reference u=|00>+t|11>, real t. Phase stabilizer partitions the co-Choi
space into blocks of size at most eight, independent of ambient dimensions.
We only construct these blocks and the p*q by p*q reference inverse.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import product
import argparse
import json
from pathlib import Path
import time
import sympy as sp

t=sp.Symbol('t',real=True,nonnegative=True)
D=t**4+4*t**2+1
den=4*(1+t*t)*D*(t*t+2)*(2*t*t+1)


def phi_entry(i,j,r,s,p,q):
    """Entry (r,s) of (Lambda_p tensor Lambda_q)(|i><j|)."""
    a,b=i; c,d=j; e,f=r; g,h=s
    return (sp.Rational(int(a==c and b==d and e==g and f==h))
            -sp.Rational(int(b==d and e==a and g==c and f==h),2)
            -sp.Rational(int(a==c and f==b and h==d and e==g),2)
            +sp.Rational(int(e==a and f==b and g==c and h==d),4))


def phase_weight(a,b,c,d,p,q):
    v=[0]*(p+q-2)
    for k in (a,c): v[k]+=1
    for k in (b,d):
        if k<2: v[k]-=1
        else: v[p+k-2]+=1
    return tuple(v)


def blocks(p,q):
    basis=list(product(range(p),range(q)))
    idx={v:k for k,v in enumerate(basis)}
    u={(0,0):sp.Integer(1),(1,1):t}
    A=sp.MutableSparseMatrix(p*q,p*q,{})
    for r,s in product(basis,repeat=2):
        value=sum(v*w*phi_entry(i,j,r,s,p,q) for i,v in u.items() for j,w in u.items())
        if value: A[idx[r],idx[s]]=value
    Ai=A.inv()

    @lru_cache(None)
    def lrow(i,r):
        return {idx[s]:sp.factor(sum(v*phi_entry(i,j,r,s,p,q) for j,v in u.items()))
                for s in basis
                if sum(v*phi_entry(i,j,r,s,p,q) for j,v in u.items())!=0}

    @lru_cache(None)
    def sentry(i,r,j,s):
        # Row input i, output r; column input j, output s.
        # S's reversed blocks are L_j A^{-1} L_i^*.
        x=lrow(j,r); y=lrow(i,s)
        return sp.factor(sum(v*Ai[k,l]*w for k,v in x.items() for l,w in y.items()))

    parts=defaultdict(list)
    for i,r in product(basis,repeat=2):
        parts[phase_weight(*i,*r,p,q)].append((i,r))
    out=[]
    seen={}
    for weight,labels in sorted(parts.items()):
        C=sp.Matrix([[phi_entry(j,i,r,s,p,q) for j,s in labels] for i,r in labels])
        S=sp.Matrix([[sentry(i,r,j,s) for j,s in labels] for i,r in labels])
        signature=tuple(C)+tuple(S)
        if signature in seen:
            out[seen[signature]]['multiplicity']+=1
            continue
        seen[signature]=len(out)
        out.append({'weight':weight,'labels':labels,'C':C,'S':S,'multiplicity':1})
    return out,len(parts),A


def coefficient_certificate(H):
    """Hermitian H with polynomial entries: charpoly det(zI+H).

    All nonnegative coefficients imply H>=0, since a negative eigenvalue
    would give a positive real zero. Each coefficient is itself certified
    nonnegative by nonnegative polynomial coefficients in t.
    """
    assert H==H.T
    polynomial=H.charpoly().as_expr()
    z=next(x for x in polynomial.free_symbols if x!=t) if len(polynomial.free_symbols-{t}) else sp.Symbol('lambda')
    coefficients=sp.Poly(polynomial,z).all_coeffs()
    # charpoly is det(zI-H); apply alternating signs to get det(zI+H).
    coefficients=[sp.factor((-1)**j*c) for j,c in enumerate(coefficients)]
    facts=[]
    for c in coefficients:
        poly=sp.Poly(c,t)
        expanded_ok=all(v>=0 for v in poly.all_coeffs())
        scalar,factors=sp.factor_list(c,t)
        factor_ok=scalar>=0 and all(power%2==0 or all(v>=0 for v in sp.Poly(f,t).all_coeffs())
                                   for f,power in factors)
        facts.append({'factor':str(c),'nonnegative_coefficients':expanded_ok,
                      'nonnegative_factor_certificate':bool(factor_ok)})
    return all(x['nonnegative_coefficients'] or x['nonnegative_factor_certificate'] for x in facts),facts


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--p',type=int,default=2);parser.add_argument('--q',type=int,default=2)
    args=parser.parse_args();start=time.perf_counter()
    bb,total,A=blocks(args.p,args.q)
    result={'status':'EXACT_SYMBOLIC_CERTIFICATE','p':args.p,'q':args.q,
            'reference':'|00>+t|11>, t>=0','positive_scaling':str(den),
            'total_phase_blocks':total,'unique_ordered_blocks':len(bb),'blocks':[]}
    for k,b in enumerate(bb):
        rec={'index':k,'dimension':b['C'].rows,'multiplicity':b['multiplicity'],
             'representative_weight':b['weight'],'representative_labels':b['labels']}
        for name,HH,scale in [('C_minus_S',b['C']-b['S'],1),('S_plus_3C',b['S']+3*b['C'],1),
                             ('S_plus_11C_over9',b['S']+sp.Rational(11,9)*b['C'],9)]:
            H=(scale*den*HH).applyfunc(sp.cancel)
            assert all(not sp.denom(v).has(t) for v in H)
            ok,facts=coefficient_certificate(H)
            rec[name]={'certified':ok,'det_zI_plus_H_coefficients':facts}
        result['blocks'].append(rec)
        print('block',k,'size',rec['dimension'],'mult',rec['multiplicity'],
              {name:rec[name]['certified'] for name in ['C_minus_S','S_plus_3C','S_plus_11C_over9']},flush=True)
    result['elapsed_code_seconds']=time.perf_counter()-start
    result['all_certified']=all(b[n]['certified'] for b in result['blocks'] for n in ['C_minus_S','S_plus_3C','S_plus_11C_over9'])
    path=Path(__file__).with_name(f'rank2_p{args.p}_q{args.q}.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print('saved',path,'all_certified',result['all_certified'],'code_seconds',result['elapsed_code_seconds'])


if __name__=='__main__':main()
