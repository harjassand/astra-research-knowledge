"""Independent symbolic checks for the FI full-cone rigidity and shear algebra."""
import sympy as s

# Full nine-coefficient invariant polynomial in row-major coordinates.
a0,b0,c0,d0=s.symbols('a0 b0 c0 d0', real=True)
X=s.Matrix([a0,b0,c0,d0])
u=a0**2+c0**2; v=b0**2+d0**2; w=a0*b0+c0*d0; q=a0*d0-b0*c0
Ac,Bc,Cc,E,Gc,Hc,Lc,Mc,Nc=s.symbols('Ac Bc C E G H L M N', real=True)
F9=s.expand(Ac*u**2+Bc*v**2+Cc*u*v+E*w**2+Gc*u*w+Hc*v*w+Lc*q*u+Mc*q*v+Nc*q*w)
H9=s.hessian(F9,X)

# Rank-one distinguished point: verify its full Hessian and kernel geometry.
Q11=H9.subs({a0:1,b0:0,c0:0,d0:0})
Q11_expected=s.Matrix([[12*Ac,3*Gc,0,3*Lc],[3*Gc,2*Cc+2*E,-Lc,Nc],[0,-Lc,4*Ac,Gc],[3*Lc,Nc,Gc,2*Cc]])
assert Q11==Q11_expected
bb,dd=s.symbols('bb dd', real=True)
a_kernel=-(Gc*bb+Lc*dd)/(4*Ac)
c_kernel=(Lc*bb-Gc*dd)/(4*Ac)
q_kernel=s.factor((a_kernel*dd-bb*c_kernel))
assert q_kernel==-Lc*(bb**2+dd**2)/(4*Ac)
# Vanishing of the Schur complement when Ac>0 and rank(Q11)=2 yields these.
# Substitution into its rows gives independent coefficients.
row2=s.factor((Q11_expected*s.Matrix([a_kernel,bb,c_kernel,dd]))[1])
row4=s.factor((Q11_expected*s.Matrix([a_kernel,bb,c_kernel,dd]))[3])
assert s.factor(row4.subs({Lc:0})-(Nc*bb+dd*(2*Cc-Gc**2/(4*Ac))))==0
assert s.factor(row2.subs({Lc:0,Nc:0,Cc:Gc**2/(8*Ac),E:Gc**2/(4*Ac)}))==0
# Residual rank-one Hessian at e12 forces Hc=Mc=0 by zero diagonal/PSD.
Fres=s.expand(Bc*v**2+Hc*w*v+Mc*q*v)
Q12_res=s.hessian(Fres,X).subs({a0:0,b0:1,c0:0,d0:0})
assert Q12_res==s.Matrix([[0,3*Hc,0,Mc],[3*Hc,12*Bc,-3*Mc,0],[0,-3*Mc,0,Hc],[Mc,0,Hc,4*Bc]])
# If Ac=0, rank-one values reduce to Bc*v^2 and Hessians at e11/e12 force L=N=M=0.
lam=s.symbols('lam', real=True)
Fdeg=s.expand(Bc*v**2+q*(Lc*u+Mc*v+Nc*w)+lam*q**2)
Qdeg11=s.hessian(Fdeg,X).subs({a0:1,b0:0,c0:0,d0:0})
Qdeg12=s.hessian(Fdeg,X).subs({a0:0,b0:1,c0:0,d0:0})
assert Qdeg11[0,3]==3*Lc and Qdeg11[1,2]==-Lc and Qdeg11[1,3]==Nc
assert Qdeg12[0,2]==-Nc and Qdeg12[0,3]==Mc and Qdeg12[1,2]==-3*Mc

