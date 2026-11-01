"""Fixed derivative-null homodyne filter for the finite direct-port readout.
Actual unknown readout-rate gain and constant detuning are NOT fitted away.
Bounds combine a reference CP instrument with a photon-cap dilation remainder.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,simpson
from scipy.optimize import brentq
from scipy.special import ndtr,log_ndtr,gammaln


def controls(t,T,r=.1):
    t=np.asarray(t); w=np.ones_like(t,dtype=float); W=t-r/2
    i=t<r;w[i]=np.sin(np.pi*t[i]/(2*r))**2;W[i]=t[i]/2-r*np.sin(np.pi*t[i]/r)/(2*np.pi)
    i=t>T-r;v=T-t[i];w[i]=np.sin(np.pi*v/(2*r))**2;W[i]=T-r-v/2+r*np.sin(np.pi*v/r)/(2*np.pi)
    return w,W


def quad_weights(t):
    n=len(t);assert n%2==1
    w=np.ones(n);w[1:-1:2]=4;w[2:-1:2]=2
    return w*(t[1]-t[0])/3


def actual_signal(t,T,kr,k0,F,detuning=0.,gain=0.):
    def rhs(s,y):
        w=controls(np.array([s]),T)[0][0]
        return [-(.5*(k0+kr*(1+gain)*w)+1j*detuning)*y[0]+F*w]
    ans=solve_ivp(rhs,[0,T],[0j],t_eval=t,method='DOP853',rtol=2e-11,atol=1e-13,max_step=.025)
    if not ans.success:raise RuntimeError(ans.message)
    w,W=controls(t,T)
    H=np.sqrt(kr*(1+gain)*w)*np.exp(-k0*t/2-kr*(1+gain)*W/2-1j*detuning*t)
    return H,np.sqrt(kr*(1+gain)*w)*ans.y[0]


def design(T,order=1,kr=4.,k0=1e-4,F=3.,nb=.1,eta=.5,points=8001):
    t=np.linspace(0,T,points); qw=quad_weights(t);w,W=controls(t,T)
    H,h=actual_signal(t,T,kr,k0,F);assert np.max(abs(h.imag))<1e-12
    columns=[];labels=[]
    for degree in range(order+1):
        for q in range(degree+1):
            r=degree-q
            columns.append(H.real*(t/T)**q*(W/T)**r);labels.append([q,r])
    C=np.array(columns).T
    C=C/np.sqrt(np.sum(qw[:,None]*C*C,axis=0))[None,:]
    U,s,_=np.linalg.svd(np.sqrt(qw)[:,None]*C,full_matrices=False)
    # All analytically independent columns retained; warn if numerical degeneracy.
    if s[-1]<1e-12:raise RuntimeError('Derivative basis unresolved')
    v=np.sqrt(qw)*h.real; vp=v-U@(U.T@v);N=vp@vp
    f=(vp/np.sqrt(N))/np.sqrt(qw)
    A=simpson(f*np.sqrt(w),x=t)
    return dict(t=t,f=f,H=H,h=h,w=w,W=W,N=N,A=A,svals=s,labels=labels,kr=kr,k0=k0,F=F,nb=nb,eta=eta,T=T,order=order)


def analytic_bounds(d,gain_bound=.01,detuning_bound=.01,Ncap=320,force_gain_bound=1e-6):
    T,kr,k0,F,nb,eta=[d[k] for k in ['T','kr','k0','F','nb','eta']]; n=d['order']+1
    a=np.hypot(gain_bound*kr/2,detuning_bound);rate=kr+k0-2*a
    if rate<=0:raise ValueError('No infinite-time exponential bound')
    # H^2 <= kr exp(kr*r) exp[-(kr+k0)t], with r=.1.
    logc=.5*np.log1p(gain_bound)+.5*(np.log(kr)+kr*.1+2*n*np.log(a)+gammaln(2*n+1)-(2*n+1)*np.log(rate))-gammaln(n+1)
    c=float(np.exp(logc))
    # Also retain a tighter fixed-filter quadrature remainder as a diagnostic.
    zabs=np.hypot(gain_bound*kr*d['W']/2,detuning_bound*d['t'])
    cq=np.sqrt(1+gain_bound)*simpson(abs(d['f']*d['H'])*zabs**n*np.exp(zabs),x=d['t'])/np.exp(gammaln(n+1))
    # Uniform analytic signal bound from forced linear equation.
    krmin=kr*(1-gain_bound);krmax=kr*(1+gain_bound)
    Dmax=2/(krmin+k0)+.1
    Bmax=Dmax*np.sqrt(krmax*T)
    a0=np.hypot(k0/2,detuning_bound)
    small=2*F/krmin*(c+a0*Bmax)
    mlo=(1-force_gain_bound)*(2*F/np.sqrt(krmax)*d['A']-small)
    mhi=(1+force_gain_bound)*(2*F/np.sqrt(krmin)*d['A']+small)
    imagmax=(1+force_gain_bound)*small
    v=2*nb+1;ww=1+2*eta*nb
    logqmax=log_ndtr(-2*np.sqrt(eta)*mlo/np.sqrt(ww));logqmin=log_ndtr(-2*np.sqrt(eta)*mhi/np.sqrt(ww))
    zz=2*np.sqrt(eta)*v*imagmax/np.sqrt(ww)
    loggamma=-np.log(2)-2*v*mlo*mlo+np.log1p(np.sqrt(2/np.pi)*zz*np.exp(zz*zz/2))
    eref=float(np.exp(logqmax)+np.exp(2*loggamma-logqmin))
    eps=float(np.arcsin(min(c,1))*np.sqrt((2*nb+1)*Ncap+nb))
    return dict(gain_bound=gain_bound,detuning_bound=detuning_bound,force_gain_bound=force_gain_bound,photon_cap=Ncap,
        incoming_overlap_bound=c,incoming_fixed_filter_quadrature_bound=float(cq),
        reference_Re_mu_lower=float(mlo),reference_Re_mu_upper=float(mhi),reference_abs_Im_mu_upper=float(imagmax),
        reference_CP_bad_upper=eref,reference_q_upper=float(np.exp(logqmax)),
        capped_instrument_dilation_error_upper=eps,
        note='Eref is an exact-parameter reference CP bound; epsilon is a coherent instrument remainder on the photon cap, not an independent error probability.')


def sample_actual(d,gains,detunings):
    ans=[];v=2*d['nb']+1;w=1+2*d['eta']*d['nb']
    for gain in gains:
        for detuning in detunings:
            H,h=actual_signal(d['t'],d['T'],d['kr'],d['k0'],d['F'],detuning,gain)
            c=simpson(d['f']*H,x=d['t']);mu=simpson(d['f']*h,x=d['t'])
            q=float(ndtr(-2*np.sqrt(d['eta'])*mu.real/np.sqrt(w)))
            gamma=np.exp(-2*v*abs(mu)**2)*ndtr(1j*2*np.sqrt(d['eta'])*v*mu.imag/np.sqrt(w))
            e=float(q+abs(gamma)**2/q)
            ans.append(dict(gain=gain,detuning=detuning,c_abs=float(abs(c)),mu_real=float(mu.real),mu_imag=float(mu.imag),reference_CP_bad=e))
    return ans


def serial(d,bounds,actual):
    nulls=[]
    for q,r in d['labels']:
        nulls.append(float(abs(simpson(d['f']*d['H']*(d['t']/d['T'])**q*(d['W']/d['T'])**r,x=d['t']))))
    return dict(T=d['T'],order=d['order'],force_cap=d['F'],readout_rate_cap=d['kr'],intrinsic_loss=d['k0'],eta=d['eta'],nb=d['nb'],ramp=.1,
        N_eff_nominal=float(d['N']),A=float(d['A']),derivative_columns=d['labels'],singular_values=list(d['svals']),max_null_residual=max(nulls),
        uniform_bounds=bounds,actual_grid_diagnostics=actual,
        peak_abs_filter=float(max(abs(d['f']))),filter_L2_norm=float(simpson(d['f']**2,x=d['t'])),
        interval_scope='Both rate and force ramps included. All additional quantum/control waiting is charged by consumer. Fixed filter is used for every actual parameter in the range.')


def main():
    rows=[]
    for order in [0,1,2]:
        for gain_bound,detuning_bound in [(.001,.0001),(.001,.000001)]:
            T=brentq(lambda T:analytic_bounds(design(T,order,F=3/(1+1e-6),points=3001),gain_bound,detuning_bound)['reference_CP_bad_upper']-1e-6,1.,12.,xtol=2e-8)
            # Small duration margin absorbs quadrature design inaccuracies.
            T=np.ceil(T*1000)/1000+.001
            d=design(T,order,F=3/(1+1e-6),points=12001)
            b=analytic_bounds(d,gain_bound,detuning_bound)
            a=sample_actual(d,[-gain_bound,0,gain_bound],[-detuning_bound,0,detuning_bound])
            assert max(x['c_abs'] for x in a)<=b['incoming_overlap_bound']*(1+1e-6)+1e-12
            assert max(x['reference_CP_bad'] for x in a)<=b['reference_CP_bad_upper']
            rows.append(serial(d,b,a))
    out={'model':'Fixed derivative-null homodyne filter; actual rate gain and frequency offset vary in declared box. Analytic conservative bounds + diagnostic parameter samples. Photon-cap remainder is amplitude, not probability.','rows':rows}
    Path(__file__).with_name('robust_longitudinal_receiver_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([dict(T=r['T'],order=r['order'],N=r['N_eff_nominal'],**r['uniform_bounds']) for r in rows],indent=2))
if __name__=='__main__':main()
