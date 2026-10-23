"""Fixed Cycle7 receiving uses. No old science is replayed.
All four full original action columns, free diagonals, rational nonzero noise.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time,resource,hashlib
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'src'))
from star_recovery import build,check_star,obstruction_spec,mixed_spec
from coordinate_decoder import prepare,decode,action,norm_sq,matrix_frobenius_sq

def pack_matrix(d,e):
    return {'diagonal':list(map(str,d)),'edges':[[u,v,str(x)] for (u,v),x in sorted(e.items())]}
def pack_action(Y):return [[str(x) for x in row] for row in Y]
def projection(plan,Y):
    n=plan['n'];colors=plan['colors'];out=[[F(0)]*4 for _ in range(n)]
    for v in range(n):out[v][colors[v]]=Y[v][colors[v]]
    for comp in plan['components']:
        a,b=comp['pair'];vs=comp['order']
        mu=sum((1 if colors[v]==a else -1)*Y[v][b if colors[v]==a else a] for v in vs)/len(vs)
        for v in vs:
            other=b if colors[v]==a else a;sign=1 if colors[v]==a else -1
            out[v][other]=Y[v][other]-sign*mu
    return out

def receiving(name,spec,old=None):
    t=time.perf_counter();g=build(spec);construction=time.perf_counter()-t
    t=time.perf_counter();cert=check_star(g['n'],g['edges'],g['colors'])
    n=g['n'];es=g['edges'];colors=g['colors'];plan=prepare(n,es,colors,4)
    for comp in plan['components']:
        assert comp['max_degree']==len(comp['order'])-1 or len(comp['order'])<=2
    prepare_time=time.perf_counter()-t
    if old:
        assert n==old['graph']['n']
        assert set(es)==set(map(tuple,old['graph']['edges']))
    t=time.perf_counter()
    diagonal=[F((13*i)%19-9 or 1,17) for i in range(n)]
    edge_values={(u,v):F((7*u+11*v)%23-11 or 1,19) for u,v in es}
    noise=[[F((7*(i+3)*(j+5))%17-8,1009) for j in range(4)] for i in range(n)]
    input_time=time.perf_counter()-t
    t=time.perf_counter();Z=action(n,4,colors,diagonal,edge_values)
    Y=[[a+b for a,b in zip(r,e)] for r,e in zip(Z,noise)]
    action_time=time.perf_counter()-t
    t=time.perf_counter();dn,en=decode(plan,Z);assert dn==diagonal and en==edge_values
    noiseless_time=time.perf_counter()-t
    t=time.perf_counter();dh,eh=decode(plan,Y);decode_time=time.perf_counter()-t
    t=time.perf_counter()
    errd=[a-b for a,b in zip(dh,diagonal)]
    erre={k:eh[k]-v for k,v in edge_values.items()}
    error_sq=matrix_frobenius_sq(errd,erre);noise_sq=norm_sq(noise)
    assert error_sq<=2*noise_sq
    assert action(n,4,colors,dh,eh)==projection(plan,Y)
    row=[abs(v) for v in errd]
    for (u,v),x in erre.items():row[u]+=abs(x);row[v]+=abs(x)
    check_time=time.perf_counter()-t
    result={'name':name,'input_spec':spec,'graph':g,'certificate':cert,
        'noise_model':'arbitrary absolute Frobenius noise; saved actual instance rational',
        'input_matrix':pack_matrix(diagonal,edge_values),'noise':pack_action(noise),
        'full_observed_action':pack_action(Y),'output_matrix':pack_matrix(dh,eh),
        'noiseless_exact':True,'projected_action_residual':'0',
        'noise_frobenius_sq':str(noise_sq),'error_frobenius_sq':str(error_sq),
        'actual_error_absolute_row_sum_upper':str(max(row)),
        'maximum_bichromatic_component':max(map(lambda c:len(c['order']),plan['components']),default=1),
        'times_seconds':{'graph_and_coloring_including_certificate_load':construction,
            'actual_star_and_decoder_preparation':prepare_time,'matrix_noise_creation':input_time,
            'full_four_actions_and_noise':action_time,'noiseless_decode_check':noiseless_time,
            'noisy_decode':decode_time,'exact_error_projection_check':check_time}}
    if old:
        t=time.perf_counter()
        w=old['witness']
        wd=[F(0)]*n;we={(u,v):F(x) for u,v,x in w['nonzero_matrix_edges']}
        W=action(n,4,colors,wd,we);whd,whe=decode(plan,W)
        assert whd==wd and all(whe[e]==we.get(e,F(0)) for e in es)
        result['inherited_witness_receiving']={
            'same_original_labeled_support':True,
            'matrix':pack_matrix(wd,we),'new_four_query_action':pack_action(W),
            'new_action_frobenius_sq':str(norm_sq(W)),
            'new_noiseless_reconstruction_exact':True,
            'old_three_query_action_frobenius_sq_as_received':w['action_frobenius_sq'],
            'old_design_inverse_lower_sq_as_received':w['operator_inverse_lower_sq'],
            'new_design_uniform_operator_inverse_upper_sq':2,
            'comparison_scope':'One additional query; this repairs the specified bad design on the same support, not a universal three-query lower or application-speed comparison.',
            'wall_seconds':time.perf_counter()-t}
    return result

def main():
    t=time.perf_counter();cpu=time.process_time()
    out=BASE/'results'
    # Native exact predecessor record copied before this execution, not regenerated.
    p=BASE/'sources/cycle6_selected/failed_even_series_rotation.json'
    raw=p.read_bytes();old=json.loads(raw)
    source={'filename':p.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    specs=[('star_three_obstruction_17',obstruction_spec(),None),
           ('arbitrary_paths_and_both_parities',mixed_spec(),None),
           ('same_saved_Q8_support',old['spec'],old)]
    summaries=[]
    for name,spec,previous in specs:
        r=receiving(name,spec,previous)
        if previous:r['inherited_input_identity']=source
        target=out/(name+'.json');target.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
        summaries.append({'name':name,'n':r['graph']['n'],'m':len(r['graph']['edges']),
             'class_counts':r['graph']['class_application_counts'],
             'K':r['maximum_bichromatic_component'],'constant_sq':2,
             'noise_sq':r['noise_frobenius_sq'],'error_sq':r['error_frobenius_sq'],
             'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    cost={'wall_seconds_including_serialization':time.perf_counter()-t,
          'cpu_seconds':time.process_time()-cpu,
          'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
          'scope':'All three actual receiving runs, saved input reading, original four actions, negative-family receiving and result serialization. Separate certificate discovery/checks and inference/authoring excluded.',
          'receiving_uses':summaries}
    (out/'RECEIVING_COSTS.json').write_text(json.dumps(cost,indent=2)+'\n')
    print(json.dumps(cost,indent=2))
if __name__=='__main__':main()

