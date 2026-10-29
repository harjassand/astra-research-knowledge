"""Scalar survival-only COMMON-BARRIER gateway tomography. No hidden matrices passed to receivers.
Standard Hankel identification is credited; construction is a model test, not a device.
"""
import json, itertools, time
import numpy as np
from scipy.linalg import expm, logm
from scipy.optimize import least_squares

class Instrument:
    def __init__(self,K,c,p,s,x=(0.6,1.8),tau=.35):
        self.K=np.asarray(K); self.c=np.asarray(c); self.p=np.asarray(p); self.s=s
        self.x=x; self.tau=tau
        self.M=[expm(tau*(self.K-xx*np.diag(self.c))) for xx in x]
        self.calls=0
    def survival(self,w):
        self.calls+=1; r=self.p.copy()
        for a in w:r=r@self.M[a]
        return float(r.sum())
    def gateway_survival(self,t):
        self.calls+=1; return float(np.exp(-self.s*self.x[0]*t))

def query_data(instrument,m):
    words={tuple([0]*k) for k in range(2*m)}
    words|={tuple([0]*i+[1]+[0]*j) for i in range(m) for j in range(m)}
    return {w:instrument.survival(w) for w in sorted(words,key=lambda z:(len(z),z))}

def recover(data,m,x,tau,s):
    def h(w):return data[tuple(w)]
    H=np.array([[h([0]*(i+j)) for j in range(m)] for i in range(m)])
    A=[]
    for a in range(2):
        Ha=np.array([[h([0]*i+[a]+[0]*j) for j in range(m)] for i in range(m)])
        A.append(np.linalg.solve(H,Ha))
    L=[logm(aa)/tau for aa in A]
    D=(L[0]-L[1])/(x[1]-x[0])
    c,V=np.linalg.eig(D)
    order=np.argsort(c.real);c=c[order];V=V[:,order]
    b=np.linalg.solve(H,np.array([h([0]*i) for i in range(m)]))
    scales=np.linalg.solve(V,b);S=V@np.diag(scales)
    K=np.linalg.solve(S,L[0]@S)+x[0]*np.diag(c)
    p=np.array([h([0]*j) for j in range(m)])@S
    imag=max(np.max(abs(K.imag)),np.max(abs(c.imag)),np.max(abs(p.imag)))
    return K.real,c.real,p.real,dict(hankel_min_sv=float(np.linalg.svd(H)[1][-1]),hankel_cond=float(np.linalg.cond(H)),imag=float(imag))

def fullQ(K,c,p,s):
    m=len(c);Q=np.zeros((m+1,m+1));Q[0,1:]=s*p;Q[1:,0]=c;Q[1:,1:]=K-np.diag(c);Q[0,0]=-s
    return Q

def entropy(Q):
    A=Q.T.copy();A[-1,:]=1;b=np.zeros(len(Q));b[-1]=1;pi=np.linalg.solve(A,b)
    ep=0.
    for i in range(len(Q)):
        for j in range(i+1,len(Q)):
            a=pi[i]*Q[i,j];b=pi[j]*Q[j,i]
            if a>0 and b>0:ep+=(a-b)*np.log(a/b)
    return float(ep)

def fit_rates(data,m,x,tau,s,init,counts=None):
    inds=[(i,j) for i in range(m) for j in range(m) if i!=j]
    def unpack(z):
        K=np.zeros((m,m))
        for k,(i,j) in enumerate(inds):K[i,j]=np.exp(z[k])
        np.fill_diagonal(K,-K.sum(axis=1))
        c=np.exp(z[len(inds):len(inds)+m]);p=np.exp(z[-m:]-max(z[-m:]));p/=p.sum()
        return K,c,p
    def residual(z):
        K,c,p=unpack(z);M=[expm(tau*(K-xx*np.diag(c))) for xx in x];r=[]
        for w,y in data.items():
            if not w:continue
            v=p
            for a in w:v=v@M[a]
            pred=float(v.sum());weight=1/max(.02,np.sqrt(y*(1-y)))
            r.append((pred-y)*weight)
        return r
    z=least_squares(residual,init,max_nfev=3000,xtol=1e-12,gtol=1e-12,ftol=1e-12)
    return (*unpack(z.x),float(np.linalg.norm(z.fun)),int(z.nfev))

