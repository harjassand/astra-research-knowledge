# Acquired operations and their limits

## 1. Finite-word closure

Let a finite alphabet B index CP instrument branches (including the classical control), on M_d. For each control, its outcome branches sum to a trace-preserving map. Fix finitely many initial density matrices. Assume every length-L word is EB, and acquire finite Holevo decompositions for all those words. Let S contain their normalized output states and the initial states. Include each nonzero normalized prefix image Phi_w(s), s in S, |w|<L, as a separate classical state, retaining its seed and prefix label.

A branch extends a prefix when |w|<L-1. At the last step its length-L Holevo decomposition expresses the image as a nonnegative combination of boundary states. Divide coefficients by the prefix trace. Zero images are discarded, never divided by. Summing the outcomes of any current control gives one in every column. Matrix intertwining proves all transcript probabilities, including causal controls; future controls are never presampled.

With P initial states, separable conic Caratheodory gives |S|<=d^4|B|^L+P and at most |S| sum_{k<L}|B|^k prefix states. This is finite and generally enormous. This final prefix-closure step is standard positive-realization geometry, rather than a new invariant-cone method. The accepted CP/two-copositive theorem supplies L=2(d-1). It alone does not supply efficient acquisition or a finite-data learner. Root separately develops this general compiler and the finite-frame bridge; the actual acquired examples and special-family theorem below are owned here.

## 2. Sharp filtered boundary for a special family

For d>=2, c>=1, define

    Phi_c(X) = (c tr(X) I - X^T)/(cd-1).

Its Choi matrix (cI-F)/(cd-1) is positive, and the map preserves trace. The next proposition is an exact specialization of Lami-Huber2016, Theorem7 and Corollary8 (arXiv1603.02158v1). Their broader classification was found and fully read before promotion. The proof below is an independently constructed replay and explicit sampler, not a new EA boundary.

**Proposition.** Phi_c tensor Phi_c maps every bipartite input to a separable output if and only if c>=(1+sqrt(3))/2. Equivalently, Phi_c Ad_A Phi_c is EB for every single-Kraus filter A. Sums of filters follow by linearity.

Take a pure input with Schmidt coefficients x_i=sqrt(lambda_i), sum lambda_i=1. Unitary covariance reduces the unnormalized output to a matrix whose |ii> block is

    A = x x^T + diag(delta_i),   delta_i=c^2-2c lambda_i,

and whose populations on |ij>, i!=j, are b_ij=c^2-c(lambda_i+lambda_j). The full normalization is (cd-1)^2. A is positive semidefinite because it is a principal block of a CP-map output. At most one delta_i is negative, since two associated lambda_i would each exceed c/2>=1/2.

A has a factorization A=VV^T with V entrywise nonnegative. Eliminate indices with delta_i>=0 first. If the current residual is diag(delta)+alpha x x^T, alpha>=0, a positive pivot k updates alpha to

    alpha delta_k/(delta_k+alpha x_k^2) >= 0.

Every Cholesky column is nonnegative. A zero pivot has zero row by positivity and is omitted. The last exceptional diagonal is nonnegative by the Schur complement. The same elimination works when all delta are nonnegative; the elementary sum diag(delta)+xx^T is an alternative factorization.

For each column v of V, average projectors of

    (sqrt(v_i) z_i)_i tensor (sqrt(v_i) conjugate(z_i))_i

over unit phases with the quartic moments of independent phases. This produces vv^T on the |ii> block and populations v_i v_j on |ij>, i!=j. Summing columns realizes A and cross-populations A_ij=x_i x_j. The remaining populations are nonnegative:

    b_ij-x_i x_j >= c^2-c-1/2 >= 0,

because lambda_i+lambda_j<=1 and sqrt(lambda_i lambda_j)<=(lambda_i+lambda_j)/2. Add these computational-basis product projectors and normalize. Mixed inputs follow by linearity.

Conversely lambda_1=lambda_2=1/2 gives a partial-transpose block with eigenvalue c^2-c-1/2. It is negative below the threshold, in every d>=2. This proves necessity.

For the filtered formulation, vectorize a matrix A as |psi_A>=(A^T tensor I)|Omega>. The matrix transpose of the superoperator Phi_c equals itself. Moving a map across |Omega> therefore identifies the Choi matrix of Phi_c Ad_A Phi_c with (Phi_c tensor Phi_c)(|psi><psi|), with |psi>=(I tensor A)|Omega>. This is an exact equivalence. It is a two-site/serial-filter identity, not arbitrary-copy tensor stability.

The bound extends below the accepted two-copositive premise c>=2. For c<2, t Phi_c is not two-positive: its action on a Schmidt-rank-two maximally entangled vector has a negative eigenvalue. This special-family conclusion therefore uses the explicit factorization, rather than silently applying the accepted word theorem outside its assumptions.

## 3. Polynomial phase discretization and an explicit trajectory sampler

Choose an odd prime p>=d, index i=0,...,d-1, and put z_i(a,b)=exp(2 pi i (a i+b i^2)/p), a,b in F_p. Averaging z_i conjugate(z_j) conjugate(z_k) z_l vanishes unless

    i+l=j+k,  i^2+l^2=j^2+k^2  (mod p).

