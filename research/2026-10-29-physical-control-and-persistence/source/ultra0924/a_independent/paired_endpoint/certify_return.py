"""Exact core algebra and dimension-uniform perturbation constants.

The all-M/all-K proofs are analytic in PROOF.md. This consumer does not
enumerate an M-mode many-body matrix, evaluate a permanent, fit a return
kernel or acquire a Gibbs oracle. It uses a 3x3 Schur calculation only.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import time
import sympy as S

HERE=Path(__file__).resolve().parent

def q(x):
    x=F(x)
    return {'numerator':x.numerator,'denominator':x.denominator}

def graph_entries(M):
    """Generate the actual rational local input in O(M) size/time.

    A dictionary stores the sparse full symmetric matrix. No eigenvalue,
    gap, conditioned matrix element or mixing-time oracle is consumed.
    """
    assert isinstance(M,int) and M>=3
    eps=F(1,100000)
    core=((3,1,-4),(1,3,-4),(-4,-4,8))
    entries={}
    def add(i,j,v):
        entries[i,j]=entries.get((i,j),F(0))+v
    blocks=M//3
    for block in range(blocks):
        for i in range(3):
            for j in range(3):add(3*block+i,3*block+j,F(core[i][j]))
    for i in range(M-1):
        same_complete_block=(i//3==(i+1)//3 and i//3<blocks)
        if not same_complete_block:
            add(i,i,eps);add(i+1,i+1,eps)
            add(i,i+1,-eps);add(i+1,i,-eps)
    return {ij:v for ij,v in entries.items() if v}

def main():
    start=time.perf_counter()
    T=S.Matrix([[3,1,-4],[1,3,-4],[-4,-4,8]])
    assert T.eigenvals()=={S.Integer(0):1,S.Integer(2):1,S.Integer(12):1}
    L=S.Matrix([[1,-1,0],[-1,2,-1],[0,-1,1]])
    A=T-S.Rational(2,3)*L
    for mask in range(1,8):
        ix=[i for i in range(3) if mask>>i&1]
        assert A.extract(ix,ix).det()>=0
    assert T*S.ones(3,1)==S.zeros(3,1)

    w=S.symbols('w',positive=True)
    B=S.Matrix([[1,1,0],[-4,0,-4],[0,-4,-4]])
    D=S.Matrix([[w+6,-4,-4],[-4,w+11,1],[-4,1,w+11]])
    Rhat=2*B.T*D.inv()*B
    expected=2*(w*w-26*w-40)/((w+10)*(w*w+18*w+40))
    assert S.factor(Rhat[0,1]-expected)==0
    S1=S.diag(7,7,17)-Rhat.subs(w,3)
    assert S1[0,1]==S.Rational(218,1339)
    assert S1[0,2]==S1[1,2]==-S.Rational(224,103)
    assert S1[0,1]*S1[1,2]*S1[2,0]>0
    assert S1[0,0]>0 and S1[:2,:2].det()>0 and S1.det()>0

    eps=F(1,100000)
    err=8*eps*27*(27+8*eps)
    lo=F(218,1339)-err
    hi=F(-224,103)+err
    assert lo>F(1,10) and hi<-2

    # Only symbolic exponent cancellation; no finite-M occupation case is run.
    M=S.symbols('M',integer=True,positive=True)
    alpha=(M+1)/(2*(M+3));p=(M+1)/(M+3)
    assert S.simplify(2*alpha-p)==0
    assert S.simplify((M+1)*(S.Rational(1,2)-alpha)-p)==0
    assert S.simplify(1-p-2/(M+3))==0

    out={
      'native_core':[[int(x) for x in T.row(i)] for i in range(3)],
      'physical_U_for_rational_Schur':q(1),'Laplace_z':q(1),
      'Rhat_12_general':'2*(w^2-26w-40)/[(w+10)*(w^2+18w+40)], w=z+2U',
      'S_core':[[q(x) for x in S1.row(i)] for i in range(3)],
      'epsilon':q(eps),'uniform_allM_S_error_upper':q(err),
      'uniform_allM_S12_lower':q(lo),'uniform_allM_S13_S23_upper':q(hi),
      'uniform_allM_return_laplace12_upper':q(-lo),
      'positive_subMarkov_boundary_Laplace_operator_error_lower':q(F(1,7868)),
      'one_particle_gap_lower':'4*epsilon/M^2',
      'one_particle_norm_upper':q(12+4*eps),
      'allU_transport':'R_U(t)=exp(-2U*t)R_0(t) at K=1; sign persists for every finite U>0',
      'allK_trial_exponent':'(M+1)/(M+3) at fixed M',
      'allK_trial_normalization':'(25/36)*16^[-(M-1)]*4^[-M(M-1)] *a^(M-1)*K^[-(M-1)/2]',
      'paired_mass_receiver':'Tr(P*rho)<=[1/sqrt(M)+sqrt(Tr(D*rho)/(2K))]^2',
      'paired_Gibbs_mass_fixedM_limit_upper':'1/M',
      'graph_compiler':'graph_entries(M), sparse rational O(M); no large graph/many-body fixture run',
      'random_draws':0,'manybody_states_enumerated':0,
      'seconds_after_imports':time.perf_counter()-start,
      'scope':'Exact core Schur and rational all-M constants; all-family probability/operator statements follow from PROOF, not finite diagnostics.'}
    (HERE/'EXACT_RETURN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
