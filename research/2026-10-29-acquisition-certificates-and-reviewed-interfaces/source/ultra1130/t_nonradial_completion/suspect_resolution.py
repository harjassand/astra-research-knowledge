"""A fixed suspect row, challenged in an independent cylindrical quadrature.

Not a theorem. Uses independent normal axial and chi2 transverse weights,
so it does not reuse the spherical radial/cosine quadrature's near-diagonal
aliasing. No kinetic or time/source grid is generated.
"""
from pathlib import Path
import json, math, time
import numpy as np
from scipy.special import roots_hermitenorm, roots_laguerre
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack, vstack, eye


def fixed(v, nz, nt, beta=.75):
    start = time.perf_counter()
    z, wz = roots_hermitenorm(nz)
    radial, wr = roots_laguerre(nt)
    z = z[:, None]/math.sqrt(beta)
    rho2 = 2*radial[None, :]/beta
    shape = (nz, nt)
    s2 = np.broadcast_to(z*z+rho2, shape).ravel()
    zflat = np.broadcast_to(z, shape).ravel()
    r2 = (v-z)**2+rho2
    kernel = (4*np.exp(v*v*rho2/(2*r2))/np.sqrt(r2)-np.sqrt(r2)).ravel()
    weights = (wz[:, None]/math.sqrt(2*math.pi)*wr[None, :]).ravel()
    weights *= beta**(-1.5)*math.exp(-(1-beta)*v*v/2)
    design = np.column_stack([np.ones(nz*nt), zflat, s2])
    ident = eye(nz*nt, format='csr')
    matrix = csr_matrix(design*weights[:, None])
    rhs = weights*kernel
    aub = vstack([hstack([-matrix,-ident]),hstack([matrix,-ident])],format='csr')
    fit = linprog(np.r_[np.zeros(3),np.ones(nz*nt)],A_ub=aub,
                  b_ub=np.r_[-rhs,rhs],bounds=[(None,None)]*3+[(0,None)]*(nz*nt),
                  method='highs', options={'dual_feasibility_tolerance':1e-9,
                                           'primal_feasibility_tolerance':1e-9})
    if not fit.success:
        raise ArithmeticError(fit.message)
    nu = (2*math.sqrt(2/math.pi) if v==0 else
          math.sqrt(2/math.pi)*math.exp(-v*v/2)+(v+1/v)*math.erf(v/math.sqrt(2)))
    cost = float(weights@np.abs(kernel-design@fit.x[:3]))/nu
    return {'v':v,'beta':beta,'orders':[nz,nt],'row':cost,'controls':fit.x[:3].tolist(),
            'objective_gap':float(fit.fun/nu-cost), 'seconds':time.perf_counter()-start}


def main():
    v = 3.3976774146868998
    result = {'status':'INDEPENDENT_COORDINATE_FLOAT_DIAGNOSTIC',
              'records':[fixed(v,96,96),fixed(v,192,192)],
              'global_admission':False}
    Path(__file__).with_name('SUSPECT_RESOLUTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
