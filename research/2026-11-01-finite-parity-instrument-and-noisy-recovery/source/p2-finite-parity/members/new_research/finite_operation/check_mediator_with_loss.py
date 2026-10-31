"""Independent finite-Fock full-coherence check of the lossy finite mediator.

Root's file supplies only the controls and scalar quantities under test. The
test evolves the full physical 3-mode cross-Lindblad generators, with all
three loss ports explicitly present. Six logical coherences are tested.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'root'))
from finite_mediator_parity import Model,solve,waveforms,instrument_gram
from dataclasses import asdict
import itertools,json
import numpy as np
from scipy.integrate import solve_ivp


def run(m,ncut):
    aa=np.diag(np.sqrt(np.arange(1,ncut)),1).astype(complex);ee=np.eye(ncut)
    b=np.kron(np.kron(aa,ee),ee);c=np.kron(np.kron(ee,aa),ee);v=np.kron(np.kron(ee,ee),aa)
    n=ncut**3
    Xb=b+b.conj().T;Xc=c+c.conj().T
    H0=m.g*(b.conj().T@v+v.conj().T@b+c.conj().T@v+v.conj().T@c)
    nc=c.conj().T@c
    LL=[np.sqrt(m.Gamma)*v,np.sqrt(m.kb)*b,np.sqrt(m.kc)*c]
    G=sum(L.conj().T@L for L in LL)
    Z1=np.array([1,1,-1,-1]);Z2=np.array([1,-1,1,-1]);S=Z1*Z2
    r,_,_=solve(m)
    rho0=np.zeros((n,n),complex);rho0[0,0]=1
    out=[]
    for i,j in [(0,0)]+list(itertools.combinations(range(4),2)):
        def rhs(t,flat):
            rho=flat.reshape(n,n);f=waveforms(m,t)
            drive=f['u']*Xb+f['w']*Xc
            Hl=H0+Z1[i]*m.chi*nc+Z2[i]*drive
            Hr=H0+Z1[j]*m.chi*nc+Z2[j]*drive
            dr=-1j*(Hl@rho-rho@Hr)-.5*(G@rho+rho@G)
            for L in LL:dr+=L@rho@L.conj().T
            return dr.ravel()
        sol=solve_ivp(rhs,[0,m.T],rho0.ravel(),method='DOP853',rtol=2e-10,atol=5e-13)
        final=sol.y[:,-1].reshape(n,n);actual=np.trace(final)
        expo=-.5*((S[i]-S[j])**2*(r['N']+m.kb*r['IU']+m.kc*r['IV'])
                  +(Z2[i]-Z2[j])**2*(m.kb+m.kc)*r['IB'])
        expo+=1j*(r['phase_Z1']*(Z1[i]-Z1[j])+r['K']*(S[i]*Z2[j]-S[j]*Z2[i]))
        expected=np.exp(expo)
        out.append(dict(i=i,j=j,actual=[actual.real,actual.imag],expected=[expected.real,expected.imag],
                        abs_error=float(abs(actual-expected)),
                        terminal_nonvacuum_diagonal=float(1-final[0,0].real) if i==j else None))
    GG=[instrument_gram(r,q) for q in (1,-1)]
    return dict(model=asdict(m),cutoff_per_mode=ncut,comparisons=out,
                max_error=max(x['abs_error'] for x in out),
                min_binned_instrument_eigenvalue=float(min(np.linalg.eigvalsh(v).min() for v in GG)),
                trace_preservation_error=float(max(abs(np.diag(GG[0]+GG[1])-1))))


if __name__=='__main__':
    m=Model(T=8,g=1,Gamma=4,chi=2,kb=.02,kc=.03,photons=.002)
    out=[]
    for cut in (2,3,4):
        r=run(m,cut);out.append(r)
        print('cutoff',cut,'max_error',r['max_error'],flush=True)
        Path(__file__).with_name('finite_mediator_loss_check.json').write_text(json.dumps(out,indent=2))
