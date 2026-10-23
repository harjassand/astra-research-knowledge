"""Principal exact-kernel and Decimal law/cost calculations for the new theorem.

No Monte Carlo trajectories. Only standard Python. Decimal calculations are
rounded, not outward interval certificates. Exact rational kernels implement
every branch of the actual two-stage operation, including early rejection.
"""
import argparse
from decimal import Decimal as D, localcontext, ROUND_CEILING
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import resource
import time


def matmul(a, b):
    m, p, n = len(a), len(b), len(b[0])
    return [[sum((a[i][k]*b[k][j] for k in range(p)), 0)
             for j in range(n)] for i in range(m)]


def rowmul(v, a):
    return [sum((v[i]*a[i][j] for i in range(len(v))), 0)
            for j in range(len(a[0]))]


def identity(n, one=F(1)):
    return [[one if i == j else one*0 for j in range(n)] for i in range(n)]


def power(a, n):
    out = identity(len(a), a[0][0]*0+1)
    while n:
        if n & 1:
            out = matmul(out, a)
        n >>= 1
        if n:
            a = matmul(a, a)
    return out


def mh(target, proposal):
    n = len(target)
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x != y and proposal[x][y]:
                out[x][y] = min(proposal[x][y],
                                target[y]*proposal[y][x]/target[x])
        out[x][x] = 1-sum(out[x])
    return out


def outcomes(kind, x, q, pi, Q, alpha=F(1, 2)):
    """Yield probability, next state, queried label (or None), global/local draws.

    A query tag indicates reaching a target evaluation, not a forced new call:
    complete memoization below reuses previously queried labels.
    """
    n = len(q)
    if kind == 'pure_imh':
        wg, wl, wi = F(1), F(0), F(0)
    else:
        wg, wl, wi = alpha/2, (1-alpha)/2, F(1, 2)
    if wi:
        yield wi, x, None, 0, 0
    for y in range(n):
        a = min(F(1), pi[y]*q[x]/(pi[x]*q[y]))
        tag = None if x == y else y
        if wg*q[y]*a:
            yield wg*q[y]*a, y, tag, 1, 0
        if wg*q[y]*(1-a):
            yield wg*q[y]*(1-a), x, tag, 1, 0
        if wl and Q[x][y]:
            if x == y:
                yield wl*Q[x][y], x, None, 0, 1
                continue
            rq = q[y]*Q[y][x]/(q[x]*Q[x][y])
            rp = pi[y]*Q[y][x]/(pi[x]*Q[x][y])
            if kind == 'ordinary_hybrid':
                a1, a2 = F(1), min(F(1), rp)
            else:
                a1 = min(F(1), rq)
                a2 = min(F(1), pi[y]*q[x]/(pi[x]*q[y]))
            if 1-a1:
                yield wl*Q[x][y]*(1-a1), x, None, 0, 1
            if a1*a2:
                yield wl*Q[x][y]*a1*a2, y, y, 0, 1
            if a1*(1-a2):
                yield wl*Q[x][y]*a1*(1-a2), x, y, 0, 1


