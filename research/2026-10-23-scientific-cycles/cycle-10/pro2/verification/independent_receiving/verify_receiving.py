#!/usr/bin/env python3
"""Independent exact receiving gate. Standard library only; no producer imports.

This checks the three saved new operations and the actual block reset. It does
not rerun an old certificate closure or perform a new scientific experiment.
Small-component Fraction normal equations deliberately differ from subtree LS.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import resource
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bound_file(path):
    data = path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)), bytes=len(data), sha256=sha(data))


def edges_of(raw):
    result = [tuple(sorted(e)) for e in raw]
    assert all(len(e) == 2 and all(type(v) is int for v in e) for e in result)
    assert len(result) == len(set(result))
    return sorted(result)


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        assert u != v and u in adj and v in adj
        adj[u].add(v); adj[v].add(u)
    return adj


def connected_parts(vertices, adj):
    unseen = set(vertices); result = []
    while unseen:
        seed = min(unseen); unseen.remove(seed)
        comp = {seed}; walk = [seed]
        for u in walk:
            new = adj[u] & unseen
            unseen.difference_update(new); comp.update(new); walk.extend(sorted(new))
        result.append(comp)
    return result


def blocks_by_vertex_deletion(vertices, edges):
    """Independent small-input decomposition, not producer's low-link walk."""
    adj = adjacency(vertices, edges)
    assert len(connected_parts(vertices, adj)) == 1
    for removed in sorted(vertices):
        pieces = connected_parts(set(vertices)-{removed}, adj)
        if len(pieces) > 1:
            blocks = []
            for part in pieces:
                vs = part | {removed}
                es = [e for e in edges if e[0] in vs and e[1] in vs]
                blocks.extend(blocks_by_vertex_deletion(vs, es))
            return blocks
    assert len(vertices) >= 3 and len(edges) >= 3, 'bridge/isolated vertex outside new native operation'
    return [sorted(edges)]


def support_certificate(n, edges):
    assert type(n) is int and n >= 3
    assert all(0 <= u < v < n for u,v in edges)
    adj = adjacency(range(n), edges)
    assert all(2 <= len(ns) <= 4 for ns in adj.values())
    blocks = sorted(blocks_by_vertex_deletion(set(range(n)), edges), key=lambda b:b[0])
    assert sorted(e for b in blocks for e in b) == edges
    vs = [sorted({v for e in b for v in e}) for b in blocks]
    bas = [adjacency(v,b) for v,b in zip(vs,blocks)]
    membership = [[i for i,v in enumerate(vs) if u in v] for u in range(n)]
    assert all(1 <= len(ids) <= 2 for ids in membership)
    tree = [[] for _ in blocks]; shared = {}
    for u, ids in enumerate(membership):
        if len(ids) == 2:
            a,b = ids
            assert len(bas[a][u]) == len(bas[b][u]) == 2
            tree[a].append(b); tree[b].append(a); shared[tuple(sorted(ids))] = u
    assert len(shared) == len(blocks)-1
    parent = [-1]*len(blocks); depth = [-1]*len(blocks)
    depth[0]=0; order=[0]
    for i in order:
        for j in sorted(tree[i]):
            if j == parent[i]: continue
            assert depth[j] == -1
            parent[j]=i; depth[j]=depth[i]+1; order.append(j)
    assert len(order)==len(blocks)

    # A successful elimination with at most two later neighbors is an explicit
    # width-two certificate. Fill is only used in this check, never in actions.
    fill = {u:set(ns) for u,ns in adj.items()}; bags=[]
    while fill:
        eligible=[u for u,ns in fill.items() if len(ns)<=2]
        assert eligible, 'no width-two certificate found'
        u=min(eligible); ns=sorted(fill[u]); bags.append([u,*ns])
        if len(ns)==2:
            a,b=ns; fill[a].add(b); fill[b].add(a)
        for v in ns: fill[v].remove(u)
        del fill[u]

    # Every original cycle is contained in a block. Complete enumeration here
    # is finite and tiny; it verifies native chordlessness without producer labels.
    cycle_counts=[]
    for vertices, ba in zip(vs,bas):
        cycles=[]
        for start in vertices:
            def visit(path, seen):
                for w in sorted(ba[path[-1]]):
                    if w==start and len(path)>=3 and path[1]<path[-1]:
                        cycles.append(tuple(path)); continue
                    if w>start and w not in seen:
                        visit(path+[w],seen|{w})
            visit([start],{start})
        assert len(cycles)==len(set(cycles))
        for cyc in cycles:
            length=len(cyc)
            for i in range(length):
                for j in range(i+1,length):
                    if j==i+1 or (i==0 and j==length-1): continue
                    assert cyc[j] not in ba[cyc[i]], 'original chord found'
        cycle_counts.append(len(cycles))
    return dict(n=n,edges=edges,adj=adj,blocks=blocks,vertices=vs,block_adj=bas,
                membership=membership,parent=parent,depth=depth,shared=shared,
                cycle_counts=cycle_counts,width2_bags=bags,
                max_degree=max(map(len,adj.values())))


