# A finite actual path earns the good-input negative activation margin

30 October 2026. Separate completion for the frozen full closure candidate. This avoids treating an unspecified repair remainder as nonpositive. Initial-phase-left convention remains in force.

Let K=r^gamma, 0<gamma<1/m, and start on the active section with A_in>K. Let U be the actual complete first-connector A-occupation. First-connector activation has probability kT q U and leaves B=2q-1, r unchanged.

## 1. Almost all activation occupation has a qualified output

Call an activation output qualified if D>0, or if D=0 and A_out>=K/2.

For a positive-D initial state, all activations with D=0 occur after first dormant entrance. Their total occupation is at most C/(1+A_in) times the initial positive episode's occupation, by SEED_PHASE_BUDGET_AND_FAST_RESET.md. Thus unqualified activation mass is at most C K^-1 U.

For a dormant initial state, activations before the first fast seed have A_out=A_in+m-1>K and are qualified. Conditional on a first seed, its A output is A_in-1 or A_in-2>K-2 and D>0. Apply the same later-dormant occupation bound there; its unqualified activation mass is again at most C K^-1 times the occupation after that seed, hence at most C K^-1 U overall.

Therefore qualified activation mass is at least `(kT q-C/K)U`.

## 2. Prescribed finite continuation after a qualified activation

From B=2q-1, prescribe a first connector clearing. It moves B to q-1 and lowers r by EXACTLY h. Then, for low B=q-1,q-2,...,2, prescribe a low activation followed by a connector clearing. Each such pair decreases B by one and is r-neutral. Finally at B=1 prescribe low activation, which enters the active section B=q and is r-neutral. There are at most q-1 clearings and q-1 low activations. No immigration is used. The terminal residual is exactly r-h.

Fast reactions, including seeds and dormant returns, are allowed inside each high phase. The prescription refers to the first ACTUAL connector event of that local phase, not to suppression of all fast reactions.

## 3. Uniform success probability

Keep a reserve floor of order K, allowing a fixed q-dependent margin. Whenever a high phase starts with positive D, the full first-connector estimates give competing-birth probability O(r^-1/2) and clearing-output probability `P(A_out<K/4)<=C K^m/r`. Its total N remains large throughout this bounded path, since each clearing changes N by only m.

Whenever a high phase starts dormant with A of order K or larger, a seed/clearing event precedes a connector birth with probability `1-O(K^(1-m))`. A direct clearing changes A by m; a following low activation/clearing pair has net A change -1. Across the bounded number of direct dormant pairs these losses are O(qm), not an unbounded erosion. A fast seed loses at most two A and creates positive D; the preceding positive-D estimate then applies. Require every positive-D clearing output to have A>=K/4. For sufficiently large K, all subsequent low inputs retain A>=K/8, even after the bounded direct-dormant losses.

At each such low input, immigration-before-activation probability is at most C/K. Thus the probability of completing the prescribed path, conditional on a qualified activation output, is at least

`1-C[K^-1 + K^(1-m) + r^-1/2 + K^m/r] = 1-o(1)`.

For a qualified initial dormant activation output A_out>=K/2, the initial direct clearing also leaves A of order K. For a qualified positive-D output no A lower bound is assumed; its first clearing's actual output law supplies the reserve. No stationary composition or independently sampled output is used.

The path hits no earlier section return: its high phases run from low b>=2 to b+q-1>=q+1, then clear to b-1; only the final low activation from b=1 returns to q. It stays active whenever it is in the high processor and respects the initial-phase-left flag.

## 4. Combine a genuine negative event with the graded positive source

On this actual path, w_next=exp(-theta h)w. Its probability is at least `(kT q-o(1))U`. Hence its negative contribution has magnitude at least c_theta U w for all sufficiently large r,K.

The explicit positive-part bound from ACTIVATION_GRADED_SOURCE_COMPLETION.md is `E[(w_next-w)_+]<=C_theta w T` for the entire cycle, including failed prescribed paths. Therefore

`P w-w <= -c_theta U w + C_theta T w`.

This does NOT declare all failed activation paths nonpositive and does not estimate their contribution by U times an uncontrolled o(1). The paid positive-part compensator and the explicit negative event are disjoint parts of the expectation. With T/U<=C/(1+A_in), the good-input drift is strictly negative.

This completes the negative-credit argument at the synthesis level; it awaits the whole-proof verdict and makes no independent global recurrence claim.
