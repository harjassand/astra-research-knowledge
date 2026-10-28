# Independent receipt: physical quadratic maximum-episode-length boundary

28 October 2026. Reviewer: `producer-workspace/review_boundary_residual_simulator`.

**ACCEPT at the stated mathematical and native-interface scope.** The explicit two-shift family has identical full classical acquisition laws for every episode of length at most `r-2`, but a constant binary-law separation at length `r-1=d²-d`. This remains true with strictly positive Choi matrices for every native branch, with the explicitly shrinking margins. No unresolved load-bearing proof obligation remains. This is neither a novelty certificate nor a sample/computation lower bound.

This receipt binds `PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH.md`, SHA256 **`fb24c0a5e0e2033276c823363f52dbfa0e514790835a18cf4f13698fee81665f`**. I read the complete final source, checked the originally assigned Jordan-state version, and reviewed both state simplifications. Only the final two-shift source receives this receipt. The preserved Jordan, explicit-diagonal and tiny-signal predecessors do not inherit acceptance. The normalized residual, raw-core and short-word-modulus sources/receipts were not edited; their existing manifests were reverified.

## Finite-field and harmonic identities

The Singer construction works for every prime power, including characteristic three. An elementary noncircular check of the trace premise is that `x+x^q+x^(q²)` is a nonzero polynomial of degree `q²<q³`, so it cannot vanish on the entire field. Its values lie in `F_q`; as a nonzero `F_q`-linear functional it has a two-dimensional kernel. For nonzero `a`, multiplication by `a` is bijective, hence `Tr(ax)` is not identically zero. If `Tr(ux)` were a scalar multiple of `Tr(x)`, this fact would force `u` into `F_q`. Thus distinct quotient classes give independent functionals and a one-dimensional kernel intersection.

The trace-zero condition is well-defined on projective multiplicative classes: multiplying by an element of `F_q*` only scales the trace. There are `q+1` zero-trace projective points, and each nonidentity cyclic translation meets this set in exactly one point. This proves the ordered-difference multiplicity, not merely a cardinality bound.

Writing `d=q+1`, `r=q²+q+1`, the resulting squared orbit overlap is

    |<s|U^t|s>|² = [d-1+r 1_{r divides t}]/d².

The proof sums all nonzero residues once. It does not assume prime `r`, distinct values of their powers for a particular `t`, or favorable numerical conditioning. This is a finite exact algebraic construction; searching for irreducible polynomials and primitive elements is computation, not a supplied oracle.

## Physicality, exact probabilities and constants

Both states `rho_j=I/(2d)+|U^j s><U^j s|/2` have eigenvalues `(d+1)/(2d)` and `1/(2d)` with multiplicity `d-1`. The common effect `E=I/2+|s><s|/4` has eigenvalues `3/4` and `1/2`. Consequently both measure-and-reset branches are CP with Choi floor at least `1/(4d)`, their sum is TP, and both outcomes reset exactly to `tau=I/d`.

For the forward channel, the unnormalized Choi matrix is `alpha |U>><<U|+(beta/d)I`, with `beta=1/(2r)` and `alpha=1-beta`. Its floor is `1/(2rd)` and its partial trace is exactly identity. Setting `alpha=1` gives the separate unitary boundary version. Depolarization acts as multiplication by `alpha` on the traceless unitary orbit because `tau` is invariant.

The independently derived first-test probability is

    p_j(k)=1/2+1/(4d)+alpha^k[r 1_{r divides(k+j)}-1]/(8d²).

Thus the first differing test occurs after `k=r-2` forward calls, not `r-1`: world 2 returns to the peak while world 1 does not. Including the test call, the distinguishing word has length `r-1`; all words of length at most `r-2` agree. After any test, the correct probability of a later outcome 1 is `1/2+1/(4d)`, not one half. The final source and both diagnostics use these revised indices and baseline consistently.

The binary TV is the single event-probability difference, with no extra factor of two:

    v = alpha^(r-2) r/(8d²).

Here `r/d²>=3/4`, and Bernoulli's inequality gives `alpha^(r-2)>1/2`. Therefore the unitary and interior separations are at least `3/32` and `3/64`, respectively. The corresponding worst-world expected prediction errors are at least `3/64` and `3/128` by the triangle inequality. Full Choi rank does not grant a uniform mixing assumption: the forward margin is `Theta(d^-3)`.

## Entire records, stopping and resource scope

Before the first test, every forward output is deterministic. An early first test has the same binary law in both worlds, and afterward the physical memory is identical. This proves equality of every whole word and every bounded classical feedback record, including early stopping and private randomization. It is stronger than a final-marginal cancellation.

