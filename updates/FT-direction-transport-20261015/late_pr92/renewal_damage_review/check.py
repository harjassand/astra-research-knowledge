#!/usr/bin/env python3
"""Independent renewal/damage checks; all added hazard inputs are synthetic."""
from pathlib import Path
import json,math,random,statistics

HERE=Path(__file__).resolve().parent

def model(p,h,l,lam,d):
    per=[]
    for rate in (h,l):
        total=rate+lam
        a=math.exp(-total*d)
        m=-math.expm1(-total*d)/total if total else d
        per.append((a,rate*m,lam*m,m))
    a,b,c,m=[p*per[0][i]+(1-p)*per[1][i] for i in range(4)]
    return dict(a=a,b=b,c=c,m=m,Y=a/(a+c),q=p*per[0][0]/a,
                mean_dose=m/(a+c),mean_attempts=1/(a+c),dose_per_accepted=m/a,
                attempts_per_accepted=1/a)

def simulate(p,h,l,lam,d,n=50000):
    rng=random.Random(20261015)
    accepted=[];heavy=[];doses=[];attempts=[];accepted_attempts=[]
    for _ in range(n):
        dose=0.;count=0
        while True:
            count+=1;H=rng.random()<p;rate=h if H else l
            eject=rng.expovariate(rate) if rate else math.inf
            damage=rng.expovariate(lam)
            dose+=min(eject,damage,d)
            if d<eject and d<damage:
                accepted.append(1.);heavy.append(float(H));accepted_attempts.append(float(count));break
            if damage<eject:
                accepted.append(0.);break
        doses.append(dose);attempts.append(float(count))
    truth=model(p,h,l,lam,d)
    errors={}
    for key,samples in [('Y',accepted),('q',heavy),('mean_dose',doses),('mean_attempts',attempts)]:
        mean=statistics.mean(samples);se=statistics.stdev(samples)/math.sqrt(len(samples))
        z=abs(mean-truth[key])/se
        assert z<6,(key,z)
        errors[key]={'monte_carlo':mean,'formula':truth[key],'standard_error':se,'absolute_z_score':z}
    conditional_mean=statistics.mean(accepted_attempts)
    conditional_se=statistics.stdev(accepted_attempts)/math.sqrt(len(accepted_attempts))
    assert abs(conditional_mean-truth['mean_attempts'])<6*conditional_se
    return {'independent_first_event_race_simulation':errors,
            'conditional_attempts_given_accepted':{'monte_carlo':conditional_mean,'standard_error':conditional_se,
                'exact_1_over_a_plus_c':truth['mean_attempts'],'aggregate_attempts_per_accepted_1_over_a':truth['attempts_per_accepted']},
            'initial_sites':n,'parameters':dict(p=p,sigma_H=h,sigma_L=l,collateral_lambda=lam,d=d),'scope':'synthetic model only'}

def run():
    rng=random.Random(20261015)
    max_identity=0.;max_renewal=0.;min_posterior_gap=1.
    for _ in range(1000):
        p=rng.uniform(.001,.999);h=rng.uniform(0,3);l=h+rng.uniform(.1,5)
        lam=rng.uniform(.001,2);d=rng.uniform(.001,3)
        z=model(p,h,l,lam,d)
        max_identity=max(max_identity,abs(1-z['Y']-lam*z['mean_dose']))
        max_renewal=max(max_renewal,abs(z['Y']-(z['a']+z['b']*z['Y'])))
        q0=p*math.exp(-h*d)/(p*math.exp(-h*d)+(1-p)*math.exp(-l*d))
        assert math.isclose(z['q'],q0,rel_tol=1e-12)
        lo=rng.random();up=rng.random()
        trueH=rng.uniform(lo,1);trueL=rng.uniform(0,up)
        bound=p*lo/(p*lo+(1-p)*up)
        actual=p*trueH/(p*trueH+(1-p)*trueL)
        min_posterior_gap=min(min_posterior_gap,actual-bound)
        ex=rng.uniform(0,p*lo)
        final_lower=(p*lo-ex)/(p*lo+(1-p)*up)
        # Worst permitted direction: all changed accepted mass is H->L.
        actual_final=(p*trueH-ex)/(p*trueH+(1-p)*trueL)
        assert actual_final>=final_lower-1e-14
    assert max_identity<1e-12 and max_renewal<1e-12
    limits=[]
    for h in (0.,1.):
        for d in (1.,10.,100.):
            z=model(.2,h,4.,.2,d)
            limits.append({'sigma_H':h,'sigma_L':4.,'lambda':.2,'d':d,**z})
        assert z['Y']<1e-8
        assert abs(z['mean_dose']-5)<1e-6
    # A planning illustration uses PR92 central values, not confidence bounds.
    p=.01109;h=2.1;l=56.6;target=.99;design=.999
    d=math.log(design*(1-p)/(p*(1-design)))/(l-h)
    sH=math.exp(-h*d);sL=math.exp(-l*d)
    epsilon_L_max=p*(1-target)/(target*(1-p))*sH-sL
    exchange_mass_max=(1-target)*p*sH-target*(1-p)*sL
    planning={'scope':'source-central-value planning only; not acquired joint rate/confidence certificate',
              'p':p,'sigma_H_mb':h,'sigma_L_mb':l,'target_q':target,'ideal_design_q':design,
              'dose_inverse_mb':d,'nominal_target_survival_H':sH,'nominal_target_survival_L':sL,
              'epsilon_L_max_if_epsilon_H_0_no_collateral_in_acceptance_event':epsilon_L_max,
              'zero_false_accept_iid_light_trials_for_95percent_bound_alone':math.ceil(math.log(.05)/math.log1p(-epsilon_L_max)),
              'accepted_exchange_total_probability_mass_max_with_no_other_errors':exchange_mass_max}
    return {'status':'conditional_internal_renewal_audit_only','historical_originality':'UNKNOWN',
            'random_algebra_checks':1000,'max_loss_dose_identity_error':max_identity,
            'max_renewal_recursion_error':max_renewal,'minimum_sampled_posterior_bound_gap':min_posterior_gap,
            'high_purity_limits_including_sigma_H_zero':limits,'planning_precision_screen':planning,
            'race_simulation':simulate(.2,1.,4.,.2,.8)}

if __name__=='__main__':
    result=run();(HERE/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='high_purity_limits_including_sigma_H_zero'},indent=2))
