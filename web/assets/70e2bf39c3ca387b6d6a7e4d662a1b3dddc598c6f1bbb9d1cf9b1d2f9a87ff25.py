from itertools import product
import json, random
from pathlib import Path

class FiniteField:
    def __init__(self, p, binary=False): self.p=p; self.binary=binary
    def add(self,a,b): return a^b if self.binary else (a+b)%self.p
    def neg(self,a): return a if self.binary else (-a)%self.p
    def mul(self,a,b):
        if not self.binary: return a*b%self.p
        r=0
        while b:
            if b&1:r^=a
            b>>=1; a<<=1
            if a&256:a^=0x11b
        return r
    def power(self,a,e):
        r=1
        while e:
            if e&1:r=self.mul(r,a)
            a=self.mul(a,a);e>>=1
        return r
    def inv(self,a):
        assert a
        return self.power(a,254 if self.binary else self.p-2)

def run(F, seed):
    random.seed(seed); n=2;m=2;D=8;L=4;t=2
    add,mul,neg=F.add,F.mul,F.neg
    def zero(): return [[0]*m for _ in range(m)]
    def eye(): return [[int(i==j) for j in range(m)] for i in range(m)]
    def madd(A,B): return [[add(A[i][j],B[i][j]) for j in range(m)] for i in range(m)]
    def mscale(A,s): return [[mul(a,s) for a in row] for row in A]
    def mmul(A,B):
        C=zero()
        for i in range(m):
            for j in range(m):
                for k in range(m):C[i][j]=add(C[i][j],mul(A[i][k],B[k][j]))
        return C
    def scalar(A): return A[0][1]
    B=[[[random.randrange(0,7) if F.binary else random.randrange(101) for j in range(m)] for i in range(m)] for _ in range(n)]
    ai=[F.power(add(1,t),i+1) for i in range(n)]
    den=[0]+[F.inv(add(F.power(t,r),neg(1))) for r in range(1,2*D)]
    H=[[zero() for h in range(L+1)] for r in range(D)];H[0][0]=eye()
    C=[[zero() for h in range(L+1)] for r in range(D)]
    for r in range(1,D):
        for i in range(n): C[r][1]=madd(C[r][1],mscale(B[i],F.power(ai[i],r-1)))
        for h in range(1,L+1):
            z=zero()
            for s in range(1,r+1): z=madd(z,mmul(C[s][1],H[r-s][h-1]))
            H[r][h]=mscale(z,den[r])
    G=[[zero() for h in range(L+1)] for r in range(D)];G[0][0]=eye()
    for r in range(1,D):
        for h in range(L+1):
            z=zero()
            for s in range(1,r+1):
                for k in range(h+1): z=madd(z,mmul(mscale(H[s][k],F.power(t,s)),G[r-s][h-k]))
            G[r][h]=mscale(z,neg(1))
    # Kernel K[a][b][h], restricted to a+b<D.
    KC={}
    for a in range(D):
        for b in range(1,D-a):
            for h in range(1,L+1):
                z=zero()
                for c in range(b):
                    d=b-c
                    for k in range(h): z=madd(z,mmul(mmul(H[a][k],G[c][h-1-k]),C[d][1]))
                KC[a,b,h]=scalar(z)
    U=[]
    for i in range(n):
        M=[[0]*D for _ in range(D)]
        for r in range(1,D):
            for q in range(r):M[r][q]=mul(F.power(ai[i],r-q-1),den[r])
        U.append(M)
    def dmul(A,B):
        C=[[0]*D for _ in range(D)]
        for r in range(D):
            for q in range(D):
                for s in range(D):C[r][q]=add(C[r][q],mul(A[r][s],B[s][q]))
        return C
    Ops=[[[0]*D for _ in range(D)] for h in range(L+1)]
    for h in range(L+1):
        for w in product(range(n),repeat=h):
            bw=eye(); uw=[[int(r==q) for q in range(D)]for r in range(D)]
            for i in w:bw=mmul(bw,B[i]);uw=dmul(uw,U[i])
            coeff=scalar(bw)
            for r in range(D):
                for q in range(D):Ops[h][r][q]=add(Ops[h][r][q],mul(coeff,uw[r][q]))
    checked=0
    for h in range(1,L+1):
        for r in range(D):
            for q in range(r):
                d=r-q;pred=0
                for b in range(1,d+1):pred=add(pred,mul(KC[d-b,b,h],den[b+q]))
                assert pred==Ops[h][r][q],('Green',F.p,seed,h,r,q,pred,Ops[h][r][q]);checked+=1
    # Product P_j(y)=A(t^j y)...A(ty) C(y); compare each diagonal.
    diag=C
    for j in range(m+1):
        if j:
            nxt=[[zero() for h in range(L+1)] for r in range(D)]
            for r in range(D):
                for h in range(L+1):
                    nxt[r][h]=diag[r][h]
                    for s in range(1,r+1):
                        if h:nxt[r][h]=madd(nxt[r][h],mmul(mscale(C[s][1],F.power(t,j*s)),diag[r-s][h-1]))
            diag=nxt
        for r in range(1,D):
            for h in range(1,L+1):
                pred=0
                for a in range(r):pred=add(pred,mul(KC[a,r-a,h],F.power(t,(j+1)*a)))
                assert pred==scalar(diag[r][h]),('Diagonal',F.p,seed,j,r,h,pred,scalar(diag[r][h]));checked+=1
    return checked

def cauchy(F,d):
    M=[[F.inv(F.add(F.power(2,q+b),F.neg(1)))for b in range(1,d+1)]for q in range(d)]
    determinant=1
    for j in range(d):
        k=next((k for k in range(j,d)if M[k][j]),None)
        assert k is not None,('Cauchy singular',F.p,d)
        if k!=j:M[k],M[j]=M[j],M[k];determinant=F.neg(determinant)
        pivot=M[j][j];determinant=F.mul(determinant,pivot); inverse=F.inv(pivot)
        for k in range(j+1,d):
            coeff=F.mul(M[k][j],inverse)
            for q in range(j,d):M[k][q]=F.add(M[k][q],F.neg(F.mul(coeff,M[j][q])))
    assert determinant
    return determinant

out={'scope':'Exact finite-field Green/operator and shifted-diagonal identities. These do not prove the universal theorem.', 'fixtures':[]}
for F in (FiniteField(101),FiniteField(2,True)):
    count=sum(run(F,seed)for seed in range(10))
    determinants={str(d):cauchy(F,d)for d in range(1,9)}
    out['fixtures'].append({'field':'GF(2^8), AES polynomial'if F.binary else 'GF(101)','t':2,'models':10,'n':2,'m':2,'z_dimension':8,'lambda_degree_checked':4,'identity_equalities':count,'cauchy_determinants':determinants})
path=Path(__file__).with_name('Q_GREEN_EXACT_CHECKS.json');path.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
