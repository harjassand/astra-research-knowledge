"""Independent first-variation checks; exact-model synthetic calculations."""
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent

def evaluate(theta,s,epsilon):
    def area(a):
        def f(u):
            r=a*math.sin(u)*(1+epsilon*math.sin(2*u))
            return r*r/(1-r*r)
        return quad(f,0,math.pi,epsabs=2e-12,epsrel=2e-12)[0]
    a=brentq(lambda a:area(a)-theta,0,.95/(1+abs(epsilon)),xtol=1e-14,rtol=1e-14)
    def rhs(u,z):
        su,cu=math.sin(u),math.cos(u)
        r=a*su*(1+epsilon*math.sin(2*u))
        rp=a*(cu*(1+epsilon*math.sin(2*u))+2*epsilon*su*math.cos(2*u))
        g=math.hypot(rp,r)/(1-r*r)
        h=2*(1+r*r)/(1-r*r)
        # Store the already scaled trace integrand to avoid a large exp(2l).
        return [g,4*math.exp(-2*(s-z[0]))*h*g]
    sol=solve_ivp(rhs,(0,math.pi),[0.,0.],method='DOP853',rtol=2e-12,atol=2e-13)
    assert sol.success
    K=sol.y[0,-1]
    trQ=sol.y[1,-1]+2*(-np.expm1(-2*(s-K)))
    return {'a':a,'length':float(K),'trace_noise':float(trQ),'area_residual':area(a)-theta}

def analytic_derivative(theta,s):
    L=math.sqrt(theta*theta+2*math.pi*theta)
    a=L/(math.pi+theta);b=math.pi/(math.pi+theta)
    def f(u):
        su,cu=math.sin(u),math.cos(u);w=su*su;x=a*a*w;d=1-x
        ell=(a/b)*math.atan2(b*su,cu)
        if x<1e-4:
            bracket=-sum(x**k/k for k in range(2,9))
        else:
            bracket=x+math.log1p(-x)
        dr=cu*(-2*d/(a**3))*bracket
        h1=8*a*su/(d*d)*dr
        weight=math.exp(-2*(s-L+ell))*math.expm1(-2*L+4*ell)
        return 4*weight*h1*a/d
    return quad(f,0,math.pi/2,epsabs=2e-13,epsrel=2e-12)[0]

def main():
    rows=[];epsilon=1e-4
    for theta in [.05,.2,.7,math.pi/2,math.pi]:
        L=math.sqrt(theta*theta+2*math.pi*theta);s=L+.2
        minus=evaluate(theta,s,-epsilon);zero=evaluate(theta,s,0.);plus=evaluate(theta,s,epsilon)
        fd=(plus['trace_noise']-minus['trace_noise'])/(2*epsilon)
        analytic=analytic_derivative(theta,s)
        rows.append({'theta':theta,'attenuation':s,'epsilon':epsilon,
                     'analytic_trace_derivative':analytic,'finite_difference_derivative':fd,
                     'absolute_difference':abs(analytic-fd),
                     'length_zero_error':zero['length']-L,
                     'length_evenness_error':plus['length']-minus['length'],
                     'length_increase_over_epsilon_squared':(plus['length']-L)/(epsilon*epsilon),
                     'positive_epsilon_trace_change':plus['trace_noise']-zero['trace_noise'],
                     'max_area_residual':max(abs(z['area_residual']) for z in [minus,zero,plus])})
    assert all(r['analytic_trace_derivative']<0 for r in rows)
    assert all(r['positive_epsilon_trace_change']<0 for r in rows)
    assert all(r['length_increase_over_epsilon_squared']>0 for r in rows)
    out={'scope':'Synthetic audit of analytic first variation; Lambda=D=1; not physical data',
         'rows':rows}
    (HERE/'variation_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
