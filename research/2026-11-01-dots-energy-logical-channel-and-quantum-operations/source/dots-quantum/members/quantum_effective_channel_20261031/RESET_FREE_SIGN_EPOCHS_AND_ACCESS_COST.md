# Reset-free private-sign epochs: complete logical composition and real access costs

Status: candidate receiving/consequence note. The sign-pair theorem is received from PRIVATE_SIGN_PAIR_REDUCTION_CANDIDATE.md, SHA299bfbc80c35aed153b4c0ea2ebe1c8ea59dc4a0c289d4335b58f1669863f3c6, independently reviewed separately. This note does not claim randomness, twirling, adiabatic elimination or quadratic cancellation as new. It constructs a paid repeated protocol and identifies its calibration and conventional-comparator boundaries.

## 1. Received one-epoch contract

The known native source has an acquired pure-dark return certificate and source resolvent norm bound ell. The centered Hermitian interaction K has an acquired upper bound b, d>=||[H0,K]||, and the SAME source generator G and system H0 are used for both signs. Let

    C1=2d ell+16b^3 ell^2,
    C2=8bd ell^2+16b^4 ell^3.

The physical operation must implement sqrt(lambda)K and -sqrt(lambda)K while leaving G,H0 unchanged, or an actually equivalent conjugation protocol. A symbolic minus or a norm promise is not physical sign access.

For one duration t without internal user controls, choose a fresh private uniform sign and keep it fixed throughout that epoch. Discard the sign from the output. The accepted theorem bounds the complete reduced system/reference channel, UNIFORMLY for every joint source/system/reference initial state, by

    delta(t)<=A(t)/lambda+B(t)/lambda^(3/2),
    A(t)=A0+A1*t+C1^2*t^2,
    A0=12b^2 ell^2,
    A1=C2+6b ell C1,
    B(t)=C1*t*(8b^2 ell^2+C2*t).

The comparator is exp(t L_eff), with the same acquired effective CP jump stack. No source reset, stationary initial state, final source output or private-sign disclosure is in this contract.

## 2. Why fresh epochs compose without resetting memory

Partition the physical run into N epochs, placing a boundary at every prescribed system-only instrument. Choose each sign independently of the entire joint state and earlier records. The previous source and any private old signs may remain arbitrarily correlated with system/reference. Old private sign/controller registers must be idle or traced after their epoch and cease controlling later hardware; merely hiding a register that still changes later dynamics is not sufficient. They are NOT replaced by a fresh bath. Apply the one-epoch theorem to this actual joint input: its reduced output differs by at most delta(t_j) from the effective channel acting on the actual input marginal.

Compare that marginal to the ideal effective marginal from preceding epochs. Contractivity of the effective CPTP channel and of each record-retaining user instrument gives the induction

    logical_error_after_j<=logical_error_before_j+delta(t_j).

This is a reduced-channel induction, not a hybrid that assumes a joint-source approximation or inserts fictitious source resets. Uniformity with an arbitrary reference covers retained past records, and the fresh sign is independent even when the source remembers all earlier signs. Thus the total error is at most min(2,sum_j delta(t_j)). Exact prescribed system-only instruments at boundaries add no model-reduction defect. Their actual implementation and outcome-record processing costs remain paid.

Numerical/control errors can be added if they obey their own uniform logical or joint-channel bounds. A previous implementation error may leave a different source state: the next epoch still admits it. This does not license changing the source generator or leaking the next private sign; those would violate the next epoch's input contract.

## 3. A fully specified linear-time schedule

For b>0 use a supplied rational upper bound for ell and form the same conservative C1,C2 from that bound. Set the maximum epoch duration

    tau=b*ell/C1.

C1 is positive under this b>0 upper-bound convention. For each positive prescribed-control interval of length Delta, use exactly ceil(Delta/tau) equal pieces, each of duration at most tau. This minimal-ceiling schedule, rather than arbitrary further subdivision, is binding for the following call-count bound. If there are p controls and total time T, the number satisfies

    N<=T/tau+p+1,
    sum t_j^2<=tau*T.

Hence

    sum A(t_j)<=12b^2 ell^2(p+1)+T*(C2+19b ell C1),
    sum B(t_j)<=T*(8b^2 ell^2 C1+b ell C2).

The complete retained logical/reference/record error is therefore bounded by

    min(2,
      [12b^2 ell^2(p+1)+T(C2+19b ell C1)]/lambda
       +T(8b^2 ell^2 C1+b ell C2)/lambda^(3/2)).

This is linear in total duration and prescribed-control count, rather than the global-sign T-squared bound. The sign-update rate C1/(b ell)=2d/b+16b^2 ell is independent of lambda. It depends on the unwanted coupling and its system commutator, not automatically on the norm of the entire system Hamiltonian. Its numerical size can still be large, and the actual system/source/control operations are not free.