def color_components(vertices, edges, colors):
    groups=defaultdict(list)
    for e in edges:
        u,v=e; assert colors[u] != colors[v]
        groups[tuple(sorted((colors[u],colors[v])))].append(e)
    comps=[]
    for pair,es in sorted(groups.items()):
        verts={v for e in es for v in e}; adj=adjacency(verts,es)
        for members in connected_parts(verts,adj):
            ce=[e for e in es if e[0] in members]
            assert len(ce)==len(members)-1, 'bichromatic cycle'
            ca=adjacency(members,ce)
            comps.append(dict(pair=pair,vertices=sorted(members),edges=ce,adj=ca))
    return comps


def profile(adj, colors, r):
    n={colors[v] for v in adj[r]}
    flags={colors[v] for v in adj[r]
           if any(w != r and colors[w] == colors[r] for w in adj[v])}
    return dict(color=colors[r],neighbors=sorted(n),flags=sorted(flags))


def verify_star(vertices, edges, colors):
    for comp in color_components(vertices,edges,colors):
        degrees=[len(comp['adj'][v]) for v in comp['vertices']]
        assert sum(d>1 for d in degrees) <= 1, 'local component is not a star'


def expression_support(nf, local_edges):
    assert edges_of(nf['original_edges'])==local_edges
    mark=nf['mark']; adj=adjacency(range(nf['n']),local_edges)
    ports=sorted(adj[mark]); assert ports==sorted(nf['ports']) and len(ports)==2
    if nf['triangle']:
        assert nf['n']==3 and len(local_edges)==3 and not nf['nodes']
        return
    built=[]; vertex_sets=[]
    for idx,node in enumerate(nf['nodes']):
        a,b=node['terminals']; kind=node['kind']; children=node.get('children',[])
        assert a!=b and all(type(j)is int and 0<=j<idx for j in children)
        if kind=='path':
            assert node['length']==2 and not children
            m=node['middle']; assert m not in (a,b)
            es={tuple(sorted((a,m))),tuple(sorted((m,b)))}
        elif kind in ('L','R'):
            assert len(children)==1
            j=children[0]; x,y=nf['nodes'][j]['terminals']; es=set(built[j])
            if kind=='L':
                assert y==b and a not in vertex_sets[j]
                es.add(tuple(sorted((a,x))))
            else:
                assert x==a and b not in vertex_sets[j]
                es.add(tuple(sorted((y,b))))
        elif kind in ('S','P'):
            assert len(children)==2
            j,k=children; x,y=nf['nodes'][j]['terminals']; z,w=nf['nodes'][k]['terminals']
            if kind=='S':
                assert x==a and w==b and y==z
                assert vertex_sets[j]&vertex_sets[k]=={y}
            else:
                assert (x,y)==(a,b)==(z,w)
                assert vertex_sets[j]&vertex_sets[k]=={a,b}
            assert not built[j]&built[k]
            es=built[j]|built[k]
        else:
            raise AssertionError(('unhandled exact native expression node',kind))
        built.append(es); vertex_sets.append({v for e in es for v in e})
    expected={e for e in local_edges if mark not in e}
    assert built[nf['root']]==expected==set(edges_of(nf['h_edges']))
    assert mark not in vertex_sets[nf['root']]


