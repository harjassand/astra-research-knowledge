"""Replay the saved deterministic peeling order on the original exact graph."""
import time
START=time.perf_counter()
CPU=time.process_time()
from pathlib import Path
import hashlib
import heapq
import json
import resource
import sys

root=Path(__file__).resolve().parents[1]
owner=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'restore_pro2'
path=owner/'sources/bcsstk08.mtx.gz'
assert hashlib.sha256(path.read_bytes()).hexdigest()=='5945836beb24009e8a94b58242d9b5c6cfd261117595898149d3fa9c99c084f7'
parser=owner/'src/exact_residual.py'
assert hashlib.sha256(parser.read_bytes()).hexdigest()=='bd3bf12b28727a0cbc500221984269b6c2eccf5acec76885e632bb74b2041d78'
sys.path.insert(0,str(parser.parent))
from exact_residual import read_mm_exact
n,entries=read_mm_exact(path)
g=[set() for _ in range(n)]
for (i,j),v in entries.items():
    if v and i!=j:
        g[i].add(j);g[j].add(i)
cert=json.loads((root/'results/sparse_degeneracy_preliminary.json').read_text())
assert cert['n']==n and sorted(cert['order'])==list(range(n))
degree=list(map(len,g));live=[True]*n
heap=[(d,i) for i,d in enumerate(degree)];heapq.heapify(heap)
seen=[];degrees=[];lower_witness=None
while heap:
    d,i=heapq.heappop(heap)
    if not live[i] or d!=degree[i]:continue
    if d==cert['degeneracy'] and lower_witness is None:
        remain=[j for j in range(n) if live[j]]
        # Independently recompute the induced-subgraph degrees for the lower bound.
        min_degree=min(sum(live[k] for k in g[j]) for j in remain)
        assert min_degree==d
        lower_witness={'order_step':len(seen),'induced_vertex_count':len(remain),
                       'minimum_induced_degree':min_degree}
    seen.append(i);degrees.append(d);live[i]=False
    for j in g[i]:
        if live[j]:
            degree[j]-=1;heapq.heappush(heap,(degree[j],j))
assert seen==cert['order'] and degrees==cert['remaining_degrees']
assert max(degrees)==cert['degeneracy']==8 and cert['generic_columns_sufficient']==9
receipt={'PASS':True,'n':n,'degeneracy':8,'generic_columns_sufficient':9,
         'all_removals_minimum_degree_with_smallest_index_tie_break':True,
         'lower_bound_induced_subgraph_witness':lower_witness,
         'wall_seconds_including_imports':time.perf_counter()-START,
         'cpu_seconds_including_imports':time.process_time()-CPU,
         'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
         'no_nine_column_rank_test_performed':True}
(root/'results/sparse_degeneracy_verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
