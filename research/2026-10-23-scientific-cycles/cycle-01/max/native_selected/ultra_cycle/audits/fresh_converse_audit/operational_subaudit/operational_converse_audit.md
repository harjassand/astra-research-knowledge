# Operational formation converse: independent audit

Date: 2026-10-21. All logarithms, entropies, and formation rates below use natural units. This is a conditional mathematical audit of the stated output witness and extraction assumptions, not an external correctness or novelty certification.

## Verdict

The supplied pure-state coefficient-entropy witness gives the requested operational entanglement-cost lower bound without any additivity assumption for entanglement of formation. The infinite-dimensional memory does not enter an entropy-continuity argument: compose formation with extraction and discard the memory first, leaving finite output ports.

A stronger stopping-projector converse also checks. Under the exact-first-output assumption it gives, for every fixed integer N >= 1,

    E_C^nat(tau) >= (ln D) sum_{i=1}^N p_i
                    - ln[1+(N-1)(1-D^{-1})]

                 >= (ln D)[N-delta N(N-1)/2]
                    - ln[1+(N-1)(1-D^{-1})].

This second proof uses a single explicitly separable input comparator, classical variational relative entropy, and joint prefix bounds. It needs neither E_F additivity nor E_F continuity. Its comparator may have arbitrary correlations among the t copies.

## Setup and operational quantifiers

Let D >= 2, m = ln D, and let tau be a normal bipartite state. Let Lambda_N be N uses of the fixed normal LOCC extraction block, with the memory discarded at the end. Its output is a state rho_N on A_N tensor B_N, where dim A_N = dim B_N = D^N. The output registers are ordered pairs 1,...,N. Define

    P_0 = I,
    P_i = Phi_D^{tensor i} tensor I_(pairs i+1,...,N),
    p_i = Tr(P_i rho_N),       1 <= i <= N.

Here Phi_D denotes the rank-one maximally entangled projector, not a dimension-D identity. The supplied real-prefix estimate is

    p_i >= 1-(i-1)delta.

In particular p_1=1. The audit assumes these are probabilities of the actual nested prefix projectors, not merely marginal success probabilities for pair i. This distinction is essential for the stronger stopping proof. If only marginal bounds have been established, the coefficient-witness route remains conditional on its stated effects, while the stopping proof needs a separate prefix estimate.

For a formation protocol at length t, write M_t for its initial maximally entangled Schmidt rank, Gamma_t for its complete LOCC map, and

    tau_hat_t = Gamma_t(Phi_{M_t}),
    epsilon_t = (1/2)||tau_hat_t-tau^{tensor t}||_1 -> 0.

Only local ancillary resources and shared classical randomness are free; no extra shared entanglement is supplied. Define

    Omega_t = Lambda_N^{tensor t} composed with Gamma_t,
    sigma_t = Omega_t(Phi_{M_t}),
    rho_t = rho_N^{tensor t}.

Trace-distance contraction gives (1/2)||sigma_t-rho_t||_1 <= epsilon_t. For fixed N, both sigma_t and rho_t are finite-dimensional states with each local output dimension d_t = D^{Nt}, even though Gamma_t and Lambda_N have infinite-dimensional intermediate memories. The converse below holds for every formation sequence, and therefore for the infimum defining operational E_C. In fact it bounds liminf_t (ln M_t)/t, which also bounds the usual achievable limsup rate.

## Original coefficient-witness route

Fix the admissible b and suppose the parent's global pure-output witness holds for every pure state psi on all t output blocks, including vectors entangled across different copies. Write

    a_b = A_b/(b ln D),        a_b >= 0.

In consistent notation that witness is

    S(psi_A) >= m[tN-a_b sum_{a=1}^t sum_{i=1}^N
                            (1-<psi|P_i^(a)|psi>)
                        -a_b t(b-1)].

It is not sufficient to know this only for vectors that factor across a. Convex-roof decompositions of rho_N^{tensor t} need not factor.

For any pure-state decomposition rho_t = sum_j q_j psi_j, linearity gives

    sum_j q_j <psi_j|P_i^(a)|psi_j> = p_i.

Averaging the witness and taking the convex-roof infimum yields

    E_F(rho_t) >= tm[N-a_b sum_i(1-p_i)-a_b(b-1)]
                >= tm[N-a_b delta N(N-1)/2-a_b(b-1)].       (1)

Finite output dimension permits finite minimizing ensembles; alternatively the affine witness can be integrated against any probability-measure ensemble directly. No E_F(tau^{tensor t}) term occurs, and no regularization identity or additivity statement is used.

### Pure branches and discarded local systems

For completeness, E_F(sigma_t) <= ln M_t has a finite-channel proof that avoids pointwise assertions about continuum transcripts. Omega_t is a channel from finite M_t-by-M_t inputs to finite d_t-by-d_t outputs. Form its normalized Choi state by applying Omega_t to the input halves of locally prepared maximally entangled pairs:

    J(Omega_t) = (Omega_t tensor id_refs)
        (Phi_{M_t}^{Ain,Aref} tensor Phi_{M_t}^{Bin,Bref}).

