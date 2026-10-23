# A fixed local safeguard restores proposal-start robustness

**Astra PRO3 — scientific checkpoint, 22 October 2026 (Australia/Brisbane).**

The new result is a sharp robustness theorem for a fixed local/global sampler,
followed by a weaker-screen extension. It does not establish a sampler speedup.
The received optional-prefix obstruction is accepted within its exact access
contract and is not repeated.

## 1. Scientific decision

I changed the construction rather than continue the closed candidate-only
optional-prefix question. An arbitrary target-reversible local move can move
initial proposal mass into a rare, persistent target region. The previous
forward-KL guarantee then has a positive worst-case error floor. The question
selected here was whether a structural restriction on the fixed local move
prevents that failure without a special global prefix.

The answer is yes. If the one-step image of the proposal satisfies

\[
qL\le \Lambda q
\]

for a common finite constant \(\Lambda\), then the original proposal-start lazy
mixture has sharp worst-case coefficient \(K\), under forward population KL
alone. A standard two-stage delayed-acceptance operation enforces this condition
with \(\Lambda=2\), using evaluable proposal ratios and an unnormalized target.

The substantive continuation then weakened that safeguard. In a finite-space
family with a fixed symmetric local proposal, every fixed positive screening
strength eliminates the uniform error floor. A proved interval near full
screening retains coefficient \(K\). The exact rate outside that interval is
the chosen next question, not a reason to reopen the old prefix result.

Pure independence Metropolis-Hastings (IMH) already has coefficient \(K\).
The value of the theorem is identifying local operations that preserve its
worst-case robustness. Neither asymptotic equality nor the numerical example
below establishes finite-time dominance or practical improvement.

## 2. Recovery and acceptance of the new input

The supplied collection was read from its actual attached local bytes. Its
identity is recorded in INPUT_RECEIPT.json. Its nested owner archive is
Astra_Intelligence_Cycle_PRO3_20261021.zip, exactly 363,537 bytes, SHA256
5f49846ea3b1d74f72833e61d17896a8609b8909be07764a070c737a2cd80f0d.
It matches the existing local owner export and is included unchanged.

I read both optional-prefix proofs, their contracts, unsuccessful approaches,
costs, and blind verdict. I accept both without repair. The critical point is
that paired positive finite instances share the entire labelled public q and Q
and the complete stopped history, including raw target values and repeats.
Averaging hidden subsets precedes Jensen; the local capture and retention
event supplies the TV consequence. Neither proof substitutes an expected
stopping time into a fixed-prefix formula.

The result excludes a uniform fixed fractional saving over the whole easy null
family under the stipulated candidate-only, bounded-fallback access model,
with the same positive supplied K. It does not exclude richer access, a
specified easy subclass, or improvements on particular instances. Arm A covers
any finite common deterministic subsequent schedule; arm B supplies its
explicit additive bound at the stated schedule. RECEIVED_PREFIX_ACCEPTANCE.md
records the owner assessment. The sources are retained under
sources/received_prefix/. Their scientific work is attributed to the incoming
contributors; accepting it is not a new proof or a prompt-tactic comparison.

## 3. Main theorem and implementable operation

Let pi and q be equivalent probability measures on an arbitrary measurable
space. Let \(W=d\pi/dq\) be a positive finite measurable version, G the IMH kernel
with proposal q, and L a fixed pi-reversible kernel. Fix \(K>0\),
\(0<\alpha<1\), \(\beta=1-\alpha\), and a finite \(\Lambda\ge1\). Retain

\[
C=\frac{I+\alpha G+\beta L}{2},\qquad X_0\sim q,
\quad D(\pi\Vert q)\le K,\quad qL\le\Lambda q.
\]

Write \(\mathcal R(n)=\sup\|qC^n-\pi\|_{\rm TV}\), with the supremum over exactly
that class, and T for its worst-case deterministic mixing time. Then

\[
\boxed{\lim_{n\to\infty}(\log n)\mathcal R(n)=K,\qquad
\lim_{\epsilon\downarrow0}\epsilon\log T(\epsilon)=K.}
\]

