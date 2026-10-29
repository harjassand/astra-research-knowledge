"""Finite outward cover, not a grid inference.

Every accepted interval covers ALL speed values in that interval and ALL
native partner angles/radii. Infinite tails are bounded analytically.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time
from flint import arb
from certify_nonradial import Integrator,controls,ball,ser,dyadic,BETA,ETA


def main():
    start=time.perf_counter();admitted=[];failed=[];attempts=[]
    pending=[(F(j,4),F(j+1,4)) for j in range(31,-1,-1)]
    while pending:
        lo,hi=pending.pop()
        co=controls((lo+hi)/2)
        tick=time.perf_counter()
        row=Integrator(lo,hi,co).run(max_cells=6000)
        row['seconds']=time.perf_counter()-tick
        attempts.append(row)
        if row['status']=='PASS':admitted.append(row)
        elif hi-lo<=F(1,1024) or len(attempts)>=512:
            failed.append(row);break
        else:
            mid=(lo+hi)/2;pending.extend([(mid,hi),(lo,mid)])
        if len(attempts)%16==0:
            print(json.dumps({'attempts':len(attempts),'admitted':len(admitted),
                              'pending':len(pending),'seconds':time.perf_counter()-start}),flush=True)
    v=ball(8);beta=ball(BETA)
    tail=ball(F(5,4))*(4/(beta*(1-beta)*v*v)
        +beta**(-1)*beta.rsqrt()*(-(1-beta)*v*v/2).exp()
         *(1+2*(2/(arb.pi()*beta)).sqrt()/v))
    passed=not pending and not failed and tail<ball(ETA)
    result={'status':'PASS_FULL_CONTINUUM' if passed else 'NOT_ACQUIRED',
            'eta':str(ETA),'beta':str(BETA),
            'phi':'1+4((s^2-4)(25-s^2))^2/194481 for2<=s<=5; else1',
            'phi_bounds':['1','5/4'],'head_domain':['0','8'],
            'admitted':admitted,'failed':failed,
            'pending':[[ser(a),ser(b)] for a,b in pending],
            'attempts':attempts,'tail_start':'8',
            'tail_row_upper':ser(dyadic(tail.upper())),
            'tail_row_display':float(tail),
            'attempt_count':len(attempts),'admitted_count':len(admitted),
            'all_box_evaluations':sum(x['box_evaluations'] for x in attempts),
            'seconds':time.perf_counter()-start,
            'continuous_velocity_output':False,'finite_bit_output':False}
    Path(__file__).with_name('NONRADIAL_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('admitted','attempts')},indent=2))


if __name__=='__main__':main()
