"""Reproducible floating-point tests, NOT an interval-certified implementation.
Run: python experiment.py --h 0.01 --duration 1200
NumPy/SciPy quadrature is independent of the stochastic implementation.
"""
from __future__ import annotations
import argparse, json, math, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from numpy.polynomial.hermite import hermgauss
from scipy.integrate import quad
from numba import njit
ROOT=Path(__file__).resolve().parent

def certificate(A,C,edges,a,c,r,u0=F(1,10),v0=F(11,10)):
    """Exact rational sufficient test for the specific paired-quartic family."""
    n=len(A); cv=lambda x: x if isinstance(x,F) else F(str(x))
    A=[[cv(x) for x in row] for row in A]; C=[[cv(x) for x in row] for row in C]
    a,c,r,u0,v0=map(cv,(a,c,r,u0,v0)); degree=[0]*n
    for i,j in edges: degree[i]+=1; degree[j]+=1
    D=max(degree)
    if min(a,c,r,u0)<=0 or v0<=1 or D<1: raise ValueError('Invalid certificate inputs')
    if any(A[i][j]!=A[j][i] or C[i][j]!=C[j][i] for i in range(n) for j in range(n)):
        raise ValueError('A and C must be symmetric')
    eset={tuple(sorted((int(i),int(j)))) for i,j in edges}
    if any(C[i][j] and tuple(sorted((i,j))) not in eset for i in range(n) for j in range(i)):
        raise ValueError('C has an unsupported off-diagonal entry')
    m=min(A[i][i]-sum(abs(A[i][j]) for j in range(n) if j!=i) for i in range(n))
    c1=max(sum(abs(v) for v in row) for row in C)
    c2=max(sum(v*v for v in row) for row in C)
    ms=m-u0*c1; th=min(3*a/F(1+2*D),3*c)
    lam=ms-(3*a+24*c*D)*r*r
    inward=ms*r-(a+8*c*D)*r**3-v0*v0*c2/(4*r*th)
    values=dict(m=m,c1=c1,c2_squared=c2,m_star=ms,theta=th,lambda_=lam,inward=inward)
    return {'passed':lam>0 and inward>0,'dimension':n,'degree':D,
            'exact':{k:str(v) for k,v in values.items()},
            'float':{k:float(v) for k,v in values.items()},
            'r':float(r),'u0':float(u0),'v0':float(v0)}

