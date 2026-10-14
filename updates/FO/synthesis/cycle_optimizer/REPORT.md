# FO cycle optimizer: adversarial profile-cycle report

**Status (15 October 2026):** no exact negative compatible closed walk was found for the new candidate below. The search produced scoped exact obstructions for the finite graphs and loops tested; it does not establish quasiconvexity of the candidate or of the full rank-one-convex quartic cone.

## 1. Incoming result and scope audit

I copied `work/FM-sources/resonant/` into `incoming_resonant/` before running its verifier and preserved the producer's original output JSON and manifest in `producer_receipts/`. The source hashes and original receipts are recorded there and in `MANIFEST.json`.

The incoming profile-graph theorem concerns the single integrand G, opposite carriers `(1,-1)`, the 81 profiles `(i/4,j/4)` with `0 <= i,j <= 8`, and widths `{1/8,1/4,1/2,1,2}`. Its 32,805 exact inequalities apply to adjusted edge cost

`integral G(Dphi) - (1/4) integral |Dphi|^4`.

The copied verifier replay passed all nine grouped checks. Its exact potential permits negative individual strips and proves a coercive lower bound for every finite closed walk in that particular vertex/width library. The source note's all-affine step is valid for that class: both carriers are odd, so each complete gradient profile changes sign under `y -> y+pi`, the cubic term in the homogeneous-quartic expansion vanishes, and the remaining affine Hessian term is nonnegative by the exact rank-one-convex acoustic form and Fourier/Parseval. This is one common affine matrix for the entire walk. The source expressly does not extend the graph theorem to arbitrary real vertices, all positive widths, arbitrary carriers, or other integrands. The coercive cost modification is part of that source theorem and is not used in the F11 raw-action search below.

I also replayed the N794 exact closed-heat certificate and Morrey-quartic checker. The heat certificate reports exact margin `1/500`, coefficient sup-norm radius `1/82000`, and Jensen constant `1/36000`; its proof is scoped to Fstar and the stated coefficient neighborhood. The copied N794 proof/checks establish Fstar as the known quasiconvex baseline in that scope. The incoming G certificate is its own exact acoustic rank-one-convexity proof. Neither certificate transfers automatically to the candidate F11.

## 2. Candidate and exact rank-one-convexity certificate

Use matrix entries `A=[[a,b],[c,d]]`, `u=a^2+c^2`, `v=b^2+d^2`, `w=ab+cd`, and `q=ad-bc`. The candidate is

`F11 = Fstar - (11/100) q^2`

`     = u^2 + v^2 + 4 w^2 + (339/100) q^2 - (29/10) q(u+v)`.

It is a new candidate in this investigation, not a historical novelty claim. The exact acoustic Hessian was reconstructed as the N794-style symmetric block matrix plus an explicit skew correction. The script verifies the polynomial identity for every acoustic direction, all eight leading principal minors, and an exact LDL factorization with positive pivots; this proves strict global rank-one convexity without angular sampling. See `acoustic_certificate_11_100.json` and `certify_candidate_11_100.py`.

The exact atomic law in that certificate has zero mean matrix and zero mean determinant, with mean F11 `-4361/500`. It proves non-polyconvexity only: the law is not a compatible gradient and is not used as a Jensen counterexample. F11 changes two coefficients relative to Fstar by `-11/100` and `+11/100`; it lies outside the N794 `1/82000` coefficient neighborhood and subtracts more than the certificate's `83/1000` determinant-square allowance. Thus the existing Fstar quasiconvexity certificate does not settle F11. Quasiconvexity of F11 remains unknown here.

## 3. Exact cycle searches

### Odd-carrier graphs

For F11 I replayed five 81-vertex graphs on `[0,2]^2` with step `1/4` and carriers `(1,-1)`, `(1,3)`, `(1,5)`, `(1,-3)`, `(3,-1)`, plus three signed-box graphs on `[-2,2]^2` with step `1/2` and carriers `(1,-1)`, `(1,3)`, `(1,-3)`. Each graph uses the five widths from the incoming library and all directed edges, for 262,440 exact edge/width cases total. All eight have rational vertex potentials, minimum checked slack zero, and no negative cycle. Since every carrier in these graphs is odd, the same half-period argument makes B=0 the global optimizer for each complete walk, not a per-strip optimization. These are raw F11 actions; no coercive term was subtracted. Results: `exact_cycle_search_11_100.json`.

Individual strips are substantially negative, so they are not treated as counterexamples. Across the eight graphs the most negative raw strip is `-16719683/76800` for carrier `(1,5)`; a closed compatible walk must telescope the vertex-potential terms and all widths must stay in the recorded finite set.

### Mixed-parity profiles and common affine optimization

For carriers `(1,2)`, the cubic profile moment need not vanish. I therefore optimized one common B over each entire loop. Eight explicit mixed-parity loops (unit, centered, translated squares and a varied-width rectangle, both carrier orders) have exact positive fully optimized gaps; the unit-square `(1,2)` case has nonzero cubic vector and optimizer

`B=(5381814/17496875, 0, 0, 496616/3499375)`.

I then tested all 64 axis-aligned elementary squares in `[-1,1]^2 intersect (1/4)Z^2`, with four constant-width patterns and two cyclic varied-width patterns. For each of the resulting 384 loops, the single common B was optimized exactly by a rational positive-definite Hessian solve over the whole loop. No fully optimized gap is negative; the exact minimum is `131019094487/537504000000`. Runtime was 91.83 seconds. Full results are in `full_affine_loop_search.json` and `full_affine_square_lattice_search.json`.

A separate exact fixed-background graph search used the same `(1,2)` carrier pair, 81 vertices on `[-1,1]^2` with step `1/4`, and widths `{1/4,1/2,1,2}`. At B=0 and at three rational backgrounds taken from the exact full-loop optimizers, each 26,244-edge/width graph has a rational potential and no negative cycle. This rules out a negative loop at those four fixed backgrounds only; it does not optimize B for every possible graph walk. See `mixed_parity_fixed_background_search.json`.

### Exact strip and timing checks

Six strip actions, including negative ones, were independently reconstructed from the source's invariant-average formulas and direct rational integration; all match exactly (`edge_formula_crosscheck.json`). A finite-width potential from the F11 `(1,-1)` graph has `P(end)-P(start)=-569753/76800` on edge `(1,2)->(2,1)`. Its exact slacks are nonnegative at the five certified widths, but at the unsampled width `4/7` the raw strip action is `-136769/16800` and the potential slack is `-388337/537600`. This is an exact obstruction to extending that particular potential unchanged to every positive width. It is not a negative closed walk and does not rule out a different all-width potential (`width_quantifier_audit.json`).

The per-edge continuous-width/Bellman search is floating discovery only; it found no numerical negative cycle in its seven graph scopes. Its near-zero Bellman slacks and violations of the finite-width potential are not exact all-width certificates (`continuous_timing_search_11_100.json`). An exact Sturm attempt for lambda `1/10` was run for more than 20 minutes and interrupted without producing a certificate or counterexample; its script and failure receipt are preserved. No conclusion is drawn from that attempt.

## 4. Result and remaining boundary

The bounded adversarial search found negative strips, exact non-polyconvexity, and exact failures of specific proposed transfers, but no exact negative compatible Jensen loop for F11. Exact graph potentials obstruct negative loops in the finite odd-carrier libraries; exact common-B minimization obstructs the 384 tested mixed-parity elementary squares; the fixed-background mixed-parity potentials apply only at four stated B values. The arbitrary-loop, arbitrary-width, and universal quasiconvexity questions remain open. No external proof review or novelty clearance is claimed.
