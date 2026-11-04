# Acquiring a positive latent-Ising sampler from raw ternary tensors

Date: 2026-11-04. Status: a complete scoped mathematical compiler assembled from established CP reconstruction and Ising algorithms. Exact finite acquisition audits pass. An independent adversarial proof audit found the scoped construction justified subject to three accounting clarifications, incorporated below. A general algebraic-number implementation, production sampler, novelty, and practical comparative advantage remain unestablished. This is a proof document, not a claim of a new tractability class.

## 1. Contract and consequence

Input: a finite simple cubic graph G=(V,E), not necessarily planar, and eight rational entries for each real tensor T_v on its three incident edge bits. No CP factors, local basis, hidden spins, graph embedding, or contraction value is supplied. Let n=|V|, m=|E|, and L be the maximum bit length of a raw rational coefficient.

Admitted recognition domain: each local 2x2x2 hyperdeterminant is nonzero. The compiler recognizes precisely the subclass described below, and otherwise returns NOT IN THIS CLASS or UNKNOWN outside the admitted domain. Neither output is a hardness assertion.

Accepted subclass:
1. Every T_v has a strictly positive real rank-two CP decomposition with nonsingular leg matrices and positive mixture coefficients.
2. After permissible hidden-state label swaps, the induced edge interactions are ferromagnetic.
3. After symmetrizing those interactions, all hidden fields on each connected component favor one common spin (zero fields allowed).

Output on acceptance: an acquired latent representation, an FPRAS for the original partition function, and an algorithm returning a sample within prescribed total-variation error epsilon of the original edge-bit distribution. Acquisition and arithmetic precision are charged. No exact #P contraction is asserted.

The useful operation is automatic discovery of a usable generative representation, beyond N1077's exact planar zero-field receiver. This does NOT define a new Ising tractability class. Its potential consequence depends on acquiring this structure in non-generated scientific inputs, which has not been demonstrated.

## 2. Exact local positive-CP acquisition

Use the nonsingular pencil construction in the saved N1077 proof. For slices T_0,T_1 choose t in {0,1,-1} with A=T_0+t T_1 invertible. Diagonalize M=T_1 A^-1. The two distinct eigenvalues lie in a quadratic extension; if they are not real, reject this positive-real class. With eigenvectors U and V^T=U^-1 A, the three CP factors are
F_0=[[1-t mu_0,1-t mu_1],[mu_0,mu_1]], F_1=U, F_2=V.

For each leg i and column s, divide the column by the sum of its two coordinates, provided that sum is nonzero. Denote the resulting column-stochastic matrix by B_(v,i), and multiply the three removed column sums to obtain c_(v,s). Test that every B entry and both c entries are strictly positive. Verify all eight tensor reconstruction identities:
T_v(x_1,x_2,x_3)=sum_(s=0,1) c_(v,s) product_i B_(v,i)(x_i,s).

Why this is complete at the local admitted scope: simple-spectrum rank-two CP decompositions with invertible legs are unique up to column scaling and a simultaneous interchange of their two terms. Column normalization removes the scaling freedom. Thus a failed strict-positivity test cannot be repaired by another rank-two CP factorization. Degenerate, non-strict, higher-rank, or entirely different latent representations are not classified.

No global number field is formed. Each local calculation has bounded algebraic degree and polynomial coefficient height. Standard exact real-algebraic arithmetic and sign isolation therefore give polynomial bit cost per vertex. The prototype audits below do not implement the full general real-algebraic backend.

## 3. Acquire the global ferromagnetic labels

For e=uv set W_e=B_(u,e)^T B_(v,e). All four entries are positive and det W_e is nonzero. Swapping the hidden labels at vertex v reverses the determinant sign of every incident edge. Solve the binary constraints
sigma_u XOR sigma_v = 1[det W_e<0]
by graph traversal. An inconsistent cycle certifies that no labeling in this positive-CP representation class makes every edge ferromagnetic. In a connected component all successful labelings differ only by a global spin flip. Apply the chosen label swaps to B and c.

This costs O(n+m) exact local sign tests and Boolean operations, not an exponential gauge search.

## 4. Acquire the hidden fields and exact prefactor

