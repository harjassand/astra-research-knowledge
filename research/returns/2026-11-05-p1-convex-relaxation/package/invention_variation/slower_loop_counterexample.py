"""Preserved failure of extending minimum-time noise optimality to more time.

The curves below are exact specified controls in the same ideal OU model.
Floating quadrature and independent drift/noise ODEs are checked at three
tolerances. These are numerical residual/convergence checks, not experimental
data or a rigorous interval-arithmetic certificate. An analytic first-
variation argument in slower_loop_derivation.txt proves the local failure
without relying on the finite example's numerical sign.
"""
from pathlib import Path
import json
import math
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.optimize import brentq
from gradient_rotation import rotation,J

HERE=Path(__file__).resolve().parent
THETA=math.pi/2
L=math.sqrt(THETA*THETA+2*math.pi*THETA)
S=L+.05
CAP=1.
DIFFUSION=1.
DRAG=1.
C0=np.array([[1.,.2],[.2,1.7]])


def H(z):
    return np.array([[z.real,z.imag],[z.imag,-z.real]])


def geometry(u,a,eps):
    su,cu=math.sin(u),math.cos(u)
    rho=a*su*(1+eps*math.sin(2*u))
    rp=a*(cu*(1+eps*math.sin(2*u))+2*eps*su*math.cos(2*u))
    z=rho*complex(math.cos(u-math.pi/2),math.sin(u-math.pi/2))
    zp=(rp+1j*rho)*complex(math.cos(u-math.pi/2),math.sin(u-math.pi/2))
    den=1-rho*rho
    ld=math.sqrt(rp*rp+rho*rho)/den
    bd=rho*rho/den
    f=1/math.sqrt(den);fp=rho*rp/(den**1.5)
    B=f*(np.eye(2)+H(z))
    Bp=fp*(np.eye(2)+H(z))+f*H(zp)
    return ld,bd,B,Bp


def compile_loop(eps):
    def area(a):
        return quad(lambda u:geometry(u,a,eps)[1],0,math.pi,
                    epsabs=2e-12,epsrel=2e-12)[0]
    a=brentq(lambda a:area(a)-THETA,1e-6,.999/(1+abs(eps)),
             xtol=1e-14,rtol=1e-14)
    K=quad(lambda u:geometry(u,a,eps)[0],0,math.pi,
           epsabs=2e-12,epsrel=2e-12)[0]
    assert K<=S
    return dict(epsilon=eps,a=a,shape_length=K,
                holonomy_quadrature=area(a),geometric_time=2*K/CAP,
                cooling_time=(S-K)/CAP,total_time=(S+K)/CAP)


def execute(loop,tolerance):
    a,eps,K=[loop[k] for k in ['a','epsilon','shape_length']]
    cap_min=[float('inf')];cap_max=[-float('inf')];sym_error=[0.]
    def rhs(u,state):
        beta=state[0];ld,bd,B,Bp=geometry(u,a,eps)
        R=rotation(beta)
        Yprime_Yinverse=bd*J+R@Bp@np.linalg.inv(B)@R.T
        Shat=-Yprime_Yinverse/ld
        A=CAP/2*(np.eye(2)+Shat)
        sym_error[0]=max(sym_error[0],float(np.linalg.norm(A-A.T)))
        eig=np.linalg.eigvalsh((A+A.T)/2)
        cap_min[0]=min(cap_min[0],float(eig[0]));cap_max[0]=max(cap_max[0],float(eig[1]))
        dtdu=2*ld/CAP
        M=state[1:5].reshape(2,2);Q=state[5:9].reshape(2,2)
        C=M@C0@M.T+Q
        heat=DRAG*dtdu*(np.trace(A@A@C)-DIFFUSION*np.trace(A))
        return np.r_[bd,(-dtdu*A@M).ravel(),
                     (dtdu*(-A@Q-Q@A.T+2*DIFFUSION*np.eye(2))).ravel(),heat]
    init=np.r_[0.,np.eye(2).ravel(),np.zeros(4),0.]
    sol=solve_ivp(rhs,(0,math.pi),init,method='DOP853',
                  rtol=tolerance,atol=tolerance/20,max_step=math.pi/100)
    if not sol.success:raise RuntimeError(sol.message)
    final=sol.y[:,-1]
    Mg=final[1:5].reshape(2,2);Qg=final[5:9].reshape(2,2)
    Cg=Mg@C0@Mg.T+Qg
    W=DRAG*CAP/2*np.trace(Cg-C0)+final[-1]
    b=math.exp(-(S-K))
    M=b*Mg
    Q=b*b*Qg+(DIFFUSION/CAP)*(1-b*b)*np.eye(2)
    target=math.exp(-S)*rotation(THETA)
    # Independently integrate the explicit pullback-noise quadrature. Its
    # state is [length, integral of e^(2 length) B^-2], no drift matrix.
    def qrhs(u,state):
        ld,bd,B,Bp=geometry(u,a,eps)
        Bi=np.linalg.inv(B)
        return np.r_[ld,(math.exp(2*state[0])*Bi@Bi.T*ld).ravel()]
    qs=solve_ivp(qrhs,(0,math.pi),np.zeros(5),method='DOP853',
                 rtol=tolerance,atol=tolerance/20,max_step=math.pi/100)
    integral=qs.y[1:,-1].reshape(2,2)
    Qind=4*DIFFUSION/CAP*math.exp(-2*S)*rotation(THETA)@integral@rotation(-THETA)
    Qind+=(DIFFUSION/CAP)*(1-b*b)*np.eye(2)
    return {'tolerance':tolerance,'M':M.tolist(),'Q':Q.tolist(),
            'trace_Q':float(np.trace(Q)),
            'noise_eigenvalues':np.linalg.eigvalsh(Q).tolist(),
            'target_response_residual_Frobenius':float(np.linalg.norm(M-target)),
            'actual_log_attenuation':-.5*math.log(np.linalg.det(M)),
            'holonomy_ODE':float(final[0]),
            'holonomy_target_error':float(final[0]-THETA),
            'cap_eigenvalue_range_on_ODE_evaluations':[cap_min[0],cap_max[0]],
            'symmetry_residual_max':sym_error[0],
            'noise_independent_quadrature_residual_Frobenius':float(np.linalg.norm(Q-Qind)),
            'net_work_with_endpoint_quenches':float(W),
            'net_work_identity_error':float(W-2*DRAG*DIFFUSION*K)}


