"""Finite-LO photon trajectories and exact regression; small-model diagnostic."""
import argparse,itertools,json,math,time
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
P={'I':np.eye(2,dtype=complex),'X':np.array([[0,1],[1,0]],complex),
   'Y':np.array([[0,-1j],[1j,0]],complex),'Z':np.diag([1,-1]).astype(complex)}
AX='XYZ'
def mat(s):
    out=np.array([[1]],complex)
    for a in s:out=np.kron(out,P[a])
    return out
def labels(n,k):return [''.join(s) for s in itertools.product('IXYZ',repeat=n) if 0<sum(a!='I' for a in s)<=k]
def ports(n):return [mat('I'*i+a+'I'*(n-i-1)) for i in range(n) for a in AX]
def layout(s):
    i=next(j for j,a in enumerate(s) if a!='I');b={'X':'Z','Y':'X','Z':'Y'}[s[i]]
    rr=list(s);rr[i]={'X':'Y','Y':'Z','Z':'X'}[s[i]]
    return [3*j+AX.index(a) for j,a in enumerate(rr) if a!='I'],3*i+AX.index(b)
def generator(h,r,n):
    d=2**n;ii=np.eye(d);eye=np.eye(d*d)
    out=-1j*(np.kron(ii,h)-np.kron(h.T,ii))
    for p in ports(n):out+=r/4*(np.kron(p.conj(),p)-eye)
    return out
def window(lgen,ops,rho,w):
    d2=len(rho);bs=1<<len(ops);big=np.zeros((bs*d2,bs*d2),complex)
    for s in range(bs):
        sl=slice(s*d2,(s+1)*d2);big[sl,sl]=lgen
        for j,a in enumerate(ops):
            if s&(1<<j):
                old=s^(1<<j);big[sl,old*d2:(old+1)*d2]=a
    v=np.zeros(bs*d2,complex);v[:d2]=rho
    return (expm(w*big)@v)[-d2:]
def response(theta,ls,r,w):
    n=len(ls[0]);d=2**n;ii=np.eye(d)
    h=sum((a*mat(s) for a,s in zip(theta,ls)),np.zeros((d,d),complex))
    ll=generator(h,r,n);rho=(ii/d).reshape(-1,order='F')
    jj=[(np.kron(ii,p)+np.kron(p.T,ii))/(2*w) for p in ports(n)]
    ff=[];rr=[]
    for s in ls:
        f,b=layout(s);fa=[jj[j] for j in f];ba=[jj[b]]
        v=window(ll,ba,window(ll,fa,rho,w),w)
        ff.append(np.trace(v.reshape((d,d),order='F')).real)
        v=window(ll,fa,window(ll,ba,rho,w),w)
        rr.append(np.trace(v.reshape((d,d),order='F')).real)
    ff=np.array(ff);rr=np.array(rr)
    return (ff-rr)/2,ff,rr
def c_slope(b,q):
    if q==0:return 2.
    def a(u):
        return (2-math.exp(-q*u)-math.exp(-q*(1-u)))/q if u<=1 else math.exp(-q*(u-1))*(-math.expm1(-q))/q
    z=(math.exp(-q)-math.exp(-2*q))/q
    f=2*z*quad(lambda u:math.expm1(q*u)/q*a(u)**(b-1),0,1,epsabs=1e-12)[0]
    v=2*math.expm1(q)/q*quad(lambda u:a(u)**(b-1)*(math.exp(-q*u)-math.exp(-2*q))/q,1,2,epsabs=1e-12)[0]
    return f+v
def statistics(counts,ls,mu,kappa,q):
    out=[]
    for s in ls:
        f,b=layout(s);left=np.prod(counts[:,0,f],axis=1)*counts[:,1,b]
        right=counts[:,0,b]*np.prod(counts[:,1,f],axis=1)
        out.append((left-right)/(2*(mu*kappa*q)**((len(f)+1)/2)))
    return np.array(out).T
