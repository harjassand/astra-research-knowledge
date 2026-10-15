#!/usr/bin/env python3
"""Independent finite-network checks. Synthetic rates; no material qualification."""
from pathlib import Path
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent/'sources'/'transport'
BETA = 1/(8.617333262145e-5*300)


def evaluate(events, wells, chi, rho):
    """Event=(origin,destination,base_rate,saddle_response,reward,label)."""
    n=len(wells)
    rates=np.array([e[2]*math.exp(-BETA*chi*(e[3]-wells[e[0]])) for e in events])
    return solve_rates(events,rates,rho,n)


def solve_rates(events,rates,rho,n):
    Q=np.zeros((n,n)); reward=np.zeros(n)
    for e,k in zip(events,rates):
        i,j,_,_,g,_=e
        assert i!=j and k>=0
        Q[i,i]-=k
        if j>=0:Q[i,j]+=k
        reward[i]+=k*g
    value=np.linalg.solve(-Q,reward)
    times=np.linalg.solve(-Q,np.ones(n))
    occupation=np.linalg.solve(-Q.T,rho)
    advantages=np.array([e[4]+(value[e[1]] if e[1]>=0 else 0)-value[e[0]] for e in events])
    weights=np.array([occupation[e[0]]*k*a for e,k,a in zip(events,rates,advantages)])
    return dict(Y=float(rho@value),tau=float(rho@times),Q=Q,value=value,
                occupation=occupation,rates=rates,advantages=advantages,weights=weights)


def random_network(rng,n):
    # Shared baseline saddles and reciprocal prefactors; antisymmetric paid
    # edge affinities are fixed. Every state has two finite killing channels.
    well_F=rng.uniform(-.02,.02,n)
    well_R=rng.uniform(0,.10,n)
    events=[]
    for i in range(n):
        for j in range(i+1,n):
            saddle_F=max(well_F[i],well_F[j])+rng.uniform(.02,.08)
            saddle_R=rng.uniform(0,.15)
            pref=rng.uniform(.5,2.)
            affinity=rng.uniform(-1,1)
            g=rng.uniform(-1,1)
            for a,b,sign in ((i,j,1),(j,i,-1)):
                rate=pref*math.exp(-BETA*(saddle_F-well_F[a])+sign*affinity/2)
                events.append((a,b,rate,saddle_R,sign*g,f'edge_{i}_{j}'))
    for i in range(n):
        for alpha in range(2):
            events.append((i,-1,float(rng.uniform(.01,.05)),float(rng.uniform(0,.15)),
                           0.,f'damage_{alpha}'))
    return events,well_R


def source_model(aL=10.,aR=1.,bL=1.,bR=1.,h=.001,d=0.,RA=.12):
    events=[(0,1,aL,.02,0.,'entry_left'),(0,1,aR,.02,-1.,'entry_right'),
            (1,0,bL,.02,0.,'exit_left'),(1,0,bR,.02,1.,'exit_right'),
            (1,-1,h,.20,0.,'damage_occupied')]
    if d>0:events.append((0,-1,d,0.,0.,'damage_empty_unaffected'))
    return events,np.array([0.,RA])


def exact_two_state(aL,aR,bL,bR,h,d):
    A=aL+aR;B=bL+bR;N=aL*bR-aR*bL
    det=A*h+d*(B+h)
    return {'Y':(N-aR*h)/det,'tau':(A+B+h)/det}


def compare_source_replay():
    a=json.loads((SOURCE/'astra_transport_check_results.json').read_text())
    b=json.loads((HERE/'source_replay_results.json').read_text())
    differences=[]
    def walk(x,y,path=''):
        if isinstance(x,dict):
            assert x.keys()==y.keys()
            for k in x:walk(x[k],y[k],path+'/'+k)
        elif isinstance(x,list):
            assert len(x)==len(y)
            for i,(s,t) in enumerate(zip(x,y)):walk(s,t,path+'/'+str(i))
        elif isinstance(x,(int,float)) and not isinstance(x,bool):
            assert math.isclose(x,y,rel_tol=1e-9,abs_tol=1e-7),(path,x,y)
            if x!=y:differences.append({'path':path,'source':x,'replay':y,'absolute_difference':abs(x-y)})
        else:assert x==y,(path,x,y)
    walk(a,b)
    return {'exact_json_equal':a==b,'all_values_within_rel_1e_9_abs_1e_7':True,
            'differences':differences,'scope':'source algebra replay only, no material acquisition'}


