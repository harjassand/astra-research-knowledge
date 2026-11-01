# Flag-free source: exact readiness bound and duty-cycle admission

Parent reconciliation, 2026-11-01 16:44–16:47 UTC. Replaces the flag protocol, rather than claiming its invariant-sector repair was completed. Parent supplied the flag-free centered-occupation idea; this note derives the source constants and coupling bound.

## 1. Actual finite clock and exact own-clock Poisson coefficients

For each check p use one private probe and a cyclic clock:
* idle state 0; start/preparation transition 0->1 at rate r;
* D busy phases, each exiting at rate kappa; the last performs readout/cache overwrite and returns to idle.
The busy sequence consists of the controlled single-data-Pauli factors and the readout; insert a fixed number of additional local operations if required and include them in D. Preparation is a TP reset channel to (I+sX)/2, epsilon=(1-s)/2. Every readout is accepted. No active/bad flags, mutual exclusion, queue, reliable external clock, or collision detector exists.

Keep partial prefix P_p=I at start, update it at factor gates, and keep P_p=S_p after completion and through idle. Start reset changes its label from S_p to I. These endpoint prefixes commute with every complete check and protected logical Pauli.

Let t0=1/r+D/kappa. The expected time to next readout is t(0)=t0 and t(j)=(D-j+1)/kappa for busy phase j. This exactly solves the readout-killed own-clock Poisson equation.

For cache p define e_p=(I-Z_cache,p Sbar_p)/2 with the root's exact dressed true check
 Sbar_p=S_p product_q Z_q^[omega(P_q,S_p)].
Define readiness r_p=1_[p busy](I-X_p P_p)/2. The armed mask is essential: r_p=0 immediately after readout and throughout idle.

The second Poisson reward coefficient is exceptionally simple: xi=t0 on ALL busy phases, zero idle. Only readout produces the bad-report gain g=kappa*t0; all interior busy transitions preserve the constant xi, and the last killed transition gives -kappa*t0. Thus xi solves the required killed reward equation exactly.

Set V_p=t(clock_p)e_p+t0 r_p. Its preparation floor is
 b_p=epsilon*r*t0*1_[p idle] <=epsilon(1+D r/kappa).
It is NOT kappa*epsilon/r. The long reset waiting time and its small arrival rate cancel.

## 2. Exact transport and bounded collision remainder

All controlled-Pauli factor hops exactly transport Sbar_p and hence e_p. Completed readout/reset of other probes also preserves this dressed observable. Own factor hops transport X_p P_p exactly because the check factors act on distinct data sites. Without an interfering neighbor, the readout channel satisfies E^*e_p'=(I-X_p S_p)/2, and the armed readiness is killed.

Two interference terms remain, with no assumption that the quantum state is classical:

(a) A neighbor q's gate U_q=C_q(R) changes readiness by
 U_q† r_p U_q-r_p
 = 1_[p busy] X_p P_p (I-Z_q)/2
when omega(P_p,R)=1, and zero otherwise (the sign convention follows U_q†(X_p P_p)U_q=X_p P_p Z_q). This Hermitian difference has operator norm <=1. The gate is enabled only while q is busy. Multiplication by t0 and its rate kappa therefore costs at most kappa*t0 I_pq in operator order, where I_pq=1_[p busy]1_[q busy]. For a given q only one legal clock exit is enabled at a time; do not multiply by the number of gate channels unnecessarily.

(b) At p readout, Sbar_p=S_p Z_extra, where Z_extra is a product of Z_q for incompatible partial neighbors. The actual post-overwrite mismatch differs from (I-X_p S_p)/2 by
 X_p S_p(I-Z_extra)/2.
Its norm is <=1. It vanishes if every neighbor is idle, since idle prefixes are complete commuting checks. Hence its positive part is bounded by sum_q 1_[q busy]. The readout source is itself busy, so its rate-weighted coefficient is bounded by kappa*t0 sum_q I_pq.

Consequently, on all legal clock configurations and arbitrary probe/data states,
 L_ideal V_p <= -e_p + epsilon*r*t0*1_[p idle] + 2 kappa*t0 sum_(q neighbor p) I_pq I_data.
This is an OPERATOR bound, not a marginal event-probability argument. It includes arbitrarily overlapping legal probes and makes no clean-flag assumption. The source potential remains positive even if different readiness terms do not commute.

Classical readout bit-flip eta adds a floor bounded by eta*kappa*t0*1_[p readout phase]. That occupation can itself be centered using an own-clock Poisson term, or priced as a bounded local perturbation. Merely bounding this by eta*kappa/r loses the duty factor. Actual detector/helper coherent errors require the root's local perturbation admission.

## 3. Centered pair occupation removes state-dependent collision gain

The ideal private clocks have independent marginal generators even when probes/data are entangled: each phase map is TP, so its total jump hazard is state independent. Their stationary busy fraction is
 f=(D/kappa)/(1/r+D/kappa)=D r/(kappa+D r).
