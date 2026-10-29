"""One predeclared attempt to escape the finite-moment no-go by a quartic norm.

B(v)=1+|v|^4/10. Four strategic velocities, not a tuning grid. Ordinary
Gaussian quadrature+weighted LAD LP; no rigorous continuum sign claimed.
"""
import json,math,time
from pathlib import Path
import numpy as np
from scipy.special import roots_genlaguerre,roots_legendre
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,hstack,vstack,eye


def main():
    tick=time.perf_counter()
    radial,wr=roots_genlaguerre(96,0.5)
    mu,wm=roots_legendre(64)
    speed=np.sqrt(2*radial)[:,None]
    cosine=mu[None,:]
    weights=(wr[:,None]/math.gamma(1.5)*wm[None,:]/2).ravel()
    w_z=(speed*cosine+np.zeros((96,64))).ravel()
    w_r2=np.broadcast_to(speed**2,(96,64)).ravel()
    design=np.column_stack([np.ones(len(weights)),w_z,w_r2])
    records=[]
    for v in (0.0,2.0,4.0,8.0):
        start=time.perf_counter()
        relative2=(v*v+speed**2-2*v*speed*cosine)
        relative=np.sqrt(relative2)
        perp2=v*v*speed**2*(1-cosine**2)/relative2
        kernel=(4*np.exp(perp2/2)/relative-relative).ravel()
        nu=2*math.sqrt(2/math.pi) if v==0 else math.sqrt(2/math.pi)*math.exp(-v*v/2)+(v+1/v)*math.erf(v/math.sqrt(2))
        weighted=weights*(1+w_r2**2/10)
        matrix=csr_matrix(design*weighted[:,None])
        rhs=kernel*weighted
        identity=eye(len(weights),format='csr')
        constraints=vstack([hstack([-matrix,-identity]),hstack([matrix,-identity])],format='csr')
        target=np.r_[np.zeros(3),np.ones(len(weights))]
        fit=linprog(target,A_ub=constraints,b_ub=np.r_[-rhs,rhs],
                    bounds=[(None,None)]*3+[(0,None)]*len(weights),method='highs')
        if not fit.success:
            records.append({'v':v,'success':False,'message':fit.message})
            continue
        controls=fit.x[:3]
        cost=float(np.dot(weighted,np.abs(kernel-design@controls)))
        records.append({'v':v,'success':True,'controls_mass_parallel_momentum_energy':controls.tolist(),
                        'controlled_absolute_row_over_nuB':cost/(nu*(1+v**4/10)),
                        'unweighted_kernel_row_mass_over_nu':float(weights@kernel)/nu,
                        'raw_absolute_weighted_row_over_nuB':float(weighted@np.abs(kernel))/(nu*(1+v**4/10)),
                        'LP_objective_vs_reconstructed':float(fit.fun-cost),
                        'seconds':time.perf_counter()-start})
    result={'status':'FLOAT_PREVIEW_not_continuum_certificate','B':'1+|v|^4/10',
            'radial_order':96,'angular_order':64,'predeclared_velocities':[0,2,4,8],
            'records':records,'seconds_total':time.perf_counter()-tick,
            'global_subcritical_claim':False,'nonlinear_closure_claim':False}
    (Path(__file__).parent/'WEIGHTED_REPAIR_PREVIEW.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
