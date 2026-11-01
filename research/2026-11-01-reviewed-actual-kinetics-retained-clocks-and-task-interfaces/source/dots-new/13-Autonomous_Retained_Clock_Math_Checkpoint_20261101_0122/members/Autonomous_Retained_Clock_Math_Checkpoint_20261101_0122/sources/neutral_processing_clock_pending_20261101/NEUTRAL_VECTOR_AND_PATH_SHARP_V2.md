# Received neutral processing: sharper vector bound and finite sampled paths

Status: separate conditional refinement, 2026-11-01 UTC. The original weaker
root remains immutable and valid. This is a self-contained rendering of the
root author's sharper storage argument, independently verified by the reviewer;
its source message is preserved and hashed below. Ordinary energy storage,
completion of a square, Markov conditioning and entropy-chain estimates receive
full credit. Historical novelty is not asserted.

**No actual global odd trial/current certificate or numerical sampled-path
claim is received here.** This is generic conditional theory, not a physical
control/preparation or executable receiving service.

## 1. Sharper vector theorem

Use the Hilbert-space reference form and ACTUAL energy-solution premises of
`PASSIVE_PORT_CLOCK_ROOT_V2.md`: positive injective self-adjoint A, unit trial
e in its form domain, a=E(e,e)>0, finite inverse form q=||A^(-1/2)e||^2, and
sigma=a-1/q in [0,a). For u(0)=e write u=c e+x with x perpendicular to e and
receive, on every finite horizon,

    c'=-ac+y,       y=-E(e,x),
    (1/2)||x(T)||^2 + int_0^T E(x,x)
          <= Re int_0^T conjugate(c)y.

All common-domain, trace, absolute-continuity and actual-wellposedness
conditions remain those of the base theorem. Put

    C=||c||_{L2(0,T)}, Y=||y||_{L2(0,T)}, b=1/sqrt(2a).

The base theorem proves C<=b+Y/a, |c(T)-exp(-aT)|<=d/2, where

    d=aq-1=sigma/(a-sigma)>=0.

For sigma>0 retain the dissipative integral instead of dropping it:

    ||x(T)||^2 <=2CY-2Y^2/sigma
              <=2bY-2gamma Y^2,
    gamma=(a-sigma)/(a sigma)>0.

Completion of the square gives, for every Y>=0,

    2bY-2gamma Y^2
      =b^2/(2gamma)-2gamma(Y-b/(2gamma))^2
      <=b^2/(2gamma)=sigma/[4(a-sigma)]=d/4.             (1)

Since x(T) is Hilbert-orthogonal to e,

    ||u(T)-exp(-aT)e||^2
      =||x(T)||^2+|c(T)-exp(-aT)|^2
      <=d(1+d)/4.                                      (2)

When sigma=0, y=0 and the integrated storage inequality also forces x(T)=0,
so (1)--(2) hold exactly. No division by zero is used.

If the same reference certificate receives a<=k and kq<=1+epsilon, then
0<=d<=epsilon and k/a-1<=epsilon, since aq>=1. The elementary rate estimate
sup_T |exp(-aT)-exp(-kT)|<=epsilon/exp(1) yields

    sup_T ||u(T)-exp(-kT)e||
      <= G(epsilon)
       :=(1/2)sqrt(epsilon(1+epsilon))+epsilon/exp(1).    (3)

Here exp(1) is Euler's number. The proof is finite-horizon first, so no global
spectral gap, infinite-time integrability assumption, stationary processing or
common processing-strength/bandwidth cap is inserted. The full received
energy-solution premise is still essential. Optimality is not claimed.

## 2. Observable chronology and the concrete two-orientation receipt

For a nonautonomous actual Markov transition propagator P_{s,t}, the chronological
forward density from e is u(r)=P_{s,s+r}^*e and satisfies u'=L_{s+r}^*u.
Path prediction needs P_{s,t}e, a different object. Fix s<t and receive

    v(r)=P_{t-r,t}e,  0<=r<=t-s,
    v'(r)=L_{t-r}v(r),  v(0)=e.                         (4)

