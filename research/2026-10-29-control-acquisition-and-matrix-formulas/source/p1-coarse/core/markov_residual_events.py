"""Positive residual flags from nonintrusive reset-state membership.
Software trajectories use exact integer transition probabilities. Early
rejection and first-step data reuse are charged in the acquisition ledger.
"""
from fractions import Fraction as F
from pathlib import Path
from math import lcm, factorial, ceil, log
import itertools, json
import numpy as np
from echo_compiler import sqrt_upper, dot, matvec
from uniform_certificate import mm, sub, diagonal, psd
from run_echo_experiment import truth, dumpable
from run_dissipation_experiment import inv2, power


class MembershipInstrument:
    def __init__(self, matrices, seed=812907):
        self.matrices=matrices;self.rng=np.random.default_rng(seed)
        self.ops=self.resets=self.bits=0

    def mixed_flag(self,i,n,depth,tail_weight,batch=100000):
        denominator=tail_weight.denominator
        label_total=depth*denominator+tail_weight.numerator
        matrix=self.matrices[i]
        den=lcm(*(x.denominator for row in matrix for x in row))
        a=[[int(x*den) for x in row] for row in matrix]
        successes=departures=0
        hist=np.zeros(depth+1,dtype=np.int64)
        departed_hist=np.zeros(depth+1,dtype=np.int64)
        for start in range(0,n,batch):
            size=min(batch,n-start)
            labels=np.minimum(self.rng.integers(label_total,size=size)//denominator,depth)
            lengths=2*labels+2
            hist+=np.bincount(labels,minlength=depth+1)
            state=np.zeros(size,dtype=np.int8)
            first_out=np.ones(size,dtype=bool)
            penultimate_out=np.zeros(size,dtype=bool)
            for step in range(1,2*depth+3):
                idx=np.flatnonzero((step<=lengths)&first_out)
                old=state[idx].copy();draws=self.rng.integers(den,size=idx.size)
                new=np.full(idx.size,2,dtype=np.int8)
                for live in [0,1]:
                    mask=old==live
                    new[mask&(draws<a[live][0])]=0
                    new[mask&(draws>=a[live][0])&(draws<a[live][0]+a[live][1])]=1
                state[idx]=new
                if step==1:
                    first_out=state!=0
                    departures+=int(np.count_nonzero(first_out))
                    departed_hist+=np.bincount(labels[first_out],minlength=depth+1)
                pen=(step==lengths-1)&first_out
                penultimate_out[pen]=state[pen]!=0
            successes+=int(np.count_nonzero(first_out&penultimate_out&(state==0)))
        costs=n+sum(int(count)*(2*k+1) for k,count in enumerate(departed_hist))
        bits=n+2*departures-int(departed_hist[0])
        self.ops+=costs;self.resets+=n;self.bits+=bits
        return {'successes':successes,'trials':n,'first_step_departures':departures,
                'model_successes':n-departures,'length_histogram':hist.tolist(),
                'departed_length_histogram':departed_hist.tolist(),
                'primitive_applications':costs,'membership_bits':bits}


def run():
    g=F(1,20);source_bound=1-g/2;depth=4
    hidden=[[[1-g,g],[g,F(1,4)]],[[1-2*g,g],[g,F(1,3)]]]
    for a in hidden:
        assert psd(a) and psd(sub(diagonal([source_bound]*2),a))
        assert all(sum(row)<=1 and min(row)>=0 for row in a)
    inst=MembershipInstrument(hidden)
    n_flag=2000000;chernoff=F(10)
    tail=1/(1-source_bound**2);normalizer=depth+tail
    model_radius=sqrt_upper(chernoff/(2*n_flag))
    models=[];receipts=[];thetas=[];zetas=[]
    for i in range(2):
        flag=inst.mixed_flag(i,n_flag,depth,tail)
        t=F(flag['model_successes'],n_flag);x=F(flag['successes'])
        p_upper=min(F(1),(x+chernoff+sqrt_upper(chernoff**2+2*x*chernoff))/n_flag)
        galerkin_q_upper=normalizer*p_upper
        proposed_q_upper=(sqrt_upper(galerkin_q_upper)+model_radius*sqrt_upper(tail))**2
        budget=1-t*t
        if budget<=0:raise ValueError('Insufficient observed computational dissipation')
        theta=proposed_q_upper/budget;zeta=model_radius/budget
        models.append(t);thetas.append(theta);zetas.append(zeta)
        # Independent checker scope: these source matrices never enter inference.
        true_t=hidden[i][0][0]
        assert abs(t-true_t)<=model_radius
        d=[true_t-t,g]
        h=sub(diagonal([F(1)]*2),mm(hidden[i],hidden[i]))
        actual_q=dot(d,matvec(inv2(h),d))
        assert actual_q<=proposed_q_upper
        p_d=[F(0),g];exact_form=F(0)
        for k in range(depth+1):
            term=dot(p_d,matvec(power(hidden[i],2*k),p_d))
            exact_form+=term*(tail if k==depth else 1)
            event=truth(hidden,[F(1),F(0)],(i,)*(2*k+2))-2*true_t*truth(hidden,[F(1),F(0)],(i,)*(2*k+1))+true_t**2*truth(hidden,[F(1),F(0)],(i,)*(2*k))
            assert event==term and event>=0
        assert exact_form/normalizer<=p_upper
        receipts.append({'primitive':i,'model':t,'model_radius':model_radius,
                         'flag':flag,'flag_probability_upper':p_upper,
                         'galerkin_inverse_dissipation_upper':galerkin_q_upper,
                         'proposed_inverse_dissipation_upper':proposed_q_upper,
                         'computational_dissipation':budget,'theta_squared':theta,
                         'correction_noise_zeta':zeta,
                         'checker_true_mixture_probability':exact_form/normalizer,
                         'checker_actual_proposed_form':actual_q})
    remainder=2*max(thetas);noise=max(zetas);total=remainder+noise
    # Joint failure <=6 exp(-10)<.001. Correlated estimates use a union bound.
    assert sum((F(10**k,factorial(k)) for k in range(40)),F(0))>6000
    tasks=list(itertools.product(range(2),repeat=6))
    tasks += [(i,)*n for i in range(2) for n in [20,40,100]]
    tasks += [tuple(j%2 for j in range(n)) for n in [20,40,100]]
    errors=[]
    for w in tasks:
        prediction=F(1)
        for i in w:prediction*=models[i]
        error=abs(truth(hidden,[F(1),F(0)],w)-prediction)
        assert error<=total;errors.append(float(error))
    direct=[]
    for menu in [1,1000,10000,100000]:
        trials=ceil(log(2*menu/0.001)/(2*float(total)**2))
        direct.append({'independent_length_20_tasks':menu,'hoeffding_trials_per_task':trials,
                       'aggregate_primitive_applications':20*menu*trials,
                       'scope':'Sufficient direct-estimation budget, not an optimal-estimator lower bound'})
    result={'source_family_checker_only':hidden,'g':g,'source_norm_warranty':source_bound,
            'additional_access':'Exact nonintrusive membership in the reset state at selected intermediate times; no hidden-state identities',
            'rank_of_hidden_system_not_given_to_learner':True,
            'depth':depth,'mixture_normalizer':normalizer,'tail_weight':tail,
            'receipts':receipts,'total_primitive_applications':inst.ops,
            'total_resets':inst.resets,'total_membership_bit_observations':inst.bits,
            'separate_model_estimation_trials':0,
            'first_step_early_rejection_and_data_reuse':True,
            'probability_of_any_false_premise_bound_at_most':F(1,1000),
            'uniform_signed_remainder_bound':remainder,'uniform_correction_noise_bound':noise,
            'uniform_all_word_amplitude_bound':total,'checked_task_count':len(tasks),
            'maximum_checked_error':max(errors),'all_exact_checks_passed':True,
            'direct_endpoint_estimation_comparator':direct,
            'simulation_scope':'Seeded integer-random Markov trajectories executed in software; no physical hardware, flawless sensor, or source norm warranty has been acquired.'}
    out=Path(__file__).resolve().parents[1]/'results'/'MARKOV_RESIDUAL_EVENTS.json'
    out.write_text(json.dumps(dumpable(result),indent=2)+'\n')
    print('operations',inst.ops,'resets',inst.resets,'membershipbits',inst.bits,
          'bound',float(total),'maxerror',max(errors),'events',[r['flag']['successes'] for r in receipts])


if __name__=='__main__':run()
