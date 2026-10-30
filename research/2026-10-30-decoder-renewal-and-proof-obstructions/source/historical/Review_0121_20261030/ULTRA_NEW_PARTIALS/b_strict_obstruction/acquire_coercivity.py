"""Exact universal coercivity data; no source case or optimizer.

Independent monomial Hessian rules acquire a strict positive base for the
whole35 ROC cone and the actual Fstar acoustic orbit used in the proof.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import prod
import hashlib,json,time


def exponents(total,n):
    if n==1:yield(total,)
    else:
        for i in range(total+1):
            for tail in exponents(total-i,n-1):yield(i,)+tail


def hessian_monomial(p,A):
    out=[[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            c=p[i]*(p[j]-(i==j))
            if c:
                e=list(p);e[i]-=1;e[j]-=1
                out[i][j]=c*prod(a**n for a,n in zip(A,e))
    return out


def dot(v,M,w):return sum(v[i]*M[i][j]*w[j]for i in range(len(v))for j in range(len(w)))


def inverse(M):
    n=len(M);a=[[F(v)for v in row]+[F(i==j)for j in range(n)]for i,row in enumerate(M)]
    for j in range(n):
        k=next(i for i in range(j,n)if a[i][j]);a[j],a[k]=a[k],a[j]
        v=a[j][j];a[j]=[x/v for x in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[j])]
    return [row[n:]for row in a]


def determinant(M):
    a=[[F(x)for x in row]for row in M];d=F(1)
    for j in range(len(a)):
        k=next((i for i in range(j,len(a))if a[i][j]),None)
        if k is None:return F(0)
        if k!=j:a[k],a[j]=a[j],a[k];d=-d
        d*=a[j][j];v=a[j][j]
        for i in range(j+1,len(a)):
            c=a[i][j]/v
            for k in range(j+1,len(a)):a[i][k]-=c*a[j][k]
    return d


def main():
    start=time.perf_counter();here=Path(__file__).parent
    powers=list(exponents(4,4));e=[[int(i==j)for i in range(4)]for j in range(4)]
    points=e+[[x+y for x,y in zip(e[i],e[j])]for i,j in combinations(range(4),2)]
    two=[(1,0),(0,1),(1,1)];rows=[]
    for A in points:
        for eta in two:
            for xi in two:
                R=[eta[i]*xi[j]for i in range(2)for j in range(2)]
                rows.append([dot(R,hessian_monomial(p,A),R)for p in powers])
    assert len(rows)==90
    echelon={};selected=[]
    for n,row in enumerate(rows):
        v=[F(x)for x in row]
        for j,w in sorted(echelon.items()):
            c=v[j]
            if c:v=[x-c*y for x,y in zip(v,w)]
        pivot=next((j for j,x in enumerate(v)if x),None)
        if pivot is not None:
            c=v[pivot];echelon[pivot]=[x/c for x in v];selected.append(n)
    assert len(selected)==35
    base_inverse=inverse([rows[i]for i in selected])
    bound=max(sum(abs(v)for v in row)for row in base_inverse)
    assert all(sum(base_inverse[i][j]*rows[selected[j]][k]for j in range(35))==int(i==k)for i in range(35)for k in range(35))
    ell=[sum(row[i]for row in rows)for i in range(35)]
    # Frame S of six rank-one compatible Hessians, two copies of S3.
    S3=((2,1,1),(1,1,1),(1,1,2))
    shifted=[[F(S3[i][j])-F(i==j,4)for j in range(3)]for i in range(3)]
    minors=[determinant([row[:k]for row in shifted[:k]])for k in range(1,4)]
    assert minors==[F(7,4),F(5,16),F(3,64)]
    assert 4*2*39*6720==2096640<2**21
    # Literal Fstar, assembled without importing a frozen source or Sympy.
    def add(p,q,scale=1):
        p=p.copy()
        for a,c in q.items():p[a]=p.get(a,0)+scale*c
        return p
    def multiply(p,q):
        r={}
        for a,c in p.items():
            for b,d in q.items():
                n=tuple(x+y for x,y in zip(a,b));r[n]=r.get(n,0)+c*d
        return r
    T={tuple(2*(j==i)for j in range(4)):1 for i in range(4)}
    q={(1,0,0,1):1,(0,1,1,0):-1}
    x={tuple(2*(j==i)for j in range(4)):s for i,s in enumerate((1,-1,1,-1))}
    target=add(add(multiply(T,T),multiply(q,q),12),multiply(q,x),4)
    H=[[sum(target.get(p,0)*hessian_monomial(p,e[0])[i][j]for p in powers)for j in range(4)]for i in range(4)]
    assert H==[[12,0,0,12],[0,4,-4,0],[0,-4,4,0],[12,0,0,28]]
    assert dot([1,0,0,0],H,[0,0,0,1])+dot([0,1,0,0],H,[0,0,1,0])==8
    out={'scope':'universal full35 ROC base and normalized closed-wedge coercivity; no source case',
         'exponent_order':[list(p)for p in powers],
         'positive_functional_coefficients':ell,
         'evaluation_count':len(rows),'evaluation_matrix':rows,
         'independent_row_indices':selected,'rank':len(selected),
         'coefficient_inf_bound_over_ell':str(bound),
         'inverse':[[str(v)for v in row]for row in base_inverse],
         'frame_S3':[list(row)for row in S3],
         'S3_minus_quarterI_Sylvester':[str(v)for v in minors],
         'general_density_bound':6720,
         'quadratic_witness_bound':2**21,
         'actual_interpolation_constant':2096640,
         'literal_Fstar_Hessian_at_E11':H,
         'acoustic_matrix':'[[12x²+4y²,8xy],[8xy,4x²+28y²]]',
         'acoustic_determinant':'48x⁴+288x²y²+112y⁴',
         'seconds':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'random_draws':0,'solver_calls':0}
    (here/'COERCIVITY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ('rank','evaluation_count','coefficient_inf_bound_over_ell','S3_minus_quarterI_Sylvester','quadratic_witness_bound','seconds')},indent=2))


if __name__=='__main__':main()
