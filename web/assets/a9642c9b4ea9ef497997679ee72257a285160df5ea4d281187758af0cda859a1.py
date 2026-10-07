from low_rank_parity import *
from paired_phase_estimator import det_elimination, matmul, adjoint
from pathlib import Path
import json,time,random
start=time.perf_counter()

def holes(F):
    n=len(F);full=(1<<n)-1;out={}
    for retained in range(1<<n):
        ids=[i for i in range(n) if retained>>i&1]
        if len(ids)%2:continue
        out[full^retained]=sum((determinant([[F[i][j] for j in ids if j not in I]
                                           for i in I]).norm()
                               for I in combinations(ids,len(ids)//2)),Q(0))
    return out

def rayleigh(f,n,i,j):
    values={a:(-1 if a in (1,2,3) else 1) for a in range(n)};group=[Q(0)]*4
    for mask,c in f.items():
        sign=(-1)**((n-mask.bit_count())//2)
        for a in range(n):
            if a not in (i,j) and mask>>a&1:sign*=values[a]
        group[(int(mask>>i&1))+2*int(mask>>j&1)]+=c*sign
    return group,group[1]*group[2]-group[0]*group[3]

F4=[[G(x) for x in row] for row in [[0,0,1,1],[0,0,1,-1],[0,0,0,0],[0,0,0,0]]]
f4=holes(F4)
def defect(f):return f[3]*f[12]+f[5]*f[10]+f[9]*f[6]-f[0]*f[15]
assert defect(f4)==-2
edges=[(0,4),(0,5),(1,4),(1,5),(2,4),(2,5),(3,4)]
F6=[[G(x) for x in row] for row in [
 [0,0,1,1,Q(-1,4),0],[0,0,1,-1,Q(-1,4),0],[0,0,0,0,Q(1,4),0],
 [0,0,0,0,Q(1,4),0],[Q(1,4),Q(1,4),0,Q(-1,4),0,1],
 [Q(-1,4),Q(-1,4),Q(-1,4),Q(-1,4),1,0]]]
f6=holes(F6);g=dict(f6)
for i,j in edges:
    pair=(1<<i)|(1<<j);old=dict(g)
    for mask in g:
        if not mask&pair:g[mask]+=old.get(mask|pair,Q(0))
newpin={mask:g[mask] for mask in range(16) if not mask.bit_count()%2}
oldpin={mask:g[mask|48] for mask in range(16) if not mask.bit_count()%2}
assert oldpin==f4 and defect(newpin)==Q(28101,32768)
A=newpin[0]*newpin[15];h=[newpin[x]*newpin[15^x] for x in (3,5,9)]
B=(sum(h)-A)/2;L=[max(Q(0),x-B) for x in h]
assert B>=0 and sum(L)<=A

F=[[G(x) for x in row] for row in [[0,1,1,1,0,0],[0,0,0,0,1,1],
 [0,0,1,0,1,0],[1,0,0,0,0,0],[0,0,0,1,0,0],[1,0,1,0,0,0]]]
f=holes(F);raw,original=rayleigh(f,6,0,4);sq,power=rayleigh({s:w*w for s,w in f.items()},6,0,4)
assert raw==list(map(Q,[-11,-7,-9,-3])) and original==30
assert sq==list(map(Q,[-55,-9,-17,-3])) and power==-12
aux={s:w+(f.get(s|3,Q(0)) if not s&3 else 0) for s,w in f.items()}
assert rayleigh({s:w*w for s,w in aux.items()},6,0,4)[1]==-15
physical_triangle=bool(F[0][2] and F[5][2] and F[5][0]);assert physical_triangle

reject=[]
for n in (4,6):
    k=n//2;F=[[G(Q(1,4)*int(i==j)+int(j==(i+1)%n)) for j in range(n)] for i in range(n)]
    sets=list(combinations(range(n),k));W=Q(0);hard=Q(0);row=[Q(0)]*n;col=[Q(0)]*n
    for I in sets:
        for J in sets:
            w=determinant([[F[i][j] for j in J] for i in I]).norm();W+=w
            for i in I:row[i]+=w
            for j in J:col[j]+=w
            if not set(I)&set(J):hard+=w
    assert hard==2 and all(x==W/2 for x in row+col)
    assert W>=Q(len(sets))*Q(3,4)**n
    reject.append({'n':n,'unrestricted_weight':str(W),'hard_weight':str(hard),'acceptance':str(hard/W)})

def pf(A):
    if not A:return G(1)
    if len(A)%2:return G()
    ans=G()
    for j in range(1,len(A)):
        ids=[a for a in range(1,len(A)) if a!=j]
        ans+=((-1)**(j-1))*A[0][j]*pf([[A[a][b] for b in ids] for a in ids])
    return ans
rng=random.Random(1202);support_cases=0
for n in (2,3,4):
    for trial in range(4):
        F=[[G(rng.randrange(-1,2),rng.randrange(-1,2)) for j in range(n)] for i in range(n)]
        M=[[G() for j in range(2*n)] for i in range(2*n)]
        for i in range(n):
            for j in range(n):M[i][n+j]=F[i][j];M[n+j][i]=-F[i][j]
        for word in product('ERC',repeat=n):
            I=[i for i,t in enumerate(word) if t=='R'];J=[i for i,t in enumerate(word) if t=='C']
            selected=sorted(I+[n+j for j in J])
            left=bool(determinant([[F[i][j] for j in J] for i in I])) if len(I)==len(J) else False
            right=bool(pf([[M[i][j] for j in selected] for i in selected]))
            assert left==right
        support_cases+=1
res={'status':'PASS','scope':'Independent exact recomputation of finite consequential peer fixtures; universal proof and imported algorithm assessment separate',
     'l01_circulants':reject,'l04_rayleigh_original':str(original),'l04_rayleigh_square':str(power),
     'l04_aux_square':str(rayleigh({s:w*w for s,w in aux.items()},6,0,4)[1]),
     'l04_physical_site_triangle_0_2_5':physical_triangle,
     'l07_old_pin_defect':str(defect(oldpin)),'l07_rescued_pin_defect':str(defect(newpin)),
     'l07_recognizer_accepts_rescued_pin':True,'l10_support_cases':support_cases,
     'elapsed_seconds':time.perf_counter()-start}
Path('work/cycle6/c02_s01/reviews').mkdir(exist_ok=True)
Path('work/cycle6/c02_s01/reviews/CROSS_REVIEW_CHECKS.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
