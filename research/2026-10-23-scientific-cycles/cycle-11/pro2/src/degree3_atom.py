"""One ACTUAL degree-three atom root with a genuinely missing neighbor color.

The exact original n/edge list is returned. A temporary subdivision is only
a way to reuse the accepted protected-edge normalizer, never an action input.
Callers supply the already loaded fixed certificate bundle for reuse.
"""
from collections import Counter
from pathlib import Path
import hashlib,json
from marked_atom import prepare_marked_atom
from loaded_recovery import prepare_certificate,classify
from hazard_ports import canonical,transform,PERMS
from project_degree3 import project,EXPECTED

class Degree3AtomOracle:
    def __init__(self,certificate_path,projection_path=None):
        raw=Path(certificate_path).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise ValueError('wrong fixed H8 certificate')
        self.cert,self.table,self.indices=prepare_certificate(certificate_path)
        self._projection(projection_path)

    @classmethod
    def from_prepared(cls,verified_marked_bundle,projection_path=None):
        """Reuse the accepted Cycle10 MarkedAtomOracle's already hash-bound table.

        The caller must supply that verified bundle, not arbitrary user data.
        No certificate reload, reindexing, or inherited closure is performed.
        """
        obj=cls.__new__(cls)
        obj.cert,obj.table,obj.indices=(verified_marked_bundle.cert,
            verified_marked_bundle.table,verified_marked_bundle.indices)
        obj._projection(projection_path)
        return obj

    def _projection(self,projection_path):
        if projection_path is None:
            self.rows={r['family']:r for r in project(self.cert)}
        else:
            projection=json.loads(Path(projection_path).read_text())
            if projection['source_sha256']!=EXPECTED:raise ValueError('unbound new projection')
            self.rows={r['family']:r for r in projection['rows']}
            # Check the NEW projection, not the old closure.
            if list(self.rows.values())!=project(self.cert):raise ValueError('projection differs from exact fixed-target calculation')

    def color(self,n,edges,mark,neighbor=None):
        if type(n) is not int or n<4 or type(mark) is not int or not 0<=mark<n:raise ValueError('native root')
        es=[]
        for e in edges:
            if len(e)!=2 or any(type(v) is not int for v in e):raise ValueError('integer original edge')
            u,v=sorted(e)
            if not 0<=u<v<n:raise ValueError('simple original edge')
            es.append((u,v))
        es.sort()
        if len(es)!=len(set(es)):raise ValueError('duplicate original edge')
        adj=[[] for _ in range(n)]
        for u,v in es:adj[u].append(v);adj[v].append(u)
        if len(adj[mark])!=3 or any(not 2<=len(ns)<=4 for ns in adj):raise ValueError('actual root degree three, atom degrees 2..4 required')
        if neighbor is None:neighbor=min(adj[mark])
        if neighbor not in adj[mark]:raise ValueError('specified edge not original')
        order=[mark,neighbor]+[v for v in range(n) if v not in (mark,neighbor)]
        local={v:i for i,v in enumerate(order)}
        local_original=sorted(tuple(sorted((local[u],local[v]))) for u,v in es)
        assert (0,1) in local_original
        local_h=[e for e in local_original if e!=(0,1)]
        subdivided=sorted(local_h+[(0,n),(1,n)])
        # The old routine's deleted mark is this temporary subdivision vertex.
        form=prepare_marked_atom(n+1,subdivided,n)
        if form['ports']!=[0,1] or sorted(form['h_edges'])!=local_h:raise ValueError('protected-edge normalization changed original H')
        labels,ds=classify(form,self.cert,self.table);root=form['root'];family=labels[root]
        if ds[root][0]!=2 or not 1<=ds[root][1]<=3:raise ValueError('actual deleted-edge loads')
        row=self.rows[family];target_index=row['target_index'];target=tuple(self.cert['families'][family]['targets'][target_index])
        if list(target)!=row['inherited_target'] or list(ds[root])!=row['degree']:raise ValueError('new target binding')
        colors=[None]*n;stack=[(root,target)]
        def assign(v,c):
            if c<0:return
            if not 0<=v<n:raise ValueError('temporary vertex escaped into actual coloring')
            if colors[v] is not None and colors[v]!=c:raise ValueError('inconsistent original color')
            colors[v]=c
        while stack:
            i,st=stack.pop();node=form['nodes'][i];s,t=node['terminals'];assign(s,st[0]);assign(t,st[1])
            can=canonical(st);ti=self.indices[labels[i]][can];perm=next(p for p in PERMS if transform(can,p)==st)
            kind=node['kind']
            if kind=='path':
                w=self.cert['leaf']['witnesses'][ti]
                if w['target']!=ti:raise ValueError('leaf witness order')
                a,c,b=[perm[x] for x in w['colors']];assign(s,a);assign(node['middle'],c);assign(t,b);continue
            children=node['children'];order_children=list(range(len(children)))
            if kind=='P':order_children.sort(key=lambda j:(labels[children[j]],j))
            transition=self.table[kind,tuple(labels[children[j]] for j in order_children)];w=transition['witnesses'][ti]
            if w['target']!=ti:raise ValueError('transition witness order')
            assigned=[None]*len(children)
            for j,sig in zip(order_children,w['child_signatures']):assigned[j]=transform(tuple(sig),perm)
            if kind=='L':assign(s,perm[w['new_color']])
            elif kind=='R':assign(t,perm[w['new_color']])
            stack.extend((children[j],assigned[j]) for j in reversed(range(len(children))))
        actual=[None]*n
        for i,v in enumerate(order):actual[v]=colors[i]
        profile=check_degree3_coloring(n,es,mark,actual)
        if row['missing_color'] not in profile['missing_neighbor_colors']:raise ValueError('promised actual missing channel absent')
        return dict(schema='astra-native-degree3-star-root/v1',n=n,edges=es,mark=mark,
            protected_original_edge=[mark,neighbor],colors=actual,q=4,profile=profile,
            root_family=family,root_target_index=target_index,root_target=list(target),
            native_vertex_order=order,temporary_normal_form=form,
            preparation_note='The extra subdivision vertex is a normalizer-only symbol; returned colors/support and all downstream actions use exactly the original n vertices and edges.')

def check_degree3_coloring(n,edges,mark,colors):
    if len(colors)!=n or any(type(c) is not int or c not in range(4) for c in colors):raise ValueError('unresolved actual colors')
    adj=[[] for _ in range(n)]
    for u,v in edges:
        if colors[u]==colors[v]:raise ValueError('not proper')
        adj[u].append(v);adj[v].append(u)
    mult=[Counter(colors[v] for v in ns) for ns in adj]
    for u,v in edges:
        if mult[u][colors[v]]>=2 and mult[v][colors[u]]>=2:raise ValueError('bichromatic P4')
    if len(adj[mark])!=3:raise ValueError('root load changed')
    neighbors=sorted(mult[mark]);missing=sorted(set(range(4))-{colors[mark]}-set(neighbors))
    if not missing:raise ValueError('no actual missing neighbor color')
    flags=sorted({colors[v] for v in adj[mark] if mult[v][colors[mark]]>=2})
    return dict(color=colors[mark],degree=3,neighbor_colors=neighbors,
        neighbor_color_multiplicities=[mult[mark].get(c,0) for c in range(4)],
        far_flags=flags,missing_neighbor_colors=missing,
        unflagged_neighbor_colors=sorted(set(neighbors)-set(flags)))
