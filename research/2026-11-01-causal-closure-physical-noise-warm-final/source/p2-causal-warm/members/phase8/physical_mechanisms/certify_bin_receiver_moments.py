"""Actual integer-weight moments,75-digit Decimal, analytic quadrature error.
Uses only the standard library. No physical oscillator truncation or ideal
coefficient precision is inserted into the receiver.
"""
import json,math
from pathlib import Path
from decimal import Decimal as D,getcontext
getcontext().prec=85
PI=D('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')

def sin(x):
    while x>PI:x-=2*PI
    while x<-PI:x+=2*PI
    term=x;ans=x;n=1
    while abs(term)>D('1e-90'):
        term*=-x*x/D((2*n)*(2*n+1));ans+=term;n+=1
    return ans

def legendre(n,x):
    p0=D(1);p1=x
    for k in range(2,n+1):p0,p1=p1,((2*k-1)*x*p1-(k-1)*p0)/k
    return p1,n*(x*p1-p0)/(x*x-1)

def gauss(n):
    rows=[]
    for k in range(1,n+1):
        x=D(str(math.cos(math.pi*(k-.25)/(n+.5))))
        for it in range(15):
            p,dp=legendre(n,x);step=p/dp;x-=step
            if abs(step)<D('1e-80'):break
        p,dp=legendre(n,x)
        assert abs(p)<D('1e-78')
        rows.append((x,2/((1-x*x)*dp*dp)))
    return rows

HERE=Path(__file__).parent
weights=json.loads((HERE/'finite_bin_receiver_weights.json').read_text())
T=D(str(weights['T']));B=weights['bins'];dt=T/B;r=D('.1');kr=D(4);k0=D('.0001')
ints=weights['integer_weights'];norm=sum(D(x)**2 for x in ints).sqrt();sqrt_dt=dt.sqrt()
rows=gauss(16);labels=[(q,d-q) for d in range(3) for q in range(d+1)]
sums={label:D(0) for label in labels};A=D(0)
for j in range(B):
    left=dt*j;right=dt*(j+1);breaks=[left]+[x for x in [r,T-r] if left<x<right]+[right]
    fj=D(ints[j])/norm/sqrt_dt
    for l,rr in zip(breaks[:-1],breaks[1:]):
        middle=(l+rr)/2;half=(rr-l)/2;branch=0 if middle<r else (2 if middle>T-r else 1)
        for node,ww in rows:
            t=middle+half*node
            if branch==0:sw=sin(PI*t/(2*r));W=t/2-r*sin(PI*t/r)/(2*PI)
            elif branch==2:
                v=T-t;sw=sin(PI*v/(2*r));W=T-r-v/2+r*sin(PI*v/r)/(2*PI)
            else:sw=D(1);W=t-r/2
            H=kr.sqrt()*sw*(-k0*t/2-kr*W/2).exp();fac=fj*half*ww
            A+=fac*sw
            for q,s in labels:sums[(q,s)]+=fac*H*(t/T)**q*(W/T)**s
R=D('.025');h=dt/2;ratio=h/R;fmax=max(abs(D(i)/norm/sqrt_dt) for i in ints)
quaderr=2*T*fmax*10*ratio**32/(1-ratio);round_margin=D('1e-20');Abounderr=quaderr+round_margin
moments=[dict(t_power=q,W_power=s,value=str(sums[q,s]),absolute_upper=str(abs(sums[q,s])+quaderr+round_margin)) for q,s in labels]
params=[]
for eps,de in [('.001','.000001'),('.001','.0001')]:
    ep=D(eps);dd=D(de)
    lower=(1+ep).sqrt()*sum((abs(sums[q,s])+quaderr+round_margin)*(dd*T)**q*(ep*kr*T/2)**s/D(math.factorial(q)*math.factorial(s)) for q,s in labels)
    a=((ep*kr/2)**2+dd**2).sqrt();n=3;rate=kr+k0-2*a
    rem=(1+ep).sqrt()/D(math.factorial(n))*(kr*(kr*r).exp()*a**(2*n)*D(math.factorial(2*n))/rate**(2*n+1)).sqrt()
    total=lower+rem;cap=total/(1-total**2).sqrt()*(D('1.2')*320+D('.1')).sqrt()
    params.append(dict(readout_gain_bound=eps,detuning_bound=de,lower_moment_contribution_upper=str(lower),Taylor_remainder_upper=str(rem),total_overlap_upper=str(total),capped_dilation_error_N320=str(cap)))
out=dict(T=str(T),bins=B,arithmetic_precision_decimal=85,quadrature_order=16,Cauchy_radius=str(R),analytic_integrand_bound=10,analytic_quadrature_remainder=str(quaderr),outward_rounding_margin=str(round_margin),A=str(A),A_error_upper=str(Abounderr),moments=moments,parameter_bounds=params,
    qualification='Quadrature error bounded by complex-disk Taylor remainder. Standard-library Decimal85-digit arithmetic, converged Legendre roots and explicit sine Taylor series; 1e-20 outward margin dominates arithmetic. Not a machine-checked interval proof. Actual integer coefficients are checked.')
(HERE/'finite_bin_receiver_moment_bounds.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
