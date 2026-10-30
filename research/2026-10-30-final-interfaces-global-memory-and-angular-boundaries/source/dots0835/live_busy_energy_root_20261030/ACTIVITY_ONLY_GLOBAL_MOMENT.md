# Can the running native apparatus already have sparse physical prefixes?
2026-10-30. Root construction candidate, not reviewed. This is a potentially stronger replacement for requiring controlled retirement before accessing bare DATA. The accepted retirement/readout constructions remain unchanged and useful if this route fails.

## 1. Separate the question from DATA energy
The accepted global memory potential pays for raw DATA syndrome energy and dirty histories, but its scalar upper bound alone does not control clean BUSY prefixes. Reusing that bound to erase all controllers was invalid. Instead build a SECOND proof observable on the SAME physical generator, using the already constructed multiplicative activity hierarchy, but no DATA energy and NO useful-recovery interpolation T_t.

Let D=Σ B_h be actual history defects, M1=Σ P_h the reviewed BUSY count, and M2=Σ_(h~j)P_hP_j the finite neighbor-pair count. B_h and P_h are actual commuting controller projectors in the forest frame. Take

  V_B=exp(s R D),
  Y=product_g exp(δ X_g^guard),  G=Y†Y,
  W=V_B G,  F_act=T_B(W).

Use the full catalog of singleton gates with coefficient Aε² and pair gates with coefficient B0; same finite guards and same controller-only history-pinched witnesses. The actual physical parameters ε,ζ and all reset/monitor rates are unchanged. These are additional mathematical proof parameters/observables.

## 2. Exact maskwise bounds on the activity weight
The reviewed activity witnesses commute EVERY P_h and B_h, and satisfy cP_h≤X_h≤CP_h. Therefore on a fixed joint mask the lower and upper singular values of a product Y can be bounded by the PRODUCT of the individual gate singular values, even if the gates fail to commute internally. This gives operator bounds sector by sector:

  log G ≤ C δ (Aε² M1+B0 M2),
  log G ≥ c δ Aε² (M1−C_guard D).

The lower bound counts all singleton anchors whose local history-good buffer is unmasked; one dirty history masks only boundedly many anchors. Pair factors are positive with minimum singular value≥1 and cannot reduce this lower bound. The inequalities require the actual catalog to include every singleton and its positive lower witness; verify no missing boundary anchors.

Since G commutes D,M1,M2, logW=sRD+logG. Crucially KEEP M2 in the upper bound. Replacing M2 by degree×M1 loses an ε² factor and can destroy the desired conclusion.

## 3. Proposed actual-controller drift
With no DATA energy, every ideal clean DATA channel leaves V_B unchanged and acts on the controller-only G through the already reviewed clean controller factor. Useful DATA-decrement commutators and T_t are unnecessary. The clean activity theorem and actual dirty-credit/cavity calculation suggest

  (T_B^{-1} L_native* T_B) W
    ≤ [−a δAε² M1 −b δB0 M2 −γD +ρ0 N] W,
  ρ0 ≤ C(δAε⁴+δ²).

Dirty masked-anchor losses O(δ)D are absorbed by strong dirty service. Cross clean/dirty blocks may leak O(δ²)N; they must not leak a generic O(δ)N source. The first acquisition and later ζ perturbations of dirty service should remain paid by D, as in the actual native credit. These are the LOAD-BEARING transfers to verify, not a claim that the old theorem automatically implies this drift.

The negative counts dominate λ logW for fixed λ>0 independent of ε, because the singleton AND pair drift coefficients match their coefficients in logG. The dirty coefficient dominates sRD after reducing λ by a fixed factor. Thus positive pullback and joint bounded-body noise would give

  L_actual* F_act ≤ −λ T_B(W logW)+ρN F_act,
  ρ=C(δAε⁴+δ²)+C_noise η.

The constants must be uniform for small ε,δ. No inequality passes through the nonpositive inverse; it is only a local similarity bookkeeping tool. Actual full propagators remain CPTP.