def operation(kind, q, pi, Q):
    n = len(q)
    P = [[F(0) for _ in range(n)] for _ in range(n)]
    reward = [[F(0)] for _ in range(n)]
    killed = [[[F(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for x in range(n):
        terms = list(outcomes(kind, x, q, pi, Q))
        assert sum(p for p, *_ in terms) == 1
        for p, y, query, _g, _l in terms:
            P[x][y] += p
            if query is not None:
                reward[x][0] += p
            for never_queried in range(n):
                if x != never_queried and query != never_queried:
                    killed[never_queried][x][y] += p
    return P, reward, killed


def dec(x):
    if isinstance(x, F):
        return D(x.numerator)/D(x.denominator)
    return D(x)


def convert(a):
    return [[dec(x) for x in row] for row in a]


def tv(v, pi):
    return sum(abs(x-y) for x, y in zip(v, pi))/2


def law_cost(n, q, pi, P, reward, killed):
    d = len(q)
    law = rowmul(q, power(P, n))
    aug = [P[i]+[reward[i][0]] for i in range(d)]
    aug.append([D(0)]*d+[D(1)])
    pn = power(aug, n)
    current_only_calls = 1+sum(q[i]*pn[i][d] for i in range(d))
    all_cache_calls = D(0)
    for label in range(d):
        init = [q[x] if x != label else D(0) for x in range(d)]
        never = sum(rowmul(init, power(killed[label], n)))
        all_cache_calls += 1-never
    return {'steps':n, 'law':law, 'TV':tv(law, pi),
            'target_calls_current_only_cache':current_only_calls,
            'target_calls_complete_memoization':all_cache_calls}


def first_crossing(q, pi, P, eps):
    count = 0
    def risk(n):
        nonlocal count
        count += 1
        return tv(rowmul(q, power(P, n)), pi)
    if risk(0) <= eps:
        return 0, count
    hi = 1
    while risk(hi) > eps:
        hi *= 2
        if hi > 2**60:
            raise RuntimeError('predeclared search cap reached')
    lo = hi//2 if hi > 1 else 0
    while hi-lo > 1:
        mid = (lo+hi)//2
        if risk(mid) <= eps:
            hi = mid
        else:
            lo = mid
    assert risk(hi) <= eps and risk(hi-1) > eps
    return hi, count


def entropy(h):
    return -h*h.ln()-(1-h)*(1-h).ln()


def envelope(K, h):
    return 1-(-(K+entropy(h))/(1-h)).exp()


def finite_bound(K, alpha, Lambda, eps, x):
    """Theorem Eq3.9, with explicit valid proof choices and t=ceil(exp(x))."""
    x = D(x)
    ex = x.exp()
    c = (1+2*alpha+(1-alpha)*Lambda)/2
    h = eps**2
    bh = envelope(K, h)
    theta = 1-alpha*(1-bh)/2
    s = max(0, int(( (eps**2/bh).ln()/theta.ln()).to_integral_value(
                   rounding=ROUND_CEILING)))
    A = c**s
    S = (c**(s+1)-1)/(c-1)
    B = ex/(A*A*x**4)
    R = ex/x**4
    if B <= 3 or R <= 3 or 1/B >= h:
        return None
    b = envelope(K, 1/B)
    a = min(D(1), K/(R.ln()-1))
    d = min(D(1), bh*theta**s+b*S/(B*h))
    M = (2*K+1).exp()
    U = M*(A*A*B+1)+A*A+R
    Delta = (2*U/(alpha*(2*ex+1))).sqrt()
    eta = (2/(ex+1)).sqrt()
    kap = (1-alpha)/(1-alpha*b)
    dl = (alpha*(Delta+a/R)+eta)/(1-alpha*b)
    bound = max(a,kap*d)+Delta+dl*d+b/B+A*a/R
    return {'bound':bound,'proof_split_s':s,'log_density_cap':A.ln(),
            'log_B':B.ln(),'log_R':R.ln(),'high_target_tail_bound':a,
            'low_state_mass_bound':d,'core_bound':Delta,
            'low_range_error':dl*d,'small_tail_corrections':b/B+A*a/R,
            'log_total_steps_upper':(ex+D(s)+1).ln()}


def pure_bound(K, x):
    x = D(x)
    R = x.exp()/x**2
    if R <= 3:
        return None
    a = K/(R.ln()-1)
    if a >= 1:
        return None
    return {'bound':a*(1+1/R)+(-x*x*(1-a)).exp()}


def budget(evaluate, eps):
    count = 0
    def check(x):
        nonlocal count
        count += 1
        v = evaluate(x)
        return v, v is not None and v['bound'] <= D('0.95')*eps
    hi = 8
    while not check(hi)[1]:
        hi *= 2
        assert hi <= 2**20
    lo = 7
    while hi-lo > 1:
        mid = (hi+lo)//2
        if check(mid)[1]:
            hi = mid
        else:
            lo = mid
    v, yes = check(hi)
    assert yes
    return hi, v, count


def stringify(v):
    if isinstance(v, (D, F)):
        return str(v)
    if isinstance(v, dict):
        return {str(k):stringify(x) for k,x in v.items()}
    if isinstance(v, (tuple,list)):
        return [stringify(x) for x in v]
    return v


def run(precision):
    wall, cpu = time.perf_counter(), time.process_time()
    with localcontext() as ctx:
        ctx.prec = precision
        p,b,r,s = F(1,50),F(1,2),F(1,50*2**20),F(1,50*2**40)
        pi, q = [p,s,1-p-s], [r,b,1-b-r]
        Q = [[F(1,5),F(4,5),F(0)], [F(4,5),F(0),F(1,5)],
             [F(0),F(1,5),F(4,5)]]
        G = mh(pi,[q[:] for _ in q])
        R = mh(q,Q)
        ordinary = mh(pi,Q)
        safe = mh(pi,R)
        # Both stages compose exactly to ordinary MH with the q-reversible R.
        exact_ops={k:operation(k,q,pi,Q) for k in
                   ['pure_imh','ordinary_hybrid','safe_hybrid']}
        assert exact_ops['pure_imh'][0] == G
        for label, L in [('ordinary_hybrid',ordinary),('safe_hybrid',safe)]:
            expected=[[(F(i==j)+G[i][j]/2+L[i][j]/2)/2
                      for j in range(3)] for i in range(3)]
            assert exact_ops[label][0] == expected
        for P in [G,ordinary,safe,R]:
            assert all(sum(row)==1 and min(row)>=0 for row in P)
        for L in [G,ordinary,safe]:
            assert all(pi[i]*L[i][j]==pi[j]*L[j][i]
                       for i in range(3) for j in range(3))
        assert rowmul(q,R) == q
        qsafe = rowmul(q,safe)
        assert all(qsafe[i] <= 2*q[i] for i in range(3))
        assert all(safe[i][j] <= ordinary[i][j]
                   for i in range(3) for j in range(3) if i!=j)
        qd,pd = list(map(dec,q)), list(map(dec,pi))
        KL = sum(pd[i]*(pd[i]/qd[i]).ln() for i in range(3))
        assert KL < 1, 'frozen example not admitted; do not retune'
        output={'contract':{'precision_digits':precision,
            'arithmetic':'exact Fraction kernels; rounded Decimal powers, no interval certification',
            'K':D(1),'alpha':D('0.5'),'Lambda_safe':D(2),
            'no_trajectories':True,'full_finite_table_not_an_application':True},
            'input':{'q':q,'pi':pi,'Q':Q,'forward_KL':KL},
            'exact_kernels':{'G':G,'R_q_mh':R,'L_ordinary':ordinary,'L_safe':safe},
            'one_step_q_density':{
                'ordinary':[rowmul(q,ordinary)[i]/q[i] for i in range(3)],
                'safe':[qsafe[i]/q[i] for i in range(3)]},
            'horizons':{},'first_accuracy_crossings':{},'certificates':[]}
        exact_law_checks=0
        evals=0
        for kind,(Pf,rf,kf) in exact_ops.items():
            P,reward,killed=convert(Pf),convert(rf),list(map(convert,kf))
            rows=[]
            for n in [1,2,5,10,25,50,100,250,500,1000]:
                val=law_cost(n,qd,pd,P,reward,killed)
                val['expected_global_candidates_including_init'] = D(1)+D(n)*(1 if kind=='pure_imh' else D('0.25'))
                val['expected_local_Q_proposals'] = D(0) if kind=='pure_imh' else D(n)/4
                rows.append(val)
                if n in [1,2,5,10]:
                    exact=rowmul(q,power(Pf,n))
                    assert max(abs(dec(a)-d) for a,d in zip(exact,val['law'])) < D(10)**(-precision+5)
                    exact_law_checks+=1
            output['horizons'][kind]=rows
            crosses=[]
            for eps in map(D,['0.1','0.03','0.01']):
                n,ncalls=first_crossing(qd,pd,P,eps)
                evals+=ncalls
                val=law_cost(n,qd,pd,P,reward,killed)
                val.update({'epsilon':eps,
                    'TV_one_step_before':tv(rowmul(qd,power(P,n-1)),pd) if n else None,
                    'expected_global_candidates_including_init':D(1)+D(n)*(1 if kind=='pure_imh' else D('0.25')),
                    'expected_local_Q_proposals':D(0) if kind=='pure_imh' else D(n)/4})
                crosses.append(val)
            output['first_accuracy_crossings'][kind]=crosses
        certcalls=0
        for eps in map(D,['0.1','0.03','0.01','0.003','0.001']):
            x,v,cc=budget(lambda x:finite_bound(D(1),D('0.5'),D(2),eps,x),eps)
            xp,vp,cp=budget(lambda x:pure_bound(D(1),x),eps)
            certcalls+=cc+cp
            output['certificates'].append({'epsilon':eps,'safe_log_t_integer_x':x,
                'safe_parts':v,'pure_log_updates_integer_x':xp,'pure_parts':vp,
                'interpretation':'Sufficient analytical budgets only; not measured mixing times or speed ratios.'})
        output['checks']={'exact_kernel_and_reversibility':'PASS',
            'safe_domination':'PASS','frozen_forward_KL_admission':'PASS',
            'exact_law_comparisons':exact_law_checks,
            'accuracy_crossing_power_evaluations':evals,
            'scalar_certificate_evaluations':certcalls}
        output['resources']={'wall_seconds':time.perf_counter()-wall,
            'cpu_seconds':time.process_time()-cpu,
            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'python':platform.python_version(),'platform':platform.platform()}
        return stringify(output)


if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--precision',type=int,default=80)
    a.add_argument('--output',type=Path,required=True)
    args=a.parse_args()
    result=run(args.precision)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'checks':result['checks'],
        'resources':result['resources'],'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
        'forward_KL':result['input']['forward_KL'],
        'crossing_steps':{k:[r['steps'] for r in v] for k,v in result['first_accuracy_crossings'].items()},
        'certificate_log_budgets':[(r['epsilon'],r['safe_log_t_integer_x'],r['pure_log_updates_integer_x']) for r in result['certificates']]},indent=2))
