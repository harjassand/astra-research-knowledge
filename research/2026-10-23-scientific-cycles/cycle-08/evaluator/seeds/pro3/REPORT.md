# Cycle7 PRO3 result: reciprocal flow, not proposal symmetry

The complete critical robustness law now holds for arbitrary fixed
target-independent row-stochastic proposals with reciprocal support. Q may
be asymmetric and nonreversible and may have unbounded degree and counting
columns across the admitted finite instances. The screen must use the actual
flow ratio q_y Q_yx/(q_x Q_xy). The corrected target kernel remains reversible.
The original population KL, proposal initialization, lazy mixture, rejection
diagonals and full-chain return conventions are unchanged.

## The sharp enlarged-class law

Put beta=1-alpha, r0=alpha exp(-K)/beta, bK=1-exp(-K). If r0<1, let
c* in (0,1) solve c*(1-c*)^((1-c*)/c*)=r0. For fixed real s:

| Regime | Across-run screen policy | Limit of (log n) times worst-case TV |
| --- | --- | --- |
| r0<1 | eta_n log n=loglog n/c*+s+o(1) | max(K,bK exp(-c*s)) |
| r0>=1, including equality | eta_n log n=loglog n+s+o(1) | max(K,(beta/alpha)(exp(K)-1)exp(-s)) |

The full proof is RECIPROCAL_PROPOSAL_THEOREM.md. Its new operation applies
Jensen with reverse proposal probabilities Q_yx, whose output-column totals
are bounded by an outgoing row of Q. The powered transition coefficient is
exactly Q_xy a_xy^p r_q^(-theta p). Subtracting actual accepted outflow through
the true rejection diagonal produces a support-uniform scalar bound.

This proves the entire weighted energy operation. At theta=c eta,w=1,
the exact scalar is F(c(1-eta)/(1-c eta))<=F(c). At theta=eta the weighted
scalar is exactly w. Both accepted absorbed first-hit interfaces therefore
survive, including the reciprocal boundary weight at r0>=1. The complete
proof retains original post-hit propagation, bounds accumulated multipliers,
uses one KL budget and transfers matching lower families by exact inclusion
of the unchanged symmetric subclass. It does not infer a law from a pointwise
off-diagonal comparison or an extremal induced norm.

## A structural classification within power screens

The natural further calculation considers first factor

    S_xy=(q_y/q_x)^eta (Q_yx/Q_xy)^kappa,

with second factor r_pi/S_xy. These kernels all preserve detailed balance.
For fixed 0<eta<1, however, uniform convergence over the unbounded proposal
class holds if and only if kappa=eta. Matched exponents have exact worst-case
amplitude K/log n. Every fixed mismatch has a positive uniform-floor lower

    beta(1-exp(-K))/(alpha exp(-K)+beta).

This is not an assertion of the exact floor. MATCHED_POWERS_THEOREM.md proves
the classification. When kappa<eta, many roots feed one leaf. When kappa>eta,
one root feeds many leaves. Use m=ceil(n^(4eta/abs(eta-kappa))) labels in the
large block, root/leaf/core proposal masses (b,b/n^4,1-b-b/n^4), and target
masses (n^-3,n^-1,1-n^-1-n^-3), with fixed 0<b<1-exp(-K). Native edge
ratios give 1<=S<=2^abs(eta-kappa), so the actual local kernel eventually
accepts forward with probability one and reverse with probability n^-2.
The native quotient is exact after all per-vertex ratios are computed.

The whole KL tends to -log(1-b)<K independently of multiplicity. A full-law
first-core/retained-leaf-block sandwich gives TV->b beta/[alpha(1-b)+beta].
Leaf-to-leaf and root-to-root global moves remain as block holds. The original
chain follows every first core hit. This proves an actual mixing obstruction.

For policies with bounded absolute mismatch, the same ceiling inequality
holds on every mismatched horizon, however small the mismatch. Thus infinitely
many mismatches prevent uniform convergence over unrestricted support. This
is only a necessary condition on moving policies; matched eta can still shrink
too quickly. The support can become enormous when mismatch is small. No
fixed-dimensional, wall-time or numerical-roundoff instability is inferred.

The separately preserved contributor source PROPOSAL_RATIO_NECESSITY.md gives
the q-only special case kappa=0, complete finite sandwiches and same-input
controls. The principal accepted that contribution without repair and supplied
the opposite geometry and general classification.

## Ordinary comparison and significance

Pure proposal-start independence MH has general leading minimax amplitude K
under the same KL premise. On the new mismatch families it has TV~1/n after
any deterministic number of steps proportional to n; the mismatched hybrid
retains positive error. The correctly matched hybrid converges on those same
inputs. Direct analytic block sampling is also admitted when that target
description is available. These are distributional comparisons, not matched
target-call or time benchmarks.

The useful result is a precise robustness condition: asymmetry of the proposal
is harmless for the stated sharp law when its reciprocal flow is screened
correctly, while reversibility alone cannot protect a differently factorized
screen. Native proposal generation, both proposal probabilities, target calls,
uniforms, caching, state indices and precision remain real costs. No normalizer,
target table, absorbed simulator or empirical KL certificate is supplied free.

## Internal checks and limits

One focused reviewer accepted the exact 21,709-byte principal theorem without
repair, including its full-return and uniformity interfaces. A distinct
construction contributor supplied the q-only example, which the principal
read and accepted. That contributor then reviewed the principal's general
powers, opposite geometry and moving-policy quantifiers; their own fan-in
material was identified as a transcription check, not counted as a second
independent audit. The 12,836-byte companion theorem was accepted without
repair within its stated scope.

Both new exact-rational diagnostics passed on their first executions, with
frozen contracts: 49 local and 49 mixture all-vector LDL certificates,
147 absorption/first-hit identities, four full-return identities, 24 native
quotient/hybrid sandwiches and eight ordinary sandwiches. The changed fan-out
geometry has its own additional frozen contract. A genuine failure of the
old counting-column premise is checked exactly: its absorbed column is 5.
The new reverse-proposal energy still passes. None of these finite checks
proves an asymptotic rate. Largest explicit matrix: 18 states.

Recorded diagnostic bodies took about 0.646 and 0.044 seconds wall time;
these are not discovery costs. Total inference/token/monetary and historical
research costs are unknown. The report and resource receipts distinguish
observed elapsed work, executable checks and later portable replay.

Closest primary comparisons and their scope are in SOURCES.md. Product-factor
detailed balance, delayed-acceptance harms and IMH weight-tail convergence
are established literature. A current DART mixing theorem also uses much
stronger geometric assumptions; no claim of the first mixing guarantee or
general sampler acceleration is made. Historical priority, external acceptance,
formal verification and useful implementation remain unestablished.

## Scientific decision and continuation

Close the reciprocal-proposal critical-law question and the stated unrestricted
two-power classification internally. Do not reopen the native fixed-parameter
boundary, prior first-order/fixed-screen/prefix or optional-prefix campaigns.
The next selected question is the sharp joint boundary with a genuine supplied
bound on proposal asymmetry, |log(Q_yx/Q_xy)|<=A_n, and a possibly mismatched
power policy. The unbounded-degree obstruction makes this an information and
resource question. Its sharp scale or amplitude is not claimed here.

The exact Cycle6 ZIP and its recursive accepted source chain are unchanged.
B3's pISO correction and failed full halo gate, the metadata and R3/anMC
closures, retired thermal/TPV/half-cell/molecular/GUIDE routes and other-owner
programmes remain preserved. Max owns integration. Private delivery is a
separate event from recipient reading, scientific acceptance or integration.
