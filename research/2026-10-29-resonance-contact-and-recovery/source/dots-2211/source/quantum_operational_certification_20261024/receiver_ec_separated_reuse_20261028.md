# Separating native residual strength from syndrome-reset error

28 October2026. New derivation; independent review pending. Depends on the received full-operator CPTP idempotent ideal EC channel P. No new physical noise assumption is inferred from its algebra.

Let actual cycle E_t=F_t N_t, where N_t is the closed native-noise plus learned-inverse residual CPTP map and F_t is the actual noisy EC CPTP map. Require fresh/discarded ancillas and inert old records, with no omitted memory returning between cycles. Assume full physical-channel bounds

    ||F_t−P||_diamond ≤ e_t,       ||N_t−I||_diamond ≤ n_t,
    b_t = (1/2)||P F_t N_t P−P||_diamond.

These are physical-map bounds, not merely encoded-input or sampled-state scores. Define Q=I−P, S_t=P E_t...E_1 P and G_t=Q E_t...E_1 P, with S_0=P, G_0=0. S_t is CPTP, so its diamond norm is one; PG_t=0 and ||Q||≤2.

Because QP=0, **Q F_t N_t=Q(F_t−P)N_t**. The native residual need not be close to identity for this identity. Hence

    g_t:=||G_t||_diamond ≤ 2e_t (1+g_(t−1)).

The logical recurrence is

    S_t−S_(t−1)
      = (P F_t N_t P−P)S_(t−1) + P F_t N_t G_(t−1).

On the off-code contribution,

    P F_t N_t G
      = P(F_t−P)N_t G + P(N_t−I)G,

using P²=P and PG=0. Therefore

    (1/2)||S_t−S_(t−1)||_diamond
      ≤ b_t + (n_t+e_t) g_(t−1)/2.

For uniform e_t≤e<1/2 and n_t≤n, g_t≤2e/(1−2e), and

    (1/2)||P E_T...E_1 P−P||_diamond
      ≤ sum_t b_t + (T−1)(n+e)e/(1−2e).

The sharper time-varying version propagates g_0=0, g_t≤2e_t(1+g_(t−1)) and sums b_t+(n_t+e_t)g_(t−1)/2. If F_t=P exactly, all g_t=0 and the bound is just sum_t b_t: native noise alone cannot leave syndrome leakage after ideal actual recovery.

This improves a bound charging the whole native strength to leakage. It does not supply numerical e_t,n_t,b_t for an experiment. Norm bounds can be obtained from complete calibrated local gate models; a deterministic channel calculation below may instead compute particular repeated logical channels directly without claiming diamond certification. Initial unknown-input injection and terminal actual readout remain separate one-off interfaces. The final P is a declared ideal decoded metric, never an inserted operation between actual cycles.
