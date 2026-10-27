# Exact white-shift boundary reduction for arbitrary qutrit mixed reset

## Theorem

Consider the actual qutrit channel E(rho)=p rho+q Tr(rho)tau, with arbitrary mixed qutrit tau. If its WH3 deficit is negative, there is another actual TP channel of the same form with reset rank at most two and normalized deficit no larger (indeed the unnormalized negative deficit is no larger before renormalization).

The construction subtracts the smallest eigenvalue of the reset noise, then renormalizes. This changes p and q, so it is an all-probability value reduction, NOT a fixed-p monotonicity theorem. A proof on the complete rank-two reset boundary, for all probabilities, would now close the full mixed-qutrit-reset class. That boundary remains to be received here.

More precisely, fix unnormalized main coefficient a>0 and diagonal noise b_i>=0. Put

 D(a,b)=Delta(3a Phi3+I3⊗diag(b)).

For every b and t>=0,

 D(a,b+t1)>=min(D(a,b),0).                              (1)

The common-noise curve has no interior minimum: it is either decreasing to zero or first increasing and then decreasing to zero. Flat intervals are excluded except trivial zero-main cases.

## 1. Actual source-locked integral

Matched physical/reference covariance diagonalizes tau without altering Phi3. The exact white-product determinant identity yields

 D(a,b)=integral_0^infinity F(m(s))ds,
 m_i(s)=a/(s+b_i), g=sum_i m_i,
 F=2sum_i log(1+(g-m_i)/2)-log(1+g)
    -3sum_i log(1+m_i/3).                              (2)

This is the actual matrix-Stieltjes specialization in white_product_noise_matrix_stieltjes_receiver.md. At positive shifts all denominators are positive. Singular b endpoints are handled by convergence/entropy continuity.

Adding t to all b_i shifts s by t. Therefore

 d/dt D(a,b+t1)=-F(m(t)).                               (3)

## 2. Exact single crossing of the integrand

By scaling set a=6 and write d_i=s+b_i. Exponentiating(2) and canceling all common baseline denominators gives

 exp F-1=H(s)/[A(s) product_i(d_i+2)^3],
 A(s)=product_i d_i+6sum_(i<j)d_i d_j,
 H(s)=product_(i<j)[d_i d_j+3(d_i+d_j)]^2
       -A(s) product_i(d_i+2)^3.                        (4)

The denominator is positive for s>0. Write H(s)=sum_(j=0)^10 c_j(b)s^j. Degrees12 and11 cancel, and c_10=72. Coefficients c_10,c_9,c_8,c_7 are polynomials in b_i with nonnegative coefficients.

The exact rational certificate constructs, for j=6,5,...,1, polynomials N_j(b)>=0 and D_j(b)>=1 such that

 N_j(b)c_j(b)-D_j(b)c_(j-1)(b)

has ONLY nonnegative monomial coefficients. Thus c_j<=0 implies c_(j-1)<=0. Reading the coefficient sequence from degree10 downwards, there can be at most one sign variation, with zeros omitted.

Descartes' rule of signs proves that H has at most one positive root, counted with multiplicity. Its positive leading coefficient then implies that either H>0 throughout s>0, or its only positive root is simple and the sign changes from negative to positive. The same sign statement holds for F. This is an exact certificate for all b_i>=0, not a finite-sample root observation.

### Certificate specification and reproducibility

Let e1=b0+b1+b2, e2=b0b1+b0b2+b1b2, e3=b0b1b2.

For j>=4, N_j is expressed in basis(1,e1), D_j=1.
For j=3,2, N_j is expressed in(1,e1,e1^2,e2), and D_j in(1,e1), with constant coefficient1.
For j=1, N_j is expressed in(1,e1,e1^2,e2,e1^3,e1e2,e3), and D_j in(1,e1,e1^2,e2), again constant coefficient1.

Every rational coefficient is recorded in qutrit_mixed_reset_white_shift_certificate.json. The companion Python replay expands(4) and checks every claimed monomial coefficient using exact SymPy rationals, with no floating-point arithmetic or optimizer. All six implications passed. The corresponding nonzero remainder monomial counts are52,79,106,180,168,235; all coefficients are strictly positive after zero monomials are omitted. The discovery used a finite linear program, but no floating solution is part of the proof.

## 3. Receiving the common-noise curve

Equation(3) and the single-crossing theorem show that D(a,b+t1) has at most one critical point, which is a maximum. Its limit as t goes to infinity is zero: expanding f(tI+Z) leaves O(1/t), since all linear/trace terms cancel between the trace-preserving source, WH output and reference maps. Hence its minimum over the compactified half-line is attained at an endpoint, proving(1).

Now start with arbitrary b and let r=min_i b_i, b'=b-r1. Apply(1) to b' and t=r. If D(a,b)<0, then necessarily D(a,b')<0 and

 D(a,b')<=D(a,b).

The new reset has at least one zero eigenvalue. If b'=0 it would be a pure reversible source with deficit zero, contradicting the negative assumption; otherwise its reset rank is one or two. The source trace decreases from3a+3sum_i b_i to3a+3sum_i b'_i while its physical marginal stays scalar. Dividing by the smaller positive trace produces an actual TP normalized Choi state, and strengthens rather than weakens a negative deficit. This proves the theorem.

## Scope and retained frontier

This closes faithful-reset reduction, not the rank-two edge itself. It does not assert that physical twirling lowers the deficit; exact twirl counterexamples remain valid. It does not assert fixed-trace noise concavity, main-weight monotonicity, or positive log-degree terms. The result is a source-compatible counterexample-preserving value reduction with a complete rational sign certificate.