For each oriented edge e=uv write W=[[W00,W01],[W10,W11]], and take the positive roots
r_(u,e)=sqrt(W10 W11/(W00 W01)),
r_(v,e)=W11/(W00 r_(u,e)).
Then
D_(u,e) W D_(v,e)=[[a_e,b_e],[b_e,a_e]],
where D_(v,e)=diag(r_(v,e),1), a_e=W11, and b_e=r_(u,e) W01.
Positive determinant gives beta_e=a_e/b_e>1.

Let g_v=product_(e incident v) r_(v,e). Compensation of the column scalings changes the vertex weights to d_(v,0)=c_(v,0)/g_v and d_(v,1)=c_(v,1). Therefore
lambda_v=c_(v,1) g_v/c_(v,0),
C=(product_e b_e)(product_v c_(v,0)/g_v),
and exactly
Z_original=C sum_s product_e beta_e^[s_u=s_v] product_v lambda_v^[s_v=1].

Accept the component iff its lambda_v are all >=1 or all <=1. A global spin flip turns the former into the latter. In the transformed partition-function convention this adds product_v lambda_v to the prefactor. For posterior sampling, simply map sampled spins back through the recorded global and vertex label flips.

Completeness within the declared class follows from local CP uniqueness, completeness of signed-graph balancing, uniqueness of positive edge symmetrization up to harmless common edge scalars, and the fact that only a global label flip remains. The compiler is not complete for all holographic reductions, graph gadgets, or general tractable tensor networks.

Each edge quantity depends on at most two local quadratic fields; each vertex field on a constant-size degree-three neighborhood and three square roots. Their algebraic degrees and expression sizes are bounded by constants independent of n. Exact comparisons to 1 remain polynomial-bit local operations. The product C may have exponentially large algebraic degree if expanded; DO NOT construct its global minimal polynomial. Its positive factors can instead be multiplied with controlled relative numerical error.

## 5. Lift samples back to the original variables

Define the positive joint weight
q(x,s)=product_v c_(v,s_v) product_(v,e incident v) B_(v,e)(x_e,s_v).
Summing over s gives the original tensor-network weight. Summing over x gives the unsymmetrized hidden Ising weight product_v c_(v,s_v) product_e W_e(s_u,s_v).

Consequently, after obtaining a hidden-spin sample in the recorded labels, independently draw each original edge bit according to
Pr[x_e=b | s_u,s_v] = B_(u,e)(b,s_u) B_(v,e)(b,s_v) / W_e(s_u,s_v).
These are genuine nonnegative normalized probabilities. This is not the invalid operation of interpreting an arbitrary holographic gauge as a stochastic channel. Strict positive CP factors are essential here.

A delta-TV hidden sampler followed by this exact stochastic kernel has at most delta TV error in the original variables. Approximating each of the m binary kernels to TV error eta adds at most m eta by coupling. Bounded observables can then be estimated additively. No multiplicative guarantee for rare original events is inferred.

## 6. A necessary bit-complexity repair: truncate couplings, not precision costs

The published Swendsen-Wang bounds contain a factor depending on beta_max and 1/(beta_min-1). Polynomial input bit length does not itself make that factor polynomial. The following constructive preprocessing closes that loophole for approximate sampling and counting.

### Strong-edge lemma
For any ferromagnetic Ising model with all 0<lambda_v<=1,
Pr[s_u!=s_v] <= 1/(beta_e+1).
Proof: expand every edge except e into its equality/random-cluster term. If u,v lie in one resulting cluster, disagreement is impossible. Otherwise let a,b in (0,1] be products of vertex activities in their two clusters. Conditional on all other clusters, the total weights for equal and different spins are beta_e(1+ab) and a+b. Since a+b<=1+ab, the claimed bound follows. All expansion weights are nonnegative, so mixing over the other edges preserves it.

### Delete weak interactions
Replace edges with 1<beta_e<1+eta by beta_e=1. Every configuration weight changes by a factor between 1 and (1+eta)^m. Partition ratios and normalized distribution ratios are consequently controlled. For example the total-variation change is at most (exp(m eta)-1), a deliberately conservative bound.

### Contract strong interactions
For beta_e>M, require endpoints to agree and contract the connected components of those edges. The probability of violating any required equality is at most m/(M+1), by the strong-edge lemma and union bound. Conditioning changes TV by exactly the excluded-event probability. The conditioned model is obtained by multiplying the fields within each contracted component and collecting all internal-edge beta factors into the known prefactor. Its partition function times that prefactor is between (1-m/(M+1)) Z and Z.

