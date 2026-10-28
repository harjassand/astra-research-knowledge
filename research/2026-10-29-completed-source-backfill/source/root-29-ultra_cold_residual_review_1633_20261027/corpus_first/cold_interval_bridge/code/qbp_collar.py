"""Bounded QBP collar and its actual temperature-logarithmic residual.

Finite matrix/ODE diagnostics. No ODE output is promoted to a rigorous
interval without a separate residual enclosure.
"""
import sys
sys.dont_write_bytecode = True
import json,time
import numpy as np
from scipy.linalg import eigh,svdvals
from scipy.integrate import solve_ivp
from seam_residual import LocalSeam,sector,bond,BASE


def qbp_pair(H0,V,beta):
    d=len(H0);identity=np.eye(d)
    def rhs(lam,vector):
        O=vector[:d*d].reshape(d,d);Y=vector[d*d:].reshape(d,d)
        w,U=eigh(H0+lam*V)
        omega=w[:,None]-w[None,:];x=beta*omega/2
        g=np.full_like(omega,-beta/2)
        np.divide(-np.tanh(x),omega,out=g,where=np.abs(omega)>1e-12)
        dg=-.5/np.cosh(x)**2
        transformed=U.T@V@U
        F=U@(g*transformed)@U.T;dF=U@(dg*transformed)@U.T
        return np.concatenate([(F@O).ravel(),(F@Y+dF@O).ravel()])
    initial=np.concatenate([identity.ravel(),np.zeros(d*d)])
    sol=solve_ivp(rhs,(0,1),initial,method='DOP853',rtol=2e-11,atol=2e-12)
    assert sol.success
    O=sol.y[:d*d,-1].reshape(d,d);Y=sol.y[d*d:,-1].reshape(d,d)
    return O,Y,sol.nfev


def measure(ell,beta):
    seam=LocalSeam(ell);local={};derivatives={};D0s=[];checks=[];calls=0
    for m in range(-2,3):
        states,lookup=sector(2*ell,m)
        V=bond(states,lookup,ell-1,ell).toarray()
        (w,U),(w0,U0)=seam.spectra[m]
        H0=(U0*w0)@U0.T;H=(U*w)@U.T
        O,Y,nfev=qbp_pair(H0,V,beta);calls+=nfev
        inverse=np.linalg.inv(O)
        D0=Y@inverse+H/2-(O@H0@inverse)/2
        D0s.append(float(svdvals(D0)[0]));local[m]=O;derivatives[m]=Y
        target=(U*np.exp(-beta*w))@U.T
        got=O@((U0*np.exp(-beta*w0))@U0.T)@O.T
        checks.append(float(np.linalg.norm(got-target)/np.linalg.norm(target)))
    d=len(seam.states);E=np.zeros((d,d));inverse=np.zeros((d,d))
    for ix,order,m in seam.blocks:
        E[np.ix_(ix,ix)]=local[m][np.ix_(order,order)]
        inverse[np.ix_(ix,ix)]=np.linalg.inv(local[m])[np.ix_(order,order)]
    R=(seam.hout@E-(seam.hout@E.T).T)@inverse
    cnorm=float(svdvals(R)[0]);D0norm=max(D0s)
    return dict(ell=ell,beta=beta,
        expansional_norm=max(float(svdvals(O)[0])for O in local.values()),
        inside_logarithmic_residual_norm=D0norm,
        one_edge_logarithmic_commutator_norm=cnorm,
        per_seam_residual_triangle_upper_numeric=D0norm+cnorm,
        local_QBP_Gibbs_identity_relative_error=max(checks),ODE_rhs_evaluations=calls)


def run():
    start=time.monotonic();rows=[]
    for ell in (1,2):
        for beta in (.125,.25,.5,.75,1.,1.5):
            row=measure(ell,beta);rows.append(row)
            print(ell,beta,'norm',row['expansional_norm'],'residual',row['per_seam_residual_triangle_upper_numeric'],flush=True)
    result=dict(status='BOUNDED_QBP_COLLAR_NUMERIC_REPAIR_EXECUTED_NOT_INTERVAL_CERTIFICATE',
        rows=rows,elapsed_seconds=time.monotonic()-start,
        scope='Actual spin2 finite collars, including derivative with respect to beta. Norm control alone does not imply a small global normalized-purity error.')
    (BASE/'results/QBP_COLLAR_DISCOVERY.json').write_text(json.dumps(result,indent=2)+'\n')
    print('elapsed',result['elapsed_seconds'])


if __name__=='__main__':run()
