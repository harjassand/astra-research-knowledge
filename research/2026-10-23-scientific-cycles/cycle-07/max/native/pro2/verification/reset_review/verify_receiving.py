#!/usr/bin/env python3
"""Independent exact check of the three saved Cycle6 scientific receiving records.

No producer module is imported. Producer source was read for the input schema;
this is independent implementation, not a claimed blind review. Graph semantics
are reimplemented recursively; products, projection and certificates use Fraction.
"""
from collections import deque
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import resource
import sys
import time


def need(test, message):
    if not test:
        raise AssertionError(message)


def parse_matrix(data, n, q):
    need(len(data)==n and all(len(r)==q for r in data),'matrix dimensions')
    return [list(map(F,r)) for r in data]


def norm_sq(a):
    return sum((x*x for row in a for x in row),F(0))


def exact_action(n,colors,diagonal,weights):
    result=[[F(0) for _ in range(3)] for _ in range(n)]
    for v,w in enumerate(diagonal):result[v][colors[v]]=w
    for (u,v),w in weights.items():
        result[u][colors[v]]+=w
        result[v][colors[u]]+=w
    return result


def semantic_binding(spec, saved, allow_even):
    """Reconstruct the specified labeled graph without the producer builder.

    The saved labeling allocates root terminals first, each node's own join
    vertices next, and child copies in declared order. A recursive emitter
    implements this deterministic semantics; repeated node IDs create copies.
    """
    nodes=spec['nodes'];root=spec['root']
    need(type(root) is int and 0<=root<len(nodes),'root index')
    for i,node in enumerate(nodes):
        kind=node['kind']
        if kind=='path':
            need(type(node['length']) is int and node['length']>=2,'leaf length')
        else:
            children=node['children']
            need(all(type(j) is int and 0<=j<i for j in children),'topological children')
            if kind=='parallel':need(2<=len(children)<=3,'parallel arity')
            elif kind=='series':need(len(children)>=3 and len(children)%2==1,'odd series arity')
            elif kind=='series_even_failure':need(allow_even and len(children)==2,'negative-only rule')
            else:need(False,'unrecognized production')
    colors=[0,1];edges=[];applications=0;depth_seen=0
    def fresh(c):
        result=len(colors);colors.append(c);return result
    def emit(k,s,t,a,b,depth):
        nonlocal applications,depth_seen
        applications+=1;depth_seen=max(depth_seen,depth)
        need((colors[s],colors[t])==(a,b) and a!=b,'terminal color assignment')
        c=3-a-b;node=nodes[k];kind=node['kind']
        if kind=='path':
            length=node['length']
            if length==2:word=[a,c,b]
            elif length==3:word=[a,c,a,b]
            else:
                canonical=[i%3 for i in range(length-1)]
                canonical.append(min(set(range(3))-{canonical[-1],1}))
                canonical.append(1)
                perm={0:a,1:b,2:c}
                word=[perm[x] for x in canonical]
            vertices=[s]+[fresh(x) for x in word[1:-1]]+[t]
            edges.extend(tuple(sorted(e)) for e in zip(vertices,vertices[1:]))
        elif kind=='parallel':
            u,z=fresh(b),fresh(c)
            edges.extend((tuple(sorted((s,u))),tuple(sorted((z,t)))))
            for child in node['children']:emit(child,u,z,b,c,depth+1)
        else:
            ch=node['children']
            sequence=([a,c,b] if kind=='series_even_failure'
                      else [a if i%2==0 else b for i in range(len(ch)+1)])
            ends=[s]+[fresh(x) for x in sequence[1:-1]]+[t]
            for j,child in enumerate(ch):
                emit(child,ends[j],ends[j+1],sequence[j],sequence[j+1],depth+1)
    emit(root,0,1,0,1,0)
    need(colors==saved['colors'],'saved colors differ from expression semantics')
    need(len(colors)==saved['n'],'saved n differs from expression')
    need(edges==list(map(tuple,saved['edges'])),'saved labeled edges differ from expression semantics')
    need(saved['terminals']==[0,1],'root terminal labels')
    need(applications==saved['applications'],'application count')
    return {'applications':applications,'expression_depth':depth_seen,
            'labeled_graph_and_color_binding':'PASS'}


