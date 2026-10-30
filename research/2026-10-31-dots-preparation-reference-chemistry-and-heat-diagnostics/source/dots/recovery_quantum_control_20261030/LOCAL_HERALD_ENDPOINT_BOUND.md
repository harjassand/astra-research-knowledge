# Local endpoint legs cost local dimension, not inverse herald probability
2026-10-30. Exact operator lemma, not an actual autonomous endpoint theorem.

Let C_X=rowspan H_X, r=dim C_X, p=2^{-r}. Let P_a be ANY attainable X-check syndrome projector, so its computational matrix entries equal p times a signed C_X-coset adjacency matrix. Let T_Z be full DATA computational dephasing. Keep an arbitrary bath R untouched by T_Z.

For footprint S define h_S=dim{g in C_X:supp(g) subset S}. For any fixed computational x, let Q_(x,S) project onto strings agreeing with x outside S. Then

 ||Q_(x,S) P_a Q_(x,S)|| = p * 2^{h_S} <= p * 2^{|S|}.

Proof: within that subcube, matrix entries vanish unless their difference belongs to C_X(S). Each coset block is p times a rank-one signed character matrix of size |C_X(S)|. Its sole nonzero eigenvalue is p |C_X(S)|. This proof also covers dependent original check presentations by using the actual stabilizer rank r.

For an arbitrary operator E supported on DATA S and the ENTIRE retained bath, define

 Phi_E(rho)=(P_a tensor I) E (T_Z tensor Id)(rho) E^dagger (P_a tensor I).

E(|x> tensor I_R) lies in Q_(x,S) tensor R. Hence the compression bound gives, as an operator inequality on R,

 <x|E^dagger(P_a tensor I)E|x> <= p 2^{h_S} ||E||^2 I_R.

Consequently Phi_E is CP with

 ||Phi_E||_diamond=||Phi_E^*(I)|| <= p 2^{h_S} ||E||^2.

This is a full operator-norm statement including arbitrary incoming DATA/bath correlation, not a Pauli-mixture or probability argument.

For E on S and F on T, with possibly different attainable projectors P_a,P_b, the bilinear map

 Phi_(E,F)(rho)=P_a E T_Z(rho) F^dagger P_b

obeys

 ||Phi_(E,F)||_diamond <= p 2^{(h_S+h_T)/2} ||E|| ||F||.

Indeed write its paired Kraus legs A_x=P_a E |x><x| and B_x=P_b F |x><x|. The operator-space Cauchy–Schwarz bound is ||sum_x A_x (.) B_x^dagger||_cb,1 <= ||sum_x A_x^dagger A_x||^(1/2)||sum_x B_x^dagger B_x||^(1/2); the two preceding CP bounds apply, including bath identities. The same proof after tensoring an arbitrary reference gives the diamond bound.

After division by the clean success p, each fixed localized fault leg costs at most an exponential in its local footprint, not exp(r). A bounded-support superoperator can be decomposed into finitely many such system legs with an additional dimension-dependent constant. This is NOT a proof that an arbitrarily long native fault history has bounded footprint.

## Missing physical links
- Actually reduce each endpoint fault to bounded DATA/bath operator legs after the same complete twirl, with any record faults represented by the correct attained/declared syndrome projectors and full classical output.
- Pay spread through extraction, resets, dirty prefixes and false acceptance. An ideal shifted projector is not automatically the real faulty acceptance instrument.
- Establish the normalized fault-family SUM norm, rather than multiplying individual estimates across an unproved factorization.
- Establish a lower success rate under the actual noisy instrument. No CP domination by a hypothetical no-fault trajectory is asserted.

Thus this lemma removes a crude inverse-success upper-bound penalty for local legs, but does not establish the whole heralded native factory.
