"""Finite-density four-site transport: floating discovery, exact rational residual check.
All input matrices in the verifier are integer numerators over a common denominator.
No floating singular value or optimizer tolerance is a certificate premise.
"""
from __future__ import annotations
import os, json, time, itertools, math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import inv

ROOT_BITS=52; ROOT_DEN=1<<ROOT_BITS; ROOT_NUM=math.isqrt(3*ROOT_DEN*ROOT_DEN)
ADEN=2400*ROOT_DEN
XBITS=44; XDEN=1<<XBITS; RBITS=42; RDEN=1<<RBITS
PARS=(F(1,25),)*4+(F(1,4096),F(1,4096)) # UL,UR,W,Z, phase error, drain error
NQ=4; D=16
pairs=[(a,b) for b in range(D) for a in range(D) if a.bit_count()==b.bit_count()]
lookup={ab:i for i,ab in enumerate(pairs)}; DIM=len(pairs)
occ=lambda a,i:(a>>(3-i))&1
zero=(0,)*6

def indices(K):
    out=[]
    def rec(rem,m,prefix):
        if m==1:out.append(tuple(prefix+[rem]));return
        for j in range(rem+1):rec(rem-j,m-1,prefix+[j])
    for degree in range(K+1):rec(degree,6,[])
    return out

def mono_radius(a):
    v=F(1)
    for r,n in zip(PARS,a):v*=r**n
    return v

def ceil_sqrt(q:F,bits=44)->F:
    if q<0: raise ValueError('negative squared norm')
    den=1<<bits
    a=q.numerator*den*den//q.denominator
    k=math.isqrt(a)
    if F(k*k,den*den)<q:k+=1
    return F(k,den)

def norm_int(r,i,den):
    ss=sum(int(a)**2+int(b)**2 for a,b in zip(r.flat,i.flat))
    return ceil_sqrt(F(ss,den*den))

def build_H(kind,m=0):
    hr=np.zeros((D,D),object);hi=np.zeros((D,D),object)
    if m==0:
        for a in range(D):
            ns=[occ(a,j) for j in range(4)]
            hr[a,a]=ADEN*(4*ns[0]*(ns[1]+ns[2])+3*ns[3]*(ns[1]+ns[2])+ns[1]*ns[2]+2*ns[0]*ns[3])
    zr=F(-1) if kind=='bad' else F(1,2)
    zi=F(0) if kind=='bad' else F(ROOT_NUM,2*ROOT_DEN)
    c=complex(0,1)**m
    zmr=(zr*int(c.real)-zi*int(c.imag))/math.factorial(m)
    zmi=(zr*int(c.imag)+zi*int(c.real))/math.factorial(m)
    for u,v in [(0,1),(0,2),(1,3),(2,3)]:
        if m and (u,v)!=(1,3):continue
        ar,ai=(zmr,zmi) if (u,v)==(1,3) else (F(1),F(0))
        assert (ar*ADEN).denominator==(ai*ADEN).denominator==1
        ar=int(ar*ADEN);ai=int(ai*ADEN)
        for a in range(D):
            if occ(a,u)==0 and occ(a,v)==1:
                b=a^(1<<(3-u))^(1<<(3-v))
                hr[b,a]-=ar;hi[b,a]-=ai
                hr[a,b]-=ar;hi[a,b]+=ai
    return hr,hi

def comm(Hr,Hi):
    R=np.zeros((DIM,DIM),object);I=np.zeros((DIM,DIM),object)
    for col,(c,e) in enumerate(pairs):
        for a in range(D):
            row=lookup.get((a,e))
            if row is not None:
                R[row,col]+=Hi[a,c];I[row,col]-=Hr[a,c]
        for b in range(D):
            row=lookup.get((c,b))
            if row is not None:
                R[row,col]-=Hi[e,b];I[row,col]+=Hr[e,b]
    return R,I

def drain():
    R=np.zeros((DIM,DIM),object);I=np.zeros((DIM,DIM),object)
    for col,(a,b) in enumerate(pairs):
        R[col,col]-=ADEN*(occ(a,3)+occ(b,3))//2
        if occ(a,3) and occ(b,3):R[lookup[a^1,b^1],col]+=ADEN
    R[0,:]=0;return R,I

