"""Exact one-level replay using the already supplied spin-one Choi witness.

No optimizer, random sampling, new covariance family, or theorem inference.
Run with system python3 (SymPy). The general proof is in the frozen text.
"""
import json
from pathlib import Path
import sympy as s

R = s.Rational
d = 3
I = s.eye(d)
J = [s.Matrix(d,d,lambda j,k:-s.I*s.LeviCivita(i,j,k)) for i in range(d)]
E = [s.sqrt(R(3,2))*A for A in J]
full = E[:]
for i,j in [(0,1),(0,2),(1,2)]:
    A=s.zeros(d); A[i,j]=A[j,i]=s.sqrt(R(3,2)); full.append(A)
full.extend([s.sqrt(R(3,2))*s.diag(1,-1,0),s.sqrt(R(1,2))*s.diag(1,1,-2)])
V=[]
for i in range(d):
    v=s.zeros(d,d*d)
    v[i,i*d+i]=4
    for j in range(d):
        if j!=i:
            v[i,j*d+j]=-2
            v[j,i*d+j]=v[j,j*d+i]=3
    V.append(v)
def Badjoint(O):
    return sum((v*O*v.T for v in V),s.zeros(d))/60
rhoBC=sum((v.T*v for v in V),s.zeros(d*d))/180
tau=lambda A:s.trace(A)/d
checks={}
checks['B_is_TP']=Badjoint(s.eye(d*d))==I
checks['normalized_HS_full_basis']=s.Matrix(8,8,lambda i,j:tau(full[i]*full[j]))==s.eye(8)
checks['slow_spin_eigenvalues_three_quarters']=all(s.simplify(Badjoint(s.kronecker_product(A,I))-R(3,4)*A)==s.zeros(d) for A in E)
C=s.Matrix(3,3,lambda a,b:s.simplify(s.trace(rhoBC*s.kronecker_product(E[a],E[b]))))
checks['C_equals_half_identity']=C==s.eye(3)/2
leaf=[]
for a,A in enumerate(J):
    for value,P in [(1,(A*A+A)/2),(-1,(A*A-A)/2),(0,I-A*A)]:
        x=s.zeros(3,1); x[a]=3*value*s.sqrt(R(3,2))
        leaf.append((P/3,x))
N0=sum((tau(F)*x*x.T for F,x in leaf),s.zeros(3))
checks['N0_equals_three_identity']=N0==3*s.eye(3)
N1=s.zeros(3); cross=s.zeros(8,3); S=s.zeros(8); sumEffects=s.zeros(3)
moment=[s.zeros(3) for _ in range(3)]
nonzero=0
for F,x in leaf:
    for G,y in leaf:
        M=Badjoint(s.kronecker_product(F,G))
        z=(x+y)*R(2,3)
        sumEffects+=M
        for a in range(3): moment[a]+=z[a]*M
        p=s.simplify(tau(M))
        if not p:
            continue
        nonzero+=1
        u=s.Matrix([s.simplify(tau(M*A)) for A in full])
        N1+=p*z*z.T
        cross+=u*z.T
        S+=u*u.T/p
N1=N1.applyfunc(s.simplify); cross=cross.applyfunc(s.simplify); S=S.applyfunc(s.simplify)
embed=s.zeros(8,3)
for a in range(3): embed[a,a]=1
checks['sum_joint_input_effects_is_identity']=sumEffects==I
checks['each_unbiased_pullback_is_exact']=all((moment[a]-E[a]).applyfunc(s.simplify)==s.zeros(3) for a in range(3))
checks['full_crossmoment_including_fast_complement']=cross==embed
checks['N1_exact_recursion']=N1==(N0+C)*R(8,9)
D1=s.eye(3)*R(32,9)
checks['N1_exact_value']=N1==s.eye(3)*R(28,9)
checks['N1_le_D1']=D1-N1==s.eye(3)*R(4,9)
lower=(S-embed*(D1.inv())*embed.T).applyfunc(s.simplify)
checks['canonical_full_covariance_diagonal_in_test_basis']=all(lower[i,j]==0 for i in range(8) for j in range(8) if i!=j)
checks['canonical_full_schur_lower_bound_exact_PSD']=checks['canonical_full_covariance_diagonal_in_test_basis'] and all(lower[i,i]>=0 for i in range(8))
result={'status':'EXACT_FINITE_MOMENT_REPLAY_ONLY','source_witness':'authorized SPIN1_ALL_WEIGHTS_THEOREM.txt R0, vectors vi',
        'checks':checks,'all_pass':all(checks.values()),'nonzero_joint_outcomes':nonzero,
        'C':str(C),'N0':str(N0),'N1':str(N1),'D1':str(D1),
        'canonical_S_diagonal':[str(S[i,i]) for i in range(8)],
        'S_minus_embedded_inverse_D1_diagonal':[str(lower[i,i]) for i in range(8)],
        'limitation':'Finite algebra does not establish the general compactness/tree proof or external correctness.'}
path=Path(__file__).with_name('exact_tree_moment_replay.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['all_pass']
