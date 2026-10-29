"""Rational-unitary three-qubit Naimark synthesis from <=4 rational qubit effects.
Numeric QR only proposes gates. Every gate and resulting effect checked rationally.
"""
from fractions import Fraction as F
from dataclasses import dataclass
import numpy as np
from certified_projection_v1 import sqrt_interval,matrix,coeff
@dataclass(frozen=True)
class C:
 r:F=F(0)
 i:F=F(0)
 def __add__(a,b):return C(a.r+b.r,a.i+b.i)
 def __neg__(a):return C(-a.r,-a.i)
 def __sub__(a,b):return a+-b
 def __mul__(a,b):return C(a.r*b.r-a.i*b.i,a.r*b.i+a.i*b.r)
 def conj(a):return C(a.r,-a.i)
 def norm2(a):return a.r*a.r+a.i*a.i
 def data(a):return [str(a.r),str(a.i)]
Z=C();O=C(F(1));NEG=C(F(-1))
def eye(n):return [[O if i==j else Z for j in range(n)] for i in range(n)]
def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),Z) for col in zip(*B)] for row in A]
def adj(A):return [[A[j][i].conj() for j in range(len(A))] for i in range(len(A[0]))]
def dy(x,bits):return F(round(float(x)*(1<<bits)),1<<bits)
def su2_round(G,bits=48):
 a,b=G[0];sign=-1 if a.real<-.9 else 1;a*=sign;b*=sign
 t=[dy(x/(1+a.real),bits) for x in [a.imag,b.real,b.imag]]
 den=1+sum(x*x for x in t);w=(1-sum(x*x for x in t))/den
 q=[2*x/den for x in t];alpha=C(sign*w,sign*q[0]);beta=C(sign*q[1],sign*q[2])
 M=[[alpha,beta],[-beta.conj(),alpha.conj()]]
 assert mm(adj(M),M)==eye(2)
 return M

def phase_round(z,bits=48):
 sign=-1 if z.real<-.9 else 1;z*=sign;t=dy(z.imag/(1+z.real),bits)
 out=C(sign*(1-t*t)/(1+t*t),sign*2*t/(1+t*t));assert out.norm2()==1
 return out

def apply_rows(U,indices,G):
 old=[U[i][:] for i in indices]
 new=mm(G,old)
 for i,row in zip(indices,new):U[i]=row

def physical_effects(U,m):
 # Ancilla outcome a occupies rows2a,2a+1; input ancilla00 uses columns0,1.
 return [mm(adj([row[:2] for row in U[2*a:2*a+2]]),[row[:2] for row in U[2*a:2*a+2]]) for a in range(m)]
def target_matrix(v):
 a,x,y,z=v
 return [[C(a+z),C(x,-y)],[C(x,y),C(a-z)]]

def synthesis(effects,bits=48):
 assert 1<=len(effects)<=4
 padded=effects+[[F(0)]*4 for _ in range(4-len(effects))]
 blocks=[]
 for e in padded:
  ev,W=np.linalg.eigh(matrix(e));blocks.append((W*np.sqrt(np.maximum(ev,0))[None,:])@W.conj().T)
 V=np.concatenate(blocks)
 U,R=np.linalg.qr(V,mode='complete')
 for j in range(2):
  phase=R[j,j]/abs(R[j,j]);U[:,j]*=phase
 work=U.copy();left=[]
 for j in range(8):
  for i in range(7,j,-1):
   a,b=work[i-1,j],work[i,j];r=np.sqrt(abs(a)**2+abs(b)**2)
   if r<1e-30:continue
   G=np.array([[np.conj(a)/r,np.conj(b)/r],[-b/r,a/r]])
   work[[i-1,i]]=G@work[[i-1,i]]
   left.append(([i-1,i],su2_round(G,bits)))
 # Circuit application order: phases first, then reversed adjoints of left eliminations.
 exact=eye(8);gates=[]
 for j in range(8):
  z=phase_round(work[j,j]/abs(work[j,j]),bits)
  exact[j]=[z*x for x in exact[j]];gates.append({'kind':'basis_phase','basis':j,'phase':z.data()})
 for indices,G in reversed(left):
  G=adj(G);apply_rows(exact,indices,G)
  gates.append({'kind':'two_level_su2','basis':indices,'matrix':[[x.data() for x in row] for row in G]})
 # Exact unitary follows from the checked primitive identities, without giant full-product Gram denominators.
 actual=physical_effects(exact,4);target=[target_matrix(v) for v in padded]
 error_bounds=[]
 for A,B in zip(actual,target):
  err=sum((A[i][j]-B[i][j]).norm2() for i in range(2) for j in range(2))
  lo,hi=sqrt_interval(err,128);error_bounds.append(hi)
 # Difference of measure/correct channels: half diamond <=(1/2) sum ||E-E'||op <= Frobenius bound.
 channel_bound=sum(error_bounds)/2
 count=0
 for g in gates:
  if g['kind']=='basis_phase':count+=1
  else:
   h=(g['basis'][0]^g['basis'][1]).bit_count();count+=2*(h-1)+1
 return {'effects':[[str(x) for x in e] for e in effects],'gate_parameter_bits':bits,'qubits':3,'ancilla_qubits':2,'gates':gates,'two_controlled_one_qubit_primitives_upper':count,'effect_Frobenius_upper':[str(x) for x in error_bounds],'correction_channel_half_diamond_upper':str(channel_bound),'correction_channel_half_diamond_upper_float':float(channel_bound),'scope':'Exact rational unitary gate model; physical gate, ancilla and readout error additional.'}
