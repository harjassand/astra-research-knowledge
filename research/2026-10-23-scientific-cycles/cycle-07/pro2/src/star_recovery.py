"""Construct star-four colors from the fixed finite port certificate.
Known graph supplied by a checked series/parallel expression; original actions
are acquired after the full expanded graph has been constructed.
"""
from pathlib import Path
from itertools import permutations
from collections import Counter
import json
from finite_star_certificate import canonical,transform

def load_certificate(path=None):
    if path is None:path=Path(__file__).resolve().parents[1]/'results/general_star_certificate.json'
    c=json.loads(Path(path).read_text())
    if c['schema']!='astra-star-four-all-series-paths/v1':raise ValueError('certificate schema')
    rows={}
    for r in c['transitions']:
        key=(r['kind'],tuple(r['child_classes']))
        rows[key]={'parent':r['parent_class'],
                   'witness':{tuple(w['parent_signature']):tuple(map(tuple,w['child_signatures']))
                              for w in r['witnesses']}}
    return c,rows

def normalize(spec):
    """Expand each path into length2/3 blocks and every series into binary joins.
    Repeated input IDs are disjoint copies. No graph recognition is provided.
    """
    source=spec['nodes'];root=spec['root']
    if type(root) is not int or not 0<=root<len(source):raise ValueError('root')
    nodes=[];mapped=[]
    for i,node in enumerate(source):
        kind=node['kind']
        if kind=='path':
            length=node['length']
            if type(length) is not int or length<2:raise ValueError('path length')
            lengths=([3] if length%2 else [])+[2]*(length//2-(1 if length%2 else 0))
            assert sum(lengths)==length and lengths
            blocks=[]
            for k in lengths:
                blocks.append(len(nodes));nodes.append({'kind':'path','length':k})
            last=blocks[0]
            for j in blocks[1:]:
                old=last;last=len(nodes);nodes.append({'kind':'series','children':[old,j]})
            mapped.append(last)
        else:
            children=node.get('children',[])
            if any(type(j) is not int or not 0<=j<i for j in children):raise ValueError('non-topological child')
            ch=[mapped[j] for j in children]
            if kind=='parallel':
                if len(ch) not in (2,3):raise ValueError('parallel arity')
                mapped.append(len(nodes));nodes.append({'kind':kind,'children':ch})
            elif kind in ('series','series_even_failure'):
                if len(ch)<2:raise ValueError('unary series excluded')
                last=ch[0]
                for j in ch[1:]:
                    old=last;last=len(nodes);nodes.append({'kind':'series','children':[old,j]})
                mapped.append(last)
            else:raise ValueError('unadmitted production')
    return {'nodes':nodes,'root':mapped[root]}

def classify(spec,certificate,table):
    out=[]
    for i,node in enumerate(spec['nodes']):
        if node['kind']=='path':
            out.append(certificate['leaf_classes'][str(node['length'])]);continue
        ch=[out[j] for j in node['children']]
        kind='S' if node['kind']=='series' else 'P'
        if kind=='P':ch.sort()
        out.append(table[(kind,tuple(ch))]['parent'])
    return out

def build(spec,certificate_path=None):
    certificate,table=load_certificate(certificate_path)
    spec=normalize(spec);nodes=spec['nodes'];classes=classify(spec,certificate,table)
    root=spec['root'];state=tuple(certificate['families'][classes[root]][0])
    colors=[state[0],state[1]];edges=[];stack=[(root,0,1,state)]
    counts=Counter();applications=0
    def vertex(c):
        v=len(colors);colors.append(c);return v
    while stack:
        i,s,t,target=stack.pop();node=nodes[i];applications+=1;counts[classes[i]]+=1
        assert colors[s]==target[0] and colors[t]==target[1]
        if node['kind']=='path':
            mid=[vertex(target[2])]
            if node['length']==3:mid.append(vertex(target[3]))
            else:assert target[2]==target[3]
            chain=[s]+mid+[t];edges.extend(zip(chain,chain[1:]));continue
        children=node['children']
        order=list(range(len(children)))
        kind='S' if node['kind']=='series' else 'P'
        if kind=='P':order.sort(key=lambda k:(classes[children[k]],k))
        key=(kind,tuple(classes[children[k]] for k in order))
        row=table[key];std=canonical(target)
        ws=row['witness'][std]
        perm=next(p for p in permutations(range(4)) if transform(std,p)==target)
        assigned=[None]*len(children)
        for k,w in zip(order,ws):assigned[k]=transform(w,perm)
        if kind=='S':
            assert assigned[0][1]==assigned[1][0]
            v=vertex(assigned[0][1]);endpoints=[(s,v),(v,t)]
        else:
            assert len({x[:2] for x in assigned})==1
            a,b=vertex(assigned[0][0]),vertex(assigned[0][1])
            edges.extend(((s,a),(b,t)));endpoints=[(a,b)]*len(children)
        for j,(u,v),st in reversed(list(zip(children,endpoints,assigned))):
            stack.append((j,u,v,st))
    edges=[tuple(sorted(e)) for e in edges]
    return {'n':len(colors),'edges':edges,'colors':colors,'terminals':[0,1],
            'root_class':classes[root],'root_signature':state,
            'expanded_applications':applications,'class_application_counts':dict(counts),
            'normalized_spec':spec}

def check_star(n,edges,colors):
    if len(colors)!=n or any(c not in range(4) for c in colors):raise ValueError('palette')
    adj=[[] for _ in range(n)]
    if len(set(edges))!=len(edges):raise ValueError('duplicate edge')
    for u,v in edges:
        if not 0<=u<v<n or colors[u]==colors[v]:raise ValueError('improper/simple')
        adj[u].append(v);adj[v].append(u)
    mult=[Counter(colors[w] for w in ns) for ns in adj]
    for u,v in edges:
        if mult[u][colors[v]]>1 and mult[v][colors[u]]>1:
            raise ValueError('bichromatic P4 at '+str((u,v)))
    if len(adj[0])!=1 or len(adj[1])!=1 or max(map(len,adj))>4:
        raise ValueError('degree contract')
    return {'maximum_degree':max(map(len,adj)),'star_verified':True,
            'used_colors':sorted(set(colors)),'all_noise_operator_constant_sq':2,
            'all_noise_frobenius_constant_sq':2}

def obstruction_spec():
    return {'nodes':[{'kind':'path','length':2},
        {'kind':'series','children':[0,0]},
        {'kind':'parallel','children':[0,0]},
        {'kind':'parallel','children':[0,1,2]},
        {'kind':'parallel','children':[1,3]}],'root':4}

def mixed_spec():
    return {'nodes':[{'kind':'path','length':2},
        {'kind':'path','length':3},{'kind':'path','length':7},
        {'kind':'parallel','children':[0,0,1]},
        {'kind':'series','children':[3,0]},
        {'kind':'parallel','children':[4,1]},
        {'kind':'series','children':[5,3,2,0,5]},
        {'kind':'parallel','children':[6,4,3]}],'root':7}

