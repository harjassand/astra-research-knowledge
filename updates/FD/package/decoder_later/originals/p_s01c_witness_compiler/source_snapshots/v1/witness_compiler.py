"""Comparison-only full fixed-degree compiler with low-codimension witnesses.

The API sees only n,r,d,beta, a random seed and a chosen-pair comparison
callback. Hidden flags/coordinates/ranks appear only in the separate harness.
The copied safe-W/raw controls use the same raw selector and beta. Every
period label is expanded into four actual source comparisons, never a
supplied polynomial oracle. Python PRNG runs are finite reproducible fixtures;
the probability proof separately assumes ideal fresh conditional randomness.
"""
from __future__ import annotations

import math
from pathlib import Path
import random
import sys
import time

SNAPSHOT = Path(__file__).resolve().parent / 'reference_snapshot'
sys.path.insert(0, str(SNAPSHOT / 'degree_extension'))
import fixed_degree as fd
ac = fd.ac


def parameters(n, r, d, beta, prefix_length=None, mode='witness'):
    if mode not in ('witness', 'safe_W', 'raw_body'):
        raise ValueError('unknown compiler mode')
    base_mode = 'raw_body' if mode == 'raw_body' else 'safe_subspace'
    cfg = fd.parameters(n, r, d, beta, prefix_length, base_mode)
    m, h = cfg['stages'], cfg['h']
    p = 2.0 ** (-r-1)
    R = math.ceil(math.log(4*m/beta)/p) if m else 0
    gamma = 2.0 ** (-2*d)
    delta_raw = beta/(4*m*R*R) if m else 0.0
    raw_t = math.ceil(math.log(1/delta_raw)/-math.log1p(-gamma)) if m else 0
    outer_L = math.ceil(math.log(8*R*(m+r)/beta)/-math.log1p(-2.0**(-d))) if m and r else 0
    eta = beta/(8*r*R) if m and r else 0.0
    nu = 2.0 ** (-(r-1)) if r else 0.0
    period_L = (1 if r == 1 else math.ceil(math.log(n*(1 << r)/eta)/-math.log1p(-nu))) if m and r else 0
    P = sum(max(0, n-k-1) for k in range(m))
    H = math.ceil(4*P+8*math.log(4/beta)) if P else 0
    # Safe-W matched control: preserve its growth cap, strengthen the membership
    # semantic budget to inverse-R, and share exactly the witness raw selector.
    Nmax = max(cfg['member_trial_caps'], default=0)
    delta_member = beta/(8*m*R*Nmax) if m else 0.0
    member_t = math.ceil(math.log(1/delta_member)/-math.log1p(-2.0**(-(d-1)))) if m else 0
    A = sum(fd.M(k+r,d) for k in range(m))
    B = A + m*(n+1) + 3*(m+r)*outer_L + 4*r*n*(1 << r)*period_L
    if mode == 'witness':
        stage_cap = B
    elif mode == 'safe_W':
        stage_cap = A + sum(1 + cap*(1+2*member_t)+(h-k)
                            for k,cap in enumerate(cfg['member_trial_caps']))
    else:
        stage_cap = m*fd.M(n,d)
    cfg.update(mode=mode,control_budget='common inverse-R raw validation; same beta and exact source',
               p=p,R=R,gamma=gamma,raw_t=raw_t,delta_raw=delta_raw,
               outer_L=outer_L,period_eta=eta,period_L_max=period_L,
               delta_member=delta_member,member_t=member_t,
               tournament_pair_count_cap=P,tournament_total_attempt_cap=H,
               leading_interpolation_cap=A if mode != 'raw_body' else m*fd.M(n,d),
               witness_conditional_cap=B,stage_comparison_cap=stage_cap,
               worst_comparison_bound=stage_cap+3*m*R*raw_t+2*H+P+cfg['tail_comparisons'],
               expected_comparison_bound=(B+3*m*((1+beta/2)*raw_t+(1-p)/(p*gamma))
                    +5*P+cfg['tail_comparisons']) if mode == 'witness' else None,
               failure_budget=dict(raw_cap=beta/4,tournament_cap=beta/4,
                   first_false_raw=beta/(4*R) if R else 0,
                   first_outer_miss=beta/(8*R) if R and mode=='witness' else 0,
                   first_period_miss=beta/(8*R) if R and mode=='witness' else 0,
                   member_growth=beta/8 if mode=='safe_W' else 0,
                   first_false_member=beta/(8*R) if R and mode=='safe_W' else 0))
    cfg['failure_bound'] = sum(cfg['failure_budget'].values())
    return cfg


