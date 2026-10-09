"""Own implementation of Ying 2025 section 3, not author code.
Finite Chebyshev dictionary, truncated SVD eigenmatrix, ESPRIT, coarse/local variance search.
The source leaves several numerical tolerances unspecified: they are explicit here.
"""
import numpy as np
from scipy.optimize import minimize_scalar

def at_variance(z,g,variance,k,support,nc=32,threshold=1e-10):
    # Normalize spectral coordinate to [-1,1] on the given support.
    c=(support[0]+support[1])/2;s=(support[1]-support[0])/2
    zz=(z-c)/s;gg=g*s;tt=variance/s**2;w=zz-tt*gg
    cc=np.cos(np.pi*(np.arange(nc)+.5)/nc)
    B=1/(w[:,None]-cc);B/=np.linalg.norm(B,axis=0)
    U,d,Vh=np.linalg.svd(B,full_matrices=False)
    rank=int(np.sum(d>threshold*d[0]))
    while True:
        keep=np.arange(len(d))<rank
        M=(B*cc)@((Vh[keep].conj().T/d[keep])@U[:,keep].conj().T)
        if np.linalg.norm(M,2)<=3.0 or rank<=k+1:break
        rank-=1
    nl=k+1
    columns=[gg]
    for _ in range(nl):columns.append(M@columns[-1])
    T=np.column_stack(columns)
    _,sv,Vh=np.linalg.svd(T,full_matrices=False)
    Vr=Vh[:k]
    E=Vr[:,1:]@np.linalg.pinv(Vr[:,:-1])
    roots=np.linalg.eigvals(E)
    aa=np.sort(roots.real)*s+c
    ww=np.linalg.lstsq(np.vstack([(1/(z[:,None]-variance*g[:,None]-aa)).real,(1/(z[:,None]-variance*g[:,None]-aa)).imag]),np.r_[g.real,g.imag],rcond=None)[0]
    valid=(np.min(ww)>-1e-6 and np.max(abs(roots.imag))<1e-4)
    return {'variance':variance,'atoms':aa,'weights':ww,'objective':float(np.log(max(sv[k],1e-300))),'valid':valid,'root_imag_max':float(max(abs(roots.imag))),'M_norm':float(np.linalg.norm(M,2)),'dictionary_rank':int(sum(keep))}

def inverse(z,g,k,support,upper,grid_size=61):
    calls=0
    def calc(t):
        nonlocal calls
        calls+=1
        return at_variance(z,g,t,k,support)
    grid=np.linspace(0,upper,grid_size)
    rr=[calc(t) for t in grid]
    valid=[i for i,r in enumerate(rr) if r['valid']]
    if not valid: raise RuntimeError('No positive real spectral reconstruction on baseline grid')
    local=[]
    for i in valid:
        v=rr[i]['objective']
        if (i==0 or v<=rr[i-1]['objective']) and (i==len(rr)-1 or v<=rr[i+1]['objective']):local.append(i)
    if not local:local=[min(valid,key=lambda i:rr[i]['objective'])]
    for i in sorted(local,key=lambda i:rr[i]['objective'])[:5]:
        def obj(t):
            r=calc(t)
            return r['objective'] if r['valid'] else 1e10
        fit=minimize_scalar(obj,bounds=(grid[max(0,i-1)],grid[min(len(grid)-1,i+1)]),method='bounded',options={'xatol':1e-9})
        rr.append(calc(float(fit.x)))
    best=min((r for r in rr if r['valid']),key=lambda r:r['objective'])
    best['calls']=calls
    return best

if __name__=='__main__':
    from pick_inverse import free_stieltjes
    for k in [3,5]:
        a=np.array([-1,.2,1]) if k==3 else np.linspace(-1,1,k)
        p=np.array([.25,.5,.25]) if k==3 else np.ones(k)/k
        theta=np.pi*(np.arange(32)+.5)/32
        z=3.0*np.cos(theta)+1.5j*np.sin(theta);z=np.r_[z,z.conj()]
        gu=free_stieltjes(z[:32],a,p,.5625);g=np.r_[gu,gu.conj()]
        r=inverse(z,g,k,(-2.6,2.6),1.5)
        print(k,r)
