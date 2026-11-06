# Continuation: safe classical references, universal collapse of the wrong set divergence, and an extensive symmetrization loss

This is r2's one authorised continuation in the bounded 6 November 2026 Sol pilot. The full common question remains **unresolved**. The initial equivalence and finite-block construction in [CONSTRUCTION.md](CONSTRUCTION.md) are preserved. No computable capacity approximation cutoff or ordinary computable-gap reduction has been constructed.

At the completed-turn boundary the lead supplied [R4_TO_R2_DIVERGENCE_OBJECT.md](../lead/R4_TO_R2_DIVERGENCE_OBJECT.md). I read that exact sparse interface, not r4's developing continuation or another constructor's results. It identifies two invalid substitutions: turning a maximum into a set infimum, and adding a fully quantum untouched reference to an unstabilized divergence. I used those objects to derive the stronger statements below and to test an available November 2026 convergence theorem at its actual hypotheses.

## 1. The infimum substitution has a universal, channel-independent answer

Fix a channel N:A->B, put r=dim A and let R=C^r. Define the two sets

    C_N = {(id_R tensor N)(rho_RA): rho_RA a density matrix},
    B_N = {I_R tensor N(sigma_A): sigma_A a density matrix}.

For any omega in C_N and sigma_B in image(N), the Umegaki convention with an unnormalized second argument gives the exact identity

    D(omega_RB || I_R tensor sigma_B)
       = -H(R|B)_omega + D(omega_B || sigma_B).

For fixed omega, its minimizing sigma_B is omega_B, which is an allowed channel output. Thus the desired one-use quantity is

    max_(omega in C_N) min_(beta in B_N) D(omega||beta) = Q^(1)(N).

The corresponding **infimum over both sets**, however, is exactly

    inf_(omega in C_N,beta in B_N) D(omega||beta) = -log_2 r

for **every** N. The lower bound follows from H(R|B)<=log_2 r and nonnegativity of the remaining relative entropy. Equality is achieved by input pi_R tensor rho_A, giving omega=pi_R tensor N(rho_A), with beta=I_R tensor N(rho_A). This remains valid for rank-deficient outputs by restricting to their common support.

With the normalized comparison pi_R tensor sigma_B, the substituted infimum is zero for every channel. With the generalized natural-log divergence Tr rho(ln rho-ln beta)-Tr rho+Tr beta, the infimum is r-1-ln r, again independent of N.

On n copies, the same answer is -n log_2 r. Its regularization therefore remains the same trivial per-copy constant. This strengthens the transferred identity-channel counterexample: the wrong outer infimum destroys channel dependence throughout the whole channel class, not only on that fixture.

### The natural sets really do have the relevant tensor structure

This is not repaired by proving more regularity of these particular sets. They are compact convex channel images and permutation invariant at block n. Both the sets and their positive polars are closed under tensor products.

For C_N, the support function at X>=0 is

    h_C(X)=lambda_max((id_R tensor N^*)(X)).

For B_N it is

    h_B(X)=lambda_max(N^*(Tr_R X)).

At product tests X tensor Y the adjoint images factorize, and the largest eigenvalue of a tensor product of positive matrices is the product of the largest eigenvalues. Consequently positive-polar membership tensorizes exactly. The same formulas apply to the block image maps.

