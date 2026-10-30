"""Independent Fraction receiver of the degree-two closed-completion barrier.

Builds all 60 coefficients by sparse monomial rules; imports no symbolic
producer. Uses neither SDP nor floating-point positivity.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import hashlib,json,time

PAIRS=list(combinations(range(4),2))
MONOMS=[tuple((k==i)+(k==j) for k in range(4)) for i in range(4) for j in range(i,4)]
J=((0,0,-1,0),(0,0,0,-1),(1,0,0,0),(0,1,0,0))
K=((0,0),(0,1),(1,0),(0,0),(0,0),(0,-2))
B1=(0,1,3,4);B2=(1,2,4,5)


def add(p,q,factor=1):
    p=p.copy()
    for e,c in q.items():
        p[e]=p.get(e,0)+factor*c
        if not p[e]:del p[e]
    return p


def derivative(p,k):
    out={}
    for e,c in p.items():
        if e[k]:
            f=list(e);f[k]-=1;out[tuple(f)]=c*e[k]
    return out


def multiply_coordinate(p,k):
    out={}
    for e,c in p.items():
        f=list(e);f[k]+=1;out[tuple(f)]=c
    return out


def omega_basis(index):
    r,k=divmod(index,10);i,j=PAIRS[r]
    out=[[{} for j in range(4)]for i in range(4)]
    out[i][j]={MONOMS[k]:1};out[j][i]={MONOMS[k]:-1}
    return out


def evaluate(p,A):return sum(c*__import__('math').prod(x**e for x,e in zip(A,alpha))for alpha,c in p.items())


def wedge_matrix(O):
    out=[[F(0)for j in range(6)]for i in range(6)]
    for i in range(4):
        for j in range(4):
            r,s=B1[i],B2[j]
            out[r][s]+=F(O[i][j],2);out[s][r]+=F(O[i][j],2)
    return out


def rows_for_basis(O):
    result={}
    for i,j,k in combinations(range(4),3):
        p=add(add(derivative(O[j][k],i),derivative(O[i][k],j),-1),derivative(O[i][j],k))
        for e,c in p.items():result[('closed',i,j,k,e)]=c
    for i,j in PAIRS:
        p={}
        for k in range(4):
            for l in range(4):
                if J[k][l]:p=add(p,multiply_coordinate(derivative(O[i][j],k),l),J[k][l])
            if J[k][i]:p=add(p,O[k][j],J[k][i])
            if J[k][j]:p=add(p,O[i][k],J[k][j])
        for e,c in p.items():result[('lie',i,j,e)]=c
    # Signed permutations y_i=sign_i*x_(perm_i).
    for label,perm,signs in [('cc',(0,1,2,3),(1,-1,-1,1)),('swap',(1,0,3,2),(1,1,1,1))]:
        inverse=[perm.index(i)for i in range(4)]
        for i,j in PAIRS:
            r,s=inverse[i],inverse[j];p=O[i][j].copy()
            for e,c in O[r][s].items():
                f=[0]*4
                for k in range(4):f[perm[k]]+=e[k];c*=signs[k]**e[k]
                c*=signs[r]*signs[s];p=add(p,{tuple(f):c})
            for e,c in p.items():result[(label,i,j,e)]=c
    at=[[evaluate(p,(1,0,0,1))for p in row]for row in O]
    C=wedge_matrix(at)
    for i in range(6):
        for j in range(2):
            c=sum(C[i][l]*K[l][j]for l in range(6))
            if c:result[('kernel',i,j)]=c
    return result


def rref(a,rhs):
    a=[[F(v)for v in row]+[F(b)]for row,b in zip(a,rhs)];pivots=[];r=0
    for j in range(60):
        pivot=next((i for i in range(r,len(a))if a[i][j]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][j]:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        pivots.append(j);r+=1
    assert all(any(row[:-1]) or row[-1]==0 for row in a)
    return a[:r],pivots


def main():
    start=time.perf_counter();here=Path(__file__).parent
    columns=[rows_for_basis(omega_basis(i))for i in range(60)]
    # Fixed heat matrix C_F(I) from literal Hessian, independently expanded.
    H=((64,0,0,56),(0,0,-24,0),(0,-24,16,0),(56,0,0,16))
    CF=[[0]*6 for i in range(6)]
    for B in (B1,B2):
        for i in range(4):
            for j in range(4):CF[B[i]][B[j]]+=H[i][j]
    fixed={('kernel',i,j):-sum(CF[i][l]*K[l][j]for l in range(6))for i in range(6)for j in range(2)}
    keys=sorted(set(fixed).union(*(col.keys()for col in columns)),key=str)
    M=[[col.get(key,0)for col in columns]for key in keys];rhs=[fixed.get(key,0)for key in keys]
    R,pivots=rref(M,rhs);assert len(pivots)==59 and 59 not in pivots
    solution=[None]*60;solution[59]=(F(0),F(1))
    for row,k in zip(R,pivots):solution[k]=(row[-1],-row[59])
    # x(z) intercept/slope, not a sampled fit. Verify the entire affine map.
    assert all(sum(row[i]*solution[i][0]for i in range(60))==b and sum(row[i]*solution[i][1]for i in range(60))==0 for row,b in zip(M,rhs))
    def omega_at(A,component):
        out=[[F(0)for j in range(4)]for i in range(4)]
        for index in range(60):
            r,k=divmod(index,10);i,j=PAIRS[r]
            v=solution[index][component]*evaluate({MONOMS[k]:1},A)
            out[i][j]+=v;out[j][i]-=v
        return out
    # Full literal Hessian of Fstar is produced by elementary monomial rules.
    # Independent target monomial dictionary is T²+12q²+4qx.
    polynomial={}
    def product(p,q):
        out={}
        for e,c in p.items():
            for f,d in q.items():out=add(out,{tuple(x+y for x,y in zip(e,f)):c*d})
        return out
    T={tuple(2*(k==i)for k in range(4)):1 for i in range(4)}
    q={(1,0,0,1):1,(0,1,1,0):-1};x={tuple(2*(k==i)for k in range(4)):sign for i,sign in enumerate((1,-1,1,-1))}
    polynomial=add(add(product(T,T),product(q,q),12),product(q,x),4)
    def density(A,h):
        b1=[h[i]for i in B1];b2=[h[i]for i in B2]
        HF=[[evaluate(derivative(derivative(polynomial,i),j),A)for j in range(4)]for i in range(4)]
        fixed=sum(HF[i][j]*(b1[i]*b1[j]+b2[i]*b2[j])for i in range(4)for j in range(4))
        values=[]
        for n in range(2):
            Om=omega_at(A,n)
            values.append((fixed if n==0 else 0)+sum(Om[i][j]*b1[i]*b2[j]for i in range(4)for j in range(4)))
        return values
    h=(0,1,0,0,0,-2)
    plus=density((F(9,8),0,0,1),h);minus=density((F(7,8),0,0,1),h)
    assert plus==[F(-1,4),F(7,64)]
    assert minus==[F(-1,4),F(-25,64)]
    assert [25*plus[i]+7*minus[i]for i in range(2)]==[F(-8),F(0)]
    out={'scope':'all closed homogeneous degree2 coefficient completions after exact symmetry averaging; no SOS',
         'rank':len(pivots),'unknowns':60,'free_index':59,
         'affine_coefficients':[[str(v)for v in pair]for pair in solution],
         'base_plus':['9/8','0','0','1'],'base_minus':['7/8','0','0','1'],
         'same_compatible_hessian':list(h),
         'density_plus':'(7z-16)/64','density_minus':'(-25z-16)/64',
         'positive_weighted_sum':'25*density_plus+7*density_minus=-8',
         'conclusion':'infeasible, independent of SOS or any SDP status',
         'seconds':time.perf_counter()-start,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (here/'QUADRATIC_EXACT_RECEIVER.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ('scope','rank','unknowns','density_plus','density_minus','positive_weighted_sum','seconds')},indent=2))


if __name__=='__main__':main()
