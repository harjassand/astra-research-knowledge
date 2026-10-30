# Generic local-congruence remainder for the useful-service assembly
2026-10-30. Algebraic candidate. This proves the local Taylor/noise step used in the new first-order assembly; it does not prove any missing actual-service premise or a continuous logical barrier.

## Local hypothesis and exact expression

Let an analytical CP generator have a sum of bounded local terms

    L_w,e^*O=sum_a J_ea^* O J_ea+K_e^*O+O K_e.

There are O(N) terms, bounded incidence, fixed support size and uniformly bounded sums of Kraus/operator norms. Put Delta_e=-L_w,e^*I; it is Hermitian and need not be positive. The conservative local term

    L_c,e^*=L_w,e^*+{Delta_e,.}/2

is unital GKLS, with the same J_ea and Hamiltonian `(K_e^*-K_e)/(2i)`. Total Delta may likewise be indefinite. These hypotheses hold for the direct local S_t=V_c^(1/2) similarity of the actual complete guarded LOAD/other bundles; no physical source-split generator is assumed.

Let X_i be bounded self-adjoint local operators with fixed support/overlap, with strengths epsilon_i. Color into finitely many layers and fix their order. Set

    Y(u)=ordered product_i exp(u epsilon_i X_i/2),
    M_e(u)=Y(u)^(-*) L_w,e^*(Y(u)^*Y(u))Y(u)^(-1).

Exactly,

    M_e(u)=sum_a [Y J_ea Y^(-1)]^*[Y J_ea Y^(-1)]
              +[Y K_e Y^(-1)]^*+Y K_e Y^(-1).         (1)

This formula includes the full anti-Hermitian and Hermitian no-jump parts. It does not require the loss or Hamiltonian to commute the credit, and does not omit killing.

## Exact finite cone and Taylor bound

For each initial operator J_ea or K_e, process the gates in the ACTUAL inside-to-outside order of the similarity. If a gate's support is disjoint from the support obtained so far, it commutes at that step and cancels; otherwise retain it and enlarge the support. A gate canceled early remains canceled even if a later gate expands the support back toward its site. Fixed depth and bounded overlap give a uniformly bounded structural cone. Taking the union over all operators in one complete e bundle gives one common subcircuit for (1). This is precisely the causal-cancellation reasoning already independently checked for the earlier weighted-debt congruence, and does not use its extra corner lemma.

All derivatives through order two on 0<=u<=1 are therefore bounded in norm by C_e epsilon_max^2, with epsilon_max=max|epsilon_i| and a fixed number of gates in each cone. In particular,

    M_e(1)=-Delta_e+sum_i epsilon_i L_c,e^*X_i+R_e,
    ||R_e||<=C_e epsilon_max^2.                        (2)

For the derivative, Y'(0)=H/2, `(Y^*Y)'(0)=H`, H=sum_i epsilon_i X_i is self-adjoint, and

    M_e'(0)=L_w,e^*H+{Delta_e,H}/2=L_c,e^*H.            (3)

Thus there is no first-order killing error. Local unitality makes every disjoint X_i contribution zero. Neither positivity of Delta_e nor commutation of X_i with Delta, raw E or other X_j is needed.

Summing O(N) bounded-incidence terms gives the FULL operator inequality

    sum_e M_e(1) <=-Delta+sum_i epsilon_i L_c^*X_i
                         +C epsilon_max^2 N I.        (4)

This is O(N), not O(N^2): no global generator norm or global Taylor expansion is used. No claim of a zero-debt corner for R_e is made or required.

## Application and continuous perturbations

Take the positive debt/activity/exposure witnesses of FIRST_ORDER_USEFUL_DEBT_ACTIVITY_ASSEMBLY.md, with strengths delta, beta_A, zeta and epsilon_max=O(delta). Let S=Y S_t, W=S^*S. Congruencing (4) gives the physical nominal drift with its first-order bound (10) and an additional C delta^2 N relative remainder.

Under the accepted normal interval-wise joint-CPTP/domain contract, a centered local HP perturbation N_e(t) of joint adjoint norm <=eta c_e contributes

    S^(-*) N_e^*(S^*S) S^(-1) <=C eta c_e I.          (5)

Indeed S is a fixed-depth circuit of local invertible SYSTEM gates (commuting local factors for V and C_h, then the colored witness factors). In the superoperator conjugation, gates disjoint from the local SYSTEM support commute with N_e, even when N_e also acts on the common retained bath, and cancel with their inverse congruences. Only a fixed system causal cone remains, with bounded gate/inverse norms. Centering N_e^*(I)=0 prevents any spurious identity source from canceled disjoint factors; the accepted centering convention may be used at its stated norm cost. The bath-only generator annihilates S^*S. Sum (5) by bounded incidence to obtain C eta N I, on the SAME actual joint evolution/reference.

Consequently the unconditional useful-service bound earned from the first-order assembly is

    L^*W <= S^*[-kappa B_cover+C rho N I]S,
    B_cover=sum_h(F_h a_h+A_h)+sum_v R_v.              (6)

The bracket B_cover dominates a fixed positive multiple of E ONLY on the admitted raw canonical basin. Because S need not preserve that basin, this does NOT yet imply a killed-process inequality with E in (6), even for an input supported in the basin. A compressed input does not imply its S-congruenced state is compressed. Here kappa=c lambda t and

    rho <=C[delta^2+lambda delta+lambda^2 t
                 +lambda t^2+(lambda t)^2/delta+eta].

For delta=C_d sqrt(lambda)t, rho/kappa<=C[t+sqrt(lambda)+lambda+eta/(lambda t)]. This confirms the proposed scale hierarchy with actual local constants; it does not extend Tanner density outside its proved basin or solve noncommuting killed compression.

## Barrier and initialization information, not a logical theorem

Since every X_i>=0, each exponential has minimum singular value >=1, and therefore Y^*Y>=I. Hence

    W>=V_c>=(1-t)^(n_h)V>=exp(-C tN)V,
    W<=exp(C delta N)V.                               (7)

The different comparison needed by the noncommuting entropy lemma is also local:

    S S^*=Y V_c Y^*<=Y V Y^*<=exp(C delta N)V.          (8)

For each witness gate, its similarity by V^(-1/2) has bounded local generator norm, so its relative norm is <=exp(C epsilon_i); multiply O(N) such bounds. This is not inferred from (7) by an invalid interchange of S^*S and SS^*.

A simple small-moment initialization is all native engines I/W/P0 with free tags, empty queues, Alice workers IDLE and Bob masters FLUSH_SEND(0), together with the stated small raw Bell-source energy/error module. Then every history/semantic/activity flag starts at zero. Exposure X need not vanish, but its norm is O(N) and its strength is zeta, giving the explicit small initial overhead. The older stochastic theorem's arbitrary FIFO/worker allowance does NOT imply a small initial E moment; recovering it here requires a separate startup argument or an explicit initial moment hypothesis.

No continuous-noise first-exit or logical-class preservation follows just from (6)-(8). Those are the next global obligations; no Poisson ancestry is imported into them.

## Precise remaining noncommuting-basin obstruction

The older accepted killed-moment proof required its energy credit to commute the basin projector and its CP maps to preserve the basin. The present debt witnesses can fail to commute raw E, so neither W nor S is known to preserve that projector. The polar/log entropy identity does NOT repair this. One needs an actual basin-preserving replacement, an independently proved noncommuting exit estimate, or a local-circuit leakage/boundary argument with the correct exponential budget. A generic global ||W|| bound may lose the barrier. Until that bridge is earned, (6) is a full-Hilbert coverage-observable drift, not a continuous-memory moment/lifetime theorem.
