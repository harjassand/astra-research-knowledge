"""Independent finite-Fock Lindblad test of full retained-oscillator channel.
Tests operator equality rho_zz'(T)=c_zz' free_thermal_channel(rho_zz'(0)).
The analytic theorem is not inferred from these finite-cutoff checks.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import gammaln
from scipy.interpolate import CubicSpline
from double_closed_hot_bus import loop

def run_one(N=32,kappa=.1,T=4,nb=.15):
    schedule=loop(kappa=kappa,T=T)
    A,B,c=schedule['coefficients']
    tgrid=np.linspace(0,T,2001); q=np.pi*tgrid/T; dq=np.pi/T
    sn=np.sin(q); cs=np.cos(q); ef=np.exp(kappa*tgrid/2)
    X=sn**2*np.sin(2*q); Xp=dq*(2*sn*cs*np.sin(2*q)+2*sn**2*np.cos(2*q))
    Y=sn**2*(np.cos(2*q)+.5); Yp=dq*(2*sn*cs*(np.cos(2*q)+.5)-2*sn**2*np.sin(2*q))
    x=A*ef*X; xp=A*ef*(Xp+kappa*X/2)
    y=B*(ef*Y-c*ef*X); yp=B*(ef*(Yp+kappa*Y/2)-c*ef*(Xp+kappa*X/2))
    fs=[CubicSpline(tgrid,1j*(xp+kappa*x/2)),CubicSpline(tgrid,-(yp+kappa*y/2))]
    a=np.diag(np.sqrt(np.arange(1,N)),1).astype(complex); ad=a.T; n=ad@a; nn=a@ad
    def dissip(R):
        return kappa*((nb+1)*(a@R@ad-(n@R+R@n)/2)+nb*(ad@R@a-(nn@R+R@nn)/2))
    def evolve(R,z=None,zp=None):
        def rhs(t,v):
            R=v.reshape(N,N); ans=dissip(R)
            if z is not None:
                f=sum(z[j]*fs[j](t) for j in range(2)); fp=sum(zp[j]*fs[j](t) for j in range(2))
                H=f*ad+f.conjugate()*a; Hp=fp*ad+fp.conjugate()*a
                ans+=-1j*(H@R-R@Hp)
            return ans.ravel()
        sol=solve_ivp(rhs,[0,T],R.ravel(),rtol=3e-10,atol=3e-12,method='DOP853')
        assert sol.success
        return sol.y[:,-1].reshape(N,N)
    def coh(alpha):
        k=np.arange(N); v=np.exp(-abs(alpha)**2/2+k*np.log(complex(alpha))-.5*gammaln(k+1));return v/np.linalg.norm(v)
    inputs={}
    R=np.zeros((N,N),complex);R[7,7]=1;inputs['fock7']=R
    inputs['coherent']=np.outer(coh(1.1+.6j),coh(1.1+.6j).conj())
    inputs['cross_operator']=np.outer(coh(.3+.7j),coh(-.8+.1j).conj())
    p=.7/1.7;inputs['thermal07']=np.diag((1-p)*p**np.arange(N)).astype(complex);inputs['thermal07']/=np.trace(inputs['thermal07'])
    checks=[]; G=np.asarray(schedule['gram_real']); theta=schedule['theta']
    for name,R in inputs.items():
        free=evolve(R)
        for z,zp in [((1,1),(1,-1)),((1,1),(-1,-1)),((1,-1),(-1,1))]:
            z=np.array(z);zp=np.array(zp);diff=z-zp
            pred=np.exp(1j*theta*(np.prod(z)-np.prod(zp))-(nb+.5)*diff@G@diff)*free
            got=evolve(R,z,zp)
            err=np.linalg.norm(got-pred,'fro')
            checks.append(dict(input=name,z=z.tolist(),zp=zp.tolist(),frobenius_error=float(err),trace_error=float(abs(np.trace(got-pred))),free_top_population=float(abs(free[-1,-1]))))
    return dict(N=N,kappa=kappa,T=T,n_b=nb,checks=checks,max_error=max(x['frobenius_error'] for x in checks))

if __name__=='__main__':
    results=[run_one(N=24),run_one(N=32)]
    Path(__file__).with_name('hot_bus_instrument_checks.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps([{'N':r['N'],'max_error':r['max_error'],'max_trace_error':max(c['trace_error'] for c in r['checks'])} for r in results],indent=2))
