"""Numerical stress checks of exact rational gap choices and log-domain limits.
These checks do not supply approximants, interpolation rank, or proof of a theorem.
"""
import json, math
from fractions import Fraction as Q
from pathlib import Path

def verify(d,nu,log_b,max_log_plus_sigma,abs_lambda):
    nu=Q(nu)
    beta=(Q(1,2)+(1-Q(d)/nu))/2
    delta=(2*beta-1)/(4*beta*beta)
    theta=1-delta
    A=1-beta*delta
    C=(A/theta+1/A)/2
    B=(A+min(1/C,C*theta))/2
    gap0=nu*(A-theta)-d*(1-theta)
    eta=gap0/(4*nu*A)
    gap=nu*(A*(1-eta)-theta)-d*(1-theta)
    assert 0<theta<A<B<1 and A*A<theta
    assert 1<C and B<1/C and B<C*theta<1 and gap>0
    eps=min(float(gap)/4,.125)
    F0=math.ceil(max(2/float(theta),4*float(nu)/eps))+1
    # Fixed-error bound: d E_clear + sum(other E_sigma) + E_tr + E_hol.
    # Terms that later vanish with w_min are excluded and separately bounded.
    def ratios(m):
        logK0=m*math.log(float(C))
        # For C^m>=2, C^m/2 <=floor(C^m)<=C^m.
        # Thus 1/v0 <= exp[-m log(C theta/B)] using v0=2 K(theta/B)^m.
        invv=math.exp(-m*math.log(float(C*theta/B)))
        Kow=math.exp(m*math.log(float(C*B)))
        invw0=math.exp(m*math.log(float(B)))
        fixed=(d*(4*math.log(2)*F0*m*invv+log_b*Kow)
               +(d-1)*(max_log_plus_sigma*Kow+math.log(1.5)*invw0+math.log(2)*invv)
               +float(nu)/F0+2*math.log(2)*invv+4*(abs_lambda+1)*Kow)
        logL=2*math.log(float(eta))+m*math.log(float(B/A))-math.log(2*(m+1))
        return fixed,logL,logK0
    m=1
    while True:
        fixed,logL,logK=ratios(m)
        if logK>=math.log(2) and fixed<eps/2 and logL>math.log((d+1)*4/math.log(2)):
            break
        m*=2
        assert m<2**50
    # A sufficient minimum w for all arithmetic/analytic remaining errors.
    # log[2 max(1,K(|lambda|+1)+log2)] <= log K + log(2(abs_lambda+1+log2)).
    qcoef=(d*(4*math.log(2)*m+float(theta))
           +(d-1)*(logK+math.log(2*(abs_lambda+1+math.log(2))))
           +math.log(4)+logK+float(nu)+logK+math.log(8*(abs_lambda+1)))
    min_weight=math.ceil(4*qcoef/eps)
    return dict(d=d,nu=str(nu),beta=str(beta),theta=str(theta),A=str(A),B=str(B),C=str(C),
                eta=str(eta),gap=float(gap),epsilon=eps,F0=F0,m=m,
                fixed_error_upper=fixed,log_collision_L=logL,log_K_upper=logK,
                minimum_weight_for_error_only=min_weight,
                note='Actual weights must additionally satisfy MI successive separation; H and approximants are not instantiated.')

cases=[verify(1,'2.1',math.log(7),0,math.log(3/7)),
       verify(2,'4.2',math.log(3),0,abs(math.log((1+math.sqrt(2))/3))),
       verify(3,'6.3',math.log(5),0,abs(math.log(2**(1/3)/5))),
       verify(2,'4.02',0,100*math.log(10),100*math.log(10))]
p=Path(__file__).with_name('parameter_schedule_checks.json')
p.write_text(json.dumps(cases,indent=2)+'\n')
print(json.dumps(cases,indent=2))
