"""Two new original edge-list receiving inputs, not a coloring search."""
from pathlib import Path
import json,time,resource

ROOT=Path(__file__).resolve().parents[1]

class Builder:
    def __init__(self): self.n=0;self.edges=[];self.parts=[]
    def vertex(self): v=self.n;self.n+=1;return v
    def edge(self,u,v): self.edges.append(tuple(sorted((u,v))))
    def atom(self,n,edges,name,identify=None):
        ids={}
        for i in range(n):
            ids[i]=identify[1] if identify is not None and i==identify[0] else self.vertex()
        for u,v in edges:self.edge(ids[u],ids[v])
        self.parts.append(dict(name=name,original_ids=[ids[i] for i in range(n)],
                               local_edges=edges,identified_vertex=identify))
        return ids
    def result(self,name,obligations):
        es=sorted(self.edges)
        assert len(es)==len(set(es))
        degree=[0]*self.n
        for u,v in es:degree[u]+=1;degree[v]+=1
        assert max(degree)<=4
        return dict(schema='astra-original-support/v1',name=name,n=self.n,edges=es,
            construction_provenance=self.parts,obligations=obligations,
            input_note='The native recovery receives only n and edges; provenance is not an oracle.')

def theta(lengths):
    es=[];n=2
    for length in lengths:
        old=0
        for _ in range(length-1):es.append((old,n));old=n;n+=1
        es.append((old,1))
    return n,es

def mixed():
    b=Builder();root=b.vertex()
    # Degree-three entry 0 is adjacent to degree-four vertex 2. The chosen
    # native incident edge reaches deleted-terminal load (2,3), family24.
    high=[(0,4),(4,1),(0,5),(5,1),(0,2),(3,6),(6,1)]
    for w in (7,8,9):high.extend([(2,w),(w,3)])
    a=b.atom(10,high,'intrinsic_non_theta_degree3_to_degree4')
    b.edge(root,a[0])
    # Internal cut-vertex composition and an outgoing bridge at a distinct,
    # adjacent actual mark. This is one module with three nontrivial atoms.
    cycle=[(0,1),(1,2),(2,3),(3,0)]
    c=b.atom(4,cycle,'C4_internal_child',(0,a[4]))
    d=b.atom(4,cycle,'C4_internal_grandchild',(0,c[1]))
    n,es=theta((2,3,5));t=b.atom(n,es,'degree3_theta_bridge_child')
    b.edge(a[1],t[0])
    # A bridge-only branching vertex follows another actual degree-three hub.
    tree=b.vertex();b.edge(t[1],tree)
    for _ in range(2):
        w=b.vertex();b.edge(tree,w)
        z=b.vertex();b.edge(w,z)
    triangle=[(0,1),(1,2),(2,0)]
    r=b.atom(3,triangle,'degree2_entry_with_outgoing_bridge')
    b.edge(a[5],r[0])
    s=b.atom(3,triangle,'second_degree2_entry')
    b.edge(r[0],s[0]) # Same original vertex has both entry and exit bridges.
    leaf=b.vertex();b.edge(s[0],leaf)
    # Multiple outgoing marks of the first module are handled simultaneously.
    n,es=theta((2,2,2));u=b.atom(n,es,'another_degree3_entry')
    b.edge(d[2],u[0])
    leaf=b.vertex();b.edge(a[5],leaf)
    # A second quotient branch containing a bare chain and a triangle atom.
    w=b.vertex();b.edge(root,w)
    z=b.vertex();b.edge(w,z)
    h=b.atom(3,triangle,'triangle_after_bare_chain');b.edge(z,h[0])
    return b.result('mixed_native_bridge_entries',[
        'original degree-three entry adjacent to a degree-four vertex',
        'a module containing adjacent internal atom cuts',
        'multiple outgoing actual marks without independent profiles',
        'incoming and outgoing bridges at the same degree-two root',
        'pure bridge-tree vertices with branching'])

def triangle_chain(k=9):
    b=Builder();roots=[]
    for i in range(k):
        t=b.atom(3,[(0,1),(1,2),(2,0)],'triangle_'+str(i));roots.append(t[0])
        if i:b.edge(roots[-2],roots[-1])
    return b.result('same_graph_entry_reset_chain',[
        'native receiving use on the exact omitted-entry-rule failure family',
        'each interior root has both bridge incidences and original degree four'])

def main():
    wall,cpu=time.perf_counter(),time.process_time()
    files=[]
    for filename,obj in [('mixed_native_bridge_entries.json',mixed()),
                         ('triangle_bridge_chain_9.json',triangle_chain())]:
        (ROOT/'inputs'/filename).write_text(json.dumps(obj,indent=2)+'\n')
        files.append(dict(file=filename,n=obj['n'],m=len(obj['edges'])))
    result=dict(files=files,wall_seconds=time.perf_counter()-wall,
        cpu_seconds=time.process_time()-cpu,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        includes='Input construction, simple-support/degree check, native input serialization.',
        excludes='This timing receipt; inference, authoring, source reading and discovery are unknown.')
    (ROOT/'results/INPUT_CONSTRUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
