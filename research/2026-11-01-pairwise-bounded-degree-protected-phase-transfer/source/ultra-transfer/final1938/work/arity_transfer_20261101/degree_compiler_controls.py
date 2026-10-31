"""Explicit bounded-degree port/subdivision/fork construction.

This builds the actual Pauli coupling and field list for a noncommuting
degree-15 star. Exact scalar counterterms are included. Its example
scales illustrate the construction; they are NOT Tanner phase parameters.
All-time qualification is the separate analytical transfer theorem.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/arity_transfer_20261101'


class Build:
    def __init__(self,old):
        self.old=old;self.next=old;self.records=[];self.fields=[]
    def mediator(self,stage,kind):
        q=self.next;self.next+=1
        gap=s.Integer(2)**(8+4*stage)
        loss=s.Integer(2)**(3+2*stage)
        self.records.append({'id':q,'stage':stage,'kind':kind,'gap':str(gap),'loss':str(loss)})
        self.fields.append((-gap/2,{q:'Z'}))
        return q,gap
    def subdivide(self,h,aa,bb,stage,kind):
        assert not(set(aa)&set(bb))
        q,gap=self.mediator(stage,kind)
        g=s.sqrt(abs(h)*gap/2)
        return (g,{**aa,q:'X'}),(-s.sign(h)*g,{**bb,q:'X'})


def encode(terms):
    return [{'coefficient':str(h),'pauli':{str(j):p for j,p in a.items()}} for h,a in terms]


def main():
    # Fifteen target triples share qubit 0 in five X, five Y, five Z
    # couplings. They do not all commute. Other old sites are private.
    roots=[]
    for j in range(15):
        roots.append((s.Rational((-1)**j,j+1),{0:'XYZ'[j%3],2*j+1:'Z',2*j+2:'Z'}))
    b=Build(31);terms=[]
    # Sequentially isolate all OLD sites of each original triple; every
    # root has its own three private ports and final internal triple.
    for h,p in roots:
        current=(h,p.copy())
        for stage,q in enumerate(sorted(p)):
            val,tail=current
            aa={q:tail[q]};bb={j:r for j,r in tail.items() if j!=q}
            isolated,current=b.subdivide(val,aa,bb,stage,'old_site_port')
            terms.append(isolated)
        terms.append(current)
    initial_port_count=b.next-b.old
    assert initial_port_count==45
    round_id=0
    while True:
        # Each currently exposed old edge has exactly one old endpoint
        # and a single controller port. Internal triples have no old site.
        groups={}
        for i,(h,p) in enumerate(terms):
            old=[q for q in p if q<b.old]
            if old:
                assert len(old)==1 and len(p)==2
                q=old[0];port=next(j for j in p if j!=q)
                assert p[port]=='X'
                groups.setdefault((q,p[q]),[]).append((i,h,port))
        pairs=[]
        for key,edges in groups.items():
            for i in range(0,len(edges)-1,2):pairs.append((key,edges[i],edges[i+1]))
        if not pairs:break
        removed=set();added=[]
        substage=3+2*round_id;forkstage=substage+1
        for (q,p),first,second in pairs:
            fresh=[]
            for index,h,port in (first,second):
                removed.add(index)
                endpoint,other=b.subdivide(h,{q:p},{port:'X'},substage,'fresh_fork_port')
                a,ep=endpoint;u=next(j for j in ep if j!=q)
                fresh.append((a,u));added.append(other)
            (a,u),(c,v)=fresh
            f,gap=b.mediator(forkstage,'fork')
            scale=s.sqrt(gap/2)
            added.extend([(scale,{q:p,f:'X'}),(-a*scale,{u:'X',f:'X'}),
                          (-c*scale,{v:'X',f:'X'}),(a*c,{u:'X',v:'X'})])
        terms=[t for i,t in enumerate(terms) if i not in removed]+added
        round_id+=1
    incidence=Counter();neighbors={q:set() for q in range(b.next)}
    for _,p in terms:
        assert 2<=len(p)<=3
        if len(p)==3:
            assert all(q>=b.old and axis=='X' for q,axis in p.items())
        else:
            assert 'X' in p.values()
        for q in p:
            incidence[q]+=1;neighbors[q].update(j for j in p if j!=q)
    assert incidence[0]==3 and max(incidence.values())<=3
    assert max(map(len,neighbors.values()))<=3
    assert round_id==3
    fork_count=sum(r['kind']=='fork' for r in b.records)
    fresh_count=sum(r['kind']=='fresh_fork_port' for r in b.records)
    assert fork_count==12 and fresh_count==2*fork_count
    out={'fixture':'noncommuting 15-edge three-body star; no logical code',
         'target':encode(roots),'physical_couplings':encode(terms),'one_body_fields':encode(b.fields),
         'mediators':b.records,'old_qubits':b.old,'physical_qubits':b.next,
         'physical_coupling_terms':len(terms),'port_mediators':initial_port_count,
         'forks':fork_count,'fresh_fork_ports':fresh_count,'pairing_rounds':round_id,
         'max_H_coupling_arity':max(len(p) for _,p in terms),
         'max_couplings_per_qubit':max(incidence.values()),
         'max_ordinary_graph_degree':max(map(len,neighbors.values())),
         'center_target_coupling_count':15,'center_final_coupling_count':incidence[0],
         'loss_arity':1,'all_fork_counterterms_included':True,
         'three_body_terms_are_controller_only_XXX':True,
         'two_body_alphabet':'P tensor X, P in X/Y/Z',
         'rates':'Illustrative finite exact scales, not certified protected-phase parameters',
         'scope':'Exact scalar/graph construction controls; no all-time numerical memory claim or device',
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'degree_construction.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'passed':True,'physical_qubits':b.next,
                     'couplings':len(terms),'max_couplings_per_qubit':max(incidence.values()),
                     'center_couplings':[15,incidence[0]]}))


if __name__=='__main__':main()
