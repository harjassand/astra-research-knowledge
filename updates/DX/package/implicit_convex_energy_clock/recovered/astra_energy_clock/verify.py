"""Focused exact checks and one all-future certificate; no general QP solver.
Run: python verify.py
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import gzip
import json
import math
import sys
from energy_clock import (EnergyQP, Certificate, certificate_action,
                         compile_action_qp, certificate_vector, norm2,
                         geometric_mesh, is_psd)

# Integers arise from an explicitly bounded rational experiment, not user input.
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parent

def F(a):
    return [[Q(x) for x in row] for row in a]


def floor_dyadic(x: Q, bits: int) -> Q:
    scale = 1 << bits
    return Q((x.numerator*scale)//x.denominator, scale)


def hinge_prox(X: Q, Y: Q, h: Q) -> tuple[Q,Q]:
    """Prox of .5*x^2 + max(0,x-y), valid on all rational inputs."""
    x = X/(1+h)
    if x <= Y:
        return x,Y
    x = (X-h)/(1+h)
    y = Y+h
    if x >= y:
        return x,y
    v = (X+Y)/(h+2)
    return v,v


def hinge_certificate() -> tuple[EnergyQP,Certificate]:
    model = EnergyQP(F([[1,0,0],[0,0,0],[0,0,0]]),
                     [Q(0),Q(0),Q(1)],
                     F([[0,0,-1],[1,-1,-1]]),[Q(0),Q(0)],2)
    eta, a = Q(1,128),Q(1,3)
    c = Certificate([Q(0)],[[Q(1),Q(0),Q(1)]],[],[])
    for _ in range(5000):
        old = c.primal[-1]
        t = c.times[-1]
        h = eta*(a+t)
        X,Y = hinge_prox(old[0],old[1],h)
        x,y = floor_dyadic(X,32),floor_dyadic(Y,32)
        # Monotone dyadic rounding preserves 0 <= y-new minus y-old <= h.
        lam2 = (y-old[1])/h
        assert 0 <= lam2 <= 1
        vx = (old[0]-x)/h
        c.primal.append([x,y,max(Q(0),x-y)])
        c.dual_w.append([vx-lam2,Q(0),Q(0)])
        c.dual_lambda.append([1-lam2,lam2])
        c.times.append(t+h)
        if x == 0:
            break
    else:
        raise RuntimeError('Stop cap reached')
    return model,c


def exp_bounds(t: Q, n: int = 40) -> tuple[Q,Q]:
    if not 0 <= t <= 1:
        raise ValueError('This elementary bound is implemented on [0,1]')
    term = Q(1)
    s = term
    for j in range(1,n+1):
        term *= t/j
        s += term
    first = term*t/(n+1)
    return s,s+first/(1-t/(n+2))


def selected_limit_bracket(bits: int = 48) -> tuple[Q,Q]:
    lo,hi = Q(0),Q(1)
    for _ in range(bits):
        mid = (lo+hi)/2
        e0,e1 = exp_bounds(mid)
        if (1+mid)*e1 < 2:
            lo = mid
        elif (1+mid)*e0 > 2:
            hi = mid
        else:
            raise ArithmeticError('Taylor bound needs refinement')
    return lo,hi


def serialize(c: Certificate) -> dict:
    def vec(v): return [str(x) for x in v]
    return {
        'times':[str(t) for t in c.times],
        'primal':[vec(y) for y in c.primal],
        'dual_w':[vec(w) for w in c.dual_w],
        'dual_lambda':[vec(l) for l in c.dual_lambda],
    }


def main() -> None:
    assert is_psd(F([[1,-1],[-1,1]]))
    assert is_psd(F([[0,0],[0,3]]))
    assert not is_psd(F([[0,1],[1,0]]))
    model,c = hinge_certificate()
    action = certificate_action(model,c)
    assert 2*action <= Q(1,40000)  # Uniform error <= 0.005, for ALL future time.
    terminal = c.primal[-1]
    assert model.verify_minimizer(terminal,[Q(1),Q(0)])
    assert model.verify_minimizer([Q(0)]*3,[Q(1),Q(0)])
    C2 = model.tail_growth_constant([Q(0)]*3,[Q(1),Q(0)],Q(3,2))
    lo,hi = selected_limit_bracket()
    endpoint_error_upper = max(abs(terminal[1]-lo),abs(terminal[1]-hi))
    assert endpoint_error_upper**2 <= 2*action
    # Test independent sparse QP assembly on a prefix, not merely action arithmetic.
    n = 8
    prefix = Certificate(c.times[:n+1],c.primal[:n+1],c.dual_w[:n],c.dual_lambda[:n])
    qp = compile_action_qp(model,prefix.times,prefix.primal[0])
    qp_value = qp.evaluate_feasible(certificate_vector(prefix))
    assert qp_value == certificate_action(model,prefix)
    # An eliminated latent quadratic: F(x)=x^2/4, not joint gradient dynamics.
    latent = EnergyQP(F([[1,-1],[-1,2]]),[Q(0),Q(0)],[],[],1)
    mesh = geometric_mesh(Q(1,4),Q(1),Q(1,4),Q(4))
    lc = Certificate(mesh,[[Q(1),Q(1,2)]],[],[])
    for i in range(1,len(mesh)):
        h = mesh[i]-mesh[i-1]
        x = lc.primal[-1][0]/(1+h/2)
        y = [x,x/2]
        lc.primal.append(y)
        lc.dual_w.append(y.copy())
        lc.dual_lambda.append([])
    lv = certificate_action(latent,lc)
    lqp = compile_action_qp(latent,mesh,lc.primal[0])
    assert lqp.evaluate_feasible(certificate_vector(lc)) == lv
    assert 2*lv <= Q(1,4)
    # Exact fixed-large-step failure on the hinge energy.
    h = Q(10**6)
    xy = hinge_prox(Q(1),Q(0),h)
    assert xy == (1/(h+2),1/(h+2))
    xy2 = hinge_prox(*xy,h)
    assert xy2[1] == xy[1]
    assert lo - xy2[1] > Q(3,10)
    # Persist enough data to replay every all-future certificate equality.
    with gzip.open(ROOT/'hinge_certificate.json.gz','wt',encoding='utf-8') as fh:
        json.dump(serialize(c),fh,separators=(',',':'))
    (ROOT/'action_exact.txt').write_text(str(action)+'\n',encoding='utf-8')
    results = {
        'status':'exact rational assertions passed; no general QP optimizer implemented',
        'prototype':'F(x,y)=x^2/2+max(0,x-y), initial (1,0)',
        'certificate_cells':len(c.times)-1,
        'certificate_terminal_time_approx':float(c.times[-1]),
        'certificate_action_approx':float(action),
        'all_future_error_bound_approx':math.sqrt(float(2*action)),
        'all_future_error_squared_le_1_over_40000':True,
        'terminal_is_exact_minimizer':True,
        'terminal_y_exact':str(terminal[1]),
        'terminal_y_approx':float(terminal[1]),
        'true_selected_limit_interval':[str(lo),str(hi)],
        'true_selected_limit_approx':float((lo+hi)/2),
        'endpoint_error_upper_approx':float(endpoint_error_upper),
        'hoffman_growth_C_squared':str(C2),
        'sparse_QP_prefix_variables':qp.n,
        'sparse_QP_prefix_equalities':len(qp.equalities),
        'sparse_QP_prefix_inequalities':len(qp.inequalities),
        'sparse_QP_prefix_exact_objective_match':True,
        'latent_quadratic_exact_objective_match':True,
        'fixed_large_step_error_greater_than_0_3':True,
        'general_theorem_independently_reviewed':False,
        'historical_novelty_established':False,
        'limitations':['Exact verification is for supplied rational candidates.',
                       'The general polynomial-time convex-QP optimization backend is an imported theorem, not implemented here.',
                       'No PDE discretization or physical experiment is validated.']
    }
    (ROOT/'verification_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))

if __name__ == '__main__':
    main()
