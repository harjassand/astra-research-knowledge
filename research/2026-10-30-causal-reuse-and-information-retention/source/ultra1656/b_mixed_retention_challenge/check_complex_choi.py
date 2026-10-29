"""Generic complex-index check; no quantum source/case is acquired."""
import json
from pathlib import Path
import time
import sympy as s

def main():
    start=time.perf_counter()
    x=s.symbols('x0:4',real=True);y=s.symbols('y0:4',real=True)
    Z=s.Matrix(2,2,lambda a,p:x[2*a+p]+s.I*y[2*a+p])
    v=s.Matrix([s.conjugate(Z[a,p]) for a in range(2) for p in range(2)])
    C=v*v.conjugate().T
    checks=0
    wrong_detected=False
    wrong=s.Matrix([Z[a,p] for a in range(2) for p in range(2)])
    wrong=wrong*wrong.conjugate().T
    for a in range(2):
        for b in range(2):
            E=s.zeros(2);E[a,b]=1
            phi=Z.conjugate().T*E*Z
            for p in range(2):
                for q in range(2):
                    assert s.expand(C[2*a+p,2*b+q]-phi[p,q])==0
                    wrong_detected |= s.expand(wrong[2*a+p,2*b+q]-phi[p,q])!=0
                    checks+=1
    assert wrong_detected
    out={'status':'EXACT_GENERIC_COMPLEX_INDEX_IDENTITIES_PASSED',
         'scope':'generic Choi/Kraus index algebra, not a new channel or theorem substitute',
         'convention':'C_(a,p),(b,q)=Phi(E_ab)_(p,q); Phi(A)=Z*AZ',
         'rank_one_vector':'v_(a,p)=conjugate(Z_(a,p))',
         'checked_polynomial_entries':checks,
         'unconjugated_vector_is_not_generally_correct':wrong_detected,
         'seconds_after_imports':time.perf_counter()-start}
    p=Path(__file__).resolve().parent/'COMPLEX_CHOI.json'
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
