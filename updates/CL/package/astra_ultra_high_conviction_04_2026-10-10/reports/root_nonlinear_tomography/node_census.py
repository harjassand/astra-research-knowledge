"""Exact finite-jet node census in a synchronized hidden-block family.

This is an exact Fraction algebra diagnostic, NOT a noise-tolerant laboratory
protocol. The physical model has one port and m hidden nodes, homogeneous
cubic coefficient alpha, and identical port coupling -c/sqrt(m). Any hidden
weighted graph Laplacian is invisible on the synchronized trajectory.
In orthonormal aggregate coordinates, the dynamics are
 y'=-a*y+c*z-alpha*y**3+u; z'=c*y-d*z-(alpha/m)*z**3.
The linear IO response has dimension two for every m. We infer m from the
cubic coefficient of the eighth-order step response, without supplying m
to the recovery formula.
"""
from fractions import Fraction as Q
import json
from pathlib import Path

def response(a, d, c, alpha, beta, depth=8):
    # Coefficients of t^j * u^p, keeping p <= 3, sufficient for this claim.
    y = [[Q(0) for _ in range(4)] for _ in range(depth+1)]
    z = [[Q(0) for _ in range(4)] for _ in range(depth+1)]
    def cube(v, k, p):
        return sum((v[i][l]*v[j][r]*v[k-i-j][p-l-r]
                    for i in range(k+1) for j in range(k-i+1)
                    for l in range(p+1) for r in range(p-l+1)), Q(0))
    for k in range(depth):
        for p in range(4):
            y[k+1][p] = (-a*y[k][p]+c*z[k][p]-alpha*cube(y,k,p)
                         +int(k==0 and p==1))/(k+1)
            z[k+1][p] = (c*y[k][p]-d*z[k][p]-beta*cube(z,k,p))/(k+1)
    return y,z

def run():
    a,d,c,alpha=Q(3),Q(2),Q(1),Q(3,5)
    rows=[]
    for m in [1,2,3,7,64,1000]:
        data,_=response(a,d,c,alpha,alpha/m)
        # Data-only extraction of linear quotient and common cubic label.
        a_hat=-2*data[2][1]
        c2_hat=6*data[3][1]-a_hat*a_hat
        d_hat=(-24*data[4][1]-a_hat**3-2*a_hat*c2_hat)/c2_hat
        alpha_hat=-4*data[4][3]
        assert (a_hat,d_hat,c2_hat,alpha_hat)==(a,d,c*c,alpha)
        # Here c=1 is exactly the positive square root of the recovered c2.
        reference,_=response(a_hat,d_hat,c,alpha_hat,Q(0))
        delta=data[8][3]-reference[8][3]
        beta_hat=-448*delta/(c2_hat*c2_hat)
        m_hat=alpha_hat/beta_hat
        assert beta_hat==alpha/m and m_hat==m
        # Adjacent population sizes become hard to distinguish: O(m^-2).
        next_data,_=response(a,d,c,alpha,alpha/(m+1))
        gap=abs(data[8][3]-next_data[8][3])
        assert gap==alpha*c**4/(448*m*(m+1))
        rows.append(dict(hidden_nodes=m, inferred_hidden_nodes=str(m_hat),
                         physical_nodes=m+1, linear_minimal_dimension=2,
                         hidden_cubic_residual=str(delta),
                         adjacent_size_coefficient_gap=str(gap)))
    result={'status':'EXACT_SCOPED_ALGEBRA_CHECK_PASS',
            'physical_acquisition':'NOT_IMPLEMENTED',
            'model_assumptions':'homogeneous cubic, synchronized M-matrix hidden block',
            'rows':rows}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    run()
