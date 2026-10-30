# Complementary actual infinite-composition trace

Status: child adversarial review passed; see INDEPENDENT_COMPLEMENTARY_ACTUAL_TRACE_AUDIT.md. Unlike the first residual trace, this statement uses the ACTUAL hard-network rates at every composition, with no A/N lower bound.

## Residual
Put N=A+C and

    g_N=4 floor(N/3)+(N mod3),   s=B−g_N.

Fast conversion preserves s. Clearing reduces N by3 and B by4, so also preserves s exactly. Immigration has s-increment0 or−1, with −1 exactly when N≡2 mod3. Activation has increment0 or+1, with +1 exactly when N≡0 mod3. All assertions include enabling conditions.

Fix s large and study the process until its first nonzero s-increment. During this neutral excursion B=s+g_N.

## Finite composition head
Take N<=8, including every composition A+C=N (45 states). Kill at a nonzero s-increment or a neutral exit to N>8. Every state reaches killing after at most three prescribed immigrations, so the finite killed graph is transient.

check_composition_head_exit_degrees.py performs exact positive rate-Schur elimination with source probes. COMPOSITION_HEAD_EXIT_DEGREES.json records the complete output. For the N<=8 head:

    max degree P(UP exit) = −1,
    max degree P(neutral tail exit) = −3.

Rates have degrees0 (immigration),1 (activation),4 (fast conversion/clearing) in s. Zero channels due to A,C enabling conditions are retained exactly. Positive coefficient sums cannot cancel, so these are exact large-s exponents, not numerical fitted slopes.

Thus uniformly over the 45 head states,

    P_UP <= C_1/s,
    P_tail <= C_2/s^3,
    E tau_head <= C_3 s^12.

The time bound follows directly from a sequence of at most three immigrations: total head rates are O(s^4), immigration rate is1, and holding means are at most1. No recurrence assumption is needed.

## Infinite composition tail: use the earned absorption theorem
For fixed N>=3 and B>=4, retain only fast A/C conversion and clearing. Clearing is killing from the N-shell. The previously checked theorem in chemical_global_gluing_20261030/KILLED_SHELL_FAST_BOUNDARY_SCALE.md gives, after enlarging its constant to cover finitely many small N,

    sup_A E tau_clear <= C N^(−9/4)/(B)_4.

This is an actual killed-shell bound, not a mixing assumption. Both fast and clearing rates share the exact factor (B)_4.

Competing immigration/activation intensity is at most1+NB. Therefore, before the next clearing,

    P(any birth first) <= C B^(−3) N^(−5/4),
    E(time stopped at birth or clearing) <= C B^(−4) N^(−9/4).

In the absence of births, each clearing changes N→N−3 and B→B−4 while preserving s. Consequently B>=s throughout. Summing over the decreasing N sequence until N<=8 gives

    P(any birth before head) <= C s^(−3) sum_(n>=9) n^(−5/4)
                                <= C' s^(−3),
    E(time stopped at birth or head) <= C s^(−4) sum_(n>=9) n^(−9/4)
                                     <= C' s^(−4).

The convergent sums make these bounds UNIFORM over arbitrarily large initial N and every composition. This is the decisive infinite-fiber step. For a fixed initial N only finitely many clearings occur before head entry, so no explosion is hidden in this stopped descent; each conservative shell is finite.

A neutral birth restarts a tail attempt with probability O(s^−3), so geometric summation preserves these orders for time to head or a nonzero s-exit.

## Close head–tail feedback
Let H_s,T_s be worst up-exit probabilities from the head and tail. Then

    H_s <= C_1/s +(C_2/s^3)T_s,
    T_s <= C_4/s^3 +H_s.

Thus the first nonzero s-exit time tau is almost surely finite and

    sup_(all N,A) P(s_tau=s+1) <= C/s,
    sup_(all N,A) E tau <= C s^12.

Holding-time renewal closes because the head-to-tail probability is O(s^−3); the tail's return probability is at most1. This establishes nonexplosion up to the residual exit without assuming global physical nonexplosion.

For every fixed d and 0<alpha<1,

    phi(s)=exp(d s) Gamma(s+1)^alpha

therefore satisfies

    E phi(s_tau)/phi(s)
       <= C exp(d) s^(alpha−1)+exp(−d)s^(−alpha) ->0.

The residual threshold set is still noncompact. Global recurrence is NOT concluded from this trace alone; the accompanying value-function construction must actually couple it to the other regimes.
