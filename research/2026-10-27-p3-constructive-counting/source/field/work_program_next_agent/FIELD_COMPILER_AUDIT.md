# Independent audit of the acquired extension-field counting interface

This audit concerns the root agent's new field pivot, not a claim that hidden-field recovery or point counting is new. All statements concern exact finite-field algebra. No numerical or practical-speed claim is made.

## 1. A deterministic field presentation without exhaustive element search

Let A be a finite-dimensional commutative F2-algebra, supplied by a multiplication table or matrices, of dimension d. Suppose A is connected (only the idempotents 0 and 1) and its Frobenius map sigma:a -> a^2 is injective. Then A is reduced, hence a product of finite fields; connectedness makes it a field of order 2^d. Both hypotheses are linear-algebraic tests: connectedness is dim ker(sigma-I)=1, and reducedness is injectivity of sigma. This avoids an unjustified search through all 2^d algebra elements.

An explicit polynomial presentation can also be acquired deterministically in polynomial time, as follows.

Factor the ordinary integer d into pairwise coprime prime powers m_i=ell_i^{e_i}. This costs polynomial time in d by trial division. Compute the F2-subspaces

    K_i = ker(sigma^{m_i}-I),
    K_i' = ker(sigma^{m_i/ell_i}-I).

Their dimensions are m_i and m_i/ell_i respectively. Choose a vector gamma_i from a computed basis of K_i which lies outside K_i'. Since the subfields of F_{2^{m_i}} have degrees dividing m_i, gamma_i has degree exactly m_i over F2.

The element alpha=sum_i gamma_i has degree d. For completeness, take two elements gamma,eta of coprime degrees m,t, and suppose a Frobenius power fixes their sum. Then

    sigma^j(gamma)-gamma = sigma^j(eta)-eta

belongs to the intersection of F_{2^m} and F_{2^t}, namely F2. Call this element delta. At least one of m,t is odd. Iterating the appropriate Frobenius restriction that many times gives 0=delta, so sigma^j fixes both gamma and eta. Therefore the stabilizer of their sum is the intersection of their stabilizers; its degree is mt. Induct on the pairwise coprime prime powers. For d=1 take alpha=1.

The powers 1,alpha,...,alpha^{d-1} form an F2-basis. Solve the first linear dependence involving alpha^d to obtain its degree-d irreducible minimal polynomial and the explicit isomorphism F2[T]/(h) -> A. The procedure uses only polynomially many algebra operations and linear systems in dimension d.

The exact program `field_acquisition_audit.py` ran this procedure on 36 independently disguised multiplication tables, with d in {1,2,3,4,5,6,8,9,10,12,15,18}. Every acquired power basis had full rank and every recovered minimal polynomial passed an independent irreducibility test. Small input fields for the test are constructed separately; the acquisition procedure does not enumerate the field.

### Nilpotents need not force rejection

If A is connected but not reduced, take the stabilized image of its Frobenius map. For any s with 2^s at least dim_F2 A, Frobenius^s kills the nilradical; its kernel is precisely that radical. It induces an automorphism on the finite residue field. Therefore its image is a canonical embedded field isomorphic to A/rad(A). Squaring images until dimension stops dropping obtains this field by linear algebra. The same generator construction applies to it. Its operators still lie in the original centroid, so the trace lift in Section 2 remains valid. The resulting field-module dimension is n/d, using the residue-field degree d, not the whole local-algebra dimension. This is also consistent with Magma's existing TensorOverCentroid machinery.

The audit additionally recovered this field from 12 disguised truncated polynomial rings F_{2^a}[epsilon]/(epsilon^h), using (a,h)=(2,2),(3,3),(4,4),(6,2). All recovered fields had the exact expected degree and yielded valid irreducible presentations.

## 2. Why a balanced binary cubic tensor has an alternating field lift

Let V be a module over an acquired field F=F_{2^d}. Let T:V^3 -> F2 be an alternating F2-trilinear tensor whose centroid includes the multiplication operators of F:

    T(cu,v,w)=T(u,cv,w)=T(u,v,cw).

The nondegenerate field trace pairing uniquely defines A:V^3 -> F by

    Tr(c A(u,v,w)) = T(cu,v,w) for every c in F.

Trace-pairing linear algebra computes A's coefficients. The slot transfers imply F-linearity in every slot. Alternation requires care in characteristic two: it follows from

    T(cu,u,w)=T(u,u,cw)=0

for every c, hence A(u,u,w)=0 by nondegeneracy. Consequently, in an acquired F-basis e_1,...,e_b, the field polynomial

    C(X)=sum_{i<j<k} A(e_i,e_j,e_k) X_i X_j X_k

has binary third derivative T after taking Tr. Any raw cubic having third derivative T differs from Tr C by a binary quadratic. This is a constructed identity, rather than a supplied field-polynomial description.

## 3. Exact low-degree fitting is a polynomial-size linear problem

For a field degree cap D, consider monomials X^e with total ordinary degree at most D and sum_i wt_2(e_i) at most three. Enumerate them as products of at most three Frobenius factors X_i^{2^j}, discarding those exceeding D and deduplicating. There are at most O((b log(D+1))^3) candidates. For each candidate, let its coefficient range over an F2-basis of F, giving d scalar columns.

