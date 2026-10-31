# Imperfect observations: stabilize replay, do not pretend to know an invariant law

Author construction, 31 October 2026. Not independently reviewed. This extends
the frozen exact frontend without changing it. It is a finite, checkable
construction, not a claim to invent stable model reduction or to outperform
equally informed retained Krylov/range/operator-inference methods.

## 1. The observation and future-task interfaces

There are m unknown n-by-n **row-stochastic** kernels A_a. Nonnegativity and
unit row sums are a model-class promise, not inferred from finitely many
samples. No common equilibrium, reversibility, low rank, useful basis,
contraction gap, or good probing directions are promised. Given rational
observable b and rational initial linear functional ell, future tasks request

    f(w) = ell^T A_(a_l) ... A_(a_1) b,   l <= L.

The task does not depend on an unknown stationary distribution. Every query
may be chosen adaptively after all earlier returned answers. This concerns
the **same realized word**, not stability of two feedback policies that pick
different words after different outputs.

The initial frontend accepts rational entry intervals [lower,upper] containing
every A_a[i,j]. It checks that each row's box meets the probability simplex.
These are genuine set-valued observations, not exact access to a hidden
rational matrix. A deterministic enclosure oracle must supply a valid error
contract and its acquisition cost; knowing that a simulator merely returned
p digits does not establish that contract. The executable simulates this
interface by outward rounding, and the learner never receives the truth.

An alternative statistical interface draws independent next-state samples
from any requested (a,i) row. At round k, take a scheduled cumulative N_k
samples per row. For entry halfwidth rho_k, Hoeffding and a union bound give
simultaneous coverage at that round if

    N_k >= log(2*m*n^2/delta_k)/(2*rho_k^2).

Use delta_k=delta/2^(k+1), k>=0. With probability >=1-delta, EVERY round's
boxes contain the truth, even when the choice of representation and stopping
round depends on all observations. Samples can be retained when N increases.
All mn rows, mn*N_final transitions, mn^2 counts/interval entries, and failed
rounds are paid. This elementary frontend is deliberately conservative; it
does not claim sample optimality. More efficient confidence sets may be used
only with their own valid simultaneous coverage proof. Geometry fitted on
the same observations is allowed because the coverage event is uniform over
the whole matrix, not a fresh-probe estimate evaluated as if independent.

## 2. What is actually acquired and certified

Choose a positive rational probability vector h from the observations;
H=diag(h). It need not be stationary for any true A_a. The executable tries
the stationary vector of the average of feasible center kernels, rounded to
a positive rational distribution, and the uniform distribution. Each is a
proposal, never an asserted property of the hidden kernels. Failed geometry
and basis candidates remain in the ledger.

Acquire any rational full-rank V whose range contains b and c=H^-1 ell.
Including 1 is useful for a gap certificate below. Let

    G=V^T H V, P=V G^-1 V^T H, Q=I-P, b=Vu, ell^T V=h_out^T.

The positive-definite Gram matrix is checked. Rational orthogonalization and
power-of-two column scaling may give I <= G < 4I; actual bit lengths and all
arithmetic still count. There is no free well-conditioned basis assumption.

Store rational small matrices B_a satisfying the *checked* inequalities

    B_a^T G B_a <= G.

They need not be the exact Galerkin blocks. One constructive way is to round
an observed Galerkin block M_a to bounded-precision entries, find a rational
s_a>=max(1,||M_a||_G) by exact PSD checks and dyadic bisection, and set
B_a=M_a/s_a. Both coefficient rounding and this stabilization bias are paid.
This always produces a stable small recurrence; it does NOT guarantee useful
accuracy. All stronger ordinary methods can use the same operation.

For every kernel family in the observation set, verify finite bounds

    ||Q A_a P||_H <= e_in,  ||P A_a Q||_H <= e_out,
    ||Q A_a Q||_H <= alpha,
    ||P A_a P - V B_a G^-1 V^T H||_H <= d.

Only the final term is restricted to range(P); both operators vanish on Q.
The letter d denotes the paid reduced-model discrepancy, NOT a minorization.
Section 4 gives directly computable sufficient bounds. No optimal norm or
worst-word planner is used.

## 3. Mixed-norm uniform replay theorem

Put M=||b||_infinity and C=||H^-1 ell||_H. Define t_0=0 and

    t_(j+1)=min(1, alpha*t_j+e_in),
    E_l = C*M*(l*d + e_out*sum_(j=0)^(l-1) t_j).

For every family in the observation set and EVERY word of length l,

    |ell^T A_w b - h_out^T B_w u| <= E_l.

In particular, when alpha<=1,

    E_l <= C*M*(l*d + e_in*e_out*S_l(alpha)),
    S_l(alpha)=sum_(j=0)^(l-2) (l-1-j)*alpha^j.

