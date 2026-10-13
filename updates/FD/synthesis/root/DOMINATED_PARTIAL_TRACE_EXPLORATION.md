# A partial-trace remainder for local reset echoes

Internal derivation, 14 October 2026. Correctness and novelty require review.

Disposition after adversarial review: valid-looking but unnecessary for the
operator-norm certificate. The critic's extremal-eigenvector argument obtains
the stronger bound p_tau >= t^2(1-Lambda*t/2)^2 ||R||^2/(4d) directly under the
original source assumptions. The product-budget construction below is retained
as explored mathematics, not the preferred proof or a required new hypothesis.

The CRAY source uses an operator-norm Taylor remainder and then compares it with
a reset-weighted Hilbert--Schmidt signal. This introduces an avoidable second
factor of collar dimension when the boundary interaction has a controlled
product decomposition. The strengthened contract is explicit below.

Let S have finite dimension d and E finite but arbitrarily large. Write
H=H_S tensor I + I tensor H_E + V, with a supplied decomposition
V=sum_l A_l tensor B_l and kappa=sum_l ||A_l|| ||B_l||. Scalars may be removed
from H_S because they commute with the residual. Let R=R_S tensor I be Hermitian,
||R||<=Rcap, J>=||H_S||, and Lambda=2J+2kappa+Rcap. No bound on ||H_E|| enters.
Define E(t)=exp(iHt)exp(-i(H+R)t) and sigma=(Tr R_S^2/d)^(1/2).

For O on S tensor E put

    N(O)=||Tr_S(O^dagger O)/d||^(1/2)
        =sup_tau ||O (I/d tensor tau)^(1/2)||_HS.

This is a norm. Left multiplication by a unitary preserves N. Right
multiplication by a product unitary preserves N; right multiplication by
A tensor B increases it by at most ||A||||B||. The last claim follows by
partial-trace cyclicity in S, AA^dagger<=||A||^2 I, and positivity, or by
expanding the scalar trace against any tau. Consequently right multiplication
by V has norm at most kappa on this normed operator space.

Separate H+R into its product-local Hamiltonian H_S+R_S and H_E, and use the
Dyson series in the interaction picture. The interaction has at every time the
same product-norm bound kappa. The series and the triangle inequality give

    N(O exp(-i(H+R)t)) <= exp(kappa |t|) N(O).

This bound applies to arbitrary O. The extensive host Hamiltonian is absorbed
by the product-local unitary, whose right multiplication is isometric. This
argument uses finite dimension; extending it to unbounded hosts requires its own
domain and convergence argument.

The echo second derivative is

    E''(s)=exp(iHs) ([H,R]-R^2) exp(-i(H+R)s).

Since R is local, the elementary product bound implies

    N([H,R]-R^2) <= (2J+2kappa+Rcap) sigma = Lambda sigma.

Twice integrating gives, with

    f_kappa(t)=integral_0^t (t-s) exp(kappa s) ds
             =(exp(kappa t)-1-kappa t)/kappa^2  (kappa>0),
    f_0(t)=t^2/2,

the relative partial-trace remainder

    N(E(t)-I+itR) <= Lambda f_kappa(t) sigma.

For EVERY outside density tau, local reset yields

    p_tau(t) = ||(E(t)-I)(I/d tensor tau)^(1/2)||_HS^2/4
             >= (t-Lambda f_kappa(t))^2 sigma^2/4
             >= (t-Lambda f_kappa(t))^2 ||R||^2/(4d),

whenever t>Lambda f_kappa(t). This is an outside-state-uniform lower bound,
so the source's conditional-history binomial domination applies unchanged.
For a probability calibration allowance gamma and any valid upper confidence
bound q_up on the uniform failure floor, one obtains

    ||R|| <= 2 sqrt(d (q_up+gamma))/(t-Lambda f_kappa(t)).

In particular kappa<=Lambda/2. At t=1/(2Lambda), kappa t<=1/4 and
f_kappa(t)<=exp(1/4)t^2/2. Using exp(1/4)<4/3 gives
Lambda f_kappa(t)<t/3, so t-Lambda f_kappa(t)>2t/3=1/(3Lambda). Thus

    p_tau >= ||R||^2/(36 Lambda^2 d),
    ||R|| <= 6 Lambda sqrt(d(q_up+gamma)).

The constants are conservative. The leading dimension factor improves from
d^2 to d for the SAME reset/readout sequence, conditional on the stronger
product-interaction budget. Zero-failure sufficient shot counts now scale as
36 Lambda^2 d epsilon^-2 log(1/alpha). The calibration floor in this sufficient
certificate is 6 Lambda sqrt(d gamma). Neither is promised to be attained by
an arbitrary residual, and actual nonzero failures remain decisive.

The factor d is unavoidable for this maximally mixed null-test interface even
with no environment: H=0, R=epsilon |0><0| gives
p=(1-cos(epsilon t))/(2d). Resolving that signal costs order d at fixed
epsilon t, while demanding operator norm control covers the exceptional state.
This does not lower-bound protocols that target other preparations, use phase
information, or exploit additional structure.

The stronger budget must be obtained from the physical interaction model or a
separate calibration. An arbitrary norm bound ||V|| cannot simply be substituted
for kappa: a SWAP interaction can transfer a pure outside state into S and
amplify reset-weighted right multiplication by sqrt(d). Few-body Pauli-product
models provide an explicit budget by summing absolute coefficients, but that
sum can be larger than the source's original operator-norm budget.

Free-energy implications, controlled-branch/local-reset implementation,
support/tail errors, sector factorization and source/model calibration remain
exactly separate obligations. This theorem is a mathematical improvement to
one scoped certificate; it establishes no physical device, generic local
comparison witness, laboratory calibration or matched-method advantage.
