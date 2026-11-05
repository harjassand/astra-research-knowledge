# Robust local preparation of noncommuting high-temperature Gibbs states

Research construction, 5 November 2026. This is a constructive extension of
Bakshi–Liu–Moitra–Tang (BLMT), not a claim to invent high-temperature Gibbs
preparation. The published sampler is reused. The added operation replaces its
last pure-product preparation with an apparatus-compatible positive mixture.
Root owns the physical noisy-controller/acquisition interface.

Primary full text: https://arxiv.org/pdf/2403.16850 (v2, 24 February 2025).
Exact inputs used: Lemma4.17; Theorem4.18; Lemma4.19; Corollary5.18;
Lemma5.12; proof of Theorem1.7 in Section5.3. The current PDF has 50 pages.

## 1. Published stronger structure behind separability

Let H=sum_a J_a E_a on n qubits, where E_a are Pauli strings, each term has
locality at most K, and the dual interaction graph has maximum degree d.
Set D=max(1,d). Different terms need not commute. The term list, supports and
coefficients are supplied as a classical target description.

For normalized terms h_a of operator norm <=1, put beta_sep=1/(100KD).
BLMT gives an exact decomposition of exp(-beta_0 sum_a h_a) into unnormalized
configurations Sigma_v. Each configuration is a product on disjoint formal
supports of factors I+c_j X_j, where X_j is a Hermitian monomial of degree t_j
in the terms. At every completed leaf,

    |c_j| <= (beta_0/beta_sep)^{t_j}.                  (1)

The normalized Gibbs mixture has leaf probabilities proportional to the
original sampling probability times Tr(Sigma_v). BLMT Section5 constructs an
efficient sampler for these weights. Simply normalizing leaves without this
reweighting is invalid.

For Pauli terms X_j is zero or x_j P_j. Its scalar magnitude is bounded by the
product of the absolute term coefficients in its formal monomial, and its
actual Pauli weight w_j<=Kt_j. Symmetrization either preserves a scalar Pauli
or gives zero. Identity monomials may have nonempty formal support; their
normalized state is maximally mixed, while their trace factor remains included
in the published leaf weight.

The finite-accuracy sampler in Section5.3 samples leaves of a truncated sample
tree. The same invariant (1) holds leafwise. The mean normalized configuration
is close to the target Gibbs state. One can retain this classical configuration
description before the paper's last pure-product-state decomposition. Its total
monomial degree is O(n log(n/epsilon)).

## 2. Exact parity preparation inside a fixed local output range

For a nonidentity Pauli string P=P_1 tensor ... tensor P_w on its actual
support, let rho_(P,a)=(I+aP)/2^w. Suppose site i can deliver both

    tau_(i,+)=(I+r_i P_i)/2,   tau_(i,-)=(I-r_i P_i)/2,

where 0<r_i<=1. Put R_P=product_i r_i. If |a|<=R_P, sample eta in {+1,-1}
with mean a/R_P; sample w-1 independent fair signs; and set the last sign
s_w=eta product_(i<w)s_i. Prepare tensor_i tau_(i,s_i).

Every proper nonempty sign product has mean zero; the full sign product has
mean a/R_P. Expanding the tensor product proves

    E[tensor_i tau_(i,s_i)] = (I+aP)/2^w.             (2)

This identity concerns the full quantum density matrix. It is not merely a
measurement-distribution simulation. It uses w-1 fair bits, one biased bit and
local preparation, with no entangling gates. Sites outside the actual support
are I/2, obtainable by a fair mixture of opposite axis states. Independent
parity sampling on disjoint configuration factors prepares their tensor product.

## 3. Apparatus-weighted coupling theorem

Suppose each site i can deliver all six states

    (I+s r_i sigma_a)/2,   a in {X,Y,Z}, s in {+1,-1},

with r_i>0. These can be implemented by positive mixtures from a larger noisy
catalog. Acquisition, conditional independence and the real final selector are
separate physical operations which root's construction must earn.

