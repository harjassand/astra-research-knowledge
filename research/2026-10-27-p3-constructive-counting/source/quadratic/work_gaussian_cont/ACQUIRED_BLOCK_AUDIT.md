# Independent adversarial audit of the acquired-block phase theorem

27 October 2026. Audited `work_dense_cont/ACQUIRED_BLOCK_PHASE_THEOREM.md`, `cubic_structure_compiler.py`, and `acquired_block_phase_checks.py` against their actual algebra and executable behavior. The phase-counting consequence remains conditional on the governing OpenAI manuscript and the separately audited phase-product extension.

## Finding

I found no remaining mathematical gap in the stated acquired-block theorem after the two implementation repairs below. The characteristic-two idempotent procedure is complete, the radical normalization satisfies e+d<=n, the cross-quadratic graph is intrinsic for a radical-free core, and the resulting phase-program size is bounded by the stated W. The compiler supplies a computed sufficient certificate; it does not establish a subexponential bound for every dense cubic.

The distinction between polynomial acquisition and exhaustive finite validation is essential. The accompanying small checks do not execute the source's asymptotic phase counter or establish practical acceleration.

## 1. Two defects found and repaired

### Missing retained elimination certificates

The proof stated that every affine substitution and equality was retained, but the first executable stored only numerical dimensions and power-of-two factors. That was a documentation/implementation mismatch: the transformations were computed but discarded.

At the parent's request, I repaired `cubic_structure_compiler.py`. Each radical round now retains:

- its input polynomial and variable count;
- radical basis, complement columns, and full invertible coordinate columns;
- each Gaussian pair's variable indices, affine A and B terms, and output polynomial;
- the remaining radical variables and their affine equations;
- the residual polynomial before affine substitution;
- the affine offset and kernel columns;
- the output polynomial, variable count and power-of-two multiplier.

In inconsistent cases the executable additionally retains an explicit subset of affine equations whose XOR is 0=1, together with prior valid rounds. This is an actual zero-sum certificate rather than an unsupported flag. All retained objects have polynomial size: cubic coefficient lists have O(n^3) entries and there are at most n elimination operations/rounds.

### Exponential diagnostic inside the acquisition function

`acquired_block_phase_checks.acquire()` originally called `edge_expansion()` unconditionally. That function enumerates all 2^t subsets of the acquired t-block graph. For t=Theta(n), this contradicted the advertised polynomial acquisition cost, even though graph expansion was not used anywhere in the theorem.

I moved the expansion computation out of `acquire()` and into the fixed small-fixture validation routine. The polynomial compiler now returns the graph and its charged edge weight without enumerating graph subsets. The finite K3,3 expansion measurement is still present in the fixture results. The independent checks also assert that acquisition itself returns no expansion diagnostic.

## 2. The characteristic-two centroid step is complete

The cubic leading part defines an alternating trilinear form T through third Boolean derivatives. No division by 3! is used or permissible here. Its squarefree cubic coefficients are exactly its values on triples of distinct coordinate basis vectors.

For zero-radical T, let C be the full set of endomorphisms transferable between all three slots. The proof of commutativity is valid in characteristic two:

    T(ABx,y,z)=T(Bx,Ay,z)=T(x,Ay,Bz)
             =T(Ax,y,Bz)=T(BAx,y,z).

Thus (AB-BA)x lies in the radical for every x, so AB=BA. Transferring one more time proves closure under products, and I belongs to C. The code's basis equations describe all of C, with no selected-subalgebra assumption.

Because the centroid matrices commute, E -> E^2+E is F_2-linear on C. Its kernel is exactly the set of F_2-rational idempotents. This argument does not assume that C is semisimple, split over F_2, or a product of scalar algebras. Nilpotents do not create an omitted nonlinear condition.

When an idempotent basis is processed, every surviving piece P is acted on by each basis idempotent as either 0 or P. Every other idempotent is their F_2-linear combination and therefore also acts as 0 or P. Hence no further rational idempotent can split that piece. Conversely, any cubic direct-sum projection transfers between the slots and belongs to C. The acquired images are consequently the complete primitive direct-sum blocks over F_2, not merely some found blocks.

The qualification "over F_2" matters: a primitive centroid component can be a larger finite field. Its absence of nontrivial F_2-rational idempotents is correct, not a failure to diagonalize over an extension. I checked explicit centroid-field examples F_4 and F_8 in addition to genuinely nonsemisimple examples.

## 3. Radical elimination, repeated reduction and normalization

After choosing a complement to the third-derivative radical, all cubic monomials containing a radical coordinate vanish. Thus the coefficient functions A and B in an eliminated radical pair are affine, so replacing st+sA+tB+C by C+AB preserves degree at most three and adds only quadratic terms involving remaining radical variables.

