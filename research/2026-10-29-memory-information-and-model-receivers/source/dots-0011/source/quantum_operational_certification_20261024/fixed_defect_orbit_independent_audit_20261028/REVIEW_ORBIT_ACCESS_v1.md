# Independent review: complete fixed-defect subgroup-orbit access

28 October2026. **Accepted at the explicit fixed-defect representation/access scope**, incorporating the author's separate `OPERATIONAL_SCOPE_ADDENDUM_v2.md`. This receipt covers Sections1–6 of `GOVERNING_ORBIT_FRAME_v1.md`, and implementation-error bookkeeping below. The random-code moment bounds, physical error-weight conventions and total soft-polar error theorem are covered by separate reviews, not granted here. Original author files are unchanged.

## Load-bearing representation argument

Use normalized operator inner product Tr(A†B)/d, with A:V_lambda→V_mu. Under H=S_(k−j), ordinary Young branching is V_lambda=⊕alpha V_alpha⊗C^(a_lambda,alpha), and similarly for mu. Every intertwiner is identity on a common V_alpha times a multiplicity matrix unit. Therefore the displayed prefix-preserving partial isometries form the COMPLETE H-invariant space, including every multiplicity pair. Their squared ordinary HS norm is d_alpha, so scaling by sqrt(d/d_alpha) makes them orthonormal in the declared inner product.

Frobenius reciprocity gives d<=L d_alpha for every occurring alpha, since V_lambda embeds in Ind_H^G V_alpha and L=[G:H]. The normalized seed operator norm is consequently at most sqrt(L). This is an operator-norm bound, not an HS-to-operator conversion hiding sqrt(d). Also the number of lambda suffix paths is at most L, and likewise for mu, so seed count s<=L² and M=Ls<=L³. All these bounds are valid for unequal lambda and mu.

For the full seed basis, its operator-space projector is P_H. Summing conjugates over representatives gH gives BB†=L times the full-group twirl of P_H. In the isotypic decomposition Hom=⊕nu V_nu⊗multiplicity, the H projector is P_(V_nu^H)⊗I_multiplicity. Thus the frame operator equals L h_nu/d_nu on EVERY copy, not just one selected intertwiner. Branching to the trivial row(k−j) shows h_nu>0 exactly when nu_1>=k−j. This proves full low-defect support.

The induced permutation representation has dimension L and contains h_nu copies of V_nu. Hence d_nu h_nu<=L, giving L h_nu/d_nu>=h_nu²>=1; the upper bound L follows from h_nu<=d_nu. There is no hidden exponential frame conditioning. This mechanism resolves the actual missing-copy failure of the earlier transposition family, rather than assuming that family was already complete.

## Central coefficient correction

The coefficient module is Ind_H^G1⊗C^s. Left multiplication acts as a permutation of cosets while leaving seed labels unchanged because the seeds are H-invariant. Consequently B is an intertwiner for this known action. Applying Z=Σ_selected sqrt[d_nu/(L h_nu)]Q_nu on the coset register gives A=B(Z⊗I_s) and AA†=Pi_selected. The coefficients satisfy0<=Z<=I. No trace estimation, hidden Gram oracle, source tomography, selected error-basis reconstruction or quantum sampling is used in this construction.

The chosen set can have zero image even if s>0: for example lambda≠mu and selecting only the trivial sector. The author's addendum correctly excludes N=0 from the positive-reference beta formula. Operationally the same filter applied to W_A=0 yields its fallback; selected physical weight is then zero. Detecting the unknown multiplicity rank N is not needed to execute the decoder. The s=0 case can be caught directly from the finite branching enumeration.

## Actual polynomial classical computation

Cosets are ordered j-tuples of distinct images; L=(k)_j. Their adjacent-generator matrices are explicit permutations. The commuting Jucys–Murphy matrices on this L-dimensional module have integer spectra in[−k,k]. At step i, use the exact Lagrange polynomial for each possible integer content c:

P_(i,c)=product_(a in[−k,k],a≠c) (J_i−aI)/(c−a).

Unused integer eigenvalues simply produce zero blocks. Refine existing joint projectors with these commuting projectors and discard exact-zero blocks. At every stage there are at most L nonzero blocks, since their positive integer ranks sum to L. There is no enumeration of all k! tableaux. The content sequence determines the final Young shape. Grouping the resulting projectors gives the exact Q_nu.

Denominator bit lengths per spectral step are O(k log k); at most k refinement steps produce polynomial bit lengths. Matrices have dimension L, and products, rational zero tests and rank traces therefore have polynomial bit complexity for fixed j. A numerical eigensolver with unresolved collisions is unnecessary. A lone central class-sum eigenvalue does not distinguish all shapes, as the preserved author's failed check correctly records.

The dilation [[Z,sqrt(I−Z²)],[sqrt(I−Z²),−Z]] is a known unitary of dimension2L, with coefficients expressed through exact rational projectors and explicit scalar square roots. Compiling this known small matrix to a declared unitary error requires polynomial gates and logarithmic precision. Rounding an arbitrary noncontractive matrix and calling it a physical block would be invalid; the implementation must synthesize the actual unitary dilation. Approximate gates remain unitary, and their errors are paid by telescoping actual circuit calls.

