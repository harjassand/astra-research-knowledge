"""Conservative complete-operation budget; no experimental parameters."""
import json
import math
from pathlib import Path


def budget(g, h, d, nu, eps):
    M=2*h+d
    tau=g/M**2
    r=(math.sqrt(2)-.5)**2*(g/M)**4
    Nc=math.ceil(math.log((eps/8)**2)/math.log1p(-r))
    Nr=math.ceil(math.log(eps/8)/math.log1p(-r))
    R=Nc+Nr
    delta=eps/(4*R)
    x=delta/(math.sqrt(1+2*delta)+1)  # solves 2*x+2*x*x=delta
    p=x*x
    m=math.ceil(math.log(2/p)/(2*(.25-nu)**2))
    pQ=2*math.exp(-2*m*(.25-nu)**2)
    err=math.sqrt((1-r)**Nc)+(1-r)**Nc+(1-r)**Nr+R*(2*math.sqrt(pQ)+2*pQ)
    assert err <= .6*eps
    return {
        'g':g,'h':h,'d':d,'nu':nu,'target_epsilon':eps,
        'r':r,'tau':tau,'capture_cap':Nc,'return_cap':Nr,
        'charge_reads':R,'probes_per_charge_read':m,
        'total_probe_uses_bound':R*m,
        'total_tunnel_exposure_bound':R*tau,
        'statistical_instrument_error_bound':err,
        'wall_time_formula':f'{R} * t_switch + {R*tau:.12g} + {R*m} * t_probe',
        'remaining_error_budget_at_least':eps-err,
        'note':'All other physical errors and initial data loading are additional; t_probe includes every probe operation.'
    }


if __name__=='__main__':
    rows=[budget(g,h,d,.05,eps)
          for g,h,d in [(1.,1.,0.),(.6,1.4,.2)]
          for eps in [.01,.001,1e-6]]
    p=Path(__file__).with_name('resource_budget_results.json')
    p.write_text(json.dumps({'status':'Conservative theorem parameters, not device estimates',
                             'budgets':rows},indent=2)+'\n')
    print(json.dumps(rows,indent=2))
