"""Finite, deterministic research protocol for task-relative CTMC abstraction.

All rate arrays for held-out networks are constructed after the reuse template has
been fixed. The full strong comparator retains and uses exactly the same array.
"""
import copy, json, time, math, os
from pathlib import Path
import numpy as np
from machinery import (Model, make_model, detect_exchangeable_classes, build_coarse,
    full_generator,state_to_counts,uniform_initial_micro,expm_distribution,
    observable_extinct,observable_full_extinct,observable_infected,
    deviations,quadratic_certificate,linear_certificate,uniformization_time)

OUT=Path(__file__).parent
np.set_printoptions(precision=8)


def create_sis(sizes,seed=1,rates=None):
    """Native site-state model; no group coordinates supplied to learner."""
    k=len(sizes);q=2
    ur=np.zeros((k,q,q));pr=np.zeros((k,k,q,q,q))
    if rates is None:
        rr=np.array([0.30+0.02*i for i in range(k)])
        mat=np.fromfunction(lambda h,g:0.035+(h==g)*0.018+(abs(h-g)==1)*0.007,(k,k),dtype=int)
    else:rr,mat=rates
    rr=np.asarray(rr,dtype=float);mat=np.asarray(mat,dtype=float)
    for g in range(k):ur[g,1,0]=float(rr[g])
    for h in range(k):
        for g in range(k):pr[h,g,1,0,1]=float(mat[h,g])
    return make_model(sizes,q,ur,pr,name='SIS')


def create_sir(sizes):
    k=len(sizes);q=3
    ur=np.zeros((k,q,q));pr=np.zeros((k,k,q,q,q))
    for g in range(k):
        ur[g,1,2]=0.4+0.03*g
        ur[g,2,0]=0.06+0.01*g # return to susceptibility (SIRS)
    for h in range(k):
        for g in range(k):
            if abs(h-g)<=1:pr[h,g,1,0,1]=0.022+0.007*(h==g)+0.002*g
    return make_model(sizes,q,ur,pr,name='SIRS')


def counts_initial(groups,q,seed_sites):
    x=[0]*sum(map(len,groups))
    for i in seed_sites:x[i]=1
    return state_to_counts(x,groups,q),tuple(x)


def solve_exact_small(m, groups, initial_counts,T):
    st=time.perf_counter();Q,states,index=full_generator(m)
    build_t=time.perf_counter()-st
    p=uniform_initial_micro(initial_counts,groups,m.q,index)
    st=time.perf_counter();pT=expm_distribution(Q,p,T)
    solve_t=time.perf_counter()-st
    event=observable_full_extinct(states)
    return {'p_extinct':float(pT@event),'mean_infected':float(pT@np.array([x.count(1) for x in states])),
            'states':len(states),'nnz':Q.nnz,'build_sec':build_t,'solve_sec':solve_t}


def solve_counts(m,groups,initial_counts,T):
    st=time.perf_counter();Q,states,index,_=build_coarse(m,groups)
    build_t=time.perf_counter()-st
    p=np.zeros(len(states));p[index[initial_counts]]=1.
    st=time.perf_counter();pT=expm_distribution(Q,p,T)
    solve_t=time.perf_counter()-st
    event=observable_extinct(states)
    K,tail=uniformization_time(Q,T)
    return {'p_extinct':float(pT@event),'mean_infected':float(pT@observable_infected(states)),
            'states':len(states),'nnz':Q.nnz,'build_sec':build_t,'solve_sec':solve_t,
            'poisson_truncation_K':K,'poisson_tail_float64':tail}


def discover(m,forced=()):
    st=time.perf_counter();groups,counts=detect_exchangeable_classes(m,forced)
    counts['discover_sec']=time.perf_counter()-st
    counts['groups']=groups;counts['sizes']=[len(g) for g in groups]
    return groups,counts