A dyadic duration below tau can be used: choose it in[tau/2,tau], paid by certified rational arithmetic, and replace19 by31 in the displayed A coefficient (the term A0/tau can double). Zero-duration intervals need no epoch. If K is certified zero, no sign protocol is needed and the ordinary H0 task is exact. A merely small nonzero upper bound is not treated as an exact zero oracle.

Bounded schedule jitter does not inherently require lambda-scale timestamp precision: if actual epoch lengths remain within the certified maximum and total physical time is T, the proof uses those actual lengths and the same effective semigroup target. This does NOT price a finite-duration physical sign-switch pulse. Evolution during a pulse must be part of an acquired operation/error model; it cannot be deleted from physical time merely by calling it a boundary.

## 4. Exact ordinary system twirling can supply the sign

Suppose an acquired system involution U obeys U dagger K U=-K and U dagger H0 U=H0. Since G acts only on the source, the negative-sign epoch channel equals Ad_U composed with the positive-sign joint channel composed with Ad_U. Thus a fair bit and at most two boundary U gates realize the epoch mixture, without measuring P, splitting source jumps, changing G, or directly reversing a native interaction amplitude. Adjacent boundary gates may be combined when appropriate; the conservative count is2N applications of U and N private bits.

The identities must hold for the ACTUAL implemented interaction/H0. They are not inferred merely from a nominal model. User controls are put between epochs, so no conjugation of internal user controls is needed. In a global-sign protocol with controls inside a branch, those controls would instead need consistent conjugation. Both descriptions are ordinary randomized compiling/twirling.

If an implemented boundary unitary differs from U by operator norm at most zeta, its channel differs by at most2zeta. Two gates per negative epoch therefore cost at most4zeta in diamond norm, independent of lambda. Across N epochs allocate4N*zeta to the gate budget. This compares actual acquired boundary OPERATIONS; their certification must include any simultaneous uncontrolled interaction during a finite pulse. Calling a physical phase change a cost-free virtual frame update is not justified without an actual frame/control derivation.

A biased sign coin with probability1/2+a changes an epoch channel by at most2|a|, so2 sum |a_j| is a safe total coin-error allocation. Exact algorithmic fair bits can instead be generated directly; their count and retained/discarded registers are paid. Sign outcomes are not public and must not condition an otherwise different protocol unless that protocol has a separate theorem.

This boundary-gate implementation is materially better than calibrating two unrelated analog Hamiltonians: its approximate-gate error does not receive an automatic sqrt(lambda) multiplier. That is an ordinary channel-composition fact, not a claim that physical gate errors or bandwidth are independent of lambda for every device.

## 5. Sign mismatch and centering cannot be left uncharged

For independently implemented branches K+ and K- that differ from the ideal ±K by operator norm at most delta_K, direct contractive Duhamel gives an epoch error at most2sqrt(lambda)*t*delta_K. Without more structure one needs actual coupling precision of order epsilon/[sqrt(lambda)T]. Source-generator changes between settings similarly require a separate bound and can carry lambda*T. The original theorem does not certify these model mismatches.

The centering issue is real, not just a loose proof. If a common source-independent residual M=mZ is added to both branches, with the rest of the dynamics trivial, the target identity differs from the actual unitary channel by2|sin(sqrt(lambda)*m*T)|. For small angle this forces m=O(epsilon/[sqrt(lambda)T]). If the residual mean reverses with the random sign, the averaged channel is dephasing with identity-channel distance2sin^2(sqrt(lambda)*m*T), forcing m=O(sqrt(epsilon)/[sqrt(lambda)T]) in the small-angle regime. Averaging the mean to zero is therefore NOT equivalent to centering each branch before applying the theorem.

Under a simple bounded-observation statistical calibration model, estimating a previously unknown mean to tolerance a generally costs order1/a^2 samples, with its confidence factors and readout cost. This can reintroduce a rate-dependent acquisition burden. It is not a universal lower bound for every structured known model: exact symmetry/algebraic centering may avoid numerical mean estimation entirely. A known nonzero mean may be included in H0, but its real sqrt(lambda) action and altered commutators remain paid; it is not silently erased.

If mismatches are certified centered, the preceding source-independent mean counterexamples do not apply. More refined response/model-robustness bounds may then avoid the worst sqrt(lambda) estimate. This note does NOT claim the direct Duhamel precision is necessary in that narrower class. Exact involution twirling avoids an independent sign-setting mismatch altogether when its actual algebraic premises hold.

## 6. A nonzero-odd-error example and the strongest conventional task comparison