K, alpha and Lambda are fixed in these limits. No uniform claim is made as
Lambda grows, alpha vanishes, or the information contract changes.
SAFE_LOCAL_THEOREM.md contains the complete upper proof, positive finite
matching lower family, explicit asymptotic inversion, and finite certificate.

To implement a sufficient condition, use a fixed q-reversible proposal R and
accept its proposal y with \(\min(1,W(y)/W(x))\). Incoming accepted q-mass is at
most qR=q, and rejected mass is at most q, so \(qL\le2q\). A concrete R is
ordinary MH(Q,q). On a local branch, first apply the q-MH acceptance and then,
only if it passes, apply the target/proposal-weight correction. Common
rescaling of the target oracle cancels. No target normalizer or normalized
weight threshold is needed.

This is the established delayed-acceptance construction, not a new acceptance
algorithm [S2]. Its density-evaluation requirements are real additional access
relative to a merely sampleable q. The theorem's new argument concerns its
uniform proposal-start entropy robustness.

### The load-bearing argument

One-step domination implies \(qC\le cq\), where
\(c=(1+2\alpha+\beta\Lambda)/2\), hence \(qC^j\le c^j q\).
Let tau be the first time the actual chain reaches \(W\ge h\). While it remains
below h, a global candidate outside that set is surely accepted. Therefore

\[
\Pr(\tau>s)\le b_h[1-\alpha(1-b_h)/2]^s,\qquad b_h=q(W<h).
\]

The first-hit submeasure at time j is bounded by \(c^j\pi/h\). Propagating that
unconditioned submeasure through the same invariant C retains all later
returns below h. For \(D\subset\{W<h\}\),

\[
(qC^s)(D)\le b_h[1-\alpha(1-b_h)/2]^s+
\frac{\pi(D)}h\sum_{j=0}^{s}c^j.
\]

This is a first-state-hitting argument along the actual unchanged hybrid.
It does not evaluate a deterministic-prefix law at a random time.

The accepted binomial near-harmonicity lemma and the anchored Dirichlet bound
are then applied to a general probability \(\mu\le Aq\), with its true low-set
mass retained. Taking \(s=O(\log\log n)\), \(h=(\log n)^{-2}\), and suitable
high and low cutoffs makes the low-set error and smoothing errors
\(o(1/\log n)\). Forward KL bounds the only leading target tail by
\((K+o(1))/\log n\). A two-state family with \(L=I\) gives the matching lower
coefficient. The full proof explicitly handles growing s and inversion.

## 4. A weaker screen: what is now proved

For this extension only, take finite strictly positive q, pi, and a fixed
symmetric stochastic Q. The support may grow in the supremum. For a fixed
\(0\le\eta\le1\), accept a local proposal with probability

\[
a_\eta(x,y)=
\min\{1,(q(y)/q(x))^\eta\}
\min\{1,(\pi(y)/\pi(x))(q(x)/q(y))^\eta\}.
\]

The reciprocal factors make \(L_\eta\) pi-reversible. Eta=0 is ordinary local
MH; eta=1 is the fully safeguarded operation. Lower eta weakly increases every
off-diagonal local acceptance. It can also increase expensive target queries.
The local kernel and eta remain fixed throughout each instance.

Let \(\theta_K=1-\alpha e^{-K}/2\). The complete proof in TEMPERED_SCREEN.md gives:

| Fixed screening strength | Established uniform conclusion |
| --- | --- |
| eta=0 | Inherited positive floor \(\beta b_K/(1-\alpha b_K)\), \(b_K=1-e^{-K}\) |
| Every eta>0 | Zero uniform floor; finite uniform time at every positive error |
| eta>\(\theta_K\) | Sharp coefficient K for both risk and mixing time |
| \(0<\eta\le\theta_K\) | Sharp coefficient unresolved; a nonsharp logarithmic risk bound is proved |

At K=1 and alpha=1/2, the sufficient sharp interval is eta>0.9080301397.
For example, a fixed eta=0.95 accepts at least as readily as full screening and
has the same uniform coefficient. This is an algebraic acceptance comparison
and a worst-case asymptotic theorem, not a TV ordering or a speed measurement.

