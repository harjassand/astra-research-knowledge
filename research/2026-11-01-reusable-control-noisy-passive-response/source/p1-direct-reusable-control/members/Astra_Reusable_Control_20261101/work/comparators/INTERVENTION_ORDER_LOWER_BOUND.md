# Simultaneous-intervention lower bound and conventional comparison

1 November 2026. Complementary derivation for the root investigation. All prior Astra source claims below refer only to revision `51ce47ce39f976517d60e2f87bbe280b651f6056` of `harjassand/astra-research-knowledge`.

## 1. Contract and notation

We observe scalar values of

    F(u)=g^T P(I+PBP)^(-1)Pg,
    P=diag(sqrt(u)), B>=0,
    |g_i|<=G, B_ii<=kappa,
    u>=0, sum_i u_i<=delta.

Assume delta,kappa,G>0 and write q=delta*kappa and L=delta*G^2. Here L is a global scale, not the actual input energy at a selected command. The experiment order is the support size of the complete actual command. A dense background plus one changed knob counts as dense.

The source representation and accepted determinant theorem are inherited from N1152. Its governing note is `research/2026-10-29-control-acquisition-and-matrix-formulas/source/p1-dark/selection/inference_determinant_tail_theorem.md`. The earlier path construction is `research/2026-10-29-control-acquisition-and-matrix-formulas/source/imports/DARK_INTERVENTION_ORDER.md` (Sections 2--4). That source was retrieved and read in full; its exact text is preserved alongside this note.

## 2. Main lower bound using the inherited path construction

For each integer n>=2 choose g=G(e_1+e_n), B_+=kappa*I+(kappa/4)*A_path, and flip the last offdiagonal edge sign to obtain B_-. Both are strictly positive definite with lower bound kappa/2. All proper-support responses agree at every nonnegative amplitude: the induced forest has at most one bright endpoint in each component, so a diagonal sign gauge can match B_+ to B_- while fixing g.

At u=(delta/n)1, let t=delta/n and a=kappa/4. Their shared determinant D_n obeys

    D_0=1, D_1=1+kappa*t,
    D_j=(1+kappa*t)D_(j-1)-(a*t)^2 D_(j-2).

The inherited cofactor identity gives the exact gap

    Delta_n=4 G^2 a^(n-1) t^n / D_n.

Because tr(t B)=q and B>=0, D_n<=exp(q). Therefore

    Delta_n >= (4L/n) exp(-q) [q/(4n)]^(n-1).       (P)

This quantified-in-n corollary is the useful addition here. The path construction and exact determinant/cofactor gap themselves are already Astra ingredients, and should not be claimed as newly invented.

Any algorithm, even adaptive and allowed arbitrarily many exact readings, whose complete commands all have support <=n-1 has identical transcripts under these two sources. A common uniform predictor cannot have worst-case absolute error below Delta_n/2 for both. Randomization does not fix this: if its success requirement exceeds 1/2 on each source, the two disjoint success events cannot both have that probability under one common output law. Bounded adversarial noise does not weaken this obstruction because identical noiseless readings remain an allowed transcript.

The same source already provides a decision consumer. The menu contains zero and the displayed full command, with intervention cost equal to the midpoint of their response improvements. They require opposite choices. Every deterministic lower-order controller has regret Delta_n/2 on one source; a randomized controller has worst-case expected regret at least Delta_n/4. This is a two-action decision result, not yet a lower bound on unconstrained continuous optimization with arbitrary prices.

## 3. Asymptotically necessary support order

Let s=log(L/epsilon) and hold q,L>0 fixed. If a method works uniformly over every control dimension and every source in the contract, with uniform absolute error <=epsilon and success probability >1/2, its maximal allowed support k must satisfy

    k >= (1-o(1)) s/log(s), as epsilon/L ->0.        (A)

Proof: apply (P) with n=k+1. Its negative log relative to L is

    log(L/Delta_n)
       <= q + log(n/4) + (n-1)log(4n/q)
        = n log n + O_q(n).

If k <=(1-c)s/log s for any fixed c>0 along a subsequence, then log(L/Delta_(k+1)) <=(1-c+o(1))s, so Delta_(k+1)>2epsilon eventually, contradicting the indistinguishability result. This proves (A).

