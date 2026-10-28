# Repeated coherent storage through a genuinely reset syndrome sector

28 October 2026. Root candidate; separate internal review pending. This is an exact channel-composition lemma, not an inference from a one-cycle fidelity test or a classical fault probability. It is intended to close a specific gap between the received flagged one-cycle construction and repeated use of the SAME learned controls.

## 1. Actual maps and norms

Let P be a CPTP idempotent on the physical storage register: P^2=P. For an error-correcting code, P=C composed R is ideal syndrome measurement/correction returning to the code, with logical information preserved. Write Q=I-P; Q is a linear map, NOT a positive operation. In complete trace/diamond norm, ||P||=1 and ||Q||<=2.

For each cycle let E_t be the ACTUAL closed CPTP round on the declared persistent register. Let A_t be a CPTP reference round satisfying

    P A_t=A_t=A_t P.                                      (1)

The simplest case is A_t=P. More generally A_t may evolve an explicitly included slow reference/bath register while resetting the syndrome, provided(1) really holds. Put Delta_t=E_t-A_t and assume certified complete-map bounds

    ||Delta_t||diamond<=epsilon_t,
    (1/2)||P Delta_t P||diamond<=b_t.                     (2)

These are different obligations. A small decoded one-cycle error b_t does not imply small epsilon_t, and marginal control characterization does not certify a complete retained-bath norm. In the Markovian physical-tile specialization, bounded actual gate-channel differences and the full fault-free circuit A_t=P can supply epsilon_t by a paid circuit hybrid.

All old syndrome/flag records must either be physically retired before future use or explicitly included in the persistent register and the proved maps. A source/controller that reads an omitted record or bath is not a closed E_t on the claimed register. Fixed coherent calibration errors ARE allowed inside E_t; independent random learned programs per cycle are not assumed.

## 2. Exact slow/fast recurrence, without ideal intermediate recovery

Define the actual accumulated map T_t=E_t...E_1 P and its two LINEAR components

    S_t=P T_t, G_t=Q T_t.

S_t is CPTP and ||S_t||diamond=1. G_t is not a state or implemented map. No P or Q is physically inserted between actual cycles. Since P G_t=0 and(1) holds,

    G_t=Q Delta_t(S_(t-1)+G_(t-1)),
    S_t=A_t S_(t-1)+P Delta_t P S_(t-1)+P Delta_t G_(t-1).

Thus, with g_0=0,

    ||G_t||diamond<=g_t,
    g_t=2epsilon_t(1+g_(t-1)).                            (3)

Compare S_t to the true reference product A_t...A_1 P. Contractivity of A_t and the fact that S_(t-1) is an actual CPTP composite give

    (1/2)||P E_T...E_1 P-A_T...A_1 P||diamond
       <=sum_(t=1)^T [b_t+(epsilon_t/2)g_(t-1)].          (4)

This is a finite-time complete-reference bound. It has no exponential factor in the number of cycles because the projected ACTUAL past map S_t has norm1; it is not bounded by multiplying perturbation norms of all earlier cycles.

If epsilon_t<=epsilon<1/2, then g_t<=2epsilon/(1-2epsilon), and

    error <= min(1, sum_t b_t
                    +(T-1)epsilon^2/(1-2epsilon)).       (5)

When b_t=O(epsilon^2), repeated error is O(T epsilon^2). The same deterministic learned receiver may be used every cycle. This does not assume that individually decoded rounds are independent channels or that every noisy round returns exactly to the code space. The fast syndrome component is controlled by its actual contraction toward the code projection.

One may improve(3)-(4) with separately certified bounds on Q Delta_t restricted to the Q-range, P Delta_t on that range, and Q Delta_t P. The displayed conservative constants require no such optimization. If the actual complete epsilon is not below1/2, the finite recurrence(3)-(4) still exists but no useful uniform geometric claim follows.

## 3. What the flagged storage construction must supply

The fault-free Chao–Reichardt five-qubit correction circuit, with actual physical Pauli corrections and discarded records, must equal the standard ideal recovery P on ALL physical operators, not merely on a particular codeword. This follows if its ideal instrument measures the commuting stabilizers completely and applies the standard syndrome correction: every nontrivial early syndrome triggers a complete fresh pass; the all-zero path has already measured all stabilizers. The author/reviewer must bind this identity to the actual circuit version.

For a complete storage cycle, ideal native-frame and ideal receiver operations must cancel on ALL physical tile operators before this EC map. The full physical-input unitary-frame architecture supplies Ad_(V dagger) composed Ad_V=identity on the entire tile, not only on encoded codewords. A receiver that is correct only on the code but changes syndrome sectors does not establish E_0=P; it requires a separately proved reference satisfying(1).

The received one-cycle single-fault theorem can then make b_t quadratic in the microscopic native/receiver/EC error strengths, with ideal final decoding used only to DEFINE P Delta_t P. A separate hybrid across EVERY potential controlled slot gives epsilon_t. Clean-path fault counts alone are not the total slot bound: branch-only rescans/corrections can contribute higher-order terms. The pending clarified unrolling counts751 potential EC locations, not the737 maximum actually executed path. Disabled zero-duration bypasses and actual hardware waits have different physical idle bills.

For the simplest specialization take a fixed finite physical code block or interleaved tile, actual native reduced CPTP channels, fixed learned local receiver circuits, fresh syndrome/flag ancillas, an actual ordered local-CPTP hardware model, and records discarded each round. Then E_t is a genuine CPTP map on that physical tile and P is its ideal recovery. Initial unknown-qubit injection/encoding and final physical decoding/readout are ONE-OFF error debits; no claim is made that arbitrary input injection becomes fault tolerant automatically.

This is not a global threshold or an arbitrary source-memory theorem. A whole-array epsilon can grow with array size even when per-location precision is fixed. Apply the lemma only to a proved closed finite tile or supply a separate local/cluster composition argument. An unmodelled shared bath can invalidate(2). If a retained bath is included, (1)-(2) must be proved on the enlarged register; tracing the bath in a one-cycle test is insufficient.

## 4. Why the fast-reset obligation is indispensable

Let the register be logical qubit L and syndrome qubit G. Set P=id_L tensor reset_|0>, but take the ACTUAL round with no reset at all:

    E=Ad exp(-i theta Z_L tensor X_G).

Starting from G=|0>, one decoded cycle is logical dephasing with error sin^2(theta). Repeating the same coherent round T times before final decoding gives error sin^2(T theta), which is quadratic in T at small angle. A one-cycle Bell/diamond test cannot justify linear-T accumulation here. The complete E is not close to P on arbitrary syndrome inputs: at theta=0, E is identity while P discards G, so their half-diamond distance is1. The hypothesis epsilon<1/2 is violated, as it should be.

This counterexample is distinct from a noisy flagged round whose fault-free operation really erases syndrome. The useful resource is the implemented reset structure, not a label that the data were 'error corrected'. No microscopic environment reconstruction is required to state the lemma, but physical control of the relevant reset interface is required to use it.

## 5. Scientific status

This is a candidate finite perturbation/composition principle around a CPTP projection. It reuses standard channel norms and code recovery; no historical novelty claim is made. The new obligation is a correct connection from the actual adaptive flagged circuit, full slot accounting and complete-map error contracts to(1)-(2). The one-cycle pilot does not by itself discharge that obligation. A rigorous proof/check and independent receiving receipt are needed before importing this into the governing storage architecture.
