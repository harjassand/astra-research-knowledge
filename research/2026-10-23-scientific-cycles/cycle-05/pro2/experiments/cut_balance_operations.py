#!/usr/bin/env python3
"""One exact receiving experiment for the new degree-free certificate.

No old benchmark, palette search, eigensolver or precision sweep is run.
"""
import sys, json, time, resource, hashlib
from pathlib import Path
from fractions import Fraction as F
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from cut_balance import prepare, decode, action, norm_sq, summary, subdivided_star, double_star
from coordinate_decoder import cut_witness, matrix_frobenius_sq


def rows(x): return [[str(v) for v in row] for row in x]
def coefficients(d,w):
    return {'diagonal':[str(x) for x in d],
            'edge_values':[[u,v,str(value)] for (u,v),value in sorted(w.items())]}


def noise_case(n,edges,colors,q):
    start=time.perf_counter(); plan=prepare(n,iter(edges),colors,q)
    prep=time.perf_counter()-start
    d=[F((i*7)%17-8,13) for i in range(n)]
    w={tuple(sorted(e)):F((11*i)%23-11,19) for i,e in enumerate(edges)}
    start=time.perf_counter(); Y=action(n,q,colors,d,w)
    action_time=time.perf_counter()-start
    start=time.perf_counter(); assert decode(plan,Y)==(d,w)
    noiseless=time.perf_counter()-start
    E=[[F((31*i+7*j)%29-14,101) for j in range(q)] for i in range(n)]
    start=time.perf_counter()
    out_d,out_w=decode(plan,[[a+e for a,e in zip(yr,er)] for yr,er in zip(Y,E)])
    noisy=time.perf_counter()-start
    delta_d=[a-b for a,b in zip(out_d,d)]
    delta_w={e:out_w[e]-w[e] for e in w}
    diagonal_noise_sq=sum((E[i][colors[i]]**2 for i in range(n)),F(0))
    used_off=set(); outgoing=[F(0)]*n
    for c in plan['components']:
        a,b=c['pair']; N=len(c['order'])
        block_noise_sq=sum((E[v][b if colors[v]==a else a]**2 for v in c['order']),F(0))
        for v in c['order']: used_off.add((v,b if colors[v]==a else a))
        child_rows={v:[] for v in c['order']}
        for v in c['order'][1:]: child_rows[c['parent'][v]].append(v)
        for parent,children in child_rows.items():
            local_sq=sum((delta_w[tuple(sorted((parent,v)))]**2 for v in children),F(0))
            assert local_sq <= c['maximum_child_subtree']*block_noise_sq
            outgoing[parent]+=local_sq
    off_noise_sq=sum((E[i][j]**2 for i,j in used_off),F(0))
    M=plan['centroid_branch_maximum']
    assert max(outgoing,default=0) <= M*off_noise_sq
    assert max((v*v for v in delta_d),default=0) <= diagonal_noise_sq
    assert diagonal_noise_sq+off_noise_sq <= norm_sq(E)
    # Actual Frobenius error is recorded, not substituted for operator error.
    record={'plan':summary(plan),'edges':edges,'colors':colors,**coefficients(d,w),
            'noise':rows(E),'decoded':coefficients(out_d,out_w),
            'noise_norm_sq':str(norm_sq(E)),
            'error_frobenius_sq':str(matrix_frobenius_sq(delta_d,delta_w)),
            'diagonal_noise_sq':str(diagonal_noise_sq),'used_off_noise_sq':str(off_noise_sq),
            'maximum_outgoing_error_sq':str(max(outgoing,default=0)),
            'all_noise_certificate':'PROOF.md centroid covariance and sparse-column inequality',
            'phase_wall_seconds':{'preparation':prep,'synthetic_action':action_time,
                                  'exact_noiseless_decoding':noiseless,'exact_noisy_decoding':noisy}}
    return plan, record


