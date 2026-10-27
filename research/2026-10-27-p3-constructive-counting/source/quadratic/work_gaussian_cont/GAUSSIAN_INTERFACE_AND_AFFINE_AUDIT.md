# Dense quadratic backgrounds: exact interfaces and the sparse-dual compiler

27 October 2026. Conditional algorithm statements refer to the proved phase-product extension of the supplied OpenAI manuscript. The algebraic identities and restricted architecture obstructions below are unconditional finite-dimensional statements. They are not general lower bounds for algorithms.

## 1. The unsolved extension and why it would matter

The target is

    Z = sum_x (-1)^[Q(x)+P(x)],

where Q is an arbitrary explicitly given quadratic polynomial over F_2, possibly containing Theta(n^2) monomials, and P is a sum of n exp(o(log n)) explicitly local fixed-degree phase terms. The phase-product theorem handles P without charging for its intermediate XOR states. Inserting all of Q's quadratic monomials into that theorem can destroy the small logarithmic-incidence parameter. Quadratic Q alone is exactly summable by Gaussian elimination. The issue is their interaction.

This extension would imply an original-input subexponential theorem for XOR/AND straight-line programs with O(n) nonlinear gates and arbitrarily many explicit XOR states, by the exact construction in Section 4. No sparse affine matrix or small cross-rank is needed for that reduction.

## 2. A precise barrier to integrating Q through the existing group sums

Split x=(u,v). Write

    Q(u,v)=Q_U(u)+Q_V(v)+u^T Bv,

and define the rational matrix K indexed by Boolean u,v, with K_(u,v)=(-1)^Q(u,v). Then

    rank_Q K = 2^[rank_F2 B].

Proof: multiplying rows and columns by the nonzero within-side phases preserves rank. The remaining row for u is the Walsh character v -> (-1)^[(B^T u)·v]. There are exactly 2^[rank B] distinct such characters. Distinct characters are orthogonal over Q, and hence linearly independent.

Consequently an exact identity K(u,v)=sum_(j=1)^R a_j(u)b_j(v) needs R>=2^[rank B]. More generally, if summary states are enumerated and each state's residual kernel is represented by a sum of separated products, then the total number of products over all summary states obeys the same lower bound. For a source-like architecture with 2^o(n) summary tuples and 2^o(n) separated residual terms, a linear cross-rank is fatal.

This applies to a universal Gaussian interface preserving arbitrary local group functions. It does NOT forbid a global Gaussian algorithm using the particular function descriptions; in particular Q alone remains polynomial-time summable despite this high matrix rank. The result excludes an otherwise tempting plug-in for Lemma 3.2, not every possible extension.

### Dense backgrounds can defeat every balanced coordinate grouping

Take a random symmetric zero-diagonal n-by-n binary matrix G, and Q(x)=sum_(i<j) G_ij x_i x_j. For a fixed cut S, its cross matrix has independent uniform entries. If a=min(|S|,n-|S|), b=max(|S|,n-|S|), then

    Pr[rank G_(S,S^c)<=a-d] <= 4·2^[-d(b-a+d)] <= 4·2^(-d^2).

Indeed every matrix of rank at most a-d has its rows in some (a-d)-dimensional subspace of F_2^b. There are at most 4·2^[(a-d)(b-a+d)] such subspaces and at most 2^[a(a-d)] row lists in each.

Choose d=ceil(sqrt(2n+4)). A union bound over all cuts shows that, with positive probability, every balanced cut has rank at least min(|S|,n-|S|)-d. In particular every cut with sides between n/3 and 2n/3 has linear cross-rank for sufficiently large n. Any partition into sufficiently small groups has a balanced union of groups, so a fully separated low-summary Gaussian kernel representation cannot be manufactured for every such Q by merely choosing a different coordinate grouping.

The probabilistic argument is an existence obstruction. It is not being used as an uncharged deterministic construction in an algorithm. The checker additionally enumerates all balanced cuts of several small explicit sampled matrices.

## 3. Exact Schur elimination can manufacture dense nonlinear phases

Let y,z be t-bit vectors, A any invertible binary t-by-t matrix, and f(x),g(x) any Boolean vector functions. Direct summation gives

    sum_(y,z) (-1)^[y^T A z+y^T f(x)+z^T g(x)]
       = 2^t (-1)^[g(x)^T A^(-1) f(x)].

