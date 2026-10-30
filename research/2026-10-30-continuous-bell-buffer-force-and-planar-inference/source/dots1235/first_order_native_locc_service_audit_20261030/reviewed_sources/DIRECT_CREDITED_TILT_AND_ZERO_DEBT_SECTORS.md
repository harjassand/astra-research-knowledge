# Direct local tilt of the guarded raw credit and its actual zero-debt sectors
2026-10-30. New candidate. Conditional on the full raw composition in `RAW_GUARDED_AC_CREDIT_COMPOSITION.md`; no continuous-memory theorem or new physical mechanism is asserted. All physical rates, gates, resolved instruments and classical communication are unchanged.

## 1. Exact local discount, not an inverse-CP order argument

Write `D_h` for the guarded A/C source projector, `A_h^c` for its positive coefficient (extended by zero), and

    a_h = V^(-1) d_h,     C_h = I-t A_h^c a_h,     0<t<1/2.

The decrement here is the true captured-program decrement on D_h, with a harmless bounded current-relative extension off its support. The local factor A_h^c a_h is positive, at most I, and commutes V. The full read footprint includes the checks deciding the actual local table and every local potential term changed by its output; equivalently, the normalized ratio V_after/V_before depends only on raw checks supported there. The overlap guard must use that FULL footprint, not merely the Pauli write support. This is the full raw-read/write footprint of the governing machine.

For h!=g, every Kraus of T_g commutes C_h. If full footprints overlap, nonidentity branches have mutually exclusive sources D_g D_h=0 and preserve their own A/C phase/activity, so both mixed products vanish. If they do not overlap, the h coefficient, program, normalized decrement and its guards commute g's DATA/controller operation; shared Alice raw-check/history controls are commuting diagonal controls and are not changed by a virtual Bob operation. No claim that T_g fixes the GLOBAL d_h is needed. Thus C_h lies in T_g's multiplicative domain and T_g(C_h)=C_h. Induction gives the EXACT identity

    V_c = T(V) = V product_h C_h.                      (1)

All C_h commute one another and V. They also commute every mechanical B, combined semantic Q and actual ACTIVE mask. Consequently

    S_t = V_c^(1/2) = V^(1/2) product_h C_h^(1/2)       (2)

is an invertible finite-depth product of bounded-support commuting positive factors. In a local similarity S_t O S_t^(-1), factors initially disjoint from O cancel EXACTLY: because all factors commute, a factor commuting O also commutes every subsequent transformed O. There is no iterated unbounded neighborhood growth. Fixed footprint incidence and C_h>=1-t give uniform local norm and inverse-norm bounds, and an O(t) comparison to the similarity by V^(1/2). The global bound (1-t)^(number of hubs) is NOT used for local operators.

## 2. Conservative completion needs total positivity only

Let L_f be the actual nominal generator with all Bob LOAD bundles removed, but all fixed positive Alice LOAD, monitors, abort, transport and resource rates retained. The raw composition gives L_f^*V_c<=0. Write its actual local terms as

    L_f^*O=sum_e [sum_a J_ea^* O J_ea+K_e^*O+O K_e],
    K_e=-iH_e-Gamma_e/2.

Use the displayed convention rather than interchanging Schroedinger/Heisenberg similarities. Put

    J'_ea=S_t J_ea S_t^(-1),   K'_e=S_t K_e S_t^(-1),
    Delta_e=-(sum_a J'_ea^*J'_ea+K'_e^*+K'_e),
    Delta=sum_e Delta_e=-S_t^(-1)L_f^*V_c S_t^(-1)>=0.  (3)

