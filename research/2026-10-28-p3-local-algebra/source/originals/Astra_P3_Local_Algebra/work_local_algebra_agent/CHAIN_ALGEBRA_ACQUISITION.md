# Exact acquisition over a hidden chain algebra

This note proves the representation interface in `local_algebra_acquisition.py`. It supplies no point counter and makes no priority claim for finite-chain-ring structure, centroid computation, coefficient-field descent, or Hensel lifting. Its purpose is to construct every hidden ring, coordinate map, scalar functional, and quadratic remainder from a raw scalar Boolean cubic with a verified exact identity.

## 1. Input and acquired output

Let p be an explicit Boolean ANF of degree at most three on V=F2^n. Let T be its third additive difference, an alternating binary trilinear form with zero radical. Define the balanced input-slot centroid

    A={a in End_F2(V): T(au,v,w)=T(u,av,w)=T(u,v,aw)}.

The algorithm constructs A by binary linear equations in n² entries. It does not receive A, a field, a ring, a decomposition, or hidden coordinates. The main recognizer accepts exactly when A is a finite commutative chain algebra and V is a free A-module. It constructs

    A ≅ F[pi]/(pi^e), F=F_(2^d), n=bde,

an irreducible binary presentation h for F, a nilpotent operator pi, an A-module basis, and an invertible binary map U:A^b -> V. Coordinates are ordered by module block, pi power, then field-basis bit. For

    lambda(a_0+...+a_(e-1)pi^(e-1))=Tr_F/F2(a_(e-1)),

it constructs coefficients c_ijk in A and an explicit binary quadratic q satisfying

    p(UY)=lambda(sum_(i<j<k) c_ijk Y_i Y_j Y_k)+q(Y)

at every Y. All original assignments are in bijection with A^b; no auxiliary counted variables are introduced. A product recognizer acquires primitive chain components and retains every cross-component quadratic interaction.

## 2. Why the centroid is a commutative algebra

The identity lies in A and its defining equations are linear. For a,b in A, transferring them through different slots gives both T(abu,v,w)=T(u,bav,w) and T(abu,v,w)=T(u,abv,w). Zero radical forces ab=ba, and the same identities imply ab belongs to A. The representation in End(V) is faithful. The implementation additionally verifies identity, commutation, and closure against the full computed matrix basis.

## 3. Coefficient field and radical by linear algebra

The square map sigma:a -> a² is binary linear. Its fixed elements are idempotents. Each local factor has just idempotents zero and one, so dim ker(sigma-I) equals the number of local factors. Dimension one certifies locality.

Compute images of sigma until their dimensions stabilize. The kernel J of that stable power is the nilradical; the stable image is a reduced subalgebra isomorphic to A/J. Indeed the nilradical has nilpotence index at most m=dim_F2 A, so sigma^t kills it for 2^t>=m, whereas Frobenius is an automorphism on every finite residue field. In the local case the stable image is the canonical coefficient field F. Its degree d and its matrix action are obtained without enumerating 2^m algebra elements.

An explicit field generator is also deterministic. Test the computed field basis elements first. If needed, factor the ordinary integer d into pairwise coprime prime powers m_i=ell_i^(a_i). Compute ker(sigma^(m_i)-I), choose gamma_i outside ker(sigma^(m_i/ell_i)-I), and sum the gamma_i. Each gamma_i has degree m_i. Their sum has degree d: for coprime extension degrees, equal Frobenius displacements lie in F2; at least one degree is odd, so iterating kills the displacement. Induction proves the full degree. The first relation among 1,alpha,...,alpha^d supplies the irreducible h.

This is the previously audited coefficient-field mechanism, now used before retaining the nilpotent part. Magma already documents local-centroid residue-field descent; this interface additionally keeps explicit nilpotent coordinates.

## 4. Acquiring the uniformizer

Compute J² from products of a basis of J. If J=0, then A=F and e=1. Otherwise require dim_F2(J/J²)=d. Any computed pi in J outside J² then generates J by Nakayama's lemma. Repeated expansion A=F+pi A shows that F[pi]=A.

Let e be least with pi^e=0. The vectors 1,pi,...,pi^(e-1) are F-independent: a relation with least nonzero coefficient at j would give pi^j u=0 for a unit u, contradicting the minimality of e. Thus m=de and A≅F[t]/t^e.

The program constructs every alpha^i pi^j, checks binary rank m, checks pi^e=0, and checks every basis product against truncated polynomial multiplication. These form an explicit ring-isomorphism certificate. The local algebra F2[u,v]/(u,v)^2 fails because dim(J/J²)=2 while d=1. This is a class boundary, not a counting-hardness result.

## 5. Acquiring a free module

The operator P for pi is F-linear and P^e=0. If its nilpotent Jordan block lengths over F are ell_1,...,ell_t, each at most e, then

    n=d sum ell_i,  dim_F2 ker P=dt.

Consequently V is free over A exactly when e dim_F2 ker P=n. Integer divisibility by m is also checked. No Jordan normal form is needed: compute pi V and greedily select an F-basis of V/pi V, using original binary vectors and their d field multiples. The selected lifts generate V by Nakayama. Their count is b=n/(de), so their full A-orbits give an invertible n-column binary basis. Its rank is checked directly.

Faithfulness does not imply freeness. For A=F2[pi]/pi², the faithful module A plus two copies of F2 has binary dimension four, divisible by dim A, but its pi operator has rank one. The Jordan-length criterion correctly rejects it.

## 6. Frobenius pairing and the alternating lift

