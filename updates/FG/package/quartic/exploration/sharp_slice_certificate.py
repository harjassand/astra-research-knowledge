import sympy as s,numpy as np,scipy.linalg as la,pickle,os,json
BASE=os.path.dirname(__file__);z=pickle.load(open(BASE+'/sharp_slice_algebraic.pkl','rb'));L=z['L'];mp=z['mp'];rr=z['rref'];piv=z['piv']
def red(p):return s.rem(s.Poly(s.expand(p),L,domain=s.QQ),s.Poly(mp,L,domain=s.QQ)).as_expr()
# Free scalar block weights: alpha=4, beta=2/3.
x=s.zeros(72,1);x[60]=4;x[66]=s.Rational(2,3)
for row,col in enumerate(piv):x[col]=rr[row,-1]-sum(rr[row,k]*x[k] for k in range(60,72))
t=s.Matrix([sum(x[6*i+j]*L**j for j in range(6)) for i in range(12)])
assert z['AA']*x==z['bb']
T=s.zeros(4)
for val,(i,j) in zip(t,z['ij4']):T[i,j]=T[j,i]=val
rt=s.Rational(29553866445792747,10**16)
print('eigen T',la.eigvalsh(np.array(T.subs(L,rt)).astype(float)),flush=True)
print('T at root',np.array(T.subs(L,rt)).astype(float),flush=True)
# Compute leading principal minors modulo minimal polynomial. Exact root interval signs are certified by interval arithmetic below.
minors=[red(T[:j,:j].det(method='domain-ge')) for j in range(1,5)]
print('minors computed',flush=True)
for m in minors:print('minor digits max',max(len(str(abs(s.numer(co)))) for co in s.Poly(m,L).all_coeffs()),'value',float(m.subs(L,rt)),flush=True)
# Interval arithmetic using rational Horner arithmetic.
def pinterval(expr,left,right):
 lo=hi=s.Rational(0)
 for cc in s.Poly(expr,L).all_coeffs():
  cand=[lo*left,lo*right,hi*left,hi*right]
  lo=min(cand)+cc;hi=max(cand)+cc
 return lo,hi
left=s.Rational(295538664457927,10**14);right=s.Rational(295538664457928,10**14)
# target root in (2.95538664457927,2.95538664457928).
assert mp.subs(L,left)*mp.subs(L,right)<0
assert s.Poly(mp,L).count_roots(left,right)==1
bounds=[pinterval(m,left,right) for m in minors]
print('bounds',[(float(a),float(b)) for a,b in bounds],flush=True)
assert all(a>0 for a,b in bounds)
with open(BASE+'/sharp_endpoint_certificate.pkl','wb') as f:pickle.dump(dict(**z,alpha=s.Rational(4),beta=s.Rational(2,3),T=T,minors=minors,left=left,right=right,intervals=bounds),f)
print('SHARP ENDPOINT POSITIVE CERTIFICATE PASSED',flush=True)