def contains(v, basis, n, meter=None):
    return len(ac.echelon(list(basis)+[v],n,meter)[0]) == len(basis)


def period_dictionary(label, n, W, xstar, cap, eta, rng, source, meter):
    """Learn ker of the hidden quotient-column map of P_x restricted to W."""
    w = len(W)
    if cap <= 0:
        return None,dict(status='UNKNOWN',reason='period_zero_cap')
    nu = 2.0 ** (-(cap-1))
    Lp = 1 if cap == 1 else math.ceil(math.log(w*(1 << cap)/eta)/-math.log1p(-nu))
    reps,columns = [],[]
    candidates = probes = rejected_count = 0
    source.phase='period_dictionary'
    for j in range(w):
        assigned = None
        for u in range(1 << len(reps)):
            candidates += 1
            meter.add('period_quotient_candidates')
            tlocal = (1 << j) ^ ac.combine(reps,u,meter)
            if not tlocal:
                assigned=u
                break
            t=ac.combine(W,tlocal,meter)
            rejected=False
            for _ in range(Lp):
                z=ac.combine(W,rng.getrandbits(w),meter)
                meter.add('period_probe_random_bits',w)
                probes+=1
                meter.add('period_second_derivative_probes')
                if label(z)^label(z^xstar)^label(z^t)^label(z^t^xstar):
                    rejected=True
                    rejected_count+=1
                    break
            if not rejected:
                assigned=u
                break
        if assigned is None:
            if len(reps)>=cap:
                return None,dict(status='UNKNOWN',reason='period_rank_cap',
                    candidates=candidates,probes=probes,probe_cap=Lp)
            assigned=1 << len(reps)
            reps.append(1 << j)
        columns.append(assigned)
    rows=[sum(((column >> i)&1) << j for j,column in enumerate(columns))
          for i in range(len(reps))]
    D=[ac.combine(W,bits,meter) for bits in ac.kernel(rows,w,meter)]
    if candidates>w*(1 << cap) or probes>w*(1 << cap)*Lp:
        raise ArithmeticError('dictionary deterministic cap')
    return D,dict(status='accepted_candidate',dimension_W=w,period_codimension=len(reps),
                  quotient_columns=columns,candidates=candidates,rejections=rejected_count,
                  probes=probes,probe_cap=Lp,source_comparisons=4*probes,nu=nu,
                  semantic_error_budget=eta)