def verify_block_records(form, design):
    colors=design['colors']; records=design['blocks']; count=len(form['blocks'])
    assert len(records)==count and {r['block'] for r in records}==set(range(count))
    by_id={r['block']:r for r in records}; blocked={}; messages=[]; processed=set()
    for rec in records:
        i=rec['block']; be=form['blocks'][i]; vertices=form['vertices'][i]; ba=form['block_adj'][i]
        p=form['parent'][i]
        assert rec['parent']==p and rec['vertex_ids']==vertices
        if p>=0:
            assert p in processed
            mark=form['shared'][tuple(sorted((i,p)))]
            assert rec['actual_mark']==mark
        else:
            mark=rec['actual_mark']; assert mark in vertices and len(ba[mark])==2
        loc={v:j for j,v in enumerate(vertices)}
        local_edges=sorted(tuple(sorted((loc[u],loc[v]))) for u,v in be)
        ans=rec['atom_certificate']
        assert ans['n']==len(vertices) and ans['q']==4
        assert edges_of(ans['edges'])==local_edges
        assert ans['mark']==rec['local_mark']==loc[mark]
        raw=ans['colors']; assert len(raw)==len(vertices) and all(type(c)is int and 0<=c<4 for c in raw)
        raw_global={v:raw[loc[v]] for v in vertices}
        raw_prof=profile(ba,raw_global,mark)
        assert len(raw_prof['neighbors'])==2 and len(raw_prof['flags'])<=1
        verify_star(vertices,be,raw_global)
        ap=ans['profile']
        assert ap['color']==raw_prof['color'] and ap['degree']==2
        assert ap['neighbor_colors']==ans['root_neighbors']==raw_prof['neighbors']
        assert ap['far_flags']==ans['root_flags']==raw_prof['flags']
        mult=[sum(raw_global[u]==c for u in ba[mark]) for c in range(4)]
        assert ap['neighbor_color_multiplicities']==mult
        expression_support(ans['native_normal_form'],local_edges)
        perm=rec['permutation']; assert sorted(perm)==list(range(4))
        actual={v:perm[raw_global[v]] for v in vertices}
        assert rec['colors']==[actual[v] for v in vertices]
        assert all(actual[v]==colors[v] for v in vertices)
        prof=profile(ba,actual,mark); assert rec['root_profile']==prof
        verify_star(vertices,be,actual)
        if p>=0:
            P=profile(form['block_adj'][p],colors,mark)['neighbors']
            assert rec['parent_neighbor_colors']==P and 1<=len(P)<=2
            forced=blocked.get(mark); assert rec['forbidden_incoming_color']==forced
            if forced is not None:
                assert forced in P and forced not in prof['neighbors']
            common=sorted(set(P)&set(prof['neighbors']))
            assert len(common)<=1 and not set(common)&set(prof['flags'])
            # Check saved deterministic choice without re-running the atom constructor.
            valid=[]
            for trial in itertools.permutations(range(4)):
                if trial[raw_prof['color']] != colors[mark]:continue
                ns={trial[x] for x in raw_prof['neighbors']}; fs={trial[x] for x in raw_prof['flags']}
                com=set(P)&ns
                if len(com)<=1 and not com&fs and (forced is None or forced not in ns):valid.append(trial)
            assert tuple(perm)==min(valid)
        else:
            assert rec['parent_neighbor_colors']==[] and rec['forbidden_incoming_color'] is None
            assert perm==list(range(4)); common=[]
        assert rec['shared_channel']==common
        outgoing=None
        if common:
            neighbors=[u for u in ba[mark] if colors[u]==common[0]]; assert len(neighbors)==1
            u=neighbors[0]
            assert sum(colors[v]==colors[mark] for v in ba[u])==1
            downstream=[j for j in form['membership'][u] if form['parent'][j]==i]
            assert len(downstream)<=1
            if downstream:
                assert u not in blocked
                blocked[u]=colors[mark]
                outgoing=dict(vertex=u,forbidden=colors[mark],child=downstream[0],incoming_edge=[mark,u])
                messages.append(outgoing)
        assert rec['outgoing_stop_message']==outgoing
        processed.add(i)
    assert design['messages']==[dict(vertex=v,forbidden=c) for v,c in sorted(blocked.items())]
    return dict(local_blocks=count,actual_rooted_star_colorings=count,
                actual_stop_messages=messages,
                native_support_expressions_checked=count)


