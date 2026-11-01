# Independent acceptance: common-form finite mean and near-sharp mean join

Date: 2026-11-01 UTC. Reviewer: independent of both root derivations.

## Verdict and exact immutable sources

**PASS:** the common-form, two-sided Markov theorem

  E_{m(.|A_set)} tau_B <=4 Q_D/M <=4 B_total/M.

**PASS:** the separately derived near-sharp mean bounds, with the controlling
convergence qualification below. These are new consequences of full reference-
energy/tail receiving, not consequences of absolute CDF accuracy alone.

Exact reviewed sources, neither modified:

1. `test_processed_clock_lifetime_20261101_0043/COMMON_FORM_UNIFORM_MEAN_ROOT.md`
   SHA-256 `adaf0b1ee53aa7560eee70e696b5100a1382801dbcd72cf2c01ae3997167690d`.
2. `neutral_processing_clock_pending_20261101/SHARP_MEAN_FROM_COMMON_FORM_ROOT.md`
   SHA-256 `5402b158d789c169535bf5007c21f575db4c3275bb810a09ed711ad83c82c4bf`.
3. Weaker-interface countermodel
   `test_processed_clock_lifetime_20261101_0043/EXACT_REVERISBLE_LIFETIME_COUNTERMODEL.md`
   SHA-256 `4ccfb5f8e077c91855395667f8c1523411b4bada660853641ad78c3164a96a93`.

The actual compact-process receiving is bound to
`PASSIVE_PORT_CLOCK_ROOT_V2.md`, SHA-256
`7696ef6f47f8003749e0b0fbbfdf8c067d1834e398d011c75c8cc075853a5579`.

### Controlling convergence wording, accepted by the root author

The proved convergence is

  k E tau_B ->1, equivalently E tau_B/(1/k)->1,

uniformly over protocols meeting the same received premises as their normalized
certificate errors vanish. If k varies toward zero, this does NOT by itself
prove the unscaled absolute difference E tau_B-1/k tends to zero. The latter
would need the normalized error bound divided by k to vanish. This controls
any ambiguous reading of “means converge to 1/k” in the unchanged sharp source.

## 1. Static reference inequality: accepted in the form domain

Let T_r=exp(-rA) be the positive self-adjoint reference killed semigroup in
L2(D,m), m(D)<infinity. For f in the form domain, 0<=f<=1_D, spectral calculus
and 1-exp(-r lambda)<=r lambda give

  ||f||^2-<f,T_r f><=r E(f,f).

Positivity permits the separate order comparisons

  <f,T_r f><=<1_D,T_r f><=<1_D,T_r 1_D>=H_ref(r).

Thus ||f||^2<=r E(f,f)+H_ref(r). No illegal use of A f in H or of
1_D in the killed form domain occurs. The constant belongs to H because m is
finite. Its inverse FORM Q_D, not the ordinary vector A^-1 1_D, is required.
Spectral Tonelli proves Q_D=int_0^infinity H_ref(r)dr even with spectrum
accumulating at zero.

## 2. Weak energy envelope, including initial 1_D

For either received actual path w(r), sub-Markov order gives 0<=w<=1_D. The
source requires full weak energy dissipation for this path, not just a
scalar/hidden-port equation for h. With F(r)=||w(r)||^2 and r>0,

  F'<=-2E(w,w)<=-2F/r+2H_ref(r)/r.

Multiplication by r^2 gives (r^2 F)'<=2rH_ref(r). Work first on [eta,t] where
the weak solution is in the form domain a.e.; use its integrated energy
inequality or the corresponding distributional/BV statement. Since
F(eta)<=m(D), the initial contribution eta^2F(eta) vanishes. Nonpositive norm
jumps likewise preserve the weighted inequality. Therefore

  F(t)<=G(t):=2t^-2 int_0^t rH_ref(r)dr.

