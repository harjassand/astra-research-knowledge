#!/usr/bin/env python3
"""Finite exact certificates implying all-state inequalities for one raw model.

This is author verification, not an independent audit. Polynomial coefficient
and monotonic-ratio proofs cover unbounded integer tails; sampled states are
not used to establish the uniform statements.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import sympy as sp
import pinned_phase_checks as model

P=Path(__file__).resolve().parent
n=model.N;x=sp.Symbol('x',nonnegative=True)
t=model.T;u=model.U;ct=model.ct
Nstar=10000;Astar=100000;reward=F(1001,1000)
cz=(1-1/u)/2

def rat(a):return sp.Rational(a.numerator,a.denominator) if isinstance(a,F) else sp.sympify(a)

def coefficients_nonnegative(expr,shift=10):
    num,den=sp.fraction(sp.factor(expr))
    pn=sp.Poly(sp.expand(num.subs(n,x+shift)),x)
    pd=sp.Poly(sp.expand(den.subs(n,x+shift)),x)
    if pd.LC()<0:pn=-pn;pd=-pd
    assert all(c>=0 for c in pn.all_coeffs()),pn.as_expr()
    assert all(c>=0 for c in pd.all_coeffs()) and pd.eval(0)>0,pd.as_expr()
    return {'shift':shift,'numerator_coefficients':[str(c) for c in pn.all_coeffs()],
            'denominator_coefficients':[str(c) for c in pd.all_coeffs()]}

if __name__=='__main__':
    cert={}
    cert['epsilon_lower']=coefficients_nonnegative(model.eps-1/(200*n))
    cert['phase_profile_upper']=[coefficients_nonnegative(2-y) for y in model.h]
    # Exact marked-state cone bound, using Qh<=ct*n and a<=n/2.
    f=sp.Rational(3,2)+sp.Rational(7,5)*n*(n-1)
    r=sp.Rational(5,4)*n+sp.Rational(7,6)*n*(n-1)*(n-2)
    wupper=rat(ct)*n+(rat(t)-1)*(n/2)*f-(1-1/rat(t))*r
    cert['marked_cone_LW_le_minus_n_over_100']=coefficients_nonnegative(-n/100-wupper)
    cert['marked_positive_part_bound']=coefficients_nonnegative(n**2/5-(2*rat(ct)+(rat(t)-1)*f))
    # For a>=2, every possibly positive reservoir coefficient is absent.
    # For a=0,1 its maximum after u^a is exactly u-1.
    assert u*(u-1-(1-1/u))<u-1
    assert 2>=4*u/3  # gives bath drift <= -(1-1/u)*a/4 for all a>=2.
    ratio=u/t
    assert F(Nstar+1,Nstar)*ratio<=1
    assert (u-1)*ratio**Nstar<=F(1,400*Nstar)
    cert['unmarked_tail_monotonicity']={
        'ratio':str(ratio),'start':Nstar,
        'exact_base_inequality':'(u-1)*(u/t)^Nstar <= 1/(400*Nstar)',
        'step_inequality':'((n+1)/n)*(u/t)<=1 for n>=Nstar'}
    # In a>n/2, the all-state exponential comparison has this rational base.
    rho=u**3/t**2
    assert rho>1
    assert rho>=F((Nstar+2)**2,Nstar**2)
    for nn in [Nstar,Nstar+1]:
        assert cz*rho**(nn//2)>=F(2*nn**2,5)
    cert['high_A_cone']={'rho':str(rho),'start_even':Nstar,'start_odd':Nstar+1,
        'exact_base_inequalities':'cz*rho^floor(n/2) >= 2*n^2/5 at both starts',
        'two_step_monotonicity':'rho >= ((n+2)/n)^2 for all n>=Nstar'}
    # The bounded-n / unbounded-a cylinder is covered without enumerating n.
    assert cz*u**Astar>=2*F(Nstar**2,5)*t**Nstar
    assert all((t-1)*F(f.subs(n,nn))<=F(Nstar**2,5) for nn in range(10))
    cert['bounded_inventory_high_A']={'inventory_bound':Nstar,'Astart':Astar,
        'exact_inequality':'cz*u^Astar >= 2*(Nstar^2/5)*t^Nstar'}
    # Reward reserves used in the proof below the certificate.
    assert t**Nstar/F(400*Nstar)>=reward**(Nstar+1)
    assert F(Nstar+1,Nstar)*(reward/t)<1
    assert (cz/2)*(u/reward)**Nstar>=1
    assert (F(Nstar,100)-(u-1))*t**Nstar>=reward**(Nstar+1)
    cert['reward_reserves']={'reward_base':str(reward),
        'exact_inequalities':[
           't^Nstar/(400*Nstar) >= reward^(Nstar+1)',
           '((n+1)/n)*(reward/t)<1 for n>=Nstar',
           '(cz/2)*(u/reward)^Nstar>=1',
           '(Nstar/100-(u-1))*t^Nstar >= reward^(Nstar+1)']}
    # Explicit finite head and factored reward bound. Enzyme source counts are
    # 0/1, and every raw free-species source order is at most three.
    S=sum(k for y,z,k,label in model.raw)
    assert max(sum(y[:2]) for y,z,k,label in model.raw)<=3
    Mbound=Astar+Nstar+1
    Qbound=S*Mbound**3
    cert['global_foster']={
        'head':'0<=a<Astar and 0<=n<Nstar; all valid phases',
        'Astar':Astar,'Nstar':Nstar,'Mbound':Mbound,'rate_sum':str(S),
        'Qbound':str(Qbound),'V_neighbor_bound':{'sum':[{'coefficient':'2','base':str(t),'exponent':Nstar+1},{'coefficient':'1','base':str(u),'exponent':Mbound}]},
        'claim':'L V <= -reward^M + C*1_head',
        'C_factored':{'sum':[{'product':[str(Qbound),{'sum':[{'product':['2',{'power':[str(t),Nstar+1]}]},{'power':[str(u),Mbound]}]}]},{'power':[str(reward),Mbound]}]},
        'invariant_bound':'pi(reward^M)<=C on every closed irreducible class',
        'materialized_C':'NOT_MATERIALIZED; exact finite positive rational expression'}
    raw_path=P/'results/pinned_phase_raw.json'
    cert['model_raw_sha256']=hashlib.sha256(raw_path.read_bytes()).hexdigest()
    out={'scope':'Finite exact symbolic/rational certificates with the accompanying all-state proof. Author verification, not independent review.',
         'results':'PASS','tail_not_sampled':True,'certificate':cert,
         'scientific_limit':'One explicit six-phase pinned model. Not arbitrary-core recurrence or a practical capability.'}
    (P/'results/pinned_uniform_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'results':'PASS','certificate_path':str(P/'results/pinned_uniform_certificate.json'),
        'global_head':cert['global_foster']['head'],'Astar':Astar,'Nstar':Nstar,'reward':str(reward),
        'raw_sha256':cert['model_raw_sha256'],'certificate_bytes':(P/'results/pinned_uniform_certificate.json').stat().st_size},indent=2))
