"""Astra XH2: source-generated developmental bootstrap seeds; analytical and
finite-network models, all probabilities/rates synthetic and NOT biological measurements.

The model assumes a complete genotype, roles whose production requires already-present
physical prerequisites (an OR of AND prerequisite alternatives), independent founder
seeding attempts, and correctly source-linked programme copying. It does NOT show a
molecularly implemented vacancy reader, seed manufacturing machinery, or physical
hereditary function. Exact closure/hitting proof in companion .md.
"""
from __future__ import annotations
import itertools, math, json
from scipy.stats import binom
import numpy as np


def closure(deps, S):
    """Boolean forward chaining, deps[j] list of AND-prerequisite bitmasks; empty tuple = spontaneous."""
    cur=S
    while True:
        new=cur
        for j, alternatives in enumerate(deps):
            if cur&(1<<j):continue
            if any((p&cur)==p for p in alternatives):new|=1<<j
        if new==cur:return cur
        cur=new


def blocking_sets(deps):
    """T is closed to recruitment without an initially active role inside T.
    For all j in T, every permitted prerequisite choice intersects T.
    """
    n=len(deps)
    out=[]
    for T in range(1,1<<n):
        if all(all(p&T for p in deps[j]) for j in range(n) if T&(1<<j)):
            out.append(T)
    minimal=[T for T in out if not any((B & T)==B and B!=T for B in out)]
    return minimal,out


def synthetic_and_triads(num_triads=4):
    """Each role in a triad requires BOTH other roles; 2 basal seeds per triad."""
    deps=[]
    for t in range(num_triads):
        g=list(range(3*t,3*t+3))
        for j in g:deps.append((sum(1<<i for i in g if i!=j),))
    return deps


def directed_cycle(n):
    return [(1<<((j-1)%n),) for j in range(n)]


def and_two_of_three_success(x,y,z):
    # At least 2 of 3 independent founder-produced seeds activate.
    return x*y+x*z+y*z-2*x*y*z


def seed_activation(n_attempts,p_attempt=.95):
    return -math.expm1(n_attempts*math.log1p(-p_attempt)) if n_attempts else 0.0


def triad_reliability(triple,p=.95):
    probs=[seed_activation(n,p) for n in triple]
    return and_two_of_three_success(*probs)


def optimize_open_loop(num_triads=4, p=.95, cap=32, max_per_role=5):
    """Exact dynamic programme: best total success across independent triads for
       each total # of attempted founder-made pioneer objects. Each role assigned
       a fixed number attempts, no feedback; 0 attempts permitted.
    """
    frontier={0:(1.,())}
    triples=list(itertools.product(range(max_per_role+1),repeat=3))
    for _ in range(num_triads):
        new={}
        for cost,(pr,plan) in frontier.items():
            for t in triples:
                j=cost+sum(t)
                if j>cap:continue
                q=pr*triad_reliability(t,p)
                if j not in new or q>new[j][0]:new[j]=(q,plan+(t,))
        frontier=new
    return frontier


def receipt_policy(K=8,N=12,p=.95,beta=.97,alpha=.03,h=3):
    """Each *attempt* makes correct pioneer (p) or fails. After each attempt
       h independent readings all must be positive to advance to the next
       needed pioneer. On nonacceptance the disposable attempt is discarded.
       Successive roles are not mixed, and false-accepted roles are not rescued
       later. K accepted pioneer roles needed; N attempt budget.
    """
    correct=p*beta**h
    false=(1-p)*alpha**h
    accept=correct+false
    p_enough=binom.sf(K-1,N,accept)
    p_correct=(correct/accept)**K
    return {'K':K,'N':N,'h':h,'attempt_accept_probability':accept,
            'correct_given_accept':correct/accept,
            'P_enough_acceptances':p_enough,
            'P_success_episode':p_enough*p_correct,
            'P_success_20_independent_generations':(p_enough*p_correct)**20,
            'mean_attempts_to_K_receipts':K/accept,
            'mean_binary_reports_per_attempt':h}


