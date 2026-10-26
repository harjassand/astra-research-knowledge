#!/usr/bin/env python3
"""A positive-energy finite-band Fano audit of bounded chiral pitch-and-catch.

Declared one-excitation Hamiltonian:
    H(t)=E0*(|L><L|+|R><R|)+ M_omega + W(t)+W(t)^*
 W_L(omega,t)=sqrt(gL(t)/(2*pi))*sqrt(h(omega)),
 W_R(omega,t)=sqrt(gR(t)/(2*pi))*sqrt(h(omega))*exp(-i*omega*tau),
 h(omega)=[1-(omega-E0)^2/E0^2]^2 on 0<omega<2 E0.

Full positive-frequency two-node ONE-CHIRAL-CHANNEL continuum is retained.
This model is not a physical reciprocal waveguide or a demonstration of
an actually manufactured strictly chiral structure.
"""
import numpy as np, math, json, time, argparse
from scipy.special import roots_legendre
from scipy.integrate import solve_ivp


def ideal(x):
    q=math.exp(-x)
    return {'receiver_probability':(1-q)**2, 'sender_probability':q,
            'bath_probability':q-q*q, 'joint_target_error':math.sqrt(2*q)}

def simulate(E0=12., gamma=.3, x=9.903487553, tau=2.5, N=900, max_step=.02, rtol=6e-8,atol=8e-10):
    A=x/gamma
    nodes, gauss_weights=roots_legendre(N)
    omega=E0*(1+nodes)
    nu=omega-E0
    h=(1-nodes*nodes)**2
    v=np.sqrt(E0*gauss_weights*h/(2*np.pi))
    phase=np.exp(-1j*omega*tau)
    vR=v*phase
    initial=np.zeros(N+2,complex);initial[0]=1
    def rates(t):
        yl=gamma/(1+np.exp(np.clip(-gamma*t,-600,600))) if -A<=t<=A else 0.
        tr=t-tau
        yr=gamma/(1+np.exp(np.clip(gamma*tr,-600,600))) if -A<=tr<=A else 0.
        return np.sqrt(yl),np.sqrt(yr)
    def rhs(t,y):
        gl,gr=rates(t)
        a,b=y[:2];z=y[2:]
        rez=np.empty_like(y)
        rez[0]=-1j*gl*np.vdot(v,z)
        rez[1]=-1j*gr*np.vdot(vR,z)
        rez[2:]=-1j*(nu*z+v*(gl*a)+vR*(gr*b))
        return rez
    t0=time.time()
    sol=solve_ivp(rhs,(-A,A+tau),initial,method='DOP853',rtol=rtol,atol=atol,max_step=max_step)
    target=-np.exp(1j*E0*tau)
    final=sol.y[:,-1];a,b=final[:2];bath=final[2:]
    pb=float(np.vdot(bath,bath).real)
    probability=float(abs(b)**2)
    unitarity=float(abs(np.vdot(final,final).real-1))
    full_error=float(np.sqrt(max(0,2-2*np.real(np.conj(target)*b))))
    return {'E0':E0,'gamma':gamma,'x':x,'tau':tau,'N':N,'A':A,'duration':2*A+tau,
            'receiver_probability':probability,'receiver_amplitude_abs':float(abs(b)),
            'receiver_phase':float(np.angle(b)), 'ideal_phase':float(np.angle(target)),
            'sender_probability':float(abs(a)**2),'bath_probability':pb,'full_state_error':full_error,
            'unitarity_residual':unitarity,'runtime_sec':time.time()-t0,
            'nfev':sol.nfev,'solver_success':sol.success,
            'analytical_schur_margin_lower_bound':E0-4*gamma/(3*np.pi),
            'ideal_cascade':ideal(x),
            'scope':'Gauss-Legendre discretization of positive-frequency finite-band chiral Fano Hamiltonian. Physical coupling and propagation not acquired. Markov limit is independent analytic comparison.'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n,ty,v in [('E0',float,12),('gamma',float,.3),('x',float,9.903487553),('tau',float,2.5),('N',int,900),('max_step',float,.02)]:p.add_argument('--'+n,type=ty,default=v)
    p.add_argument('--out',default='/mnt/data/astra_chiral_no_bypass_finite_band_20261027.json')
    a=p.parse_args();ans=simulate(**{k:getattr(a,k) for k in ('E0','gamma','x','tau','N','max_step')})
    with open(a.out,'w') as f:json.dump(ans,f,indent=2)
    print(json.dumps(ans,indent=2))