Since p is odd and all indices are distinct representatives, these equations say {i,l}={j,k}. They yield exactly the required independent-phase quartic moments. There are p^2 assignments, at most O(d^2), and at most d nonnegative Cholesky columns. This supplies a polynomial-size finite decomposition, without enumerating exponentially many independent phases.

Sampling is simpler. Select column v with unnormalized probability (sum_i v_i)^2 or select a residual basis population b_ij-x_i x_j. For a selected column, sample a,b uniformly and output the normalized local vectors sqrt(v_i)z_i and its conjugate, rotated back by the input Schmidt bases. Their product projector has the required average. The total unnormalized probability is (cd-1)^2. Gate multiplication, Schmidt decomposition and nonnegative factorization are explicit local matrix operations; there is no generic separability oracle. Exact algebraic inputs give algebraic factors. A uniform polynomial bit-precision/stability analysis at singular parameter boundaries is not supplied by the arithmetic construction.

This is an acquired ordinary separability-preserving trajectory comparator for the finite-frame compiler: after any two-site gate, the equal local noise above leaves a product-state mixture. It provides classical sampling at fixed local dimension by the Harrow-Nielsen approach. A finite cached frame is not a new tractability class. No statement here establishes the corresponding property for arbitrary many-site gates.

## 4. Direct local frame and a genuine tensor obstruction

For d=3 let P15 contain computational basis projectors and, for each i<j, projectors onto (e_i+z e_j)/sqrt(2), z in {1,-1,i,-i}. Its cone contains every Hermitian Y satisfying

    Y_ii >= sum_{j!=i} (|Re Y_ij|+|Im Y_ij|).

Split each real and imaginary coherence between the corresponding signed pair projector and leave the nonnegative diagonal remainder. For X>=0, tau=tr X, x=X_ii/tau,

    sum_{j!=i}(|Re X_ij|+|Im X_ij|)
       <= tau sqrt(2(d-1)x(1-x)).

The maximum of x+sqrt(2(d-1)x(1-x)) is (1+sqrt(2d-1))/2. Consequently Phi_c(PSD_d) lies in this finite pair-phase cone whenever c exceeds that value. For c=2 this holds for d<=5; for d=3 it holds already at the golden ratio. At c=2 the diagonal residual in the normalized output is at least tau(3-sqrt(5))/10. This gives an explicit finite-state simulator for arbitrary single-site filters followed by the noise. The inverse coordinates use absolute values and are not a fixed positive affine encoding of arbitrary quantum inputs; Phi_c need not be EB.

Tensoring this frame fails even at c=9/5, where each single-site operation closes. The exact rational witness W and rational unitary U in EXACT_PRODUCT_COUNTEREXAMPLE.json satisfy

    tr[W(sigma_i tensor sigma_j)] >= 0 for all225 product vertices,
    tr[W (Phi_9/5 tensor Phi_9/5)(U|20><20|U*)]
       = -206278465199/53256381503809 < 0.

U is an explicitly acquired rational complex Householder unitary, with U|20> equal to the recorded rational unit vector. All225 witness inequalities, unitarity and the negative value are replayed exactly. This is a fixed-frame obstruction, not a separability or classical-simulation obstruction.

## 5. Acquired repaired frame and open channel neighbourhood

A separating-witness search proposed two additional rational pure qutrit states. Appending them gives P17. For the same U followed by Phi_9/5 on both sites, all289 product vertices have acquired nonnegative rational expansions over P17 tensor P17, with columns summing exactly to one. The full4.1MB kernel is saved. Exact matrix intertwining, rather than a trajectory grid, proves composition on overlapping/reversed gate placements, arbitrary width/depth, and causal scheduling, from initial product-frame mixtures. Arbitrary local filters followed by the same noise also close, since P15 is a subset. Final local measurements use their Born probabilities on the stored physical states.

The floating LP was used only to propose weights. Each column reserved a positive multiple of I/9. Rounding weights down to a binary grid produces an exact rational residual; a fixed81-element product basis corrects it. The reserve supplies positive weights on all225 original product vertices, so the correction leaves all weights nonnegative. Exact arithmetic then checks every column against the physical nine-by-nine output matrix, and its normalization. Minimum reserved I/9 weight is0.08291160370771067; the largest coordinate residual before exact correction was4.02e-14.

There is a nonempty physical-channel neighbourhood. The minimum kernel weight on the fixed81 spanning products is

    mu=312488322534019272594095249676274297 /
       848010042353008854646811647764804403200 > 1/3000.

Each local dual-basis observable has operator norm at most the golden ratio<2 (the three diagonal duals are rank-two star matrices; the other six have norm1). Product duals therefore have norm<4. A trace-preserving two-qutrit channel Lambda whose diamond distance from the acquired map is at most1/12000 changes every basis coefficient on a normalized input by at most4/12000<mu. Correct the kernel through those81 products. All weights remain nonnegative; trace preservation retains column sums. This is uniform over supplied channels in that ball. Their actual channel data is still needed to compute transitions; no physical calibration is claimed.