def brute_exact_seed_hitting(deps):
    """For n<=12, exact enumeration; validate blocking set dual criterion."""
    n=len(deps);allmask=(1<<n)-1
    mins,blocks=blocking_sets(deps)
    sizes=[];minimal_seeds=[]; mismatches=[]
    for S in range(1<<n):
        yes=closure(deps,S)==allmask
        hits=all((S&B)!=0 for B in mins)
        if yes!=hits:mismatches.append(S)
        if yes:
            num=S.bit_count()
            if not sizes or num<=min(sizes):
                if not sizes or num<min(sizes):minimal_seeds=[]
                minimal_seeds.append(S)
            sizes.append(num)
    return {'n':n,'min_seed_count':min(sizes),'number_min_sets':len(minimal_seeds),
            'number_min_blocking_sets':len(mins), 'min_blocking_sets':mins,
            'bad_theorem_counterexamples':mismatches,'num_feasible_sets':len(sizes)}


def exact_probability_random_spontaneous(num_triads=4,p=.05):
    return (3*p*p-2*p**3)**num_triads


def monte_carlo_pioneer(trials=200000, seed=42, K=8, N=12, p=.95, beta=.97,alpha=.03,h=3):
    rng=np.random.default_rng(seed)
    # vectorized over trials; per attempt: correct-read-success / wrong-accepted / declined
    u=rng.random((trials,N))
    correct=p*beta**h;false=(1-p)*alpha**h
    accepted=(u<correct+false)
    wrong=(u>=correct)&accepted
    enough=accepted.sum(axis=1)>=K
    # wrong within first K acceptances invalidates the construction
    ranks=np.cumsum(accepted,axis=1)
    corrupt=np.any(wrong & (ranks<=K),axis=1)
    outcome=enough&~corrupt
    estimate=float(outcome.mean());err=math.sqrt(estimate*(1-estimate)/trials)
    return {'trials':trials,'estimate':estimate,'standard_error':err,
            'predicted':receipt_policy(K,N,p,beta,alpha,h)['P_success_episode']}


def run():
    cycle=brute_exact_seed_hitting(directed_cycle(12))
    triads=brute_exact_seed_hitting(synthetic_and_triads(4))
    dp=optimize_open_loop()
    goal=.95
    open_loop=[{'attempts':N,'success_episode':q,'success_20_gen':q**20,
                'seed_pulses_by_triad':[list(t) for t in plan]}
               for N,(q,plan) in sorted(dp.items()) if N in (12,16,18,19,20,21,22,23,24)]
    min_for_goal=min((N for N,(q,plan) in dp.items() if q**20>=goal),default=None)
    receipts=[receipt_policy(h=h,N=n) for h in (1,2,3,4) for n in (10,11,12,13,14)]
    return {'cycle_unary':cycle,'triadic_and_cycles':{k:v for k,v in triads.items() if k!='min_blocking_sets'},
            'random_spontaneous_per_episode_p05':exact_probability_random_spontaneous(),
            'open_loop_selected_budgets':open_loop,'minimum_open_loop_attempts_20_gen_95pct':min_for_goal,
            'receipts_at_budget_12':[r for r in receipts if r['N']==12],
            'minimum_receipt_attempts_20_gen_95pct':{h:next((n for n in range(8,80)
                if receipt_policy(N=n,h=h)['P_success_20_independent_generations']>=goal),None)
                for h in (1,2,3,4)},
            'receipt_mc':monte_carlo_pioneer(),
            'shared_episode_failure_max_over20_gens_at_0.005':(1-.005)**20}

if __name__=='__main__':
    out=run()
    for name,value in out.items():print(name,':',value)
    with open('/mnt/data/astra_xh2_bootstrap_seed_checks.json','w') as f:json.dump(out,f,indent=2)

# --- Second attack: seed persistence and premature release during AND-cycle startup ---
def pioneer_race(num_triads=4, generations=20, maturation=1.0, seed_decay=0.01):
    """Assume exactly two already-present pioneer roles per triad; the third
       matures at exp(rate maturation). Either pioneer is lost at exp(seed_decay)
       and the triad fails irrecoverably. No retry or re-seed (strict baseline).
    """
    q=maturation/(maturation+2*seed_decay)
    return {'per_triad':q,'per_episode':q**num_triads,'across_generations':q**(num_triads*generations)}

def threshold_for_maturation(num_triads=4,generations=20,target=.95):
    q=target**(1/(num_triads*generations))
    # maturation / decay >= 2 q/(1-q)
    return 2*q/(1-q)

def prematurity_budget(num_triads=4,generations=20,target=.95,alpha=.03):
    m=num_triads*generations
    max_false=1-target**(1/m)
    return {'total_critical_releases':m,'max_false_per_release':max_false,
            'h_required_independent_positive_readings':next(h for h in range(1,15) if alpha**h<=max_false),
            '20_gen_reliability_readings_2':(1-alpha**2)**m,
            '20_gen_reliability_readings_3':(1-alpha**3)**m}

