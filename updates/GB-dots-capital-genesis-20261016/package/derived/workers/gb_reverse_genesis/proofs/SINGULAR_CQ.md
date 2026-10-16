# A support-exact reconstruction of the CQ reverse-radius theorem

Author: worker gb_reverse_genesis, 16 October 2026. Status: internal proof; no external review, formal verification, or historical priority certification.

This closes an endpoint explicitly omitted by the supplied faithful-output packet. It is also a direct independent reconstruction of a CQ consequence already latent in Astra's broader internal N402 Choi candidate. It is not claimed to be a new theorem in the literature or new to Astra's full archive. The proof below does not assume that broader candidate.

## 1. Exact statement and support convention

Let a classical input i in {1,...,m} prepare a density matrix sigma_i >= 0 on a finite-dimensional output Q. Set

    S = intersection_i range(sigma_i),
    V = span_i range(sigma_i),
    P_S = orthogonal projection onto S,
    G_i = (P_S sigma_i^+ P_S)|_S.

Here + is the Moore-Penrose inverse, and every G_i is positive definite on S when S is nonzero. For p in the FULL simplex Delta_m define

    G_p = sum_i p_i G_i,
    h(p) = Tr_S G_p^-1.

When S={0}, set h(p)=0. Crucially S is the intersection for ALL channel inputs, including inputs with p_i=0. A boundary p is the continuous extension of strictly positive priors with this fixed S. Replacing S by the support intersection of only the positive-prior inputs changes the answer.

For faithful reference blocks R_i>0 summing to I_R and Hermitian H_i, put

    K = sum_i H_i,
    A = sum_i sigma_i tensor R_i,
    J = sum_i sigma_i tensor H_i.

All output inverses are taken on V tensor R; A is strictly positive there. Define the conditional RLD input and output costs by

    E = sum_i Tr H_i R_i^-1 H_i - Tr K^2,
    N = Tr J A^-1 J - Tr K^2.

The unrestricted complete conditional coefficient is the supremum N/E over finite references and E>0. Equivalently one may permit arbitrary positive reference marginal W and subtract Tr K W^-1 K. The usual congruence removes W without enlarging the reference dimension.

Then

    C = min_{U=U*, U=P_S U P_S} max_i
          Tr[(sigma_i-U) sigma_i^+ (sigma_i-U)]
      = 1 - min_{p in Delta_m} h(p).                         (1)

The operator-valued conditional defect has the same sharp constant. Reference dimension at most m-1 suffices in the supremum for the RLD lower construction when the channel is nonconstant. A constant channel has C=0 and reference dimension one suffices.

For reveal-or-erase E_q, q>=C is necessary and sufficient for ordinary, unsmoothed complete SLD / binary quadratic-MMSE dominance. It also suffices for every real-label ensemble with finite second moment. For any q<C there is a strict faithful binary-input-state witness with the same reference marginal and reference dimension at most m. These are sufficient dimensions, not minimality assertions. Singular prepared outputs are allowed; input encodings in the strict witnesses are faithful.

## 2. Upper bound and finite-dimensional minimax

For supported Hermitian U,

    f_i(U) = 1 - 2 Tr U + Tr U G_i U.

These are strictly convex, uniformly coercive quadratics on Herm(S). Convex minimax gives

    min_U max_i f_i(U)
      = max_p min_U [1-2Tr U+Tr U G_p U].

The inner stationarity equation is G_p U+U G_p=2I_S, with unique solution U=G_p^-1. Its value is 1-h(p), proving the equality between the two expressions in (1). If S is zero, U=0 and both expressions give one. The minimizing prior exists because h is continuous on the compact FULL simplex with the fixed S.

For the channel bound set Z_i=H_i-R_i K. Then sum_i Z_i=0 and the physical conditional defect is

    sum_i Z_i* R_i^-1 Z_i

at the input, and

    Tr_Q Z* A^-1 Z,     Z=sum_i sigma_i tensor Z_i

at the output. This is the same exact expansion as in the faithful-output proof. It remains valid on V tensor R because A has that fixed support and J is supported there.

Apply supported matrix weighted Cauchy to

    A_i=sigma_i tensor R_i,
    B_i=(sigma_i-U) tensor Z_i.

Since range(B_i) is contained in range(A_i),

    (sum B_i)* (sum A_i)^+ (sum B_i)
      <= sum B_i* A_i^+ B_i.

Partial trace gives

    Tr_Q Z* A^-1 Z
      <= sum_i f_i(U) Z_i* R_i^-1 Z_i
      <= (max_i f_i(U)) sum_i Z_i* R_i^-1 Z_i.              (2)

