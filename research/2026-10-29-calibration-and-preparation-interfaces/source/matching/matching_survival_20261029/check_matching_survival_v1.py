#!/usr/bin/env python3
"""Deterministic numerical checks; not a floating-point proof certificate."""
import json, math, hashlib, pathlib
import numpy as np
from scipy.linalg import eigh, expm
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parent
RNG=np.random.default_rng(202610290405)
def matchings(vertices):
    if not vertices:
        yield (); return
    a=vertices[0]
    for k in range(1,len(vertices)):
        b=vertices[k]
        for tail in matchings(vertices[1:k]+vertices[k+1:]):
            yield ((a,b),)+tail

def partitions(n, maxpart=None, maxlen=None):
    if n==0:
        yield (); return
    if maxlen==0:return
    for p in range(min(n,maxpart or n),0,-1):
        for tail in partitions(n-p,p,None if maxlen is None else maxlen-1):
            yield (p,)+tail

def zprod(lam):
    return math.prod(4+2*j-i-1 for i,l in enumerate(lam,1) for j in range(1,l+1))
def hooks_dimension(lam):
    h=math.prod(lam[i]-j+sum(k>i and lam[k]>j for k in range(len(lam)))
                for i in range(len(lam)) for j in range(lam[i]))
    return math.factorial(sum(lam))//h

def state(n,M):
    v=np.zeros(2**n)
    for choice in range(2**len(M)):
        ix=0; s=1
        for k,(a,b) in enumerate(M):
            rev=(choice>>k)&1
            ix|=1<<(a if rev else b)
            if rev:s=-s
        v[ix]=s/np.sqrt(2**len(M))
    return v

def loops(n,M,N):
    par=list(range(n))
    def find(x):
        while par[x]!=x:
            par[x]=par[par[x]];x=par[x]
        return x
    for a,b in M+N:
        par[find(a)]=find(b)
    return len({find(a) for a in range(n)})

def random_isometry(a,b):
    x=RNG.normal(size=(a,b))+1j*RNG.normal(size=(a,b))
    q,r=np.linalg.qr(x)
    q*=np.diag(r).conj()/np.maximum(np.abs(np.diag(r)),1e-300)
    return q

out={'seed':202610290405,'status':'author checks, not independent review','spectra':[],
     'partition_order':[], 'cptp_cases':[], 'sharpness':[]}
for m in range(2,61):
    top=zprod((m,)); sec=zprod((m-1,1)); count=0
    assert Fraction(sec,top)==Fraction(3,2*m+2)
    for p in partitions(m,maxlen=4):
        val=zprod(p); assert val>0
        assert val<=top and (p==(m,) or val<=sec)
        count+=1
    out['partition_order'].append({'n':2*m,'partitions_le4':count,'ratio':str(Fraction(sec,top))})
