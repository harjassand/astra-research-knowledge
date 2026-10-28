"""Matched ordinary PH comparator for a stored mode and exact child law.

Solve the explicit Q_child tensor L_death block, then compare its output law
against the falling-factorial spectral contraction. No producer imports.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import time,json
from model import Chain
from exact_solve import ExactFactor,verify_system

ROOT=Path(__file__).resolve().parents[1]

def run():
    begin=time.monotonic();lam=F(999,1000);chain=Chain(lam)
    states,initial,Q,R=chain.matrices(2);K=4;D=K+1;S=len(states);size=S*D
    L=[list(chain.loss(i))+[F(0)]*(K-i)for i in range(D)]
    productQ=[[Q[a][b]*L[i][j]for b in range(S)for j in range(D)]
               for a in range(S)for i in range(D)]
    productR=[[R[a][j]*L[i][l]for j in range(D)for l in range(D)]
               for a in range(S)for i in range(D)]
    childcache={};cases=[]
    def child(exponent):
        if exponent not in childcache:
            z=lam**exponent
            A=[[F(a==b)-z*Q[a][b]for b in range(S)]for a in range(S)]
            B=[[z*v for v in row]for row in R]
            X=ExactFactor(A).solve(B);verify_system(A,X,B)
            childcache[exponent]=X[initial]
        return childcache[exponent]
    for exponent in (0,2):
        z=lam**exponent
        A=[[F(a==b)-z*productQ[a][b]for b in range(size)]for a in range(size)]
        B=[[z*v for v in row]for row in productR]
        X=ExactFactor(A).solve(B);verify_system(A,X,B)
        count=0
        for i in range(D):
            for j in range(D):
                for l in range(D):
                    spectral=F(0)if l>i else comb(i,l)*sum((-1)**s*comb(i-l,s)*child(exponent+l+s)[j]
                                                               for s in range(i-l+1))
                    assert X[initial*D+i][j*D+l]==spectral
                    count+=1
        cases.append({'z':str(z),'exact_joint_components':count})
    output={'status':'PASS_EXPLICIT_PHASE_TYPE_TENSOR_VS_SPECTRAL_REDUCTION',
            'child_states':S,'held_count_states':D,'explicit_waiting_block_states':size,
            'cases':cases,'distinct_child_resolvent_arguments':len(childcache),
            'elapsed_seconds':time.monotonic()-begin,
            'interpretation':'An equally informed ordinary phase-type solver recovers the identical shifted PGF contraction. This is not evidence of a separation from that comparator.'}
    (ROOT/'results/phase_type_waiting.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':run()
