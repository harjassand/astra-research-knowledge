# Actual-coordinate Gibbs-sampler boundary for the BDL memory

## Status and consequence

At sufficiently large even construction depth, the physical Z-check matroid of the BDL random-embedding family has a minor consisting of a direct sum of a linear number of Fano-dual matroids. Constants depend on the fixed refinement parameter. This excludes a regular cover of codimension O(log N), and therefore excludes applying the published Code Swendsen–Wang near-graphic/near-cographic theorem, the regular-matroid FPRAS, or a regular-cover sampler followed by only polynomial-cost parity rejection as a black-box loading shortcut.

This excludes those sufficient conditions. It is not a lower bound against arbitrary Gibbs sampling: P1's accepted decoder-history/polymer sampler remains a polynomial loader in its stated low-temperature regime. Its compiler and loading theorem are not re-audited here. A full auxiliary Gibbs sampler would be a valid same-access comparator because the syndrome can be sampled before the unknown logical input arrives and its initial error is paid once.

The key operation is an exact matroid minor obtained by contracting physical Hamiltonian check coordinates in the actual RX replacement. It is not based on the intuitive tensor-product variant or on check weights. The computer-assisted discovery reduces to a 53-element local certificate, independently verified using Gaussian elimination. The symbolic physical-family bridge works for every fixed odd ell >= 5, including BDL's much larger geometric choice.

## 1. Notation

For a physical Z-check matrix h_Z with m check rows and n qubit columns, put A=h_Z^T. Its physical check-coordinate matroid is M(A): ground elements are the m actual Hamiltonian Z checks. Define the augmented matroid

    N(A) = M([I_m | A^T]).

Its m identity elements are labeled by actual checks and its n other elements by actual qubits. N(A) is an algebraic intermediate; it is not asserted to be the physical Gibbs matroid. All arithmetic is over F2.

## 2. Exact RX contraction: the Lawrence double

BDL Section 3.2.2, equations (61)–(72), constructs RX from local cellular complexes Y_x and Y_q. Its physical Z-check boundary matrix has the form

    rows:    x-local edges, q-local vertices
    columns: x-local faces, q-local edges, doubled old-Z points

    B = [ D_X   G_1   0 ]
        [  0    D_Q   P ].

D_X is the direct sum of face-to-edge boundary maps of Y_x; D_Q is the edge-to-vertex incidence map of the disjoint Y_q graphs; G_1 includes Y_q edges into adjacent Y_x blocks; P puts the old-Z point copies into their neighboring Y_q leaves.

### Lemma 1: physical RX minor

M(B) has a minor represented by

    L(A) = [ A  0  I_n ]
           [ 0  A  I_n ].

Zero rows of A may be omitted; BDL has no such isolated Z-sector qubits.

**Proof.** Contract all x-local face elements. For each x, H_1(Y_x)=0 by BDL Lemma 3.8 and its proof, so im D_X=ker d_X, where d_X is edge-to-vertex boundary. Quotienting x-edge coordinates by im D_X is faithfully represented by applying d_X. The quotient matrix is

    [ d_X G_1   0 ]
    [    D_Q    P ].

Inclusions commute with boundary: d_X G_1=G_0 D_Q. Also G_0 P=0 by old CSS commutation, equivalently the paired Tanner faces at every old X/Z corner. Thus the first block row is G_0 times the second and is redundant.

The remainder is the incidence matrix of disjoint Y_q graphs with point columns P appended. In each Y_q contract the upper subdivided star and lower subdivided star, leaving vertices q_0 and q_1. Each old adjacent Z leaf gives a bridge with column e_(q,0)+e_(q,1). Keep one bridge per q and delete its parallel copies. The point columns become A on the upper and lower blocks. This is L(A). All contractions and deletions were of actual physical Z-check elements. ∎

### Lemma 2: augmented dual minor

N(A)^* is a minor of M(L(A)), hence of the physical Z-check matroid after RX.

**Proof.** A dependence of L(A) is exactly

    (u, u+r, Au),  u in F2^m, r in ker A.

Using a basis for ker A, a dual representation consequently has upper-check columns (e_j,0), lower-check columns (e_j,R_j), and bridge columns ((A^T)_q,0). Restrict this dual representation to upper checks and bridges. The result is [I_m | A^T] with zero auxiliary rows. Dualizing restriction gives contraction of all lower-check columns in the original matroid. No independence assumption on old checks is used. ∎

## 3. A local Fano certificate

Let T_strip consist of two adjacent Tanner squares

    (x_0,q_0,z,q_1), (x_1,q_1,z,q_2),