def reconstruct(n,r,d,k,v,prefix,source,rng,cfg,meter,state):
    h=cfg['h']
    S=list(prefix.S)
    W=list(S)
    target=h-k
    c=len(W)-target
    source.phase='witness_base'
    q0=ac.core._label(source,v,0)
    label=lambda x:ac.core._label(source,v,x)
    if not 0<=c<=r or not contains(v,W,n,meter):
        return None,dict(status='UNKNOWN',reason='constant_input_guard')
    L=cfg['outer_L']
    mu=2.0 ** (-min(d-1,k+r-1)) if k+r>=2 else None
    tests=epochs=0
    witnesses=[]
    if c and d>1 and k+r>=2:
        while len(W)>target:
            epochs+=1
            state['outer_epochs']+=1
            if state['outer_epochs']>cfg['stages']+r:
                return None,dict(status='UNKNOWN',reason='global_outer_epoch_cap')
            witness=None
            source.phase='outer_witness_tests'
            for _ in range(L):
                s=ac.combine(W,rng.getrandbits(len(W)),meter)
                x=rng.getrandbits(n)
                meter.add('outer_direction_random_bits',len(W))
                meter.add('outer_point_random_bits',n)
                meter.add('outer_witness_probes')
                tests+=1
                if label(s)^label(x)^label(x^s)^q0:
                    witness=(s,x)
                    break
            if witness is None:
                break
            # This is intentionally BEFORE the paid dictionary. Post-drop-only
            # checking could pay one extra invocation after a bad-history refund.
            if state['global_drop']>=r or state['paid_dictionaries']>=r:
                return None,dict(status='UNKNOWN',reason='global_witness_budget_before_dictionary',
                                 outer_tests=tests,witnesses=witnesses)
            detected,xstar=witness
            state['paid_dictionaries']+=1
            D,receipt=period_dictionary(label,n,W,xstar,len(W)-target,
                                       cfg['period_eta'],rng,source,meter)
            if D is None:
                return None,dict(status='UNKNOWN',reason=receipt['reason'],dictionary=receipt)
            if len(ac.echelon(D,n,meter)[0])!=len(D) or not all(contains(s,W,n,meter) for s in D):
                return None,dict(status='UNKNOWN',reason='period_subspace_guard')
            if len(D)<target or not contains(v,D,n,meter):
                return None,dict(status='UNKNOWN',reason='period_minimum_or_own_toggle_guard')
            if len(D)>=len(W) or contains(detected,D,n,meter):
                return None,dict(status='UNKNOWN',reason='period_strict_drop_or_witness_guard')
            drop=len(W)-len(D)
            if state['global_drop']+drop>r:
                return None,dict(status='UNKNOWN',reason='global_drop_cap')
            state['global_drop']+=drop
            receipt.update(old_dimension=len(W),new_dimension=len(D),drop=drop,
                           xstar=xstar,detected_direction=detected,
                           global_drop_after=state['global_drop'])
            witnesses.append(receipt)
            W=D
    U=ac.complement(W,n,meter)
    if len(U)>k+r:
        return None,dict(status='UNKNOWN',reason='quotient_dimension_guard')
    source.phase='witness_quotient_interpolation'
    values={0:q0}
    for bits in fd.points(len(U),d)[1:]:
        values[bits]=label(ac.combine(U,bits,meter))
    qU=fd.interpolate(values,len(U),d,meter)
    source.phase='witness_affine_responses'
    responses=sum((label(w)^q0) << j for j,w in enumerate(W))
    basis=U+W
    rows=[sum(((basis[j] >> i)&1) << j for j in range(n)) for i in range(n)]
    coordinates=ac.matrix_inverse(rows,n,meter)
    u=len(U)
    def f(x):
        c=ac.linear(coordinates,x,meter)
        return qU(c&((1 << u)-1),meter)^ac.parity(responses&(c >> u),meter)
    # Raw polynomial expansion is local, separately charged; it is not a source
    # query and is not a compact-update bit-work claim.
    raw=fd.interpolate({x:f(x) for x in fd.points(n,d)},n,d,meter)
    if not raw.toggles(v,meter) or not all(old.invariant(v,meter) for old in prefix.q):
        return None,dict(status='UNKNOWN',reason='post_interpolation_toggle_gate')
    exact_C,_=fd.translation_filtration(raw,S,meter,constant_only=True)
    if not all(contains(w,exact_C,n,meter) for w in W):
        return None,dict(status='UNKNOWN',reason='constructed_affine_space_guard')
    return raw,dict(status='accepted_candidate',constant_space_basis=W,
                   constant_space_dimension=len(W),outer_tests=tests,outer_epochs=epochs,
                   outer_cap=L,mu=mu,witnesses=witnesses,
                   source_free_known_constant_space=(c==0 or k+r<=1 or d<=1),
                   quotient_dimension=u,quotient_anchor_count=fd.M(u,d),
                   affine_response_count=len(W),local_raw_expansion_anchors=fd.M(n,d),
                   semantic_exactness='conditional on raw/outer/period semantic success')


