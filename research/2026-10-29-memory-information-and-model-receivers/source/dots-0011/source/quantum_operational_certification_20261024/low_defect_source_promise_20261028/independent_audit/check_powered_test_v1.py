#!/usr/bin/env python3
from fractions import Fraction as F
from math import ceil,log
from pathlib import Path
import json,hashlib,sys
sys.set_int_max_str_digits(0)
HERE=Path(__file__).parent
def cdf_integer(n,q,k):
 a,b=q.numerator,q.denominator;term=(b-a)**n;num=term
 for t in range(k):
  numerator=term*(n-t)*a;den=(t+1)*(b-a);assert numerator%den==0;term=numerator//den;num+=term
 return num,b**n
rows=[]
for delta in [F(1,20),F(1,100),F(1,200)]:
 q=delta*(1-delta);n=ceil(32*log(1000)/float(q));cut=int(3*n*q/4)
 num,den=cdf_integer(n,q,cut);num2,den2=cdf_integer(n,q/2,cut);reject=den2-num2
 assert num*1000<=den and reject*1000<=den2
 dig=lambda z:hashlib.sha256(str(z).encode()).hexdigest()
 rows.append({'delta':str(delta),'null_q0':str(q),'alternative_q1':str(q/2),'n':n,'cutoff':cut,'source_copies':2*n,'null_false_acceptance':float(F(num,den)),'alternative_rejection':float(F(reject,den2)),'null_numerator_sha256':dig(num),'null_denominator_sha256':dig(den),'alternative_reject_numerator_sha256':dig(reject),'alternative_denominator_sha256':dig(den2)})
(HERE/'powered_test_check_v1.json').write_text(json.dumps({'status':'PASS_EXACT_INTEGER_FALSE_ACCEPT_AND_POWER_CHECKS','beta':'1/1000','rows':rows,'scope':'Fixed protocol design, no acquired experimental or simulated counts.'},indent=2)+'\n');print(json.dumps(rows,indent=2))
