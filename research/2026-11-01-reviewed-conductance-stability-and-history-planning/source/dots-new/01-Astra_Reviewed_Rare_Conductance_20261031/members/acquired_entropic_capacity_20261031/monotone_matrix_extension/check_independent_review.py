import sys,json
from fractions import Fraction as F
from copy import deepcopy
from itertools import combinations
from random import Random
import sympy as s
sys.path.insert(0,sys.argv[1])
import compile as c
checks=[]
def ck(label,v):
 assert v,label
 checks.append(label)
def reject(label,fn):
 try:fn()
 except c.Unknown:checks.append(label);return
 raise AssertionError('accepted '+label)
raw=c.fixture(2);cert=c.certify(raw);ac=cert['acquisition']
ck('baseline whole receiver',c.verify(raw,cert)['status']=='PASS')
rng=Random(1828)
for q in range(60):
 A=s.zeros(4)
 for i in range(4):
  for j in range(i,4):A[i,j]=A[j,i]=s.Rational(rng.randrange(-5,6),rng.randrange(1,7))
 minors=[A.extract(a,a).det() for k in range(1,5) for a in combinations(range(4),k)]
 ck('4x4 all principal minors '+str(q),c.psd(A)==all(x>=0 for x in minors))
 ck('4x4 strict minors '+str(q),c.psd(A,True)==all(A[:k,:k].det()>0 for k in range(1,5)))
# Rank-one H2; physical dimension and inherited tail are independent of determinant degree.
H1=s.Matrix(ac['H1']).applyfunc(s.Rational)
for H2 in [s.diag(0,s.Rational(1,2),0),s.Matrix([[0,0,0],[0,s.Rational(1,3),s.Rational(1,3)],[0,s.Rational(1,3),s.Rational(1,3)]])]:
 r=c.encode_terms(3,c.aligned_terms(H1,H2));a=c.acquire(r);ii=c.new_integrator(a,192,10000,200000)
 ck('rank tail m '+str(H2),a['determinant_degree']==3 and ii.m==2)
 ck('rank tail determinant '+str(H2),ii.leading==F((H1+s.diag(1,0,0)).det()))
 out=c.certify(r);ck('rank receiver '+str(H2),c.verify(r,out)['status']=='PASS')
 for T in [F(2),F(4),F(8)]:
  # Compare directly to the inherited physical-m expression.
  from capacity import sqrt_bounds
  hi=sqrt_bounds(1/F(a['tail_det_H1']),192)[1]
  exact=F(hi,2**192)*(1-1/(T*T))**(-2)*T**(-3)/3
  ck('physical tail formula '+str((H2,T)),ii.tail(T)==exact)
# Aligned coordinate j=1 instead of an assumed first coordinate.
M1=s.Matrix([[s.Rational(3,4),0,s.Rational(1,8)],[0,0,0],[s.Rational(1,8),0,s.Rational(1,2)]])
M2=s.diag(s.Rational(1,4),0,s.Rational(1,2))
r=c.encode_terms(3,c.aligned_terms(M1,M2,1));a=c.acquire(r)
ck('aligned nonfirst axis',a['direction']==['0','1','0'])
ck('aligned whole receiver',c.verify(r,c.certify(r))['status']=='PASS')
# Dense irrational unit direction and noncommuting rank-one second matrix.
xs=s.symbols('x0:3');x=s.Matrix(xs);u=s.Matrix([1,2,3]);Pi=u*u.T/14;P=s.eye(3)-Pi
M1=P*s.diag(s.Rational(1,2),s.Rational(3,4),s.Rational(4,3))*P
w=s.Matrix([2,-1,0]);M2=w*w.T/50;z=(x.T*Pi*x)[0]
expr=s.expand(((x.T*P*x)[0]+(1-z)**2*(x.T*M1*x)[0]+(1-z)**4*(x.T*M2*x)[0])/2)
r=c.encode_terms(3,dict(s.Poly(expr,*xs).terms()));a=c.acquire(r)
ck('dense exact direction',a['direction']==['1','2','3'] and a['direction_norm_squared']=='14')
ck('dense genuine noncommutation',F(a['commutator_squared_frobenius'])>0)
ck('dense whole receiving',c.verify(r,c.certify(r))['status']=='PASS')
for bad1,bad2,label in [(s.diag(0,0,1),s.diag(0,1,1),'singular H1'),(s.diag(0,-1,1),s.diag(0,3,1),'negative H1 despite positive Hessian'),(H1,s.diag(0,-s.Rational(1,4),1),'indefinite H2')]:
 r=c.encode_terms(3,c.aligned_terms(bad1,bad2));reject(label,lambda r=r:c.acquire(r))
for degree in [0,1,3,5,7,9]:
 r=deepcopy(raw);r['terms'].append({'powers':[degree,0,0],'coefficient':'1/101'})
 reject('full polynomial omitted degree '+str(degree),lambda r=r:c.acquire(r))
for field in ['n','m','determinant_degree','tail_exponent_physical_m','norm_tests']:
 for val in [True,False,2.0,'2']:
  out=deepcopy(cert);out['acquisition'][field]=val
  reject('acquisition type '+str((field,val)),lambda out=out:c.verify(raw,out))
for i in range(len(ac['acquired_joint_component_sizes'])):
 for val in [float(ac['acquired_joint_component_sizes'][i]),True,False]:
  out=deepcopy(cert);out['acquisition']['acquired_joint_component_sizes'][i]=val
  reject('nested component type '+str((i,val)),lambda out=out:c.verify(raw,out))
for field in ['N','precision_bits']:
 for val in [True,False,64.0,'64']:
  out=deepcopy(cert);out[field]=val
  reject('certificate type '+str((field,val)),lambda out=out:c.verify(raw,out))
for arg in ['max_grid','max_points','max_cutoff','max_precision','max_product_bits']:
 for val in [True,False,float('nan'),float('inf'),1.5,0,-1]:
  reject('external budget '+str((arg,val)),lambda arg=arg,val=val:c.verify(raw,cert,**{arg:val}))
for val in [True,float('nan'),float('inf'),.01,F(0),F(-1)]:
 reject('external exact width '+str(val),lambda val=val:c.verify(raw,cert,quad_relative=val))
out=deepcopy(cert);out['acquisition']['tail_exponent_physical_m']=4
reject('tail degree spoof',lambda:c.verify(raw,out))
out=deepcopy(cert);out['basins']='x0 <= 0 and x0 >= 1'
reject('physical basin spoof',lambda:c.verify(raw,out))
out=deepcopy(cert);out['full_rate']['upper']='1/100000000000000000000'
reject('interval spoof',lambda:c.verify(raw,out))
print(json.dumps({'status':'PASS','checks':len(checks),'labels':checks,'scope':'Exact independent algebra, physical tail, raw acquisition, external task and typed tamper checks; not physical or sampling validation.'},indent=2))
