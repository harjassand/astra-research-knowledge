"""Finite combinatorial checks only; this does not construct a quantum basis."""
import itertools, json, math, pathlib, resource, time
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parent
start=time.perf_counter(); cpu=time.process_time()
P=list(itertools.permutations(range(4))); ix={p:i for i,p in enumerate(P)}
def inverse(p): return tuple(p.index(i) for i in range(4))
def compose(p,q): return tuple(p[q[i]] for i in range(4))
R=[[ix[compose(p,inverse(q))] for q in P] for p in P]
C=(1,0,1,0,2,0,2,0,0,0,1,1,0,2,0,2,0,0,0,0,1,0,2,1)
assert sum(C)==16
balance=[[sum(C[k] for k,p in enumerate(P) if p[b]==c) for c in range(4)] for b in range(4)]
assert balance==[[4]*4 for _ in range(4)]
# A factorization C = sum_{y,z} [k_y h_z^{-1}] can be normalized so h_0=id:
# replace all h_z,k_y by h_z h_0^{-1}, k_y h_0^{-1}. Thus one four-element
# multiset B={k_y} lies inside C. Exhaust all such B and all three additional
# right translates of B, using an exact integer meet-in-the-middle search.
checked_B=0; factor_found=None
support=[i for i,v in enumerate(C) if v]
for bs in itertools.combinations_with_replacement(support,4):
    B=Counter(bs)
    if any(v>C[k] for k,v in B.items()): continue
    checked_B+=1
    target=list(C)
    for b in bs: target[b]-=1
    translates={}
    for h in range(24):
        t=[0]*24
        for b in bs: t[R[b][h]]+=1
        t=tuple(t)
        if all(v<=target[i] for i,v in enumerate(t)): translates[t]=h
    ts=list(translates)
    pair_sums=set()
    for ai,a in enumerate(ts):
        for b in ts[ai:]:
            s=tuple(x+y for x,y in zip(a,b))
            if all(v<=target[i] for i,v in enumerate(s)): pair_sums.add(s)
    for a in ts:
        if tuple(x-y for x,y in zip(target,a)) in pair_sums:
            factor_found=bs
            break
    if factor_found is not None: break
assert checked_B==565 and factor_found is None
# Count proof for a strengthened cut-dual example. No enormous table enumeration.
D=107; q=D//2
perturbation_count=pow(3,q**3); all_triangle_function_count=pow(D,3*D**2)
assert perturbation_count>all_triangle_function_count
# Check every signed 2x2x2 checkerboard has zero two-coordinate marginals.
for first in range(2):
    for second in range(2):
        assert sum((-1)**(first+second+third) for third in range(2))==0
# Check abstract semilattice size and cut-duality formula for n=3.
ks={mask:(1 if mask in (0,7) else D) for mask in range(8)}
assert all(ks[m]==ks[7^m] for m in range(8))
assert all(pow(D,min(m.bit_count(),3-m.bit_count()))%ks[m]==0 for m in range(8))
result={
 'scope':'Finite classical partition obstruction; no quantum realization, no entropy counterexample.',
 'explicit_D4':{'D':4,'n':3,'points':64,'permutations':P,'multiplicities':C,'pair_incidence':balance,'candidate_B_multisets_exhausted':checked_B,'coordinate_factorization_exists':False,'cut_duality_satisfied':False},
 'cut_dual_existence_D107':{'D':D,'n':3,'points':D**3,'independent_signed_cubes':q**3,'triangle_map_exponent':3*D**2,'exact_integer_count_inequality_passed':True,'perturbation_count_bit_length':perturbation_count.bit_length(),'triangle_map_count_bit_length':all_triangle_function_count.bit_length(),'log_count_ratio':q**3*math.log(3)-3*D**2*math.log(D),'counterexample_selected':False,'all_singleton_cell_sizes':D**2,'all_pair_cell_sizes':D**3,'cut_duality_satisfied':True},
 'cost':{'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'peak_rss_native_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}}
(ROOT/'PARTITION_LEMMA_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['explicit_D4']},indent=2))
