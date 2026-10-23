"""Construct the original graph and four-action star seed from the finite proof.
No graph recognition or reduced-action oracle is provided or assumed.
"""
from pathlib import Path
from collections import Counter
import json
from hazard_ports import canonical,transform,PERMS,degrees,admissible,output_degree

def normalize(spec):
    src=spec['nodes'];root=spec['root']
    if type(root) is not int or not 0<=root<len(src):raise ValueError('root')
    out=[];mapping=[]
    for i,node in enumerate(src):
        k=node['kind']
        if k=='path':
            length=node['length']
            if type(length) is not int or length<2:raise ValueError('path length')
            v=len(out);out.append({'kind':'path','length':2})
            for _ in range(length-2):
                u=v;v=len(out);out.append({'kind':'L','children':[u]})
        else:
            ch=node['children']
            if any(type(j) is not int or not 0<=j<i for j in ch):raise ValueError('topology')
            ch=[mapping[j] for j in ch]
            if k in ('L','R'):
                if len(ch)!=1:raise ValueError('extension arity')
                v=len(out);out.append({'kind':k,'children':ch})
            elif k in ('S','P'):
                if len(ch)<2:raise ValueError('join arity')
                v=ch[0]
                for j in ch[1:]:
                    old=v;v=len(out);out.append({'kind':k,'children':[old,j]})
            else:raise ValueError('unadmitted production')
        mapping.append(v)
    return {'nodes':out,'root':mapping[root]}

def prepare_certificate(path=None):
    if path is None:path=Path(__file__).resolve().parents[1]/'results/loaded_star_certificate.json'
    c=json.loads(Path(path).read_text())
    if c['schema']!='astra-loaded-star-four/v1' or c['palette']!=4:raise ValueError('certificate schema')
    families=c['families'];table={}
    for row in c['transitions']:
        key=(row['kind'],tuple(row['children']))
        if key in table:raise ValueError('duplicate transition')
        table[key]=row
    indices=[{tuple(s):j for j,s in enumerate(f['targets'])} for f in families]
    return c,table,indices

def classify(spec,cert,table):
    labels=[];ds=[]
    for node in spec['nodes']:
        k=node['kind']
        if k=='path':labels.append(cert['leaf']['family']);ds.append((1,1));continue
        ch=node['children'];dd=ds[ch[0]];ee=ds[ch[1]] if len(ch)==2 else None
        if not admissible(k,dd,ee):raise ValueError('actual terminal degree exceeds four')
        cs=[labels[j] for j in ch]
        if k=='P':cs.sort()
        label=table[k,tuple(cs)]['parent'];d=output_degree(k,dd,ee)
        if tuple(cert['families'][label]['degree'])!=d:raise ValueError('certificate load mismatch')
        labels.append(label);ds.append(d)
    return labels,ds

def build(spec,certificate_path=None):
    cert,table,indices=prepare_certificate(certificate_path)
    spec=normalize(spec);labels,ds=classify(spec,cert,table);nodes=spec['nodes'];root=spec['root']
    target=tuple(cert['families'][labels[root]]['targets'][0])
    colors=[None,None];edges=[];stack=[(root,0,1,target)];counts=Counter();steps=0
    def color(v,c):
        if c<0:return
        if colors[v] is not None and colors[v]!=c:raise ValueError('inconsistent actual vertex color')
        colors[v]=c
    def new(c=None):
        v=len(colors);colors.append(c);return v
    while stack:
        i,s,t,st=stack.pop();steps+=1;label=labels[i];counts[label]+=1
        color(s,st[0]);color(t,st[1]);canon=canonical(st);ti=indices[label][canon]
        p=next(p for p in PERMS if transform(canon,p)==st)
        node=nodes[i];k=node['kind']
        if k=='path':
            w=cert['leaf']['witnesses'][ti]
            if w['target']!=ti:raise ValueError('leaf order')
            a,c,b=[p[x] for x in w['colors']];color(s,a);color(t,b)
            v=new(c);edges.extend(((s,v),(v,t)));continue
        children=node['children'];order=list(range(len(children)))
        if k=='P':order.sort(key=lambda j:(labels[children[j]],j))
        key=(k,tuple(labels[children[j]] for j in order));row=table[key]
        w=row['witnesses'][ti]
        if w['target']!=ti:raise ValueError('witness order')
        assigned=[None]*len(children)
        for j,ch in zip(order,w['child_signatures']):assigned[j]=transform(tuple(ch),p)
        if k=='S':
            if assigned[0][1]!=assigned[1][0] or assigned[0][1]<0:raise ValueError('series color')
            v=new(assigned[0][1]);ports=[(s,v),(v,t)]
        elif k=='P':ports=[(s,t)]*2
        elif k=='L':
            a=p[w['new_color']];color(s,a);v=new(assigned[0][0]);edges.append((s,v));ports=[(v,t)]
        else:
            b=p[w['new_color']];color(t,b);v=new(assigned[0][1]);edges.append((v,t));ports=[(s,v)]
        for j,(u,v),sig in reversed(list(zip(children,ports,assigned))):stack.append((j,u,v,sig))
    if any(c is None for c in colors):raise ValueError('unresolved saturated terminal color')
    edges=sorted(tuple(sorted(e)) for e in edges)
    return dict(n=len(colors),edges=edges,colors=colors,terminals=[0,1],root_family=labels[root],root_target=target,
                terminal_degrees=ds[root],expanded_occurrences=steps,family_occurrences=dict(counts),normalized_spec=spec)

def check_original_graph(g):
    n=g['n'];edges=g['edges'];cs=g['colors']
    if len(cs)!=n or any(type(c) is not int or c not in range(4) for c in cs):raise ValueError('actual color')
    if len(set(edges))!=len(edges):raise ValueError('duplicate edges')
    adj=[[] for _ in range(n)]
    for u,v in edges:
        if not 0<=u<v<n or cs[u]==cs[v]:raise ValueError('simple proper support')
        adj[u].append(v);adj[v].append(u)
    mult=[Counter(cs[v] for v in ns) for ns in adj]
    for u,v in edges:
        if mult[u][cs[v]]>=2 and mult[v][cs[u]]>=2:raise ValueError('actual bichromatic P4')
    if max(map(len,adj),default=0)>4:raise ValueError('degree cap')
    s,t=g.get('terminals',[0,1])
    if t in adj[s]:raise ValueError('adjacent ports')
    if [len(adj[s]),len(adj[t])]!=list(g['terminal_degrees']):raise ValueError('actual port loads')
    return dict(star=True,maximum_degree=max(map(len,adj)),actual_neighbor_color_multiplicities=[[m.get(c,0) for c in range(4)] for m in mult],
                all_noise_operator_constant_sq='3/2',all_noise_frobenius_constant_sq='2',row_energy_sq=1)

def mixed_spec():
    # New unequal-load operation: A4 atom with a port extension, joined at
    # load 1+3 to a theta(2,3,2), which contains an actual five-cycle.
    return {'nodes':[{'kind':'path','length':2},
        {'kind':'P','children':[0,0]},
        {'kind':'path','length':3},
        {'kind':'S','children':[1,2]},
        {'kind':'R','children':[1]},
        {'kind':'P','children':[3,4]},
        {'kind':'R','children':[5]},
        {'kind':'P','children':[0,2,0]},
        {'kind':'S','children':[6,7]}],'root':8}

def a_l_spec(length):
    return {'nodes':[{'kind':'path','length':2},{'kind':'path','length':length},
        {'kind':'P','children':[0,0]},{'kind':'S','children':[2,1]},
        {'kind':'P','children':[0,0,3]}],'root':4}
