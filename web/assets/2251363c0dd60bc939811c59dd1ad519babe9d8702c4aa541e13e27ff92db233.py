"""Direct Fano checker; uses the 3-column XOR characterization, no search imports."""
from itertools import combinations,combinations_with_replacement,permutations
from pathlib import Path
import json
bases=[tuple(S) for S in combinations(range(7),3)
       if (S[0]+1)^(S[1]+1)^(S[2]+1)]
assert len(bases)==28
A=((0,1,3),(0,2,4),(1,5,6))
B=((0,1,6),(0,2,5),(1,3,4))
def incidence(U):return tuple(sum(e in x for x in U) for e in range(7))
def deficit(U,V):return min(sum(len(set(x)-set(y)) for x,y in zip(U,P)) for P in permutations(V))
assert all(x in bases for x in A+B)
assert incidence(A)==incidence(B)==(2,2,1,1,1,1,1)
out=set()
for i,j in combinations(range(3),2):
    s=incidence((A[i],A[j]))
    for x,y in combinations_with_replacement(bases,2):
        if incidence((x,y))==s:
            T=list(A);T[i]=x;T[j]=y;T=tuple(sorted(T))
            if T!=A:out.add(T)
assert deficit(A,B)==3 and len(out)==7
assert min(deficit(T,B) for T in out)==3
path=[A,((0,1,3),(0,4,5),(1,2,6)),
      ((0,1,6),(0,4,5),(1,2,3)),B]
def symadj(U,V):
    for Q in permutations(V):
        ch=[i for i in range(3) if U[i]!=Q[i]]
        if len(ch)!=2:continue
        i,j=ch
        if len(set(U[i])^set(Q[i]))==2 and len(set(U[j])^set(Q[j]))==2 and (
            set(U[i])^set(Q[i]))==(set(U[j])^set(Q[j])):
            return True
    return False
assert all(all(x in bases for x in T) and incidence(T)==incidence(A) for T in path)
assert all(symadj(U,V) for U,V in zip(path,path[1:]))
R={"status":"PASS","scope":"exact fixed Fano local-minimum witness for all arbitrary pair replacements",
   "basis_count":28,"A":A,"B":B,"deficit":3,
   "neighbors":[{"state":T,"deficit":deficit(T,B)} for T in sorted(out)],
   "path":path,"path_deficits":[deficit(T,B) for T in path],
   "connectivity_counterexample":False,"novelty":"UNKNOWN; no scientific promotion"}
(Path(__file__).parent/"verify_fano_results.json").write_text(json.dumps(R,indent=2)+"\n")
print("PASS: 28 bases, all 7 arbitrary-pair neighbors have deficit >=3; plateau path3,3,2,0.")

