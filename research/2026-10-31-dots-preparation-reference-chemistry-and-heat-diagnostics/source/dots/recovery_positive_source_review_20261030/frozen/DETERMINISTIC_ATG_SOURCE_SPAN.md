# Deterministic ATG source certificate and coherent good-pattern lift
2026-10-30. Independent source extraction plus new conditional span construction. No noisy autonomous apparatus theorem.

## Primary-source facts (compressed)
Bergamaschi–Liu, https://arxiv.org/html/2411.04405v1, sections 4–5: equations 21–23 cancel the raw outcome from corrected stabilizer signs. Definitions 18–20 give recovery depending on outcomes and repair depending on bulk error. The inferred bulk error has minimum weight at fixed metasyndrome. Equations 26–27 define the two mismatch graphs. Lemmas 5.2–5.4 prove componentwise minimum-weight comparisons and a boundary repair comparison; equations 32,39 give half-occupied bulk witnesses and quarter-occupied completed witnesses. Equation 44 gives zero syndrome for the collapsed operator of each nonbridging component. A component with nontrivial logical class must therefore have at least distance d vertices. Lemma 5.5 counts boundary-anchored unions, while Lemma 5.6 counts logical witnesses.

Caution: the sentence in Lemma 5.4 equating equal syndrome with stabilizer equivalence is too strong. Equal syndrome gives a normalizer difference; its minimum-weight argument needs only equal syndrome. Distance is used later to exclude a nontrivial logical class.

## 1. Fix the decoder before considering any noisy state
Use a fixed lexicographic tie rule for the minimum-weight bulk estimate beta(y), where y is ONLY the metasyndrome. It must not consult other raw outcome bits. Fix all subsequent minimum-weight boundary representatives similarly. Let M denote the binary metacheck matrix and let L collect the bulk X legs of a complete independent set of target Bell stabilizers. Let sigma denote their Pauli commutation vector on the two output blocks.

For bulk Z-defect pattern eta and supported recorded outcome m, M m=M eta. Choose the fixed physical-frame map P(m) satisfying sigma(P(m))=L(m+beta(M m)). A solution exists for these attainable outcomes; fix it once. The uncorrected boundary signs are L(m+eta), so after the frame they are

    L(m+eta)+L(m+beta(M m)) = L(eta+beta(M eta)).

This expression is independent of m. A complete pure Bell stabilizer group determines the state ray, so choose E(eta) with this sign vector. Every supported outcome yields the SAME E(eta)|Bell>, up to a scalar phase and branch amplitude. A physical boundary Pauli E_B multiplies this residual; commuting it through P(m) changes only a phase. Bulk X parts of a general Pauli affect only outcome-dependent scalars. This is an exact amplitude statement, not an assertion of a Pauli-mixture noise model.

Without syndrome-only tie-breaking, beta can vary among equally light minimizers as m changes. The outcome-independent repair claim is then not supplied by the cancellation alone. This is repaired by an explicit decoder convention, not by averaging outcomes.

## 2. A deterministic, outcome-independent good-pattern predicate
For each eta, construct beta as above. In each of the X/Z syndrome graphs mark bulk vertices where eta and beta differ. Choose minimum-weight boundary syndrome repair G_X or G_Z. Add its boundary support to the graph, giving completed marked components.

Call eta good at radius t if in BOTH sectors:
1. No bulk mismatch component bridges the two boundary layers.
2. Every completed marked component has fewer than d vertices.
3. The combined boundary repair satisfies |G_X|+|G_Z|<=t.

For a completed component K, telescope the metachecks along its layers and include its endpoint repair. The collapsed boundary operator has zero base-code syndrome. Its weight is at most |K|<d, hence it is a stabilizer, not a nontrivial logical. Multiplying components leaves no logical mismatch. Consequently E(eta)=G_X G_Z can be selected with support size at most t. The predicate uses only eta, fixed graph, and fixed decoders, never the random valid outcome.