def analyze_graph(g):
    n=g['n'];cs=g['colors'];es=[tuple(e) for e in g['edges']]
    need(type(n) is int and n>=1 and len(cs)==n,'graph order')
    need(all(type(c) is int and c in range(3) for c in cs),'three-color alphabet')
    need(len(es)==len(set(es)),'simple graph duplicate edges')
    adj=[set() for _ in range(n)]
    for u,v in es:
        need(type(u) is int and type(v) is int and 0<=u<v<n,'canonical edge')
        need(cs[u]!=cs[v],'proper coloring')
        adj[u].add(v);adj[v].add(u)
    degree=max(map(len,adj));need(degree==g['maximum_degree'] and degree<=4,'degree cap')
    s,t=g['terminals'];need(s!=t and len(adj[s])==len(adj[t])==1,'terminal degree')
    need((cs[s],cs[t])==(0,1),'terminal ordered colors')
    seen={s};queue=[s]
    for v in queue:
        for u in adj[v]:
            if u not in seen:seen.add(u);queue.append(u)
    need(len(seen)==n,'connected input graph')
    blocks=[];membership={};K=1;row_mass=[0]*n
    gamma=F(0);M=0;frob_constant=F(1);incoming=[0]*n
    for pair in combinations(range(3),2):
        todo={v for v in range(n) if cs[v] in pair}
        while todo:
            root=min(todo);todo.remove(root);vertices=[root];parent={root:None}
            for v in vertices:
                for u in sorted(adj[v]):
                    if cs[u] in pair and u not in parent:
                        parent[u]=v;vertices.append(u);todo.remove(u)
            vs=set(vertices)
            local_edges=[(u,v) for u in vertices for v in adj[u] if u<v and v in vs]
            need(len(local_edges)==len(vertices)-1,'bichromatic cycle')
            need(not {s,t}<=vs,'terminal transmission')
            N=len(vertices);K=max(K,N)
            for v in vertices:row_mass[v]+=N-1
            block={'pair':pair,'vertices':vertices,'edges':local_edges,'parent':parent}
            blocks.append(block)
            for v in vertices:membership[pair,v]=block
            sizes={v:1 for v in vertices}
            for v in reversed(vertices[1:]):sizes[parent[v]]+=sizes[v]
            cuts=[]
            for v in vertices[1:]:
                a=sizes[v];cuts.append(F(a*(N-a),N));M=max(M,min(a,N-a))
            if cuts:
                gamma=max(gamma,max(cuts));frob_constant=max(frob_constant,2*sum(cuts,F(0)))
            # Choose an independently defined centroid (smallest vertex label).
            candidates=[]
            for v in vertices:
                branches=[N-sizes[v]] if parent[v] is not None else []
                branches += [sizes[u] for u in adj[v] if u in parent and parent[u]==v]
                if max(branches,default=0)*2<=N:candidates.append(v)
            need(candidates,'tree centroid exists')
            center=min(candidates);oriented={center};order=[center]
            for v in order:
                for u in adj[v]:
                    if u in vs and u not in oriented:
                        oriented.add(u);order.append(u);incoming[u]+=1
    r=max((len({cs[u] for u in adj[v]}) for v in range(n)),default=0)
    r0=max(incoming,default=0);row_constant=F(1+max(row_mass,default=0))
    cut_constant=F(1+4*r0*M)
    boundary=[len(membership[p,v]['vertices']) for v,p in
              ((s,(0,1)),(s,(0,2)),(t,(0,1)),(t,(1,2)))]
    return dict(n=n,edges=es,colors=cs,adj=adj,blocks=blocks,membership=membership,
                profile={'K':K,'boundary':boundary},degree=degree,r=r,r0=r0,
                gamma=gamma,M=M,row_constant=row_constant,cut_constant=cut_constant,
                frob_constant=frob_constant)


def projected_action(y, info):
    n,cs=info['n'],info['colors']
    p=[[F(0) for _ in range(3)] for _ in range(n)]
    for v in range(n):p[v][cs[v]]=y[v][cs[v]]
    for block in info['blocks']:
        a,b=block['pair'];vs=block['vertices']
        f={v:(1 if cs[v]==a else -1)*y[v][b if cs[v]==a else a] for v in vs}
        mean=sum(f.values(),F(0))/len(vs)
        for v in vs:
            sig=1 if cs[v]==a else -1
            p[v][b if cs[v]==a else a]=sig*(f[v]-mean)
    return p