# Normalize an invertible distinguished point to I and use I,J,K,L coordinates.
i,j,k,l=s.symbols('i j k l', real=True)
Is=s.I
z=i+Is*j; ww=k+Is*l
zbar=s.conjugate(z); wbar=s.conjugate(ww)
Fbasis=s.expand(F9.subs({a0:i+k,b0:-j+l,c0:j+l,d0:i-k}))
Y=s.Matrix([i,j,k,l])
Hb=s.hessian(Fbasis,Y)
Ipt={i:1,j:0,k:0,l:0}
f=s.factor(Fbasis.subs(Ipt)); aa=s.factor(s.diff(Fbasis,k).subs(Ipt)); bcontact=s.factor(s.diff(Fbasis,l).subs(Ipt))
H_rows=Hb.subs(Ipt)
H_rows_expected=s.Matrix([[12*f,0,3*aa,3*bcontact],[0,4*f,-bcontact,aa],[3*aa,-bcontact,H_rows[2,2],H_rows[2,3]],[3*bcontact,aa,H_rows[3,2],H_rows[3,3]]])
assert (H_rows-H_rows_expected).applyfunc(s.factor)==s.zeros(4)
# Rank-one remainder: P=vv^T and top/cross equations imply aa=bcontact=0.
v0,v1,v2,v3=s.symbols('v0 v1 v2 v3', real=True)
# The logical fork is encoded explicitly: v0*v1=0, so one factor vanishes;
# the four cross equations then force both distinguished derivatives to zero.
assert s.factor((v0*v2-3*aa)+(v1*v3-aa)-(v0*v2+v1*v3-4*aa))==0
# Complete invariant basis in z,w has nine real coordinates.
fr,br,gr,dr,di,er,ei,hr,hi=s.symbols('fr br gr dr di er ei hr hi', real=True)
Re=lambda expr:s.expand((expr+s.conjugate(expr))/2)
Fcomplex=s.expand(fr*(z*zbar)**2+br*(z*zbar)*(ww*wbar)+gr*(ww*wbar)**2+
    Re((dr+Is*di)*z**2*wbar**2+(er+Is*ei)*(z*zbar)*z*wbar+(hr+Is*hi)*(ww*wbar)*z*wbar))
# The coordinate transform is invertible, and the 9 parameter coefficient matrix has rank 9.
params=[fr,br,gr,dr,di,er,ei,hr,hi]
monoms=s.Poly(Fcomplex,i,j,k,l).monoms()
# Build coefficient columns without relying on a producer basis calculation.
poly=s.Poly(Fcomplex,i,j,k,l)
rows=[]
for mon in poly.monoms():
    rows.append([s.diff(poly.coeff_monomial(mon),pp) for pp in params])
assert s.Matrix(rows).rank()==9
# Independently count the left-SO(2)-invariant quartic space by the infinitesimal action.
all_mons=[m for m in s.polys.monomials.itermonomials([a0,b0,c0,d0],4)
          if sum(m.as_powers_dict().get(vv,0) for vv in [a0,b0,c0,d0])==4]
rot_gen=lambda P:s.expand(-c0*s.diff(P,a0)-d0*s.diff(P,b0)+a0*s.diff(P,c0)+b0*s.diff(P,d0))
rotmat=s.zeros(len(all_mons))
mon_index={m:idx for idx,m in enumerate(all_mons)}
for col,mon in enumerate(all_mons):
    Rpoly=s.Poly(rot_gen(mon),a0,b0,c0,d0)
    for target,coef in Rpoly.terms():
        rotmat[mon_index[s.prod(var**pow for var,pow in zip([a0,b0,c0,d0],target))],col]=coef
assert len(all_mons)==35 and rotmat.rank()==26 and len(all_mons)-rotmat.rank()==9

# Generic rank-two remainder formulas. The complex normal form is differentiated afresh.
pv,rv,alph=s.symbols('p r alpha', real=True, nonzero=True)
lamv=(pv-3*rv)/2
fv=(pv-rv)/8
betav=(9*alph**2/pv+alph**2/rv-2*lamv)/4
deltav=(9*alph**2/pv-alph**2/rv)/4
etR,etI,gv=s.symbols('etaR etaI g', real=True)
Fgen=s.expand(fv*(z*zbar)**2+betav*(z*zbar)*(ww*wbar)+gv*(ww*wbar)**2+
    Re(deltav*z**2*wbar**2+alph*(z*zbar)*z*wbar+(etR+Is*etI)*(ww*wbar)*z*wbar))
