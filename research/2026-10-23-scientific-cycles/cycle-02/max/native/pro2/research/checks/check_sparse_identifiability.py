"""Construct/replay exact local identifiability of the original sparse pattern.

One fixed prefix, depth then probe, of q=max original row-support size columns.
No coefficient solve, eigenvalue calculation, probe generation or prefix sweep.
Usage: python check_sparse_identifiability.py --construct [--owner PATH]
       python check_sparse_identifiability.py --verify [--owner PATH]
"""
import time
PROCESS_STARTED=time.perf_counter()
CPU_STARTED=time.process_time()
import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path
import resource
import sys
import numpy as np

PRIME=2147483647
PINNED={
    'sources/bcsstk08.mtx.gz':'5945836beb24009e8a94b58242d9b5c6cfd261117595898149d3fa9c99c084f7',
    'witnesses/lanczos.npz':'e69c119c0cc6ecc3e7cbc9402041c1c606e09eb25e91011040beadedeb2e92b3',
    'src/exact_residual.py':'bd3bf12b28727a0cbc500221984269b6c2eccf5acec76885e632bb74b2041d78',
}


def require(x,msg):
    if not x: raise ValueError(msg)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def is_prime_exact(p):
    if p<2: return False
    if p%2==0: return p==2
    return all(p%d for d in range(3,isqrt(p)+1,2))


def load(owner):
    started=time.perf_counter()
    for path,digest in PINNED.items():
        require(sha(owner/path)==digest,'source hash mismatch: '+path)
    # Reuse the original exact-decimal Matrix Market parser, whose bytes above
    # are independently pinned. No rounded operator or nonzero filter is loaded.
    sys.path.insert(0,str((owner/'src').resolve()))
    from exact_residual import read_mm_exact
    n,entries=read_mm_exact(owner/'sources/bcsstk08.mtx.gz')
    supports=[set() for _ in range(n)]
    for (i,j),value in entries.items():
        if value != 0:
            supports[i].add(j)
            supports[j].add(i)
    supports=[sorted(s) for s in supports]
    q=max(map(len,supports))
    with np.load(owner/'witnesses/lanczos.npz',allow_pickle=False) as z:
        basis=z['basis']
    require(basis.dtype==np.dtype('int64'),'integer basis dtype')
    require(basis.shape==(8,n,64),'actual saved basis dimensions')
    require(q<=512,'prescribed prefix unavailable; stop instead of escalating')
    prefix=[(ell,depth) for depth in range(64) for ell in range(8)][:q]
    x=np.column_stack([basis[ell,:,depth] for ell,depth in prefix])
    require(x.shape==(n,q),'prefix shape')
    facts={'n':n,'q':q,'stored_columns_available':512,
           'column_order':'depth increasing, then probe index increasing',
           'last_column_probe_depth':list(prefix[-1]),
           'lower_triangle_records':len(entries),
           'exact_zero_records':sum(v==0 for v in entries.values()),
           'expanded_original_nnz':sum(map(len,supports)),
           'min_row_support':min(map(len,supports)),
           'max_row_support':q,
           'rows_at_max_support':[i for i,s in enumerate(supports) if len(s)==q],
           'basis_denominator':2**29,
           'pinned_source_sha256':PINNED,
           'source_and_prefix_wall_seconds':time.perf_counter()-started}
    return x,supports,facts


def rank_witness(a,p):
    """Rectangular row elimination; selected minor and pivots are the witness."""
    a=np.remainder(a,p).astype(np.int64,copy=True)
    m,q=a.shape
    row_permutation=list(range(m))
    rank=0;columns=[];pivots=[];sign=1
    for col in range(q):
        candidates=np.flatnonzero(a[rank:,col])
        if not len(candidates): continue
        pick=rank+int(candidates[0])
        if pick!=rank:
            a[[rank,pick]]=a[[pick,rank]]
            row_permutation[rank],row_permutation[pick]=row_permutation[pick],row_permutation[rank]
            sign=-sign
        pivot=int(a[rank,col]);pivots.append(pivot);columns.append(col)
        inverse=pow(pivot,-1,p)
        a[rank,col:]=(a[rank,col:]*inverse)%p
        if rank+1<m:
            factors=a[rank+1:,col].copy()
            a[rank+1:,col:]=(a[rank+1:,col:]-factors[:,None]*a[rank,col:])%p
        rank+=1
        if rank==m: break
    determinant=sign
    for v in pivots: determinant=(determinant*v)%p
    return {'rank_mod_prime':rank,'pivot_columns':columns,
            'row_permutation':row_permutation,'pivot_values_mod_prime':pivots,
            'determinant_of_selected_minor_mod_prime':determinant%p if rank==m else None}


def permutation_sign(perm):
    return -1 if sum(perm[i]>perm[j] for i in range(len(perm))
                     for j in range(i+1,len(perm)))%2 else 1


