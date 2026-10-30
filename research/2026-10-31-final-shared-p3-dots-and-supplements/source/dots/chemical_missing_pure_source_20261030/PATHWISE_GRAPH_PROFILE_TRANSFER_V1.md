# Graph-path profile transfer by an exact common-seed clock
Status: new personal derivation, unreviewed. This file removes the immediate-A-production premise from the profile implementation, conditional on the corrected whole-cycle profile construction. It does not modify any frozen proof bytes.

## Contract
Fix a0>=2, v>=2, m=a0+v, q>m, and d>=2 composition species. Every fast degree-m complex contains at least a0 A. The finite fast graph is strongly connected and contains mA and a0 A+vX_i for every reservoir species. No immediate A-producing edge is required from these sources. All rates are fixed positive. Add common qB catalyst and connector0->A+B->mA+qB->0.

Subtract a0 A from every fast complex and set A'=A-a0 on A>=a0. The residual graph is a strongly connected homogeneous degree-v graph containing every pure vX_i (including vA'). Its total count is n=N-a0. Exact factorial factorization gives the original fast/clearing generator as

    (A)_a0 (B)_q times [residual fast generator minus killing k_D(A')_v].

Thus its operational-time clearing path is exactly the already-reviewed pure-source killed process. The strict-power independent receipt ffe4918940dd02794a71c5fb653ca390850ce81aa8cddf0080b8d831144f49b9 supplies constants C,c,delta>0, depending on the fixed residual graph, with

    P(tau_op>t)<=C exp[-c n^(v-1+delta)t],
    E tau_op<=C n^-(v-1+delta).

For example delta=1/(vL+1), with L obtained from its graph accessibility proof. This is an operational-clock statement, not an assumed physical-time mixing theorem.

## 1. Physical occupations and actual competition
Physical time and A-occupation up to the first connector event are

    T=E int_0^sigma 1/[(A)_a0(B)_q] ds,
    U=E int_0^sigma A/[(A)_a0(B)_q] ds,

where sigma is the first operational clearing/immigration/activation time. It can be coupled so sigma<=tau_op. On A>=a0, both reciprocal factors 1/(A)_a0 and A/(A)_a0 are uniformly bounded. Consequently, with b=v-1+delta>0,

    T+U<=C N^-b/(B)_q.

The actual immigration and activation probabilities are k_I T and k_T B U, so clearing-first probability tends uniformly to1 for B>=q. The clearing-output inverse-m-th moment is <=C(B)_q T by the same elementary compensator inequality as before. These are the needed uniform small-event/output estimates, with p0(r)=Cr^-b. Small active states are treated separately by finite complex-path access; inactive states are not included.

## 2. Incoming inverse moments without a pointwise negative drift
Let f_s(A)=(1+A)^-s for fixed s>0 and let Q_op be the residual fast generator. Any A-decreasing edge must have residual source A' multiplicity at least1, because all products still contain at least a0 A. Its rate is <=C A' n^(v-1), while its positive f_s increment is <=C_s f_s(A)/A. Therefore, even where Q_op f_s has the WRONG sign,

    Q_op f_s <=lambda_s f_s, lambda_s=C_s n^(v-1).      (1)

Use the underlying unkilled operational fast path with the actual connector clocks as additional independent exponential marks. The nonnegative process exp(-lambda_(2s)t)f_(2s)(A_t) is a supermartingale. Optional stopping at sigma, first localized then by Fatou, gives its expectation at the pre-connector state at most f_(2s)(A_initial). Connector immigration and activation increase A; clearing decreases A by fixed m and has f_s(A_after)<=C_{m,s}f_s(A_before). Hence

    E[e^-lambda_(2s)sigma f_s(A_after)^2]
       <=C_s f_s(A_initial)^2.

The operational survival bound gives

    E exp(lambda_(2s)sigma)
       <=E exp(lambda_(2s)tau_op)
       <=1+C lambda_(2s)/(c n^(v-1+delta)-lambda_(2s))
       <=C_s

for large n. Cauchy-Schwarz, with no independence assumption, yields the actual joint FIRST-connector bound

    E[f_s(A_after); any connector event]
       <=C_s f_s(A_initial).                          (Mpath)

The same argument works for every fixed exponent needed in the full-cycle enumeration. Combining it with a rare-event probability epsilon_N and the 2s version gives the rare-subkernel profile norm C_s sqrt(epsilon_N). This replaces the directional Qf_s<=0 argument by graph-path accessibility plus an exactly controlled clock.

## 3. Good-region time/occupation gap from a stopped barrier
Choose K=N^gamma, gamma>0 small, and start with A>=K. Let rho be first entrance into A<=K/2, stopped also at the first connector event. Before rho, T_pre<=2U_pre/K.

Set s=a0-1 and

    G_K(A)=[(K/A)^s-1]_+.

It is0 initially and bounded below by a fixed positive constant at an entrance into A<=K/2 (bounded jumps only improve this for large K). Only A-decreasing fast edges can increase it. The same source-degree estimate, now restoring the physical clock, gives

    L_fast G_K <=C (B)_q K^s N^(v-1) A.                (2)

Indeed the positive increment is <=C K^s A^(-s-1), the operational decreasing rate is <=C A N^(v-1), and the clock factor (A)_a0 contributes at most C A^a0; since a0-s=1 the remaining occupation is exactly A. The positive-part kink obeys the same bounded-jump estimate. Killing at the connector sends G_K to0 and only improves the upper bound.

Stopped Dynkin therefore gives

    P(rho precedes the connector)
       <=C (B)_q K^(a0-1)N^(v-1) U_pre.

After rho, the uniform physical remaining-time bound from section1 is <=C N^-b/(B)_q. Strong Markov yields

    T/U <=2/K+C K^(a0-1)N^-delta.                    (Gpath)

This tends to0 if gamma(a0-1)<delta. It does NOT assert a scalar gap at low-A inputs; those are handled by the actual bad-return Neumann correction.

## 4. Feeding the whole-cycle boundary mechanism
Use bad set A<=r^gamma and choose

    0<gamma<min(b/m, delta/(a0-1)).

Then p0 K^m->0 and the good-region ratio eta(r)=C/K+C K^(a0-1)r^-delta tends to0. The corrected full-cycle incoming-profile proof requires precisely:
- joint f_s transport for finitely many fixed exponents;
- rare high-activation profile norms;
- uniform small first-event and clearing-output moments p0;
- an actual good-region time/occupation ratio eta;
- physical inactive seeding and coefficient-one weighted repair.

Sections1–3 earn the first four from the residual reaction graph without immediate A-producing edges. The connector/phase identities and inactive-seeding rules are unchanged; the V2 rule designating EVERY inactive high-B entrance remains necessary. The good-side Neumann leakage is bounded by C p0 K^m(eta+p0)U, which tends to0. Since b<=v<m-1, the polynomial cost enlargement by r^(m-1) still pays both bad and good section drifts.

The complementary Z trace uses only uniform physical T,U and clearing-output activity, already earned in section1, so its large inactive strip protocol remains applicable. Accordingly this supplies a candidate extension of the PROFILE mechanism to arbitrary strongly connected residual pure-source paths, not merely directional source graphs.

## Limits
The pure-source operational theorem is used only at its real fixed-graph scope and v>=2. No claim for v=1 is made here. More importantly, arbitrary weakly reversible fast graphs need not have a removable common seed, a conserved positive shell, or pure residual sources. Those remain genuine structural restrictions. The primitive advance here is incoming-profile control through a common clock even when pointwise inverse-A drift fails, not a declaration of general recurrence or novelty.
