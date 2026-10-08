"""Independent certificate checker: dense F2 elimination and codeword automorphisms.
Does not import generator/search code.
"""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter
import json,time
P=Path(__file__).parent
C=json.loads((P/"buffer_all_variables_certificate.json").read_text())
ROWS=C["rows"];FULL=(1<<18)-1

def dense_full_rank(mask):
    cols=[i for i in range(18) if (mask>>i)&1]
    if len(cols)!=9:return False
    A=[[ROWS[i][j] for j in cols] for i in range(9)]
    for k in range(9):
        pivot=next((i for i in range(k,9) if A[i][k]),None)
        if pivot is None:return False
        A[k],A[pivot]=A[pivot],A[k]
        for i in range(k+1,9):
            if A[i][k]:A[i]=[x^y for x,y in zip(A[i],A[k])]
    return True

def permute(x,p):
    y=0
    for old,new in enumerate(p):
        if x&(1<<old):y|=1<<new
    return y

def split_count(mask):
    return sum(((mask>>(2*i))&3) in (1,2) for i in range(9))

def exchange_ordered(S,T):
    changed=[i for i in range(len(S)) if S[i]!=T[i]]
    if len(changed)!=2:return False
    i,j=changed;delta=S[i]^T[i]
    return delta==S[j]^T[j] and delta.bit_count()==2 and (
        S[i]&delta).bit_count()==1 and (S[j]&delta).bit_count()==1 and (
        S[i]&delta)!=(S[j]&delta)

def exchange_unordered(S,T):
    return any(exchange_ordered(S,Q) for Q in permutations(T))

start=time.monotonic()
bases={sum(1<<j for j in I) for I in combinations(range(18),9)
       if dense_full_rank(sum(1<<j for j in I))}
assert len(bases)==14848
# Verify automorphisms via exact whole binary linear code, independently of RREF.
row_masks=[sum(x<<j for j,x in enumerate(row)) for row in ROWS]
code={0}
for row in row_masks:code|={x^row for x in list(code)}
assert len(code)==512
G=C["automorphisms"]
for g in G:
    perm=g["perm"]
    assert sorted(perm)==list(range(18))
    assert all(permute(w,perm) in code for w in code)
    assert all(perm[2*i]//2==perm[2*i+1]//2 for i in range(9))
# Orbit trees provide exact coverage and actual automorphism edges.
covered=set();representatives=[]
for tree in C["orbit_parent_trees"]:
    seen=set();root=tree[0][0];representatives.append(root)
    for row in tree:
        x=row[0]
        assert x in bases and x not in covered
        if len(row)==1:assert x==root
        else:
            parent,gi=row[1:]
            assert parent in seen
            assert permute(parent,G[gi]["perm"])==x
        seen.add(x);covered.add(x)
assert covered==bases
# Pair component trees verify connectivity; split levels verify separation.
pair_cover=set()
for ci,tree in enumerate(C["pair_component_parent_trees"]):
    seen=set()
    for row in tree:
        state=tuple(row[:2])
        assert state[0] in bases and state[1] in bases and state[0]^state[1]==FULL
        assert state not in pair_cover
        assert split_count(state[0]) in ({7,9} if ci==0 else {3})
        if len(row)>2:
            parent=tuple(row[2:])
            assert parent in seen and exchange_unordered(parent,state)
        seen.add(state);pair_cover.add(state)
all_pairs={tuple(sorted((b,FULL^b))) for b in bases if FULL^b in bases}
assert pair_cover==all_pairs and len(all_pairs)==2808
assert {split_count(b) for b in bases if FULL^b in bases}=={3,7,9}
# A symmetric exchange changes split count by at most 2, separating the sectors.
for tree in C["pair_component_parent_trees"]:
    assert len(tree) in (864,1920)
B,D=C["B"],C["D"]
assert split_count(B)==3 and split_count(D)==7
for p in C["representative_paths"]:
    N=p["buffer_mask"];path=[tuple(x) for x in p["path"]]
    assert p["status"]=="FOUND" and N in representatives
    assert path[0]==tuple(sorted((N,B,FULL^B)))
    assert path[-1]==tuple(sorted((N,D,FULL^D)))
    for S in path:
        assert all(x in bases for x in S)
        assert [sum((x>>j)&1 for x in S) for j in range(18)]==[
            2 if (N>>j)&1 else 1 for j in range(18)]
    assert all(exchange_unordered(S,T) for S,T in zip(path,path[1:]))
# Ordered certificates support the stronger fixed-slot interface only for representatives.
OC=json.loads((P/"buffer_ordered_certificate.json").read_text())
for p in OC["paths"]:
    N=p["buffer_mask"];path=[tuple(x) for x in p["path"]]
    assert path[0]==(N,B,FULL^B) and path[-1]==(N,D,FULL^D)
    assert all(all(x in bases for x in S) for S in path)
    assert all(exchange_ordered(S,T) for S,T in zip(path,path[1:]))
result={"status":"PASS","scope":"finite matrix/orbit/pair-fiber/path certificate only",
        "basis_count":len(bases),"pair_count":len(all_pairs),
        "orbit_count":len(representatives),"automorphism_count":len(G),
        "pair_component_sizes":[864,1920],
        "conclusion":"For this published matroid and distinguished f, f not in J and every basis-variable multiple is in J.",
        "formal_replay":False,"external_validation":False,
        "wall_seconds":time.monotonic()-start}
(P/"verify_certificate_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
