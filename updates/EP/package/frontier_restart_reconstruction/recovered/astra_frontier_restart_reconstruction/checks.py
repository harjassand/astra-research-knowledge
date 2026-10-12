"""Finite diagnostics for restart-and-reconstruct transport.

Dense/sparse small-system tests, NOT the asymptotic locality-based simulator.
Exact rational block algebra is distinguished from floating spin/trajectory checks.
"""
from __future__ import annotations
import json, math, time
from fractions import Fraction
from pathlib import Path
import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
import scipy.sparse.linalg as sla
import sympy as sy

ROOT=Path(__file__).resolve().parent

def weights(m: int) -> list[Fraction]:
    assert m >= 1
    return [math.prod([Fraction(-(m+k), j-k) for k in range(m+1) if k != j]) for j in range(m+1)]

def sector(n:int,k:int,t:float=1.,U:float=4.,V:float=1.):
    states=[x for x in range(1<<n) if x.bit_count()==k]; ind={x:i for i,x in enumerate(states)}; D=len(states)
    H=np.zeros((D,D),complex); bonds=[np.zeros_like(H) for _ in range(n)]
    for ix,x in enumerate(states):
        occ=[((x>>i)&1)-.5 for i in range(n)]
        H[ix,ix]=sum(U*occ[i]*occ[(i+1)%n]+V*occ[i]*occ[(i+2)%n] for i in range(n))
        for i in range(n):
            j=(i+1)%n
            ni=(x>>i)&1; nj=(x>>j)&1
            if ni!=nj:
                y=x^(1<<i)^(1<<j); iy=ind[y]
                H[iy,ix] += -t
                # Hopping current convention; a global sign does not change response.
                bonds[i][iy,ix] += 1j*t*(ni-nj)
    return states,H,sum(bonds),bonds

def response(n:int,r:complex=0.,lam:float=0.,d:float=2.,U:float=4.,V:float=1.):
    value=0j; residual=0.
    for k in range(1,n):
        states,H,J,_=sector(n,k,U=U,V=V); D=len(states)
        A=-1j*(sp.kron(sp.eye(D),sp.csc_matrix(H))-sp.kron(sp.csc_matrix(H.T),sp.eye(D)))
        rates=np.array([.5*d*(x^y).bit_count() for y in states for x in states])
        q=np.array([float(x!=y) for y in states for x in states])
        v=np.eye(D).reshape(-1,order='F'); vsp=sp.csc_matrix(v[:,None])
        gauge=vsp@vsp.T/D
        B=(A+sp.diags(rates+r*q+lam)+gauge).tocsc()
        j=J.reshape(-1,order='F'); sol=sla.spsolve(B,j)
        value+=np.vdot(j,sol)/(n*2**n)
        residual=max(residual,float(la.norm(B@sol-j)/max(1.,la.norm(j))))
    return value,residual

def exact_blocks():
    # Coordinates: two populations and five coherences. All arithmetic exact.
    S=sy.diag(0,0,2,3,2,4,5)
    A=sy.Matrix([[0,0,1,2,0,1,0],[0,0,0,1,1,-1,2],[-1,0,0,2,-1,0,1],[-2,-1,-2,0,1,1,0],[0,-1,1,-1,0,2,1],[-1,1,0,-1,-2,0,1],[0,-2,-1,0,-1,-1,0]])
    assert A.T == -A
    Q=sy.diag(0,0,1,1,1,1,1); B=S+A
    j=sy.Matrix([0,0,1,-2,0,1,2]); a=(j.T*j)[0]; d=sy.Rational(2)
    N=sy.Matrix.hstack(*A[:2,2:].nullspace())
    M=N.T*N; C=N.T*(S+A)[2:,2:]*N; v=N.T*j[2:,:]
    out=[]
    for r in [sy.Rational(0),sy.Rational(1,4),sy.Rational(3,8),sy.Rational(1,2),sy.I/3]:
        full=(j.T*(B+r*Q).inv()*j)[0]
        compressed=(v.T*(C+r*M).inv()*v)[0]
        assert sy.simplify(full-compressed)==0
        out.append({'r':str(r),'response':str(full)})
    f0=(j.T*B.inv()*j)[0]
    interpolation=[]
    for m in (1,2,3,4,6):
        ww=weights(m); est=0
        for jj,w in enumerate(ww):
            r=d*sy.Rational(m+jj,8*m)
            est+=sy.Rational(w.numerator,w.denominator)*(j.T*(B+r*Q).inv()*j)[0]
        err=abs(est-f0); bound=4*a/d*sy.Rational(1,2**(m+1))
        assert err<=bound
        assert sum(ww)==1
        for power in range(1,m+1):
            assert sum(w*Fraction(m+jj,m)**power for jj,w in enumerate(ww))==0
        interpolation.append({'order':m,'estimate':str(est),'error':str(err),'bound':str(bound),'weight_l1':str(sum(abs(w) for w in ww))})
    # A population pole is not protected under ordinary identity regularisation.
    tiny=sy.Rational(1,100)
    B2=sy.Matrix([[0,tiny],[-tiny,1]])
    assert sy.simplify((B2.inv())[1,1])==0
    return {'exact_equalities':len(out),'values':out,'interpolation':interpolation,'status':'exact rational/symbolic identities; not external validation'}

