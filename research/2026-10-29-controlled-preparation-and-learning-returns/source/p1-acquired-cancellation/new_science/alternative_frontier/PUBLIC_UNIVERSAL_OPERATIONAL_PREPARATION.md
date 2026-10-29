# Public universal preparation from an unknown contractive word

29 October 2026. Complementary Astra P1 construction. Ordinary proof below is new in this continuation; no external review, hardware operation, acquisition or historical priority is claimed.

## 1. Destination and selected obstruction

The consequential alternative to native thermal inference is a preparation operation that makes an inaccessible, possibly infinite, environment operationally forget old calibration records. A learner could then reuse a source without microscopic regeneration. The meaningful target is joint future-output decoupling from arbitrary retained classical or quantum records, not agreement of one visible marginal.

Current Astra already supplies two different pieces. U1198's corrected complete-port source (9481fa0a...) turns actually informationally complete input/output experiments and a supplied finite hidden dimension into complete finite-horizon prediction; its whole-process starts remain paid. The later operational-quotient reset source caf0b2b... has a completed independent ordinary review (0d7e218f...) despite a stale pending-review header. It replaces future starts after an acquired complete core by a fixed certified contractive word, and explicitly preserves the cold-start gap. Selecting different reset words from a pilot can select different limiting preparations, leaving information about the pilot in the prepared source.

The construction here removes WORD SELECTION from the physical operation. Before acquiring any source-dependent data, fix a public finite control sequence that contains every sufficiently short possible reset word. If one of those words contracts the COMPLETE operational distinguishability, the fixed sequence contracts too. No secret key or knowledge of the successful word is needed. The contractive-word length and strength are still substantive, acquired or warranted inputs.

## 2. Native operation and operational norm

Let M be the source memory, which may be a separable infinite-dimensional Hilbert space. A finite alphabet A of s>=1 legal completed operations induces normal CPTP maps Phi_a on trace-class memory operators. Each completed operation initializes its accessible ancillas in a fixed fresh state, executes the native operation, and discards accessible outputs/outcomes. The choices of letters and their timings are fixed independently of the old record. Native outcomes are not postselected or silently retained for feedback.

Fix an invariant reachable algebraic domain of Hermitian trace-class operators. Finite reference amplifications are included. Let F range over all declared finite future accessible controllers, retaining a finite reference R if present. The complete future-distinguishability seminorm is

    ||X_MR||_op = sup_F ||F(X_MR)||_1.

The supremum includes leaving R unchanged and retains the complete averaged output, without normalizing rare branches. An invisible operator may have zero seminorm. Every allowed future map is CPTP on the physical source and caller, so ||X||_op<=||X||_1. For a positive unit-trace state the norm is one, provided a trace-retaining trivial future is admitted.

A completed native word can be prepended to every allowed future controller. Therefore, for every word w,

    ||(Phi_w tensor id_R)(X)||_op <= ||X||_op.              (1)

This is a property of the DEFINED future interface. A smaller test menu that is not closed under prepending native words would not justify (1).

### Complete contraction promise

There is at least one nonempty word w_* of length at most L such that, for every finite R and every Hermitian X in the stated amplified domain satisfying Tr_M X=0,

    ||(Phi_w* tensor id_R)(X)||_op <= c ||X||_op,           (2)

where a warranted numerical c<1 is supplied. The zero marginal is an OPERATOR identity on R. A coefficient proved only for two uncorrelated scalar initial states is insufficient.

This promise does not assert full hidden-memory trace-norm contraction. It can hold when an invisible counter records every earlier operation forever. It is also stronger than a private convex mixture that contracts only after its key is discarded.

## 3. Fixed cover operation

For s>=2 choose a de Bruijn cycle of order L over A and append its first L-1 letters. The resulting public linear word C has length

    N_cover = s^L + L - 1,                                (3)

and contains every length-L word as a contiguous substring, hence every nonempty word of length at most L. For s=1 use the unique length-L word, also consistent with (3). A standard Euler-cycle construction gives the word on the graph whose vertices are length-(L-1) strings and edges are length-L strings. The full word can be streamed; no oracle for the unknown source is used.

Write C=p w_* q. With letters applied from left to right, Phi_C=Phi_q Phi_w* Phi_p. Partial trace over M is preserved by every CPTP factor, so Phi_p X remains in the zero-marginal domain. Equations (1)-(2) give

    ||(Phi_C tensor id_R)(X)||_op <= c ||X||_op.           (4)

