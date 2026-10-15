"""Exact necessary PC-support checks; does not decide PC or QC."""
import json
from pathlib import Path
import sympy as S

a,b,c,d,k,t = S.symbols('a b c d k t', real=True)
h = S.Matrix(S.symbols('h0:4', real=True))
z = S.Matrix([a,b,c,d])
u,v,w,q = a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
F = S.expand(u*u+v*v+S.Rational(166,3)*u*v-S.Rational(460,9)*w*w-S.Rational(52,9)*q*(u-v))
grad = S.Matrix([F.diff(x) for x in z])
Hess = S.hessian(F,z)
shift = dict(zip(z,z+h))
at_h = dict(zip(z,h))
exact_remainder = S.expand(F.subs(shift, simultaneous=True)-F-(grad.T*h)[0])
quartic_remainder = S.expand(F.subs(at_h, simultaneous=True)+(grad.subs(at_h, simultaneous=True).T*z)[0]+(h.T*Hess*h)[0]/2)
assert exact_remainder == quartic_remainder

P = 17*k**4-314*k*k+17
rem = lambda expr: S.rem(S.expand(expr),P,k)
A = S.Matrix([203-17*k*k,k*(85*k*k-1551),2*k*(944-51*k*k),134])
at_A = dict(zip(z,A))
R = S.Matrix([1,k,0,0])
cof_R = S.Matrix([0,0,-k,1])
lamb = S.Rational(1,3)*(56694784-3364864*k*k)
assert all(rem(x)==0 for x in Hess.subs(at_A, simultaneous=True)*R-lamb*cof_R)
FA = rem(F.subs(at_A, simultaneous=True))
qA = rem(q.subs(at_A, simultaneous=True))
margin = rem(2*FA-lamb*qA)
expected_margin = S.Rational(881721344,153)*(48246-2597*k*k)
assert S.expand(margin-expected_margin)==0
assert S.Rational(48246)-2597*S.Rational(314,17)>0
assert S.Rational(314,17)>0 and S.Rational(17,17)>0
assert 314**2-4*17*17>0
radial = S.expand(exact_remainder.subs(dict(zip(h,t*z)), simultaneous=True))
assert S.expand(radial-t*t*((t+2)**2+2)*F)==0
receipt = {
 'scope':'Instantiated Aubert PC support criterion and necessary contact/radial consequences only',
 'criterion_applies':True,
 'Dacorogna_Koshigoe_special_criterion_applies':False,
 'failed_hypothesis':'Right SO(2) invariance',
 'exact_checks':{'quartic_Bregman_identity':True,'contact_Hessian_kernel_identity':True,
                 'radial_increment_identity':True,'strict_radial_support_margin_at_four_contacts':True},
 'forced_contact_lambda_mod_P':str(lamb),'contact_determinant_mod_P':str(qA),
 'radial_margin_mod_P':str(margin),
 'global_support_sentence_evaluated':False,'PC':'UNKNOWN','QC':'UNKNOWN',
 'sympy_version':S.__version__
}
out = Path(__file__).with_name('PC_CRITERION_RECEIPT.v0002.json')
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'all_four_exact_checks_passed':True,'PC':'UNKNOWN','QC':'UNKNOWN'},indent=2))
