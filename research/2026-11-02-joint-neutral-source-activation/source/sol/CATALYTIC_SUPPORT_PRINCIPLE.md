# Cooperative activation through a catalytic gate: a complete physical return principle

Same-principal author proof. No independent review or historical-priority claim. This is a sufficient structural theorem, not unrestricted weak reversibility. It uses the raw support-activation lemma proved in HYDRO_ACTIVATION_RECEIVER.md and classical finite-time density/martingale reasoning, not stationary-fiber averaging.

## 1. Raw list and statement

There is one port 0->A of rate lambda>0 and A->0 of rate mu A. All internal reactions preserve total count N. For a fixed integer a>=1, EVERY internal source and product contains aA. Subtract aA from those endpoints. The residual internal list is conservative, has largest source degree ell>=2, and its degree-ell support closure reaches residual A from EVERY singleton support. Lower-degree residual reactions are allowed. All present constants are fixed positive and propensities are falling factorials.

The full list is weakly reversible for the classwise conclusion. The raw constructor checks this and the literal conservation/gate/support conditions; they are not a furnished boundary oracle.

**Theorem.** Every actual irreducible class is nonexplosive and positive recurrent. For its stationary law and every r>0,

    E_pi [(1+q(X)) exp(rN(X))]<infinity.                     (C1)

For rational input, rational 1<u<t and an adequate arithmetic budget, the finite data below acquire one global head and a real stopping episode with

    E_x[ integral (1+q)u^N ds+V(actual output)]<=V(x)−1,      (C2)

where V=t^N outside the head and zero on it. This receives all simultaneous inventory changes without phase resampling, fixed landing profiles, a mixing gap or an infinite-rate limit. A stationary moment constant still needs the actual finite-head trace; the constructor does not claim to compute that constant.

## 2. Exact residual clock and paid seeding

Write R=X−a e_A on A>=a and n=sum R=N−a. The exact factorial identity is

    (X)_(a e_A+y)=(A)_a (R)_y.

Hence in the OPERATIONAL clock du=(A)_a dt the internal residual rates are exactly kappa_r(R)_y. This is an exact time change, not an averaging limit. While A>=a, operational port intensities satisfy

    lambda/(A)_a<=Lambda=lambda/a!,
    mu A/(A)_a<=M=mu/(a−1)!.

Every internal reaction keeps A>=a; only a genuine port death can cross the gate.

If initially A<a, all internal rates vanish. Let the actual port birth/death process run until A=a, retaining every holding time and death. Set

    p=[lambda/(lambda+mu a)]^a.

In blocks of a genuine jumps, a successive-birth word reaches the gate with probability at least p, regardless of the current A<a. Thus the expected jump count is <=a/p and mean time <=a/(lambda p). During this stage N<=N_in+a, and the exact physical holding reward yields

    E seed F-cost <=C_seed u^N_in,
    C_seed=(a/p)(1+1/lambda)u^a.                             (C3)

At completion hidden counts are unchanged and A=a exactly. If A>=a already, skip this stage. In either case the residual count n is DETERMINISTIC given the original launch and satisfies N_in−a<=n<=N_in; N_seed<=N_in+a.

## 3. Uniform residual activation and persistence from raw supports

Apply the raw support construction of HYDRO_ACTIVATION_RECEIVER.md to the degree-ell residual list. It acquires T=d+1, L_0=ell K_ell, b=2^(−ceil(2L_0T)) and delta>0 such that its conservative leading ODE has z_A(s)>=delta on [d,T], for EVERY initial normalized composition.

Use the smaller tracking tolerance

    epsilon=delta b/(16d).

The same compensated-Poisson proof, now with bounded adapted operational port intensities Lambda,M, gives computable C,c>0 and n_track such that an operational block of length T v^(1−ell), started at residual count v>=n_track, tracks its leading ODE within epsilon with failure probability <=C exp(−cv). It may be stopped earlier at a physical gate/mass/time boundary. Here one may use

    L_F=ell^2 2^ell K_ell,
    C_E=ell^3 3^(ell−1)K_ell+ell 2^(ell−1)K_lo+Lambda+M,
    Q=2^ell K+Lambda+M,
    b_F=2^(−ceil(2L_FT)), h=epsilon b_F/2,
    c=min(h^2/[4(ell^2QT+ell h)],1/2),
    C=2d+2^ceil(2Lambda T),
    n_track>=max(ell,2C_ET/(epsilon b_F)).                  (C4)

For comparison one can reflect the operational port death at residual A=0. The original process and that auxiliary chain coincide until gate crossing. A tracking path with a positive macroscopic A lower bound cannot reach that crossing; no reflected dynamics is substituted into the physical reward.

First run an ACTIVATION block, stopped at its operational length or the first actual port event. The port-event probability is at most

    (Lambda+M)T n^(1−ell)<=C_port/n,
    C_port=(Lambda+M)T.

On no port event, n is unchanged. Except for a further C exp(−cn) error, the block ends with residual A>=delta n/2. Its physical length is <=T n^(1−ell)/a! and its entire physical reward is bounded by

    C_amp n u^N_seed,
    C_amp=T(K+Lambda+M+1/a!).                               (C5)

Indeed q_internal dt=q_residual du exactly, so total genuine activity costs O(n), while residence and operational port compensators are bounded by the same block. All failed activations terminate at their actual output: a first port event changes N by at most one; a low-A terminal input otherwise has unchanged N. No failure is discarded.

The stronger fact needed next is PERSISTENCE without mixing. Suppose a residual block starts at count v with A_res>=delta v/2. The leading loss bound dot z_A>=−L_0 z_A keeps it >=delta b/2 throughout that block. On tracking, the actual residual A is >=delta b v/4 throughout. At its end activation gives A_res>=(delta−epsilon)v, while the new residual total is <=(1+d epsilon)v. Their ratio is >delta/2. Thus the same qualification passes to the NEXT ACTUAL block, without a neighboring-profile premise or composition reset.

