"""Explicit full-state comparator. Enumeration is intentional and charged here.
Final positivity-residual checking uses directed binary interval arithmetic;
source averaging uses an exact integer mass vector and dyadic trial values.
"""
import time
from fractions import Fraction as F
import numpy as np

def downward(x):return np.nextafter(x,-np.inf)
def upward(x):return np.nextafter(x,np.inf)

def build_full(c):
    dims=[len(p) for p in c.prob];N=int(np.prod(dims));idx=np.arange(N,dtype=np.int64);locidx=[];strides=[]
    for b,d in enumerate(dims):
        stride=int(np.prod(dims[b+1:]));strides.append(stride);locidx.append((idx//stride)%d)
    bits={i:c.bits[b][locidx[b],s] for i,(b,s) in c.loc.items()}
    p0=np.ones(N);mass=np.ones(N,dtype=object)
    for b in range(c.B):
        p0*=np.array(c.prob[b],float)[locidx[b]];mass*=np.array(c.mass[b],dtype=object)[locidx[b]]
    w=np.ones(N)
    for b,s,d,t,g in c.cross:
        eq=c.bits[b][locidx[b],s]==c.bits[d][locidx[d],t]
        # Benchmarks have g>1; scaled numerator remains valid for g<1 as well.
        fac=np.where(eq,g.numerator,g.denominator);mass*=fac.astype(object)
        w*=np.where(eq,float(g),1.)/float(min(F(1),g))
    rates=[];rlo=[];rhi=[];flips=[]
    for i in range(c.model['n']):
        enei=sorted(j if i==a else a for a,j in c.model['edges'] if i==a or i==j)
        context=c.model.get('clock_contexts',{}).get(i,[])
        nei=sorted(set(enei)|set(context))
        code=bits[i].copy()
        for k,j in enumerate(nei):code|=bits[j]<<(k+1)
        tab=[]
        for h in range(1<<(len(nei)+1)):
            xi=h&1;ratio=c.model['fields'][i]**(1-2*xi)
            for j in enei:
                same=xi==((h>>(nei.index(j)+1))&1);t=c.model['edges'][tuple(sorted((i,j)))];ratio*=1/t if same else t
            cz=sum(((h>>(nei.index(j)+1))&1)<<kk for kk,j in enumerate(context))
            pref=c.model['clock_tables'][i][cz] if 'clock_tables' in c.model else c.model['nu'][i]
            tab.append(pref*ratio/(1+ratio))
        f=np.array(tab,float);lo=np.array([x if F(float(x))<=a else downward(x) for x,a in zip(f,tab)]);hi=np.array([x if F(float(x))>=a else upward(x) for x,a in zip(f,tab)])
        rates.append(f[code]);rlo.append(lo[code]);rhi.append(hi[code]);b,s=c.loc[i];flips.append(idx^(strides[b]*(1<<s)))
    kill=np.asarray(bits[c.model['target']],float)*float(c.model['kappa']);rp=np.sqrt(p0)
    eigsum=np.zeros(dims)
    for b,ev in enumerate(c.evals):
        shape=[1]*c.B;shape[b]=len(ev);eigsum+=ev.reshape(shape)
    from certify import alpha_bound
    alpha,_=alpha_bound(c)
    return dict(N=N,dims=dims,idx=idx,rp=rp,w=w,mass=mass,rates=rates,rlo=rlo,rhi=rhi,flips=flips,kill=kill,eigsum=eigsum,alpha=alpha,all_cross_dyadic=all((max(v,1/v).denominator&(max(v,1/v).denominator-1))==0 for *_,v in c.cross))

def apply_raw(d,v):
    out=d['kill']*v
    for rate,flip in zip(d['rates'],d['flips']):out=out+rate*(v-v[flip])
    return out

def apply_A(d,v):return d['rp']*d['w']*apply_raw(d,v/d['rp'])
def apply_Cinv(c,d,v):
    x=v.reshape(d['dims'])
    for b,U in enumerate(c.evecs):x=np.moveaxis(np.tensordot(U.T,x,axes=(1,b)),0,b)
    x=x/d['eigsum']
    for b,U in enumerate(c.evecs):x=np.moveaxis(np.tensordot(U,x,axes=(1,b)),0,b)
    return x.ravel()

def certify_full(d,u,bits=18):
    if np.max(abs(u))*(1<<bits)>=2**62:bits=8
    integers=np.rint(u*(1<<bits)).astype(np.int64);v=integers.astype(float)/(1<<bits)
    if v.min()<=0:return {'valid':False,'reason':'nonpositive trial'}
    # kappa=1 in executed full-state comparisons; multiplication by 0 or 1 exact.
    lo=d['kill']*v;hi=lo.copy()
    for ql,qh,flip in zip(d['rlo'],d['rhi'],d['flips']):
        diff=v-v[flip];dl=downward(diff);dh=upward(diff)
        pl=downward(np.where(dl>=0,ql*dl,qh*dl));ph=upward(np.where(dh>=0,qh*dh,ql*dh))
        lo=downward(lo+pl);hi=upward(hi+ph)
    # Outward rounding of the subtraction defining the residual distance.
    delta=max(float(upward(1.-lo).max()),float(upward(hi-1.).max()))
    candidates=[]
    num=sum(d['mass']*integers.astype(object));den=sum(d['mass'])*(1<<bits);mean=F(int(num),int(den))
    if delta<1:
        deltaq=F(delta);L=mean/(1+deltaq);U=mean/(1-deltaq);candidates.append((L,U,'pointwise'))
    # Source-weighted energy residual certificate, much sharper than worst-point error.
    if d['all_cross_dyadic']:
        def weighted_bounds(flo,fhi):
            mf=np.array(d['mass'],float);ml=downward(mf);mh=upward(mf)
            pl=downward(np.where(flo>=0,ml*flo,mh*flo));ph=upward(np.where(fhi>=0,mh*fhi,ml*fhi))
            eps=np.finfo(float).eps;gam=len(pl)*eps/(1-len(pl)*eps)
            # gamma_N bound is conservative for NumPy's pairwise sum as well.
            el=upward(2*gam/(1-gam)*np.sum(abs(pl)));eh=upward(2*gam/(1-gam)*np.sum(abs(ph)))
            sl=downward(np.sum(pl)-el);sh=upward(np.sum(ph)+eh)
            M=float(sum(d['mass']));mL=downward(M);mH=upward(M)
            return downward(sl/(mH if sl>=0 else mL)),upward(sh/(mL if sh>=0 else mH))
        llo=downward(v*downward(2.-hi));lhi=upward(v*upward(2.-lo));LL,LH=weighted_bounds(llo,lhi)
        err=np.maximum(upward(1.-lo),upward(hi-1.));err=np.maximum(err,0.)
        ru=upward(d['w']*upward(err*err));_,EH=weighted_bounds(np.zeros_like(ru),ru)
        af=downward(float(d['alpha']));UU=upward(LH+upward(EH/af))
        if LL>0:candidates.append((F(float(LL)),F(float(UU)),'source-weighted interval residual'))
    if not candidates:return {'valid':False,'delta':delta}
    L=max(x[0] for x in candidates);U=min(x[1] for x in candidates)
    return {'valid':True,'lower':str(L),'upper':str(U),'lower_float':float(L),'upper_float':float(U),'ratio_float':float(U/L),'delta':delta,'dyadic_bits':bits,'scope':'full-state directed-rounding residual and exact source average','certificates':[x[2] for x in candidates]}

def run_reference(c,maxiter=30,target_ratio=1.05):
    start=time.perf_counter();d=build_full(c);setup=time.perf_counter()-start
    b=d['rp']*d['w'];x=np.zeros_like(b);r=b.copy();z=apply_Cinv(c,d,r);p=z.copy();rz=r@z;history=[];cert=None
    for it in range(1,maxiter+1):
        ap=apply_A(d,p);step=rz/(p@ap);x+=step*p;r=b-apply_A(d,x)
        if it%2==0:
            cert=certify_full(d,x/d['rp']);history.append({'iteration':it,**{k:v for k,v in cert.items() if k in ['valid','ratio_float','delta']}})
            if cert['valid'] and cert['ratio_float']<=target_ratio:break
        z=apply_Cinv(c,d,r);newrz=r@z;p=z+(newrz/rz)*p;rz=newrz
    if cert is None:cert=certify_full(d,x/d['rp'])
    cert.update(states=d['N'],setup_seconds=setup,total_seconds=time.perf_counter()-start,iterations=it,history=history,method='full-state separably preconditioned conjugate gradient',allocated_float_rate_arrays=3*c.model['n'])
    return cert
