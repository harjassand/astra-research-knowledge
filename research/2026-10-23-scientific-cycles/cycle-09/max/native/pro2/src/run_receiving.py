"""New original-action receiving operations, exact rational input and output.
This is a diagnostic of the operation, not an application runtime benchmark.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time,resource,hashlib,importlib.util
from loaded_recovery import build,check_original_graph,mixed_spec
from coordinate_decoder import prepare,decode,action,matrix_frobenius_sq,norm_sq

ROOT=Path(__file__).resolve().parents[1]

def rational_psd(A):
    """Exact symmetric Schur complements; pivots are the saved PSD witness."""
    A=[r[:] for r in A];pivots=[];n=len(A)
    for k in range(n):
        p=A[k][k];pivots.append(p)
        if p<0:raise ArithmeticError('negative exact PSD pivot')
        if p==0:
            if any(A[i][k] for i in range(k+1,n)):raise ArithmeticError('zero PSD pivot with nonzero column')
            continue
        for i in range(k+1,n):
            for j in range(i,n):
                A[i][j]-=A[i][k]*A[j][k]/p;A[j][i]=A[i][j]
    return pivots

def receiving(name,graph_source,q):
    t0=time.perf_counter();cpu=time.process_time();stages={}
    t=time.perf_counter();g=graph_source();stages['graph_color_construction']=time.perf_counter()-t
    n=g['n'];es=[tuple(e) for e in g['edges']];cs=g['colors']
    t=time.perf_counter();check=check_original_graph(g);plan=prepare(n,es,cs,q)
    stages['actual_graph_and_decoder_preparation']=time.perf_counter()-t
    t=time.perf_counter()
    diag=[F(((17*i+5)%23)-11 or 13,31) for i in range(n)]
    edges={(u,v):F(((13*u+7*v+3)%19)-9 or 10,37) for u,v in es}
    E=[[F(((5*i+3*c+1)%13)-6,101) for c in range(q)] for i in range(n)]
    stages['matrix_and_noise_input']=time.perf_counter()-t
    t=time.perf_counter();DX=action(n,q,cs,diag,edges)
    Y=[[DX[i][c]+E[i][c] for c in range(q)] for i in range(n)]
    stages['all_original_actions_and_noise']=time.perf_counter()-t
    t=time.perf_counter();d0,e0=decode(plan,DX);assert (d0,e0)==(diag,edges)
    stages['noiseless_decode_and_equality']=time.perf_counter()-t
    t=time.perf_counter();dh,eh=decode(plan,Y)
    stages['noisy_decode']=time.perf_counter()-t
    t=time.perf_counter();actual=action(n,q,cs,dh,eh)
    projected=[[F(0) for _ in range(q)] for _ in range(n)]
    for i in range(n):projected[i][cs[i]]=Y[i][cs[i]]
    for comp in plan['components']:
        a,b=comp['pair'];vs=comp['order'];sgn={v:1 if cs[v]==a else -1 for v in vs}
        mean=sum((sgn[v]*Y[v][b if cs[v]==a else a] for v in vs),F(0))/len(vs)
        for v in vs:
            col=b if cs[v]==a else a;projected[v][col]=Y[v][col]-sgn[v]*mean
    assert actual==projected
    dd=[dh[i]-diag[i] for i in range(n)];de={e:eh[e]-edges[e] for e in es}
    noise2=norm_sq(E);errorF2=matrix_frobenius_sq(dd,de);assert errorF2<=2*noise2
    stages['exact_projection_and_frobenius_check']=time.perf_counter()-t
    t=time.perf_counter();B=[[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):B[i][i]=dd[i]
    for (u,v),val in de.items():B[u][v]=B[v][u]=val
    C=[[(F(3,2)*noise2 if i==j else F(0))-sum((B[i][k]*B[k][j] for k in range(n)),F(0)) for j in range(n)] for i in range(n)]
    pivots=rational_psd(C);stages['additional_dense_exact_operator_check']=time.perf_counter()-t
    rec=dict(schema='astra-loaded-star-full-action-receiving/v1',name=name,graph=g,query_count=q,
        graph_check=check,actual_design=dict(type='coordinate',colors=cs,row_energy_sq=1),
        matrix=dict(diagonal=list(map(str,diag)),edges=[[u,v,str(edges[u,v])] for u,v in es]),
        noise=[[str(v) for v in r] for r in E],full_action=[[str(v) for v in r] for r in DX],
        observed_action=[[str(v) for v in r] for r in Y],output=dict(diagonal=list(map(str,dh)),edges=[[u,v,str(eh[u,v])] for u,v in es]),
        projected_action=[[str(v) for v in r] for r in projected],
        exact_checks=dict(noiseless_equality=True,projected_action_residual_sq='0',noise_norm_sq=str(noise2),
            error_frobenius_sq=str(errorF2),frobenius_constant_sq='2',operator_constant_sq='3/2',
            operator_psd_matrix='(3/2)*||E||F^2*I - (Dhat-D)^2',operator_psd_pivots=list(map(str,pivots))),
        stage_wall_seconds=stages)
    p=ROOT/'results'/f'{name}.json';p.write_text(json.dumps(rec,indent=2)+'\n')
    cost=dict(name=name,body_wall_seconds=time.perf_counter()-t0,body_cpu_seconds=time.process_time()-cpu,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        stage_wall_seconds=stages,record_bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        scope='all stages and receiving record serialization; excludes startup and final cost receipt')
    return cost

def main():
    start=time.perf_counter();cpu=time.process_time()
    # The selected length crosses the proven period boundary; no size sweep.
    spec=importlib.util.spec_from_file_location('a_l_control',ROOT/'research/structural_scope/a_l_three_control.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    def control():
        g=mod.atom(5);g['edges']=sorted(map(tuple,g['edges']));g['terminal_degrees']=[4,3];g['terminals']=[0,1];g['length']=5;return g
    def mixed():
        s=mixed_spec();g=build(s);g['original_spec']=s;return g
    rows=[receiving('A5_three_action_control',control,3),receiving('mixed_loaded_16_four_action',mixed,4)]
    result=dict(operations=rows,total_body_wall_seconds=time.perf_counter()-start,total_body_cpu_seconds=time.process_time()-cpu,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        includes_additional_dense_operator_diagnostics=True,application_speedup_claim=False)
    (ROOT/'results/RECEIVING_COSTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