Thus eta=Theta(epsilon/m) and M=Theta(m/epsilon) give O(epsilon) error while leaving external couplings in [1+eta,M]. Field products remain consistent and their rational encodings have only additive bit-length growth.

### Remove parallel-edge technicalities without multiplying huge couplings
Contraction can create parallel edges. Replace each remaining edge of weight beta by a unique two-edge path through an auxiliary spin of field 1, both new weights t=beta+sqrt(beta^2-1). Summing the auxiliary spin gives 2t times the original beta edge interaction. The expanded partition function is the pre-subdivision partition function multiplied by product_e(2t_e). Therefore recovering the pre-subdivision partition function requires DIVISION by product_e(2t_e), not multiplication. The resulting graph is simple, has O(n+m) vertices/edges, and 1+eta<=t<=2M. Original hidden spins are marginals of this enlarged model. This avoids merging many bounded parallel couplings into one exponentially large parameter.

If no interactions remain, sample the independent vertex spins and count product_v(1+lambda_v) directly, including all recorded prefactors. Isolated vertices are likewise handled directly. These reductions preserve the consistent-field contract. They do not work merely from ferromagnetic couplings with arbitrary opposing fields: strongly pinned opposite spins can disagree even across a large coupling.

## 7. Complete approximate sampling and partition algorithm

First round the constant-degree algebraic beta, lambda, local conditional kernels and positive prefactors to rational relative/logarithmic error O(epsilon/(n+m)), preserving beta>=1 and 0<lambda<=1 by directed rounding/clipping. Exact class-membership comparisons precede rounding. Positive local quantities have logarithmic magnitudes and separation bounds polynomial in L, so this takes poly(L,log(n/epsilon)) precision, not an exponentially large field representation. Field products after contraction require O(n) times that bit budget.

Apply the weak/strong preprocessing with its own allocated error budget. Subdivision introduces a second algebraic step: even rational beta generally produces irrational t=beta+sqrt(beta^2-1). Rationalize each such t a second time, to logarithmic error at most epsilon/[100(n+m)] per enlarged-graph interaction (reducing this tolerance further if necessary for the allocated error budget), preserving t>=1+eta/2 by directed rounding. The enlarged graph has O(n+m) interactions, so its total log-weight perturbation is O(epsilon). These square roots have degree two and polynomial height. Approximate the reciprocal subdivision normalizations 1/(2t) separately to the allocated relative precision, using the unrounded t values in the identity; the small difference between the rounded expanded model and that exact identity is covered by the second perturbation budget. Run the published general consistent-field Swendsen-Wang sampler on the bounded-range simple model. Its polynomial-in-size mixing bound now has polynomial parameter factors as well. Each sweep uses polynomially many rational Bernoulli draws and cluster products; exact rational-coin simulation has polynomial expected bit cost. Expand contracted spins, discard auxiliary spins, undo labels, then apply the edge kernels evaluated from certified approximations of the ORIGINAL positive CP factors. Those kernels need not agree exactly with a rational CP decomposition of the rounded backend; their individual approximation error is independently budgeted. Allocate the approximation, truncation, mixing and kernel budgets so their sum is <=epsilon.

This proves polynomial EXPECTED bit complexity in n,L,1/epsilon,log(1/delta) for approximate sampling, using conservative existing mixing bounds. To obtain the usual bounded-time randomized formulation, implement a rational coin a/b by drawing ceil(log2 b) unbiased bits and rejecting integers >=b. Every attempt succeeds with probability greater than 1/2. The deterministic sweep and sampling schedule bounds the number of coin calls by a polynomial Q. Cap each call at ceil(log2(Q/gamma))+1 attempts. The probability of any cap exceedance is at most gamma by a union bound. Return a fixed fallback sample or a flagged counting failure on this event, charging gamma to the total-variation or failure budget. This gives worst-case polynomial bit runtime with the stated approximation guarantees; it does not claim a worst-case bound for an uncapped exact coin. It does not establish near-linear complexity uniformly in arbitrary encoded weights.

