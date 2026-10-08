from math import exp, log
from pulse_witness import EDGES, eye, matmul, matvec, expm, matscale, generator, phase_transition_and_flux


def protocol(A, d, B0, tau):
    q=exp(-A); c=exp(-B0)
    Es=[[0.,-A,-A],[-A,0.,-A],[-A,-A,0.]]
    Bs=[[B0-d,B0,B0+d],[B0+d,B0-d,B0],[B0,B0+d,B0-d]]
    # one period map, column-vector convention
    P=eye(3)
    for E,B in zip(Es,Bs):
        Q,_=generator(E,B)
        P=matmul(expm(matscale(Q,tau)),P)
    p=[1/3]*3
    for _ in range(200000):
        pn=matvec(P,p)
        err=sum(abs(pn[i]-p[i]) for i in range(3))
        p=pn
        if err<2e-15: break
    p0=p.copy()
    flux=[0.]*3; W=0.; Eprev=Es[-1]
    phase_starts=[]
    for E,B in zip(Es,Bs):
        W += sum(p[i]*(E[i]-Eprev[i]) for i in range(3))
        phase_starts.append(p.copy())
        p, fl=phase_transition_and_flux(E,B,p,tau)
        flux=[flux[i]+fl[i] for i in range(3)]
        Eprev=E
    J=sum(flux)/3
    u=c/3*(exp(d)+q*(1+exp(-d)))
    w=c/3*(exp(-d)+q*(1+exp(d)))
    Jinf=(u-w)/3
    T=u+w
    aff=3*log(u/w)
    ETP=T/3*__import__('math').tanh(abs(aff)/6)
    Wrateinf=2*c*A/3*(1-q)*__import__('math').cosh(d)
    return dict(A=A,d=d,B0=B0,tau=tau,period=3*tau,p0=p0,phase_starts=phase_starts,
                closure=err,flux=flux,J=J,J_inf=Jinf,J_err=J-Jinf,
                Jpersec=J/(3*tau),Jinf_persec=Jinf,
                Wwell=W,Wwell_rate=W/(3*tau),Wwell_rate_inf=Wrateinf,
                Wwell_per_product=W/J if J else float('inf'),T=T,aff=aff,ETP=ETP,
                u=u,w=w, c0=c)

if __name__=='__main__':
    A=4.; d=.1; B0=.5
    print('params A=4 kBT, d=0.1 kBT barrier downward gate, B0=0.5 kBT, nu=1 s^-1; all phase rates DB')
    for tau in [.5,.2,.1,.05,.02,.01,.005]:
        z=protocol(A,d,B0,tau)
        print('tau={tau:.5g} P={period:.5g} J/cycle={J:.12g} Jrate={Jpersec:.12g} Jinf={Jinf_persec:.12g} relJ={rel:.5g} Wwell/cycle={Wwell:.12g} Wrate={Wwell_rate:.12g} Wrate_inf={Wwell_rate_inf:.12g} relW={relW:.5g} W/J={Wwell_per_product:.9g} closure={closure:.2g} p0={p0}'.format(**z,rel=(z['Jpersec']-z['Jinf_persec'])/z['Jinf_persec'],relW=(z['Wwell_rate']-z['Wwell_rate_inf'])/z['Wwell_rate_inf']))
    # rates and exact averaged bound
    z=protocol(A,d,B0,.02)
    print('u,w,T,Aeff,ETP,Jinf:',z['u'],z['w'],z['T'],z['aff'],z['ETP'],z['Jinf_persec'])
