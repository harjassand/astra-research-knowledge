# Independent check: finite correction latency plus atomic joint post-error

2026-10-15. Inspected COMPOSED_POST_ERROR_INTERFACE.md and the joint character-instrument and good-map proof in ../../coherent_memory_packet_2026-10-15/bridge/BATH_QUANTUM_AUDIT.md. This is a conditional mathematical verification, not a physical implementation theorem.

## Verdict

The strict composition closes. Its gatewise bath-independent correction premise prevents the noncommuting shared-bath serialization obstruction. The added marked-birth rate and A0 nu/kappa+B0 kappa tau+C0 delta_coh^2 budget are correct. No bath-coupled operation needs to be moved. Finite duration is established for the ideal correction circuit only; the completion post-error remains an atomic assumed primitive.

Final clarification verified and resolved, 2026-10-15 20:24 UTC: Section 3 now defines an explicit input-independent actual-record predicate G(h,chi), sums its selected actual instrument Kraus maps to form the good CP subchannel, and uses auxiliary coupling only to bound its complement uniformly. This closes the audit without broadening the theorem.

Historical clarification requested, 2026-10-15 20:17 UTC (now resolved): **the good CP subchannel must be selected by an input-independent predicate of actual primitive and character records, never by the state-dependent auxiliary Bernoulli coupling**. The coupling serves only to bound that predicate's failure probability uniformly. The revised Section 3 now supplies exactly this distinction.

## Serialization, including joint inputs

Write a clean correction gate as K_(A,a) tensor Id_B, with a its private initialized ancillas. An intervening remote post-error or bad operation may act on B, but its data/private-ancilla support is disjoint from A,a by geometric cleanliness. Hence the two superoperators act on disjoint tensor factors and commute, including on arbitrarily entangled inputs. Bath-only operations commute for the same reason. Gates of overlapping attempts are never moved as clean gates. Clean attempts on intersecting patches have disjoint intervals and retain their order.

Move only these K gates to the corresponding start and discard/reset their private outputs as stipulated. The result is C_i on data, with the joint exterior identity. The post-error T_i remains at s+tau in physical order relative to every other bath-coupled event. Pending prefixes stay as actual bad local gates. The CNOT echo counterexample in the text is valid: V dagger Z_B V=Z_A Z_B, although the isolated V dagger V circuit is identity. Gatewise Id_B excludes exactly that counterexample; a merely bath-independent composite would not.

Any physical control dependence on a private correction record would have to be represented in the joint instrument rather than silently discarding that record. Under the stated discarded/private-record and exact C_i assumptions, it cannot create an extra unmodeled shared resource.

## Character effect and arbitrary preceding faults

The joint character channel is an exact Kraus decomposition after inaccessible independent frames are averaged. Setting D=U-I tensor V gives

sum_(chi nonzero) U_chi dagger U_chi
 = E_G(D dagger D)-E_G(D) dagger E_G(D)
 <= delta_coh^2 I.

Thus the nonzero-character conditional probability is at most p on every normalized current joint state. This remains true after arbitrary bad-gadget channels, conditional physical records, correction outcomes, and initial logical-bath-reference entanglement. The proof uses the full joint effect inequality, not closeness of a reduced memory channel.

Detection completeness and absence of local logical Paulis imply that supported Paulis with one character differ by stabilizers. On any definite-syndrome orbit, each U_chi is a representative patch Pauli times a syndrome-dependent bath coefficient. Zero character has representative identity. It need not be identity on coherent superpositions of syndrome sectors, but that is harmless: arbitrary bad gates have already been expanded algebraically into a sum of individual orbit histories, and the same identity holds termwise. No cross terms are discarded. All bath coefficient products retain chronological order.

## Conditioning and same-parent reference marks

Fix the entire exogenous clock/noise schedule. Geometric cleanliness and completion by T are then deterministic. For every admissible physical causal record, the same effect inequality holds. Conditioning on future schedule increments cannot violate it because those increments are external primitives and never an input-dependent postselection or accessible anticipatory control. Future-generated quantum records must not also be conditioned on when asserting the one-step probability bound.

At each clean completion, let q_j<=p be the conditional probability of a nonzero character given the preceding actual records. Sample its binary indicator with a fresh U_j uniform on [0,1] as 1{U_j<=q_j}; then the reference mark 1{U_j<=p} dominates it. Conditional distributions within the zero/nonzero branch and physical record probabilities can be sampled subsequently, so this construction reproduces the actual record law. For any fixed input state, all U_j are iid conditional on the exogenous schedule. Pad all other parent starts with independent Bernoulli(p) marks. The resulting reference marked-start law is therefore independent Bernoulli marking of the original Poisson streams, even though the coupling to actual character records can depend on the initial state.

The clean-subset completion process is not claimed to be Poisson. Fixed tau makes parent-start order and completion order compatible; no attempted reordering of bath operations is hidden in the marking construction.

## Input-independent good CP map

For an actual complete clock/noise/character record r, define Good(r) by the universal classical support certificate for:

- the scheduled omitted corrections and all allowed bad-gate Pauli supports;
- births at the actual nonzero-character completions;
- the actual primitive noise supports.

Equivalently, one may select all actual records for which every legal expansion history is corrected by the fixed decoder. This is an input-independent property of the support/record data and does not inspect unknown amplitudes, the initial state, or the auxiliary coupling uniforms.

