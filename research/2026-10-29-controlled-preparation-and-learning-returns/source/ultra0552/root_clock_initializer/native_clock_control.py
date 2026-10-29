"""Finite native clock consumer; chosen lambda is NOT all-family admitted."""
from pathlib import Path
import json,time
import numpy as np
from scipy.linalg import eigh,norm
from scipy.integrate import solve_ivp

def kp(xs):
    out=np.ones((1,1),complex)
    for x in xs:out=np.kron(out,x)
    return out

def run():
    start=time.perf_counter();L=4;lam=1/8;beta=.01;Delta=1/(4*lam**L)
    i2=np.eye(2);x=np.array(((0,1),(1,0)),complex);z=np.diag((1.,-1.))
    ps=[[kp([p if j==a else i2 for j in range(4)]) for a in range(4)] for p in (x,z)]
    checks=[kp([p]*4) for p in (x,z)];idd=np.eye(16);ic=np.eye(L)
    proj=[np.diag([float(j==a) for j in range(L)]) for a in range(L)]
    q=ic-proj[0];nclock=np.kron(q,ic)+np.kron(ic,q)
    h=np.kron(idd,nclock).astype(complex);gauges=[]
    for c in range(2):
        pref=idd.copy();g=np.zeros_like(h)
        for a in range(L):
            cp=np.kron(proj[a],ic) if c==0 else np.kron(ic,proj[a])
            g+=np.kron(pref,cp);pref=pref@ps[c][a]
        gauges.append(g)
        for j in range(1,L+1):
            hop=np.zeros((L,L),complex);hop[j%L,(j-1)%L]=1;hop[(j-1)%L,j%L]=1
            cp=np.kron(hop,ic) if c==0 else np.kron(ic,hop)
            h-=lam*np.kron(ps[c][j-1],cp)
    u=gauges[1]@gauges[0];hg=u@h@u.conj().T
    assert norm(u.conj().T@u-np.eye(256))<1e-12
    sectors=[];rebuilt=np.zeros_like(h)
    for sx in (1,-1):
        for sz in (1,-1):
            p=(idd+sx*checks[0])@(idd+sz*checks[1])/4
            hs=np.einsum('ab,bcad->cd',p,hg.reshape(16,16,16,16))/4
            ev,vec=eigh(hs);rebuilt+=np.kron(p,hs)
            sectors.append(dict(s=(sx,sz),p=p,h=hs,e=ev,psi=vec[:,0]))
    residual=float(norm(hg-rebuilt));assert residual<1e-11
    es=np.array([s['e'][0] for s in sectors]);e0=es.min()
    zf=np.array([np.exp(-beta*Delta*(s['e']-e0)).sum() for s in sectors])
    zg=np.exp(-beta*Delta*(es-e0));pg=zg/zg.sum();pf=zf/zf.sum();outside=1-zg.sum()/zf.sum()
    rf=np.zeros_like(h);rg=np.zeros_like(h)
    for j,s in enumerate(sectors):
        ev,vec=eigh(s['h']);thermal=(vec*np.exp(-beta*Delta*(ev-e0)))@vec.conj().T/zf.sum()
        rf+=np.kron(s['p']/4,thermal)
        rg+=pg[j]*np.kron(s['p']/4,np.outer(s['psi'],s['psi'].conj()))
    error=float(np.abs(eigh(rf-rg,eigvals_only=True)).sum())
    assert abs(error-2*outside)<2e-12
    coeff={str(a):float(sum(e*np.prod([v for v,b in zip(s['s'],a) if b])
                              for e,s in zip(es,sectors))/4*Delta)
           for a in ((1,0),(0,1),(1,1))}
    vac=np.zeros(16,complex);vac[0]=1;T=500.;adiabatic=[]
    for s in sectors:
        v=s['h']-nclock
        sol=solve_ivp(lambda t,y:-1j*(nclock+(t/T)*v)@y,(0,T),vac,
                      rtol=2e-9,atol=2e-11,method='DOP853')
        f=float(abs(np.vdot(s['psi'],sol.y[:,-1]))**2);assert f>.99999
        adiabatic.append(dict(s=s['s'],T=T,fidelity=f,nfev=sol.nfev,norm=float(norm(sol.y[:,-1]))))
    return dict(scope='finite actual two-body-qudit control; not all-size admission or native performance',
                data_qubits=4,checks=['XXXX','ZZZZ'],clock_dimension=L,physical_dimension=256,
                lambda_value=lam,beta=beta,Delta=Delta,gauge_residual=residual,
                gaps=[float(s['e'][1]-s['e'][0]) for s in sectors],scaled_energy_coefficients=coeff,
                ground_conditioned_syndrome_law=pg.tolist(),full_syndrome_law=pf.tolist(),
                marginal_l1_difference=float(np.abs(pg-pf).sum()),outside_probability=float(outside),
                projection_trace_error=error,twice_outside=float(2*outside),
                actual_adiabatic_preparations=adiabatic,seconds=time.perf_counter()-start)

if __name__=='__main__':
    r=run();Path(__file__).with_name('NATIVE_CLOCK_CONTROL.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