Every term is local with fixed bounds. An individual Delta_e MAY BE INDEFINITE: the credit generally fails to commute the resource/clock Hamiltonians whose service it measures. This is not an obstruction. The exact CP subunital generator and its conservative completion are

    L_w^*O=S_t^(-1)L_f^*(S_t O S_t)S_t^(-1),
    L_c,t^*O=L_w^*O+{Delta,O}/2
       =sum_e[sum_a J'_ea^*O J'_ea-{sum_a J'_ea^*J'_ea,O}/2
                +i[H'_e,O]],
    H'_e=(K'_e^*-K'_e)/(2i).                           (4)

Thus L_c,t is a genuine local unital GKLS generator. This uses the unchanged actual J_e and K_e, not a fictitious physical splitting by a coherent guard. Total Delta positivity is needed for the subunital service interpretation, but even the GKLS identity itself does not require positivity of each Delta_e. Shared monitors appear once in the actual sum.

## 3. Specific one-step flag lemma for V_c

**Claim.** For every actual complete local bundle, including each Hamiltonian separately, and every Q/B projector R,

    [L_e^*V_c,R]=0,   [Delta_e,R]=0.                    (5)

This is a statement about THIS credited observable. It does not assert that the entire joint-Q commutant is invariant. That stronger assertion has an accepted counterexample.

The original H_e and Gamma_e commute R, and V_c does too. Their terms therefore commute R, even though [H_e,V_c] need not vanish. It remains to check the COMPLETE gain. The following are the actual source cases.

### A. Full and incomplete Bob terminal sources

In a full-ownership C_L source, h's target Q0 still has all its own tags. It is ACTIVE, so every overlapping Bob credit is off at both source and target. The own credit is off at the target. Nonoverlapping credits commute the full h circuit. The remaining target raw weight is diagonal in all raw syndromes and final W/P/source labels. The actual complete extraction/lookup/controlled-Pauli label normalizer therefore removes the W=0/W!=0 source cross block exactly, with the other coefficients as spectators.

An incomplete mask or R source is entirely mechanically bad. For an overlapping target credit to open after T_h, h must become FREE. Since T does not change tags, this requires no o_h OR z_h tag anywhere. In particular its ownership-deleted forest is identity. The new overlapping coefficient then has no hidden h-DATA prefix with which it could form a mixed mechanical block. If any own tag remains, every overlapping target credit stays off. Own h clock/W/P are completely source resolved at T, so no mixed h mechanical source block remains. Other owners' consistency masks are preserved by these operators.

B0 has identity frame. Nonprefix I/A/Q reset sources are fixed clock/source labels with identity frame and complete W/P erasure. A target may open a neighbor credit but cannot generate a source good/bad cross block. Bob never changes Alice raw truth. The program/cache erasures and transfers are separately value resolved; remaining A/C coefficients preserve valid P and classical values. These facts give all semantic-Q commutators as well as the mechanical ones.

### B. Alice terminals and strong Alice LOAD

No Bob coefficient has Alice clock/tag OFF-DIAGONALS: its Alice dependence is solely the commuting parent-history/truth guards. A full Alice terminal pulls the raw-syndrome/final-pointer algebra through the complete syndrome-XOR normalizer, even with spectator Bob A/C coefficients. Hence it has no Alice W-good/W-bad cross block. In an incomplete/R source, B_g=1. Every Q_j whose compared checks/worker can be changed by g is then identically I. The arbitrary partial-DATA block is consequently confined to a saturated Q_j corner. Unaffected Q_j commute strongly. This is the same structural parent set as in the raw proof; no pruning by an accidental prefix is allowed.

Alice LOAD is NOT removed: its I/A0 consistency predicates coincide, W and source classical labels are separately erased/resolved, and Bob coefficients have only diagonal Alice clock/tag dependence. W healing or newly opened parent guards cannot create a mechanical cross block. Fixed READ program has no semantic payload token. COMMIT, READY and W refresh have the same resolved-source argument and matching source/target structural predicates.

### C. The nontrivial cleanup test

A resource cleanup gain z_h->free is not clock resolved, so merely invoking no-creation is insufficient. The credited observable has controller off-diagonal blocks ONLY within Bob A or C coefficients; it has NO own I/Q clock coherence. (It can have resource/monitor coefficients within those A/C blocks.)

Fix the cleaned resource index j. A consistent target A_i block with tag_j=free must have i<j. Any A_i/A_l coherence in that target therefore has BOTH i,l<j. Pulling it back through z_h->free gives tag_j=z_h at both endpoints, violating the unacquired-suffix consistency test on BOTH endpoints. Thus this entire newly opened coefficient lies inside B_h=1, not between B_h=0 and 1. A target C coefficient requires tag_j=o_h and is annihilated by the cleanup pullback. Other h phases contribute only diagonal clock/tag raw weights or spectator coefficients and cannot introduce a cross block.

For another Bob g, tags z_h and free are both not-own-g. Any g coefficient has the same g consistency test on them; its required h-FREE guard may open, but its own A/C block remains mechanically good at both endpoints. Other Bob mechanical masks and all Alice-parent masks commute. Within the only own-h A coherences P validity is constant, and all value labels/raw Alice truth are unchanged. Hence the gain commutes every semantic Q as well. For Alice cleanup there is no own off-diagonal Alice A/C credit at all; only diagonal parent guards can open.

This is exactly why the same argument DOES NOT apply to a general availability witness with Q_i/Q_l clock coherence. Such a witness can pull back across a mechanical good/bad boundary; it must be treated by a clean/dirty cross estimate later.

### D. Remaining classes

Acquisition, payload, inverse rail, Q verification, failed-test and owner-cleanup Hamiltonians are covered by the original H flag commutators. Prefix-watchdog gains have source-resolved C_t, identity W/P frame, and target B outside the own A/C credit; active overlapping credits remain off. Finite monitor jumps preserve each flag strongly. Source-resolved packet shifts, receive/discard, worker/HOLD transitions and pointer transfers preserve or delete value tokens; any opening is diagonal in the source value/raw-syndrome algebra. They carry no unmeasured classical erasure. All complete equal-rate losses were included above. This exhausts the accepted alphabet; no Bob LOAD is in L_f.

Together these cases prove (5). It is not inferred from Delta>=0, compressed service, or the individual-good-range fact alone.

## 4. Zero-debt invariance and stable old witnesses

For any one R in the Q/B family, the original J_ea preserve ker R, and S_t commutes R; hence J'_ea preserve ker R. Original K_e and S_t commute R, so K'_e does also. Equation (5) makes the conservative no-jump drift preserve ker R. Thus

    0<=exp(u L_c,t^*)R<=R.                             (6)

Only own-zero invariance is asserted. It implies that L_c,t^*Z is supported in the R corner whenever Z=RZR: every Kraus path preserves ker R, so both the zero compression and the cross blocks vanish. This is stronger than an unsigned norm estimate on the identity.

Let L_c,0 be the accepted conservative RAW-V tilt of the SAME Bob-LOAD-off physical generator. Its finite local witness satisfies alpha R<=Z_R<=R and L_c,0^*Z_R<=-r_R R. By (1)-(4), only finitely many transformed local terms meet Z_R and

    ||(L_c,t^*-L_c,0^*)Z_R||<=C_R t.

Both generators preserve ker R, so the difference is R-supported. Therefore, for fixed small t,

    L_c,t^*Z_R <=-(r_R-C_R t)R <=-r_R R/2.             (7)

This transfers the already earned actual debt return witness without pretending that the transformed monitors are unchanged. It uses no Poisson ancestry and no fresh physical return mechanism. Finite spatial/type families allow one positive t independent of N. The same reasoning can be used for ACTIVITY only after its corresponding one-step/zero-sector property is established; it is not automatic from (5).

## 5. What this earns, and what remains

Equations (1)-(7) supply local credited tilt, specific reducing debt sectors and a strictly negative first-order weighted-debt service with unchanged physical rates. They do not by themselves supply exposure times a current decrement, restored-LOAD bookkeeping, or global useful-energy coverage. A local finite-depth dressing can tolerate a generic O(N delta^2) second-order remainder if its scale hierarchy pays a small final energy density; no exact joint commutant or second-order corner closure is asserted here. The old stochastic result, all raw receipts and their initialization/noise/output restrictions remain unchanged.

## 6. Focused diagnostics and sufficient weak-LOAD fallback

`check_credited_cleanup_and_tilt.py/json` uses all 180 phase/tag/W basis states for the two-resource cleanup fixture, arbitrary positive coherent A and C coefficients, and both actual z->free cleanup maps. All mechanical cross blocks and the part of a newly opened A coefficient outside the dirty corner are zero. The same fixture gives a 1/2 good/bad cross for a positive Q0/Q1-coherent target observable, confirming that section 3C is a special property, not generic no-creation. A separately labeled abstract three-state diagnostic has an indefinite Hamiltonian Delta_e (eigenvalues +/-0.2683), total Delta>=0, conservative-GKLS identity error 2.2e-15 and exact zero-corner preservation. It tests the algebra in (4), not the full native generator. Existing actual gate/terminal tests remain the source for those operations.

For the eventual weak-LOAD composition, no extra LOAD-zero-invariance theorem is required. One may conservatize the FULL generator: (4) is GKLS for any Hermitian Delta, while the full raw inequality supplies Delta>=useful+debt-C lambda t ACTIVE rather than Delta>=0. The change in the debt-witness drift due to the actual complete weak Bob LOAD bundles is bounded locally by C lambda I. At debt-dressing strength delta this costs C lambda delta N. With useful scale kappa~lambda t and delta=sqrt(lambda)*t, its final density cost is C sqrt(lambda), which is small. The no-LOAD zero-corner proof above is the load-bearing claim; any sharper restored-LOAD commutant is optional, not assumed here. No complete guarded LOAD bundle is replaced by lambda(Phi-I).
