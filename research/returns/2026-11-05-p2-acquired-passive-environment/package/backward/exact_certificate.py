"""Exact dyadic/rational certificate primitives; no floating SVD is trusted."""
from fractions import Fraction
from itertools import combinations


def positive_definite_integer(matrix):
    """Sylvester's criterion via fraction-free Bareiss elimination.

    On a symmetric integer matrix, the successive diagonal pivots are its
    leading principal determinants. No numerical tolerance or pivoting.
    """
    B = [row[:] for row in matrix]
    n = len(B)
    previous = 1
    for k in range(n):
        pivot = B[k][k]
        if pivot <= 0:
            return False
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = B[i][j]*pivot-B[i][k]*B[k][j]
                quotient, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError('Bareiss division was not exact')
                B[i][j] = quotient
        previous = pivot
    return True


def dyadic_scaled_matrix(X):
    """Represent a stored binary64 matrix exactly as integer matrix / D."""
    pairs = [[float(v).as_integer_ratio() for v in row] for row in X]
    D = max(b for row in pairs for _,b in row)
    I = [[a*(D//b) for a,b in row] for row in pairs]
    return I,D


def certify_restricted_lower_bound(X, k, a_num=1, a_den=64):
    """Prove sigma_min(X.T[:,S]/sqrt(q)) > a for every |S|=k."""
    I,D = dyadic_scaled_matrix(X)
    d,q = len(I),len(I[0])
    G = [[sum(I[i][t]*I[j][t] for t in range(q)) for j in range(d)] for i in range(d)]
    # Multiply by a_den**2 to keep all Gram shift entries integral.
    shift = q*a_num*a_num*D*D
    checked = 0
    for S in combinations(range(d),k):
        M = [[a_den*a_den*G[i][j]-(shift if i==j else 0) for j in S] for i in S]
        if not positive_definite_integer(M):
            return {'passed':False,'failing_support':list(S),'supports_checked':checked+1}
        checked += 1
    return {'passed':True,'lower_bound_numerator':a_num,'lower_bound_denominator':a_den,'supports_checked':checked}


def certify_all_row_residuals(Kfit,X,H,eta_squared):
    """Prove ||X.T k_i - H_i||^2/q <= eta_squared, using rational arithmetic."""
    Xf = [[Fraction(float(v)) for v in row] for row in X]
    Hf = [[Fraction(float(v)) for v in row] for row in H]
    Kf = [[Fraction(float(v)) for v in row] for row in Kfit]
    d,q=len(Xf),len(Xf[0])
    ratios=[]
    for i in range(d):
        rr=Fraction(0)
        for t in range(q):
            r=sum((Kf[i][j]*Xf[j][t] for j in range(d)),Fraction(0))-Hf[i][t]
            rr += r*r
        ratio=rr/(q*eta_squared)
        if ratio > 1:
            return {'passed':False,'failing_row':i,'ratio':float(ratio)}
        ratios.append(float(ratio))
    return {'passed':True,'rows_checked':d,'largest_squared_residual_to_budget_ratio':max(ratios)}

if __name__ == '__main__':
    import json
    from pathlib import Path
    import sys
    path = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('certified_network.json')
    data = json.loads(path.read_text())
    X = [[float.fromhex(v) for v in row] for row in data['state_hex']]
    H = [[float.fromhex(v) for v in row] for row in data['control_hex']]
    Kfit = [[float.fromhex(v) for v in row] for row in data['raw_coefficients_hex']]
    a = Fraction(data['alpha_lower']); eta2 = Fraction(data['eta_squared'])
    d,s = data['dimension'],data['sparsity']
    assert all(sum(v!=0 for v in row)<=s for row in Kfit)
    alpha = certify_restricted_lower_bound(X,min(2*s,d),a.numerator,a.denominator)
    residual = certify_all_row_residuals(Kfit,X,H,eta2)
    assert alpha['passed'] and residual['passed']
    tau2 = 4*eta2/(a*a)
    B = [[Fraction(v) if Fraction(v)**2>tau2 else Fraction(0) for v in row] for row in Kfit]
    Kout = [[(B[i][j]+B[j][i])/2 for j in range(d)] for i in range(d)]
    assert Kout == [[Fraction(v) for v in row] for row in data['output_stiffness_rational']]
    # Delta^2 = (2*s*tau)^2; positivity is rationally decidable.
    delta2 = 4*s*s*tau2
    m = Fraction(data['m_assumption'])
    assert delta2 < m*m
    print(json.dumps({'passed':True,'restricted_injectivity':alpha,'row_residuals':residual,
                      'exact_output_threshold_and_symmetry':True,
                      'delta_less_than_assumed_m':True,
                      'conditional_assumptions':['true sparse symmetric quadratic law',
                          'supplied m and L bounds','true-row residual at most eta']},indent=2))
