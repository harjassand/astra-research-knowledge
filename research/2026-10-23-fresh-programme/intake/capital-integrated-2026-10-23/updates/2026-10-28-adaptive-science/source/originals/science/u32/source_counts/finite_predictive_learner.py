#!/usr/bin/env python3
"""Count-only controlled observable-operator learner and operation compiler.

This file deliberately does not import the simulated plant. Its inputs are
integer action/outcome counts, the legal interface, and a PAID architecture
rank bound. Coordinates are probabilities of legal future tests, not hidden
density matrices. Learned matrices may be signed; physicality is not claimed.
"""
import itertools
import math
import numpy as np


class CountOracle:
    def __init__(self, data, alpha=0.01):
        self.settings = data['settings']
        self.actions = data['number_actions']
        self.outcomes = data['number_outcomes']
        self.rank_bound = data['observable_rank_upper_bound']
        self.maximum_length = data['maximum_length']
        # Every fixed action word and wildcard/outcome event of every length
        # up to L is covered BEFORE the data-dependent basis is selected.
        self.confidence_pool = sum((self.actions*(self.outcomes+1))**n
                                   for n in range(1,self.maximum_length+1))
        self.alpha = alpha
        self.cache = {}

    def event(self, actions, outcomes):
        actions,outcomes = tuple(actions),tuple(outcomes)
        key = actions,outcomes
        if key in self.cache:
            return self.cache[key]
        if not len(actions) or all(o is None for o in outcomes):
            result = (1.0,0.0,0,0)
        else:
            successes,total = 0,0
            n = len(actions)
            if len(outcomes) != n or n > self.maximum_length:
                raise ValueError('Unacquired event')
            for setting in self.settings:
                aa = tuple(setting['actions'])
                if aa[:n] != actions:
                    continue
                counts = setting['counts']
                total += sum(counts)
                for number,count in enumerate(counts):
                    bits = tuple((number >> (len(aa)-1-j)) & 1 for j in range(n))
                    if all(o is None or bits[j] == o for j,o in enumerate(outcomes)):
                        successes += count
            if not total:
                raise ValueError('No shots for event')
            width = math.sqrt(math.log(2*self.confidence_pool/self.alpha)/(2*total))
            result = (successes/total,width,successes,total)
        self.cache[key] = result
        return result

    def cell(self, preparation, future, insertion=()):
        # Preparation outcomes are intentionally discarded. An insertion or
        # future consists of (action, outcome) pairs. No conditional oracle.
        actions = tuple(preparation)+tuple(a for a,o in insertion+future)
        outcomes = (None,)*len(preparation)+tuple(o for a,o in insertion+future)
        return self.event(actions,outcomes)


def learn(data, alpha=0.01):
    q = CountOracle(data,alpha)
    r = q.rank_bound
    if r != 4 or q.outcomes != 2:
        raise ValueError('This prototype searches the stated qubit rank-4 basis')
    preparations = [()]+[(a,) for a in range(q.actions)]
    tests = [()]+[((a,o),) for a in range(q.actions) for o in range(2)]
    table = np.array([[q.cell(p,f)[0] for p in preparations] for f in tests])
    best = None
    # Empty test is fixed as row zero, making the trace functional known.
    for cols in itertools.combinations(range(len(preparations)),r):
        for other in itertools.combinations(range(1,len(tests)),r-1):
            rows = (0,)+other
            h = table[np.ix_(rows,cols)]
            singular = np.linalg.svd(h,compute_uv=False)
            if best is None or singular[-1] > best[0]:
                best = singular[-1],rows,cols
    _,rows,cols = best
    fs = [tests[i] for i in rows]
    ps = [preparations[j] for j in cols]
    h = table[np.ix_(rows,cols)]
    inv = np.linalg.inv(h)
    dh = np.array([[q.cell(p,f)[1] for p in ps] for f in fs])
    raw,shift_widths = {},{}
    for a in range(q.actions):
        for o in range(2):
            z = ((a,o),)
            hz = np.array([[q.cell(p,f,z)[0] for p in ps] for f in fs])
            dz = np.array([[q.cell(p,f,z)[1] for p in ps] for f in fs])
            raw[a,o] = hz@inv
            shift_widths[a,o] = dz
    b = {z:v.copy() for z,v in raw.items()}
    trace = np.eye(r)[0]
    # Exact causal normalization is known from the interface. Apply a declared
    # row repair; its size and extra error are included in the ledger below.
    for a in range(q.actions):
        discrepancy = trace-b[a,0][0]-b[a,1][0]
        b[a,1][0] += discrepancy
    x0 = np.array([q.cell((),f)[0] for f in fs])
    dx0 = max(q.cell((),f)[1] for f in fs)
    jhat = float(np.linalg.norm(inv,np.inf))
    deltah = float(np.linalg.norm(dh,np.inf))
    neumann = jhat*deltah
    cert = {'confidence_failure_probability':alpha,
            'uniform_event_pool_size':q.confidence_pool,
            'H_error_infinity_bound':deltah,
            'inverse_H_infinity_norm':jhat,
            'inverse_neumann_product':neumann,
            'initial_coordinate_infinity_error':dx0,
            'all_candidate_events_simultaneously_covered':True}
    if neumann < 1:
        jtrue = jhat/(1-neumann)
        kappa = r*jtrue
        errors = {}
        for z in raw:
            dshift = float(np.linalg.norm(shift_widths[z],np.inf))
            errors[z] = (dshift+np.linalg.norm(raw[z],np.inf)*deltah)*jtrue
        # The causal row repair changes only branch 1, by a measured amount.
        for a in range(q.actions):
            errors[a,1] += float(np.linalg.norm(b[a,1]-raw[a,1],np.inf))
        summed = max(errors[a,0]+errors[a,1] for a in range(q.actions))
        cert.update({'rank_4_certified_given_architecture_bound':True,
                     'true_inverse_H_infinity_upper_bound':jtrue,
                     'quotient_norm_equivalence_kappa_upper_bound':kappa,
                     'primitive_instrument_quotient_error_upper_bound':kappa*summed,
                     'branch_coordinate_error_bounds':{f'{a},{o}':float(v) for (a,o),v in errors.items()},
                     'initial_quotient_error_upper_bound':kappa*dx0})
    else:
        cert['rank_4_certified_given_architecture_bound'] = False
    return {'H':h,'H_inverse':inv,'preparations':ps,'tests':fs,'B':b,'raw_B':raw,
            'x0':x0,'certificate':cert,'architecture_rank_upper_bound':r}