with h_X=[[1,1,0],[0,1,1]] and h_Z=[[1,1,1]]. This is a valid CSS Tanner complex. Apply RX with ell=3 (the unsubdivided block). Dimensions are (X checks, qubits, Z checks)=(16,34,19), with ranks (16,18).

In N(A), label the 19 identity/check elements 0,...,18 and the 34 qubit elements 19,...,52. The deterministic cell ordering is in bdl_matrices.py. Contract

    C = [13,19,29,26,52,22,44,10,32,6,17,33,24,21,36,50]

and retain in order

    R = [2,4,25,14,51,7,37].

Delete all other elements. The contracted columns have rank 16. A quotient map P:F2^19 -> F2^3 has row supports

    [2,3,5,8,9,12,16,18],
    [4,7,11],
    [7,14].

Every contracted column lies in ker P, and the retained columns map to binary integers 1,2,3,4,5,6,7: all seven nonzero vectors of F2^3. This is a complete Fano certificate. The independent verify_two_square_fano.py checks the Tanner construction, CSS commutation, contraction rank, annihilation and all images, without using CMR. The JSON certificate includes cell labels as well as indices.

## 4. Refinement and subcomplex transport

### Lemma 3: ell-independent strip obstruction

For every odd ell >= 3, N_Z(RX_ell(T_strip)) has the preceding F7 minor.

**Proof.** Set s=(ell-1)/2. Identity columns are available for every Z-check row in the augmented representation. In each subdivided x-local face, contract qubit columns on a dual spanning tree of the s-by-s subdivision. Each interior subdivision edge gives a column with exactly two local face entries; these contractions identify all subface coordinates of the original face. Do the same along each subdivided side strip. Its internal vertical edges are not edges of Y_q, so no q-block check entry interferes.

Within each subdivided q-local edge, contract qubit columns at internal vertices. Each has exactly two q-edge check entries and no old-Z point entry. This identifies its subdivided edge-check coordinates. Keep one identity column per merged check coordinate. Boundary qubit columns now have identical parallel copies along each old edge; keep one. The resulting augmented matrix is exactly the ell=3 matrix. Apply the certified local minor. ∎

### Lemma 4: subcomplex and direct-sum extraction

If T contains vertex-disjoint copies of T_strip, then N_Z(RX_ell(T)) has a minor equal to a direct sum of one F7 per selected copy.

**Proof.** RX assigns blocks to old Tanner vertices and glues by restrictions along old incidences. The cells attached to a closed Tanner subcomplex are therefore subsets of the full RX cells. Contract identity columns for check coordinates outside the selected cells (coordinate projection), then delete qubit columns outside them. This leaves the augmented RX matrix of each selected strip. Extra incident faces and star arms disappear under the same projection.

Distinct copies use disjoint old x,q,z vertices. A retained x-block edge only couples to its own x-face checks and q-edge checks with the same selected q/edge label. A retained q-block vertex only couples to its own q-edge checks and selected z-point checks. Consequently no off-diagonal entries remain between selected copies. Apply Lemma 3 in each block. ∎

## 5. The intervening RZ step

### Lemma 5: augmented monotonicity in the unexpanded sector

N_Z(RZ(T)) has N_Z(T) as a minor for every refinement parameter.

**Proof.** RZ is dual RX. Its physical Z checks are vertices of connected local Y_z graphs. Internal-edge qubits have exactly their two endpoint Z checks as column entries. In the augmented matrix, contract these columns on a spanning tree of each Y_z, thereby identifying every row coordinate in its z block. Keep one identity column per old z. For each old q retain the qubit at one root vertex q_0 of Y_q: it has exactly one incidence in each adjacent old z block. Its projected column is therefore the old q column of h_Z. Delete all other columns, leaving [I_oldZ | old h_Z]. ∎

### Lemma 6: physical monotonicity in the unexpanded sector

The physical Z-check matroid after RZ is a series extension of the old physical Z-check matroid.

**Proof.** A dependence among the new Z checks is constant on each connected Y_z vertex block, because its internal edge-qubit rows impose equality. The q-root rows then impose exactly the old dependence equations. Every other q-block vertex imposes the same equation, since the whole Y_q embeds in every adjacent Y_z. Thus each old relation coefficient is repeated throughout its new vertex block. Repetition in the cycle space is a series extension; contracting all but one element in each series class recovers the old matroid. ∎

Lemmas 1–6 give the exact chain:

    r disjoint strips in T
      -> direct sum r F7 minor in N_Z(RX(T))
      -> direct sum r F7 minor in N_Z(RZ RX(T))
      -> direct sum r F7* minor in physical M_Z(RX RZ RX(T))
      -> the same physical minor after a final RZ.

Each operation preserves the direct-sum minor and uses specified coordinate labels.

## 6. Extensive packing in the actual fixed-ell family

