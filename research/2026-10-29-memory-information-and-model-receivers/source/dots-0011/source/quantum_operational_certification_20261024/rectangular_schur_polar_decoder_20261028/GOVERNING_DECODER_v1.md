# A polynomial-access polar decoder for a rectangular low-defect Schur sector

28 October2026. **New author construction; independent review pending.** This is a restricted constructive bridge, not a solution of general universal quantum decoding or an end-to-end hardware claim.

## Source and target (source summary)

Rizzo, Lami, Eisert and Leone, *Universal quantum coding*, arXiv2609.38038v1, https://arxiv.org/html/2609.38038v1 , equations14,63–66,74–79,146–152 and implementation discussion following175 define a representation-theoretic reference channel and polar recovery. Their implementation discussion leaves the decoder's computational efficiency open. I inspected those governing passages. Their Haar Gram-moment identity and Schur error-space identification are used here at their stated scope; no generic source-rank promise is treated as an efficient-access oracle. The paper concerns iid copies, not an arbitrary retained-memory source. Standard QSVT is due to Gilyén et al., arXiv1806.01838; it implements bounded singular-value polynomials given a block encoding. It does not create the encoding for free.

## 1. Explicit special sector and its error space

Let k=2m>=4 and lambda=mu=(m,m). Let V_lambda be the real Young-orthogonal Specht representation, dimension

    d = Catalan(m) = C(2m,m)/(m+1).

Take the selected environmental irreps T={(k),(k−2,2)}. Write q=C(k,2), r2=k(k−3)/2 and N=1+r2. These are dimensions of the trivial plus (k−2,2) error space, not Hilbert-space input ranks. The reference channel has d-dimensional input and output.

The conjugation module End(V_lambda) contains trivial multiplicity1, standard (k−1,1) multiplicity0 and (k−2,2) multiplicity1. Here is a short derivation, making completeness rather than mere inclusion explicit.

Restriction of a rectangular Specht representation to S_(k−1) has exactly one removable-corner branch, so its commutant dimension is1. Frobenius reciprocity for the point permutation module (k)⊕(k−1,1) therefore gives standard multiplicity0. Restriction to S_(k−2)×S_2 has exactly two multiplicity-one summands: remove a horizontal two-box strip from the bottom row, or a vertical two-box strip from the last column. The resulting S_2 shapes are respectively (2) and (1,1), so the two summands are inequivalent even if small dimensions coincide. Its commutant dimension is2. The two-subset permutation module is (k)⊕(k−1,1)⊕(k−2,2); reciprocity now gives the last multiplicity1.

Let U_e=p_lambda((ij)) for the unordered edge e={i,j}. Conjugating permutes these q matrices. The intertwiner from the edge permutation module to End(V_lambda) has nonzero (k−2,2) image: otherwise all transpositions would act by the same scalar, forcing this irreducible representation to be one-dimensional, whereas d>=2. Hence the span of I and all U_e is exactly the FULL sum of the two selected isotypic spaces. No missing multiplicity copy is silently discarded. For k4 the scalar component of the U_e span vanishes, so I is explicitly added.

Under vectorization, conjugation p_lambda⊗p_lambda is the same diagonal group action identifying the paper's elementary Choi error sectors. An orthonormal operator basis of this full subspace is therefore a unitary change of error basis for the reference channel. Recovery followed by tracing the error register is invariant under that basis change; arbitrary physical positive error weights are transformed with the same unitary.

## 2. Polynomial Gram matrix and explicit normalized frame

All traces below are divided by d. The central transposition sum acts by the sum of the Young contents, m(m−2). Thus each U_e has normalized trace

    c=(k−4)/(2(k−1)).

Let B be the q-by-k edge/vertex incidence matrix, B_(e,v)=1 if v belongs to e. Then B^T B=(k−2)I+J, and

    P2=I−B(B^T B)^−1 B^T

is the rational orthogonal projector onto the (k−2,2) component of the edge module. The transposition Gram matrix is invariant and, by Section1, has no standard component. Its trivial component is c²11^T. Its remaining eigenvalue h is fixed by its trace q:

    H = c²11^T + h P2,
    h = q(1−c²)/r2 = 3(k²−4)/(4(k−1)(k−3)).          (1)

