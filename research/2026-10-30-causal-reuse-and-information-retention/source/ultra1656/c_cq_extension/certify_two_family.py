"""Exact SAME0,+ two-family conditional receiver, standard library only.

Rebuilds the noncommuting source coefficients and checks an explicit rank1
Choi certificate. Numerical producer coefficients are compared, never used
as the mathematical premise. No quantum-reference or physical sampling.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,resource,hashlib
ROOT=Path(__file__).resolve().parent


def zero(n,m=None):return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]
def eye(n):
    M=zero(n)
    for i in range(n):M[i][i]=F(1)
    return M
def tr(A):return sum(A[i][i] for i in range(len(A)))
def T(A):return list(map(list,zip(*A)))
def mm(A,B):return [[sum(a*b for a,b in zip(ar,bc)) for bc in zip(*B)] for ar in A]
def add(A,B):return [[a+b for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def scale(s,A):return [[s*v for v in row] for row in A]
def kron(A,B):return [[a*b for a in ar for b in br] for ar in A for br in B]
def enc(A):return [[str(x) for x in row] for row in A]


def ldl(A):
    n=len(A);L=eye(n);D=[]
    for j in range(n):
        d=A[j][j]-sum(L[j][k]**2*D[k] for k in range(j));assert d>0
        D.append(d)
        for i in range(j+1,n):L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*D[k] for k in range(j)))/d
    return min(D)


def main():
    tick=time.perf_counter();taus=[[[F(1),F(0)],[F(0),F(0)]],[[F(1,2)]*2 for _ in range(2)]]
    P=[[[F(1),F(-1)],[F(-1),F(1)]],[[F(0),F(0)],[F(0),F(2)]]]
    for i in range(2):
        for j in range(2):assert tr(mm(P[i],taus[j]))==(i==j)
    W=[kron(eye(2),t) for t in taus]+[kron(T(t),eye(2)) for t in taus]
    TT=[[p[i][j] for j in range(2) for i in range(2)] for p in P]
    assert TT==[[1,-1,-1,1],[0,0,0,2]]
    for j,M in enumerate(W):
        expected=zero(2);expected[j%2][j%2]=F(2)
        assert mm(mm(TT,M),T(TT))==expected
    e,f=9,3;A0=zero(e)
    for i in range(4):A0[i][i]=F(1,4)
    WH=scale(F(1,4),add(add(W[0],W[1]),add(W[2],W[3])))
    for i in range(4):
        for j in range(4):A0[4+i][4+j]=WH[i][j]
    A0[-1][-1]=F(1)
    source=[A0];labels=[0,1,0,1]
    B0=zero(f);B0[0][0]=B0[1][1]=F(1,2);B0[2][2]=F(2);target=[B0]
    for j in range(3):
        A=zero(e);A[j][j]=F(1);A[3][3]=F(-1)
        diff=add(W[j],scale(F(-1),W[3]))
        for p in range(4):
            for q in range(4):A[4+p][4+q]=diff[p][q]
        source.append(A);B=zero(f);B[labels[j]][labels[j]]+=1;B[1][1]-=1;target.append(B)
    delta=[taus[0][i][j]-taus[1][i][j] for j in range(2) for i in range(2)]
    for skew in (False,True):
        A=zero(e)
        for p in range(4):A[4+p][8]=delta[p];A[8][4+p]=-delta[p] if skew else delta[p]
        source.append(A);B=zero(f);B[0][2]=F(1);B[1][2]=F(-1)
        B[2][0]=F(-1) if skew else F(1);B[2][1]=F(1) if skew else F(-1);target.append(B)
    # Explicit rational PD source margin; not an eigensolver sign.
    margin=add(A0,scale(F(-1,8),eye(e)));pivot=ldl(margin)
    Z=zero(e,f)
    for i in range(4):
        for j in range(2):Z[4+i][j]=TT[j][i]
    Z[8][2]=F(2)
    checks=[]
    for j,(A,B) in enumerate(zip(source,target)):
        got=scale(F(1,2),mm(mm(T(Z),A),Z));assert got==B
        checks.append({'coefficient':j,'full_matrix_exact':True,'imaginary_coefficient_stripped':j==5})
    vec=[x for row in Z for x in row]
    C=[[a*b/2 for b in vec] for a in vec]
    # Rebuild Phi_C(A) as well; this pays the Choi block convention.
    for A,B in zip(source,target):
        got=zero(f)
        for a in range(e):
            for b in range(e):
                if A[a][b]:
                    for p in range(f):
                        for q in range(f):got[p][q]+=A[a][b]*C[a*f+p][b*f+q]
        assert got==B
    prop_path=ROOT/'TWO_FAMILY_PROPOSAL.json'
    if prop_path.exists():
        prop=json.loads(prop_path.read_text())
        assert [enc(A) for A in source]==prop['source_pencil']
        assert [enc(B) for B in target[1:]]==prop['target_nonconstant']
        numerical={'proposal_c':prop['c_proposal'],'status':prop['status'],
            'sha256':hashlib.sha256(prop_path.read_bytes()).hexdigest(),
            'used_as_proof_premise':False,'source_and_nonconstant_target_identical':True}
    else:numerical=None
    result={'status':'EXACT_CQ_CONDITIONAL_UPPER_TWO',
        'scope':'all two-family noncommuting effects, hence all faithful CQ inputs/references and finite-divergence regularized limits; no physical inverse map',
        'tau':list(map(enc,taus)),'dual_projectors':list(map(enc,P)),'HS_T':enc(TT),
        'source_order':e,'target_order':f,'Choi_order':e*f,'c':'2',
        'source_constant_PD_margin':'1/8','source_margin_min_LDL_pivot':str(pivot),
        'source_pencil':list(map(enc,source)),'target_pencil':list(map(enc,target)),
        'Z':enc(Z),'Choi':enc(C),'Choi_PSD_reason':'one-half exact outer product; rank1',
        'PSD_remainder':'0','coefficient_checks':checks,
        'numerical_proposal_comparison':numerical,'new_solver_calls':0,'quantum_reference_queries':0,
        'seconds':time.perf_counter()-tick,'peak_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (ROOT/'EXACT_TWO_FAMILY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'c':'2','rank1_Choi_order':e*f,
        'all_coefficients':len(checks),'seconds':result['seconds'],'peak_RSS_bytes':result['peak_RSS_bytes']},indent=2))


if __name__=='__main__':main()