def matrices(kind,kappa):
    R,I=comm(*build_H(kind,0))
    Dr,Di=drain()
    # Drain() has zero trace-replacement row, before imposing normalization.
    for col,(a,b) in enumerate(pairs):
        R[col,col]-=ADEN*(a^b).bit_count()//200
        R[col,col]-=ADEN*((1-occ(a,0))+(1-occ(b,0)))//5
        if not occ(a,0) and not occ(b,0):R[lookup[a^8,b^8],col]+=ADEN*2//5
    R+=kappa*Dr
    # Missing original drain row is overwritten by the trace equation.
    R[0,:]=0;I[0,:]=0
    for col,(a,b) in enumerate(pairs):
        if a==b:R[0,col]=ADEN
    terms=[]
    funcs=[lambda n:n[0]*(n[1]+n[2]),lambda n:n[3]*(n[1]+n[2]),lambda n:n[1]*n[2],lambda n:n[0]*n[3]]
    for j,fn in enumerate(funcs):
        vals=[fn([occ(a,l) for l in range(4)]) for a in range(D)]
        rr=np.zeros((DIM,DIM),object);ii=np.zeros((DIM,DIM),object)
        for col,(a,b) in enumerate(pairs):ii[col,col]=-ADEN*(vals[a]-vals[b])
        ii[0,:]=0;beta=list(zero);beta[j]=1;terms.append((tuple(beta),rr,ii))
    for m in range(1,5):
        rr,ii=comm(*build_H(kind,m));rr[0,:]=0;ii[0,:]=0
        beta=list(zero);beta[4]=m;terms.append((tuple(beta),rr,ii))
    beta=list(zero);beta[5]=1;terms.append((tuple(beta),Dr,Di))
    return R,I,terms

def sparse(r,i):
    return [(a,b,int(r[a,b]),int(i[a,b])) for a in range(r.shape[0]) for b in range(r.shape[1]) if r[a,b] or i[a,b]]

def exact_matvec(entries,xr,xi):
    rr=[0]*DIM;ii=[0]*DIM
    for a,b,ar,ai in entries:
        br=int(xr[b]);bi=int(xi[b]);rr[a]+=ar*br-ai*bi;ii[a]+=ar*bi+ai*br
    return rr,ii

def exact_RA(Rr,Ri,entries):
    rr=[[0]*DIM for _ in range(DIM)];ii=[[0]*DIM for _ in range(DIM)]
    for a,b,ar,ai in entries:
        for k in range(DIM):
            br=int(Rr[k,a]);bi=int(Ri[k,a]);rr[k][b]+=br*ar-bi*ai;ii[k][b]+=br*ai+bi*ar
    return rr,ii

def fstr(x):return str(x.numerator)+'/'+str(x.denominator)

