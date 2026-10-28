# Independent local persistent-excitation statistics and finite-guard derivation

28 October 2026. Mathematical proof/check support for the separately authored acquired-patch-excitation candidate, not yet a receiving receipt. The prior approximate-on-site source and its statistics receipt remain unchanged. No sampled source calls, RNG, hardware execution or production finite eigensolver is claimed.

## 1. One physical bank and its three conditional matrix means

Condition on a coarse history whose learned width-W envelopes contain the fixed true X/Z generators; put d=2^W. In each actual block all q logical inputs receive fresh independent X/Z axes and signs, and all physical outputs receive fresh independent Pauli readout axes. On each acquired envelope let Z be the product local-Pauli shadow. The three actual matrix records are

    Y_0=Z,   Y_j=2*1{selected input axis=j}*s_i*Z, j=X,Z.

All conditional means are given the COMPLETE PRIOR history. Other current labels and outcomes are averaged, not conditioned upon. The means are rho_t and Delta_j,t=B_j R_j,t, with kappa rho_t<=R_j,t<=rho_t and [B_j,R_j,t]=0. Because the two signed estimators share the same fresh sign-averaged input, they share the SAME rho_t. The exact factorization of averages Delta_bar=B Rbar requires a FIXED B; gauge/Pauli weights and retained memory may otherwise drift arbitrarily.

The standard one-copy identity gives E[Z^2|past]=Phi^tensor(W)(rho_t)<=3^W I. Input-axis probability 1/2 gives E[Y_j^2|past]=2 Phi^tensor(W)(rho_t)<=2*3^W I. Each centered increment has norm at most 4d; the conditional centered square is no larger than the uncentered second moment. Hence each of the 3q matrix martingales obeys the two-sided fixed-bank tail

    P(||mean-predictable average||op>a)
      <=2d exp[-N a^2/{2(2*3^W+4da/3)}].             (1)

No same-copy, cross-logical or across-time independence is asserted.

## 2. A fixed finite geometric schedule

Let beta0=beta1=beta/2, and fund a finite integer cap S. For b the largest positive dyadic with b^2<=epsilon/(18Aq), set

    L=ceil log2(6dq(S+1)/beta1),
    a_s=2^(-s)/(16d),
    N_s=ceil(8*3^W*L/a_s^2), s=0,...,S.              (2)

Since a_s<=1/(16d), the denominator in (1) is at most 5*3^W. Union over 3q matrices and S+1 possible reached banks costs at most beta1. Each bank's inequality holds conditional on any previous complete stage history, so early stopping is legal. A union of conditional failure probabilities suffices; one need not assume an optional-stopping iid theorem. Together with the received coarse error beta0, ONE event Good of probability at least 1-beta gives all simultaneous operator confidence bounds for every reached stage.

The ceil in N_s is redundant: every factor in 8*3^W*L*(16d)^2*4^s is an integer. Thus

    sum_(t=0)^s N_t
      =8*3^W*L*(16d)^2*(4^(s+1)-1)/3 <(4/3)N_s.     (3)

This is an explicit fixed worst-case source cap at s=S, not an unbounded search for a possibly absent floor.

## 3. A computable marginal floor and finite raw sign

Apply the received rational-unitary Jacobi primitive to each KNOWN empirical matrix, with Frobenius residual <=a/4. It outputs C=Q D Q†, where Q is exactly rational unitary and D has rational real labels. Matrix norms are bounded on every record: the unsigned average by d and each signed average by 2d. No unknown source eigenvalue or source eigengap enters the solver's precision or scaling.

For the unsigned mean, define l=min diagonal(D_rho)-5a/4. On Good,

    lambda_min(rho_bar)>=l.

If the actual averaged floor is at least r, the generic residual guarantee gives l>=r-5a/2. The slightly sharper r-9a/4 follows if D is used as the exact diagonal of Q†rhohat Q, but is not needed by the candidate's more conservative bound.

For each signed mean define S=Q diag(sign D)Q†, with sign(0)=+1. S is exactly a rational Hermitian involution on every record. The combined empirical and finite-solver error is

    ||C-Delta_bar||op<=e:=5a/4.                       (4)

## 4. Operator sign lemma and both exact rational guards

