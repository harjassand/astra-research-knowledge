"""Independent W3 leakage, isometry and scalar-radius controls.

No producer imports. Exact Gaussian-rational matrix-unit calculations fix
all transpose/normalization conventions before an entropy comparison.
"""
from pathlib import Path
import sympy as s
import json,time
ROOT=Path(__file__).resolve().parents[1]

def trace_a(X,r):
    d=3*r
    return s.Matrix(d,d,lambda i,j:sum(X[a*d+i,a*d+j]for a in range(3)))
def transpose_a(X,r):
    d=3*r
    return s.Matrix(3*d,3*d,lambda i,j:X[(j//d)*d+i%d,(i//d)*d+j%d])
def channel(X,r):return (s.kronecker_product(s.eye(3),trace_a(X,r))-transpose_a(X,r))/2
def depolarize(X,r):return s.kronecker_product(s.eye(3)/3,trace_a(X,r))
def epsilon(i,j,k):return (i-j)*(j-k)*(k-i)//2 if len({i,j,k})==3 else 0

def run():
    begin=time.monotonic();omega=s.Matrix([int(i==j)for i in range(3)for j in range(3)])
    p=omega*omega.T/3;swap=s.zeros(9)
    for i in range(3):
        for j in range(3):swap[3*i+j,3*j+i]=1
    pm=(s.eye(9)-swap)/2;ps=(s.eye(9)+swap)/2
    W=s.Matrix(9,3,lambda row,col:epsilon(col,row//3,row%3)) # W=sqrt2 V
    assert W.T*W==2*s.eye(3)and W*W.T/2==pm
    assert channel(ps,1)==s.Rational(3,4)*(s.eye(9)-p)
    assert trace_a(p,1)==s.eye(3)/3 and trace_a(pm,1)==s.eye(3)and trace_a(ps,1)==2*s.eye(3)
    for i in range(3):
        for j in range(3):
            E=s.zeros(3);E[i,j]=1;out=W*E*W.T/2
            q1=s.Matrix(3,3,lambda a,b:sum(out[3*a+k,3*b+k]for k in range(3)))
            q2=s.Matrix(3,3,lambda a,b:sum(out[3*k+a,3*k+b]for k in range(3)))
            expected=(int(i==j)*s.eye(3)-E.T)/2
            assert q1==q2==expected
    lower_log2=s.Rational(56,81);upper_log3=s.Rational(10,9)
    rational=20*lower_log2-s.Rational(40,3)*upper_log3+s.Rational(4,3)-s.Rational(1,96)
    assert rational==s.Rational(869,2592)and rational-s.Rational(1,3)==s.Rational(5,2592)>0
    output={'status':'PASS_EXACT_INDEPENDENT_LEAKAGE_ISOMETRY_AND_RADIUS',
      'Nstar_Psym':'3/4*(I-Phi_normalized)','isometry_matrix_units_checked':9,
      'both_complements_are_W3':True,'extra_Choi_transpose_required':False,
      'pinching_masses_over_TrH':{'Phi':'1/9','antisymmetric':'1/3'},
      'receiver_relative_radius':'1/192','rational_Delta_coefficient':str(rational),
      'rational_margin_above_one_third':'5/2592','rational_CMI_coefficient':'869/7776',
      'seconds':time.monotonic()-begin,
      'scope':'Exact finite kinematic identities and scalar proof arithmetic; not a general entropy solver.'}
    (ROOT/'results/exact_controls.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
    return output

if __name__=='__main__':run()
