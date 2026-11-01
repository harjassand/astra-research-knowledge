"""Independent Weyl-feedback and continuum cold-port bound verification."""
import json
import numpy as np
from scipy.linalg import expm
from scipy.integrate import cumulative_trapezoid
from scipy.special import gammaln
from numpy.polynomial.hermite import hermgauss


def fock_heterodyne_check(cutoff=32,quadrature=52):
    a=np.diag(np.sqrt(np.arange(1,cutoff,dtype=float)),1).astype(complex)
    q=(a+a.conj().T)/np.sqrt(2)
    p=(a-a.conj().T)/(1j*np.sqrt(2))
    L=np.array([.4,.7]);k=np.array([.2,-.3])
    omega=np.array([[0,1],[-1,0]])
    phase=.21;s=1.;sp=-.5;delta=s-sp
    nbar=.4;V=(nbar+.5)*np.eye(2)
    rho=np.diag([(nbar**n)/(nbar+1)**(n+1) for n in range(cutoff)])
    rho/=np.trace(rho)
    generator=L[0]*q+L[1]*p
    A=expm(1j*s*generator)@rho@expm(-1j*sp*generator)
    points,weights=hermgauss(quadrature)
    root_factorial=np.exp(gammaln(np.arange(cutoff)+1)/2)
    integral=0j
    for ix,x in enumerate(points):
        for iy,y in enumerate(points):
            alpha=x+1j*y
            coherent_polynomial=alpha**np.arange(cutoff)/root_factorial
            qsymbol=np.vdot(coherent_polynomial,A@coherent_polynomial)
            feedback=np.exp(-1j*delta*np.sqrt(2)*(k[0]*x+k[1]*y))
            integral+=weights[ix]*weights[iy]/np.pi*qsymbol*feedback
    actual=np.exp(1j*phase*(s*s-sp*sp))*integral
    variance=(L-k)@V@(L-k)+.5*(k@k)
    effective_phase=phase-.5*L@omega@k
    predicted=np.exp(1j*effective_phase*(s*s-sp*sp)-.5*delta*delta*variance)
    no_phase_correction=np.exp(1j*phase*(s*s-sp*sp)-.5*delta*delta*variance)
    return {
        "fock_cutoff":cutoff,
        "heterodyne_nodes_per_quadrature":quadrature,
        "exact_coherence_real":float(actual.real),
        "exact_coherence_imag":float(actual.imag),
        "weyl_formula_error":float(abs(actual-predicted)),
        "variance_only_formula_error":float(abs(actual-no_phase_correction)),
        "intended_phase":phase,
        "actual_feedback_gate_phase":float(effective_phase),
    }


def continuum_check():
    kh=.3;kc=1.;kap=kh+kc;duration=2.;target_phase=.4
    t=np.linspace(0,duration,12001)
    nu=2*np.pi/duration
    r=np.sqrt(target_phase/(2*np.pi))
    beta=r*(np.exp(1j*nu*t)-1)
    betadot=1j*nu*r*np.exp(1j*nu*t)
    f=1j*(betadot+kap*beta/2)
    trap=lambda z:np.trapezoid(z,t)
    phase=-float(np.real(trap(f*beta.conj())))
    drive_energy=float(np.real(trap(abs(f)**2)))
    rows=[]
    for cancellation_fraction in (0.,.5,.9,1.):
        # General complex perturbation ensures that this is not only a real
        # scalar gain identity except in the exact-cancellation row.
        extra=(1-cancellation_fraction)*.08*np.exp(3j*nu*t)
        w=-cancellation_fraction*f/np.sqrt(kc)+extra
        u=f+np.sqrt(kc)*w
        weighted=np.exp(-kap*t/2)*u
        backwards=-cumulative_trapezoid(weighted[::-1],t[::-1],initial=0)[::-1]
        backward_response=np.exp(kap*t/2)*backwards
        effective=phase-np.sqrt(kc)*float(np.real(trap(w*beta.conj())))
        by_u=-float(np.real(trap(u*beta.conj())))
        by_q=float(np.imag(trap(backward_response*f.conj())))
        q_energy=float(np.real(trap(abs(backward_response)**2)))
        hot_exponent_per_variance=abs(backward_response[0])**2+kh*q_energy
        lower=kh*effective*effective/drive_energy
        rows.append({
            "cancellation_fraction":cancellation_fraction,
            "effective_phase":effective,
            "direct_u_phase_error":float(abs(effective-by_u)),
            "volterra_phase_identity_error":float(abs(effective-by_q)),
            "hot_exponent_per_unit_V_and_unit_gap":float(hot_exponent_per_variance),
            "proved_lower_bound":float(lower),
            "bound_slack":float(hot_exponent_per_variance-lower),
        })
    return {"kappa_hot":kh,"kappa_cold":kc,"duration":duration,"drive_energy":drive_energy,"checks":rows}


def main():
    fock=fock_heterodyne_check()
    continuum=continuum_check()
    passed=(fock["weyl_formula_error"]<1e-10
            and max(r["volterra_phase_identity_error"] for r in continuum["checks"])<1e-6
            and min(r["bound_slack"] for r in continuum["checks"])>=-1e-12)
    print(json.dumps({"fock_heterodyne":fock,"continuum":continuum,"passed":passed},indent=2))
    if not passed:raise SystemExit(1)


if __name__=="__main__":main()
