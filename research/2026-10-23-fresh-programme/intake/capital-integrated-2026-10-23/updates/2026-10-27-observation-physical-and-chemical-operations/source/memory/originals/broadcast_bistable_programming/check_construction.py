"""Exact arithmetic lifecycle checks and local independent-event certificates.

Finite checks corroborate the separate spatial-induction proof; they do not
themselves prove arbitrary N or physical device reliability.
"""
import itertools,json,time
from pathlib import Path
from fractions import Fraction as F
from network import build,run,serializable,protocol


def canonical_start(net):
    state=[-1]*len(net.names)
    for j,i in enumerate(net.q):state[i]=1 if j%2==0 and j>0 else -1
    for i in net.z:state[i]=1
    return state


def initial_phases(net):
    state=[-1]*len(net.names)
    out=[]
    def add(name,H,indices,sign):
        nonlocal state
        before=list(state)
        for i in indices:state[i]=sign
        out.append((name,F(H),before,list(state)))
    add('prepare',-10,net.q[2::2],1)
    add('align',8,[net.q[0]],1)
    add('temporary_set',15,net.m,1)
    add('arm',24,net.z,1)
    add('nucleate',-10,[net.q[0]],-1)
    add('erase',-16,net.m,-1)
    assert state==canonical_start(net)
    return out


def local_event_certificate(net,H,before,after):
    changed=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b]
    assert changed
    # Desired switches are pairwise uncoupled, so any order gives the same
    # critical field and target local force; no directed edge is assumed.
    independent=all(j not in net.J[i] for i in changed for j in changed if i!=j)
    assert independent
    f0=net.local(before,F(0))
    criticals=[(after[i]*net.c[i]-f0[i])/net.g[i] for i in changed]
    assert len(set(criticals))==1
    hc=criticals[0]
    direction=after[changed[0]]
    assert all(after[i]==direction for i in changed)
    assert direction*(H-hc)>0
    changed_set=set(changed)
    wrong=[]
    for i in range(len(before)):
        if i in changed_set:continue
        # At the critical field, test the entire continuous box x_j in [-1,1]
        # for all switching cells, not just one asynchronous update order.
        fixed=net.g[i]*hc+net.b[i]+sum(w*before[j] for j,w in net.J[i].items() if j not in changed_set)
        uncertainty=sum(abs(w) for j,w in net.J[i].items() if j in changed_set)
        lower_margin=net.c[i]+before[i]*fixed-uncertainty
        wrong.append(lower_margin)
    final_margins=net.margins(after,H)
    return dict(changed=[net.names[i] for i in changed],critical_field=hc,
                target_amplitude_margin=abs(H-hc),
                minimum_wrong_cell_margin_at_event=min(wrong),
                minimum_final_endpoint_margin=min(final_margins),
                independent_switching_cells=independent,
                positive_wrong_margins=bool(min(wrong)>0 and min(final_margins)>0))


def programming_certificates(N):
    net=build(N);rows=[]
    for step in range(N):
        for prefix in itertools.product([-1,1],repeat=step):
            state=canonical_start(net)
            for j in range(2*step+1):state[net.q[j]]= -1 if j%2==0 else 1
            for j,bit in enumerate(prefix):state[net.m[j]]=bit
            # Initial domain wall is between q_(2step+1) and q_(2step+2).
            for bit in [0,1]:
                before=list(state);after=list(state);after[net.q[2*step+1]]=1
                a=local_event_certificate(net,F(10),before,after)
                rows.append(dict(N=N,step=step+1,prefix=prefix,bit=bit,phase='position',certificate=a))
                state2=after
                if bit:
                    before=list(state2);after=list(state2);after[net.m[step]]=1
                    b=local_event_certificate(net,F(12),before,after)
                    rows.append(dict(N=N,step=step+1,prefix=prefix,bit=bit,phase='write',certificate=b))
                    state2=after
                before=list(state2);after=list(state2);after[net.q[2*step+2]]=-1
                c=local_event_certificate(net,F(-10),before,after)
                rows.append(dict(N=N,step=step+1,prefix=prefix,bit=bit,phase='advance',certificate=c))
    return rows


def main():
    start=time.monotonic();root=Path(__file__).resolve().parent
    rows=[]
    for N in range(1,7):
        for bits in itertools.product([0,1],repeat=N):
            r=run(bits)
            if not r['correct']:raise AssertionError((bits,r['output']))
            rows.append(dict(N=N,bits=bits,correct=True,minimum_endpoint_margin=min(x['minimum_endpoint_margin'] for x in r['phases']),
                             work=r['work'],dissipation=r['dissipation'],gross_positive_work=r['gross_positive_work'],
                             flips=sum(e['kind']=='flip' for e in r['events'])))
    lifecycle=[]
    for N in [1,2,3]:
        final=[]
        for old in itertools.product([0,1],repeat=N):
            old_state=run(old)['state']
            for new in itertools.product([0,1],repeat=N):
                for order in ['lowest','highest','steepest']:
                    z=run(new,initial=old_state,order=order)
                    if not z['correct']:raise AssertionError((old,new,order))
                    final.append(dict(old=old,new=new,order=order,work=z['work'],dissipation=z['dissipation'],
                                      gross_positive_work=z['gross_positive_work'],energy_change=z['energy_change']))
        lifecycle.append(dict(N=N,cases=final))
    cert=[]
    for N in range(1,5):
        net=build(N)
        for phase,H,before,after in initial_phases(net):
            cert.append(dict(N=N,phase=phase,certificate=local_event_certificate(net,H,before,after)))
        cert.extend(programming_certificates(N))
    assert all(x['certificate']['positive_wrong_margins'] for x in cert)
    resource=[]
    for N in [1,2,4,8,16,32]:
        row=[]
        for bit in [0,1]:
            bits=[bit]*N
            r0=run(bits)
            r=run([1-bit]*N,initial=r0['state'])
            row.append(dict(old_bit=bit,new_bit=1-bit,cells=len(r['net'].names),edges=sum(len(x) for x in r['net'].J)//2,
                            pulses=len(protocol([1-bit]*N)),work=r['work'],dissipation=r['dissipation'],gross_positive_work=r['gross_positive_work'],
                            flips=sum(e['kind']=='flip' for e in r['events']),correct=r['correct']))
        resource.append(dict(N=N,cases=row))
    output=dict(status='EXACT_ARITHMETIC_MODEL_CHECKS_NOT_PHYSICAL_VALIDATION',
                target_pattern_checks=rows,rewrite_order_checks=lifecycle,
                local_continuous_transition_certificates=cert,resource_scaling=resource,
                elapsed_s=time.monotonic()-start)
    (root/'CHECKS.json').write_text(json.dumps(serializable(output),indent=2)+'\n')
    print(json.dumps(dict(patterns=len(rows),rewrite_cases=sum(len(x['cases']) for x in lifecycle),
                          local_certificates=len(cert),all_passed=True,elapsed_s=output['elapsed_s'])))
    for z in resource:print(json.dumps(serializable(z)))
    demo=run([1,0,1,1,0])
    (root/'EXAMPLE_10110.json').write_text(json.dumps(serializable(demo),indent=2)+'\n')


if __name__=='__main__':main()