The derivative follows from partial_s P_{s,t}=-L_s P_{s,t}. Its time ordering
must not be replaced by an adjoint-symbol swap. If (4) has the SAME weak scalar
and hidden-storage receiving, (3) applies to P_{s,t}e.

For the compact transverse stirring class already proved global in the base
V2, write its generator as L_t=L0+s_amp(t)C, with

    C=c_field dot grad,
    c_field=(0,phi(y)psi_cut(U(z)) J grad U(z)),

where J is constant skew and the cutoffs are smooth and compactly supported.
The amplitude s_amp is predetermined, measurable and locally bounded. The
weighted divergence is zero, C is antisymmetric, and it annihilates every
received scalar trial depending only on y, on both sides. Its form is bounded
on the common reference form domain. The actual process is globally received
by the explicit proper Lyapunov bound in the base V2.

The two relevant equations are therefore

    forward density:      L0-s_amp(s+r)C,
    backward observable:  L0+s_amp(t-r)C.                (5)

Both signs and every finite reversed-time schedule have the same common form,
zero real transport energy, neutrality and Lyapunov receiving. Thus both
orientations are genuinely earned for this concrete class whenever the trial
is a received scalar function of y. A general phase-space trial is NOT fixed
by this circulation merely because the original scalar killed trial was fixed;
its neutrality must separately be proved.

## 3. Global mean-zero observable

For a conservative actual Markov process, let pi be its common invariant
PROBABILITY measure and the reference invariant measure. Restrict the reference
form to

    H0={f in L2(pi): integral f d pi=0}.

Require A to be injective on H0. Choose a nonzero mean-zero trial psi in the
reference form domain with finite inverse FORM on H0. Put N=||psi||_2^2 and
receive

    E(psi,psi)/N<=k,
    k<psi,A^(-1)psi>/N<=1+epsilon.                       (6)

The actual evolution must preserve pi, preserve H0, and annihilate psi through
its additional processing on both sides. Its backward observable evolution
must earn section 2. Then

    ||P_{s,t}psi-exp[-k(t-s)]psi||_2
       <=sqrt(N)G(epsilon).                             (7)

The energy proof takes place on H0; positivity and Markov kernels are still
properties of the full process, not a fictitious Markov process on H0.

In the original connected whole-space constant-SPD diffusion, zero reference
energy implies a constant function. Hence restricting to H0 removes the
constant kernel. Common pi preservation makes both actual orientations preserve
H0. This does NOT prove finite inverse form for an arbitrary proposed global
trial. An odd scalar trial can have zero mean by y symmetry, but its form
membership, normalization, inverse-form/source-current cost and actual label
approximation must still be earned. That concrete global acquisition remains
pending in this package.

## 4. Conditional finite sampled-path join

Let Z be an actual measurable +/-1 label on the ENTIRE state space, with
||Z-psi||_2<=eta. Choose deterministic finite observation times
0=t0<t1<...<tn, Delta_i=t_i-t_(i-1)>0. Let

    r_i=exp(-k Delta_i),
    delta_i=sqrt(N)G(epsilon)+(1+r_i)eta.                (8)

Markov contraction, (7) and the triangle inequality give

    ||P_{t_(i-1),t_i}Z-r_i Z||_2<=delta_i.

Suppose the actual initial law nu has density f0<=R with respect to pi. Since
P_{s,t} preserves pi, its adjoint preserves 1 and positivity gives
f_t=P_{0,t}^*f0<=R at every deterministic time. Compare the actual label record
with the two-state chain that has the SAME initial label distribution and
transitions

    Q_i(z,z')=(1+r_i z z')/2.                            (9)