For counting, one may invoke the established consistent-field Ising FPRAS, or use the same sampler in a fully explicit annealing reduction: start with no edges and known Z_0=product_v(1+lambda_v); add each bounded edge at its first nontrivial weight min(2,t_final), then strengthen by doubling, capping the last step at t_final. Every ratio is at most 2, and every nontrivial absolute coupling is at least min(2,t_final), so all intermediate models retain the inverse-polynomial margin above 1; absent/unit edges are removed. There are K=O(m log M) stages. Each ratio is an expectation of a variable in [1,2]. Estimate each to relative O(epsilon/K) with fresh approximately independent samples, budget their biases and failure probabilities, and multiply the ratios and all recorded prefactors. Hoeffding gives a polynomial, albeit deliberately unoptimized, total sampling cost. This avoids self-reduction by pinning spins, which could create inconsistent fields. The low/high coupling reductions already bound their partition-function error.

## 8. Exact raw-tensor audits

### A. Heterogeneous rational gauge, nonplanar K3,3
At left vertices build tensors from columns of A=[[3,1],[1,2]]; at right vertices use B=[[11,8],[17,21]], with CP coefficients (1,v+2). Then DISCARD those factors and run the pencil recovery on the raw integer tensors. The audit recovers positive CP factors and fields 2,3,4,5,6,7; all couplings equal 10/9.
The source N1077 intrinsic beta values after absorbing CP coefficients are 4,9,16,25,36,49, not 1. Hence both nonplanarity and nonzero fields genuinely fall outside that original theorem.
Direct enumeration of all 512 original edge states and all 64 hidden states gives Z=29462868436378906250. All nine original edge marginals match the acquired conditional-kernel formula exactly.
Files: audit.py, results.json.

### B. Raw rational input requiring irrational positive factors
Use the symmetric raw signature [40,20,20,90] on every K3,3 vertex. Pencil recovery yields the two positive conjugate directions proportional to (2+sqrt(2),3-sqrt(2)) and (2-sqrt(2),3+sqrt(2)), not a rational hidden gauge. The acquired coupling is sqrt(281)/9 and a field choice is ((17+2sqrt(2))/(17-2sqrt(2)))^(3/2). Exact arithmetic in Q(sqrt(2)) verifies cancellation to rational Z=1093333000000, matching direct raw contraction.
Files: irrational_audit.py, irrational_results.json.

Both are GENERATED finite algebra audits, not independent scientific workloads, practical speed benchmarks, or implemented FPRAS experiments. The scripts recover factors from raw slices, rather than feeding the hidden factors to the recovery step.

## 9. Strongest same-resource comparison and remaining consequence gap

- The expensive computational engine is established ferromagnetic Ising sampling/counting, not new here. An ordinary baseline receiving the same acquired factors can do exactly the same work. Charge the compiler's local exact algebra, sign traversal, numerical precision, and reconstruction overhead.
- Holographic reductions to Ising already underpin approximation algorithms for real Boolean Holant signatures. A 2022 paper explicitly treats generalized second-order recurrence constraints. Our heterogeneous nonsymmetric raw-instance acquisition contract is more explicit than the retrieved abstract, but that difference is NOT proof of novelty.
- Established near-linear samplers apply when the required interaction/field margins are controlled. In the rational K3,3 audit those margins are fixed, so the strongest comparator is not an exponential tensor contraction or the slowest historical Ising chain.
- Current 2026 work also improves counting/sampling for broader ferromagnetic two-spin regimes. Those admitted regions could become further backend choices; this document does not claim our consistent-field test exhausts efficient possibilities.
- Arbitrary mixed fields are #BIS-hard in general. Our test's failure there is a meaningful limitation, not proof of impossibility for each rejected instance.

What is actually gained relative to N1077 is a scoped acquired GENERATIVE operation on nonplanar, nonzero-field raw tensor networks. What is not gained is a new tractability class or a demonstrated computational advantage over an ordinary algorithm allowed the same acquisition. Transformative consequence remains unearned until such structure is acquired from a consequential non-generated model, or the acquisition/computation mechanism is materially extended beyond known tractable backends.

## 10. Robustness: an open accepted class and an honest noisy-input contract