def run():
    rng=np.random.default_rng(20261015)
    invariance=[];derivatives=[];bellman=[];affinities=[];committors=[]
    for _ in range(200):
        n=int(rng.integers(3,8))
        events,wells=random_network(rng,n)
        rho=rng.uniform(0,1,n);rho/=rho.sum()
        chi=float(rng.uniform(.1,.7))
        x=evaluate(events,wells,chi,rho)
        changed=evaluate(events,rng.uniform(0,.10,n),chi,rho)
        invariance.append(abs(x['Y']-changed['Y']))
        cp=[(i,j,k,R,float(label=='damage_0'),label) for i,j,k,R,g,label in events]
        p1=evaluate(cp,wells,chi,rho)['Y']
        p2=evaluate(cp,rng.uniform(0,.10,n),chi,rho)['Y']
        committors.append(abs(p1-p2));assert 0<=p1<=1
        full=sum(w*(-BETA*(e[3]-wells[e[0]])) for e,w in zip(events,x['weights']))
        saddle=-BETA*sum(w*e[3] for e,w in zip(events,x['weights']))
        eps=1e-5
        fd=(evaluate(events,wells,chi+eps,rho)['Y']-evaluate(events,wells,chi-eps,rho)['Y'])/(2*eps)
        derivatives.append({'full_vs_saddle':abs(full-saddle),'finite_difference_scaled_error':abs(fd-saddle)/(1+abs(saddle))})
        residual=np.zeros(n)
        for e,k,a in zip(events,x['rates'],x['advantages']):residual[e[0]]+=k*a
        bellman.append(float(abs(residual).max()))
        # Compare one actual reversible 3-cycle affinity at the same chi.
        def edge_rate(i,j,z):
            e=next(e for e in events if e[0]==i and e[1]==j)
            return e[2]*math.exp(-BETA*z*(e[3]-wells[i]))
        def affinity(z):return sum(math.log(edge_rate(i,j,z)/edge_rate(j,i,z)) for i,j in ((0,1),(1,2),(2,0)))
        affinities.append(abs(affinity(chi)-affinity(0)))
    assert max(invariance)<1e-10
    assert max(committors)<1e-12
    assert max(bellman)<1e-10
    assert max(affinities)<1e-12
    assert max(z['full_vs_saddle'] for z in derivatives)<1e-9
    assert max(z['finite_difference_scaled_error'] for z in derivatives)<1e-6

    rho=np.array([1.,0.])
    well_clock=[]
    for RA in (0.,.06,.12,.18,.24):
        events,wells=source_model(RA=RA)
        z=evaluate(events,wells,.5,rho)
        alpha=math.exp(-BETA*.5*.02);q=math.exp(BETA*.5*(RA-.02))
        current=alpha*q*9/(alpha*11+q*2)
        well_clock.append({'synthetic_R_A_eV':RA,'expected_net_right_transfer_before_failure':z['Y'],
                           'mean_lifetime_s':z['tau'],'damage_free_steady_current_per_s':current})
    assert max(z['expected_net_right_transfer_before_failure'] for z in well_clock)-min(z['expected_net_right_transfer_before_failure'] for z in well_clock)<1e-5
    alpha=math.exp(-BETA*.5*.02);q=math.exp(BETA*.5*(.12-.02));rr=math.exp(-BETA*.5*(.20-.12))
    A=11.;B=2.;N=9.;h=.001;aR=1.
    denominator=(N-aR*h)*(q*B+rr*h)-alpha*(q*N-aR*rr*h)*(B+h)
    crossover=alpha*A*h*N*(q-rr)/denominator
    damage=[]
    for d in (0.,.001,crossover,.02,.1):
        events,wells=source_model(d=d)
        before=evaluate(events,wells,0.,rho)
        after=evaluate(events,wells,.5,rho)
        eb=exact_two_state(10,1,1,1,h,d)
        ea=exact_two_state(alpha*10,alpha,q,q,rr*h,d)
        for key in ('Y','tau'):
            assert math.isclose(before[key],eb[key],rel_tol=1e-9)
            assert math.isclose(after[key],ea[key],rel_tol=1e-9)
        damage.append({'synthetic_empty_state_damage_rate_s_inverse':d,
                       'Y_before':before['Y'],'Y_after':after['Y'],'yield_multiplier':after['Y']/before['Y'],
                       'lifetime_before_s':before['tau'],'lifetime_after_s':after['tau']})
    assert math.isclose(damage[2]['yield_multiplier'],1,rel_tol=1e-9)
    assert damage[3]['yield_multiplier']<1

    # Independent 2-port matrix derivative check: actual response C=.5 aa^T.
    events,wells=random_network(rng,4);rho=np.array([1.,0.,0.,0.])
    well_a=rng.normal(size=(4,2));saddle_a={e[5]:rng.normal(size=2) for e in events}
    Qc=.2*np.eye(2);direction=np.array([[.3,.1],[.1,.2]])
    def multi(qc):
        rates=[]
        for e in events:
            a=saddle_a[e[5]];b=well_a[e[0]]
            shift=.5*(a@qc@a-b@qc@b)
            rates.append(e[2]*math.exp(-BETA*shift))
        return solve_rates(events,np.array(rates),rho,4)
    z=multi(Qc)
    matrix=sum((-.5*BETA*w*np.outer(saddle_a[e[5]],saddle_a[e[5]]) for e,w in zip(events,z['weights'])),np.zeros((2,2)))
    analytic=float(np.trace(direction@matrix))
    eps=1e-6
    fd=(multi(Qc+eps*direction)['Y']-multi(Qc-eps*direction)['Y'])/(2*eps)
    assert abs(fd-analytic)/(1+abs(analytic))<1e-6

    return {'status':'conditional_internal_checks_only_no_material_or_novelty_validation',
        'historical_originality':'UNKNOWN','seed':20261015,'random_networks':200,
        'max_row_clock_reward_absolute_error':max(invariance),
        'max_committor_absolute_error':max(committors),
        'max_bellman_absolute_residual':max(bellman),
        'max_cycle_affinity_change_nats':max(affinities),
        'max_full_vs_saddle_gradient_absolute_error':max(z['full_vs_saddle'] for z in derivatives),
        'max_gradient_finite_difference_scaled_error':max(z['finite_difference_scaled_error'] for z in derivatives),
        'source_well_response_only_clock_changes':well_clock,
        'empty_damage_crossover_s_inverse':crossover,'empty_damage_counterexamples':damage,
        'multiport_local_gradient':{'analytic':analytic,'finite_difference':fd,
            'scaled_error':abs(fd-analytic)/(1+abs(analytic)),
            'scope':'local directional derivative only; finite Y is not claimed concave'},
        'source_replay_comparison':compare_source_replay(),
        'scope':'No measured material parameters. All extra network inputs synthetic.'}


if __name__=='__main__':
    results=run()
    (HERE/'results.json').write_text(json.dumps(results,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k not in ('source_replay_comparison','source_well_response_only_clock_changes','empty_damage_counterexamples')},indent=2))
