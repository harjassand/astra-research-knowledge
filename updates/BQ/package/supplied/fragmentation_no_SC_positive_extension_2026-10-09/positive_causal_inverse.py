"""Causal inversion via nonnegative uniformization coefficients, without W.

All path-table updates are sums/products of nonnegative numbers. The one
subtraction Y-G is the genuine inverse problem, followed immediately by clipping.
Operation count O(J*m^2), storage O(J*m), with a displayed analytic tail bound.
"""
import math
import numpy as np


def choose_order(a,radius,tolerance):
    """Chernoff bound: exp(a(R-1))*Pr(Pois(aR)>J)."""
    if a<=0 or radius<1 or not 0<tolerance<1:raise ValueError('invalid uniformization parameters')
    mu=a*radius
    J=max(1,int(math.ceil(mu)))
    while True:
        j=J+1
        logbound=-a+j*(1+math.log(mu/j))
        if logbound<=math.log(tolerance):return J,math.exp(logbound)
        J+=1


def positive_inverse(y,a,cap,*,logq=None,rates=None,tolerance=1e-12):
    """Recover a bounded kernel prefix without a renewal intertwiner.

    rates is b_n/b_0, with rates[0]=1 and all rates in [0,1]. Alternatively
    logq=-gamma*h supplies the power-law profile, including logq=0.
    alpha*T is a. cap is M*h per positive jump bin. Known initial is delta_0.
    The output is pre mass repair. The returned table is optional evidence of
    the nonnegative forward coefficients; it can be omitted by consumers.
    """
    y=np.asarray(y,dtype=float);n=len(y)
    if cap<=0 or len(y)<2:raise ValueError('positive cap and at least one bin required')
    if rates is None:
        if logq is None or logq>0:raise ValueError('nonpositive logq required')
        rates=np.exp(logq*np.arange(n))
        z=-np.expm1(logq*np.arange(n))
    else:
        rates=np.asarray(rates,dtype=float)
        if len(rates)!=n or rates[0]!=1 or np.any(rates<0) or np.any(rates>1):
            raise ValueError('rates must have length n, start at 1, and lie in [0,1]')
        z=1-rates
    radius=max(1.,cap*(n-1))
    J,tail=choose_order(a,radius,tolerance)
    # Store POISSON-WEIGHTED coefficients. This avoids forming a potentially
    # huge P^r and subsequently multiplying it by an extremely small weight.
    v=np.zeros((J+1,n));v[0,0]=np.exp(-a)
    k=np.zeros(n);p=np.zeros(n);p[0]=np.exp(-a)
    for i in range(1,n):
        b=v[:J,1:i]@(k[i-1:0:-1]*rates[1:i])
        rem=np.empty(J)
        last=0.;direct_last=a*np.exp(-a)
        direct=np.empty(J)
        for j in range(J):
            last=(a/(j+1))*(z[i]*last+b[j])
            rem[j]=last
            if j:direct_last*=a*z[i]/(j+1)
            direct[j]=direct_last
        G=np.sum(rem)
        A=a*np.exp(-a) if z[i]==0 else np.exp(-a)*np.expm1(a*z[i])/z[i]
        k[i]=np.clip((y[i]-G)/A,0,cap)
        v[1:,i]=rem+k[i]*direct
        p[i]=A*k[i]+G
    return k,{'order':J,'tail_l1_bound':tail,'radius_bound':radius,
              'predicted_endpoint_truncated':p,'table_max':float(np.max(v)),
              'minimum_table_entry':float(np.min(v))}
