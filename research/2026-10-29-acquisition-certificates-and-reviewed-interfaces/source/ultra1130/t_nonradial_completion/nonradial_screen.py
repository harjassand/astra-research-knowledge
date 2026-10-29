"""Targeted max/min diagnostic of the FULL angular controlled row.

This is not an enclosure and never admits a continuum row or source.
Unlike the radial certificate, absolute value is taken before angular
integration. Axially allowed controls are 1,w_parallel,|w|^2.
"""
from pathlib import Path
import json, math, time
import numpy as np
from scipy.special import roots_genlaguerre, roots_legendre
from scipy.optimize import linprog, minimize_scalar
from scipy.sparse import csr_matrix, hstack, vstack, eye


def make_row(nr=96, na=64, beta=.75):
    radial, wr = roots_genlaguerre(nr, .5)
    mu, wm = roots_legendre(na)
    s = np.sqrt(2*radial/beta)[:, None]
    mu = mu[None, :]
    weights0 = (wr[:, None]/math.gamma(1.5)*wm[None, :]/2).ravel()
    s2 = np.broadcast_to(s*s, (nr, na)).ravel()
    design = np.column_stack([np.ones(nr*na), (s*mu).ravel(), s2])
    ident = eye(nr*na, format='csr')
    records = []

    def row(v):
        start = time.perf_counter()
        r2 = v*v+s*s-2*v*s*mu
        r = np.sqrt(r2)
        perp2 = v*v*s*s*(1-mu*mu)/r2
        kernel = (4*np.exp(perp2/2)/r-r).ravel()
        nu = (2*math.sqrt(2/math.pi) if v == 0 else
              math.sqrt(2/math.pi)*math.exp(-v*v/2)
              +(v+1/v)*math.erf(v/math.sqrt(2)))
        weights = weights0*beta**(-1.5)*math.exp(-(1-beta)*v*v/2)
        matrix = csr_matrix(design*weights[:, None])
        rhs = weights*kernel
        aub = vstack([hstack([-matrix, -ident]),
                      hstack([matrix, -ident])], format='csr')
        fit = linprog(np.r_[np.zeros(3), np.ones(nr*na)],
                      A_ub=aub, b_ub=np.r_[-rhs, rhs],
                      bounds=[(None, None)]*3+[(0, None)]*(nr*na),
                      method='highs', options={'dual_feasibility_tolerance':1e-9,
                                               'primal_feasibility_tolerance':1e-9})
        if not fit.success:
            raise ArithmeticError(fit.message)
        coeff = fit.x[:3]
        residual = kernel-design@coeff
        cost = float(weights@np.abs(residual))/nu
        # An LP dual control, still only on the quadrature measure.
        signed = fit.ineqlin.marginals[:nr*na]-fit.ineqlin.marginals[nr*na:]
        dual = float((-rhs)@fit.ineqlin.marginals[:nr*na]
                     +rhs@fit.ineqlin.marginals[nr*na:])/nu
        records.append({'v':float(v), 'row':cost, 'controls':coeff.tolist(),
                        'dual':dual,
                        'quadrature_dual_moment':(design.T@(weights*signed)).tolist(),
                        'objective_reconstruction':float(fit.fun/nu-cost),
                        'seconds':time.perf_counter()-start})
        return cost
    return row, records


def main():
    begin = time.perf_counter()
    row, records = make_row()
    anchors = {str(v):row(v) for v in (0., 2., 4., 6., 8.)}
    fit = minimize_scalar(lambda v:-row(v), bounds=(2., 6.),
                          method='bounded', options={'xatol':.002, 'maxiter':35})
    # One fixed-location resolution challenge, not another source/cohort.
    fine, fine_records = make_row(160, 128)
    fine(float(fit.x))
    result = {'status':'DETERMINISTIC_FLOAT_DIAGNOSTIC_NOT_A_THEOREM',
              'beta':'3/4', 'full_angular_absolute_value':True,
              'moment_controls':['mass', 'parallel_momentum', 'energy'],
              'coarse_orders':[96,64], 'anchors':anchors,
              'bounded_optimizer':{'success':bool(fit.success), 'v':float(fit.x),
                                   'row':float(-fit.fun), 'evaluations':int(fit.nfev)},
              'records':records, 'fixed_location_resolution_orders':[160,128],
              'resolution_challenge':fine_records,
              'seconds':time.perf_counter()-begin,
              'nonradial_global_operation_acquired':False}
    target = Path(__file__).with_name('NONRADIAL_SCREEN.json')
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}, indent=2))


if __name__=='__main__':
    main()
