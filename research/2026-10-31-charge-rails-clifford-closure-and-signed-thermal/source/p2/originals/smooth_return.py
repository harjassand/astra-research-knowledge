"""Supply a finite, smooth, symmetry-preserving quarter-X pulse.

The actual four-charge-state Hamiltonian retains its fixed Delta.
Two numerical pulse parameters repair a cosine-ramped positive hopping.
This is not a multiband device calculation or an interval root certificate.
"""
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
from scipy.linalg import expm
HERE=Path(__file__).resolve().parent
Hc=np.diag([0.,0.,1.,1.]).astype(complex)
Ht=np.array([[0,0,-1,-1],[0,0,-1,-1],[-1,-1,0,0],[-1,-1,0,0]],complex)
Hd=np.diag([0.,0.,1.,-1.]);E=np.eye(4)[:,:2];X=np.array([[0,1],[1,0]],complex);Z=np.diag([1.,-1.])
def norm(a):return float(np.linalg.norm(a,2))
RISE=.25
def shape(t,total):
    if t<RISE:return math.sin(math.pi*t/(2*RISE))**2
    if t>total-RISE:return math.sin(math.pi*(total-t)/(2*RISE))**2
    return 1.
def doublet(parameters):
    amp,total=parameters
    def rhs(t,y):
        h=np.array([[0.,-2*amp*shape(t,total)],[-2*amp*shape(t,total),1.]])
        return (-1j*h@y.reshape(2,2)).reshape(-1)
    sol=solve_ivp(rhs,[0,total],np.eye(2,dtype=complex).reshape(-1),method='DOP853',rtol=2e-12,atol=2e-14,max_step=.05)
    return sol.y[:,-1].reshape(2,2)
def equations(x):
    u=doublet(x);total=x[1]
    return [float((np.exp(1j*total/2)*u[1,0]).imag),float(np.angle(u[0,0]/1j))]
def physical(parameters,delta=0.,omega=1.):
    amp,total=parameters;eye=np.eye(2)
    hb=np.kron(np.eye(4),omega*Z/2);error=delta*np.kron(Hd,X)
    def rhs(t,y):
        h=np.kron(Hc+amp*shape(t,total)*Ht,eye)+hb+error
        return (-1j*h@y.reshape(8,8)).reshape(-1)
    sol=solve_ivp(rhs,[0,total],np.eye(8,dtype=complex).reshape(-1),method='DOP853',rtol=2e-12,atol=2e-14,max_step=.05)
    return sol.y[:,-1].reshape(8,8)
def main():
    answer=root(equations,[.47,math.pi+.15],tol=1e-10)
    if not answer.success or norm(np.asarray(equations(answer.x)).reshape(-1,1))>1e-9:raise RuntimeError(str(answer))
    amp,total=answer.x;u=doublet(answer.x)
    target=np.exp(1j*math.pi/4)*expm(1j*math.pi*X/4)
    embedding=np.kron(E,np.eye(2));p=embedding@embedding.conj().T;rows=[]
    for omega in [0.,1.,7.]:
        ideal=physical(answer.x,0.,omega)@embedding
        for delta in [.01,.003]:
            actual=physical(answer.x,delta,omega)@embedding
            rows.append(dict(source_frequency=omega,dipole_strength=delta,
                raw_error=norm(actual-ideal),accepted_error=norm(p@actual-ideal),
                worst_reject_probability=norm((np.eye(8)-p)@actual)**2,
                accepted_bound=.5*(delta*total)**2))
    exact=physical(answer.x,0.,0.)@embedding
    expected=embedding@np.kron(target,np.eye(2))
    out=dict(scope='Finite smooth pulse in the fixed orbital Hamiltonian; ordinary ODE/root precision, not certified enclosure.',
        rise_time=RISE,peak_t_over_Delta=float(amp),total_time_hbar_over_Delta=float(total),
        maximum_hopping_slew=float(amp*math.pi/(2*RISE)),
        doublet_return_residual=norm(u[:,0]-np.array([1j,0])),
        full_charge_spin_identity_gate_error=norm(exact-expected),
        quantum_source_checks=rows)
    (HERE/'smooth_return_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