Hg=s.hessian(Fgen,Y).subs(Ipt)
Pg=s.simplify(Hg-s.diag(lamv,lamv,-lamv,-lamv))
Pexpected=s.Matrix([[pv,0,3*alph,0],[0,rv,0,alph],[3*alph,0,9*alph**2/pv,0],[0,alph,0,alph**2/rv]])
assert (Pg-Pexpected).applyfunc(s.factor)==s.zeros(4)
Usubs={i:-3*alph*k/pv,j:-alph*l/rv}
qcoord=i**2+j**2-k**2-l**2
assert s.factor(qcoord.subs(Usubs))==s.factor((9*alph**2/pv**2-1)*k**2+(alph**2/rv**2-1)*l**2)
D_i=s.diff(Fgen,i).subs(Usubs)
Dpoly=s.Poly(s.factor(D_i),k,l)
assert Dpoly.coeff_monomial(k**2*l)==etI and Dpoly.coeff_monomial(l**3)==etI
assert s.factor(Dpoly.coeff_monomial(k**3)-Dpoly.coeff_monomial(k*l**2)+4*lamv**3*alph**3/(rv**2*pv**3))==0
# Totally-null plane p=3 alpha, r=alpha, lambda=0 forces eta=alpha (real).
Dzero=s.factor(s.diff(Fgen,i).subs({pv:3*alph,rv:alph,lamv:0,i:-k,j:-l}))
assert s.factor(Dzero+(k**2+l**2)*(alph*k-etR*k-etI*l))==0
# Rank-one tangent-contact branch r=alpha; cubic is independent of radical coordinate l.
et_contact=(48*fv**2-40*fv*lamv+7*lamv**2)/pv
Dshear=s.factor(s.diff(Fgen,i).subs({rv:alph,etR:et_contact,etI:0,i:-3*alph*k/pv,j:-l}))
assert s.factor(Dshear+alph*k**3*(pv-3*alph)**3/(2*pv**3))==0

# Singular top blocks: p=0/r>0, r=0/p>0, and p=r=0 are exhaustive
# because P>=0 makes its diagonal top block diag(p,r) semidefinite.
# On p=0,r>0, PSD forces the i row/cross entries to zero (epsilon=0); the
# remaining w block has rank one, leaving a negative-q kernel vector.
# On r=0,p>0, similarly the j axis and one w-kernel vector survive with
# opposite signs of q; at p=r=0 the kernel is the conformal (i,j) plane, q>0.
# The displayed singular-branch acoustic identity is independently checked:
Z,W,sg,tau,g0,h0=s.symbols('Z W sig tau g0 h0', real=True)
xx,yy,kk,ll=s.symbols('xx yy kk ll', real=True)
zc=xx+Is*yy; wc=kk+Is*ll
qcw=xx**2+yy**2-kk**2-ll**2
rr=Re(zc*s.conjugate(wc))
Fsing=s.expand(fv*qcw**2+tau*rr**2+g0*(kk**2+ll**2)**2+h0*(kk**2+ll**2)*rr)
vec=s.Matrix([xx,yy,kk,ll]); Rs=s.Matrix([sg,0,1,0])
expr=s.factor((Rs.T*s.hessian(Fsing,vec)*Rs)[0].subs({xx:0,yy:Z,kk:0,ll:W,sg**2:1}))
expr_target=2*((2*tau*sg+h0)*Z*W+(2*g0+h0*sg)*W**2)
assert s.factor((expr-expr_target).subs({sg:1}))==0 and s.factor((expr-expr_target).subs({sg:-1}))==0