The same public C works for every source that satisfies the promise, even if the successful word and its limiting state differ between sources. Repeating C t times yields coefficient c^t. This is the exact construction; it is not a claim that finding a shorter synchronizing word is hard or that this exhaustive cover beats a known successful word.

A finite predeclared candidate pool can instead be concatenated, or covered by a shortest common superstring computed conventionally. The full-word cover (3) is convenient when only L is available. If a particular reset word is already known and its target is acceptable, repeating that word is the stronger conventional route.

## 4. Common operational limit and complete decoupling

The map C is now FIXED before calibration. It has a single operational limiting preparation independent of the input record, even when no hidden trace-class stationary state exists.

Take an arbitrary physical reference input rho_*. For integers m>=n,

    ||Phi_C^n(rho_*) - Phi_C^m(rho_*)||_op
      = ||Phi_C^n[rho_* - Phi_C^(m-n)(rho_*)]||_op
      <=2 c^n.                                           (5)

Thus every finite accessible output process has a norm limit. The finite input/output Choi matrices of these processes converge, remain CP and TP, and remain causally consistent. Denote the resulting compatible finite-horizon process by P_infty. This is an operational process, not a claimed normal invariant state of M.

Now let Omega_MR be ANY normalized positive joint state in the invariant amplified domain, and let Omega_R be its retained-record marginal. For m>=n,

    ||Phi_C^n(Omega_MR)
        - Phi_C^m(rho_*) tensor Omega_R||_op
      <= c^n ||Omega_MR
        - Phi_C^(m-n)(rho_*) tensor Omega_R||_op
      <=2 c^n.                                           (6)

Pass to the finite accessible-output limit m->infinity. Every subsequent finite allowed controller, which can use R coherently and adaptively, has output half trace distance at most

    epsilon_reset(n) = min(1,c^n)                         (7)

from the same controller acting on P_infty independently of R. The comparison retains R and all future outputs. There is no dimension factor for R.

This proof gives a uniform bound against arbitrary initially correlated records. It does not need the hidden state to converge, an environmental reset, a stationary density, a hidden-state readout, or literal finite Markov order.

### What may remain public

The action word C and its fixed duration may be public: they are identical for every old history. A service can retain all records that existed BEFORE preparation. The fresh native outcomes produced DURING preparation must be discarded as stipulated. Retaining those outcomes can correlate the final source with them and requires a new analysis; it is not licensed merely because the action schedule is public.

One can choose the repetition count n from a classical calibration record, while keeping C fixed, provided n is finite and its branchwise certified error is bounded by the same epsilon. Conditional on that record, (7) has the SAME P_infty for all n. Summing the unnormalized classical branches preserves the guarantee. The count itself may be public. This statement relies on stationary native operations: an external source aging with wall-clock time would need time in the physical model.

If the identity of C, its parameters, or the action alphabet is selected from calibration, the common-limit conclusion does NOT follow. That would restore the source's already-corrected selection problem.

## 5. Calibration and actual cost

The theorem needs a genuine certificate or construction warrant for (2), a fixed L, and the actual operation library. It does not manufacture that certificate from visible fitting. A simultaneous interval certificate that establishes at least one member of a PREDECLARED pool contracts can be used without revealing or physically selecting which member; execute the same cover on every successful history.

The raw operational-quotient source's column-sum bound is in a coordinate norm. It must not simply be substituted for c in (2). A complete norm comparison is needed. For example, if a finite physical test core H and its inverse are known with valid intervals, each operator-valued raw test is bounded by ||X||_op. Hence a coordinate map Pi formed from r such tests satisfies

    ||Pi(X)||_Sigma <= r ||H^-1||_(1->1) ||X||_op.

If the source's trace-zero coordinate evolution obeys
||C_R^k Pi(X)||_Sigma <=2 c_0^k ||Pi(X)||_Sigma
and the signed physical-prefix lift has norm at most one, then

    ||Phi_R^k(X)||_op
      <=2 r ||H^-1||_(1->1) c_0^k ||X||_op.               (8)

Thus a sufficiently long repeated R supplies (2). The actual core, its complete validity, conditioning, all shifted joint tables, and independent acquisition starts remain paid. Equation (8) is a conditional transfer of supplied finite-core properties, not a new reset-free core learner. A cover length based on this amplification must be fixed before the record from which unconditional decoupling is sought, or its limiting-configuration dependence must be kept.

To target epsilon>0, use c=0 and one block, or c in (0,1) and the smallest n with c^n<=epsilon. The total native calls are n N_cover. Each letter's actual ancilla preparation, action duration, discarded output/record handling and control precision is charged. The deterministic schedule uses no fresh selection entropy; this does not make ancilla initialization or disposal thermodynamically free.