def verify_spiders(comps, witnesses):
    indexed={ (tuple(c['pair']),tuple(c['vertices'])):c for c in comps }
    assert len(witnesses)==len(comps); seen=set()
    gamma=F(0)
    for w in witnesses:
        center=w['center']; arms=w['arms']; verts={center}; described=set()
        for arm in arms:
            assert 1<=len(arm)<=2 and not verts.intersection(arm)
            assert len(arm)==len(set(arm)); verts.update(arm)
            chain=[center,*arm]
            described.update(tuple(sorted((u,v))) for u,v in zip(chain,chain[1:]))
        key=(tuple(w['pair']),tuple(sorted(verts)))
        assert key in indexed and key not in seen;seen.add(key)
        comp=indexed[key]; assert described==set(comp['edges'])
        if 'vertices' in w:assert w['vertices']==len(verts)
        for u,v in comp['edges']:
            walk=[u]; reached={u}
            for x in walk:
                for y in comp['adj'][x]:
                    if {x,y}=={u,v} or y in reached:continue
                    reached.add(y);walk.append(y)
            a=len(reached);b=len(verts)-a;assert a>0 and b>0
            gamma=max(gamma,F(a*b,a+b))
    assert len(seen)==len(comps)
    return gamma


def rational_matrix(raw,n,q):
    assert len(raw)==n and all(len(row)==q for row in raw)
    return [[F(x) for x in row] for row in raw]


def coefficients(raw,n,edges):
    d=[F(x) for x in raw['diagonal']];assert len(d)==n
    ev={tuple(x['edge']):F(x['value']) for x in raw['edges']}
    assert len(ev)==len(raw['edges'])==len(edges) and sorted(ev)==edges
    return d,ev


def act(n,q,colors,d,ev):
    out=[[F(0) for _ in range(q)] for _ in range(n)]
    for v in range(n):out[v][colors[v]]+=d[v]
    for (u,v),w in ev.items():out[u][colors[v]]+=w;out[v][colors[u]]+=w
    return out


def solve(a,b):
    """Fraction Gauss-Jordan elimination on SPD edge Gram matrix."""
    n=len(b);rows=[[F(x) for x in row]+[F(v)] for row,v in zip(a,b)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if rows[i][k])
        rows[k],rows[pivot]=rows[pivot],rows[k]
        div=rows[k][k];rows[k]=[x/div for x in rows[k]]
        for i in range(n):
            if i==k:continue
            scale=rows[i][k]
            if scale:rows[i]=[x-scale*y for x,y in zip(rows[i],rows[k])]
    assert all(rows[i][j]==int(i==j) for i in range(n) for j in range(n))
    return [row[-1] for row in rows]


def normal_equations(n,colors,comps,Y):
    diag=[Y[i][colors[i]] for i in range(n)];values={};maxdim=0
    for c in comps:
        es=c['edges'];maxdim=max(maxdim,len(es))
        gram=[[len(set(e)&set(f)) for f in es] for e in es]
        rhs=[Y[u][colors[v]]+Y[v][colors[u]] for u,v in es]
        w=solve(gram,rhs)
        values.update(zip(es,w))
    return diag,values,maxdim


def f2(matrix):return sum((x*x for row in matrix for x in row),F(0))