def main():
    wall=time.perf_counter(); cpu=time.process_time()
    L=12; m=33
    n,edges,colors,arms=subdivided_star([L]*m)
    plan,case=noise_case(n,edges,colors,2)
    assert plan['gamma']==F(L*(n-L),n) and plan['centroid_branch_maximum']==L
    assert plan['cut_operator_constant_sq']==49
    cut=cut_witness(plan)
    cut_record={**coefficients(cut['diagonal'],cut['edge_values']),
                'edge':cut['edge'],'a':cut['a'],'b':cut['b'],
                'action_norm_sq':str(cut['action_norm_sq']),
                'inverse_lower_sq':str(cut['inverse_lower_sq'])}
    path=list(reversed(arms[0]))+[0]+arms[1]
    ramp={tuple(sorted(e)):F(0) for e in edges}
    for j,(u,v) in enumerate(zip(path,path[1:]),1):
        ramp[tuple(sorted((u,v)))]=F((-1)**(j-1)*min(j,2*L+1-j))
    ramp_action=action(n,2,colors,[F(0)]*n,ramp)
    f2=matrix_frobenius_sq([F(0)]*n,ramp)
    assert norm_sq(ramp_action)==2*L
    assert f2/norm_sq(ramp_action)==F((L+1)*(2*L+1),3)
    # Same graph, established forest depth-mod-three comparator, not new science.
    colors3=[0]*n
    for arm in arms:
        for depth,v in enumerate(arm,1): colors3[v]=depth%3
    p3=prepare(n,edges,colors3,3)
    for comp in p3['components']:
        degrees={v:0 for v in comp['order']}
        for v in comp['order'][1:]:
            degrees[v]+=1; degrees[comp['parent'][v]]+=1
        assert sum(d>1 for d in degrees.values())<=1
    t=32; dn,de,dc=double_star(t); dp=prepare(dn,de,dc,2)
    dw={tuple(sorted(e)):(F(1) if e==(0,1) else -F(1,t+1)) for e in de}
    dy=action(dn,2,dc,[F(0)]*dn,dw)
    assert norm_sq(dy)==F(2,t+1) and dp['gamma']==F(t+1,2)
    result={'status':'PASS','experiment':'cut_balance_operations',
            'arm_operation':case,'arm_lengths':[L]*m,
            'cut_adversary':cut_record,
            'operator_vs_frobenius_witness':{**coefficients([F(0)]*n,ramp),
                'selected_path':path,'action_norm_sq':str(norm_sq(ramp_action)),
                'matrix_frobenius_sq':str(f2),
                'frobenius_inverse_lower_sq':str(f2/norm_sq(ramp_action)),
                'operator_inverse_upper_sq':'49',
                'scope':'The exact SAME admitted design separates the two output norms.'},
            'same_graph_ordinary_comparator':{'q':3,'colors':colors3,
                'all_bichromatic_components_are_stars':True,
                'frobenius_and_operator_constant_sq':'2',
                'source':'Inherited depth-mod-three forest operation; no runtime superiority claimed.'},
            'double_star_failure':{'plan':summary(dp),'leaves_each':t,'edges':de,'colors':dc,
                **coefficients([F(0)]*dn,dw),'action':rows(dy),
                'action_norm_sq':str(norm_sq(dy)), 'unit_central_edge':[0,1],
                'operator_inverse_lower_sq':str(F(t+1,2)),
                'diameter':3,'scope':'Coordinate-design gluing failure, unbounded degree family; not full Δ4 obstruction.'},
            'costs':{'body_wall_seconds':time.perf_counter()-wall,
                     'body_cpu_seconds':time.process_time()-cpu,
                     'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                     'executions':1,'discovery_and_authoring':'unmetered; not included'}}
    path=ROOT/'results/cut_balance_operations.json'
    raw=(json.dumps(result,indent=2)+'\n').encode(); path.write_bytes(raw)
    print(json.dumps({'status':result['status'],'arm':case['plan'],
                      'ramp_frobenius_lower_sq':str(f2/norm_sq(ramp_action)),
                      'double_star':result['double_star_failure']['plan'],
                      'costs':result['costs'],'fixture_bytes':len(raw),
                      'fixture_sha256':hashlib.sha256(raw).hexdigest()},indent=2))


if __name__=='__main__': main()
