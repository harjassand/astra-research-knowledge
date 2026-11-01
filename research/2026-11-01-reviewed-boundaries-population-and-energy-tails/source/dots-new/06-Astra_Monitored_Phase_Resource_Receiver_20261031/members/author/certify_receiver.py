#!/usr/bin/env python3
"""Exact Gaussian-integer CQ exponential and terminal decoding certificate.
No floating matrix exponential or physical data is used by certify_case.
"""
from fractions import Fraction as F
from math import lcm
from pathlib import Path
import numpy as np,json,hashlib,time
BITS=112;S=1<<BITS;DEGREE=48

def eye(n):return np.eye(n,dtype=object)
def zero(n):return np.zeros((n,n),dtype=object)
def mul(A,B):
 a,b=A;c,d=B;return a@c-b@d,a@d+b@c

def near(x,d):return (x+d//2)//d if x>=0 else -((-x+d//2)//d)
def rnd(A,d):return tuple(np.array([[near(int(v),d) for v in row] for row in M],dtype=object) for M in A)

def exponential(A,C,dim):
 """A rational Gaussian matrix generating a contractive CQ semigroup.
 dim is the Hilbert dimension of the classical-direct-sum algebra.
 """
 den=1
 for M in A:
  for x in M.flat:den=lcm(den,F(x).denominator)
 num=tuple(np.array([[int(F(v)*den) for v in row] for row in M],dtype=object) for M in A)
 N=1;s=0
 while N<4*C:N*=2;s+=1
 n=len(num[0]);D=den*N;acc=(eye(n),zero(n));dd=1
 for j in range(DEGREE,0,-1):
  acc=mul(num,acc);acc=(acc[0]+j*D*dd*eye(n),acc[1]);dd*=j*D
 acc=rnd(tuple(M*S for M in acc),dd)
 for _ in range(s):acc=rnd(mul(acc,acc),S)
 tail=F(2,4**(DEGREE+1));rounding=F(2*dim**3,S)
 assert N*(tail+2*rounding)<=F(1,2)
 error=2*N*(tail+2*rounding)
 return acc,error,dict(squarings=s,denominator=den,generator_bound=str(C),bits=BITS,degree=DEGREE,cb_error=str(error))

def build(c,loss,up,em,ep,dt,dark=F(0)):
 I=eye(2);X=np.array([[0,1],[1,0]],dtype=object);sm=np.array([[0,1],[0,0]],dtype=object);Q=sm.T@sm;P=I-Q
 Ar=-F(1,2)*loss*(np.kron(I,Q)+np.kron(Q,I))-F(1,2)*up*(np.kron(I,P)+np.kron(P,I))
 Ai=-c*(np.kron(I,X)-np.kron(X,I))
 Jm=loss*np.kron(sm,sm);Jp=up*np.kron(sm.T,sm.T)
 A=(zero(16),zero(16))
 for p in [0,1]:
  for flag in [0,1]:
   src=p+2*flag;sl=slice(4*src,4*src+4)
   A[0][sl,sl]+=Ar;A[1][sl,sl]+=Ai
   if flag==0:
    A[0][sl,sl]-=dark*eye(4)
    dst=1-p+2;A[0][4*dst:4*dst+4,sl]+=dark*eye(4)
    # Captured jump is included in the known correction; residual parity unchanged.
    dst=p+2;A[0][4*dst:4*dst+4,sl]+=em*Jm+ep*Jp
    dst=1-p;A[0][4*dst:4*dst+4,sl]+=(1-em)*Jm+(1-ep)*Jp
   else:
    dst=1-p+2;A[0][4*dst:4*dst+4,sl]+=Jm+Jp
 return tuple(M*dt for M in A),dt*(2*c+12*(loss+up)+8*dark)

def signed_instruments(E):
 """Input parity even; Fourier difference of the output parity blocks."""
 return tuple(tuple(M[8*f:8*f+4,:4]-M[8*f+4:8*f+8,:4] for M in E) for f in [0,1])

def vecmul(A,v):
 a,b=A;c,d=v;return a@c-b@d,a@d+b@c

def certify_case(c=F(1),loss=F(256),up=F(0),eta_m=F(99,100),eta_p=F(0),T=F(1),bins=4,readout=F(1,1000),q0=0,dark=F(0),endpoint='noisy_bit'):
 args=locals().copy();A,C=build(c,loss,up,eta_m,eta_p,T/bins,dark)
 E,err,meta=exponential(A,C,8);Ms=signed_instruments(E)
 v=np.zeros(4,dtype=object);v[0 if q0==0 else 3]=1
 branches=[(v,np.zeros(4,dtype=object))]
 for _ in range(bins):branches=[vecmul(M,v) for v in branches for M in Ms]
 den=S**bins;score=F(0);blind=F(0)
 for v,imag in branches:
  assert imag[0]==0 and imag[3]==0
  if endpoint=='noisy_bit':
   blind+=(1-2*readout)*F(int(v[0]+v[3]),den)
   score+=abs((1-readout)*F(int(v[0]),den)-readout*F(int(v[3]),den))
   score+=abs((1-readout)*F(int(v[3]),den)-readout*F(int(v[0]),den))
  elif endpoint=='none':
   blind+=F(int(v[0]-v[3]),den)
   score+=abs(F(int(v[0]-v[3]),den))
  else:raise ValueError('Unknown endpoint operation')
 # m-fold approximate instrument versus true complete record instrument.
 # Each approximate step norm <=1+err; telescope <=(1+err)^m-1.
 total=(1+err)**bins-1
 p=(1-score)/2;pb=(1-blind)/2
 # Terminal outcome/Pauli decision are contractive. Score and success are
 # Lipschitz in the cq trace norm; use full total as deliberately safe risk radius.
 out={'parameters':{k:str(v) for k,v in args.items()},'exponential':meta,'process_risk_radius':str(total),'bayes_risk_interval':[str(max(F(0),p-total)),str(min(F(1),p+total))],'blind_risk_interval':[str(max(F(0),pb-total)),str(min(F(1),pb+total))],'bayes_risk_display':float(p),'blind_risk_display':float(pb),'scope':'Exact declared finite-source/one-click-bin model, known initial source bit, explicit noisy-bit or absent endpoint operation. Not physical detector calibration.'}
 return out

def certify_echo(c,loss,up,T,bins):
    r=(loss+up)/2
    M=np.array([[0,-2*c],[2*c,-r]],dtype=object)*(T/bins)
    E,err,meta=exponential((M,zero(2)),(2*c+r)*T/bins,2)
    v=np.array([1,0],dtype=object);D=np.array([[1,0],[0,-1]],dtype=object)
    for j in range(bins):v=(E[0] if j%2==0 else D@E[0]@D)@v
    p=(1-F(int(v[0]),S**bins))/2;total=(1+err)**bins-1
    return {'raw_dephasing_interval':[str(max(F(0),p-total)),str(min(F(1),p+total))],'risk_display':float(p),'pi_pulses':bins-1,'exponential':meta,'scope':'Ideal instantaneous data sign flips, no pulse errors included. Euclidean-contractive exact telegraph ODE.'}

if __name__=='__main__':
 rows=[]
 for l in [16,64,256,1024,4096]:
  row=certify_case(loss=F(l));row['no_record_comparator']=certify_echo(F(1),F(l),F(0),F(1),1);row['three_pulse_echo_comparator']=certify_echo(F(1),F(l),F(0),F(1),4);row['photon_only_receiver']=certify_case(loss=F(l),endpoint='none',readout=F(0));rows.append(row)
 out={'method':'Gaussian-integer Taylor scaling and squaring, CQ completely bounded norm remainder; optimal complete-record terminal Pauli decoder','rows':rows}
 p=Path(__file__).with_name('receiver_certificates.json');p.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps([{k:r[k] for k in ['parameters','bayes_risk_display','blind_risk_display']} for r in rows],indent=2))
