from fractions import Fraction as F
import json
from pathlib import Path
import sympy as s

def log_bounds(x,n=20):
    z=(x-1)/(x+1)
    assert 0<=z<1
    lo=2*sum((z**(2*j+1)/F(2*j+1) for j in range(n)),F(0))
    hi=lo+2*z**(2*n+1)/(F(2*n+1)*(1-z*z))
    return lo,hi
l43,h43=log_bounds(F(4,3)); l3,h3=log_bounds(F(3))
imlo,imhi=12*l43-3,12*h43-3
iqlo,iqhi=F(3,4)*(2-h3),F(3,4)*(2-l3)
assert imlo-iqhi/2>F(1,9)
assert F(3,2)*imlo-iqhi>0
M=s.symbols('M',real=True)
I=s.eye(9); swap=s.zeros(9)
for a in range(3):
    for b in range(3): swap[3*b+a,3*a+b]=1
X=M*(I+swap)/2+(3-2*M)*(I-swap)/2
R=s.zeros(3); TX=s.zeros(9)
for a in range(3):
    for b in range(3):
        for i in range(3):
            for j in range(3):
                TX[3*a+i,3*b+j]=X[3*b+i,3*a+j]
                if a==b: R[i,j]+=X[3*a+i,3*b+j]
assert s.simplify(R-3*s.eye(3))==s.zeros(3)
phi=s.zeros(9,1)
for a in range(3): phi[3*a+a]=1
out=(s.kronecker_product(s.eye(3),R)-TX)/2
expected=(3+M)*I/4-3*(M-1)*(phi*phi.T)/4
assert s.simplify(out-expected)==s.zeros(9)
report={'status':'PASS','gap_lower':str(imlo-iqhi/2),'gap_lower_float':float(imlo-iqhi/2),'eta_upper_float':float(iqhi/(4*imlo)),'strict_eta_below_3_over_8':True,'sharp_output_floor_exact':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
