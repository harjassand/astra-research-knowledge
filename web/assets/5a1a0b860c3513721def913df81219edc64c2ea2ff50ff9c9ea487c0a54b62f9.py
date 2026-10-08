"""Post-baseline exact audit of the authorized spin-5/2 originator witness."""
from sympy import Rational as R, Matrix, sqrt, simplify, eye, factorial, symbols, I

# Same self-contained classical Racah factorial definition used in blind replay.
def triangle(a,b,c):
    if c<abs(a-b) or c>a+b or (a+b+c).q!=1: return R(0)
    return sqrt(factorial(a+b-c)*factorial(a-b+c)*factorial(-a+b+c)/factorial(a+b+c+1))
def sixj(a,b,c,d,e,f):
    pref=triangle(a,b,c)*triangle(a,e,f)*triangle(d,b,f)*triangle(d,e,c)
    if pref==0: return R(0)
    lo=max(a+b+c,a+e+f,d+b+f,d+e+c); hi=min(a+b+d+e,a+c+d+f,b+c+e+f)
    return simplify(pref*sum((-1)**z*factorial(z+1)/(
        factorial(z-a-b-c)*factorial(z-a-e-f)*factorial(z-d-b-f)*factorial(z-d-e-c)
        *factorial(a+b+d+e-z)*factorial(a+c+d+f-z)*factorial(b+c+e+f-z)
    ) for z in range(int(lo),int(hi)+1)))

j=R(5,2); n=5; d=6; K=j
labels=list(range(6))
U=Matrix([[sqrt((2*L+1)*(2*J+1))*sixj(j,j,L,j,K,J) for J in labels] for L in labels])
assert simplify(U*U.T)==eye(6)
h=[Matrix.diag(*[simplify(d*(-1)**(n+J+l)*sixj(j,j,l,j,j,J)) for J in labels]) for l in labels]
G=[simplify(U*M*U.T).extract([3,5],[3,5]) for M in h]
v=Matrix([1,1])/sqrt(2)
lam=[simplify((v.T*M*v)[0]) for M in G][1:]
expected=[R(3,5),R(31,100)+5*sqrt(77)/588,R(31,105)+25*sqrt(77)/882,R(1,7)+13*sqrt(77)/294,R(109,924)+13*sqrt(77)/396]
assert all(simplify(a-b)==0 for a,b in zip(lam,expected))
assert all(a.is_positive is True for a in lam)
assert simplify(18*G[4])==Matrix([[R(33,14),39*sqrt(77)/49],[39*sqrt(77)/49,R(39,14)]])
print('EXACT channel lambda:',lam)
print('EXACT rank4 star 18 G4:',simplify(18*G[4]))

# Independent seed profile computation using Casimir spectral projectors,
# rather than the originator profile table or floating tensor/Choi replay.
ms=[j-k for k in range(d)]
Jz=Matrix.diag(*ms)
Jp=Matrix(d,d,lambda a,b:sqrt((j-ms[b])*(j+ms[b]+1)) if ms[a]==ms[b]+1 else 0)
Jm=Jp.T
Jx=(Jp+Jm)/2; Jy=(Jp-Jm)/(2*I)
spins=[Jx,Jy,Jz]
def casimir(X): return simplify(2*j*(j+1)*X-2*sum((M*X*M for M in spins),Matrix.zeros(d)))
def rank_component(X,l):
    out=X
    for k in range(n+1):
        if k==l: continue
        out=simplify((casimir(out)-k*(k+1)*out)/(l*(l+1)-k*(k+1)))
    return out
eta=Matrix([R(2,3),0,0,sqrt(5)/3,0,0])
rho=eta*eta.T
assert simplify(rho.trace())==1
components=[rank_component(rho,l) for l in range(n+1)]
assert simplify(sum(components,Matrix.zeros(d)))==rho
r=[simplify(d*(rho*M).trace()) for M in components][1:]
assert r==[R(5,21),0,R(40,27),2,R(242,189)]
print('EXACT eta rank profile from spin Casimir:',r)

coh=Matrix([1,0,0,0,0,0]); coh_rho=coh*coh.T
cohr=[simplify(d*(coh_rho*rank_component(coh_rho,l)).trace()) for l in range(1,n+1)]
cat=Matrix([1,0,0,0,0,1])/sqrt(2); catrho=cat*cat.T
catr=[simplify(d*(catrho*rank_component(catrho,l)).trace()) for l in range(1,n+1)]
assert [cohr[1],cohr[3]]==[R(25,14),R(3,14)]
assert [catr[1],catr[3]]==[R(25,14),R(3,14)]
assert sum(r[1::2])==2
print('EXACT coherent r profile:',cohr)
print('EXACT cat r profile:',catr)

mixg=[simplify((cohr[l-1]+r[l-1])/(2*(2*l+1))) for l in range(1,n+1)]
slack=[simplify(g-(2*l-1)) for g,l in zip(mixg,lam)]
assert all(x.is_positive is True for x in slack)
print('EXACT repaired mixture g:',mixg)
print('EXACT C2 slack g-(2lambda-1):',slack)
margin=simplify(18*lam[3]-R(129,14))
assert margin.is_positive is True
print('EXACT restricted-hull failure margin:',margin)
print('PASS: all checked algebraically; no floating spectra or dense Choi premise.')

# All-j formula is an affine-image identity; unrestricted q simplex is invalid.
# Check negative coefficients already at spin 3/2 for rank1, symmetric L1.
assert simplify(4*3*sixj(R(3,2),R(3,2),1,R(3,2),R(3,2),1))==-R(11,5)
print('PASS: formula20 coefficient -11/5 at j=3/2,L=1 disproves whole-q-simplex attainability.')
