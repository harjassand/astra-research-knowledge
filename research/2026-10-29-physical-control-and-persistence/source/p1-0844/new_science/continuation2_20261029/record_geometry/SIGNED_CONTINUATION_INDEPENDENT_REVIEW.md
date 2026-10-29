# Independent internal review: signed continuation and physical terminal control

29 October2026. Reviewer: complementary record-geometry researcher in the same
Astra P1 allocation. This is an actual mathematical review, not external peer
review, formal verification, an apparatus test or historical-priority finding.

Reviewed input SHA256:
`f05c28e6c516510179ef2e68b51ed2b3594e6471d7d7ee15c8e8fe2912d69a15`.
An exact snapshot is preserved as REVIEWED_SIGNED_CONTINUATION_f05c28e6c516.md.
Scope: Sections3--8, calibration/clock interpretation, and Section10's ring
consumer. The exact ring executable was independently rerun in isolation.

## Verdict

ACCEPT the main signed-continuation witness, bounded-time and heralded
obstructions, exposed-clock independence obstruction, and ring construction
at their stated interfaces. No load-bearing counterexample or wrong constant
was found. Three short proof/scope clarifications are recommended below;
they do not change the theorem or its scientific conclusion.

## 1. Holomorphic stopped likelihood

Fix one controller seed and a reference path. The controller's selected mode,
switches, stopping functional and accepted event are functions of that fixed
path/seed, hence do not vary with the complex parameter. On a finite menu,
the integrated rate is a finite sum of holomorphic rates weighted by the
occupation times of the selected state/control pairs. Infinitely many
switches cause no analytic difficulty when the predictable intensity process
is well-defined: each occupation time is bounded by T. The finite reference
jump product is holomorphic too.

The reference process uses positive rho on the UNION of allowed directed
edges. Every physical controlled law on a bounded interval is dominated by
this reference, even when a selected mode disables an edge or is a zero-rate
hold. Reference jumps during such disabled selections simply have likelihood
zero. The likelihood includes the survival correction and all jumps up to the
stopping time, so stopping at a jump is covered by the predictable pre-jump
control. It is not a likelihood for an independently redrawn endpoint model.

The Poisson-dominated jump count and the displayed compact-uniform envelope
are sufficient for dominated Morera/Fubini, including averaging arbitrary
independent controller seeds. No finite bound on the number of actual jumps
or policy switches is needed. Negative witness rates are used only inside
this integrable signed continuation.

Minor proof clarification: Section5.1 states tau<=T only almost surely under
physical laws, whereas the envelope in Section4 is pathwise on reference
paths. Explicitly replace the stopping functional by tau cap T before applying
the lemma. This changes no physical law under the premise and defines a
bounded functional even on disabled-edge reference paths of zero physical
likelihood. For heralding, similarly interrupt at T and mark noncompletion
as failure. This closes the reference-null-path presentation gap.

## 2. Sign and the identity theorem

At the real witness all active nonzero jump factors are negative, while the
survival exponential is positive. Bipartiteness identifies jump parity with
the final physical colour. Thus every nonzero likelihood contribution to an
opposite-colour event has the SAME negative sign; same-colour contributions
have positive sign. Positive physical event probability implies a set of
positive reference measure on which physical likelihood is positive. Strict
nonzero witness rates on the same enabled edges preserve nonzero likelihood
there, proving the required strict sign. There is no cancellation of signs
within either final-colour class.

A holomorphic opposite-event probability constant c>0 on the physical interval
would remain c at the witness, contradicting its nonpositive sign. The
identity theorem also justifies equality on any support with an interior
accumulation point. A finite set or accumulation only at a domain boundary
would not suffice; the draft correctly excludes those shortcuts.

For a heralded event, the function (1-c)F-cE has strictly negative witness
value whenever success has positive physical probability and0<c<1. One need
not assume both witness terms are strict: positive success makes at least
one strict, and both coefficients are nonzero. The deterministic c=1 or c=0
exceptions are genuine and are correctly retained.

## 3. Exposed clocks

If a finite but unbounded stopping rule had endpoint probability c and that
endpoint were independent of its completion time for every h, then truncating
at T and accepting only completed runs would give the forbidden bounded-time
heralded distribution. Some finite T has positive completion probability,
so the argument is valid. Genuine padding that keeps the physical output as
the declared final native state can be included in the stopping/controller
interface. If padding changes the state, the terminal state must be evaluated
after those allowed changes. Reporting a previously remembered bit is outside
the physical-output premise.

The exact proved statement is impossibility of a common nondegenerate endpoint
law that is also clock-independent THROUGHOUT the parameter family. It need
not establish clock dependence at every individual parameter separately.
Avoid reading the phrase 'parameter-dependent output-clock relation' as a
claim that the conditional dependence pattern must vary with h. For example,
choose an independent target bit; stop at0 for the original target and at the
first jump for the opposite target. Then opposite output is exactly the event
{tau>0}, the same deterministic relation for all h, although the joint law and
positive-time clock distribution depend on h. This example respects the no-go.

