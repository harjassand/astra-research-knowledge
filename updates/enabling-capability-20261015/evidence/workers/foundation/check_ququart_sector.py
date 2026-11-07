"""Exact separator of proposed sector from the located source scopes.
This checks one positive example, not the universal sector theorem.
"""
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

D=4
U=[(0,0,0),(0,1,1)]
X=[(1,0,1),(2,1,2),(3,2,3),(3,3,0)]
V=[(1,0,0),(1,1,1)]
Y=[(0,0,2),(2,1,0),(0,2,1),(3,3,2),(3,0,3)]


def matrix():
    entries={}
    for left,right in [(U,V),(X,Y)]:
        for a,b in product(left,right):
            entries[a,b]=entries.get((a,b),0)+1
    return entries


def trace_norm(entries,traced):
    out={}
    for (a,b),z in entries.items():
        if any(a[i]!=b[i] for i in traced):continue
        kept=[i for i in range(3) if i not in traced]
        key=tuple(a[i] for i in kept),tuple(b[i] for i in kept)
        out[key]=out.get(key,0)+z
    return sum(z*z for z in out.values())


def local_support_ranks(left,right):
    ranks=[]
    for site in range(3):
        columns=[]
        for words in [left,right]:
            for other in product(range(D),repeat=2):
                column=[0]*D
                for a in words:
                    if tuple(a[i] for i in range(3) if i!=site)==other:
                        column[a[site]]+=1
                if any(column):columns.append(column)
        a=[[Fraction(z) for z in row] for row in zip(*columns)]
        r=0
        for j in range(len(columns)):
            p=next((i for i in range(r,D) if a[i][j]),None)
            if p is None:continue
            a[r],a[p]=a[p],a[r]
            z=a[r][j];a[r]=[x/z for x in a[r]]
            for i in range(D):
                if i!=r:
                    z=a[i][j];a[i]=[x-z*y for x,y in zip(a[i],a[r])]
            r+=1
            if r==D:break
        ranks.append(r)
    return ranks


def main():
    groups=[set(w) for w in [U,X,V,Y]]
    disjoint=all(not(a&b) for a,b in combinations(groups,2))
    if not disjoint:raise RuntimeError("Disjoint-support rank/nilpotence proof failed")
    entries=matrix();terms=[];q=Fraction(0)
    for n in range(4):
        for traced in combinations(range(3),n):
            norm2=trace_norm(entries,traced)
            q+=Fraction(-1,2)**n*norm2
            terms.append({"traced":list(traced),"norm_squared":norm2})
    out_rank=local_support_ranks(U,X);in_rank=local_support_ranks(V,Y)
    if q!=Fraction(65,4) or out_rank!=[4,4,4] or in_rank!=[4,4,4]:
        raise RuntimeError("Exact expected identity failed")
    data={"status":"EXACT_INTEGER_AND_RATIONAL_CHECK_PASS","local_dimension":D,
          "vectors":{"u":U,"x":X,"v":V,"y":Y},"operator":"|u><v|+|x><y|",
          "four_vector_supports_pairwise_disjoint":disjoint,"rank":2,"nilpotence":"K^2=0",
          "output_local_support_ranks":out_rank,"input_local_support_ranks":in_rank,
          "partial_trace_norm_squared":terms,"q3":str(q),
          "scope":"One positive example in the proposed sector, not a universal theorem or physical operation",
          "analytic_separation":[
              "Range A0 slice is alpha*(|00>+|11>); fully product forces alpha=0, then x is entangled across A|BC.",
              "Input-range A1 slice is alpha*(|00>+|11>); same reasoning applies to y.",
              "Non-product biseparable u cannot lie in any locally orthogonal product code: A|BC rank one forces one codeword, which would be fully product.",
              "Nonzero nilpotence excludes normality; four disjoint vectors give combined support dimension four.",
              "Every one-site partial trace is nonzero; local input-output support overlaps are four.",
              "Full local ranks four exclude any three-qutrit tensor support; hence outside the October qutrit candidate scope."
          ]}
    Path(__file__).with_name("ququart_sector.json").write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({"status":data["status"],"q3":data["q3"],"local_support_ranks":[out_rank,in_rank]}))


if __name__=="__main__":main()