Thus (1) is an upper bound in every reference dimension. No inverse of a zero eigenvalue is assigned a finite unsupported cost.

## 3. The exact singular Schur complement

Fix p_i>0 for every i. Let s=(sqrt(p_i)), P=I-ss*, H=s^perp, v_i=P e_i and

    R_i^0=v_i v_i*,     z_i=sqrt(p_i) v_i.

These act on H, of dimension m-1. Sum R_i^0=I_H, sum z_i=0, and the supported inverse input vector energy is one.

Let D=direct_sum_i sigma_i on C^m tensor Q, decomposed as (span(s) tensor Q) direct_sum (H tensor Q):

    D = [[B,W*],[W,A_0]],
    B=sum_i p_i sigma_i,
    A_0=sum_i R_i^0 tensor sigma_i,
    W=sum_i z_i tensor sigma_i.

If x is in ker A_0, then x*D x=0, so D^(1/2)x=0 and W* x=0. Hence range(W) is contained in range(A_0). In particular the generalized Schur complement

    Lambda = B-W* A_0^+ W

is well-defined, positive, and is the quadratic form obtained by minimizing over the lower block.

We now calculate it, without an appeal to continuity or an interchange of limits. For any v in Q,

    v* Lambda v
      = min_{u_i: sum_i sqrt(p_i) u_i=v} sum_i u_i* sigma_i u_i. (3)

For every w in S, completing squares on the individual supported ranges gives

    sum_i u_i* sigma_i u_i
      >= 2 Re w* v - w* G_p w.

The maximum of this lower bound is

    (P_S v)* G_p^-1 (P_S v).

It is attained. Put w=G_p^-1 P_S v. The residual

    r=v-sum_i p_i sigma_i^+ w

has P_S r=0. Since

    S^perp = sum_i ker(sigma_i),

and p_i>0, choose k_i in ker(sigma_i) with sum_i sqrt(p_i) k_i=r. Then

    u_i=sqrt(p_i) sigma_i^+ w+k_i

satisfy the constraint and achieve the lower bound. For S=0, the same argument uses w=0 and represents every v by kernel vectors, giving value zero. Thus exactly

    Lambda=P_S G_p^-1 P_S,
    Tr W* A_0^+ W=1-h(p).                                  (4)

This is the weighted harmonic / parallel-sum support rule. It is established matrix machinery, reconstructed here explicitly because the support condition is the load-bearing endpoint.

## 4. Faithful input regularization, with the range proof paid

Put R_i(epsilon)=(R_i^0+epsilon I)/(1+m epsilon), keeping z_i fixed. The input vector costs converge to one. The output baseline is

    A_epsilon=(A_0+epsilon B_0)/(1+m epsilon),
    B_0=I_H tensor sum_i sigma_i.

B_0 is positive definite on H tensor V. Because range(W) is contained in range(A_0),

    Tr W* A_epsilon^-1 W -> Tr W* A_0^+ W.                 (5)

Here is the precise inverse-limit fact used in (5). For A>=0, B>0 and range(W) contained in range(A), split range(A) direct_sum ker(A). The upper-left inverse block of A+epsilon B is

    [A_11+epsilon(B_11-B_12 B_22^-1 B_21)]^-1,

which converges to A_11^-1. W has zero lower block, so its inverse quadratic cost has the claimed supported limit. There is no assertion that the full inverse converges.

Every positive prior therefore gives lower ratios approaching 1-h(p). Positive priors are dense and h is continuous on the fixed-support simplex, proving vector sharpness of (1).

For the physical Hermitian lower construction choose real, nonconstant h_i and H_i=h_i R_i^0. With K=sum H_i the centered matrices satisfy

    Z_i=H_i-R_i^0 K=z_i w*,
    w*=s* diag(h) P,
    ||w||^2=Var_p(h)>0.

Subtracting alpha=Tr K/(m-1) from every h_i makes Tr K=0 without changing Z_i. The input physical conditional cost is ||w||^2, and the output cost is ||w||^2[1-h(p)] by (4).

Keep these H_i fixed during the baseline regularization. Each H_i is supported in R_i^0. Moreover J=sum_i sigma_i tensor H_i is a real linear combination of the positive summands sigma_i tensor R_i^0, so range(J) is contained in range(A_0). The inverse-limit lemma consequently applies to the physical output cost as well. The reference baseline stays I and K stays fixed. Both physical conditional costs converge, and every strict lower ratio persists at a finite epsilon.

Normalize by m-1 and take a sufficiently small nonzero Hermitian perturbation to obtain faithful normalized input-state pairs. This proves physical sharpness in the same dimension. It also explains why merely regularizing outputs and interchanging a supremum with a limit would have been an incomplete proof.

