# Independent review of original global cut-energy acquisition

Read ACTUAL_ENERGY_PROPOSAL.md and UNROOTED_MARKED_REFINEMENT.md in n1722_global_walk_trial_20261113. The change-of-variables, refined multiplicity and missing-image algebra pass, conditional on the explicitly inherited cut geometry and authorized auxiliary-core acquisition primitive. This review does not silently certify a new core sampler or the entire global walk-envelope derivation.

## Accepted law

For each actual structural cut edge, its old affected outer-domain tuple is fixed. Flipping the full domains is an involution, so the inverse configuration y is unique. The inherited map y in M and the thermal full-domain ratio w(x)/w(y)<=product b are essential; a pure-shape or independent-interior argument is not substituted.

In the refined scheme, every actual contour of physical perimeter P has P distinct rooted physical-edge encodings, and all j! orders of distinct domains are present. Per ordered rooted tuple, the proposal weight product(b/P)*(3S/j!) cancels with uniform selection among3S boundary marks. Requiring the FIRST mark yielding a proposed gate leaves exactly one mark for EACH representation, not one mark across the whole equivalence class. Each representation therefore contributes g/[Q Z_aux j! product P]; summing its j!product P representations yields EXACT g/(Q Z_aux).

Selecting only canonical roots/order after already dividing by their multiplicity would undercount; the refined note correctly says not to do that. Likewise accepting every repeated boundary mark would overcount; the first-mark condition correctly removes it.

## Missing-image bound

Fix a tuple/gate representation. Inverse flipping is injective on its accepted physical sources. On omitted sources y in M\C_r', sum the SAME actual w(y), use the full-domain ratio bound, and then sum the positive tuple/gate overcount. This gives Q Z_M mu_M(C_r'^c)<=Q Z_M u(r'). No distributional claim about actual entrance currents or the original source is needed. The auxiliary core is a proposal only; original A and its clock stay untouched.

Long-contour tails, target crossings inside M, and reservoir/target overlap are separate original trial-energy terms. They must remain included in DeltaW, as the note does. A capacity lower ell then converts DeltaW into a relative full-trial energy error. Low acceptance is not removed: the available original lower and complete envelope still give an enormous exp(O(R)) rejection bound. Higher precision only controls accepted-law bias; it does not make the number of attempts polynomial.

## Independent executed refined test

`check.py` reconstructs the actual3x3 rational heatbath graph separately and verifies all126 structural birth edges. It explicitly enumerates8,856 rooted/order representations, constructs all3S boundary marks, verifies the canonical first mark exists, and checks the summed accepted density is g/(Q Z_aux) exactly. The resulting SMALL-instance acceptance is about0.03438. This is not a large-contour execution, not evidence for practical R200 acceptance, and not a W/C theorem.

## Outcome

This is a genuinely global trial-energy acquisition INTERFACE, materially different from a sampler supported only on a convenient canonical morphology. Its retained accepted law and missing-image correction are earned under the listed existing primitives. The main missing result is affordable envelope-to-energy/capacity ratio and a runnable large-instance implementation with the original decision-time costs paid. No breakthrough claim follows from the present exponential certificate.