Suppose a round starts with n=d+2p+q variables, where d is the nonradical complement dimension, p Gaussian pairs are removed, and q radical variables remain. The q variables impose affine equations of rank h on the d complement coordinates. The new core has d'=d-h variables and the multiplier exponent is p+q. Therefore

    (p+q)+d' = n-p-h <= n.

Iterating this inequality proves e+d_final<=n_original. Repeating the radical extraction after each affine restriction is necessary, because the restricted cubic can acquire a new radical; the actual loop performs this repetition.

If a remaining affine system is inconsistent, the signed sum is zero. This does not mean that the original cubic has no zero inputs: its zero-input count is then 2^(n_original-1). The implementation's `count` field in these structure checks is a signed phase sum; the theorem correctly distinguishes Z from N0.

The retained certificate checks now verify coordinate identities, each four-term Gaussian sum, the affine constraints, the parametrization and the multiplier inequality independently on the finite examples. They also verify the explicit XOR-to-contradiction witnesses.

## 4. Intrinsic coupling graph and the size certificate

For distinct primitive cubic blocks U_i,U_j, the mixed second derivative of p with one direction in each block is a bilinear form independent of the base point. Mixed cubic derivatives vanish by the direct-sum property. This gives an intrinsic cross-block bilinear coupling, represented by Q_ij in any chosen block bases.

Changing those bases replaces Q_ij by A_i^T Q_ij A_j with invertible A_i,A_j; zero/nonzero status is preserved. Affine translations of a cubic block create lower-degree terms only within that block. Translating a cross-block quadratic adds affine terms but leaves its bilinear matrix unchanged. Thus the block dimensions and zero/nonzero coupling graph are invariant under arbitrary affine disguises of a radical-free input, up to permutation.

After radical reduction, no invariance across all possible reduction strategies is needed or claimed: the computed core and its explicit certificate suffice.

In acquired coordinates, no cubic monomial crosses primitive blocks. Therefore the nonconstant monomial count M obeys

    M <= sum_i [B_i+binom(B_i,2)+binom(B_i,3)]
           +sum_(edges i,j) B_i B_j <= W,

where W=d+sum_i B_i^3+sum_(edges i,j) B_i B_j. Every term of this representation is explicitly computed. Small W is not assumed as a free decomposition or inferred from a heuristic graph search.

## 5. Polynomial acquisition and original-input reconstruction

The centroid system has 2d^3 equations in d^2 unknowns. Naive binary elimination has a universal polynomial bit bound, with O(d^7) sufficient for this matrix step. Polynomial substitution expands products of at most three affine forms; intermediate canonical ANFs have only O(n^3) possible monomials. Repeated radical reductions and all retained proof records therefore remain polynomial in L+n. No exponential idempotent enumeration or graph-subset computation remains in acquisition.

For phase counting, padding the acquired d-bit core with n-d unused variables is legitimate and avoids an accidental change of the density reference from n to d. It creates the known factor 2^(n-d), not new constraints. Precision n+2 reconstructs the signed padded sum exactly in [-2^n,2^n]. Removing that known multiplicity by exact integer division and then multiplying by 2^e is safe because e+d<=n. The original count follows from (2^n+Z)/2.

Consequently the phase-product theorem does imply poly(L+n)2^o(n) time and polynomial space whenever the computed M, or its sufficient upper bound W, is n exp(o(log n)). The graph can be cyclic or expanding; the construction invokes no graph-width promise. The result remains restricted by its computed algebraic/density certificate.

## 6. Re-execution and adversarial finite checks

After both repairs I re-executed the affected original programs:

- All 37 `cubic_structure_compiler.py` fixtures passed.
- All four non-forest acquired-block fixtures passed, with 16,384 pointwise identities and independently exhaustive raw/hidden/acquired phase sums.
- The retained JSON records were inspected directly, including three zero-sum certificates.

I additionally executed `work_gaussian_cont/acquired_block_audit_checks.py`. It passed:

- Five complete centroid/idempotent fixture audits, enumerating all 40 elements of their independently computed centroid spaces.
- Twelve arbitrary affine-disguise fixtures, including nonzero translations, preserving the acquired coupling graph and exact count.
- Fifteen retained radical rounds, with 7,452 exact coordinate/elimination/parametrization identities.
- Three explicit XOR-of-equations contradiction witnesses.

The idempotent fixtures include a six-dimensional nonsemisimple primitive block with a nonzero square-zero centroid element; two such blocks; primitive volumes over F_4 and F_8 viewed over F_2; and three split three-dimensional volume blocks. In each case all idempotents were found, and every idempotent acted as zero or identity on every acquired primitive image. The field examples had no nonzero square-zero elements and correctly remained primitive over F_2.

Actual audit results are in `work_gaussian_cont/acquired_block_audit_results.json`. These checks exercise the delicate characteristic-two and certificate claims. The algebraic proof supplies the general theorem; finite enumeration is not offered as its proof or as a practical benchmark.