def check_positive(d):
    binding=semantic_binding(d['spec'],d['graph'],False)
    info=analyze_graph(d['graph']);n=info['n'];es=info['edges'];cs=info['colors']
    need(info['profile']==d['actual_profile'],'actual profile')
    symbolic=d['all_symbolic_profiles'][d['spec']['root']]
    need(symbolic['boundary']==info['profile']['boundary'] and symbolic['K']==info['profile']['K'],
         'saved symbolic root profile')
    need((symbolic['n'],symbolic['m'])==(n,len(es)),'symbolic root graph sizes')
    need(symbolic['applications']==binding['applications'] and symbolic['depth']==binding['expression_depth'],
         'symbolic root construction counts')
    cap=d['uniform_component_cap'];need(info['profile']['K']<=cap,'uniform K on input')
    need(d['uniform_operator_constant_sq']==2*cap-1,'uniform row-noise constant')
    cert=d['certificate']
    for key,value in [('n',n),('edges',len(es)),('q',3),('maximum_degree',info['degree']),
                      ('neighbour_color_count',info['r']),('maximum_component_size',info['profile']['K']),
                      ('centroid_branch_maximum',info['M'])]:need(cert[key]==value,'certificate '+key)
    need(F(cert['gamma'])==info['gamma'],'cut gamma')
    need(cert['maximum_incoming']>=info['r0'],'valid independently realized column multiplicity')
    need(F(cert['cut_operator_constant_sq'])>=info['cut_constant'],'cut operator upper')
    best=min(info['row_constant'],info['cut_constant'],info['frob_constant'])
    need(F(cert['best_supplied_operator_constant_sq'])==best,'strongest independently recomputed supplied bound')
    need(best==info['row_constant'],'claimed winning row certificate on saved input')
    e4=d['adjacent_degree_four_vertices']
    need(tuple(sorted(e4)) in set(es) and all(len(info['adj'][v])==4 for v in e4),'adjacent degree-four witness')
    mi=d['matrix_input'];ni=d['noise_input']
    need(len(mi['diagonal_numerators'])==n and len(mi['edge_numerators_in_graph_order'])==len(es),'matrix coefficient count')
    need(mi['diagonal_denominator']>0 and mi['edge_denominator']>0 and ni['denominator']>0,'positive exact denominators')
    diagonal=[F(x,mi['diagonal_denominator']) for x in mi['diagonal_numerators']]
    weights={e:F(x,mi['edge_denominator']) for e,x in zip(es,mi['edge_numerators_in_graph_order'])}
    need(len(ni['numerators'])==n and all(len(row)==3 for row in ni['numerators']),'noise shape')
    noise=[[F(x,ni['denominator']) for x in row] for row in ni['numerators']]
    noiseless=exact_action(n,cs,diagonal,weights)
    y=[[x+e for x,e in zip(a,b)] for a,b in zip(noiseless,noise)]
    need(y==parse_matrix(d['observed_full_actions'],n,3),'full exact DX+E')
    need(projected_action(noiseless,info)==noiseless,'noiseless action is exactly in signal range')
    recovered=d['recovered']
    need(len(recovered['diagonal'])==n and len(recovered['edge_values_in_graph_order'])==len(es),'recovered coefficient counts')
    rd=list(map(F,recovered['diagonal']));rw=dict(zip(es,map(F,recovered['edge_values_in_graph_order'])))
    ry=exact_action(n,cs,rd,rw);py=projected_action(y,info)
    need(ry==py,'recovered projected-action residual is zero')
    ed=[x-z for x,z in zip(rd,diagonal)];ew={e:rw[e]-weights[e] for e in es}
    rows=list(map(abs,ed))
    for (u,v),w in ew.items():rows[u]+=abs(w);rows[v]+=abs(w)
    noise2=norm_sq(noise);error2=sum((x*x for x in ed),F(0))+2*sum((x*x for x in ew.values()),F(0))
    infinity=max(rows);vf=d['verification']
    need(F(vf['noise_frobenius_sq'])==noise2,'noise Frobenius norm')
    need(F(vf['actual_error_frobenius_sq'])==error2,'error Frobenius norm')
    need(F(vf['actual_error_infinity_upper'])==infinity,'actual error maximum absolute row sum')
    need(F(vf['projected_action_residual_sq'])==0,'saved exact residual')
    need(F(vf['certified_operator_error_sq'])==best*noise2,'certified operator budget')
    need(infinity**2<=best*noise2,'actual error within certified budget')
    return {'status':'PASS',**binding,'n':n,'m':len(es),'degree':info['degree'],
            'profile':info['profile'],'gamma':str(info['gamma']),'M':info['M'],
            'operator_constant_sq':str(best),'row_certificate_for_all_noise':'PASS',
            'full_exact_action_and_noise':'PASS','unique_projected_action_solution':'PASS',
            'noise_frobenius_sq':str(noise2),'error_frobenius_sq':str(error2),
            'actual_error_row_sum':str(infinity),'projected_action_residual_sq':'0'}