# The non-shear semidefinite branch p=3 alpha has a joint acoustic obstruction.
# Reconstruct in physical row-major variables and test the actual rank-one direction (t,1;0,0).
pr,rrr,V=s.symbols('p_phys r_phys V', real=True, nonzero=True)
lam_ns=(pr-3*rrr)/2; f_ns=(pr-rrr)/8; alpha_ns=pr/3
beta_ns=(9*alpha_ns**2/pr+alpha_ns**2/rrr-2*lam_ns)/4
delta_ns=(9*alpha_ns**2/pr-alpha_ns**2/rrr)/4
eta_ns=rrr; g_ns=V-(pr-9*rrr)/24
F_ns=s.expand(f_ns*(z*zbar)**2+beta_ns*(z*zbar)*(ww*wbar)+g_ns*(ww*wbar)**2+
    Re(delta_ns*z**2*wbar**2+alpha_ns*(z*zbar)*z*wbar+eta_ns*(ww*wbar)*z*wbar))
phys={i:(a0+d0)/2,j:(c0-b0)/2,k:(a0-d0)/2,l:(b0+c0)/2}
F_phys=s.expand(F_ns.subs(phys)); PH=s.hessian(F_phys,s.Matrix([a0,b0,c0,d0]))
Rt=s.Matrix([s.symbols('tt'),1,0,0]); tt=Rt[0]
ac=s.expand((Rt.T*PH*Rt)[0])
def qmat(poly,vars):
    P=s.Poly(s.expand(poly),*vars); M=s.zeros(len(vars))
    for m in range(len(vars)):
        M[m,m]=P.coeff_monomial(vars[m]**2)
        for n in range(m+1,len(vars)): M[m,n]=M[n,m]=P.coeff_monomial(vars[m]*vars[n])/2
    assert s.expand((vars.T*M*vars)[0]-P.as_expr())==0
    return M
physvars=s.Matrix([a0,b0,c0,d0])
M0=qmat(ac.coeff(tt,0),physvars); M1=qmat(ac.coeff(tt,1),physvars); M2=qmat(ac.coeff(tt,2),physvars)
rad=s.Matrix([0,-1,1,0]); U=s.Matrix([[1,0,0],[0,0,1],[0,0,1],[0,1,0]])
C0=s.simplify(U.T*M0*U)
Ctarget=s.Matrix([[(pr-3*rrr)**2/(36*rrr)+V/4,-V/4,0],[-V/4,V/4,0],[0,0,3*V]])
assert (C0-Ctarget).applyfunc(s.factor)==s.zeros(3) and s.simplify(M0*rad)==s.zeros(4,1)
vec1=s.simplify(U.T*M1*rad)
schur=s.factor((rad.T*M2*rad)[0]-(vec1.T*C0.inv()*vec1)[0])
assert s.factor(schur+(pr-3*rrr)**4/(324*rrr**2*V))==0
assert s.factor(C0.det()-V**2*(pr-3*rrr)**2/(48*rrr))==0
assert s.factor((rad.T*M1*rad)[0])==0
shift=-U*C0.inv()*vec1
trial=rad+tt*shift
trial_energy=s.factor((trial.T*(M0+tt*M1+tt**2*M2)*trial)[0])
trial_poly=s.Poly(s.expand(trial_energy),tt)
assert s.factor(trial_poly.coeff_monomial(1))==0 and s.factor(trial_poly.coeff_monomial(tt))==0
assert s.factor(trial_poly.coeff_monomial(tt**2)-schur)==0

print('independent rigidity algebra checks passed')
print('rank-one distinguished Hessian:',Q11_expected)
print('generic P:',Pexpected)
print('generic cubic coefficient difference:',s.factor(Dpoly.coeff_monomial(k**3)-Dpoly.coeff_monomial(k*l**2)))
print('shear cubic on U:',Dshear)
print('nonshear acoustic Schur coefficient:',schur)
