# A common-form, two-sided Markov energy principle does bound the mean

Status: new exact proof, 2026-11-01 UTC; independent review pending.
This is a mathematical consequence of the full common-form positive Markov
structure, NOT of uniform absolute CDF accuracy. No physical implementation,
feedback, acquisition, or quantum conclusion is supplied. Ordinary semigroup
energy, spectral calculus, and Cauchy--Schwarz receive full prior credit;
historical novelty is not asserted.

## 1. Received premises

Let m be a finite measure on the killed state space D. Let A be a nonnegative
injective self-adjoint reference killed Markov generator on H=L2(D,m), with
closed form E. Its semigroup T_r=exp(-rA) is positive and sub-Markov. Put

    H_ref(r)=<1_D,T_r 1_D>,
    Q_D=||A^(-1/2)1_D||^2=int_0^infinity H_ref(r)dr<infinity.   (1)

The inverse is only a form/monotone zero-resolvent limit. No spectral gap,
ordinary vector A^(-1)1_D, or form-domain membership of 1_D is assumed.

Let P_{s,t} be the actual chronological killed transition propagator. Require:

(a) positivity, Chapman--Kolmogorov, and both sub-Markov inequalities

    0<=P_{s,t}1_D<=1_D,   0<=P_{s,t}^*1_D<=1_D;              (2)

(b) the FULL common-form energy estimate for both actual forward densities
and reversed-time backward observables. Precisely, for each s and each finite
terminal time t, the paths

    u(r)=P_{s,s+r}^*1_D,       0<=r<=t-s,
    v(r)=P_{t-r,t}1_D,         0<=r<=t-s                      (3)

have the usual H-continuous weak energy representatives (or the explicitly
received contractive-jump analogue), belong locally in time to the form
domain, and obey

    (d/dr)||u(r)||^2 <= -2 E(u(r),u(r)),
    (d/dr)||v(r)||^2 <= -2 E(v(r),v(r)).                       (4)

Integrated versions suffice. The finite-energy/weak-domain receiving must
legitimately allow the weighted calculation below; ordinary weak form
solutions, including arbitrary H initial data, do so. Contractive neutral
interventions can contribute only nonpositive jumps to squared norms.

These are stronger premises than the scalar/hidden port inequalities merely
for the one initial vector h. They are earned by the actual common-form
process in PASSIVE_PORT_CLOCK_ROOT_V2, section 6: the adjoint form changes the
sign of the antisymmetric transport, and reversing the bounded measurable
time schedule preserves form-domain bounds and coercive energy estimates.
Additional common-measure dissipative Markov processing has the same property
when both its forward and adjoint forms are actually received. No neutrality
of h is needed for the mean theorem AFTER these full premises are earned.

## 2. A reference inequality for any bounded positive density

For every f in the form domain with 0<=f<=1_D and every r>0,

    ||f||^2 <= r E(f,f)+H_ref(r).                              (5)

Indeed spectral calculus gives

    <f,(I-T_r)f> <= r E(f,f).

Positivity and 0<=f<=1_D give

    0<=<f,T_r f><=<1_D,T_r 1_D>=H_ref(r).

Adding proves (5). This is where the actual Markov order bound, absent from
abstract passive L2 small gain, is used.

## 3. Universal squared-norm envelope

Consider ANY path w(r), initially 1_D, satisfying 0<=w<=1_D and the energy
inequality (4). Let F(r)=||w(r)||^2. For a.e. r>0, apply (5) with the reference
semigroup duration also equal to r. Then

    F'(r) <= -2 E(w,w) <= -(2/r)F(r)+(2/r)H_ref(r).

Therefore

    (r^2 F(r))' <= 2r H_ref(r).

Since 0<=F(r)<=m(D), lim_{r downarrow 0}r^2 F(r)=0. Integrating gives

    F(r) <= G(r):=(2/r^2) int_0^r s H_ref(s) ds.               (6)

This proof is finite-horizon and does not presuppose an integrable actual
lifetime or squared norm. For weak solutions it is justified first on
[eta,r], then eta tends to zero. Contractive jumps preserve the inequality.

Tonelli's theorem yields the exact envelope integral

    int_0^infinity G(r) dr
      =int_0^infinity 2s H_ref(s)[int_s^infinity r^(-2)dr]ds
      =2 Q_D.                                                 (7)

