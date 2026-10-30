# Uncapped actual activity-credit trace and stopped-cost certificate

Status: independently derived 2026-10-30 by the child reviewer at the parent's request. This removes the composition cap from the activity-credit trace under the explicit homogeneous fast-graph contract. It is not a global recurrence theorem; a companion N-directed certificate and actual drift matching remain separate obligations.

## 1. Contract and exact residual

There are k>=2 composition species X_1=A,X_2,...,X_k, total N. A finite strongly connected fast graph consists of homogeneous degree-m composition complexes, contains every pure mX_i, and has common catalyst qB, where q>m>=2. The connector is

    0 -> A+B -> mA+qB -> 0.

All coefficients are fixed positive constants. Bounds can be uniform over a fixed positive compact box of constant coefficients; arbitrary state-dependent controls are not claimed here.

Let h=q-m>0. Let I(x) indicate that some fast COMPOSITION source is enabled, and put

    Z=B-N-hI(x),       K=k(m-1),       H=K+m.

The common catalyst is enabled whenever Z is sufficiently large. Fast jumps preserve I by the enabled complex return-path argument. Adding A cannot disable I, and activation from an inactive A>=1 state lands active because it creates at least m copies of A. Inactivity implies N<=K. The exact residual increments are:

- fast: 0;
- immigration: -h if it turns activity on, otherwise 0;
- inactive activation: 0;
- active activation: +h;
- clearing: -h if its target stays active, otherwise 0.

In particular any nonzero residual exit is exactly +/-h.

## 2. Uniform active episode bounds, with no composition cap

Use the earned strict-power clearing estimate, enlarged over the finitely many smaller active states/components by complex-path accessibility. For some epsilon>0,

    sup_active E tau_clear
      <= C (1+N)^(1-m-epsilon)/(B)_q,    B>=q.

Inactive small states are excluded from this estimate and will be treated explicitly below. In an active episode stop at the first clearing or competing connector birth. Before that event, N and B are fixed. The total birth intensity is <=C(1+N)B. Additional killing or integrated-hazard comparison therefore gives

    P(birth before clearing)
      <= C (1+N)^(2-m-epsilon) B^(1-q)
      <= C Z^{-(q-1)},

and

    E(time to clearing or birth)<=C Z^-q.

These bounds hold uniformly over ALL active N and compositions, not merely a slowly growing cap. Since m>=2, the displayed N exponent is nonpositive. In fact the earlier O(N^(1-m)) bound already suffices for this uncapping: its exponent 2-m is also nonpositive. The strict-power theorem strengthens the estimate but is not a necessary dependency for this particular conclusion.

## 3. Stopped nonexplosion with an infinite hidden composition space

Fix initial Z=z sufficiently large and stop at its first nonzero increment, tau_z. Before this exit, active activation cannot occur because it would be an upward exit. Every neutral activation starts inactive and ends with

    N_new<=K+m-1=H-1.

A clearing that remains neutral must land inactive; all clearings decrease N. Fast jumps preserve N. Thus, pathwise before tau_z,

    N_t <= max(N_0,H)+J_I(t),

where J_I is the constant-rate immigration count. Its rate is the fixed connector immigration coefficient, so it may be realized by a Poisson clock independent of the other reaction clocks. Also B_t=z+N_t+hI_t. On every bounded time interval the Poisson count is finite almost surely; the resulting bounds on N,B put the process in a finite set with bounded total rates. Localization therefore rules out explosion before tau_z. This argument does not assume the eventual exit time is finite and does not use a global recurrence theorem.

## 4. Uniform blocks at a fixed residual

If an active state has N>H, a clearing leaves N-m>K and therefore necessarily stays active. The active episode then ends down with probability at least 1-Cz^{-(q-1)}, up only through an active activation, or neutrally through immigration. Its mean duration is <=Cz^-q.

For the bounded head N<=H use the following protocol. Starting active, prescribe clearing before a birth. It either exits down or lands inactive with N<=K. At an inactive A>=1 state, prescribe activation before immigration; its probability is at least 1-C/z because 1<=A<=m-1 and B=z+O(1). Then prescribe clearing before a birth. If that clearing is neutral, the combined activation/clearing pair reduces N by exactly one. At most K such pairs reach an inactive A=0 state or a down exit.

At inactive A=0, prescribe successive immigrations until I turns on. The first occurs at the constant immigration rate. At most m-1 more are needed; each, if necessary, beats activation with probability at least c/z. The immigration that turns on activity is a down exit. An earlier turn-on only helps.

A block stops at the first failure of a prescribed choice or at a nonzero residual exit. Any nonterminal failure is residual-neutral, so the next block starts at exactly the same z. A failed inactive activation prescription is immigration, which is neutral or down. A failed inactive immigration prescription is activation, which is neutral. A birth during an active episode is neutral immigration or up activation. There are only a fixed number of active episodes and inactive holding periods per block.

Uniformly over every starting composition, including arbitrary N,

    P(block ends down)>=c z^{-(m-1)},
    P(block ends up)<=C z^{-(q-1)},
    E(block duration)<=C.

All constants depend only on the fixed graph/dimension/orders/coefficient bounds. The large active tail satisfies a stronger near-one down probability, so the same lower bound applies there.