def check_operation(op,obj,form):
    n=obj['n'];edges=form['edges'];q=op['q'];assert q==4
    assert op['n']==n and op['m']==len(edges)
    design=op['design'];colors=design['colors']
    assert design['q']==4 and len(colors)==n and all(type(c)is int and 0<=c<q for c in colors)
    comps=color_components(range(n),edges,colors)
    witnesses=design['components'] if op['mode']=='block_reset' else design['spiders']
    gamma=verify_spiders(comps,witnesses)
    assert F(op['actual_cut_gamma'])==gamma
    assert op['largest_component_vertices']==max(len(c['vertices']) for c in comps)
    if op['mode']=='block_reset':
        block_report=verify_block_records(form,design)
        assert op['summary']['stop_messages']==len(block_report['actual_stop_messages'])
        assert op['summary']['depth']==max(form['depth'])
    else:
        assert op['mode']=='theta_explicit'
        block_report={'scope':'Alternative actual coloring and receiving verified; its separate construction proof is not re-executed.'}
    assert op['summary']['blocks']==len(form['blocks'])
    assert op['summary']['maximum_degree']==form['max_degree']
    assert design['guarantee']['operator_constant_sq']=='3+sqrt(5)'
    assert design['guarantee']['frobenius_constant_sq']=='3+sqrt(5)'
    d,ev=coefficients(op['original_coefficients'],n,edges)
    assert d==[F((37*i+11)%31-15,13) for i in range(n)]
    assert ev=={(u,v):F((23*u+17*v+5)%43-21,17) for u,v in edges}
    E=rational_matrix(op['noise'],n,q)
    assert E==[[F((11*i+7*j+3)%19-9,101) for j in range(q)] for i in range(n)]
    DX=act(n,q,colors,d,ev)
    assert DX==rational_matrix(op['full_noiseless_actions'],n,q)
    Y=[[a+b for a,b in zip(x,e)] for x,e in zip(DX,E)]
    assert Y==rational_matrix(op['observations'],n,q)
    d0,v0,maxdim=normal_equations(n,colors,comps,DX)
    assert d0==d and v0==ev
    dh,vh,_=normal_equations(n,colors,comps,Y)
    assert (dh,vh)==coefficients(op['output'],n,edges)
    projected=act(n,q,colors,dh,vh)
    assert projected==rational_matrix(op['projected_actions'],n,q)
    residual=[[a-b for a,b in zip(y,p)] for y,p in zip(Y,projected)]
    assert residual==rational_matrix(op['raw_residual'],n,q)
    assert all(residual[i][colors[i]]==0 for i in range(n))
    assert all(residual[u][colors[v]]+residual[v][colors[u]]==0 for u,v in edges)
    assert F(op['raw_residual_norm_sq'])==f2(residual)
    error=sum(((a-b)**2 for a,b in zip(dh,d)),F(0))+2*sum(((vh[e]-ev[e])**2 for e in edges),F(0))
    noise=f2(E);assert noise>0
    ratio=error/noise;assert ratio<=3 or (ratio-3)**2<=5
    assert F(op['error_frobenius_sq'])==error and F(op['noise_frobenius_sq'])==noise
    assert F(op['ratio'])==ratio
    assert op['exact_noiseless_reconstruction'] is True
    assert op['normal_equations_pass'] is True
    assert F(op['projected_numerical_residual_norm_sq'])==0
    return dict(input=op['input'],mode=op['mode'],status='PASS',n=n,m=len(edges),q=q,
                exact_original_action_columns_checked=q,
                exact_projected_action_columns_checked=q,
                bichromatic_components=len(comps),largest_component=max(len(c['vertices']) for c in comps),
                largest_independent_Gram_order=maxdim,
                original_coefficients=n+len(edges),cut_gamma=str(gamma),
                original_noise_norm_sq=str(noise),error_frobenius_sq=str(error),ratio=str(ratio),
                raw_residual_norm_sq=str(f2(residual)),projected_numerical_residual_norm_sq='0',
                block_records=block_report)