This argument does not assume finite actual mean or integrability of F.
Nonnegative Tonelli then yields

  int_0^infinity G(t)dt
    =int_0^infinity 2rH_ref(r)[int_r^infinity t^-2dt]dr
    =2Q_D.

Both the factor 2 and the boundary at zero are correct. Merely saying that a
formal generator dissipates is insufficient; the source explicitly demands
energy representatives for the constant initial vector. Ordinary common-domain
parabolic form solutions allow every H initial datum, including 1_D even
though it usually violates the killed Dirichlet boundary trace at time zero.

## 3. Chronology, midpoint and the factor 4

The exact chronological factorization is

  P_{0,t}=P_{0,t/2}P_{t/2,t},
  H_actual(t)=<P_{0,t/2}^*1_D,P_{t/2,t}1_D>.

The first vector comes from a forward-density path of duration t/2. The second
comes from the reversed-time backward path r ->P_{t-r,t}1_D, again of duration
t/2. It is not obtained by a formal adjoint-symbol swap. Applying the common
G bound separately to their squared norms gives H_actual(t)<=G(t/2).
Changing variables t=2r yields

  int_0^infinity H_actual(t)dt<=2 int_0^infinity G(r)dr=4Q_D.

Positivity gives survival from exact m(.|A_set) at most H_actual(t)/M. Tonelli
identifies its mean, and the displayed finite bound proves finiteness rather
than assuming it. The factor 4 is valid, not claimed sharp. No stationary
resolvent variational theorem is improperly applied to a time-dependent
propagator.

Both P_{s,t} and P_{s,t}^* must be sub-Markov in the SAME m, on every interval.
Forward or reverse energy receiving solely for the special trial e is not
sufficient. A whole-domain source bound Q_D is essential; a bound only for
<h,A^-1h> does not substitute for it.

## 4. Actual compact drift receives the stronger premises

The base V2's killed diffusion is associated with a common reference form plus
s_amp(t) times a compact smooth weighted-divergence-free transverse transport C.
The reference/full measures are the same; the full actual diffusion preserves
that measure and is conservative by the explicitly proved proper Lyapunov
bound. Killing then gives both P1_D<=1_D and P^*1_D<=1_D. The latter follows
also by testing against nonnegative f and domination by the full invariant
propagator. It is not inferred from forward sub-Markovness alone.

The transport form is bounded on the common H-plus-energy domain and has zero
real diagonal part. Forward density uses -s_amp(s+r)C; reversed-backward
observable evolution uses +s_amp(t-r)C. Both schedules are bounded on each
finite interval, both signs have identical energy estimates, and both
variational equations admit arbitrary H initial data. Thus the constant-source
paths in the common-form theorem are actually earned by this class. No claim
that 1_D belongs to the killed form domain is required. Neutrality of a trial
h is unnecessary for this mean bound once those full premises hold.

For additional non-skew/dissipative processing, the analogous property remains
a separate two-sided common-form receiving obligation. Arbitrary formal
operators, unbounded mobilities, or record-selected controls are not admitted.

## 5. Full-current join is exact

For D=A_set disjoint-union S, inverse-form Cauchy--Schwarz gives

  Q_D<= (sqrt(Q_A)+sqrt(Q_S))^2
      <= (sqrt(B_A)+sqrt(B_S))^2=B_total.

Both source currents must be earned. With k0=C0/M and
1+epsilon=C0 B_total/M^2,

  4B_total/M=4(1+epsilon)/k0.

The mean theorem does not require trial neutrality; that condition was used
for the separate uniform-CDF theorem, which can be combined with it under the
intersection of their premises.

## 6. Independent sharp-tail calculation

The source receives the same model/measure and exact basin initial law, actual
and reference survival errors delta_a,delta_r>=0 around exp(-kt), k>0, and
Q_D<=Qupper with qbar=kQupper/M>=1. Its tail identity is exact:

  int_L^infinity G(t/2)dt/M
    =4Q_D/M -4 int_0^(L/2)(1-2s/L)H_ref(s)ds/M.

