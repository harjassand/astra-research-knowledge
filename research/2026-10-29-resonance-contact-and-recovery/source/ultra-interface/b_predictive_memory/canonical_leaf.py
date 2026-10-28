"""Exact canonical Gaussian-leaf receiver and four-mode interface counter.

General functions use covariance/Pfaffian arithmetic, not a density matrix.
The finite 16-dimensional density below is only an independent exact control
for the stated counterexample. No Gibbs-history sampler or physical record.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
import sympy as s

def pfaffian(matrix):
    """Cubic elimination, with exact pivoting and no square-root branch."""
    A=s.MutableDenseMatrix(matrix)
    n=A.rows
    assert n==A.cols and n%2==0
    out=s.Integer(1)
    for i in range(0,n,2):
        pivot=next((j for j in range(i+1,n) if s.simplify(A[i,j])!=0),None)
        if pivot is None:return s.Integer(0)
        if pivot!=i+1:
            A.row_swap(pivot,i+1);A.col_swap(pivot,i+1);out=-out
        p=A[i,i+1];out*=p
        for j in range(i+2,n):
            for k in range(j+1,n):
                A[j,k]=s.cancel(A[j,k]-(A[i,j]*A[i+1,k]-A[i,k]*A[i+1,j])/p)
                A[k,j]=-A[j,k]
    return s.simplify(out)

def charge_probabilities(Gamma):
    """All coefficients of the Gaussian number FCS, exact arithmetic."""
    n=Gamma.rows//2
    J=s.diag(*([s.Matrix([[0,1],[-1,0]])]*n)) if n else s.zeros(0)
    vals=[s.simplify(pfaffian((1+x)*J+(x-1)*Gamma)/2**n) for x in range(n+1)]
    z=s.Symbol('z')
    polynomial=s.Poly(s.interpolate(list(enumerate(vals)),z),z)
    answer=[s.simplify(polynomial.nth(q)) for q in range(n+1)]
    assert s.simplify(sum(answer)-1)==0
    return answer

def first_mode_update(Gamma,bit):
    """Gaussian update after observing occupation bit in the FIRST mode."""
    sign=2*bit-1
    denom=1+sign*Gamma[0,1]
    probability=s.simplify(denom/2)
    if probability==0:return probability,None
    m=Gamma.rows-2
    new=s.zeros(m)
    for c in range(m):
        for d in range(m):
            cc,dd=c+2,d+2
            new[c,d]=s.simplify(Gamma[cc,dd]+sign*(-Gamma[cc,0]*Gamma[dd,1]+Gamma[cc,1]*Gamma[dd,0])/denom)
    assert new+new.T==s.zeros(m)
    return probability,new

def exact_conditional_law(Gamma,charge,prefix=()):
    """Control-only enumeration of the sequential receiver's output law.

    The sampling algorithm follows ONE path; this test enumerates all
    branches only for the fixed four-mode counter, not at growing n.
    """
    n=Gamma.rows//2
    weights=charge_probabilities(Gamma)
    if charge<0 or charge>n or weights[charge]==0:return {}
    if not n:return {prefix:s.Integer(1)}
    result={}
    branch_sum=0
    for bit in (0,1):
        probability,new=first_mode_update(Gamma,bit)
        if probability==0 or charge-bit<0 or charge-bit>n-1:continue
        weight=charge_probabilities(new)[charge-bit]
        branch=s.simplify(probability*weight/weights[charge])
        branch_sum+=branch
        if branch==0:continue
        for word,value in exact_conditional_law(new,charge-bit,prefix+(bit,)).items():
            result[word]=s.simplify(branch*value)
    assert s.simplify(branch_sum-1)==0
    return result

def main():
    started=time.perf_counter()
    tau=s.Matrix([[2,0,0,s.sqrt(3)],[0,1,0,0],[0,0,1,0],[s.sqrt(3),0,0,2]])/6
    assert tau.trace()==1
    rho=s.kronecker_product(tau,tau)
    numbers=[int(i).bit_count() for i in range(16)]
    twirled=s.Matrix(16,16,lambda i,j:rho[i,j] if numbers[i]==numbers[j] else 0)
    target=[i for i in range(16) if numbers[i]==2]
    w2=s.simplify(sum(twirled[i,i] for i in target))
    assert w2==s.Rational(1,3)
    rho2=twirled.extract(target,target)/w2
    psi=s.zeros(6,1)
    psi[target.index(3)]=1/s.sqrt(2)
    psi[target.index(12)]=1/s.sqrt(2)
    assert s.simplify(rho2-s.eye(6)/12-psi*psi.T/2)==s.zeros(6)
    witness=s.eye(6)/2-psi*psi.T
    expectation=s.simplify((witness*rho2).trace())
    assert expectation==-s.Rational(1,12)

    # Independently acquire Gamma from explicit Jordan--Wigner Majoranas.
    I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
    majoranas=[]
    for mode in range(4):
        for op in (X,Y):
            majoranas.append(s.kronecker_product(*([Z]*mode+[op]+[I]*(3-mode))))
    Gamma=s.zeros(8)
    for a in range(8):
        for b in range(a+1,8):
            Gamma[a,b]=s.simplify(s.I*(rho*majoranas[a]*majoranas[b]).trace())
            Gamma[b,a]=-Gamma[a,b]
    fcs=charge_probabilities(Gamma)
    literal=[s.simplify(sum(rho[i,i] for i in range(16) if numbers[i]==q)) for q in range(5)]
    assert fcs==literal
    law=exact_conditional_law(Gamma,2)
    assert len(law)==6
    for word,probability in law.items():
        idx=sum(bit*2**(3-j) for j,bit in enumerate(word))
        assert s.simplify(probability-rho[idx,idx]/w2)==0

    result={
      'status':'EXACT_COUNTER_AND_CONDITIONAL_RECEIVER_PASSED',
      'full_rank_gaussian_pair_eigenvalues':['(2+sqrt(3))/6','(2-sqrt(3))/6','1/6','1/6'],
      'gaussian_components_in_exact_charge_twirl':5,
      'charge_probabilities':[str(x) for x in fcs],
      'N2_probability':str(w2),'nonconvex_gaussian_witness':str(expectation),
      'all_nonzero_conditional_output_probabilities':{''.join(map(str,k)):str(v) for k,v in sorted(law.items())},
      'scope':'general covariance/Pfaffian formula; all branches checked only for this exact four-mode interface counter',
      'not_acquired':['canonical Gibbs history weights','new mixing theorem','continuous-time trajectory law','physical data','practical advantage'],
      'time_seconds_excluding_imports':time.perf_counter()-started}
    Path(__file__).with_name('CANONICAL_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