A stronger statement that the ENTIRE joint(endpoint,clock) law cannot be the
same for all h also follows from the same witness: if it were common, then
P_h(opposite,tau<=T) would be a positive constant for some finite T, directly
contradicting the sign/identity argument. This is a precise alternative wording
if parameter independence of the joint record is the intended claim.

## 4. Source B and endpoint-polynomial scope

For source B the logarithm arguments have positive real part on Re z<4/3.
The smallest zero threshold is mode1's4/3; the four rates are therefore
holomorphic on the claimed connected domain. At h=-4 the endpoint parameters
are(-1/10,-3/10,-3/20,-1/20), so all continued rates are strictly negative.
Physical probabilities lie in[1/20,9/20], giving the stated upper rate
log(10)/(2t0). The binary graph supplies the required common colouring.

The endpoint polynomial proof is valid for programs with at most L calls of
the specified fixed duration, observing their ENDPOINTS. Positive slope gives
highest-coefficient sign(-1)^(d-r), so maximal accepted depths cannot cancel
in either the total opposite event or (1-c)F-cE. The Chebyshev witness at-7/2
is also valid: every p_j there is nonpositive (mode3 is zero), nonflip factors
are positive, hence f(-7/2)<=0. The extremal polynomial argument and
c/T_L(7/2) bound are correct and conservative.

Scope clarification recommended: explicitly say Section7 is ENDPOINT-ONLY,
with the specified duration t0 per call. Its polynomial degree bound is not a
bound for continuous intra-call observation, arbitrary durations or switching.
Those stronger programs are excluded exactly by Sections4--6, but they do not
inherit this finite-degree quantitative estimate merely by counting invocations.

## 5. Calibration and complete retained information

A finite endpoint calibration history with nonzero likelihood has positive
likelihood for every physical h in this strictly positive source. A finite
continuous-path history has positive density relative to a common reference
for all physical h, with the usual almost-everywhere conditional qualification.
Thus an initially supported continuum is not reduced to an exactly known h
by these finite records. Conditional on a fixed complete history, the future
rule is common across the remaining parameter support, so the no-go still
applies to a future row required to ignore H and arbitrary retained old data.

Clarify that D here includes ALL retained calibration/controller state,
including reused random seeds, or that all subsequent randomization is fresh
and independent of H conditional on D. Conditioning only on an outcome summary
can correlate a previously independent seed with H. The proof is restored by
conditioning on the full retained seed/history; the claimed universal
old-information guarantee already requires that complete interface.

The theorem does not rule out a posterior-averaged target, approximate
per-device calibration, or a preparation resource acquired using unbounded
prior time and then discarded from the requested record. A bounded deadline
for the whole operation includes its calibration; an earlier calibration
outside that deadline can be addressed by the conditional-on-complete-D
argument only for the stronger retained-information-independent target.
The draft's distinction between pointwise autonomy and Bayesian prediction
is therefore substantive and correct.

## 6. Ising-ring consumer

With spins2y-1, beta J=(1/4)log(5/3) gives conditional probabilities3/8,1/2,5/8
when the two neighbours sum to0,1,2. Multiplying the required change probability
by9/20 yields exactly27/160,9/40,9/32. Mixing the compiled flip rates3/20 and
3/10 requires B probabilities1/8,1/2,7/8, respectively.

Three bits realize those outer probabilities exactly. Two more bits realize
A's3/4:1/4 raw selection or B's1/2:1/2 selection with one unused bit. All32
five-bit keys are accounted for. The raw-mode counts are respectively
(21,7,2,2), (12,4,8,8), (3,1,14,14). In each case their u-weighted mean is the
required flip probability and their signed-v-weighted mean is exactly zero.
Thus cancellation holds for ALL h, not merely the tested hidden values.
The conditional local kernel is exactly(11/20)I+(9/20)heatbath, without needing
a separately available identity hold. Each call still requires the declared
addressability, neighbour/current reads, isolation of other sites, fresh hidden
selectors, equal duration and fixed controller latency.

I independently reran check_ring() from the root executable. It passes all64
local contexts, all256 detailed-balance pairs and the full16-state stationarity
check. The stationary weights are25/248 for the two aligned states,9/248 for
the two alternating states and15/248 otherwise. The nearest-neighbour spin
correlation is4/31. The rerun receipt is SIGNED_RING_REVIEW_RERUN.json.

Random scan with state-independent selection is reversible for this target.
A deterministic scan preserves the target but its full sweep need not itself
be reversible. Arbitrary feedback-selected sites still have exactly the
corresponding ideal controlled law; they do not automatically retain Gibbs
stationarity. The draft does not require such a stronger assertion. It also
correctly avoids fast-mixing, computational-speedup and hardware claims.

## Review conclusion

The signed continuation changes the obstruction beyond finite-word or
monotonicity arguments and survives continuous observation, feedback and
bounded stopping at its specified physical terminal-state interface. The
proof is a sufficient witness for the explicit analytic family, not a finite-
data certificate of that family and not physical negative-rate access.
The minor explicit-scope edits above would make the governing note harder to
misapply. No revision of the main mathematical conclusion is required.
