# Independent canonical-record and energy-interface check

## Scope
The path generator is borrowed, explicitly, from creative's deterministic construction. Energy, reconstruction, exterior-factorization and seam probes are independently implemented using exact integers E/.04=200P−|S|. Passing finite tests is not a proof of the full R200 contour envelopes or killed-generator theorem.

## Growth/history tests actually executed
`test_energy_records.py` examined27,756 finite initial configurations: all below-majority nonempty4×4 configurations, plus fixed-seed random and explicit winding cases on odd/even tori5,7,8,9,12. It made138,747 growth-record probes, including35,678 partial-bootstrap shapes,6356 periodic-seam shapes and2550 records where earlier erased history crosses the overwrite region.

Every probe passed:
1. Original full components factor exactly: E(X)=E(T)+E(X\T).
2. Outside overwriteU, X\T agrees with currentz.
3. With S=(X\T)∩U, X=(z\U)∪S∪T.
4. E(z)−E(X)<=E(U)−E(S)−E(T), the correct exterior-plus sign.
5. Periodic relative energy is bounded by its opened-seam counterpart.
6. The scaled partial-bootstrap gap is bounded by2C energy units .04 when both dimensions<=C.

The actual exterior-plus comparison was strict in50,184 probes, so it should not be replaced by an equality.

## Concrete lost-history shortcut counterexample
Among834 records with physical nearest-neighbor bonds crossing T∩U versus T\U, a small explicit example has T={(2,1),(2,2)} on a7×7 torus, with only(2,1) inU. Its true energy is1198 units .04; splitting T gives1598 units. The artificial split adds400×.04=16 physical energy, underweighting that erased history by exp16.

Thus full earlier ORIGINAL components must be encoded and Gibbs-factored BEFORE any split at the current overwrite boundary. Creative's current full-T prescription passes; the shortcut does not. The complete actual X,z,U example is saved in the JSON.

## Erosion/thermal-exterior tests
`test_erosion_exterior.py` independently checked33,748 deletion edges across32,091 finite initial configurations.25,180 edges had nonempty previously erased history. It verified the exact active-component identity

 E(current)−E(original)=E(active residual)−E(original active component)−E(full earlier history),

and reconstruction X=current∪upper-deletedU∪current-row-deletedD∪T.

There were1220 cases where the artificial full wire touches an unchanged original companion even though that companion did not touch the original active component. Therefore the full-state wire-insertion energy is NOT equal to the isolated active-wire insertion energy. Example: active component{(3,0),(4,1)}, wire{(3,0),(4,0)}; isolated insertion energy798 units versus full insertion398, a difference16. Full insertion is more favorable, but an equality-based proof would be wrong. Flow's stated method factors ORIGINAL components first and uses isolated active energy, which avoids this mistake and passed all checks.

## Analytic record observations
- Winding originals need no global bbox: a locally lifted connected prefix stops as soon as a span reaches400. Before that, both spans<400<L/2; a winding inconsistency cannot occur without first crossing that span threshold.
- Deletions are monotone until the first large component; additions are monotone thereafter. Each phase flips a site at most once, so length<=2n. First-majority stopping must be tested after every actual addition; already-plus bookkeeping steps are not transitions.
- In the postwrap phase, a completed cylinder of widthk is contained in the below-majority current state. Thus kL<n/2, hence k<=799 atL1600. The enclosing next column has width<=800, including early-majority exits.
- For a fixed current edge and geometric overwrite record, S and whole T reconstruct the original X uniquely. No extra original component label is needed for that inverse; summing S,T must still pay their stated marked/unmarked gas activities.
- A path may use an undirected edge once in deletion and once in addition. Sum phase contributions rather than declaring supports disjoint.

## Remaining obligations
These tests found no counterexample to the CURRENT full-T/seam/isolated-wire interfaces. They do not establish the numerical magnetic-strip/hull bounds, their high-perimeter tails, or the full Poincare/occupation transfer. Those certificates and exact record counts must still be integrated before a duration theorem is claimed.
