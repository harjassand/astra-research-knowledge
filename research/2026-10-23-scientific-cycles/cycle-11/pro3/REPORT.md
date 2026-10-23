# Astra PRO3 Cycle11 scientific checkpoint

23 October 2026, Australia/Brisbane.

## Strongest result

The arbitrary-geometry gap is closed internally. The critical worst-case
total-variation risk has the same phase modulation as the previously attained
tree family. A heterogeneous reciprocal proposal cannot fill a nonzero-phase
trough at leading order. When its transport amplitude exceeds the ordinary
information amplitude K, the unrestricted minimax amplitude itself has no
limit: its exact liminf and limsup differ.

The governing proof is NATIVE_PATH_COMPOSITION_THEOREM.md. Its new finite
path-composition bound is the main structural result. It does not presume
that transport has a scalar state coordinate or that a general graph reduces
to a forward tree. It accommodates proposal cycles with nonzero likelihood
circulation, merging, native row budgets, global transitions, real rejection
diagonals and all original post-hit returns.

The same argument proves a wider law for arbitrary fixed, target-independent
antisymmetric log-screen distortions bounded by d. This separates the
robustness mechanism from a particular choice of mismatched proposal powers.
It is an exact-real theorem, not a numerical-error or implementation claim.

## Exact conclusion

The native contract remains finite positive pi,q, one population
D(pi||q)<=K, q initialization, fixed alpha in (0,1), beta=1-alpha and
target-independent reciprocal row-stochastic Q. At horizon n the public
screen parameters and proposal stay fixed during the run. The screen and its
second Hastings correction, actual diagonal and lazy mixture are unchanged.
The public asymmetry promise gives |kappa_n-eta_n|A_n=d>0.

Write ell=log n, L=log ell, u_n=eta_n ell and

    r=alpha exp(-K)/beta, b0=1-exp(-K),
    gamma=log(1+r), t=r/(1+r), d_star=gamma/t,
    c(d)=inf_{a>=0} log(1+r exp(a))/(d+a).

For fixed d>d_star and s, at c(d)u_n=L+s+o(1), put

    Psi(x)=min{(dt-gamma)x,gamma(1-x)}, 0<=x<=1,
    phi_n={u_n/d}.

The new theorem is the pointwise asymptotic law

    (log n)R_n=max{K,b0 exp[-s-Psi(phi_n)]}+o(1).

Consequently,

    limsup (log n)R_n=max{K,b0 exp(-s)},
    liminf (log n)R_n=
      max{K,b0 exp[-s-gamma(1-d_star/d)]}.

The limit exists exactly when b0 exp(-s)<=K, in which case it is K.
For the other critical regimes, the previously completed limits are
preserved unchanged.

For the unchanged illustrative values K=1, alpha=1/2, d=3, s=-1, the exact
limsup is approximately 1.718281828459045 and the exact liminf is approximately
1.418630176071266. Previously the latter number was only a lower bound.
Now the entire phase curve is proved for the unrestricted supremum. The
figure in evidence/phase_law/ evaluates this formula; it is not a matrix-power
experiment or new empirical evidence.

## The new finite operation

Let A be a low-importance-weight set, E a subset of its complement, b=q(A),
e=q(E), and r_b=alpha(1-b)/beta. Let H_N(E) denote the mass of original
first exits from A by time N that land in E, starting from q restricted to A.
The theorem proves, for every U>0,

    H_N(E)<=b V_{d,r_b}(U)+3e(3/2)^N exp(U/eta),
    V_{d,r_b}(U)=
      exp[-min_{J>=1} J log(1+r_b exp((U/J-d)_+))].

The control value V was already proved in Cycle10. The new work is the
valid connection from arbitrary native paths to that value.

Resolve each off-diagonal transition into its local or global mixture tag,
and keep every actual stay as one diagonal tag. Reverse the proposal
factors along a path, paying the full actual diagonal. A local edge
contributes signed progress -eta log r_q; a global edge contributes zero.
The auxiliary reference is not a Markov kernel: its row sums are at most
3/2. That produces the explicit second term in the bound. It controls paths
that reach a q-small set without sufficient signed progress, including
paths through cycles and shared terminal states.

For the remaining paths, clip negative local progress to zero only in the
proof counter. Every global exit from the low-weight set is accepted and
has exact killing probability alpha(1-b)/2. The true local acceptance and
the complete proposal row budget give a bounded supermartingale from the
closed control value. Global moves within the set and negative-progress
local moves may change state and reveal history; the inequality holds
after every such history. They are not deleted.

A final global hit in E has zero progress. If its path has enough signed
progress, it crossed the threshold earlier and has already paid the control
cost. Otherwise it is included in the rare-set reverse bound. This resolves
the potentially uncharged direct-global-hit branch.

