"""Independent exact rational replay. Python standard library only.

Determinants use the Leibniz permutation formula and sparse Fraction
polynomials, rather than the CAS path that generated the certificate.
Congruence scaling by 1/sqrt(2) on the two u nodes removes radicals.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib,json,time

OUT=Path(__file__).resolve().parent
ZERO=(0,0,0)

def add(*polys):
    out={}
    for P in polys:
        for m,c in P.items():out[m]=out.get(m,F(0))+c
    return {m:c for m,c in out.items() if c}

def scale(P,c):return {m:c*v for m,v in P.items() if c*v}

def mul(A,B):
    out={}
    for m,x in A.items():
        for n,y in B.items():
            k=tuple(m[i]+n[i] for i in range(3))
            out[k]=out.get(k,F(0))+x*y
    return {m:c for m,c in out.items() if c}

def lin(v):
    return {tuple(int(i==j) for i in range(3)):F(c) for j,c in enumerate(v) if c}

def determinant(M):
    n=len(M);out={}
    for perm in permutations(range(n)):
        inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        product={ZERO:F((-1)**inversions)}
        for i,j in enumerate(perm):
            product=mul(product,M[i][j])
            if not product:break
        out=add(out,product)
    return out

def parityblock(w,K,i):
    j,k=[u for u in range(3) if u!=i]
    diag=[scale(K[i],5),add(scale(K[i],3),scale(K[j],2)),add(scale(K[i],3),scale(K[k],2)),scale(add(K[i],scale(K[j],4)),F(1,2)),scale(add(K[i],scale(K[k],4)),F(1,2))]
    M=[[{} for _ in range(5)] for _ in range(5)]
    for u,x in enumerate(diag):M[u][u]=x
    for u,v,x in [(0,3,scale(w[k],-5)),(1,3,scale(w[k],-5)),(0,4,scale(w[j],-5)),(2,4,scale(w[j],-5)),(3,4,scale(w[i],F(-5,2)))]:M[u][v]=M[v][u]=x
    return M

def oddblock(w,K):
    M=[[{} for _ in range(3)] for _ in range(3)]
    for i in range(3):
        M[i][i]=add(scale(K[i],2),*K)
        for j in range(i+1,3):M[i][j]=M[j][i]=scale(w[3-i-j],-5)
    return M

def run():
    started=time.perf_counter()
    certpath=OUT/'triaxial_symbolic_certificate.json'
    data=json.loads(certpath.read_text())
    inputs={
      'A_allactive':[(2,3,1),(1,3,1),(1,2,1)],
      'B1_twoactive':[(2,2,1),(1,1,1),(1,0,0)],
      'B2_twoactive':[(2,3,1),(1,3,1),(1,2,0)],
      'C_oneactive':[(2,2,1),(1,1,0),(1,0,0)],
    }
    checks=[]
    for cone in data['cones']:
        name=cone['name'];a=[lin(x) for x in inputs[name]]
        if name.startswith('A'):
            z=[add(*(a[j] for j in range(3) if j!=i),scale(a[i],-1)) for i in range(3)]
        elif name.startswith('B'):
            z=[scale(add(scale(a[1],2),scale(a[0],-1)),F(2,3)),scale(add(scale(a[0],2),scale(a[1],-1)),F(2,3)),scale(add(a[0],a[1]),F(2,3))]
        else:z=[{},a[0],a[0]]
        w=[mul(x,x) for x in a]
        K=[add(*(w[j] for j in range(3) if j!=i),mul(z[i],z[i])) for i in range(3)]
        assert all(P and all(c>=0 for c in P.values()) for P in K)
        matrices={f'parity{i+1}':parityblock(w,K,i) for i in range(3)}
        matrices['odd']=oddblock(w,K)
        for label,record in cone['minors'].items():
            kind,size=label.split('_leading');size=int(size)
            M=matrices[kind];P=determinant([row[:size] for row in M[:size]])
            # Each scaled u node multiplies its leading determinant by 1/2.
            undo=2 if kind.startswith('parity') and size==4 else 4 if kind.startswith('parity') and size==5 else 1
            P=scale(P,undo)
            expected={tuple(term['powers']):F(term['coefficient']) for term in record['positive_terms']+record['negative_terms']}
            assert P==expected,(name,label)
            assert P and all(c>=0 for c in P.values()),(name,label)
            checks.append({'cone':name,'minor':label,'term_count':len(P),'nonzero':True,'all_coefficients_nonnegative':True,'CAS_coefficients_match':True,'min_nonzero_coefficient':str(min(P.values()))})
    report={'status':'PASS','certificate_sha256':hashlib.sha256(certpath.read_bytes()).hexdigest(),'checks':checks,'checked_count':len(checks),'seconds':time.perf_counter()-started,'method':'stdlib Fraction polynomial arithmetic and Leibniz permutation determinant; independent from SymPy generation'}
    (OUT/'independent_coefficient_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'checked_count':len(checks),'seconds':report['seconds'],'certificate_sha256':report['certificate_sha256']}))

if __name__=='__main__':run()
