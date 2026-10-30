"""Exact finite orientation/control of the all-Q Schur/ordered-wait identity.

Hook-length and hook-content dimensions are evaluated independently of RSK.
This is not a source/solver/quantum run or a substitute for the general proof.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial, comb
from pathlib import Path
import json,time

@lru_cache(None)
def parts(n,maximum):
    if n==0: return ((),)
    return tuple((a,)+tail for a in range(min(n,maximum),0,-1)
                 for tail in parts(n-a,a))

def dims(shape,r):
    hook=1;content=1
    for i,row in enumerate(shape):
      for j in range(row):
        hook*=row-j+sum(other>j for other in shape[i+1:])
        content*=r+j-i
    specht=F(factorial(sum(shape)),hook)
    unitary=F(content,hook)
    assert specht.denominator==unitary.denominator==1
    return int(specht),int(unitary)

def main():
    start=time.perf_counter();records=[]
    for r in range(2,7):
      for q in range(25):
        masses={}
        for shape in parts(q,q):
          if len(shape)>r: continue
          f,s=dims(shape,r)
          masses[shape]=f*s
        assert sum(masses.values())==r**q
        full=F(sum(m for shape,m in masses.items() if len(shape)==r),r**q)
        tail=F(sum(comb(q,j)*(r-1)**(q-j) for j in range(r,q+1)),r**q)
        assert full==tail
        # This union bound counts positions of the ONE strictly-decreasing
        # full-alphabet pattern; no false independence between patterns.
        union=F(comb(q,r),r**r) if q>=r else F(0)
        assert full<=union
        records.append({'r':r,'Q':q,'full_height_probability':str(full),
                        'same_exact_Binomial_tail':str(tail)})
    out={'scope':'finite exact hook-length/content control of general RSK identity, r2..6,Q0..24',
         'cases':len(records),'all_total_dimensions_exact':True,
         'all_full_height_Binomial_tails_exact':True,
         'no_source_solver_random_or_quantum_calls':True,
         'records':records,'seconds_after_imports':time.perf_counter()-start}
    Path(__file__).with_name('SCHUR_TAIL_INTAKE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))

if __name__=='__main__': main()
