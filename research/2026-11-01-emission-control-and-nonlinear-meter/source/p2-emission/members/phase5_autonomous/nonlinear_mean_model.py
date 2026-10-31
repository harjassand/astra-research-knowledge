"""Exact classical branch means and local Hessians of the full cat meter.

This corrects the fixed idle-cat expansion.  The resulting Gaussian channel is
still an approximation, but its omitted Hamiltonian is cubic in FLUCTUATIONS.
The same reference is used by the displaced full-Fock audit.
"""
from pathlib import Path
import argparse,itertools,json,time
import numpy as np
from joint_gaussian_instrument import Model,run


def controls(model,t,z,include_parasitics=True,include_odd=True):
    on=t<model.drive_time
    theta,dtheta=model.phases_at(t)
    delta=dtheta[None,:]*(model.eps_common+(model.odd*z if include_odd else 0.)) if on else np.zeros_like(z)
    coeff=[]
    for R,phi in zip(model.Rs,model.phases):
        eps=model.u*model.g3*model.alpha**(3-len(R)) if on and include_parasitics else 0.
        coeff.append(eps*np.prod(z[:,R],axis=1)*np.exp(-1j*(np.sum(theta[list(R)])-phi)))
    return delta,coeff,on


def classical_rhs(model,t,amplitudes,z,include_parasitics=True,include_odd=True):
    A=amplitudes[:,:3];B=amplitudes[:,3:]
    delta,coeff,on=controls(model,t,z,include_parasitics,include_odd)
    ua=2*model.g2*A.conj()*B+delta*A
    if on:
        S=np.prod(z,axis=1)
        for j in range(3):
            ua[:,j]+=model.g3*S*np.prod(A[:,[k for k in range(3) if k!=j]].conj(),axis=1)
        for R,kappa in zip(model.Rs,coeff):
            for j in R:
                other=[k for k in R if k!=j]
                ua[:,j]+=kappa.conj()*(np.prod(A[:,other].conj(),axis=1) if other else 1.)
    ub=model.g2*(A*A-model.n)
    return np.c_[-1j*ua,-1j*ub-(model.gamma-model.heat)*B/2]


def classical_trajectory(model,z=None,include_parasitics=True,include_odd=True):
    z=model.z if z is None else np.asarray(z)
    amp=np.zeros((len(z),6),complex);amp[:,:3]=model.alpha
    ts=[0.];amps=[amp.copy()]
    t=0.;stop=model.drive_time+model.ringdown
    step=model.dt/2
    while t<stop-1e-11:
        boundary=min(model.drive_time,(np.floor((t+1e-9)/model.segment)+1)*model.segment) if t<model.drive_time-1e-10 else stop
        dt=min(step,boundary-t,stop-t)
        if dt<1e-10:t=boundary;continue
        def f(tt,aa):return classical_rhs(model,tt,aa,z,include_parasitics,include_odd)
        k1=f(t+1e-10,amp);k2=f(t+dt/2,amp+dt*k1/2)
        k3=f(t+dt/2,amp+dt*k2/2);k4=f(t+dt-1e-10,amp+dt*k3)
        amp+=dt*(k1+2*k2+2*k3+k4)/6
        t+=dt;ts.append(t);amps.append(amp.copy())
    return np.array(ts),np.array(amps)


def trajectory_at(ts,amps,t):
    k=np.searchsorted(ts,t)
    if k==0:return amps[0]
    if k>=len(ts):return amps[-1]
    f=(t-ts[k-1])/(ts[k]-ts[k-1])
    return (1-f)*amps[k-1]+f*amps[k]


