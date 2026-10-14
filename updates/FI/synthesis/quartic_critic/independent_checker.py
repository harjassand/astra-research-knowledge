"""Independent exact algebra for the FI quartic packet.

This checker reconstructs the integrand, acoustic certificate, contact identities,
and concentrating compatible profile directly from the stated coefficients. It
never imports or reads the producer verifier or producer JSON outputs.
"""
import sympy as s

# Row-major coordinates for A=(x|y): (a,b,c,d).
a,b,c,d = s.symbols('a b c d', real=True)
X = s.Matrix([a,b,c,d])
u = a**2+c**2
v = b**2+d**2
w = a*b+c*d
q = a*d-b*c
G = s.expand(3*(u+v-2*q)**2 + s.Rational(35,24)*u**2 + q**2 - s.Rational(5,2)*q*u)
grad = s.Matrix([s.diff(G,z) for z in X])
HG = s.hessian(G, X)


def qmat(poly, vars):
    """Symmetric matrix M with poly=vars.T*M*vars for a homogeneous quadratic."""
    poly=s.Poly(s.expand(poly), *vars)
    n=len(vars); M=s.zeros(n)
    for i in range(n):
        M[i,i]=poly.coeff_monomial(vars[i]**2)
        for j in range(i+1,n):
            M[i,j]=M[j,i]=poly.coeff_monomial(vars[i]*vars[j])/2
    assert s.expand((s.Matrix(vars).T*M*s.Matrix(vars))[0]-poly.as_expr())==0
    return M


def minors_leading(M):
    return [s.factor(M[:k,:k].det()) for k in range(1,M.rows+1)]

# 1. Exact acoustic SOS certificate for the non-polyconvex example.
s0,t0=s.symbols('s t', real=True)
R=s.Matrix([s0,t0,0,0])
acoustic=s.expand((R.T*HG*R)[0])
M11=qmat(s.expand(acoustic.coeff(s0,2).coeff(t0,0)),X)
M12=qmat(s.expand(acoustic.coeff(s0,1).coeff(t0,1))/2,X)
M22=qmat(s.expand(acoustic.coeff(s0,0).coeff(t0,2)),X)
K=s.zeros(4)
for (i,j,val) in [(0,1,11),(0,2,s.Rational(91,6)),(0,3,0),(1,2,0),(1,3,11),(2,3,s.Rational(41,3))]:
    K[i,j]=val; K[j,i]=-val
Q=s.BlockMatrix([[M11,M12+K],[M12-K,M22]]).as_explicit()
null1=s.Matrix([-s.Rational(2,3),0,0,-s.Rational(2,3),0,-1,1,0])
null2=s.Matrix([0,0,0,0,1,0,0,1])
acoustic_reconstruction=s.expand((s.Matrix.vstack(s0*X,t0*X).T*Q*s.Matrix.vstack(s0*X,t0*X))[0]-acoustic)
assert acoustic_reconstruction==0
assert Q*null1==s.zeros(8,1) and Q*null2==s.zeros(8,1)
Qmins=minors_leading(Q[:6,:6])
assert Qmins==[s.Rational(107,2),s.Integer(642),s.Rational(1605,8),s.Rational(8445,16),s.Rational(2815,8),s.Rational(26865,4)]
assert all(x>0 for x in Qmins)
assert Q[:6,:6].det()!=0 and Q.rank()==6

# Non-polyconvexity witness (a law only; it is not a gradient).
I=s.Matrix([1,0,0,1]); D=s.Matrix([1,0,0,-1])
G_I=s.factor(G.subs(dict(zip(X,I))))
G_D=s.factor(G.subs(dict(zip(X,D))))
# symmetric masses at +/-36 I and +/-diag(1,-1), with total low/high weights
p_low=s.Rational(1,2*(1+36**2)); p_high=s.Rational(36**2,2*(1+36**2))
nonpoly_energy=s.factor(2*p_low*(36**4)*G_I+2*p_high*G_D)
assert G_I==-s.Rational(1,24) and G_D==s.Rational(1271,24)
assert nonpoly_energy==-s.Rational(1350,1297)