The displayed input is product across Alice versus Bob, although it is entangled within each laboratory. Complete LOCC preserves separability with the local references retained. Hence J(Omega_t) is separable across (Aout,Aref):(Bout,Bref). As all four Choi registers are finite, it has a finite pure-product decomposition. Vectorizing those pure product vectors gives a finite product-Kraus representation

    Omega_t(X) = sum_l (A_l tensor B_l) X (A_l tensor B_l)^*.

This representation is a mathematical representation of the finite composite channel; it need not be a physical refinement of the original protocol transcript. Each nonzero vector (A_l tensor B_l)|Phi_{M_t}> has Schmidt rank at most M_t, since it is a sum of M_t product vectors. Consequently sigma_t has a finite pure-state decomposition with every term's entanglement at most ln M_t, proving

    E_F(sigma_t) <= ln M_t.                                  (2)

All local discarded systems and all measurable classical outcomes have already been absorbed into Omega_t. Thus no unbounded Kraus density for a general infinite-dimensional instrument is being assumed. Equivalently one can refine local discarded environments mathematically: applying local bras to a rank-M vector leaves at most M product summands. Finite-dimensional Schmidt-number sets are closed, so mixtures and operational limits preserve the same rank bound.

### Explicit finite-output continuity

For states rho,sigma on d-by-d outputs at half-trace distance at most epsilon, put

    eta = sqrt(epsilon(2-epsilon)),
    g(eta) = (1+eta)ln(1+eta)-eta ln eta,

with the continuous endpoint convention. Then

    E_F(rho) <= E_F(sigma)+eta ln d+g(eta).                   (3)

The complete proof is in continuity_note.md in this directory. Its steps are finite: choose a finite optimal ensemble of sigma (at most d^4+1 pure states suffice by compactness and Caratheodory); purify that ensemble on a padded finite ancilla; choose a nearby purification of rho by Uhlmann; measure the same rank-one ancilla basis. The resulting cq states have conditional entropies equal to the sigma ensemble cost and an upper bound on E_F(rho), and half-trace distance at most eta. For cq states, 0 <= H(A|X) <= ln d. The Jordan positive and negative parts remain cq, and the binary mixture inequality gives the explicit continuity term eta ln d+g(eta).

Apply (3) with d=d_t and eta_t=sqrt(epsilon_t(2-epsilon_t)). From (1) and (2),

    (ln M_t)/t >= m[N-a_b delta N(N-1)/2-a_b(b-1)]
                   -Nm eta_t-g(eta_t)/t.

At fixed N and b, eta_t -> 0, so every vanishing-global-error formation sequence obeys

    E_C^nat(tau) >= m[N-a_b delta N(N-1)/2-a_b(b-1)].        (4)

This proves the requested operational implication. No rate of error convergence is required. N and b must be held fixed when t tends to infinity; they may be optimized afterwards. If the right-hand side is negative, the separate nonnegativity bound is stronger.

## Stronger stopping-projector proof

Define the projective stopping measurement on one N-pair output by

    F_k = P_k-P_{k+1},       0 <= k < N,
    F_N = P_N.

The P_k are nested orthogonal projectors, so the F_k form a complete projective measurement. Let pi(k)=Tr(F_k rho_N), and let K have law pi. Then

    pi(0)=1-p_1=0,
    E_pi K = sum_{i=1}^N p_i.

On rho_t the joint measurement law is pi^{tensor t}. The stopping measurement is used only as a mathematical relative-entropy test; no LOCC implementation of a Bell projection is assumed or charged as a free operation.

### Arbitrarily correlated separable comparators

For any separable state zeta on the whole t-copy bipartition and any subset S of copies with thresholds i_a in {1,...,N},

    Pr_zeta(K_a >= i_a for all a in S)
        = Tr[zeta product_{a in S} P_{i_a}^{(a)}]
        <= D^{-sum_{a in S} i_a}.                           (5)

Indeed the selected prefixes form one maximally entangled projector of Schmidt rank D^{sum i_a}, tensored with identity on the remaining pairs. On a product density alpha_A tensor beta_B its expectation is

    D^{-sum i_a} Tr(alpha_selected^T beta_selected)
       <= D^{-sum i_a}.

Convexity and finite-dimensional closure extend this to all separable states. The comparator need not factor between copies. In particular, for the joint cell probability q(k_1,...,k_t), F_{k_a} <= P_{k_a} gives

    q(k_1,...,k_t) <= D^{-sum_a k_a}.                       (6)

### One explicit formation-input comparator

Use

    omega_M = M^{-1} sum_{j=1}^M |jj><jj|,
    D(Phi_M || omega_M) = ln M.