For a Pauli string E define W(E)=product_(i in supp(E))r_i^{-1}. Then
W(PQ)<=W(P)W(Q), since Pauli multiplication cannot introduce a site absent
from both inputs and r_i<=1. Define

    J_app=max_a |J_a| W(E_a).

If J_app=0 the target is maximally mixed. Otherwise run BLMT on the same
target represented as H_0=H/J_app and beta_0=beta J_app. All normalized terms
have norm <=1. Every degree-t monomial X=xP in them satisfies

    |x| W(P)
       <= product_over_occurrences [|J_a|W(E_a)/J_app]
       <=1.                                         (3)

Combining (1)-(3), each leaf factor has physical parity bias

    |c x|/R_P <= (beta J_app/beta_sep)^t.

Consequently the explicit sufficient condition

    beta J_app <= 1/(200KD)                          (4)

makes every nontrivial parity bias at most 2^{-t}<=1/2. All leaf preparation
weights are positive, including for the finite truncated tree. In the uniform
case r_i=r and |J_a|<=J, a simpler sufficient bound is

    beta J <= r^K/(200KD).                           (5)

The weighted version accounts for weak terms touching noisier sites. At fixed
K,D,J and fixed positive radius lower bound, the temperature condition is
independent of n. It is sufficient, not an optimized practical threshold.

Theorem: under (4), there is a classical randomized algorithm producing one
local preparation prescription per site, whose independent physical execution
prepares rho_beta to arbitrary global trace accuracy. Use the published BLMT
leaf sampler unchanged, then replace only its final pure-state decomposition
by (2). Every delivered leaf has exactly its intended density matrix, so the
original mixture-approximation guarantee is preserved. No target Hamiltonian
evolution, Gibbs bath, quantum communication, target entangling gate, global
postselection or physical inverse channel is needed at this interface.

The exact infinite decomposition also proves membership in the convex hull of
these fixed-radius product states. This is a quantitative interior statement
stronger than bare separability. Efficient sampling comes from BLMT's actual
leaf sampler, not from mere convex-hull existence.

## 4. Product Pauli noise as a special case; no inverse-error amplification

Suppose the complete local output operation is a known invertible unital Pauli
channel K_i with K_i(sigma_a)=lambda_(i,a)sigma_a and
|lambda_(i,a)|>=r_i>0. Pure Pauli inputs followed by K_i produce the required
axis directions; random label flips can reduce their radius to r_i. Negative
eigenvalues are handled by reversing the label.

Equivalently, replace each sampled factor I+c xP by the factor with coefficient

    c x / product_(i in supp(P))lambda_(i,P_i),

prepare its positive Pauli parity mixture, and let actual K restore the
original factor. Equation (3) proves positivity before noise. For the exact
infinite decomposition this gives

    mu_exact=(tensor_i K_i^{-1})(rho_beta)>=0,
    Tr(mu_exact)=1,

and mu_exact is separable. This is a noncommuting many-body positive-inverse
corollary. It does not claim K_i^{-1} is a positive map on arbitrary states.

Crucial accuracy scope: the polynomial algorithm samples inverses of the
*finite-accuracy BLMT mixture*. It need not approximate mu_exact in global
trace norm. The actual forward noise restores each original leaf exactly;
therefore the delivered Gibbs error is the original BLMT error. No extensive
inverse-channel norm multiplies epsilon. The stronger exact-inverse sampling
claim is unnecessary and is not asserted here.

Even entanglement-breaking output channels are allowed. For example, the
depolarizing Bloch contraction can be any fixed 0<lambda<=1/3. The sufficient
temperature shrinks with lambda^K. This is known separable mixed-state
preparation, not preservation of arbitrary unknown quantum information, so
there is no conflict with an unknown-qubit raw-port floor.

## 5. Precision and complete local-factory error composition