def compile_pattern_controller(model, abort_probability):
    """Two classical states; action 0/3; success at observed pattern 1,0.

    Force an exact external abort coin BEFORE each primitive. Abort preserves
    physical memory. Success and abort both remain terminal outcomes.
    """
    b = model['B']
    r = len(model['x0'])
    q = np.zeros((2*r,2*r))
    a_success = np.zeros((r,2*r))
    for c,action in [(0,0),(1,3)]:
        for o in range(2):
            if c == 1 and o == 0:
                a_success[:,c*r:(c+1)*r] += b[action,o]
            else:
                q[o*r:(o+1)*r,c*r:(c+1)*r] += b[action,o]
    entry = np.vstack([np.eye(r),np.zeros((r,r))])
    merge = np.hstack([np.eye(r),np.eye(r)])
    gamma = 1-abort_probability
    resolvent = np.linalg.inv(np.eye(2*r)-gamma*q)
    os = gamma*a_success@resolvent@entry
    oa = abort_probability*merge@resolvent@entry
    trace_c = np.tile(np.eye(r)[0],2)
    expected_calls = gamma*trace_c@resolvent@entry
    return {'success':os,'abort':oa,'expected_calls_row':expected_calls,
            'continuation_spectral_radius':float(max(abs(np.linalg.eigvals(gamma*q)))),
            'resolvent_2_condition_number':float(np.linalg.cond(np.eye(2*r)-gamma*q)),
            'causal_row_error':float(np.max(abs((os+oa)[0]-np.eye(r)[0])))}


def predict_controller(model,compiled,continuation_action=2):
    x0,b = model['x0'],model['B']
    s = compiled['success']@x0
    a = compiled['abort']@x0
    ss = compiled['success']@s
    return {'success_probability':float(s[0]),
            'success_joint_test1':float((b[continuation_action,1]@s)[0]),
            'success_conditional_test1':float((b[continuation_action,1]@s)[0]/s[0]),
            'abort_joint_test1':float((b[continuation_action,1]@a)[0]),
            'abort_conditional_test1':float((b[continuation_action,1]@a)[0]/a[0]),
            'two_success_probability':float(ss[0]),
            'two_success_joint_test1':float((b[continuation_action,1]@ss)[0]),
            'two_success_conditional_test1':float((b[continuation_action,1]@ss)[0]/ss[0]),
            'expected_primitive_calls':float(compiled['expected_calls_row']@x0)}


def search_reset_word(model,maximum_length=4):
    b = model['B']
    r = len(model['x0'])
    candidates = []
    for length in range(1,maximum_length+1):
        for word in itertools.product(range(4),repeat=length):
            op = np.eye(r)
            for a in word:
                op = (b[a,0]+b[a,1])@op
            # The exact trace row preserves mass; differences of normalized
            # histories have coordinate zero in that row.
            contraction = float(np.linalg.norm(op[1:,1:],np.inf))
            candidates.append((contraction**(1/length),contraction,word,op))
    score,contraction,word,op = min(candidates,key=lambda x:x[0])
    fixed = np.linalg.solve(np.eye(r-1)-op[1:,1:],op[1:,0])
    return {'word':list(word),'length':len(word),'coordinate_contraction':contraction,
            'per_primitive_contraction_score':score,'fixed_predictive_state':np.r_[1,fixed],
            'operator':op}


def serializable(model):
    return {'H':model['H'].tolist(),'H_inverse':model['H_inverse'].tolist(),
            'preparations':[list(x) for x in model['preparations']],
            'tests':[[list(z) for z in f] for f in model['tests']],
            'B':{f'{a},{o}':v.tolist() for (a,o),v in model['B'].items()},
            'x0':model['x0'].tolist(),'certificate':model['certificate'],
            'architecture_rank_upper_bound':model['architecture_rank_upper_bound']}
