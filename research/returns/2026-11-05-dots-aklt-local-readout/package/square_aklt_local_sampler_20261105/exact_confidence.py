"""Outward rational Hoeffding confidence arithmetic for bounded iid samples."""
from fractions import Fraction as F
from math import isqrt
from exact_lazy_time import log_bounds

def rational_probability(alpha):return F(str(alpha)) if isinstance(alpha,float) else F(alpha)
def log_failure_upper(alpha):
 alpha=rational_probability(alpha);assert 0<alpha<1
 return log_bounds(2/alpha,terms=24)[1]
def required_attempts(range_width,epsilon,alpha=F(1,20)):
 r=F(range_width);e=F(epsilon);assert r>0 and e>0
 q=r*r*log_failure_upper(alpha)/(2*e*e)
 return(q.numerator+q.denominator-1)//q.denominator

def confidence_radius(range_width,n,alpha=F(1,20),decimal_places=12):
 assert n>=1 and decimal_places>=0
 r=F(range_width);q=r*r*log_failure_upper(alpha)/(2*n)
 scale=10**decimal_places;a=q.numerator*scale*scale;b=q.denominator;k=isqrt(a//b)
 if k*k*b<a:k+=1
 return F(k,scale)
