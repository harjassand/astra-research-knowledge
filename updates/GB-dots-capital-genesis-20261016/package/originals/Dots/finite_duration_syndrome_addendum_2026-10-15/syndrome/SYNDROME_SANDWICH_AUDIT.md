# Independent audit: actual syndrome-sandwich alternative

Date: 2026-10-15.

## Verdict

PASS under the stated ideal-measurement, completed-correction, fixed-patch, local-detection/no-local-logical, and uniform conditional joint-unitary assumptions. The construction supplies genuine mismatch labels with the required all-input conditional effect bound, and preserves the encoded Pauli-history structure needed by the separate same-attempt marked-clock theorem. No private random frame is required. This is a separate operational tradeoff and does not modify the frozen twirl/bath packet.

Reviewed: SYNDROME_SANDWICH_ALTERNATIVE.md and ../checks/check_syndrome_sandwich_exact.py. The exact script was rerun successfully. Supplemental exact checks also verified unitarity, the stated operator-norm distance, and the positive difference between its norm bound and actual mismatch probability.

## 1. Completeness and label-dependent errors

Let R_s be the nonzero joint spectral projectors of the actually measured commuting stabilizer checks, and K_j=Q_j Pi_j the completed correction Kraus operators. Since the Pi_j are stabilizer functions, [Pi_j,R_s]=0. Pauli conjugation maps a feasible measured sector to a feasible sector with the prescribed syndrome flip. Hence L_sj=Q_j Pi_j R_s has range in R_s', even when the correction support extends outside the measured checks.

For each genuine premeasurement/correction record s,j, the actual U_sj is a specified unitary on A tensor B. Its dependence on earlier genuine records does not spoil completeness:

sum_t B_sjt† B_sjt = L_sj† U_sj† U_sj L_sj = L_sj† L_sj,

and summing s,j gives identity. Tensor factors on B are implicit. Thus the summed instrument is CPTP on the full joint physical input space. Outcomes can be retained in orthogonal classical registers or used for classical control; summing over them is not postselection. Infeasible zero branches are simply omitted.

A single unconditional U formula must not be used when U depends on s,j. The explicit instrument, which the construction states, is the correct map. Dependence on the yet-unobserved final outcome t is not allowed; genuine later feedback is allowed subject to the same model restrictions at subsequent proposals.

## 2. All-input and conditioned mismatch effects

After conditioning on any feasible s,j, the normalized joint state is supported in P=R_s' tensor I_B. The bath-only comparison unitary I tensor V_sj preserves this subspace. Set D=U_sj-I tensor V_sj. Then

(I-P)U_sj P=(I-P)D P,

so

P U_sj†(I-P)U_sj P=P D†(I-P)D P <= delta² P.

This operator inequality holds with any untouched reference, on every conditioned state, and without assuming an encoded input. It is exactly the probability of a postmeasurement label differing from the predicted label. Both actual outcome conditioning and arbitrary initial bath correlations are covered. The required norm bound is pointwise for every admissible record, not an ensemble calibration bound.

Sandwiching by L_sj and summing gives