In particular h>=3/4; there is no exponential Gram-conditioning cost. Choose any orthonormal basis v_a, a=1,...,r2, of range(P2), and set

    F0=I,
    Fa=h^(−1/2) sum_e (v_a)_e U_e.                  (2)

Then Tr(Fa†Fb)=d delta_ab, including a0. The full span is invariant under conjugation; therefore sum_a FaFa† and sum_a Fa†Fa commute with the irreducible representation. Their trace fixes both sums to N I. Consequently (1/N)sum_a Fa X Fa† is exactly a trace-preserving unital reference channel with the desired Choi support.

The coefficient one-norm for Fa is at most sqrt(q/h)<2k. The q-by-r2 basis may be computed classically from the explicit rational P2. Only polynomially many entries are required. A deterministic independent-column/QR method has polynomial precision bit complexity: denominators of P2 are polynomial in k, nonzero pivot determinants have denominator at most that denominator to powerO(q), and logarithmic precisionO(poly(k)) suffices. This is not an exponential-size Specht-coordinate table. The example program uses floating eigendecomposition only for diagnostics.

## 3. Actual access construction and normalization

A standard Young tableau can be stored using O(k log k) bits. Adjacent transpositions act on at most two tableau basis states: their diagonal coefficient is the reciprocal axial distance, and the off-diagonal coefficient is sqrt(1−1/r²), with invalid swaps absent. Contents and validity are computed reversibly in poly(k) time. An arbitrary transposition (ij) is a product of at most2k adjacent transpositions. Therefore each controlled U_e is implementable with poly(k,log(1/precision)) gates WITHOUT listing d coordinates.

Prepare the polynomial-sized coefficient registers for (2), use SELECT over these known transposition circuits, and unprepare. Standard linear-combination-of-unitaries gives a projected block encoding of each Fa with one common normalization a=2k; pad the coefficient lists with cancelling dummy terms if needed. All coefficient lists have only q entries. They are known numbers computed from P2, not channel samples or an unknown Kraus oracle.

Let C:C^K→V_lambda be the actual supplied efficiently implemented code isometry, including the shared random seed and chosen code-block index. This retains the encoder-access premise of the source protocol. It is not supplied as a dense d-by-K matrix. On input |x>|a>, apply C and the controlled Fa block. Project the a register onto the known uniform state N^(−1/2)sum_a|a>. This gives a rectangular projected block encoding of

    W_C |x,a> = Fa C|x>,
    W_C / alpha,  alpha=2k sqrt(N)=O(k²).             (3)

The uniform-state preparation and projection are implemented coherently, including the non-power-of-two register case. Projected blocks are incorporated into a unitary dilation; one does not physically postselect each oracle call. Notice the paid sqrt(N) normalization. Since W_C W_C†<=sum_a FaFa†=N I, alpha is safely larger than ||W_C||. No exponentially small Choi-state preparation probability appears. Building the classical coefficient tables uses poly(k) arithmetic/storage; each block call uses a code circuit or its inverse and polynomially many known gates. Finite synthesis errors accumulate according to the actual number of calls and must be budgeted.

## 4. Soft polar recovery without a spectral-gap assumption

A packing bound controls a mean Gram defect, NOT the smallest singular value of W_C. We do not assume such a value, and we do not ask QSVT to implement a discontinuous cutoff.

For an integer M>=0 define the explicit odd polynomial

    f_M(z)=z sum_(j=0)^M [C(2j,j)/4^j](1−z²)^j.       (4)

For 0<=z<=1 its terms are nonnegative, and the infinite sum is1. Thus 0<=f_M(z)<=1; by oddness it is bounded by1 on[-1,1]. For z>0, using the coefficients<=1,

    0<=1−f_M(z)<= (1−z²)^(M+1)/z.

Choose M+1>=4 alpha² log(2alpha/epsilon). Then f_M(s/alpha)>=1−epsilon whenever s>=1/2. Its degree is2M+1=O(alpha² log(alpha/epsilon)), polynomial in k. Bounded real odd-polynomial singular-value transformation produces a contraction R_M from Bob's space to logical⊗error space, with singular vectors of W_C† and singular values f_M(s/alpha). Measure its success flag, trace the error register on success, and output a fixed logical state on failure. This is a TOTAL CPTP recovery, not a successful-branch decoder. Standard polynomial/phase compilation and gate precision are still paid. Formula(4) is a finite explicit polynomial; the pilot does not claim to have executed its large QSVT circuit.

