"""Independent Fraction recomputation of the frozen sparse noise witness.

No eigensolver, SVD, main producer import, or new query direction is used.
"""
from pathlib import Path
from fractions import Fraction as F
import gzip, hashlib, json, resource, time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OWNER=ROOT.parent/'restore_pro2'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def f(v):return F(int(v['numerator']),int(v['denominator']))

def main():
    start=time.perf_counter();cpu=time.process_time()
    producer_path=ROOT/'results/sparse_condition_producer.json'
    replay_path=ROOT/'results/sparse_condition_replay.json'
    prior_hashes={p.name:digest(p) for p in [producer_path,replay_path]}
    result=json.loads(producer_path.read_text())
    kp=OWNER/'sources/bcsstk08.mtx.gz'
    xp=OWNER/'witnesses/lanczos.npz'
    assert digest(kp)==result['source_sha256']['K']=='5945836beb24009e8a94b58242d9b5c6cfd261117595898149d3fa9c99c084f7'
    assert digest(xp)==result['source_sha256']['lanczos']=='e69c119c0cc6ecc3e7cbc9402041c1c606e09eb25e91011040beadedeb2e92b3'
    text=gzip.decompress(kp.read_bytes()).decode('ascii')
    lines=[line.split() for line in text.splitlines() if line.strip() and not line.startswith('%')]
    n,n2,count=map(int,lines[0]);assert n==n2==1074 and count==len(lines)-1
    coefficients={}
    for line in lines[1:]:
        i,j=int(line[0])-1,int(line[1])-1
        assert 0<=j<=i<n and (i,j) not in coefficients
        coefficients[(i,j)]=F(line[2])
    core=result['core_vertices'];assert len(core)==len(set(core))==84
    assert all(type(i) is int and 0<=i<n for i in core)
    assert core==json.loads((ROOT/'results/eight_probe_core_preliminary.json').read_text())['core_vertices']
    with np.load(xp,allow_pickle=False) as z:
        basis=z['basis'];assert basis.dtype==np.int64 and basis.shape==(8,1074,64)
        # Assemble rows directly, using the nine explicitly named saved directions.
        xi=[[int(basis[ell,i,0]) for ell in range(8)]+[int(basis[0,i,1])] for i in core]
    wp=ROOT/'witnesses/sparse_noise_direction.npz'
    assert digest(wp)==result['witness_sha256']
    with np.load(wp,allow_pickle=False) as z:
        d=z['perturbation'];w=z['rayleigh_vector']
    assert d.dtype==np.int64 and d.shape==(84,84) and np.array_equal(d,d.T)
    assert w.dtype==np.int64 and w.shape==(84,)
    all_pattern=[]; nonzero_pattern=[]
    for i,ri in enumerate(core):
        for j,rj in enumerate(core):
            key=(max(ri,rj),min(ri,rj))
            if key in coefficients:all_pattern.append((i,j))
            if key in coefficients and coefficients[key]!=0:nonzero_pattern.append((i,j))
            if d[i,j]:
                assert key in coefficients and coefficients[key]!=0
    assert sum(i<=j for i,j in all_pattern)==result['independent_symmetric_coefficients']==657
    DD=result['perturbation_denominator'];VD=result['probe_denominator'];WD=result['Rayleigh_denominator']
    assert DD==2**40 and VD==WD==2**29
    D=[[F(int(d[i,j]),DD) for j in range(84)] for i in range(84)]
    X=[[F(v,VD) for v in row] for row in xi]
    V=[F(int(v),WD) for v in w]
    DX=[[sum(D[i][j]*X[j][ell] for j in range(84)) for ell in range(9)] for i in range(84)]
    norm2=sum(v*v for row in DX for v in row)
    fro2=sum(v*v for row in D for v in row)
    rayleigh=abs(sum(V[i]*sum(D[i][j]*V[j] for j in range(84)) for i in range(84))/sum(v*v for v in V))
    assert norm2==f(result['action_Frobenius_norm_squared'])>0
    assert fro2==f(result['perturbation_Frobenius_norm_squared'])
    assert rayleigh==f(result['operator_norm_lower'])>0
    upper=f(result['action_Frobenius_norm_upper']);assert upper>0 and upper*upper>=norm2
    amplification=rayleigh/upper
    assert amplification==f(result['operator_per_action_norm_amplification_lower'])
    assert amplification>F(798762179,100000)
    assert all(digest(p)==prior_hashes[p.name] for p in [producer_path,replay_path])
    out={'PASS':True,'check':'Independent direct Fraction evaluation of every entry of the core action and Rayleigh quotient',
         'original_nonzero_support_verified':True,'core_vertices_unique_and_bound':True,
         'same_nine_saved_directions_verified':True,
         'core_dimension':84,'independent_symmetric_coefficients':657,
         'operator_norm_lower':{'numerator':str(rayleigh.numerator),'denominator':str(rayleigh.denominator)},
         'action_norm_upper':{'numerator':str(upper.numerator),'denominator':str(upper.denominator)},
         'amplification_lower':{'numerator':str(amplification.numerator),'denominator':str(amplification.denominator)},
         'decimal_lower_bound_strict':'7987.62179',
         'original_receipts_unchanged':True,'original_receipt_hashes':prior_hashes,
         'new_SVD_calls':0,'new_eigensolver_calls':0,'new_directions':0,
         'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
         'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
         'scope':'A lower bound on operator error per query-Frobenius error on symmetric original-support perturbations; not an upper inverse bound or threshold-count ambiguity.'}
    (ROOT/'results/sparse_noise_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