For every alpha>=0 the capped bound satisfies E_l<=C*M*l*(d+e_out).
There is no exponential factor from an approximately invariant geometry.

**Proof.** The true full trajectory x_j satisfies ||x_j||_infinity<=M because
every true A_a is stochastic. As sum h_i=1, ||x_j||_H<=M. H-orthogonal P,Q
give ||p_j||_H,||q_j||_H<=M. Starting with q_0=0, its exact block recurrence
gives ||q_(j+1)||_H<=alpha||q_j||_H+e_in M, and the global bound permits the
cap at M. Lift the reduced trajectory z_j=V B_(a_j)...B_(a_1)u. The difference
p_(j+1)-z_(j+1) equals the stable reduced block applied to p_j-z_j, plus the
P-block model discrepancy applied to p_j, plus P A_(a_(j+1)) Q q_j. Thus its
norm is at most its previous norm + d M + e_out M t_j. Sum, and pair with
c in range(P); ell^T q_j=0. The uncapped geometric recurrence gives the
second display. QED.

This is the constructive distinction: full-system boundedness is obtained
from the stochastic model class in infinity norm; the learned geometry is
used for task-sensitive two-sided cancellation, while stability is enforced
and certified on the *small replay representation*. Exact common stationarity
is unnecessary. Poor geometry, large uncertainty or destructive stabilization
can still make the error bound useless, and that is reported, not hidden.

On the simultaneous confidence event, this one certificate covers arbitrarily
many later adaptive word queries of length <=L. There is no extra confidence
union penalty for how many queries are asked. It does not extend to longer
horizons, new b/ell not admitted to the representation, drifting kernels, or
a state-dependent switching policy interpreted as a new nonlinear operator.

## 4. Explicit enclosure calculations, including uncertain geometry

Choose any feasible rational center C_a in each row box. Let
R_a[i,j]=max(C_a[i,j]-lower_a[i,j],upper_a[i,j]-C_a[i,j]). Then

    eta^2 = max_a sum_(i,j) h_i*R_a[i,j]^2/h_j

bounds ||A_a-C_a||_H^2 by the weighted Frobenius norm. All h_j are explicit
positive rationals. Orthogonal projection cannot increase that norm. Exact
center residual norms, plus eta, therefore bound both leakage directions;
the norm of its reduced-block discrepancy, plus eta, bounds d. Rational
square-root upper enclosures are used, not unverified floating estimates.
This full-entry uncertainty bound may be very conservative for small h_min.
It is a sufficient frontend, not a claim that its rare-state dependence is
necessary for every scalar task.

A complement bound does not require exact stationarity. If 1 is in range(V),
let

    minor = min_(a,i,j) lower_a[i,j]/h_j,
    kappa = max_(a,j) sum_i h_i*upper_a[i,j]/h_j.

Clip minor at zero and one, and require kappa>=minor. For minor<1, write any
true A=minor*1*h^T+(1-minor)R. R is row-stochastic. Jensen gives
||R||_H^2 <= (kappa-minor)/(1-minor). Since Q annihilates 1 and h^T Q=0,

    ||Q A Q||_H^2 <= (1-minor)*(kappa-minor).

At minor=1 every consistent A=1*h^T and the complement vanishes. This is a
robust *acquired* geometric certificate, not a presupposed invariant norm.
One can take the minimum with an independently checked bound on Q C_a Q plus
eta. When no gap is certified, the capped theorem remains sound.

## 5. Bounded-bit execution is part of the model

### A stronger observation transport, before entering the learned geometry

There is no reason to force all observation uncertainty through a possibly
ill-conditioned learned H. For the feasible stochastic centers C_a, set

    eta_inf = max_(a,i) sum_j R_a[i,j].

Contractive telescoping in infinity norm gives, uniformly over every word,

    |ell^T A_w b - ell^T C_w b| <= ||ell||_1 ||b||_infinity l*eta_inf.

Apply the mixed-norm theorem to the EXACT OBSERVED CENTERS, with eta=0, and
add this external observation term. The centers are known finite data, not
assumed true operators. Their stable small replay and geometry remain
acquired and certified, even if the centers have no common stationary law.
One may take the minimum of this transported bound and the direct robust
weighted bound from Section 4. This often avoids an artificial h_min penalty
or norm inflation in acquisition: all true kernels share the original
infinity-norm stability, while task compression uses a learned Hilbert
geometry only for the observed center family. The ordinary full-space
comparator receives exactly the same favorable observation term.

This modular route is the default executable certificate. It does not remove
the unavoidable observation error, and requires all centers to be genuinely
stochastic. It also does not infer true common stationarity from noisy data.

