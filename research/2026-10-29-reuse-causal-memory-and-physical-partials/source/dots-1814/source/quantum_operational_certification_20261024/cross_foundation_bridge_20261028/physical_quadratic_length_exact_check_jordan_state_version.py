#!/usr/bin/env python3
"""Singer constant-signal physical delay: exact finite fields + rational certificates.
Numerical density matrices are display/supporting checks, not the exact proof.
"""
from itertools import product
from collections import Counter
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json
import sympy as sp
import numpy as np
root=Path(__file__).resolve().parent
x=sp.symbols('x')

def singer(p,n):
    q=p**n;m=3*n
    coeff=next(c for c in product(range(p),repeat=m) if c[0] and sp.Poly(x**m+sum(c[i]*x**i for i in range(m)),x,modulus=p).is_irreducible)
    zero=(0,)*m;one=(1,)+(0,)*(m-1)
    def add(a,b):return tuple((i+j)%p for i,j in zip(a,b))
    def mul(a,b):
        c=[0]*(2*m-1)
        for i in range(m):
            for j in range(m):c[i+j]=(c[i+j]+a[i]*b[j])%p
        for k in range(2*m-2,m-1,-1):
            t=c[k]
            for j in range(m):c[k-m+j]=(c[k-m+j]-t*coeff[j])%p
        return tuple(c[:m])
    def power(a,k):
        v=one
        while k:
            if k&1:v=mul(v,a)
            a=mul(a,a);k//=2
        return v
    order=q**3-1;prime_divisors=list(sp.factorint(order))
    gen=next(a for a in product(range(p),repeat=m) if a!=zero and all(power(a,order//l)!=one for l in prime_divisors))
    r=q*q+q+1;D=[]
    for k in range(r):
        a=power(gen,k);tr=add(add(a,power(a,q)),power(a,q*q))
        assert power(tr,q)==tr
        if tr==zero:D.append(k)
    assert len(D)==q+1
    count=Counter((a-b)%r for a in D for b in D if a!=b)
    assert count==Counter({k:1 for k in range(1,r)})
    return q,coeff,gen,D

rows=[]
for p,n in [(2,1),(3,1),(2,2),(5,1),(7,1),(2,3)]:
    q,coeff,gen,exponents=singer(p,n);d=q+1;r=q*q+q+1
    # Exact cancellation at every early first-test time, INCLUDING composite r.
    cyclo=sp.Poly(sp.cyclotomic_poly(r,x),x)
    for k in range(r):
        residue=Counter((t*(k+1))%r for t in range(r))
        polynomial=sp.Poly.from_dict({(j,):v for j,v in residue.items()},x)
        rem=sp.rem(polynomial,cyclo)
        assert rem==(sp.Poly(r,x) if k==r-1 else sp.Poly(0,x))
    b=[2*j-d+1 for j in range(d)];S=sum(t*t for t in b);eps=Q(1,8*d)
    assert sum(b)==0 and S==d*(d*d-1)//3
    assert max(abs(t)+d-1 for t in b)*eps<=Q(1,4)
    negative_diagonal=[-1+Q(t,S) for t in b]
    assert all(v<0 for v in negative_diagonal)
    assert sum(abs(v) for v in negative_diagonal)==d
    scale=Q(1,r)/eps;T_bound=2*d*scale
    assert 1/T_bound>=Q(3,64)
    beta=Q(1,2*r);damping=(1-beta)**(r-1)
    assert damping>=1-(r-1)*beta>Q(1,2)
    signal_bound=damping/T_bound
    assert signal_bound>Q(3,128)
    # Explicit physical matrices, checked numerically in addition to exact margins.
    u=np.exp(2j*np.pi*np.array(exponents)/r);U=np.diag(u);tau=np.eye(d)/d
    B=np.ones((d,d));np.fill_diagonal(B,b);E=np.eye(d)/2+float(eps)*B
    # Spectrum of Delta equals that of a REAL RATIONAL symmetric matrix.
    real_Q=np.ones((d,d))-np.eye(d)+np.diag(np.array(b,dtype=float)/S)
    ev,V=np.linalg.eigh(float(scale)*real_Q)
    Delta=(u[:,None]*V)@np.diag(ev)@(u[:,None]*V).conj().T
    positive=(u[:,None]*V)@np.diag(np.maximum(ev,0))@(u[:,None]*V).conj().T
    negative=(u[:,None]*V)@np.diag(np.maximum(-ev,0))@(u[:,None]*V).conj().T
    T=float(np.sum(np.abs(ev)));rp=tau/2+positive/T;rm=tau/2+negative/T
    assert abs(np.trace(rp)-1)<1e-12 and abs(np.trace(rm)-1)<1e-12
    assert np.linalg.eigvalsh(rp)[0]>=1/(2*d)-1e-12 and np.linalg.eigvalsh(rm)[0]>=1/(2*d)-1e-12
    assert T<=float(T_bound)+1e-11
    early=[]
    for k in range(r):
        uk=u**k;diff=float(1-beta)**k*(uk[:,None]*(rp-rm)*uk.conj()[None,:])
        gap=float(np.trace(E@diff).real)
        if k<r-1:early.append(abs(gap))
        else:late=abs(gap)
    assert max(early)<2e-11 and late>=float(signal_bound)-2e-11
    vU=U.T.reshape(-1);Ja=(1-float(beta))*np.outer(vU,vU.conj())+float(beta)/d*np.eye(d*d)
    J1=np.kron(E.T,tau);J0=np.kron((np.eye(d)-E).T,tau)
    assert np.linalg.eigvalsh(Ja)[0]>=float(beta)/d-1e-11
    assert np.linalg.eigvalsh(J0)[0]>=1/(4*d)-1e-11 and np.linalg.eigvalsh(J1)[0]>=1/(4*d)-1e-11
    partial=lambda J:np.einsum('iaja->ij',J.reshape(d,d,d,d))
    assert np.max(np.abs(partial(Ja)-np.eye(d)))<1e-11
    assert np.max(np.abs(partial(J0+J1)-np.eye(d)))<1e-11
    rows.append({'q':q,'d':d,'r':r,'field_characteristic':p,'base_extension_degree':n,
      'irreducible_polynomial_low_coefficients':list(coeff),'primitive_element':list(gen),'difference_set':exponents,
      'all_nonzero_ordered_difference_multiplicities':1,'exact_cyclotomic_moments_checked':r,
      'all_short_native_words_agree_through':r-1,'first_distinguishing_native_length':r,
      'forward_depolarizing_beta':str(beta),'forward_choi_floor':str(beta/d),'test_choi_floor':str(Q(1,4*d)),
      'initial_eigenvalue_floor':str(Q(1,2*d)),'exact_trace_norm_upper':str(T_bound),
      'exact_unitary_signal_lower':str(1/T_bound),'exact_interior_signal_lower':str(signal_bound),
      'numerical_trace_norm_display':T,'numerical_interior_signal_display':late,'maximum_numerical_early_gap':max(early)})
report={'status':'PASS exact finite-field/root-sum/rational-margin proof checks, numerical physical replay supports only',
 'source_calls':0,'episode_starts':0,'rng_calls':0,'hardware_execution':False,
 'source_sha256':hashlib.sha256((root/'PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH_jordan_state_version.md').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'uniform_interior_signal_lower':'3/128','uniform_unitary_signal_lower':'3/64','dimensions':rows}
(root/'physical_quadratic_length_exact_check_jordan_state_version.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'source_sha256':report['source_sha256'],'cases':[{'q':v['q'],'d':v['d'],'r':v['r'],'signal':v['numerical_interior_signal_display'],'early_gap':v['maximum_numerical_early_gap']} for v in rows]},indent=2))
