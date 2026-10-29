# Fixed-accuracy extension from graph degree to local interaction strength
2026-10-29. Root construction, independent receiving pending. Sampling and matrix concentration are established mechanisms; no novelty claim for the sparsifier.

## Input and target
Let H=sum_e h_e be an explicitly given k-local qubit Hamiltonian. Remove scalar terms separately. Suppose rational envelopes alpha_e>=||h_e|| are supplied or computed from the fixed-size local matrices, and
 g_v=sum_{e containing v} alpha_e<=g
for a fixed g. At fixed local matrix dimension d=2^k, the explicit choice alpha_e=sum_ij(|Re h_e,ij|+|Im h_e,ij|) is rational, computable in polynomial input-bit time, and satisfies ||h_e||<=alpha_e<=2d^2||h_e||. Thus a bounded actual local-norm sum supplies a bounded computable envelope sum up to a fixed factor; no separate norm oracle is required. There is NO bound on how many weak terms touch a site. Put L=sum alpha_e<=ng; zero-envelope terms are zero and discarded. For fixed rational eps in(0,1], we construct a bounded-degree Hamiltonian Htilde satisfying ||Htilde-H||<=eps*n/2 with probability >.97. This only preserves density-scale energies/free energies; it does not preserve spectral gaps, ground spaces, dynamics, or global Gibbs states.

If L<=eps*n/4, return the ZERO HAMILTONIAN as the approximation. Its free-energy density is -ln2/beta, not zero; its ground-energy density is zero. The known scalar shift is restored in both cases.

## Sampling
Otherwise a=eps*n/4<L. Draw q=ceil(512 L^2/(eps^2 n)) independent indices with probabilities p_e=alpha_e/L, and set
 Hhat=(L/q) sum_{j=1}^q h_(e_j)/alpha_(e_j).
For Y=h_e/p_e, E Y=H, ||Y-H||<=2L and E(Y-H)^2=E Y^2-H^2<=L^2 I. Applying the two-sided matrix Bernstein bound in dimension2^n yields
 Pr(||Hhat-H||>a)<=2^(n+1) exp[-q a^2/(2L^2+(4/3)La)]
 <=2^(n+1) exp(-9.6n)<.00028.
Here a<L, q>=512 L^2/(eps^2 n), and 512/(16*(10/3))=9.6. This is an operator-norm guarantee for all states, not only a sampled expectation value.

## Trim unusually high sampled degrees
Let X_v count sampled terms incident to v. It is binomial with mean mu_v=q g_v/L. Since L>eps*n/4 and L<=ng,
 mu_v<=Lambda:=512g^2/eps^2+4g/eps.
Choose an integer D with D>=9Lambda and D>=ln(200g/eps). One fully rational rule is
 D=ceil(9Lambda)+ceil(log2(max(2,200g/eps))),
where the second ceiling uses integer comparisons on a positive rational, not an exact logarithm oracle.

Delete every sampled term touching any vertex with X_v>D. Remaining incidence is at mostD. Every retained term has norm at most L/q<=eps/128, so local norm is also bounded independently of n.

For X~Bin(q,p), the exact identity
 E[X 1{X>D}]=qp Pr(Bin(q-1,p)>=D)
combined with the binomial Chernoff bound gives
 E[X_v 1{X_v>D}]<=mu_v (eLambda/D)^D<=mu_v e^(-D),
because D>=9Lambda>e^2 Lambda. A deleted term may be counted several times; that only increases the following upper bound. Thus
 E||Hhat-Htilde|| <=(L/q)sum_v E[X_v1{X_v>D}]
 <=sum_v g_v e^(-D)<=ng e^(-D)<=eps*n/200.
Markov gives Pr(||Hhat-Htilde||>eps*n/4)<=.02. The combined success probability is >.9797; the looser stated >.97 allows further bounded random-bit failures. The actual deletion bound (L/q) times the number of deleted samples is computable from the sample, although the original operator-norm sampling error is not claimed efficiently observable.

## Resources and thermal transfer
q=O(n g^2/eps^2), and D is independent of n at fixed eps,g. Original terms have fixed support sizek. Sampling probabilities are exact rationals. Integer-prefix sampling uses expected polynomial random-bit work; alternatively cap each draw's rejection attempts and charge the union failure probability. Input reading, rational arithmetic, all sampled indices and repetitions are charged. No exponential-dimensional matrix is formed by the preprocessing algorithm; dense matrices are used only in small diagnostics.

Apply the received bounded-degree thermal/counting construction to Htilde with its remaining error budget. Operator-norm perturbation changes ground/free-energy density by at most eps/2. Therefore, conditional on the imported counting theorem, bounded-local-strength k-local Hamiltonians admit RANDOMIZED subexponential-volume fixed-density-accuracy evaluation and the corresponding approximate low-energy witness, with constant success probability. The witness's error against original H pays the norm perturbation twice, so allocate a smaller sparsification budget for that claim.

The logarithmically vanishing-accuracy theorem does NOT transfer automatically: D grows with1/eps and the local-cone constant can then destroy the subexponential bound. The deterministic bounded-degree theorem and this randomized local-strength extension remain separate.

## Established alternatives and boundaries
Matrix concentration: Tropp, User-Friendly Tail Bounds for Sums of Random Matrices (FOCM2012; arXiv1004.4389), applied to centered Hermitian sums. Existing Hamiltonian term sampling and degree control must be compared with Anshu–Nirkhe2025 AppendixC LemmaC.4; broad PSD multiplicative sparsification with Basu–Brakensiek–Putterman arXiv2605.02211. Aharonov–Zhou2019 gap-simulation impossibility is not contradicted by this extensive additive-norm approximation. Product-state/mean-field algorithms already handle important high-degree/dense subclasses more efficiently. No claim of practical superiority or a new general sparsification principle is made.
