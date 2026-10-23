"""Independent support count and small exact fixtures for the eight-query bound.

The 657-variable map is NOT formed or solved. Its kernel bound is a theorem
from the supported-space dimension and the full symmetric-action rank formula.
"""
import time
START=time.perf_counter()
CPU=time.process_time()
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import gzip
import hashlib
import json
import resource
import sys


def rank(rows):
    if not rows: return 0
    a=[[F(v) for v in row] for row in rows]
    m,n=len(a),len(a[0]);r=0
    for j in range(n):
        k=next((k for k in range(r,m) if a[k][j]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        p=a[r][j]
        a[r]=[v/p for v in a[r]]
        for k in range(r+1,m):
            p=a[k][j]
            if p:a[k]=[v-p*w for v,w in zip(a[k],a[r])]
        r+=1
        if r==m:break
    return r


def fixture(m,r,q):
    assert 0<=r<=min(m,q)
    # A Vandermonde left factor has rank r; the right factor starts with I_r.
    left=[[F((i+1)**j) for j in range(r)] for i in range(m)]
    right=[[F(i==j) if j<r else F((i+1)*(j+1)+1) for j in range(q)] for i in range(r)]
    x=[[sum((left[i][k]*right[k][j] for k in range(r)),F(0)) for j in range(q)] for i in range(m)]
    assert rank(x)==r
    variables=[(i,j) for i in range(m) for j in range(i,m)]
    # Each column is vec(E_ij X), using the actual symmetric basis E_ij+E_ji.
    columns=[]
    for i,j in variables:
        output=[[F(0) for _ in range(q)] for _ in range(m)]
        output[i]=x[j][:]
        if i!=j:output[j]=x[i][:]
        columns.append([v for row in output for v in row])
    action=[list(row) for row in zip(*columns)]
    actual=rank(action)
    expected=m*r-r*(r-1)//2
    assert actual==expected
    return {'m':m,'q':q,'rank_X':r,'computed_full_symmetric_action_rank':actual,
            'formula_rank':expected,'full_symmetric_dimension':len(variables)}


def main():
    root=Path(__file__).resolve().parents[1]
    owner=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'restore_pro2'
    path=owner/'sources/bcsstk08.mtx.gz'
    raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    assert digest=='5945836beb24009e8a94b58242d9b5c6cfd261117595898149d3fa9c99c084f7'
    # Independent tiny parser, rather than importing the old parser's support.
    lines=gzip.decompress(raw).decode('ascii').splitlines()
    assert lines[0].strip().lower()=='%%matrixmarket matrix coordinate real symmetric'
    body=[s.split() for s in lines[1:] if s.strip() and not s.lstrip().startswith('%')]
    n,m,nnz=map(int,body[0]);assert n==m==1074 and nnz==len(body)-1==7017
    original={}
    for row in body[1:]:
        assert len(row)==3
        i,j=int(row[0])-1,int(row[1])-1
        assert 0<=j<=i<n and (i,j) not in original
        original[i,j]=F(row[2])
    graph=[set() for _ in range(n)];diagonal=set()
    for (i,j),v in original.items():
        if not v:continue
        if i==j:diagonal.add(i)
        else:graph[i].add(j);graph[j].add(i)
    # FIFO deletion of degree<8 vertices, independent of the saved min-heap order.
    degree=list(map(len,graph));live=[True]*n
    queue=deque(i for i,d in enumerate(degree) if d<8)
    while queue:
        i=queue.popleft()
        if not live[i]:continue
        assert degree[i]<8
        live[i]=False
        for j in graph[i]:
            if live[j]:
                degree[j]-=1
                if degree[j]==7:queue.append(j)
    core=[i for i in range(n) if live[i]]
    cp=root/'results/eight_probe_core_preliminary.json'
    supplied=json.loads(cp.read_text())
    assert core==supplied['core_vertices']
    edges=[(i,j) for i in core for j in sorted(graph[i]) if live[j] and i<j]
    diag=[i for i in core if i in diagonal]
    assert len(core)==supplied['core_size']==84
    assert len(edges)==supplied['core_edges']==573
    assert len(diag)==84 and len(edges)+len(diag)==supplied['core_variables']==657
    assert min(degree[i] for i in core)==8
    assert supplied['core_equations']==84*8==672
    t=time.perf_counter()
    fixtures=[fixture(*args) for args in [(3,0,2),(4,1,3),(4,2,4),(4,3,3),(5,4,6)]]
    fixture_seconds=time.perf_counter()-t
    ranks=[84*r-r*(r-1)//2 for r in range(9)]
    assert max(ranks)==644 and 657-max(ranks)==13
    receipt={'PASS':True,'source_sha256':digest,
             'independent_core_method':'FIFO iterative deletion of offdiagonal degree<8',
             'core_preliminary_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
             'core_vertices':core,'core_size':84,'induced_offdiagonal_edges':573,
             'permitted_diagonals':84,'symmetric_supported_space_dimension':657,
             'raw_eight_query_output_coordinates':672,
             'maximum_full_symmetric_action_rank_for_eight_directions':644,
             'guaranteed_kernel_dimension_at_least':13,
             'rank_formula_values_for_rankX_0_through_8':ranks,
             'small_exact_rational_fixtures':fixtures,
             'fixture_wall_seconds':fixture_seconds,
             'wall_seconds_including_imports':time.perf_counter()-START,
             'cpu_seconds_including_imports':time.process_time()-CPU,
             'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
             'large_linear_system_constructed':False,
             'scope':'Exact identification lower bound, not a CDF accuracy or stability theorem.'}
    out=root/'results/eight_probe_obstruction_challenge.json'
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='core_vertices'},indent=2))


if __name__=='__main__':main()
