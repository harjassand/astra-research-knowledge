"""Independent O(n^2) Bernoulli boundary transfer; no upstream imports."""
import numpy as np
from scipy.integrate import quad

def pmf(strengths, F, probabilities):
    s=np.asarray(strengths,dtype=float); p=np.asarray(probabilities,dtype=float)
    order=np.argsort(-s,kind='stable');s=s[order];p=p[order];n=len(s)
    if n==0:return np.array([1.])
    # j_m is the size of the strict eligibility prefix A_m.
    js=np.zeros(n+1,dtype=int)
    for m in range(1,n+1):js[m]=np.count_nonzero(s>F/m)
    buckets=[[] for _ in range(n+1)]
    for m,j in enumerate(js):
        if j>=m:buckets[j].append(m)
    prefix=np.zeros(n+1);prefix[0]=1.;a=np.zeros(n+1)
    for m in buckets[0]:a[m]=prefix[m]
    for j in range(1,n+1):
        old=prefix.copy();prefix*=1-p[j-1];prefix[1:]+=p[j-1]*old[:-1]
        for m in buckets[j]:a[m]=prefix[m]
    h=np.ones(n+1);out=np.zeros(n+1)
    for m in buckets[n]:out[m]=a[m]*h[m]
    c=np.arange(n+1);stress=np.zeros(n+1);stress[1:]=F/c[1:]
    for j in range(n-1,-1,-1):
        # A count of zero is always below the failure boundary.
        ok=s[j]<=stress;ok[0]=True
        gated=h*ok
        h=(1-p[j])*gated
        h[:-1]+=p[j]*gated[1:]
        for m in buckets[j]:out[m]=a[m]*h[m]
    return out

def exhaustive(strengths,F,probabilities):
    s=np.asarray(strengths);p=np.asarray(probabilities);n=len(s);out=np.zeros(n+1)
    for mask in range(1<<n):
        x=((mask>>np.arange(n))&1).astype(bool)
        w=np.prod(np.where(x,p,1-p));k=0
        for c in range(1,n+1):
            if np.count_nonzero(x&(s>F/c))>=c:k=c
        out[k]+=w
    return out

def mean_quad(strengths,F,T,epsabs=1e-7):
    s=np.asarray(strengths);n=len(s)
    if n==0:return {'mean':0.,'quadrature_error_estimate':0.,'tail_upper_bound':0.}
    lam=np.exp(-s/T);lmin=lam.min();r=lam/lmin
    psi=np.zeros(n+1);psi[1:]=np.exp(-F/(T*np.arange(1,n+1)))
    # Physical tail <= psi(n) sum_i exp(-lambda_i U)/lambda_i.
    L=max(0.,np.log(max(1.,psi[n]*n/(lmin*epsabs))))
    def g(x):return pmf(s,F,np.exp(-r*x))@psi
    val,err=quad(g,0,L,epsabs=epsabs*lmin,epsrel=1e-10,limit=300)
    tail=psi[n]*np.sum(np.exp(-r*L)/lam)
    return {'mean':val/lmin,'quadrature_error_estimate':err/lmin,'tail_upper_bound':tail,'scaled_upper_limit':L}

def mean_monotone_bracket(strengths,F,T,absolute_gap=1.,max_evals=1000000):
    """Mathematical enclosure via monotone rectangles; floating arithmetic uncertified."""
    import heapq
    s=np.asarray(strengths);n=len(s);lam=np.exp(-s/T);lmin=lam.min();r=lam/lmin
    psi=np.zeros(n+1);psi[1:]=np.exp(-F/(T*np.arange(1,n+1)))
    L=max(1.,np.log(max(1.,4*psi[n]*n/(lmin*absolute_gap))))
    tail=psi[n]*np.sum(np.exp(-r*L)/lam)
    def g(x):return float(pmf(s,F,np.exp(-r*x))@psi/lmin)
    a,b=g(0.),g(L);lo=L*b;hi=L*a;heap=[(-L*(a-b),0.,L,a,b)];evals=2
    while hi-lo+tail>absolute_gap and evals<max_evals:
        _,left,right,gl,gr=heapq.heappop(heap);mid=(left+right)/2;gm=g(mid);evals+=1
        width=(right-left)/2;lo+=width*(gm-gr);hi-=width*(gl-gm)
        heapq.heappush(heap,(-width*(gl-gm),left,mid,gl,gm))
        heapq.heappush(heap,(-width*(gm-gr),mid,right,gm,gr))
    return {'lower':lo,'upper':hi+tail,'gap':hi+tail-lo,'evaluations':evals,'tail_upper_bound':tail,'roundoff_certified':False}

def mean_geometric_bracket(strengths,F,T,relative_gap=.01):
    """Geometric monotone quadrature with a posteriori relative gap.
    Bounds hold in exact arithmetic; ordinary floating-point implementation.
    """
    s=np.asarray(strengths);n=len(s);lam=np.exp(-s/T);lmin=lam.min();r=lam/lmin
    psi=np.zeros(n+1);psi[1:]=np.exp(-F/(T*np.arange(1,n+1)))
    def g(x):return float(pmf(s,F,np.exp(-r*x))@psi/lmin)
    g0=g(0.)
    if g0==0.:return {'lower':0.,'upper':0.,'evaluations':1,'roundoff_certified':False}
    # Seek a useful strictly positive lower bound on the integral.
    x=1.;gx=g(x);evals=2
    while gx<g0/2:
        x/=2;gx=g(x);evals+=1
    H=x*gx;budget=relative_gap*H/8
    x0=budget/g0
    L=max(x0*2,np.log(max(1.,psi[n]*n/(lmin*budget))))
    ratio=1+relative_gap/2
    count=int(np.ceil(np.log(L/x0)/np.log(ratio)))
    xs=np.geomspace(x0,L,count+1)
    vals=np.array([g(t) for t in xs]);evals+=len(xs)
    widths=np.diff(xs);lo=np.dot(widths,vals[1:]);hi=np.dot(widths,vals[:-1])
    # Initial rectangle contributes lower x0*g(x0), upper x0*g(0).
    lo+=x0*vals[0];hi+=x0*g0
    tail=psi[n]*np.sum(np.exp(-r*L)/lam);hi+=tail
    return {'lower':float(lo),'upper':float(hi),'relative_gap':float((hi-lo)/lo),
            'evaluations':evals,'tail_upper_bound':float(tail),'initial_upper_bound':float(x0*g0),
            'roundoff_certified':False}
