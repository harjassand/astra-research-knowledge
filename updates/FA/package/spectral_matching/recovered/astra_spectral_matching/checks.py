#!/usr/bin/env python3
"""Reproducible finite diagnostics, not a proof of thermodynamic transport.

Run with OPENBLAS_NUM_THREADS=1 python checks.py.
Requires numpy and scipy. Outputs JSON. Random seed is fixed.
"""
from __future__ import annotations
import itertools, json, math, time
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.optimize import minimize_scalar
from scipy.integrate import quad
from scipy.special import k1

ROOT=Path(__file__).resolve().parent
A=32/25
BETA=15/4
COMPETITIVE=0.97

def matched_gamma(delta, eta):
    mass=BETA*eta
    # Rationalized difference avoids cancellation for small gaps.
    delta=np.asarray(delta)
    return eta+A*delta*delta/(np.hypot(mass,delta)+mass)

def matched_exponent(delta, eta):
    return matched_gamma(delta,eta)-eta

def rate(delta: np.ndarray, gamma: np.ndarray, hopping: float=1.0):
    return 2.0*hopping*hopping*gamma/(gamma*gamma+delta*delta)

def analytic_checks():
    x=np.unique(np.r_[0., np.logspace(-8,8,200001), 1/math.sqrt(2),1.])
    gm=matched_gamma(x,1.)
    go=np.maximum(1,x)
    ratio=rate(x,gm)/rate(x,go)
    c=COMPETITIVE
    assert np.min(ratio)>=c-1e-14
    assert np.max(ratio)<=1+1e-14
    # Exact rational certificate for the low-gap polynomial after t=sqrt(225+16*x*x)-15.
    qa=F(502547,10000); qb=F(4891,200)
    qmin=F(3)-qb*qb/(4*qa)
    assert qmin==F(200375,8040752) and qmin>0
    r2=F(688,1125)
    high_margin=4*r2/(1+r2)**2-F(97,100)**2
    assert high_margin>0 and F(1600,1649)>F(97,100)
    # No universal symmetric Levy phase law can guarantee .973 against the same edge oracle.
    a=F(2,3);t0=F(69,1000);w=4*a;g=1+t0;h=1+16*t0
    upper1=g*(1+a*a)/(g*g+a*a);upper2=2*w*h/(h*h+w*w)
    assert upper1<F(973,1000) and upper2<F(973,1000)
    return {'proved_competitive_constant':c,'grid_points':len(x),'grid_min':float(min(ratio)),
            'argmin':float(x[np.argmin(ratio)]),'exact_low_gap_quadratic_minimum':str(qmin),
            'exact_high_gap_squared_margin':str(high_margin),
            'universal_symmetric_levy_upper_bound':str(max(upper1,upper2)),
            'universal_symmetric_levy_upper_bound_decimal':float(max(upper1,upper2))}

def system(n: int, k: int, seed: int=17):
    if not (n>=4 and 0<k<n):
        raise ValueError('Require n>=4 and 0<k<n')
    rng=np.random.default_rng(seed)
    occ=np.asarray([[(b>>i)&1 for i in range(n)] for b in range(1<<n) if b.bit_count()==k],float)
    bitvals=np.sum(occ*(1<<np.arange(n)),axis=1).astype(int)
    index={v:i for i,v in enumerate(bitvals)}
    m=len(occ)
    v=rng.uniform(-4,4,n)
    u=rng.uniform(1,5,n)
    energies=occ@v+np.sum(u[None,:]*occ*np.roll(occ,-1,axis=1),axis=1)
    rows=[];cols=[];ds=[]
    for ix,b in enumerate(bitvals):
        for j in range(n):
            r=(j+1)%n
            if occ[ix,j]==1 and occ[ix,r]==0:
                y=index[b^(1<<j)^(1<<r)]
                rows.extend([ix,y]);cols.extend([y,ix]);ds.extend([1.,-1.])
    rows=np.asarray(rows);cols=np.asarray(cols);ds=np.asarray(ds)
    hop=sparse.csr_matrix((-np.ones(len(rows)),(rows,cols)),shape=(m,m))
    delta=energies[rows]-energies[cols]
    # Every allowed hop changes two bits. Fixed-number off-diagonal pairs change >=2.
    hamming=np.sum(np.abs(occ[:,None,:]-occ[None,:,:]),axis=2)
    return dict(n=n,k=k,m=m,occ=occ,energies=energies,rows=rows,cols=cols,ds=ds,hop=hop,
                delta=delta,hamming=hamming,site_fields=v,interactions=u)

def classical_current(data, eta:float, mode:str, scalar_gamma:float|None=None):
    de=data['delta']; r=data['rows']; c=data['cols']; d=data['ds'];m=data['m'];n=data['n']
    if mode=='matched': gam=matched_gamma(de,eta)
    elif mode=='oracle':gam=np.maximum(eta,np.abs(de))
    elif mode=='scalar':
        if scalar_gamma is None or scalar_gamma<eta:raise ValueError('bad gamma')
        gam=np.full_like(de,scalar_gamma)
    elif mode=='cancel_D':gam=np.full_like(de,eta);de=np.zeros_like(de)
    else:raise ValueError(mode)
    q=rate(de,gam)
    deg=np.bincount(r,weights=q,minlength=m)
    K=sparse.diags(deg)-sparse.csr_matrix((q,(r,c)),shape=(m,m))
    drift=np.bincount(r,weights=q*d,minlength=m)
    # Pin one value rather than invert singular conserved-population generator.
    f=np.zeros(m);f[1:]=spsolve(K[1:,1:].tocsc(),drift[1:])
    ans=(0.5*np.sum(q*d*d)-np.dot(drift,f))/(n*m)
    err=np.linalg.norm(K@f-drift)
    return float(ans),float(err)

