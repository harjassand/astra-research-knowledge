"""Coordinate-level formula for BDL RX physical Z-check relations, ell=3.
The formula also determines relations at larger subdivisions by repetition.
"""
from collections import defaultdict
from bdl_matroid_probe import canonical_edge,rank_and_relations,relation_columns

def rx_Z_relations(old):
    names=[]
    def var(name):
        i=len(names);names.append(name);return 1<<i
    _,oldhz=old.matrices()
    _,oldrels=rank_and_relations(oldhz)
    dcols=relation_columns(oldrels,len(old.Z))
    names.extend(('d',j) for j in range(len(oldrels)))
    d=dict(zip(old.Z,dcols))
    s={z:var(('s',z)) for z in old.Z}
    qzs=defaultdict(list)
    for q,z in sorted(old.qz,key=repr):qzs[q].append(z)
    a={}
    for q in old.Q:
        zs=qzs[q]
        assert zs
        first=zs[0];v=0
        for z in zs[1:]:
            a[q,z]=var(('a',q,z));v^=a[q,z]
        a[q,first]=v
    out={}
    for x in old.X:
        fs=[f for f in old.faces if f[0]==x]
        qs=sorted({q for xx,q in old.xq if xx==x},key=repr);qi={q:i for i,q in enumerate(qs)}
        fcols=[(1<<qi[f[1]])^(1<<qi[f[3]]) for f in fs]
        _,cycles=rank_and_relations(fcols)
        localcols=relation_columns(cycles,len(fs));off=len(names)
        names.extend(('F',x,j) for j in range(len(cycles)))
        F=[v<<off for v in localcols]
        byqz={}
        for i,(_,q1,z,q2) in enumerate(fs):
            for t in (0,1):out[('XF',x,2*i+t)]=F[i]^(d[z] if t else 0)
            for q in (q1,q2):
                assert (q,z) not in byqz
                byqz[q,z]=i
        bdry_edges=sorted({canonical_edge(('q',q),('z',z)) for q,z in byqz},key=repr)
        for j,e in enumerate(bdry_edges):
            q=next(v[1] for v in e if v[0]=='q');z=next(v[1] for v in e if v[0]=='z')
            out[('XF',x,2*len(fs)+j)]=F[byqz[q,z]]^a[q,z]
    for q in old.Q:
        for z in qzs[q]:
            for t in (0,1):
                e=canonical_edge((('q',q),t),(('z',z),t))
                out[('QE',q,e)]=a[q,z]^(d[z] if t else 0)
            e=canonical_edge((('z',z),0),(('z',z),1))
            out[('QE',q,e)]=a[q,z]^s[z]
    for z in old.Z:
        for t in (0,1):out[('ZV',z,t)]=s[z]^(d[z] if t else 0)
    return names,out

if __name__=='__main__':
    from pathlib import Path
    import json
    from bdl_matroid_probe import seed,rx
    from bdl_cmr_probe import fundamental
    from reduce_matroid_probe import write_fundamental
    old=rx(rx(seed()).dual()).dual();new=rx(old)
    names,columns=rx_Z_relations(old)
    assert set(columns)==set(new.Z)
    qubits=defaultdict(int)
    for q,z in new.qz:qubits[q]^=columns[z]
    assert not any(qubits.values())
    rank,_=rank_and_relations(list(columns.values()))
    _,hz=new.matrices();hzrank,_=rank_and_relations(hz)
    assert rank==len(names)==len(new.Z)-hzrank
    print({'parameters':len(names),'old_relation':sum(x[0]=='d' for x in names),'s':sum(x[0]=='s' for x in names),'a':sum(x[0]=='a' for x in names),'F':sum(x[0]=='F' for x in names),'exact_verified':True},flush=True)
    b=Path(__file__).parent/'matroid_certificates'
    selected,rest=write_fundamental([columns[z] for z in new.Z],b/'level3_Z_dual_analytic.sparse')
    (b/'level3_Z_dual_analytic_map.json').write_text(json.dumps({'parameters':[repr(x) for x in names],'basis_physical_indices':selected,'rest_physical_indices':rest,'physical_labels':[repr(x) for x in new.Z]},indent=2)+'\n')
    (b/'level3_Z_dual_analytic_columns.json').write_text(json.dumps([hex(columns[z]) for z in new.Z])+'\n')