Summing y first imposes Az=f(x), leaving the unique z=A^(-1)f(x). This proves the identity without a numerical Gaussian approximation.

Now let f_i=a_i b_i and g_j=c_j d_j on 4t distinct original variables. Before elimination the nonlinear part consists of only 2t cubic monomials, y_i a_i b_i and z_j c_j d_j. After exact elimination it contains one distinct quartic monomial a_i b_i c_j d_j for every nonzero entry (A^(-1))_(j,i). For dense inverse matrices this is Theta(t^2) distinct ANF monomials. They cannot cancel because their supports are distinct.

For an explicit even-t example, A=I+J over F_2 has A^(-1)=A, since J^2=tJ=0. The resulting canonical quartic polynomial has exactly t(t-1) terms. This particular matrix has additional structure, so the example is only a demonstration that unstructured ANF materialization can explode; it is not a lower bound against alternative representations. The identity holds for arbitrary invertible A, including generic dense choices.

A proposed repair that diagonalizes Q first has the same issue: the basis change turns a local product into a product of dense affine forms. Neither operation preserves the small monomial-scope representation automatically.

### What elimination does solve

Variables absent from every nonlinear factor can be eliminated in polynomial time. A general quadratic form on those variables can be put into hyperbolic pairs plus a radical. Each pair gives a factor 2 and a quadratic Schur phase; each radical variable gives a factor 2 and an affine constraint on the remaining variables. Thus the result is a new quadratic phase times affine constraints, on the union of nonlinear supports. This is useful when that union is small. When all n variables occur in local nonlinear terms, it leaves the main obstruction intact.

## 4. Exact compiler from raw XOR/AND programs to the Gaussian frontier

Let a raw straight-line program use n original inputs, t binary AND gates, arbitrary XOR gates and negations, with explicit references to earlier states. There may be arbitrarily many affine states. Introduce one formal output symbol z_i per AND gate. Scan the original program and store every affine state as an affine form in x_1,...,x_n,z_1,...,z_t. An XOR combines forms; a negation flips the constant. At an AND gate record its two affine operand forms, then replace its output by the new symbol z_i. This costs a polynomial in the raw description length and n+t, and constructs the affine data rather than assuming it.

For each AND gate introduce operand bits u_i,v_i, and impose

    u_i=A_i(x,z),  v_i=B_i(x,z),  z_i=u_i v_i.

Prescribed outputs become affine equations in x,z. Row reduction can discard dependent output equations; inconsistency gives count zero. Their independent number q is at most n+t.

There are n+3t primal variables and r=3t+q equations. Add a Fourier multiplier lambda_j for each equation. The phase is the XOR of lambda_j times its equation. Every affine equation contributes only linear and quadratic monomials, potentially dense. Each nonlinear equation contributes one cubic monomial lambda_i u_i v_i, plus the quadratic lambda_i z_i. Thus the whole phase has an arbitrary quadratic background and exactly t local cubic terms, on

    N=n+6t+q <= 2n+7t

Boolean variables. Summing the multiplier bits enforces every equation:

    sum_(all primal bits, multipliers) (-1)^phase
       = 2^r · original target-preimage count.

The primal trace is unique for each original input by the original topological evaluation, including all introduced operand bits. The known division by 2^r is exact. No intermediate XOR state is counted as an independent bit in the phase description.

This is an exact frontier reduction, not a proof that the dense-Gaussian extension has been solved. If that extension were subexponential in N for O(N) local cubic terms, it would immediately give subexponential original-n counting for t=O(n), independent of the number and density of affine states.

## 5. Audit of the parent's manufactured sparse-dual alternative

The parent proposes a narrower positive compiler: construct the affine image y=Ax+c with r=O(n) distinct readout forms, followed by m=n exp(o(log n)) explicitly local fixed-degree phase factors on y. Let a=rank A and C=im A. The dual space C^perp=ker A^T has dimension cdim=r-a.

Enumerate every row-index subset of size at most w and test whether the XOR of its LINEAR row vectors is zero. Keep a basis B_0 of the discovered dual vectors, of rank c0. This enumerates at most

    2^[O(w log(er/w))]

candidates, with polynomial bit work per candidate. Store their affine right-hand sides h·c. Do not require the augmented affine rows to XOR to zero: valid relations may have right-hand side one.