A good reference marked-clock certificate implies Good(r), because every actual character birth is dominated at the same completion time and all other births are already charged. Consequently, for every initial joint input, P(not Good(r)) is at most the common reference failure bound epsilon. This implication is the sole use of the state-dependent coupling.

For each selected actual Kraus record, expanding bad gates and applying character identities leaves a sum of logical identity tensor ordered bath coefficients after the fixed decoder. Thus the good subchannel is Id_L tensor Lambda_g, with Lambda_g CP trace-nonincreasing. It is not a normalized good conditional channel.

The complementary bad CP subchannel H has effect

H*(I)=I_L tensor D, D=I-Lambda_g*(I).

The uniform probability bound gives 0<=D<=epsilon I. Complete Lambda_g using Lambda_b(X)=Tr(DX) sigma for any fixed output bath state sigma. Then Lambda=Lambda_g+Lambda_b is CPTP and

||Gamma-Id_L tensor Lambda||_diamond
 <= ||H||_diamond+||Id_L tensor Lambda_b||_diamond
 =2||D|| <=2 epsilon.

This establishes the stated joint-domain conclusion without treating rare bad characters as an input-independent physical mixture. An initially fixed independent bath preparation gives the ordinary logical channel as a corollary.

## Delayed births, rates, and packet replay

A reference mark attached to parent start s yields a reference birth at s+tau. Do not move that birth to s: moving it across C_i can change the syndrome/support history. For a slab [a,a+Delta], every relevant completion has a parent in [a-tau,a+Delta], a deliberately enlarged interval. Campbell's first moment for independently marked starts gives

P(marked-birth flag) <= N kappa p (Delta+tau)
                    <= N kappa p (Delta+2tau).

Geometry must include randomizers, error support, correction supports and all local ancillas. The bound is before geometric selection, so selection introduces no independence assumption. Marks on pending/conflicting attempts are harmless overcounting and do not describe their actual quantum operations.

Include each independent reference mark in the primitive variable of its parent start. Overlapping slab flags consult the same marked point, never resampled copies. Their windows remain contained in [a-2tau,a+Delta+tau], so the previously verified bounded-degree spacetime graph works. Deterministic-anchor replay copies the marked streams jointly over the whole union of required windows and reconstructs delayed births from the copied parent times. The ancestor witness is unaffected by time overlap of primitive windows because its CA parent edges still decrease layer index and its entire needed primitive region was fixed before copying.

The terminal flag is correctly localized in the new text. The pending classification and therefore the circuit representation depend on the fixed deterministic T. No simultaneous all-T physical history or adaptive stopping-time claim follows.

With x=kappa tau<=1 and Delta=Cb/kappa,

N kappa p (Delta+2tau)=N p(Cb+2x)<=N(Cb+2)p=C0 delta_coh^2.

The other verified terms give A0 nu/kappa+B0 kappa tau. delta_ideal is explicitly slow+fast only. Fix coarse geometry/dependency before choosing b, then choose parameters to fit the remaining marginal budget. For fixed nu,tau the minimum rate-dependent pair is 2 sqrt(A0 B0 nu tau) when its optimizer obeys the additional constraints. The coherent contribution reduces the remaining budget but does not alter that minimization.

## Remaining boundaries

No claim is established for temporally extended post-errors interleaved with shared-bath operations, faulty clean syndrome gates, leaked twirl frames, input-dependent clocks, arbitrary continuous memory-bath coupling, unknown initial ancilla states, or an unbounded retained output record. The atomic post-error and all exact-reset, joint-channel, local-support and full-code decoder assumptions remain substantive.


## Runnable exact-algebra addendum — 2026-10-15 20:24 UTC

The script ../checks/check_composition_algebra.py was executed successfully with SymPy 1.14.0. Its exact output is in ../verification/composition_algebra_results.json. Run it with `python ../checks/check_composition_algebra.py` from this folder. These finite algebraic checks corroborate the displayed counterexample and budget identities; they do not computationally verify the complete memory theorem.

In the basis |memory,bath>=(|00>,|01>,|10>,|11>), the memory-control CNOT V satisfies V dagger V=I, whereas

    V dagger (I tensor Z) V = Z tensor Z.

Incorrectly collapsing the isolated echo to identity would give I tensor Z. On |+> tensor |0>, the physical echo yields |-> tensor |0>, while the incorrect serialization leaves |+> tensor |0>. These output states are orthogonal; their density difference has exact trace norm 2. Thus the obstruction changes the actual channel, rather than merely an irrelevant operator phase. The gatewise Id_B hypothesis excludes its first and last gates.

For positive A,B,nu,tau the script verifies both the stationary point and the global square certificate

    A nu/kappa+B kappa tau-2 sqrt(A B nu tau)
      = (sqrt(A nu/kappa)-sqrt(B kappa tau))^2.

The optimizer is kappa=sqrt(A nu/(B tau)). Adding C delta_coh^2 changes only the minimum value, not the optimizer. If kappa tau<=1 is the sole additional constraint, the optimizer is admissible exactly when A nu tau<=B. Otherwise the constrained minimum occurs at kappa=1/tau and equals A nu tau+B (plus the coherent constant). Other constraints in the theorem must still be checked separately. Zero nu or tau requires direct limiting treatment rather than the positive-symbol optimizer formula.

Finally the exact slack between the conservative composed budget and its unsimplified expression is

    2(1-x) [F y+2NDx+Np],

where x=kappa tau, y=nu/kappa, p=delta_coh^2. It is nonnegative for 0<=x<=1, proving the stated A0, B0 and C0 coefficients simultaneously.
