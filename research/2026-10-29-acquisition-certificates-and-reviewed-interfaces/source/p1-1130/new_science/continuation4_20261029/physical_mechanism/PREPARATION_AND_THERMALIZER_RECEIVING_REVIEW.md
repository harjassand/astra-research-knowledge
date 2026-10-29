# Focused receiving review: preparation and selective memory repair

29 October 2026. Existing physical-mechanism role. This is a proof/interface
review, not a priority decision or apparatus acceptance. The independent
fixed-clock alternative is unchanged.

## Reviewed versions and disposition

- `PREPARATION_FROM_FLUCTUATIONS_AND_MEMORY.md`: SHA256
  `d5e366bdd17980e3ca6d894068ec09895d7a617c4583e4769df34c33853a9c90`.
- `SELECTIVE_MEMORY_THERMALIZATION.md`: SHA256
  `cd667a7b53580772953c6f0dc0aef1bb88f409bac1e5c23b5d488c2acf9ab836`.
- `check_preparation_memory.py`: SHA256
  `5e2a3310b68f014b327a1ebcc90f476a0282f6e60ab78bd257f22c65fc751aab`.
- Root check results: SHA256
  `197cb1b65da1f680c9d1619cf65c0bdf1ab1dccf9452a3fe97a838aa7221d408`.

Actual copies and the later conditional-compiler input are preserved in
`reviewed_versions/`, with their hash receipt. I read the complete proofs and
checker, reconstructed the arguments below, and reran that exact checker
from the pinned copy. No new fixture or wider test suite was added.

**Disposition:** the orbit inequality, componentwise-balanced causal matching,
full microscopic transport, finite-error cost order, finite-memory counterpart,
ordinary thinning failure, and selective heat repair pass this review at their
declared interfaces. The joint record bound passes for the literal stopped-
prefix protocol with independent controller seeds and unrecorded fresh heat
noise. Two sentences should be tightened before unqualified acceptance of the
written conditional-reference claim; neither changes the construction or its
constants. The general conditional-compiler theorem passes under its explicit,
strong conditional Markov instrument premise.

## 1. Orbit inequality and precision cost

The coupling uses the actual initial and terminal specimen states. Either
direction of a net shift J makes the two n-point orbit windows share at least
(n-|J|)_+ entries, counted with multiplicity. Averaging their TV bound and using
stationarity gives TV(rho A_n,mu)<=E min(K/n,1). Applying the same window kernel
to rho and nu gives

    F_n/2 <= E min(K,n)+n epsilon.

The backward density sum is changed to the forward sum by a fixed translation
of the stationary initial point, not time reversal. This is not an optional-
stopping argument. Complete microscopic knowledge and inverse access do not
evade it.

For iid signs, E|B_n|~sqrt(2n/pi). If E sqrt(K) were finite, the bound
min(K,n)/sqrt(n)<=sqrt(K) and dominated convergence would contradict this
asymptotic. Optimizing a sqrt(n/(2pi))-epsilon n yields n~a^2/(8pi epsilon^2)
and the stated lower constant a^2/(8pi) for epsilon E K. No factor of two was
lost. The confidence radius is also correct: each measured absolute block sum
lies in [0,nA], and the source explicitly requires independently warranted
baseline blocks and simultaneous treatment of multiple chosen n.

Starting from -1, the Catalan first-return distribution gives
q_N=binom(N,floor(N/2))/2^N. Dispatch has probability a/2, so the cap coupling
has error at most (a/2)q_N and cost

    1+(a/2) E min(H,N)=1+(a/2)sum_{j<N}q_j.

These give epsilon_N C_N -> a^2/pi. Thus the inverse-tolerance mean order is
proved, with a factor-eight leading-constant gap left open and a supplied
quadratic hard deadline. Conditioning on early completion is correctly excluded.

For the finite balanced bridge, zF'(z)U(z)=z^2/(1-z^2), whose coefficient at
z^(2m) is one. Dividing by the balanced-bridge probability gives
E R=4^m/binom(2m,m), then the stated initial-call cost and cap. Each cyclic
orbit is itself balanced, so target tilting does not change its conserved
weight. Half-window hypergeometric fluctuations give the asserted square-root
memory-length lower order.

## 2. Complete matching and the microscopic law