Conditional renewal requires no independence of blocks. Expected block count is at most C z^{m-1}. Summing conditional up probabilities and durations proves the ACTUAL uncapped estimates

    P_x(Z_tau_z=z+h)<=C z^{-h},
    E_x tau_z<=C z^{m-1},

uniformly over all states with Z=z sufficiently large. In particular tau_z is finite almost surely. No logarithmic or o(1) loss remains.

## 5. Finite stopped cost uniform in hidden N

Fix 0<alpha<1 and a positive factorial weight phi with bounded fixed-h tilt ratios; examples are

    phi(z)=Gamma(z+1)^alpha exp(dz),             fixed d,
    phi(z)=Gamma(z+1)^alpha exp[(log z)^a],      fixed a>1.

Choose an integer threshold z_0 sufficiently large, including z_0>h. The exact factorial ratios and the preceding up bound give

    E[phi(Z_tau_z) 1_{Z_tau_z>z_0}]/phi(z)
      <= C z^{-(1-alpha)h}+C z^{-alpha h} ->0.

The same contraction holds for Psi(z)=(1+z)^(m-1)phi(z). Increase z_0 so its contraction factor is at most 1/2 and phi>=1 above the threshold.

Let T=inf{t:Z_t<=z_0}. Define

    W_Z(x,B)=E_(x,B) integral_0^T phi(Z_t)dt  if Z>z_0,
    W_Z=0                                   if Z<=z_0.

The running residual is constant during each neutral excursion. Its expected excursion cost is at most C(1+z)^(m-1)phi(z). Iterating the Psi contraction and summing proves

    0<=W_Z(x,B)<=C(1+Z)^(m-1)phi(Z),
    E_(x,B) T<=C(1+Z)^(m-1)phi(Z),

uniformly over the hidden N and composition. Since Psi has a positive minimum above threshold, the expected number of residual excursions is finite. Together with stopped nonexplosion and finite duration of each excursion, this also proves nonexplosion up to T. It does not assert anything about the unrestricted process after T.

First-jump decomposition is legitimate after this construction: there are finitely many outgoing channels at every state, the value is finite, and the stopped cost is integrable. It gives the exact actual-generator identity

    L W_Z=-phi(Z)   on Z>z_0.

No invariant cap, matrix-head hypothesis, stationary distribution, or pre-existing Lyapunov function is used.

## 6. Exact threshold leakage: polynomial, not finitely supported

The only upward residual jump is active activation. Therefore from the zero-value region, entry into the positive domain is possible only when

    z_0-h < Z <= z_0,

and then its target residual belongs to the fixed finite set {z_0+1,...,z_0+h}. The uniform-in-hidden-N value bound makes every such target value <=C_0. Consequently

    (L W_Z)^+ <= C A B <= C N B

on this strip, and L W_Z=0 on Z<=z_0-h. This leakage generally has INFINITE support: Z bounded can coexist with arbitrarily large N and B. It must be absorbed by another genuine certificate; it is not a finite boundary term.

## 7. A quantitative lower bound and conditional normlikeness

Let S=N+B and D=m+q. Total physical reaction intensity is at most C(1+S)^D. From a state with Z>z_0, the defining stopping time cannot precede the first reaction event. The expected cost accrued before that event therefore yields

    W_Z(x,B)>=phi(Z)/[C(1+S)^D].

This is a useful lower bound, but it is not uniform in hidden N at fixed Z. W_Z alone need not be normlike on the whole state space, and the target {Z<=z_0} is noncompact.

Suppose independently that a companion nonnegative stopped-cost certificate W_r has the analogous lower bound phi_r(r)/poly(1+S) on r above its threshold, with phi_r growing faster than every polynomial, and that

    max(Z,r)>=cS-C_1.

Then W_Z+W_r is normlike: one of the two residuals is a positive linear fraction of S, and its factorial running-cost lower bound dominates the polynomial holding-time denominator. This proves ONLY normlikeness, not the sign of the sum's drift.

For example, if r=N-aB+O(1) with a<1 and a>=0, then

    max(B-N,N-aB)>=(1-a)/(3+a) (N+B).

Indeed (1+a)(B-N)+2(N-aB)=(1-a)(N+B). The bounded activity credit and bounded r offset only change the additive constant. Thus the required geometry holds for such complementary residuals, but the companion value and its drift comparison still have to be earned.

## Scope

This uncapped trace is an actual infinite-background result in every fixed composition dimension under the explicit pure-complex homogeneous fast contract. Its constants are not claimed dimension-uniform. The threshold target is noncompact, its leakage is polynomial on an infinite strip, and a companion N-directed return bias/output-composition argument is not supplied here. The higher-dimensional global drift/entropy-interface obstruction is not declared solved.

### Local dependency receipts

The active clearing estimate is supplied by either the strict-power startup proof or, already sufficiently for this uncapping, the weaker bounded-oscillation killed-fiber estimate. The indicator and block algebra are rederived above rather than assumed from a finite-cap model. Relevant supporting files are `UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME_V2.md`, `STRICT_POWER_FAST_CLEARING_CANDIDATE.md`, and their independent audits. This new uncapped derivation has not yet received a separate whole-proof review.