Complete B_0 to a basis B=(B_0;B_1) of ker A^T by Gaussian elimination. Put delta=cdim-c0. Every y satisfies the exact identity

    1_[y in c+C]
      = 2^(-cdim) sum_(lambda in F_2^c0,mu in F_2^delta)
          (-1)^[lambda^T B_0(y+c)+mu^T B_1(y+c)].

For each mu, regard lambda as additional Boolean inputs and add its short dual constraints to the phase polynomial. There are at most c0 w bilinear monomials lambda_j y_i, at most c0 unary offset terms, and at most r unary terms from the fixed mu. Thus the phase uses r+c0=O(n) independent summation bits and m+O(c0w+r) factors. If w=n^o(1), this is n exp(o(log n)). The degree remains fixed, at most max(k,2), and the phase-product theorem applies.

Reconstruct each inner signed phase sum exactly before summing mu and dividing by 2^cdim. This avoids precision loss from modular division. Multiply the resulting affine-image sum by the known fiber size 2^(n-a), because every affine image point has exactly that many original preimages. For Boolean phase output, convert the original signed sum to its two output counts; fixed root-of-unity outputs use the already audited character reconstruction.

The total time is

    poly(L+n) 2^[O(w log(er/w))+delta+o(n)],

and polynomial workspace, with sequential enumeration. If r+c0=o(n), direct enumeration already gives the required subexponential bound: m need not be near-linear in a much smaller r. Otherwise, along any subsequence with r+c0 bounded below by a positive multiple of n, the phase-product density condition holds in that many variables. This establishes the claimed o(n) exponent generally by the usual subsequence argument; one can implement it as the minimum of the phase-product counter and exhaustive enumeration.

Therefore the sparse-dual alternative is valid when w=n^o(1) and delta=o(n), even if cdim=Theta(n). The short dual basis is actually discovered and its search cost is charged. Generic dense affine images can have no nonzero low-weight dual vectors; then delta remains Theta(n), and the guarantee correctly disappears. This is a narrower successful compiler, not a solution of the unrestricted Gaussian/XOR-AND frontier.

The stronger parameter is the actual total weight W_0 of the retained short basis, since the factor count is m+O(W_0+r), not necessarily m+c0w. Enumerating rows in increasing weight and adding a row whenever it raises the span rank is the linear-matroid greedy algorithm, so it chooses a minimum-total-weight basis of the discovered subspace. Consequently one may allow the wider search range w log(er/w)=o(n), provided the manufactured basis satisfies m+W_0=n exp(o(log n)) and delta=o(n). The convenient condition w=n^o(1) guarantees the first two requirements automatically, but is not necessary. This refinement pays for the discovered representation's actual size.

## Executed checks

`gaussian_affine_checks.py` verifies the cross-kernel rank identity on finite examples, the Schur identity and induced quartic monomial count, the raw-program Fourier compiler against direct original-input evaluation, and the sparse-dual compiler including nonzero affine right-hand sides. Its counting and rank checks are finite exact validation, not a practical fast solver or execution of the source's asymptotic algorithm.

The executed run passed 48 kernel-rank fixtures, 43,554 balanced graph-cut checks, 304 Schur identities, 12 raw-program compiler fixtures (232,960 enumerated phase assignments), and 13 sparse-dual fixtures. Nine discovered short dual rows had nonzero affine right-hand sides. Actual results are in `gaussian_affine_results.json`.

## Primary-literature positioning

The cut-rank identity is established graph-state ancestry, not a claimed new theorem: M. Hein, J. Eisert and H. J. Briegel, *Multi-party entanglement in graph states*, Phys. Rev. A 69, 062311; https://arxiv.org/abs/quant-ph/0307130 . The statement is also proved directly above to make its restricted algorithmic implication explicit.

Clifford-plus-diagonal simulation already has extensive machinery based on stabilizer decompositions; an appropriate primary comparison is S. Bravyi et al., *Simulation of quantum circuits by low-rank stabilizer decompositions*, https://arxiv.org/abs/1808.00128 . Our notes make no performance claim over those algorithms.

A recent broader representation is A. Bauer and S. Lloyd, *Quadratic tensors as a unification of Clifford, Gaussian, and free-fermion physics* (21 January 2026), https://arxiv.org/abs/2601.15396 . Its quadratic tensor coefficient representation and Schur-like contraction are pertinent machinery. The paper explicitly distinguishes this efficient quadratic closure from general higher-order tensor networks; it does not, by that result alone, supply the missing dense-quadratic-plus-local-cubic counter.
