"""Fixed native algebra and exact conservative all-K bound evaluations.

No many-body fixture, state sampling, Gaussian draw or fitted asymptotic.
The Robertson/squeezed-state/Trotter proofs are in PROOF.md, not inferred
from these finite symbolic checks.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,math,time
import sympy as S

HERE=Path(__file__).resolve().parent

def main():
    start=time.perf_counter();T=S.Matrix([[3,1,-4],[1,3,-4],[-4,-4,8]])
    u=S.Matrix([1,1,1])/S.sqrt(3);v=S.Matrix([1,-1,0])/S.sqrt(2)
    P=u*u.T;Q=S.eye(3)-P;f=S.diag(1,-1,0)
    j=S.I*(u*v.T-v*u.T);C=S.simplify(S.I*(f*j-j*f))
    assert T.eigenvals()=={S.Integer(0):1,S.Integer(2):1,S.Integer(12):1}
    assert T*u==S.zeros(3,1)
    assert all(x>=0 for x in (T-2*Q).eigenvals())
    assert all(x>=0 for x in (12*Q-T).eigenvals())
    assert S.simplify((u.T*C*u)[0]-2*S.sqrt(S.Rational(2,3)))==0
    for sign in (-1,1):
        A=2*S.eye(3)+sign*C
        # All principal minors, not a floating eigenvalue proposal.
        for mask in range(1,1<<3):
            ids=[i for i in range(3) if mask>>i&1]
            assert S.simplify(A.extract(ids,ids).det())>=0
    c0=F(25,7056*4**6)
    evaluations=[]
    for K in (10**2,10**4,10**6,10**12):
        D=(K+1)*(K+2)//2
        rootlo=math.isqrt(K//6)
        bits=D.bit_length()
        exponent=max(0,rootlo-2*bits-1)
        numerator=max(0,rootlo-2*bits-2)
        denom=2*(30*K).bit_length()
        L=(numerator+denom-1)//denom if numerator else 0
        evaluations.append({'K_each':K,'D_one_flavor':str(D),'sqrt_K_over6_integer_lower':rootlo,
          'uniform_normalizable_fugacity_count_upper':{'base':2,'exponent':-exponent},
          'grand_filter_expected_proposals_lower':{'base':2,'exponent':exponent},
          'necessary_slices_for_log_error_at_most1_lower':L,
          'qualification':'Exact conservative dyadic/integer consequence of PROOF, not measured sampling work or a sharp mesh threshold.'})
    out={'T':[[int(x) for x in T.row(i)] for i in range(3)],'U':1,
      'one_particle_eigenvalues':[0,2,12],'one_particle_zero_vector':'(1,1,1)/sqrt3',
      'hopping_triangle_product':int(T[0,1]*T[1,2]*T[2,0]),
      'C_matrix':str(C),'C_condensate_expectation':'2sqrt(2/3)',
      'certified_C_norm_upper':2,'squared_s':{'numerator':2,'denominator':3},
      'depletion_small_case_threshold':'d<=N/24',
      'grand_coercivity':'H_N>=sqrt(N/12)-1',
      'trial_normalization_constant':{'numerator':c0.numerator,'denominator':c0.denominator},
      'trial_energy_upper':'K^(2/3)*(16/c0+ln(1/c0)+(lnK)/3)',
      'finite_slice_allK_lower':'(5/6)^(2L)/(25K)^(2L-1)',
      'L1_allK_lower':'1/(36K)',
      'evaluations':evaluations,'seconds_after_imports':time.perf_counter()-start,
      'random_draws':0,'manybody_states_enumerated':0,
      'scope':'Exact one-particle symbolic algebra and exact integer bound evaluation; all-occupation proof is analytic. No critical many-body prediction or generic hardness claim.'}
    (HERE/'EXACT_DATA.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
