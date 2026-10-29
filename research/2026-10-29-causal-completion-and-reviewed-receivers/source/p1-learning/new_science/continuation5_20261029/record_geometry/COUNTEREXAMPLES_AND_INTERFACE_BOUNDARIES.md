# Local certificates: three exact failures and the missing interfaces

29 October 2026. Complementary constructive challenges within Astra P1.
The examples are mathematical models, not apparatus measurements. Their
arithmetic checks are in check_local_control_boundaries.py and its report.

## 1. An arbitrarily small acquired closure defect can miss a long-time local response

Take one visible sign Y and a frozen fair hidden sign H, with full baseline
mu uniform on the four pairs. A native call flips Y with probability

    p_H=delta(1+H/2),   0<delta<=2/3,

and leaves H unchanged. This kernel is reversible for mu. Conditional on H,
increments are independent. The visible projection on span{1,Y} has flip
probability p_bar=delta and is a genuine positive Markov kernel.

For either output label, the conditional-response residual is, up to its
sign, p_H-p_bar. Therefore the sum of the two output-row defect energies is

    epsilon^2 = 2 Var(p_H) = delta^2/2.                (1)

It is exactly a Gram/return-loop quantity under the existing reversible
acquisition interface. No hypothetical copy of the hidden state is used.

Retain the actual initial visible sign Z=Y_0. For m native calls,

    C_actual(m)=E[Z Y_m]
      = [(1-delta)^m+(1-3delta)^m]/2,
    C_projected(m)=(1-2delta)^m.                       (2)

Both single-time visible laws remain exactly fair. With delta=1/(2m),

    C_actual(m)-C_projected(m)
      -> exp(-1)[cosh(1/2)-1] > 0.                    (3)

The TV distance of the two genuine joint laws of (Z,Y_m) is half the
absolute correlation difference. Thus epsilon->0 does not give a modulus
of approximation tending to zero uniformly in service horizon, even for
one site and one retained old bit. All microscopic equilibrium laws agree.
There is no global density factor to blame.

The mechanism is relative rather than absolute error. Each hidden sector's
conductance differs by 50% from its average, independently of delta. The
visible relaxation time grows like 1/delta. The relative kinetic receiver
therefore correctly refuses a vanishing certificate.

Tensoring this device with any number of spectator sites embeds the
failure in arbitrarily large finite-range systems without changing it.
The example disproves a general all-time claim. It does not contradict
a theorem with a fixed positive contraction rate, a relative energy
certificate, or a bounded time horizon.

## 2. A retained visible calibration record can select rare local failures

For N sites, let H_i be independent Bernoulli(q), and initially let all
visible signs Y_i be independent and fair, independently of H. Every
native site call is local, reversible for this same product mu, and obeys

    H_i=0: refresh Y_i to a fresh fair sign;
    H_i=1: keep Y_i unchanged.

There is no hidden sensing. For a predetermined site the compressed flip
probability is (1-q)/2, and its acquired output-row defect is

    epsilon_i^2 = q(1-q)/2 -> 0.                      (4)

Perform L native calls on each site and retain their visible readouts Z.
Flag a site if none of its L visible increments flips. Every H_i=1 site
is flagged. Each H_i=0 site is falsely flagged with probability 2^(-L).
The full microscopic law after this deterministic calibration schedule
is still mu: every call preserves mu.

Now use Z to select the first flagged site, and make one further call
there. If no site is flagged, report a distinguished no-service output.
The reference retains the **same actual Z** and initial visible state but
uses the positive compressed kernel for this selected call.

Consider the observable event that a flagged site was selected and the
service call flips its sign. The reference probability is at least

    (1-q)/2 [1-(1-q)^N].

The actual probability is at most N(1-q)2^(-L)/2, since a service flip
requires that some nonfrozen site was falsely flagged. Consequently the
joint record TV distance is at least

    (1-q)/2 [1-(1-q)^N-N 2^(-L)].                     (5)

There is also an exact expression. Put a=q+(1-q)2^(-L) and
b=(1-q)2^(-L). A selected flagged site is nonfrozen with conditional
probability b/a, so the joint TV distance is

    [1-(1-a)^N] [(1-q)-b/a]/2.                        (5a)

The coefficient is nonnegative. Initial signs and all other visible
readouts do not further change the selected site's posterior hidden
type, because under the nonfrozen device the flip increments are iid
fair. The checker also verifies (5a) by a separate small enumeration.

Choose N=q^(-2) along reciprocal-integer q, and
L=2 ceil(log2 N). Then N2^(-L)<=1/N and (5) tends to 1/2, while every
fixed-site defect (4) vanishes.

