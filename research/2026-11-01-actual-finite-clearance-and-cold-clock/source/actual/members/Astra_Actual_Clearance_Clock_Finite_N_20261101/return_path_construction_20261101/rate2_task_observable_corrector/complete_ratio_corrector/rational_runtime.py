#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,sys
from exact_fraction_coefficients import h1,h2,h3,c0,c1,c2,c3
sys.set_int_max_str_digits(0)
P=Path(__file__).parent
rows=[('0->A',(1,1,0,0,1)),('A->0',(-1,-1,0,0,-1)),('2A->AC',(-1,F(-1,2),0,1,0)),('AC->2A',(1,F(1,2),0,-1,0)),('2A->AD',(-1,F(-1,2),0,-1,0)),('AD->2A',(1,F(1,2),0,1,0)),('2A->AE',(-1,-1,1,0,0)),('AE->2A',(1,1,-1,0,0)),('AE->CD',(-1,0,-1,0,0)),('CD->AE',(1,0,1,0,0)),('CD->AB',(1,0,0,0,0)),('AB->CD',(-1,0,0,0,0))]
def chi(x):rr,uu,tt,aa,zz,ss=x;return h1(rr,uu,tt,zz,ss)*aa+h2(rr,uu,tt,zz,ss)*aa*aa+h3(rr,uu,tt,zz,ss)*aa**3
def val(x):rr,uu,tt,aa,zz,ss=x;return rr*(1-aa*uu)+chi(x)
def moved(x,j):
 rr,uu,tt,aa,zz,ss=x;da,dl,de,dz,dn=j;c=1+de*uu*tt/rr;h=1+dl*tt
 return rr*c*c/h,uu*c,tt/h,(aa+tt*da)/h,(zz+tt*dz)/h,ss+dn*uu*uu*tt/rr
def rates(x):
 rr,uu,tt,aa,zz,ss=x;cd=(1-aa)**2-zz*zz/4
 return [tt*tt,aa*tt,aa*(aa-tt),aa*(1-aa+zz/2),aa*(aa-tt),aa*(1-aa-zz/2),aa*(aa-tt),aa*rr/uu,aa*rr/uu,2*cd,cd,aa*(ss*rr/uu**2-2+aa-rr/uu)]
def mean(x):
 rr,uu,tt,aa,zz,ss=x;K=ss-uu+2*uu*uu*(1-tt)/rr;Lam=3-3*zz*zz/4+tt*tt
 mu=uu*uu*Lam/(rr*K);et=tt*uu/K
 mm=[1,mu,mu*(mu+et),mu*(mu+et)*(mu+2*et)]
 return 4-3*rr-rr*tt*tt/uu+sum(fn(rr,uu,tt,zz,ss)*m for fn,m in zip([c0,c1,c2,c3],mm))
def cert(x):return {'approx':float(x),'sign':(x>0)-(x<0),'sha256':hashlib.sha256((str(x.numerator)+'/'+str(x.denominator)).encode()).hexdigest(),'numerator_bits':abs(x.numerator).bit_length(),'denominator_bits':x.denominator.bit_length()}
