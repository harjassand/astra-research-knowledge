# Quadratic pair kernels force quadratic matrix-design leverage

28 October 2026. Author mechanism boundary, independent receiving pending. This is NOT an operational learning lower bound. Its physical source deliberately has trivial optimal policy risk, making explicit why a task quotient is necessary rather than promoting uniform matrix confidence to a mission requirement.

## 1. A fixed four-coordinate physical source

For any k>=4 let w_i=(1,i,i²,i³)^T, i=1,...,k, let S=sum_i w_i w_i^T, and v_i=S^(-1/2)w_i. Then

    sum_i v_i v_i^T=I_4,

and any four v_i are independent. Put p_i(x)=|v_i^T x|² for real x in S³. The physical encoder is V_x|psi>=|x> tensor |psi> on an eight-dimensional source input. This is also realizable as a quaternion family: use real left-quaternion multiplication on the four-dimensional selector, tensor the logical identity, and take the first selector basis state as the anchor.

The source measures the selector POVM {v_i v_i^T}, discards the logical input, and prepares an orthogonal output flag |i>. It is a single CPTP source, not a different channel supplied at each x. Its encoded output is

    E_x(rho)=rho_x Tr rho, rho_x=sum_i p_i(x)|i><i|.

The actual ordinary loss density is T_x=rho_x tensor I_2/2. It is a positive matrix-valued quadratic with the required reference marginal and rank at most2k. Take the admitted confidence envelopes

    U_x=T_x+eta I_(2k).

These obey eta I<=U_x and U_x<=3T_x+32eta I. Thus no arbitrary nonphysical covariance family is being slipped into the design example.

## 2. The precise matrix-design objective

Use an orthonormal real basis for symmetric4 by4 matrices and a(x)=vec_sym(xx^T), so ||a(x)||=1. On Hermitian output matrices let

    K(U)(H)=(UH+HU)/2,
    V_pi=E_{z~pi} [a(z)a(z)^T tensor K(U_z)^(-1)].

This is the actual SLD block design of the received matrix-GLS route, for ANY probability distribution pi on the whole encoder sphere. Its uniform operator leverage constant is the least L such that

    F_x* V_pi^(-1) F_x <= L K(U_x)                     (1)

for every x, with F_x=a(x) tensor I. If a required feature lies outside the design range, take L=infinity; otherwise inverses may be read on the acquired span. The question here is whether the constant input dimension alone lets one replace the generic O(k²) trace-leverage bound by O(k) or O(1).

## 3. Every pair has its own rare coherence direction

For each i<j choose a real unit x_ij orthogonal to v_i,v_j. Such a vector exists because their span has dimension two. Let H_ij be the Hilbert-Schmidt unit Hermitian coherence between |i> tensor |0> and |j> tensor |0>. Since U_z is diagonal, these different output-operator directions are invariant and mutually orthogonal sectors of V_pi. In that sector the inverse-variance weight is

    b_ij(z)=4/[p_i(z)+p_j(z)+4eta].

At x_ij, b_ij=1/eta and K(U_xij) acts by eta. Put f_ij(z)=eta b_ij(z), so0<f_ij<=1. Cauchy for the positive sector design gives

    L >= (1/eta) a(x_ij)^T
           [E b_ij(z)a(z)a(z)^T]^(-1) a(x_ij)
      >=1/[E f_ij(z)|a(z)^T a(x_ij)|²]
      >=1/E f_ij(z).                                  (2)

This bound is uniform over designs whose weights depend on eta. It is not an asymptotic argument with a fixed prior allocation.

## 4. At most three rare outputs can be covered simultaneously

Define the known positive frame constant

    c=min_{I subset[k], |I|=4} lambda_min(sum_{i in I}v_i v_i^T)>0.

At every x, at most three p_i(x) can be strictly below c/4. Otherwise four of them would sum to less than c, contradicting the definition. Among P=binom(k,2) pairs, at most three pairs have BOTH entries below c/4. Every remaining pair satisfies f_ij(z)<=16eta/c. Consequently, pointwise in z and hence for every pi,

    sum_{i<j} E f_ij(z) <=3+16P eta/c.                  (3)

Summing the necessary inequalities E f_ij>=1/L from(2) proves

    L >= P/[3+16P eta/c].                              (4)

In particular eta<=c/(16P) forces L>=P/4=Omega(k²). This is the same quadratic order as the generic block trace bound. The four real encoder coordinates do NOT reduce it by themselves.

The small c is not concealing a noncomputable or uncontrolled source gap. Every four-row Vandermonde determinant is a nonzero integer, while det S<=(Tr S/4)^4<=k^28. The corresponding four-frame Gram determinant is at least k^(-28). Its eigenvalues are at most1 because it is a subset of a Parseval frame, so its smallest eigenvalue is at least its determinant. Thus one can use the explicit conservative c>=k^(-28). The displayed obstruction appears at a polynomially small regularization scale, not only an unspecified limiting instance.

## 5. Fixed-grid version and exact operational limitation

A fixed encoder net with Euclidean covering radius h<=sqrt(eta) also sees the obstruction up to a numerical constant. A point within h of x_ij has p_i+p_j<=2h², because ||v_i||<=1. Its inverse-variance weight is at least2/(3eta). Repeating(2) multiplies the lower bound in(4) by2/3. This addresses the actual finite-grid design interface, rather than requiring the algorithm to query an exact unknown real root.

The source is logically useless: for EVERY x and every CPTP decoder, the logical channel is a replacement channel. Its entanglement fidelity is1/4 and its optimal Bell loss is3/4. All policies are task-equivalent. A conventional learner can attain the optimum with a fixed replacement output and no training. This note therefore does not lower-bound active ordinary task acquisition, total rank-weighted source cost, or access with coherent references.

What it DOES rule out is improving the existing ALL-ENCODER, ALL-HERMITIAN SLD matrix-confidence design merely by replacing its trace leverage D=Theta(k²) with a dimension-free or linear-k operator bound based on the four-dimensional encoder selector. Its many rare pair-coherence directions are operationally irrelevant in this example. A better generic task learner must avoid paying for them, rather than infer a source lower bound from this uniform-confidence obstruction.

## 6. Positive-model distinction: the ambient directions are not independent sources

At a pair-null encoder, positivity itself forces the corresponding true coherence to vanish: for every PSD matrix T, |T_ij|²<=T_ii T_jj. The example has both diagonal entries zero. Thus the full Hermitian coefficient-confidence space used by(1) treats certain ambient directions as independently uncertain even when an acquired positive polynomial model could constrain them from its diagonal information. This is not a lower bound on confidence methods that retain that coupling. More sharply, if a scalar positive matrix polynomial has known diagonal entries l_i(x)² with independent real linear forms l_i, then each quadratic off-diagonal entry must vanish on both hyperplanes l_i=0 and l_j=0; polynomial divisibility forces T_ij(x)=c_ij l_i(x)l_j(x). Such a structural quotient removes the apparent independent pair directions. Its acquisition and error stability for a general unknown source are NOT proved by this exact observation. The earlier positive-completion/Bures-transfer counterexamples remain in force: an arbitrary fitted PSD completion is not thereby acquired in a task-sufficient metric.
