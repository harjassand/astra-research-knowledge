"""Independent high-precision endpoint/rounding checks; not an interval proof."""
import json
from pathlib import Path
import mpmath as mp
mp.mp.dps = 100


def logcosh(x):
    return x + mp.log1p(mp.exp(-2*x)) - mp.log(2)


def case(tau, kappa, epsilon):
    L=mp.log(1/epsilon); L1=mp.log(4/epsilon)
    F=L*L/tau if mp.isinf(kappa) else mp.sqrt(kappa)*L*mp.log1p(L/(tau*mp.sqrt(kappa)))
    m=int(mp.ceil(min(mp.sqrt(kappa)*L1/2,L1*L1/(2*tau))))
    h=tau/(m+1)
    lo=-mp.expm1(-h)
    up=mp.mpf(1) if mp.isinf(kappa) else -mp.expm1(-kappa*h)
    beta=2*mp.atanh(mp.sqrt(lo/up))
    a=1-up; b=1-lo; width=up-lo
    logW=logcosh(m*mp.acosh((2+a+b)/width))-logcosh(m*beta)
    logbias=-logcosh(m*beta)
    assert logbias <= mp.log(epsilon/2)+mp.mpf('1e-80')
    L0=mp.log(1/(4*epsilon))
    K=min(kappa,(L0/(8*mp.e*tau))**2)
    lower_m=int(mp.floor(mp.sqrt(K)*L0/4))
    q=(mp.sqrt(K)-1)/(mp.sqrt(K)+1)
    exact_gap=(K-1)/K*q**lower_m
    assert K>=16 and lower_m+1>=2 and exact_gap>4*epsilon
    R=mp.e*tau*(K-1)/(lower_m+1)
    assert R<=mp.mpf('.5')
    minus_log_kernel=-(mp.log(2)+(lower_m+1)*mp.log(R))
    return dict(tau=str(tau),kappa=str(kappa),epsilon=mp.nstr(epsilon,8),
                upper_degree=m,lower_degree=lower_m,
                log_precision_cost_over_F=float((logW+mp.log(2/epsilon))/F),
                minus_log_kernel_bound_over_F=float(minus_log_kernel/F),
                gap_over_4epsilon=float(exact_gap/(4*epsilon)))


def main():
    taus=[mp.mpf(1)/64,mp.mpf('1e-3'),mp.mpf('1e-6'),mp.mpf('1e-10')]
    kappas=[mp.mpf(16),mp.mpf(100),mp.mpf('1e4'),mp.mpf('1e8'),mp.mpf('1e20'),mp.inf]
    epsilons=[mp.mpf(1)/16,mp.mpf('1e-3'),mp.exp(-30),mp.exp(-100),mp.exp(-1000)]
    rows=[case(t,k,e) for t in taus for k in kappas for e in epsilons]
    out=dict(cases=len(rows),precision_decimal_digits=mp.mp.dps,
             min_lower_exponent_ratio=min(r['minus_log_kernel_bound_over_F'] for r in rows),
             max_upper_log_precision_ratio=max(r['log_precision_cost_over_F'] for r in rows),
             minimum_gap_margin=min(r['gap_over_4epsilon'] for r in rows),rows=rows)
    Path(__file__).with_name('audit_grid.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))


if __name__=='__main__':
    main()