The parameter k is the correlation-decay rate. If represented by a continuous-
time symmetric two-state chain, its flip rate would be k/2, not k; no renewal
claim is needed here.

Let p_i be the actual conditional next-positive-label probability given the
entire ACTUAL previous label history, and q_i its comparison value from (9).
The actual Markov property implies

    p_i-q_i=E[(P_{t_(i-1),t_i}Z-r_i Z)(X_{t_(i-1)})/2
                 | actual label history].

Conditional Jensen and the UNCONDITIONAL deterministic-time density bound give
E(p_i-q_i)^2<=R delta_i^2/4. Since q_i(1-q_i)=(1-r_i^2)/4 and Bernoulli
KL<=chi-square, the entropy chain rule along actual histories proves

    KL(actual finite record || Q finite record)
       <=R sum_i delta_i^2/(1-r_i^2),                   (10)
    TV(actual finite record,Q finite record)
       <=min(1,sqrt[(R/2)sum_i delta_i^2/(1-r_i^2)]).    (11)

Natural logarithms and TV=sup_events|P(E)-Q(E)| are used. All comparison
transitions are positive and initial label laws match, so null histories cause
no absolute-continuity defect. No bound on a hidden-state density CONDITIONED
on the label history is assumed or needed.

Finite initial L2 concentration alone does not replace R in (10). Under only
||f0||_2<=sqrt(D_init), the separately accepted weaker alternative is
TV<=min(1,(sqrt(D_init)/2)sum_i delta_i), obtained by actual-prefix telescoping.
The supplied path audit contains a finite-state counterexample to an unjustified
quadratic KL replacement using only D_init.

## 5. Controlling computational-cost qualification

The source path theorem's phrase "bounded accumulator" is controlled by its
independent audit, SHA-256 below: for J FINITE accumulator states and fixed-cost
updates, standard comparison-chain dynamic programming uses O(nJ) arithmetic
operations and O(J) working space. O(n) means J fixed. Exact-bit complexity,
input decoding, rate/exponential enclosures and numerical error are separate
costs. Bounded real-valued range alone gives no fixed state count and no such
universal cheap-query guarantee. The audit supplies the bounded-range weighted
subset-sum counterexample.

## 6. Limits and provenance

This concerns one finite record of the SAME continuing actual trajectory at
predetermined times, not a reset/iid construction. The singular short-lag factor
1/(1-r_i^2) is charged. Arbitrary adaptive observations, source-conditioned
feedback, continuous renewal laws, indefinite records, processed mean-time
bounds, relative rare-event errors, physical preparation/control, arbitrary
predicate efficiency and executable/numerical receiving are NOT supplied.
The independent path audit includes counterexamples for the density, adaptive-
observation and cost boundaries. The global odd trial/current and actual
numeric path certificate remain pending.

Bound sources:

- Base `PASSIVE_PORT_CLOCK_ROOT_V2.md`:
  `7696ef6f47f8003749e0b0fbbfdf8c067d1834e398d011c75c8cc075853a5579`.
- Unchanged weaker `NEUTRAL_VECTOR_AND_PATH_ROOT.md`:
  `c3c9b693788febb28770bc153ce6594695e5f91fef23c5740783d18ae59ffb26`.
- Root author's refinement message, preserved in
  `audit_vector_path_20261101_0049/ROOT_REFINEMENT_MESSAGE.txt`:
  `1e88f97db1502286a1de43fc4a99ae5cb1e9595ecbd03ec9bd8b8ba172ee1180`.
- `ROOT_VECTOR_TO_PATH_THEOREM.md`:
  `d1eb7f96cd68e1c681baa4907f888265dbd16a233096d9a345a53003d53e4979`.
- Controlling `sampled_clock_process_audit_20261101_0045/INDEPENDENT_AUDIT.md`:
  `592b28cb65e75da7f4ea4274754147892c1e1cb56ddf3dc25cda6ae3afc73bfe`.

No existing proof archive is modified by this refinement.