for n in (4,6,8,10):
    m=n//2; d=math.comb(n,m)//(m+1)
    Ms=list(matchings(tuple(range(n)))); L=len(Ms)
    V=np.column_stack([state(n,M) for M in Ms]); overlap=V.T@V
    G=overlap**2/L
    eig=eigh(G,eigvals_only=True)
    pred=[]
    for p in partitions(m):
        pred += [zprod(p)/(4**m*L)]*hooks_dimension(tuple(2*x for x in p))
    pred=np.sort(pred)
    assert len(pred)==L
    spectrum_err=float(np.max(np.abs(eig-pred)))
    assert spectrum_err<2e-12
    # Recover singlet coordinates without choosing a supplied code oracle.
    vals,vecs=eigh(overlap,subset_by_index=(L-d,L-1))
    U=V@vecs/np.sqrt(vals)[None,:]
    C=U.T@V
    tight_err=float(np.linalg.norm(C@C.T/L-np.eye(d)/d))
    assert tight_err<1e-11
    loop_err=0.
    for i in range(L):
        # Every pair through n=8; fixed sampled columns for n=10.
        js=range(L) if n<=8 else (0,(17*i+3)%L,L-1)
        for j in js:
            loop_err=max(loop_err,abs(overlap[i,j]**2-4.**(loops(n,Ms[i],Ms[j])-m)))
    assert loop_err<1e-12
    out['spectra'].append({'n':n,'d':d,'matchings':L,'max_spectrum_error':spectrum_err,
                          'tight_frame_error':tight_err,'loop_overlap_error':loop_err,
                          'second_over_top':float(eig[-2]/eig[-1]),
                          'full_coefficient':(n+2)/(n-1)})
    # An explicit second-eigenspace Hermitian generator: centered SWAP(0,1).
    ix=np.arange(2**n); perm=ix.copy()
    diff=((ix>>0)^(ix>>1))&1
    perm^=diff*((1<<0)|(1<<1))
    H=U.T@U[perm,:]; H-=np.trace(H)/d*np.eye(d)
    H/=np.linalg.norm(H)
    frameH=(C*(np.einsum('ij,ij->j',C,H@C))[None,:])@C.T/L
    hres=float(np.linalg.norm(frameH-3/(d*(n+2))*H))
    assert hres<2e-12
    for t in (.2,.05,.01):
        A=expm(1j*t*H)
        fe=abs(np.trace(A)/d)**2
        pp=float(np.mean(abs(np.einsum('ij,ij->j',C,A@C))**2))
        ratio=(1-fe)/(1-pp)
        out['sharpness'].append({'n':n,'t':t,'loss_over_q':ratio,'target':(n+2)/(n-1),'H_eigen_residual':hres})
        assert ratio<=(n+2)/(n-1)+1e-8
    # Arbitrary rectangular Kraus maps from the singlet input to code+leak.
    # Any such map extends to the entire physical input using extra Kraus
    # operators on P-perp; output dimension d+3 <=2^n.
    for case in range(24):
        dout=d+3; rank=3
        W=random_isometry(dout*rank,d)
        Ks=list(W.reshape(rank,dout,d))
        p=(1.,.1,1e-4)[case%3]
        I=np.zeros((dout,d),complex);I[:d]=np.eye(d)
        Ks=[np.sqrt(1-p)*I]+[np.sqrt(p)*a for a in Ks]
        tp=np.linalg.norm(sum(a.conj().T@a for a in Ks)-np.eye(d))
        pp=sum(np.mean(abs(np.einsum('ij,ij->j',C,a[:d]@C))**2) for a in Ks)
        q=1-float(pp)
        f0=sum(abs(np.trace(a[:d])/d)**2 for a in Ks)
        bound=(n+2)/(n-1)*q
        assert 1-f0<=bound+1e-12 and tp<1e-11
        k=2**int(math.log2(d)); Q=random_isometry(d,k)
        fsub=sum(abs(np.trace(Q.conj().T@a[:d]@Q)/k)**2 for a in Ks)
        leak=sum(np.linalg.norm(a@Q)**2-np.linalg.norm(Q.conj().T@a[:d]@Q)**2 for a in Ks)
        # Reset to maximally mixed logical state; its entanglement-fidelity
        # contribution is Tr(leak input effect)/k^3.
        fe_reset=fsub+leak/(k**3)
        subbound=d/k*bound
        assert 1-fsub<=subbound+1e-12
        assert 1-fe_reset<=subbound+1e-12
        out['cptp_cases'].append({'n':n,'case':case,'p':p,'K':k,'test_failure':q,
          'raw_full_loss':float(1-f0),'full_bound':bound,'reset_subcode_loss':float(1-fe_reset),
          'subcode_bound':subbound,'trace_preservation_residual':float(tp)})
# One-site Z maps every matching singlet product to an orthogonal state.
for n in (4,6,8):
    Ms=list(matchings(tuple(range(n))));mx=0.
    signs=1-2*(np.arange(2**n)&1)
    for M in Ms:
        v=state(n,M);mx=max(mx,abs(v@(signs*v))**2)
    assert mx<1e-15
out['single_site_Z_pass_probability']='exactly zero by singlet/triplet orthogonality; checked n=4,6,8'
out['all_checks_passed']=True
out['script_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
p=(ROOT/'check_matching_survival_v1.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'partition_checks':sum(x['partitions_le4'] for x in out['partition_order']),
 'cptp_checks':len(out['cptp_cases']),'spectra':out['spectra'],'output':str(p)},indent=2))
