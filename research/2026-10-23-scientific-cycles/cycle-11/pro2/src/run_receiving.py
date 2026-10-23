"""New Cycle11 original-action receivers; no inherited scientific suite replay."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,time,resource,traceback
from marked_atom import prepare_marked_certificate
from degree3_atom import Degree3AtomOracle
from bridge_recovery import prepare_recovery
from coordinate_decoder import action,decode,norm_sq,matrix_frobenius_sq

ROOT=Path(__file__).resolve().parents[1]

def jsonify(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):jsonify(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [jsonify(v) for v in x]
    return x

def coefficients(diag,ev):
    return dict(diagonal=list(map(str,diag)),edges=[dict(edge=list(e),value=str(w)) for e,w in sorted(ev.items())])

def receive(obj,bundle,d3):
    wall,cpu=time.perf_counter(),time.process_time()
    n=obj['n'];es=sorted(tuple(sorted(e)) for e in obj['edges'])
    p=time.perf_counter();form,design,plan=prepare_recovery(n,es,bundle,d3)
    prep=time.perf_counter()-p;cs=design['colors'];q=4
    diag=[F((37*i+11)%31-15,13) for i in range(n)]
    ev={(u,v):F((23*u+17*v+5)%43-21,17) for u,v in es}
    noise=[[F((11*i+7*j+3)%19-9,101) for j in range(q)] for i in range(n)]
    p=time.perf_counter();dx=action(n,q,cs,diag,ev);acquisition=time.perf_counter()-p
    y=[[a+b for a,b in zip(row,erow)] for row,erow in zip(dx,noise)]
    p=time.perf_counter();d0,w0=decode(plan,dx);noiseless_time=time.perf_counter()-p
    assert d0==diag and w0==ev
    p=time.perf_counter();dh,wh=decode(plan,y);noisy_time=time.perf_counter()-p
    projected=action(n,q,cs,dh,wh)
    residual=[[a-b for a,b in zip(row,pr)] for row,pr in zip(y,projected)]
    assert all(residual[i][cs[i]]==0 for i in range(n))
    assert all(residual[u][cs[v]]+residual[v][cs[u]]==0 for u,v in es)
    f2=matrix_frobenius_sq([a-b for a,b in zip(dh,diag)],{e:wh[e]-ev[e] for e in es})
    e2=norm_sq(noise)
    assert f2<=18*e2
    assert f2<=F(design['guarantee']['finite_frobenius_constant_sq'])*e2
    entry_degrees=[m['certificate']['entry_qualification']['actual_degree']
        for m in design['modules'] if m['certificate']['entry_qualification'] is not None]
    summary=dict(modules=len(form['modules']),nontrivial_modules=sum(bool(m['edges']) for m in form['modules']),
        bridges=len(form['bridges']),quotient_depth=max(form['depth']),
        maximum_degree=form['maximum_degree'],entry_degrees=entry_degrees,
        entry_vertex_bridge_resets=sum(r['entry_vertex_reset'] for r in design['bridges']),
        atom_count=sum(len(m['certificate']['blocks']) for m in design['modules']),
        internal_stop_messages=sum(len(m['certificate']['messages']) for m in design['modules']),
        degree3_families=[r['atom_certificate']['root_family'] for m in design['modules']
                         for r in m['certificate']['blocks'] if r['actual_degree']==3])
    return jsonify(dict(name=obj['name'],n=n,m=len(es),q=q,summary=summary,design=design,
        original_coefficients=coefficients(diag,ev),noise=noise,full_noiseless_actions=dx,
        observations=y,output=coefficients(dh,wh),projected_actions=projected,
        raw_residual=residual,raw_residual_norm_sq=norm_sq(residual),
        projected_numerical_residual_norm_sq='0',normal_equations_pass=True,
        exact_noiseless_reconstruction=True,noise_frobenius_sq=e2,
        error_frobenius_sq=f2,ratio_frobenius_sq=f2/e2,
        largest_component_vertices=max((len(c['order']) for c in plan['components']),default=1),
        actual_cut_gamma=plan['kappa2'],
        timing=dict(native_preparation_seconds=prep,explicit_original_action_seconds=acquisition,
            noiseless_decode_seconds=noiseless_time,noisy_decode_seconds=noisy_time,
            body_wall_seconds_before_serialization=time.perf_counter()-wall,
            body_cpu_seconds_before_serialization=time.process_time()-cpu)))

def main():
    wall,cpu=time.perf_counter(),time.process_time();stage='fixed_bundle'
    try:
        p=time.perf_counter()
        bundle=prepare_marked_certificate(ROOT/'sources/loaded_star_certificate.json',ROOT/'sources/marked_root_projection.json')
        fixed=time.perf_counter()-p;p=time.perf_counter()
        d3=Degree3AtomOracle.from_prepared(bundle,ROOT/'sources/DEGREE3_PROJECTION.json')
        projection=time.perf_counter()-p
        result=dict(schema='astra-cycle11-original-actions/v1',status='PASS',operations=[],input_bindings=[],
            shared_fixed_certificate_seconds=fixed,new_projection_reuse_seconds=projection,
            source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').glob('*.py'))})
        for filename in ['mixed_native_bridge_entries.json','triangle_bridge_chain_9.json']:
            stage=filename;raw=(ROOT/'inputs'/filename).read_bytes();obj=json.loads(raw)
            result['input_bindings'].append(dict(path='inputs/'+filename,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
            result['operations'].append(receive(obj,bundle,d3))
        # The new bridge-forest entry point claims isolated/disconnected supports.
        # This is an implementation branch check, not a new forest theorem.
        stage='isolated_direct_sum';p=time.perf_counter()
        f,d,plan=prepare_recovery(3,[],bundle,d3)
        y=[[F(i+j+1,7) for j in range(4)] for i in range(3)]
        dd,ww=decode(plan,y)
        assert dd==[r[0] for r in y] and ww=={} and len(f['roots'])==3
        result['isolated_direct_sum_check']=dict(n=3,edges=[],colors=d['colors'],observations=jsonify(y),
            recovered_diagonal=list(map(str,dd)),status='PASS',wall_seconds=time.perf_counter()-p)
        result['body_wall_seconds_before_serialization']=time.perf_counter()-wall
        result['body_cpu_seconds_before_serialization']=time.process_time()-cpu
        result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
        result['cost_scope']='Includes shared table/projection, both new native receivers, both noiseless and noisy decodes, exact action checks, and isolated branch. Excludes interpreter startup, final JSON serialization, discovery/inference, authoring, independent review and delivery.'
        p=time.perf_counter();(ROOT/'results/RECEIVING.json').write_text(json.dumps(result,indent=2)+'\n')
        serial=time.perf_counter()-p
        receipt=dict(status='PASS',body_wall_seconds=result['body_wall_seconds_before_serialization'],
            body_cpu_seconds=result['body_cpu_seconds_before_serialization'],result_serialization_seconds=serial,
            peak_rss_bytes=result['peak_rss_bytes'],operations=[{k:r[k] for k in ['name','n','m','q','summary','largest_component_vertices','actual_cut_gamma','ratio_frobenius_sq','timing']} for r in result['operations']])
        (ROOT/'results/RECEIVING_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt,indent=2))
    except BaseException:
        failed=dict(status='FAILED',stage=stage,traceback=traceback.format_exc(),
            wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
            peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024)
        name='FAILED_RECEIVING_'+str(time.time_ns())+'.json'
        (ROOT/'results'/name).write_text(json.dumps(failed,indent=2)+'\n')
        raise

if __name__=='__main__':main()
