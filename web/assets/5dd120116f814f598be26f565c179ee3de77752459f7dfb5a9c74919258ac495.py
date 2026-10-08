"""Reconstruct Larson's published binary matroid and bounded buffered paths."""
from itertools import combinations
from collections import Counter
import json,time

ROWS=[
[0,0,1,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0],
[0,1,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0],
[0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,0,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1],
]
COLS=[sum(ROWS[j][i]<<j for j in range(9)) for i in range(18)]
ALL=(1<<18)-1

def mask(xs):return sum(1<<(x-1) for x in xs)
def labels(b):return [i+1 for i in range(18) if b>>i&1]
def rank(xs):
    piv={}
    for i in xs:
        x=COLS[i]
        while x:
            k=x.bit_length()-1
            if k in piv:x^=piv[k]
            else:piv[k]=x;break
    return len(piv)

def build_bases():
    return {sum(1<<i for i in xs) for xs in combinations(range(18),9) if rank(xs)==9}

def bitlist(m):
    out=[]
    while m:
        bit=m&-m;out.append(bit);m-=bit
    return out

def neighbors(S,bases):
    out=set()
    for i,j in combinations(range(len(S)),2):
        A,B=S[i],S[j]
        for e in bitlist(A&~B):
            for f in bitlist(B&~A):
                ap=A^e^f;bp=B^e^f
                if ap in bases and bp in bases:
                    T=list(S);T[i]=ap;T[j]=bp;T=tuple(sorted(T))
                    if T!=S:out.add(T)
    return out

def split_count(B):
    return sum(bool(B>>(2*i)&1)^bool(B>>(2*i+1)&1) for i in range(9))

def bidir(start,goal,bases,cap=100000):
    parents=[{start:None},{goal:None}]
    fronts=[{start},{goal}]; expanded=0;edgecount=0
    while fronts[0] and fronts[1] and expanded<cap:
        side=0 if len(fronts[0])<=len(fronts[1]) else 1
        new=set()
        for S in fronts[side]:
            expanded+=1
            for T in neighbors(S,bases):
                edgecount+=1
                if T in parents[side]:continue
                parents[side][T]=S;new.add(T)
                if T in parents[1-side]:
                    meet=T
                    left=[];X=meet
                    while X is not None:left.append(X);X=parents[0][X]
                    left.reverse()
                    right=[];X=parents[1][meet]
                    while X is not None:right.append(X);X=parents[1][X]
                    return {"status":"FOUND","path":left+right,"expanded":expanded,
                            "edges":edgecount,"seen":[len(x) for x in parents]}
            if expanded>=cap:break
        fronts[side]=new
    return {"status":"CAP_OR_EXHAUSTED","expanded":expanded,"edges":edgecount,
            "seen":[len(x) for x in parents],"remaining":[len(x) for x in fronts]}

if __name__=="__main__":
    starttime=time.monotonic();bases=build_bases()
    B=mask([1,2,3,7,8,9,13,14,15])
    D=mask([1,2,3,5,7,9,11,13,15])
    assert B in bases and (ALL^B) in bases and D in bases and (ALL^D) in bases
    paircounts=Counter(split_count(x) for x in bases if ALL^x in bases)
    R=bidir(tuple(sorted((B,B,ALL^B))),tuple(sorted((B,D,ALL^D))),bases)
    if "path" in R:
        P=R["path"]
        assert all(all(b in bases for b in S) for S in P)
        assert all(P[i+1] in neighbors(P[i],bases) for i in range(len(P)-1))
        for S in P:
            assert [sum(bool(b>>i&1) for b in S) for i in range(18)]==[
                2 if B>>i&1 else 1 for i in range(18)]
        R["path"]=[[labels(b) for b in S] for S in P]
        R["length"]=len(P)-1
    R.update({"source":"Larson2607.02208 Example1.4/Theorem1.5","rows":ROWS,
              "basis_count":len(bases),"complement_basis_split_counts":dict(paircounts),
              "buffer":labels(B),"B":labels(B),"D":labels(D),
              "wall_seconds":time.monotonic()-starttime})
    print(json.dumps(R,indent=2))