## 4. Scalar moment and direct BUSY tail
For σ=T_B*(ρ_phys), spectral Jensen gives Tr(WlogW σ)≥x logx with x=Tr(F_actρ_phys), since T_B is unital CP and σ has trace1 (or≤1 in a justified killed use). Consequently

  d logx/dt ≤ −λ logx+ρN.

From encoded/ready initialization F_act=1 on the actual controller input, so logx≤(ρ/λ)N uniformly for all time. This estimate should be proved on the FULL physical evolution: no DATA basin is required because the observable and clean activity calculation do not need active DATA-density or a small canonical error. Whether all dirty full-Hilbert terms are covered is part of §3.

The dirty no-jump coefficients preserve D and every BUSY projector and have identity on good histories, minimum survival s_min on bad histories. On each mask, T_B's retained no-jump branch therefore costs at most κ_D D, κ_D=−log s_min. Unlike the memory potential, there is NO (1−t)^N useful-interpolation cost. Combining with the maskwise G lower bound gives, if sR−κ_D pays cδAε² C_guard,

  F_act ≥ exp(k δAε² M1)

for fixed k>0, potentially with an additional positive dirty weight. This step needs actual commutation of no-jump coefficients with the BUSY mask; norm lower bounds suffice within a fixed mask even if they do not commute G.

Hence

  Pr(M1≥βN) ≤ exp{[ρ/λ−kδAε²β]N}.

Set δ=dε². The source-to-BUSY-barrier ratio is controlled by

  O(ε²)+O(d/A)+O(η/(dAε⁴)).

Choose d small relative to β and fixed hierarchy coefficients, then ε small, then η below the required positive threshold. This is potentially compatible with the already selected memory device; the proof parameters may be chosen separately, but simultaneous physical inequalities must be checked. No useful numerical threshold is asserted.

## 5. Consequence only if the drift closes
Combine the full-state BUSY tail with the accepted global memory full/killed comparison and canonical Pauli radius. On the joint positive good branch, bare physical DATA has coefficients supported on the canonical error plus at most r_R βN active owner footprints. A single ordinary DATA decoder then corrects it without waiting for controllers to idle or applying a forest inverse. This would be a direct live encoded-output contract, not a claim that one can arbitrarily interact with that output while its memory Hamiltonian remains on.

For destructive readout, a finite payload shutoff ramp can use this initial sparse BUSY mask rather than a preceding retirement dwell, if the separately constructed invariant-mask ramp proof applies. A physical quantum output handoff still needs its actual coupling/routing mechanism. The accepted retirement route remains a constructive fallback.

## 6. Falsification targets
- A hidden O(δ)N source in the full dirty surgery defeats the stated parameter scaling.
- If no-jump dirty coefficients fail to preserve the BUSY mask, the direct lower bound may need repair.
- If the activity catalog omits singletons or its lower witness is only valid in a stronger good corner not covered by D, the BUSY lower bound is not earned.
- If physical rate choices for the full-memory theorem and this second observable conflict, they cannot be silently retuned independently.
- This is not a new principle merely because it has a new potential; its value would be removing an actual access operation under the same continuous-noise model.

## Stronger lower-bound route suggested by actual source algebra
The native author reports an exact stronger property of the fresh dirty CP credit: T_B fixes the entire commuting BUSY algebra, not merely its no-jump branch. Own history-bad source lies within own BUSY, and its erasure target Q0,W0 is also BUSY; for another owner the monitored source algebra acts nontrivially only on h-owned/z_h labels and is scalar on their complement, preserving every other own-tag readiness predicate. Each weighted erasure/no-jump Kraus thus preserves all BUSY masks. This fact still requires independent source verification.

If verified, the direct lower bound simplifies. The maskwise estimate gives W≥exp(k δAε² M1) as soon as sR≥k δAε² C_guard. Positivity and exact fixation then imply

  F_act=T_B(W)≥T_B(exp(k δAε² M1))=exp(k δAε² M1).

No dirty survival penalty is needed for this BUSY tail. The no-jump alternative in §4 remains a possible weaker route, but should not obscure this exact algebra if earned. The actual drift/source budget remains the decisive unresolved obligation.