def acquire_radius(A,C,edges,a,c,u0=F(1,10),v0=F(11,10)):
    """Acquire a rational radius or prove no radius passes this sufficient test.
    Reduces feasibility to a concave quadratic in s=r^2; no hidden oracle.
    Runtime can depend on the bit size of small strict margins.
    """
    cv=lambda x: x if isinstance(x,F) else F(str(x))
    n=len(A); AF=[[cv(x) for x in row] for row in A];CF=[[cv(x) for x in row] for row in C]
    a,c,u0,v0=map(cv,(a,c,u0,v0));degree=[0]*n
    for i,j in edges:degree[i]+=1;degree[j]+=1
    D=max(degree)
    if min(a,c,u0)<=0 or v0<=1 or D<1:raise ValueError('Invalid inputs')
    m=min(AF[i][i]-sum(abs(AF[i][j]) for j in range(n) if j!=i) for i in range(n))
    c1=max(sum(abs(x) for x in row) for row in CF)
    c2=max(sum(x*x for x in row) for row in CF)
    ms=m-u0*c1
    if ms<=0:return None
    th=min(3*a/F(1+2*D),3*c); alpha=a+8*c*D
    cap=ms/(3*a+24*c*D); kappa=v0*v0*c2/(4*th)
    f=lambda s:ms*s-alpha*s*s-kappa
    center=min(ms/(2*alpha),cap)
    if f(center)<=0:return None
    chosen=center
    if center==cap:
        k=1
        while True:
            chosen=cap*(1-F(1,2**k))
            if f(chosen)>0:break
            k+=1
    bits=1
    while True:
        den=2**bits; num=math.isqrt((chosen.numerator*den*den)//chosen.denominator)
        radius=F(num,den)
        if radius>0 and radius*radius<cap and f(radius*radius)>0:
            cert=certificate(AF,CF,edges,a,c,radius,u0,v0)
            assert cert['passed']
            return radius,cert
        bits+=1

@njit(cache=True)
def gh(z,A,C,edges,a,c,t):
    n=len(z); H=A.astype(np.complex128)-1j*t*C
    g=H@z
    for i in range(n):
        g[i]+=a*z[i]**3; H[i,i]+=3*a*z[i]**2
    for ij in edges:
        i,j=ij[0],ij[1]; p=z[i]+z[j]; q=z[i]-z[j]
        g[i]+=c*(p**3+q**3); g[j]+=c*(p**3-q**3)
        d=3*c*(p*p+q*q); off=3*c*(p*p-q*q)
        H[i,i]+=d; H[j,j]+=d; H[i,j]+=off; H[j,i]+=off
    return g,H

@njit(cache=True)
def implicit_step(z,noise,h,A,C,edges,a,c,t,r,tol):
    w=z+noise; v=z.copy(); n=len(z)
    for it in range(30):
        g,H=gh(v,A,C,edges,a,c,t); res=v+h*g-w; rn=np.sqrt(np.sum(np.abs(res)**2))
        if rn<=tol: return v,rn,it,0
        for i in range(n): H[i,i]+=1/h
        step=np.linalg.solve(H,res/h); fac=1.; ok=False
        for back in range(40):
            trial=v-fac*step
            if np.max(np.abs(trial.imag))<r:
                gt,_=gh(trial,A,C,edges,a,c,t)
                nr=np.sqrt(np.sum(np.abs(trial+h*gt-w)**2))
                if nr<=(1-1.e-4*fac)*rn:
                    v=trial; ok=True; break
            fac*=.5
        if not ok: return v,rn,it,-1
    g,_=gh(v,A,C,edges,a,c,t)
    return v,np.sqrt(np.sum(np.abs(v+h*g-w)**2)),30,-2

@njit(cache=True)
def run_chain(seed,nsteps,burn,h,A,C,edges,a,c,t,r,batchsteps):
    np.random.seed(seed); n=len(A); z=np.zeros(n,dtype=np.complex128)
    nb=(nsteps-burn)//batchsteps; means=np.zeros(nb,dtype=np.complex128)
    maximag=0.; maxres=0.; maxit=0; failures=0; total=0j; b=0; count=0
    for step in range(nsteps):
        noise=np.sqrt(2*h)*np.random.normal(0.,1.,n)
        z,res,it,fail=implicit_step(z,noise,h,A,C,edges,a,c,t,r,1.e-11)
        maximag=max(maximag,np.max(np.abs(z.imag))); maxres=max(maxres,res); maxit=max(maxit,it)
        if fail: failures+=1; break
        if step>=burn and b<nb:
            total+=.5j*np.dot(z,C.astype(np.complex128)@z); count+=1
            if count==batchsteps:
                means[b]=total/batchsteps; b+=1; total=0j; count=0
    return means[:b],maximag,maxres,maxit,failures

def target_2d(A,C,a,c,t,order):
    q,w=hermgauss(order); scale=math.sqrt(float(np.min(np.diag(A)))/2)
    x=q[:,None]/scale; y=q[None,:]/scale
    V=.5*(A[0,0]*x*x+2*A[0,1]*x*y+A[1,1]*y*y)+a/4*(x**4+y**4)+c/4*((x+y)**4+(x-y)**4)
    W=.5*(C[0,0]*x*x+2*C[0,1]*x*y+C[1,1]*y*y)
    terms=(w[:,None]*w[None,:])*np.exp(-V+scale**2*(x*x+y*y)+1j*t*W)/(scale*scale)
    Z=terms.sum(); return complex(Z),complex((terms*1j*W).sum()/Z)

def pair(z): return [float(z.real),float(z.imag)]
def fixture():
    return np.array([[2.4,-.4],[-.4,2.4]]),np.array([[.4,.2],[.2,.4]]),np.array([[0,1]],dtype=np.int64),.5,.2,.45

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--h',type=float,default=.01); ap.add_argument('--duration',type=float,default=1200); ap.add_argument('--nodes',type=int,default=6)
    args=ap.parse_args(); A,C,edges,a,c,r=fixture(); cert=certificate(A,C,edges,a,c,r)
    assert cert['passed']; start=time.perf_counter()
    truth=[]
    for order in (64,100,160):
        Z0,_=target_2d(A,C,a,c,0.,order); Z1,_=target_2d(A,C,a,c,1.,order)
        truth.append({'order':order,'log_ratio':pair(np.log(Z1/Z0))})
    nodes,weights=leggauss(args.nodes); nodes=(nodes+1)/2; weights=weights/2
    gltruth=sum(w*target_2d(A,C,a,c,float(t),160)[1] for t,w in zip(nodes,weights))
    run_chain(1,20,0,.01,A,C,edges,a,c,.5,r,5) # compilation excluded from recorded trajectory time
    jit_done=time.perf_counter(); records=[]; final=0j; varre=0.; varim=0.
    h=args.h; burn=int(math.ceil(20/h)); batchsteps=int(round(10/h)); nb=int(args.duration/10)
    for j,(t,w) in enumerate(zip(nodes,weights)):
        means,mi,mr,it,fail=run_chain(190700+1000*j+int(round(1/h)),burn+nb*batchsteps,burn,h,A,C,edges,a,c,float(t),r,batchsteps)
        if fail or len(means)<2: raise RuntimeError(f'Implicit solve failed: {fail}')
        avg=means.mean(); sr=means.real.std(ddof=1)/math.sqrt(len(means)); si=means.imag.std(ddof=1)/math.sqrt(len(means))
        final+=w*avg; varre+=(w*sr)**2; varim+=(w*si)**2
        records.append({'t':float(t),'mean_iW':pair(avg),'empirical_batch_se':[float(sr),float(si)],'batches':len(means),'max_abs_imag':float(mi),'max_solver_residual':float(mr),'max_Newton_iterations':int(it),'failures':int(fail)})
    tm=time.perf_counter()
    def moment(sign):
        f=lambda x: math.exp(-x**4/4+sign*x*x/2)
        den=quad(f,-np.inf,np.inf,epsabs=1.e-12,epsrel=1.e-12)[0]
        return quad(lambda x:x*x*f(x),-np.inf,np.inf,epsabs=1.e-12,epsrel=1.e-12)[0]/den
    base=complex(*truth[-1]['log_ratio']); replication=[]
    for B in (1,100,1000,10000):
        lm=B*base.real; x=-2*lm
        logvar=x if x>50 else math.log(math.expm1(x))
        replication.append({'blocks':B,'log_mean_phase_modulus':lm,'log_relative_variance_times_samples':logvar})
    output={'status':'floating-point diagnostic; empirical batch errors are not rigorous confidence intervals','fixture':{'A':A.tolist(),'C':C.tolist(),'edges':edges.tolist(),'a':a,'c':c,'r':r},'certificate':cert,'quadrature_truth':truth,'GL_truth':pair(gltruth),'h':h,'burn_time':20,'measurement_time_per_node':nb*10,'nodes':args.nodes,'log_ratio_estimate':pair(final),'empirical_batch_se':[math.sqrt(varre),math.sqrt(varim)],'error_vs_quadrature':pair(final-base),'node_records':records,'replicated_phase_example':replication,'wrong_cycle':{'real_cycle_second_moment':moment(1),'imaginary_cycle_second_moment':-moment(-1)},'timing_seconds':{'JIT_and_quadrature':jit_done-start,'trajectories':tm-jit_done,'total':time.perf_counter()-start}}
    out=ROOT/f'results_h_{h:g}.json';out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('h','log_ratio_estimate','empirical_batch_se','error_vs_quadrature','timing_seconds')},indent=2),flush=True)
if __name__=='__main__':main()
