#!/usr/bin/env python3
"""Exact coherent-projection overlap of driven damped source and its entire field.
Uses 2x2 real negative-definite matrix contraction, not a Fock truncation.
"""
from fractions import Fraction as F
from math import isqrt,lcm
import numpy as np
BITS=128;S=1<<BITS;DEGREE=48

def sqrt_up(x,bits=100):
 assert x>=0
 d=1<<bits;n=(x.numerator*d*d+x.denominator-1)//x.denominator;r=isqrt(n)
 if r*r<n:r+=1
 return F(r,d)

def near(x,d):return (x+d//2)//d if x>=0 else -((-x+d//2)//d)
def round_matrix(M,d):return np.array([[near(int(x),d) for x in row] for row in M],dtype=object)

def certify_overlap(lam,b,T):
 assert lam>0 and b>=0 and T>=0
 rn=isqrt(lam.numerator);rd=isqrt(lam.denominator)
 assert rn*rn==lam.numerator and rd*rd==lam.denominator,'This exact frontend receives rational sqrt(lambda) only.'
 c=F(rn,rd)*b
 B=np.array([[-2*b*b,c],[c,-lam/2-2*b*b]],dtype=object)*T
 den=1
 for x in B.flat:den=lcm(den,F(x).denominator)
 A=np.array([[int(x*den) for x in row] for row in B],dtype=object)
 C=(lam/2+2*b*b+c)*T
 N=1;s=0
 while N<4*C:N*=2;s+=1
 D=den*N;acc=np.eye(2,dtype=object);dd=1
 for j in range(DEGREE,0,-1):acc=A@acc+j*D*dd*np.eye(2,dtype=object);dd*=j*D
 acc=round_matrix(acc*S,dd)
 for _ in range(s):acc=round_matrix(acc@acc,S)
 tail=F(2,4**(DEGREE+1));r=F(4,S)
 assert N*(tail+2*r)<=F(1,2)
 err=2*N*(tail+2*r)
 a=F(int(acc[0,0]),S);lo=max(F(0),a-err);hi=min(F(1),a+err)
 delta=min(F(2),2*sqrt_up(2-2*lo))
 return {'amplitude_interval':[str(lo),str(hi)],'complete_channel_comparison_upper':str(delta),'display_only':{'overlap':float(a),'channel_upper':float(delta)},'certificate':{'bits':BITS,'degree':DEGREE,'squarings':s,'generator_operator_norm_bound':str(C),'exponential_error':str(err)},'scope':'Exact initialized source+entire-emitted-field coherent projection, known cold source and vacuum input. No optical apparatus calibration.'}
