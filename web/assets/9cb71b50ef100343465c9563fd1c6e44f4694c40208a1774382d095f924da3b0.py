"""Finite certificate of whether every basis variable kills the published degree-2 gap."""
from buffer_attack import *
from itertools import permutations
from collections import Counter
import json,time

def rref(rows):
    piv={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k in piv:x^=piv[k]
            else:piv[k]=x;break
    for k in sorted(piv):
        for j in list(piv):
            if j!=k and (piv[j]>>k)&1:piv[j]^=piv[k]
    return tuple(sorted(piv.values()))

def permute_bits(x,perm):
    return sum(((x>>i)&1)<<perm[i] for i in range(18))

def automorphisms():
    r=[sum(v<<i for i,v in enumerate(row)) for row in ROWS]
    canon=rref(r);out=[]
    for block in range(3):
        off=6*block
        for local in permutations(range(6)):
            perm=list(range(18))
            for i in range(6):perm[off+i]=off+local[i]
            if rref([permute_bits(row,perm) for row in r])==canon:
                lookup=[sum(((x>>i)&1)<<local[i] for i in range(6)) for x in range(64)]
                out.append({"kind":"block","block":block,"local":local,"lookup":lookup,"perm":perm})
    perm=[(i+6)%18 for i in range(18)]
    assert rref([permute_bits(row,perm) for row in r])==canon
    out.append({"kind":"cycle","perm":perm})
    return out

def act(x,g):
    if g["kind"]=="cycle":return ((x<<6)&ALL)|(x>>12)
    off=6*g["block"];old=(x>>off)&63
    return (x&~(63<<off))|(g["lookup"][old]<<off)

def all_pair_components(bases):
    V={tuple(sorted((x,ALL^x))) for x in bases if ALL^x in bases}
    unseen=set(V);out=[]
    while unseen:
        root=min(unseen);Q=[root];parent={root:None};unseen.remove(root)
        for S in Q:
            for T in sorted(neighbors(S,bases)):
                if T in unseen:unseen.remove(T);parent[T]=S;Q.append(T)
        out.append(parent)
    return out

if __name__=="__main__":
    started=time.monotonic();bases=build_bases();G=automorphisms()
    assert all(all(act(x,g) in bases for x in bases) for g in G)
    assert all(all({g['perm'][2*i]//2,g['perm'][2*i+1]//2}.__len__()==1
                   for i in range(9)) for g in G)
    unseen=set(bases);orbits=[]
    while unseen:
        root=min(unseen);Q=[root];parent={root:None};unseen.remove(root)
        for x in Q:
            for gi,g in enumerate(G):
                y=act(x,g)
                if y in unseen:unseen.remove(y);parent[y]=[x,gi];Q.append(y)
        orbits.append(parent)
    B=mask([1,2,3,7,8,9,13,14,15]);D=mask([1,2,3,5,7,9,11,13,15])
    comp=all_pair_components(bases)
    assert len(comp)==2
    assert {split_count(x[0]) for x in comp[0]}=={7,9}
    assert {split_count(x[0]) for x in comp[1]}=={3}
    paths=[]
    for O in orbits:
        C=next(iter(O))
        R=bidir(tuple(sorted((C,B,ALL^B))),tuple(sorted((C,D,ALL^D))),bases,cap=100000)
        if "path" in R:
            P=R["path"]
            assert all(all(x in bases for x in S) for S in P)
            assert all(P[i+1] in neighbors(P[i],bases) for i in range(len(P)-1))
            assert all([sum(bool(x>>i&1) for x in S) for i in range(18)]==
                       [2 if C>>i&1 else 1 for i in range(18)] for S in P)
        paths.append({"buffer_mask":C,"orbit_size":len(O),**R})
    certificate={"schema":"matroid.buffer-finite.v1","rows":ROWS,"B":B,"D":D,
                 "basis_count":len(bases),"automorphisms":[{k:v for k,v in g.items() if k!="lookup"} for g in G],
                 "orbit_parent_trees":[[[x,*parent] if parent else [x] for x,parent in O.items()] for O in orbits],
                 "pair_component_parent_trees":[[[*x,*parent] if parent else list(x) for x,parent in C.items()] for C in comp],
                 "representative_paths":paths,"wall_seconds":time.monotonic()-started}
    open("work/agents/independent/phase2/buffer_all_variables_certificate.json","w").write(json.dumps(certificate,separators=(",",":"))+"\n")
    print(json.dumps({"basis_count":len(bases),"automorphism_count":len(G),"orbit_sizes":[len(x) for x in orbits],
                      "results":[{k:v for k,v in x.items() if k!="path"} for x in paths],
                      "wall_seconds":certificate["wall_seconds"]},indent=2))

