# Independent audit: filtered-subspace parent consumer

2026-11-01. **PASS-CONDITIONAL for the exact parent construction, its weak-interaction representation, polynomial finite-system implementation and logical parallel-transport estimate**, with the graph and size conventions clarified below. The gap theorem, uniform relative Gram estimate and ensemble sampler remain separate inputs. No numerical fixture is treated as a theorem.

Audited file: `filtered_parent_consumer.md`, SHA256 `1d3b1ac59e14881f9d2051d3588afa3ec3f514f70cc79936582042f8cfaf65a4`.

## 1. Exact algebra and uniform signed sectors

A(s) is invertible in each finite system. Therefore the simultaneous kernel of L_a=AQ_aA^-1 is exactly A ran(P), and F=sum L_a†L_a has exactly that kernel and is positive. No postselection probability occurs. At V=0, [Href,Q_a]=0 yields L_a=Q_a and F0=sum Q_a, whose nonzero eigenvalues are positive integers; redundant commuting projectors do not invalidate the gap >=1.

A valid syndrome representative is a physical Pauli tensor product, and the bath-label change is an onsite unitary. These conjugate all signed F0 parents to a common unsigned code-plus-product parent without enlarging supports or changing norms. A stability theorem uniform over arbitrary weak perturbations in the proved interaction norm therefore applies to all labels with the same constants. This is conditional on that theorem's actual hypotheses, not a derivation of them.

## 2. Imaginary-time connected interaction bound

Because reference terms commute, only those touching the original support of a local operator enter its reference conjugation; terms outside commute with both that operator and the retained reference terms. The stated one-star support and exp(C beta |support|) norm bound are valid, including arbitrary bounded-dimensional onsite baths.

The interaction-picture differential equation and nested commutator expansion are correct. At order k, only sequences cumulatively connected to the root survive. The number/norm sum of choices is bounded by a product of affine-in-step support sizes. The simplex factorial cancels its factorial growth, leaving a polynomial(k) times a fixed constant to the k. Final reference conjugation contributes another exp(C beta k), absorbed into q. Choosing V sufficiently small at fixed beta gives a convergent exponentially support-weighted interaction decomposition.

Re-rooting must be done on the actual bounded-degree enlarged interaction graph. Additional graph-counting exponentials, if used in a conservative re-rooting bound, should be absorbed into the constant defining q before imposing smallness; they need not literally be polynomial factors. This does not change the existence of a fixed sufficiently small perturbation region. Derivatives with respect to s add fixed polynomial factors in cluster size and are controlled by the exponential slack.

Products in F share the parent root, so their union is rooted-connected with additive size. Expansion of F-F0 and the convolution of the convergent tails give weak interaction norm O(q), whereas its global norm may be O(Nq). Here and below **N counts ALL accessible memory and bath spins/terms**. An arbitrarily larger bath cannot silently be counted as n memory spins.

## 3. Linked-set computation: essential graph convention

The exact inclusion-exclusion construction is valid if a linked support C means **C together with the root Q_a is connected**. C by itself need not be connected: two perturbation branches can meet different parts of the same multi-site Q_a and produce a nonzero mixed nested commutator. Omitting such root-connected branching sets would give a wrong operator. Include Q_a as a fixed root vertex in the enlarged event graph (and use generous reference-star adjacency); then the number of size-k sets remains exp(O(k)).

For each subset T of C, exact conjugation with only perturbations in T can be calculated on the union of Q_a, those perturbation supports and all reference terms touching them. All other reference terms commute with this entire restricted Hamiltonian and Q_a and cancel. That union contains O(|C|+1) spins; it is not a full spatial ball of radius |C|. Inclusion-exclusion isolates histories using every label in C, including all repetitions and time orderings. Coefficients disconnected from the root vanish.

The norm of each linked coefficient is bounded by the sum of its absolute nested-commutator histories. Thus omitted sets of cardinality >K are bounded by the already controlled order->K tail. At fixed local dimension, matrices on O(K) spins, subset enumeration and local exponential calculations cost exp(O(K)) up to precision factors. Local Hamiltonian norms are O(K), so inverse/exponential conditioning costs exp(O(beta K)), not exp(O(N)). This permits polynomially many precision bits at K=O(log(N/eta)).

Truncate every L_a with a total error budget that controls F globally; the uniform bound on ||L_a|| and O(N) roots makes this straightforward. Expand pairwise products explicitly. Each pair occupies O(K) spins and there are polynomially many pairs. The result is a polynomial-size list of explicit Hermitian O(log(N/eta))-spin terms for F, not a dense matrix on a log^3(N) spatial collar and not an oracle for a conditional quantum channel.

## 4. Conditional adiabatic implementation

