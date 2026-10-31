"""Exact finite-bandwidth three-mode parity emission; no eliminated bath.

Hamiltonian (hbar=1):
  g[(b†+c†)m+h.c.] + chi Z1 c†c
  + u(t) Z2(b+b†) + w(t) Z2(c+c†).
Outlets sqrt(Gamma)m, sqrt(kb)b, sqrt(kc)c. All baths vacuum.
The direct finite-mode construction is owned/derived by root. It replaces
an ideal cascade with an explicit reciprocal finite damped mediator.
"""
from dataclasses import dataclass,asdict
from pathlib import Path
import json
import numpy as np
from scipy.integrate import simpson,solve_ivp
from scipy.special import ndtri,ndtr

@dataclass
class Model:
    T:float=8.
    g:float=1.
    Gamma:float=4.
    chi:float=2.
    kb:float=0.
    kc:float=0.
    eta:float=.5
    assignment_error:float=.001
    photons:float|None=None
    @property
    def N(self):return self.photons if self.photons is not None else ndtri(self.assignment_error)**2/(4*self.eta)

def unscaled(m,t):
    t=np.asarray(t);k=np.pi/m.T
    U=[]
    for n in range(5):
        r=np.zeros_like(t,dtype=float)
        if n==0:r=r+10/32
        for h,coef in [(2,-15/32),(4,6/32),(6,-1/32)]:
            r=r+coef*(h*k)**n*np.cos(h*k*t+n*np.pi/2)
        U.append(r)
    ab,ac=m.kb/2,m.kc/2
    rt=np.sqrt(m.Gamma)
    A=[rt/m.g*(U[j+1]+ab*U[j]) for j in range(4)]
    V=[-(A[j+1]+m.Gamma*A[j]/2)/(m.g*rt)-U[j] for j in range(3)]
    B=(-ac*V[0]+m.g*A[0]/rt-V[1])/m.chi
    dB=(-ac*V[1]+m.g*A[1]/rt-V[2])/m.chi
    u=-dB-ab*B
    w=dB+ac*B-m.chi*V[0]
    return dict(A=A[0],U=U[0],V=V[0],B=B,u=u,w=w)

def normalization(m):
    # The sin^6 polynomial has an exact orthogonal Fourier norm. Its
    # derivative and itself are orthogonal over a complete compact pulse.
    k=np.pi/m.T;ab=m.kb/2
    Iu=m.T*(10/32)**2+m.T/2*sum(v*v for v in (-15/32,6/32,-1/32))
    Idu=m.T/2*sum(v*v*(h*k)**2 for h,v in [(2,-15/32),(4,6/32),(6,-1/32)])
    return np.sqrt(m.N/(m.Gamma/m.g**2*(Idu+ab*ab*Iu)))

def waveforms(m,t):
    scale=normalization(m)
    f={k:scale*v for k,v in unscaled(m,t).items()}
    f['b']=f['U']+1j*f['B']
    f['c']=f['V']-1j*f['B']
    f['meter']=1j*f['A']/np.sqrt(m.Gamma)
    return f

