"""Numerical discriminating checks for the frozen independent derivation.

All measurements used for the scaling check are x_1 only. The simulation knows
the matrices to generate a synthetic benchmark, not to supply the estimator.
"""
import json
import numpy as np

def rk4(f,x,t,h):
    k1=f(t,x); k2=f(t+h/2,x+h*k1/2)
    k3=f(t+h/2,x+h*k2/2); k4=f(t+h,x+h*k3)
    return x+h*(k1+2*k2+2*k3+k4)/6

def matrix(theta,mu):
    co=np.cos(theta); si=np.sin(theta)
    transform=np.array([[1,0,0],[0,co,-si],[0,si,co]])
    modal=np.array([[2.,-1,0],[-1,2,0],[0,0,mu]])
    return transform@modal@transform.T

amps=np.array([0.03,0.05,0.08,0.12,0.2,0.32])
h=0.001; steps=8000
def raw_difference(theta):
    matrices=np.stack([matrix(theta,mu) for mu in (3.,5.)])
    state=np.zeros((2,len(amps),3))
    maximum=np.zeros(len(amps))
    def f(t,x):
        force=1-np.exp(-2*t)
        val=-np.einsum('mij,maj->mai',matrices,x)-x**3
        val[:,:,0]+=amps*force
        return val
    for j in range(steps):
        state=rk4(f,state,j*h,h)
        maximum=np.maximum(maximum,abs(state[0,:,0]-state[1,:,0]))
    return maximum

generic=raw_difference(np.pi/8)
sync=raw_difference(np.pi/4)
delta_results=[]
for delta in (0.2,0.1,0.05,0.02):
    diff=raw_difference(np.pi/4-delta)[-1]
    delta_results.append(dict(delta=delta,max_difference_at_amplitude_0_32=float(diff),
                              difference_over_delta_squared=float(diff/delta**2)))

K0=np.array([[4.,-1,-1],[-1,4,0],[-1,0,4]])
K1=np.array([[4.,-1,-1],[-1,5,-1],[-1,-1,5]])

out=dict(counterexample_eigenvalues=[np.linalg.eigvalsh(K0).tolist(),
                                     np.linalg.eigvalsh(K1).tolist()],
         amplitudes=amps.tolist(),generic_max_output_difference=generic.tolist(),
         generic_difference_over_amplitude_fifth=(generic/amps**5).tolist(),
         adjacent_log_slopes=(np.diff(np.log(generic))/np.diff(np.log(amps))).tolist(),
         synchronized_max_output_difference=sync.tolist(),near_sync=delta_results,
         integration=dict(method='RK4',time_step=h,horizon=steps*h),
         status='synthetic finite checks; exact equal-I/O claim follows from invariant-subspace proof')
with open(__file__.replace('.py','_results.json'),'w') as f:
    json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