Given an actual exact-path gap >=1/poly(N), fixed logical band dimension, and the derived polynomial derivative bounds, a finite-time degenerate adiabatic evolution produces the parallel-transport isometry to controlled polynomial-time error. F's exact logical energies are zero, hence there is no logical dynamical phase in the exact path. A globally uniform Hamiltonian approximation error eta contributes at most runtime*eta by Duhamel's bound, including any artificial logical splitting introduced by truncation.

An explicit polynomial list of logarithmically supported matrices can be decomposed/simulated with polynomial gate count and numerical precision. This is a charged active quantum algorithm with access to the relevant bath spins and the supplied encoded input. It is not a passive physical relaxation theorem, constant-depth local circuit, fault-tolerant endpoint theorem or an inaccessible-bath preparation method. All controls, clean states, routing and simulation errors must remain in the resource contract.

The gap theorem is a genuine separate gate: finite-parent numerics and exact preservation of kernel dimension do not imply its gap hypothesis.

## 5. Exact holonomy estimate

Let G=A_P†A_P>0 on the fixed d_L-dimensional input space. Because H is fixed along the scalar-s path,

    A_P†A_P'=G'/2,
    G'=-A_P† H A_P.

Consequently K=W†W' is anti-Hermitian and has the displayed formula in the candidate. The following explicit divided-difference calculation proves the asserted smallness without assuming a small derivative of the relative Gram error.

At a given s choose an eigenbasis G=diag(lambda_i). The Frechet derivative of x^(-1/2) gives

    (G^(-1/2)')_ij
       = -G'_ij/[sqrt(lambda_i) sqrt(lambda_j)
                         (sqrt(lambda_i)+sqrt(lambda_j))].

Thus

    K_ij = G'_ij (sqrt(lambda_j)-sqrt(lambda_i)) /
           [2 sqrt(lambda_i) sqrt(lambda_j)
                         (sqrt(lambda_i)+sqrt(lambda_j))],
    K_ii=0.

If G=g(I+E) and ||E||<=delta<1/2, all lambda_i lie in g[1-delta,1+delta]. For fixed d_L=2 this directly gives ||K||<=C delta ||G'||/g. Moreover, using A_P=W G^(1/2),

    G'=-G^(1/2) W†H W G^(1/2),
    ||G'||/g <=(1+delta)||H||.

Hence ||K||<=C delta||H||, with no bound on E' required. If delta is uniform in s, then integral_0^beta||K||<=C beta delta||H||. The parallel-transport isometry is W(s)U(s), where U'=-K U and U(0)=I; unitarity gives ||U(beta)-I||<=integral||K|| without an exponential Gronwall penalty. The induced channel trace-norm error, with arbitrary reference, is at most twice this isometry-norm error.

At exactly scalar G the connection vanishes identically. Thus there is no hidden unknown logical Berry rotation along this FIXED-H inverse-temperature path. A varying-H filter path would not satisfy the key Hermiticity identity in general.

The norm ||H|| is O(N), not uniformly O(n_memory) for an arbitrarily large bath. The consumer therefore incurs a polynomial-total-system-size factor. Any memory-size-only or infinite-bath transport assertion would require an additional refined estimate and is not earned here.

## 6. Ensemble-to-storage interface remains distinct

The algorithm described prepares, for each sampled label a, W_a rho_LR W_a†, approximately and with the above logical alignment. Sampling labels produces the corresponding filtered-subspace encoding. This is not automatically the earlier fixed-decoder equilibrium-overwrite encoding merely from relative Gram scalarity. The parent must supply a separate reference-safe comparison or storage-admission argument for that ensemble, in addition to the correct classical weights. The thermal agent's separate Gram/ensemble calculation may supply it; it is not proved by the parent-consumer algebra alone.

For orientation, scalar/near-scalar Grams do give useful domination of the averaged filtered output by a constant times actual Gibbs when weights are chosen as Tr(G_a)/Z. But this alone does not establish correct initial recovery by the old decoder for arbitrary logical input. That logical interface cannot be inferred from the maximally mixed input or from matching the equilibrium density matrix only.

## Decision boundary

With the rooted-connected convention, total-system size N, and independently earned gap/Gram/weight/interface inputs, the concrete consumer is valid and avoids normalization postselection and ordered-history factorial costs. No fatal obstruction was found to this conditional preparation algorithm. The stated missing inputs are not certified by this receipt. No external source or numerical fixture was used as a substitute for these direct algebraic checks.

Parent subsequently reports a separate thermal-agent ensemble comparison and actual-host/gap receipts. This consumer receipt does not re-audit those other gates; its Section 6 correctly identifies their required role rather than asserting they remain unproved by the team. The root-connected-set correction and N-size convention remain part of this receipt.
