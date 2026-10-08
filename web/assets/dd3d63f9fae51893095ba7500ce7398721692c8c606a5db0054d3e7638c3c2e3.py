"""Small finite convention checks; not evidence for arbitrary L or prior art."""
from pathlib import Path
import json, math
import numpy as np
from numpy.linalg import eigh

def entropy(r):
    p=np.linalg.eigvalsh((r+r.T)/2)
    p=p[p>1e-14]
    return float(-np.dot(p,np.log(p)))

def gibbs(h,beta):
    e,u=eigh(h)
    w=np.exp(-beta*(e-e[0])); z=w.sum()
    return (u*(w/z))@u.T,float(np.log(z)-beta*e[0])

receipts=[]; minimum=1e100
for L in range(4,9):
    J=1.; tau=.09; lam=7.; beta=tau*L*L
    ns=L-1; D=1<<ns
    occ=np.array([[(x>>i)&1 for i in range(ns)] for x in range(D)])
    num=occ.sum(axis=1); K=np.diag(4*J*num.astype(float))
    for x in range(D):
        for i in range(ns-1):
            if occ[x,i]!=occ[x,i+1]: K[x,x^(3<<i)]=-2*J
    H0=K-np.diag(lam*num/L**2); rho0,logZ0=gibbs(H0,beta)
    modes=np.arange(1,L); eps=4*J*(1-np.cos(np.pi*modes/L))
    f=1/(1+np.exp(tau*(L*L*eps-lam)))
    phi=np.sqrt(2/L)*np.sin(np.pi*np.outer(np.arange(1,L),modes)/L)
    corr=(phi*f)@phi.T
    assert abs(np.dot(np.diag(rho0),num)-sum(f))<2e-12
    for R in (1,2):
        pairs=[(i,i+r) for r in range(1,R+1) for i in range(ns-r)]
        pairnum=sum((occ[:,i]*occ[:,j] for i,j in pairs),np.zeros(D,dtype=int))
        forbidden=pairnum>0; allowed=~forbidden
        delta=float(np.diag(rho0)[forbidden].sum()); p=1-delta
        qM=float(np.dot(np.diag(rho0)[forbidden],num[forbidden]))
        pair_expect=sum(corr[i,i]*corr[j,j]-corr[i,j]**2 for i,j in pairs)
        assert delta <= pair_expect+2e-12
        assert qM <= (2+sum(f))*pair_expect+2e-12
        sigma=rho0*np.outer(allowed,allowed)/p
        kinetic=float(np.trace(sigma@K)-np.trace(rho0@K))
        kb=(delta*np.trace(rho0@K)+8*J*qM)/p
        assert kinetic <= kb+2e-12
        h2=-(delta*math.log(delta)+(1-delta)*math.log1p(-delta)) if delta else 0
        sb=(h2+delta*ns*math.log(2))/p
        assert entropy(rho0)-entropy(sigma)<=sb+3e-12
        distance0=float(np.abs(np.linalg.eigvalsh(sigma-rho0)).sum())
        assert distance0<=2*math.sqrt(delta)+3e-12
        for scale,kind in [(v,"density") for v in (.2,3.,1000.)]+[(3.,"non_number_conserving"),(1000.,"non_number_conserving")]:
            # Inhomogeneous positive values; at zero strength the forbidden
            # projection would still be legal, so not all pairs need appear.
            W=sum((scale*(1+(i+2*j)%4)*occ[:,i]*occ[:,j]
                   for i,j in pairs),np.zeros(D))
            W=np.diag(W)
            if kind=="non_number_conserving":
                # Rank-one PSD perturbation on the forbidden space, mixing
                # different M sectors. Its kernel contains P exactly.
                v=np.where(forbidden,np.cos(np.arange(D)*1.713),0.)
                v=v/np.linalg.norm(v)
                W=scale*np.outer(v,v)
                assert np.linalg.norm(W[:,allowed])<1e-12
                assert np.linalg.norm(W@np.diag(num)-np.diag(num)@W)>1e-7
            rhoW,logZW=gibbs(H0+W,beta)
            ds=-entropy(sigma)+beta*float(np.trace(sigma@H0))+logZW
            variational=(entropy(rho0)-entropy(sigma)+
                         beta*float(np.trace((sigma-rho0)@H0)))
            assert ds>=-1e-9 and ds<=variational+1e-9
            dsw=float(np.abs(np.linalg.eigvalsh(sigma-rhoW)).sum())
            assert dsw<=math.sqrt(2*max(0,ds))+2e-7
            bound=2*math.sqrt(delta)+math.sqrt(2*max(0,variational))
            dw=float(np.abs(np.linalg.eigvalsh(rhoW-rho0)).sum())
            assert dw<=bound+2e-7
            # One fixed free-canonical decoder, valid without [W,M]=0.
            decoded=np.zeros((D,D)); decoded_free=np.zeros((D,D))
            for m in range(ns+1):
                sel=num==m
                pm=float(np.diag(rho0)[sel].sum())
                canon=rho0*np.outer(sel,sel)/pm
                decoded += float(np.diag(rhoW)[sel].sum())*canon
                decoded_free += pm*canon
            assert np.linalg.norm(decoded_free-rho0)<2e-12
            deb=float(np.abs(np.linalg.eigvalsh(decoded-rhoW)).sum())
            assert deb<=2*dw+2e-7
            minimum=min(minimum,bound-dw)
            receipts.append({'L':L,'R':R,'strength_scale':scale,'interaction_type':kind,'EB_trace_error':deb,
                'forbidden_probability':delta,'actual_trace_error':dw,
                'projection_variational_bound':bound,
                'relative_entropy':ds})
out={'status':'PASS','fixtures':len(receipts),'L':'4..8','minimum_bound_margin':minimum,
     'arithmetic':'double precision finite matrix diagonalization',
     'scope':'Convention diagnostics only; all-L proof and external validation separate.',
     'measurements':receipts}
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:v for k,v in out.items() if k!='measurements'})
