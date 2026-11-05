"""Independent matrix and ODE checks; synthetic model calculations only."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp

HERE=Path(__file__).resolve().parent
I=np.eye(2);S=np.diag([1.,-1.]);J=np.array([[0.,-1.],[1.,0.]])
K=np.array([[0.,1.],[1.,0.]])
def R(t):
    c,s=np.cos(t),np.sin(t)
    return np.array([[c,-s],[s,c]])
def compose(ch2,ch1):
    F2,Q2=ch2;F1,Q1=ch1
    return F2@F1,Q2+F2@Q1@F2.T
def const_channel(A,t,D):
    lam,U=np.linalg.eigh(A)
    f=np.exp(-lam*t)
    q=np.array([2*D*t if abs(x)<1e-13 else D*(-np.expm1(-2*x*t))/x for x in lam])
    return (U*f)@U.T,(U*q)@U.T
def rotating_segment(ell0,ell1,theta,cap,D):
    L=np.sqrt(theta*theta+2*np.pi*abs(theta))
    T=2*(ell1-ell0)/cap
    if T==0:return I.copy(),np.zeros((2,2))
    omega=cap*(theta+np.sign(theta)*np.pi)/(2*L)
    p0=(theta+np.sign(theta)*np.pi)*ell0/L
    p1=(theta+np.sign(theta)*np.pi)*ell1/L
    B=-cap/2*I-cap/2*S-omega*J
    V=expm(np.block([[B,2*D*I],[np.zeros((2,2)),-B.T]])*T)
    F0=V[:2,:2];Q0=V[:2,2:]@F0.T
    return R(p1)@F0@R(-p0),R(p1)@Q0@R(-p1)
def closed_noise(theta,cap,D):
    L=np.sqrt(theta*theta+2*np.pi*abs(theta));rho=L/(np.pi+abs(theta))
    m=D/cap;f=-np.expm1(-2*L)
    a=2*m*f*(1+rho*rho);b=2*m*f*rho*np.sqrt(1+rho*rho)
    Q0=a*I-2*m*f*rho*rho*S+np.sign(theta)*2*m*f*rho*K
    return R(theta)@Q0@R(-theta),a,b

def work_ode(theta,s,cap,D,gamma,S0):
    """Direct work integration through smooth rotation plus endpoint quenches."""
    L=np.sqrt(theta*theta+2*np.pi*abs(theta));Tr=2*L/cap
    omega=(theta+np.sign(theta)*np.pi)/Tr
    def A(t):return cap/2*(I+R(omega*t)@S@R(-omega*t))
    def dA(t):return cap/2*omega*R(omega*t)@(J@S-S@J)@R(-omega*t)
    W0=gamma/2*np.trace((A(0)-cap*I)@S0)
    z0=np.r_[S0.ravel(),W0]
    def rhs(t,z):
        C=z[:4].reshape(2,2);a=A(t)
        return np.r_[(-a@C-C@a+2*D*I).ravel(),gamma/2*np.trace(dA(t)@C)]
    sol=solve_ivp(rhs,(0,Tr),z0,rtol=2e-11,atol=2e-12)
    C=sol.y[:4,-1].reshape(2,2);W=sol.y[4,-1]
    W+=gamma/2*np.trace((cap*I-A(Tr))@C)
    tc=(s-L)/cap
    F,Q=const_channel(cap*I,tc,D)
    C=F@C@F.T+Q
    return {'numeric_expected_work':float(W),'formula_expected_work':float(2*gamma*D*L),
            'absolute_error':float(abs(W-2*gamma*D*L)),
            'final_second_moment':C.tolist(),'solver_success':bool(sol.success)}

def main():
    cap=1.7;D=.3;rng=np.random.default_rng(17052)
    basic=[];order=[];iso=[];work=[]
    for theta in [.1,.7,-1.2,np.pi]:
        L=np.sqrt(theta*theta+2*np.pi*abs(theta));Q,a,b=closed_noise(theta,cap,D)
        Fnum,Qnum=rotating_segment(0,L,theta,cap,D)
        basic.append({'theta':theta,'mean_error':float(np.linalg.norm(Fnum-np.exp(-L)*R(theta))),
                      'noise_error':float(np.linalg.norm(Qnum-Q))})
        delta=.8;s=L+delta
        Qmin=np.exp(-2*delta)*Q+(D/cap)*(1-np.exp(-2*delta))*I
        for trial in range(12):
            knots=np.r_[0,np.sort(rng.random(5))*L,L]
            pieces=rng.dirichlet(np.ones(len(knots)))*delta
            ch=(I.copy(),np.zeros((2,2)))
            for j,e in enumerate(knots):
                ch=compose(const_channel(cap*I,pieces[j]/cap,D),ch)
                if j<len(knots)-1:
                    ch=compose(rotating_segment(e,knots[j+1],theta,cap,D),ch)
            diff=(ch[1]-Qmin);diff=(diff+diff.T)/2
            order.append({'theta':theta,'trial':trial,'mean_error':float(np.linalg.norm(ch[0]-np.exp(-s)*R(theta))),
                          'smallest_noise_difference_eigenvalue':float(np.linalg.eigvalsh(diff)[0])})
        for delta in [.02,.2,1.]:
            beta=cap*b/D
            eta=min(delta,1.,.5*np.sqrt(beta/(np.exp(2)-1)))
            wait=b/(D*np.expm1(2*eta))-eta/cap
            assert wait>=0
            _,vec=np.linalg.eigh(Q);v=vec[:,0];P=np.outer(v,v)
            ch=(Fnum,Qnum)
            ch=compose(const_channel(cap*P,eta/cap,D),ch)
            ch=compose(const_channel(np.zeros((2,2)),wait,D),ch)
            ch=compose(const_channel(cap*(I-P),eta/cap,D),ch)
            ch=compose(const_channel(cap*I,(delta-eta)/cap,D),ch)
            q=np.exp(-2*delta)*(a+b/np.tanh(eta))+(D/cap)*(1-np.exp(-2*delta))
            T=(2*L+delta)/cap+b/(D*np.expm1(2*eta))
            iso.append({'theta':theta,'delta':delta,'eta':eta,'wait':wait,'total_time':T,'noise_variance':q,
                        'mean_error':float(np.linalg.norm(ch[0]-np.exp(-L-delta)*R(theta))),
                        'isotropic_noise_error':float(np.linalg.norm(ch[1]-q*I)),
                        'expected_work_over_kBT':2*(cap*T-L-delta)})
        if theta!=np.pi:
            C0=np.array([[2.,.4],[.4,1.]])+np.outer([1.,-.5],[1.,-.5])
            row=work_ode(theta,L+.5,cap,D,1.3,C0);row['theta']=theta;work.append(row)
    assert max(x['mean_error'] for x in basic)<1e-10
    assert max(x['noise_error'] for x in basic)<1e-9
    assert min(x['smallest_noise_difference_eigenvalue'] for x in order)>-1e-9
    assert max(x['isotropic_noise_error'] for x in iso)<1e-8
    assert max(x['absolute_error'] for x in work)<1e-8
    out={'scope':'Synthetic verification of analytic model claims; not physical evidence',
         'controls':'prescribed, amplitude cap only; no finite slew bound',
         'boundary_checks':basic,'time_optimal_reordering_checks':order,
         'exact_isotropic_noise_constructions':iso,'direct_work_integration':work}
    (HERE/'results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'boundary_max_mean_error':max(x['mean_error'] for x in basic),
                     'boundary_max_noise_error':max(x['noise_error'] for x in basic),
                     'minimum_reordering_eigenvalue':min(x['smallest_noise_difference_eigenvalue'] for x in order),
                     'isotropic_noise_max_error':max(x['isotropic_noise_error'] for x in iso),
                     'expected_work_max_error':max(x['absolute_error'] for x in work)},indent=2))

if __name__=='__main__':main()