# 2. Tangent contact, rank-two remainder, and cubic shear invariance for G.
H_at_I=HG.subs(dict(zip(X,I)))
P_contact=s.simplify(H_at_I - s.diag(1,0,0,1)) # checked below by exact polynomial identity instead
# The asserted decomposition is D2G(I)[X,X]=1/2(3a-2d)^2+5/6 c^2-q(X).
contact_identity=s.factor((X.T*H_at_I*X)[0] - (s.Rational(1,2)*(3*a-2*d)**2+s.Rational(5,6)*c**2-q))
assert contact_identity==0
U_sub={c:0,d:s.Rational(3,2)*a}
contact_q=s.factor(q.subs(U_sub))
cubic_contact=s.factor((grad.dot(I)).subs(U_sub))
assert contact_q==s.Rational(3,2)*a**2
assert cubic_contact==-s.Rational(5,12)*a**3
assert s.factor((grad.dot(I)).subs({a:0,c:0,d:0}))==0

# 3. Exact compatible concentrating profile on a unit square.
svar,tvar=s.symbols('s t', real=True)
k=tvar*(1-tvar); kp=s.diff(k,tvar)
g=svar*(1-svar); gp=s.diff(g,svar)
profile_mats=[]
for lo,hi,ff in [(s.Integer(0),s.Rational(1,3),2*svar),(s.Rational(1,3),s.Integer(1),1-svar)]:
    fp=s.diff(ff,svar)
    gradpsi=s.Matrix([fp*k, ff*kp, gp*k, g*kp])
    profile_mats.append((lo,hi,gradpsi))

def integ(expr):
    return s.factor(sum(s.integrate(s.integrate(s.expand(expr),(tvar,0,1)),(svar,lo,hi)) for lo,hi,_ in profile_mats))

Cpsi=s.zeros(4); Hpsi=s.zeros(4,4); bpsi=s.zeros(4,1)
cpsi=0; fourth=0
for lo,hi,gradpsi in profile_mats:
    subs=dict(zip(X,gradpsi))
    for i in range(4):
        bpsi[i]+=s.integrate(s.integrate(s.expand(grad[i].subs(subs)),(tvar,0,1)),(svar,lo,hi))
        for j in range(4):
            Cpsi[i,j]+=s.integrate(s.integrate(s.expand(gradpsi[i]*gradpsi[j]),(tvar,0,1)),(svar,lo,hi))
            Hpsi[i,j]+=s.integrate(s.integrate(s.expand(HG[i,j].subs(subs)),(tvar,0,1)),(svar,lo,hi))
    cpsi+=s.integrate(s.integrate(s.expand(G.subs(subs)),(tvar,0,1)),(svar,lo,hi))
    norm2=s.expand(sum(x*x for x in gradpsi))
    fourth+=s.integrate(s.integrate(s.expand(norm2**2),(tvar,0,1)),(svar,lo,hi))
Cpsi=Cpsi.applyfunc(s.factor); Hpsi=Hpsi.applyfunc(s.factor); bpsi=bpsi.applyfunc(s.factor)
cpsi=s.factor(cpsi); fourth=s.factor(fourth)
C_expected=s.Matrix([[s.Rational(1,15),0,s.Rational(1,45),0],[0,s.Rational(4,81),0,s.Rational(11,486)],[s.Rational(1,45),0,s.Rational(1,90),0],[0,s.Rational(11,486),0,s.Rational(1,90)]])
H_expected=s.Matrix([[s.Rational(2581,540),s.Rational(41,405),s.Rational(248,1215),-s.Rational(2189,540)],[s.Rational(41,405),s.Rational(47,15),s.Rational(121,36),-s.Rational(14,405)],[s.Rational(248,1215),s.Rational(121,36),s.Rational(1229,324),-s.Rational(41,405)],[-s.Rational(2189,540),-s.Rational(14,405),-s.Rational(41,405),s.Rational(494,135)]])
b_expected=s.Matrix([s.Rational(191,756),s.Rational(1231,11340),s.Rational(1439,11340),-s.Rational(2299,11340)])
assert Cpsi==C_expected
assert Hpsi==H_expected
assert bpsi==b_expected
assert cpsi==s.Rational(5951,58800)
assert fourth==s.Rational(29023,1071630)
assert all(x>0 for x in minors_leading(Cpsi))
assert all(x>0 for x in minors_leading(Hpsi))