def spin_quotient():
    rng=np.random.default_rng(771231); tests=[]
    for n,k in [(4,2),(5,2),(6,2)]:
        states,H,J,_=sector(n,k); D=len(states)
        A=-1j*(np.kron(np.eye(D),H)-np.kron(H.T,np.eye(D)))
        off=np.array([i for i in range(D*D) if i%(D+1)!=0]); pop=np.arange(0,D*D,D+1)
        rates=np.array([(x^y).bit_count() for y in states for x in states])
        Aqq=A[np.ix_(off,off)]; Apq=A[np.ix_(pop,off)]
        N=la.null_space(Apq); C=N.conj().T@(np.diag(rates[off])+Aqq)@N
        ev=la.eigvalsh((C+C.conj().T)/2)
        assert ev.min()>2-1e-10
        jj=J.reshape(-1,order='F'); v=N.conj().T@jj[off]
        gauge=np.zeros((D*D,D*D)); gauge[np.ix_(pop,pop)]=1/D
        for z in [0.,.25,.5,-.6+.7j]:
            qdiag=np.ones(D*D);qdiag[pop]=0
            full=np.vdot(jj,la.solve(np.diag(rates+z*qdiag)+A+gauge,jj))
            comp=np.vdot(v,la.solve(C+z*np.eye(len(C)),v))
            err=abs(full-comp)
            assert err<2e-9
            assert abs(comp)<=np.vdot(jj,jj).real/(2+complex(z).real)+1e-8
            tests.append({'n':n,'sector':k,'z':str(z),'error':float(err),'minimum_real_part':float(ev.min()),'constraint_dimension':int(N.shape[1])})
    return tests

def spin_interpolation():
    out=[]
    for n in [5,6,7]:
        base,res=response(n); by=[]; cache={}
        for m in [1,2,4,8]:
            ww=weights(m); est=0j
            for j,w in enumerate(ww):
                key=Fraction(m+j,4*m)
                if key not in cache: cache[key]=response(n,r=float(key))
                val,err=cache[key];res=max(res,err)
                est+=float(w)*val
            analytic=2**(-(m+1)) # 4a/d=1 for t=1,d=2
            assert abs(est-base)<=analytic+1e-8
            by.append({'order':m,'D_estimate':float(4*est.real),'absolute_D_error':float(4*abs(est-base)),'D_analytic_bias_bound':float(4*analytic),'weight_l1':str(sum(abs(w) for w in ww))})
        out.append({'n':n,'D_direct':float(4*base.real),'largest_solve_residual':res,'interpolation':by})
    return out