## 4. A real mature interval, with every intervening port event

After successful activation, observe the original process for physical duration H/n, stopping earlier if residual total leaves [n/2,2n] or the gate is crossed. Lower exit is favorable and upper/gate exits will be paid as errors. Decompose this interval into the actual residual operational blocks of Section3, truncating the last one at the physical endpoint.

On the mass strip and n>=a, (A)_a<=(3n)^a. The total operational time is therefore at most 3^a H n^(a−1). Each full block has operational length at least T(2n)^(1−ell). With D=a+ell, the number of full/partial blocks is at most

    J(n)<=J_c n^(D−2),
    J_c=2+3^a 2^(ell−1)H/T.                                (C6)

Every block starts at residual count >=n/2. Conditional bounds and a union bound, with NO independence assumption, make their total tracking error <=C J_c n^(D−2)exp(−cn/2). A gate crossing on an otherwise tracking block is impossible. Upper mass exit requires at least n immigrations; if n>=H its probability is <=2^ceil(2lambda) exp(−n/2). Thus

    P(bad mature exit)<=C_J n^(D−2)exp(−c_M n),
    C_J=C J_c+2^ceil(2lambda), c_M=min(c/2,1/2).             (C7)

Unless there is a favorable lower exit, all qualified blocks give throughout the ENTIRE physical interval

    A>=a_* n,                  a_*=delta b/8.

The actual death hazard is at least mu a_* H. Independent raw Poisson drivers and the event-dropping/Cauchy argument used in (H7) therefore give

    E[t^(N_out−N_seed)]
      <=exp[lambda H(t−1)/n−Delta_t mu a_*H]
        +t^(−n/2)+B_t sqrt(P(bad mature exit)),             (C8)

where Delta_t=1−1/t and B_t=2^ceil(lambda(t^2−1)) for n>=H. The favorable lower exit supplies the second term; every adverse actual path supplies the last one. Actual death and immigration continue throughout this interval.

## 5. All choices are finite and can be acquired

Choose the integer

    H>= [a(t−1)+4]/[Delta_t mu a_*].                         (C9)

Then the death exponential in (C8) is <t^(−a)/16. Require n>=2lambda H(t−1) so its positive immigration factor is <=2. Require n>=2a+8/Delta_t so the lower-exit term, after multiplying by t^a, is <=1/16. Let

    epsilon_bad=1/[16 t^a B_t], p_M=D−2.

The finite sufficient thresholds

    n>=(2p_M/c_M)^2,
    n>=2C_J/(c_M epsilon_bad^2)

make the mature bad probability <=epsilon_bad^2. They use p_M log n<=c_M n/2 and exp(−c_Mn/2)<=2/(c_Mn). Thus the three terms of (C8), including the possible seeding increase t^a, total at most1/4.

The two failed-activation terms contribute at most1/8 if

    n>=16t^(a+1) C_port,
    n>=16t^a C/c.

Also require n>=max(a,H,2n_track,1). The FULL actual outgoing law of seeding, activation and maturity consequently satisfies, conservatively,

    E t^N_out <=(1/2)t^N_in.                               (C10)

This is an earned receiver on ALL states, not only an approach to a chosen face.

The complete mature physical F cost is at most C_mat n^(D−1)u^N_seed. For n>=H, the immigration count is dominated by Pois(lambda), so an acquired bound is

    C_mat=H 2^D(1+lambda+mu+K)
      *2^ceil(2lambda(u−1))
      *sum_(j=0)^D S(D+1,j+1)(lambda u)^j.

Together with (C3),(C5), the entire episode costs at most

    C_all N_in^(D−1)u^N_in,
    C_all=C_seed+u^a(C_amp+C_mat).                          (C11)

This includes unbounded seed holding, every genuine internal reaction, every mature port event and all failed branches. No physical interval is deleted.

Let zeta=1−u/t. A single head L includes a plus all n-thresholds above, and

    L>=(2(D−1)/zeta)^2,
    L>=8C_all/zeta, L>=4/Delta_t.

Then (C11) is <=t^N/4 and (C10) leaves residual at least one. Set V=0 on that head and V=t^N outside; stopping early at the head removes only nonnegative future cost/output. This proves (C2). No asymptotic numerical fitting chooses L.

## 6. Physical recurrence and the full remaining frontier

Only immigration increases N, so N(s)<=N(0)+Pois(lambda s) pathwise and the actual chain is nonexplosive. Repeat the real episodes with absorption at the acquired head. Their nonnegative potential plus accumulated F reward gives finite expected entire F occupation until that head. The residual one-unit loss gives finitely many episodes; there is no infinite sequence of uncharged re-seedings. Closing the true finite-head trace on any actual closed irreducible class proves finite physical return reward and (C1), exactly as in the uncatalyzed receiver theorem.

This construction handles cooperative, mutually evolving, unbounded activation inventories. Its joint rule is a finite raw support witness followed by a quantitatively proved persistence block, not a scalar constant landing profile. The real-rate gate clock is restored using its exact factorial factor and bounded operational port hazards; the long mature physical interval is paid using polynomially many controlled blocks. Neither stationarity nor rapid mixing of a conservative shell is assumed.

It still requires a common catalytic gate and a support-activating leading residual system. The accepted rate-2 five-species N1621 model has an A-free CD source and is outside this guard. General conservative cores with incompatible gates, and arbitrary nonconservative weakly reversible lists, still require a different joint return construction. This theorem is a bankable structural operation toward that destination, not the destination itself.
