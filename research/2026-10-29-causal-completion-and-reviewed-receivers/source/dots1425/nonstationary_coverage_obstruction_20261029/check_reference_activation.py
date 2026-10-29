import sympy as s,json,mpmath as m
x=s.symbols('e',positive=True);r=s.zeros(4);r[0,0]=2*x/3;r[1,1]=s.Rational(1,3);r[3,3]=2*(1-x)/3;r[0,3]=r[3,0]=2*s.sqrt(x*(1-x))/3
X=s.Matrix([[0,1],[1,0]]);A=[s.kronecker_product(X*s.diag(1,1/s.sqrt(2)),s.eye(2)),s.kronecker_product(X*s.Matrix([[0,1/s.sqrt(2)],[0,0]]),s.eye(2))]
F=lambda q:s.simplify(sum((a*q*a.T for a in A),s.zeros(4)))
o=F(r);o2=F(o);assert s.simplify(o[1,1]*o[2,2]-o[1,2]**2)==0
assert s.simplify(o[1,1]+o[2,2])==(1+x)/3
assert o2[2,2]==x/3 and o2[1,1]==s.Rational(1,3)-x/6
assert s.simplify(o2[0,0]*o2[3,3]-o2[0,3]**2-x/9+x*x/18)==0
m.mp.dps=70;h=lambda z:-z*m.log(z)-(1-z)*m.log(1-z);rows=[]
for k in [2,4,8,16,32]:
 e=m.mpf(10)**(-k);l1=h((1+e)/3)-h(m.mpf(1)/3)+e*m.log(2)
 tr=m.mpf(2)/3-e/6;det=e/9-e*e/18;small=2*det/(tr+m.sqrt(tr*tr-4*det));large=tr-small
 ev=[small,large,e/3,m.mpf(1)/3-e/6];entropy=-sum(z*m.log(z) for z in ev)
 # A=0 population decreases by e/2 under Φ².
 l2=entropy-h(m.mpf(1)/3)+e*m.log(2)/2
 rows.append({'e':str(e),'coherence_over_L1':str((m.mpf(2)/3)*h(e)/l1),'L2_over_L1':str(l2/l1)})
print(rows);open('REFERENCE_ACTIVATION_CHECKS.json','w').write(json.dumps({'symbolic_matrix_assertions':'pass','numerical_precision_digits':70,'rows':rows},indent=2)+'\n')
