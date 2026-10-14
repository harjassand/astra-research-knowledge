#!/usr/bin/env python3
"""Try to extend one rational cycle potential to every positive strip width.

For each fixed profile edge, exact Laurent integration gives
W(t)=c0*t+c1+c2/t+c3/t^2+c4/t^3. Multiplying W(t)-dV by t^3
produces a rational quartic. Exact Sturm root isolation checks its sign on
(0,infinity); this is a separate, stronger test than the five sampled widths.
"""
from fractions import Fraction as Q
from pathlib import Path
import json, sys
import sympy as S

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'incoming_resonant'))
from profile_algebra import add,scale,mul,cos,sin,meanprod,poly_terms,edge_coeffs,r,s,p,q

def energy(n,m):
    a=add(scale(cos(n),p),scale(cos(m),q)); c=add(scale(sin(n),p),scale(sin(m),q))
    b=add(scale(sin(n),-n*r),scale(sin(m),-m*s)); d=add(scale(cos(n),n*r),scale(cos(m),m*s))
    u=add(mul(a,a),mul(c,c)); v=add(mul(b,b),mul(d,d)); w=add(mul(a,b),mul(c,d)); det=add(mul(a,d),scale(mul(b,c),-1))
    F=meanprod(u,u)+meanprod(v,v)+4*meanprod(w,w)+Q(17,5)*meanprod(det,det)-Q(29,10)*meanprod(det,add(u,v))
    return poly_terms(F)

def nonnegative_on_positive(poly,t):
    p=S.Poly(poly,t,domain=S.QQ)
    while p.eval(0)==0:
        p=p.exquo(S.Poly(t,t,domain=S.QQ))
    roots=p.intervals(eps=S.Rational(1,10**12))
    pos=[]
    for (lo,hi),mult in roots:
        if hi<=0: continue
        if lo<0:
            # The zero root was removed above; a positive root is isolated
            # strictly unless the requested precision was unexpectedly poor.
            raise AssertionError((lo,hi,mult))
        pos.append((lo,hi,mult))
    if not pos:
        return p.eval(1)>=0, []
    samples=[]
    first=pos[0][0]
    samples.append(first/2 if first>0 else pos[0][1]+1)
    for (lo1,hi1,_),(lo2,hi2,_) in zip(pos,pos[1:]):
        samples.append((hi1+lo2)/2)
    samples.append(pos[-1][1]+1)
    signs=[S.sign(p.eval(x)) for x in samples]
    return all(vv>=0 for vv in signs), [(str(x),int(vv)) for x,vv in zip(samples,signs)]

def main():
    runs=json.loads((ROOT/'exact_cycle_search.json').read_text())
    source=runs[0]
    assert source['carriers']==[1,-1] and source['profile_box']==['0','2']
    vertices=[(Q(i,4),Q(j,4)) for i in range(9) for j in range(9)]
    potential=[Q(v) for v in source['potential']]
    terms=energy(1,-1); tau=S.symbols('tau',positive=True)
    failures=[]; root_edges=0; checked=0; min_coeff_signs=None
    for i,a in enumerate(vertices):
        for j,b in enumerate(vertices):
            co=edge_coeffs(terms,a,b)
            delta=potential[j]-potential[i]
            poly=co[0]*tau**4+(co[1]-delta)*tau**3+co[2]*tau**2+co[3]*tau+co[4]
            ok,samples=nonnegative_on_positive(poly,tau)
            checked+=1
            if samples: root_edges+=1
            if not ok and len(failures)<20:
                failures.append({'from':list(map(str,a)),'to':list(map(str,b)),
                                 'poly_coeff_high_to_low':[str(v) for v in S.Poly(poly,tau).all_coeffs()],
                                 'negative_sample':next((x for x,v in samples if v<0),None),
                                 'sample_signs':samples})
    out={'status':'EXACT PASS' if not failures else 'CONTINUOUS-WIDTH EXTENSION REFUTED FOR THIS POTENTIAL',
         'scope':'F_new, carriers (1,-1), same 81 vertices; every positive real strip width',
         'checked_directed_profile_edges':checked,'edges_with_positive_roots':root_edges,
         'potential_source':'exact Bellman potential from the five-width finite graph',
         'counterexample_edges':failures}
    (ROOT/'all_width_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
