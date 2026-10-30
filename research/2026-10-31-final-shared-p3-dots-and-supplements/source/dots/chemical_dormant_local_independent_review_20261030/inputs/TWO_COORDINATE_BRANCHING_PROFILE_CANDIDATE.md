# A two-coordinate profile that survives both reservoir faces
Status: personal derivation, unreviewed. Local fast/clearing/first-connector interface only; not a full network recurrence theorem.

Residual chain2A'<->A'+D<->C+D, fixed positive rates. Restore common seed a0 A with a0>=2, so physical A=a+a0, m=a0+2, and common catalyst qB. Fast killing/clearing is at k_D(a)_2 in operational time, or k_D(A)_m(B)_q physically. This graph lacks pure residual C and D sources.

The scalar reserve a+2D worked only near one face. The following paired profile instead uses the actual branching/conversion structure of the A'/C population catalyzed by D.

## 1. A graph-derived upstream reserve
For each fixed s>0 choose eta<1 sufficiently close to1 and put

    S=A+eta C, f_s(A)=(1+A)^-s, h_s=(1+S)^-s.

The three linear-in-D channels are A'D->2A', A'D->C+D, and C+D->A'+D. Their S jumps are +1, -(1-eta), +(1-eta). Finite-jump power inequalities therefore give

    Q_lin h_s
      <=D h_s/(1+S)[-c_s k_birth a
                     +C_s(1-eta)k_convert a
                     -c_s(1-eta)k_return c].

Choose1-eta small enough that the first two terms have a strictly negative A' coefficient. On active D>0 states, a+c>=1 and (a+c)/(1+S) is bounded below by a positive constant depending only on a0,eta. Hence

    Q_lin h_s<=-c_s' D h_s.                          (R)

This is a proved branching reserve, not a supplied Lyapunov barrier or mixing hypothesis.

For the physical-A profile, the same jump estimates give

    Q_lin f_s<=D f_s/(1+A)[C_s a-c_s c].              (A)

If c>=M(1+A), (A) is strongly negative. On the complementary region, S<=C_M(1+A), so f_s<=C_M' h_s. Thus for constants C1,C2, choosing C2 sufficiently large relative to C1 makes

    Q_lin F_s<=0,  F_s=C1 f_s+C2 h_s,

and gives a strictly negative bound of order D h_s in the complementary region. On c>=M(1+A), it retains the negative term of order D c f_s/(1+A). Also F_s<=C_s f_s because S>=A.

## 2. Nonlinear seed creation is controlled by its competing clearing
The2A'->A'+D reaction decreases A and S by1 and has propensity k_seed(a)_2. Its positive contribution is bounded by

    Q_seed F_s<=C_s a F_s.

At clearing, physical A_after=a-2. Its terminal inverse moment g_s=(1+a-2)^-s, for a>=2, satisfies g_s<=C_{a0,s} f_s(A). Choose C1>=2C_{a0,s}, so F_s-g_s>=cF_s. The killed-generator inequality becomes

    (Q-k_D(a)_2)F_s+k_D(a)_2 g_s
       <=Q_lin F_s+C_s aF_s-c(a)_2F_s.

For a above a fixed A_star, the last negative term dominates the seed contribution. For bounded a and large n=a+c+d with d>0, the negative linear contribution dominates uniformly: either c is large, giving order Dc in (A), or c is bounded and d is large, giving order D in (R). Thus for sufficiently large n the whole right side is nonpositive on EVERY active d>0 state, including both reservoir-dominant faces.

## 3. Stop at the dormant face rather than pretending it is covered
Stop at clearing, the first actual connector birth, or d=0. At a d=0 entrance, A increases by1, so the terminal f_s reward is bounded by F_s. Connector immigration/activation also increase A and S and are handled by their killing terms. Restoring the common clock multiplies the fast/clearing inequality by a positive factor and does not change its sign. Stopped Dynkin yields the joint stopped kernel bound

    E[f_s(A_out)]<=C_s f_s(A_in)                    (P+)

for every active positive-D input. It is not a bound conditional on observed A_out.

DORMANT_TRIANGLE_UNIFORM_FAST_MEAN.md derives a uniform probability O(n^-1/8) of hitting d=0 before clearing from ANY positive-D input. Adding connector stopping only decreases it. Combining (P+) at exponent2s with Cauchy-Schwarz gives the small dormant-return profile norm

    E[f_s(A_out); d=0 exit]<=C_s n^-1/16 f_s(A_in).  (D+)

At active d=0, a>=2. The first fast event is clearing or D seeding, with fixed rate ratio and bounded A jumps; competing connector births terminate with increased A. Therefore direct terminal rewards are <=C_s f_s, and a seed passes a profile <=C_s f_s to a positive-D input. Combining this first-event equation with (D+) is a genuine positive-kernel contraction for large n. It earns the full first-connector/clearing incoming-profile bound uniformly over ALL active compositions, including d=0:

    E[f_s(A_terminal)]<=C_s f_s(A_initial).

No pure residual source, globally vanishing clearing time, or globally negative scalar Qf_s was assumed.

## 4. Incoming-dependent physical time, needed for fast immigration
Use s=m. On large a, the negative killed drift in section2, after the physical clock, has magnitude at least

    c(A)_a0(a)_2 F_m >=c'>0.

On bounded a and large n, the linear negative term grows at least linearly in n and the common A-factor is bounded below. Thus the same F_m pays a unit elapsed-time cost up to the stopped positive-D boundary:

    (B)_q E tau_+<=C f_m(A_initial).

At active d=0, the first-event physical time is <=C/[(A)_m(B)_q]<=C f_m(A)/(B)_q; seeding passes a bounded f_m profile to d>0. The small return norm (D+) closes the two actual time equations, giving

    (B)_q T<=C(1+A_initial)^-m

for the full first-connector/clearing episode. Therefore fast immigration can be charged to the incoming inverse-m profile, not merely to a worst-case mean.

The uniform operational means additionally give T+U<=Cn^-1/8/(B)_q from d>0 and <=C/(B)_q from d=0. The latter non-small dormant case is deliberately retained.

## Remaining global obligation
This construction earns a local two-coordinate reserve profile and a coupled dormant/seeded fast interface. The full boundary-cycle exponential-residual Green through the NON-small d=0 block, and its coefficient-one/weighted forcing into the corrected section operator, still need an actual proof. Separate profile preservation and finiteness of all dormant exit moments do not automatically give that same-exponent norm. General weakly reversible recurrence remains open.
