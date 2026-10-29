# A noise-stable one-use information window and its composition failure

30 October 2026. Root construction; B independently reconstructed the bound and
supplied the decisive parity obstruction below. No new scientific instance or
physical experiment has been executed. Historical priority is unknown; the
matrix conditioning itself is ordinary. This is not a replacement for the
accepted sharp all-input private-support theorem.

## One-use principle

Let tau_1,...,tau_n be density matrices and G_ij=Tr(tau_i tau_j). Let P0 be the
orthogonal projection onto 1-perp in C^n and suppose

    P0 G P0 >= g P0, g>0.

This is affine independence, not private-support separation. Put
k=||sum_i tau_i||op<=n. Consider classical-quantum hypotheses rho_i,sigma_i on
an arbitrary finite reference, with the explicit balance promises

    rho_i>=lambda rho_R, sigma_i>=lambda sigma_R,
    0<lambda<=1/n, rho_R=sum_i rho_i, sigma_R=sum_i sigma_i.

For finite defined conditional divergence differences,

    J_tau >= (lambda g/k) J_X.                         (1)

Faithful full-rank preparations can satisfy affine independence. Unlike the
sharp all-input constant, this restricted-window coefficient survives small
full-rank contamination. The Loewner balance promise is essential and is an
actual restriction on both hypotheses, including their quantum reference.

## Changing-reference proof

On the affine path A_i(t) between the hypotheses let M=sum A_i and H=sum H_i.
For each s in(0,1), on reference Hilbert--Schmidt space define

    Q_i=s L_Ai+(1-s)R_Ai, Z=sum Q_i,
    z=Z^(-1)H, u_i=H_i-Q_i z, sum_i u_i=0.

Balance gives Q_i>=lambda Z. Since also A_i<=M,

    W=s sum_i L_tau_i tensor L_Ai
         +(1-s)sum_i R_tau_i tensor R_Ai
      <=k I_HS tensor Z.

The accepted exact modular gauge from root_cq_retention/PROOF gives

    F_X=sum_i <u_i,Q_i^(-1)u_i>,
    F_tau=<sum_i |tau_i> tensor u_i,
               W^(-1) sum_i |tau_i> tensor u_i>.

Consequently

    F_tau >=(1/k) sum_(i,j)G_ij <u_i,Z^(-1)u_j>
           >=(g/k) sum_i <u_i,Z^(-1)u_i>
           >=(lambda g/k) F_X.

The middle inequality uses sum_i u_i=0 and the Hilbert-space extension of the
Gram inequality; no classical-reference reduction is assumed. Integrate over
s to obtain the BKM comparison, then over the affine hypothesis path with
weight1-t. The balance condition persists on that path. This proves(1), with
common-support limits where needed. No private-support measurement or physical
decoder is assumed.

For rational preparations, H0=P0 G P0+11*/n is rational positive definite.
The rational number gamma=1/[1+Tr(H0^(-1))] is a conservative lower bound for g.
Thus lambda gamma/n is acquired by exact rational linear algebra. This is an
explicit coefficient, not optimality or a laboratory acquisition guarantee.

## Why this does not solve the consequential multi-use question

B supplied a purely classical countermechanism. Let a hidden bit Theta be
uniform. Draw X_1,...,X_(T-1) independent uniform bits and let

    X_T=Theta xor X_1 xor ... xor X_(T-1) xor E,
    E~Bernoulli(lambda), 0<lambda<1/2.

At every ideal prefix the next-label probabilities conditioned on Theta are
between lambda and1-lambda; earlier steps are exactly uniform. The full ideal
transcript has I(Theta;X)=1-h2(lambda). Pass each label independently through
BSC(delta), 0<delta<1/2. Its two classical preparations are faithful and affinely
independent, so the one-use bounded-window coefficient is positive. Nevertheless
the noisy transcript's only Theta-dependent statistic is its parity, whose
bias is

    (1-2lambda)(1-2delta)^T.

Thus I(Theta;Y)=1-h2([1-(1-2lambda)(1-2delta)^T]/2) decays exponentially.
Parity is computable in O(T). Bounded local priors, finite computation and
faithful distinguishability do not yield a horizon-independent retention rule.
This does not contradict(1); its naive sequential promotion fails.

The surviving question is how to acquire NOISE-STABLE useful distinctions and
their explanatory/control structure, with actual data and composition costs.
Ordinary Fourier noise stability, error correction, PGM/Petz recovery and
experiment comparison are the serious incumbents. Merely defining stable tasks,
assuming their tests, or reporting another coefficient leaves the enabling
operation unpaid. B/C continue that question-first attack independently of the
capital-first compiler construction.