# Base field +/-e12 on total measure 1/2 and zero elsewhere.
e12=s.Matrix([0,1,0,0])
H0=HG.subs(dict(zip(X,e12)))/2
C0=s.diag(0,s.Rational(1,2),0,0)
b0=s.zeros(4,1)
c0=s.Rational(3,2)
assert H0==s.Matrix([[6,0,0,-6],[0,18,18,0],[0,18,19,0],[-6,0,0,6]])
assert H0.rank()==3 and H0*I==s.zeros(4,1) and H0.is_positive_semidefinite
assert b0==s.zeros(4,1)
assert (I.dot(bpsi))==s.Rational(283,5670)
assert (I.T*Hpsi*I)[0]==s.Rational(179,540)

rho=s.symbols('rho', positive=True)
Hr=(H0+rho*Hpsi)
br=s.sqrt(rho)*bpsi
cr=c0+cpsi
loss=s.factor((br.T*Hr.inv()*br)[0]/2)
gap=s.factor(cr-loss)
scaled_opt=s.simplify(-rho*Hr.inv()*bpsi)
loss_limit=s.limit(loss,rho,0,dir='+')
opt_limit=scaled_opt.applyfunc(lambda z:s.limit(z,rho,0,dir='+'))
assert loss_limit==s.Rational(80089,21313530)
assert opt_limit==-s.Rational(566,3759)*I
# Check exact numerator and denominator have positive coefficients, hence gap>0 for rho>0.
gap_num,gap_den=s.fraction(gap)
gap_num_poly=s.Poly(gap_num,rho); gap_den_poly=s.Poly(gap_den,rho)
assert all(coef>0 for coef in gap_num_poly.all_coeffs())
assert all(coef>0 for coef in gap_den_poly.all_coeffs())
assert s.simplify(s.limit(gap,rho,0,dir='+'))>0

# 4. Exact determinant-balanced noncompatible law from Section 8.
eps=s.Rational(1,10**6); m=9
S=s.Matrix([1,0,0,s.Rational(3,2)])
tval=s.factor((s.Rational(9,2)*m**2*eps)/(1-s.Rational(3,2)*eps))
Rt=s.Matrix([0,1,tval,0]); minus2mS=-2*m*S
# probabilities: +/- R_t each (1-3eps/2)/2, mS with eps, -2mS with eps/2
pr=s.Rational(1,2)*(1-s.Rational(3,2)*eps)
mean=pr*Rt-pr*Rt+eps*m*S+(eps/2)*minus2mS
meanq=2*pr*q.subs(dict(zip(X,Rt)))+eps*q.subs(dict(zip(X,m*S)))+(eps/2)*q.subs(dict(zip(X,minus2mS)))
C_law=2*pr*(Rt*Rt.T)+eps*(m*S)*(m*S).T+(eps/2)*minus2mS*minus2mS.T
H_law=2*pr*HG.subs(dict(zip(X,Rt)))+eps*HG.subs(dict(zip(X,m*S)))+(eps/2)*HG.subs(dict(zip(X,minus2mS)))
b_law=2*pr*grad.subs(dict(zip(X,Rt)))+eps*grad.subs(dict(zip(X,m*S)))+(eps/2)*grad.subs(dict(zip(X,minus2mS)))
c_law=s.factor(2*pr*G.subs(dict(zip(X,Rt)))+eps*G.subs(dict(zip(X,m*S)))+(eps/2)*G.subs(dict(zip(X,minus2mS))))
line_gap=s.factor(c_law-(I.dot(b_law))**2/(2*(I.T*H_law*I)[0]))
assert mean==s.zeros(4,1) and meanq==0 and C_law.rank()==2
assert all(x>0 for x in minors_leading(H_law))
assert (I.T*H_law*I)[0]==s.Rational(177147,1599997600000)
assert I.dot(b_law)==s.Rational(729,800000)
assert line_gap==-s.Rational(11792123534471829388849317,15999928000107999946000000)

print('independent exact checks passed')
print('G acoustic Gram leading minors:', Qmins)
print('G values and nonconvexity witness:', G_I, G_D, nonpoly_energy)
print('profile Cpsi PD leading minors:', minors_leading(Cpsi))
print('profile Hpsi PD leading minors:', minors_leading(Hpsi))
print('profile moments:', 'C=', Cpsi, 'H=', Hpsi, 'b=', bpsi, 'c=', cpsi, 'm4=', fourth)
print('concentrating loss limit:', loss_limit)
print('scaled optimizer limit:', list(opt_limit))
print('concentrating gap exact:', gap)
print('noncompatible balanced-law directional gap:', line_gap)
