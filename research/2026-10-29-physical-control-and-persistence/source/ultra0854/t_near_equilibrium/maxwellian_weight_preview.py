"""One structurally different weighted repair: g=(f-M)/M^(3/4).

Unlike a polynomial relative-M weight, this space can bound the nonlinear
quadratic by a Gaussian partner integral. Four anchors only; no theorem is
inferred from this quadrature/LAD preview.
"""
import json,math,time
from pathlib import Path
import numpy as np
from scipy.special import roots_genlaguerre,roots_legendre
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,hstack,vstack,eye

def main():
    started=time.perf_counter();beta=0.75
    radial,wr=roots_genlaguerre(96,0.5);mu,wm=roots_legendre(64)
    speed=np.sqrt(2*radial/beta)[:,None];cosine=mu[None,:]
    base_weights=(wr[:,None]/math.gamma(1.5)*wm[None,:]/2).ravel()
    wz=(speed*cosine+np.zeros((96,64))).ravel()
    w2=np.broadcast_to(speed**2,(96,64)).ravel()
    design=np.column_stack([np.ones(len(w2)),wz,w2]);records=[]
    identity=eye(len(w2),format='csr')
    for v in (0.0,2.0,4.0,8.0):
        tick=time.perf_counter()
        r2=v*v+speed**2-2*v*speed*cosine;r=np.sqrt(r2)
        perp2=v*v*speed**2*(1-cosine**2)/r2
        kernel=(4*np.exp(perp2/2)/r-r).ravel()
        nu=2*math.sqrt(2/math.pi) if v==0 else math.sqrt(2/math.pi)*math.exp(-v*v/2)+(v+1/v)*math.erf(v/math.sqrt(2))
        weights=base_weights*beta**(-1.5)*math.exp(-(1-beta)*v*v/2)
        matrix=csr_matrix(design*weights[:,None]);rhs=weights*kernel
        constraints=vstack([hstack([-matrix,-identity]),hstack([matrix,-identity])],format='csr')
        fit=linprog(np.r_[np.zeros(3),np.ones(len(weights))],A_ub=constraints,
                    b_ub=np.r_[-rhs,rhs],bounds=[(None,None)]*3+[(0,None)]*len(weights),method='highs')
        if not fit.success:
            records.append({'v':v,'success':False,'message':fit.message});continue
        cost=float(weights@np.abs(kernel-design@fit.x[:3]))
        records.append({'v':v,'success':True,'controls_before_common_scaling':fit.x[:3].tolist(),
                        'controlled_absolute_row_over_nu':cost/nu,
                        'raw_absolute_row_over_nu':float(weights@np.abs(kernel))/nu,
                        'objective_reconstruction_difference':float(fit.fun-cost),
                        'seconds':time.perf_counter()-tick})
    result={'status':'FLOAT_PREVIEW_not_continuum_certificate','beta':'3/4',
            'representation':'(f-M)/M^beta','radial_order':96,'angular_order':64,
            'records':records,'seconds_total':time.perf_counter()-started,
            'global_or_nonlinear_receiver_acquired':False}
    (Path(__file__).parent/'MAXWELLIAN_WEIGHT_PREVIEW.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
