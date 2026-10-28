"""Exact standard5-qubit code PTM and rational single-qubit sources.
Encoder convention copied from learned_five_qubit_nonpauli_bridge_20261028.py:
XZZXI,IXZZX,XIXZZ,ZXIXZ; |0L>=normalizedP|00000>, |1L>=XXXXX|0L>.
This module has no acquired data or candidate access to source parameters.
"""
import itertools,math
from functools import reduce
import sympy as s
import numpy as np
I=s.eye(2);P=[I,s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
Pnp=[np.array(a,dtype=complex) for a in P]
GWORDS=['XZZXI','IXZZX','XIXZZ','ZXIXZ'];chars='IXYZ'

def mulword(a,b):
 out=[];phase=1
 for x,y in zip(a,b):
  if x==0:out.append(y)
  elif y==0:out.append(x)
  elif x==y:out.append(0)
  else:
   z=6-x-y;out.append(z);phase*=1j if (x,y) in [(1,2),(2,3),(3,1)] else -1j
 return tuple(out),phase
G=[tuple(chars.index(c) for c in w) for w in GWORDS]
STAB=[]
for mask in range(16):
 word=(0,)*5;phase=1
 for j,g in enumerate(G):
  if (mask>>j)&1:word,ph=mulword(word,g);phase*=ph
 assert abs(complex(phase).imag)==0 and complex(phase).real in [-1,1]
 STAB.append((word,int(complex(phase).real)))
COS=[]
for a in range(4):
 row=[]
 for word,phase in STAB:
  ww,ph=mulword(word,(a,)*5);ph*=phase;assert complex(ph).imag==0;row.append((ww,int(complex(ph).real)))
 COS.append(row)

def kron(xs):
 out=s.ones(1,1)
 for x in xs:out=s.kronecker_product(out,x)
 return out

def exact_encoder_recovery():
 Proj=sum((sign*kron([P[a] for a in word]) for word,sign in STAB),s.zeros(32))/16
 zero=Proj[:,0];norm=s.sqrt((zero.H*zero)[0]);zero=zero/norm
 Enc=zero.row_join(kron([P[1]]*5)*zero)
 errors=[s.eye(32)]+[kron([P[a] if k==i else I for k in range(5)]) for i in range(5) for a in [1,2,3]]
 Rec=[Enc.H*E.H for E in errors]
 return Enc,Rec

def stereographic_unitary(t):
 t=list(map(s.Rational,t));den=1+sum(x*x for x in t);q0=(1-sum(x*x for x in t))/den;v=[2*x/den for x in t]
 U=q0*I-s.I*sum((v[j]*P[j+1] for j in range(3)),s.zeros(2));assert (U.H*U-I).applyfunc(s.cancel)==s.zeros(2)
 return U.applyfunc(s.cancel)

def exact_ptm(Ks):
 return s.Matrix(4,4,lambda a,b:s.cancel(sum(s.trace(P[a]*K*P[b]*K.H)/2 for K in Ks)))

def generator_sources():
 # These are generator-only parameters. Learner functions do not receive them.
 axes=[(s.Rational(1,3),s.Rational(1,5),0),(s.Rational(-1,4),s.Rational(2,7),s.Rational(1,6)),(s.Rational(1,5),s.Rational(-1,3),s.Rational(2,9)),(s.Rational(2,5),0,s.Rational(-1,4)),(s.Rational(1,7),s.Rational(3,8),s.Rational(-2,9))]
 frames=[(s.Rational(2,3),s.Rational(1,7),s.Rational(-1,5)),(s.Rational(1,4),s.Rational(-2,5),s.Rational(1,3)),(s.Rational(-2,7),s.Rational(3,5),s.Rational(1,6)),(s.Rational(2,9),s.Rational(1,2),s.Rational(-2,3)),(s.Rational(3,7),s.Rational(-1,5),s.Rational(2,5))]
 rows=[]
 for i,m in enumerate([20,19,18,17,16]):
  t=s.Rational(1,m);c=(1-t*t)/(1+t*t);j=2*t/(1+t*t);gamma=j*j
  A=stereographic_unitary(axes[i]);V=stereographic_unitary(frames[i]);base=[s.diag(1,c),s.Matrix([[0,j],[0,0]])]
  Ks=[(V*A*K*A.H).applyfunc(s.cancel) for K in base]
  rows.append({'gamma':gamma,'axis_U':A,'frame_V':V,'Ks':Ks,'PTM':exact_ptm(Ks),'ideal_residual_PTM':exact_ptm([(V.H*K).applyfunc(s.cancel) for K in Ks])})
 return rows

def logical_ptm(local):
 # Exact Pauli polynomial, equivalent to Enc / local CPTP maps / 16 Rec Kraus.
 nums=[];dens=[]
 for M in local:
  dd=s.ilcm(*[int(s.denom(x)) for x in M]);nums.append([[int(s.cancel(M[a,b]*dd)) for b in range(4)] for a in range(4)]);dens.append(int(dd))
 den=16*math.prod(dens);out=s.zeros(4)
 for a,b in itertools.product(range(4),repeat=2):
  val=0
  for wo,so in COS[a]:
   weight=sum(x!=0 for x in wo);recsum=16-4*weight
   if recsum==0:continue
   for wi,si in COS[b]:
    term=so*si*recsum
    for k in range(5):term*=nums[k][wo[k]][wi[k]]
    val+=term
  out[a,b]=s.Rational(val,den)
 assert out[0,0]==1 and all(out[0,j]==0 for j in [1,2,3])
 return out

def choi(M):return sum((M[a,b]*s.kronecker_product(P[a],P[b].T)/4 for a,b in itertools.product(range(4),repeat=2)),s.zeros(4))
def infidelity(M):return s.cancel((3-sum(M[j,j] for j in [1,2,3]))/4)
def holdout_failure_probabilities(M):
 out=[]
 for j,sg in itertools.product([1,2,3],[-1,1]):
  v=s.cancel((1-M[j,j]-sg*M[j,0])/2);assert 0<=v<=1;out.append(v)
 return out

def numpy_apply_local(rho,Ks,site):
 n=5;sites=[site];rest=[i for i in range(n) if i!=site];perm=sites+rest+[i+n for i in sites]+[i+n for i in rest]
 A=rho.reshape([2]*10).transpose(perm).reshape(2,16,2,16)
 B=sum(np.einsum('ki,irjs,lj->krls',K,A,K.conj(),optimize=True) for K in Ks)
 return B.reshape([2]*10).transpose(np.argsort(perm)).reshape(32,32)

def direct_numeric_ptm(localKs):
 Enc,Rec=exact_encoder_recovery();Enc=np.array(Enc,dtype=complex);Rec=[np.array(r,dtype=complex) for r in Rec]
 outs=[]
 for b in range(4):
  A=Enc@Pnp[b]@Enc.conj().T
  for site,Ks in enumerate(localKs):A=numpy_apply_local(A,[np.array(k,complex) for k in Ks],site)
  outs.append(sum((R@A@R.conj().T for R in Rec),np.zeros((2,2),complex)))
 return np.array([[np.trace(Pnp[a]@outs[b]).real/2 for b in range(4)] for a in range(4)])

if __name__=='__main__':
 sources=generator_sources();identity=[s.eye(4)]*5;assert logical_ptm(identity)==s.eye(4)
 for i in range(5):
  ms=[s.eye(4)]*5;ms[i]=sources[i]['ideal_residual_PTM'];assert logical_ptm(ms)==s.eye(4)
 M=logical_ptm([x['ideal_residual_PTM'] for x in sources]);actual=direct_numeric_ptm([[(x['frame_V'].H*k).applyfunc(s.cancel) for k in x['Ks']] for x in sources]);assert np.max(abs(actual-np.array(M,float)))<1e-12
 print('rates',[float(x['gamma']) for x in sources]);print('ideal code infidelity',float(infidelity(M)));print('unencoded infidelities',[float(infidelity(x['ideal_residual_PTM'])) for x in sources]);print('six-state failures',list(map(float,holdout_failure_probabilities(M))))
