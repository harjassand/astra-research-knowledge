#!/usr/bin/env python3
"""Rational certification of a displayed full-law lower-bound example.
This does not prove the analytic full-law theorem; see its complete proof.
"""
from fractions import Fraction as F
from pathlib import Path
import math,json
k=100;r=F(3,4);D=F(1,2)*r**(2*k+2)*(1+r*r)/(1-r**(2*k+2));E=r**(2*k+1)*(1+r*r)/(1-r**(2*k+2))
scale=10**40
def sqrt_upper(x):
 n=math.isqrt((x.numerator*scale*scale)//x.denominator)+1
 return F(n,scale)
sD=sqrt_upper(D);rho=sqrt_upper(F(1,2));H=3*sD+E
# pi > 3.14 is a standard elementary lower bound. No floating arithmetic.
eps=4*H/F(157,50)
if not rho+3*sD<r:raise RuntimeError('bootstrap gate')
# log2 = 2*atanh(1/3); all omitted terms are positive.
ln2_lower=2*sum(F(1,3)**(2*j+1)/F(2*j+1) for j in range(8))
N=850_000_000_000
if not F(N)*eps/(1-eps)<ln2_lower:raise RuntimeError('product test bound')
report={'status':'PASS','k':k,'a':1,'b':1,'r':str(r),'bootstrap_gate_certified':True,'TV_upper_exact':str(eps),'TV_upper_numeric':float(eps),'log2_lower_exact':str(ln2_lower),'IID_samples_insufficient':N,'confidence_each_model':'.75','absolute_variance_error_strictly_below':'.5','reason':'N eps/(1-eps)<log2 =>(1-eps)^N>1/2; product TV<1/2, contradicting two testing errors <=1/4 each','arithmetic':'Fraction and integer isqrt; pi>157/50','analytic_premise':'work/spectral_acquisition/FULL_LAW_BARRIER.md'}
p=Path(__file__).with_name('SPECTRAL_CONSTANT_CERTIFICATE.json');p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','TV_upper_numeric','IID_samples_insufficient']},indent=2))