Let the intended prescription distribution be p and its implemented law p_hat.
Suppose the actual delivered local state at site i differs by at most eta_i
in half trace distance from the intended state, uniformly over the finite
prescription alphabet, and the control compiler gives conditional product
execution up to channel error delta_ctrl. Then

    d(actual,rho_beta)
      <=epsilon_BLMT+TV(p,p_hat)+sum_i eta_i+delta_ctrl. (6)

Couple prescription laws, telescope products, and average. If local mixture
weights are computed from estimated factory states, compare actual and
estimated *forward positive mixtures*. Their coefficients sum to one, so
factory uncertainty enters additively; no global inverse norm is needed.

There are at most n disjoint factors. Approximate each parity coin to error
epsilon/(4n). Under (4), biases for t>=log_2(4n/epsilon) can be replaced by zero
within budget, since they are at most 2^{-t}. Small probabilities do not force
exponentially many precision bits. Remaining monomials are explicitly products
of input coefficients and finite sampling coefficients, and require polynomial
bit precision in the explicit input size, n and log(1/epsilon).

If coefficients of the target Hamiltonian are uncertain, then

    ||rho_beta(H)-rho_beta(H_hat)||_1
      <=2 beta ||H-H_hat||
      <=2 beta sum_a |J_a-J_hat_a|.                   (7)

Proof: differentiate along a linear interpolation. Each Duhamel term has trace
norm <=beta||H-H_hat|| by Schatten Holder, and normalization adds at most the
same amount. Integrate. A classical target term list is not a protocol for
learning an unknown physical Hamiltonian; any acquisition must be stated and
paid separately.

## 6. Complexity and limitations

The extra decomposition costs O(nK log(n/epsilon)) arithmetic operations to
evaluate the Pauli monomials, O(n) prescription samples, and their polynomial
precision cost. The dominant sampler is BLMT. Its Theorem1.7 states

    tilde O(n^{6+log(D)/log(beta_alg/beta_0)}
            log^3(1/epsilon) poly(K,D)),

with beta_alg=1/(gamma KD) and its fixed universal gamma. If using the explicit
beta_0<=1/(200KD) regime from its Section5.3 proof, retain the less-simplified
bound

    tilde O((100n)^{5+(4+log(D))/log(beta_CE/beta_0)}
            log^3(1/epsilon) poly(K,D)),
    beta_CE=1/(100D).

No n^7-scale polynomial is described as a practical fast algorithm. Noisy
classical computation, message transport, records, regeneration, calibration,
reset and energy must be added by the physical construction.

General K-local Hermitian terms can be expanded into at most 4^K Pauli terms
with coefficients bounded by term norm. This includes noncommuting local
Hamiltonians but inflates the degree and constants. Arbitrarily large on-site
fields are not covered at fixed beta, because they enter J_app.

BLMT already gives ideal high-temperature product preparation. The new robust
radius is derived from its stronger coefficient invariant; the same sampler
supplies it. Zhang et al.2309.01434 already supplies the inverse-state
precompensation viewpoint. This bridge supplies a uniform many-body regime and
a constructive delivered-state algorithm without an exponentially large SDP.

The strongest time comparator includes Rouze–Franca–Alhambra,
https://arxiv.org/pdf/2411.04885 (v2, February2026, PRL136060601): rapid mixing
at high temperature on Lieb–Robinson systems and nearly linear ideal quantum
preparation. This local-factory construction makes no total-resource advantage
claim against it. It exchanges coherent/entangling hardware for classical
sampling and local noisy preparation.

Bakshi–Moitra–Tan, https://arxiv.org/abs/2604.08408 (v2, October2026,
Algorithmic Aspects of the Fermi–Hubbard Model) allows arbitrary on-site energy
scales with temperature set by intersite interactions, including non-product
regimes. Our theorem does not cover that stronger field regime. Near-pure
marginals can lie outside the local preparation range, and local product
factories cannot prepare entangled targets.