def verify_selected_minor(x,support,w,p):
    """Square-minor Schur elimination, no rank search or chosen alternate minor."""
    m=len(support)
    cols=w['pivot_columns'];perm=w['row_permutation']
    require(w['rank_mod_prime']==m,'row rank incomplete')
    require(len(cols)==m and sorted(set(cols))==cols,'ordered distinct minor columns')
    require(all(type(c) is int and 0<=c<x.shape[1] for c in cols),'minor columns range')
    require(sorted(perm)==list(range(m)),'row permutation')
    require(len(w['pivot_values_mod_prime'])==m,'pivot witness length')
    a=np.remainder(x[np.ix_(support,cols)],p).astype(np.int64,copy=True)
    a=a[perm,:]
    product=permutation_sign(perm)
    for j in range(m):
        pivot=int(a[j,j])
        require(pivot!=0,'singular declared minor')
        require(pivot==w['pivot_values_mod_prime'][j],'pivot receipt mismatch')
        product=product*pivot%p
        if j+1<m:
            factors=(a[j+1:,j]*pow(pivot,p-2,p))%p
            a[j+1:,j+1:]=(a[j+1:,j+1:]-factors[:,None]*a[j,j+1:])%p
    require(product==w['determinant_of_selected_minor_mod_prime'],'determinant mismatch')
    require(product!=0,'zero determinant')


def main():
    ap=argparse.ArgumentParser()
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--construct',action='store_true')
    mode.add_argument('--verify',action='store_true')
    ap.add_argument('--owner',type=Path,default=Path(__file__).resolve().parents[2]/'restore_pro2')
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    cp=root/'results/sparse_identifiability_certificate.json'
    out=root/'results'/('sparse_identifiability.json' if args.construct else 'sparse_identifiability_replay.json')
    x,supports,facts=load(args.owner)
    t=time.perf_counter()
    require(is_prime_exact(PRIME),'declared modulus must be prime')
    # Each NumPy expression multiplies at most two residues before reducing.
    # No dot products or accumulated sums occur in those int64 kernels.
    require((PRIME-1)**2<2**63,'int64 multiplication guard')
    prime_seconds=time.perf_counter()-t
    t=time.perf_counter()
    if args.construct:
        require(not cp.exists(),'refuse to overwrite an existing construction')
        rows=[]
        for i,s in enumerate(supports):
            w=rank_witness(x[s,:],PRIME)
            rows.append({'row':i,'support':s,**w})
        algebra_seconds=time.perf_counter()-t
        failed=[r['row'] for r in rows if r['rank_mod_prime']!=len(r['support'])]
        cert={'schema':'original-pattern-row-identifiability-v1','prime':PRIME,
              'facts':facts,'rows':rows,'failed_rows':failed,
              'claim':'Exact injectivity on matrices supported on original K pattern, conditional on each row minor being nonzero.'}
        cp.write_text(json.dumps(cert,separators=(',',':'))+'\n')
        receipt={'PASS':not failed,'mode':'construct','facts':facts,
                 'attempt_count':1,'failed_rows':failed,
                 'row_rank_construction_wall_seconds':algebra_seconds,
                 'prime_validation_wall_seconds':prime_seconds,
                 'certificate_bytes':cp.stat().st_size,'certificate_sha256':sha(cp),
                 'least_minor_residue':min((r['determinant_of_selected_minor_mod_prime'] or 0) for r in rows),
                 'max_selected_column_index':max(c for r in rows for c in r['pivot_columns'])}
    else:
        cert=json.loads(cp.read_text())
        require(cert['schema']=='original-pattern-row-identifiability-v1','schema')
        require(cert['prime']==PRIME,'prime')
        for key,value in facts.items():
            if not key.endswith('_seconds'):
                require(cert['facts'][key]==value,'facts mismatch: '+key)
        require(cert['failed_rows']==[],'construction contains failed rows')
        require(len(cert['rows'])==facts['n'],'row count')
        for i,(s,w) in enumerate(zip(supports,cert['rows'])):
            require(w['row']==i and w['support']==s,'source row binding')
            verify_selected_minor(x,s,w,PRIME)
        receipt={'PASS':True,'mode':'verify','facts':facts,
                 'all_original_rows_checked':facts['n'],
                 'independent_minor_verification_wall_seconds':time.perf_counter()-t,
                 'prime_validation_wall_seconds':prime_seconds,
                 'certificate_sha256':sha(cp)}
    receipt.update({'wall_seconds_including_python_imports':time.perf_counter()-PROCESS_STARTED,
                    'cpu_seconds_including_python_imports':time.process_time()-CPU_STARTED,
                    'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                    'not_claimed':['stable recovery','spectral speedup','few-probe optimum','exact action already available from saved scalar Jacobi moments']})
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
