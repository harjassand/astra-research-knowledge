"""Hot-side overlap gate. Derived model only, not a material simulation."""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize_scalar

OUT = Path(__file__).resolve().parent
H=6.62607015e-34
KB=1.380649e-23

def bose(f,t):
    return 1/np.expm1(H*f/(KB*t))

def qcold(a,x,b,g,d0,da):
    ka=a+x
    nbar_difference=d0+x/ka*da
    coop=4*g*g/(ka*b)
    current=ka*b/(ka+b)*coop/(1+coop)*nbar_difference
    # Q/(hbar wc), which is a rate.
    return a/ka*(current-x*da)

def xi_threshold_at_x(a,x,d0,da):
    e=x*da
    return da/(4*d0*d0)*(np.sqrt(e)+np.sqrt(e+d0*(a+x)))**2

def optimized_q_at_u(u,z,d0,da):
    return u*u*(4*z*z*d0-da*(1+u*u+4*u*z))/(1+u*u+2*u*z)**2

def main():
    rng=np.random.default_rng(202610231)
    max_id_error=0.0
    max_threshold_error=0.0
    for _ in range(200):
        a,x,xi=10**rng.uniform(-2,2,3)
        d0,da=10**rng.uniform(-2,1,2)
        g=np.sqrt(x*xi)
        b=2*g
        got=qcold(a,x,b,g,d0,da)/a
        formula=optimized_q_at_u(np.sqrt(x/a),np.sqrt(xi/a),d0,da)
        max_id_error=max(max_id_error,abs(got-formula))
        critical_xi=xi_threshold_at_x(a,x,d0,da)
        critical_g=np.sqrt(x*critical_xi)
        residual=qcold(a,x,2*critical_g,critical_g,d0,da)
        max_threshold_error=max(max_threshold_error,abs(residual)/(a*(d0+da)))
    assert max_id_error<1e-11
    assert max_threshold_error<1e-12

    nc=bose(12.21e12,300)
    nlow_hot=bose(12.21e12,330)
    nhigh_hot=bose(14.54e12,330)
    d0=nc-nhigh_hot;da=nlow_hot-nc
    ratio=da/(4*d0)
    rows=[]
    for xi_over_a in [0.1,ratio,0.4,0.5,1,2,10,100]:
        z=np.sqrt(xi_over_a)
        if xi_over_a<=ratio*(1+1e-12):
            rows.append(dict(Xi_over_A=float(xi_over_a),positive_cooling=False,
                             limiting_Q_over_hbar_wc_A_Delta0=0))
            continue
        umax=-2*z+np.sqrt(4*z*z*(1+d0/da)-1)
        res=minimize_scalar(lambda u:-optimized_q_at_u(u,z,d0,da),
                            bounds=(0,umax),method='bounded',options={'xatol':1e-13})
        u=res.x
        rows.append(dict(Xi_over_A=float(xi_over_a),positive_cooling=True,
                         optimum_x_over_A=float(u*u),
                         optimum_B_over_A=float(2*u*z),
                         optimum_g_over_A=float(u*z),
                         Q_over_hbar_wc_A_Delta0=float(-res.fun/d0)))
    result=dict(status='DERIVED_REDUCED_MODEL_NO_MATERIAL_DATA',
        identity_checks=200,max_absolute_normalized_identity_error=max_id_error,
        max_relative_threshold_residual=max_threshold_error,
        temperature_frequency_example=dict(Tc_K=300,Th_K=330,fc_THz=12.21,fh_THz=14.54,
            n_cold=nc,n_hot_low=nlow_hot,n_hot_high=nhigh_hot,
            Delta0=d0,Delta_a=da,max_x_over_B=d0/da,
            Xi_over_A_existence_infimum=ratio),
        geometry_optimized_table=rows)
    (OUT/'hot_side_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