## Seed and representation circuits, without a uniform huge prefix bank

A seed acts on a prefix already coherently present in the supplied input tableau. Compare the suffix with its known path, replace that suffix on a direction-tagged padded register, and leave the prefix untouched. Complete unmatched branches to a reversible operation. A controlled rotation of amplitude sqrt[d/(L d_alpha)] supplies the desired projected block F_s/sqrt(L). No uniform superposition over all d_alpha prefix tableaux is prepared or stored.

Hook-formula dimensions are integers with polynomial bit length in k. Adjacent Young generators act on at most a tableau and its valid adjacent-label swap; contents and validity are computed reversibly, and the two-dimensional block has computable inverse-axial-distance coefficients. A canonical coset permutation has a polynomial-length adjacent-transposition word. Controlled choices over the polynomial number M of labels remain polynomial, with no exponentially indexed quantum memory.

If the supplied code circuit uses binary ranks rather than tableau strings, general-shape rank/unrank is also polynomial: remove labels k,k−1,... in a fixed corner order; the interval size for a candidate corner is the hook-formula dimension of the remaining shape. Branching makes those intervals partition the current dimension. Compute the polynomially many hook products at each of k steps, subtract the selected interval offset and record the chosen row. This needs no table of all subdiagrams. Its reversible version supplies the conversion on superpositions. A code circuit C and its inverse still remain an explicit dependency; no random orientation is inferred from a block projector alone.

## Paid block normalization and finite precision

The stronger normalization alpha=sqrt(LM) is valid. Apply the normalization-one Z dilation first on the input error label; use the controlled raw seed/orbit block divided by sqrt(L); project the label onto the known uniform M-state, contributing1/sqrt(M). These are coherent projected unitary blocks, not a physical postselection repeated at every query. The resulting block is exactly W_A/alpha. Expanding each corrected column into a separate LCU would give a weaker normalization, but is unnecessary here.

For clarity, a direct coefficient perturbation admits a dimension-free polynomial bound. Let W_B=[F_(g,s)C] be the uncorrected row operator. Since every column operator has norm at most sqrt(L), ||W_B||<=sqrt(ML). Therefore replacing Z by Z+Delta on its coefficient register changes the raw row operator by at most sqrt(ML)||Delta||. There is no factor sqrt(d) or sqrt(D). This auxiliary estimate does not authorize an unphysical noncontractive approximateZ; actual implementation uses the unitary dilation and its circuit error. Each QSVT query, inverse, controlled reflection, code call and synthesis gate must contribute to the total implementation allowance. This review does not claim the resulting polynomial gate count is experimentally modest.

## Redundant labels and correct support bookkeeping

Because AA† is a projector, abstractly A=F V† for an orthonormal operator basis F and an isometry V. This is only a proof coordinate change; neither F nor V is an implementation oracle. The physical error weight becomes V T V†, supported on VV†. The row operators satisfy W_A=W_F(I⊗V†). Any odd singular-value filter with f(0)=0 consequently satisfies R_A=(I⊗V)R_F. Tracing error labels gives the identical success channel, and the failure effects also agree.

The redundant Gram is not close to identity in an unweighted operator sense: it has structural null directions. Nevertheless the supported weighted expression with I_M is legitimate:

Tr[(V T V†)(G_A−I_M)²]=Tr[T(G_F−I_N)²],

with the corresponding logical identities understood. The weight annihilates the unused complement. Replacing N by M in the orthonormal Haar equality or allowing arbitrary unsupported M-dimensional weights would be wrong; using M only in conservative bounds is different.

## Independent executable challenges

No author implementation is imported. `check_orbit_v1.py` builds general Young representations, common-prefix seeds, all coset orbits and the coefficient-module JM decomposition. It covers:

- lambda(3,1), mu(2,2), k4: selected rank6 from36 orbit columns;
- lambda(3,2), mu(3,1,1), k5: rank21 from100 columns;
- lambda=mu=(4,2), k6: rank34 from180 columns;
- lambda(4,2), mu(3,3), k6: rank15 from90 columns.

The third fixture contains the additional (4,2) multiplicity copy that transpositions missed. An independent character-sum computation in `check_multiplicities_v1.py` confirms all selected ranks and multiplicities; the second fixture also contains multiplicity2 in (3,1,1). Central preconditioning makes the operator-space frame a projector to within3.5e−15. The explicit bounded odd cubic filter verifies the redundant/orthonormal recovery isometry relation within4.7e−16. These are floating finite fixtures supporting the analytic argument, not outward-rounded certificates or compiled QSVT execution.

## Scope retained

This is k^(O(j)) access for fixed defect j, including arbitrary local shapes and unequal dimensions. It is not uniform polynomial complexity when j grows extensively. It removes the rare exact-rectangle restriction but not the source's low-environment-defect requirement. Generic positive-entropy iid mixed sources need not put useful mass in these sectors. Rejected source weight, code-block remainder, approximate-design error, control/storage costs, physical noise assumptions and actual yield remain separate obligations.
