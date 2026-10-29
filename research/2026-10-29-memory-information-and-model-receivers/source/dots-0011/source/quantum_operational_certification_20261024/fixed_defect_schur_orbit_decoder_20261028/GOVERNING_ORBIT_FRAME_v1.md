# Fixed-defect Schur recovery from explicit subgroup-orbit frames

28 October2026. **Author theorem candidate; independent review pending.** This extends the preserved rectangular construction to unequal and nonrectangular local sectors. It is not a full decoder for arbitrary positive-entropy mixed sources. No unknown environment, Clebsch–Gordan basis or exponentially large Choi matrix is accessed.

## 1. Objective and supplied input

Let lambda,mu be partitions of k, with real Young-orthogonal Specht spaces V_lambda,V_mu of dimensions d,D. Fix an integer defect j, 0<=j<k. Let H=S_(k−j) fix the last j labels pointwise and L=[S_k:H]=(k)_j. Let S be any selected set of partitions nu with nu_1>=k−j. A rank ceiling, dimension cutoff or other computable predicate may further restrict S.

The target is the full Choi error space consisting of ALL multiplicity copies of these nu in Hom(V_lambda,V_mu). The corresponding orthogonal isotropic reference channel and the physical positive error weights are those of the universal Schur code. Its decoder input also includes an actual code-isometry circuit C:C^K→V_lambda and its inverse, not an exponential dense table. K>=2 and d>=2 are the substantive case; K1 is a trivial one-dimensional output. Random-code averaging assumes code choices independent of physical weights; any approximate-design moment error remains paid.

Central primary source: Rizzo et al., *Universal quantum coding*, arXiv2609.38038v1, equations14,63–66,74–79,146–152 and implementation discussion after175. That source defines the reference/error-weight interface and leaves efficient polar implementation open. The present contribution is an explicit access construction for fixed defect, not a new statement that QSVT implements a supplied matrix. Standard Schur branching, subgroup averaging and QSVT are credited ingredients. Astra's separately reviewed gap-free error-frame recovery lemma supplies the total decoder once access is built.

## 2. Explicit H-invariant matrix units

Restrict the Young bases to their first k−j entries. A tableau of shape lambda is uniquely a prefix tableau T of some shape alpha⊢k−j and a suffix branching path q of length j ending at lambda. Similarly use p for mu. For each common alpha and every pair(p,q), define a partial isometry

    E_(alpha,p,q)|T,q> = |T,p>,

zero on other suffix paths. This is an explicit map V_lambda→V_mu preserving T. Branching gives

    Hom_H(V_lambda,V_mu)
       = span{E_(alpha,p,q)}.

No irreducible tensor-product coupling basis is required. If a_lambda,alpha and a_mu,alpha count suffix paths, the seed count is s=sum_alpha a_lambda,alpha a_mu,alpha. Distinct seeds are Hilbert–Schmidt orthogonal and ||E||_HS²=d_alpha.

Normalize the operator-space inner product as <A,B>=Tr(A†B)/d and set

    F_(alpha,p,q)=sqrt(d/d_alpha) E_(alpha,p,q).       (1)

These seeds are an orthonormal basis of the H-fixed subspace. The induction dimension bound d<=L d_alpha holds whenever alpha occurs in the restriction, because V_lambda appears in Ind_H^(S_k)V_alpha, whose dimension is Ld_alpha. Therefore ||F_s||_op<=sqrt(L). The total number of lambda paths is at most L: d=sum_alpha a_lambda,alpha d_alpha and every nonzero d_alpha>=d/L. The same holds for mu. Consequently s<=L².

All paths are enumerated by j corner removals. For fixed j, the counts, hook-formula dimensions and coefficient bit lengths are polynomial in k. If s=0, no selected low-defect error exists and the algorithm returns a fixed output; it does not invent a nonempty reference channel.

## 3. Orbit synthesis and complete multiplicities

Choose canonical right-coset representatives g in S_k/H by the ordered images of the last j labels; fill the other images in increasing order. There are L representatives. Define normalized orbit columns

    F_(g,s)=p_mu(g) F_s p_lambda(g)†,
    B:C^(L s)→Hom(V_lambda,V_mu),  B|g,s>=F_(g,s).

