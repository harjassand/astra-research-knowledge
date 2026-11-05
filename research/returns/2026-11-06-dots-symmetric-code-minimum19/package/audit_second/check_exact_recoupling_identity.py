"""Exact CG-sum checks of the stated lifted-KL identity at actual n=18."""
from functools import lru_cache
from pathlib import Path
import hashlib,json
import sympy as s
from sympy.physics.wigner import clebsch_gordan,wigner_6j

ROOT=Path(__file__).resolve().parent

@lru_cache(None)
def C(a,b,c,u,v,w):
    return clebsch_gordan(a,b,c,u,v,w)

def check(n,l,lp,r,J):
    j=s.Rational(n,2);J=s.Rational(J)
    value=s.S.Zero;nonzero=0
    for m in range(-min(l,lp),min(l,lp)+1):
        aa=(-1)**(lp-m)*C(l,lp,r,m,-m,0)
        if not aa:continue
        for k in range(n+1):
            mu=k-j;M=m+mu
            if abs(M)>J:continue
            term=aa*(-1)**(j-mu)*C(j,j,r,mu,-mu,0)*C(l,j,J,m,mu,M)*C(lp,j,J,m,mu,M)
            if term:nonzero+=1;value+=term
    expected=(-1)**(lp+j+J)*(2*J+1)*wigner_6j(l,j,J,j,lp,r)
    difference=s.simplify(value-expected);assert difference==0
    return {'n':n,'l':l,'lprime':lp,'rank':r,'J':str(J),
            'nonzero_CG_sum_terms':nonzero,'exact_coefficient':str(expected),
            'exact_difference':'0'}

if __name__=='__main__':
    result={'checks':[check(*case) for case in [(18,4,7,3,9),(18,9,9,4,9),(18,6,8,4,10)]],
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'exact_recoupling_identity_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