def hessian_and_affine(model,t,amplitudes,z):
    """Weyl quadratic H about exact classical means, in original c,b coords."""
    A=amplitudes[:,:3];B=amplitudes[:,3:];nb=len(z)
    G=np.zeros((nb,13,13));grad=np.zeros((nb,13))
    delta,coeff,on=controls(model,t,z)
    S=np.prod(z,axis=1)
    H=np.sum(2*model.g2*np.real((A*A-model.n)*B.conj())+delta*(abs(A)**2-.5),axis=1)
    ua=2*model.g2*A.conj()*B+delta*A
    ub=model.g2*(A*A-model.n)
    def pair_param(i,j,kappa):
        for p,q,val in [(2*i,2*j,kappa.real),(2*i+1,2*j+1,-kappa.real),
                        (2*i,2*j+1,-kappa.imag),(2*i+1,2*j,-kappa.imag)]:
            G[:,p,q]+=val;G[:,q,p]+=val
    for j in range(3):
        G[:,2*j,2*j]+=delta[:,j];G[:,2*j+1,2*j+1]+=delta[:,j]
        kappa=2*model.g2*A[:,j]
        for p,q,val in [(2*j,6+2*j,kappa.real),(2*j+1,7+2*j,kappa.real),
                        (2*j,7+2*j,kappa.imag),(2*j+1,6+2*j,-kappa.imag)]:
            G[:,p,q]+=val;G[:,q,p]+=val
        sq=model.g2*B[:,j].conj()
        G[:,2*j,2*j]+=2*sq.real;G[:,2*j+1,2*j+1]-=2*sq.real
        G[:,2*j,2*j+1]-=2*sq.imag;G[:,2*j+1,2*j]-=2*sq.imag
    if on:
        H+=2*model.g3*S*np.real(np.prod(A,axis=1))
        for j in range(3):
            ua[:,j]+=model.g3*S*np.prod(A[:,[k for k in range(3) if k!=j]].conj(),axis=1)
        for i,j in itertools.combinations(range(3),2):
            k=3-i-j
            pair_param(i,j,model.g3*S*A[:,k])
        for R,kappa in zip(model.Rs,coeff):
            H+=2*np.real(kappa*np.prod(A[:,R],axis=1))
            for j in R:
                other=[k for k in R if k!=j]
                ua[:,j]+=kappa.conj()*(np.prod(A[:,other].conj(),axis=1) if other else 1.)
            if len(R)==2:pair_param(R[0],R[1],kappa)
    grad[:,:6:2]=np.sqrt(2)*ua.real;grad[:,1:6:2]=np.sqrt(2)*ua.imag
    grad[:,6:12:2]=np.sqrt(2)*ub.real;grad[:,7:12:2]=np.sqrt(2)*ub.imag
    x=np.zeros((nb,13));ac=np.c_[A-model.alpha,B]
    x[:,:12:2]=np.sqrt(2)*ac.real;x[:,1:12:2]=np.sqrt(2)*ac.imag
    d=grad-(G@x[...,None])[...,0]
    h=H-np.sum(grad*x,axis=1)+.5*np.einsum('...i,...ij,...j->...',x,G,x)
    return G,d,h


class NonlinearMeanModel(Model):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.reference_times,self.reference_amplitudes=classical_trajectory(self)

    def matrices(self,t):
        old=super().matrices(t)
        amp=trajectory_at(self.reference_times,self.reference_amplitudes,t)
        G,d,h=hessian_and_affine(self,t,amp,self.z)
        il=np.r_[self.il,self.il];ir=np.r_[self.ir,self.ir]
        return G[il],G[ir],d[il],d[ir],h[il],h[ir],old[-2],old[-1]


class AlternatingNonlinearMeanModel(NonlinearMeanModel):
    """Reverse the orientation of successive complete closed 16-step cycles."""
    def phases_at(self,t):
        th,dth=super().phases_at(t)
        orientation=(-1.)**int(np.floor(t/self.cycle))
        return orientation*th,orientation*dth


def check_classical_formula():
    m=Model(modulated=False,cycles=1)
    m.u=0.;m.heat=0.
    out=[]
    for s,z in [(1,[[1,1,1]]),(-1,[[1,1,-1]])]:
        u=np.sqrt(1+3*m.nu*m.nu/4)-1j*s*m.nu/2
        A=m.alpha*u;B=-m.g3*s*A.conjugate()/(2*m.g2)
        rhs=classical_rhs(m,0,np.array([[A,A,A,B,B,B]]),np.array(z),False,False)
        out.append({'S':s,'A':[A.real,A.imag],'B':[B.real,B.imag],'residual':float(abs(rhs).max())})
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=['mod','unmod'],default='mod')
    p.add_argument('--odd',type=float,default=.0001);p.add_argument('--steps',type=int,default=32)
    p.add_argument('--label',default=None);p.add_argument('--cycles',type=int,default=16)
    p.add_argument('--alternate-cycles',action='store_true')
    a=p.parse_args();print(json.dumps({'exact_classical_steady_check':check_classical_formula()}),flush=True)
    cls=AlternatingNonlinearMeanModel if a.alternate_cycles else NonlinearMeanModel
    model=cls(modulated=a.case=='mod',odd=a.odd,steps_per_segment=a.steps,cycles=a.cycles)
    label=a.label or 'nonlinear_mean_'+a.case
    result=run(model,label)
    result['scope']='Exact classical mean / time-dependent Hessian Gaussian instrument. Nonlinear cubic fluctuation remainder remains.'
    result['parameters']['alternate_cycle_orientation']=a.alternate_cycles
    result['classical_reference_max_mean_mismatch']=float(np.max(np.abs(np.array(result['final_gauge_means'])[:,::2]+1j*np.array(result['final_gauge_means'])[:,1::2]-np.sqrt(2)*(model.reference_amplitudes[-1]-np.r_[np.full(3,model.alpha),np.zeros(3)]))))
    out=Path(__file__).parent/f'joint_{label}_results.json';out.write_text(json.dumps(result,indent=2)+'\n')
