# Efficient universal distillation for a dilute mixed-source family

28 October2026. **New consequence candidate, pending independent review.** Depends on the fixed-defect orbit access theorem and total soft-polar recovery, with their finite encoder/control implementation conditions. It is not a theorem for a fixed positive-noise source, hardware, or practical gate counts.

## Statement

Fix local dimensions a,b>=2, constants c>=0, R>=0, Delta>0 and0<epsilon<1. Consider any unknown iid k-copy source rho_k on A tensor B whose dominant spectral component obeys

    rho_k=(1−delta_k)|psi_k><psi_k|+delta_k tau_k,
    delta_k<=c/k,  tau_k supported orthogonally to psi_k,
    H((psi_k)_B)>=R+Delta.

Neither eigenvector, contamination state nor their support is supplied to the protocol. For sufficiently large k depending only on the displayed parameters, the orbit decoder combined with the universal Schur encoder gives a one-way LOCC protocol outputting floor(kR) ebits with mean infidelity at most epsilon. Its gate/classical cost is polynomial in k for fixed c,epsilon,Delta,a,b. The degree depends on the chosen defect cutoff and can be large. Computation uses known representation circuits, not reconstruction of rho_k or its environment.

This statement assumes standard efficient circuit synthesis and approximate2design implementation with the specified moment norm/precision, as in the separately reviewed encoder-access construction. It is an algorithmic ideal-gate theorem with a paid finite compiler budget, not fault tolerance at a fixed physical gate-noise rate. The supplied impurity/entropy bounds are source promises, not estimates acquired by this theorem.

## Explicit finite parameters

Use the positive soft-polar constant A0=20/9 (or A0=4 with the separately received faster bounded sign filter). Choose a fixed nonnegative integer j such that

    c^(j+1)/(j+1)! <= epsilon/6.                      (1)

For c0 take j0. This choice is finite and independent of k. For k>j let L=(k)_j, use the uniform bounds M0=L³ and alpha0=L², and target K=2^floor(kR).

Set b0=(b−1)(b+2)/2 and

    u_k=sqrt[(2/k) ln(6(k+1)^b0/epsilon)],
    f_b(x)=x log2(b−1)+h2(x).

Take k large enough that c/k<=1/2, u_k<=1, and

    k[Delta−f_b(c/k)−f_b(u_k/2)]−b0 log2(k+b)
         >= 3 log2 L + log2(6A0/epsilon).             (2)

Such k exists: left side is kDelta−o(k), right sideO(jlogk). Alice/Bob use every observed local sector with enough code space and

    D=d_mu >= (6A0/epsilon) K M0.                    (3)

Other outcomes output a fixed failure state. They choose the selected environment set nu_1>=k−j and use the complete orbit frame, including every multiplicity. No equality lambda=mu or rare rectangular-sector postselection is imposed.

## Environmental bad mass

The governing orbit proof shows defect k−nu_1 is stochastically bounded by the number of non-dominant eigen-symbols X~Binomial(k,c/k). For r=j+1,

    Pr[X>=r] <= E C(X,r)
             =C(k,r)(c/k)^r <=c^r/r! <=epsilon/6.

This applies regardless of the rank and eigenvectors of the contamination. Source label probabilities are evaluated on the original quantum state; diagonal eigen-symbols are a proof device, not a measurement the protocol performs.

## Local Schur-dimension tail

Let p be the spectrum of(rho_k)_B and let mu be Bob's actual Schur outcome. Its probability obeys

    Pr(mu)<= (k+1)^[b(b−1)/2] exp[−k D(mu/k||p)].

For completeness, the Schur probability is d_mu s_mu(p); the maximal monomial in the Schur character at sorted p is p^mu, while its number of terms counting multiplicities is at most the unitary-representation dimension(k+1)^[b(b−1)/2]. Combine d_mu<=2^[kH(mu/k)] with that monomial bound. There are at most(k+1)^(b−1) diagrams. Pinsker's inequality therefore gives

    Pr[||mu/k−p||_1>u_k]<=epsilon/6.                 (4)