The assumptions used by the convex-set AEP and efficient relative-entropy approximation theorems therefore do not magically change the outer operation. [Fang–Fawzi–Fawzi, Definition 8, Assumption 9 and Theorem 10](https://arxiv.org/html/2502.15659) concern an infimum over both sets. Applied to these natural sets, they approximate the constant just derived. They do not compute Q.

## 2. A full-rank comparison channel does not fix full stabilization

There is a particularly transparent rational example satisfying the positive-definite comparison-Choi hypothesis of the recent [Xu–Fang theorem, Section 7](https://arxiv.org/html/2611.02425).

Let the physical channel N be the qubit completely depolarizing channel, N(X)=Tr(X)I_2/2. Its ordinary quantum capacity is zero. On input R A with both systems qubits, define actual CPTP maps

    S=id_R tensor N,
    T=R_R^pi tensor N,
    R_R^pi(X)=Tr(X)I_R/2.

The input and output dimensions of both maps are four. In the normalized Choi convention,

    J_T=I_16/16>0,
    det J_T=2^-64.

Thus the comparison channel is not merely supported on a smaller face; it is completely depolarizing and has a known full-rank spectral bound.

For every unreferenced input rho_RA,

    D(S(rho)||T(rho))=1-S(rho_R)<=1.

A pure rho_R attains one bit. Tensoring does not change this rate, so the unstabilized regularized divergence is one bit. Subtracting the normalized-replacer offset log_2 r=1 gives the correct ordinary capacity zero.

Now allow an additional untouched qubit Z and use Phi_ZR tensor |0><0|_A. Then

    (id_Z tensor S)(rho)=Phi_ZR tensor I_B/2,
    (id_Z tensor T)(rho)=I_Z/2 tensor I_R/2 tensor I_B/2,

whose relative entropy is two bits. The general conditional-entropy bound makes two bits the exact fully stabilized maximum. On n copies it is 2n bits. Subtracting the same one-bit offset therefore leaves the erroneous value one, while the physical channel still has Q=0.

Using R_R^I instead of R_R^pi scales the second map by two and subtracts one from either divergence. The unstabilized value is then zero, and the fully stabilized value is one, with no normalization offset remaining.

The November 2 theorem's stabilized divergence is therefore a different quantity even when its comparison channel is strictly positive with an explicit rational lower bound. Making that denominator full rank or paying for its spectral bound does not repair the reference substitution. No contradiction with its stated result follows; it correctly evaluates a different divergence.

## 3. A safe stabilization exists, but its chain rule is insufficient

The transferred failure suggested preserving only a *classical* untouched label. This gives an exact reformulation, rather than an approximation.

For CP maps S,T and an additional classical register X, write rho_XK as the direct sum of p_x rho_x. The same-input relative entropy satisfies

    D((id_X tensor S)(rho) || (id_X tensor T)(rho))
       = sum_x p_x D(S(rho_x)||T(rho_x)).

Taking the supremum cannot improve the unstabilized divergence; one label attains the reverse inequality. Hence classical stabilization equals the unstabilized divergence, at every finite block length and after regularization. For S=id_R tensor N and T=R_R^I tensor N, it retains precisely Q^(1)(N) at one block and Q(N) after regularization.

This does not make the ordinary capacity computable. The crucial amortization operation also remains too small. For two input states rho,sigma on R A, let rho_RB and sigma_B denote their actual channel outputs. Then

    D(S(rho)||T(sigma))-D(rho||sigma)
      = -H(R|B)_rho
        +D(rho_B||sigma_B)-D(rho||sigma)
      <= -H(R|B)_rho <= Q^(1)(N).

The first inequality is ordinary data processing. Taking rho=sigma at an optimizing input gives equality. Thus this amortized, unstabilized value is exactly Q^(1)(N). This collapse is also stated in [Zhu–Mao–Fang–Wang, Theorem 2](https://www.kunfang.info/pdfs/ZMFW25-arXiv.pdf).

Classical labels do not change that conclusion even when the two inputs have different classical weights. For rho_XK=direct_sum p_x rho_x and sigma_XK=direct_sum q_x sigma_x, the classical relative entropy D(p||q) occurs in both the input and output and cancels. The net gain is the p-weighted average of the unreferenced gains above.

The equality between amortized and regularized fully stabilized channel relative entropy consequently cannot be retained while replacing quantum references by classical labels. Were that equality valid for this restricted pair, it would force Q(N)=Q^(1)(N) for every channel. Established coherent-information nonadditivity rules this out. This is a failure of that exact attempted adaptation, not a no-go result for all upper-approximation algorithms.

The useful representation left after this repair is therefore:

    ordinary Q = regularized, classically stabilized divergence of this pair;
    its classical-reference amortized one-use quantity = Q^(1).

The remaining many-use supremum has not been removed.

## 4. Permutation averaging can lose a linear amount of coherent information

I also tested a second ingredient of the stabilized-divergence approximation proof: reducing the input optimization by averaging a marginal over permutations. The stabilized divergence has a concavity property used in that argument. Ordinary coherent information does not share it. The distinction can have extensive size even at fixed physical channel dimensions.

Take the qubit erasure channel with erasure probability p=3/4. Let n be even, and start with the pure product input consisting of n/2 zeros followed by n/2 ones. Its coherent information is zero. Every permuted input is still pure and has coherent information zero.

Average these inputs over all permutations, obtaining rho_type, the uniform classical distribution over binary strings of Hamming weight n/2. Let H_k be the entropy of any k-bit marginal. Since the central binomial probability is at least 1/(n+1),

    rho_type <= (n+1) I/2^n.

Partial trace and nonnegativity of relative entropy to the uniform distribution give

    k-log_2(n+1) <= H_k <= k.

In the erasure dilation, both parties retain the actual orthogonal erasure mask. Its classical entropy cancels in coherent information. If Bob retains K qubits, the two quantum entropies are H_K and H_(n-K), respectively. Therefore

    I_c(rho_type,E_(2,p)^n)
       = E[H_K-H_(n-K)],       K~Binomial(n,1-p),

and

    (1-2p)n-log_2(n+1)
      <= I_c(rho_type,E_(2,p)^n)
      <= (1-2p)n+log_2(n+1).

At p=3/4 this is -n/2+O(log n), compared with zero before averaging. The loss is linear. A claim that this averaging changes coherent information by only O(log n) is false.

For an explicit finite calculation at n=32, the upper bound is

    -16+log_2(33)<-10 bits.

The independently executed compressed calculation gives the certified rational interval

    -15.537374709200437 <= I_c <= -15.537374709200434 bits.

The exact rational endpoints are in [divergence_checks.json](divergence_checks.json). The code does not build a 2^32-dimensional density matrix. For a particular k-bit string of weight j, its probability is exactly

    binom(n-k,n/2-j)/binom(n,n/2),

and there are binom(k,j) such strings. This gives H_k as a finite rational-probability entropy sum. Outward rational logarithm bounds use binary range reduction followed by the atanh series with ratio at most 1/3. All entropy and binomial averages are then exact interval arithmetic.

This example excludes the naive averaging step and a sublinear-loss claim for that step. It does not exclude a different symmetric optimization: a concave envelope could retain an ensemble of asymmetric inputs, and an optimizing channel input may happen to be symmetric. Evaluating that envelope or its exponentially large ensemble is an additional operation, not supplied by averaging the original state.

## 5. What this does and does not supply for the full question

The two exact transfer counterexamples were used to eliminate attractive but invalid upper-bound substitutions. Their strengthened forms now cover all channels for the outer-infimum substitution and an explicitly full-rank comparison channel for stabilization. A classical-reference repair preserves the right quantity but does not inherit the needed amortization identity. The extensive symmetrization example identifies another failed step with an analytic bound and a certified, inexpensive calculation.

I investigated whether the new regularized-divergence convergence theorem supplies the missing dimension-only cutoff from the initial construction. Its reference convention and its quantum-reference amortization step are essential; on the exact full-rank test above, its output remains the wrong constant for ordinary Q. The safe classical restriction leaves the original regularization unresolved. Convex-set AEP applied to the natural image sets computes an infimum with no remaining channel dependence. No adaptation with the required error guarantee was constructed.

The noncomputability direction still lacks a finite rational ordinary channel with a positive rate bounded below by computable instance data in the halting case. None of these divergence deductions removes N1680's signed extensive history correction or supplies an exactly returned mixed catalyst with that yield. I have no argument excluding every such construction. The accepted N675, N1677, N1680 and N684 scopes remain as before.

Thus the initial exact equivalence still describes the unresolved operation: construct an independent computable approximation cutoff F(a,b,epsilon), or prove that no total evaluator exists by a genuine ordinary-capacity gap reduction. Neither is completed in this continuation.

## 6. Execution and resource accounting

New files are [divergence_interface.py](divergence_interface.py), [divergence_checks.json](divergence_checks.json) and this continuation. Initial scientific originals and all shared/predecessor files remain unchanged.

`python3 divergence_interface.py` passed. It checks the exact full-rank normalized Choi matrix and determinant, trace preservation, the one-bit unstabilized and two-bit stabilized normalized-replacer fixtures, the -1-bit set-infimum fixture, a classical-label fixture, the 32-use compressed rational entropy interval, and the p=1/2 symmetry control. Its final measured script runtime was approximately 0.31 seconds. This is mathematical execution, not a physical experiment or a capacity evaluation for arbitrary inputs.

Source acquisition used six ordinary web tool requests, containing five search queries and direct original-source reads/finds. The newly encountered November 2 preprint was read at its actual stabilized/full-rank scope. One public-source find timed out after its page had already been read; it supplies no missing premise. No held transfer was retried, no package was installed, and no external paid/API service, outreach, physical experiment, shared-source write, memory write, goal, automation or descendant agent was used.

The transferred r4 object is material peer exposure and is identified above. Other constructors' developing results were not accessed. These new restricted deductions do not convert the bounded pilot's scientific resource stop into a resolution of the full question.
