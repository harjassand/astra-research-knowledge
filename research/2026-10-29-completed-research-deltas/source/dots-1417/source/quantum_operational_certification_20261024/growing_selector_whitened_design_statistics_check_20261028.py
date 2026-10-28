"""Exact prescribed-design algebra only: no source queries, Bernoulli draws or RNG."""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json


def eye(m): return [[F(i == j) for j in range(m)] for i in range(m)]
def zeros(m): return [[F(0) for _ in range(m)] for _ in range(m)]
def mul(A, B):
    m = len(A)
    return [[sum((A[i][k]*B[k][j] for k in range(m)), F(0)) for j in range(m)] for i in range(m)]
def tr(A): return sum((A[i][i] for i in range(len(A))), F(0))
def inner(A, B): return sum((A[i][j]*B[j][i] for i in range(len(A)) for j in range(len(A))), F(0))
def string(x): return str(x)

rows=[]
for m in range(1,7):
    I=eye(m)
    design=[]
    for a in range(m):
        P=zeros(m);P[a][a]=F(1)
        design.append((F(2,m*(m+2)), P))
    for signs in product((-1,1),repeat=m):
        P=[[F(signs[i]*signs[j],m) for j in range(m)] for i in range(m)]
        design.append((F(m,(m+2)*2**m),P))
    assert sum((p for p,_ in design),F(0))==1
    for i in range(m):
      for j in range(m):
        assert sum((p*P[i][j] for p,P in design),F(0))==F(i==j,m)
        for k in range(m):
          for l in range(m):
            rhs=F((i==j)*(k==l)+(i==k)*(j==l)+(i==l)*(j==k),m*(m+2))
            assert sum((p*P[i][j]*P[k][l] for p,P in design),F(0))==rhs
    # B=C^2 with C diagonal rational; A=C E C, 0<E<=I/2.
    C=[F(1,2**j) for j in range(m)]
    B=[[C[i]**2 if i==j else F(0) for j in range(m)] for i in range(m)]
    Binv=[[1/(C[i]**2) if i==j else F(0) for j in range(m)] for i in range(m)]
    E=[[F(i==j,4)+F(1,4*m) for j in range(m)] for i in range(m)]
    A=[[C[i]*E[i][j]*C[j] for j in range(m)] for i in range(m)]
    tau=min(c*c for c in C)
    mean=zeros(m); ET2=zeros(m); EYnorm2=F(0)
    for prob,P in design:
        s=inner(Binv,P)
        e=inner(E,P)
        bernoulli_p=e/s
        assert 0<=bernoulli_p<=1
        T=[[F(m*(m+2),2)*P[i][j]-F(m,2)*I[i][j] for j in range(m)] for i in range(m)]
        T2=mul(T,T)
        assert tr(T2)==F(m**3*(m+3),4)
        for i in range(m):
          for j in range(m):
            assert T2[i][j]==F(m**3*(m+2),4)*P[i][j]+F(m*m,4)*I[i][j]
            mean[i][j]+=prob*bernoulli_p*s*T[i][j]
            ET2[i][j]+=prob*T2[i][j]
        EYnorm2+=prob*bernoulli_p*s*s*tr(T2)
    assert mean==E
    assert ET2==[[F(m*m*(m+3),4)*I[i][j] for j in range(m)] for i in range(m)]
    variance=EYnorm2-inner(E,E)
    V=F(m**3*(m+3),4)/tau
    assert 0<=variance<=V
    assert m**3*(m+3)<=4*m**4
    noncommuting=(mul(A,B)!=mul(B,A))
    assert noncommuting==(m>=2)
    rows.append({'m':m,'finite_design_atoms_with_duplicates':len(design),'all_second_and_fourth_moments':'PASS','mean_identity':'PASS','T_squared_identity':'PASS','tau':string(tau),'exact_Frobenius_variance':string(variance),'claimed_variance_upper_bound':string(V),'A_and_B_noncommuting':noncommuting})

