#!/usr/bin/env python3
"""Exact synthetic identifiability test; not empirical paper data or AI trials."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from pathlib import Path
import json, math, time, resource, sys

def ranks(values):
    groups={}
    for i,x in enumerate(values): groups.setdefault(x,[]).append(i)
    result=[None]*len(values); pos=1
    for x,indices in sorted(groups.items()):
        r=F(2*pos+len(indices)-1,2)
        for i in indices:result[i]=r
        pos+=len(indices)
    return result

def cov(a,b):
    n=len(a); ma=sum(a,F(0))/n; mb=sum(b,F(0))/n
    return sum(((x-ma)*(y-mb) for x,y in zip(a,b)),F(0))/n

def correlation(a,b):
    ra,rb=ranks(a),ranks(b); c=cov(ra,rb); va=cov(ra,ra);vb=cov(rb,rb)
    if not va or not vb: return None
    q=c*c/(va*vb)
    return {'sign':0 if c==0 else (1 if c>0 else -1),'squared':str(q),'value':math.copysign(math.sqrt(float(q)),float(c)) if c else 0.0}

def independent(a,b):
    ca,cb,cab=Counter(a),Counter(b),Counter(zip(a,b)); n=len(a)
    return all(cab[x,y]*n==ca[x]*cb[y] for x in ca for y in cb)

def rows(n,m=4,lengths=(100,200)):
    return [{'V':10**j,'L':ell,'d':d,'I':F(100*10**j,ell),'U':d*10**j}
            for j,ell,d in product(range(n),lengths,range(1,m+1))]

def summarize(rr):
    I,U,d=([r[k] for r in rr] for k in ('I','U','d'))
    return {'n_rows':len(rr),'rho_I_U':correlation(I,U),'rho_I_d':correlation(I,d),'I_d_exactly_independent':independent(I,d)}

def run():
    t=time.monotonic(); out=[]
    for n in (2,5,10,50):
        rr=rows(n); s=summarize(rr)
        assert s['I_d_exactly_independent'] and s['rho_I_d']['value']==0
        out.append({'proof_cost_levels':n,'statement_lengths':[100,200],'use_counts':[1,2,3,4],**s})
    # Exact theorem checked separately from varying-statement-length witness.
    formula_checks=0
    for n in range(2,51):
        for m in range(2,9):
            rr=rows(n,m,(100,)); observed=summarize(rr)
            theory=F(m*m*(n*n-1),m*m*n*n-1)
            assert F(observed['rho_I_U']['squared'])==theory
            assert observed['I_d_exactly_independent']
            formula_checks+=1
    rr=rows(10); reference=summarize(rr)
    # d=0 additions have every original V,L pair, uniformly repeated.
    null=[dict(V=r['V'],L=r['L'],d=0,I=r['I'],U=0) for r in rr]
    zero_extension=[]
    for mult in (0,1,9,99):
        extended=rr+null*mult; selected=[r for r in extended if r['d']>0]
        assert summarize(selected)==reference
        zero_extension.append({'zero_repetition_multiple':mult,'all_rows':len(extended),'ever_used_fraction':str(F(len(selected),len(extended))),'rho_conditional_positive_use':reference['rho_I_U'],'conditioning_exactly_preserves_result':True})
    result={'kind':'exact synthetic countermodel; not original paper rows','status':'PASS','source_formulas':{'I':'100 V / L','U':'d V'},'cartesian_cases':out,'constant_length_formula':'rho(I,U)^2 = m^2(n^2-1)/(m^2*n^2-1)','formula_checks':formula_checks,'zero_use_extension':zero_extension,'scope':['High I-U correlation alone does not identify prediction of reuse count or of the fraction ever used.','This does not refute actual I-U correlation, actual compression usefulness, generated theorem quality, or future method performance.','The complete joint table makes no assumptions about an actual Lean proof distribution.'],'elapsed_seconds':time.monotonic()-t,'peak_rss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'rss_platform':sys.platform}
    p=Path(__file__).parent/'EXACT_SHARED_FACTOR_RESULT.json';p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
