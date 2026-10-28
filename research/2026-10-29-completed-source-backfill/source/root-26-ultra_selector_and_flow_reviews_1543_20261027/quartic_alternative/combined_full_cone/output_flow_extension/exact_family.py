"""Rational affine-parameter dual covering all b and all admitted gamma."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr
import sys,json,time
import numpy as np
import sympy as s
from sympy.polys.matrices import DomainMatrix
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from maps import load
from exact_acoustic import ldl


def matrix(rows):return DomainMatrix.from_Matrix(s.Matrix(rows)).convert_to(s.QQ)
def fraction(x):return F(int(x.numerator),int(x.denominator))
def dot(x,y):return sum((a*b for a,b in zip(x,y)),F(0))


def closure_eta(d,lam):
    C=matrix([[F(float(x)) for x in row] for row in d['C']]).transpose()
    O=matrix([[F(float(x)) for x in row] for row in d['O']]).transpose()
    rhs=O.matmul(matrix(lam));_,cols=C.rref();cols=list(cols)
    cp=C.extract(list(range(60)),cols);_,rows=cp.transpose().rref();rows=list(rows)
    correction=cp.extract(rows,list(range(len(cols)))).lu_solve(rhs.extract(rows,[0]))
    eta=[F(0)]*16
    for j,c in zip(cols,correction.to_list()):eta[j]=fraction(c[0])
    assert C.matmul(matrix(eta))==rhs
    return eta


def main():
    start=time.monotonic();d=load();flow=json.loads((ROOT/'FLOW_MAPS.json').read_text())
    ef,ejf,ed,ejd=[list(map(F,flow[k])) for k in ['standard_F','mixed_F','standard_det2','mixed_det2']]
    G=F(json.loads((ROOT/'GAMMA_BOUND.json').read_text())['used_rational_upper_bound'])
    on=[[F(float(x)) for x in row] for row in d['ON'].T]
    zero=[F(0)]*210
    equations=[row+zero for row in on]+[zero+row for row in on]
    equations += [ejf+zero,[-G*x for x in ejd]+ejf,zero+ejd]
    C=matrix(equations);_,cols=C.rref();cols=list(cols);rank=len(cols)
    cp=C.extract(list(range(C.shape[0])),cols);_,rows=cp.transpose().rref();rows=list(rows)
    square=cp.extract(rows,list(range(rank)))
    H=[[3,0,1],[0,1,0],[1,0,3]]
    anchor=[F(H[k%3][l%3] if i==j and k//3==l//3 else 0)
            for i,j in cwr(range(4),2) for k,l in cwr(range(6),2)]+zero
    assert C.matmul(matrix(anchor)).is_zero_matrix
    numeric=np.load(ROOT/'PARAMETER_FAMILY_NUMERIC.npz');floating=np.r_[numeric['L0'],numeric['L1']]
    attempts=[];weight=F(1,100000)
    for denominator in [10**10,10**12]:
        values=[F(round(float(x)*denominator),denominator) for x in floating]
        residual=C.matmul(matrix(values));delta=square.lu_solve(residual.extract(rows,[0]))
        for j,c in zip(cols,delta.to_list()):values[j]-=fraction(c[0])
        values=[x+weight*a for x,a in zip(values,anchor)]
        assert C.matmul(matrix(values)).is_zero_matrix
        l0,l1=values[:210],values[210:];end=[a+b for a,b in zip(l0,l1)]
        Y0=[[l0[int(d['heat_indices'][24*i+j])] for j in range(24)] for i in range(24)]
        Ye=[[end[int(d['heat_indices'][24*i+j])] for j in range(24)] for i in range(24)]
        q0=dot(l0,ef);q1=dot(l1,ef)-G*dot(l0,ed);q2=-G*dot(l1,ed)
        bern=[q0,q0+q1/2,q0+q1+q2]
        try:
            assert all(x<0 for x in bern),bern
            piv0=ldl(Y0);pive=ldl(Ye);break
        except AssertionError as error:attempts.append({'denominator':denominator,'reason':str(error)[:180]})
    else:raise AssertionError('exact parameter family not reconstructed')
    eta0,eta1=closure_eta(d,l0),closure_eta(d,l1)
    out={'status':'EXACT_ALL_B_AFFINE_GAMMA_PURE_FLOW_SEPARATOR_ACQUIRED',
         'target_coefficients':flow['target_coefficients'],'gamma_upper':str(G),
         'L0':list(map(str,l0)),'L1':list(map(str,l1)),
         'closedness_eta0':list(map(str,eta0)),'closedness_eta1':list(map(str,eta1)),
         'moment0_LDL_pivots':list(map(str,piv0)),'moment_end_LDL_pivots':list(map(str,pive)),
         'energy_power_coefficients':list(map(str,[q0,q1,q2])),'energy_Bernstein_coefficients':list(map(str,bern)),
         'mixed_identities':[str(dot(l0,ejf)),str(dot(l1,ejf)-G*dot(l0,ejd)),str(dot(l1,ejd))],
         'linear_rank':rank,'rounding_denominator':denominator,'Gaussian_weight':str(weight),
         'rejected_reconstructions':attempts,'seconds':time.monotonic()-start,
         'scope':'Pure symmetric target minus nonnegative gamma det²; all canonical real b and gamma in proved interval. General constant stronglyparabolic output flows follow only by the actual target symmetries. Not an unknown-component combined-flow theorem.'}
    (ROOT/'EXACT_FLOW_FAMILY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['L0','L1','closedness_eta0','closedness_eta1','moment0_LDL_pivots','moment_end_LDL_pivots']},indent=2))


if __name__=='__main__':main()
