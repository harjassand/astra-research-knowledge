"""Exact rational common dual reconstruction, using a strict Gaussian anchor."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr
import json,time
import numpy as np
import sympy as s
from sympy.polys.matrices import DomainMatrix
from maps import load,ROOT,gaussian_moment
from exact_acoustic import ldl


def dm(array):
    return DomainMatrix.from_Matrix(s.Matrix([[s.Rational(float(x)) for x in row] for row in array])).convert_to(s.QQ)
def frac(x):return F(int(x.numerator),int(x.denominator))


def main():
    start=time.monotonic();d=load();p_record=json.loads((ROOT/'heat_normal_extreme_ROC.json').read_text())
    p=list(map(F,p_record['coefficients']));numeric=np.load(ROOT/'heat_normal_extreme_combined.npz')
    # Exact10 selector,45 closed-form and9 shared energy equations.
    C=np.block([[d['A'][:,1830:].toarray().T,np.zeros((10,210))],
                [np.zeros((45,658)),d['ON'].T],
                [d['B'].T,-d['E'].T]])
    cd=dm(C);_,cols=cd.rref();cols=list(cols);rank=len(cols)
    cp=cd.extract(list(range(64)),cols);_,rows=cp.transpose().rref();rows=list(rows)
    square=cp.extract(rows,list(range(rank)))
    lp0=[F(gaussian_moment(e),242) for e in d['pc_exponents']]
    H=[[3,0,1],[0,1,0],[1,0,3]]
    lh0=[F(5,968)*(H[k%3][l%3] if i==j and k//3==l//3 else 0)
         for i,j in cwr(range(4),2) for k,l in cwr(range(6),2)]
    anchor=lp0+lh0
    assert cd.matmul(DomainMatrix.from_Matrix(s.Matrix(anchor)).convert_to(s.QQ)).is_zero_matrix
    normal=np.r_[numeric['dual_0'],numeric['dual_1']]
    attempts=[];weight=F(1,20000)
    for denominator in [10**10,10**12,10**14]:
        v=[F(round(float(x)*denominator),denominator) for x in normal]
        vd=DomainMatrix.from_Matrix(s.Matrix(v)).convert_to(s.QQ)
        residual=cd.matmul(vd);delta=square.lu_solve(residual.extract(rows,[0]))
        for j,c in zip(cols,delta.to_list()):v[j]-=frac(c[0])
        v=[x+weight*a for x,a in zip(v,anchor)]
        exact=DomainMatrix.from_Matrix(s.Matrix(v)).convert_to(s.QQ)
        assert cd.matmul(exact).is_zero_matrix
        lp,lh=v[:658],v[658:]
        Mp=[[lp[int(d['pc_indices'][60*i+j])] for j in range(60)] for i in range(60)]
        Mh=[[lh[int(d['heat_indices'][24*i+j])] for j in range(24)] for i in range(24)]
        g=[sum(F(float(d['B'][j,i]))*lp[j] for j in range(658)) for i in range(9)]
        target=sum(a*b for a,b in zip(g,p))
        try:
            assert target<0,target
            dp=ldl(Mp);dh=ldl(Mh);break
        except AssertionError as error:attempts.append({'denominator':denominator,'reason':str(error)[:150]})
    else:raise AssertionError('exact positive moments not acquired')
    # Store a source-free proof of annihilation of EVERY closed form:
    # lambda_heat O = eta C, where C is the literal16-equation exterior derivative.
    closed=dm(d['C']).transpose();rhs=dm(d['O']).transpose().matmul(DomainMatrix.from_Matrix(s.Matrix(lh)).convert_to(s.QQ))
    _,ecols=closed.rref();ecols=list(ecols);sub=closed.extract(list(range(60)),ecols)
    _,erows=sub.transpose().rref();erows=list(erows)
    eta_sub=sub.extract(erows,list(range(len(ecols)))).lu_solve(rhs.extract(erows,[0]))
    eta=[F(0)]*16
    for j,c in zip(ecols,eta_sub.to_list()):eta[j]=frac(c[0])
    assert closed.matmul(DomainMatrix.from_Matrix(s.Matrix(eta)).convert_to(s.QQ))==rhs
    out={'status':'EXACT_COMMON_PC1_HEAT_SEPARATOR_ACQUIRED',
         'target_coefficients':list(map(str,p)),
         'PC_monomial_order':d['pc_exponents'].tolist(),'PC_lambda':list(map(str,lp)),
         'heat_order':'A_i A_j, i<=j, then jet_k jet_l,k<=l; jet=(uxx,uxy,uyy,vxx,vxy,vyy)',
         'heat_lambda':list(map(str,lh)),'closedness_dual_eta':list(map(str,eta)),
         'shared_energy_normal':list(map(str,g)),'target_pairing':str(target),
         'PC_positive_LDL_pivots':list(map(str,dp)),'heat_positive_LDL_pivots':list(map(str,dh)),
         'homogeneous_degree':'PC6 with |X|² multiplier; heat4 in A and compatible second jet',
         'selector_annihilators':10,'closed_form_dimension':45,'shared_energy_equations':9,
         'linear_constraint_rank':rank,'rounding_denominator':denominator,'Gaussian_weight':str(weight),
         'rejected_reconstructions':attempts,'seconds':time.monotonic()-start,
         'scope':'Excludes the sum of fixed level1 polynomial norm support and identity-diffusion closedquadratic/bilinearSOS heat cones. Does not exclude truePC, higher multipliers, other flows orQC.'}
    (ROOT/'EXACT_COMMON_SEPARATOR.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['PC_monomial_order','PC_lambda','heat_lambda','closedness_dual_eta','PC_positive_LDL_pivots','heat_positive_LDL_pivots']},indent=2))


if __name__=='__main__':main()