Write M=L s<=L³. Because seeds are H-invariant, left multiplication permutes cosets without changing the seed index. Thus B intertwines the known coefficient representation

    R = Ind_H^(S_k)(1) tensor I_s

with the conjugation action on Hom(V_lambda,V_mu).

Let P_H be the orthogonal projector onto the H-fixed subspace of Hom. Then

    BB† = sum_(gH) rho(g) P_H rho(g)†
         = L times the full-group average of P_H.

Decompose Hom as direct sum V_nu tensor C^(g_lambda,mu,nu). On that component P_H=P_(V_nu^H) tensor I. Put h_nu=dim V_nu^H. Schur averaging gives exactly

    BB† = direct_sum_nu [L h_nu/d_nu] I_nu tensor I_mult.   (2)

Branching identifies h_nu with the number of length-j paths from the row(k−j) to nu. It is positive exactly when nu_1>=k−j. Thus the orbit spans EVERY multiplicity copy of EVERY selected low-defect irrep; it is not just one convenient submodule. Moreover Ind_H1 has dimension L and contains h_nu copies of V_nu, so 1<=L h_nu/d_nu<=L whenever h_nu>0. There is no exponentially small nonzero orbit-frame eigenvalue.

## 4. Known coefficient-space correction: no Gram acquisition

Let Q_nu be the isotypic projector for nu in the L-dimensional coset permutation representation. Form the explicit contraction

    Z = sum_(nu in S) sqrt[d_nu/(L h_nu)] Q_nu,

and extend it by I_s on seed labels. Define A=B(Z tensor I_s). Intertwining and(2) imply

    AA† = Pi_S,                                        (3)

the FULL selected Choi error projector in Hom, including all multiplicities. Columns A_a form a redundant Parseval error frame. No quantum trace estimation, source samples, operator tomography, unknown Gram matrix, or numerical inverse of a hidden frame is needed.

The Q_nu are computable on a polynomial-size known representation. Adjacent transpositions act as explicit permutation matrices on ordered j-tuples. Build the commuting Jucys–Murphy matrices J_l=sum_(i<l)R((i,l)). Their joint eigenvalues are integer tableau contents in[−k,k]; joint content strings identify the Young shape. Exact spectral projections can be made by Lagrange polynomials on the integer spectrum, with denominator bit lengthO(k log k) per step. Refining joint spectral blocks through k stages produces at most L nonzero blocks at each stage, because they have positive integer ranks summing to L. Group the blocks by final shape to obtain Q_nu. Rational arithmetic, matrix sizeL and bit lengths remain polynomial for fixed j. A single central transposition sum is NOT sufficient in general: different shapes can have the same content sum. The retained failed v1 numerical check illustrates this collision and v2 uses full joint decomposition for its independent target check.

One may compile the known contraction Z by the unitary dilation

    [[Z, sqrt(I−Z²)], [sqrt(I−Z²), −Z]].

Both matrices use the same known projectors and explicit scalar coefficients. It is an L-dimensional operation, repeated trivially on the seed label; not a d- or D-dimensional dense matrix. Standard finite gate synthesis costs polynomial in L and log(1/precision).

## 5. Physical block access and cost

In Young-tableau encoding, a seed E_(alpha,p,q) is implemented by checking the known suffix path q and reversibly replacing it with p while preserving the prefix. Use a shape/direction flag and its inverse to complete the partial isometry to a unitary on a padded register. Controlled rotation by sqrt[d/(L d_alpha)] yields an exact projected block F_s/sqrt(L), up to declared gate synthesis precision. Dimension ratios come from integer hook formulas. There is no preparation of a uniform exponentially large prefix bank.

Each p_lambda(g),p_mu(g) is implemented as a polynomial-length product of adjacent Young generators. These act on at most two tableaux, with computable axial-distance coefficients and reversible validity checks. Tableau storage usesO(k log k) bits. This does not enumerate d or D tableaux. A code circuit C is used on the input logical register.

Apply Z to the input error label, apply the controlled normalized orbit seed, then project the coefficient label onto the known uniform M-state. Embedded as a projected unitary block, not physical postselection per query, this gives

    W_A|x,a>=A_a C|x>,
    W_A/alpha,    alpha=sqrt(L M)<=L².                (4)

