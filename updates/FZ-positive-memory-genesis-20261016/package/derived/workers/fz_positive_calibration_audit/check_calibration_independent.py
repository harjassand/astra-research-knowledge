#!/usr/bin/env python3
"""Equation-first exact checks; does not import a supplied verifier or Gram data.

Run from any directory with Python 3 and SymPy. The analytic sign and Sobolev
arguments are in AUDIT.md. This script verifies polynomial/rational identities,
not the infinite-dimensional quasiconvexity question or historical priority.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path
import sympy as sp

OUT = Path(__file__).resolve().parent
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
R = Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-16-positive-memory-genesis-v1')
groups = []

def equal(name, left, right=0):
    vals = list(left-right) if isinstance(left, sp.MatrixBase) else [left-right]
    residuals = [sp.factor(sp.cancel(sp.together(x))) for x in vals]
    if any(x != 0 for x in residuals):
        raise AssertionError((name, residuals))
    groups.append({'name': name, 'status': 'PASS', 'method': 'exact symbolic equality',
                   'scalar_residual_count': len(residuals)})
    print('PASS', name, flush=True)

def norm2(X):
    return sum(x*x for x in X)

def invs(A):
    return (norm2(A[:,0]), norm2(A[:,1]), (A[:,0].T*A[:,1])[0], A.det())

def cf(X):
    return sp.Matrix([X[0,0]-X[1,1], X[0,1]+X[1,0]])

def cofactor2(X):
    return sp.Matrix([[X[1,1], -X[1,0]], [-X[0,1], X[0,0]]])

r = sp.symbols('r', positive=True)
k = sp.symbols('k', real=True)
a,b,c,d,e,f,g,h = sp.symbols('a b c d e f g h', real=True)
x,y,zv,q = sp.symbols('x y zv q', real=True)
A = sp.Matrix([[a,b],[c,d]])
B = sp.Matrix([[e,f],[g,h]])
V = A-B
u,v,w,j = invs(A)
ub,vb,wb,jb = invs(B)
alpha = 3*r/(8*(r+2))
beta = r*(r-1)/6
t = (2*r+1)/3

def J(X, rr=r):
    uu,vv,ww,jj = invs(X)
    return 3*rr/(8*(rr+2))*(uu+vv-2*jj)**2 + rr*(rr-1)/6*uu**2 + jj**2 + rr*uu*jj

def L(X, kk=k, rr=r):
    uu,vv,ww,jj = invs(X)
    tt=(2*rr+1)/3
    return sp.Matrix([[tt**2*uu+(1-kk)*vv+2*tt*jj,kk*ww],
                      [kk*ww,(1-kk)*uu+vv-2*jj]])

M=sp.Matrix([[t*t,1-k,2*t],[1-k,1,-2],[2*t,-2,4+2*k+1/alpha]])
lam=(2+8*alpha+4*alpha*k)*jb+(r-4*alpha)*ub-4*alpha*vb
JA=J(A)
varsA=[a,b,c,d]
gradJ=sp.Matrix([sp.diff(JA,aa) for aa in varsA])
subB=dict(zip(varsA,[e,f,g,h]))
linear=(gradJ.subs(subB).T*sp.Matrix(list(V)))[0]
residual=JA-J(B)-linear-lam*V.det()
delta=sp.Matrix([u-ub,v-vb,j-jb])
rhs=alpha*(delta.T*M*delta)[0]+2*alpha*k*(w-wb)**2+2*alpha*sp.trace(V*L(B)*V.T)

equal('invariant_constraint',u*v-w*w-j*j)
equal('parameter_beta_relation',beta,alpha*(t*t-1))
equal('parameter_uj_relation',r-4*alpha,4*alpha*t)
equal('gram_polarization', (A.T*A-B.T*B).det(),j*j+jb*jb-norm2(A*B.adjugate()))
equal('conformal_defect',norm2(A)-2*A.det(),norm2(cf(A)))
equal('universal_gram_difference',(A.T*A-B.T*B).det()-(j-jb)**2,-norm2(cf(V*B.adjugate())))
equal('universal_support_residual',residual,rhs)
equal('translation_L_derivative',sp.diff(L(B),k),-cofactor2(B.T*B))
equal('translation_slope_derivative',sp.diff(lam,k),4*alpha*jb)

D=9*r*k*k+6*(r+2)**2*k-4*(r+2)**2
equal('M_leading_minor2',M[:2,:2].det(),(1+t-k)*(t+k-1))
equal('M_determinant',M.det(),2*(-3*k+2*r+4)*D/(27*r))
equal('D_at_one',D.subs(k,1),2*r*r+17*r+8)
equal('D_at_half_upper',D.subs(k,(r+2)/3),3*r*(r+2)**2)
equal('D_at_lower_minor_boundary',D.subs(k,1-t),-12*r*(2*r+1))
root=4*(r+2)/(3*(sp.sqrt(r*r+8*r+4)+r+2))
equal('positive_root_formula',sp.simplify(D.subs(k,root)))
Mrat=M.subs(k,sp.Rational(2,3))
equal('rational_M_minor2',Mrat[:2,:2].det(),4*r*(r+1)/9)
equal('rational_M_minor3',Mrat.det(),16*(r+1)/27)
trace_inverse=sp.factor(sp.trace(Mrat.inv()))
equal('rational_M_trace_inverse',trace_inverse,
      (15*r**3+31*r**2+46*r+40)/(4*r*(r+1)))

p,qq=sp.symbols('p qq', real=True)
Bs=sp.Matrix([[p,qq],[0,0]])
Lsing=L(Bs)
equal('singular_L_determinant',Lsing.det(),(1-k)*(t*p*p-qq*qq)**2+(t+1)*(t+1-2*k)*p*p*qq*qq)
Lsingrat=Lsing.subs(k,sp.Rational(2,3))
equal('singular_rational_L_determinant',Lsingrat.det(),sp.Rational(1,3)*(t*p*p-qq*qq)**2+(t+1)*(t-sp.Rational(1,3))*p*p*qq*qq)
equal('singular_small_r_determinant_margin',Lsingrat.det()-r*(r+1)/6*(p*p+qq*qq)**2,
      (1-t*t)/24*(p*p-3*qq*qq)**2)
equal('singular_large_r_determinant_margin',Lsingrat.det()-sp.Rational(1,3)*(p*p+qq*qq)**2,
      (t*t-1)/3*p*p*(p*p+3*qq*qq))

Vfree=sp.Matrix([[x,y],[zv,q]])
As=Bs+Vfree
dus,dvs,dws,js=invs(As)
du=dus-p*p
dv=dvs-qq*qq
dw=dws-p*qq
res_sing=residual.subs({a:p+x,b:qq+y,c:zv,d:q,e:p,f:qq,g:0,h:0})
rhs_one=(du+2*js)**2/8+(dv-2*js)**2/8+dw**2/4+3*js**2/4+norm2(Vfree*Bs.T)/4
equal('r1_singular_square_identity',res_sing.subs(r,1),rhs_one)
equal('r1_rational_L',Lsingrat.subs(r,1),sp.eye(2)*(p*p+qq*qq)/3+sp.Rational(2,3)*Bs.T*Bs)
X=(Bs.T*Vfree).trace()
equal('rank1_Cauchy_gap',norm2(Vfree*Bs.T)-X*X,(p*zv+qq*q)**2)
S=norm2(Vfree)
equal('sum_of_gram_differences',du+dv,S+2*X)
ss,xx=sp.symbols('ss xx', real=True)
equal('r1_quartic_margin_completion',(ss+2*xx)**2/16+xx**2/4,ss**2/32+(ss+4*xx)**2/32)
equal('r1_mixed_inverse_constant',sp.Integer(12)+32,44)

U,Vv,Ww,Jj=sp.symbols('U Vv Ww Jj', real=True)
Linv=sp.Matrix([[U+(1-k)*Vv+2*Jj,k*Ww],[k*Ww,(1-k)*U+Vv-2*Jj]])
det_expected=(1-k)*(U+Vv)**2-2*k*(U-Vv)*Jj-(4-k*k)*Jj*Jj
equal('r1_full_rank_trace',sp.trace(Linv),(2-k)*(U+Vv))
equal('r1_full_rank_determinant',Linv.det()-det_expected,k*k*(U*Vv-Ww*Ww-Jj*Jj))
ee=sp.symbols('ee', nonnegative=True)
equal('r1_diagonal_worst_eigenvalue',L(sp.diag(1,ee),k,sp.Integer(1))[1,1],(1-ee)**2-k)
kone=sp.sqrt(13)-3
equal('r1_root_value',sp.simplify(root.subs(r,1)),kone)
ratio=1-sp.sqrt(kone)
equal('orientation_uniform_threshold',(1-ratio)**2,kone)

# Independent ROC: differentiate J, then form its background coefficient matrix.
zz,nn,mm=sp.symbols('zz nn mm',real=True)
dirvec=sp.Matrix([1,zz,0,0])
acoustic=sp.expand((dirvec.T*sp.hessian(JA,varsA)*dirvec)[0])
PP,QQ,XX,YY=sp.symbols('PP QQ XX YY',real=True)
conformal_vars=[PP,QQ,XX,YY]
to_conformal={a:(PP+XX)/2,b:(YY-QQ)/2,c:(YY+QQ)/2,d:(PP-XX)/2}
aq=sp.expand(acoustic.subs(to_conformal))
T=sp.simplify(sp.hessian(aq,conformal_vars)/2)
Ac=sp.Matrix([[(r+1)**2/2,-zz*(r+1)/2],[-zz*(r+1)/2,(3*zz*zz+r*(r+2))/6]])
equal('ROC_conformal_block_from_J',T[:2,:2],Ac)
equal('ROC_conformal_block_determinant',Ac.det(),r*(r+1)**2*(r+2)/12)
br=r*(5*r+4)/(24*(r+1)**2)
cr=alpha/(r+1)**2
Schur=sp.simplify(T[2:,2:]-T[2:,:2]*Ac.inv()*T[:2,2:])
Schur_expected=4*sp.Matrix([[(alpha-cr)*zz*zz+3*(alpha-br),(2*alpha-alpha/(r+1))*zz],
                           [(2*alpha-alpha/(r+1))*zz,3*alpha*zz*zz]])
equal('ROC_Schur_from_J',Schur,Schur_expected)
equal('ROC_Schur_determinant',Schur.det(),48*alpha*(alpha-cr)*zz**4)
equal('ROC_constant_positive_factor',alpha-br,r*(2*r+1)**2/(24*(r+1)**2*(r+2)))
equal('ROC_z2_positive_factor',alpha-cr,3*r*r/(8*(r+1)**2))
dirnm=sp.Matrix([nn,mm,0,0])
acousticnm=sp.expand((dirnm.T*sp.hessian(JA,varsA)*dirnm)[0])
T_original=sp.hessian(acousticnm,varsA)/2
equal('ROC_original_full_acoustic_determinant',T_original.det(),9*r**4*nn**4*mm**4)

# General shear-sector decomposition and its two acoustic necessity tests.
aa0,bb0,gg0,dd0,eps,ll=sp.symbols('aa0 bb0 gg0 dd0 eps ll',real=True)
def F(XX):
    uu,vv,ww,jj=invs(XX)
    return aa0*(uu+vv-2*jj)**2+bb0*uu*uu+gg0*jj*jj+dd0*uu*jj
FA=F(A)
HessF=sp.hessian(FA,varsA)
direction=sp.Matrix([eps,1,0,0])
testA={a:1,b:-ll*eps,c:ll*eps,d:1}
test=(direction.T*HessF.subs(testA)*direction)[0]/2
equal('shear_LMI1_necessity_acoustic_limit',test,
      eps**2*(6*bb0+dd0+2*dd0*(1-ll)+gg0*(1-ll)**2)+eps**4*ll*ll*(2*bb0+dd0))
test2=(HessF[0,0]/2).subs({a:0,d:0})
equal('shear_LMI2_necessity',test2,2*aa0*(b+c)**2-dd0*(b+c)*c+(2*bb0+dd0)*c*c)
rho=(6*bb0+dd0)/dd0
eta=dd0*dd0/(6*bb0+dd0)
uu,vv,ww,jj=invs(A)
equal('positive_shear_decomposition',F(A),eta*J(A,rho)+(gg0-eta)*jj*jj+
      (aa0-dd0*dd0/(8*(2*bb0+dd0)))*(uu+vv-2*jj)**2)

# Local minor-support obstruction and compatible conformal expansion.
ell=sp.symbols('ell',real=True)
I=sp.eye(2)
gradientI=gradJ.subs({a:1,b:0,c:0,d:1})
slope_gap=J(I+Vfree)-J(I)-(gradientI.T*sp.Matrix(list(Vfree)))[0]-ell*Vfree.det()
q2=sp.Poly(sp.expand(slope_gap),x,y,zv,q)
quadratic=sum(coef*x**mon[0]*y**mon[1]*zv**mon[2]*q**mon[3]
              for mon,coef in q2.terms() if sum(mon)==2)
expected_q=(r+1)**2*x*x+(4+3*r-ell)*x*q+q*q+r*(r+2)*zv*zv/3+(ell-r-2)*y*zv
equal('conformal_support_quadratic',quadratic,expected_q)
equal('conformal_forced_slope_null_form',quadratic.subs(ell,r+2),((r+1)*x+q)**2+r*(r+2)*zv*zv/3)
ss=sp.symbols('ss',real=True)
null_sub={x:ss,y:0,zv:0,q:-(r+1)*ss,ell:r+2}
cubic_expected=-r*(r+2)*ss**3/3+(alpha*(r+2)**4+(r+2)*(r+3)/6)*ss**4
equal('conformal_cubic_obstruction',slope_gap.subs(null_sub),cubic_expected)
poly_r1=sp.Poly(sp.expand(J(ss*I+Vfree,sp.Integer(1))-J(ss*I,sp.Integer(1))),ss)
C3=x**3+5*x*x*q-4*x*y*zv+x*zv*zv+2*x*q*q-2*y*zv*q+zv*zv*q
equal('conformal_r1_cubic_expansion',poly_r1.coeff_monomial(ss),C3)
equal('conformal_r1_cubic_directional_derivative',C3,
      (gradJ.subs(r,1).subs({a:x,b:y,c:zv,d:q}).T*sp.Matrix([1,0,0,1]))[0])
equal('conformal_r1_quadratic_expansion',poly_r1.coeff_monomial(ss**2),
      (2*x+q)**2+zv*zv+3*Vfree.det())
equal('conformal_r1_linear_in_gradient_term',poly_r1.coeff_monomial(ss**3),5*x+3*q)
equal('conformal_pointwise_compensation_failure',C3.subs({x:1,y:0,zv:0,q:-2}),-1)
negative=slope_gap.subs({r:1,ell:3,x:sp.Rational(1,100),y:0,zv:0,q:-sp.Rational(1,50)})
equal('exact_minor_support_counterexample_r1',negative,-sp.Rational(703,800000000))

# Primary-comparator hypotheses fail in explicit, independently checkable ways.
Qrot=sp.Matrix([[0,-1],[1,0]])
equal('failure_of_right_rotational_invariance',J(sp.diag(2,1))-J(sp.diag(2,1)*Qrot),r*(5*r+7)/2)
J_I=JA.subs({a:1,b:0,c:0,d:1,r:1})
J_e11=sp.diff(JA,a).subs({a:1,b:0,c:0,d:1,r:1})
J_e11_e11=sp.diff(JA,a,2).subs({a:1,b:0,c:0,d:1,r:1})
equal('fourth_root_rank1_convexity_failure',4*J_I*J_e11_e11-3*J_e11**2,-11)

sources=[Path('/Users/harjas/Downloads/RESEARCH_REPORT.md'),R/'sources/positive_core_report.txt',
 W/'AGENTS.md',W/'00_START_HERE.txt',
 W/'updates/FW-moving-heat-observable-20261015/package/derived/workers/contact_face_priority_audit/STRUCTURAL_PROOF.txt',
 W/'updates/FW-moving-heat-observable-20261015/package/derived/workers/moving_kernel_genesis/REPORT.v0002.txt',
 W/'updates/FX-global-completion-axis-20261015/package/derived/workers/global_completion_reconstruction/EXACT_NONPOLYCONVEX_COMPLETION.md',
 W/'updates/FY-sharp-ion-genesis-20261015/package/derived/root/GLOBAL_COMPLETION_THEOREM.v0002.md']
receipt={'status':'PASS','audit_kind':'independent equation-first exact symbolic reconstruction',
 'repository_pin':'3dde9ce74d829a93388e64032d27351b36dd2221',
 'python':platform.python_version(),'sympy':sp.__version__,
 'check_count':len(groups),'groups':groups,
 'source_hashes':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources],
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'derived':{'trace_M_rational_inverse':str(trace_inverse),
            'orientation_ratio_exact':str(ratio),'orientation_ratio_decimal':str(sp.N(ratio,30)),
            'explicit_support_gap_at_r1_s_1_over100':str(negative)},
 'limits':['Supplied 24-group verifier, ZIP, candidate arrays and 200-run search not replayed.',
           'Sign proofs for r>0 and function-space implications are analytic in AUDIT.md.',
           'No all-background positive-core QC or compatible negative Jensen field obtained.',
           'Not formal proof verification, external review, or historical priority clearance.']}
(OUT/'EXACT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('COMPLETE',len(groups),'exact symbolic groups',flush=True)
