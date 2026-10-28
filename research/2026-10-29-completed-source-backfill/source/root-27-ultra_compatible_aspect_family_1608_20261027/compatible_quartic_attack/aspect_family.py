"""Exact compatible anisotropic family; degree<=12 Schur-remainder sign.

phi_t(x,y)=bar_phi(x)+t psi(x,y/t), on[0,1]x[0,t]. The original
equal-weight P1 gradient law is transformed by an actual potential, not an
arbitrary moment operation. All polynomial arithmetic is rational.
"""
import json,math,itertools,time
from fractions import Fraction as F
from exact_profile import ROOT,polynomial,diff,add,mul,var

def trim(p):
 p=list(p)
 while len(p)>1 and not p[-1]:p.pop()
 return p
def ua(*ps):
 out=[F(0)]*max(map(len,ps))
 for p in ps:
  for i,c in enumerate(p):out[i]+=c
 return trim(out)
def us(p,c):return trim([x*c for x in p])
def um(p,q):
 out=[F(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):out[i+j]+=a*b
 return trim(out)
def determinant(A):
 n=len(A);terms=[]
 for perm in itertools.permutations(range(n)):
  sign=(-1)**sum(perm[i]>perm[j]for i in range(n)for j in range(i+1,n));p=[F(sign)]
  for i,j in enumerate(perm):p=um(p,A[i][j])
  terms.append(p)
 return ua(*terms)
def primitive(p):
 p=trim(p);lcm=math.lcm(*(x.denominator for x in p));v=[int(x*lcm)for x in p];g=math.gcd(*v)
 return [F(x//g)for x in v]if g else[F(0)]
def remainder(a,b):
 a=trim(a);b=trim(b)
 while len(a)>=len(b)and any(a):
  c=a[-1]/b[-1];k=len(a)-len(b)
  for j,x in enumerate(b):a[j+k]-=c*x
  a=trim(a)
 return a
def sturm(p):
 p=primitive(p);q=primitive([i*p[i]for i in range(1,len(p))]);seq=[p,q]
 while any(seq[-1]):
  r=remainder(seq[-2],seq[-1])
  if not any(r):break
  seq.append(primitive(us(r,-1)))
 return seq
def variation(signs):return sum(a!=b for a,b in zip(signs,signs[1:]))
def sgn(x):return(1 if x>0 else -1 if x<0 else 0)
def evaluate(p,t):
 z=F(0)
 for c in reversed(p):z=z*t+c
 return z

def acquire():
 start=time.monotonic();source=json.loads((ROOT/'data/EXACT_COMPATIBLE_PROFILE.json').read_text());nodes=source['integer_nodes'];n=source['mesh'];D=source['node_denominator'];N=2*n*n
 f,coeff=polynomial();df=[diff(f,i)for i in range(4)];hh=[[diff(df[i],j)for j in range(4)]for i in range(4)]
 norm2=add(*(mul(var(i),var(i))for i in range(4)));needed=set(f)|set(norm2)
 for p in df:needed.update(p)
 for row in hh:
  for p in row:needed.update(p)
 sums={e:[0]*5 for e in needed};balance=[0,0];means=[[0,0]for _ in range(4)]
 for i in range(n):
  bar=[sum(nodes[(i+1)%n][j][o]-nodes[i][j][o]for j in range(n))for o in range(2)]
  for j in range(n):
   a=nodes[i][j];b=nodes[(i+1)%n][j];c=nodes[(i+1)%n][(j+1)%n];d=nodes[i][(j+1)%n]
   atoms=[[(n*(b[o]-a[o]),n*(c[o]-b[o]))for o in range(2)],[(n*(c[o]-d[o]),n*(d[o]-a[o]))for o in range(2)]]
   for X in atoms:
    aa,bb=bar[0],X[0][0]-bar[0];cc=X[0][1];dd,ee=bar[1],X[1][0]-bar[1];ff=X[1][1]
    affine=[(aa,bb),(cc,0),(dd,ee),(ff,0)]
    for k,(v,w)in enumerate(affine):means[k][0]+=v;means[k][1]+=w
    balance[0]+=aa*ff-cc*dd;balance[1]+=bb*ff-cc*ee
    powers=[[1,z,z*z,z**3,z**4]for z in [aa,bb,cc,dd,ee,ff]]
    for e in needed:
     common=powers[2][e[1]]*powers[5][e[3]]
     for k in range(e[0]+1):
      left=common*math.comb(e[0],k)*powers[0][e[0]-k]*powers[1][k]
      for l in range(e[2]+1):sums[e][k+l]+=left*math.comb(e[2],l)*powers[3][e[2]-l]*powers[4][l]
 assert balance==[0,0]and not any(x for row in means for x in row)
 moments={e:trim([F(x,N*D**sum(e))for x in v])for e,v in sums.items()}
 def average(poly):return ua(*(us(moments[e],c)for e,c in poly.items()))if poly else[F(0)]
 C=average(f);B=[average(p)for p in df];H=[[average(p)for p in row]for row in hh];M2=average(norm2)
 assert M2[0]>0 and (len(M2)<2 or M2[1]==0) and all(x>=0 for x in M2)
 assert evaluate(C,F(1))==F(source['c'])
 assert all(evaluate(B[i],F(1))==F(source['b'][i])for i in range(4))
 assert all(evaluate(H[i][j],F(1))==F(source['H'][i][j])for i in range(4)for j in range(4))
 det=determinant(H);quad=[]
 for i in range(4):
  for j in range(4):
   minor=[[H[r][c]for c in range(4)if c!=i]for r in range(4)if r!=j]
   adj=us(determinant(minor),(-1)**(i+j));quad.append(um(um(B[i],adj),B[j]))
 P=ua(us(um(C,det),2),us(ua(*quad),-1));assert len(P)<=13
 assert evaluate(P,F(1))==2*evaluate(det,F(1))*F(source['optimized_gap'])
 seq=sturm(P);at0=[sgn(next(x for x in p if x))for p in seq];atInf=[sgn(p[-1])for p in seq]
 roots=variation(at0)-variation(atInf);assert roots>=0
 # A quantitative continuum guard, chosen strictly below the observed
 # one-dimensional minimum and then verified without floating arithmetic.
 epsilon=F(41,400);guard=ua(P,us(um(C,det),-2*epsilon));guard_seq=sturm(guard)
 guard0=[sgn(next(x for x in p if x))for p in guard_seq];guardInf=[sgn(p[-1])for p in guard_seq]
 guard_roots=variation(guard0)-variation(guardInf)
 assert guard_roots==0 and guard[0]>0
 result={'status':'EXACT_COMPATIBLE_ASPECT_FAMILY_SIGN_ACQUIRED','mesh':n,'potential_source':'data/EXACT_COMPATIBLE_PROFILE.json',
  'family':'phi_t(x,y)=bar_phi(x)+t psi(x,y/t), t>0, rectangle[0,1]x[0,t]',
  'H_coefficients':[[list(map(str,p))for p in row]for row in H],'b_coefficients':[list(map(str,p))for p in B],
  'c_coefficients':list(map(str,C)),'M2_coefficients':list(map(str,M2)),'detH_coefficients':list(map(str,det)),
  'cleared_gap_polynomial':list(map(str,P)),'primitive_cleared_gap_polynomial':list(map(str,primitive(P))),
  'Sturm_sequence':[list(map(str,p))for p in seq],'Sturm_variations_zero_plus':variation(at0),'Sturm_variations_positive_infinity':variation(atInf),
  'positive_real_roots':roots,'P_at_zero_positive':P[0]>0,'all_positive_aspect_ratios_have_positive_optimized_gap':roots==0 and P[0]>0,
  'exact_t_equals_one_replay':True,'positive_M2_for_all_positive_t':True,
  'uniform_relative_gap_lower':str(epsilon),'relative_guard_polynomial':list(map(str,guard)),
  'relative_guard_Sturm_sequence':[list(map(str,p))for p in guard_seq],
  'relative_guard_Sturm_variations_zero_plus':variation(guard0),'relative_guard_Sturm_variations_positive_infinity':variation(guardInf),
  'relative_guard_positive_roots':guard_roots,'relative_guard_at_zero_positive':guard[0]>0,
  'determinant_balance_polynomial':balance,'gradient_mean_polynomial':means,'seconds':time.monotonic()-start,
  'scope':'This one rational profile and its entire compatible aspect-ratio family, all affine backgrounds. Does not prove QC of the target for arbitrary profiles.'}
 if roots:
  candidates=[F(2)**k for k in range(-12,13)]+[F(k,20)for k in range(1,101)]
  result['negative_rational_parameters']=[str(t)for t in candidates if evaluate(P,t)<0]
 (ROOT/'data/EXACT_ASPECT_FAMILY.json').write_text(json.dumps(result,indent=2));print({k:result[k]for k in ['status','positive_real_roots','all_positive_aspect_ratios_have_positive_optimized_gap','seconds']});return result
if __name__=='__main__':acquire()