def quantum_current(data,eta:float,eps:float,mode:str,scalar_gamma:float|None=None):
    m=data['m'];n=data['n']; E=data['energies']
    full_delta=E[:,None]-E[None,:]
    if mode=='matched':
        gamma=eta*data['hamming']/2+matched_exponent(full_delta,eta)
    elif mode=='scalar':
        gamma=scalar_gamma*data['hamming']/2
    elif mode=='cancel_D':
        gamma=eta*data['hamming']/2
        E=np.zeros_like(E)
    else:raise ValueError(mode)
    H=sparse.diags(E)+eps*data['hop']; Id=sparse.eye(m,format='csr')
    # Column-major vectorization: vec([H,O])=(I kron H-H.T kron I)vec(O).
    B=sparse.diags(gamma.reshape(-1,order='F')).astype(complex)-1j*(sparse.kron(Id,H)-sparse.kron(H.T,Id))
    # J_xy = -i eps d_xy ; current orientation does not affect this quadratic form.
    J=sparse.csr_matrix((-1j*eps*data['ds'],(data['rows'],data['cols'])),shape=(m,m)).toarray()
    j=J.reshape(-1,order='F')
    tr=np.zeros(m*m,complex);tr[np.arange(m)*(m+1)]=1/math.sqrt(m)
    # Sparse bordered solve enforces trace zero and preserves all other equations.
    bordered=sparse.bmat([[B,sparse.csc_matrix(tr[:,None])],
                         [sparse.csc_matrix(tr.conj()[None,:]),None]],format='csc')
    z=spsolve(bordered,np.r_[j,0j])[:-1]
    resid=float(np.linalg.norm(B@z-j)/max(np.linalg.norm(j),1e-30))
    ans=float(np.vdot(j,z).real/(n*m))
    return ans,resid

def finite_diagnostics():
    out=[]
    for n,k in [(4,2),(6,3)]:
        dat=system(n,k)
        eta=1.
        cm,err=classical_current(dat,eta,'matched')
        co,_=classical_current(dat,eta,'oracle')
        # Beyond max(|gap|,eta), every edge rate decreases: no maximizer is lost.
        upper=max(eta,float(np.max(np.abs(dat['delta']))))
        grid=np.linspace(math.log(eta),math.log(upper),129)
        vals=np.array([classical_current(dat,eta,'scalar',math.exp(z))[0] for z in grid])
        candidates=[(float(vals[0]),float(grid[0])),(float(vals[-1]),float(grid[-1]))]
        for i in range(1,len(grid)-1):
            if vals[i]>=vals[i-1] and vals[i]>=vals[i+1]:
                opt=minimize_scalar(lambda logg:-classical_current(dat,eta,'scalar',math.exp(logg))[0],
                                    bounds=(grid[i-1],grid[i+1]),method='bounded',options={'xatol':1e-11})
                candidates.append((-float(opt.fun),float(opt.x)))
        best,logbest=max(candidates)
        bestg=math.exp(logbest)
        cc,_=classical_current(dat,eta,'cancel_D')
        assert cm>=COMPETITIVE*co-1e-12 and cm<=co+1e-12
        entries=[]
        for eps in [.02,.05,.1,.2,.5,1.,2.]:
            q,r=quantum_current(dat,eta,eps,'matched')
            qs,rs=quantum_current(dat,eta,eps,'scalar',bestg)
            qc,rc=quantum_current(dat,eta,eps,'cancel_D')
            entries.append(dict(epsilon=eps,matched_quantum_over_eps2=q/eps**2,
                                matched_to_kinetic=q/(eps**2*cm),
                                fixed_scalar_quantum_over_eps2=qs/eps**2,
                                cancellation_quantum_over_eps2=qc/eps**2,
                                max_linear_residual=max(r,rs,rc)))
        out.append(dict(sites=n,particles=k,states=dat['m'],seed=17,
                        fields=dat['site_fields'].tolist(),interactions=dat['interactions'].tolist(),
                        kinetic_matched=cm,kinetic_oracle=co,matched_over_oracle=cm/co,
                        kinetic_numerically_optimized_scalar=best,numerically_optimized_scalar_gamma=bestg,
                        scalar_search='129 log-grid points plus bounded refinement; not interval certified',
                        matched_over_numerically_optimized_scalar=cm/best,kinetic_cancel_D=cc,
                        classical_solve_residual=err,quantum=entries))
    return out

def levy_checks():
    # Numerically integrate in logarithmic pulse-size coordinates; exact bounds in note.
    eta=1.; tests=[]
    for w in [.2,1.,3.,10.]:
        integ,_=quad(lambda s:2*(1-math.cos(w*s))*A*BETA*eta*k1(BETA*eta*s)/(math.pi*s),
                     1e-8,40,epsabs=1e-9,limit=1000)
        exact=float(matched_exponent(w,eta))
        assert abs(integ-exact)<2e-5
        tests.append(dict(detuning=w,levy_integral=integ,exact_exponent=exact))
    return tests

if __name__=='__main__':
    t=time.perf_counter()
    result={'status':'finite floating-point diagnostics; not independent proof or experiment',
            'analytic_rate_check':analytic_checks(),'levy_integral_check':levy_checks(),
            'finite_interacting_ring_diagnostics':finite_diagnostics()}
    result['wall_seconds']=time.perf_counter()-t
    (ROOT/'results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
