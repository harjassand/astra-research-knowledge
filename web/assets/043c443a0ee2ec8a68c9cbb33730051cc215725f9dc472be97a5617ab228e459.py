"""Bounded floating diagnostic for the analytic covariance-field construction.

Mid-sized R only: no sampling or numerical evaluation of enormous rare tails.
This does not certify quadrature, proof, generality, or novelty.
"""
import json
import math
import time
from pathlib import Path


ROOT2 = math.sqrt(2)
ROOT2PI = math.sqrt(2*math.pi)


def cdf(t):
    return math.erfc(-t/ROOT2)/2


def cdf_difference(a,b):
    if b >= 0:
        return (math.erfc(b/ROOT2)-math.erfc(a/ROOT2))/2
    if a <= 0:
        return (math.erfc(-a/ROOT2)-math.erfc(-b/ROOT2))/2
    return 1-math.erfc(a/ROOT2)/2-math.erfc(-b/ROOT2)/2


def h_and_derivative(y,R,sigma):
    # Composite Simpson on an exact compact positive integral.
    n=32
    hs=0.0
    ds=0.0
    for j in range(n+1):
        u=j/n
        w=(1 if j in (0,n) else 4 if j%2 else 2)*6*u*(1-u)
        t=(y-R+1-u)/sigma
        hs += w*cdf(t)
        ds += w*math.exp(-t*t/2)/(sigma*ROOT2PI)
    return hs/(3*n),ds/(3*n)


def tail_probability_Y(t,R):
    zz=-math.expm1(-2*R)
    return (math.erfc(t/ROOT2)/2
            -math.exp(-2*R)*math.erfc((t-2*R)/ROOT2)/2
            +math.exp(-t+.5)*cdf_difference(t-1,t-2*R-1))/zz


def one(R):
    K=64*R
    M=math.log(K)
    zz=-math.expm1(-2*R)
    sigma=math.sqrt(1/(2*math.log(2*M/math.log(2))))
    lo=-8
    hi=2*R+8
    n=4096
    dx=(hi-lo)/n
    vals=dict(normalization=0.0,energy=0.0,event_probability=0.0,false_positive=0.0)
    for j in range(n+1):
        y=lo+j*dx
        w=1 if j in (0,n) else 4 if j%2 else 2
        rho=math.exp(-y+.5)/zz*cdf_difference(2*R-y+1,1-y)
        h,hp=h_and_derivative(y,R,sigma)
        a=math.exp(M*h)
        qE=math.erfc(math.sqrt(8*R/(2*a)))
        vals['normalization'] +=w*rho
        vals['energy'] +=w*rho*M*M*hp*hp/2
        vals['event_probability'] +=w*rho*qE
        if y<=R-2:
            vals['false_positive'] +=w*rho*qE
    vals={key:v*dx/3 for key,v in vals.items()}
    pB=tail_probability_Y(R-2,R)
    eta=vals['false_positive']/vals['event_probability']
    hb=0 if eta==0 else -eta*math.log(eta)-(1-eta)*math.log1p(-eta)
    ilower=vals['event_probability']*((1-eta)*math.log(1/pB)-hb)
    jbound=(9/8)*(math.e-1)*math.exp(.5+sigma*sigma/2)/zz*math.exp(-R)*M*M
    ibound=(1-math.exp(-1))/(16*math.sqrt(math.e))*R*math.exp(-R)
    hlow,_=h_and_derivative(R-2,R,sigma)
    hhigh,_=h_and_derivative(R+1,R,sigma)
    assert abs(vals['normalization']-1)<1e-7
    assert math.exp(M*hlow)<=math.sqrt(2)*(1+1e-8)
    assert math.exp(M*hhigh)>=K/math.sqrt(2)*(1-1e-8)
    assert vals['energy'] <=jbound*1.01
    assert ilower>=ibound*.99
    return dict(R=R,K=K,sigma=sigma,**vals,
                pB=pB,event_posterior_error=eta,
                numerical_event_information_lower=ilower,
                analytic_information_lower=ibound,
                analytic_Fisher_upper=jbound,
                numerical_event_I_over_5J=ilower/(5*vals['energy']),
                scope='Uncertified Simpson diagnostic; exact inequalities are in 01_contrast_and_scale.txt.')


if __name__=='__main__':
    started=time.perf_counter()
    result=dict(status='PASS',fixtures=[one(R) for R in (32,64)],
                seconds=time.perf_counter()-started,
                work_budget={'outer_points_per_fixture':4097,'inner_points':33,'fixtures':2},
                limitation='No MI estimator, rare-event acquisition, interval integration, quantum memory, or novelty certification.')
    p=Path(__file__).with_suffix('.json')
    p.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','seconds':result['seconds'],
                      'normalization_residuals':[abs(x['normalization']-1) for x in result['fixtures']],
                      'output':str(p)}))