def solve(m,samples=12001):
    t=np.linspace(0,m.T,samples);f=waveforms(m,t)
    integ=lambda x:float(simpson(x,x=t))
    N=integ(f['A']**2);IB=integ(f['B']**2)
    IU=integ(f['U']**2);IV=integ(f['V']**2)
    CU=integ(f['U']*f['B']);CV=integ(f['V']*f['B'])
    K=m.kc*CV-m.kb*CU
    phase=-integ(f['u']*f['U']+f['w']*f['V'])
    D=(m.kb+m.kc)*IB
    r={'model':asdict(m),'N':N,'IB':IB,'IU':IU,'IV':IV,'CU':CU,'CV':CV,'K':K,
       'phase_Z1':phase,'local_Z1_correction':phase-K,
       'assignment_error':float(ndtr(-2*np.sqrt(m.eta*N))),
       'same_parity_visibility':float(np.exp(-2*D)),
       'same_parity_pZ':float(-np.expm1(-2*D)/2),
       'peak_u':float(np.max(abs(f['u']))),'peak_w':float(np.max(abs(f['w']))),
       'action_u':integ(f['u']**2),'action_w':integ(f['w']**2),
       'exposure_b':IU+IB,'exposure_c':IV+IB,'exposure_meter':N/m.Gamma,
       'peak_n_b':float(np.max(abs(f['b'])**2)),
       'peak_n_c':float(np.max(abs(f['c'])**2)),
       'peak_n_meter':float(np.max(abs(f['meter'])**2)),
       'terminal_photons':float(abs(f['b'][-1])**2+abs(f['c'][-1])**2+abs(f['meter'][-1])**2),
       'initial_drive_max':float(max(abs(f['u'][0]),abs(f['w'][0]))),
       'final_drive_max':float(max(abs(f['u'][-1]),abs(f['w'][-1])))}
    return r,t,f

Z1=np.array([1,1,-1,-1]);Z2=np.array([1,-1,1,-1]);S=Z1*Z2
def instrument_gram(r,reported=1):
    m=r['model'];eta=m['eta'];N=r['N'];IB=r['IB'];K=r['K']
    parity_hidden=m['kb']*r['IU']+m['kc']*r['IV']
    local_hidden=(m['kb']+m['kc'])*IB
    G=np.zeros((4,4),complex)
    for i in range(4):
        for j in range(4):
            expo=-(N+parity_hidden)*(S[i]-S[j])**2/2-local_hidden*(Z2[i]-Z2[j])**2/2
            expo+=1j*K*((Z1[i]-Z1[j])+S[i]*Z2[j]-S[j]*Z2[i])
            G[i,j]=np.exp(expo)*ndtr(reported*(S[i]+S[j])*np.sqrt(eta*N))
    return G

def check_ode(m):
    def rhs(t,z):
        b,c,d=z;f=waveforms(m,t)
        return np.array([-m.kb*b/2-1j*m.g*d-1j*f['u'],
                         -(m.kc/2+1j*m.chi)*c-1j*m.g*d-1j*f['w'],
                         -m.Gamma*d/2-1j*m.g*(b+c)])
    tt=np.linspace(0,m.T,3001)
    z=solve_ivp(rhs,[0,m.T],np.zeros(3,complex),t_eval=tt,method='DOP853',rtol=2e-12,atol=1e-13)
    f=waveforms(m,tt)
    return {'success':bool(z.success),
            'max_amplitude_error':float(np.max(abs(z.y-np.array([f['b'],f['c'],f['meter']])))),
            'max_parity_outlet_error':float(np.max(abs(np.sqrt(m.Gamma)*z.y[2]-1j*f['A']))),
            'terminal_photons_from_ode':float(np.sum(abs(z.y[:,-1])**2))}

def main():
    rows=[]
    for T in (4.,8.,12.,16.):
        for rate in (0.,1e-5,1e-4,1e-3):
            m=Model(T=T,kb=rate,kc=rate)
            r,_,_=solve(m)
            P,M=[instrument_gram(r,s) for s in (1,-1)]
            r['min_instrument_eigenvalue']=float(min(np.linalg.eigvalsh(P).min(),np.linalg.eigvalsh(M).min()))
            r['TP_error']=float(np.max(abs(np.diag(P+M)-1)))
            rows.append(r)
            print(T,rate,'pZ',r['same_parity_pZ'],'drives',r['peak_u'],r['peak_w'],'peaks',r['peak_n_b'],r['peak_n_c'],flush=True)
    tests=[]
    for rate in (0.,.001):
        m=Model(kb=rate,kc=rate)
        tests.append({'model':asdict(m),**check_ode(m)})
    Path(__file__).with_name('finite_mediator_results.json').write_text(json.dumps({'cases':rows,'ode_checks':tests},indent=2))
    print('ODE',tests)
if __name__=='__main__':main()
