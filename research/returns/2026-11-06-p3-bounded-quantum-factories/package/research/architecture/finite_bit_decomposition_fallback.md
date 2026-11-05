# Independent finite-bit fallback for the all-family operation

5 November 2026. This is a computability and resource-closure theorem, not an
efficient substitute for the accepted Gibbs sampler. It uses the accepted
existence of a uniformly mixed bounded-interval decomposition. No exact-real,
eigenvalue, SDP or ideal-sampling oracle is required.

## Inputs and working floors

Let D=2^N and let the target rho_N be the Gibbs state of the supplied finite
one-dimensional Hamiltonian. The local terms, inverse temperature, and a
strict positive lower bound on the accepted mixed-block floor are supplied
as rational data or computable numbers with certified error bounds. If the
Hamiltonian is inferred physically, its acquisition accuracy and cost are
additional paid inputs; no arbitrary real is made computable by this theorem.

The accepted representation is a probability mixture of tensor products over
interval partitions with block size at most B, and each block tau satisfies
tau >= eta_0 I/d. B and a rational 0<eta<eta_0/4 are fixed independently of
N and epsilon. Use the working floor 2 eta for finite approximants, leaving
constant slack for the later accepted product-channel inverse. Changing this
constant floor only changes fixed factory parameters.

Define the real-entry norm

    C(A) = sum_ij ( |Re A_ij| + |Im A_ij| ).

It obeys ||A||_1 <= C(A) <= sqrt(2) D ||A||_1, and we use the conservative
upper bound 2D||A||_1. The first inequality follows by decomposing A into
matrix units; the second follows from Cauchy-Schwarz and ||A||F<=||A||1.

## A finite rational net of positive block states

For each d<=2^B enumerate Hermitian matrices with rational real/imaginary
entries on a grid of denominator Q, trace exactly one, bounded entries, and
sigma >= 2 eta I/d. Positive semidefiniteness of a rational Hermitian matrix
is decidable by exact rational algebra (for example all principal minors),
so this produces an explicit finite list of valid density matrices.

Round the independent entries of any accepted block tau to the grid and
correct one diagonal entry to restore trace one. The entry and trace-norm
perturbations are bounded by a dimension-dependent constant times 1/Q.
Choose Q large enough that the trace-norm perturbation is at most

    delta_leaf = epsilon/(128 N D)

and its operator-norm perturbation is smaller than the fixed eigenvalue
slack. Then every accepted block is within delta_leaf of a retained net point.
The grid net has size at most

    S <= (C_B N D/epsilon)^{C_B 4^B},

with an explicit fixed constant obtainable from the chosen grid. The exact
exponent is immaterial for computability but must not be called near-linear.

## Enumerate the product vertices

Enumerate every interval partition with block lengths at most B and every
assignment of the appropriate rational net point to each block. Form the
corresponding tensor-product matrix V_j. All V_j are exact rational density
matrices. The number M of vertices is bounded conservatively by

    M <= 2^N S^N
      <= 2^N (C_B N D/epsilon)^{C_B N 4^B}.

Map each block in the accepted mixture to one nearest net point. Tensor
telescoping gives a global trace error at most N delta_leaf for every product
term. After averaging, a state rho_net in conv{V_j} therefore satisfies

    ||rho_net-rho_N||_1 <= N delta_leaf,
    C(rho_net-rho_N) <= 2DN delta_leaf <= epsilon/64.

This is only an existence argument for feasibility. The algorithm below
does not need to know the accepted mixture's real-valued weights or to draw
from its ideal source.

## Dense target computation with certified finite bits

Compute a rational Hermitian trace-one approximation rho_hat with
C(rho_hat-rho_N)<=epsilon/64. One elementary route constructs the dense H,
uses a rational Taylor or scaling-and-squaring exponential, and normalizes
its trace. A computable bound M_H>=beta||H|| supplies both the Taylor
remainder bound and the lower bound Z>=D exp(-M_H) needed to control
normalization. Rational upper/lower bounds on the exponential suffice. The
required absolute errors can be exponentially small; their precision is
finite and computable. The number of arithmetic operations and memory can
be exponential or larger in N. No quantum coherent data are alive during
this calculation.

For ordinary fixed finite-range bounded couplings, M_H=O(N). Exponentially
small entry errors therefore require only polynomially many precision bits,
although there are D^2 exponentially many entries. This observation does not
remove the enormous cost of the vertex enumeration.

## Rational LP replaces the unknown mixture

Solve the finite rational linear program

    minimize C( sum_j w_j V_j - rho_hat )
    subject to w_j>=0, sum_j w_j=1.

Linearize the absolute values of real and imaginary matrix entries using
nonnegative slack variables. All coefficients are rational. Ordinary finite
bit linear programming therefore applies; no semidefinite optimization
oracle is used. Feasibility above shows the optimum is at most epsilon/32.
An exact rational optimum or any certified feasible solution with objective
at most epsilon/16 gives

    || sum_j w_j V_j-rho_N ||_1
      <= C(sum_j w_j V_j-rho_hat)+C(rho_hat-rho_N)
      <= 5 epsilon/64.

The slack permits ordinary certified approximate LP algorithms as well.

Sample the resulting rational probability vector by a finite classical
procedure. For example use a common denominator, draw a uniform integer
by rejection from a binary interval, and cap the number of repetitions.
Each attempt accepts with probability at least one half, so capping at t
attempts costs at most 2^{-t} in total variation. All bits, comparisons and
fallbacks are protected classical computation, charged at their real size.

## Why this does not enlarge the quantum factory

The rational block-state grid refines as epsilon decreases. The quantum
channel library does not. Each selected rational block state retains the
same fixed positive floor; after the accepted local precompensation it stays
inside the same compact set of full-rank replacement channels. The fixed
complete-map palette realizes that whole set by changing classical mixture
weights. Those weights and acquired physical maps are computed to the
requested classical precision. Coherent workspace, native circuit length,
round count and data lifetime depend on B, eta and the chosen fixed noise
threshold, not N or epsilon.

Calibration error, noisy classical computation, word history-erasure error,
palette-weight approximation and finite-time sampling failure receive their
own additive budgets. The proof above deliberately spends less than epsilon
on the classical target source so the final trace-distance budget can include
all of them. A trace-norm bound also implies the corresponding trace-distance
bound with the usual factor one half.

## Cost and scope

At fixed B, the bound on M is roughly exponential in N^2+N log(1/epsilon),
before linear-program and protected-classical overhead. This is an explicit
finite-bit fallback, not an efficient physical preparation recommendation.
Its contribution is narrower: even if the inherited efficient sampler's
numerical oracle convention is not strengthened, the new bounded-coherence
operation still has an ordinary computable classical implementation. The
inherited efficient-source theorem and this much more expensive finite-bit
closure must be reported separately.