Suppose Delta=B R, [B,R]=0, R>=gI, and ||C-Delta||<=e<g. If P is Delta's positive spectral projector and Q_+ is C's positive spectral projector (zero assigned positive), then the cross-overlap P(I-Q_+) solves a Sylvester equation. The true positive generator is >=g and the negative estimated generator is <=-(g-e). Its semigroup integral therefore has norm <=e/(2g-e). The opposite overlap has the same bound. Since ||P-Q_+|| equals the maximum of the two cross-overlap norms,

    ||sign(C)-B||op<=2e/(2g-e)<=2e/g.                 (5)

This argument is insensitive to repeated eigenvalues within either sign sector and can be proved directly from the convergent integral, without an inaccessible eigenbasis algorithm.

The MARGINAL guard is

    l>0,   5a<=2b kappa l.                            (6)

On Good it implies g>=kappa l and e/g<=b/2, hence (5) gives sign error <=b.

A stronger conventional guard uses the observed signed gap h=min|D_kk|. If h>e, Weyl's inequality gives a true gap at least h-e; positivity of R then implies sign(Delta_bar)=B even when no positive lower marginal bound was otherwise used. Combining true gap h-e with estimated gap h in the SAME Sylvester proof gives

    ||sign(C)-B||op<=2e/(2h-e).

Therefore the DIRECT SIGNED-GAP guard is exactly

    h>5a/4,   10a<=b(8h-5a).                         (7)

Every generator may qualify by (6) OR (7). The union rule uses the same three-matrix confidence event and costs no extra probability or calls. A zero signed sector cannot pass (7) on Good. Both routes yield operator-norm, not training-state-weighted, approximation to the fixed true generators.

## 5. Automatic completion, without a conditioning shortcut

At a reached stage suppose its ACTUAL predictable averaged marginals have minimum eigenvalues at least r. If a_s<=b kappa r/5, then l>=r-5a_s/2>=r/2 and (6) holds. Alternatively, if every actual signed contrast has absolute spectral gap at least gamma and a_s<=b gamma/5, then e<=b gamma/4, h>=gamma-e and

    2e/(2h-e)<=(b/2)/(2-3b/4)<b,

so every direct guard (7) passes. Neither r nor gamma is supplied to the algorithm.

These are PATHWISE implications on ONE simultaneous high-probability event, for each reached stage and its random predictable averages. A probability of completion by a deterministic stage needs the excitation/gap condition to hold almost surely on reached histories or needs a separate debit for the chance it fails. It is invalid to turn the assertion into P(failure | random favorable average)<=beta without the conditional denominator.

For a common persistent r, let s* be the first scale with a_s*<=b kappa r/5. Since any density-matrix minimum eigenvalue r<=1/d and b<=1/4, a_0 is larger than the target; hence s*>0 and a_s*>b kappa r/10. With b^2>epsilon/(72Aq),

    N_s*<=57600 A q 3^W L/(kappa^2 r^2 epsilon)+1.

The total fine cost is less than 4N_s*/3, and the funding cap must reach s*. The SAME proof replaces kappa^2 r^2 by gamma^2 for persistent actual signed gaps; coarse localization still costs its supplied-kappa bank. The bound is instance-dependent, not floor-free.

Here all predictable averages and the first completion probability belong to the DECLARED calibration experiment with ideal trusted controls and the unknown noisy source. Its resulting record event transfers to the physical implementation with the nu_cal TV debit. A floor known only on a different imperfect-memory trajectory cannot be substituted into the declared experiment by record TV alone. A source excitation promise uniform over every allowed history is a sufficient safe way to apply the completion claim to both implementations.

## 6. From the acquired operator certificate to future service

The received colored coherent-extraction bound is ell0<=3A sum_i(delta_iZ+delta_iX/2). On an accepted Good record the operator certificate gives each delta_ij<=b^2 for EVERY gauge/retained-memory state, so ell0<=(9/2)Aq b^2<=epsilon/4. This changes the broad local theorem's training-state guarantee into a state-uniform frozen decoder, without reconstructing a microscopic environment. The learned reflections need not satisfy exact Pauli relations: the three controlled-reflection blocks remain physical, and the received full-reference inequality supplies their joint composition.

Future CP identity dominance makes exact extraction the same-current-memory full-CPTP oracle. A total calibration-record TV discrepancy changes the bad-accepted mass and completion probability once, by nu_cal. A one-service whole-q-input half-diamond discrepancy costs nu_svc. This supports an ACCEPTED unnormalized excess-risk bound, not an unconditional service claim after abstention and not a beta posterior guarantee for every accepted record. Fixed generators, source structure and complete current-coin nonanticipation remain external promises.
