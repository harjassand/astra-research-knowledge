"""Finite physical checks for the root's renewable geometric-reference mechanism.

Scope: scalar common-length load paths, harmonic series transducers, ideal
passive circuit for a finite time window, and quasistatic actuator work. No
claim of a fabricated device, unlimited static piezo readout or fault-free meter.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad


def series_transducer():
    kb,kp,h,b,bm=2.,3.,.4,.5,.3
    signs=np.array([1.,-1.,0.])
    hs=h*signs
    n=3
    # Variables are three piezo extensions y_i and common series charge Q.
    H=np.zeros((n+1,n+1))
    H[:n,:n]=(kb+kp)*np.eye(n)
    H[:n,n]=H[n,:n]=-hs
    H[n,n]=n*b+bm
    assert np.linalg.eigvalsh(H).min()>0
    keff=kb*kp/(kb+kp)
    theta=kb*hs/(kb+kp)
    beff=n*b+bm-np.sum(hs**2)/(kb+kp)
    assert beff-np.sum(theta**2)/keff>0
    defect=np.array([.03,0,0])
    predicted=-theta@defect/beff
    readouts=[]
    for L in [-.5,0,.2,1.1]:
        g=np.r_[-kb*(L-defect),0.]
        means=np.linalg.solve(H,-g)
        assert abs(means[-1]-predicted)<1e-15
        readouts.append(dict(common_extension=L,charge_mean=float(means[-1])))
    variance=np.linalg.inv(H)[-1,-1] # units kBT=1
    assert abs(variance-1/beff)<1e-15
    # A parallel piezo patch couples to actual extension, not the damage-bearing
    # spring's elastic extension; differential sum is identically zero.
    parallel_charge=(hs.sum()*.2)/(n*b+bm)
    assert parallel_charge==0
    incompat_energy=.5*keff*np.sum((defect-defect.mean())**2)
    snr2=predicted**2/variance
    assert snr2<=2*incompat_energy+1e-15
    return dict(k_effective=keff,theta=theta.tolist(),charge_curvature=beff,
                charge_variance_kBT1=float(variance),readouts=readouts,
                parallel_patch_charge=parallel_charge,
                squared_snapshot_SNR=snr2,energy_bound=2*incompat_energy)


def nonlinear_false_signal():
    values=[]
    for eps in [.001,.01,.05,.1]:
        exact=eps/np.sqrt(2)-(np.sqrt((1+eps)**2+1)-np.sqrt(2))
        asymptotic=-eps**2/(4*np.sqrt(2))
        values.append(dict(horizontal_strain=eps,false_syndrome=float(exact),
                           leading_quadratic=float(asymptotic)))
    return values


def nonlinear_zero_copy():
    # Same strictly increasing nonlinear force law on all three paths.
    force=lambda e: e+2*e**3
    ls=np.array([1.,1.,1.03])
    ans=[]
    for L in [.5,1.1,2.]:
        fs=np.array([force(L-l) for l in ls])
        ref=np.median(fs)
        corrected=brentq(lambda ell:force(L-ell)-ref,.5,1.5)
        assert abs(corrected-1)<1e-12
        assert np.array_equal(np.argsort(fs),np.argsort(-ls,kind='stable'))
        ans.append(dict(common_length=L,forces=fs.tolist(),copied_rest_length=corrected))
    return ans


def renewal_work():
    k,F,l0=3.,2.,1.
    cases=[]
    for Delta in [-.1,.01,.1]:
        li=np.array([l0,l0,l0+Delta])
        lf=np.array([l0,l0,l0])
        def G(ell):
            L=ell.mean()+F/(3*k)
            return .5*k*np.sum((L-ell)**2)-F*L
        exact=G(lf)-G(li)
        predicted=F*Delta/3-k*Delta**2/3
        assert abs(exact-predicted)<1e-14
        # Quasistatic branch force while moving rest length from l0+Delta to l0.
        force=lambda ell_j: F/3-2*k*(ell_j-l0)/3
        integral=-quad(force,l0+Delta,l0)[0]
        assert abs(integral-exact)<1e-14
        cases.append(dict(defect=Delta,external_force=F,
                          reversible_work=exact,force_integral=integral))
    return cases


def finite_window():
    tau=1.
    leak=100.
    # Variance of uniform temporal mean of a stationary OU meter, v=1.
    def varmean(T):
        return 2*(tau/T-(tau/T)**2*(-np.expm1(-T/tau)))
    # Start with meter at zero; source decays from a known input step at t=0.
    def response(t):
        return leak/(leak-tau)*(np.exp(-t/leak)-np.exp(-t/tau))
    def meanresponse(T):
        return leak/(leak-tau)/T*(leak*(-np.expm1(-T/leak))-tau*(-np.expm1(-T/tau)))
    cases=[]
    for T in [.1,1.,10.,100.,1000.]:
        numerical=quad(response,0,T)[0]/T
        m=meanresponse(T)
        assert abs(m-numerical)<1e-11
        cases.append(dict(T=T,mean_signal=m,variance=varmean(T),
                           squared_SNR=m*m/varmean(T)))
    opt=minimize_scalar(lambda z:-meanresponse(np.exp(z))**2/varmean(np.exp(z)),
                        bounds=(np.log(.01),np.log(1e5)),method='bounded')
    # Uniform-average optimum only; not an information bound over all estimators.
    return dict(tau_meter=tau,tau_leak=leak,cases=cases,
                optimum_average_duration=float(np.exp(opt.x)),
                optimum_average_squared_SNR=float(-opt.fun))


def main():
    result=dict(series_transducer=series_transducer(),
                generic_frame_nonlinearity=nonlinear_false_signal(),
                identical_nonlinear_paths=nonlinear_zero_copy(),
                renewal_under_load=renewal_work(),finite_RC_window=finite_window())
    Path(__file__).with_name('meter_renewal_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
