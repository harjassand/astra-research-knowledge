# Guarded animal-local activity weights: exact dirty-sector cavity charge
2026-10-30. New governing lemma candidate for composition. It addresses the zero-order animal-dependent reweighting, not merely a local Taylor remainder.

## 1. Input and noncircular guard
Work after the accepted dirty-credit normalization, so Lhat=sum_h Lhat_h is local HP/unital and has the raw uniform history-defect drift proved in `DIRTY_CREDIT_RAW_SIMILARITY.md`. Retain the actual own source-block calculation, not only its summed inequality. Every owner operation preserves every other B_j exactly; all its Hamiltonians preserve B_h. Its only B_h-changing gains clear B_h.

Take the controller-only, B-pinched activity generators from `CONTROLLER_ONLY_ACTIVITY_EXTENSION.md`. For an original active gate X_g let K_g be its support before adding B guards. Let N(g) include every owner h whose actual own generator or dirty credit can fail to commute with X_g; choosing all h with S_h intersect K_g nonempty is sufficient, where S_h is the fixed support of that own generator/credit. Define

    P_g^good=product_{h in N(g)}(I-B_h),
    X_g^guard=P_g^good X_g.

These factors commute, so X_g^guard remains positive and preserves activity corners. Use exp(delta X_g^guard) in the animal-local circuit Y_A, with the same globally fixed color order. The enlarged supports and incidence remain bounded.

No recursive support enlargement is needed. Added B guards commute all activity coefficients, all dirty survival coefficients, and every Hamiltonian. An h reset changes only B_h. Thus only the ORIGINAL active support determines which h must be guarded; other guards do not create new noncommuting owner actions.

## 2. Cavity identity on a bad source
For fixed h delete from Y_A every gate whose guard contains h, obtaining Y_A^{\h}. The number of deleted gates is bounded independently of A and N. Every retained gate commutes the entire h own generator, the erasure map and S_h. On B_h=1 every deleted gate is exactly identity, so

    Y_A B_h=Y_A^{\h} B_h,
    [Y_A^{\h}, L_h terms]=[Y_A^{\h},S_h]=0.

All activity gates are controller-only and B-preserving, hence commute every f_A. Write G_A^{\h}=Y_A^{\h dagger}Y_A^{\h}. The bad-source observable is therefore exactly f_A G_A^{\h}, not a small global approximation.

If B=A union D for a bounded local completion, the cavity circuits differ in O(1) gates; the same cancellation proof as in `ANIMAL_LOCAL_ACTIVITY_WEIGHT_CHARGE.md` gives

    e^{-Cdelta} G_A^{\h}<=G_B^{\h}<=e^{Cdelta}G_A^{\h}.

## 3. The raw bad proof reruns with cavity weights
Define

    V_cav,h=sum_A f_A G_A^{\h},
    Delta_cav,h=V_cav,h(B_h=1)-V_cav,h(B_h=0)>=0.

The cavity factors commute S_h, every h reset and every h-affected local syndrome/flag predicate. In the spectral-envelope proof, replace each scalar animal by that scalar times the positive controller weight G_A^{\h}. All source/target extrema remain Loewner inequalities, because the h instrument commutes these weights. The completion step is still valid even if different G_A do not commute with one another: the bounded-extension comparison above is sufficient for charging each positive source to its completed negative target.

Thus the token surplus changes only from q_R to q_R e^{Cdelta}. Choose the original q_R with strict margin (e.g. q_R<1/8), then delta small so this remains below 1/4. The SAME killed-resolvent/congruence calculation gives, on the h bad source,

    Lhat_h(V_cav,h)<=-gamma B_h Delta_cav,h,

with a fixed fraction of the original gamma retained. This proves the zero-order animal-dependent bad charge; it is not obtained by multiplying Lhat(V) by a varying G_A.

## 4. Healing-target activation is only a local O(delta) error
For a bad-to-bad h gain, the deleted gates are off at both ends and the cavity calculation is exact. A gain clearing B_h can turn on only the bounded set of deleted gates. Fixed-depth cancellation gives a local quotient Z_A with

    Y_A=Z_A Y_A^{\h}  (equivalently use the correctly ordered right quotient),
    ||Z_A-I||<=Cdelta,   e^{-Cdelta}I<=Z_A^dagger Z_A<=e^{Cdelta}I.

All factors commute f_A. Consequently its actual target gain is bounded above by (1+C'delta) times the cavity target gain, after increasing the constant for a fixed small delta range. This is an operator inequality before the h reset pullback, hence remains valid for arbitrary nonmonomial DATA/workspace reset and reference entanglement.

Only animals whose selected gates include one of the deleted factors contribute an error. They meet a fixed patch near h. Completing each such animal by that patch, every h token, and the h DATA-reset footprint gives a bounded-preimage charge to Delta_cav,h. This is the same local-token completion used in the raw bad proof, now with the cavity comparison factor e^{Cdelta}. Therefore the total extra bad diagonal term is at most

    Cdelta B_h Delta_cav,h.

For delta small compared with gamma this is absorbed. The inverse dirty-credit congruence is harmless here because the cavity factors commute S_h; its local fixed norm can be included in C.

## 5. Clean/dirty cross blocks
The cavity CONTROLLER factor commutes the h local Stinespring unitary; the remaining f_A is DATA-syndrome diagonal. The full f_A need not commute with the correction unitary. The deterministic-syndrome clean image therefore still makes the complete terminal good/dirty cross block EXACTLY ZERO for the cavity baseline. Other raw own terms have the same exact block property as before.

The only new target factor is Z_A-I=O(delta), supported on a fixed local patch. Its cross block has relative animal norm O(delta). Since local syndrome/token orbit ratios are finite, block Young gives

    +/- cross <= a B_h f_A G_A^{\h}
                 +C_a delta^2 (I-B_h) f_A G_A^{\h}

after bounded-patch completion if the local h token bundle is not already in A. Allocate a fixed part of gamma Delta_cav,h to the first term. The second term sums over the bounded-incidence supports meeting A, hence costs C delta^2 sum_A |A| f_A G_A, with exactly one |A| factor. Cavity and full weights for a fixed A differ by only O(1) gates and are uniformly comparable.

This proves that dirty diagonal activation is O(delta) times the available dirty charge, while clean leakage costs O(delta^2) W_G. It does not invent a physical B measurement.

## 6. Near-identity useful-credit terms
Guard each useful-credit primitive on the local all-B-good buffer covering every own term with which its original active support interacts. At a source B_h=1 that primitive is identity; on a healing target it can switch on by O(t). At first order the same cavity/source-target reasoning gives bad diagonal error O(t) Delta_cav,h and cross amplitude O(t). Thus the combined dirty surgery costs

    C(t+delta) Delta_bad + C(t+delta)^2 W_G.

Finite-depth second-order useful-circuit remainders have separate local O(t^2) relative animal bounds; mixed useful/activity conjugation terms have local O(t delta) bounds. These do not replace the zero-order cavity proof in sections 2-4. Higher linked terms are handled with the fixed local circuit depth and norm bounds, not a global expansion G_A-I.

The clean all-good calculation is unchanged by these history guards. The remaining task is the actual clean first-order DATA/activity inequality, including useful recovery, weighted coverage and its constants. This lemma does not assert that theorem by itself.
