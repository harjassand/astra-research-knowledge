"""Independent stdlib exact consumer of the angular heat certificate.

No Sympy, CVXPY, NumPy, symbolic strings, producer function or numerical
source is imported. Rebuilds the actual primitive derivative, heat density,
symmetries, six determinants (fraction-free polynomial Bareiss), and every
univariate sign/root statement (integer primitive Sturm sequence).
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
from functools import reduce
import hashlib,json,time


def add(p,q,s=1):
    r=p.copy()
    for e,c in q.items():
        r[e]=r.get(e,0)+s*c
        if not r[e]:del r[e]
    return r


def scale(p,s):return {e:c*s for e,c in p.items()if c*s}


def mul(p,q):
    r={}
    for e,c in p.items():
        for f,d in q.items():
            a=tuple(x+y for x,y in zip(e,f));r[a]=r.get(a,0)+c*d
    return {e:c for e,c in r.items()if c}


def power(p,n):
    r={tuple(0 for _ in next(iter(p))):1}
    for _ in range(n):r=mul(r,p)
    return r


def deriv(p,k):
    r={}
    for e,c in p.items():
        if e[k]:
            f=list(e);f[k]-=1;r[tuple(f)]=c*e[k]
    return r


def coord(p,k):
    return {tuple(e[j]+(j==k)for j in range(len(e))):c for e,c in p.items()}


def permute(p,permutation,signs):
    out={}
    for e,c in p.items():
        f=[0]*len(e)
        for j in range(len(e)):f[permutation[j]]+=e[j];c*=signs[j]**e[j]
        out[tuple(f)]=c
    return out


def exact_divide(p,q):
    assert q;r=p.copy();quotient={};qe=max(q);qc=q[qe]
    while r:
        re=max(r);rc=r[re];e=tuple(a-b for a,b in zip(re,qe))
        assert min(e)>=0 and rc%qc==0
        c=rc//qc;quotient[e]=quotient.get(e,0)+c
        r=add(r,{tuple(a+b for a,b in zip(e,f)):c*d for f,d in q.items()},-1)
    return quotient


def bareiss(M):
    a=[[p.copy()for p in row]for row in M];n=len(a);previous={(0,0):1};minors=[]
    for k in range(n):
        pivot=a[k][k];assert pivot;minors.append(pivot)
        if k==n-1:break
        for i in range(k+1,n):
            for j in range(k+1,n):
                a[i][j]=exact_divide(add(mul(pivot,a[i][j]),mul(a[i][k],a[k][j]),-1),previous)
        previous=pivot
    return minors


def trim(p):
    while p and p[-1]==0:p.pop()
    return p


def primitive(p):
    p=trim(p.copy())
    if not p:return p
    g=reduce(gcd,(abs(x)for x in p));return [x//g for x in p]


def uadd(p,q,s=1):
    r=p.copy()+[0]*max(0,len(q)-len(p))
    for i,c in enumerate(q):r[i]+=s*c
    return trim(r)


def umul(p,q):
    r=[0]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):r[i+j]+=c*d
    return trim(r)


def evaluate(p,x):
    value=0
    for c in reversed(p):value=value*x+c
    return value


def endpoint_strip(p):
    p=p.copy();multiplicities=[]
    for root in (-1,1):
        count=0
        while len(p)>1 and evaluate(p,root)==0:
            q=[0]*(len(p)-1);q[-1]=p[-1]
            for j in range(len(q)-2,-1,-1):q[j]=p[j+1]+root*q[j+1]
            assert p[0]+root*q[0]==0;p=trim(q);count+=1
        multiplicities.append(count)
    return p,multiplicities


def positive_pseudoremainder(a,b):
    # abs(lc b) keeps EVERY rescaling positive, preserving Sturm signs.
    r=primitive(a);b=primitive(b);lc=b[-1];s=1 if lc>0 else -1
    while len(r)>=len(b):
        degree=len(r)-len(b);lead=r[-1]
        r=uadd([abs(lc)*v for v in r],[0]*degree+[s*lead*v for v in b],-1)
        r=primitive(r)
    return r


def sturm_no_roots(p):
    q,removed=endpoint_strip(p);q=primitive(q);assert q
    derivative=primitive([j*q[j]for j in range(1,len(q))]);chain=[q]
    if derivative:
        chain.append(derivative)
        while True:
            r=positive_pseudoremainder(chain[-2],chain[-1])
            if not r:break
            chain.append([-v for v in r])
    def signs(x):return [(value>0)-(value<0)for v in chain if (value:=evaluate(v,x))]
    def changes(s):return sum(a!=b for a,b in zip(s,s[1:]))
    left,right=signs(-1),signs(1);roots=changes(left)-changes(right)
    assert roots==0
    assert evaluate(p,0)>0
    return {'degree':len(p)-1,'endpoint_multiplicities':removed,
            'chain_degrees':[len(q)-1 for q in chain],
            'left_signs':left,'right_signs':right,'interior_roots':roots,'sign_at_zero':1}


def main():
    started=time.perf_counter();here=Path(__file__).parent
    source=here/'PRIMITIVE_CERTIFICATE.json';raw=json.loads(source.read_text())
    assert raw['denominator']=='T=a²+b²+c²+d²'
    D=1
    for i,e,c in raw['primitive_terms']:D=lcm(D,F(c).denominator)
    P=[{}for _ in range(4)]
    for i,e,c in raw['primitive_terms']:
        assert 0<=i<4 and sum(e)==5 and len(e)==4
        v=F(c)*D;assert v.denominator==1 and tuple(e)not in P[i]
        P[i][tuple(e)]=v.numerator
    # Literal continuous and discrete primitive symmetries.
    Jaction=((2,-1),(3,-1),(0,1),(1,1));Jtranspose=((2,1),(3,1),(0,-1),(1,-1))
    for j in range(4):
        lie={}
        for k,(index,sign)in enumerate(Jaction):lie=add(lie,coord(deriv(P[j],k),index),sign)
        index,sign=Jtranspose[j];lie=add(lie,P[index],sign);assert not lie
        assert not add(P[j],scale(permute(P[j],(0,1,2,3),(1,-1,-1,1)),(1,-1,-1,1)[j]))
        swap=(1,0,3,2);assert not add(P[j],permute(P[swap[j]],swap,(1,1,1,1)))
    T={tuple(2*(k==i)for k in range(4)):1 for i in range(4)}
    q={(1,0,0,1):1,(0,1,1,0):-1}
    X={tuple(2*(k==i)for k in range(4)):sign for i,sign in enumerate((1,-1,1,-1))}
    Y={(1,1,0,0):2,(0,0,1,1):2};Z=scale(q,2)
    Fstar=add(add(mul(T,T),mul(q,q),12),mul(q,X),4)
    T2=mul(T,T);B1=(0,1,3,4);B2=(1,2,4,5)
    C=[[{}for j in range(6)]for i in range(6)]
    for i in range(4):
        for j in range(4):
            H=scale(mul(T2,deriv(deriv(Fstar,i),j)),2*D)
            for B in (B1,B2):C[B[i]][B[j]]=add(C[B[i]][B[j]],H)
            Omega=add(mul(T,add(deriv(P[j],i),deriv(P[i],j),-1)),
                      add(coord(P[j],i),coord(P[i],j),-1),-2)
            C[B1[i]][B2[j]]=add(C[B1[i]][B2[j]],Omega)
            C[B2[j]][B1[i]]=add(C[B2[j]][B1[i]],Omega)
    assert all(C[i][j]==C[j][i]for i in range(6)for j in range(6))
    def canonical(p):
        r={}
        for e,c in p.items():
            if e[2]==0:r[(e[1],e[3])]=r.get((e[1],e[3]),0)+c
        return {e:c for e,c in r.items()if c}
    matrix=[[canonical(p)for p in row]for row in C]
    mapped=time.perf_counter();minors=bareiss(matrix);det_time=time.perf_counter()-mapped
    checks=[];exception=None
    for row,actual in zip(raw['leading_minor_factorizations'],minors):
        k=row['k'];product={(0,0):1}
        for index,factor in enumerate(row['factors']):
            f={tuple(e):int(c)for e,c in factor['terms']};assert all(F(c).denominator==1 for e,c in factor['terms'])
            product=mul(product,power(f,factor['power']))
            assert all(e[0]%2==0 for e in f)
            maxpower=max(e[0]for e in f)//2
            slices=[]
            for j in range(maxpower+1):
                p=[0]*(1+max(e[1]for e in f))
                for e,c in f.items():
                    if e[0]==2*j:p[e[1]]+=c
                p=trim(p);slices.append(p)
                if not p:continue
                if (k,index,j)==(6,1,1):continue
                report=sturm_no_roots(p);report.update({'minor':k,'factor':index,'b2_power':j});checks.append(report)
            if (k,index)==(6,1):exception=slices
        constant=F(row['constant'])*(2*D)**k;assert constant>0
        assert set(actual)==set(product)
        assert all(F(actual[e])==constant*product[e]for e in product)
    assert exception is not None
    disc=uadd([4*v for v in umul(exception[0],exception[2])],umul(exception[1],exception[1]),-1)
    disc_report=sturm_no_roots(disc)
    # Pay the compact Euler/Hopf representative by an exact polynomial identity.
    R={}
    for i in range(4):R=add(R,coord(P[i],i))
    f_basis=[mul(T2,X),mul(T2,Z),power(X,3),mul(mul(X,X),Z),mul(X,mul(Z,Z)),power(Z,3)]
    pr_basis=[T2,mul(X,X),mul(X,Z),mul(Z,Z)]
    def combination(coefficients,basis):
        p={}
        for c,b in zip(coefficients,basis):
            c=F(c)*4*D;p=add(p,b,c)
        return p
    fnum=combination(raw['Hopf_f_coefficients'],f_basis)
    pnum=combination(raw['Hopf_p_coefficients'],pr_basis)
    rnum=combination(raw['Hopf_r_coefficients'],pr_basis)
    for i,(index,sign)in enumerate(Jaction):
        left=add(add(scale(mul(T,P[i]),4),mul(T,deriv(R,i)),-1),mul(R,deriv(T,i)))
        right=scale(coord(fnum,index),sign)
        right=add(right,mul(pnum,add(mul(Y,deriv(X,i)),mul(X,deriv(Y,i)),-1)))
        right=add(right,mul(rnum,add(mul(Y,deriv(Z,i)),mul(Z,deriv(Y,i)),-1)))
        assert left==right
    out={'scope':'literal rational angular ordinary-heat certificate; exact source/circuit-free mathematics',
         'primitive_term_count':sum(len(p)for p in P),'common_P_denominator':str(D),
         'global_primitive_symmetries':True,'independent_density_reconstruction':True,
         'all_six_polynomial_determinant_identities':True,
         'univariate_positive_checks':len(checks),'checks':checks,
         'exceptional_quadratic_discriminant':disc_report,
         'canonical_Hopf_Euler_identity':True,
         'conclusion':'all leading minors strictly positive for b²>=0,−1<d<1; boundary PSD by continuity; canonical symmetry cover gives global completion',
         'mapping_seconds':mapped-started,'bareiss_seconds':det_time,
         'total_seconds':time.perf_counter()-started,
         'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'random_draws':0,'solver_calls':0,'imported_symbolic_packages':0}
    (here/'LITERAL_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ('primitive_term_count','global_primitive_symmetries','all_six_polynomial_determinant_identities','univariate_positive_checks','canonical_Hopf_Euler_identity','mapping_seconds','bareiss_seconds','total_seconds')},indent=2))


if __name__=='__main__':main()