The termination proof is valid for stationary, possibly nonergodic signs with
E[xi_0|I]=0. An unmatched minus cannot precede an unmatched plus: the last
downward crossing of the latter plus's return level supplies its partner.
If both unmatched types existed, there would therefore be a last unmatched
plus, with a translation-invariant distribution on the integers. That is
impossible. The events that some unmatched minus or some unmatched plus exists
are themselves invariant. On either event, conditional sign balance and mass
transport give equal unmatched intensities. One type is absent, hence both
intensities vanish; countability and stationarity then exclude any unmatched
point. This does not require a visible Markov model or ergodic hidden memory.

The row transport has unit mass and its column mass is 1+a xi_0. Stationarity
and Tonelli transfer an arbitrary nonnegative test function of the complete
microscopic trajectory from the random destination to the incoming column.
Thus the conclusion is the full state law g mu, not just the sign marginal.
The two-sided extension certifies columns; the implemented row is forward-
causal. The charged first native call preserves the actual stationary premise.
Subsequent intervention programs require the complete operational Markov state,
as the draft says; unmodeled physical memory cannot be omitted.

For primary comparison I read the relevant introductions and theorem passages
of Holroyd–Peres, https://arxiv.org/pdf/math/0306402 , Last–Thorisson,
https://arxiv.org/pdf/0906.2062 , and Mörters–Redl,
https://www.mi.uni-koeln.de/~moerters/papers/Shift-revision.pdf . In particular,
Last–Thorisson Theorem 5.1 requires equality of intensities conditional on the
invariant sigma-field. This corroborates the load-bearing component condition.
The draft correctly treats these transport mechanisms as established. No
historical-priority conclusion is made here.

## 3. Ordinary thinning and the additional heat supplier

The baker map is invertible and area preserving apart from the declared null
binary ambiguities. Thinning fresh forward endpoint bits gives geometric call
count with mean 1+a and the exact desired u marginal. The rejected bits are
all zero. Conditional on T=t, v is uniform on [0,2^(-(t-1))), which gives the
written mixture density r(v) and leading-past-bit probability 1/[2(1+a)].
One inverse call exposes this deviation from the full target.

The Fourier heat bound is uniform in the actual input v. The inequality
k^2>=1+3(k-1) gives q/(1-q^3). For q=epsilon/2 and epsilon<=1, this is at
most 4epsilon/7, so the chosen thermalization time is sufficient. The physical
circumference-squared factor and diffusivity units are correct.

Since the added operation fixes u and uniformly mixes v, integrating against
the actual correlated input proves the full modeled-state error bound. Constant
mean native calls plus logarithmic thermalization time is a valid comparison
with the orbit-only inverse-tolerance mean lower bound. It is expressly an
added-resource separation. A conventional controller supplied the same heat
operation can use this protocol, and a genuine full baseline initializer is
another strong ordinary escape at its actual cost.

The state here is the complete state of the supplied operational model (u,v)
with a Markov heat bath. A bath or apparatus variable that affects future
operations or is accessible to future measurements belongs in the joint model.
The written instrument paragraph supplies that boundary. This is not acceptance
of erasure of every record in an unmodeled physical bath.

## 4. Retained record: valid theorem and two wording corrections

For the intended protocol, R is generated by the observed stopped prefix and
independent controller seeds. Unread accepted-u digits are still fair conditional
on that whole record. Keeping the actual (R,u) and replacing v by a fresh
uniform coordinate therefore gives a positive reference whose conditional state
law is nu given the recorded final bit. Uniform heat mixing gives the joint TV
bound. A common later physical continuation kernel contracts it, including
policies using R, without a growing observation-depth factor. Initial mu
conditional on the old record D is a real premise.

### Correction 1: marginal independence of added randomness is not enough

The phrase “extra randomness independent of the unexposed bit stream” should
be replaced by an explicit stopped-information condition. Let B be the first
unread bit after acceptance and Z a fresh retained fair seed independent of
the experiment. The extra variable A=B xor Z is itself independent of the
entire unread stream, but the joint record (A,Z) reveals B. Conditional on
this record, u occupies one quarter interval, not the full observed half;
the conditional discrepancy from nu|Y is 1/2. Heat acting only on v cannot
repair that information about u.

This is not executable using only the declared sole native bit read. It is
a precise counterexample to interpreting the permissive sentence as a mere
marginal-independence requirement. The joint inequality against a reference
retaining the actual R and actual u would survive, but the claim that this
reference is conditionally nu|Y would not.