def first_variation():
    a=L/(math.pi+THETA);b=math.sqrt(1-a*a)
    def integrand(u):
        sn,cs=math.sin(u),math.cos(u)
        x=a*a*sn*sn;den=1-x
        rem=x+math.log1p(-x) if x>1e-5 else -sum(x**j/j for j in range(2,8))
        drho=cs*(-2*den/a**3)*rem
        h1=8*a*sn/den**2*drho
        ell=a/b*math.atan2(b*sn,cs)
        ld=a/den
        return 4*DIFFUSION/CAP*math.exp(-2*(S-ell))*h1*ld
    val,err=quad(integrand,0,math.pi,epsabs=2e-12,epsrel=2e-12)
    return {'trace_noise_first_derivative':val,'quadrature_reported_absolute_error':err,
            'interpretation':'Sign is proved analytically in slower_loop_derivation.txt; numerical value is supplemental.'}


def main():
    cases=[]
    for eps in [0.,.05]:
        loop=compile_loop(eps)
        loop['executions']=[execute(loop,tol) for tol in [1e-9,1e-11,1e-13]]
        for r in loop['executions']:
            assert r['target_response_residual_Frobenius']<1e-9
            assert abs(r['actual_log_attenuation']-S)<1e-8
            assert abs(r['holonomy_target_error'])<1e-9
            assert r['cap_eigenvalue_range_on_ODE_evaluations'][0]>-1e-10
            assert r['cap_eigenvalue_range_on_ODE_evaluations'][1]<CAP+1e-10
            assert r['noise_independent_quadrature_residual_Frobenius']<1e-8
            assert abs(r['net_work_identity_error'])<1e-8
        cases.append(loop)
    b,c=cases
    gap=b['executions'][-1]['trace_Q']-c['executions'][-1]['trace_Q']
    assert gap>.03
    out={'status':'Executed numerical counterexample to a stronger claim; analytic local failure separately proved',
         'model':'Same controlled OU model; Lambda=D=gamma=1, endpoints A=I',
         'target_angle':THETA,'target_log_attenuation':S,
         'exact_rotation_distance':L,'cases':cases,
         'trace_noise_reduction':gap,
         'additional_time':c['total_time']-b['total_time'],
         'additional_net_work':2*(c['shape_length']-b['shape_length']),
         'first_variation':first_variation(),
         'error_scope':'Converged floating quadrature/ODE residuals, not interval arithmetic or physical measurement. No global optimum beyond minimum time claimed.'}
    (HERE/'slower_loop_counterexample_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:out[k] for k in ['target_log_attenuation','exact_rotation_distance',
          'trace_noise_reduction','additional_time','additional_net_work','first_variation']},indent=2))
    print('Residuals:',[(r['epsilon'],r['executions'][-1]['target_response_residual_Frobenius'],
                       r['executions'][-1]['noise_independent_quadrature_residual_Frobenius']) for r in cases])


if __name__=='__main__':main()