def aligned_error(K,c,p,K0,c0,p0):
    m=len(c)
    return min(float(np.linalg.norm(K[np.ix_(perm,perm)]-K0)+np.linalg.norm(c[list(perm)]-c0)+np.linalg.norm(p[list(perm)]-p0)) for perm in itertools.permutations(range(m)))

def exact_three_state():
    from fractions import Fraction as F
    a,b,c,d,e,f=map(F,[2,1,1,3,4,2]);s=a+b
    Cs=[];Ps=[];Rs=[]
    for x in [F(1),F(2)]:
        Cs.append((c+e)*x+d+f);Ps.append(c*e*x*x+(c*f+d*e)*x);Rs.append((a*c+b*e)/s*x)
    C=Cs[1]-Cs[0];D=Cs[0]-C;P=Ps[1]/2-Ps[0];Q=Ps[0]-P;R=Rs[0]
    # Here using x as killing scale, inverse of old one-parameter notation.
    disc=C*C-4*P
    assert disc==9
    cc=(C-F(3))/2;ee=(C+F(3))/2
    aa=s*(R-ee)/(cc-ee);bb=s-aa;dd=(Q-cc*D)/(ee-cc);ff=D-dd
    assert [aa,bb,cc,dd,ee,ff]==[a,b,c,d,e,f]
    return {"rates_recovered":list(map(str,[aa,bb,cc,dd,ee,ff])),"coefficient_data":list(map(str,Cs+Ps+Rs)),"exact_fraction_assertions":"PASS"}

