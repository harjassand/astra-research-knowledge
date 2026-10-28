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

def first_test(d,r,alpha,j,k):
    return Q(1,2)+Q(1,4*d)+alpha**k*Q(r*int((k+j)%r==0)-1,8*d*d)

def word_probability(d,r,alpha,j,word):
    mass=Q(1);k=0;tested=False
    for z in word:
        if z=="a":
            if not tested:k+=1
        else:
            p=Q(1,2)+Q(1,4*d) if tested else first_test(d,r,alpha,j,k)
            mass*=p if z=="b1" else 1-p
            tested=True
    return mass

def feedback_records(d,r,alpha,j,H,pid):
    leaves={}
    def visit(word,mass):
        depth=len(word);bits=tuple(int(z[-1]) for z in word if z!="a")
        if depth==H or (depth and bits and (depth+pid+sum(bits))%11==0):
            leaves[word]=mass;return
        action="a" if (depth+2*pid+sum(bits))%4==0 else "b"
        if action=="a":visit(word+("a",),mass)
        else:
            p=Q(1,2)+Q(1,4*d) if bits else first_test(d,r,alpha,j,depth)
            visit(word+("b1",),mass*p);visit(word+("b0",),mass*(1-p))
    visit((),Q(1));assert sum(leaves.values())==1
    return leaves

rows=[];word_checks=feedback_checks=0
for p,n in [(2,1),(3,1),(2,2),(5,1),(7,1),(2,3)]:
    q,coeff,gen,exponents=singer(p,n);d=q+1;r=q*q+q+1
    # Exact squared-overlap polynomial for every t, including composite r.
    cyclo=sp.Poly(sp.cyclotomic_poly(r,x),x)
    for t in range(r):
        residue=Counter(((a-b)*t)%r for a in exponents for b in exponents)
        polynomial=sp.Poly.from_dict({(j,):v for j,v in residue.items()},x)
        assert sp.rem(polynomial,cyclo)==sp.Poly(d*d if t==0 else d-1,x)
    beta=Q(1,2*r);alpha=1-beta;damping=alpha**(r-2)
    assert damping>=1-(r-2)*beta>Q(1,2)
    unitary_signal=Q(r,8*d*d);signal=damping*unitary_signal
    assert unitary_signal>=Q(3,32) and signal>Q(3,64)
    for a in [Q(1),alpha]:
        for k in range(r-2):assert first_test(d,r,a,1,k)==first_test(d,r,a,2,k)
        assert first_test(d,r,a,2,r-2)-first_test(d,r,a,1,r-2)==a**(r-2)*unitary_signal
        for j in [1,2]:
            for k in range(2*r):assert 0<first_test(d,r,a,j,k)<1
        if q==2:
            for h in range(r-1):
                for word in product(["a","b0","b1"],repeat=h):
                    assert word_probability(d,r,a,1,word)==word_probability(d,r,a,2,word)
                    word_checks+=1
        if q in [2,3]:
            for pid in range(12):
                assert feedback_records(d,r,a,1,r-2,pid)==feedback_records(d,r,a,2,r-2,pid)
                feedback_checks+=1
    # Supplementary numerical full physical matrices, with exact margins proved above.
    u=np.exp(2j*np.pi*np.array(exponents)/r);U=np.diag(u);tau=np.eye(d)/d
    s=np.ones(d)/np.sqrt(d);E=np.eye(d)/2+np.outer(s,s)/4
    rho=[tau/2+np.outer(u**j*s,(u**j*s).conj())/2 for j in [1,2]]
    assert all(abs(np.trace(v)-1)<1e-12 for v in rho)
    assert all(np.linalg.eigvalsh(v)[0]>=1/(2*d)-1e-12 for v in rho)
    max_residual=0.
    for j,state in enumerate(rho,1):
        for k in range(2*r):
            uk=u**k;physical=tau+float(alpha)**k*(uk[:,None]*(state-tau)*uk.conj()[None,:])
            gap=abs(float(np.trace(E@physical).real)-float(first_test(d,r,alpha,j,k)))
            max_residual=max(max_residual,gap)
    assert max_residual<2e-11
    vU=U.T.reshape(-1);Ja=float(alpha)*np.outer(vU,vU.conj())+float(beta)/d*np.eye(d*d)
    J1=np.kron(E.T,tau);J0=np.kron((np.eye(d)-E).T,tau)
    assert np.linalg.eigvalsh(Ja)[0]>=float(beta)/d-1e-11
    assert np.linalg.eigvalsh(J0)[0]>=1/(4*d)-1e-11 and np.linalg.eigvalsh(J1)[0]>=1/(4*d)-1e-11
    partial=lambda J:np.einsum('iaja->ij',J.reshape(d,d,d,d))
    assert np.max(np.abs(partial(Ja)-np.eye(d)))<1e-11
    assert np.max(np.abs(partial(J0+J1)-np.eye(d)))<1e-11
    rows.append({'q':q,'d':d,'r':r,'field_characteristic':p,'base_extension_degree':n,
      'irreducible_polynomial_low_coefficients':list(coeff),'primitive_element':list(gen),'difference_set':exponents,
      'all_nonzero_ordered_difference_multiplicities':1,'exact_cyclotomic_overlaps_checked':r,
      'all_short_native_words_agree_through':r-2,'first_distinguishing_native_length':r-1,
      'forward_depolarizing_beta':str(beta),'forward_choi_floor':str(beta/d),'test_choi_floor':str(Q(1,4*d)),
      'initial_eigenvalue_floor':str(Q(1,2*d)),'common_postreset_probability':str(Q(1,2)+Q(1,4*d)),
      'exact_unitary_signal':str(unitary_signal),'exact_interior_signal':str(signal),
      'numerical_interior_signal_display':float(signal),'maximum_numerical_formula_residual':max_residual})
report={'status':'PASS exact finite-field/root-sum/rational-margin/full-word checks; numerical matrix replay supplementary',
 'source_calls':0,'episode_starts':0,'rng_calls':0,'hardware_execution':False,
 'source_sha256':hashlib.sha256((root/'PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH.md').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'uniform_interior_signal_lower':'3/64','uniform_unitary_signal_lower':'3/32',
 'exact_full_short_word_pairs':word_checks,'exact_adaptive_full_record_pairs':feedback_checks,'dimensions':rows}
(root/'physical_quadratic_length_exact_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'source_sha256':report['source_sha256'],'word_pairs':word_checks,'feedback_pairs':feedback_checks,'cases':[{'q':v['q'],'d':v['d'],'r':v['r'],'signal':v['numerical_interior_signal_display'],'matrix_formula_residual':v['maximum_numerical_formula_residual']} for v in rows]},indent=2))
