"""Independent small full-state equations and explicit residual checks.

The oracle rates use heatbath Gibbs ratios, not sparse_galerkin's rate table.
Both killed and full Poisson equations are assembled on the complete small
even-parity space. Large fixtures never use this enumeration.
"""
from fractions import Fraction as F
from pathlib import Path
import sys, json, time
sys.dont_write_bytecode = True
from sparse_galerkin import (certify, fixture, decode, rational_box, ActualOperator,
                             fmpq, fmpq_mat)


def prod(xs):
    p = F(1)
    for x in xs:
        p *= x
    return p


def solve(A,b):
    mat = fmpq_mat([[fmpq(x.numerator,x.denominator) for x in row] for row in A])
    rhs = fmpq_mat([[fmpq(x.numerator,x.denominator)] for x in b])
    ans = mat.solve(rhs)
    assert mat*ans == rhs
    return [F(int(ans[i,0].p),int(ans[i,0].q)) for i in range(len(b))]


def dense_model(theta, clocks, delta):
    m = len(theta)
    states = [x for x in range(1<<m) if x.bit_count()%2 == 0]
    index = {x:i for i,x in enumerate(states)}
    w = [prod(theta[i] for i in range(m) if x>>i&1) for x in states]
    dim = len(states)
    H = [[F(0) for _ in states] for _ in states]
    for ix,x in enumerate(states):
        for i,clock in enumerate(clocks):
            y = x ^ (3<<i)
            iy = index[y]
            # Heatbath ratio: rate(x,y)=alpha*w(y)/(w(x)+w(y)).
            # The outside bit is untouched by this spin/pair flip.
            outside_site = i-1 if i else 2
            factor = 1+delta*((x>>outside_site)&1)
            q = clock*w[iy]/(w[ix]+w[iy])*factor
            H[ix][ix] += q
            H[ix][iy] -= q
    assert all(sum(row,F(0)) == 0 for row in H)
    assert all(w[i]*H[i][j] == w[j]*H[j][i]
               for i in range(dim) for j in range(dim))
    return states,index,w,H


def mv(A,v):
    return [sum((a*x for a,x in zip(row,v)),F(0)) for row in A]


def dotw(w,a,b):
    return sum((wi*ai*bi for wi,ai,bi in zip(w,a,b)),F(0))


def exact_oracles(states,index,w,H):
    ia,ib = index[0],index[max(states)]
    rho = w[ib]
    ra = H[ia][ia]
    keep = [i for i in range(len(states)) if i not in (ia,ib)]
    q = [F(0)]*len(states)
    q[ib] = F(1)
    solved = solve([[H[i][j] for j in keep] for i in keep],
                   [-H[i][ib] for i in keep])
    for i,value in zip(keep,solved):
        q[i] = value
    assert all(mv(H,q)[i] == 0 for i in keep)
    p = -sum((H[ia][j]*q[j] for j in range(len(states)) if j != ia),F(0))/ra
    u = [F(0)]*len(states)
    u[ia],u[ib] = rho,F(-1)
    rest = [i for i in range(len(states)) if i != ia]
    z = [F(0)]*len(states)
    solved = solve([[H[i][j] for j in rest] for i in rest],[u[i] for i in rest])
    for i,value in zip(rest,solved):
        z[i] = value
    assert mv(H,z) == u
    exact_I = dotw(w,u,z)/rho
    assert exact_I == -z[ib] == rho/(ra*p)
    assert 0 < p < 1
    return exact_I,p,u,ra


def one_check(theta,clocks,delta,name):
    start = time.perf_counter()
    states,index,w,H = dense_model(theta,clocks,delta)
    exact_I,p,u,ra = exact_oracles(states,index,w,H)
    result,internal = certify(theta,clocks,delta,max_degree=3,
                              eps=F(1,10**8),return_internal=True)
    op,vectors,gram,alpha = internal
    assert op.Ra == ra
    assert op.rho == w[-1]
    # A vector with arbitrary mean verifies complete BACKWARD orientation.
    generic = {x:(17*i%23)-11 for i,x in enumerate(states)}
    sparse_A = op.apply_A(generic)
    dense_A = [op.D*z for z in mv(H,[F(generic[x]) for x in states])]
    assert all(sparse_A.get(x,0) == dense_A[i] for i,x in enumerate(states))
    for record in result['degrees']:
        assert decode(record['I_lower']) <= exact_I <= decode(record['I_upper'])
        assert decode(record['p_lower']) <= p <= decode(record['p_upper'])
    y = [F(op.D,op.W)*sum((a*v.get(x,0)
          for a,v in zip(alpha,vectors)),F(0)) for x in states]
    Hy = mv(H,y)
    residual = [ui-h for ui,h in zip(u,Hy)]
    L = (2*dotw(w,u,y)-dotw(w,y,Hy))/op.rho
    error = dotw(w,residual,residual)/(op.rho*op.gap)
    last = result['degrees'][-1]
    assert L == decode(last['raw_Galerkin_lower'])
    assert L+error == decode(last['raw_residual_upper'])
    assert dotw(w,residual,residual)*(op.W**3) == decode(last['residual_norm_scaled'])
    for v in vectors[:-1]:
        assert dotw(w,[F(v.get(x,0)) for x in states],residual) == 0
    # Adding a constant is harmless; the certificate uses a pseudoinverse,
    # not an unstated zero-mean requirement on the trial function.
    shifted = [v+F(7,13) for v in y]
    Hshifted = mv(H,shifted)
    assert Hshifted == Hy
    assert (2*dotw(w,u,shifted)-dotw(w,shifted,Hshifted))/op.rho == L
    assert sum((wi*ri for wi,ri in zip(w,residual)),F(0)) == 0
    assert L <= exact_I <= L+error
    return {'name':name,'M':len(theta),'delta':str(delta),'states':len(states),
            'exact_p':rational_box(p),'exact_I':rational_box(exact_I),
            'certified_p_lower':result['p_lower'],'certified_p_upper':result['p_upper'],
            'degree_widths':[q['relative_width'] for q in result['degrees']],
            'full_operator_orientation':'PASS','full_residual_Gram_identity':'PASS',
            'independent_killed_Poisson_agreement':'PASS',
            'arbitrary_constant_trial_invariance':'PASS',
            'weighted_residual_mean_and_Galerkin_orthogonality':'PASS',
            'all_degrees_contain_exact':'PASS','seconds':time.perf_counter()-start}


if __name__ == '__main__':
    fixtures = [('accepted_M4',*fixture(4)),('accepted_M6',*fixture(6)),
                ('new_M6',[F(2,5),F(3,8),F(7,13),F(4,9),F(5,12),F(8,15)],
                 [F(5,4),F(7,6),F(9,8),F(11,10),F(13,12)])]
    checks = []
    for name,theta,clocks in fixtures:
        for delta in (F(0),F(1,20),F(1,2)):
            checks.append(one_check(theta,clocks,delta,name))
            print(name,str(delta),checks[-1]['degree_widths'],flush=True)
    out = {'status':'PASS','checks':checks,
           'scope':'Nine fully enumerated small models, 27 degree enclosures; no exhaustive large-model oracle.'}
    Path('EXACT_SMALL_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',len(checks),'models',flush=True)
