# Conditional canonical-path congestion for direct erosion

Status: reconstruction proof for the DELETION branch, conditional on the stated static hull envelope/inherited contour interface. It does not bound growth-branch currents or complete killed duration. It does preserve arbitrary unchanged thermal exterior and Gibbs-sums previous erased components.

## Path rule and domain
Select an original augmented plus component C. Erode it only if both of its contractible bbox side lengths are <=400. Keep this original C as the active component even if its remainder disconnects. Delete sites in descending lifted y, then ascending x. Finish C before selecting another component. Components with a larger side/winding are handled by a separate growth rule, not this proof. Assume the complete algorithm makes at most n deletions followed by at most n additions, hence length<=2n. This bound is valid for the direct-erosion/then-monotone-growth proposal; no hidden bootstrap merger histories are included.

At a deletion edge, the active remaining gate has no active plus above or left. Other original components cannot be physical neighbors of C. Thus its native neighbor count k<=2 and deletion rate >=1/(1+exp(.04)). Fix the full pre-deletion configuration eta and gate v=(x0,y0).

## Recoverable data, not a free record of all spins
For each initial configuration x whose path uses this deletion edge, let E be the union of previously erased ORIGINAL components. Let D be C's erased portion on row y0, and U its erased rows above y0. Then

 x = eta union E union D union U.

These inserted sets determine x uniquely; the active residual need not be separately labeled among eta's components. We overcount all compatible records below. Earlier erased original components all have bbox sides<=400 and are mutually nonadjacent to the original active component and unchanged exterior. Their weights factor, so dropping compatibility costs at most Z_A400/w(a)<=Z_A650/w(a)<1.000001, not2^n histories.

## Upper rows via a wired current row
Record C's original bbox width W<=400 and its left coordinate. Since v lies in the bbox, there are at most W left-coordinate choices, hence sum W=80200 width/anchor records. Let F be the full width-W row at y0.

Every augmented connected component of U connects in original C to the remaining gate through row y0. Thus U union F is augmented-connected. Inserting U sees active plus neighbors only on row y0. Replacing their pattern by the full wire maximizes physical plus contacts and lowers insertion energy. Original external components have no physical adjacency to U, so their unchanged presence introduces no missing attractive terms. Consequently

 w(eta union D union U)/w(eta union D) <= w(U union F)/w(F).

The wired shape has bbox W by h, h<=400, with its anchor fixed by F. The static filled-hull/holes envelope gives

 sum_U w(U union F)/w(F)
 <= sum_(h=1)^400 exp[K + Gamma_holes] exp[-E(rect(W,h))+E(F)]
 <=400 exp[K+Gamma_holes],

because E(rect(W,h))-E(F)=(h-1)(16-.04W)>=0. Here K<=877.768275 and Gamma_holes<6e-7. This is a CONDITIONAL completion bound relative to the actual residual, not an unsupported replacement of the residual by a filled rectangle.

## Unknown current-row prefix: exact run counting
D lies strictly left of the retained gate in an interval of length m<=W-1; allowing m<=400 is conservative. For k nonempty runs of D, all below-row contacts can be made plus to lower its insertion energy. At most one run additionally contacts the retained gate on its right. There is no above-row active plus at this stage. Hence

 E(eta union D)-E(eta) >=16k-.04|D|-16 delta,

where delta<=1 records that open right end. The number of binary strings of length m with k runs is binom(m+1,2k). Therefore

 sum_D w(eta union D)/w(eta)
 <= exp(.04m+16) sum_k binom(m+1,2k) exp(-16k)
 <=exp32 (1+exp(-8))^401,

whose logarithm is <32.134498. No2^400 row record is used. Allowing impossible patterns only enlarges this bound.

## Result for deletion currents
Use unnormalized native conductances c(eta,eta-v)=w(eta)q(eta,eta-v). Each initial path deletes a given site at most once, so this oriented deletion edge has at most one deletion occurrence. For the deletion contribution to canonical-path congestion,

 rho_delete <= (2n)(1+exp(.04)) *80200*400
                 *exp[K+32.134498+Gamma_holes+log(Z_A400/w(a))].

`erosion_congestion.json` reserves total thermal/hole logarithm1e-6 and gives

 log rho_delete <943.348529 <944.

This is below the new roughly1027 total budget but it is NOT a bound on rho_total: growth currents can contribute on the same undirected edge and must be added, not discarded. The source/target remain the actual hard all-minus and first-majority sets. No change of native clock is made.

## Finite checks and remaining conditions
`erosion_wire_check.py/json` checks all connected components in a4-by4 box under the fixed northeast augmentation. Along every actual erosion edge it verifies the reconstruction, wire connectivity, exact integer wired-energy inequality, row-run energy inequality and k<=2 deletion rate premise. This is finite evidence for the displayed general arguments, not a numerical R200 enumeration.

Outstanding: the static K theorem still uses the inherited filled-domain magnetic contour interface. The complete duration theorem additionally needs the growth branch, including pre-wrap marked component mass, arbitrary overwritten exterior bits, post-wrap configurations and final target stopping. None is inferred from this erosion lemma.
