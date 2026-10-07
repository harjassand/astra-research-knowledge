"""Deterministic quadrature diagnostic; not a proof of the asymptotic bounds."""
from math import erf, erfc, exp, log, pi, sqrt, tan
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SQ2 = sqrt(2.0)
SQ2PI = sqrt(2.0*pi)

def phi(x):
    return exp(-0.5*x*x)/SQ2PI

def cdf(x):
    return 0.5*erfc(-x/SQ2)

def mass(a,b):
    if a > 0:
        return 0.5*(erfc(a/SQ2)-erfc(b/SQ2))
    return cdf(b)-cdf(a)

def linear_mass(a,b,left,right,theta):
    m = mass(a-theta,b-theta)
    first = theta*m + phi(a-theta)-phi(b-theta)
    return left*m + (right-left)*(first-a*m)/(b-a)

def hat_mass(nodes,i,theta):
    c = nodes[i]
    if i == 0:
        total = cdf(c-theta)
    else:
        total = linear_mass(nodes[i-1],c,0.0,1.0,theta)
    if i == len(nodes)-1:
        total += 0.5*erfc((c-theta)/SQ2)
    else:
        total += linear_mass(c,nodes[i+1],1.0,0.0,theta)
    return total

def simpson(fun,a,b,panels=128):
    if a == b:
        return 0.0
    h=(b-a)/panels
    total=fun(a)+fun(b)
    total+=4*sum(fun(a+(2*i-1)*h) for i in range(1,panels//2+1))
    total+=2*sum(fun(a+2*i*h) for i in range(1,panels//2))
    return total*h/3

def diagnostic(J,theta,panels):
    cutoff=8+sqrt(16*log(J))
    nodes=[tan(pi*(j/J-0.5)) for j in range(1,J)]
    nodes=[x for x in nodes if abs(x)<=cutoff]
    reference=[hat_mass(nodes,i,0.0) for i in range(len(nodes))]
    shifted=[hat_mass(nodes,i,theta) for i in range(len(nodes))]
    ratios=[p/q for p,q in zip(shifted,reference)]
    tv=chi=0.0
    intervals=[(-max(12,nodes[-1]+8),nodes[0],ratios[0],ratios[0])]
    intervals.extend((a,b,ratios[i],ratios[i+1]) for i,(a,b) in enumerate(zip(nodes,nodes[1:])))
    intervals.append((nodes[-1],max(12,nodes[-1]+8),ratios[-1],ratios[-1]))
    for a,b,c,d in intervals:
        def qratio(x):
            return c+(d-c)*(x-a)/(b-a)
        def tv_fun(x):
            likelihood=exp(theta*x-0.5*theta*theta)
            return 0.5*phi(x)*abs(qratio(x)-likelihood)
        def chi_fun(x):
            likelihood=exp(theta*x-0.5*theta*theta)
            return phi(x)*(qratio(x)-likelihood)**2/likelihood
        tv+=simpson(tv_fun,a,b,panels)
        chi+=simpson(chi_fun,a,b,panels)
    return dict(J=J,theta=theta,alphabet=len(nodes),panels=panels,
                normalizer0=sum(reference),normalizer1=sum(shifted),
                tv=tv,chi2=chi,tv_scaled=tv*J*J/abs(theta),
                chi_scaled=chi*J**4/(theta*theta))

if __name__ == '__main__':
    rows=[]
    for J in (16,32,64,128,256,512,1024):
        for theta in (1.0,0.1,0.0001):
            for panels in (128,256):
                rows.append(diagnostic(J,theta,panels))
    with (ROOT/'hat_diagnostic.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        if row['panels']==256:
            print(f"J={row['J']:4} theta={row['theta']:.4g} "
                  f"TV*J²/theta={row['tv_scaled']:.6g} "
                  f"chi²*J⁴/theta²={row['chi_scaled']:.6g} "
                  f"mass0={row['normalizer0']:.12g} mass1={row['normalizer1']:.12g}")