Every candidate scalar function Tr(c X^e), pulled back through the acquired linear coordinate map, has Boolean degree at most three. Its coefficients can be obtained from its values at original Boolean points of Hamming weight at most three. Evaluation on those points is an injective linear map on the space of Boolean cubics: the restricted Boolean Mobius transform recovers all coefficients. Thus a target supplied as a verified raw cubic can be fitted exactly by a binary linear system with O(n^3) rows. A successful fit is a globally exact identity, not empirical agreement at a few points.

The acquisition cost is polynomial in n, L and log(D+1), as long as the candidate-exponent representation and field operations are charged. For the intended regime D<2^d, the field-degree certificate avoids needless degree reduction modulo X^{2^d}-X. The later point counter still pays for D; this efficient coefficient fitting does not remove that arithmetic cost.

The candidate class is invariant under F-linear affine changes of its b field coordinates without raising D. Indeed, a Frobenius power of an affine linear form is again an affine combination of Frobenius powers. Expanding a product of at most three such factors gives only monomials of binary exponent weight at most three; carrying equal powers can only lower that weight. Ordinary polynomial degree does not increase under affine substitution. A different field isomorphism differs by Frobenius, which conjugates coefficients and preserves the trace and the degree certificate.

The executable audit formed five random field polynomials, changed field coordinates by nonsingular affine maps, then recovered exact trace-polynomial descriptions by this linear system. The cases use (d,b,D)=(2,3,3),(3,3,3),(3,3,5),(4,2,9),(5,2,17). All 2,368 Boolean evaluations agreed, including the final ANF-degree checks. These tests validate the interface, not the asymptotic point-counting engine.

## 4. Point counting is a prior exact evaluator, with explicit reconstruction

For q=2^d and a fitted field polynomial F in b variables, consider

    Y^2+Y=F(X_1,...,X_b).

For each X, this equation has two F_q-solutions exactly when Tr F(X)=0, and none otherwise. Therefore if N_AS is its affine point count,

    N_0 = N_AS/2,
    N_1 = q^b - N_AS/2,
    sum_X (-1)^{Tr F(X)} = N_AS - q^b.

Lauder--Wan's Theorem 1 gives a deterministic bit algorithm polynomial in

    p^v D^{v^2} a^v,

where v is the number of field variables, q=p^a, and D is total degree. Here v=b+1, p=2 and a=d. No smoothness assumption is required. Thus fixed b and D polynomial in n give polynomial bit time; fixed b and log D=o(n) give subexponential time. The source has explicit larger exponents and space bounds, and does not by itself give polynomial space when D is subexponential. A polynomial-space claim in that latter regime requires a separate implementation argument and must not be inherited from the earlier replacement-form engine.

Primary source: Alan G. B. Lauder and Daqing Wan, *Counting points on varieties over finite fields of small characteristic*, Theorem 1 and Theorem 37.
https://arxiv.org/pdf/math/0612147

## 5. Prior machinery and boundaries

Hidden field recovery from raw tensors is established machinery. Magma's official `TensorOverCentroid` operation explicitly rewrites a tensor over the residue field of its centroid and demonstrates recovery of a hidden GF(2^10) structure. It cites Brooksbank--Wilson's cyclic-module algorithms. This should be credited, rather than presented as a new field-recovery invention:

- https://magma.maths.usyd.edu.au/magma/handbook/text/672 (TensorOverCentroid and its worked example).
- Peter A. Brooksbank and James B. Wilson, *The module isomorphism problem reconsidered*, J. Algebra 421 (2015), 541--559; official bibliography https://magma.maths.usyd.edu.au/magma/handbook/text/666.
- Uriya First, Joshua Maglione and James B. Wilson, *A spectral theory for transverse tensor operators*, cited by the same handbook for the centroid's universal scalar-ring property.

HFE and medium-field multivariate cryptography also has substantial field-recovery ancestry; public vector maps differ from the present single scalar trace polynomial, but should be compared before a priority claim:
https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=925999

The exact scope potentially added here is the acquired scalar cubic tensor, its exact lower-degree trace fitting, and its connection to this fixed-dimensional exact evaluator. A focused search does not establish first priority for that full interface.

The field-degree bound is essential. Sparse polynomials and straight-line programs may hide very high degree, and cannot be charged as though their degree were their short description length. Cheng--Hill--Wan give relevant complexity results and explicitly distinguish these representations:
https://arxiv.org/pdf/1111.1224

One cannot automatically derive efficient original-coordinate prefix counts from the fixed-field-dimensional evaluator: each additional binary trace constraint may add a field variable to an Artin--Schreier construction, or require Fourier enumeration of all constraints. Also, nonconstant scalar Boolean cubics already have each nonempty output label on at least a 1/8 fraction of inputs, by the Reed--Muller minimum-distance bound; ordinary rejection sampling is therefore already an expected-constant-evaluation method. The new exact counting guarantee must not be sold as a novel scalar-cubic inversion or sampling capability.

Finally, fitting only low-Hamming-weight evaluations of an arbitrary raw circuit is unsound without its established cubic degree. The zero circuit and the point indicator at an unqueried assignment have identical sampled values. The indicator has a linear-size AND/NOT circuit, so any deterministic exact black-box certification of cubic degree or identity with zero needs every Boolean point in the worst case. This is a value-query obstruction, not a lower bound against white-box program analysis.
