# Short-time exact CP averaging as an autonomous drift compiler
2026-10-30 01:10 UTC. Root working construction; independent review needed.

## Aim
Replace special coherent-clock credit by an actual finite-window service inequality. This is not yet a native memory theorem: the required full-Hilbert monotonicity and finite-window decrement must be earned for the native apparatus. The proposed mechanism addresses the noise-transfer obstacle without a global simulation estimate or a long-time effective generator.

Let L be a bounded-incidence sum of bounded-support Lindblad generators on a finite graph. Let V,W be positive animal observables, W=sum_A |A| f_A. Assume the ACTUAL full-Hilbert clean generator obeys L V<=0 and L W<=0. Suppose, on an invariant safe basin, the actual semigroup has finite-time decrement

    exp(T L)V - V <= -alpha W + b N I,

for some fixed positive T,alpha. Define the exact positive observable

    F_T = integral_0^T exp(s L)V ds.

Then exactly L F_T=exp(TL)V-V. Also F_T<=T V. No finite-time simulation approximation is used.

## Key extra monotonicity
The original per-move animal charging proof also proves monotonicity of W, not merely V: every increasing source animal A is charged to B=A union D, and |A|<=|B|. Multiplying the positive contribution by |A| and its paying negative contribution by |B| therefore retains the same slack. This works for every accepted deterministic bounded move for which the original charge holds, including augmented unary-token moves. Hamiltonians commuting with the joint occupancy algebra commute with W too. Arbitrary CP dirty resets require a separate spectral-envelope argument; do not infer this from their V bound alone.

## Exact local-noise conjugation for sufficiently SMALL fixed T
For a local HP identity-annihilating perturbation N*, write, on finite volume,

    N* exp(sL) = exp(sL) M_s,
    M_s = exp(-sL) N* exp(sL)
        = sum_{n>=0} (-s)^n/n! ad_L^n(N*).

The inverse need not be CP. Only exp(sL) on the outside must be positive.

Each nested commutator vanishes unless successive clean supports meet the accumulated support. If initial support size is at most q, clean term size at most r, local incidence at most z and clean cb norm at most J, the anchored nth coefficient is bounded by

    ||N*|| (2Jz)^n product_{j=0}^{n-1}(q+j r)/n!.

Its support has at most q+nr sites. A bounded local term changes only a bounded number k of check/flag factors per site. Thus the relative animal-orbit estimate costs at worst a factor C_theta^(q+nr), where C_theta is fixed (possibly enormous). Summing initial noise supports with bounded incidence and connected extensions adds only another exponential-in-n factor and a polynomial factor: anchor the union at a vertex of A and overcount all connected support trees and all positions of the distinguished noise support. Hence for sufficiently small positive T independent of N the series converges in the weighted local interaction norm and gives

    M_s V <= C_noise eta W,   0<=s<=T.

This connected-cluster counting step needs a fully explicit incidence proof before acceptance; no claim based on total global generator norm is allowed.

Positivity and clean W monotonicity now give

    N* exp(sL)V <= C_noise eta exp(sL)W <= C_noise eta W,
    N* F_T <= C_noise eta T W.

Therefore (L+N*)F_T <= -(alpha-C_noise eta T)W+bN.
The small service constant alpha is allowed to be extremely poor. A prescribed finite reset path has positive probability for ANY T>0, so making T small need not destroy existence of service; its actual coherent full-Hilbert proof remains essential.

## Barrier comparison without a long-time approximation
For an individual positive animal f_A, local bounded generators and finite local orbit ratios imply L f_A >= -c |A| f_A. Positivity yields exp(sL)f_A >= exp(-c s |A|) f_A. For two admissible exponents a_+>a_0, choose cT<=a_+-a_0. Then

    F_T[V_(a_+)] >= T V_(a_0).

The initial expectation is <=T V_(a_+)(vacuum)=O(N). This is compatible with choosing T very small. The basin must be defined with raw V_(a_0), and invariance/commutation must be proved for the real semigroup; it is not supplied by this abstract lemma.

## Current scope
A proposed exact short-horizon CP-average transfer, with a plausible connected-support convergence proof. The remaining native obligations are real raw V/W descent including coherent dirty resets; finite-window weighted service on the full physical Hilbert space; and basin compatibility. This note does not claim them, nor practical constants. It avoids the false shortcut that an arbitrary finite-time semigroup is a bounded-depth circuit.
