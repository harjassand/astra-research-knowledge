"""Reproducible checks of exact coherent receiver and exposure formulas.

No nonlinear oscillator approximation is certified here. The ODE comparison
is the declared linear, vacuum, conserved-data-Z model. Scientific checks
target the derived formulas and negative control, not the code implementation.
"""
from pathlib import Path
import itertools
import json
import numpy as np
from scipy.integrate import solve_ivp, simpson, quad
from scipy.special import erfc, erfcinv


def sine4(t, T, amp=1.0):
    x = np.pi * t / T
    s, c = np.sin(x), np.cos(x)
    r = np.pi / T
    return (amp*s**4,
            4*amp*r*s**3*c,
            4*amp*r*r*(3*s*s*c*c-s**4))


def closed_direct_test(T=8.0, a=0.8, chi=1.7, g=0.6):
    """Compare inverse-designed pointer with four exact classical branches."""
    ts=np.linspace(0,T,16001)
    z=np.array(list(itertools.product((1.,-1.),repeat=2)))
    def rhs(t,cavity):
        A,Ap,App=sine4(t,T)
        u=-(App+2*a*Ap+(a*a+chi*chi)*A)/chi
        return -(a+1j*chi*z[:,0])*cavity-1j*g*u*z[:,1]
    sol=solve_ivp(rhs,(0,T),np.zeros(4,complex),t_eval=ts,
                  rtol=2e-11,atol=2e-13)
    A,Ap,App=sine4(ts,T)
    b=(Ap+a*A)/chi
    exact=g*(A[None,:]*np.prod(z,axis=1)[:,None]+1j*b[None,:]*z[:,1,None])
    EA=simpson(A*A,x=ts);EB=simpson(b*b,x=ts)
    ratio=(a*a+16*np.pi*np.pi/(7*T*T))/(chi*chi)
    return {"maximum_amplitude_ODE_error":float(abs(sol.y-exact).max()),
            "maximum_final_cavity_amplitude":float(abs(sol.y[:,-1]).max()),
            "numerical_exposure_ratio":float(EB/EA),
            "analytic_exposure_ratio":float(ratio),
            "Wirtinger_lower_bound":float((a*a+np.pi*np.pi/T**2)/chi**2)}


def homodyne_overlap(alpha,beta,eta,theta):
    """Numerically integrate absolute corrected coherent-wavefunction overlap."""
    aa=np.sqrt(eta)*alpha*np.exp(-1j*theta)
    bb=np.sqrt(eta)*beta*np.exp(-1j*theta)
    def integrand(x):
        return np.exp(-((x-np.sqrt(2)*aa.real)**2+
                        (x-np.sqrt(2)*bb.real)**2)/2)/np.sqrt(np.pi)
    observed,_=quad(integrand,-np.inf,np.inf,epsabs=1e-12)
    lost=np.exp(-(1-eta)*abs(alpha-beta)**2/2)
    expected=np.exp(-((1-eta)*abs(alpha-beta)**2+
                      eta*np.real(np.exp(-1j*theta)*(alpha-beta))**2)/2)
    return float(lost*observed),float(expected)


def receiver_tests():
    examples=[(0.2+1.1j,-0.8+.5j,.35,.73),
              (1.0,-1.0,1.0,np.pi/2),
              (1.0,-1.0,.5,np.pi/2)]
    vals=[homodyne_overlap(*e) for e in examples]
    a=.7
    angles=np.linspace(0,np.pi,20001)
    best=np.max(np.minimum(np.exp(-2*a*a*np.cos(angles)**2),
                           np.exp(-2*a*a*np.sin(angles)**2)))
    return {"formula_checks":[{"integral":x,"formula":y,"error":abs(x-y)}
                              for x,y in vals],
            "nonisotropic_square_best_worst_homodyne_visibility":float(best),
            "square_analytic_bound":float(np.exp(-a*a)),
            "square_symplectic_area":float(4*a*a)}


def upstream_ledger(q=1e-3,eta=.5,T=8.,ac=1.,ae=1.):
    """Same q, actual source/corrector forces, variable chi, no hardware rates."""
    Nout=float(erfcinv(2*q)**2/(2*eta))
    # integral sin^8(pi t/T)=35 T/128
    amp=np.sqrt(Nout/(35*T/128))
    ts=np.linspace(0,T,20001)
    A,Ap,App=sine4(ts,T,amp)
    cases=[]
    for chi in [1.,2.,5.,10.]:
        kc=2*ac;ke=2*ae
        B=-(Ap+ac*A)/chi
        Bp=-(App+ac*Ap)/chi
        u=-(Bp+ae*B)/np.sqrt(ke)
        w=(Bp-ac*B-chi*A)/np.sqrt(kc)
        Npre=float(simpson(B*B,x=ts))
        losses=[]
        for tau in [.99,.999,.9999]:
            exponent=2*(1-tau)/tau*Npre
            losses.append({"tau":tau,"visibility":float(np.exp(-exponent)),
                           "equivalent_phase_flip_probability":float(-np.expm1(-exponent)/2)})
        cases.append({"chi_over_ac":chi/ac,"Nout":Nout,"Npre":Npre,
                      "ratio":Npre/Nout,
                      "ratio_lower_bound":(ac*ac+np.pi*np.pi/T**2)/(chi*chi),
                      "source_force_peak":float(abs(u).max()),
                      "corrector_force_peak":float(abs(w).max()),
                      "source_max_photons":float((B*B/ke).max()),
                      "corrector_max_photons":float(((A*A+B*B)/kc).max()),
                      "line_loss_cases":losses})
    return {"scope":"Illustrative dimensionless design ledger, not measured hardware or total gate errors.",
            "q":q,"eta":eta,"T":T,"ac":ac,"ae":ae,"pointer_peak":float(amp),
            "cases":cases}


def main():
    result={"direct_cavity":closed_direct_test(),"receiver":receiver_tests(),
            "upstream_ledger":upstream_ledger()}
    out=Path(__file__).with_name("receiver_and_cost_results.json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
