# Independent review: Choi spectral bound for quantum transmission codes

Reviewer: `recurrent_bath_rank`. Date: 21 October 2026.

## Verdict

**The finite-block inequality is correct, including for arbitrary CPTP encoders.** No reduction to an isometric coding convention is needed. The bound uses the largest eigenvalue of the standard normalized maximally-entangled Choi state, not a Choi state weighted by a biased input reference.

For a channel M from dimension D to dimension D, a code of dimension K, a CPTP encoder E, and a CPTP decoder R, let f be entanglement fidelity, namely the overlap of the decoded normalized Choi state with the normalized maximally entangled state. Then

    f <= min{1, lambda_max(Gamma_M) (D/K)^2}.                 (1)

If a sequence of square n-use block channels has input/output dimension D_n=d^n and standard normalized Choi states satisfying

    lambda_max(Gamma_n) <= C exp(-c n),                      (2)

then every sequence of ordinary unassisted quantum transmission codes with entanglement fidelity tending to one has asymptotic rate at most

    ln d - c/2                                               (3)

in nats per channel use. Rates strictly above this threshold have entanglement fidelity tending to zero exponentially. The result is a min-entropy bound with a complete finite-block proof; it is not inferred from von Neumann entropy alone.

## Definitions and normalization

Let A and B both have dimension D, and let L and L' both have dimension K. Fix orthonormal bases and define

    |Phi_D> = D^(-1/2) sum_(a=1)^D |a>_A |a>_(A'),
    Gamma_M = (M tensor identity_(A'))(|Phi_D><Phi_D|).

Thus Gamma_M is a density operator of trace one. The encoder and decoder are arbitrary CPTP maps

    E : B(L) -> B(A),
    R : B(B) -> B(L).

Write

    J_enc = (M E tensor identity_(L'))(|Phi_K><Phi_K|),
    f = <Phi_K|(R tensor identity_(L'))(J_enc)|Phi_K>.

Here f is the usual entanglement fidelity, or squared Uhlmann fidelity against the pure target. If an unsquared fidelity convention is used, (1) bounds its square.

## Direct index check for arbitrary encoders

Take any Kraus representation

    E(X) = sum_j A_j X A_j*,
    A_j : C^K -> C^D,
    sum_j A_j* A_j = I_K.

Define a completely positive map L_E from D-dimensional matrices to K-dimensional matrices by

    L_E(X) = sum_j A_j^T X overline(A_j).

The right factor is the adjoint of A_j^T, so L_E is CP. Its unitality follows from encoder trace preservation:

    L_E(I_D)
      = sum_j A_j^T overline(A_j)
      = [sum_j A_j* A_j]^T
      = I_K.                                                (4)

The index identity that determines the transpose and conjugation is

    [A_j^T |a><b| overline(A_j)]_(u,v)
       = (A_j)_(a,u) overline((A_j)_(b,v)).                  (5)

Expanding Gamma_M as

    Gamma_M = (1/D) sum_(a,b) M(|a><b|) tensor |a><b|

and using (5) gives exactly

    J_enc = (D/K) (identity_B tensor L_E)(Gamma_M).            (6)

In particular, the formula uses A_j^T on the left and overline(A_j) on the right. The corresponding isometric-encoder formula is the special case of one Kraus operator.

Let lambda=lambda_max(Gamma_M). Since Gamma_M<=lambda I_(B A'), complete positivity and (4) yield

    J_enc <= (D/K) lambda I_(B L').                          (7)

Define the positive decoder test

    T = (R* tensor identity_(L'))(|Phi_K><Phi_K|).

The adjoint R* is unital, because R is trace preserving. Therefore

    Tr T
      = Tr R*[Tr_(L') |Phi_K><Phi_K|]
      = Tr R*(I_K/K)
      = D/K.                                                (8)

Duality, positivity, (7), and (8) now give

    f = Tr(J_enc T)
      <= (D/K) lambda Tr T
      = lambda (D/K)^2.

This proves (1) for arbitrary CPTP encoders and decoders. No assumption about encoder environment dimension or isometric encoding was used.

## Independent CP-order proof

Let Delta_D be the completely depolarizing channel,

    Delta_D(X)=Tr(X) I_D/D.

Its standard normalized Choi state is I_(D^2)/D^2. Consequently

    Gamma_M <= lambda I_(D^2)

is equivalent, by the finite-dimensional Choi criterion, to

    M <=_CP (D^2 lambda) Delta_D,                            (9)

where <=_CP means that the difference of the right side and left side is a completely positive map. Composing (9) with the encoder and decoder preserves this order. Since both are trace preserving,

    R Delta_D E(X) = Tr(X) omega,
    omega = R(I_D/D),
    Tr omega=1.

This replacement channel has normalized Choi state omega tensor I_K/K. Its overlap with |Phi_K> is

    <Phi_K|omega tensor I_K/K|Phi_K> = 1/K^2.

Taking the same positive Choi overlap after (9) gives

    f <= (D^2 lambda)/K^2,

independently verifying every normalization factor in the first proof.

## Asymptotic rate and error boundary

For block length n, put R_n=(ln K_n)/n. Combining (1) and (2),

    f_n <= min{1, C exp[-n(c-2 ln d+2R_n)]}.                 (10)

If f_n tends to one, then ln f_n/n tends to zero. Taking logarithms before a limit gives

    R_n <= ln d-c/2 + (ln C-ln f_n)/(2n).

Hence limsup_n R_n<=ln d-c/2 for any such reliable sequence. In fact a nonvanishing fidelity lower bound is enough for the same rate constraint. If R_n>=ln d-c/2+alpha eventually for any alpha>0, then

    f_n <= C exp(-2alpha n).                                (11)

The decoded Choi state's half trace distance from the pure ideal state is at least 1-f_n, by measuring the ideal-state projector. Thus (11) also forces this half trace distance to one. Its full trace distance tends to two.

No independence between channel uses is required for the finite-block argument. The maps M_n can be correlated memory channels. What is needed is that each code has an ordinary block factorization R_n M_n E_n, with E_n preparing the n input systems and R_n decoding the n outputs. Sequential encoders with private memory and no output feedback admit this representation; sequential decoders can be combined into R_n. Feedback, assistance, or a different communication contract should be defined and analyzed separately rather than silently included in this proof.

Natural logarithms give nats per use. In bits, the threshold is

    log_2 d - c/(2 ln 2).

Because a normalized density operator on dimension d^(2n) has largest eigenvalue at least d^(-2n), an estimate of the form (2) with fixed positive C can only hold asymptotically with c<=2 ln d. The resulting threshold is nonnegative.

## Exact sharpness checks

1. For the completely depolarizing channel, lambda=1/D^2. Every encoder/decoder combination produces a replacement channel, so f=1/K^2 exactly. Equation (1) is equality.

2. For identity transmission with K=D, lambda=1 and perfect encoding/decoding gives f=1. Equation (1) is equality.

3. More substantively, take D=k b and M=identity_k tensor Delta_b. Its normalized Choi state is Phi_k tensor I_(b^2)/b^2, so lambda=1/b^2. Encoding a k-dimensional system in the noiseless factor and decoding that factor gives f=1. Equation (1) gives (1/b^2)(kb/k)^2=1, again exactly. For independent repetitions, c=2 ln b and the rate upper bound is ln(kb)-ln b=ln k, attained by the noiseless subsystem. Thus the coefficient 1/2 in (3) cannot be improved uniformly using only this spectral hypothesis.

These are analytic normalization and sharpness checks, not numerical experiments or external certification.

## Standard versus biased-reference Choi states

The word "Choi" must be accompanied by its normalization and input reference. The proof above specifically requires Gamma_M formed from |Phi_D>. A spectral bound for

    Theta_eta = (M tensor identity)(|psi_eta><psi_eta|)

with a nonuniform faithful input eta cannot be substituted unchanged.

In an eigenbasis of eta,

    Theta_eta = D (I tensor sqrt(eta)) Gamma_M
                         (I tensor sqrt(eta)),

so

    lambda_max(Gamma_M)
       <= lambda_max(Theta_eta)/(D lambda_min(eta)).          (12)

For n inputs with reference eta^(tensor n), this can lose an exponential factor:

    lambda_max(Gamma_n)
       <= lambda_max(Theta_(eta,n))/(d lambda_min(eta))^n.

If the weighted bound has exponent c, this conversion only gives the standard-Choi exponent c+ln(d lambda_min(eta)), which may be nonpositive.

### Explicit failure of an unconverted weighted substitution

Let D=8. Define M to preserve the span of basis vectors 1,...,4 exactly, while replacing input basis vectors 5,...,8 by the output flag |5>. One Kraus representation is

    K_0 = sum_(i=1)^4 |i><i|,
    K_j = |5><j|, j=5,...,8.

Take faithful eta with eigenvalues 1/20 on the first four basis vectors and 1/5 on the last four. Its weighted state Theta_eta is the sum of five mutually orthogonal rank-one terms, each with weight 1/5. Thus lambda_max(Theta_eta)=1/5.

A perfect K=4 code exists in the preserved subspace. Incorrectly inserting the weighted eigenvalue into (1) would give

    1=f <= (1/5)(8/4)^2=4/5,

a contradiction. The standard Choi state instead has largest eigenvalue 1/2, so the actual bound is valid.

For the root investigator's tree-reservoir application, the root explicitly confirmed that its spectral estimate is for Gamma_n produced by independent maximally entangled inputs, while recurrence is separately under a biased faithful eta. Those two roles are distinct and compatible. The weighted-state counterexample is therefore a scope warning, not an identified gap in that application. This review does not independently verify the tree model's spectral estimate.

## Final assessment

The proposed finite-block lemma and its strict nonmaximal-rate consequence are valid under the stated standard-Choi spectral assumption. The general-encoder issue is resolved directly, not deferred to a coding theorem. The tree application's remaining load-bearing obligation is its actual standard-Choi eigenvalue estimate; this review does not certify that estimate or a historical novelty claim.