def check_negative(d):
    binding=semantic_binding(d['spec'],d['graph'],True)
    info=analyze_graph(d['graph']);n=info['n'];es=set(info['edges']);cs=info['colors']
    need(info['profile']==d['actual_profile'],'negative graph profile')
    h=d['depth'];need(info['profile']['boundary'][0]==2**h,'exponential boundary recurrence')
    need(n==7*2**h-4 and len(es)==8*2**h-6 and info['degree']==3,'negative graph counts')
    sym=d['exact_symbolic_profile']
    need(sym['boundary']==info['profile']['boundary'] and sym['K']==info['profile']['K'],'negative symbolic profile')
    need((sym['n'],sym['m'],sym['applications'],sym['depth'])==
         (n,len(es),binding['applications'],binding['expression_depth']),'negative symbolic counts')
    w=d['witness'];weights={}
    for u,v,raw in w['nonzero_matrix_edges']:
        need((u,v) in es and (u,v) not in weights,'negative witness support')
        weights[u,v]=F(raw);need(weights[u,v]!=0,'claimed nonzero edge')
    action=exact_action(n,cs,[F(0)]*n,weights)
    sparse={(i,j):x for i,row in enumerate(action) for j,x in enumerate(row) if x}
    saved={}
    for i,j,raw in w['nonzero_action_cells']:
        need(type(i) is int and 0<=i<n and type(j) is int and 0<=j<3 and (i,j) not in saved,'sparse action coordinates')
        saved[i,j]=F(raw);need(saved[i,j]!=0,'claimed nonzero action')
    need(sparse==saved,'negative full DX equals saved sparse action')
    edge=tuple(w['edge']);need(edge in weights,'witness cut edge')
    need(weights[edge]==F(w['unit_edge_value']) and abs(weights[edge])==1,'absolute unit edge coefficient')
    block=info['membership'][(0,1),d['graph']['terminals'][0]]
    vs=set(block['vertices']);need(set(edge)<=vs,'cut belongs to claimed boundary tree')
    need(all(u in vs and v in vs for u,v in weights),'witness loaded only on boundary tree')
    reached={edge[0]};queue=[edge[0]]
    for v in queue:
        for u in info['adj'][v]:
            if u in vs and tuple(sorted((u,v)))!=edge and u not in reached:
                reached.add(u);queue.append(u)
    a,b=len(reached),len(vs)-len(reached)
    need(sorted((a,b))==sorted(w['cut_sides']),'independent cut sizes')
    need(a and b and len(vs)==2**h,'boundary cut order')
    signed=[]
    for side in (reached,vs-reached):
        loads={(1 if cs[v]==0 else -1)*action[v][1 if cs[v]==0 else 0] for v in side}
        need(len(loads)==1,'constant signed load on each cut side')
        z=loads.pop();need(abs(z)==F(1,len(side)),'exact reciprocal-size cut load');signed.append(z)
    need(signed[0]*signed[1]<0,'opposite signed cut loads')
    norm2=norm_sq(action);gamma=F(a*b,a+b)
    need(norm2==F(w['action_frobenius_sq'])==F(1,a)+F(1,b),'negative action norm')
    need(gamma==F(w['operator_inverse_lower_sq'])==1/norm2,'negative inverse lower')
    need(gamma==F(2**(2*h-2)-1,2**h),'explicit all-depth branch cut')
    return {'status':'PASS',**binding,'n':n,'m':len(es),'degree':info['degree'],
            'profile':info['profile'],'cut_sizes':sorted((a,b)),
            'absolute_cut_entry':'1','full_exact_witness_action':'PASS',
            'action_frobenius_sq':str(norm2),'inverse_lower_sq':str(gamma),
            'scope':'Specified coloring failure; no universal graph obstruction.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-directory',type=Path,
                        default=Path(__file__).resolve().parents[2]/'results')
    parser.add_argument('--output',type=Path,
                        default=Path(__file__).with_name('RECEIVING_RESULT.json'))
    args=parser.parse_args();wall,cpu=time.perf_counter(),time.process_time()
    rows=[]
    for name in ('base_paths_odd_series_and_forks','arbitrary_paths_odd_series_and_forks','failed_even_series_rotation'):
        path=args.input_directory/(name+'.json');raw=path.read_bytes();data=json.loads(raw)
        need(data['name']==name,'pinned case identity')
        checked=(check_negative(data) if name=='failed_even_series_rotation' else check_positive(data))
        rows.append({'filename':path.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),**checked})
    report={'status':'PASS','producer_imported':False,'producer_source_read_for_schema':True,
            'mathematical_arithmetic':'integer and fractions.Fraction only','cases':rows,
            'costs':{'body_wall_seconds':time.perf_counter()-wall,'body_cpu_seconds':time.process_time()-cpu,
                     'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
                     'input_reading_included':True,'output_serialization_included':False,
                     'scope':'Exact verification body; authoring, proof review, service and integration additional.'},
            'scope':'Source-bound fixed-input verification plus all-noise graph certificate; no novelty or application-speed claim.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