This is a separable input state. The finite output zeta_t=Omega_t(omega_{M_t}) is separable, even when there were arbitrary correlations or infinite memories inside the protocol. Applying quantum and classical relative-entropy data processing to Omega_t and the stopping measurement gives

    ln M_t >= D(sigma_t || zeta_t)
             >= D(pi_t_tilde || q_t).                      (7)

Here pi_t_tilde is the stopping law of sigma_t, q_t that of zeta_t, and TV(pi_t_tilde,pi^{tensor t}) <= epsilon_t. This direct comparator proof needs no separate theorem identifying entanglement cost with a regularized entanglement measure.

### Entropy-loss version

Equation (6) gives

    D(pi_t_tilde||q_t)
       >= m E_(pi_t_tilde) sum_a K_a-H(pi_t_tilde).

The expectation differs from the target by at most tN epsilon_t. For all sufficiently large t, the finite-alphabet entropy bound gives

    H(pi_t_tilde)
       <= tH(pi)+epsilon_t t ln(N+1)+h_2(epsilon_t).

Therefore, after division by t and passage to the limit,

    E_C^nat(tau) >= m sum_i p_i-H(pi)
                 >= m sum_i p_i-ln(N+1).                   (8)

The h_2 term uses natural logarithms. This version already avoids E_F completely.

### Improved partition factor

Fix L >= 0 and set

    g_L(0)=exp(-L),
    g_L(k)=D^k,             1 <= k <= N.

All increments Delta g_L(i)=g_L(i)-g_L(i-1) are nonnegative. Expand the product using

    g_L(K)=g_L(0)+sum_{i=1}^N Delta g_L(i) 1_{K>=i}.

Use (5) term by term. For every globally separable comparator law q_t,

    E_(q_t) product_{a=1}^t g_L(K_a) <= Z_L^t,

where

    Z_L = g_L(0)+sum_{i=1}^N Delta g_L(i)D^{-i}
        = 1+(N-1+exp(-L))(1-D^{-1}).                        (9)

The product bound follows from the nonnegative multivariate tail expansion, not from an independence assumption on q_t.

For a strictly positive f on a finite alphabet,

    D(p||q) >= E_p ln f-ln E_q f.

To verify it, normalize q_f=q f/E_q f and use D(p||q_f)>=0; the same statement holds with infinite relative entropy. Apply it with f=product_a g_L(K_a), combine (7) and (9), and use pi(0)=0:

    E_(pi^{tensor t}) sum_a ln g_L(K_a)
          = tm E_pi K = tm sum_i p_i.

The function sum_a ln g_L(K_a) has range contained in [-tL,tmN]. Its expectation under pi_t_tilde loses at most t(mN+L)epsilon_t. Thus

    (ln M_t)/t >= m sum_i p_i-ln Z_L-(mN+L)epsilon_t.       (10)

First let t tend to infinity at fixed N and L, then let L tend to infinity. Equations (9)-(10) prove

    E_C^nat(tau) >= m sum_i p_i
                    -ln[1+(N-1)(1-D^{-1})].               (11)

The exact-first-output condition is material here: if pi(0)>0, the target expectation contains an additional -L pi(0) term, and L cannot simply be sent to infinity. The present setup has pi(0)=0 exactly.

Substituting the supplied prefix estimate gives the verdict's stronger finite-N bound. One can replace 1-(i-1)delta by its positive part inside the sum for an additional elementary improvement. N=1 yields E_C^nat(tau)>=ln D, as it should. For delta=0, sending N to infinity excludes finite operational formation cost.

## Boundary conditions retained

- The formation error is global half-trace distance to tau^{tensor t}. Per-copy marginal error alone does not give the trace-distance contraction used above.
- The formation resource is a maximally entangled state of rank M_t, with no uncharged shared entanglement. If a different resource is allowed, its separable-comparator divergence or entanglement budget must be charged explicitly.
- Normality is used for well-defined trace-class channel action and contractivity. Normality alone does not define LOCC: an arbitrary normal global channel can create entanglement. The protocol must be built from local operations and classical communication, or be an operational limit of such protocols preserving separability on every fixed finite set of output ports and local references.
- For finite-round normal LOCC with measurable outcomes, product inputs remain barycenters of product conditional outputs. Compactness of finite-dimensional separable sets handles continuum outcomes. Almost-surely terminating protocols and trace-norm limits on finite ports obey the same property. No conditioning on a probability-zero infinite transcript is used.
- Infinite intermediate local dimensions and locally discarded systems do not change (2), (7), or (11). Every entropy and every relative entropy in the displayed proof is evaluated on finite input or finite output states.
- The pure coefficient witness and the real-prefix recurrence estimate are upstream mathematical premises. This audit verifies the operational implication and the stopping comparison; it does not supply a separate proof of those premises.
- The stronger stopping bound dominates the need for the coarse-grained coefficient witness in this operational converse. The coefficient argument remains valid under its stated global pure-vector hypothesis.

No external sources or empirical checks were needed: these are finite-dimensional channel, convexity, and measurement calculations after the extraction channel is composed with formation.