def acquire(n,r,d,query,seed,beta=.01,prefix_length=None,mode='witness',
            force_zero_directions=False):
    """Full model only under ALL-output degree promise; prefix allows arbitrary tail."""
    start=time.perf_counter()
    cfg=parameters(n,r,d,beta,prefix_length,mode)
    source,meter=ac.Source(query),ac.Meter()
    prefix=fd.Prefix(n,meter)
    stages=[]
    tournament=dict(attempts=0,matches=0)
    witness_state=dict(global_drop=0,paid_dictionaries=0,outer_epochs=0)
    def finish(status,reason=None,model=None):
        out=dict(status=status,reason=reason,parameters=cfg,comparison_calls=source.calls,
                 source_calls_by_phase=dict(source.by_phase),local_operations=dict(meter.ops),
                 random_bits={k:v for k,v in meter.ops.items() if k.endswith('random_bits')},
                 acquisition_seconds=time.perf_counter()-start,stages=stages,
                 acquired_toggle_vectors=list(prefix.toggles),acquired_stabilizer_basis=list(prefix.S),
                 model_bodies=[q.body() for q in model] if model is not None else None,
                 witness_totals=dict(witness_state),tournament_totals=dict(tournament),
                 failure_fixture='forced zero direction tape' if force_zero_directions else None)
        if source.calls>cfg['worst_comparison_bound']:
            raise ArithmeticError('whole learner deterministic query cap')
        if mode=='witness' and witness_state['paid_dictionaries']>r:
            raise ArithmeticError('global paid dictionary cap')
        return out,model,prefix
    for k in range(cfg['stages']):
        before=len(prefix.S)
        if not cfg['h']-k<=before<=n-k:
            return finish('UNKNOWN','stabilizer_dimension_guard')
        raw_rng=random.Random(seed+1000003*(k+1))
        witness_rng=random.Random(seed+1900033*(k+1))
        certified_zero=before==cfg['h']-k
        if certified_zero and not force_zero_directions:
            winner,trials,reason=ac._select_certified_zero(prefix.S,k,source,raw_rng,cfg,meter,tournament)
            if reason:
                return finish('UNKNOWN',reason)
        else:
            sampler=prefix.sampler()
            winner=None
            trials=[]
            for j in range(cfg['R']):
                v=0 if force_zero_directions else ac.combine(prefix.S,raw_rng.getrandbits(before),meter)
                meter.add('direction_random_bits',0 if force_zero_directions else before)
                if not v:
                    meter.add('zero_raw_directions_skipped')
                    continue
                source.phase='raw_pair_validation'
                passed=True
                for test in range(cfg['raw_t']):
                    if not ac.core._pair_test(k,v,sampler,source,raw_rng,meter):
                        passed=False
                        break
                trials.append(dict(direction=v,passed=passed,pair_tests=test+1))
                if passed:
                    winner=v
                    break
            if winner is None:
                return finish('UNKNOWN','raw_direction_cap')
        if mode=='raw_body':
            source.phase='raw_interpolation'
            q=fd.interpolate({x:ac.core._label(source,winner,x) for x in fd.points(n,d)},n,d,meter)
            rec=dict(status='accepted_candidate',raw_anchor_count=fd.M(n,d))
            if not q.toggles(winner,meter) or not all(old.invariant(winner,meter) for old in prefix.q):
                return finish('UNKNOWN','post_interpolation_toggle_gate')
        elif mode=='safe_W':
            q,rec=fd.reconstruct(n,r,d,k,winner,prefix,source,witness_rng,cfg,meter)
            if q is None:
                return finish('UNKNOWN',rec['reason'])
        else:
            q,rec=reconstruct(n,r,d,k,winner,prefix,source,witness_rng,cfg,meter,witness_state)
            if q is None:
                out,model,prefix=finish('UNKNOWN',rec['reason'])
                out['failed_reconstruction']=rec
                return out,model,prefix
        update=prefix.add(q,winner)
        after=len(prefix.S)
        if n-k-1-after>r:
            return finish('UNKNOWN','stabilizer_defect_guard')
        stages.append(dict(stage=k,selector='certified_zero_tournament' if certified_zero else 'raw_paired_cut',
                           dimension_S_before=before,dimension_S_after=after,
                           defect_before=n-k-before,defect_after=n-k-1-after,
                           direction=winner,trials=trials,reconstruction=rec,exact_update=update))
    if prefix_length is not None:
        return finish('returned_prefix',model=list(prefix.q))
    source.phase='tail_enumeration'
    sampler=prefix.sampler()
    values=[{} for _ in range(r)]
    for x in fd.points(n,d):
        local=sum(source(y,x) for y in sampler.fiber(prefix.prefix(x)) if y!=x)
        for j in range(r):
            values[j][x]=(local >> (r-j-1))&1
    if source.by_phase['tail_enumeration']!=cfg['tail_comparisons']:
        raise ArithmeticError('full tail accounting')
    model=list(prefix.q)+[fd.interpolate(values_j,n,d,meter) for values_j in values]
    return finish('returned_model',model=model)