def small_holdout(m,T,seed_sites):
    groups,learn=discover(m)
    c,x=counts_initial(groups,m.q,seed_sites)
    a=solve_counts(m,groups,c,T)
    b=solve_exact_small(m,groups,c,T)
    return {'model':m.name,'n':m.n,'q':m.q,'T':T,'discover':learn,
            'reduction':a,'strong_exact_comparator':b,
            'absolute_error':abs(a['p_extinct']-b['p_extinct']),
            'mean_infected_difference':abs(a['mean_infected']-b['mean_infected'])}


def direct_full_one_site(m,preparation_full,T,site):
    Q,states,index=full_generator(m)
    p=np.zeros(len(states));p[index[tuple(preparation_full)]]=1.
    pT=expm_distribution(Q,p,T)
    return float(sum(pT[idx] for idx,x in enumerate(states) if x[site]==1))


def anonymous_vs_named(m,T,site=0):
    groups,info=discover(m)
    x=[0]*m.n;x[site]=1
    initial=state_to_counts(x,groups,m.q)
    Q,states,idx,_=build_coarse(m,groups)
    p=np.zeros(len(states));p[idx[initial]]=1
    pT=expm_distribution(Q,p,T)
    # x0 is not orbit-uniform: group mean differs from a named-site marginal.
    g_id=next(g for g,si in enumerate(groups) if site in si)
    naive=float(sum(prob*st[g_id][1]/len(groups[g_id]) for prob,st in zip(pT,states)))
    actual=direct_full_one_site(m,x,T,site)
    refined,find=discover(m,forced=(site,))
    refined_init=state_to_counts(x,refined,m.q)
    R,rs,ridx,_=build_coarse(m,refined)
    pr=np.zeros(len(rs));pr[ridx[refined_init]]=1
    post=expm_distribution(R,pr,T)
    g_s=next(g for g,si in enumerate(refined) if si==[site])
    learned=float(sum(prob*st[g_s][1] for prob,st in zip(post,rs)))
    return {'n':m.n,'T':T,'site':site,'unrefined_states':len(states),'refined_states':len(rs),
            'full_states':m.q**m.n,'unrefined_named_site_estimate':naive,
            'strong_exact_comparator':actual,'refined_exact_prediction':learned,
            'failure_abs_error':abs(naive-actual), 'refined_abs_error':abs(learned-actual),
            'new_discovered_groups':refined,'refinement_discovery':find}


def hetero(m,groups,delta):
    """Intentionally break symmetry by a few anomalous physical contacts.
    The original source and its existing grouping remain available.
    """
    new=Model(m.unary.copy(),m.pair.copy(),name='perturbed-'+m.name)
    src0=groups[0][0]; src1=groups[0][1]
    dst0=groups[1][0];dst1=groups[1][1]
    # At q=2 the selected native 1,0->1 infection channel changes.
    new.pair[src0,dst0,1,0,1]+=delta
    new.pair[src1,dst1,1,0,1]-=delta
    assert np.min(new.pair)>=0
    return new.validate()


def distributed_hetero(m,groups,eta_budget=0.0057):
    """Create EVERYWHERE symmetry-breaking but zero-mean genuine native rates.

    This is an adverse fixture for *exact* symmetry reductions: even tiny,
    distinct unary rates destroy every transposition within every cohort.
    In each previously learned group, centered arange weights sum to zero;
    remeasuring group-averaged dynamics therefore keeps exactly the old R.
    """
    new=Model(m.unary.copy(),m.pair.copy(),name='diffuse-perturbed-'+m.name)
    weights=[]
    for nodes in groups:
        weights.extend([(j, float(i-(len(nodes)-1)/2)) for i,j in enumerate(nodes)])
    z=sum(abs(w) for _,w in weights)
    for j,w in weights:
        new.unary[j,1,0]+=eta_budget*w/z
    assert min(new.unary[:,1,0])>0
    return new.validate()


