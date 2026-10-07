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

def run(F, seed, m=2):
    random.seed(seed); n=2;D=2*n*(m-1);L=m+1;t=2
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
    def scalar(A): return A[0][m-1]
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
    # Transfer coefficients, L=u H(z) H(y)^(-1) v, via H(y)^(-1)=G(y)A(y).
    LC={}
    for a in range(D):
        for b in range(D-a):
            for h in range(1,L+1):
                z=zero()
                for k in range(h+1):z=madd(z,mmul(H[a][k],G[b][h-k]))
                val=scalar(z)
                if b:val=add(val,KC[a,b,h])
                LC[a,b,h]=val
                if b:
                    assert KC[a,b,h]==mul(add(1,neg(F.power(t,b))),val),('Transfer difference',F.p,seed,m,a,b,h)
                    checked+=1
    # L(t^j y,y)=R_j(y)v, beginning at j=0, whose scalar is uv=0.
    rp=[[zero() for h in range(L+1)]for r in range(D)];rp[0][0]=eye()
    for j in range(m):
        if j:
            nxt=[[zero()for h in range(L+1)]for r in range(D)]
            for r in range(D):
                for h in range(L+1):
                    nxt[r][h]=rp[r][h]
                    for s in range(1,r+1):
                        if h:nxt[r][h]=madd(nxt[r][h],mmul(mscale(C[s][1],F.power(t,(j-1)*s)),rp[r-s][h-1]))
            rp=nxt
        for r in range(D):
            for h in range(1,L+1):
                val=0
                for a in range(r+1):val=add(val,mul(LC[a,r-a,h],F.power(t,j*a)))
                assert val==scalar(rp[r][h]),('Transfer diagonal',F.p,seed,m,j,r,h,val,scalar(rp[r][h]));checked+=1
    # Check exact finite all-word zero certificate by reachable row closure.
    reach=[];front=[eye()[0]]
    def rank(rows):
        rows=[row[:]for row in rows];r=0
        for c in range(m):
            pivot=next((i for i in range(r,len(rows))if rows[i][c]),None)
            if pivot is None:continue
            rows[r],rows[pivot]=rows[pivot],rows[r];iv=F.inv(rows[r][c])
            rows[r]=[mul(x,iv)for x in rows[r]]
            for i in range(len(rows)):
                if i!=r:
                    fac=rows[i][c]
                    rows[i]=[add(x,neg(mul(fac,y)))for x,y in zip(rows[i],rows[r])]
            r+=1
        return r
    while front:
        new=[]
        for row in front:
            if rank(reach+[row])>len(reach):
                reach.append(row)
                for bi in B:
                    rr=[0]*m
                    for c in range(m):
                        for k in range(m):rr[c]=add(rr[c],mul(row[k],bi[k][c]))
                    new.append(rr)
        front=new
    true_nonzero=any(row[m-1]for row in reach)
    compact_nonzero=any(any(any(row)for row in Ops[h])for h in range(m))
    assert compact_nonzero==true_nonzero,('Compact witness',F.p,seed,m)
    return checked, true_nonzero

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

out={'scope':'Exact transfer/difference/shifted-diagonal identities and compact marker detection, with independent all-word reachable-space zero certificates. These finite fixtures do not prove the universal theorem.', 'fixtures':[]}
for F in (FiniteField(101),FiniteField(2,True)):
    for m in (2,3):
        results=[run(F,seed,m)for seed in range(20)]
        out['fixtures'].append({'field':'GF(2^8), AES polynomial'if F.binary else 'GF(101)','t':2,'models':20,'n':2,'m':m,'z_dimension':4*(m-1),'marker_dimension':m,'lambda_degree_checked':m+1,'identity_equalities':sum(c for c,nz in results),'nonzero_models':sum(nz for c,nz in results),'all_word_equality_certificates':'reachable row-span stabilization'})
path=Path(__file__).with_name('TRANSFER_KERNEL_EXACT_CHECKS.json');path.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
