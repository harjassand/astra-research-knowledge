"""Independent exact staged-gate/tag-lifetime receiver; no producer imports.

Reconstruct V from its two Kronecker-delta tensors, then apply each
controlled permutation and Hadamard literally. This certifies the finite
CP walk and Lyapunov arithmetic; its physical reduction is reviewed in prose.
"""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import hashlib, json, time

def main():
    start = time.perf_counter()
    here = Path(__file__).parent
    path = here.parent / "c_three_carrier_controller/LIFETIME_CERTIFICATE.json"
    raw = json.loads(path.read_text())
    a, b = F(raw["port"]["a"]), F(raw["port"]["b"])
    assert a == F(11, 14) and b == F(5, 14) and a*a+3*b*b == 1
    arr = list(permutations(range(3))); assert raw["tag_basis"] == [list(x) for x in arr]
    where = {x:i for i,x in enumerate(arr)}
    K = {}
    for labels in arr:
        for old in range(2):
            for m, logical, ref, final in product(range(2), repeat=4):
                # V=(a+b)(id_M tensor Bell_AR)+(b-a)SWAP_MR(id tensor Bell).
                amp = (a+b)*int(m == old and logical == ref)
                amp += (b-a)*int(ref == old and logical == m)
                amp *= F((-1)**(m*final), 2)
                if not amp: continue
                tags = list(labels) + [3]
                for control, x, y in [(old,0,1),(m,0,1),(ref,1,3),(m,1,2)]:
                    if control: tags[x],tags[y]=tags[y],tags[x]
                lost = tags.pop()
                remaining = sorted(set(tags)-{0})
                rename = ({x:i for i,x in enumerate(sorted(tags))} if lost == 0
                          else {0:0, **{x:i+1 for i,x in enumerate(remaining)}})
                new = tuple(rename[x] for x in tags)
                label = (logical,ref,lost)
                ij = (2*where[new]+final,2*where[labels]+old)
                mat=K.setdefault(label,{})
                mat[ij]=mat.get(ij,F(0))+amp
    K={label:{ij:v for ij,v in mat.items() if v}for label,mat in K.items()}
    supplied={(z["source_logical_traced"],z["R_discarded"],z["discarded_tag"]):
              {(i,j):F(v)for i,j,v in z["entries"]}for z in raw["kraus"]}
    assert K == supplied
    n=12; G=[[F(x)for x in row]for row in raw["lyapunov_G"]]
    assert all(G[i][j] == G[j][i]for i in range(n)for j in range(n))
    def dual(B, survival):
        ans=[[F(0)for _ in range(n)]for _ in range(n)]
        for label,mat in K.items():
            if survival and label[2] == 0: continue
            for (u,i),x in mat.items():
                for (v,j),y in mat.items(): ans[i][j]+=x*B[u][v]*y
        return ans
    I=[[F(i==j)for j in range(n)]for i in range(n)]
    assert dual(I,False) == I
    S=dual(G,True)
    assert all(G[i][j]-S[i][j] == I[i][j]for i in range(n)for j in range(n))
    # Independent symmetric Schur elimination, retaining each positive pivot.
    R=[row[:] for row in G]; pivots=[]
    for k in range(n):
        p=R[k][k]; assert p>0; pivots.append(p)
        for i in range(k+1,n):
            for j in range(k+1,n): R[i][j]-=R[i][k]*R[k][j]/p
    assert [str(p)for p in pivots] == raw["G_strict_LDL_pivots"]
    upper=max(sum(abs(x)for x in row)for row in G)
    initial=sum(G[i][j]for i,j in product((0,1),repeat=2))/2
    assert upper == F(raw["uniform_lifetime_bound"]) < 16
    assert initial == F(raw["initial_plus_lifetime_bound"]) < 15
    out={"scope":"independent literal staged circuit, coherent tag CP map and lifetime arithmetic; physical collision bridge is separate",
         "no_producer_imports":True,"staged_Kraus_match":True,"CPTP_all144_entries":True,
         "G_minus_dual_G_equals_I_all144_entries":True,"strict_positive_pivots":len(pivots),
         "uniform_lifetime_upper":str(upper),"initial_plus_lifetime_upper":str(initial),
         "uniform_less_than":16,"initial_plus_less_than":15,
         "source_rank_substitutions":0,"trajectories":0,"optimizers":0,
         "seconds":time.perf_counter()-start,
         "input_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
         "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (here/"LIFETIME_INTAKE.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))

if __name__ == "__main__": main()