For a neighboring pair let Q_pair be their finite product generator. Solve
 Q_pair h=-(I_pq-f²).
A solution is h(x)=integral_0^infinity [E_x I_pq(X_t)-f²]dt, up to an additive constant. Shift it so min h=0.

For each ordered neighboring pair add 2 kappa*t0 h(clock_p,clock_q) I_data to the positive potential. Its exact generator contribution cancels the corresponding 2 kappa*t0 I_pq upper bound. The remaining collision floor per ordered pair is
 2 kappa*t0 f²
 = 2 D² (r/kappa)/(1+D r/kappa).
Thus, summing checks,
 L_ideal V_total <= -sum_p e_p + N epsilon(1+D r/kappa)
                    + 2 D² (r/kappa)/(1+D r/kappa) * (# ordered neighbor pairs).
Heterogeneous rates/weights use the actual product-chain stationary probabilities and per-pair coefficients; identical parameters are used here only for transparent scaling.

This is a genuine global mean source Foster bound on legal clock configurations. It has tunable collision floor O(Delta D² r/kappa), finite reset-purity floor, and no global-in-time approximation. It is not an exponential-memory proof by itself.

## 4. Uniform bound on the pair Poisson span

Assume D r/kappa<=1. Couple two copies of the pair chain using common start ticks (rate r) and common progress ticks (rate kappa) for each component. A progress tick advances a busy phase and does nothing in idle; a start tick starts idle and does nothing in busy.

Over a block T=2D/kappa, require no start ticks for either component and at least D progress ticks for each. Then both copies have reached (idle,idle) and coalesced, regardless of initial phases. The no-start probability is exp(-4D r/kappa)>=exp(-4). A Poisson(2D) variable is at least D with probability >=1/2 for D>=1, giving block success probability q>=exp(-4)/4. Therefore
 E tau_couple <= T/q =8 exp(4) D/kappa.
For an observable with range [0,1], the coupling representation gives
 span(h)<=8 exp(4) D/kappa.
The shifted h is nonnegative with this bound. Hence the added collision-potential span per ordered pair is at most 16 exp(4) D*t0=O(D/r). This large but finite local overhead must be charged to initial apparatus energy, barrier constants, and perturbation susceptibility. It is not free and is not proportional to total runtime.

## 5. Remaining physical-clock repair boundary

The derivation covers ALL overlaps of valid private clocks; it does not require legal collision flags. It still assumes a valid finite cycle encoding. Use the physical-qubit sorting clock only after checking that (i) sorting preserves decoded phase/rank and therefore t, r masks, dressed true checks and pair h; (ii) invalid factor hops, mode flips and premature resets have bounded local potential increase; (iii) sorting's negative inversion drift dominates those bounded illegal contributions. The slow idle/start stage must be physically represented in that cycle and its rate r included. Reset and readout are TP labelled GKSL channels; a two-body microscopic derivation remains unprovided.

Clock faults create inversion/phase debt and are charged through the actual local noise admission. No perfect clock initialization or single-particle sector is silently restored. The large coefficients O(1/r) amplify helper-noise susceptibility, imposing a genuine lower bound on usable r while collision dilution imposes an upper bound.

## 6. Superseding physical phase-count reconciliation (16:48 UTC)

Parent/native-clock builder confirms the actual sorting-clock cycle has 2M+2 legal phases: M forward steps (including prep, controlled-Pauli factors, readout), one mode flip, M return steps, and the other mode flip. The first preparation step is slow, rate r; all other transitions have rate kappa. Readout occurs BEFORE return, not at the idle boundary.

For this actual cycle replace the idealized section-1 coefficients as follows:
* D_eff=2M+1 counts all fast nonidle holding phases.
* T_cycle=1/r+D_eff/kappa is the full mean cycle time.
* t(x) is the sum of mean holding times from phase x through the NEXT readout (explicit finite sum). In particular t(post-readout)=T_cycle, while t(idle) generally is smaller and is NOT T_cycle.
* xi=T_cycle on armed phases, zero after readout and through return. The accepted-readout gain is kappa*T_cycle.
* A conservative busy indicator is every nonidle phase, including unarmed return. Its stationary fraction is f=D_eff*r/(kappa+D_eff*r).

The actual exact bounds therefore use
 V_p=t(x_p)e_p+T_cycle*r_p,
 reset floor <=epsilon*r*T_cycle=epsilon(1+D_eff*r/kappa),
 collision coefficient 2*kappa*T_cycle,
 collision floor per ordered pair 2 D_eff²(r/kappa)/(1+D_eff*r/kappa).
The pair coupling proof applies with D_eff: D_eff fast ticks with no slow-start ticks drain any phase into idle. The earlier no-return t0=t(idle) identification must NOT be applied to this physical cycle. All source equations above remain valid with this explicitly corrected destination-readout coefficient.