def main():
    rng=np.random.default_rng(20261029)
    K=np.array([[-.8,.6,.2],[.15,-.85,.7],[.5,.1,-.6]])
    c=np.array([.25,1.5,4.]);p=np.array([.25,.4,.35]);s=1.7;m=3;x=(.6,1.8);tau=.35
    ins=Instrument(K,c,p,s,x,tau);data=query_data(ins,m)
    sq=-np.log(ins.gateway_survival(tau))/(tau*x[0])
    kh,ch,ph,diag=recover(data,m,x,tau,sq)
    out={"exact_three_state":exact_three_state(),"settings":len(data),"max_intervals":max(map(len,data)),"scalar_instrument_calls":ins.calls,"exact_probability_receiver":{"aligned_parameter_error":aligned_error(kh,ch,ph,K,c,p),"entropy_true":entropy(fullQ(K,c,p,s)),"entropy_recovered":entropy(fullQ(kh,ch,ph,sq)),**diag},"bounded_error_sweep":[],"sampling_comparison":[]}
    for eta in [1e-12,1e-10,1e-8,1e-6]:
        noisy={w:(v if not w else float(np.clip(v+rng.uniform(-eta,eta),0,1))) for w,v in data.items()}
        try:
            kk,cc,pp,dd=recover(noisy,m,x,tau,sq)
            out['bounded_error_sweep'].append({"eta":eta,"aligned_error":aligned_error(kk,cc,pp,K,c,p),**dd,"minimum_offdiagonal":float(min(kk[i,j] for i in range(m) for j in range(m) if i!=j)),"minimum_probability":float(pp.min())})
        except Exception as e:out['bounded_error_sweep'].append({"eta":eta,"error":str(e)})
    # Equally informed conventional positive fitting, no true parameters used in initializer.
    for N in [100_000,10_000_000]:
        noisy={w:(1. if not w else float(rng.binomial(N,v)/N)) for w,v in data.items()}
        rec={"trials_per_setting":N,"total_excursions":N*(len(data)-1)}
        try:
            kk,cc,pp,dd=recover(noisy,m,x,tau,sq)
            rec['spectral']={"aligned_error":aligned_error(kk,cc,pp,K,c,p),"imag":dd['imag'],"minimum_probability":float(pp.min()),"minimum_offdiagonal":float(min(kk[i,j] for i in range(m) for j in range(m) if i!=j))}
        except Exception as e:rec['spectral']={"error":str(e)}
        st=time.perf_counter();fits=[]
        for seed in range(3):
            r=np.random.default_rng(seed);init=r.normal(0,.5,m*(m-1)+2*m)
            fits.append(fit_rates(noisy,m,x,tau,sq,init))
        best=min(fits,key=lambda z:z[-2]);kk,cc,pp,loss,neval=best
        rec['ordinary_positive_fit']={"aligned_error":aligned_error(kk,cc,pp,K,c,p),"residual":loss,"nfev":neval,"runtime_seconds":time.perf_counter()-st,"entropy":entropy(fullQ(kk,cc,pp,sq))}
        out['sampling_comparison'].append(rec)
    # Equal killing no-go: hidden 3-cycle equilibrium versus dissipative cycle.
    records=[]
    for u,v in [(1,1),(20,.05)]:
        kk=np.array([[-u-v,u,v],[v,-u-v,u],[u,v,-u-v]])
        inst=Instrument(kk,np.ones(3),np.ones(3)/3,1.,x,tau)
        ww=(0,1,1,0,1)
        records.append({"u":u,"v":v,"survival":inst.survival(ww),"closed_form":float(np.exp(-tau*sum(x[a] for a in ww))),"entropy":entropy(fullQ(kk,np.ones(3),np.ones(3)/3,1.))})
    out['equal_hazard_no_go']=records
    # A physical degree-one gateway: similarity acts only in hidden zero-hazard sector.
    import sympy as sp
    Kexact=sp.Matrix([[-3,1,2],[1,-4,3],[2,3,-5]])
    Sexact=sp.Matrix([[1,0,0],[0,sp.Rational(11,10),sp.Rational(-1,10)],[0,0,1]])
    Knew=Sexact.inv()*Kexact*Sexact
    dexact=sp.diag(1,0,0)
    assert Sexact*sp.ones(3,1)==sp.ones(3,1)
    assert Sexact*dexact==dexact*Sexact
    assert sp.Matrix([[1,0,0]])*Sexact==sp.Matrix([[1,0,0]])
    assert Knew*sp.ones(3,1)==sp.zeros(3,1)
    assert all(Knew[i,j]>0 for i in range(3) for j in range(3) if i!=j)
    cyc=sp.cancel(Knew[0,1]*Knew[1,2]*Knew[2,0]/(Knew[0,2]*Knew[2,1]*Knew[1,0]))
    assert cyc!=1
    ki=np.array(Kexact).astype(float);kj=np.array(Knew).astype(float)
    ii=Instrument(ki,np.array([1.,0,0]),np.array([1.,0,0]),1.,x,tau)
    jj=Instrument(kj,np.array([1.,0,0]),np.array([1.,0,0]),1.,x,tau)
    words=[tuple(w) for n in range(7) for w in itertools.product([0,1],repeat=n)]
    out['degree_one_gateway_no_go']={"K_equilibrium":[list(map(str,Kexact.row(i))) for i in range(3)],"K_nonequilibrium":[list(map(str,Knew.row(i))) for i in range(3)],"cycle_affinity_ratio":str(cyc),"entropy_equilibrium":entropy(fullQ(ki,ii.c,ii.p,1.)),"entropy_nonequilibrium":entropy(fullQ(kj,jj.c,jj.p,1.)),"127_word_max_discrepancy":max(abs(ii.survival(w)-jj.survival(w)) for w in words),"exact_similarity_assertions":"PASS"}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
