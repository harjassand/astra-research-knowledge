"""Search a specified finite rational facet ansatz; verify exact all-scale obligations.

No coefficients from a known successful barrier are input. This is a specialized
exact proof checker, not a general CAD engine. Its sufficient inequalities are
derived in TWO_LINKAGE_PROOF.md. Rejections mean this proof template did not
certify the candidate, not that it is unsafe or the network is nonpermanent.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

KAPPA, RATE_K = F(1), F(4)
NETWORK = [((1,0),(0,2)), ((0,2),(1,0)),
           ((0,1),(2,0)), ((2,0),(0,1))]

def check(candidate):
    A,B,C,s,zp,a = candidate
    tp=zp*zp
    # Direct exact conditions for all-scale compactness, c=(1,1), coverage.
    geometric = [A>1, 0<C<1, 0<s<1, 0<zp<1,
                 A*tp<=1, B*tp<=2, C>=2*tp,
                 zp*A<=1, zp*B<=2, 2*zp<=C]
    if not all(geometric): return None
    # At active coordinate facet a<=A*t and b>=(B-A/s)*t.
    L=2*KAPPA*(B-A/s)-RATE_K*A-2*RATE_K*A*A*tp
    # At active small-total facet, 2*t^2<=a+b<=B*t.
    small_total=KAPPA-RATE_K*B*tp
    # At active large-total facet, a+b>=C/t>=C/tp.
    umin=C/tp
    large_total=umin*(KAPPA*umin/F(2)-RATE_K)
    if not (B-A/s>0 and L>=a*tp and small_total>0
            and 2*s*small_total>=a and umin>=2*RATE_K/KAPPA
            and large_total>=a*tp*tp):
        return None
    return {'coordinate_coefficient': L,
            'small_total_coefficient': 2*s*small_total,
            'large_total_constant': large_total,
            'uniform_drift_coefficient': a}

def q(x): return str(x.numerator) if x.denominator==1 else str(x)

def main():
    searched=0
    # Chosen facet directions / scale exponents form an explicit ansatz;
    # all intercept multipliers, slope weight, scale cap, and margin are searched.
    slopes=sorted({F(n,d) for d in range(2,7) for n in range(1,d)})
    for A,B,C,s,n,a in product(range(2,5),range(2,25),
                               [F(1,3),F(1,2),F(2,3)],slopes,
                               range(2,9),[F(1),F(1,2),F(1,4),F(1,8)]):
        candidate=(F(A),F(B),C,s,F(1,2**n),a)
        searched+=1
        proof=check(candidate)
        if proof is None: continue
        A,B,C,s,zp,a=candidate
        result={'status':'CERTIFIED_BY_EXACT_SUFFICIENT_ALL_SCALE_PROOF',
                'scope':'searched rational ansatz for one genuinely unbounded class',
                'network':NETWORK, 'rate_box':[q(KAPPA),q(RATE_K)],
                'representative':['1','1'],
                'candidates_checked':searched,
                'q':4,'eta':'1/4','p':4,'a':q(a),'z_P':q(zp),
                'parameters':{k:q(v) for k,v in zip(['A','B','C','s'],[A,B,C,s])},
                'proof_margins':{k:q(v) for k,v in proof.items()},
                'facets':[{'slope':['0','0'],'offset':[]},
                          {'slope':['1','0'],'offset':[[q(-A),2]]},
                          {'slope':['0','1'],'offset':[[q(-A),2]]},
                          {'slope':[q(s),q(s)],'offset':[[q(-s*B),2]]},
                          {'slope':['-1','-1'],'offset':[[q(C),-2]]}],
                'absorber': {'a_min':q(A*zp*zp),'b_min':q(A*zp*zp),
                             'total_min':q(B*zp*zp),'total_max':q(C/(zp*zp))}}
        out=Path(__file__).with_name('two_linkage_certificate.json')
        out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ['status','candidates_checked','parameters','z_P','proof_margins','absorber']},indent=2))
        return
    raise RuntimeError('UNKNOWN: finite ansatz search exhausted')

if __name__=='__main__': main()