# Canonical source implementation: rational BINOMIAL polynomial C, not the
# exact inverse square root and not the optional Newton construction.
canonical=[]
for m in range(1,5):
    I=eye(m)
    R=eye(m)
    if m>=2:
        R[0][0]=R[1][1]=F(3,5);R[0][1]=F(-4,5);R[1][0]=F(4,5)
    Rt=[list(row) for row in zip(*R)]
    eig=[F(1,2)+F(j,2*m) for j in range(m)]
    B=mul(mul(R,[[eig[i] if i==j else F(0) for j in range(m)] for i in range(m)]),Rt)
    A=[[B[i][j]/4+F(1,8*m) for j in range(m)] for i in range(m)]
    tau=F(1,2)
    Kplus=48  # (4/tau)*ceil(log2(32/tau))=8*6, exact.
    Q=[[I[i][j]-B[i][j]/4 for j in range(m)] for i in range(m)]
    Qpow=eye(m);coef=F(1);C=zeros(m)
    for k in range(Kplus):
        for i in range(m):
            for j in range(m):C[i][j]+=coef*Qpow[i][j]/2
        Qpow=mul(Qpow,Q)
        coef*=F(2*k+1,2*k+2)
    assert mul(C,B)==mul(B,C)
    Ceig=mul(mul(Rt,C),R)
    for i in range(m):
        assert all(Ceig[i][j]==0 for j in range(m) if j!=i)
        ci=Ceig[i][i];bi=eig[i]
        assert ci>=F(7,16)
        assert F(49,64)<=ci*ci*bi<=1
        assert ci*ci<=1/tau
        assert (ci+F(1,16))**2*bi>=1  # exact backward tail <=1/16
    C2=mul(C,C);target=mul(mul(C,A),C)
    design=[]
    for a in range(m):
        P=zeros(m);P[a][a]=F(1);design.append((F(2,m*(m+2)),P))
    for signs in product((-1,1),repeat=m):
        design.append((F(m,(m+2)*2**m),[[F(signs[i]*signs[j],m) for j in range(m)] for i in range(m)]))
    mean=zeros(m);EYnorm2=F(0);Lm=F(m**3*(m+3),4)
    for probability,P in design:
        weight=inner(C2,P);effect=inner(target,P)
        assert F(0)<=effect/weight<=1
        T=[[F(m*(m+2),2)*P[i][j]-F(m,2)*I[i][j] for j in range(m)] for i in range(m)]
        for i in range(m):
            for j in range(m):mean[i][j]+=probability*effect*T[i][j]
        EYnorm2+=probability*weight*effect*Lm
    assert mean==target
    variance=EYnorm2-inner(target,target)
    assert 0<=variance<=Lm/tau
    c=F(1,32);r=c/12
    bound=2304*Lm/(tau*c*c);N=(bound.numerator+bound.denominator-1)//bound.denominator
    assert Lm/(tau*N*r*r)<=F(1,16)
    canonical.append({'m':m,'K_plus_1':Kplus,'tau':str(tau),'preconditioner':'canonical rational binomial polynomial','commutes_with_B':True,'CBC_bounds_49_over_64_and_1':'PASS','backward_tail_1_over_16':'PASS','A_and_B_noncommuting':mul(A,B)!=mul(B,A),'exact_mean_CAC':'PASS','variance_bound':'PASS','canonical_batch_Markov_bound':'PASS','computed_but_NOT_sampled_batch_size':N})

majority=[]
for b in range(1,24,2):
    tail=sum((F(comb(b,k))*F(1,16)**k*F(15,16)**(b-k) for k in range((b+1)//2,b+1)),F(0))
    bound=F(1,2**(b+2))
    assert tail<=bound
    majority.append({'b':b,'exact_binomial_tail_at_bad_probability_1_over_16':str(tail),'union_bound':str(bound)})

# This is a deterministic decision-boundary example, not a sampled batch.
points=[F(-1),F(1),F(3)];r=F(1);k=2
exact_counts=[sum((x-y)**2<=4*r*r for y in points) for x in points]
strict_counts=[sum((x-y)**2<4*r*r for y in points) for x in points]
assert max(exact_counts)>=k and max(strict_counts)<k
result={'status':'PASS','source_calls':0,'Bernoulli_samples':0,'RNG_used':False,'kind':'Exact finite-design moment sums, prescribed feasible matrices and deterministic medoid boundary arithmetic; not an acquisition simulation.','matrix_cases':rows,'canonical_binomial_preconditioner_cases':canonical,'majority_failure_bounds':majority,'inclusive_threshold_boundary_example':{'target':0,'radius':1,'batch_matrices':[-1,1,3],'good_indices':[0,1],'required_neighborhood_count_including_self':2,'inclusive_counts':exact_counts,'strict_counts':strict_counts,'conclusion':'Inclusive exact squared-distance threshold is needed; replacing <= by < or unpadded approximate comparisons can lose all eligible outputs.'},'constants':{'variance':'m^3*(m+3)/(4*tau)','exact_batch_N':'ceil(4*m^3*(m+3)/(tau*r^2))','c_target_N':'ceil(36*m^3*(m+3)/(tau*c^2))','rounded_batch_N':'ceil(16*m^3*(m+3)/(tau*r^2))','medoid_error':'at most 3*r','odd_b_majority_failure':'at most 2^(-b-2)'}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print('PASS: six exact design/matrix cases, four canonical binomial cases, twelve odd-b tail sums, inclusive-threshold witness; zero source calls/RNG.')