To verify it, swap the nonnegative integrals in
4 int_(L/2)^infinity r^-2 int_0^r sH_ref(s)ds dr; contributions from s<L/2
have weight 2s/L and contributions from s>=L/2 have weight 1. Q_D is finite,
so the subsequent subtraction does not subtract infinities.

Reference positivity gives H_ref(s)>=M S_ref(s). The weight 1-2s/L is
nonnegative on the integration range, so S_ref(s)>=exp(-ks)-delta_r remains
usable even where its lower bound is negative. Set ell=kL. Direct integration
of the weighted exponential and constant gives

  4k int_0^(L/2)(1-2s/L)exp(-ks)ds
     =4-8(1-exp(-ell/2))/ell,
  4k delta_r int_0^(L/2)(1-2s/L)ds=delta_r ell.

Therefore the actual tail obeys exactly

  k int_L^infinity S_a(t)dt
    <=4(qbar-1)+8(1-exp(-ell/2))/ell+delta_r ell.

Combining with the actual prefix CDF bounds proves the source's two-sided
finite-ell mean envelope. The lower bound only uses nonnegative tail mass.
For Dsum=delta_a+delta_r>0, replacing 1-exp(-ell/2) by 1 and taking
ell=sqrt(8/Dsum) gives the correct safe upper

  k E tau_B <=1+4(qbar-1)+2sqrt(8Dsum).

For 0<delta_a<1, ell=log(1/delta_a) gives the correct lower
1-delta_a[1+log(1/delta_a)]. At delta_a=0, the actual survival is exactly
exp(-kt) and its mean is exactly 1/k, so no limiting optimization is needed.
For delta_a>=1 the trivial nonnegative lower bound remains; the source does
not assert the logarithmic formula there. Intersecting the upper bound with
4qbar is valid. These are exact-real analytical statements, not numerical
arithmetic/exponential receipts.

## 7. Exact weaker-interface countermodel

The supplied three-state construction is valid. Its conductance identity
r p=rho b makes the killed generator reversible in its displayed weights.
Direct solving gives a=1, q_h=1+delta, fixed rho, and actual basin mean

  1+delta+rho+delta rho/r.

The actual survival differs from exp(-t) by at most the initial exceptional
mass r, while that mean diverges. The source-S inverse form is
rho^2(delta+r)^2/(delta r^2), which diverges, so the family does not satisfy a
uniform whole-domain/both-current certificate. Its reference model/measure
vary with r; it disproves a universal bound from the listed fixed trial data,
not a fixed-reference full-common-form theorem.

Splitting the slab into two equal atoms and adding symmetric locally bounded
exchange preserves the three-state lumped law, common measure and trial;
it is a valid genuinely time-dependent neutral Markov variant. The countermodel
supports rather than contradicts the distinction made by the new theorem.
Its final statement that the stronger question “remains open” is historical:
the full two-sided common-form/whole-source case is now settled by the new
4Q theorem. Port-only or unreceived-processing cases are still not silently
promoted. This receipt supersedes that stale open-question wording without
changing the frozen countermodel.

## 8. Scope and evidence

These new conclusions establish finite and asymptotically near-reference
NORMALIZED means for the specified exact initialization and full actual-process
receiving. They supply no finite second/exponential moment, relative-tail
accuracy, arbitrary total-variation preparation transfer for means, iid
restart, arbitrary feedback, physical control/calibration or quantum claim.
The extra tail receiving, not absolute CDF error alone, closes the mean gap.
Ordinary spectral, semigroup-energy and Cauchy--Schwarz explanations receive
full credit; historical novelty remains unresolved.

The accompanying exact-rational checker binds the reviewed bytes and checks
the finite-chain, source-split and optimization algebra. It is regression
evidence, not a finite substitute for the proofs. Both existing proof ZIPs
remain unchanged. No helper, denied read, permission escalation, upload or
external contact was used for this audit.
