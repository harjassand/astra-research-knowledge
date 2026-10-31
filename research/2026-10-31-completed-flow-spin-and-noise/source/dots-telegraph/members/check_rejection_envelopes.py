"""Floating sanity checks only; does not implement certified random sampling."""
import math,json

gamma_rows=[];poisson_rows=[]
for m in list(range(1,100))+[1000,10000,1000000]:
    d=2.0**((m.bit_length()-1)//2-1)
    a,b=m-d,m+d
    Z=2*m/d+2*d
    targetmass=math.exp(math.lgamma(m+1)+m-m*math.log(m))
    acc=targetmass/Z
    assert acc>1/32
    maxgap=-math.inf
    for i in range(1,501):
        x=max(.000001,m+((i/500)*12-6)*math.sqrt(m))
        logf=m*math.log(x/m)-x+m
        logg=(d/(m-d))*(x-a) if x<a else (-(d/(m+d))*(x-b) if x>b else 0)
        maxgap=max(maxgap,logf-logg)
    assert maxgap<1e-7,(m,maxgap)
    gamma_rows.append({'m':m,'acceptance':acc,'largest_log_envelope_violation':maxgap})
for mu in [1,1.01,1.999,2,3.7,10,100.5,1000.1,10000.9,1000000.3]:
    m=math.floor(mu);d=math.ceil(math.sqrt(m));a=m-d;b=m+d
    rl=a/mu;rr=mu/(b+1)
    Z=2*d+1+(rl/(1-rl) if rl else 0)+rr/(1-rr)
    mass=math.exp(mu+math.lgamma(m+1)-m*math.log(mu))
    assert mass/Z>=1/64
    maxgap=-math.inf
    lo=max(0,m-int(10*math.sqrt(m))-10);hi=m+int(10*math.sqrt(m))+10
    for n in range(lo,hi+1):
        logf=(n-m)*math.log(mu)+math.lgamma(m+1)-math.lgamma(n+1)
        logg=(a-n)*math.log(rl) if n<a else ((n-b)*math.log(rr) if n>b else 0)
        maxgap=max(maxgap,logf-logg)
    assert maxgap<1e-7,(mu,maxgap)
    poisson_rows.append({'mu':mu,'acceptance':mass/Z,'largest_log_envelope_violation':maxgap})
print(json.dumps({'scope':'floating envelope checks; not certified sampler','gamma':gamma_rows,'poisson':poisson_rows},indent=2))
