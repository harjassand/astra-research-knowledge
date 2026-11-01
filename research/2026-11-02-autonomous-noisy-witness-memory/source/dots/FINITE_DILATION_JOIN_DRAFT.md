# Finite-rate autonomous dilation: proposed whole join

Root composition, 2026-11-01. Pending whole-join receiving. This replaces the ideal conditional dissipative jump by an exact finite-ancilla Hamiltonian/reset model, not by a finite-time approximation. It STILL requires high-body graph-local couplings and Markov reset reservoirs; native few-body hardware is not supplied.

## Construction and counts

Use the specified Tanner-witness system and W of the separately received controller theorem. Retain only strictly downhill conditional-Pauli branches; no-op dephasing branches are unnecessary for its drift. Split each into exact integer drops J_alpha, [W,J_alpha]=-d_alpha J_alpha, 1<=d_alpha<=d_max, with ||J_alpha||<=1. Branch splitting is into disjoint local patterns and does not multiply the number of simultaneously enabled moves.

For every admitted label in the safe system basin,

 W/K <=sum_alpha J_alpha*J_alpha<=4W.

The upper bound follows because there are j compatibility repairs and at most4z mismatch vertices touching a disagreement, per sector. It is an operator bound on diagonal labels, not a classical-state assumption.

Attach a two-level ancilla to EACH channel alpha. Let M_anc<=L0 n, where L0 is a finite, potentially enormous degree/pattern constant. The full qubit count is5n+M_anc, NOT5n. Define

 A_alpha=J_alpha sigma_alpha^+,
 H=g sum_alpha(A_alpha+A_alpha*),
 Q=W+sum_alpha d_alpha n_alpha,
 C=i sum_alpha(A_alpha-A_alpha*),
 V=Q+epsilon C.

Use actual lowering resets gamma sum_alpha D[sigma_alpha^-]. g,gamma are finite positive constants independent of n. There is no external sequence/clock. All native J couplings and reservoir assumptions are explicit physical premises.

## Direct Lyapunov admission

Let c=1/K, C0=4, and C1=2(1+z)j_*² for the actual channel-overlap bound z. Choose epsilon>0 so

 epsilon sqrt(C0)<=1/4,
 epsilon[2gC1+gamma²C0/(4gc)]<=gamma d_min/2.

Then eta=epsilon sqrt(C0)<=1/4,

 (1-eta)Q<=V<=(1+eta)Q, [Q,V]=0,
 Lideal* V<=-c_V Q,
 c_V=min(epsilon g c, gamma d_min/(2d_max))>0.

The independent derivation is in ANCILLA_CURRENT_HYPOCOERCIVE_LIFT.md. This is a full finite-generator statement; no limit g/gamma->0 is taken.

For local V=sum_X v_X with support<=s, incidence<=zeta and ||v_X||<=v_*, let r bound supports of all Hamiltonian and jump/noise terms (including l*l). Put C_loc=2 zeta v_*(r+s). The proposed independently checked commutator estimate gives, for a<=1/(2C_loc),

 F=e^(aV),
 F^-1/2 Lideal*F F^-1/2 <=-a c_V Q+C2 a² n I,
 C2=C_loc²(H0+2R0),

where sum||h_ideal||<=H0 n and sum||l_ideal||²<=R0 n. These counts include ALL reset ancillas; H0,R0 can be enormous constants.

Let the additional local Hamiltonian/bath and additive dissipative-noise budgets be sum||h_noise||<=h n and sum||l_noise||²<=gamma_noise n. The same local series gives a weighted perturbation contribution at most2 C_loc a(h+gamma_noise)n. Every data, witness, and added-ancilla noise source belongs in these sums. Miscalibrated existing jumps need a separate bilinear perturbation bound, not a free positive-noise interpretation.

Choose theta=beta/4, where beta is the Tanner component cutoff density, and choose

 a<=min[1/(2C_loc), c_V theta/(4C2)],
 h+gamma_noise<=c_V theta/(8C_loc).