At a sufficiently large even level j, the last operation is RZ. Its local Y_z complexes contain subdivided square layers (BDL Section 3.2.5). For s=(ell-1)/2 >= 2, every old Tanner square supplies an internal grid edge incident to two distinct grid faces. At one endpoint v, the two faces, the common edge and their two other incident edges form T_strip: v is a Z-check vertex, the faces are the X checks and the edges are the three qubits.

Here is the count rather than an unproved density assumption. Every qubit has at least one neighbor of each check type. This holds in the base code and is preserved by RX: an x-block edge has its two local X endpoints and lies in a local face; a q-block vertex is incident to a local Y_q edge and receives an X incidence from every old X neighbor of q. RZ is dual. Each Tanner edge is consequently in a Tanner face by commutation and the source's pairing rule. Bounded degree then gives number of Tanner faces = Theta(number of qubits).

Every old face supplies a distinct grid patch in the new local Y_z complexes. Choose one internal edge and endpoint in each patch. Bounded Tanner degree bounds how many selected six-vertex strip neighborhoods intersect a given one. Greedy packing therefore retains c_ell N_(j-1) vertex-disjoint strips. The fixed-ell expansion ratio is bounded, so this is also c'_ell N_j.

Apply the four-step chain to T_(2k-4). Growth through four replacements is a fixed constant depending on ell. Hence for some a_ell>0 and all sufficiently large k, the final physical Z-check matroid has a minor

    direct sum_{i=1}^{r_k} F7*,  r_k >= a_ell N_(2k).

The constants may be very small. This is an asymptotic fixed-ell statement under exactly BDL's geometric resource convention, with no alteration of embedding, physical checks or bath law.

## 7. Quantitative regular-cover obstruction

For a binary cycle space C define its regular-cover defect to be the minimum dim(D/C) over cycle spaces D of regular matroids on the same ground set with C subset D. The same definition applies to a syndrome space: it is the cycle space of the dual physical-check matroid.

### Lemma 7

If M has a minor consisting of a direct sum of r F7 or F7* blocks, its regular-cover defect is at least r. The same holds for its syndrome space after dualizing.

**Proof.** Deletion intersects the cycle space with a coordinate subspace; contraction projects it. Both preserve inclusions and cannot increase their codimension. Regular matroids stay regular under these operations. Reduce to C=direct sum C_i on disjoint blocks E_i, where each C_i is the cycle space of F7 or F7*.

For a regular cover D, the subspace D intersect F2^(E_i) is the cycle space of a regular restriction. It contains C_i strictly, since F7 and F7* are nonregular. Pick one vector from each strict difference. The resulting r vectors are independent modulo C because their supports lie in distinct blocks. Thus dim(D/C)>=r. ∎

Both published CSW possibilities consequently require Delta=Omega(N): graphic matroids are regular, and regularity is closed under duality. Its published Delta-(co)graphic theorem supplies no polynomial mixing bound here. The exact regular-matroid FPRAS premise fails too. Even an O(log N)-codimension regular syndrome cover followed by parity rejection is impossible because no such cover exists.

This does not prove that actual CSW dynamics are exponentially slow. It is not a general Gibbs-sampling lower bound. P1's accepted history sampler is precisely a different efficient route. The conclusion is that its loading operation is not already supplied by the published regular/near-graphic sufficient conditions on the actual physical coordinates.

## 8. Primary sources and reproducibility

- BDL, A passive self-correcting quantum memory in three dimensions, arXiv:2605.10943v1; Sections 3.2.2, 3.2.5 and Lemma 3.8: https://arxiv.org/html/2605.10943v1
- Hangleiter, Ju, Vazirani, Code Swendsen–Wang Dynamics, arXiv:2510.08446v4; Definition 10, Theorem 16, Corollary 17: https://arxiv.org/html/2510.08446v4
- Goldberg and Jerrum, A polynomial-time algorithm for estimating the partition function of the ferromagnetic Ising model on a regular matroid, arXiv:1010.6231v2: https://arxiv.org/html/1010.6231v2
- CMR primary algorithm implementation, Walter–Truemper and collaborators (discovery only): https://discopt.github.io/cmr/ and https://github.com/discopt/cmr

From the workspace root run:

    python exchange_work/sampler_route/verify_two_square_fano.py

The larger fano_dual_exact.json independently gives a physical F7* minor at ell=3, depth3. It is not used as a substitute for the symbolic arbitrary-ell proof. The earlier diagnostic CMR graph certificates are exactly verified by their binary row spaces; positive shallow-level regularity does not extend to all depths.

### Independent audit and scope refinements