def uniform_recovery_policy(m,sites,increment):
    """Known simulator policy, with calibration/control costs excluded from
    software benchmark and explicitly NOT claimed to have been acquired."""
    out=Model(m.unary.copy(),m.pair.copy(),name='recovery-policy-'+m.name)
    for j in sites:out.unary[j,1,0]+=increment
    return out.validate()


def hetero_experiment(base,groups,T,counts,epss,full=True):
    rec=[]
    for delta in epss:
        m=hetero(base,groups,delta)
        d=deviations(m,groups);pred=solve_counts(m,groups,counts,T)
        exact=solve_exact_small(m,groups,counts,T) if full else None
        err=abs(pred['p_extinct']-exact['p_extinct']) if exact else None
        rec.append({'perturbation':delta,'eta_upper':d['eta_upper'],
                    'linear_error_bound':linear_certificate(d['eta_upper'],T),
                    'quadratic_error_bound':quadratic_certificate(d['eta_upper'],T),
                    'projected_p':pred['p_extinct'],'exact_p':exact['p_extinct'] if exact else None,
                    'observed_abs_error':err,'coarse_states':pred['states'],
                    'full_states':m.q**m.n,'projection_elapsed_sec':pred['build_sec']+pred['solve_sec'],
                    'full_elapsed_sec':exact['build_sec']+exact['solve_sec'] if exact else None})
    return rec


