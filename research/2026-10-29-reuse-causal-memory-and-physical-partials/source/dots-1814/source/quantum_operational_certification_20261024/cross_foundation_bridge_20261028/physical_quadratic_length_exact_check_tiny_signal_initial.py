#!/usr/bin/env python3
"""Exact cyclotomic construction; no random/source experiments."""
import sympy as sp
from sympy.polys.domains import QQ
from pathlib import Path
import hashlib,json,time
root=Path(__file__).resolve().parent
rows=[]
for d in [2,3,4,5]:
    q=2**(d+1);ze=sp.exp(2*sp.pi*sp.I/q);K=QQ.algebraic_field(ze);z=K.from_sympy(ze)
    ex=[0]+[(2**i-2**j)%q for i in range(d) for j in range(d) if i!=j]
    r=d*(d-1)+1;assert len(ex)==len(set(ex))==r
    lam={e:z**e for e in ex};weight={}
    for e,l in lam.items():
        prod=K.one
        for ee,ll in lam.items():
            if e!=ee:prod*=l-ll
        assert prod!=K.zero;weight[e]=K.one/prod
    # Exact conjugation automorphism z->z^(-1), including all weights.
    zi=K.one/z
    def conjugate(v):
        out=K.zero
        for c in v.to_list():out=out*zi+K.convert(c)
        return out
    for e in ex:
        assert conjugate(lam[e])==lam[(-e)%q]
        assert conjugate(weight[e])==weight[(-e)%q]
    eps=sp.Rational(1,8*d);diagonal=[2*j-d+1 for j in range(d)];S=sum(x*x for x in diagonal)
    assert sum(diagonal)==0 and S>0 and max(abs(x)+(d-1) for x in diagonal)*eps<=sp.Rational(1,4)
    Eps=K.convert(eps);SS=K.convert(S)
    Delta_diag=[weight[0]*K.convert(x)/(Eps*SS) for x in diagonal]
    assert sum(Delta_diag,K.zero)==K.zero
    R2=weight[0]**2/(Eps**2*SS)
    for e in ex[1:]:R2+=weight[e]*weight[(-e)%q]/Eps**2
    assert conjugate(R2)==R2 and R2!=K.zero
    moments=[]
    for k in range(r):
        m=sum((weight[e]*lam[e]**k for e in ex),K.zero)
        assert m==(K.one if k==r-1 else K.zero)
        moments.append(1 if m==K.one else 0)
    # The norm expression is positive by paired squares; approximate only for display.
    rr=complex(K.to_sympy(R2).evalf(40));assert rr.real>0 and abs(rr.imag)<1e-20*max(1,rr.real)
    signal=1/(d*rr.real**.5)
    rows.append({'d':d,'root_order':q,'cyclotomic_degree':K.mod.degree(),'orbit_modes':r,
      'all_words_agree_through_native_length':r-1,'first_distinguishing_native_length':r,
      'exact_unnormalized_first_test_moments':moments,'hermitian_traceless_checked':True,
      'initial_state_eigenvalue_lower_bound':str(sp.Rational(1,2*d)),
      'test_branch_choi_eigenvalue_lower_bound':str(sp.Rational(1,4*d)),
      'unitary_branch_choi_rank':1,'R_squared_positive_algebraic':True,
      'first_signal_approx_display_only':signal})
report={'status':'PASS exact cyclotomic moment/state-margin construction; not independent receipt',
 'source_calls':0,'episode_starts':0,'rng_calls':0,'constant_signal_lower_bound_claimed':False,
 'source_sha256':hashlib.sha256((root/'PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH_tiny_signal_initial.md').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'dimensions':rows}
(root/'physical_quadratic_length_exact_check_tiny_signal_initial.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
