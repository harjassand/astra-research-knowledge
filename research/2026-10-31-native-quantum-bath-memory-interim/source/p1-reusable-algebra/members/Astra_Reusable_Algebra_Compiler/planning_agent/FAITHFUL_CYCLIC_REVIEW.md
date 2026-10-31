# Independent proof review: faithful cyclic compression of a Hermitian operator library

## Verdict

The exact theorem is correct. It produces a reusable finite representation of every future expression in a fixed finitely generated matrix *-algebra. The all-future spectral conclusion is stronger than one fitted response, but its mathematical mechanism is established cyclic-subspace / GNS representation theory and simultaneous matrix-* algebra reduction. Novelty cannot be inferred from an independently derived proof.

The genuinely useful question is whether the matrix-free acquisition interface, total costs, and adaptive trace certification produce something beyond existing implementations. The theorem below gives an exact executable acquisition without supplying hidden blocks or a basis as input.

## Fixed library and algebra

Fix Hermitian matrices A_1,...,A_k in C^(N x N) before randomization. Let A be their unital complex *-algebra. Its unitary representation has the form

    A ≅ direct_sum_alpha (M_(r_alpha)(C) tensor I_(m_alpha)).

Write a=dim_C A=sum r_alpha^2 and N=sum r_alpha*m_alpha.

For g in C^N, let K=A g=span{w(A)g: w is a finite word}. If G_alpha is the r_alpha-by-m_alpha reshaping of g's component in block alpha, then

    dim K = sum_alpha r_alpha * rank(G_alpha).

To see this, the alpha block of A g is the image of X -> X G_alpha. Its kernel consists of matrices killing the column space of G_alpha, so its image has dimension r_alpha*rank(G_alpha). Different simple blocks are independently selectable by the central projections of A, and therefore the dimensions add.

Because the A_i are Hermitian, K is reducing. If Q is an orthonormal basis of K, compression rho(X)=Q*XQ is a unital *-homomorphism: XQ=Qrho(X), hence rho(XY)=rho(X)rho(Y) and rho(X*)=rho(X)*.

The restriction in block alpha is M_(r_alpha) acting with multiplicity s_alpha=rank(G_alpha). It is faithful iff s_alpha>0 for every alpha. A Gaussian g has maximal possible rank s_alpha=min(r_alpha,m_alpha), almost surely. Thus

    D=dim K=sum r_alpha min(r_alpha,m_alpha) <= min(N,a).

All simple blocks remain present, so rho is injective. In a finite-dimensional unital *-algebra, a faithful *-representation preserves spectra, invertibility, operator norm, singular values as a set (not their multiplicities), and the positive cone. These statements apply simultaneously to every future element X in A, including elements selected adaptively after inspecting the compressed representation.

In particular, if all inverses used in a noncommutative rational expression exist in the original system, its compressed evaluation exists and agrees with rho of the original evaluation. Conversely, compressed invertibility certifies original invertibility. Determinants and traces are NOT preserved without the original multiplicity weights.

## Finite-randomness version

Continuous Gaussian samples are unnecessary for the exact algebraic theorem. Choose each standard-coordinate entry of g independently and uniformly from a finite real set S of q distinct rational numbers.

For each alpha, choose one maximal minor of the linear reshape G_alpha(g) whose determinant is a nonzero polynomial in the coordinates of g. Such a minor exists because the coordinate transformation is invertible over C. The product of these minors is a nonzero complex polynomial of degree

    b=sum_alpha min(r_alpha,m_alpha) <= N.

The elementary polynomial zero-count bound gives failure probability at most b/q <= N/q. Hence q>=N/delta gives the same maximal-rank conclusion with probability at least 1-delta. Coefficients of the polynomial need not be known by the algorithm. The matrices must be fixed before the random draw. The probability statement concerns a polynomial over C evaluated on the rational grid, which is legitimate because a nonzero complex polynomial cannot vanish identically on the real grid of arbitrary size.

For faithfulness alone, full rank is unnecessary: it is enough that every simple-block component be nonzero.

## Exact executable acquisition

Input is only N, the k matrix-vector services, and a chosen seed g. No irreducible blocks, symmetry group, basis, or algebra dimension is provided.

1. Initialize an independent-vector queue with g (resample if g=0).
2. For each queued basis vector v_i and every generator A_j, query y=A_j v_i.
3. Test whether y lies in the current span. If not, append y to the basis queue. Retain its word/provenance. Record the exact coefficient vector for y in the eventually padded basis.
4. Stop when every generator has been applied to every retained basis vector.

If the final dimension is D, precisely kD generator applications suffice. Closure gives an invariant subspace containing g; induction in word length shows it equals K. No enumeration of k^D words is needed.

Using a maintained rank factorization, a conservative arithmetic cost is O(k N D^2 + k D^3), in addition to the kD matrix-vector service costs. Storage is O(ND+kD^2). Generating and reading the seed costs O(N); the output vectors from the acquisition each have N coordinates. Thus the acquisition cost is not dimension-free.