This follows because SELECT supplies1/sqrt(L) and the uniform projection supplies1/sqrt(M); Z is a contraction encoded with normalization1. Preparing the known uniform coset/seed registers costs polynomial in M. Input and output projector controls and inverse circuits are included. For j fixed, every preparation, table, classical computation and quantum block query is polynomial in k, logK and precision. Constants/exponents in j are NOT hidden as uniform polynomiality: L=k(k−1)...(k−j+1), so the cost grows as k^(O(j)).

Implementation errors are charged at the block/circuit level. All seed operator norms are bounded bysqrt(L), and coefficient-space operations have polynomial dimension. Entrywise coefficient approximation can be converted to operator error using these bounds and polynomial M; no false HS-to-operator conversion with an omitted sqrt(d) factor is used. Actual unitary synthesis errors compose over the performed gates. These statements provide an algorithmic gate-access theorem, not a compiled laboratory pulse sequence.

## 6. Why redundant error labels do not spoil polar recovery

Choose ABSTRACTLY an orthonormal basis F of range(Pi_S), dimension N. Equation(3) means A=F V† for an isometry V:C^N→C^M. This V need not be computed. Any physical positive error weight T in the orthonormal basis is embedded as

    T_red=V T V†,
    W_A=W_F(I_K tensor V†).

The physical encoded output is unchanged. The redundant Gram has M−N null directions, but T_red is supported on VV†. On that support its weighted Gram defect agrees exactly with the orthonormal one. One cannot apply an orthonormal formula with arbitrary M-dimensional weights or replace N by M inside an equality.

Every odd singular-value filter f satisfies f(0)=0. Its decoder contraction obeys

    R_A=(I_K tensor V) R_F.

Thus tracing the M-dimensional error register gives exactly the same recovery as tracing the N-dimensional one. Also W_AW_A†=W_FW_F†, so the failure flag and prepared fallback agree. This proves that the total soft-polar decoder is independent of the unknown multiplicity basis. N<=M is used only for conservative resource/rate upper bounds.

## 7. Error guarantee, encoder precision and source scope

The reference frame F is orthonormal in normalized HS inner product and invariant under left/right irreducible group action. Therefore sum_i F_i†F_i=N I_d and sum_i F_iF_i†=(dN/D)I_D, exactly the orthogonal isotropic interface. For Haar code C, the source Gram identity gives, for each fixed T independent of C,

    E weighted Gram defect = beta Tr T,
    beta=(dK−1)(dN/D−1)/(d²−1) <= KN/D−K/d.          (5)

For the reviewed bounded positive-binomial soft filter, a total CPTP decoder implemented through(4) has averaged Bell failure at most

    [(20/9) beta + 2 epsilon] Tr T                   (6)

under the ideal Haar ensemble. The2epsilon improvement uses the first Gram moment and concavity; the simpler uniformly valid remainder2alpha epsilon may always be substituted. The standard fast bounded sign filter instead gives4beta with the corresponding remainder and query degreeO(alpha log(1/epsilon)); the positive filter has degreeO(alpha² log(alpha/epsilon)). Neither requires a smallest singular value promise. These are mean failure-weight statements, not per-seed or per-history certificates.

An approximate two-design must approximate the appropriate first/second moments with a stated norm. A conservative diamond-norm moment budget eta gives extra mean defect at most

    eta [K M² alpha^4 + 2M alpha²],                  (7)

for normalized T. To see it, expand the quadratic Gram expression in the orthonormal error basis. Each F_i has operator norm<=alpha (write F=BZV and use coefficient2-norm<=1 plus seed normsqrt(L)). The quadratic swap-test coefficient norm is bounded byN²alpha^4, its two-copy code-projector input has traceK², and the prefactor is1/K. The linear term is bounded by2Nalpha² and its input has traceK. Replace N by M only in these bounds. The first moment is inherited from the second-moment channel by feeding a maximally mixed second input. For approximate designs one may retain the uniform2alpha epsilon filter remainder to avoid silently transferring the exact Haar first moment. Choosing eta inverse-polynomial in those displayed quantities needs only polynomial logarithmic precision even when K is exponential. Actual availability of a suitable efficient code ensemble remains an explicit encoder dependency; it is not supplied by a Gaussian sum over all permutations.

