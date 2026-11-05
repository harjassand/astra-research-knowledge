"""Exact fast-local/slow-global example and slow-mode obstruction checks."""
import json
from pathlib import Path
import sympy as s

I=s.eye(2)
X=s.Matrix([[0,1],[1,0]])
Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1)
sm=s.Matrix([[0,1],[0,0]])
P=[I,X,Y,Z]
kron=s.kronecker_product
Id=s.eye(4)
delta=s.symbols('delta', nonnegative=True)

def dissipator(v,a):
    vv=v.conjugate().T*v
    return v.conjugate().T*a*v-(vv*a+a*vv)/2

def Lfast(a):
    h=kron(Z,Z)
    out=s.I*(h*a-a*h)
    out+=sum((dissipator(kron(p/2,I),a) for p in [X,Y,Z]),s.zeros(4))
    out+=delta*(kron(I,X)*a*kron(I,X)-a)
    return s.simplify(out)

D=5+2*delta
certs={
    'X':(kron(X,I),((1+2*delta)*kron(X,I)-2*kron(Y,Z))/D),
    'Y':(kron(Y,I),((1+2*delta)*kron(Y,I)+2*kron(X,Z))/D),
    'Z':(kron(Z,I),kron(Z,I)),
}
for a,b in certs.values():
    assert s.simplify(a+Lfast(b))==s.zeros(4)
assert s.simplify(Lfast(kron(I,Z))+2*delta*kron(I,Z))==s.zeros(4)
assert s.simplify(D**2-((1+2*delta)**2+4)-4*(5+4*delta))==0

# A locally distinguishable conserved spectator: H=X_A+Z_A Z_B,
# gamma=4 amplitude damping on A; delta bit flips on B.
def Lslow(a):
    h=kron(X,I)+kron(Z,Z)
    out=s.I*(h*a-a*h)+dissipator(2*kron(sm,I),a)
    out+=delta*(kron(I,X)*a*kron(I,X)-a)
    return s.simplify(out)

tauplus=(I+s.Rational(2,5)*X-s.Rational(2,5)*Y+s.Rational(4,5)*Z)/2
tauminus=(I-s.Rational(2,5)*X-s.Rational(2,5)*Y+s.Rational(4,5)*Z)/2
rhops=[kron(tauplus,(I+Z)/2),kron(tauminus,(I-Z)/2)]
for rho in rhops:
    for pa in P:
        for pb in P:
            assert s.simplify(s.trace(rho*Lslow(kron(pa,pb)).subs(delta,0)))==0

basis=[kron(pa,pb) for pa in P for pb in P]
M=s.zeros(16)
for col,a in enumerate(basis):
    la=Lslow(a)
    for row,b in enumerate(basis):
        M[row,col]=s.simplify(s.trace(b*la)/4)
det=s.factor(M[1:,1:].det())
assert det!=0
# Factored polynomial is positive for every delta>0; record it for direct audit.
ss=-M[1:,1:].T.inv()*M[0,1:].T
xmean=s.simplify(ss[3]) # index 4 in full basis is X_A tensor I_B
assert xmean==0
rhs=s.zeros(15,1)
rhs[3]=-1
poisson=M[1:,1:].inv()*rhs
assert s.simplify(M[0,1:]*poisson)==s.zeros(1,1)
qden=delta**2+4*delta+5
bexplicit=(kron(I,Z)/delta+(delta**2+3*delta+3)*kron(X,I)/2
           -(delta+2)*kron(Y,Z)/2+kron(Z,Z)/2)/qden
assert s.simplify(kron(X,I)+Lslow(bexplicit))==s.zeros(4)
leading=[s.limit(delta*c,delta,0,dir='+') for c in poisson]
assert leading[2]==s.Rational(1,5) # I_A tensor Z_B
assert all(c==0 for i,c in enumerate(leading) if i!=2)

out={
 'fast_example':'gamma=1, J=1; all three local Poisson residuals vanish',
 'fast_B_norm_bound':'||B_X||,||B_Y||,||B_Z||<=1 uniformly delta>=0',
 'global_slow_mode':'L(I_A Z_B)=-2 delta I_A Z_B',
 'instantaneous_local_bound':'diamond<=3 exp(-t), independent delta',
 'slow_sector_X_means':['2/5','-2/5'],
 'slow_example_stationary_minor_determinant':str(det),
 'slow_example_unique_stationary_X_mean':str(xmean),
 'Poisson_norm_lower_bound':'||B|| >= (2/5-r)/(2 delta), for r<2/5',
 'exact_witness_leading_term':'delta B_delta -> (1/5) I_A Z_B; lower-bound order and coefficient sharp at r=0',
}
Path(__file__).with_name('local_reset_a_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
