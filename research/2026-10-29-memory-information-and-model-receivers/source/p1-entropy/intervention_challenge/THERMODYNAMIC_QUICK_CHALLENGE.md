# Quick complementary check of the root's thermodynamic opening

29 October2026. Scope: a short ordinary derivation prompted by the root's
candidate theorem. This is not an independent review of a completed root
manuscript or an external novelty determination.

## Normalization and witness scaling

For stationary finite row generator Q with positive pi, geometric edge flows
g_xy=sqrt(pi_x Q_xy pi_y Q_yx) define Q_geo,xy=g_xy/pi_x off diagonal and
Q_geo,xx=Q_xx. Stationary balance and Cauchy–Schwarz give sum_y g_xy<=pi_x q_x,
so this is a legitimate reversibly killed generator. Its path measure is the
geometric mean of stationary forward and reversed path measures. The AM–GM
deficit is entrywise nonnegative at any endpoints.

For nonnegative label functions f_a, the scalar sum of deficits equals
1 minus path Hellinger affinity only if sum_a f_a(x)=1. A subpartition gives
an inequality in the useful direction. For unrestricted nonnegative labels,
include the factor M² with M=sup_x sum_a f_a(x). Raw unnormalized labels do
not satisfy the normalized entropy-rate bound without this factor.

For copositive witness H and gamma=-<H,C_sym>>0, write C_sym=C_geo+D with
D entrywise nonnegative and C_geo completely positive. Then

    gamma <= h_- sum_ab D_ab,
    h_-=max(0,-min_ab H_ab).

This can sharpen h=max_ab |H_ab|. Under normalized labels and the stationary
all-even time-reversal convention, D_1/2=-2log(affinity)<=KL=σt gives

    σt >= -2log(1-gamma/h_-).

The geometric propagator's midpoint factorization is completely positive:
in sqrt(pi) coordinates its generator is symmetric and Metzler; hence its
half-time exponential and the transformed label matrix are entrywise
nonnegative. Complete positivity refers to uncentered two-time joints.

## Constructive converse in closure

Fix t>0. Let C be any completely positive symmetric matrix with total entry
sum one. Take a supplied factorization C=sum_k v_k v_k^T, v_k>=0. Delete zero
terms. Set s_k=1^T v_k, w_k=s_k², r_k=v_k/s_k, p=C1. Then sum_k w_k=1 and
C=sum_k w_k r_k r_k^T.

Make hidden states (k,a) for each positive r_ka, with stationary probability
mu_ka=w_k r_ka and deterministic observed label a. Within each fixed k,
refresh the label from r_k at rate R. Additionally refresh the whole hidden
state from mu at rate epsilon. Both generators satisfy detailed balance.
They commute because the within-mode generator annihilates1 and preserves
mu. The global refresh makes the finite chain irreducible for epsilon>0.

Direct exponentiation gives the observed lag joint exactly:

    C_(R,epsilon)
      =exp(-epsilon*t) [exp(-R*t) diag(p)+(1-exp(-R*t)) C]
        +(1-exp(-epsilon*t)) p p^T.

Therefore

    TV(C_(R,epsilon),C) <= exp(-R*t)+epsilon*t.

Each state-changing departure rate is <=R+epsilon. Choosing finite large R
and finite small positive epsilon approximates C at any positive tolerance.
Thus the closure of equilibrium even-state finite hidden-Markov two-time
joint matrices with normalized deterministic labels is exactly the normalized
completely positive cone. Necessity is the root's midpoint argument.

This converse assumes the CP factorization is supplied. It does not make
finding the factorization cheap, give exact finite-clock realization of every
boundary point, or establish historical novelty. Conditional iid latent
mixtures, reflection positivity and CP factorization are classical nearby
ideas. The proposed thermodynamic separation and resource guarantee require
their own scoped collision check.

## Non-CP PSD target for a constructive test

On five visible labels, C=(aI+Adj(C5))/(5(a+2)) is a normalized symmetric,
entrywise nonnegative PSD matrix for a>=2cos(pi/5), and the classical Horn
copositive witness detects it for a<2. A possible hidden kinetic realization
is a mixture of nearly static positions and a precise one-step clock around
the five-cycle, with equally weighted hidden directions. Time reversal swaps
the directions, giving reversible observed paths even though the hidden
all-even model dissipates. Finite phase clocks approximate the one-step law;
slow reversible mode changes make irreducible. This paragraph proposes a
construction to the root; it is not an executed generator certificate here.
An odd-direction physical time-reversal convention is a different hypothesis.