The separate verifier in ../decoding_route/audit_matroid_subdivision.py constructs the strip's grid/cylinder blocks independently of bdl_matrices.py and verifies the refinement contractions and pulled-back Fano quotient at ell=3,5,7,9. The contraction rank is the full augmented row rank minus three and the seven images are exactly 1,...,7 in each case. Its symbolic grouping proof covers all odd ell. verify_lawrence_minor.py independently verifies equality of the contracted physical matroid and L(A) on a dependent-check input (19 checks, rank18, 34 qubits); the retained Lawrence matrix has 72 columns and rank52. Neither verifier depends on CMR.

The combinatorial obstruction persists for all strictly positive commuting check coefficients: changing coefficients changes Gibbs weights but not the matroid on the actual Hamiltonian check coordinates. Arbitrary invertible changes of physical Pauli-label coordinates do not change this matroid. Replacing the Hamiltonian check basis, however, generally changes the weighted interaction law and is not a free representation change for sampling.

A linear cover codimension does not by itself prove an exponentially small acceptance probability for every possible high-codimension weighted cover. The proved exclusion is absence of O(log N)-codimension regular covers, and therefore failure of that generic polynomial-guarantee route. Actual CSW torpid mixing, arbitrary reductions to regular systems with extra resources, and universal sampling lower bounds are not claimed.

## 9. Stronger comparator: regular covers and finite-accuracy rejection

Let L be the desired valid-syndrome code and R a linear cover on the same m physical coordinates, with L subset R and codim_R L=q. For nonnegative dimensionless check energies lambda_i, put x_i=exp(-lambda_i) in [0,1] and

    w(s)=product_i x_i^(s_i),   pi_R(s)=w(s)/Z_R for s in R.

Then

    pi_R(L) >= 2^(-q).

This guarantee does not require R to be regular. Regularity only supplies the existing polynomial sampling method for pi_R.

**Proof.** The binary Fourier expansion of w has nonnegative coefficients:

    w(s)=product_i [(1+x_i)/2 + (1-x_i)(-1)^(s_i)/2].

For every character chi_v(s)=(-1)^(v dot s),

    sum_(s in R) w(s) chi_v(s)
      = |R| sum_(u in v+R^perp) hat_w(u) >= 0.

There are 2^q characters of R/L and

    1_L(s)=2^(-q) sum_(chi in (R/L)^*) chi(s),  s in R.

Taking expectation under pi_R, the trivial character contributes 1 and every other contribution is nonnegative. Thus the acceptance probability is at least 2^(-q). Equivalently the zero coset has at least as much weighted mass as any other coset. This uses the zero-preferred positive-coupling weight convention; it is not a statement about arbitrary frustrated weights. ∎

For an approximate proposal nu with TV(nu,pi_R)<=delta, exact membership rejection gives acceptance at least 2^(-q)-delta. If delta<=2^(-q-1), its expected number of proposals is at most 2^(q+1). The accepted law obeys

    TV(nu(.|L),pi_R(.|L)) <= delta/pi_R(L) <= 2^q delta.

One proof of the first inequality uses common mass on L. If a=pi_R(L)>=b=nu(L), then min(pi_R(s)/a,nu(s)/b)>=min(pi_R(s),nu(s))/a; the lost common mass is at most delta. The case b>=a is symmetric and gives the stronger denominator max(a,b).

Choose delta=epsilon_alg 2^(-q), with epsilon_alg<=1/2. Using fresh independent proposals and truncating after

    K=ceil(2^(q+1) log(1/zeta))

trials bounds the abort probability by zeta. The accepted conditional law is epsilon_alg-close; adding an abort flag, or a fixed valid fallback, costs at most another zeta in the unconditional output. Membership in L is checked by precomputed binary parity equations.

If the regular-cover sampler has cost P(m,1/delta,B), where B records weight precision, the finite worst-case rejection route costs

    O(2^q log(1/zeta) P(m,2^q/epsilon_alg,B))

plus membership checks and the cost of constructing/certifying the cover. For q=O(log m) this remains polynomial, including the inverse-accuracy dependence of the Goldberg–Jerrum route. Therefore inverse-polynomial source accuracy is not an obstruction to this comparator.

Coefficient uncertainty can be paid on the final target code instead of amplified through rejection. Sample and reject using nonnegative estimated lambda_hat, obtaining the target law pi_L(lambda_hat) within epsilon_alg. The accepted calibration estimate gives

    TV(pi_L(lambda_hat),pi_L(lambda)) <= (1/4) sum_i |lambda_hat_i-lambda_i|.

Thus the proposal's numerical sampling error needs the factor 2^(-q), while the final coefficient-calibration budget need not. The BDL obstruction above excludes every q=O(log N) regular cover, regardless of how it is discovered. It does not assert that every high-codimension weighted cover has exponentially small acceptance.
