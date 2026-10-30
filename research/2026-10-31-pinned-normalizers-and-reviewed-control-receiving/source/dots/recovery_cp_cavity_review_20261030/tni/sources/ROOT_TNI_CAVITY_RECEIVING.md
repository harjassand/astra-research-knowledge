# CP/TNI cavity receiving for a processor beside a protected native bank
30 October 2026. Root construction candidate, independent review pending. This is not permission to condition on an unobserved successful event and pretend the noise is unchanged.

## 1. A precise extension of the already accepted cavity algebra
Let the finite bounded scheduled processor generator be

 K(t)=L_id(t)+K_B,raw(t)+sum_e M_e(t),

on processor S and retained B. The TOTAL generator has CP and trace-NONINCREASING propagators on every interval. Each M_e is HP, supported on at most q processor sites plus arbitrary B, with the same bounded per-processor-site incident diamond-norm sum. Individual M_e need not annihilate trace. Intended L_id gates are the usual CPTP generators on disjoint active processor blocks.

For selected processor blocks R define the same normalized partial-trace generator projection P_R and

 K^R=L_id+P_R(K-L_id)=P_R K+sum_(j in R)L_id,j.

The reduced short-step maps Tr_R exp(hK) E_R are CP/TNI, equal the identity at h=0, and have derivative Tr_R K E_R. Their repeated-product limit is CP/TNI. Hence each K^R and each convex cavity interpolation is CP/TNI, with complete norm at most1 between derivative insertions.

The remaining accepted proof is unchanged: a term NOT touching a differentiated processor block is killed by P_j-I whether or not that term is trace annihilating. Norms of the projections are still at most1. The same ordered-partition estimate, rooted recursion, Möbius cancellation and fault-location LINEAR-SPAN support therefore give

 ||sum_(F contains S0)E_F||_diamond
 <=[2*3^(q-1)g eta tau]^(|S0|/q).

E_empty is the ideal processor circuit tensored with a TNI bath map. Exact-target approximate-gate slots are received in the same way: fixed difference insertions multiply norms, while all intervening maps are CP/TNI contractions. Strength becomes product_(j in S0)(x+delta_j).

This is a statement for a whole CP/TNI generator, not arbitrary nonpositive conditional evolution. No positivity of an individual local M_e or signed fault map is used. Bounded finite-dimensional/domain assumptions remain as in the accepted core.

## 2. Concrete native-killed application
During protected computation of classical commands, let the native DATA bank(s) run their own correction and let the ordinary processor run its disjoint scheduled gates. There are no nominal processor-DATA gates in this waiting phase. Let P be the actual canonical native memory cut, independent of processor variables. The complete-loss killed joint dynamics is CP/TNI. On its range it factors as identity on the native logical subsystem times a TNI dynamics of native auxiliary variables, processor and bath.

Because the processor intended gates commute P, they remain the same intended gates after compression. The nominal native part is a B-only generator. Compressing each actual local weak perturbation to P changes its action on B but does NOT enlarge its processor support; the complete compression has diamond norm at most1. Its individual trace-annihilation may be lost, which is why section1 states the extension explicitly. Any complete-loss definition must be the actual P L(P dot P)P restricted generator, retaining original losses; no outgoing gains are reintroduced by normalizing the state.

Thus the ordinary processor's fault expansion and disjoint-rectangle recursion can be performed on the SAME native-killed dynamics. Every computation-good path acts as the intended processor logical operation AND native logical identity, with arbitrary common retained auxiliary coefficients. It is unnecessary, and generally invalid, to combine two marginal logical guarantees by declaring the other live logical subsystem an inert reference.

The native full-versus-killed error is separately bounded by its actual operator boundary proof, uniformly over the admitted processor input/domain. Its initial native energy/BUSY moment bounds must be operator-uniform on that processor space; a state-dependent assignment correlated with the unknown native logical input cannot be smuggled in. A product source, or a common logical/module chart with the stated positive auxiliary receiving contract, is required.

## 3. Trace loss and what a receiving proof must pay
Let epsilon_cut bound the actual full channel minus the native-killed channel on the admitted source. Let b_proc bound the killed processor's complete bad-path map after the same actual scheduled FT analysis. The killed processor channel is not TP, so the old trace-defect normalization cannot set its effect to I exactly.

Instead, native loss has effect norm at most epsilon_cut on the declared source. In the common decoded logical chart the good processor/native map factors as the desired logical operation(s) times a signed auxiliary map. Its trace defect is bounded by epsilon_cut+b_proc. Add the reduced bad part and the original full/killed comparison, or use an explicit positive auxiliary-factor repair. A safe normalized logical error budget is therefore a fixed constant times epsilon_cut+b_proc, with the exact factor stated by the final composition. Do not discard the native loss or renormalize on survival.

This extension only supplies the concurrent waiting/computation interface. It does not establish a native logical measurement, reliable raw-input encoder, distributed physical feedforward or an autonomous command scheduler. Those actual operations still require their own correctable-span and resource proofs.
