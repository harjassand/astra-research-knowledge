"""Exact rational certificate for a real-source pair Jensen gap payment."""
from fractions import Fraction as F
import json
from pathlib import Path

def log_interval(x, n=40):
    y=(x-1)/(x+1)
    p=sum((y**(2*k+1)/F(2*k+1) for k in range(n)),F(0))*2
    e=2*abs(y)**(2*n+1)/(F(2*n+1)*(1-y*y))
    return p-e,p+e
lo1,hi1=log_interval(F(256,343)); lo2,hi2=log_interval(F(9,7))
lo=lo1/3+F(6,7)-3*hi2
hi=hi1/3+F(6,7)-3*lo2
assert lo>F(1,200)
# K=[[1/6,-1/6],[-1/6,2/3]]. L=3/4:
assert (F(3,4)-F(1,6))*(F(3,4)-F(2,3))-F(1,6)**2>0
receipt={'status':'EXACT PASS','method':'40-term rational atanh log series with geometric remainder',
 'lower':float(lo),'upper':float(hi),'certified_strict_lower':'1/200',
 'scope':'Repairs one actual-source scalar-pair Jensen obstruction; not a universal theorem'}
Path(__file__).with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