sum_(s,j,t != s') B_sjt†B_sjt <= delta² sum_sj L_sj†L_sj=delta² I.

The choice of bath-only V may vary by s,j or earlier genuine history; it cancels sector leakage branch by branch. Local detectability and no-local-logical assumptions are not needed for this probability estimate, but are essential for interpreting a no-mismatch outcome as harmless on an encoded Pauli orbit.

## 3. Orbit interpretation and no hidden refinement

A Pauli supported in A changes the measured syndrome by its G character. Therefore R_t U_sj R_s' selects precisely the character chi=t xor s'. If two supported Paulis have that character, their product centralizes all checks detected by G. Detection completeness and no local logical operators make that product a code stabilizer, modulo phase. Each selected character block can consequently be written P_chi times a polynomial in patch-supported stabilizers with bath-operator coefficients.

On the full-code orbit EV, those stabilizers are scalar independently of the logical vector. The block therefore acts as P_chi EV tensor A_chi,E. This is a linear-map identity, so it retains logical-bath-reference entanglement. Every premeasurement projector, correction projector, and postmeasurement projector either kills the corresponding orbit or preserves it before the stipulated Pauli operation.

For t=s', P_0 can be identity: the orbit is unchanged, although the bath undergoes a possibly syndrome-dependent filter. For t != s', one bounded-patch Pauli representative is added after the correction. No claim of a full-input ideal-channel CP minorant follows, and no such claim is needed. Measuring G need not resolve every stabilizer appearing in the polynomial, because the encoded-history argument uses definite full-syndrome orbits.

## 4. Ideal trajectories and operational cost

With bath-only post-error, the reduced memory channel is C D_G, where D_G is the actual premeasurement dephasing. The final measured label is the predicted label with certainty. This reduced-memory statement remains true if the bath-only unitary depends on s,j, but the joint map need not factor as C D_G tensor one common bath channel.

D_G fixes every definite full-syndrome orbit density, including logical-reference operators. Thus the ideal Pauli correction transitions are unchanged. General syndrome coherences are dephased, so the full-input channel is genuinely modified.

For a single label-independent U, D_G Ad_U C D_G=T_U C D_G is also valid: C maps G-block-diagonal inputs to G-block-diagonal outputs, and dephasing the output removes the cross-character terms. This is an algebraic comparison of the actually measured channel, not a requirement to implement random frames.

The added measurements and truthful records are substantive ideal operations. Their entire check-support neighborhood must be bounded, as assumed. Measurement circuitry faults, wrong outcomes, ancilla reset faults, error during measurement latency, and overlapping finite-duration gadgets are not covered by treating the ideal measurements as support-free. The note explicitly states these costs and does not silently claim a physical implementation theorem.

## 5. Same-attempt corollary

The quantum instrument supplies exactly the interfaces required by the separately verified same-attempt classical module:

- every exogenous ideal correction clock still fires at its original rate;
- pre/post measurements do not add ideal Pauli support;
- the actual mismatch has conditional probability at most delta² for every current joint state and admissible past record;
- a mismatch adds bounded support after that same correction;
- a matched outcome adds no Pauli support.

Averaging over the within-slot premeasurement and correction outcomes preserves the same conditional probability upper bound. Genuine labels may affect later U or finite controller records, provided clocks remain exogenous/nonanticipating, patch enclosures remain fixed, and the norm bound remains uniform. Arbitrary record-driven memory operations outside the specified correction/error instruments do not follow from this allowance.

The existing marked-clock comparison can therefore be applied under its own monotone-certificate hypotheses. It preserves the correlation between a correction and its possible same-attempt birth; it must not be replaced by the independent thinned-stream argument. No correction-rate reduction is introduced in this route.

The common-decoder good-record factorization and TNI bath-map completion then give the same quantum error bound as the marked-proposal theorem, conditional on all its other classical/geometric hypotheses. Good records form a CP trace-nonincreasing map, never an automatically normalized CPTP map. The record-selection rule and resulting maps are fixed independently of the unknown input state.

Finite bath input/output dimensions remain the audited setting. Genuine classical histories can be indexed and summed/discarded without changing that setting. If all unbounded histories are retained as a quantum output register, that is an additional dimension extension, not established here.

## 6. Exact check results

The supplied script passes exact symbolic Kraus equality, completeness, and the mismatch effect for the controlled-rotation example. Independently checked:

- U†U=I;
- with D=U-I, D†D=(4/101) I_A tensor |1><1|_B;
- therefore ||U-I||²=4/101;
- the bad effect is I_A tensor diag(0,400/10201);
- the bound exceeds the nonzero mismatch eigenvalue by exactly 4/10201.

The example's good outcome is a bath filter. It illustrates the instrument/TNI framework, not an independent bath-only CPTP mixture. The general proof, rather than this single example, establishes label-dependent-U completeness and the all-input effect bound.

No counterexample was found under the stated hypotheses. No general continuous-Hamiltonian noise, imperfect-measurement, hardware feasibility, or historical-novelty claim is certified.
