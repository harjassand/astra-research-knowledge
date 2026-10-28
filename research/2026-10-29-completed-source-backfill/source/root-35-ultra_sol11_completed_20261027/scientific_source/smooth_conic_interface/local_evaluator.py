"""Exact local calibrated70 certificates; floating Newton proposes only."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import itertools,json,math,time
MODULE_STARTED=time.monotonic()
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import scipy.optimize as opt
import sympy as sp
OUT=Path(__file__).resolve().parent
WORK=OUT.parents[1]
OLD=WORK/'sol8_opportunity_selection_20261027/rational_selector'
COMP=OUT.parent/'support_gram_compiler'
ZERO=(0,0,0,0)
EPS,KAPPA,SIGMA=Q(1,100),Q(1,20000000),Q(1,34)
E=EPS-KAPPA
def exponent(ii):return tuple(ii.count(i)for i in range(4))
def monomials(lo,hi):
 return[exponent(ii)for d in range(lo,hi+1)for ii in itertools.combinations_with_replacement(range(4),d)]
FEAT=monomials(1,4);ALL=monomials(0,8)
assert len(FEAT)==69 and len(ALL)==495
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def serial(x):
 x=Q(x);return str(x.numerator)+'/'+str(x.denominator)
def rational(x):return Q(int(x.p),int(x.q))
A=sp.symbols('a0:4');B=sp.symbols('b0:4');s=sp.symbols('s')
aa,bb,cc,dd=A
T=sum(x*x for x in A);q=aa*dd-bb*cc
u,v,w=aa*aa+cc*cc,bb*bb+dd*dd,aa*bb+cc*dd
x,y,z=u-v,2*w,2*q
F=(sp.Rational(55220381,10**10)*(u*u+v*v)
 +sp.Rational(114430029,625000000)*u*v
 -sp.Rational(801761987,5000000000)*w*w
 +sp.Rational(118849817,4000000000)*q*(u-v))
p=(sp.Rational(6222019,200000000)*x**3
 +sp.Rational(1686519911,10**10)*x*x*z
 +sp.Rational(81172813,2000000000)*x*z*z
 +sp.Rational(1726116771,10**10)*z**3
 +sp.Rational(128626163,5000000000)*x*y*y
 +sp.Rational(373321239,2000000000)*y*y*z)
H=sp.expand(F-sp.Rational(KAPPA)*q*q)
pH=sp.expand(p-2*sp.Rational(KAPPA)*q*T*T)
D=sp.expand((T+sp.Rational(SIGMA))**2);cof=[dd,-cc,-bb,aa]
N0=sp.expand(D*(-3*H-sp.Rational(E)*T)+pH*q)
NB=[sp.expand(D*(sp.diff(H,a)+2*sp.Rational(E)*a)-pH*c)for a,c in zip(A,cof)]
NPOLY=[N0]+NB+[pH]
N=sp.expand(N0+sum(b*n for b,n in zip(B,NB))+s*pH);ELL=N/D
def literal(poly):return{a:rational(c)for a,c in sp.Poly(poly,*A,domain=sp.QQ).terms()if c}
def ldl(mat):
 n=len(mat);low=[[Q(0)for _ in range(n)]for _ in range(n)];piv=[]
 for i in range(n):
  t=mat[i][i]-sum(low[i][k]**2*piv[k]for k in range(i));assert t>0
  piv.append(t);low[i][i]=1
  for j in range(i+1,n):
   low[j][i]=(mat[j][i]-sum(low[j][k]*low[i][k]*piv[k]for k in range(i)))/t
 return min(piv)
def matrix_poly(mat,features):
 out={}
 for i,a in enumerate(features):
  for j in range(i,len(features)):
   value=mat[i][j]*(1 if i==j else 2)
   if value:
    k=plus(a,features[j]);out[k]=out.get(k,Q(0))+value
 return{a:v for a,v in out.items()if v}
def build_base_gram():
 old=json.loads((OLD/'EXACT_RATIONAL_SUPPORT.json').read_text())
 g35=json.loads((COMP/'EXACT35_LEADING_GRAM.json').read_text())
 den=old['gram_denominator'];f2=monomials(2,2);f3=monomials(3,3);f4=monomials(4,4)
 qvec=[literal(q).get(a,Q(0))for a in f2]
 qf=[[Q(old['gram_integer_matrix'][80+i][80+j],den)-KAPPA*qvec[i]*qvec[j]
      for j in range(10)]for i in range(10)]
 assert matrix_poly(qf,f2)==literal(H)
 g1=[[E*SIGMA*SIGMA*(i==j)for j in range(4)]for i in range(4)]
 g2=[[3*SIGMA*SIGMA*qf[i][j]for j in range(10)]for i in range(10)]
 for i,a in enumerate(f2):g2[i][i]+=2*E*SIGMA*(1 if 2 in a else 2)
 g3=[[Q(0)for _ in f3]for _ in f3]
 for i,a in enumerate(f3):g3[i][i]+=E*(math.factorial(3)//math.prod(math.factorial(t)for t in a))
 for k in range(4):
  ii=[f3.index(tuple(t+(j==k)for j,t in enumerate(a)))for a in f2]
  for i in range(10):
   for j in range(10):g3[ii[i]][ii[j]]+=6*SIGMA*qf[i][j]
 v4=[literal(T*q).get(a,Q(0))for a in f4]
 assert g35['features']==[list(a)for a in f4]
 g4=[[Q(g35['gram_numerators'][i][j],g35['gram_denominator'])-KAPPA*v4[i]*v4[j]
      for j in range(35)]for i in range(35)]
 blocks=[g1,g2,g3,g4];scales=[Q(1,400),Q(1,50),Q(9,100),Q(3,100)]
 result=[[Q(0)for _ in FEAT]for _ in FEAT];start=0;pivots=[]
 for block,scale in zip(blocks,scales):
  pivots.append(ldl([[v-(scale*scale if i==j else 0)for j,v in enumerate(row)]for i,row in enumerate(block)]))
  for i,row in enumerate(block):
   for j,v in enumerate(row):result[start+i][start+j]=v
  start+=len(block)
 assert matrix_poly(result,FEAT)==literal(-N0)
 ds=[scales[sum(a)-1]for a in FEAT]
 return result,ds,pivots

def shifts(poly):
 """Coefficients in Y of poly(a+Y), as exact polynomials in anchor a."""
 out={}
 for ex,c in literal(poly).items():
  for yy in itertools.product(*(range(n+1)for n in ex)):
   power=tuple(e-y for e,y in zip(ex,yy))
   val=c*math.prod(math.comb(e,y)for e,y in zip(ex,yy))
   dest=out.setdefault(yy,{})
   dest[power]=dest.get(power,Q(0))+val
 return out

def aggregate_bound(poly):
 """Group absolute coefficients by anchor degree, B degree and s degree."""
 out={}
 for ex,c in poly.items():
  if c:
   key=(sum(ex[:4]),sum(ex[4:8]),ex[8]);out[key]=out.get(key,Q(0))+abs(c)
 return out

def bound(aggregate,ra,rb,rs):
 return sum(c*ra**a*rb**b*rs**s for (a,b,s),c in aggregate.items())

def compile_bounds(ds):
 shifted={}
 for n,poly in enumerate(NPOLY):
  for yy,pp in shifts(poly).items():
   dest=shifted.setdefault(yy,{})
   zz=(0,0,0,0,0)if n==0 else tuple(int(i==n-1)for i in range(5))
   for ex,c in pp.items():
    key=ex+zz;dest[key]=dest.get(key,Q(0))+c
 dshift=shifts(D);n0=literal(N0);dn={};db={};pick={}
 for yy in ALL:
  if sum(yy)<2:continue
  pp=dict(shifted.get(yy,{}));zero9=(0,)*9
  pp[zero9]=pp.get(zero9,Q(0))-n0.get(yy,Q(0))
  dn[yy]=aggregate_bound(pp)
  db[yy]=aggregate_bound({ex+(0,)*5:c for ex,c in dshift.get(yy,{}).items()})
  choices=[(i,j)for i,a in enumerate(FEAT)for j in range(i,len(FEAT))if plus(a,FEAT[j])==yy]
  best=max(ds[i]*ds[j]for i,j in choices)
  pick[yy]=[(i,j)for i,j in choices if ds[i]*ds[j]==best]
 return shifted,dshift,dn,db,pick,aggregate_bound(shifted[ZERO])

def box_bound(ds,compiled,ra,rb,rs):
 shifted,dshift,dn,db,pick,nbound=compiled
 tbound=bound(nbound,ra,rb,rs)/(SIGMA*SIGMA)
 rows=[Q(0)for _ in FEAT]
 for yy in dn:
  c=bound(dn[yy],ra,rb,rs)+bound(db[yy],ra,rb,rs)*tbound
  for i,j in pick[yy]:
   error=c/(len(pick[yy])*(1 if i==j else 2)*ds[i]*ds[j])
   rows[i]+=error
   if i!=j:rows[j]+=error
 return max(rows),tbound

def concavity_bound(ra,rb,rs):
 """Operator Hessian deviation on |a|<=ra, |B|<=2rb."""
 C=sum(abs(c)for c in literal(H).values());P=sum(abs(c)for c in literal(pH).values())
 r,b=ra,2*rb
 k0=P*r**6/SIGMA**2
 k1=6*P*r**5/SIGMA**2+4*P*r**7/SIGMA**3
 k2=30*P*r**4/SIGMA**2+52*P*r**6/SIGMA**3+24*P*r**8/SIGMA**4
 rr=rs+r*r/2+r*b
 return 36*C*r*r+24*C*r*b+k2*rr+2*k1*(r+b)+k0

def evaluate_poly(poly,point):
 return sum(c*math.prod(t**n for t,n in zip(point,ex))for ex,c in poly.items())

def scalar_shift_value(pp,anchor):return evaluate_poly(pp,anchor)

def value_and_gram(anchor,zz,base,ds,compiled):
 """Exact affine coefficient correction; no Newton accuracy premise."""
 shifted,dshift,dn,db,pick,nbound=compiled
 allparams=tuple(anchor)+tuple(zz)
 den=evaluate_poly(literal(D),anchor)
 t0=evaluate_poly(shifted[ZERO],allparams)/den
 coeff={yy:scalar_shift_value(dshift.get(yy,{}),anchor)*t0
            -evaluate_poly(shifted.get(yy,{}),allparams)for yy in ALL}
 assert coeff[ZERO]==0
 result=[row[:]for row in base]
 p0=literal(-N0)
 for yy in dn:
  correction=coeff[yy]-p0.get(yy,Q(0))
  for i,j in pick[yy]:
   value=correction/(len(pick[yy])*(1 if i==j else 2))
   result[i][j]+=value
   if i!=j:result[j][i]+=value
 assert matrix_poly(result,FEAT)=={ex:v for ex,v in coeff.items()if sum(ex)>=2 and v}
 deviation=max(sum(abs(result[i][j]-base[i][j])/(ds[i]*ds[j])for j in range(69))for i in range(69))
 assert deviation<1
 b=(1-deviation)*ds[0]**2/2
 ell=[coeff[tuple(int(j==i)for j in range(4))]/2 for i in range(4)]
 eta=2*sum(v*v for v in ell)/(SIGMA**2*b)
 assert sum(a*a for a in anchor)<=SIGMA/4
 offset=KAPPA*sum(z*z for z in zz)
 return {'lower':t0+offset,'upper':t0+eta+offset,'completion_eta':eta,
         'scaled_Gram_row_norm':deviation,'linear_residual':ell,'b':b,'anchor':anchor,
         'V_lower':t0,'constant_coefficient_zero':True,'nonconstant_Gram_identity':True}

_NEWTON_FUNCTIONS=None
def propose(zz):
 global _NEWTON_FUNCTIONS
 compile_begin=time.monotonic()
 variables=A+B+(s,)
 if _NEWTON_FUNCTIONS is None:
  _NEWTON_FUNCTIONS=(sp.lambdify(variables,[sp.diff(ELL,a)for a in A],'numpy',cse=True),
                    sp.lambdify(variables,sp.hessian(ELL,A),'numpy',cse=True))
 gradient,hessian=_NEWTON_FUNCTIONS
 compile_seconds=time.monotonic()-compile_begin
 point=np.array(zz[:4],dtype=float)
 begin=time.monotonic();iterations=0
 for _ in range(12):
  args=tuple(point)+tuple(map(float,zz))
  g=np.array(gradient(*args),dtype=float);hh=np.array(hessian(*args),dtype=float)
  step=np.linalg.solve(hh,g);point-=step;iterations+=1
  if np.linalg.norm(step,np.inf)<1e-18:break
 anchor=[Q(round(float(t)*(1<<60)),1<<60)for t in point]
 return anchor,{'iterations':iterations,'proposal_seconds':time.monotonic()-begin,
                'function_compile_seconds':compile_seconds,
                'proposal_accuracy_trusted':False}

def record_value(v):
 return {key:([serial(x)for x in value]if isinstance(value,list)else serial(value)
              if isinstance(value,Q)else value)for key,value in v.items()}

def sqrt_bracket(x,bits=110):
 n=math.isqrt((x.numerator<<(2*bits))//x.denominator)
 lo,hi=Q(n,1<<bits),Q(n+1,1<<bits)
 assert lo*lo<=x<=hi*hi
 return lo,hi

def old15_axis_value(ss):
 """Exact old15 slice, using its proved 1D reduction instead of an SDP."""
 p0=Q(55220381,10**10);ell=Q(118849817,4000000000)
 c0=2*p0+Q(114430029,625000000)
 assert ss>0
 lo,hi=-ell*ss/(2*p0),Q(0)
 def derivative(xx):
  rl,rh=sqrt_bracket(xx*xx+4*ss*ss)
  quot=sorted([xx/rl,xx/rh])
  return 2*p0*xx+ell*ss+EPS*quot[0],2*p0*xx+ell*ss+EPS*quot[1]
 begin=time.monotonic()
 for _ in range(80):
  mid=(lo+hi)/2;dl,dh=derivative(mid)
  if dh<0:lo=mid
  elif dl>0:hi=mid
  else:raise AssertionError('increase scalar precision')
 mid=(lo+hi)/2;rl,rh=sqrt_bracket(mid*mid+4*ss*ss)
 polynomial=p0*mid*mid+ell*ss*mid+c0*ss*ss
 dl,dh=derivative(mid);error=max(abs(dl),abs(dh))*(hi-lo)/2
 return {'lower':serial(polynomial+EPS*rl-error),'upper':serial(polynomial+EPS*rh),
         'display_only':[float(polynomial+EPS*rl-error),float(polynomial+EPS*rh)],
         'iterations':80,'seconds':time.monotonic()-begin,
         'operation':'proved exact B0 slice of frozen15-moment value; rational derivative bisection'}

def main():
 setup_seconds=time.monotonic()-MODULE_STARTED
 started=time.monotonic();base,ds,pivots=build_base_gram()
 gram_seconds=time.monotonic()-started
 tick=time.monotonic();compiled=compile_bounds(ds);compile_seconds=time.monotonic()-tick
 trials=[];selected=None
 for denominator in [100,500,1000,2000,4000,10000,20000,50000]:
  ra=Q(1,denominator);rb=ra/8;rs=Q(1,10000)
  rho,tbound=box_bound(ds,compiled,ra,rb,rs)
  concavity=concavity_bound(ra,rb,rs)
  trials.append({'anchor_component_radius':serial(ra),'B_component_radius':serial(rb),
                 's_radius':serial(rs),'rho':serial(rho),'rho_display':float(rho),
                 'Hessian_deviation_bound':serial(concavity)})
  if rho<Q(1,2)and concavity<E:
   selected=(ra,rb,rs,rho,concavity);break
 assert selected is not None,'No explicit box acquired'
 ra,rb,rs,rho,concavity=selected
 print('box',float(ra),float(rb),float(rs),'rho',float(rho),flush=True)
 examples=[]
 points=[[rb/2,-rb/3,rb/5,rb/4,rs/2],
         [rb/3,rb/4,-rb/5,rb/2,-rs/2]]
 for zz in points:
  anchor,proposal=propose(zz)
  assert max(map(abs,anchor))<=ra
  assert sum(a*a for a in anchor)<=ra*ra
  tick=time.monotonic();verified=value_and_gram(anchor,zz,base,ds,compiled)
  verification_seconds=time.monotonic()-tick
  detb=zz[0]*zz[3]-zz[1]*zz[2]
  old_lower=EPS*sum(t*t for t in zz[:4])+2*EPS*abs(zz[4]-detb)
  assert old_lower>verified['upper']
  example={'query':[serial(x)for x in zz],'proposal':proposal,
           'certificate':record_value(verified),
           'display_only_value':[float(verified['lower']),float(verified['upper'])],
           'interval_width_display_only':float(verified['upper']-verified['lower']),
           'exact_verification_seconds':verification_seconds,
           'old15_value_lower_bound':serial(old_lower),
           'old15_lower_display_only':float(old_lower)}
  examples.append(example)
  print('value',example['display_only_value'],'width',example['interval_width_display_only'],flush=True)
 axis_s=Q(1,10000);axis_value=KAPPA*axis_s*axis_s
 old_axis=old15_axis_value(axis_s)
 result={'status':'EXACT_OPEN_BOX_AND_LOCAL70_VALUE_CERTIFICATES',
  'parameters':{'epsilon':serial(EPS),'kappa':serial(KAPPA),'e':serial(E),'sigma':serial(SIGMA)},
  'finite_cone':{'PSD_size':70,'coefficient_equations':495,'nonconstant_features':69},
  'base_Gram_identity':True,'exact_shifted_block_LDL_pivots':[serial(v)for v in pivots],
  'feature_scales_by_degree':[serial(ds[0]),serial(ds[4]),serial(ds[14]),serial(ds[34])],
  'box_trials':trials,'open_box':{'abs_B_i_less_than':serial(rb),'abs_s_less_than':serial(rs),
    'anchor_bound':serial(ra),'scaled_coefficient_Gram_row_bound':serial(rho),
    'anchor_bound_norm':'Euclidean for root existence; coordinate cube for coefficient test',
    'Hessian_deviation_from_minus2eI':serial(concavity),
    'e_margin':serial(E),'root_existence_and_smoothness':'strict concavity on |a|<=ra, boundary derivative inward; certified Gram at root proves global cone exactness'},
  'examples':examples,'axis_comparison':{'s':serial(axis_s),'new_G_exact':serial(axis_value),
   'old15_exact_slice':old_axis,'new_G_display_only':float(axis_value)},
  'seconds':{'base_Gram':gram_seconds,'coefficient_bound_compiler':compile_seconds,
              'total_with_examples_and_comparator':time.monotonic()-started,
              'module_import_and_literal_setup':setup_seconds,
              'module_elapsed_excluding_Python_startup':time.monotonic()-MODULE_STARTED},
  'scope':'Global finite strongly convex primitive, smooth near entire graph; explicit local full5D box and certified off-axis evaluations. No global smoothness or general speed advantage claimed; no70 SDP solve performed.'}
 (OUT/'LOCAL_EVALUATION.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':result['status'],'seconds':result['seconds'],
                   'box':result['open_box'],'axis_new':float(axis_value),
                   'axis_old':old_axis['display_only']},indent=2))

if __name__=='__main__':main()
