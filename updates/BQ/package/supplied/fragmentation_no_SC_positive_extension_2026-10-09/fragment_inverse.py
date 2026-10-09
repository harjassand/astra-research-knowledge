"""Finite-time, geometric-size fragmentation inversion.

Internal research prototype. The inverse is exact for the stated lattice model;
continuum discretization, measurement noise, and rate error are separate issues.
"""
import numpy as np
from scipy.linalg import expm, expm_frechet
from scipy.optimize import minimize
from scipy.sparse.linalg import expm_multiply
from scipy.special import gammaln
from scipy.stats import poisson


def generator(k, q, alpha=1.0):
    """Mass-weighted generator: jump probabilities k[1:], k[0] must be 0."""
    n = len(k)
    rates = alpha * q ** np.arange(n)
    A = -np.diag(rates)
    for j in range(1, n):
        A[np.arange(j, n), np.arange(n-j)] = k[j]*rates[:n-j]
    return A


def endpoint(k, q, t=1., alpha=1.):
    e0 = np.zeros(len(k)); e0[0] = 1
    return expm_multiply(t * generator(k, q, alpha), e0)


def invert(f, q, t=1., alpha=1., dtype=np.float64):
    """Two causal algebraic recurrences; no time-discretization error."""
    f = np.asarray(f, dtype=dtype)
    w = np.zeros_like(f); w[0] = 1
    k = np.zeros_like(f)
    a = dtype(alpha*t)
    for n in range(1, len(f)):
        one_minus_qn = -np.expm1(dtype(n)*np.log(dtype(q)))
        # e^(-a*q^n) - e^(-a), written without cancellation at q ~= 1.
        den = np.exp(-a)*np.expm1(a*one_minus_qn)
        w[n] = np.dot(f[1:n+1], w[n-1::-1])/den
        k[n] = one_minus_qn*w[n] - np.dot(k[1:n], w[n-1:0:-1])
    return k, w


def invert_mp(f,q,t=1.,alpha=1.,dps=70):
    """High-precision fallback when the intertwiner has large coefficients.

    This corrects representation cancellation; it does not cure statistical
    ill-conditioning or inaccurate input data.
    """
    import mpmath as mp
    with mp.workdps(dps):
        f=[mp.mpf(float(x)) for x in f]
        q=mp.mpf(float(q));a=mp.mpf(float(alpha*t))
        w=[mp.mpf(0)]*len(f);w[0]=mp.mpf(1)
        k=[mp.mpf(0)]*len(f)
        for n in range(1,len(f)):
            z=1-q**n
            den=mp.exp(-a)*mp.expm1(a*z)
            w[n]=mp.fsum(f[i]*w[n-i] for i in range(1,n+1))/den
            k[n]=z*w[n]-mp.fsum(k[i]*w[n-i] for i in range(1,n))
        return np.array([float(x) for x in k]),float(max(abs(x) for x in w))


def forward_recurrence(k, q, t=1., alpha=1., dtype=np.float64):
    k = np.asarray(k, dtype=dtype)
    w = np.zeros_like(k); w[0] = 1
    f = np.zeros_like(k); f[0] = np.exp(-dtype(t*alpha))
    for n in range(1,len(k)):
        one_minus_qn = -np.expm1(dtype(n)*np.log(dtype(q)))
        w[n] = (k[n] + np.dot(k[1:n], w[n-1:0:-1]))/one_minus_qn
        den = f[0]*np.expm1(dtype(t*alpha)*one_minus_qn)
        f[n] = den*w[n] - np.dot(f[1:n], w[n-1:0:-1])
    return f, w


def uniformized_forward(k,q,t=1.,alpha=1.,gradient=None):
    """Classical uniformization, independent of the proposed inverse.

    If gradient is supplied it is d(objective)/d(endpoint), and the returned
    vector is the exact series-truncated gradient with respect to k.
    """
    n=len(k);D=q**np.arange(n);a=alpha*t
    radius=max(1.,float(np.sum(abs(k))))
    m=int(poisson.isf(1e-15,a*radius))+4
    w=np.exp(-a+np.arange(m+1)*np.log(a)-gammaln(np.arange(m+1)+1))
    v=np.zeros((m+1,n));v[0,0]=1
    for i in range(m):
        v[i+1]=(1-D)*v[i]+np.convolve(k,D*v[i])[:n]
    y=w@v
    if gradient is None:return y
    adj=w[-1]*gradient
    g=np.zeros(n)
    for i in range(m-1,-1,-1):
        g+=np.correlate(adj,D*v[i],mode='full')[n-1:]
        adj=w[i]*gradient+(1-D)*adj+D*np.correlate(adj,k,mode='full')[n-1:]
    return y,g