In particular G is integrable even if the reference spectrum accumulates at
zero. Every forward or reversed-backward interval in (3), regardless of its
calendar start time, has the SAME envelope (6).

## 4. The actual heat content and mean bound

Use the chronological factorization at t/2:

    H_actual(t):=<1_D,P_{0,t}1_D>
       =<P_{0,t/2}^*1_D, P_{t/2,t}1_D>.

The first vector is a forward-density path of duration t/2, while the second
is a reversed-backward path of the same duration. Cauchy--Schwarz and (6) give

    0<=H_actual(t)<=G(t/2).                                   (8)

Consequently, by (7),

    int_0^infinity H_actual(t)dt <=4 Q_D.                       (9)

For the exact basin initial law m(.|A_set), where M=m(A_set)>0, positivity
implies

    P_{m(.|A_set)}(tau_B>t)
       =<1_A_set,P_{0,t}1_D>/M <=H_actual(t)/M.

Thus the earned mean theorem is

    E_{m(.|A_set)} tau_B <=4 Q_D/M.                            (10)

The constant 4 is a proved upper bound, not claimed optimal. The stationary
variational inequality giving the sharper constant 1 in appropriate
correlation settings is NOT silently used in the time-dependent case.

## 5. Both-current certificate closes the intended interface

Suppose the SAME reference form has independent source certificates

    <1_A_set,A^(-1)1_A_set><=B_A,
    <1_S,A^(-1)1_S><=B_S,
    D=A_set disjoint-union S.

Inverse-form Cauchy--Schwarz gives

    Q_D<=B_total:=(sqrt(B_A)+sqrt(B_S))^2.

Therefore every actual process earning sections 1--4 satisfies

    E_{m(.|A_set)} tau_B <=4 B_total/M.                        (11)

In the clock normalization k0=C0/M and

    epsilon=C0 B_total/M^2-1,

this becomes

    E tau_B <=4(1+epsilon)/k0.                                (12)

It is a genuine uniform finite-mean principle for the intended two-current
certificate. It needs no global gap and no uniform numerical cap on neutral
processing strength after the actual process and both energy directions have
been received. Independent random predetermined schedules can be conditioned
on and averaged when their paths meet the same premises/certificate.

## 6. Exact scope boundaries

1. A uniform absolute CDF bound alone never implies (10). Here positivity,
   bounded densities on BOTH propagation directions, the full reference
   energy, and finite whole-domain inverse form supplied the missing input.
2. The port assumptions only for u=P^*e do not by themselves earn (4) for the
   constant-source forward and reversed-backward paths. This receiving must
   be explicit. The concrete smooth common-form class in V2 does earn it.
3. Merely fixed trial a and q_h do not suffice for actual lifetime. The exact
   three-state model in EXACT_REVERISBLE_LIFETIME_COUNTERMODEL.md has a=1,
   q_h=1+delta, fixed rho, and mean diverging as r tends to zero, because its
   B_S diverges. That construction does not pass the intended uniformly
   bounded both-current interface, and does not contradict (11).
4. This theorem proves a finite upper mean, not relative-tail accuracy, an
   exponential moment, or that the processed mean is exactly 1/k0. A separate
   sharper approximation argument would be needed for closeness of means.
5. Source-dependent record feedback is not admitted by branchwise common
   measure alone. Its joint actual process must earn the stated premises.
6. Markov neutrality has no implication of zero work, free switching, physical
   source acquisition, or an executable quantum interface.

## 7. Verification, provenance, and blockers

The proof is self-contained. Reference inputs inspected: the original root,
its V2, and audit_neutral_processing_process_20261101_0034. All originals are
immutable and were left unchanged. No numerical fixture is needed for the
proof. A separate finite exact chain checks the weaker-interface distinction.

A short primary-source search found adjacent time-inhomogeneous random-walk
literature, but no external result is needed or claimed as this theorem.
No novelty claim is made. No external state was changed. No tool denial or
blocked retrieval occurred. The remaining action is independent mathematical
review of (5)--(11), especially chronology and the explicit two-sided full-
form receiving; no external authorization is needed for that local review.
