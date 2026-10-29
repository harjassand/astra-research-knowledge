# Gap-free soft polar recovery from a known error frame

28 October2026. Root derivation candidate, independent review pending. This is a physical recovery lemma conditional on efficient block access; it does NOT supply that access or a Schur branching oracle. The intended application is separately under construction. No hardware or novelty assertion.

## 1. Exact finite interface

Let F_i:C^K -> C^D, i=1,...,N, be a specified family. Write M:C^N tensor C^K -> C^D for M(|i> tensor |v>)=F_i|v>, and G=M†M. Let S>=0, TrS=1, and assume the actual source

 E_S(rho)=sum_{i,j} S_ij F_i rho F_j†

is trace preserving. S can be unknown and need not commute with G. Every claim below is pointwise in S. Source memory across successive calls is not covered merely by this one-use channel statement. Set R=S tensor I_K/K and defect b=Tr[R(G-I)^2]. The transpose convention is fixed by using S as the actual coefficient matrix as displayed, not by silently changing vectorization.

Let alpha>=max(1,||M||). Suppose one can execute a projected unitary encoding M/alpha and its inverse, with declared finite gate/precision costs. This is a substantive supplied/constructed operation, not an oracle free of cost. For any real odd polynomial f bounded in absolute value by1 on[-1,1], the desired success contraction is

 A=f^(SV)(M/alpha)† : C^D -> C^N tensor C^K.

It is implemented as a heralded block; on failure prepare a fixed logical state and retain a distinct failure environment. On success discard the error-index register. This defines a total CPTP decoder. A classical algorithm for polynomial phase synthesis and the exact projected-encoding convention must accompany any implementation claim. The algebraic theorem first treats A as the stated contraction.

## 2. Recovery inequality without a smallest-singular-value premise

Choose a purification |s>=sum_i |i>|e_i> with <e_j|e_i>=S_ij. Apply M to the error-index/logical half of |s> tensor |Phi_K>. The resulting normalized vector purifies (id tensor E_S)(Phi_K). An ideal decoder would return |s> tensor |Phi_K>.

The squared norm of the success-vector discrepancy is Tr[R(AM-I)†(AM-I)]. The failure probability is Tr[R M†(I-A†A)M]. These formulas follow by summing i,j; in particular <i|R|j>=S_ij I/K. The sum is

 L=Tr[R(I+G-2 sqrt(G) f(sqrt(G)/alpha))].

If z is the overlap of the actual decoder Stinespring vector with the ideal vector embedded in the success environment, then L=2-2 Re z. Tracing decoder/environment registers gives F_e >= |z|^2 >= 2 Re z-1. Therefore

 1-F_e(D_f E_S) <= L.

There is no division by a small singular value, discarded success probability, or postselection normalization. A rank-deficient frame is allowed. Unknown S remains in the weighted defect but does not enter decoder implementation.

## 3. An explicit positive soft filter

For m>=0 define

 f_m(x)=x sum_{j=0}^m c_j(1-x^2)^j,
 c_j=binom(2j,j)/4^j.

It is an odd polynomial of degree2m+1. The binomial expansion of (1-y)^(-1/2) gives 0<=f_m(x)<=1 for0<=x<=1. For x>=delta>0,

 0<=1-f_m(x)<=exp(-(m+1)delta^2)/delta,

using c_j<=1 and the geometric tail. Let delta=1/(2alpha), and choose

 m+1 >= 4alpha^2 log(2alpha/epsilon),  0<epsilon<1.

Then 1-f_m(sigma/alpha)<=epsilon for every sigma>=1/2. At sigma<=1/2, positivity of f gives

 1+sigma^2-2sigma f_m(sigma/alpha)
 <=1+sigma^2 <=(20/9)(sigma^2-1)^2.

At sigma>=1/2,

 1+sigma^2-2sigma f_m(sigma/alpha)
 <=(sigma-1)^2+2alpha epsilon
 <=(4/9)(sigma^2-1)^2+2alpha epsilon.

Functional calculus and R>=0, TrR=1 therefore yield the complete one-use Bell guarantee

 1-F_e(D_f E_S) <= min(1,(20/9)b+2alpha epsilon).

This is a soft filter, not an exact discontinuous cutoff. It needs no spectral gap around1/2. Degree O(alpha^2 log(alpha/epsilon)) is deliberately conservative. Faster sign filters may improve this but are unnecessary when alpha is polynomial. All scalar coefficients are explicit rational numbers; elementary computation of them has polynomial bit complexity in m and requested precision.

## 4. What this resolves, and what it does not

A small source-weighted quadratic Gram defect already controls a physical total recovery, even if G has zero or arbitrarily small eigenvalues. Thus a universal coding argument based on a mean Gram-defect bound need not secretly assume uniform polar conditioning. Expectation over chosen code parameters may be taken afterwards because the inequality is pointwise for each actual channel S and frame.

Efficient recovery still requires polynomial normalization alpha, efficient projected-unitary access and inverse access to M/alpha, implementable input/output registers and polynomial phase compilation. A forward source channel alone does not supply these operations. General Schur reference frames can be exponentially large; the lemma alone does not resolve their computational access. Approximate block encodings and gate synthesis need a separate complete-operation error budget. The one-use Bell guarantee is not a joint retained-environment guarantee or an indefinitely reusable memory theorem.

Primary comparison/implementation target: Rizzo et al., Universal quantum coding, arXiv2609.38038v1, AppendixC reference error frame and explicit open polar-decoder efficiency discussion. This source motivates the obligation, not the algebra above. Standard singular-value polynomial transformation: Gilyen et al., arXiv1806.01838. Its exact real-polynomial implementation interface must be checked before claiming a compiled circuit here; only the abstract and primary record have yet been inspected by root.
