"""Independent stdlib integer/Fraction acquisition of the full35 face.

No Sympy/CVXPY or producer matrix generator is imported. Monomial Hessian
and first-derivative rules are expanded directly before orbit substitution.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,time


def exponents(total,n):
    if n==1:yield(total,)
    else:
        for j in range(total+1):
            for tail in exponents(total-j,n-1):yield(j,)+tail


def rank(matrix):
    a=[[F(v) for v in row] for row in matrix];r=0;pivots=[]
    for j in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];p=a[r][j]
        a[r]=[v/p for v in a[r]]
        for i in range(r+1,len(a)):
            if a[i][j]:
                p=a[i][j];a[i]=[x-p*y for x,y in zip(a[i],a[r])]
        pivots.append(j);r+=1
    return r,pivots


def add(p,q,scale=1):
    out=p.copy()
    for e,c in q.items():out[e]=out.get(e,0)+scale*c
    return {e:c for e,c in out.items()if c}


def multiply(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            exponent=tuple(x+y for x,y in zip(e,f));out[exponent]=out.get(exponent,0)+c*d
    return out


def literal_target():
    T={tuple(2*(k==i)for k in range(4)):1 for i in range(4)}
    q={(1,0,0,1):1,(0,1,1,0):-1}
    x={tuple(2*(k==i)for k in range(4)):s for i,s in enumerate((1,-1,1,-1))}
    return add(add(multiply(T,T),multiply(q,q),12),multiply(q,x),4)


def diagonal_line(polynomial,R):
    # Univariate coefficients of literal F(R+tI), no symbolic producer.
    out=[F(0)]*5
    for exponent,c in polynomial.items():
        current=[F(c)]
        for k,n in enumerate(exponent):
            linear=[F(R[k]),F(k in (0,3))]
            for _ in range(n):
                nxt=[F(0)]*(len(current)+1)
                for i,v in enumerate(current):
                    for j,w in enumerate(linear):nxt[i+j]+=v*w
                current=nxt
        for i,v in enumerate(current):out[i]+=v
    return out


def main():
    start=time.perf_counter();here=Path(__file__).parent
    powers=list(exponents(4,4));rows={}
    # Variables before substitution: A4,eta2,xi2. Each Hessian term is
    # coefficient*A^alpha*eta^beta*xi^gamma. At the two zero orbits every
    # A entry and eta entry is one signed C or D.
    for orbit in range(2):
        amap=[(1,-1),(0,1),(0,1),(1,1)] if orbit==0 else [(0,1),(1,-1),(1,1),(0,1)]
        xi_nonzero=0 if orbit==0 else 1
        for variable in range(8):
            degree=3 if variable<6 else 4
            for k in range(degree+1):rows[(orbit,variable,k)]=[0]*35
            for col,p in enumerate(powers):
                for i in range(4):
                    for j in range(4):
                        coefficient=p[i]*(p[j]-(i==j))
                        if not coefficient:continue
                        e=list(p)+[0]*4;e[i]-=1;e[j]-=1
                        e[4+i//2]+=1;e[4+j//2]+=1
                        e[6+i%2]+=1;e[6+j%2]+=1
                        coefficient*=e[variable]
                        if not coefficient:continue
                        e[variable]-=1
                        if e[6+1-xi_nonzero]:continue
                        cpower=e[4];dpower=e[5]
                        for n,(cd,sign) in enumerate(amap):
                            coefficient*=sign**e[n]
                            if cd==0:cpower+=e[n]
                            else:dpower+=e[n]
                        assert cpower+dpower==degree
                        rows[(orbit,variable,dpower)][col]+=coefficient
    M=sorted(set(tuple(row) for row in rows.values()))
    producer=json.loads((here/'EXTREME_FACE.json').read_text())
    expected=[tuple(int(x) for x in row) for row in producer['constraint_matrix']]
    assert M==expected
    r,pivots=rank(M);assert r==33
    q2=[0]*35
    for e,c in [((2,0,0,2),1),((1,1,1,1),-2),((0,2,2,0),1)]:q2[powers.index(e)]=c
    polynomial=literal_target();target=[polynomial.get(p,0)for p in powers]
    assert target==[int(v)for v in producer['target_coefficients']]
    assert all(sum(x*y for x,y in zip(row,q2))==0 for row in M)
    assert all(sum(x*y for x,y in zip(row,target))==0 for row in M)
    assert any(q2[i]*target[j]!=q2[j]*target[i] for i in range(35) for j in range(35))
    plus=diagonal_line(polynomial,(0,200,-1,0));minus=diagonal_line(polynomial,(1,0,0,-2))
    upper=(plus[2]-plus[1]**2/(4*plus[0]))/200
    lower=(minus[2]-minus[1]**2/(4*minus[0]))/(-2)
    assert plus[1]==0 and plus[2]==4808 and minus[:3]==[97,-8,-48]
    assert upper==F(601,25) and lower-upper==F(103,2425)>0
    out={'scope':'independent whole35 necessary face and exact unrestrictedPC support gap',
         'matrix_rows':len(M),'rank':r,'nullity':35-r,'pivot_columns':pivots,
         'basis':'span{q²,Fstar}; G=a(T²+4qx)+bq²',
         'remaining_ROC_condition':'a>=0,b>=12a, imported exact aligned acoustic boundary',
         'PC_support_upper':str(upper),'PC_support_lower':str(lower),'strict_gap':str(lower-upper),
         'literal_Rplus_line':[str(v)for v in plus], 'literal_Rminus_line':[str(v)for v in minus],
         'matches_independent_symbolic_matrix':True,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'input_sha256':hashlib.sha256((here/'EXTREME_FACE.json').read_bytes()).hexdigest(),
         'seconds':time.perf_counter()-start,'random_draws':0,'ROC_samples':0}
    (here/'FACE_EXACT_RECEIVER.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