def validate_race(reps=300000, seed=11, maturation=1., loss=.01):
    rng=np.random.default_rng(seed)
    maturation_time=rng.exponential(1/maturation,reps)
    first_loss_time=np.minimum(rng.exponential(1/loss,reps),rng.exponential(1/loss,reps))
    obs=float((maturation_time<first_loss_time).mean())
    expect=pioneer_race(maturation=maturation,seed_decay=loss)['per_triad']
    se=math.sqrt(expect*(1-expect)/reps)
    assert abs(obs-expect)<5*se
    return {'observed':obs,'predicted':expect,'standard_error':se}

def check_random_hypergraphs(reps=60, n=7, seed=122):
    rng=np.random.default_rng(seed)
    for _ in range(reps):
        deps=[]
        for j in range(n):
            nalt=int(rng.integers(1,4))
            choices=[]
            for _ in range(nalt):
                subset=int(rng.integers(0,1<<n))
                choices.append(subset)
            deps.append(tuple(choices))
        out=brute_exact_seed_hitting(deps)
        assert not out['bad_theorem_counterexamples']
    return {'random_hypergraphs_checked':reps,'roles_per_graph':n,'theorem_violations':0}

if __name__=='__main__':
    additional={'pioneer_lifetime_competition':{f'gamma_over_lambda_{ratio}':pioneer_race(maturation=ratio,seed_decay=1) for ratio in [10,100,1000,4000]},
        'minimum_maturation_to_decay_ratio_for_95pct_20gen':threshold_for_maturation(),
        'escrow_confirmation_error_budget':prematurity_budget(),
        'pioneer_race_mc':validate_race(),
        'random_hypergraph_validation':check_random_hypergraphs()}
    with open('/mnt/data/astra_xh2_bootstrap_lifetime_checks.json','w') as f:json.dump(additional,f,indent=2)
    for k,v in additional.items():print(k,v)

# --- Third attack: source-copy fidelity vs temporary physical seed removal, information cost ---
def receipt_policy_shared(K=8,N=13,p=.95,beta=.97,alpha=.03,h=2,zeta=0.):
    good=p*(zeta+(1-zeta)*beta**h)
    bad=(1-p)*(zeta+(1-zeta)*alpha**h)
    a=good+bad
    return {'N':N,'h':h,'shared_false_episode':zeta,'P_good_given_receipt':good/a,
            'P_episode':float(binom.sf(K-1,N,a)*(good/a)**K),
            'P_20_gen':float((binom.sf(K-1,N,a)*(good/a)**K)**20),
            'P_max_20_gen_without_budget':(good/a)**(K*20)}

def expected_stopped_attempts(K,N,p,beta,alpha,h):
    a=p*beta**h+(1-p)*alpha**h
    return sum(float(binom.cdf(K-1,j,a)) for j in range(N))

if __name__=='__main__':
    third={'receipt_cost_vs_open_loop':{'open_loop_attempts':20,
        'h2_N13_expected_attempts':expected_stopped_attempts(8,13,.95,.97,.03,2),
        'h2_N13_expected_binary_reports':2*expected_stopped_attempts(8,13,.95,.97,.03,2),
        'h2_N13_20gen_reliability':receipt_policy(N=13,h=2)['P_success_20_independent_generations']},
        'shared_episode_false_positive':{str(z):receipt_policy_shared(zeta=z)
             for z in (0,.001,.003,.005,.01)},
        'one_founder_programme_defect_across_20_gens':{str(mu):(1-mu)**20 for mu in (0,.001,.005,.01)}}
    with open('/mnt/data/astra_xh2_bootstrap_receipt_robustness.json','w') as f:json.dump(third,f,indent=2)
    for k,v in third.items():print(k,v)

# --- Fourth attack: phenotype-only bootstrap-order assay ---
def triad_bootstrap_slope(p,triads=4):
    q=(3*p*p-2*p**3)**triads
    slope=triads*(2-2*p/(3-2*p))
    return {'seed_rate':p,'P_global_success':q,'logarithmic_response':slope,'trials_for_100_expected_successes':100/q}

if __name__=='__main__':
    d={str(p):triad_bootstrap_slope(p) for p in (.05,.10,.25,.50)}
    with open('/mnt/data/astra_xh2_bootstrap_order_checks.json','w') as f:json.dump(d,f,indent=2)
    print('bootstrap_order_observability',d)
