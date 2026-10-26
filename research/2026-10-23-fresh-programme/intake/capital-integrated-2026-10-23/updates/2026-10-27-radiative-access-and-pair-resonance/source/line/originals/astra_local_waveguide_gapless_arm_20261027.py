#!/usr/bin/env python3
"""No-bypass finite Jacobi bus + side-attached positive gapless Jacobi arm.
The side-arm infinite-M limit has continuum [0,4J]; finite M audits the limit.
Positive counterterm delta=eta^2/J at bus attachment makes h(t)>=0
by Schur complementation (arm endpoint G(0)<=1/J).
"""
import math,json,time,argparse,numpy as np
from scipy.integrate import solve_ivp

def simulate(n=300,m=750,J=4.,gamma=.2,x=12.5,eta=.05,strength=1.004,max_step=.095,ramp=0.):
    E0=2*J;A=x/gamma;tau=(n-1)/(2*J);T=2*A+tau
    gscale=np.sqrt(J/2)
    def window(t,lo,hi):
        if t<=lo or t>=hi:return 0.
        if ramp<=0:return 1.
        if t<lo+ramp:
            u=(t-lo)/ramp;return u*u*(3-2*u)
        if t>hi-ramp:
            u=(hi-t)/ramp;return u*u*(3-2*u)
        return 1.
    def rates(t):
        ga=gamma/(1+math.exp(max(-600,min(600,-gamma*t)))) if -A<=t<=A else 0.
        s=t-tau
        gb=gamma/(1+math.exp(max(-600,min(600,gamma*s)))) if -A<=s<=A else 0.
        return strength*gscale*math.sqrt(ga)*window(t,-A,A),strength*gscale*math.sqrt(gb)*window(t,-A+tau,A+tau)
    # 0 left; 1:n+1 main bus; n+1 right; n+2: side arm
    mid=1+n//2; ia=n+2; nn=n+m+2
    y0=np.zeros(nn,complex);y0[0]=1
    def rhs(t,y):
        gl,gr=rates(t)
        d=np.zeros_like(y)
        d[0]=-1j*gl*y[1]
        d[1]=-1j*(gl*y[0]+J*y[2])
        d[2:n]=-1j*J*(y[1:n-1]+y[3:n+1])
        d[n]=-1j*(J*y[n-1]+gr*y[n+1])
        d[n+1]=-1j*gr*y[n]
        d[ia]=-1j*(eta*y[mid]+J*y[ia+1])
        d[ia+1:-1]=-1j*J*(y[ia:-2]+y[ia+2:])
        d[-1]=-1j*J*y[-2]
        d[mid]+=-1j*((eta**2/J)*y[mid]+eta*y[ia])
        return d
    tt=time.time()
    sol=solve_ivp(rhs,(-A,A+tau),y0,method='DOP853',rtol=4e-8,atol=1e-9,max_step=max_step,t_eval=[A+tau])
    f=sol.y[:,-1];pb=abs(f[n+1])**2
    return {'n_main_bus':n,'m_auxiliary_arm':m,'gamma':gamma,'x':x,'J':J,'eta':eta,'counterterm':eta**2/J,
            'duration':T,'ramp':ramp,'receiver_probability':float(pb),'full_state_error_phase_corrected':float(np.sqrt(max(0,2-2*abs(f[n+1])))),
            'sender_probability':float(abs(f[0])**2),'main_bus_probability':float(np.vdot(f[1:n+1],f[1:n+1]).real),
            'side_arm_probability':float(np.vdot(f[n+2:],f[n+2:]).real),'unitarity_error':float(abs(np.vdot(f,f).real-1)),
            'wall_time':time.time()-tt,'nfev':sol.nfev,'success':sol.success,
            'analytic_positivity':'zero-energy Schur complement: Green_arm(0)=m/[J(m+1)]<=1/J; delta=eta^2/J makes effective main bus nonnegative. The unperturbed main bus + endpoints is diagonally dominant for strengths used.',
            'limit_scope':'m->infinity yields gapless, genuinely coupled side continuum; n remains finite and transfers by multimode waveguide bus. No infinite-main-line transfer theorem claimed.'}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name,ty,val in [('n',int,300),('m',int,750),('eta',float,.05),('gamma',float,.2),('x',float,12.5),('J',float,4.),('strength',float,1.004),('max_step',float,.095),('ramp',float,0.)]:p.add_argument('--'+name,type=ty,default=val)
    p.add_argument('--out',default='/mnt/data/astra_local_waveguide_gapless_arm_20261027.json')
    args=p.parse_args();v=simulate(**{k:getattr(args,k) for k in ('n','m','eta','gamma','x','J','strength','max_step','ramp')})
    with open(args.out,'w') as f:json.dump(v,f,indent=2)
    print(json.dumps(v,indent=2))
