# Independent review: canonical local polar orientation

28 October 2026. Reviewer `producer-workspace/review_effect_only_acquisition`. **PASS for the exact algebraic extension, with the scope below.** The author source is unchanged; the accompanying receipt binds its bytes. This is not a finite statistical acquisition theorem.

## Canonical target and local gauge

With Bloch columns, right polar T=O S, S=(T^T T)^(1/2)>0, gives O in SO(3) precisely when det T>0. A qubit unitary U implementing O exists. Postcomposing E by Ad_Udagger is a physical operation, so its data (S,O^T t) are CPTP without any claim that the dissipative inverse is CP. Factoring the product U into V proves the displayed source rewrite exactly.

The original V has the stated local-unitary ambiguity. Under V'=V tensor W and T_i'=R_i^T T_i for proper rotations R_i of W_i, the right positive factor S_i is unchanged and O_i'=R_i^T O_i. Thus V_eff'=V_eff up to irrelevant unitary phases. This checks that the convention actually fixes the specified gauge; it is not an assertion that an arbitrary black-box source can be certified to belong to this family. Fixed labeled input factors are part of the interface. Local supports are unchanged as whole Pauli algebras, although individual generators may have smaller support.

## Contrast, partial trace and Gram proof

For signed axis j, the contrast is E_i'(sigma_j)/2 tensor the other averaged outputs. Inserting B_a and R_i gives exactly sum_a S[a,j] B_a R_i, including the 1/2 normalization. R_i commutes with its own full Pauli algebra because it contains identity on that input factor. It need not commute with other factors' algebras. If B_a is supported in J, partial trace obeys Tr_Jc(B_a R)=B_a,J Tr_Jc R, and commutation similarly descends to J.

For a!=b, B_a B_b is plus or minus i times the third Pauli. Conjugation by a distinct own Pauli negates this product while leaving R_J^2 fixed. Cyclicity of trace forces its trace to zero; for a=b the trace equals g=Tr R_J^2>0. Therefore G=g S^T S=g S^2, with REAL positive definite Gram matrix, and G^(-1/2)=S^(-1)/sqrt(g). Column-index contraction yields F_j=B_j R_J/sqrt(g). This is Hermitian by commutation. Positivity of R_J makes its sign exactly B_j. Without scalar R_J, F_j itself generally is not unitary/reflection; the source correctly keeps the sign operation.

## Strict positivity and boundaries

If E(I/2) has rank one, E(rho)<=E(I)=2E(I/2) for any density rho. Positivity and unit trace imply every E(rho) is the same pure state, so T=0. Thus invertible T ensures E(I/2)>0. Since every spectator has this property, the finite global R_i is strictly positive; unitary conjugation and partial trace preserve strict positivity. No usable quantitative floor follows without additional instance bounds. The source correctly separates finite guards and backward-cone floor analysis.

A negative-determinant physical example exists: the equal mixture of X,Y,Z conjugations has T=-I/3. Its polar orthogonal factor is -I, not a proper rotation; sending all three Paulis to their negatives violates XY=iZ. Singular T gives a singular Gram matrix and the proposed whitening is undefined. Neither boundary is a general impossibility theorem for all recovery objectives. Different conditional channels need not share one common R and S, so averaging them cannot silently inherit this algebra.

## Independent executable fixture

`local_polar_identifiability_independent_check_20261028.py` uses exact symbolic rational/surd arithmetic, three physical qubits, rotated amplitude damping with non-diagonal positive polar S, a CNOT output mixer, and nonflat full-rank spectators. It verifies the actual channel rewrite on a matrix basis, all three signed contrasts, a proper partial trace to a two-qubit envelope, the Gram identity, the whitened common factor, and the final sign identity. It checks whitening is not already a reflection and includes the negative-determinant CPTP and singular examples. Initial development used a structural symbolic equality where expanded equality was required; the completed check compares the actual matrix difference to zero. This was a test-expression issue, not a changed author theorem.

These are exact fixtures with zero source draws. No finite estimator, perturbation guard, controller compiler, hardware operation or sample advantage is received here. General source-family membership, unknown support, conditioning, source drift and finite physical precision remain the separate acquisition obligations.