The pairing (a,b) -> lambda(ab) is nondegenerate. For nonzero a, let k be its lowest nonzero pi degree, and choose b=pi^(e-1-k)c with Tr(c a_k)=1. Then lambda(ab)=1. Thus its m by m binary Gram matrix is invertible.

Define the unique A-valued form t by

    lambda(c t(u,v,w))=T(cu,v,w) for all c in A.

The Gram matrix computes the needed coefficients. Centroid balancing and nondegeneracy prove A-linearity in each slot. Alternation follows even in characteristic two because T(cu,u,w)=T(u,u,cw)=0 for every c, hence t(u,u,w)=0.

Set c_ijk=t(e_i,e_j,e_k) in the acquired module basis. The A-cubic C(Y)=sum c_ijkY_iY_jY_k has scalar third difference T. Therefore p(UY)+lambda(C(Y)) is an exact binary quadratic. Values at points of weight at most two recover its constant, unary, and pair coefficients. The production algorithm relies on this proved identity and fully checked centroid/ring/basis certificates. An optional `verify_cubic_coefficients=True` independently checks every third ANF coefficient; finite audits enable it.

For b=3, t is a scalar a times the A-volume form. Zero radical forces a to be a unit, since a nonunit has a nonzero annihilator and would produce a radical vector in one coordinate. Conversely lambda(det_A) on A³ has balanced centroid exactly A. Repeated-coordinate test vectors force every off-diagonal block of a centroid operator to vanish, using nondegeneracy of lambda(xy). The remaining diagonal maps satisfy f_1(x)y=x f_2(y) after varying the third argument. Setting x or y to one makes all three multiplication by a common scalar. Thus the fixtures have the intended full centroid, not just a contained ring.

## 7. Primitive products and retained quadratic glue

When dim ker(sigma-I)>1, choose a nontrivial fixed vector e. It is an idempotent, and its matrix splits V=eV plus (1+e)V and A=eA times (1+e)A. Restrict the matrix algebra to each image and recurse. Every split is strict, at most m factors occur, and a basis of the fixed subspace supplies a splitting vector; no 2^k enumeration is needed.

Distinct components have no mixed cubic interaction: if u=eu and v=fv with ef=0, then T(u,v,w)=T(u,ev,w)=0. Each restricted tensor remains radical-free, and its full centroid is its local factor. Apply the chain and free-module tests to every component.

Concatenate their module coordinates. The scalar p is a sum of local cubic traces plus one global quadratic. The implementation retains all cross-component pairs. Each component also exposes `local_quadratic_remainder`, restricting the global remainder to that component and assigning the sole global constant to component zero. This is a convenience for a downstream evaluator; the global remainder remains authoritative for interactions. No independent-count product is assumed.

## 8. Description size and costs

The input is an explicit ANF of bit length L and its original bit count n. The centroid has n² unknowns and O(n³) equations; naive binary elimination uses O(n^7) bit operations and O(n^4) bits. All subsequent matrix products, subspace operations, Frobenius iterations, field-generator construction, uniformizer recognition, and module-basis acquisition have polynomial bit cost. The free-module recognizer rejects m>n or m not dividing n before its multiplication table is expanded. A conservative combined bound, including the optional full third-coefficient audit, is O(n^7+L n^4) bit operations. There is no hidden 2^d or 2^(de) factor.

The scalar polynomial representation needs O(n²+m binomial(b,3)) bits, besides h and the n²-bit coordinate matrix. Retaining all m ring-action matrices adds O(mn²) bits; these certificates can be discarded after the map and ring presentation are fixed. Ring elements have de bits, schoolbook multiplication costs O(e²d²), and exact binary coordinate transforms cost O(n²).

These are representation costs. No arbitrary A-cubic, arbitrary quadratic remainder, or product with arbitrary cross interactions has been declared easy to count. A later evaluator must charge its rank expansion and arithmetic.

## 9. Executed checks

`local_algebra_checks.py` acquired nine dense-affine-disguised raw cubics with arbitrary binary quadratic remainders for

    (d,e,b)=(1,2,3),(2,2,3),(1,4,3),(2,3,3),(3,2,3),
             (2,4,3),(3,3,3),(1,3,5),(2,2,5).

These span n=6 through 27; all 46,144 validation points agreed. Four cases use all assignments. Larger cases use reproducible points in addition to every third-coefficient identity. The non-chain radical, unsplit product, and faithful nonfree module are rejected.

`product_chain_checks.py` acquired mixed products of two or three local factors at n=12,15,27,30. All 40,960 pointwise checks agreed, with 21,25,118,105 cross-component quadratic terms retained. This is not an independent-count factorization.

## 10. Primary-source comparison

- Magma's official documentation describes A-centroids and `TensorOverCentroid`, including residue-field recovery for a finite commutative local centroid, and credits Brooksbank--Wilson's module algorithms: https://magma.maths.usyd.edu.au/magma/handbook/text/672
- Characteristic-p finite chain rings being F_q[u]/(u^e) is standard. An explicit primary statement is Proposition 2 of *Constacyclic Codes over Finite Chain Rings of Characteristic p*, Axioms 10(4), 303 (2021): https://www.mdpi.com/2075-1680/10/4/303
- Broader principal-ring structure appears in Matthe van der Lee, *Finite local principal ideal rings*, arXiv:2301.07664: https://arxiv.org/abs/2301.07664

This work supplies a raw-scalar representation interface for a downstream exact evaluator. It is not a new classification of finite algebras or a generic tensor-contraction algorithm.
