"""Evaluate a sufficient coarse acquisition bill; no observations are executed."""
import json,math
from pathlib import Path
import numpy as np
from run_direct_decision import LocalHoldSource

def evaluate(N):
    src=LocalHoldSource(N,1)
    t0,omega,stat,bias=5.,.01,.01,.0005
    radius=stat+bias; qlo=np.zeros((N,4)); qhi=np.zeros((N,4)); rmin=1.
    ratio=(1+omega)/(1-omega)
    for s in range(4):
        left,right=s//2,s%2; ii=np.arange(N)
        q=1/(1+np.exp(-(src.fields+np.roll(src.J,1)*left+src.J*right)))
        for u in ['slow_near_failure','fast_near_failure','mixed_clock']:
            r=src.rate(u,ii,left,right)
            dl=-np.expm1(-r*t0*(1-omega)); du=-np.expm1(-r*t0*(1+omega))
            al=np.maximum(0,q*dl-2*radius); au=np.minimum(1,q*du+2*radius)
            bl=np.maximum(0,(1-q)*dl-2*radius); bu=np.minimum(1,(1-q)*du+2*radius)
            lower=-np.log1p(-np.maximum(0,al+bl))/(t0*(1+omega))
            rmin=min(rmin,float(lower.min()))
            if u=='slow_near_failure':
                qlo[:,s]=al/(al+ratio*bu); qhi[:,s]=ratio*au/(ratio*au+bl)
    row=np.zeros(N)
    for bit in [1,2]:
        dif=np.zeros(N)
        for s in range(4): dif=np.maximum(dif,qhi[:,s]-qlo[:,s^bit])
        row+=dif
    alpha=1-float(row.max()); C=3*N*4; delta=.005
    m=math.ceil(math.log(4*C/delta)/(2*stat**2)); calls=2*C*m
    assert qhi.max()<.25 and qlo.min()>.025 and rmin>.2 and alpha>.7
    gamma,beta=.14,.01; xi=math.tanh(beta/2)
    prep=(N*math.log(1/.025)+math.log(1/xi))/gamma
    retry=math.ceil(math.log(.001)/math.log(.51))
    return {'N':N,'contexts_all_menus':C,'reads_per_start_bit_per_context':m,
       'pins_and_reads_upper':calls,'free_cell_exposure_upper':calls*t0*(1+omega),
       'calibration_hold_nominal':t0,'calibration_absolute_deadline_error':t0*omega,
       'conditional_indicator_bias':bias,'statistical_radius':stat,'confidence_failure':delta,
       'worst_good_event_numeric_margins':{'q_lower':float(qlo.min()),'q_upper':float(qhi.max()),
             'clock_lower':rmin,'Dobrushin_margin':alpha},
       'accepted_bounds':{'q_lower':.025,'q_upper':.25,'clock_lower':.2,'clock_upper_supplied':1.,'alpha':.7},
       'prep_density_log_allowance':beta,'prep_time_each_attempt':prep,'prep_retry_cap':retry,
       'prep_free_evolution_upper':prep*retry,
       'additional_costs':'All pin/read/context/timer/field/slew services, installation, N-bit inspection.'}

if __name__=='__main__':
    rows=[evaluate(N) for N in [64,256,1024,4096]]
    result={'status':'sufficient cost evaluation and deterministic margin diagnostic; NOT calibration execution',
        'precision':'floating margin checks with strict slack; actual certificates use interval formulas','rows':rows}
    Path(__file__).with_name('calibration_costs.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
