"""Exact order-8 nonabelian group certificate; no floating-point quantum matrix."""
import itertools,json,time,resource,platform
from pathlib import Path
start=time.perf_counter();cpu=time.process_time()
# (r,s) in Z4 semidirect Z2, multiplication r+(-1)^s t, s+u.
G=list(itertools.product(range(4),range(2))); idx={x:i for i,x in enumerate(G)}
D=len(G); n=3
mul=lambda x,y:idx[((G[x][0]+(-1)**G[x][1]*G[y][0])%4,(G[x][1]+G[y][1])%2)]
e=idx[(0,0)]
inv=lambda x:next(y for y in range(D) if mul(x,y)==e and mul(y,x)==e)
labels=list(itertools.product(range(D),repeat=3))
y=[(c,mul(c,a),mul(c,b)) for a,b,c in labels]; assert len(set(y))==D**3
noncomm=next((x,z) for x in range(D) for z in range(D) if mul(x,z)!=mul(z,x))
subsets=[s for k in range(4) for s in itertools.combinations(range(3),k)]
cell_sizes={}
for S in subsets:
    keep=tuple(i for i in range(3) if i not in S)
    def key(L):
        a,b,c=L;aa=(e,a,b)
        if not S:return ('point',L)
        return tuple(sorted(tuple(mul(g,aa[i]) for i in keep) for g in range(D)))
    cells={};fibers={}
    for j,L in enumerate(labels):
        k=key(L);cells.setdefault(k,[]).append(j)
        fkey=tuple(y[j][i] for i in keep)
        assert fkey not in fibers or fibers[fkey]==k
        fibers[fkey]=k
    sizes=sorted(set(map(len,cells.values())))
    expected=1 if not S else D**3 if len(S)==3 else D**(len(S)+1)
    assert sizes==[expected]
    cell_sizes[str(S)]={'cells':len(cells),'size':expected,'coordinate_fibers':len(fibers)}
# Triple a,b,a^-1 b is a genuine nonabelian Latin square, pairwise independent.
triples=[(a,b,mul(inv(a),b)) for a in range(D) for b in range(D)]
for i,j in ((0,1),(0,2),(1,2)): assert len({(t[i],t[j]) for t in triples})==D**2
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
out={'group':'Z4 semidirect Z2, dihedral order 8','noncommuting_pair':noncomm,'dimension_per_site':D,'block_sites':3,'labels_checked':len(labels),'all_subsets_checked':len(subsets),'cell_sizes':cell_sizes,'triple_net_pairwise_independence':'EXACT','coordinate_fiber_containment':'EXACT','field_linear_incompatibility':'Analytic isotope proof in PROOF.txt, Section C, not brute-force search','wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':rss if platform.system()=='Darwin' else rss*1024}
Path(__file__).with_name('DIHEDRAL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