No iid environmental trajectory premise beyond the stated k-copy source is hidden here.

Marginal trace distance between(rho_k)_B and(psi_k)_B is at mostdelta_k. Entropy continuity gives H(p)>=R+Delta−f_b(c/k) for sufficiently large k (on the monotone range of f_b). On the event complementary to(4), H(mu/k)>=H(p)−f_b(u_k/2). The hook-dimension bound

    log2 d_mu >= kH(mu/k)−b0 log2(k+b)

then proves(3) by(2). Thus insufficient-B-dimension outcomes cost at mostepsilon/6.

On a selected environment component, lambda and mu share some restriction prefix alpha, so d_mu<=L d_alpha<=L d_lambda. Consequently(3) also implies d_lambda>=K. If no selected component exists, its mass is already included in the environmental bad event. One does not silently assume a code fits in every Alice sector.

## Packing, residual blocks and finite implementation

For a complete code block, reference average failure is at mostA0 beta plus the chosen approximation errors. Alice's residual code-block mass q is less thanK/d_lambda. Since beta<=KN/D−K/d_lambda and A0>=1,

    q+A0 beta <=A0 KN/D<=A0 K M0/D<=epsilon/6.        (5)

This is the same weighted complete-block argument used in the universal code: each complete block has fixed weightK/d_lambda and its physical error weights are independent of the random code. Excluded environment labels are orthogonal after tracing the environment, so their bad mass is charged linearly. Arbitrary coherent cross-selected/rejected weights are not treated this way.

Use a bounded-filter approximation parameter epsilon_f<=epsilon/(12alpha0), giving uniform total-filter remainder<=epsilon/6. Choose the code ensemble's diamond second-moment error eta satisfying

    eta [K M0² alpha0^4 +2M0 alpha0²] <=epsilon/(6A0).

Its contribution is at mostepsilon/6 by the governing conservative moment bound. Finally synthesize and execute the complete intended finite circuit within operational discrepancyepsilon/6, charging all local Schur transforms, code circuits, coefficient-space dilations, selector controls, QSVT calls, measurements, routing and classical messages. This is an explicit precision target; it does not assert that an existing noisy device achieves it.

Adding the six allocated losses (environment, local dimension, packing/residual, filter, encoder moments, implementation) proves the claimed infidelityepsilon. Block count does not multiply the mean moment-error allowance: complete-block probabilities sum to at most1. The required code block index is handled by reversible arithmetic on itsO(log d_lambda)-bit label, not by compiling exponentially many dense code matrices.

The logarithm of1/eta isO(k+jlogk+log(1/epsilon)) for fixed dimensions/rate. Standard efficient approximate designs therefore retain polynomial synthesis cost at this precision. Orbit tables have size at mostL³ and the explicit block normalization at mostL²; the faster filter has polynomial query countO(L²log(alpha0/epsilon)), while the conservative positive filter usesO(L^4log(alpha0/epsilon)). Other table/representation costs are polynomial too. No claim of a small polynomial exponent or practical runtime follows.

## Why this is more than replacing the block by a pure state

For orthogonal contamination atdelta_k=c/k, the original block's trace distance from|psi_k><psi_k|^tensor k is1−(1−c/k)^k→1−e^(−c). That loss does not tend to zero. The protocol instead corrects finitely many representation defects and pays the much smaller factorial/binomial tail. The supplied source can have arbitrary unknown contaminating directions and weights.

This remains a changing-source/dilute-noise theorem. For a fixed mixed source with nonzero impurity, the requiredj generally grows withk and this access method no longer gives a uniform polynomial-time implementation. Taking epsilon→0 withk can also growj and the polynomial degree. Comparison with strong conventional near-pure entanglement purification and other universal codes remains required before any priority or practical-advantage claim.
