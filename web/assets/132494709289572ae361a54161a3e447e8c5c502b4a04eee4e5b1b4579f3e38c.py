#!/usr/bin/env python3
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json,time
started=time.monotonic()

def dim(s,d): return comb(s+d-1,d-1)
def berezin(s,l,d):
    if l>s:return F(0)
    p=F(1)
    for j in range(l):p*=F(s-j,s+d+j)
    return p
count=0;maxratio=F(0);argmax=None
for d in [2,3,4,8,16,64,1024]:
    for n in range(2,41):
        for k in sorted({1,n//2}):
            c=F(n,n-k)
            for l in range(n+1):
                b=berezin(n,l,d);bk=berezin(k,l,d)
                lam=bk/b
                assert 0<=b<=1 and 0<=lam<=1
                assert 1-b<=c*(1-lam)
                if l and lam!=1:
                    ratio=(1-b)/(1-lam)
                    if ratio>maxratio:maxratio,argmax=ratio,(d,n,k,l)
                count+=1
            assert sum(dim(l,d)**2-(dim(l-1,d)**2 if l else 0) for l in range(n+1))==dim(n,d)**2

out={'scope':'Fraction eigenvalue/Dirichlet checks are transcription diagnostics for the complete proof in symmetric_sector_rounding.txt. Dense optional fixtures directly construct partial trace/Petz channels.','fraction_fixtures':count,'maximum_observed_ratio':str(maxratio),'argmax':argmax,'dense':[]}
try:
    import numpy as np
    from math import sqrt
    def occupations(s,d):
        if d==1:return [(s,)]
        return [(r,)+tail for r in range(s+1) for tail in occupations(s-r,d-1)]
    def multinomial(a):
        v=1;remain=sum(a)
        for x in a:v*=comb(remain,x);remain-=x
        return v
    for d,n,k in [(2,2,1),(2,4,2),(2,6,3),(3,2,1),(3,3,1)]:
        oo=occupations(n,d);aa=occupations(k,d);bb=occupations(n-k,d)
        Dn,Dk,Db=len(oo),len(aa),len(bb)
        V=np.zeros((Dk,Db,Dn))
        lookup={c:i for i,c in enumerate(oo)}
        for aidx,a in enumerate(aa):
            for bidx,b in enumerate(bb):
                c=tuple(x+y for x,y in zip(a,b))
                V[aidx,bidx,lookup[c]]=sqrt(multinomial(a)*multinomial(b)/multinomial(c))
        vv=V.reshape(Dk*Db,Dn)
        iso=float(np.max(np.abs(vv.T@vv-np.eye(Dn))))
        K=[V[:,b,:] for b in range(Db)]
        def T(A):return sum((z@A@z.T for z in K),np.zeros((Dk,Dk)))
        def R(A):return (Dk/Dn)*sum((z.T@A@z for z in K),np.zeros((Dn,Dn)))
        Phi=np.zeros((Dn*Dn,Dn*Dn))
        for i in range(Dn):
            for j in range(Dn):
                A=np.zeros((Dn,Dn));A[i,j]=1
                Phi[:,i*Dn+j]=R(T(A)).reshape(-1)
        predicted=[]
        for l in range(n+1):
            multiplicity=dim(l,d)**2-(dim(l-1,d)**2 if l else 0)
            predicted.extend([float(berezin(k,l,d)/berezin(n,l,d))]*multiplicity)
        actual=np.linalg.eigvalsh((Phi+Phi.T)/2)
        spectral=float(np.max(np.abs(actual-np.sort(predicted))))
        adjoint=float(np.max(np.abs(Phi-Phi.T)))
        ref=float(np.max(np.abs(R(T(np.eye(Dn)))-np.eye(Dn))))
        assert iso<1e-12 and spectral<1e-12 and adjoint<1e-12 and ref<1e-12
        out['dense'].append({'d':d,'n':n,'k':k,'Dn':Dn,'Dk':Dk,'isometry_defect':iso,'spectrum_defect':spectral,'selfadjoint_defect':adjoint,'reference_defect':ref})
except ImportError:
    out['dense_status']='NumPy unavailable; complete derivation is unaffected.'
out['elapsed_seconds']=time.monotonic()-started
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'fraction_fixtures':count,'dense_fixtures':len(out['dense']),'elapsed_seconds':out['elapsed_seconds'],'all_passed':True}))
