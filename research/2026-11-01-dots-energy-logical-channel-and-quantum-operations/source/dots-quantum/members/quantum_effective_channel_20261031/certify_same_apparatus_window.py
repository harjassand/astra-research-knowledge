#!/usr/bin/env python3
"""Exact Gaussian-integer scaling/squaring certificate; no floating expm used."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import numpy as np,json,hashlib,time
BITS=128; SCALE=1<<BITS; DEGREE=48

def eye(n): return np.eye(n,dtype=object)
def zeros(n):return np.zeros((n,n),dtype=object)
def mul(A,B):
 a,b=A;c,d=B
 return a@c-b@d,a@d+b@c

def nearest(a,d):
 return (a+d//2)//d if a>=0 else -((-a+d//2)//d)
def rounded(A,d):return tuple(np.array([[nearest(int(x),d) for x in row] for row in M],dtype=object) for M in A)
def diss_real(L):
 n=len(L); B=L.T@L
 return np.kron(L,L)-(np.kron(eye(n),B)+np.kron(B.T,eye(n)))/F(2)
def ham_imag(H):
 n=len(H);return -(np.kron(eye(n),H)-np.kron(H.T,eye(n)))
def encode12(A):
 out=[]
 for M in A:
  assert all((F(x)*12).denominator==1 for x in M.flat)
  out.append(np.array([[int(F(x)*12) for x in row] for row in M],dtype=object))
 return tuple(out)
def exp_cert(A,C,d):
 """A numerator over12, C upper diamond generator norm, channel dimension d."""
 n=len(A[0]); N=1;s=0
 while N<4*C:N*=2;s+=1
 D=12*N; den=1; acc=(eye(n),zeros(n))
 # Exact Horner Taylor, no intermediate rounding.
 for j in range(DEGREE,0,-1):
  acc=mul(A,acc);acc=(acc[0]+j*D*den*eye(n),acc[1]);den*=j*D
 acc=rounded(tuple(M*SCALE for M in acc),den)
 for _ in range(s):acc=rounded(mul(acc,acc),SCALE)
 tail=F(2,4**(DEGREE+1)); rounding=F(2*d**3,SCALE)
 # e_base<=tail+r; x=e+r obeys x_next<=(1+x)^2-1.
 x=tail+2*rounding
 assert N*x<=F(1,2)
 err=2*N*x
 assert err<F(1,10**18)
 return acc,err,dict(dimension=d,squarings=s,N=N,Taylor_degree=DEGREE,dyadic_bits=BITS,generator_diamond_bound=str(C),Taylor_tail=str(tail),rounding_bound=str(rounding),final_diamond_error_bound=str(err))

def fracstr(q):return str(q.numerator)+'/'+str(q.denominator)
def sqrt_upper(q,bits=100):
 den=1<<bits;num=(q.numerator*den*den+q.denominator-1)//q.denominator
 r=isqrt(num)
 if r*r<num:r+=1
 assert F(r*r,den*den)>=q
 return F(r,den)
def build():
 I=eye(2);Z=np.diag([1,-1]).astype(object);sm=np.array([[0,1],[0,0]],dtype=object);sp=sm.T
 K=zeros(6)
 e10=zeros(3);e10[1,0]=1;e20=zeros(3);e20[2,0]=1
 K=np.kron(e10,sm)+F(1,2)*np.kron(e20,sp);K=K+K.T
 L1=zeros(3);L1[0,1]=L1[2,1]=1
 L2=zeros(3);L2[0,2]=1
 G=diss_real(np.kron(L1,I))+2*diss_real(np.kron(L2,I))
 H=np.kron(eye(3),F(1,3)*Z)+1000*K
 physical=encode12((10**6*G,ham_imag(H)))
 effective=encode12((2*diss_real(sm)+F(1,2)*diss_real(sp),ham_imag(F(1,3)*Z)))
 return physical,effective

def main():
 t=time.time();physical,effective=build()
 full,ep,mp=exp_cert(physical,F(8002002),6)
 target,et,mt=exp_cert(effective,F(6),2)
 # Cold |0><0| source, then exact source trace; column-major vectorization.
 reduced=tuple(np.array([[sum(M[(2*a+i)+6*(2*a+j),u+6*v] for a in range(3)) for v in range(2) for u in range(2)] for j in range(2) for i in range(2)],dtype=object) for M in full)
 parity=np.array([1,-1,-1,1],dtype=object)
 # +/-K apparatus branches are related by exact system Z conjugation.
 paired=tuple(np.array([[M[i,j] if parity[i]*parity[j]==1 else 0 for j in range(4)] for i in range(4)],dtype=object) for M in reduced)
 difference=tuple(a-b for a,b in zip(reduced,target));pdiff=tuple(a-b for a,b in zip(paired,target))
 # Every qubit superoperator entry occurs once in its unnormalized Choi reshuffle.
 frob2=F(sum(int(x)**2 for M in pdiff for x in M.flat),SCALE*SCALE)
 upper=2*sqrt_upper(frob2)+ep+et
 # Explicit rational input/Pauli probes, exact Gaussian rational operations.
 paulis={
 'X':(np.array([[0,1],[1,0]],dtype=object),zeros(2)),
 'Y':(zeros(2),np.array([[0,-1],[1,0]],dtype=object)),
 'Z':(np.diag([1,-1]).astype(object),zeros(2))}
 witnesses=[]
 for name,(ar,ai) in paulis.items():
  for sign in [-1,1]:
   rr=(eye(2)+sign*ar);ri=sign*ai # numerator with denominator2
   vr=rr.reshape(4,order='F');vi=ri.reshape(4,order='F')
   yr=difference[0]@vr-difference[1]@vi;yi=difference[0]@vi+difference[1]@vr
   yr=yr.reshape((2,2),order='F');yi=yi.reshape((2,2),order='F')
   for obs,(br,bi) in paulis.items():
    val=F(int(np.trace(br@yr-bi@yi)),2*SCALE)
    imag=int(np.trace(br@yi+bi@yr));assert imag==0
    witnesses.append((abs(val),name,sign,obs,val))
 best=max(witnesses);lower=best[0]-ep-et
 assert lower>F(1,10000)
 assert upper<F(1,10000)
 # Exact dyadic matrices permit independent replay of all Choi/witness arithmetic.
 artifact={'scale_bits':BITS,'physical_reduced_real':reduced[0].tolist(),'physical_reduced_imag':reduced[1].tolist(),'effective_real':target[0].tolist(),'effective_imag':target[1].tolist()}
 artifact={k:([[str(x) for x in row] for row in v] if isinstance(v,list) else v) for k,v in artifact.items()}
 ap=Path(__file__).with_name('same_apparatus_exact_matrices.json');ap.write_text(json.dumps(artifact,indent=2)+'\n')
 out={'scope':'Certified finite numerical same-apparatus cold-input interval T=1, lambda=1000000. No gate backend. Strong ordinary improvement is system-Z twirling itself.',
 'physical':mp,'effective':mt,'matrix_artifact_sha256':hashlib.sha256(ap.read_bytes()).hexdigest(),
 'witness':{'input':f'(I+({best[2]}){best[1]})/2','observable':best[3],'signed_approximate_expectation_exact':fracstr(best[4]),'certified_absolute_expectation_lower':fracstr(lower),'lower_decimal_display_only':float(lower)},
 'paired_complete_channel':{'Choi_Frobenius_squared_exact':fracstr(frob2),'certified_diamond_upper':fracstr(upper),'upper_decimal_display_only':float(upper),'inequality':'diamond <= ||J||1 <= 2||J||F, plus certified physical/effective exponential errors'},
 'target_error':'1/10000','unpaired_fails':True,'paired_passes':True,'elapsed_seconds_diagnostic':time.time()-t}
 p=Path(__file__).with_name('same_apparatus_certified_window.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
