# Static target-bank dressing: a preset entangling-transfer comparator

30 October 2026. New conditional exact-conjugation construction. The parent is separately proving the unconditional B-attractor router; this note does not certify that underlying theorem or a completed physical composition.

## 1. Interface actually needed

Suppose an unconditional protected router transfers an arbitrary joint encoded input in two source blocks A1,A2 into two receiver blocks B1,B2, with a common retained-bath/reference guarantee. Spare receiver state may be arbitrary in the admitted initialization class. The proof must give more than reduced decoded fidelity: on its good subspace, receiver DATA coefficients belong to a fixed correctable operator span E, with all native controller/BUSY/router residuals included. Let the bound on discarded/bad channels be epsilon.

Let U_B be a fixed transversal CNOT from B1 to B2 for identical CSS codes, hence U_B Enc_B = Enc_B U_L. Pair corresponding receiver columns physically. Define the NEW nominal apparatus

    L_gate = Ad_(U_B) L_router Ad_(U_B dagger).

Conjugate every nominal memory, routing, monitor and reset coefficient, not just the swap hopping term. This is an exact physical generator declaration, not an effective-generator approximation. If all four source/receiver DATA factors at each paired column can be jointly addressed, U_B is onsite on that declared enlarged site. Hub/column two-site structure is preserved in that new resource setting. It is not elementary-qubit two-body locality or remote LOCC.

The initial A input is unchanged by U_B. Its action on the arbitrary B spare is absorbed into that arbitrary initialization class. Thus no encoded logical input gate is supplied during initialization. Perturbations transform with the same support and cb norm in the declared paired-site geometry; adjusted per-site constants must be checked for two blocks jointly.

## 2. Why this physically performs the logical gate

For an ideal complete swap router, the dressed transfer maps

    rho_A tensor sigma_B -> sigma'_A tensor U_B rho_B U_B dagger.

For the protected partial-transfer apparatus, work in the router reference frame. On every good coefficient E of the receiver error span, the physical receiver has coefficient

    U_B E Enc_B = (U_B E U_B dagger) Enc_B U_L.

A physical transversal CNOT spreads a Pauli error by at most a factor two in aggregate weight. Reserve twice the required error margin so that the ONE ordinary product-code recovery corrects every U_B E U_B dagger and every cross term, with retained auxiliary/reference coefficients. Then the fixed receiver decoder returns U_L rho U_L dagger on the whole good span. It does not insert U_L into recovery.

Contractivity handles the original bad part, with the same qualification on gentle projections and normalization as the underlying router proof. Mere closeness after the undressed decoder would not be enough: the full common correctable span and enlarged weight margin are load-bearing.

The gate is executed through the dressed physical routing/memory coefficients. It does not require a gate program clock to be started after both receivers are loaded. A finite startup dwell and ongoing paired apparatus may still be required by the router. Physical detachment and standalone quantum output are not implied.

## 3. Consequence for long waits

Independent autonomous protection of each live encoded bank can replace raw physical waiting by protected-storage time. The Erlang waiting example therefore need not destroy DATA if such protection is actually present. For a known bounded maximum wait H_N within the memory theorem's lifetime, use its error bound with H_N and include all bank/controller resources. Unbounded waiting still cannot be replaced by an infinite-lifetime claim.

The static dressed router supplies a plausible fixed entangling transfer without a new warm-start gate trigger. It does not make a generic later consumer able to access or detach a live encoded B, and it does not solve selected command delivery, stale-prefix safety, universal non-Clifford operations, or arbitrary composition.

## 4. Why naïve concatenation cancels the computation

Give each permanent gate-output bank g its own fixed dressing U_g and globally conjugate an identity transfer fabric by G=product_g U_g. On a wire from bank p to bank g, the physical transfer becomes

    Ad_(U_g) transfer Ad_(U_p dagger).

A state U_p psi is transferred to U_g psi, not U_g U_p psi. The preceding gate is removed by the source-side gauge. Therefore a global static gauge on a chain of identity routers remembers only the final frame. It is NOT an autonomous universal computer hidden in notation.

To accumulate a programmed circuit one must physically supply the transition U_g U_p (or an appropriate relative frame for cumulative circuit prefixes). Cumulative prefixes generally cease to be onsite/bounded-depth, while actual relative transitions need their own protected implementation and causal schedule. That is the honest next interface.

## 5. Comparison and present status

Ordinary scheduled encoded CNOT and gate-teleportation already supply the logical operation with suitable controls. The intended new guarantee is a fixed native autonomous transfer-plus-gate under the router's continuous noisy-controller model, with no adaptive gate-start switch. This is a conditional construction/comparator, not a novelty claim, independent review, accepted router corollary, or universal architecture.

The earlier accepted autonomous one-layer gate already proves a different program-clock construction, with all memory terms gauge-conjugated and explicit target native frame. The present proposal is simpler for preset transfers and cannot be used to broaden that receipt.
