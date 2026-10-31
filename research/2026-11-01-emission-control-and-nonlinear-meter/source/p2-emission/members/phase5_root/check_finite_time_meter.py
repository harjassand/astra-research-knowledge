"""Finite-time mean/Hessian Gaussian sensing with a fixed stored cat size.

All branches here are ideal parity branches; parasitic filtering and full
nonlinear Fock convergence are separate saved calculations, not silently
inherited by this speed comparison.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erfc

def realvec(z):
    r=np.empty(2*len(z));r[::2]=z.real;r[1::2]=z.imag
    return r

def jacobian(a,b,g2,g3,s,gamma):
    A=np.zeros((6,6),complex);B=np.zeros_like(A)
    A[:3,3:]=-2j*g2*np.diag(a.conj())
    A[3:,:3]=-2j*g2*np.diag(a)
    A[3:,3:]=-gamma/2*np.eye(3)
    B[:3,:3]=-2j*g2*np.diag(b)
    for j in range(3):
        for k in range(3):
            if j!=k:B[j,k]=-1j*g3*s*a[3-j-k].conjugate()
    J=np.empty((12,12))
    J[::2,::2]=(A+B).real;J[::2,1::2]=-(A-B).imag
    J[1::2,::2]=(A+B).imag;J[1::2,1::2]=(A-B).real
    return J

def run(nu,matched):
    alpha0=4.;g2=.125;gamma=10.;heat=.01;eta=.5
    alpha=alpha0/np.sqrt(1+nu*nu) if matched else alpha0
    g3=nu*4*alpha*g2*g2/gamma
    initial=np.r_[np.full(3,alpha0),np.zeros(3)].astype(complex)
    V=np.zeros((13,13));V[:12,:12]=.501*np.eye(12)
    y0=np.r_[realvec(initial),0.,V.ravel(),0.]
    D=np.zeros((13,13));D[6:12,6:12]=(gamma+heat)/2*np.eye(6)
    D[-1,-1]=1.
    for j in range(3):D[6+2*j,-1]=D[-1,6+2*j]=np.sqrt(eta*gamma/6)
    def rhs(t,y):
        z=y[:12:2]+1j*y[1:12:2];a=z[:3];b=z[3:]
        da=-2j*g2*a.conj()*b
        for j in range(3):da[j]-=1j*g3*np.prod(np.delete(a.conj(),j))
        db=-1j*g2*(a*a-alpha*alpha)-(gamma-heat)*b/2
        V=y[13:182].reshape(13,13)
        J=np.zeros((13,13));J[:12,:12]=jacobian(a,b,g2,g3,1,gamma-heat)
        for j in range(3):J[-1,6+2*j]=-np.sqrt(2*eta*gamma/3)
        dV=J@V+V@J.T+D
        dm=-2*np.sqrt(eta*gamma/3)*np.sum(b.real)
        pop=sum(abs(a[j])**2+(V[2*j,2*j]+V[2*j+1,2*j+1]-1)/2 for j in range(3))
        return np.r_[realvec(np.r_[da,db]),dm,dV.ravel(),pop]
    t=np.linspace(0,160,8001)
    sol=solve_ivp(rhs,(0,160),y0,t_eval=t,method='DOP853',rtol=2e-8,atol=1e-10,max_step=.12)
    if not sol.success:raise RuntimeError(sol.message)
    var=sol.y[13+168]
    assignment=.5*erfc(sol.y[12]/np.sqrt(2*np.maximum(var,1e-100)))
    rows=[]
    for target in (1e-4,1e-7):
        found=np.flatnonzero(assignment<=target)
        if not len(found):rows.append({'assignment_target':target,'reached':False});continue
        k=found[0];z=sol.y[:12:2,k]+1j*sol.y[1:12:2,k]
        rows.append({'assignment_target':target,'reached':True,'sensing_time':float(t[k]),
                     'assignment_at_time':float(assignment[k]),'total_storage_photon_exposure':float(sol.y[-1,k]),
                     'mean_storage_number_at_read':float(np.mean(abs(z[:3])**2)),
                     'max_mean_storage_number_so_far':float(np.max(abs(sol.y[:6:2,:k+1]+1j*sol.y[1:6:2,:k+1])**2)),
                     'mean_buffer_amplitude_at_read':[float(np.mean(z[3:]).real),float(np.mean(z[3:]).imag)]})
    return {'nu':nu,'stored_photons':16,'matched_operating_amplitude':matched,
            'pump_cat_amplitude':float(alpha),'g3':float(g3),'cases':rows}

def main():
    rows=[run(nu,matched) for nu,matched in ((.2,False),(.5,True),(1.,True),(2.,True))]
    out={'cases':rows,'scope':'Finite-time exact classical mean plus Hessian Gaussian fluctuations/readout. Includes buffer heating and all three ports; initial gauge thermal occupation.001. Excludes parasitic drives, physical phase-cycle error, stopping/return, state loading, X readout and storage-jump feedback. Those costs must not be omitted in a complete operation.'}
    dest=Path(__file__).with_name('finite_time_meter_results.json')
    dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
