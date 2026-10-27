"""Exact conditional retry gate. No read, write or reset law acquired."""
from fractions import Fraction as F
from pathlib import Path
import json
import math

def val(x): return {'exact':str(x),'float':float(x)}

def main():
    goal=F(99,100)
    rows=[]
    for p in (F(16,100),F(28,100),F(68,100),F(90,100)):
        for q in (F(995,1000),F(9999,10000)):
            # Proposal probability p; read survival q and perfect classification;
            # rejected proposal resets cleanly with probability r. Failures end run.
            success=q*p/(1-q*(1-p))
            r_needed=(1-q*p/goal)/(q*(1-p))
            q_needed=goal/(p+goal*(1-p))
            rows.append({'declared_proposal_probability':val(p),
                         'declared_read_survival':val(q),
                         'success_with_perfect_reset':val(success),
                         'reset_success_needed_for_99percent':val(r_needed),
                         'feasible_reset_probability_exists':r_needed<=1,
                         'read_survival_needed_even_with_perfect_reset':val(q_needed),
                         'expected_attempts_with_perfect_reset':val(1/(1-q*(1-p)))})
    p,q,r=F(7,10),F(999,1000),F(999,1000)
    c=q*(1-p)*r
    for k in (1,2,10,40):
        finite=sum((q*p*c**i for i in range(k)),F(0))
        assert finite==q*p*(1-c**k)/(1-c)
    pulse_rows=[]
    for p in (0.16,0.28,0.68,0.90):
        # Optimistic fixed Poisson kernel, perfect classification/reset;
        # every >=2-event pulse is recognized but terminal.
        limit=p*(1-float(goal))/(p+float(goal)*(1-p))
        q_needed=(1-limit)*math.exp(limit)
        for q in (0.995,0.9999,0.99999):
            lo,hi=0.,1.
            for _ in range(70):
                mid=(lo+hi)/2
                if 1-mid-q*math.exp(-mid)>0: lo=mid
                else: hi=mid
            mean=(lo+hi)/2
            pulse_rows.append({'declared_target_event_fraction':p,'declared_read_survival':q,
                               'optimal_pulse_mean_events':mean,
                               'best_success':p*(1-mean)/(p+(1-p)*mean),
                               'read_survival_required_for_99percent':q_needed})
    out={'scope':__doc__,'target_success':val(goal),'rows':rows,'finite_pulse_rows':pulse_rows,
         'guarantees':'Exact for stated regenerative model, perfect classification, failures terminal. Parameters are illustrative, not acquired physical fidelities.'}
    Path(__file__).resolve().with_name('HERALDED_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
