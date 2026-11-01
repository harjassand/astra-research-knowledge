"""Gaussian reference for an interacting Glauber ring, and nonintegrable kinetics.

Original implementation in this investigation.  Classical probabilities, not a
quantum device.  Floating point computations are checks, not interval proofs.
Rates are heat-bath pair flips of domain walls.  Even wall parity is explicit.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import json, time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, expm
from scipy.integrate import quad
from scipy.special import expit
from numpy.polynomial.legendre import leggauss


def model(J, nu=None):
    J = np.asarray(J, dtype=float)  # dimensionless beta*J
    n = len(J)
    if n < 4 or n % 2:
        raise ValueError('Use even n >= 4; even wall-parity sector.')
    nu = np.ones(n) if nu is None else np.asarray(nu, dtype=float)
    if nu.shape != J.shape or not np.all(np.isfinite(J)) or not np.all(np.isfinite(nu)) or np.any(nu <= 0):
        raise ValueError('Finite couplings and matching strictly positive attempt rates required.')
    c = nu * expit(-2*(J + np.roll(J, -1)))
    a = nu * expit(2*(J + np.roll(J, -1)))
    d = nu * expit(-2*(np.roll(J, -1) - J))
    e = nu * expit(2*(np.roll(J, -1) - J))
    if min(c.min(),a.min(),d.min(),e.min()) <= 0:
        raise ValueError('A physical rate underflows in double precision; use arbitrary precision.')
    D = np.zeros((n,n)); A = np.zeros((n,n))
    for i in range(n):
        j = (i+1) % n
        D[i,i] += c[i]-d[i]
        D[j,j] += c[i]-e[i]
        sg = 1 if j > i else -1  # antiperiodic JW boundary in even sector
        hop = sg*np.sqrt(d[i]*e[i])
        pair = sg*np.sqrt(c[i]*a[i])
        D[j,i] += hop; D[i,j] += hop
        A[i,j] += pair; A[j,i] -= pair
    # H=-Q_s has BdG matrix [h,Delta;-Delta,-h^T].
    h, Delta = -D, -A
    bdg = np.block([[h, Delta],[-Delta,-h.T]])
    vals, vecs = eigh(bdg)
    eps = vals[n:]
    U, V = vecs[:n,n:], vecs[n:,n:]
    Z = -np.linalg.solve(U, V)
    anti_error = np.max(np.abs(Z+Z.T))
    Z = (Z-Z.T)/2
    lp = -0.5*np.linalg.slogdet(np.eye(n)+Z.T@Z)[1]
    # Domain-wall equilibrium is a product measure conditioned on even parity.
    logpi = np.log(2)-np.logaddexp(0,-2*J).sum()-np.log1p(np.prod(np.tanh(J)))
    gap=float(eps[0]+eps[1])
    # A refusal diagnostic, not a certified eigenvalue enclosure.
    floor=128*np.finfo(float).eps*max(float(np.linalg.norm(bdg,ord=np.inf)),1e-300)
    return dict(n=n,J=J,nu=nu,c=c,a=a,d=d,e=e,D=D,A=A,eps=eps,
                U=U,V=V,Z=Z,logpi=logpi,gaussian_logpi=lp,
                gap=gap,gap_resolved_in_double=bool(gap>floor),
                numerical_gap_floor=floor,
                antisymmetry_error=float(anti_error),
                normalization_error=float(abs(lp-logpi)))


def log_return(m,t):
    # Ground-state representation prevents exp(+epsilon*t) instability.
    half = np.exp(-m['eps']*t/2)
    W = half[:,None]*m['Z']*half[None,:]
    return m['logpi'] + 0.5*np.linalg.slogdet(np.eye(m['n'])+W.T@W)[1]


def return_excess(m,t):
    half = np.exp(-m['eps']*t/2)
    W = half[:,None]*m['Z']*half[None,:]
    # eigvalsh produces nonnegative terms; log1p retains late-time excess.
    d = np.maximum(eigh(W.T@W, eigvals_only=True),0)
    lratio = 0.5*np.log1p(d).sum()
    if lratio > 1:
        return np.exp(m['logpi']+lratio)*(-np.expm1(-lratio))
    return np.exp(m['logpi'])*np.expm1(lratio)


def mean_reference(m,rtol=1e-9):
    if not m['gap_resolved_in_double']:
        raise ValueError('Gap unresolved in double precision; use higher precision or a proved spectral bound.')
    pi = np.exp(m['logpi'])
    if not 0 < pi < 1:
        raise ValueError('Target probability or its complement is unresolved in double precision; use arbitrary precision.')
    upper_spectrum = 2*m['nu'].sum()  # conservative maximum exit-rate bound
    g = m['gap']
    T = np.log(upper_spectrum/(rtol*g))/g
    val,err=quad(lambda t:return_excess(m,t),0,T,
                 epsabs=rtol/(10*upper_spectrum),epsrel=rtol/10,limit=250)
    tail=(1-pi)*np.exp(-g*T)/g
    logmean=np.log(val)-m['logpi']-np.log1p(-pi)
    return dict(W=val,mean=float(np.exp(logmean)),log_mean=float(logmean),
                cutoff=T,analytic_tail_bound=tail,quad_error_estimate=err)


def dense_generator(m, facilitation=0.0):
    n=m['n']
    states=[s for s in range(1<<n) if s.bit_count()%2==0]
    index={s:i for i,s in enumerate(states)}
    Q=np.zeros((len(states),len(states)))
    for col,s in enumerate(states):
        for i in range(n):
            j=(i+1)%n; k=(i+2)%n
            x,y=(s>>i)&1,(s>>j)&1
            rate=(m['c'][i] if (x,y)==(0,0) else
                  m['a'][i] if (x,y)==(1,1) else
                  m['d'][i] if (x,y)==(1,0) else m['e'][i])
            # Spectator multiplier is equal on both ends of each transition.
            rate*=1+facilitation*((s>>k)&1)
            row=index[s^(1<<i)^(1<<j)]
            Q[row,col]+=rate; Q[col,col]-=rate
    energies=np.array([sum(2*m['J'][i]*((s>>i)&1) for i in range(n)) for s in states])
    p=np.exp(-energies); p/=p.sum()
    K=-Q*np.sqrt(p)[None,:]/np.sqrt(p)[:,None]
    return states,Q,K,p


def gaussian_contractions(m,s,t):
    """<vac|e^(Q_s s) [c,c^dag]_a[c,c^dag]_b e^(Q_s t)|vac>/R(s+t)."""
    es=np.exp(-m['eps']*s); et=np.exp(-m['eps']*t)
    G=es[:,None]*m['Z']*es[None,:]
    F=et[:,None]*m['Z']*et[None,:]
    I=np.eye(m['n'])
    M=np.linalg.solve(I-F@G,I)
    C=np.block([[-M@F,M],[I-M.T,G@M]])
    UV=np.block([[m['U'],m['V']],[m['V'],m['U']]])
    return UV@C@UV.T


def wick4(C,a,b,c,d):
    return C[a,b]*C[c,d]-C[a,c]*C[b,d]+C[a,d]*C[b,c]


def local_insertions(m,s,t):
    """<b|P_s [sum_i (-q_i) n_(i+2)] P_t|b>, no enumeration.

    q_i is the symmetrized local heat-bath generator.  The added spectator
    occupation turns this into a genuinely quartic/non-Gaussian generator.
    """
    n=m['n']; C=gaussian_contractions(m,s,t)
    total=0.0
    for i in range(n):
        j=(i+1)%n; k=(i+2)%n
        nk=C[n+k,k]
        qn=-m['c'][i]*nk
        qn+=(m['c'][i]-m['d'][i])*wick4(C,n+i,i,n+k,k)
        qn+=(m['c'][i]-m['e'][i])*wick4(C,n+j,j,n+k,k)
        sg=1 if j>i else -1
        pair=sg*np.sqrt(m['a'][i]*m['c'][i])
        hop=sg*np.sqrt(m['d'][i]*m['e'][i])
        qn+=pair*(wick4(C,n+i,n+j,n+k,k)-wick4(C,i,j,n+k,k))
        qn+=hop*(wick4(C,n+j,i,n+k,k)+wick4(C,n+i,j,n+k,k))
        total-=qn
    return np.exp(log_return(m,s+t))*total


def dense_checks():
    rng=np.random.default_rng(20261101)
    records=[]
    for n in [4,6,8]:
        for run in range(2):
            m=model(rng.uniform(.2,1.2,n),rng.uniform(.6,1.4,n))
            states,Q,K,p=dense_generator(m)
            ev,O=eigh(K); g=np.sqrt(p)
            G=(O[:,1:]/ev[1:])@O[:,1:].T
            r=mean_reference(m)
            ret_err=max(abs(np.exp(log_return(m,t))-expm(-K*t)[0,0]) for t in [.001,.1,1,10])
            mean=G[0,0]/(p[0]*(1-p[0]))
            # E is quartic; same Gibbs law is directly checked.
            _,Q1,K1,p1=dense_generator(m,1.0)
            E=K1-K
            first=(G@E@G)[0,0]
            contraction_err=0
            for s,t in [(.01,.2),(.7,.3),(2,4)]:
                exact=(expm(-K*s)@E@expm(-K*t))[0,0]
                contraction_err=max(contraction_err,abs(local_insertions(m,s,t)-exact))
            eps=.7; _,Qe,Ke,pe=dense_generator(m,eps)
            ewe,ove=eigh(Ke)
            Ge=(ove[:,1:]/ewe[1:])@ove[:,1:].T
            We=Ge[0,0]; W0=G[0,0]
            # Recenter contrast for all-order series.
            c=1+eps/2; rho=eps/(2+eps)
            Gr=G/c; Er=Ke-c*K
            terms=[]; v=Gr[:,0].copy(); accum=Gr[0,0]
            for order in range(1,5):
                term=(-1)**order*(Gr@np.linalg.matrix_power(Er@Gr,order))[0,0]
                accum+=term
                bound=rho**(order+1)
                terms.append(dict(order=order,estimate=accum,relative_error=abs(accum/We-1),bound=bound))
            records.append(dict(n=n,seed_run=run,logpi=m['logpi'],normalization_error=m['normalization_error'],
                return_absolute_error=ret_err,mean_relative_error=abs(r['mean']/mean-1),
                local_insertion_absolute_error=contraction_err,
                stationary_residual=float(np.max(np.abs(Qe@pe))),
                first_order_coefficient=first,first_order_fraction=first/W0,
                recentered_series=terms))
    return records


def first_correction(m,nu_nodes=80,nv_nodes=16,tol=1e-8):
    """Gaussian Wick quadrature for the first nonintegrable correction.

    Uses u=s+t, v=s/(s+t), then a logarithmic grid in u.  All factors
    are from 2n-mode linear algebra; no full configurations are enumerated.
    Gauss quadrature errors are assessed by refinement, not certified here.
    """
    n=m['n']; g=m['gap']; Lam=2*m['nu'].sum()
    T=np.log(Lam**2/(tol*g**2))/g
    # Increase until the conservative full u>T double-integral tail is small.
    while Lam*np.exp(-g*T)*(T/g+1/g**2)>tol/Lam:
        T+=1/g
    t0=1/Lam; xmax=np.log1p(T/t0)
    xu,wu=leggauss(nu_nodes); xv,wv=leggauss(nv_nodes)
    x=(xu+1)*xmax/2; v=(xv+1)/2
    result=0.
    for xx,ww in zip(x,wu*xmax/2):
        u=t0*np.expm1(xx); jac=t0*np.exp(xx)
        inner=sum(w*local_insertions(m,u*z,u*(1-z)) for z,w in zip(v,wv/2))
        result+=ww*jac*u*inner
    tail=Lam*(1-np.exp(m['logpi']))*np.exp(-g*T)*(T/g+1/g**2)
    return dict(coefficient=float(result),cutoff=T,analytic_tail_bound=float(tail),
                nodes=[nu_nodes,nv_nodes])


def large_run():
    out=[]
    for n in [32,64,128,256]:
        begin=time.perf_counter()
        # Antiferromagnetic spin interaction.  No-wall/global ferromagnetic
        # target is rare; rates remain genuine interacting heat-bath rates.
        m=model(np.full(n,-.4))
        r=mean_reference(m,rtol=1e-8)
        out.append(dict(n=n,configurations=f'2^{n-1}',log10_pi=m['logpi']/np.log(10),
            gaussian_normalization_error=m['normalization_error'],gap=m['gap'],
            reference=r,seconds=time.perf_counter()-begin))
    return out


if __name__=='__main__':
    start=time.perf_counter()
    results={'scope':'exact algebra; floating point evidence, not an interval implementation',
             'dense_checks':dense_checks(), 'large_reference':large_run()}
    results['seconds']=time.perf_counter()-start
    Path(__file__).with_name('gaussian_results.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
