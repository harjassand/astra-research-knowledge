"""Emit explicit finite witnesses, so checking needs no search or optimizer."""
from pathlib import Path
import itertools,json,time,resource,hashlib
from hazard_ports import *

def make(source):
    d=json.loads(Path(source).read_text());assert d['reason']=='closed'
    rows=[d['records'][i] for i in d['basis_ids']]
    families=[dict(id=i,degree=r['degree'],targets=r['states'],discovery_id=r['id']) for i,r in enumerate(rows)]
    sets=[frozenset(map(tuple,r['states'])) for r in rows]
    deg=[tuple(r['degree']) for r in rows]
    def choose(st,ds):
        return min((i for i in range(len(rows)) if deg[i]==ds and covers(st,sets[i])),key=lambda i:(len(sets[i]),i))
    leafid=choose(path2(),(1,1));leafw=[]
    for j,t in enumerate(families[leafid]['targets']):
        t=tuple(t)
        for a,c,b in itertools.product(range(4),repeat=3):
            if c in (a,b):continue
            s=(a,b,1,1<<c,(1<<c) if a==b else 0,1,1<<c,(1<<c) if a==b else 0)
            if below(s,t):leafw.append(dict(target=j,colors=[a,c,b]));break
        else:raise AssertionError('leaf target')
    cases=[]
    for i,ds in enumerate(deg):
        for k in ('L','R'):
            if admissible(k,ds):cases.append((k,i))
        for j,es in enumerate(deg):
            if admissible('S',ds,es):cases.append(('S',i,j))
            if i<=j and admissible('P',ds,es):cases.append(('P',i,j))
    transitions=[]
    for key in cases:
        k=key[0];i=key[1];j=key[2] if len(key)==3 else None
        outputs=apply(k,sets[i],None if j is None else sets[j],with_witness=True)
        ds=output_degree(k,deg[i],None if j is None else deg[j]);parent=choose(frozenset(outputs),ds)
        ws=[]
        for ti,t0 in enumerate(families[parent]['targets']):
            t=tuple(t0);u=covering_witness(frozenset(outputs),t);uc=canonical(u)
            p=next(p for p in PERMS if transform(uc,p)==u)
            children=outputs[uc]
            if k in ('L','R'):
                ws.append(dict(target=ti,child_signatures=[serialize(transform(children[0],p))],new_color=p[children[1]]))
            else:ws.append(dict(target=ti,child_signatures=[serialize(transform(ch,p)) for ch in children]))
        transitions.append(dict(kind=k,children=list(key[1:]),parent=parent,witnesses=ws))
    return dict(schema='astra-loaded-star-four/v1',palette=4,state_format=['a','b','left_degree','left_neighbor_color_mask','left_far_flag_mask','right_degree','right_neighbor_color_mask','right_far_flag_mask'],
        semantics='exact visible terminal colors and degrees; realized neighbor-color supports and far flags are subsets of target masks; SAT4 is existential unprescribed color -1 and masks0',
        grammar=dict(leaf='path2',operations=['L','R','S','P'],positive_terminal_load=True,max_degree=4,nonadjacent_terminals=True,disjoint_child_occurrences=True),
        families=families,leaf=dict(family=leafid,witnesses=leafw),transitions=transitions,
        source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest())

if __name__=='__main__':
    start=time.perf_counter();cpu=time.process_time();root=Path(__file__).resolve().parents[1]
    cert=make(root/'results/hazard_closure.json');p=root/'results/loaded_star_certificate.json'
    p.write_text(json.dumps(cert,separators=(',',':'))+'\n')
    receipt=dict(families=len(cert['families']),profiles=sum(len(f['targets']) for f in cert['families']),cases=len(cert['transitions']),
        witnesses=sum(len(r['witnesses']) for r in cert['transitions']),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        body_wall_seconds=time.perf_counter()-start,body_cpu_seconds=time.process_time()-cpu,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        scope='certificate construction including input read and final certificate serialization, excludes startup and receipt write')
    (root/'results/CERTIFICATE_COSTS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
