"""Valid-counter arithmetic only, not physical/counter provenance validation."""
from fractions import Fraction as F
from math import comb,isqrt

def upper_root(x,bits=32):
 x=F(x)
 if x<0:raise ValueError('negative radicand')
 scale=1<<bits;n=x.numerator*scale*scale;d=x.denominator;r=isqrt(n//d)
 if r*r*d<n:r+=1
 return F(r,scale)

def evaluate(*,T,J,t,services,p,m,score_upper,k_loss=20,k_fault=20,verified_code=False,resource_abort=False):
 if any(type(x) is not int for x in [T,J,t,services,m,k_loss,k_fault]):raise ValueError('integer parameters required')
 if T<1 or not 1<=J<=T or not 0<=services<=J or not 0<=t<=J or m<1 or (m+1)%2 or min(k_loss,k_fault)<1:raise ValueError('invalid public counts')
 p=F(p);score_upper=F(score_upper)
 if not 0<p<1:raise ValueError('invalid role probability')
 n=m+1;alpha=F(2**n,comb(n,n//2)//(n//2+1))
 radius=F(45*m,p)*upper_root(F(T*k_loss,2))
 selected=max(F(0),score_upper+radius)
 bad=(1-p)*alpha*selected+upper_root(F(T*k_fault,2))
 return dict(accept=verified_code is True and resource_abort is False and services==J and bad<=t,selected_loss_upper=str(selected),loss_radius=str(radius),bad_count_upper=str(bad),half_diamond_budget=str(F(1,2**k_loss)+F(1,2**k_fault)),scope='Only valid predeclared parameters and genuine prequential upper counters have theorem meaning; no physical provenance or yield claim.')