The inherited smoothing decomposition uses the original chain after every
first hit. Taking N=O(loglog n), e<=O((log n)^6(loglog n+1)/n), and an
explicit threshold U=u-o(1) makes the complete reverse defect at most
(log n)^-3. The integer crossing cost remains. One KL inequality,
k+(log n)a<=K+o(1), then couples the source and information tail and gives
the MAX in the theorem.

## Broader mathematical consequence

The finite transport theorem does not itself need a target, a KL bound or
stationarity. It needs a proposal likelihood-ratio bound on local
acceptance, the actual proposal rows and a global transition component
dominated by q with the specified exits. Its proof gives a way to combine
rare-set mass, cumulative likelihood progress and real killing without a
deterministic geometric coordinate.

In the target-corrected application one may replace the power screen by
S_xy=r_q(x,y)^eta exp(xi_xy), where xi is a fixed, target-independent,
antisymmetric edge function with |xi|<=d. The second Hastings factor still
gives pi-reversibility. The same upper applies and the old native families
are a subclass, so the sharp law is unchanged. This is a broader
robustness statement than the original formula tied to Q asymmetry.

Path reversal and periodic tails are established mathematical ideas. The
new claim is the stated finite composition inequality and its exact
information-constrained minimax consequence, under its explicit hypotheses.
The focused primary comparison in SOURCES.md does not establish historical
priority or external mathematical acceptance.

## Strong ordinary comparison

Ordinary independence MH remains allowed the same q and target-ratio
information. Its minimax amplitude is K. On the SAME adverse native
families, its error is O((log n)^-4) at a positive fraction of n global
transitions, while the hybrid error is order 1/log n. Direct analytic
sampling is legitimate when the analytic target is actually supplied.

This result explains a sharp robustness failure of the hybrid; it is not
a useful-sampler, target-call or wall-time improvement. The actual tree
construction can have enormous support and tiny atoms. Its preparation,
labels, target/proposal calls, reverse probabilities, precision and storage
remain charged. A proof counter is not an implementable absorbed sampler.

## Checks, corrections and resource scope

The supplied original archive matched 3,508,928 bytes and SHA256
55afc9d70013d8cc0332d6a03c51901876533d908412448d7d81b2b6f393e1c1.
The local principal proof matched the same scientific version; no newer
owner-local result was overwritten. The full predecessor is retained
unchanged, with its recursively preserved source chain.

One new exact rational diagnostic uses a frozen four-state reciprocal but
nonreversible proposal at deterministic horizon 5. It checks 16,401 tagged
path identities over 4,686 first-hit paths, actual diagonal and row budgets,
positive and negative cycle progress, and 640 high-progress paths ending
globally. Every such global-ending path completed its threshold earlier.
An independent exact first-hit recurrence agrees with path enumeration.
The example is admitted with K=24 by an explicit exact bound; it is not a
K=1 example or a critical-scale estimate. Its inputs were frozen before
execution and were not retuned.

The diagnostic reported 0.129040814 CPU seconds, 0.12904939099826152 wall
seconds and peak RSS 10,624 KiB. Source reads, artifact handling and the
formula figure are accounted for separately. Inference/token, design and
total discovery costs are unknown. Short diagnostic or transfer time is
not discovery cost.

A separate source-bound reviewer checked the finite bridge, full-return
replacement, cutoff, stability, one-budget allocation, phase quantifiers
and wider screen class. The review requested an explicit absent-edge
convention, which was added; no mathematical repair of the theorem was
needed. The final review and exact source binding are in reviews/.
Internal acceptance is separate from formal verification, historical
novelty, external acceptance and useful implementation.

The admitted 32-state historical fixture and failed-K=1 5,462-state
coalescence fixture remain unchanged. Neither the old suites nor the
evaluator's subset-observation query was rerun. The earlier precision note
was not made into a new campaign. Protected and retired programmes remain
untouched. There is no active numerical job at this checkpoint.

## Scientific continuation and receiving use

The finite arbitrary-geometry critical phase question is now closed
internally. The selected next question is a representation-independent
extension to standard Borel spaces using the reciprocal proposal flow
m(dx,dy)=q(dx)Q(x,dy), rather than assuming a counting measure or a
forward/reverse density oracle.

A complete extension must handle singular/self proposals, measurable
path reversal, the bad-set/full-return interface and actual evaluation
requirements. A sharp atomless realization must be constructed; a finite
quotient cannot be renamed a continuous sampler. This direction tests the
transport principle beyond its finite representation, rather than refining
another constant. It is not claimed solved here.

The actual receiving use in this checkpoint is precise: the Cycle10
history-dependent control and full-law native lower, together with the
Cycle8 smoothing/return operation, became the matched arbitrary-geometry
phase law through the new path bridge. This is cumulative scientific use.
It does not identify a causal advantage from a prompt style, agent count,
fresh reset, numerical instrument or archive delivery.

Max receives the complete source through the established private handoff.
The same source is available to the evaluator. The external delivery
receipt records byte identities and verified transport separately from
reading, scientific acceptance and repository integration. No user file
handling or coordination is needed.
