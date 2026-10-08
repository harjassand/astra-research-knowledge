"""Exact local-monotonicity attack; no theorem promotion from finite enumeration."""
from itertools import combinations, combinations_with_replacement, permutations
from collections import defaultdict, deque
import json, time

def binary_rank(columns):
    piv={}
    for x in columns:
        while x:
            k=x.bit_length()-1
            if k in piv: x ^= piv[k]
            else:
                piv[k]=x
                break
    return len(piv)

def bases_fano():
    return [tuple(c) for c in combinations(range(7),3)
            if binary_rank([i+1 for i in c])==3]

def distance(A,B):
    return min(sum(len(set(x)-set(y)) for x,y in zip(A,P))
               for P in permutations(B))

def signature(A,n):
    return tuple(sum(e in b for b in A) for e in range(n))

def adjacent(A,bases_set):
    out=set()
    for i,j in combinations(range(len(A)),2):
        a,b=set(A[i]),set(A[j])
        for e in a-b:
            for f in b-a:
                ap=tuple(sorted((a-{e})|{f}))
                bp=tuple(sorted((b-{f})|{e}))
                if ap in bases_set and bp in bases_set:
                    C=list(A); C[i]=ap; C[j]=bp
                    C=tuple(sorted(C))
                    if C!=A: out.add(C)
    return out

def attack(name,bases,n=7,p=3):
    start=time.monotonic()
    bset=set(bases); fibers=defaultdict(list)
    for A in combinations_with_replacement(bases,p):
        fibers[signature(A,n)].append(A)
    tested=0
    for sig,F in sorted(fibers.items(),key=lambda kv:-len(kv[1])):
        if len(F)<2:continue
        neighbors={A:adjacent(A,bset) for A in F}
        for A in F:
            for B in F:
                if A==B:continue
                tested+=1
                d=distance(A,B)
                nb=[(C,distance(C,B)) for C in sorted(neighbors[A])]
                if all(dc>=d for C,dc in nb):
                    prev={A:None}; Q=deque([A])
                    while Q and B not in prev:
                        X=Q.popleft()
                        for Y in neighbors[X]:
                            if Y not in prev:
                                prev[Y]=X;Q.append(Y)
                    path=[]
                    if B in prev:
                        X=B
                        while X is not None:path.append(X);X=prev[X]
                        path.reverse()
                    return {"model":name,"n":n,"p":p,"bases":bases,"signature":sig,
                            "A":A,"B":B,"distance":d,"neighbors":nb,
                            "path":path,"path_distances":[distance(X,B) for X in path],
                            "fiber_size":len(F),"tested":tested,
                            "wall_seconds":time.monotonic()-start}
    return {"model":name,"n":n,"p":p,"status":"NO_STRICT_LOCAL_MINIMUM_FOUND",
            "fibers":len(fibers),"tested":tested,"wall_seconds":time.monotonic()-start}

if __name__=="__main__":
    b=bases_fano()
    results=[]
    for name,bases in [("Fano",b),("Fano_dual",[tuple(i for i in range(7) if i not in x) for x in b])]:
        results.append(attack(name,bases))
    print(json.dumps(results,indent=2))
