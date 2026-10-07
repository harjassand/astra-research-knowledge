"""Bounded 2-by-2 floating diagnostics; no external dependencies."""
import json,math
from pathlib import Path

def eig(a):
    mid=(a[0]+a[2])/2
    radius=math.hypot((a[0]-a[2])/2,a[1])
    return [max(0.,mid-radius),mid+radius]
def trfun(a,fun): return sum(fun(v) for v in eig(a))
def mean(a,b): return tuple((x+y)/2 for x,y in zip(a,b))
def fmatrix(a,t,l):
    vals=eig(a);v,w=vals
    fv=t*v/(1+t*v/l);fw=t*w/(1+t*w/l)
    if abs(w-v)<1e-14: return (fv,0.,fv)
    slope=(fw-fv)/(w-v);intercept=fv-slope*v
    return (slope*a[0]+intercept,slope*a[1],slope*a[2]+intercept)
def logcap(x,t,l): return math.log1p((1+1/l)*t*x)-math.log1p(t*x/l)
def xlogx(x): return x*math.log(x) if x>0 else 0.
def simpson(fun,lo=-24,hi=24,n=4000):
    step=(hi-lo)/n
    ans=fun(lo)+fun(hi)
    for i in range(1,n): ans+=(4 if i%2 else 2)*fun(lo+i*step)
    return ans*step/3

examples=[((0.,0.,2.),(2.,0.,0.)),
          ((1.,0.,4.),(2.5,1.5,2.5)),
          ((0.,0.,3.),(2.,1.,2.)),
          ((.2,.1,2.),(1.5,-.4,.8))]
out=[]
for a,b in examples:
    m=mean(a,b)
    entropy=(trfun(a,xlogx)+trfun(b,xlogx))/2-trfun(m,xlogx)
    row={'A1':a,'A2':b,'entropy':entropy,'caps':[]}
    assert entropy>=-1e-14
    for cap in [1.,4.,32.,256.]:
        def gap(t):
            return trfun(m,lambda x:logcap(x,t,cap))-(
                trfun(a,lambda x:logcap(x,t,cap))+
                trfun(b,lambda x:logcap(x,t,cap)))/2
        integral=simpson(lambda u:gap(math.exp(u))*math.exp(-u))
        max_jensen_violation=0.
        for t in [1e-4,.01,.1,1.,10.,1e3,1e4]:
            ca=fmatrix(a,t,cap);cb=fmatrix(b,t,cap);ec=mean(ca,cb)
            actual=trfun(ec,math.log1p)-(
                trfun(a,lambda x:logcap(x,t,cap))+
                trfun(b,lambda x:logcap(x,t,cap)))/2
            max_jensen_violation=max(max_jensen_violation,actual-gap(t))
        assert abs(integral-entropy)<5e-7
        assert max_jensen_violation<2e-10
        row['caps'].append({'cap':cap,'integral_gap':integral,
                            'absolute_identity_error':abs(integral-entropy),
                            'max_jensen_violation':max_jensen_violation})
    out.append(row)
j={'status':'DIAGNOSTIC_ONLY','examples':out,
   'scope':'Finite 2x2 floating Jensen and scale-integral checks; no MI quadrature or KLS validation'}
Path(__file__).with_name('matrix_entropy_check.json').write_text(json.dumps(j,indent=2))
print(json.dumps({'status':j['status'],'examples':len(out),
                  'max_identity_error':max(x['absolute_identity_error'] for r in out for x in r['caps'])}))