## 5. SLD / MMSE erasure threshold with singular outputs

When C<1, the normalized density radius is

    K_rad=min_{omega density on S} max_i Tr omega sigma_i^+ omega
         =1/(1-C).

This follows by compact minimax and the fixed-p optimizer omega=G_p^-1/h(p). Thus an optimal omega has

    max_i chi_i <= C/(1-C),
    chi_i=Tr(omega-sigma_i) sigma_i^+ (omega-sigma_i).

The purification variance proof in supplied CQ_OPERATIONAL Section 'Purification proof' works with sqrt(sigma_i) and sigma_i^{+1/2}. All directions omega-sigma_i are supported in sigma_i; the zero-eigenvalue components never enter the calculation. It gives, for every joint Hermitian observable A on Q tensor R,

    [Phi_omega(A)-Phi_sigma_i(A)]^2
      <= chi_i [Phi_sigma_i(A^2)-Phi_sigma_i(A)^2].           (6)

For 0<q<1 and q>=C compile the target A to the erasure-reference observables

    B_0=Phi_omega(A),
    B_i=[Phi_sigma_i(A)-(1-q)B_0]/q.

They preserve the mean and do not increase its second moment, by (6). This proves all the stated quadratic-risk and SLD upper comparisons. At q=1 reveal the input and measure Phi_sigma_i(A); at q=0 only a constant family can be dominated.

For necessity choose a finite faithful vector witness from Section 4 with N>qE. Add one coherent reference flag with baseline blocks diag(delta a_i,R_i), tangent blocks [[0,z_i*],[z_i,0]], a_i>0, sum a_i=1. Their total tangent is zero.

On the effective output support V the target baseline is diag(delta sigma_a,A), where sigma_a=sum_i a_i sigma_i>0 on V. Its SLD offdiagonal solution X_delta obeys

    A X_delta+delta X_delta sigma_a=2B,
    B=sum_i sigma_i tensor z_i.

Since A>0 on V tensor R, X_delta tends to 2A^-1 B and the output SLD cost tends to 4N. The input cost is exactly

    4 sum_i z_i* (R_i+delta a_i I)^-1 z_i -> 4E.

Choose finite positive delta for a strict violation, normalize, then choose a finite t>0 satisfying the input Schur bounds

    t^2 z_i* R_i^-1 z_i < delta a_i.

Both binary input states are faithful, normalized and have the same reference marginal. The exact binary MMSE identity converts the strict SLD failure into an ordinary finite MMSE failure. This proof uses no Hermitian smoothing and does not identify fixed-reference SLD and RLD coefficients.

## 6. Three exact endpoint traps

First, C=1 iff S={0}. If S is nonzero, every G_p is uniformly positive and bounded, so min_p h(p)>0. Thus any two distinct pure states have C=1 even if their trace distance is arbitrarily small. At two identical pure states C=0. The exact complete threshold is discontinuous on this rank-deficient stratum.

Second, replacing inverses by pseudoinverses without the common-range constraint is invalid. For sigma_1=|0><0| and sigma_2=|+><+|, S=0 and C=1. At p=(1/2,1/2), sum p_i sigma_i^+ is their average state and has inverse trace 8. A naive unrestricted pseudoinverse harmonic expression gives 1-8=-7, rather than one.

Third, compressing sigma_i first and then inverting is also invalid. The exact rank-two qutrit fixture in checks/verify_exact.py has S=span(e_1), G_1=8/3, G_2=12/7, and C=5/8. Replacing G_i by (P_S sigma_i P_S)^-1 gives C=1/2. The distinction is the shorted operator, rather than a notational convention.

## 7. Attribution and next useful work

The weighted-harmonic support geometry is old parallel-sum / shorted-operator theory; see Fillmore-Williams, *On operator ranges*, Section 4, pp.276-279, reporting the Anderson-Duffin finite-dimensional result and proving its extension. Quantum left-radius theory and common-support restrictions have existing precedents in Mosonyi-Bunth-Vrana. Signed variance lifts and the MMSE-SLD dictionary are established in Zhu-Wang and Hirche. Exact citations and inspected scope are in ../SOURCES.md.

Astra's prior N402 candidate, original RESULTS Eqs.(3.3)-(3.4), already gives the same common-support density radius upon substituting the CQ Choi matrix direct_sum_i sigma_i. This proof independently establishes the narrow CQ coefficient and operational endpoint without relying on N402's broad entropy claims. The remaining useful frontier is an actual calibrated finite decision payoff at paid preparation/receiver precision, not a claim of maximal practical capability from C=1.