def trajectory_check(N:int=16000):
    """Small full-state simulation. Reproduces the monitored estimator only."""
    n=4;d=2.;r=.3;lam=1.;t=1.
    rng=np.random.default_rng(128210)
    D=1<<n;H=np.zeros((D,D),complex);bonds=[np.zeros_like(H) for _ in range(n)]
    for k in range(n+1):
        states,h,j,bb=sector(n,k)
        H[np.ix_(states,states)]=h
        for i in range(n):bonds[i][np.ix_(states,states)]=bb[i]
    ev,U=la.eigh(H)
    zz=np.array([[1-2*((x>>i)&1) for x in range(D)] for i in range(n)])
    pair=np.array([1,2]);pair_j=bonds[0][np.ix_(pair,pair)]
    pev,pU=la.eigh(pair_j)
    meas=[]
    for j in range(n):
        e,v=la.eigh(bonds[j]/t);meas.append((e,v))
    def evolve(v,dt):return U@(np.exp(-1j*ev*dt)*(U.conj().T@v))
    vals=np.empty(N); total_events=0;max_interval=0.; resets=0
    for q in range(N):
        sign=1 if rng.integers(2) else -1
        rest=int(rng.integers(1<<(n-2)))<<2
        mode=int(rng.integers(4));psi=np.zeros(D,complex)
        if mode==0:psi[rest]=1
        elif mode==1:psi[rest+3]=1
        else:psi[rest+pair]=pU[:,0 if sign<0 else 1]
        T=rng.exponential(1/lam);now=0.;since=0.;rate=r+n*d/4
        while now<T:
            wait=rng.exponential(1/rate);dt=min(wait,T-now)
            psi=evolve(psi,dt);now+=dt;since+=dt
            if now>=T:break
            total_events+=1
            if rng.random()<r/rate:
                x=rng.choice(D,p=np.maximum(0,abs(psi)**2)/sum(abs(psi)**2));psi[:]=0;psi[x]=1
                resets+=1;max_interval=max(max_interval,since);since=0.
            else:psi*=zz[rng.integers(n)]
        max_interval=max(max_interval,since)
        j=int(rng.integers(n)); e,v=meas[j];pp=abs(v.conj().T@psi)**2;pp/=sum(pp)
        y=float(e[rng.choice(D,p=pp)])
        vals[q]=n*t*t/lam*sign*y
    exact,_=response(n,r=r,lam=lam)
    rad=4*math.sqrt(2*math.log(200)/N)
    assert abs(vals.mean()-exact.real)<rad
    return {'status':'synthetic full-state monitored-trajectory diagnostic, not scalable compiler or laboratory data','n':n,'r':r,'lambda':lam,'samples':N,'exact_regularized_kappa':float(exact.real),'sample_mean':float(vals.mean()),'standard_error':float(vals.std(ddof=1)/math.sqrt(N)),'hoeffding_99pct_radius':rad,'events':total_events,'global_measurements':resets,'longest_coherent_interval':max_interval}

def budget(n:int=8,eps:float=.01,alpha:float=.01):
    # Conservative self-contained polynomial inverse bound (no Aldous theorem).
    d=2.;t=1.;a=.5;h_sum=n*(t+4/4+1/4)
    sigma=t/(2*n*n);s=d*n/2+d/4;Amax=2*h_sum
    R=2/sigma+(1+(s+Amax)/sigma)**2/d
    m=max(1,math.ceil(math.log2(16*a/(d*eps))))
    W=sum(abs(w) for w in weights(m));delta=eps/(4*float(W))
    lam=min(1.,delta/(8*a*R*R));B=n*t*t/lam
    log10N=math.log10(128)+2*math.log10(B)-2*math.log10(delta)+math.log10(math.log(2*(m+1)/alpha))
    p=delta/(64*B);Tcut=math.log(1/p)/lam
    E=(d/8)*Tcut;cap=math.ceil(2*(math.e-1)*E+math.log(1/p)+2)
    tau=8/d*math.log((cap+1)/p)
    return {'n':n,'epsilon_kappa':eps,'m':m,'weight_l1':str(W),'node_accuracy':delta,'inverse_bound_R':R,'lambda':lam,'estimator_bound':B,'log10_samples_per_node':log10N,'coherent_interval_cap':tau,'total_time_cap':Tcut,'status':'conservative proof budget; plainly impractical, not implemented'}

def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--part',choices=['all','blocks','quotient','interpolation','trajectory','budget'],default='all')
    args=parser.parse_args()
    tasks={'blocks':('exact_block_checks',exact_blocks),'quotient':('physical_quotient_checks',spin_quotient),'interpolation':('physical_interpolation',spin_interpolation),'trajectory':('monitored_sampling',trajectory_check),'budget':('resource_budget',budget)}
    target=ROOT/'checks.json'
    out=json.loads(target.read_text()) if target.exists() else {}
    selected=list(tasks) if args.part=='all' else [args.part]
    for name in selected:
        key,func=tasks[name];start=time.time()
        print('Starting',name,flush=True)
        out[key]=func()
        out.setdefault('section_seconds',{})[name]=time.time()-start
        out['versions']={'numpy':np.__version__,'scipy':__import__('scipy').__version__,'sympy':sy.__version__}
        target.write_text(json.dumps(out,indent=2))
        print('Finished',name,'seconds',out['section_seconds'][name],flush=True)
    print('Results:',target,flush=True)
if __name__=='__main__':main()