The online operator is the stored, certified B_a, not an ideal unrounded
projection. Initialize with rounded coordinates u_tilde and, after each exact
rational small matrix-vector product, round coordinates to the nearest grid
2^-p (a specified tie rule). If each coordinate error is <=2^(-p-1), its
G-norm is at most

    r_step = sqrt(lambda_max(G)*r)*2^(-p-1).

Certified contraction implies total state error <=r_init+l*r_step. Evaluate
h_out^T z exactly with the stored output vector, then round the scalar with
absolute error <=2^(-p-1). The total admitted error is

    E_l + C*(r_init+l*r_step) + 2^(-p-1).

The executable checks a rational upper bound on this entire sum against the
externally requested tolerance. Matrix coefficients have bounded stored bit
length, and each query state has at most p fractional bits. Its integer part
is bounded using lambda_min(G) and ||u||_G+L*r_step, so denominators do not
grow with each word as they did in the exact-rational fixture. Every multiply,
round, read and output still costs bits. Acquire and store ONE common integer
denominator per B_a and the corresponding integer numerators; B denotes the
largest bit length in this common-denominator encoding, not the largest
individual rational entry. In the stated construction this denominator is
explicitly available from the dyadic M_a and its single rational scale s_a.
For a general supplied rational B, the lcm acquisition and possibly r^2-fold
denominator-bit growth must instead be paid. With query-state bit budget T,
schoolbook replay costs O(L*r^2*(B+T+log(r))^2), including conservative
division/rounding costs. The output vector is likewise converted to a paid
common denominator, with its own bit budget and one final dot product. Offline
basis/metric/certificate arithmetic may still have much larger bit lengths.
Those are measured separately; a small rank is not a full complexity ledger.

## 6. Precision cannot simply disappear into acquired knowledge

Take a two-state absorbing kernel A_p=[[1-p,p],[0,1]], initial row ell=e_1,
and b=e_1. The length-L value is (1-p)^L. For 0<eps<=1/8, choose
p=4eps/L. The values for p=0 and this p differ by at least
Lp-binomial(L,2)p^2 >=4eps-8eps^2 >=3eps >2eps.
Entry observations with a common halfwidth >=2eps/L can enclose BOTH models.
No algorithm, regardless of retained learning, can output an eps-accurate
answer for that word uniformly over the same data. This is an information
obstruction at fixed observation precision, not a computational-hardness
claim. It explains why a paid term linear in L times model uncertainty cannot
be removed in general. Additional structure or a shorter task is needed.

For iid row samples, even a one-step Bernoulli response costs order eps^-2
samples at fixed confidence. Near p=1/L, distinguishing p from p+Theta(eps/L)
also costs order L/eps^2 by the Bernoulli KL testing bound. The elementary
full-entry Hoeffding frontend can be much worse, and is not called optimal.

## 7. Acquisition policy, failure, and strong comparators

At scheduled observation precisions, retain/refine boxes; propose geometries;
start from 1,b,H^-1 ell; add largest center forward/adjoint residuals using
ordinary retained bidirectional Krylov. Recheck robust bounds after each
expansion. Rank cannot exceed n. All failed candidates, all source-entry
precision returned, orthogonalization, PSD tests, coefficient rounding and
exact verification are charged. Refinement can terminate with an admitted
small recurrence, full-space representation, or INCONCLUSIVE at the allowed
precision budget. The latter is not proof of absent useful structure.

The equally informed comparisons are ordinary retaining Krylov, randomized
range/Nystrom, spectral/balanced reduction and stable operator inference with
these SAME enclosures/certificate/stabilizer, and full-space on-demand
evaluation with retained boxes, prefix states and the same bounded-bit
execution. Only measured acquisition-plus-execution savings can justify
amortization. Full-entry observation can dominate all subsequent savings.

## Prior work and claim boundary

Stable projection is established: Bond--Daniel, 2008,
https://www.mit.edu/~dluca/publications/2008-iccad-Bond-StableProjectionLinearMOR.pdf
and Pulch, https://arxiv.org/abs/1711.02912 . Nonintrusive operator inference
and structure-preserving stable learned models are established:
https://doi.org/10.1016/j.cma.2016.03.025 and
https://doi.org/10.1016/j.cma.2022.115836 . Data-driven common-Lyapunov and
uncertainty-set analysis are also established:
https://arxiv.org/abs/2105.00112 and
https://www.math.rug.nl/~trentelman/psfiles/beyond.pdf .

The present result is the explicit mixed-norm, uncertainty-set, finite-replay
certificate above and its acquisition ledger. A historically new major
capability or a strong-baseline advantage has NOT been established. The
scientific question now has a sound imperfect-observation interface rather
than silently replacing an unknown system by an exact fitted matrix.