An exact rational implementation can avoid square roots: retain a nonorthogonal basis V and Gram matrix G=V*V, and generator coordinate matrices B_j satisfying A_j V=V B_j. Then G B_j=B_j* G. The compressed inner product is x*G y. A Cholesky change of coordinates produces Hermitian matrices if desired, but generalized Hermitian pencils already express positivity and spectral questions. Bit complexity depends on the rational description or exact-field oracle and rank arithmetic; a real-arithmetic matvec count is not a bit-complexity theorem.

Every acquired word has length at most D-1, since each new vector extends one already acquired word. That depth does not bound inverse conditioning or numerical stability.

## Finite-precision limitations

### Arbitrary future rational expressions are not uniformly robust

The two libraries {0} and {diag(0,eta)} are eta-close in operator norm. Yet the future expression p(X)=X/eta separates their spectra by one. The denominator X-eta I is invertible for the first and singular for the second. Therefore an approximate generator fit cannot preserve every future expression uniformly without charging coefficients, word/circuit depth, conditioning, and spectral/PSD margins.

The algebra dimension is itself unstable. Let A=diag(1,2,...,N) and B_eta=eta times the adjacency matrix of a connected path. At eta=0 the generated algebra is the N-dimensional diagonal algebra. For every eta != 0 the generated *-algebra is all M_N: polynomial spectral projectors of A isolate diagonal units, E_ii B_eta E_jj gives adjacent matrix units, and products give all matrix units. Small numerical residuals therefore cannot certify a small exact algebra dimension.

### Small closure residual does not certify that every spectral sector is present

A subspace can be exactly invariant while missing an entire block. If the seed has zero component in that block, the omitted block is invisible to every word on the seed. Randomization controls this only for a fixed library and exact arithmetic; tolerance-based rank decisions need a quantitative lower bound on sector visibility or an explicitly probabilistic numerical analysis.

For a concrete noisy oracle model, suppose each reply obeys ||reply-A v|| <= eta ||v||. Compare A_0=0 and A_1=lambda u u*, with ||u||=1. A zero reply is permitted whenever |u*v|/||v|| <= eta/lambda. Against any q-query algorithm receiving the all-zero transcript, its queries are fixed conditional on its randomness. For uniform complex-sphere u,

    P(|u*v|/||v|| > t) = (1-t^2)^(N-1) <= exp(-(N-1)t^2).

A union bound shows that all q zero replies can be consistent with A_1 with probability at least

    1 - q exp(-(N-1) eta^2/lambda^2).

Thus a small set of probes at this adversarial per-query error level cannot reliably rule out a norm-lambda hidden sector. This is a statement about the specified per-query noise model, not about a single fixed global perturbation bound or arbitrary stochastic noise models.

## Adaptive enlargement must refresh randomness

The uniform theorem covers every adaptive expression in the fixed acquired algebra. It does not cover arbitrary new generators selected after seeing g or K. If dim K<N, choose a unit u perpendicular to K and introduce A_new=u u*. Every existing seed word remains blind to its eigenvalue one, and naive closure testing reports no new direction. An independently randomized new seed, with a fresh error allocation and acquisition cost, repairs this probabilistically for the enlarged fixed library. No free cumulative guarantee should be claimed across adversarially chosen new generators.

## Existing primary machinery to compare directly

1. Murota, Kanno, Kojima, and Kojima, **A Numerical Algorithm for Block-Diagonal Decomposition of Matrix *-Algebras, Part I** (2007 preprint; 2010 journal publication). Primary preprint: https://optimization-online.org/2007/10/1802/ and https://optimization-online.org/wp-content/uploads/2007/10/1802.pdf . Finds irreducible decomposition from matrix generators and applies it to SDP.
2. Maehara and Murota, **A Numerical Algorithm for Block-Diagonal Decomposition of Matrix *-Algebras, Part II: General Algorithm**: https://optimization-online.org/2009/05/2292/ . The generated algebra is the input; hidden symmetry is not assumed known.
3. Maehara and Murota, **Algorithm for Error-Controlled Simultaneous Block-Diagonalization of Matrices**, SIAM J. Matrix Analysis and Applications (2011), DOI 10.1137/090779966. Primary preprint: https://www.keisu.t.u-tokyo.ac.jp/data/2009/METR09-53.pdf . Explicit numerical error control is existing machinery.
4. de Klerk, Pasechnik, and Schrijver, **Reduction of Symmetric Semidefinite Programs Using the Regular *-Representation**: https://optimization-online.org/2005/03/1083/ . Low-order faithful matrix-* representations for SDP are established.
5. Zhang and Motter's matrix-* algebra SBD implementation sequentially explores invariant subspaces under matrix multiplications: https://github.com/y-z-zhang/net-sync-sym . Its paper must be inspected before treating the BFS acquisition itself as new.

## Assessment

The construction earns a reusable spectral computation interface from actual matrix-vector access and proves a simultaneous guarantee. That is useful. It does not yet demonstrate a new computational boundary over the strongest retained invariant-subspace/*-algebra methods. Its most defensible developing contribution would be an operationally complete theorem joining acquisition, uniform adaptive trace estimation, numerical visibility, and downstream costs, if the latter supplies a new advantage rather than a restatement of regular-representation SDP reduction.
