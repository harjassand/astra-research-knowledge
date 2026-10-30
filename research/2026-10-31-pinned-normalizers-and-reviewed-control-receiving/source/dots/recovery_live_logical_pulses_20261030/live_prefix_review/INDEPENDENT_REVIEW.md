# Narrow independent review: live prefixes and fixed native cycle
2026-10-30. Reviewer `producer-workspace/review_live_prefix_cycle`.

Reviewed manuscript: `live_prefix_derivation/LIVE_PREFIX_AND_FIXED_CYCLE.md`, original SHA-256 `57b0b1ef649837ab69b73690939804ee76f7883d44c10d0ae1a4deb81bb21c06`.

## Verdict
The deterministic live-prefix radius/BUSY/energy bounds, exact warm energy/BUSY entropy relaxation, explicit parameter budget and fixed dwell are **sound under the cited accepted native contracts**. One receiving qualification is required before these establish an exactly factorized positive restart channel: the positive logical-factor repair below must be included. The original note avoids calling the signed good map positive, but its positive support projection alone does not establish exact logical factorization. This is a repairable seam, not a counterexample to the closed cycle.

This review does NOT accept the root's separately developing full-register CP-cavity tail, arbitrary bath extensions, or whole selectable-gate theorem. It does not re-audit accepted native foundations or factory boot.

## Source checks
Directly read actual global compiler §§2,4–7, singleton `DIRECT_SINGLETON_DERIVATION_V1.md`, the independent singleton receipt, the independent global-energy receipt, actual whole-recipient receipt, and frozen native forest/readiness source. In particular:
- BUSY predicate is controller/workspace/tag-only, not DATA- or monitor-outcome-dependent.
- Actual forest preserves readiness masks; its nonidentity DATA action is confined per coefficient to full footprints of nonready owners.
- History-bad is contained in stronger BUSY.
- Singleton delta_B is an independent analytical choice, not necessarily global delta=d epsilon²; the singleton independent receipt explicitly confirms this.
- Global pullback supplies the actual raw negative energy term, not merely an upper spectral envelope. Global proof tuning makes rho/lambda arbitrarily small with fixed proof ratios chosen before epsilon/noise.

## Deterministic constants
For each output bank the manuscript's

    r_+ <= 2r_in+6f m_in+2(1+fa)ell,
    M_+ <= m_in+a ell,
    E_+ <= c_U r_+ + R M_+

are valid conservative bounds, with f measured in PHYSICAL DATA sites and r in summed CSS weights. Initial forests contribute 2f m_in in each input bank, CNOT per-bank output weight is at most the sum of the two inputs, and final forest contributes 2f(m_in+aell). The factor six is not double-counting; a notation using f as CSS footprint would have factor three instead. All locality counts are per coherent mask, never a union over all masks. ell must already bound physical sites AFTER intended gate propagation, as the note states.

## Relaxation and budget
The scalar spectral Jensen step is valid for arbitrary positive subnormalized sigma; its mass correction has the favorable sign. The global exponent is exactly nu_E=g+s rho_E/lambda_E and damping lambda_E/s. The full-state BUSY exponent is nu_B=rho_B/lambda_B and damping lambda_B. Transferring the full BUSY tail through the full-versus-killed bound avoids an unjustified killed BUSY generator inequality.

The proposed alpha,e,b,p choice gives E_+<alpha, r_+<r0/2, sE_+<s'e_cut/4. Combined with the strict small-parameter inequalities, both initial warm exponent and stationary floor lie strictly below the native exit barrier. The log-max dwell expressions work also when the warm exponent is below its stationary floor; the max(0,...) prevents invalid logarithms and zero dwell already satisfies the desired midpoint bound. The maximum dwell meets both energy and BUSY cuts. Constants can be very large/small, but are independent of N, bank count and gate-history length.

## Required positive logical-factor repair
Let L be the whole logical register and A all retained syndrome/controller/bath auxiliaries after the fixed KL chart. Suppose the actual positive projected channel is Phi and the signed good pulse map is

    G = Ad(U_L) tensor A_good,
    ||Phi-G||_diamond <= beta.

Here beta is the signed bad pulse-map norm after projection; support of G ensures projecting it changes nothing. A_good need not be CP. Undo U_L in notation. Define the CP auxiliary map

    A_pos(X)=Tr_L[Phi(I_L/d_L tensor X)].

Then set Psi=Id_L tensor A_pos (restore Ad(U_L) afterward). Evaluation at I_L/d_L and partial trace are channels; hence

    ||A_pos-A_good||_diamond <= beta,
    ||Psi-Phi||_diamond <= 2 beta.

This is a mathematical repair, not a physical decoder/reset/re-encoder. Phi CP/TNI makes A_pos CP/TNI. Because the positive projection cut is I_L tensor P_A in the common KL chart, A_pos has exactly the same supported auxiliary range. Its energy/BUSY envelopes therefore remain valid. It gives the exactly logical-factorized positive restart needed by the native theorem. When the auxiliary input is fixed independently of the unknown logical input, the same construction simply gives a positive subnormalized auxiliary state.

The actual unprojected channel differs from Phi by the separately priced gentle bound <=2 sqrt(beta) (up to any already charged incoming error). Thus a safe receiving charge is 2 sqrt(beta)+2 beta. Do not infer exact logical identity from mere membership in the common correctable span: an undetected logical error acts entirely inside the code subspace and is the simplest counterexample.

## Scope
The repair is valid for joint L and arbitrary retained reference; it does not replace root's need for a joint matching fault-tail estimate. Treating other logical banks as a bath and proving only marginal fidelity would remain insufficient. Full-register common KL factorization of the signed good map is the necessary premise.

## Binding completion: 19:02 UTC
The author incorporated the positive logical-factor repair in §3 and supplied direct actual forest and quantitative rate-source checks in §7. I read those amendments and the cited actual `FULL_HILBERT_FOREST_GAUGE.md` §§1–3 and `GLOBAL_EXPONENTIAL_CONTROLLER_INTERFACE_CANDIDATE.md` §6. The final reviewed manuscript SHA-256 is:

`2ef4ba241fb2a590e0b3859cd6571efc73a4183f44f08c7ad0df842a271048e9`.

**Final scoped verdict: PASS for the deterministic live-prefix receiving lemma, its positive logical-factor repair, exact warm entropy relaxation, and strict fixed cycle budget under the explicitly imported native contracts and the supplied joint good/bad pulse-map premise. No remaining blocker was found in these seams.**

The earlier qualification above is retained as failure history and is now discharged. Full-matching CP-cavity receiving, physical matching schedule and integrated whole-register theorem remain outside this review. The repair uses only analytical maps and leaves the actual same dirty apparatus unchanged.