The new technical step is setwise power domination. Holder gives
\(qL_\eta(A)\le q(A)+q(A)^\eta\), and then
\(qC_\eta^j(A)\le D_j q(A)^{\eta^j}\), with
\(D_j\le(3/2)^{1/(1-\eta)}\). A layer-cake/Jensen lemma transports this bound
through kernels. First-hit propagation controls the low-weight mass;
density truncation constructs a comparison probability bounded by \((V+1)q\).
Its TV approximation error and added low-set mass are both charged.

Choosing fixed parameters before sending time to infinity proves the zero
floor for every fixed eta>0. For eta>\(\theta_K\), a growing-time balance
makes the first-hit, truncation and core errors all \(o(1/\log n)\).
The remaining upper coefficient is K, matched by Q=I.

For eta in (0,1), put \(\kappa=-\log\theta_K\), \(\ell=-\log\eta\). The same
estimates prove, for any fixed
\(0<\zeta<\min(1,\kappa/\ell)\),
\[
\mathcal R_\eta(n)=O((\log n)^{-\zeta}),\qquad
T_\eta(\epsilon)\le\exp[O(\epsilon^{-1/\zeta})].
\]
This sufficient bound is not sharp. In particular, it does not prove that a
positive eta has a coefficient larger than K. The independent reviewer
identified this quantitative consequence; its attribution is retained.

## 5. Actual calculations and matched ordinary methods

The principal implemented exact rational kernels, deterministic matrix laws,
and cost accounting in safe_local_calculations.py. No sampler trajectories were
simulated. The fixed input and thresholds preceded inspection of these outputs.
The three-state target and proposal use

\[
p=1/50,\ b=1/2,\ r=p2^{-20},\ s=p2^{-40},\quad
\pi=(p,s,1-p-s),\quad q=(r,b,1-b-r),
\]

and the symmetric proposal
\[
Q=\begin{pmatrix}1/5&4/5&0\\4/5&0&1/5\\0&1/5&4/5\end{pmatrix}.
\]

The forward KL is approximately 0.936744493385, below the frozen bound 1.
Ordinary local capture gives a one-step q-density multiplier of about
20,971,520 at the trap; full screening satisfies the proved bound 2.

The first deterministic-time TV crossings are:

| Target TV | Pure IMH steps | Ordinary hybrid steps | Safeguarded hybrid steps |
| --- | ---: | ---: | ---: |
| 0.10 | 3 | 3,786,904 | 9 |
| 0.03 | 5 | 8,836,729 | 15 |
| 0.01 | 726,817 | 13,444,641 | 2,907,262 |

These are matrix-power calculations, not executed runs of millions of sampler
transitions. Both bracketing adjacent times were computed. The exact rational
short-horizon checks and 80/120-digit consistency checks are separately recorded.
They are not outward-rounded interval proofs of every displayed decimal.

At TV 0.03, the expected cost breakdown is:

| Operation | Global candidates including initialization | Local Q proposals | Target evaluations with complete memoization |
| --- | ---: | ---: | ---: |
| Pure IMH | 6 | 0 | 1.9687501109 |
| Ordinary hybrid | 2,209,183.25 | 2,209,182.25 | 2.2969250524 |
| Safeguarded hybrid | 4.75 | 3.75 | 1.9441776112 |

The last row uses fewer global draws and slightly fewer distinct target values
than pure IMH on this input, but more total proposals and more implementation
work. No wall-clock exchange rate for those costs is supplied. The tiny
distinct-query counts are possible because this diagnostic has only three
states and complete memoization; they do not make millions of proposals cheap.
If the entire normalized finite target table were provided to the actual
sampler, direct discrete sampling would be stronger. This is a mathematical
mechanism diagnostic, not a scientific application benchmark.

The frozen contract originally specified current-state caching. A subsequent
cost challenge correctly required complete memoization too. The implementation
reports both; COST_CONTRACT_ADDENDUM.md records that strengthening without
changing the input, accuracy thresholds, or theorem acceptance gate.

