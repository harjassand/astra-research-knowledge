"""Checks the full covariant ME->M CPTP region and exact signal recurrence."""
import json
import math
from pathlib import Path
import numpy as np

I=np.eye(2,dtype=complex)
P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),
   np.diag([1,-1]).astype(complex)]
K=np.kron(P[0],P[1])-np.kron(P[1],P[0])
SM=[np.kron(P[2],I),np.kron(I,P[2]),K]

def levi(i,j,k):
    if len({i,j,k})<3:return 0
    return 1 if (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)] else -1

def choi(alpha,beta,gamma):
    observables=[]
    for i in range(3):
        f=alpha*np.kron(P[i],I)+beta*np.kron(I,P[i])
        f+=gamma*sum(levi(i,j,k)*np.kron(P[j],P[k]) for j in range(3) for k in range(3))
        observables.append(f)
    return (np.eye(8)+sum(np.kron(p,f.T) for p,f in zip(P,observables)))/2

def sample_channel(rng):
    total=rng.uniform(-.5,1.)
    radius=math.sqrt((1+2*total)/3)*math.sqrt(rng.random())
    angle=rng.uniform(0,2*math.pi)
    difference=radius*math.cos(angle)
    gamma=radius*math.sin(angle)/2
    return (total+difference)/2,(total-difference)/2,gamma

def step(vector,theta,control):
    a,b,z=vector;alpha,beta,gamma=control
    c,s=math.cos(theta),math.sin(theta)
    return np.array([c*c*a,alpha*b+s*s*beta*a-2*s*s*gamma*z,
                     -c*s*beta*a+(c*c*alpha+c*s*gamma)*z])

def direct_step(vector,theta,control):
    j=choi(*control)
    values,vectors=np.linalg.eigh(j)
    kraus=[math.sqrt(max(0,e))*v.reshape(2,4)
           for e,v in zip(values,vectors.T) if e>1e-13]
    swap=np.zeros((8,8),complex)
    for bits in range(8):
        a=(bits>>2)&1;b=bits&1
        target=bits^((a^b)<<2)^(a^b)
        swap[target,bits]=1
    unitary=math.cos(theta)*np.eye(8)+1j*math.sin(theta)*swap
    delta=sum(a*x for a,x in zip(vector,SM))/4
    state=unitary@np.kron(delta,I/2)@unitary.conj().T
    out=sum(np.kron(I,k)@state@np.kron(I,k).conj().T for k in kraus)
    return np.array([np.trace(SM[0]@out).real,np.trace(SM[1]@out).real,
                     np.trace(K@out).real/2])

def main():
    rng=np.random.default_rng(170191)
    err=0.;tp_err=0.;mineig=1.;control_excess=0.;c_excess=0.;b_excess=0.;count=0
    for theta in [.01,.1,.3,.7,1.3]:
        c,s=math.cos(theta),math.sin(theta);kappa=(3-c)/4
        controls=[sample_channel(rng) for _ in range(50)]
        controls += [(math.cos(phi)**2,math.sin(phi)**2,math.cos(phi)*math.sin(phi))
                     for phi in [0,theta/2,theta,-theta,math.pi/2]]
        controls += [(-1/3,0,0),(0,-1/3,0),(-.25,-.25,0),(0,0,0)]
        for control in controls:
            j=choi(*control)
            mineig=min(mineig,float(np.linalg.eigvalsh(j).min()))
            tp=np.trace(j.reshape(2,4,2,4),axis1=0,axis2=2)
            tp_err=max(tp_err,float(np.linalg.norm(tp-np.eye(4))))
            vector=rng.normal(size=3)
            err=max(err,float(np.max(np.abs(step(vector,theta,control)-direct_step(vector,theta,control)))))
            alpha,beta,gamma=control
            control_excess=max(control_excess,abs(c*alpha+s*gamma)+kappa*abs(beta)-1)
            assert abs(alpha)+abs(beta)<=1+1e-12
            assert gamma*gamma<=1-abs(alpha)+1e-12
            count+=1
        for mode in ['random','matched','half_matched']:
            signal=np.array([1.,0.,0.]);b_bound=min(1.,s*s*(1+2/kappa))
            for n in range(1,5001):
                if mode=='random':control=controls[int(rng.integers(len(controls)))]
                else:
                    phi=theta if mode=='matched' else theta/2
                    control=(math.cos(phi)**2,math.sin(phi)**2,math.cos(phi)*math.sin(phi))
                signal=step(signal,theta,control)
                c_excess=max(c_excess,abs(signal[2])-(s/kappa)*c**n)
                b_excess=max(b_excess,abs(signal[1])-b_bound)
    theta=.1;c=math.cos(theta);s=math.sin(theta);kappa=(3-c)/4
    result={'scope':'Nonselective time-dependent SU(2)-covariant ME->M CPTP maps, tracial initial memory; no retained instrument outcomes',
            'direct_matrix_channel_checks':count,'maximum_recurrence_error':err,
            'maximum_TP_residual':tp_err,'minimum_choi_eigenvalue':mineig,
            'maximum_control_inequality_excess':control_excess,
            'maximum_correlation_bound_excess':c_excess,'maximum_visibility_bound_excess':b_excess,
            'theta_0p1':{'visibility_upper_bound':s*s*(1+2/kappa),
                         'half_diamond_error_lower_bound':.75*(1-s*s*(1+2/kappa))}}
    assert err<1e-11
    assert mineig>-1e-11
    assert max(control_excess,c_excess,b_excess)<1e-11
    Path(__file__).with_name('covariant_qubit_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
