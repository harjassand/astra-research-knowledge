from fractions import Fraction as Q
import json,time,pathlib
from itertools import product
start=time.perf_counter()
def rank(M):
    A=[[Q(x) for x in row] for row in M]
    r=0
    for j in range(len(A[0])):
        p=next((i for i in range(r,len(A)) if A[i][j]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r]
        v=A[r][j];A[r]=[x/v for x in A[r]]
        for i in range(r+1,len(A)):
            if A[i][j]:
                v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r

def kron(A,B):return [[A[i][j]*B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))] for i in range(len(A)) for k in range(len(B))]
W=[[2*int(i!=j) for j in range(4)] for i in range(4)]
# Hermitian rank-two kernel A=u u* -v v*, v=(1,-1,i,-i), u=(1,1,1,1).
# Its squared-entry matrix is exact and real.
points=[(1,0),(-1,0),(0,1),(0,-1)]
G=[[2*(1-a*c-b*d) for c,d in points] for a,b in points]
assert rank(W)==4
assert rank(G)==3
T=W;S=G
fixtures=[]
for q in range(1,4):
    assert rank(T)==4**q
    assert rank(S)==3**q
    fixtures.append({'q':q,'target_pair_matrix_rank':rank(T),'one_component_max_rank_bound':3**q,'circle_example_rank':rank(S),'mixture_count_lower_bound':(4**q+3**q-1)//(3**q)})
    if q<3:T=kron(T,W);S=kron(S,G)
result={'status':'PASS','scope':'exact ranks for q=1,2,3; written tensor-rank argument proves all q','fixtures':fixtures,'elapsed_seconds':time.perf_counter()-start}
pathlib.Path('work/cycle6/c02_s01/mixture_rank_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
