"""Conventional pulse optimization of the SAME exact finite-mode apparatus.

All modes, couplings and losses match root/finite_mediator_parity.py.  This
does not compare a new recipe with an artificially unoptimized controller.
It minimizes integrated logical-information exposure in an endpoint-safe
Fourier family, with fixed measurement assignment, duration and drive caps.
The reported feasible solution is not claimed to be a global optimum.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.linalg import eigh
from scipy.optimize import minimize, minimize_scalar
from scipy.special import ndtri, ndtr


def fourier_basis(n):
    """Rows are coefficients of sin^6(x)*cos(j*x), j=0..n."""
    C=np.zeros((n+1,n+7))
    for j in range(n+1):
        C[j,j]+=10/32
        for k,v in ((2,-15/32),(4,6/32),(6,-1/32)):
            C[j,abs(j-k)]+=v/2
            C[j,j+k]+=v/2
    return C


def matrices(n,t,m):
    C=fourier_basis(n)
    omega=np.arange(n+7)*np.pi/m['T']
    U=[(np.cos(np.outer(t,omega)+j*np.pi/2)*omega**j)@C.T
       for j in range(5)]
    ab=m['kb']/2;ac=m['kc']/2;rt=np.sqrt(m['Gamma']);g=m['g'];chi=m['chi']
    A=[rt/g*(U[j+1]+ab*U[j]) for j in range(4)]
    V=[-(A[j+1]+m['Gamma']*A[j]/2)/(g*rt)-U[j] for j in range(3)]
    B=(-ac*V[0]+g*A[0]/rt-V[1])/chi
    dB=(-ac*V[1]+g*A[1]/rt-V[2])/chi
    return dict(U=U[0],V=V[0],A=A[0],B=B,u=-dB-ab*B,
                w=dB+ac*B-chi*V[0])


def gram(X,t):
    # Simpson is exact to far beyond needed precision on this smooth grid.
    return simpson(X[:,:,None]*X[:,None,:],x=t,axis=0)


def minimize_exposure(n,m,initial_coeff=None,seed=703):
    t=np.linspace(0,m['T'],4001)
    f=matrices(n,t,m)
    QA=gram(f['A'],t);QB=gram(f['B'],t)
    da,va=eigh(QA)
    W=va@np.diag(1/np.sqrt(da))
    H=W.T@QB@W
    vals,vecs=eigh(H)
    N=ndtri(m['q'])**2/(4*m['eta'])
    # Normalize y to ||y||=1; coefficient c=sqrt(N)*W*y.
    # Dense grid is independently checked and adaptively refined if needed.
    sample=np.linspace(0,m['T'],601)
    fs=matrices(n,sample,m)
    J=np.vstack([fs['u'],fs['w']])@W*np.sqrt(N)
    # Reserve a tiny tolerance so a sampled constraint never silently claims
    # that a continuous-time peak infinitesimally above 3 is below 3.
    cap=m['cap']-1e-4
    con=[{'type':'eq','fun':lambda y:float(y@y-1),
          'jac':lambda y:2*y},
         {'type':'ineq','fun':lambda y:cap-J@y,
          'jac':lambda y:-J},
         {'type':'ineq','fun':lambda y:cap+J@y,
          'jac':lambda y:J}]
    def from_coeff(c):
        y=np.linalg.solve(W,c)
        return y/np.linalg.norm(y)
    starts=[vecs[:,0]]
    starts.append(from_coeff(np.r_[1.,np.zeros(n)]))
    if initial_coeff is not None:
        c=np.zeros(n+1);c[:min(len(c),len(initial_coeff))]=initial_coeff[:len(c)]
        starts.append(from_coeff(c))
    rng=np.random.default_rng(seed)
    for _ in range(2):
        y=vecs[:,0]+.05*rng.normal(size=n+1)
        starts.append(y/np.linalg.norm(y))
    rows=[];best=None
    for y0 in starts:
        opt=minimize(lambda y:float(y@H@y),y0,jac=lambda y:2*H@y,
                     method='SLSQP',constraints=con,
                     options={'ftol':2e-11,'maxiter':600,'disp':False})
        feasible=abs(opt.x@opt.x-1)<2e-7 and np.max(abs(J@opt.x))<=cap+2e-6
        rows.append({'success':bool(opt.success),'feasible':bool(feasible),
                     'ratio':float(opt.fun),'message':str(opt.message),
                     'iterations':int(opt.nit)})
        if feasible and (best is None or opt.fun<best.fun):best=opt
    if best is None:raise RuntimeError(rows)
    c=np.sqrt(N)*W@best.x
    # Refine the sampled amplitude constraints at every continuous extremum.
    # A high-resolution independent scan locates tiny grid excursions first.
    dense=np.linspace(0,m['T'],40001)
    fd=matrices(n,dense,m)
    peaks={k:float(np.max(abs(fd[k]@c))) for k in ('u','w')}
    for refinement in range(4):
        if max(peaks.values())<=cap+1e-7:break
        dense_values=np.r_[fd['u']@c,fd['w']@c]
        # Add local maxima beyond the cap to the original linear grid.
        extra=[]
        for k in ('u','w'):
            value=fd[k]@c
            ix=np.flatnonzero((abs(value[1:-1])>=abs(value[:-2]))&
                              (abs(value[1:-1])>=abs(value[2:])))+1
            for j in ix:
                ext=minimize_scalar(lambda tt:-abs((matrices(n,np.array([tt]),m)[k]@c).item()),
                                    bounds=(dense[j-1],dense[j+1]),method='bounded',
                                    options={'xatol':1e-12})
                extra.append(matrices(n,np.array([ext.x]),m)[k][0]@W*np.sqrt(N))
        J=np.vstack([J,np.array(extra)])
        opt=minimize(lambda y:float(y@H@y),best.x,jac=lambda y:2*H@y,
                     method='SLSQP',constraints=con,
                     options={'ftol':1e-12,'maxiter':300})
        if abs(opt.x@opt.x-1)>1e-7 or np.max(abs(J@opt.x))>cap+1e-6:
            raise RuntimeError('Continuous peak refinement did not converge')
        c=np.sqrt(N)*W@opt.x
        best=opt
        peaks={k:float(np.max(abs(fd[k]@c))) for k in ('u','w')}
        rows.append({'refinement':True,'success':bool(opt.success),
                     'ratio':float(opt.fun),'iterations':int(opt.nit)})
    report=ledger(c,m,samples=20001)
    if max(report['peak_u'],report['peak_w'])>m['cap']:
        raise RuntimeError('Validated dense-grid drive exceeds the requested cap')
    report.update(n=n,coefficients=c.tolist(),unconstrained_basis_lower_bound=float(vals[0]),
                  optimizations=rows,normalization_condition_number=float(da[-1]/da[0]))
    return report


def ledger(c,m,samples=20001):
    t=np.linspace(0,m['T'],samples)
    f={k:v@c for k,v in matrices(len(c)-1,t,m).items()}
    integ=lambda x:float(simpson(x,x=t))
    N=integ(f['A']**2);IB=integ(f['B']**2)
    D=(m['kb']+m['kc'])*IB
    r={'N':N,'IB':IB,'IB_over_N':IB/N,
       'q':float(ndtr(-2*np.sqrt(m['eta']*N))),
       'same_parity_pZ':float(-np.expm1(-2*D)/2),
       'visibility':float(np.exp(-2*D)),
       'peak_u':float(np.max(abs(f['u']))),'peak_w':float(np.max(abs(f['w']))),
       'action_u':integ(f['u']**2),'action_w':integ(f['w']**2),
       'exposure_b':integ(f['U']**2+f['B']**2),
       'exposure_c':integ(f['V']**2+f['B']**2),
       'exposure_meter':N/m['Gamma'],
       'peak_n_b':float(np.max(f['U']**2+f['B']**2)),
       'peak_n_c':float(np.max(f['V']**2+f['B']**2)),
       'peak_n_meter':float(np.max(f['A']**2/m['Gamma'])),
       'terminal_photons':float(f['U'][-1]**2+f['V'][-1]**2+2*f['B'][-1]**2+f['A'][-1]**2/m['Gamma']),
       'endpoint_drive_max':float(max(abs(f['u'][[0,-1]]).max(),abs(f['w'][[0,-1]]).max()))}
    return r


def validate_ode(c,m):
    z1=np.array([1.,1.,-1.,-1.]);z2=np.array([1.,-1.,1.,-1.]);S=z1*z2
    def fun(t,y):
        b,cav,med=y.reshape(3,4)
        f={k:(v@c).item() for k,v in matrices(len(c)-1,np.array([t]),m).items()}
        return np.r_[-m['kb']*b/2-1j*m['g']*med-1j*f['u']*z2,
                      -(m['kc']/2+1j*m['chi']*z1)*cav-1j*m['g']*med-1j*f['w']*z2,
                      -m['Gamma']*med/2-1j*m['g']*(b+cav)]
    t=np.linspace(0,m['T'],4001)
    sol=solve_ivp(fun,[0,m['T']],np.zeros(12,complex),t_eval=t,
                  method='DOP853',rtol=4e-12,atol=1e-13)
    f={k:v@c for k,v in matrices(len(c)-1,t,m).items()}
    exact=np.array([f['U'][:,None]*S+1j*f['B'][:,None]*z2,
                    f['V'][:,None]*S-1j*f['B'][:,None]*z2,
                    1j*f['A'][:,None]*S/np.sqrt(m['Gamma'])]).transpose(0,2,1).reshape(12,-1)
    return {'success':bool(sol.success),'max_amplitude_error':float(np.max(abs(sol.y-exact))),
            'terminal_photons_max_branch':float(np.sum(abs(sol.y[:,-1].reshape(3,4))**2,axis=0).max())}


def general_spectral_floor(m):
    h=m['Gamma']/2;ab=m['kb']/2;ac=m['kc']/2;g=m['g'];chi=m['chi']
    if abs(ab-ac)<1e-18:
        C=h*h+ab*ab-4*g*g;K=h*ab+2*g*g
        omega2=max(0.,-C/2)
        return {'ratio':float((omega2**2+C*omega2+K*K)/(chi*chi*g*g*m['Gamma'])),
                'frequency':float(np.sqrt(omega2)),'scope':'Infinite-support spectral lower bound, equal intrinsic rates.'}
    p2=h+ab+ac;p1=h*(ab+ac)+ab*ac+2*g*g;p0=h*ab*ac+g*g*(ab+ac)
    def rat(y):
        if y+ab*ab==0:return np.inf
        return ((p0-p2*y)**2+y*(p1-y)**2)/(chi*chi*g*g*m['Gamma']*(y+ab*ab))
    opt=minimize_scalar(rat,bounds=(0,100*(h*h+g*g+ab*ab+ac*ac)),method='bounded')
    y=opt.x if opt.fun<rat(0) else 0.
    return {'ratio':float(rat(y)),'frequency':float(np.sqrt(y)),
            'scope':'Numerical spectral lower bound for given rates; search range recorded in code.'}


def finite_time_floor(m):
    """Rigorous relaxed floor from weighted zero-area and clamped endpoints.

    Scope: equal internal rates, nonnegative coefficient C, fixed real-force
    exact-parity-output family. Derivation is in the accompanying proof memo.
    """
    a=m['kb']/2;h=m['Gamma']/2;g=m['g'];T=m['T'];chi=m['chi']
    C=h*h+a*a-4*g*g;K=h*a+2*g*g
    if m['kb']!=m['kc'] or C<0:return {'applicable':False}
    beta2=7.853204624095838
    R4=np.exp(-2*a*T)*((beta2/T)**4+2*a*a*(np.pi/T)**2+a**4)
    ratio=(R4+C*(np.pi/T)**2+K*K)/(chi*chi*g*g*m['Gamma'])
    N=ndtri(m['q'])**2/(4*m['eta'])
    return {'applicable':True,'IB_over_N_lower_bound':float(ratio),
            'same_parity_pZ_lower_bound':float(-np.expm1(-2*(m['kb']+m['kc'])*N*ratio)/2),
            'scope':'Fixed model exact-output family; no force caps imposed in lower bound.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--orders',default='6,14,22,30')
    args=ap.parse_args()
    m={'T':8.,'g':1.,'Gamma':4.,'chi':2.,'kb':1e-4,'kc':1e-4,'eta':.5,'q':1e-3,'cap':3.}
    QA=gram(matrices(0,np.linspace(0,m['T'],4001),m)['A'],np.linspace(0,m['T'],4001))
    N=ndtri(m['q'])**2/(4*m['eta'])
    base=np.array([np.sqrt(N/QA[0,0])])
    result={'model':m,'baseline_sine6':ledger(base,m),'spectral_floor':general_spectral_floor(m),
            'finite_time_floor':finite_time_floor(m),'optimized':[]}
    c=None
    for n in map(int,args.orders.split(',')):
        r=minimize_exposure(n,m,initial_coeff=c)
        result['optimized'].append(r);c=np.array(r['coefficients'])
        print(json.dumps({k:r[k] for k in ('n','IB_over_N','peak_u','peak_w','same_parity_pZ','peak_n_b','peak_n_c')}),flush=True)
        Path(__file__).with_name('finite_mediator_optimization_results.json').write_text(json.dumps(result,indent=2)+'\n')
    result['optimized_ode_check']=validate_ode(c,m)
    Path(__file__).with_name('finite_mediator_optimization_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['optimized_ode_check']),flush=True)


if __name__=='__main__':main()