def run_case(kind,kappa,K=6,folder=None,witness=None):
    st=time.perf_counter();Ari,Aii,terms=matrices(kind,kappa)
    inds=indices(K);idx={a:i for i,a in enumerate(inds)}
    if witness is None:
        A=np.asarray(Ari,float)/ADEN+1j*np.asarray(Aii,float)/ADEN
        R=inv(A); b=np.zeros(DIM);b[0]=1
        tf=[(beta,np.asarray(ar,float)/ADEN+1j*np.asarray(ai,float)/ADEN) for beta,ar,ai in terms]
        x=np.zeros((len(inds),DIM),complex)
        for j,a in enumerate(inds):
            if a==zero:x[j]=R@b;continue
            rhs=np.zeros(DIM,complex)
            for beta,M in tf:
                if all(v<=u for u,v in zip(a,beta)):
                    aa=tuple(u-v for u,v in zip(a,beta));rhs-=M@x[idx[aa]]
            x[j]=R@rhs
        if max(np.max(np.abs(x.real)),np.max(np.abs(x.imag)))*XDEN >= 2**62:
            raise OverflowError('trial quantization exceeds supported integer range')
        if max(np.max(np.abs(R.real)),np.max(np.abs(R.imag)))*RDEN >= 2**62:
            raise OverflowError('inverse quantization exceeds supported integer range')
        xr=np.rint(x.real*XDEN).astype(np.int64);xi=np.rint(x.imag*XDEN).astype(np.int64)
        Rr=np.rint(R.real*RDEN).astype(np.int64);Ri=np.rint(R.imag*RDEN).astype(np.int64)
    else:
        dat=np.load(witness,allow_pickle=False)
        xr,xi,Rr,Ri=[dat[k] for k in ['xr','xi','Rr','Ri']]
        if list(map(tuple,dat['indices'].tolist())) != inds:raise ValueError('wrong polynomial index set')
        if any(a.dtype.kind not in 'iu' for a in [xr,xi,Rr,Ri]):raise ValueError('witness arrays must be integers')
        if xr.shape != (len(inds),DIM) or xi.shape!=xr.shape or Rr.shape!=(DIM,DIM) or Ri.shape!=Rr.shape:
            raise ValueError('wrong certificate dimensions')
    # Exact left-inverse residual and norm; perturbed denominators never unit cost.
    e0=sparse(Ari,Aii);rr,ii=exact_RA(Rr,Ri,e0)
    for j in range(DIM):rr[j][j]-=RDEN*ADEN
    eta0=norm_int(np.array(rr,object),np.array(ii,object),RDEN*ADEN)
    Rnorm=norm_int(Rr,Ri,RDEN)
    # Joint nuisance perturbation: Frobenius norm at all 16 vertices.
    colnorm=[sum(int(Rr[i,j])**2+int(Ri[i,j])**2 for i in range(DIM)) for j in range(DIM)]
    diag=[ [int(ai[j,j]//ADEN) for j in range(DIM)] for _,ar,ai in terms[:4]]
    q2=F(0)
    for signs in itertools.product([-1,1],repeat=4):
        ds=[sum(signs[l]*diag[l][j] for l in range(4)) for j in range(DIM)]
        z=F(sum(ds[j]**2*colnorm[j] for j in range(DIM)),RDEN*RDEN)*PARS[0]**2
        q2=max(q2,z)
    q=ceil_sqrt(q2)
    qextra=F(0)
    for beta,ar,ai in terms[4:]:
        rr,ii=exact_RA(Rr,Ri,sparse(ar,ai))
        qextra+=norm_int(np.array(rr,object),np.array(ii,object),RDEN*ADEN)*mono_radius(beta)
    # sqrt(3) surrogate and phase Taylor tail: Hilbert-space superoperator norm.
    root_err=F(2,ROOT_DEN) # safely bounds generator error for e^(i phi) phase values
    phase_tail=F(4)*PARS[4]**5/F(math.factorial(5)) # exp(|delta|)<2
    a_error=root_err+phase_tail
    qtotal=eta0+q+qextra+Rnorm*a_error
    if qtotal>=1:raise ValueError(f'Neumann certificate failed: {float(qtotal)}')
    invbound=Rnorm/(1-qtotal)
    # Build complete residual polynomial, including every output above trial degree.
    residual={}
    def add(key,r,i):
        if key not in residual:residual[key]=[[0]*DIM,[0]*DIM]
        v,w=residual[key]
        for j in range(DIM):v[j]+=r[j];w[j]+=i[j]
    ts=[(beta,sparse(ar,ai)) for beta,ar,ai in terms]
    for j,a in enumerate(inds):
        rr,ii=exact_matvec(e0,xr[j],xi[j]);add(a,rr,ii)
        for beta,es in ts:
            aa=tuple(u+v for u,v in zip(a,beta));rr,ii=exact_matvec(es,xr[j],xi[j]);add(aa,rr,ii)
    residual[zero][0][0]-=ADEN*XDEN
    resbound=F(0);statebound=F(0)
    for a,(rr,ii) in residual.items():
        resbound+=norm_int(np.array(rr,object),np.array(ii,object),ADEN*XDEN)*mono_radius(a)
    for j,a in enumerate(inds):statebound+=norm_int(xr[j],xi[j],XDEN)*mono_radius(a)
    resbound+=a_error*statebound
    # exact objective polynomial, including changed drain coefficient
    coef={}
    targets=[j for j,(a,b) in enumerate(pairs) if a==b and occ(a,3)]
    for j,a in enumerate(inds):
        val=F(sum(int(xr[j,l]) for l in targets),XDEN)
        coef[a]=coef.get(a,F(0))+kappa*val
        aa=list(a);aa[5]+=1;aa=tuple(aa);coef[aa]=coef.get(aa,F(0))+val
    error=3*(kappa+PARS[5])*invbound*resbound
    span=sum(abs(v)*mono_radius(a) for a,v in coef.items() if a!=zero)
    center=coef[zero];low=center-span-error;high=center+span+error
    actuation=sum(abs(v)*mono_radius(a) for a,v in coef.items() if a[4]+a[5]>0)+2*error
    if folder:
        folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(folder/f'{kind}_{kappa}_witness.npz',xr=xr,xi=xi,Rr=Rr,Ri=Ri,indices=np.array(inds,dtype=np.int16))
    rec={'kind':kind,'kappa':kappa,'degree':K,'dimension':DIM,'trial_coefficients':len(inds),
         'q':fstr(qtotal),'inverse_bound':fstr(invbound),'residual':fstr(resbound),'error':fstr(error),
         'lower':fstr(low),'upper':fstr(high),'actuation_allowance':fstr(actuation),
         'center':fstr(center),'coefficient_polynomial':{','.join(map(str,a)):fstr(v) for a,v in coef.items()},
         'seconds':time.perf_counter()-st,'root_interval':[f'{ROOT_NUM}/{ROOT_DEN}',f'{ROOT_NUM+1}/{ROOT_DEN}']}
    if folder:(folder/f'{kind}_{kappa}.json').write_text(json.dumps(rec,indent=2))
    print(kind,kappa,'q',float(qtotal),'error',float(error),'interval',[float(low),float(high)],'act',float(actuation),'seconds',rec['seconds'],flush=True)
    return rec

if __name__=='__main__':
    import argparse
    pa=argparse.ArgumentParser();pa.add_argument('--degree',type=int,default=6);pa.add_argument('--output',default='results');args=pa.parse_args()
    records=[run_case(kind,k,args.degree,args.output) for k in [2,4,8] for kind in ['bad','good']]
    Path(args.output,'all_cases.json').write_text(json.dumps(records,indent=2))
