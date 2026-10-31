"""Independent all-coherence check of root's finite reciprocal mediator.

This checker defines its own Fourier-form pulse and Hamiltonian. No cascaded
or eliminated bath is used: b and c couple reciprocally to a third oscillator
m, and only m has an engineered dissipator sqrt(Gamma)m. Low-photon checks
qualify the ordinary algebra/sign derivation, not a high-energy device model.
"""
from pathlib import Path
from dataclasses import dataclass, asdict
import json
import itertools
import numpy as np
from scipy.integrate import simpson, solve_ivp


@dataclass
class Mediator:
    T: float=4.0
    Gamma: float=4.0
    g: float=2.0
    chi: float=2.0
    photons: float=0.002


def design(m,t):
    t=np.asarray(t)[...,None]
    om=np.array([2.,4.,6.])*np.pi/m.T
    coeff=np.array([5/16,-1/4,1/16])
    A0=np.sqrt(m.photons*256/(21*m.T))
    deriv=[A0*np.sum(coeff*om**j*np.sin(om*t+j*np.pi/2),axis=-1) for j in range(4)]
    A,dA,ddA,dddA=deriv
    F=A0*np.sum(coeff*(1-np.cos(om*t))/om,axis=-1)
    sq=np.sqrt(m.Gamma)
    D=-(dA+m.Gamma*A/2)/(m.g*sq)
    dD=-(ddA+m.Gamma*dA/2)/(m.g*sq)
    U=m.g*F/sq
    V=D-U
    B=(2*m.g*A/sq-dD)/m.chi
    dB=(dddA+m.Gamma*ddA/2+2*m.g*m.g*dA)/(m.g*m.chi*sq)
    u=-dB
    w=dB-m.chi*V
    return dict(A=A,F=F,U=U,V=V,B=B,u=u,w=w)


def independent_ode(m):
    t=np.linspace(0,m.T,2001)
    f=design(m,t)
    def rhs(t,x):
        p=design(m,t)
        b,c,v=x
        return [-1j*m.g*v-1j*p['u'],
                -1j*m.g*v-1j*m.chi*c-1j*p['w'],
                -m.Gamma*v/2-1j*m.g*(b+c)]
    sol=solve_ivp(rhs,[0,m.T],np.zeros(3,complex),t_eval=t,method='DOP853',rtol=2e-12,atol=1e-13)
    expected=np.array([f['U']+1j*f['B'],f['V']-1j*f['B'],1j*f['A']/np.sqrt(m.Gamma)])
    return {'max_amplitude_error':float(np.max(abs(sol.y-expected))),
            'terminal_population':float(np.sum(abs(sol.y[:,-1])**2)),
            'output_waveform_error':float(np.max(abs(np.sqrt(m.Gamma)*sol.y[2]-1j*f['A'])))}


def fock(m,ncut):
    aa=np.diag(np.sqrt(np.arange(1,ncut)),1).astype(complex)
    ee=np.eye(ncut)
    b=np.kron(np.kron(aa,ee),ee)
    c=np.kron(np.kron(ee,aa),ee)
    v=np.kron(np.kron(ee,ee),aa)
    n=ncut**3
    Xb=b+b.conj().T;Xc=c+c.conj().T
    H0=m.g*(b.conj().T@v+v.conj().T@b+c.conj().T@v+v.conj().T@c)
    nc=c.conj().T@c
    L=np.sqrt(m.Gamma)*v
    G=L.conj().T@L
    Z1=np.array([1,1,-1,-1]);Z2=np.array([1,-1,1,-1]);S=Z1*Z2
    t=np.linspace(0,m.T,10001);p=design(m,t)
    phi=-float(simpson(p['u']*p['U']+p['w']*p['V'],x=t))
    N=float(simpson(p['A']**2,x=t))
    rho0=np.zeros((n,n),complex);rho0[0,0]=1
    output=[]
    for i,j in [(0,0)]+list(itertools.combinations(range(4),2)):
        def rhs(t,flat):
            rho=flat.reshape(n,n)
            p=design(m,t)
            drive=p['u']*Xb+p['w']*Xc
            Hl=H0+Z1[i]*m.chi*nc+Z2[i]*drive
            Hr=H0+Z1[j]*m.chi*nc+Z2[j]*drive
            return (-1j*(Hl@rho-rho@Hr)+L@rho@L.conj().T-.5*(G@rho+rho@G)).ravel()
        sol=solve_ivp(rhs,[0,m.T],rho0.ravel(),method='DOP853',rtol=2e-10,atol=1e-12)
        final=sol.y[:,-1].reshape(n,n)
        actual=np.trace(final)
        target=np.exp(-.5*(S[i]-S[j])**2*N+1j*(Z1[i]-Z1[j])*phi)
        output.append({'i':i,'j':j,'actual':[actual.real,actual.imag],
                       'target':[target.real,target.imag],'abs_error':float(abs(actual-target)),
                       'terminal_nonvacuum_diagonal':float(1-final[0,0].real) if i==j else None})
    return {'model':asdict(m),'cutoff_per_mode':ncut,'phase':phi,'comparisons':output,
            'max_error':max(p['abs_error'] for p in output)}


if __name__=='__main__':
    m=Mediator()
    out={'model':asdict(m),'independent_ode':independent_ode(m),'fock_checks':[]}
    for cut in (2,3,4):
        r=fock(m,cut)
        out['fock_checks'].append(r)
        print('cutoff',cut,'max_error',r['max_error'],flush=True)
        Path(__file__).with_name('finite_mediator_independent_check.json').write_text(json.dumps(out,indent=2))