def run():
    t0=time.perf_counter();records={}
    # TRAINING: acquire a reusable *compiler rule* from two structurally distinct
    # source algebras (q=2 and q=3), including all symmetry tests. The code for
    # group reduction is an engineered prior and is NOT autonomously invented.
    train_sis,_=create_sis([3,2]);train_sir,_=create_sir([2,2]);
    records['training']=[small_holdout(train_sis,1.7,[0,3]),small_holdout(train_sir,1.5,[0,2])]

    # FREEZE: no rates from these held-out models are consulted during the
    # engineering of the reducer.
    test_a,_=create_sis([4,3],rates=([.37,.29],[[.04,.015],[.012,.055]]))
    test_b,_=create_sis([3,3,2],rates=([.32,.37,.26],[[.039,.021,0],[.011,.047,.015],[0,.014,.05]]))
    test_c,_=create_sir([3,3])
    records['unseen_exact_tests']=[small_holdout(test_a,2.8,[0,4]),
                                    small_holdout(test_b,2.0,[0,3,6]),
                                    small_holdout(test_c,1.1,[0,3])]
    records['failed_named_prediction_and_repair']=anonymous_vs_named(test_a,2.8,0)
    # Break symmetry of already learned source and test projected uncertain
    # predictions on a genuinely NEW physical rate matrix.
    b,bi=discover(test_a)
    ci,x=counts_initial(b,test_a.q,[0,4])
    records['nonexchangeable_perturbation'] = hetero_experiment(test_a,b,2.8,ci,[0.001,0.002,0.004,0.008],full=True)

    # Genuine large heldouts: never enumerate the microstate space.
    large,_=create_sis([9,8,8],rates=([.29,.35,.31],[[.042,.012,0],[.01,.055,.016],[0,.013,.049]]))
    gl,geo=discover(large)
    cli,_=counts_initial(gl,large.q,[0,9,17])
    large_pred=solve_counts(large,gl,cli,2.6)
    records['large_unseen_exact_symmetry']={'n':large.n,'q':large.q,'new_groups':gl,
        'group_discovery':geo,'coarse_solver':large_pred,'full_possible_states':large.q**large.n,
        'full_exact_attempted':False,'exact_symbolic_lumpability':True}
    # Full strong incumbent on a SPARSE symmetry violation: it simply splits
    # the four exceptional sites and computes the NEW policy exactly.
    sparse=hetero(large,gl,0.003)
    sg,sgi=discover(sparse)
    sparse_init,_=counts_initial(sg,sparse.q,[0,9,17])
    sparse_exact=solve_counts(sparse,sg,sparse_init,2.6)
    records['ordinary_sparse_exact_refinement']={
        'discover':sgi,'refined_states':sparse_exact['states'],
        'strong_ordinary_exact_prediction':sparse_exact['p_extinct'],
        'build_plus_solve_seconds':sparse_exact['build_sec']+sparse_exact['solve_sec'],
        'full_microstate_space_size':sparse.q**sparse.n,
        'comment':'Standard exact symmetry refinement handles this sparse case; adopting it dominates a loose approximate certificate.'}
    # Future policy changes one source site; trial certified via cheap perturbation
    # bound, not hidden ground truth.
    new=hetero(large,gl,0.003)
    unc=deviations(new,gl)
    pred=solve_counts(new,gl,cli,2.6)
    verdict={'upper':min(1,pred['p_extinct']+quadratic_certificate(unc['eta_upper'],2.6)),
             'lower':max(0,pred['p_extinct']-quadratic_certificate(unc['eta_upper'],2.6))}
    records['large_unseen_intervention']={'n':new.n,'q':new.q,'coarse_solver':pred,
        'deviation':unc,'linear_error_bound':linear_certificate(unc['eta_upper'],2.6),
        'quadratic_error_bound':quadratic_certificate(unc['eta_upper'],2.6),
        'rigorous_analytic_interval_excluding_float_rounding':verdict,
        'exact_ground_truth_unavailable':True}
    # ADVERSE *NOVEL* intervention: every site has a different unary recovery
    # rate, so the strongest EXACT ordinary lumping has singleton cells and
    # 2**25 states. Unlike sparse anomalies, localization is no longer cheap.
    # The group symmetrized reference is still acquired by averaging given rates.
    diffuse=distributed_hetero(large,gl,0.0057)
    dg,di=discover(diffuse)
    un=deviations(diffuse,gl)
    base_pred=solve_counts(diffuse,gl,cli,2.6)
    # Follow-up policy: uniformly add a recovery rate in learned group zero,
    # while diffuse asymmetry is unchanged (all finite rates are still native).
    treat=uniform_recovery_policy(diffuse,gl[0],0.08)
    ut=deviations(treat,gl)
    treatment_pred=solve_counts(treat,gl,cli,2.6)
    target=0.075
    def decision(p,err):
        lo=max(0,p-err);hi=min(1,p+err)
        return {'prediction':p,'analytic_interval_excluding_rounding':[lo,hi],
                'passes_threshold':bool(lo>target),'fails_threshold':bool(hi<target)}
    records['diffuse_new_intervention_and_policy']={
        'n':diffuse.n,'group_discovery_when_independently_restarted':di,
        'ordinary_exact_symmetry_states':math.prod(
            math.comb(len(g)+diffuse.q-1,diffuse.q-1) for g in dg),
        'retained_approximate_state_count':base_pred['states'],
        'retained_discovered_groups':gl,
        'native_scalar_entries_each':diffuse.unary.size+diffuse.pair.size,
        'diffuse_deviation':un,'treatment_deviation':ut,
        'ordinary_linear_error_bound':linear_certificate(un['eta_upper'],2.6),
        'zero_first_order_error_bound':quadratic_certificate(un['eta_upper'],2.6),
        'target_threshold':target,'treatment_recovery_rate_increment':0.08,
        'no_treatment':decision(base_pred['p_extinct'],quadratic_certificate(un['eta_upper'],2.6)),
        'with_treatment':decision(treatment_pred['p_extinct'],quadratic_certificate(ut['eta_upper'],2.6)),
        'preparation':'uniformly randomized placement within each learned group',
        'exact_full_model_not_enumerated':True,
        'physical_intervention_and_actuation_not_executed':True,
        'first_order_cancellation_premises_checked':{
             'coarse_group_averages_unchanged':np.allclose(
                 base_pred['p_extinct'],large_pred['p_extinct']),
             'all_singletons_after_diffuse_perturbation':len(dg)==diffuse.n}
    }
    # Cross-state-family adverse test: every q=3 site distinguishable,
    # but original 3-state SIRS counts retain a safe zero-first-order bound.
    sirs8,_=create_sir([4,4]); sirs_groups,_=discover(sirs8)
    sirs_dist=Model(sirs8.unary.copy(),sirs8.pair.copy(),name='diffuse-SIRS')
    weights=[]
    for nodes in sirs_groups:
        weights += [(j,float(i-(len(nodes)-1)/2)) for i,j in enumerate(nodes)]
    den=sum(abs(w) for j,w in weights)
    for j,w in weights:sirs_dist.unary[j,1,2]+=0.014*w/den
    sirs_dist.validate(); sig,diag=discover(sirs_dist)
    cs,_=counts_initial(sirs_groups,sirs8.q,[0,4])
    sirs_p=solve_counts(sirs_dist,sirs_groups,cs,0.85)
    sirs_exact=solve_exact_small(sirs_dist,sirs_groups,cs,0.85)
    sirs_eta=deviations(sirs_dist,sirs_groups)['eta_upper']
    assert len(sig)==sirs_dist.n
    assert abs(sirs_p['p_extinct']-sirs_exact['p_extinct']) < quadratic_certificate(sirs_eta,0.85)
    records['unseen_diffuse_three_state']={
        'state_count_exact':sirs_exact['states'],'states_approx':sirs_p['states'],
        'exact_solution':sirs_exact['p_extinct'],'projected_solution':sirs_p['p_extinct'],
        'absolute_error':abs(sirs_p['p_extinct']-sirs_exact['p_extinct']),
        'analytic_error_bound':quadratic_certificate(sirs_eta,0.85),
        'ordinary_exact_symmetry_groups':sig,'exact_solve_seconds':sirs_exact['build_sec']+sirs_exact['solve_sec']}
    # Cost ledger: read all native coefficients, source constructor, attempted
    # symmetry tests, sparse generator build, matrix exponential, output storage.
    records['ledger']={'train_native_scalar_entries':sum(
        v.unary.size+v.pair.size for v in [train_sis,train_sir]),
        'test_native_scalar_entries':sum(
        v.unary.size+v.pair.size for v in [test_a,test_b,test_c,large,new,diffuse,treat,sirs8,sirs_dist]),
        'train_full_generator_states':sum(v['strong_exact_comparator']['states'] for v in records['training']),
        'training_comparator_full_states_processed':sum(v['strong_exact_comparator']['states'] for v in records['training']),
        'number_new_exact_tests':3,
        'note':'Both sides retain native rates and past computations. No physical experiments, simulations of private hidden trajectories, neural training or code synthesis search were performed. Generic quotient compiler was researcher-written, not acquired from scratch.'}
    records['wallclock_total_seconds']=time.perf_counter()-t0
    (OUT/'results.json').write_text(json.dumps(records,indent=2))
    print('TOTAL',round(records['wallclock_total_seconds'],2))
    for s in records['training']+records['unseen_exact_tests']:
        print(s['model'], 'n',s['n'], 'q',s['q'],'full',s['strong_exact_comparator']['states'], 'coarse',s['reduction']['states'], 'abs-error',s['absolute_error'])
    print('failed named prediction',records['failed_named_prediction_and_repair']['failure_abs_error'],
          'fixed',records['failed_named_prediction_and_repair']['refined_abs_error'])
    for r in records['nonexchangeable_perturbation']:
        print('hetero',r['perturbation'],'trueerr',r['observed_abs_error'],'linear bound',r['linear_error_bound'],'quadratic',r['quadratic_error_bound'])
    print('LARGE',records['large_unseen_exact_symmetry']['full_possible_states'],'to',large_pred['states'],
          'intervention interval',verdict)
    print('DIFFUSE',records['diffuse_new_intervention_and_policy']['ordinary_exact_symmetry_states'],'to',base_pred['states'],
          'decision',records['diffuse_new_intervention_and_policy']['no_treatment'],
          records['diffuse_new_intervention_and_policy']['with_treatment'])

if __name__=='__main__':run()