The criterion may be checked by exhaustive decoding. It does not claim efficient computation or supply a physical success flag.

## 3. An upward-closed bad-support witness construction
For a support set A of possible effective bulk defects, exclude the following witnesses in either sector:
(a) A connected bulk set K of size at least T with |A intersect K|>=|K|/2.
(b) A connected completed-graph set K of size at least d with |A intersect bulk(K)|>=|K|/4.
(c) A union W of connected sets, each touching a boundary, with at least a selected boundary vertices, |W|>=2a, and |A intersect bulk(W)|>=|W|/4, where a=floor(t/2)+1.

Then every eta supported inside A is good at radius t. A bridge would produce (a) by local minimum-weight replacement. With bridges excluded, each completed component has boundary-repair weight at most its interior data mismatch weight; together with local minimum-weight replacement this bounds its size by four times its true defect count. A large component would produce (b). If either |G_X| or |G_Z| exceeds t/2, take all components touching an a-element subset of that repair: their union produces (c). This argument is hereditary in A. It does not confuse small connected components with small TOTAL repair weight; condition (c) is essential for a low-density receiver.

The threshold constants can be deliberately weakened when applying witness counting. For example, if Pr[B subset A]<=q^|B| and graph degree is bounded, a fixed size-s witness requiring s/4 occupied sites costs at most 2^s q^(s/4). Counting boundary-rooted unions gives a geometric series times a factor exponential in a, followed by choosing a roots among 2n boundary sites. Taking a proportional to n and q sufficiently small yields an exponential-in-n density tail. Bridges and logical witnesses instead give volume times geometric tails starting at T and d. This estimate is for the positive distribution of commuting defect-projector outcomes; it needs no signed channel expansion.

## 4. Good-pattern projection really gives a common coherent span
Suppose the completed Clifford source before ideal measurement has an orthonormal defect basis |z> and a projector Pi_good=sum_good z |z><z|. Suppose each such basis vector propagates to a Pauli pattern (eta_z,E_B,z) satisfying the deterministic criterion, and |E_B,z|<=u. Retain an arbitrary bath/reference.

Apply the SAME measurement instrument and the SAME controlled frame P(m) to every basis vector. For each actual m, linearity maps the full projected subspace into

    span{ E |Bell> : |supp E|<=t+u } tensor bath.

Different z components may interfere, have different scalar amplitudes, or become entangled with the bath. None changes this span inclusion. There is no coefficient-sum penalty and no independent-branch assumption. If Tr[(I-Pi_good)rho]<=epsilon, the unnormalized good projection differs from rho by trace norm at most 2 sqrt(epsilon); subsequent physical channels cannot increase that distance. This is an incoming-state statement. A diamond-norm claim for an arbitrary-input computation requires the good-projector tail uniformly on all retained inputs, which has not been proved here.

## 5. Fixed-baseline density in the same actual-record branch
Let b select the local adjacent record bits that define output-check baseline signs. Count every effective bulk measurement flip and actual capture flip in eta; do not silently count a physical bulk Z defect neither as an outcome flip nor in the baseline identity. Then the uncorrected boundary syndrome is b(m)+b(eta)+sigma(E_B). If E_total=E_B E(eta) is the corrected residual,

    D(m):=b(m)+sigma(P(m))
         =sigma(E_total)+b(eta)+sigma(E_B).

Thus |D(m)|<=nu(|E_total|+|E_B|)+|b(eta)| for check incidence nu. For fixed m the left side is one fixed bitstring shared by ALL coherent components. A uniform good-pattern bound on t,u and the number of terminal-baseline flips therefore supplies both a common correctable quantum span and a common small-D target sector. Bound |b(eta)| by a separate local terminal-defect density event; the absence of logical clusters alone does not bound it.

If extra capture hardware spreads faults, its lightcone/support map must be included before applying this statement. Neither reliable capture, legal classical-memory initialization, native fixed-baseline drift, delayed frame computation nor physical completion is furnished by this source certificate.
