"""Independent rigorous interval check for a three-copy PI-code dual witness.
All interval endpoints are integers over2**PREC. Racah coefficients use the
factorial formula with exact rational prefactors and integer-square-root bounds.
A positive reported contradiction margin is an exact Fraction inequality.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import factorial,isqrt
import json,hashlib,time,sys
import numpy as np
PREC=192;Q=1<<PREC
class B:
 def __init__(self,m,r=0):
  self.m=np.asarray(m,dtype=object);self.r=np.broadcast_to(np.asarray(r,dtype=object),self.m.shape).copy()
 @staticmethod
 def exact(x):
  a=np.asarray(x,dtype=object);ms=[];rs=[]
  for v in a.flat:
   f=F.from_float(v) if isinstance(v,(float,np.floating)) else F(v)
   lo,rem=divmod(f.numerator*Q,f.denominator);ms.append(lo);rs.append(int(rem!=0))
  return B(np.array(ms,dtype=object).reshape(a.shape),np.array(rs,dtype=object).reshape(a.shape))
 def __add__(a,b):
  if not isinstance(b,B):b=B.exact(b)
  return B(a.m+b.m,a.r+b.r)
 __radd__=__add__
 def __neg__(a):return B(-a.m,a.r)
 def __sub__(a,b):return a+-b if isinstance(b,B) else a+B.exact(-b)
 def __rsub__(a,b):return B.exact(b)+-a
 def __mul__(a,b):
  if not isinstance(b,B):b=B.exact(b)
  mid=a.m*b.m;rad=abs(a.m)*b.r+a.r*abs(b.m)+a.r*b.r
  return B(mid//Q,(rad+Q-1)//Q+1)
 __rmul__=__mul__
 def __matmul__(a,b):
  mid=a.m@b.m;rad=abs(a.m)@b.r+a.r@abs(b.m)+a.r@b.r
  return B(mid//Q,(rad+Q-1)//Q+1)
 @property
 def T(a):return B(a.m.T,a.r.T)
 def __getitem__(a,k):return B(a.m[k],a.r[k])
 def add_entry(a,i,j,b):a.m[i,j]+=b.m.item();a.r[i,j]+=b.r.item()
 def trace(a):return B(np.trace(a.m),np.trace(a.r))
 def max_abs(a):return F(int(np.max(abs(a.m)+a.r)),Q)
 def max_row_abs_sum(a):return F(int(np.max(np.sum(abs(a.m)+a.r,axis=1))),Q)
 def gram_lower(a):
  return F(min(int(a.m[i,i]-a.r[i,i]-sum(abs(a.m[i,j])+a.r[i,j] for j in range(a.m.shape[0]) if i!=j)) for i in range(a.m.shape[0])),Q)
 def unique_integer(a):
  lo=int(a.m-a.r);hi=int(a.m+a.r);l=-(-lo//Q);h=hi//Q;assert l==h,(l,h,float(F(lo,Q)),float(F(hi,Q)));return l

def bsqrt(f):
 f=F(f);assert f>=0;t=isqrt((f.numerator*Q*Q)//f.denominator);exact=t*t*f.denominator==f.numerator*Q*Q;return B(t,0 if exact else 1)
@lru_cache(None)
def six(a,b,c,d,e,f):
 tri=[(a,b,c),(a,e,f),(d,b,f),(d,e,c)];rad=F(1);ts=[]
 for u,v,w in tri:
  if (u+v+w)%2 or u+v<w or u+w<v or v+w<u:return B.exact(0)
  t=(u+v+w)//2;ts.append(t);rad*=F(factorial(t-u)*factorial(t-v)*factorial(t-w),factorial(t+1))
 us=[(a+b+d+e)//2,(a+c+d+f)//2,(b+c+e+f)//2];summ=F(0)
 for z in range(max(ts),min(us)+1):
  den=1
  for v in ts:den*=factorial(z-v)
  for v in us:den*=factorial(v-z)
  summ+=F((-1)**z*factorial(z+1),den)
 return bsqrt(rad)*summ

def exact_rational_six(a,b,c,d,e,f):
 tri=[(a,b,c),(a,e,f),(d,b,f),(d,e,c)];rad=F(1);ts=[]
 for u,v,w in tri:
  assert (u+v+w)%2==0 and u+v>=w and u+w>=v and v+w>=u
  t=(u+v+w)//2;ts.append(t);rad*=F(factorial(t-u)*factorial(t-v)*factorial(t-w),factorial(t+1))
 us=[(a+b+d+e)//2,(a+c+d+f)//2,(b+c+e+f)//2];summ=F(0)
 for z in range(max(ts),min(us)+1):
  den=1
  for v in ts:den*=factorial(z-v)
  for v in us:den*=factorial(v-z)
  summ+=F((-1)**z*factorial(z+1),den)
 rn=isqrt(rad.numerator);rd=isqrt(rad.denominator)
 assert rn*rn==rad.numerator and rd*rd==rad.denominator
 return summ*F(rn,rd)

def eye(n):return B.exact(np.eye(n,dtype=int))
def zeros(n,m=None):return B.exact(np.zeros((n,n if m is None else m),dtype=int))
def matrix_from_entries(rows):return B(np.array([[v.m.item() for v in row]for row in rows],dtype=object),np.array([[v.r.item()for v in row]for row in rows],dtype=object))
def fraction_string(x):return str(F(x))
def main(path):
 start=time.perf_counter();p=Path(path);data=json.loads(p.read_text());print('candidate keys',list(data),flush=True)
 n=data.get('n',18);D=n+1;K=2;assert n==18
 # The candidate schema is deliberately checked explicitly below.
 linear=data['linear_duals'];seeddata=data['basis_seed_data'];metas=data['psd_meta'];factors=data['psd_cholesky_factors'];assert len(linear)==8 and len(metas)==len(factors)
 dual=[];clipped=[]
 for i,v in enumerate(linear):
  z=np.asarray(v,dtype=float)
  if i in [0,3,5]:
   clipped.append({'index':i,'negative_entries_clipped':int(np.sum(z<0))});z=np.maximum(z,0)
  dual.append(B.exact(z))
 const=-F.from_float(float(np.asarray(linear[1])))-F(D,2)*F.from_float(float(np.asarray(linear[2])))
 exact_M=[[exact_rational_six(n,n,2*k,n,n,2*l)*((-1)**(n+k+l)*(2*k+1)) for l in range(D)] for k in range(D)]
 M=B.exact(exact_M);G=M*2-eye(D);W=M*F(4,D)*B.exact(np.array([(-1)**l for l in range(D)]))
 saved=json.loads((Path(__file__).resolve().parents[1]/f'transform_n{n}.json').read_text())
 assert all(exact_M[i][j]==F(saved[i][j]) for i in range(D) for j in range(D))
 assert all(sum(exact_M[i][j] for i in range(D))==(D if j==0 else 0) for j in range(D))
 ra=-dual[0]-G.T@dual[3]-W.T@dual[5]-W.T@dual[6]*K
 ra=ra+B.exact(np.r_[float(np.asarray(linear[1])),np.zeros(D-1)])+B.exact(np.full(D,float(np.asarray(linear[2]))))+G[1:5,:].T@dual[4]
 blocks={};rankchecks=[]
 for J2 in range(n%2,3*n+1,2):
  ls=[l for l in range(D)if abs(2*l-n)<=J2<=2*l+n];h=len(ls);I=eye(h);V=B.exact(np.diag([(-1)**(n-l)for l in ls]));U=matrix_from_entries([[six(n,n,2*l,n,J2,2*lp)*bsqrt((2*l+1)*(2*lp+1))*((-1)**(n+l+lp))for lp in ls]for l in ls])
  Ps=(I+V+U+V@U@V+V@U+U@V)*F(1,6);Pa=(I-V-U-V@U@V+V@U+U@V)*F(1,6);Pt=I-Ps-Pa;Pp=Pt@(I+V)*F(1,2)
  raw=seeddata[str(J2)];assert raw['ls']==ls
  zs=np.asarray(raw['symmetric_seed'],dtype=float).reshape(h,-1);zp=np.asarray(raw['standard_seed'],dtype=float).reshape(h,-1)
  assert Ps.trace().unique_integer()==zs.shape[1];assert Pp.trace().unique_integer()==zp.shape[1]
  qs=Ps@B.exact(zs);qp=Pp@B.exact(zp);qm=(I-V)@U@qp*bsqrt(F(1,3));grams={};frames={}
  for label,A,Bb in [('sym',qs,None),('std',qp,qm)]:
   if A.m.shape[1]:
    gram=A.T@A
    if Bb is not None:gram=gram+Bb.T@Bb
    gl=gram.gram_lower();assert gl>0;grams[label]=gl;frames[label]=(A,Bb)
  C=zeros(h)
  for z,l in enumerate(ls):C.add_entry(z,z,dual[6][l]*(J2+1))
  blocks[J2]={'ls':ls,'U':U,'C':C,'frames':frames,'gram_lower':grams,'base':{},'pt_coefficient':zeros(h)}
  rankchecks.append({'J2':J2,'sym_rank':zs.shape[1],'std_plus_rank':zp.shape[1],'gram_lower':{k:str(v)for k,v in grams.items()}})
 klrow=0
 for rank in range(5):
  for l in range(D):
   for lp in range(l,min(D,l+rank+1)):
    if l+lp<rank:continue
    zdual=dual[7][klrow];klrow+=1
    for J2,block in blocks.items():
     ls=block['ls']
     if l not in ls or lp not in ls:continue
     i=ls.index(lp);col=ls.index(l);phase=(-1)**((2*lp+n+J2+2*rank)//2);co=six(2*l,n,J2,n,2*lp,2*rank)*phase*(J2+1)*zdual
     for z in range(len(ls)):block['C'].add_entry(i,z,co*(block['U'][z,col]-F(int(z==col),2)))
 assert klrow==np.asarray(linear[7]).size
 for meta,factor in zip(metas,factors):
  J2=int(meta['J2']);block=blocks[J2];L=B.exact(np.asarray(factor,dtype=float));S=L@L.T;typ=meta['type']
  if typ=='base':block['base'][meta['label']]=S;continue
  if typ=='ppt':block['pt_coefficient']=block['pt_coefficient']-S
  elif typ=='BminusR':block['C']=block['C']+S
  elif typ=='BminusPpt':block['pt_coefficient']=block['pt_coefficient']+S
  else:raise AssertionError(typ)
  if typ in ['BminusR','BminusPpt']:
   for i,l in enumerate(block['ls']):ra=ra-W[l,:]*S[i,i]*F(1,2*l+1)
 # Original tensor-rank sum for partial time reversal. No shortcut identity is assumed.
 for l in range(D):
  print('PPT rank-sum row',l,'of',D,flush=True)
  for lp in range(D):
   allowed=[J2 for J2,b in blocks.items() if l in b['ls'] and lp in b['ls']]
   ranks=list(range(abs(l-lp),min(l+lp,n)+1))
   C=matrix_from_entries([[six(2*l,n,J2,n,2*lp,2*rank)*((-1)**((2*lp+n+J2+2*rank)//2)) for rank in ranks] for J2 in allowed])
   weighted=C*B.exact(np.array([(-1)**rank*(2*rank+1) for rank in ranks]))
   T=(weighted@C.T)*B.exact(np.array([J2+1 for J2 in allowed]))
   for zz,Jp2 in enumerate(allowed):
    dst=blocks[Jp2];di=dst['ls'].index(l);dj=dst['ls'].index(lp);v=B.exact(0)
    for z,J2 in enumerate(allowed):
     src=blocks[J2];i=src['ls'].index(l);j=src['ls'].index(lp)
     v=v+T[z,zz]*src['pt_coefficient'][i,j]
    dst['C'].add_entry(di,dj,v)
 residuals=[];rxmax=F(0)
 for J2,block in blocks.items():
  for lab,(A,Bb)in block['frames'].items():
   H=A.T@block['C']@A
   if Bb is not None:H=H+Bb.T@block['C']@Bb
   H=H-block['base'][lab];H=(H+H.T)*F(1,2);norm=H.max_row_abs_sum();bound=norm/F(J2+1)/block['gram_lower'][lab];rxmax=max(rxmax,bound)
   residuals.append({'J2':J2,'label':lab,'row_sum_operator_norm_upper':str(norm),'trace_normalized_upper':str(bound)})
 ra_norm=ra.max_abs();loss_a=F(D,2)*ra_norm;loss_x=8*rxmax;margin=const-loss_a-loss_x
 out={'status':'CERTIFIED EXCLUSION' if margin>0 else 'NOT CERTIFIED','n':n,'rank':K,'distance':5,'precision_binary_bits':PREC,'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'constant_exact':str(const),'a_residual_infinity_upper':str(ra_norm),'a_residual_penalty_upper':str(loss_a),'X_residual_trace_penalty_upper':str(loss_x),'strict_contradiction_margin_lower_exact':str(margin),'strict_contradiction_margin_lower_float':float(margin),'positive_scalar_duals':clipped,'PSD_dual_certification':'Every PSD dual defined exactly as product of supplied dyadic factor with its transpose; interval multiplication encloses that exact matrix.','exact_M_and_trace_normalization_independently_verified':True,'frame_rank_and_gram_checks':rankchecks,'reduced_residuals':residuals,'elapsed_seconds':time.perf_counter()-start,'mathematical_scope':'Necessary three-copy invariant moment conditions for an arbitrary complex rank-two code in spin n/2. Analytic S3/Racah recoupling and partial-time-reversal identities used; all coefficient calculations and final inequalities certified by directed integer intervals. Not a floating solver-status argument.'}
 target=Path(__file__).parent/'interval_certificate.json';target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['frame_rank_and_gram_checks','reduced_residuals']},indent=2),flush=True)
if __name__=='__main__':main(sys.argv[1])
