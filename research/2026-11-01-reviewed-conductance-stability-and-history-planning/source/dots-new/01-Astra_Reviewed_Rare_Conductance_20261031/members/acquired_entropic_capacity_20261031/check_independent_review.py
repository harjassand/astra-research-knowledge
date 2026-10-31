from fractions import Fraction as F
from copy import deepcopy
import json,sys,random
import sympy as s
sys.path.insert(0,sys.argv[1])
from capacity import acquire,certify,encode,Integrator,Unknown,sparse_fixture
from verify import receiving_verify
checks=[]
def ck(label,x):
 assert x,label
 checks.append(label)
def reject(label,fn):
 try:fn()
 except (Unknown,ValueError,TypeError,KeyError):checks.append(label);return
 raise AssertionError('accepted '+label)
raw=sparse_fixture(2);ac=acquire(raw);cert=certify(ac)
ck('baseline',receiving_verify(raw,cert)['status']=='PASS')
for k in [F(1,10),F(1,2),F(1),F(3),F(20)]:
 it=Integrator([k,k],192)
 lo,hi=it.monotone_integral(F(0),F(1,2),64,1)
 exact=1+F(203,240)*k
 ck('exact resistance integral '+str(k),2*lo<=exact<=2*hi)
 for y in [F(0),F(1,2),F(1),F(5,4),F(2)]:
  q,w=it.point(y);D=1+k*(1-y*y)**2
  ck('exact rational q '+str((k,y)),F(q[0],2**192)<=1/D<=F(q[1],2**192))
  ck('exact rational w '+str((k,y)),F(w[0],2**192)<=D<=F(w[1],2**192))
# Unequal rational fiber matrices with non-coordinate rational null direction.
for j in range(1,7):
 xs=s.symbols('x0:3');x=s.Matrix(xs);u=s.Matrix([1,j,-1]);Pi=u*u.T/(u.dot(u));P=s.eye(3)-Pi
 H=P*s.diag(s.Rational(j,3),s.Rational(j+1,2),s.Rational(j+3,4))*P
 expr=s.expand(((x.T*P*x)[0]+(1-(x.T*Pi*x)[0])**2*(x.T*H*x)[0])/2)
 rr=encode(expr,xs);aa=acquire(rr)
 ck('nullspace direction '+str(j),aa['direction_rational']==[str(v) for v in u])
 t=s.symbols('t');poly=sum(s.Rational(v)*t**i for i,v in enumerate(aa['determinant_coefficients']))
 ck('direct determinant '+str(j),s.expand(poly-(s.eye(3)+t*H).det())==0)
 cc=certify(aa,quad_relative=F(1,20));ck('dense whole receiver '+str(j),receiving_verify(rr,cc,max_quad_ratio=F(21,20))['status']=='PASS')
 for power in [[1,0,0],[0,3,0],[0,0,5]]:
  bad=deepcopy(rr);bad['terms'].append({'powers':power,'coefficient':'1/1009'})
  reject('full polynomial corruption '+str((j,power)),lambda bad=bad:acquire(bad))
for field in ['n','m','grid_N','precision_bits']:
 for value in [True,False,1.0,'1',None,[],{}]:
  bad=deepcopy(cert);bad[field]=value
  reject('certificate type '+str((field,value)),lambda bad=bad:receiving_verify(raw,bad))
for field in ['lower','upper']:
 for name in ['mass_A_unnormalized','resistance','free_energy_rate','full_diffusion_rate']:
  for value in [1,True,1.0,'2/2','nan','inf']:
   bad=deepcopy(cert);bad[name][field]=value
   reject('interval type '+str((field,name,value)),lambda bad=bad:receiving_verify(raw,bad))
for arg in ['max_quad_ratio','max_grid','max_precision','max_points','max_product_bits']:
 for value in [float('nan'),float('inf'),True,False,0,-1,2.0]:
  reject('external receiver budget '+str((arg,value)),lambda arg=arg,value=value:receiving_verify(raw,cert,**{arg:value}))
for arg in ['max_grid','max_precision','max_points','max_cutoff','max_product_bits']:
 for value in [float('nan'),float('inf'),True,False,0,-1,2.0]:
  reject('external producer budget '+str((arg,value)),lambda arg=arg,value=value:certify(ac,**{arg:value}))
# Prior valid-input failure: cannot resolve the seed; now finite UNKNOWN.
huge={'kappa':[str(2**1000)]*2,'determinant_coefficients':None,'m':2,'ell':['1','0','0'],'direction_rational':['1','0','0'],'direction_norm_squared':'1'}
reject('zero seed finite UNKNOWN',lambda:certify(huge))
smallbeta=F(1,2**2000);cb=certify(ac,beta=smallbeta)
ck('display overflow exact receiver',receiving_verify(raw,cb,beta=smallbeta)['status']=='PASS')
ck('display overflow explicit null',cb['free_energy_rate']['upper_display'] is None)
# Display values are deliberately NOT a mathematical proof input.
bad=deepcopy(cert);bad['full_diffusion_rate']['upper_display']='not a proof field'
ck('display ignored by scoped receiver',receiving_verify(raw,bad)['status']=='PASS')
# Changed physical raw task must be reacquired, not trusted from the certificate.
badraw=deepcopy(raw);badraw['terms'][0]['coefficient']='47/19'
reject('changed actual polynomial',lambda:receiving_verify(badraw,cert))
print(json.dumps({'status':'PASS','checks':len(checks),'labels':checks,'scope':'Exact algebra, rational intervals, raw-model identity and external-task rejection. No experimental or sampling claim.'},indent=2))