def main():
    wall,cpu=time.perf_counter(),time.process_time()
    stage='read_and_bind'
    try:
        data_path=ROOT/'results/RECEIVING.json';data=json.loads(data_path.read_text())
        assert data['schema']=='astra-cycle10-original-actions/v1'
        assert len(data['inputs'])==2 and len(data['operations'])==3
        bindings=[bound_file(data_path),bound_file(ROOT/'PROOF.md'),bound_file(Path(__file__))]
        for name,h in data['source_hashes'].items():
            item=bound_file(ROOT/'src'/name);assert item['sha256']==h;bindings.append(item)
        objects={};forms={};supports=[]
        for record in data['inputs']:
            p=ROOT/record['path'];binding=bound_file(p);assert binding==record;bindings.append(binding)
            obj=json.loads(p.read_text());edges=edges_of(obj['edges'])
            stage='native_support:'+record['path']
            form=support_certificate(obj['n'],edges)
            objects[record['path']]=obj;forms[record['path']]=form
            supports.append(dict(input=record['path'],vertices=obj['n'],edges=len(edges),
                                 blocks=len(form['blocks']),maximum_degree=form['max_degree'],
                                 all_original_cycles_chordless=True,
                                 cycle_counts_by_block=form['cycle_counts'],
                                 width_two_fill_bags=form['width2_bags']))
        reports=[]
        for op in data['operations']:
            stage='operation:'+op['input']+':'+op['mode']
            reports.append(check_operation(op,objects[op['input']],forms[op['input']]))
        a,b=data['operations'][:2]
        assert a['input']==b['input'] and a['original_coefficients']==b['original_coefficients'] and a['noise']==b['noise']
        assert data['same_theta_D_and_absolute_noise'] is True
        mixed=[r for r in reports if r['n']==30]
        assert len(mixed)==1 and mixed[0]['block_records']['actual_stop_messages']==[
            dict(vertex=11,forbidden=3,child=5,incoming_edge=[6,11])]
        report=dict(status='PASS',schema='astra-cycle10-independent-receiving/v1',
                    scope='No-producer-import exact verification of the three NEW saved full-original-action operations; not an old suite replay, historical-priority result, application benchmark, or proof of unrestricted class coverage.',
                    independent_methods=['Vertex-deletion block decomposition',
                        'Original-cycle enumeration for chordlessness on these small native blocks',
                        'Successful width-two fill-elimination witness',
                        'Actual raw/permuted rooted profiles and one-message records',
                        'Independent expression support expansion',
                        'Fraction edge-Gram normal equations, not subtree sums'],
                    source_bindings=bindings,support_checks=supports,operations=reports,
                    paired_theta_D_and_noise_identical=True,
                    saved_message_actually_exercised=True,
                    nonlinear_or_spectral_optimization_used=False,
                    claims_not_checked=['Historical priority/external acceptance',
                        'All old atom table transitions (accepted dependency, not rerun)',
                        'Scientific performance on another application',
                        'Complete chordlessness recognition on every possible rejected/accepted input'],
                    reviewed_scope_correction='Theorem A/native operation should specify at least one edge; isolated K1 has trivial recovery outside n>=3 entrypoint. Root accepted this wording correction; receiver unchanged.')
        out=HERE/'VERDICT.json';out.write_text(json.dumps(report,indent=2)+'\n')
        # Timer includes loading, all checks, and complete scientific-report serialization.
        cost=dict(status='PASS',wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
                  peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                  includes_scientific_report_serialization=True,
                  excludes='This final cost-receipt serialization, source reading, authoring, inference, review drafting and integration.',
                  verdict_bytes=out.stat().st_size,verdict_sha256=sha(out.read_bytes()),
                  source_sha256=sha(Path(__file__).read_bytes()),python=sys.version)
        (HERE/'COSTS.json').write_text(json.dumps(cost,indent=2)+'\n')
        print(json.dumps(dict(status='PASS',operations=len(reports),cost=cost),indent=2))
    except Exception:
        failure=dict(status='FAIL',stage=stage,traceback=traceback.format_exc(),
                     wall_seconds=time.perf_counter()-wall,cpu_seconds=time.process_time()-cpu,
                     peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                     source_sha256=sha(Path(__file__).read_bytes()))
        (HERE/'FAILED_ATTEMPT.json').write_text(json.dumps(failure,indent=2)+'\n')
        raise


if __name__=='__main__':main()