Write G=W_C†W_C, A=pi_K⊗T for any fixed positive physical error operator T independent of the random code, and t=Tr T. Use a purification chi of A. The pre-decoding vector is W_C chi. On the success branch R_M W_C acts as sqrt(G)f_M(sqrt(G)/alpha). The Bell-error component is bounded by its squared difference from chi. Adding the entire failure-flag probability gives the pointwise spectral penalty

    L_M(x)=1+x−2sqrt(x) f_M(sqrt(x)/alpha).             (5)

For x<=1/4, positivity of f_M and

    1+x <= (20/9)(x−1)²

give L_M(x)<=(20/9)(x−1)². For x>=1/4, (4) gives

    L_M(x)<=(sqrt(x)−1)²+2epsilon sqrt(x)
           <=(x−1)²+2epsilon sqrt(x).

Hence total Bell failure is at most

    (20/9) Tr[A(G−I)²] +2epsilon Tr[A sqrt(G)].        (6)

The source's Haar Gram identities, applicable to the explicit orthogonal isotropic frame above, imply

    E_C Tr[A(G−I)²]=beta t,
    E_C Tr[A G]=t,
    beta=(dK−1)(N−1)/(d²−1) <=K(N−1)/d.

Concavity/Cauchy–Schwarz on the joint weighted spectral law gives E_C Tr[A sqrt(G)]<=t. Thus our IMPLEMENTABLE soft recovery satisfies

    E_C Bell failure <= [(20/9) beta+2epsilon] t.      (7)

No lower singular-value bound, successful-block test, error-weight reconstruction or environment access was used. Constants are less sharp than exact polar recovery, intentionally. Null directions and poor individual seeds are allowed. The assertion is an averaged-code guarantee for each fixed physical T, not a common good seed for all T or a per-record certification. Approximate designs require their own explicit second-moment error; the source's design precision argument cannot be dropped.

## 5. What is actually newly enabled

For this COMPLETE nontrivial reference error space, both its oracle construction and a useful polar-type decoder have gate counts polynomial in k and the requested inverse precision, despite d being exponential in k. The code dimension K can itself be exponential: for example K<=eta d/N makes the reference average boundO(eta). Quantum registers scale as log d+log K+log N=O(k), not d classical amplitudes. This is a constructive special-case answer to a decoder implementation gap, not a generic QSVT invocation.

The polynomial from(4) is conservative: alpha≈O(k²) yields degree roughlyO(k^4 log(k/epsilon)), before the coefficient/representation/encoder circuit bill. This is not a practical gate-count advantage over a strong decoder. Faster established sign approximations could improve that degree, but are not needed for polynomiality.

## 6. Scope that limits the opportunity

The observable local sectors must actually be lambda=mu=(m,m). These exact sectors can be uncommon; their sampling probability and rejected blocks are part of the overall yield. This note does not provide efficient decoders for every local Schur outcome.

Only environmental sectors(k) and(k−2,2) are retained. Under rank ceiling2 and k>=10 these are the nonzero-multiplicity sectors in the dimension cutoff d_nu<=d_(k−2,2): the standard sector has multiplicity0. This fact is not essential to(7), which accepts an explicitly chosen T. Other environment-sector weight is charged as rejected/bad source mass. For a fixed positive-entropy iid mixed source, near-one-row sectors generally do NOT carry most probability as k grows. A global rank2 promise alone does not establish useful total yield or vanishing overall error. The regime instead exposes a low-defect, near-pure or finite-block opening. It is scientifically narrower than the general coherent-information-rate theorem.

A nonrectangular lambda can have extra multiplicity copies invisible to the transposition span; mere inclusion of an easy error subspace would not implement the full reference. Extending the efficient span to such multiplicities or growing-defect sectors is a genuine next obligation. Unknown generic Kraus access, full reference-channel Stinespring access, ideal quantum random-access memory, or an inverse permutation oracle are not smuggled into(3).

No hardware, compiled QSVT phase circuit, positive-throughput universal protocol, historical priority or general no-environment decoder has been demonstrated. This construction is separate from the correlated-memory125-pair distillation comparator and from Astra's actual noisy five-qubit controller.
