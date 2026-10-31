"""Exact classical parity-meter centers, stability and stationary readout.

Static sensing estimates are NOT complete gate durations. This tests the
nonlinear correction to expanding about (alpha,0) at nonzero gate strength.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import solve_continuous_lyapunov
from scipy.special import ndtri

def realvec(v):
    z=np.empty(2*len(v));z[::2]=v.real;z[1::2]=v.imag
    return z

def field(r,alpha,g2,g3,gamma,parity):
    z=r[::2]+1j*r[1::2];a=z[:3];b=z[3:]
    da=-2j*g2*a.conj()*b
    for j in range(3):da[j]-=1j*g3*parity*np.prod(np.delete(a.conj(),j))
    db=-1j*g2*(a*a-alpha*alpha)-gamma*b/2
    return realvec(np.r_[da,db])

def case(nu,n=16.,G=1.,gamma=10.,eta=.5):
    alpha=np.sqrt(n);g2=G/(2*alpha);g3=nu*G*G/(gamma*alpha)
    center=alpha*(np.sqrt(1+3*nu*nu/4)-1j*nu/2)
    pointer=-g3*center.conjugate()/(2*g2)
    r=realvec(np.r_[np.full(3,center),np.full(3,pointer)])
    step=1e-5
    jac=np.column_stack([(field(r+np.eye(12)[j]*step,alpha,g2,g3,gamma,1)-
                          field(r-np.eye(12)[j]*step,alpha,g2,g3,gamma,1))/(2*step)
                         for j in range(12)])
    eig=np.linalg.eigvals(jac)
    G_eff=G*np.sqrt(1+nu*nu);h_eff=g3*abs(center)
    predicted=[]
    for multiplicity,delta in ((1,h_eff),(2,2*h_eff)):
        for sign in (-1,1):
            predicted.extend(list(np.roots([1,gamma/2+sign*delta,
                                            G_eff*G_eff+sign*delta*gamma/2]))*multiplicity)
    predicted=np.array(predicted)
    out={"nu":nu,"classical_storage_number":float(abs(center)**2),
         "classical_buffer_number":float(abs(pointer)**2),
         "center": [float(center.real),float(center.imag)],
         "pointer": [float(pointer.real),float(pointer.imag)],
         "steady_equation_residual":float(np.linalg.norm(field(r,alpha,g2,g3,gamma,1))),
         "linearization_max_real_eigenvalue":float(max(eig.real)),
         "analytic_poles_residual":float(max(min(abs(x-predicted)) for x in eig))}
    if max(eig.real)<-1e-8:
        D=np.zeros((12,12));D[6:,6:]=gamma/2*np.eye(6)
        V=solve_continuous_lyapunov(jac,-D)
        pops=np.array([(V[2*j,2*j]+V[2*j+1,2*j+1]-1)/2 for j in range(6)])
        B=np.zeros((12,6));B[6:,:]=-np.sqrt(gamma)*np.eye(6)
        weights=np.zeros(6);weights[::2]=1/np.sqrt(3)
        C=np.zeros(12);C[6:]=np.sqrt(gamma)*weights
        transfer=weights+C@np.linalg.solve(-jac,B)
        fano=(1-eta)+eta*np.vdot(transfer,transfer).real
        half_signal=2*np.sqrt(3*eta*gamma)*abs(pointer.real)
        info=half_signal**2/fano
        time=float(ndtri(1-1e-4)**2/info)
        out.update({"quadratic_fluctuation_numbers":pops.tolist(),
                    "sum_homodyne_zero_frequency_Fano":float(fano),
                    "steady_information_rate":float(info),
                    "stationary_time_for_assignment_1e4":time,
                    "stationary_per_cat_photon_exposure":float((abs(center)**2+pops[:3].max())*time)})
    return out

def main():
    rows=[case(nu) for nu in (.05,.1,.2,.5,1.,2.,4.,5.,8.)]
    out={"parameters":{"n":16.,"G":1.,"gamma":10.,"efficiency":.5},
         "cases":rows,
         "scope":"Exact classical fixed points and local Hessian stability; Gaussian stationary noise about those centers. Steady assignment estimates exclude turn-on, stop, loading, correction and transient covariance. No physical-device speed advantage is claimed."}
    path=Path(__file__).with_name("nonlinear_operating_point_results.json")
    path.write_text(json.dumps(out,indent=2)+"\n")
    summary=[]
    for row in rows:
        x={k:row[k] for k in ("nu","linearization_max_real_eigenvalue","analytic_poles_residual")}
        if "steady_information_rate" in row:
            x.update(steady_time=row["stationary_time_for_assignment_1e4"],exposure=row["stationary_per_cat_photon_exposure"])
        summary.append(x)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