def fit_uniformized(f,q,t=1.,alpha=1.,x0=None,maxiter=500):
    """Nonnegative finite-time Poisson MLE, matrix-free classical baseline."""
    n=len(f)
    if x0 is None:x0=np.r_[0.,np.repeat(.9/(n-1),n-1)]
    calls=0
    def fun(x):
        nonlocal calls
        calls+=1
        k=np.r_[0.,x]
        y=uniformized_forward(k,q,t,alpha)
        yp=np.maximum(y,1e-100)
        d=1-f/yp;d[0]=0
        _,g=uniformized_forward(k,q,t,alpha,gradient=d)
        loss=np.sum(yp[1:]-f[1:]*np.log(yp[1:]))
        return loss,g[1:]
    res=minimize(fun,np.asarray(x0)[1:],jac=True,method='L-BFGS-B',
                  bounds=[(0,None)]*(n-1),
                  options={'maxiter':maxiter,'ftol':1e-13,'gtol':1e-10,'maxls':30})
    return np.r_[0.,res.x],res,calls


def fit_endpoint(f, q, t=1., alpha=1., x0=None, sigma=None,
                 normalization=False, maxiter=500, likelihood='squares'):
    """Strong model-matched nonlinear baseline, exact Frechet adjoint gradient.

    Known intact atom is excluded from objective, since independent of k.
    Optional equality sum(k)=1 is appropriate only if observed kernel support
    has no unobserved tail; it is not used for observation-truncation tests.
    """
    n = len(f)
    e0 = np.zeros(n); e0[0] = 1
    rates = alpha * q**np.arange(n)
    if x0 is None:
        x0 = np.repeat(1/(n-1),n-1)
    else:
        x0 = np.asarray(x0)[1:]
    if sigma is None:
        sigma = np.ones(n)
    scale = np.asarray(sigma)
    calls = 0
    def fun(x):
        nonlocal calls
        calls += 1
        k = np.r_[0.,x]
        A = t*generator(k,q,alpha)
        y = expm(A)[:,0]
        if likelihood=='poisson':
            yp=np.maximum(y,1e-100)
            d=1-f/yp
            loss=np.sum(yp[1:]-f[1:]*np.log(yp[1:]))
        else:
            d = (y-f)/(scale*scale)
            loss = .5*np.sum(((y[1:]-f[1:])/scale[1:])**2)
        d[0]=0
        G = expm_frechet(A.T,np.outer(d,e0),compute_expm=False)
        grad = np.array([t*np.dot(rates[:n-j],G[np.arange(j,n),np.arange(n-j)])
                         for j in range(1,n)])
        return loss,grad
    constraints=[]
    method='L-BFGS-B'
    options={'maxiter':maxiter,'ftol':1e-13,'gtol':1e-10,'maxls':30}
    if normalization:
        method='SLSQP'
        constraints=[{'type':'eq','fun':lambda x:x.sum()-1,
                      'jac':lambda x:np.ones_like(x)}]
        options={'maxiter':maxiter,'ftol':1e-12}
    result=minimize(fun,x0,jac=True,method=method,bounds=[(0,None)]*(n-1),
                    constraints=constraints,options=options)
    return np.r_[0.,result.x],result,calls


if __name__=='__main__':
    rng=np.random.default_rng(74)
    for q in [.5,.9,.99]:
        k=np.r_[0,rng.dirichlet(np.ones(40))]
        f=endpoint(k,q,2.3)
        kk,w=invert(f,q,2.3)
        ff,_=forward_recurrence(k,q,2.3)
        print(q,'inverse',np.max(abs(kk-k)),'forward',np.max(abs(ff-f)),
              'max W',max(w))
