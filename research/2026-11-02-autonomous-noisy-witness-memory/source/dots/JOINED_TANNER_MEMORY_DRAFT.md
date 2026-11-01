# Candidate joined theorem: graph-local autonomous subsystem memory

Root composition draft, 2026-11-01. The abstract criterion and controller have separate independent conditional receipts. This file joins their assumptions explicitly; whole-join acceptance is still required. It is a formal bounded-degree interaction-graph result, NOT a useful-cost hardware proposal or a Euclidean-locality result.

## Imported controller facts

For the specified sufficiently-large-fixed-Delta LZ quantum Tanner family, let n be original data qubits, d_n>=delta_code n, and let four witness qubits per data qubit be added. The joint physical system has5n qubits, before microscopic controller apparatus.

The constructor's W=W_X+W_Z is a sum of bounded local functions of commuting joint stabilizer labels: each sector contributes (Delta²+1) times the number of local compatibility violations plus the number of disagreeing witness-copy pairs. It has a finite fixed graph-local channel implementation with

 K=8Delta^4+2Delta²+1,
 Lcool^* exp(aW) <=-kappa(1-exp(-a)) W exp(aW)/K

on every diagonal joint label having a joint Pauli representative of weight below R_n=rho n. rho>0 is the explicit constant in the controller note, further shrunk if needed. This is pointwise, hence an operator inequality for coherent gauge/witness states.

The exact ground subsystem is a depth-two local Clifford transform of the original code tensor auxiliary gauge qubits with copy-agreement constraints. Its protected dressed distance is at least d_n/5. The local conditional projectors can be functions only of joint commuting compatibility/copy syndrome, not raw unprotected logical or gauge data. Count full conditioning support in physical locality and perturbation admission.

Each downhill correction flips at most b_c=2Delta² witness qubits and lowers W by at least1. Its condition uses a larger but fixed bounded support. At a vertex/type, all mutually exclusive truth-table branches form ONE CPTP map Phi_v; use kappa(Phi_v-id). This normalizes total attempt rate per vertex/type rather than assigning an exponential rate to candidate patterns.

## From the algorithmic basin to a flat low-potential component

Shrink rho so R_n<=d_protected/8. Let r(s) be the minimum weight of ANY enlarged-system Pauli producing joint syndrome s from ground. This is an analysis quantity; the controller never computes it. Since a minimum representative exists, the controller drift hypothesis applies whenever r(s)<R_n, regardless of the actual unknown logical state or error history.

If r(s)<=R_n/2 but W(s)<r(s)/b_c, a downhill sequence would have fewer than r(s)/b_c steps, stay within radiusR_n, and end in W=0. Its total correction weight would be less than r(s), contradicting minimum syndrome weight. Thus

 W(s)>=r(s)/b_c  whenever r(s)<=R_n/2.

Let w bound the weight of every Pauli in the admitted perturbation alphabet and every correction, and let

 B_n=beta n, beta=rho/(8b_c).

Take n large enough that w<R_n/4. Along any admitted edge, r changes by at most w. The connected joint-syndrome component S0 containing ground within W<B_n cannot reach r>=R_n/4: the first such vertex still has r<R_n/2 and therefore W>=R_n/(4b_c)>B_n. All labels in S0 consequently have representatives E_s with weight<R_n/4.

For an admitted Pauli T:s->t with both labels in S0, E_t* T E_s preserves the ground subsystem and has weight<R_n/2+w<d_protected. It must therefore be gauge, not protected logical. This proves flat protected-logical transport on the whole component. Functions of joint syndrome act trivially on the decoded logical subsystem. Arbitrary witness coherences are allowed; gauge motion is not mistaken for memory corruption.

This establishes the precise component premise of the abstract quantum criterion without assuming global qLTC soundness or declaring all low-energy configurations correctable.

## Fixed local perturbations and lifetime

Let b bound |Delta W| for admitted Pauli components. Include all data and witness noise in the budgets

 sum_P ||B_P(t)||<=h n,
 sum_J (sum_P |j_(J,P)|)^2<=gamma n.

The first permits arbitrary time-dependent local Hamiltonian couplings P tensor B_P(t) to an environment. The second is the displayed additive local dissipative-noise model. A per-enlarged-qubit rate must be converted to these per-original-n budgets, including the factor5 and any finite-support Pauli-expansion factor. Unknown apparatus not included in the5n system has not magically been admitted.

Choose theta=beta/2 and a>0. Define

 g= kappa theta(1-exp(-a))/K,
 u= 2h sinh(ab/2)+gamma(exp(ab)-1).

Require u<=g/2. These are fixed positive ratio conditions independent of n, although the certified numerical constants may be unusably small. The auxiliary reflected channel on S0 exactly preserves protected logical information. The independently checked two-step boundary comparison gives

 ||rho_actual(T)-rho_ref(T)||_1
 <=sqrt(3) n(2h+4gamma) T exp(ab) exp(-a beta n/4)

for arbitrary encoded logical/reference states and admitted bath states, under the criterion's precise bath initialization qualification. With a fixed independent bath input this yields a restricted-code channel bound; initially correlated baths give the stated joint-state/output bound rather than an automatically defined channel.

After canonical syndrome/frame decoding, the reflected channel is identity on all protected logical qubits. Thus choosing T_n=exp(a beta n/8) gives error tending to0 as n grows, while local rates and ratios remain fixed. The construction retains the original positive-rate protected code space asymptotically, with constant witness overhead in this abstract model.

## Admission and cost limits

- Only the specified Tanner family and actual source hypotheses are used. Arbitrary Tanner, LDPC, low-degree fixtures, or GPT's different potential do not inherit this theorem.
- rho is a tiny sufficient constant, not a measured physical threshold. The optimistic finite Delta diagnostics are not certified code instances.
- The graph is an expander; fixed-density3D local routing is not supplied and can impose a growing slowdown.
- Conditional jumps act on O(Delta²) qubits/registers and require local syndrome predicates. Direct truth tables can be exponentially large in Delta. No native few-body synthesis, finite-temperature controller realization, or same-resource hardware advantage is earned.
- All witness qubits are noisy in the displayed admission. Further ancillas, calibration errors and reset services need their actual local-generator/interaction model before inclusion.
- Initial encoding/witness preparation and final controlled-frame plus syndrome recovery are charged operations. The memory theorem begins with an encoded state; it does not manufacture an unknown encoded input for free.
- Existing active quantum Tanner memory receives the same interactions, classical information, noise rates and preparation/readout. Its comparison cannot be replaced by a weak decoder.

The proposed scientific advance is an abstract conversion of local decoding witnesses into a robust, clock-free dissipative memory, including coherent errors on those witnesses. It would not by itself be the civilisation-level north star. The essential next physical gate is a concrete finite code and noisy native-interaction realization, not merely sharpening the conservative constants.
