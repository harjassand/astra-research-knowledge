"""Independent finite-Fock Lindblad check of the exact mapping-overlap law.

This compares the full off-diagonal data density block, not a jump count or
an endpoint coherent mean. All storage-loss jump and no-jump terms remain.
Finite-Fock convergence is checked only for the specified thermal examples;
the arbitrary-state result is proved analytically, not inferred from cutoff.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp, quad
from bracketed_parity_meter import Model, envelope, mapping_theta


def analytic(model, lam, nbar, area_error=0.):
    T=model.mapping_time
    theta=lambda t:(1+area_error)*float(mapping_theta(t,model))
    chi=lambda t:(1+area_error)*model.chi*float(envelope(t,T,model.ramp_chi))
    # For general endpoint angle the surviving storage contributes its own
    # phase to the compressed one-particle overlap as well as the outlet.
    M=np.exp(-model.ka*T-2j*theta(T))+model.ka*quad(
        lambda t:np.exp(-model.ka*t)*np.cos(2*theta(t)),0,T,epsabs=1e-13)[0]
    M+=-1j*model.ka*quad(lambda t:np.exp(-model.ka*t)*np.sin(2*theta(t)),0,T,epsabs=1e-13)[0]
    C=1-M
    K=quad(lambda t:chi(t)*np.exp(-model.ka*t),0,T,epsabs=1e-11)[0]
    # The simple displaced-number compression holds for the compensated
    # force and any endpoint angle; the final-mode overlap supplies the
    # boundary term that cancels the action's linear coherent-input phase.
    return np.exp(2j*lam**2*K)/(1+nbar*C)*np.exp(-C*lam**2/(1+nbar*C))


def lindblad(model,lam,nbar,cutoff,area_error=0.):
    N=cutoff
    nn=np.arange(N)
    nsum=nn[:,None]+nn[None,:]
    rt=np.sqrt(np.arange(1,N))
    jumpweight=rt[:,None]*rt[None,:]
    prob=(nbar/(1+nbar))**nn/(1+nbar) if nbar else np.eye(1,N)[0]
    rho0=np.diag(prob).astype(complex)
    def rhs(t,y):
        rho=y.reshape(N,N)
        chi=(1+area_error)*model.chi*float(envelope(t,model.mapping_time,model.ramp_chi))
        u=lam*chi*np.exp(-model.ka*t/2)
        out=(-1j*chi-model.ka/2)*nsum*rho
        drive=np.zeros_like(rho)
        drive[:-1,:]+=rt[:,None]*rho[1:,:]
        drive[1:,:]+=rt[:,None]*rho[:-1,:]
        drive[:,:-1]+=rt[None,:]*rho[:,1:]
        drive[:,1:]+=rt[None,:]*rho[:,:-1]
        out-=1j*u*drive
        out[:-1,:-1]+=model.ka*jumpweight*rho[1:,1:]
        return out.ravel()
    sol=solve_ivp(rhs,[0,model.mapping_time],rho0.ravel(),method='DOP853',
                  rtol=2e-10,atol=3e-13,max_step=.025)
    return complex(np.trace(sol.y[:,-1].reshape(N,N))),bool(sol.success),float(1-prob.sum())


def main():
    model=Model()
    rows=[]
    for nbar in [0.,.01,.3]:
        exact=analytic(model,1.5,nbar)
        vals=[]
        for cut in [40,60]:
            val,ok,tail=lindblad(model,1.5,nbar,cut)
            vals.append(val)
            row=dict(nbar=nbar,cutoff=cut,success=ok,initial_thermal_tail=tail,
                     predicted_real=exact.real,predicted_imag=exact.imag,
                     lindblad_real=val.real,lindblad_imag=val.imag,
                     absolute_residual=abs(val-exact),
                     dephasing_after_known_phase=(1-abs(val))/2)
            rows.append(row)
            print(row,flush=True)
    imperfections=[]
    zero_loss=Model(ka=0.)
    for err in [0.,1e-4,1e-3,.01]:
        for nbar in [0.,.3,3.]:
            val=analytic(zero_loss,1.5,nbar,err)
            imperfections.append(dict(relative_area_error=err,mapping_nbar=nbar,
                                      same_parity_pZ_after_phase=(1-abs(val))/2))
    Path(__file__).with_name('mapping_loss_checks.json').write_text(json.dumps(
        dict(cases=rows,area_error_without_storage_loss=imperfections,
             scope='Specified unconditioned thermal mapping block; not a repeated logical error rate.'),indent=2)+'\n')


if __name__=='__main__':
    main()
