"""Exact secant/knapsack certificate for a normalized positive quadratic.

This is a finite-input operator, not continuation-interval acquisition or
a new generic fractional-programming method. All arithmetic is rational.
"""
from fractions import Fraction as F

def validate(lo,hi,r):
    if not lo or len(lo)!=len(hi) or len(lo)!=len(r):raise ValueError('dimensions')
    if any(a<0 or a>b or c<0 for a,b,c in zip(lo,hi,r)):raise ValueError('positive box required')
    if not any(hi):raise ValueError('all continuations zero')

def value(w,r):
    S=sum(w,F(0))
    if not S:raise ValueError('zero denominator')
    return sum((c*z*z for c,z in zip(r,w)),F(0))/(S*S)

def dual_bound(lo,hi,r,nu):
    """O(k) certificate from any rational nu with negative eta."""
    eta=sum((max((c*(a+b)-nu)*a,(c*(a+b)-nu)*b)-c*a*b for a,b,c in zip(lo,hi,r)),F(0))
    if nu<=0 or eta>=0:raise ValueError('nonpositive quadratic certificate')
    return -nu*nu/(4*eta),eta

def compile_box(lo,hi,r):
    validate(lo,hi,r);k=len(lo);baseS=sum(lo,F(0))
    if not baseS:
        j=max((i for i in range(k) if hi[i]),key=lambda i:r[i])
        return {'kind':'zero_lower','upper':r[j],'lower':r[j],'lower_upper_indices':[j],
                'factor':F(1),'nu':None,'eta':None,'size':k}
    baseN=sum((c*a*a for a,c in zip(lo,r)),F(0))
    order=sorted((i for i in range(k) if hi[i]>lo[i]),key=lambda i:(-r[i]*(lo[i]+hi[i]),i))
    S,N=baseS,baseN;L=U=N/(S*S);best_count=0;bestS=S;active=None
    for j,i in enumerate(order):
        width=hi[i]-lo[i];density=r[i]*(lo[i]+hi[i])
        if density:
            critical=2*S-2*N/density
            if S<critical<S+width:
                candidate=(N+density*(critical-S))/(critical*critical)
                if candidate>U:
                    U=candidate;bestS=critical
                    theta=(critical-S)/width;active=(i,theta,width,critical)
        S+=width;N+=density*width;endpoint=N/(S*S)
        if endpoint>L:L=endpoint;best_count=j+1
        if endpoint>U:U=endpoint;bestS=S;active=None
    lower_kind=('prefix',best_count)
    # Equally cheap ordinary improvements: singleton and complement corners.
    for i in range(k):
        width=hi[i]-lo[i];profit=r[i]*(hi[i]*hi[i]-lo[i]*lo[i])
        singleton=(baseN+profit)/(baseS+width)**2
        if singleton>L:L=singleton;lower_kind=('single',i)
        if S-width:
            complement=(N-profit)/(S-width)**2
            if complement>L:L=complement;lower_kind=('complement',i)
    if lower_kind[0]=='prefix':lower_indices=order[:lower_kind[1]]
    elif lower_kind[0]=='single':lower_indices=[lower_kind[1]]
    else:lower_indices=[i for i in range(k) if i!=lower_kind[1]]
    if not U:
        return {'kind':'zero_numerator','upper':F(0),'lower':F(0),'lower_upper_indices':lower_indices,
                'factor':F(1),'nu':None,'eta':None,'size':k}
    nu=2*U*bestS;check,eta=dual_bound(lo,hi,r,nu)
    assert check==U and L<=U
    if U==L:factor=F(1);active=None
    else:
        assert active is not None
        _,theta,width,critical=active
        factor=1+theta*(1-theta)*(width/critical)**2
    assert U<=L*factor
    return {'kind':'secant_dual','upper':U,'lower':L,'lower_upper_indices':lower_indices,
            'factor':factor,'nu':nu,'eta':eta,'active':active,'size':k}

def verify_certificate(lo,hi,r,cert):
    """No sort/optimizer: one scalar upper certificate and one corner."""
    validate(lo,hi,r)
    chosen=cert['lower_upper_indices']
    if len(set(chosen))!=len(chosen) or any(i<0 or i>=len(lo) for i in chosen):raise ValueError('corner')
    w=list(lo)
    for i in chosen:w[i]=hi[i]
    L=value(w,r)
    assert L==cert['lower']
    if cert['kind']=='zero_lower':
        assert not sum(lo) and cert['upper']==max(c for b,c in zip(hi,r) if b)
    elif cert['kind']=='zero_numerator':
        assert all(c*b*b==0 for b,c in zip(hi,r)) and cert['upper']==0
    else:
        U,eta=dual_bound(lo,hi,r,cert['nu'])
        assert eta==cert['eta'] and U<=cert['upper']
    assert cert['upper']<=L*cert['factor']
    return True

def from_branch_data(P,q,B,ell,up):
    if not all(len(x)==len(P) for x in [q,B,ell,up]):raise ValueError('branch dimensions')
    if sum(P)!=1 or sum(q)!=1 or any(x<0 for x in P+q):raise ValueError('probabilities')
    if any(not (0<=a<=b<=1) or z<1 for a,b,z in zip(ell,up,B)):raise ValueError('branch bounds')
    keep=[i for i in range(len(P)) if P[i]*up[i]>0]
    if any(q[i]<=0 for i in keep):raise ValueError('success support')
    return ([P[i]*ell[i] for i in keep],[P[i]*up[i] for i in keep],[B[i]/q[i] for i in keep])

def exhaustive_max(lo,hi,r):
    """Small-instance exact comparator; Gray-code arithmetic updates."""
    k=len(lo);S=sum(lo,F(0));N=sum((c*a*a for a,c in zip(lo,r)),F(0))
    widths=[b-a for a,b in zip(lo,hi)];profits=[c*(b*b-a*a) for a,b,c in zip(lo,hi,r)]
    best=N/(S*S) if S else F(0);previous=0
    for j in range(1,1<<k):
        code=j^(j>>1);change=code^previous;i=change.bit_length()-1
        sign=1 if code&change else -1
        S+=sign*widths[i];N+=sign*profits[i]
        if S:best=max(best,N/(S*S))
        previous=code
    return best