Both are fixed positive conditions independent of n. Then the reflected actual generator obeys

 Lref*F<=-k n F+2k n exp[a(1+eta)theta n] I,
 k=a c_V theta/2.

## Component and logical interface

Enlarge the previous low-W component by the ancillary computational-basis labels and cut off at Q<beta n. Since W<=Q, every such reachable label lies in the original safe W component. Ideal A_alpha conserve Q and resets lower Q; they preserve the below-cutoff connected component. Its projector P commutes with Q,C,V,F. The activity and local-series bounds therefore survive reflection/compression.

Protected logical information is the original subsystem. Ancilla ground states add only fixed stabilizers; arbitrary ancilla excitation labels carry no new protected logical qubits. Canonical representatives may correct ancilla labels separately. Protected flatness follows from the old low-weight data/witness representatives; ancillary factors cannot create a protected logical action. All local ideal branches and their projectors act trivially on that subsystem within the component.

For local perturbations, let b_Q bound the change in Q of every admitted Pauli component. The SAME two-step boundary correction is required for general dissipators: use Q>=beta n-2b_Q. Because Q commutes with V,

 Pr_ref[boundary]<=C_init exp{-a[(1-eta)(beta n-2b_Q)-(1+eta)theta n]}.

With eta<=1/4, theta=beta/4, the extensive exponent margin is at least7beta/16. The actual/reflected comparison is thus at most

 n(2h+4gamma_noise) T sqrt(C_init)
 * exp[a(1-eta)b_Q]
 * exp[-a((1-eta)beta-(1+eta)theta)n/2],

before any initial-state truncation/readout errors. This proposes exponentially long protection in the exact finite-dilation model, not an O(epsilon T) elimination transfer.

## Vacuum and warm initial ancillas

For encoded system/witness ground input and vacuum ancillas, F has expectation1 and C_init=3 suffices after the Foster estimate. Fixed independent bath/ancilla initialization yields a restricted-code channel statement; correlated input baths require the earlier joint-state qualification.

Independent thermal ancillas have nonzero support ABOVE the cutoff; a small moment does NOT make actual/reflected initial states equal. Suppose their actual probabilities q_alpha satisfy

 sum_alpha log[1-q_alpha+q_alpha exp(a(1+eta)d_alpha)]
 <=a(1+eta)theta n.

With system W=0, Chernoff gives

 p_out=Pr[Q>=beta n]<=exp[-a(1+eta)(beta-theta)n].

All auxiliary patterns below the cutoff are reachable by monotone ancilla flips, hence belong to P. Truncate/renormalize that initial classical mixture, paying trace distance2p_out. For p_out<=1/2 its initial F moment is at most2exp[a(1+eta)theta n], and C_init=4 suffices. This is an explicitly charged small thermal-excitation density, not arbitrary hot preparation. General correlated or erroneous data preparations need their own logical and tail admission.

The explicit ideal terminal consumer is the fixed witness-frame Clifford U† followed by the original efficient Tanner decoder, with the radius shrink in TANNER_IDEAL_READOUT_ADDENDUM.md. It corrects the coherent error span and discards witnesses/ancillas. No noisy hardware decoder or free input encoder is supplied.

## Physical significance and remaining hard gate

If received, the meaningful change is direct rare-event control of a finite Hamiltonian-plus-reset apparatus, including its noisy ancillas. The conditional energy-flow estimate alone would not provide this result; the positive current-corrected exponential potential is essential.

The construction still uses high-body syndrome-conditioned J_alpha in H. Its local ancilla count may be enormous, the code family has no certified useful finite instance, and expander edges are not3D short-range links. The reset reservoir's microscopic finite-capacity realization and synthesis from native few-body interactions remain unearned. This is an abstract finite-rate autonomy advance, not the civilisation-level capability or a practical resource advantage. Those hard gates are being evaluated before further constant refinements.