Conditioning on the preceding acquisition record proves that any adaptively selected next short episode has the same law. Induction gives equality for every finite number of whole-process restarts; equality of cylinder laws also covers an almost-surely finite stopping rule. Postselection does not help: selected events have equal joint probabilities. All attempted starts remain resources. The whole-process restart restores the world's unknown `rho_j`; native test/reset restores the known common `tau`. Confusing these two operations would invalidate the interface.

The lower bound persists even when both candidate descriptions are supplied. It concerns a strict maximum episode length. It does not cover occasional longer episodes, coherent access, arbitrary final readout, a flag for the depolarizing mixture, or free hidden-memory controls. In particular, an extra `U†` action followed by the test exposes the two phase shifts immediately. Matrix knowledge does not provide this action through the declared black box.

A pre-call clock leaves every abort record equal. The exact clocked target TV is `gamma^(r-1)v`; there is no dimension-uniform constant-risk consequence for fixed positive abort probability. A clock with abort probability of order `1/r` keeps constant survival while paying expected duration of order `r`.

For supplied `D_max>=3`, choosing the largest power of two `q<=D_max-1` gives `d=q+1<=D_max` and `r-1=q²+q>(D_max-1)²/4`. The family already belongs to the dimension-bounded class. No padding, spare hidden state or promise of exact dimension is used. This establishes the quadratic order comparison with the received `O(d²)` short-experiment upper bound, not equality of constants or sample/computation optimality.

## Independent evidence

The final author script was replayed in `producer-workspace/singer_author_replay_final`; its JSON was byte-identical. Its floating-point matrix replay is supplementary, not the proof of PSD or exact cancellation.

The separately written `physical_quadratic_length_independent_check.py` uses independent integer-encoded finite-field arithmetic, exact polynomial remainders and rational probabilities, with no floating point. For the author's six cases it reads only proposed field/primitive certificates and verifies them independently. It adds independently searched `q=9` and `q=16`, giving **eight prime powers: 2, 3, 4, 5, 7, 8, 9, 16**. Checks include irreducibility, primitive order, all nonzero field powers, trace image and kernel size, every projective kernel intersection, ordered differences, every cyclotomic overlap, state/effect spectra, CP margins and exact target probabilities. Characteristic-three cases explicitly include `Tr(1)=0`; composite periods include 21, 57, 91 and 273.

For `q=2`, independent exact record calculations cover:

- 2,186 words through the first distinguishing length across both channel variants: 728 short equalities and exactly four differing target-branch words;
- 24 full-record comparisons, including adaptation of a second independently reset episode to the entire first record;
- six clocked target laws with exact survival-weighted TV;
- four exact rational Hankel-rank checks, one for each world/channel variant.

The dimension-bound selection was additionally checked for all 1,998 integers `D_max=3,...,2000`. The general results rest on the reviewed proof, not extrapolation from these finite checks. Source calls, episode starts, RNG calls and hardware executions are all zero.

A useful additional reviewer observation is that the two worlds have the same exact observable rank `r`, so rank asymmetry is not the source of hardness. Their first-test sequence has one constant mode and `r-1` distinct modes `alpha zeta^ell`, each with a nonzero coefficient. The resulting scalar Hankel rank is `r`. Conversely, the physical reachable space is contained in the `r`-dimensional span of `tau` and all off-diagonal matrix units. This observation is not needed for the main lower bound; the small exact Hankel checks support its direct algebraic proof.

## Prior-art adjudication and final boundary

I directly read [Mereghetti–Palano (2002), Section 2 and Theorem 2.3](https://cdn.sciengine.com/doi/pdfView/72767B2A6A314F249B84DADD1A3E1A4B): Fourier coefficients, difference-cover phases and positive-operator decompositions already produce periodic quantum events with `O(sqrt(period))` states. The [Bertoni–Mereghetti–Palano (2003) primary abstract](https://doi.org/10.1142/S0129054103002060) explicitly identifies the projective `q²+q+1` construction for quantum automata. Its full text was not obtained. These are close antecedents, not generic background; the final source now credits them. No novelty of the harmonic quantum connection, or of the present wrapper, is certified.

The [Li–Qiu Theorem 5](https://arxiv.org/pdf/quant-ph/0604085) upper bound and Singer construction remain established imports. This receipt accepts a concrete physical full-record, constant-signal example under its exact native interface. It does not reinterpret the governing S7 signed-quotient theorem or its norm adjudication, change earlier residual guarantees, or turn mathematical existence into practical implementation or experimental evidence. **No blocking correction is required for source hash `fb24c0a5…`.**