Use the coherent-output qutrit from ODD_INTERACTION_COLD_CHANNEL_AND_ROUTING.md: jumps (|0>+|2>)<1| and sqrt(2)|0><2| at p1/2, H=Q, and K=|1><0| tensor sigma_minus+(1/2)|2><0| tensor sigma_plus+adjoint, H0=Z/3. U=Z on the system anticommutes with every term in K and commutes H0. The jump output is mixed P/Q, so the cold selection B=0 theorem does not apply. Finite diagnostics exhibit a nonzero inverse-square-root correction before twirling. Nevertheless the sign is supplied EXACTLY by the ordinary two-boundary-Z construction, with no source projector access. The leading target remains standard nonunital generalized amplitude damping.

This is a real nonzero odd-error regime, not an ideal star model already enjoying O(1/lambda). It still does not beat the direct generalized-amplitude-damping ancilla circuit for executing the leading logical channel. An exact small dense full-source solver is also a strong competitor for predicting this tiny apparatus. A failed unpaired sufficient bound is NOT a lower bound on its actual error; numerical Choi brackets remain diagnostics unless separately certified.

For the suggested autonomous-correction setting, a product of physical Z gates flips every conditional-X recovery operator R_a=X_i P_syndrome because the syndrome projectors are diagonal. It can therefore provide the same ordinary parity twirl when the entire actual coupling has that parity and H0 is compatible. But the same information also enables a strong direct recovery-channel implementation. For disjoint syndrome projectors with R_a dagger R_a=P_a and all R_a mapping into the code, sum P_a=Q_code, the exact recovery semigroup has Kraus

    K0=P_code+exp(-t/2)Q_code,
    K_a=sqrt(1-exp(-t))*R_a.

Ordinary coherent syndrome extraction, a partial-jump flag, acquired correction/decoder and uncomputation implement this channel directly; measured-syndrome correction is another comparator when its output task matches. All syndrome/decoder/control costs are paid. Do not assign those resources only to the autonomous architecture or call their acquisition novel. Many ideal reset-star sources already have the odd/output-homogeneous cold selection and gain no asymptotic order from sign mixing.

There is a concrete compatibility obstruction in the odd-length repetition code: U=Z tensor ... tensor Z restricts to logical Z on span{|0...0>,|1...1>}. It therefore reverses a continuous logical-X Hamiltonian. Two boundary U gates around the positive apparatus then implement the negative interaction AND the reversed logical-X drift, not the desired negative-interaction branch with the same H0. The accepted theorem cannot be applied to that operation unchanged. One must acquire compensating H0 sign control, use a compatible drift, or restrict the task to boundary logical controls; each changes the real operation/cost premise. Even when compatible, a product-Z implementation costs up to n physical gates per U (or an actually acquired parallel/frame operation), so the conservative epoch cost is2nN gates rather than2N cost-free symbols. The conventional measured/coherent recovery comparator receives the same syndrome and parity access.

## 7. Resource conclusion and prior scope

The earned protocol uses fresh private signs at a lambda-independent rate, does not reset the retained source, and has a uniform all-input logical composition proof with linear-time inverse-rate error. Its possible benefit is suppressing a finite-rate bias in a FIXED noisy apparatus when exact cheap sign symmetry is genuinely available. It is not a more efficient way to implement a logical channel already supplied in direct Kraus/Lindblad form.

Randomized compilation, antithetic cancellation and positive-mixture improvement are established ordinary methods. Primary examples are Campbell, arXiv:1612.02689 (unitary mixing and quadratic coherent-error suppression), Wallman-Emerson, arXiv:1512.01098, and Winick et al., arXiv:2212.07500. The root comparison note records their actual inspected scopes, including non-Markovian randomization; this note does not assert that a title/abstract excludes prior coverage of this protocol. In particular, the inspected Winick et al. primary text (https://arxiv.org/html/2212.07500v1, Sections III.2–III.4 and Theorem 3) explicitly treats a persistent ancillary environment and warns that leakage of even a twirl-parity bit through gate-dependent noise can defeat suppression. Its local-Pauli formula retains environment-dependent weights; it must not be quoted as a bath-independent logical channel for arbitrary initial correlations. Reset-free memory, privacy and quadratic randomization are therefore not new ingredients by themselves. The specific receiving claim here is a fixed effective NONUNITAL target with explicit microscopic complete-norm rate bounds, followed by the paid sign/calibration interface. No claim that the prior paper excludes this consequence is made.

No novelty, hardware feasibility, universal calibration shortcut, practical advantage over the direct operation, or source-output equivalence is established. If physical sign access, exact centering or compatible controls are unavailable, that is an actual missing operation, not something a theorem about ±K supplies for free.
