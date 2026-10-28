"""Integer Cayley charts and exact acoustic blow-up for a two-site lattice."""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,math
import numpy as np
BASE=Path(__file__).parent

def one_poly(R,n):
    out=[(0,0) for _ in range(2*n+1)]
    for j in range(2*abs(R)+1):
      a,b=[(1,0),(0,1),(-1,0),(0,-1)][j%4]
      if R<0:b=-b
      for k in range(n-abs(R)+1):
        m=math.comb(2*abs(R),j)*math.comb(n-abs(R),k);idx=j+2*k
        x,y=out[idx];out[idx]=(x+m*a,y+m*b)
    return out

def load_laurent():
    data=json.loads((BASE/'MODEL.json').read_text());rows=data['coefficients']
    vals=[F(v) for row in rows for a in row['matrix'] for v in a]
    den=math.lcm(*(x.denominator for x in vals));coeff={}
    for row in rows:coeff[tuple(row['R'])]=np.array([[int(F(v)*den) for v in a] for a in row['matrix']],dtype=object)
    n=tuple(max(abs(r[j]) for r in coeff) for j in range(3))
    return coeff,den,n

def cayley(coeff,n,signs):
    shape=tuple(2*x+1 for x in n)+(6,6);re=np.zeros(shape,dtype=object);im=re.copy()
    for R,A in coeff.items():
        ps=[one_poly(R[j],n[j]) for j in range(3)]
        sgn=1 if sum(signs[j]*R[j] for j in range(3))%2==0 else -1
        for idx in itertools.product(*(range(len(x)) for x in ps)):
            a,b=1,0
            for j in range(3):c,d=ps[j][idx[j]];a,b=a*c-b*d,a*d+b*c
            if a:re[idx]+=sgn*a*A
            if b:im[idx]+=sgn*b*A
    assert np.array_equal(re,np.swapaxes(re,-1,-2))
    assert np.array_equal(im,-np.swapaxes(im,-1,-2))
    return re,im

def blowup(re,im,axis,sign):
    n=re.shape[:3];other=[j for j in range(3) if j!=axis]
    shape=(sum(x-1 for x in n)+1,n[other[0]],n[other[1]],6,6)
    out=[np.zeros(shape,dtype=object) for _ in range(2)]
    Z=np.block([[np.eye(3,dtype=int),np.eye(3,dtype=int)],[np.eye(3,dtype=int),-np.eye(3,dtype=int)]]).astype(object)
    for part,arr in enumerate([re,im]):
      for idx in itertools.product(*(range(x) for x in n)):
        A=Z.T@arr[idx]@Z;total=sum(idx);u,v=idx[other[0]],idx[other[1]];sgn=sign**idx[axis]
        for i,j in itertools.product(range(6),repeat=2):
            if not A[i,j]:continue
            power=total-int(i<3)-int(j<3)
            assert power>=0,('acoustic divisibility failed',idx,i,j,A[i,j])
            out[part][power,u,v,i,j]+=sgn*A[i,j]
    return out

def basis_matrix(n,a,w):
    U=[]
    for i in range(n+1):
        U.append([sum((F(math.comb(j,k))*w**k*a**(j-k)*F(math.comb(i,k),math.comb(n,k)) for k in range(min(i,j)+1)),F(0)) for j in range(n+1)])
    den=math.lcm(*(x.denominator for row in U for x in row))
    return np.array([[int(x*den) for x in row] for row in U],dtype=object),den

def bernstein(re,im,lower):
    deg=tuple(x-1 for x in re.shape[:3]);den=1
    for axis in range(3):
        U,d=basis_matrix(deg[axis],F(lower[axis]),F(1-lower[axis]));den*=d
        def apply(A):
            z=np.tensordot(U,A,axes=(1,axis));return np.moveaxis(z,0,axis)
        re,im=apply(re),apply(im)
    return re,im,den

def charts():
    c,den,n=load_laurent()
    for signs in itertools.product([0,1],repeat=3):
        re,im=cayley(c,n,signs)
        if any(signs):
            r,i,d=bernstein(re,im,(-1,-1,-1));yield 'regular'+''.join(map(str,signs)),r,i,den*d
        else:
            for axis,sign in itertools.product(range(3),[-1,1]):
                r,i=blowup(re,im,axis,sign);r,i,d=bernstein(r,i,(0,-1,-1));yield f'acoustic{axis}{sign:+d}',r,i,den*d

def split(re,im,axis):
    """Midpoint de Casteljau; the common denominator is multiplied by 2^n."""
    n=re.shape[axis]-1
    L=np.zeros((n+1,n+1),dtype=object);R=L.copy()
    for i in range(n+1):
        for j in range(i+1):L[i,j]=(1<<(n-i))*math.comb(i,j)
        for j in range(n-i+1):R[i,i+j]=(1<<i)*math.comb(n-i,j)
    def apply(U,A):return np.moveaxis(np.tensordot(U,A,axes=(1,axis)),0,axis)
    return (apply(L,re),apply(L,im)),(apply(R,re),apply(R,im)),1<<n

def center(A):
    A=np.asarray(A,dtype=float)
    for n in [x-1 for x in A.shape[:3]]:
        w=np.array([math.comb(n,i)/(2**n) for i in range(n+1)])
        A=np.tensordot(w,A,axes=(0,0))
    return A

def approximate_whitener(re,im,den):
    B=(np.array(re,dtype=float)+1j*np.array(im,dtype=float))/float(den)
    M=center(re)/float(den)+1j*center(im)/float(den)
    w,V=np.linalg.eigh(M)
    if w[0]<=0:return None,float(w[0])
    S=V/np.sqrt(w)
    W=np.matmul(np.matmul(S.conj().T,B),S)
    ab=abs(W.real)+abs(W.imag);diag=np.diagonal(W.real,axis1=-2,axis2=-1)
    margin=float(np.min(diag-ab.sum(axis=-1)+abs(diag)))
    return S,margin

def exact_margin(re,im,den,S,bits=24):
    sr=np.rint(S.real*(1<<bits)).astype(np.int64).astype(object);si=np.rint(S.imag*(1<<bits)).astype(np.int64).astype(object)
    cr=re@sr-im@si;ci=re@si+im@sr
    wr=sr.T@cr+si.T@ci;wi=sr.T@ci-si.T@cr
    assert np.array_equal(wr,np.swapaxes(wr,-1,-2)) and np.array_equal(wi,-np.swapaxes(wi,-1,-2))
    diag=np.diagonal(wr,axis1=-2,axis2=-1)
    margins=diag-(abs(wr)+abs(wi)).sum(axis=-1)+abs(diag)
    margin=int(np.min(margins));norm=sum(int(x)**2 for x in sr.flat)+sum(int(x)**2 for x in si.flat)
    return margin,F(margin,den*norm),sr,si,bits