The fixed-q factorial upper tail has the same order in k. If the root finite-noise construction really acquires its approximation at k=O_q(s/log s), then it is order-optimal in simultaneous active controls. This says nothing comparable about total experiments, bit complexity, conditioning, or physical work. At fixed finite n, the conclusion saturates at n; the asymptotic dimension-uniform claim uses dimensions that grow with required accuracy.

## 4. Alternative single-bright-endpoint cycle witness

This independently constructed witness makes all but one actuator exactly dark. For n>=3, let B_+=kappa I+(kappa/2)A_cycle and let B_- flip one cycle edge. Both are PSD: for any real x, each edge cross term is bounded below by -kappa(x_i^2+x_j^2)/2, and each vertex has degree two. Take g=Ge_1.

For every proper support, the induced graph is a forest. A componentwise diagonal sign gauge fixing vertex 1 (if present) matches the two matrices and leaves g unchanged. Thus every proper-support experiment agrees exactly, at every dose.

At u=t1, t=delta/n, let a=kappa/2 and M_s=I+tB_s. The principal cofactor C=det(M_s without row/column 1) is independent of the signing and satisfies C>=1. All determinant expansion terms involving an edge an even number of times are sign invariant. The only sign-sensitive permutations are the two oriented full cycles. Therefore

    D_+-D_-=4(-1)^(n-1)(at)^n,
    F_s=G^2 t C/D_s,
    |F_+-F_-|=4G^2 t C(at)^n/(D_+D_-)
              >=(4L/n)exp(-2q)[q/(2n)]^n.          (C)

For n=3, kappa=G=1, this is the root's explicit pair-blind fixture:

    B_s = [[1,1/2,1/2],[1/2,1,s/2],[1/2,s/2,1]],
    g=(1,0,0),
    F_-(t1)=t(2+t)/(2+3t),
    F_+(t1)=t(2+3t)/(2+5t+2t^2),
    F_--F_+=2t^4/[(2+3t)(2+5t+2t^2)].

The sign placement in the general cycle and in this triangle is related by a gauge fixing vertex 1, so the same scalar gap applies. The leading gap is t^4/2. The earlier incorrect informal alternate factorization was corrected before this note.

The cycle gives the same asymptotic support-order lower bound as the stronger inherited path. Its useful distinction is one bright actuator rather than two. It is not needed to manufacture a new lower bound where the pinned corpus already supplies one.

## 5. Comparison with full Gram identification

The legal observable is one scalar response under positive diagonal interventions. It does not directly supply B, its entries, g, vector actions, or arbitrary quadratic-form probes. Full Gram identification with a calibrated freely configurable vector shunt is a stronger interface; Astra U1050 explicitly prices that alternative. Pair-scalar acquisition is exactly nonidentifying on these dark examples, even at unlimited precision. Generic bright-coupling reconstruction can be cheaper under its nonzero/conditioning promises, but these promises exclude the displayed examples or become singular near them.

This does not imply that global response learning is always cheaper than model identification. A small known state model or a well-conditioned bright source can favor direct parametric identification. A method given the same warranted positive-source class may use the inherited determinant representation and any new finite-noise bridge; it should be credited as adopting the Astra ingredient. No exclusive physical or computational superiority follows merely from naming the acquired object a response law.

## 6. Preserved quantum alternative finding

Before this branch was redirected, selective quantum reading found that generic no-reset or correlated-bath statements would not by themselves be a major advance. N951 already has physical fresh-Pauli shared-bath subset bounds under local support and integrated norm/key-isolation hypotheses. N517 supplies correlated global-cylinder encoded memory/CNOT/transfer, while charging scratch resets and supplied protected resources. N1023 has accepted complete coarse-memory role-sealed service equivalence, but explicitly leaves trusted framing/terminal operations and hardware acquisition open. Established primary comparator: Ng and Preskill, *Fault-tolerant quantum computation versus Gaussian noise*, Phys. Rev. A 79, 032318 (2009), https://arxiv.org/abs/0810.4953. A more recent obstruction is Burgelman et al., *Limitations to Dynamical Error Suppression and Gate-Error Virtualization from Temporally Correlated Nonclassical Noise*, PRX Quantum 6, 010323 (2025), https://arxiv.org/abs/2407.04766. These were examined as alternatives, not premises of the response theorem.