The independent exact four-state counterexample is stronger than a caution:
q is uniform, pi=(3/8,3/8,1/8,1/8), and Q swaps within each pair. Here qL=q.
At four hybrid steps, TV is 625/5184 and the expected total number of target
queries is 442183/196608. One pure-IMH update uses the same expected one
post-initial global draw, has TV 1/12 and uses only 7/4 target queries.
The counts include initialization and full memoization. An explicitly
randomized one-or-two-update pure-IMH comparator also beats the hybrid at
exactly equal expected target-query cost. The code and complete calculations
are in reviews/safeguarded_cost_challenge.md and its companion files.

Finally, the five evaluated conservative uniform certificates all favor pure
IMH. For errors 0.1, 0.03, 0.01, 0.003, 0.001, the chosen integer x in a budget
roughly exp(x) is respectively 83,114,145,382,1088 for the hybrid and
18,44,116,364,1068 for pure IMH. These are sufficient bounds with specified,
unoptimized proof parameters, not measured mixing times or efficiency ratios.

## 6. Verification, failures and boundaries

The main argument passed an independent targeted check of first-hit measures,
the finite initial-law inequality, growing-s uniformity, and the lower
inversion. The final proof source is bound by exact hash. The extension passed
a separate full-source challenge of power transport, density truncation, the
order of limits, and the sharp-interval exponents. One display was corrected:
since A=V+1, its asymptotic A-squared expression needs an o(1) in the exponent.
No conclusion changed. The old proof bytes were not rewritten.

Actual exact diagnostics checked 15 chains, 250 first-hit decompositions and
6,740 rational inequalities. The principal's 80- and 120-digit outputs agree
on all crossing times, integer counts and certificate budgets; among 404
numeric-string values the largest absolute difference is about
\(1.26\times10^{-67}\). The relocated four-configuration replay reproduced
all scientific JSON, ignoring resource fields. No old theorem or controlled
trial was rerun.

Two failures matter for continuation. A tempting linear-in-time density bound
\(qL^t\le(t+1)q\) is false, with an exact three-state witness retained. Also,
for every eta<1, a positive two-state forward-KL family makes
\(qL_\eta(A)/q(A)\) unbounded. The latter defeats direct reuse of the linear
domination proof; it does not defeat the tempered sampler. Its weaker power
bound is precisely why the new proof is needed.

The implementation uses ideal exact kernels for the theorem and finite rational
diagnostics. Approximate ratios, floating-point accept/reject error, approximate
q, nonreversible or changing L, deterministic schedules, and empirical KL
certification require separate analysis. The tempered result is finite-space;
the general domination theorem has arbitrary-measurable-space scope. These
contracts are not conflated.

## 7. Relation to existing methods and status

Delayed acceptance and reference-reversible proposals are established methods
[S2]. Stationary efficiency ordering does not supply the new proposal-start TV
theorem [S2,S4]. Existing weak-Poincare transfer arguments have relevant
L2/integrability hypotheses; those do not follow from this forward-KL
proposal-start contract [S3]. The new first-hit and density-truncation arguments
handle that missing initial-law control.

Kurennoy--Yarullin--Reid Theorem 6 concerns a fixed-pool rollout/certification
barrier, including its own discussion of known proposal/support access [S1].
It is not substituted for the received known-K optional-prefix proofs, and it
does not rule out the explicit structural kernel restriction used here.
SOURCES.md records exact sections, URLs and the limits of the bounded search.
Historical priority and external mathematical acceptance remain unestablished.

Scientific source and the private handoff remain distinct from receiver
collection, independent external acceptance, and Max's integration. The old
B3 correction/rejection and R3/anMC rejection stay preserved with exact source
identities. No empirical campaign, protected-owner construction, public release,
purchase, laboratory intervention, or user relay was initiated.

## 8. Next owned scientific step

Determine the sharp coefficient for the same fixed tempered family in
\(0<\eta\le1-\alpha e^{-K}/2\). Is it K for every positive eta, or does a valid
positive-eta construction force a larger coefficient or a different scale?

The present sufficient threshold comes from balancing the geometric first-hit
hazard against repeated deterioration of a power bound. A stronger upper
argument must improve that accumulation or control excursions directly.
A lower construction must respect positivity, the forward-KL budget, the fixed
public symmetric Q, and both acceptance stages. Failure of a sufficient bound
alone is not a lower theorem. This is the precise next boundary; no application
search is needed to justify its structural significance.