Suggested replacement: R is measurable with respect to the stopped observed
prefix, D and controller randomness independent jointly of the initial state
and native innovations. Any additional record must obey the same conditional
non-revelation property for unread bits; timing must be measurable in this
information or independently certified to reveal no unread bits.

### Correction 2: equal external policy information does not control correlation

In the main preparation proof, “when supplied with the same external policy
information” should explicitly mean a fixed policy or independent shared policy
randomness. Equal state marginals and equal record marginals do not control
their joint law. Retained state-correlated preparation records need a conditional
or joint bound such as the thermalizer's equation (11). The surrounding text
indicates the correct intended scope, but the standalone sentence is broader.

Suggested replacement: Full-state TV controls later actual records for a fixed
policy or independent common policy randomness. A policy using state-correlated
retained information requires a bound on the complete joint state/record law;
the marginal matching theorem alone does not supply it.

## 5. Exposed thermal noise: an attack inside the stated protocol

The draft's known-input counterexample is correct: given initial v and exposed
Brownian displacement A modulo one, v_out=v+A is a point conditional on A.
Its TV from an independently uniform coordinate is one, regardless of the
near-uniform marginal heat kernel.

The same failure can be witnessed directly in the stated thinning protocol,
without a known initial v. Let R_0 be its ordinary record and K=T-1 the number
of rejected endpoints. Conditional on R_0, v_in is uniform on an interval of
length 2^(-K). Retaining the heat displacement A makes v_out uniform on a
translated interval of that same length. Hence the joint TV from a reference
preserving (R_0,A,u) but replacing v by an independent uniform coordinate is
exactly

    E[1-2^(-K)] = 1-s/(1-q/2) = a/(2+a),
    s=1/(1+a), q=a/(1+a).

For a=1/3 the floor is 1/7, independent of heat time. This is an analytical
attack on the exposed-noise extension, not a new numerical fixture. It confirms
that the unrecorded-noise premise is load bearing. Additional initial bit reads
can make the floor larger. It does not invalidate the declared unrecorded bath.

## 6. General conditional compiler: focused check

I also read the complete `CONDITIONAL_PREPARATION_COMPILER.md` at the version
specified in the input receipt. Its actual premise is the per-input, complete-
instrument bound

    TV(J_y(x,da,dx'), J_y^A(x,da) mu_y(dx')) <= epsilon_y,

valid after conditioning on the actual preceding history. Integrating this
bound over any record-conditioned input law yields exactly the same actual
record marginal times mu_y. Further integration over R and L gives the written
reference Law(R,A) mu_L and error E epsilon_L. No initial-baseline independence
is needed. Since L|D=q(D) and actual reachability terminates, the reference state
marginal conditional on D is the claimed mixture. A fresh specified label draw
has its usual conditional independence from unknown device parameters.

This instrument premise is substantially stronger than stationarity, a marginal
mixing kernel, or a nominal average over an advance noise key. It may be
impossible if an unconditioned frozen hidden sector must remain unchanged while
mu_y mixes sectors. The calibration/device clause correctly conditions instead
on the actual parameter and preserves its posterior. Initializers, sensing,
reachability, actual elapsed time, and supplier acquisition remain real costs.

The proof is an averaged joint-TV guarantee, not a uniform conditional bound
for each rare emitted record. Arbitrary later programs are covered with their
complete unconditioned records; a separately postselected conditional comparison
would require its own success-probability accounting. The draft makes no such
stronger claim. The reduced-memory version in Section 5 correctly treats
readiness of (R,u) as a separate proved premise. Its use for the baker receiver
needs the stopped-record precision correction above.

## 7. Validation and final scope

The unchanged pinned checker was rerun successfully: twelve balanced-ring
cases, 252 orbit inequalities, ballot survival, precision values, thinning
failures, inverse-map identities and heat-bound arithmetic. Its retained-noise
binary example is an instrument illustration, not a Brownian apparatus run.
The reproduced JSON is saved alongside the snapshots.

No algebraic defect was found in the central preparation or repair construction.
With the two record sentences made explicit, the complete retained-record claim
is accepted at its stated operation, baseline and instrument interfaces.
No acceptance extends to arbitrary calibration-conditioned baselines for the
reduced baker repair, exposed bath-noise records, finite-precision apparatus,
same-resource practical superiority, or historical priority.