def simulate(theta,ls,r,w,kappa,mu,N,seed,batch=10000):
    n=len(ls[0]);d=2**n;np_=3*n;rng=np.random.default_rng(seed)
    h=sum((a*mat(s) for a,s in zip(theta,ls)),np.zeros((d,d),complex))
    energy,u=np.linalg.eigh(h);pp=[u.conj().T@p@u for p in ports(n)]
    lo=math.sqrt(mu/w);amp=math.sqrt(kappa*r)/2;per=r/4+lo*lo
    lostp=(1-kappa)*r/(4*per);det=amp*amp+lo*lo;rate=np_*per
    sums=np.zeros(len(ls));sq=sums.copy();cross=np.zeros((len(ls),len(ls)))
    photons=0;maximum=0
    for start in range(0,N,batch):
        size=min(batch,N-start);ne=rng.poisson(rate*2*w,size)
        photons+=int(ne.sum());steps=int(ne.max());maximum=max(maximum,steps)
        tt=rng.random((size,steps))*2*w;tt[np.arange(steps)[None,:]>=ne[:,None]]=np.inf;tt.sort(axis=1)
        init=rng.integers(d,size=size);psi=u.conj().T[:,init].T.copy();last=np.zeros(size)
        counts=np.zeros((size,2,np_),np.int32)
        for j in range(steps):
            ids=np.flatnonzero(ne>j)
            elapsed=tt[ids,j]-last[ids];last[ids]=tt[ids,j]
            psi[ids]*=np.exp(-1j*elapsed[:,None]*energy[None,:])
            choice=rng.integers(np_,size=len(ids));lost=rng.random(len(ids))<lostp
            for port,p in enumerate(pp):
                pick=np.flatnonzero(choice==port)
                if len(pick)==0:continue
                ix=ids[pick];st=psi[ix];ps=st@p.T;il=lost[pick]
                psi[ix[il]]=ps[il];keep=~il
                if not np.any(keep):continue
                ix2=ix[keep];st=st[keep];ps=ps[keep]
                ex=np.einsum('ij,ij->i',st.conj(),ps).real
                prob=(det+2*amp*lo*ex)/(2*det)
                sign=np.where(rng.random(len(ix2))<prob,1,-1)
                new=lo*st+sign[:,None]*amp*ps;new/=np.linalg.norm(new,axis=1)[:,None]
                psi[ix2]=new;win=(tt[ix2,j]>=w).astype(int);counts[ix2,win,port]+=sign
        yy=statistics(counts,ls,mu,kappa,r*w)
        sums+=yy.sum(0);sq+=(yy*yy).sum(0);cross+=yy.T@yy
    mean=sums/N;var=(sq-N*mean*mean)/(N-1);cov=(cross-N*np.outer(mean,mean))/(N-1)
    return mean,np.sqrt(var/N),cov,photons,maximum,rate*2*w
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=100000)
    ap.add_argument('--seed',type=int,default=20261105);ap.add_argument('--r',type=float,default=4)
    ap.add_argument('--w',type=float,default=.25);ap.add_argument('--kappa',type=float,default=.6)
    ap.add_argument('--mu',type=float,default=1);ap.add_argument('--iterations',type=int,default=6)
    ap.add_argument('--output',default='passive_photocount_results.json');args=ap.parse_args();tic=time.perf_counter()
    ls=labels(2,2);truth={'XI':.37,'IY':-.23,'ZZ':.41,'XY':.19,'ZX':-.17}
    theta=np.array([truth.get(s,0.) for s in ls]);y,f,v=response(theta,ls,args.r,args.w)
    yn,fn,_=response(-theta,ls,args.r,args.w)
    slopes=np.array([args.w*c_slope(sum(a!='I' for a in s),args.r*args.w) for s in ls])
    exact_fit=np.zeros_like(theta);exact_errors=[]
    for _ in range(args.iterations):
        z,_,_=response(exact_fit,ls,args.r,args.w);exact_fit+=(y-z)/slopes
        exact_errors.append(float(np.max(np.abs(exact_fit-theta))))
    mean,se,cov,photons,maxevents,expected=simulate(theta,ls,args.r,args.w,args.kappa,args.mu,args.trials,args.seed)
    fitted=np.zeros_like(theta);fit_errors=[]
    for _ in range(args.iterations):
        z,_,_=response(fitted,ls,args.r,args.w);fitted+=(mean-z)/slopes
        fit_errors.append(float(np.max(np.abs(fitted-theta))))
    rows=[{'label':s,'theta':float(theta[j]),'exact_response':float(y[j]),'sample_mean':float(mean[j]),
           'standard_error':float(se[j]),'z_score':float((mean[j]-y[j])/se[j]) if se[j]>0 else None,
           'linear_fit':float(mean[j]/slopes[j]),'nonlinear_fit':float(fitted[j]),'linear_slope':float(slopes[j])}
          for j,s in enumerate(ls)]
    result={'status':'Executed ideal Markov photon-count simulation; not physical data.',
      'scope':'Default r4,w.25 point is not claimed inside the conservative universal inverse certificate. Empirical convergence does not certify global identifiability.',
      'settings':vars(args),'hamiltonian':truth,'labels':ls,'rows':rows,
      'reversal_error':float(np.max(np.abs(v-fn))),'odd_error':float(np.max(np.abs(y+yn))),
      'exact_mean_iteration_errors':exact_errors,'sample_iteration_errors':fit_errors,
      'empirical_covariance':cov.tolist(),'source_and_LO_events':photons,
      'maximum_events_per_block':maxevents,'expected_events_per_block':expected,
      'source_exposure_excluding_burnin_service':2*args.w*args.trials,
      'initialization':'Each simulation starts at I/d; physical preparation requires the separately paid burn-in.',
      'omitted':'No deadtime, timing errors, dark counts, clipping, or physical factories. Efficiency and finite LO are included.',
      'runtime_seconds':time.perf_counter()-tic}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    keys=['reversal_error','odd_error','exact_mean_iteration_errors','sample_iteration_errors','source_and_LO_events','runtime_seconds']
    print(json.dumps({k:result[k] for k in keys},indent=2))
if __name__=='__main__':main()
