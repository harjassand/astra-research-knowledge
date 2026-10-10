from event_germs import *
import math, random, time, pathlib, hashlib, platform

HERE = pathlib.Path(__file__).resolve().parent


def lcm_denoms(result):
    d = 1
    for st in result['states'].values():
        if st['status'] == 'fires':
            for e, c in st['time'].terms:
                d = math.lcm(d, e.denominator)
    return d


def finite_checks(nodes, r, extra=(0, 1, 3)):
    d = lcm_denoms(r)
    L = max(d, ((r['L']+d-1)//d)*d)
    return [verify_at_dyadic(nodes, r, L+k*d) for k in extra]


def cancellation_case():
    # A's time = 1-sqrt(eps); B's time=1-sqrt(eps)-eps**3.
    return [node('A', 1, affine_reset=(F(2), F(0)), priority=0),
            node('prepare_B', F(1,2), eps_power=6, priority=1),
            node('B', F(1,2), activation=('prepare_B',), eps_power=1,
                 affine_reset=(F(1), F(1)), priority=2)]


def cascade(K):
    return [node(f'C{i}', priority=i, eps_power=1 if i==0 else 0,
                 activation=() if i==0 else (f'C{i-1}',),
                 gap_powers={} if i==0 else {f'C{i-1}': 1}) for i in range(K)]


def mixed_case(rng, layers=4, width=3):
    nodes=[]
    for layer in range(layers):
        for j in range(width):
            name=f'L{layer}N{j}'
            parents=() if layer==0 else tuple(f'L{layer-1}N{x}' for x in rng.sample(range(width), 2))
            weights={p: rng.choice([0,1,2]) for p in parents}
            ep=rng.randint(1,3) if not any(weights.values()) else rng.randint(0,2)
            nodes.append(node(name, rng.choice([F(1), F(1), F(2)]), activation=parents,
                              eps_power=ep, gap_powers=weights, priority=len(nodes),
                              affine_reset=(F(rng.randint(-2,2)), F(rng.randint(-3,3)))))
    return nodes


def run():
    results={'runtime': {'python': platform.python_version(), 'platform': platform.platform()},
             'status': 'Restricted exact prototype, not a novel general computational operation'}
    n=cancellation_case(); r=compile(n); base=nominal(n)
    assert r['order']==['prepare_B','B','A']
    assert r['output']==2 and base['output']==1
    gap=r['states']['A']['time']-r['states']['B']['time']
    assert gap==GP.monomial(3)
    checks=finite_checks(n,r)
    eps=1e-6
    ta=1-math.sqrt(eps)
    tb=(0.5-math.sqrt(eps**6))+(0.5-math.sqrt(eps))
    float_order=sorted([('A',ta,0),('B',tb,2)],key=lambda v:(v[1],v[2]))
    assert ta==tb and [x[0] for x in float_order]==['A','B']
    float_y=0
    for name,_,_ in float_order:
        float_y = 2*float_y if name=='A' else float_y+1
    assert float_y==1
    results['cancellation']={'exact_order':r['order'],'exact_output':str(r['output']),
                             'nominal_output':str(base['output']), 'L':r['L'],
                             'difference_A_minus_B':gap.serial(),
                             'binary64_epsilon':eps,'binary64_A_time':ta,'binary64_B_time':tb,
                             'binary64_wrong_order':[x[0] for x in float_order], 'binary64_wrong_output':float_y,
                             'finite_rational_checks': checks}
    (HERE/'cancellation_input.json').write_text(json.dumps([x.serial() for x in n],indent=2)+'\n')
    (HERE/'cancellation_certificate.json').write_text(serialize_result(r)+'\n')
    reloaded=compile(load_native_file(HERE/'cancellation_input.json'))
    assert serialize_result(reloaded)==serialize_result(r)

    n=[node('vanishes',source_sign=-1,affine_reset=(F(1),F(1)),priority=0),
       node('blocked',activation=('vanishes',),eps_power=0,gap_powers={'vanishes':1},
            affine_reset=(F(1),F(2)),priority=1)]
    r=compile(n)
    assert r['order']==[] and r['output']==0 and nominal(n)['output']==3
    finite_checks(n,r)
    results['event_disappearance']={'one_sided_output':str(r['output']),
                                   'nominal_output':str(nominal(n)['output']),
                                   'statuses':{k:v['status'] for k,v in r['states'].items()}}

    rng=random.Random(20261010)
    count,events,comparisons,order_changes=0,0,0,0
    worst_L=0
    for test in range(100):
        n=mixed_case(rng)
        r=compile(n)
        for check in finite_checks(n,r):
            count+=1;events+=check['events'];comparisons+=check['comparisons']
        order_changes+=r['order']!=nominal(n)['order']
        worst_L=max(worst_L,r['L'])
    results['random_native_dags']={'models':100,'rational_epsilon_checks':count,
                                  'native_guard_checks':events,'sign_checks':comparisons,
                                  'models_with_order_change_from_nominal':order_changes,
                                  'largest_certificate_exponent_L':worst_L,'seed':20261010}

    benchmarks=[]
    for K in (8,16,32,64,128,256):
        t=time.perf_counter(); n=cascade(K);r=compile(n); dt=time.perf_counter()-t
        last=r['states'][f'C{K-1}']
        assert last['exponent']==F(1,2**K)
        assert len(last['time'].terms)==K+1
        # An independent native guard-identity check using exponents, no numerics.
        for i in range(K):
            a=r['states'][f'C{i}']['exponent']
            source=F(1) if i==0 else r['states'][f'C{i-1}']['exponent']
            assert 2*a==source
        if K==8: finite_checks(n,r)
        benchmarks.append({'events':K,'elapsed_seconds':dt,
                           'last_exponent':str(last['exponent']),
                           'last_exponent_denominator_bits':last['exponent'].denominator.bit_length(),
                           'last_time_terms':len(last['time'].terms),
                           'all_state_time_terms':sum(len(s['time'].terms) for s in r['states'].values()),
                           'L_bits':r['L'].bit_length(), 'L':str(r['L']),
                           'queue_and_activation_sign_checks':len(r['comparisons'])})
    results['growing_cascades']=benchmarks

    # A finite-epsilon ordering reversal: germ order is not globally valid.
    p=GP.make([(F(1,2), 1),(1,-2)])
    cert=p.sign_certificate()
    assert cert['sign']==1
    assert p.at_power_of_two(2)==0
    assert p.at_power_of_two(0)<0
    assert p.at_power_of_two(4)>0
    results['finite_radius_matters']={'difference':p.serial(),'certificate':cert,
                                      'at_epsilon_1':'negative',
                                      'at_epsilon_1_over_4':'zero',
                                      'at_epsilon_1_over_16':'positive'}

    # Native-input boundary checks must reject, not silently accept.
    rejects=[]
    bad=[Node('bad_guard',(F(2),F(-2),F(1)),priority=0),
         node('bad_constant_source',eps_power=0,priority=0)]
    for item in bad:
        try: compile([item])
        except ValueError as e: rejects.append(str(e))
        else: raise AssertionError('Out-of-class guard silently accepted')
    results['rejected_out_of_class_inputs']=rejects
    (HERE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': run()