The physically selected Schur environment labels are orthogonal after tracing the environment. Consequently excluded nu mass is a positive bad component and can be charged linearly. Arbitrary cross-selected/rejected coherent error weights would require a separate analysis and are NOT assigned this linear bad-mass bound. Within selected sectors, arbitrary positive weights and multiplicity coherences are retained. Alice's complete code-block outcome must preserve the physical weight independence required by the source argument.

Since N<=M, K<=eta0 D/M gives conditional reference failureO(eta0), provided K<=d. This can leave exponentially large K even while all fixed-j access costs are polynomial. However a fixed j only captures environment Schur diagrams within j boxes of the first row. A generic fixed positive-entropy iid mixed source has growing defect; low global rank alone does NOT imply significant selected mass. The present theorem removes rare exact-rectangle local-sector restrictions, not this environmental limitation. Source probability, rejected sectors, code-block residues, sampled encoder precision, gate errors and storage/control costs all remain in any complete rate claim.

For j growing with k the explicit access cost is k^(O(j)); no uniform efficient decoder for extensive defect follows. This parameter dependence is an honest route for further work, not concealed exponential complexity. No hardware operation, general coherent-information-rate implementation, historical novelty or superiority over an equally informed conventional group-representation algorithm is claimed.

### Subnormalized good-sector clarification

For a general positive T, an individual code's good output may have mass p_C=Tr[(pi_K tensor T)G] different from t=Tr T. The soft-filter proof bounds Bell ERROR MASS, not a normalized channel loss. The purification chi has norm²t and the actual encoded vector has norm²p_C. If z=<chi|sqrt(G)f(sqrt(G)/alpha)|chi>, the success Bell mass is at least|z|²/t for t>0. Therefore p_C−Bell_mass<=p_C+t−2Re z, the same spectral penalty used above. The t0 case is zero. No pointwise TP assertion is imported for a subnormalized selected branch.

## 8. A realizable source promise: bounded expected contamination

Suppose the unknown iid block source rho_k has largest eigenvalue at least1−c/k, with arbitrary unknown dominant eigenvector and arbitrary orthogonal contaminating state. The contaminating rank is unrestricted. Let nu be the environment Schur label of any purification. Then

    Pr[k−nu_1>j] <= Pr[Binomial(k,c/k)>j].             (8)

Proof: diagonalize the environment marginal, whose nonzero spectrum equals that of rho_k. In a computational eigenbasis string, let n0 count occurrences of its largest-eigenvalue symbol. The string is invariant under permutations of those n0 equal positions. A Specht sector with a nonzero projection of that string must contain an invariant vector for a conjugate S_n0; branching implies nu_1>=n0. Thus defect k−nu_1 is at most the number of non-dominant symbols. Those symbols have iid Bernoulli probability at mostc/k, giving(8). This is a proof of distributional dominance, not an assumption that quantum errors are classical independent events at the output. The protocol does not know the diagonalizing eigenvector.

For fixed c and target error, choose fixed j so the binomial/Poisson tail is small. Then the orbit access remains polynomial in k and covers all local lambda,mu at that defect. A supplied local Schur-dimension lower quantile supplies the desired code size; selected local code blocks still incur their actual residual/packing and implementation budgets. For fixed local dimension and a family tending to a pure entangled state, standard Schur spectrum concentration can provide large typical D, but this manuscript does not replace those source probability bounds by a bare rank claim.

This is not merely treating the entire block as pure. For rho_k=(1−c/k)|psi><psi|+(c/k)tau with tau orthogonal to psi, the trace distance between rho_k^tensor k and |psi><psi|^tensor k is exactly1−(1−c/k)^k, tending to1−e^(−c). At c1 that is about.632, whereas a fixed sufficiently large defect cutoff makes(8) much smaller. The decoder corrects the representation error family rather than spending that constant pure-approximation loss. This distinguishes a nontrivial source regime from the trivial rank1/pure case.

Fixed positive contamination does not meet this promise: its typical defect grows linearly, making the present k^(O(j)) algorithm expensive. A joint limit of vanishing target error may also require growing j. These costs remain explicit.
