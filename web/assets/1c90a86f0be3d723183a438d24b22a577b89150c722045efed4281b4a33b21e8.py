"""Exact star-gap check against a universal pure-moment outer support bound."""
import json
from itertools import combinations
from pathlib import Path
import sympy as sp

HERE=Path(__file__).parent
D=json.loads((HERE/'spin11_fullstar_blocks.json').read_text())
VERT=[sp.Matrix(v) for v in D['pure_moment_outer_vertices_not_claimed_attainable']]
TRACE=sp.Matrix(D['trace_coefficients'])

def prim(q):
    den=sp.ilcm(*(x.q for x in q)); z=[int(x*den) for x in q]
    from math import gcd
    g=0
    for x in z:g=gcd(g,abs(x))
    return tuple(x//g for x in z)

def rays(w):
    rows=[sp.eye(5).row(i) for i in range(5)]
    rows += [(VERT[w]-VERT[j]).T for j in range(len(VERT)) if j!=w]
    out=set()
    for inds in combinations(range(len(rows)),4):
        M=sp.Matrix.vstack(*(sp.Matrix(rows[i]) for i in inds))
        if M.rank()!=4:continue
        ker=M.nullspace()
        if len(ker)!=1:continue
        q=ker[0]
        if all((row*q)[0]>=0 for row in rows):pass
        elif all((row*(-q))[0]>=0 for row in rows):q=-q
        else:continue
        out.add(prim(q))
    return out

def mat(vals):return sp.Matrix([[sp.Rational(x) for x in row] for row in vals])

def main():
    cones=[rays(i) for i in range(len(VERT))]
    allr=set().union(*cones)
    records=[]; failures=[]; unknown=[]
    for ray in sorted(allr):
        a=sp.Matrix(ray); scores=[(v.T*a)[0] for v in VERT]; sup=max(scores); bound=(TRACE.T*a)[0]+sup
        rec={'ray':list(ray),'winner_values':[str(x) for x in scores],'outer_support':str(sup),'bound':str(bound),'blocks':[]}
        for key,obj in D['blocks'].items():
            G=mat(obj['gram']); Bs=[mat(x) for x in obj['bilinear_H']]
            H=sum((a[k]*Bs[k] for k in range(5)),sp.zeros(G.rows))
            gap=sp.simplify(bound*G-H)
            mins=[]
            for n in range(1,gap.rows+1):
                for ix in combinations(range(gap.rows),n):
                    val=sp.factor(gap.extract(ix,ix).det())
                    mins.append((ix,val))
            bad=[(ix,v) for ix,v in mins if v.is_negative is True]
            undec=[(ix,v) for ix,v in mins if v.is_nonnegative is None]
            if bad:failures.append({'ray':ray,'block':key,'negative_minors':[(list(ix),str(v)) for ix,v in bad]})
            if undec:unknown.append({'ray':ray,'block':key,'undecided_minors':[(list(ix),str(v)) for ix,v in undec]})
            rec['blocks'].append({'block':key,'gap':[[str(sp.factor(gap[i,j])) for j in range(gap.cols)] for i in range(gap.rows)],
                                 'all_principal_minors_nonnegative':not bad and not undec})
        records.append(rec)
        print(f'ray {ray}: winner support {sup}, bound {bound}, blocks={len(rec["blocks"])}; '+('FAIL' if any(x['ray']==ray for x in failures) else 'PASS/UNDECIDED'),flush=True)
    # Isotropic normalization by exact PSD at the universal identity-weight bound d^2+d-2=1054.
    iso_fail=[]
    for key,obj in D['blocks'].items():
        G=mat(obj['gram']); Bs=[mat(x) for x in obj['bilinear_H']]
        gap=sp.simplify(1054*G-sum(Bs,sp.zeros(G.rows)))
        bad=[]
        for n in range(1,gap.rows+1):
            for ix in combinations(range(gap.rows),n):
                val=sp.factor(gap.extract(ix,ix).det())
                if val.is_negative is True:bad.append((ix,str(val)))
                elif val.is_nonnegative is None:bad.append((ix,'UNDECIDED '+str(val)))
        if bad:iso_fail.append({'block':key,'bad':bad})
    output={'status':'PASS' if not failures and not unknown and not iso_fail else ('VIOLATION' if failures else 'INCOMPLETE'),
            'support_scope':'valid universal outer bound for full-domain canonical EB: pure moments satisfy s1<=1, s2<=5, 0<=s3,s4,s5<=31, sum s_k=31; vertices are outer-polytope vertices, not asserted attainable',
            'outer_vertices':D['pure_moment_outer_vertices_not_claimed_attainable'],'trace_coefficients':D['trace_coefficients'],
            'cone_ray_counts':[len(x) for x in cones],'cone_rays':[sorted([list(v) for v in x]) for x in cones],
            'distinct_rays':len(allr),'ray_certificates':records,'failures':failures,'unknown':unknown,
            'isotropic_bound':1054,'isotropic_failures':iso_fail}
    (HERE/'spin11_outer_support_check.json').write_text(json.dumps(output,indent=2)+'\n')
    print('ray counts',list(map(len,cones)),'distinct',len(allr),'status',output['status'],flush=True)

if __name__=='__main__': main()