The information costs N L native calls and their real endpoint reads.
This is not free acquisition through retained bits. The example matters
because a theorem cannot promise a dimension-free guarantee for arbitrary
record-selected service locations merely from the same small stationary
defect at every predetermined site. A fixed observation region, a local
causal controller, conditional per-device calibration, or a paid selection
bound is needed. Conditioning only on the rare flag at one predetermined
site already defeats a per-record conditional claim; using many sites
amplifies that issue into an order-one **joint**, not just conditional,
error.

The devices are identically distributed. Translation invariance in law
does not repair the selection problem. Nor does unconditional stationarity
of the source after calibration.

## 3. Uniformly small local row errors can select a different finite-range phase

This elementary example uses a one-dimensional ring in a low-temperature
sequence, rather than invoking a fixed-temperature two-dimensional phase
transition theorem. It proves a failure of any uniform assertion over
noncontractive local receivers. It does not claim a finite-temperature
phase transition in one dimension.

Let s_i in{0,1} on a ring of length N>=3. Put

    q_N=N^(-2),       r_N=1+1/N,
    pi_0(s) proportional to q_N^(number of domain walls),
    pi_1(s) proportional to
          q_N^(number of domain walls) r_N^(number of ones).       (6)

Both laws have full support. Their random-scan heat-bath chains are local,
irreducible and reversible. In spin notation sigma_i=2s_i-1, the coupling
is beta_N=log N and the small dimensionless field is
h_N=(1/2)log(1+1/N).

For fixed neighbours, the ideal conditional odds for s_i=1 are
u in {N^(-4),1,N^4}; the perturbed odds are r_N u. The largest row TV
difference occurs at the mixed-neighbour context u=1 and is exactly

    delta_N = r_N/(1+r_N)-1/2 = 1/[2(2N+1)].           (7)

Thus the error at every local update tends to zero uniformly over state.
It is stronger control than a stationary L2 row estimate.

Nevertheless the equilibrium mean spin at any predetermined site changes
by order one. The unperturbed mean is exactly zero. The two constant
configurations have relative weights 1 and r_N^N, so their conditional
mean spin is

    m_const,N=(r_N^N-1)/(r_N^N+1) -> tanh(1/2).         (8)

Nonconstant configurations have at least two domain walls. There are
2 binomial(N,k) configurations with k walls for even k. As their field
factor is at most r_N^N, their weight divided by the constant weight is
bounded by

    [2 r_N^N/(1+r_N^N)]
       sum_(k>=2) binomial(N,k) q_N^k
    <= [r_N^N/(1+r_N^N)] (N q_N)^2 exp(N q_N).        (9)

The last inequality follows by bounding the binomial sum by the
exponential series from order two onward. It tends to zero as N^(-2).
Hence the actual equilibrium mean m_N tends to tanh(1/2), by translation
invariance and an error at most twice the nonconstant probability.

Each finite positive heat-bath chain converges to its own equilibrium.
Starting both from any common state, sufficiently long deterministic
times therefore expose this discrepancy. There can be no all-time,
volume-independent local-observable modulus tending to zero with delta_N
for this class.

This failure concerns a **conservative coherent field**. It is not an
error that must violate a cycle condition. Exact preservation of the
intended energy ratios matters even if all numerical errors are tiny.
For each fixed time, finite-speed/local-coupling estimates remain valid;
the problematic limits involve increasingly slow, strongly correlated
receivers and long times.

The checker evaluates (6) by exact two-by-two transfer matrices:

    M=[[1,q_N r_N],[q_N,r_N]],      Z=trace(M^N).

The logarithmic derivative r_N d(log Z)/dr_N gives the mean number of
ones. All weights, matrix products and derivatives are rational.

## 4. Three distinctions a receiving theorem must retain

**An endpoint versus an ever-growing local record.** Even iid Bernoulli
outputs with probabilities p and p+epsilon can be distinguished with
arbitrarily high probability from a long record. A uniform endpoint or
fixed-lag correlation guarantee is not uniform TV of an unbounded record.

**Physical locality versus local readouts.** Knowing that only a nearby
label is read does not imply a finite-range microscopic generator. An
unmeasured shared bath, a simultaneous global actuator, or global
controller communication can move predictive influence outside a proposed
causal cone. Microscopic locality, bounded event opportunities and the
controller's communication range need their own warranted interface.

**A local experiment versus a universal material law.** Finite calibration
at some sites cannot certify unobserved heterogeneous devices. To reuse
one certificate across arbitrarily large volumes one needs a structural
common local operation, a justified parameter-sharing or sector premise,
or calibration of the affected deployment sites. Spatial replication of
an experiment does not itself justify that premise.

These are supplier boundaries. They do not invalidate a finite-time local
theorem with fixed observation geometry or the relative kinetic receiver
with its stronger exact-balance and relative-energy assumptions.