If each implemented complete letter deviates from its ideal by half diamond norm at most delta_a on all relevant input/reference states, a conventional whole-protocol hybrid gives additional error at most n sum_(a in C) delta_a. A hardware error certificate in a weaker marginal norm is insufficient. A direct whole-preparation complete error may be used instead. Confidence failure is added once; the resulting high-probability reset guarantee is not an exact iid-start assertion.

The target P_infty is NEW. The operation does not prepare the original rho or an arbitrary specified Gibbs/payload state without a separate target-matching argument.

## 6. A dimension-two quantitative boundary

Neither finite hidden dimension nor existence of some exact reset word supplies a uniform useful L or c.

Let A be qubit dephasing in the Z basis. Let B_n be unitary rotation by Bloch angle phi_n=pi/(2n) about Y. Then

    A B_n^n A

is the completely depolarizing channel: the first A keeps only the Z component, B_n^n rotates it into X, and the final A removes it. Thus each member of this two-channel, two-dimensional family possesses an exact reset word.

At phi=0, every word in A and B_0 leaves |0><0| and |1><1| unchanged. The half diamond distance between B_n and identity is sin(phi_n/2)<=phi_n/2. For ANY fixed word containing at most N native calls, the ordinary channel hybrid bounds each output's trace-distance displacement from the phi=0 model by N phi_n/2. Therefore the two initial pole states remain separated after that word by at least

    1 - N phi_n = 1 - pi N/(2n).                         (9)

For every proposed finite N and epsilon<1, choose n>pi N/[2(1-epsilon)]. No word of length at most N contracts those two states to separation epsilon, although a later exact reset exists. Randomness or a public schedule cannot repair the missing scale without paying additional calls or acquiring information about the small rotation. An adaptive quantum experiment with a bounded number of B calls has the analogous N-times single-call hybrid bound; this is an information restriction, not a device-noise claim.

The alphabet here is exactly the two supplied native channels; an additional direct qubit replacement operation would change the question. Both pole states are reachable from |0> by native rotations, so this is not an unreachable-state artifact.

This ordinary proof is self-contained. Current primary work by Lee, Lee and Kjos-Hanssen (arXiv:2609.40154) also studies unbounded exact synchronizing-word length in fixed qubit dimension. Only its official search abstract was retrieved; this note does not rely on its uninspected full proof. The quantitative finite-call approximate obstruction (9) is supplied above.

## 7. Cold-start obstruction remains

An unknown contraction coefficient cannot generally be acquired from one uncontrolled realization without a structural exploration/preparation premise. As an elementary extreme, a hidden static Bernoulli bit is repeatedly read without alteration; all later observations repeat the same draw. Arbitrarily long repeated observation does not estimate its original mixture weight as independent trials would. This example lacks the contraction promise and therefore does not refute the theorem; it identifies what that promise buys.

More generally, the native two-channel family in Section 6 has reset words but no uniform acquisition or stopping bound over n. Small visible change during a finite pilot cannot certify a uniform reset rate. Finite-rank/core information and explicit confidence intervals can supply a conditional certificate, but they do not retroactively create independent original starts.

The present construction solves selection-independent EXECUTION once a finite contractive-word promise is valid. It does not claim to solve arbitrary cold-start discovery of that promise.

## 8. Conventional comparator and actual addition

Synchronizing words, quantum channel composition, de Bruijn covering sequences, complete-norm hybrids and contraction coupling are established machinery. Primary quantum synchronizing-channel work already constructs deterministic resetting compositions from nonresetting channels. Process-tensor work already makes memory instrument-dependent. Astra's corrected complete-quotient construction already proves fixed-word operational forgetting without physical hidden-state convergence.

The specific additional construction is the PUBLIC SOURCE-INDEPENDENT COVER: it turns an existential finite-word complete contraction contract into a single fixed preparation with a common limiting process, preserving correlations with arbitrary finite old records. This avoids the configuration dependence of data-selected reset targets and the secret-key requirement of cancellation-only marginal randomization. Its exponential native-call cost is explicit. An equally informed conventional controller can adopt exactly this construction; no algorithmic speedup is asserted.

This is useful reusable capital, but it does not currently justify displacing the parent's native-port research. Its central acquisition premise remains substantial, and the strongest standard controller with a known reset word is cheaper. The more consequential unresolved bridge is acquiring a valid complete contraction or source-faithful port influence description without whole-process starts.