The construction is not confined to the equality variety beta_v=1. At either exact audit example, all local positive-CP entries, coefficients, determinant signs, and oriented fields satisfy strict inequalities. Simple eigenvalues and their normalized factors vary continuously. Therefore sufficiently small raw-entry perturbations preserve acceptance. For a family of fixed-degree graphs using these fixed local templates, a uniform local perturbation radius exists because each field test involves only a bounded-size neighborhood. This proves the existence of an open accepted neighborhood, not a measured margin or a claim that arbitrary models usually belong to it.

Correctness with noisy raw inputs can be separated from conditioning of CP recovery. Suppose the true tensors T_v are strictly positive and a rational estimate T_hat_v satisfies, simultaneously for every entry,
(1-rho_v) T_v(x) <= T_hat_v(x) <= (1+rho_v) T_v(x), with 0<=rho_v<=1/2.
If the compiler accepts T_hat, its sampler targets the approximate network. For every original configuration, the ratio of unnormalized weights lies between product_v(1-rho_v) and product_v(1+rho_v). Hence its logarithmic spread is at most 3 sum_v rho_v, giving a conservative total-variation bound exp(3 sum_v rho_v)-1 and analogous explicit partition bounds. Taking sum_v rho_v=O(epsilon) and allocating the remaining sampler error gives an O(epsilon)-accurate operation for the TRUE network, whether or not that true network was itself certified in the class.

Thus unstable inferred factors cannot silently invalidate the output: acceptance is checked on the actual rational estimate, and raw positive-weight errors are controlled before any gauge change. Ill-conditioning can still reduce the probability of acceptance, increase precision/cost, or produce UNKNOWN. It is not a guarantee of successful recovery near the class boundary.

If entries are acquired by independent repeated scalar measurements with a known variance upper bound sigma^2 and a known positive lower bound tau on all true entries, a standard median-of-means acquisition with absolute error O(tau epsilon/n) costs O(sigma^2 n^3/(tau^2 epsilon^2) log(n/delta)) readings across the 8n entries, up to constants and a minimum sample count. This is a sufficient, deliberately conservative acquisition bound under those explicit measurement assumptions. Very small tau may make acquisition impractical; no such measurement interface or physical workload is claimed here. Merely quoting polynomial symbolic bit complexity does not pay this statistical cost.

### Quantitative implementation detail for Section 7
For 0<epsilon<=1/10, a concrete conservative allocation is initial log-weight error <=epsilon/[100(n+m)] per positive parameter, weak threshold eta=epsilon/(100m), and strong cutoff M=100m/epsilon. Allocate comparable independent budgets to subdivision rounding, chain mixing, and original-edge kernels; constants can be increased so the total TV error is <=epsilon. Directed rounding keeps the final active couplings in [1+eta/2,3M]. Remove exact unit interactions.

Writing N',m'=O(n+m) for the enlarged simple graph, the parameter-dependent factor in the published mixing proof is bounded by O(R log R), where R=beta_max+beta_min/(beta_min-1)=O(m/epsilon). Its conservative SW step bound is therefore
O((m/epsilon) log(m/epsilon) (N')^4 (m')^2 (m'+log(1/zeta)))
for target TV error zeta. This is intentionally not competitive with fixed-margin near-linear backends. Each sweep can be implemented using O(N'+m') cluster/edge operations with rational inputs whose bit lengths are polynomial in n,L,log(1/epsilon),log(1/zeta). Cluster field products have O(n) times the local bit length. Exact rational Bernoulli simulation uses polynomial expected bit work; this statement is expected bit complexity, not a worst-case bound on random bits. The capped rejection implementation above gives a bounded-time alternative, with aggregate cap probability gamma charged explicitly. This cap also applies to original-edge kernel coins.

For the counting reduction, let K=O(m' log M) be the number of ratio stages. Each stage uses O(K^2 epsilon^-2 log(K/delta)) fresh independently randomized chain runs, each targeting TV error O(epsilon/K). The observable lies in [1,2], so its approximation bias and Hoeffding sampling error are both controlled. There are O(K^3 epsilon^-2 log(K/delta)) total runs. Their products estimate the contracted/subdivided model's partition function; divide out subdivision factors and multiply all positive original/gauge/contraction factors with the remaining precision budget. Together with the bounded deletion/conditioning errors this gives the stated FPRAS. Output length and all accumulated exponents are polynomial in n,L.
