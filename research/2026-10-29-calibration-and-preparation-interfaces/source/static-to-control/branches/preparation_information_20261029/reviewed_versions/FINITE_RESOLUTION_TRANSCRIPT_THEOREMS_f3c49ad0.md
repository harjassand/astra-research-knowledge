# From native trajectory coupling to complete finite-resolution experiment laws

29 October 2026. Complementary construction and ordinary proofs. This extends
the root's position-sensor argument to convolution, sampled momentum, continuous
Gaussian meters, and causal record-driven forcing. A separate independent
review of these extensions has not yet been completed.

## 1. Physical source, preparation and the actual observation contract

Use the root's kinetic shear family on the two-dimensional torus:

    dx=v dt,  dv=-gamma v dt+sqrt(2 gamma tau)dW1,
    dy=w dt,  dw=[a sin(nx)-gamma w+u_t]dt
                                      +sqrt(2 gamma tau)dW2.

The native free comparison omits a sin(nx), with the SAME bath and permitted
controller. Controls in this note act only additively on w; they do not alter
x/v, the force field, friction or thermal noise. There are no hidden parity
operations. The following two preparations are supported separately:

- The root's stationary source/free coupling, for which the momentum
  difference is the stationary filtered force Y_n.
- The SAME uniform-position Maxwell preparation in both sources, for which
  the difference is Y_n^0(t)=int_0^t exp[-gamma(t-s)]a sin(nx_s)ds.

Write Y for either version and

    V_n=tau sigma_n/gamma,
    sup_(0<=t<=h) E[Y(t)^2] <= V_n,
    |Y(t)|<=a/gamma,       |Y'(t)|<=2a.                    (1)

Here sigma_n is the root's exact stationary entropy formula and V_n=O(1/n).
In the common-Maxwell version sigma_n is a comparison parameter bounding
transient variance/work, not the claim that every transient rate equals it.
The conditional Gaussian-shift construction and nonnegative force covariance
justify (1) in that version.

An observation policy makes at most N readouts by physical time h. It can
choose future query times, sensor settings, noise levels, filters and when
to stop using its previous REPORTS and independent randomness. Query times
are nondecreasing and chosen causally. It does not receive uncharged exact
y/w trajectories, force increments, hidden event-trigger times or other
unspecified measurements. Every report's noise is freshly independent with
the declared Gaussian covariance. Correlated or overlapping readout noise
must be described by its actual covariance or continuous-channel model.

All query settings, times, stopping decisions and declared commands belong
to the complete transcript. A fixed query count is not assumed to buy its
noise level, timing or spatial/temporal resolution.

## 2. The common-history likelihood construction

Let xi contain the common initial variables, the x/v Brownian driver and
the w thermal Brownian driver, excluding sensor noise. Its probability law
is the SAME in both models. Given xi and a possible previous report history
r_<j, solve the two native controlled systems using that common history.
Their next conditional sensor means are m_n,j(xi,r_<j) and m_0,j(xi,r_<j).
The settings and observation time are the same because the policy sees
the same history in this comparison. For a scalar Gaussian report with
variance eta_j(r_<j)^2,

    KL_j = |m_n,j-m_0,j|^2/(2 eta_j^2).                    (2)

Let P_aug and Q_aug be the two laws of xi and the complete reports. They
are each built recursively from the same xi law and their own correct
conditional Gaussian kernels. The KL chain rule gives exactly

    D(P_aug||Q_aug)
      = (1/2) E_P sum_j |m_n,j-m_0,j|^2/eta_j^2.           (3)

Matrix-valued reports use the corresponding inverse covariance quadratic
form. Stops can be padded with a common dummy kernel. Random policy seeds
can be included in xi. Marginalizing xi gives a transcript KL upper bound.
In particular, every pathwise bound depending on xi alone has the SAME
expectation under either augmented law, because both xi marginals remain
the original driver law.

This is not a construction that couples two independently generated report
histories and pretends their actions agree. It compares their conditional
means at one common history, exactly as required by the likelihood chain.

## 3. Record-driven additive forcing cannot magnify the information

Suppose u_t is any well-posed causal function of the previous permitted
reports and known external inputs. It is not additionally allowed to depend
on unobserved y/w. At one common report history, its realized waveform is
identical in the two models. It therefore cancels when subtracting their
w equations. The differences are exactly

    delta w(t)=Y(t),
    delta y(t)=int_0^t Y(s)ds.                            (4)

No Lipschitz condition on the dependence of u on the report history is
needed for this conclusion. An arbitrarily large commanded gain does not
alter (4) at a common history. Well-posedness and the physical time/energy
cost of the commanded waveform remain required; this is not a free-control
operation or a bound on its work.

Consequently

    E sup_t |delta y(t)|^2 <= h^2 V_n,
    E int_0^h |delta w(t)|^2dt <= h V_n.                  (5)

The torus distance is bounded by the displayed common-lift displacement.
The x/v coordinates are identical under the coupling.

There is an exact statistical explanation for raw linear/translation-
equivariant sensors. Relative to the uncontrolled trajectory, a realized
command adds the known shifts

    A_u(t)=int_0^t exp[-gamma(t-s)]u_s ds,
    B_u(t)=int_0^t [1-exp(-gamma(t-s))]u_s/gamma ds

to w and the lifted y. Subtract A_u (or its convolution) from momentum
reports and subtract B_u modulo 2pi from wrapped-position reports. This is
an invertible causal transformation of the transcript: original reports
and commands can be reconstructed recursively. Thus this feedback experiment
is equivalent to a passive ADAPTIVE observation experiment with the same
query/noise resources. Purely amplifying a noisy report does not reveal a
new force channel. This exact equivalence is restricted to the declared
additive control and translation-compatible readouts.

For a pre-existing native state-feedback force u(t,x,v,y,w), the root's
uniform K-Lipschitz condition in y,w gives instead

    E sup |delta y|^2 <= C_h^2 h^2 V_n,
    E int |delta w|^2 <= 2(1+C_h^2 h^2)h V_n,
    C_h=(1+K)exp[(1+gamma+K)h].                           (6)

The same bounds hold for history-selected members of a uniformly
K-Lipschitz family, by rebuilding both states at the common history. An
unrecorded internal state-feedback law is not an extra exact sensor for
the experimenter. If its actual continuously varying command values reveal
y/w and are also returned, those constitute additional observations and
must be included in the interface and likelihood.

## 4. Adaptive Gaussian position and convolution readouts

A position report has a mean map phi_j(q) of known spatial gain L_j:
|phi_j(q)-phi_j(q')|<=L_j d_torus(q,q'), and independent Gaussian noise
standard deviation eta_q,j. This includes sine/cosine phase meters with
spatial frequency b and amplitude c, for which L_j<=|c|b. It also includes
wrapped position plus Gaussian noise: apply modulo 2pi to a Gaussian
observation of the common torus lift, using data processing.

A momentum-convolution report is

    Z_p,j = int_0^(t_j) k_j(s) w(s)ds + eta_p,j G_j,

where k_j is a causal square-integrable kernel selected from the previous
reports and G_j is a fresh standard Gaussian. Its squared signal difference
is at most ||k_j||_2^2 int_0^h |delta w|^2. Assume the following deterministic
budget ceilings hold for EVERY possible report history:

    J_q = sup_history sum_j L_j^2/eta_q,j^2,
    J_p = sup_history sum_j ||k_j||_2^2/eta_p,j^2.          (7)

Combining (3), (5) and (7) yields the full adaptive-transcript theorem

    D(P_transcript,n||P_transcript,0)
         <= (V_n/2)(h^2 J_q+h J_p),
    TV(P_transcript,n,P_transcript,0)
         <= (1/2)sqrt[V_n(h^2 J_q+h J_p)].                (8)

The bounds include all reports, adaptive settings/times, commands and
stopping decisions. They imply a bound for EVERY subsequent statistical
test or decision, however nonlinear or discontinuous. They are stronger
than convergence of a chosen class of expectation functionals.

For the uniformly K-Lipschitz native feedback in (6), replace the right
KL side by

    (V_n/2)[C_h^2 h^2 J_q
                   +2(1+C_h^2 h^2)h J_p].               (9)

### Explicit bandwidth and precision accounting

A boxcar average over a window Delta_j wholly inside [0,t_j] has
||k_j||_2^2=1/Delta_j. Hence N reports with Delta_j>=Delta_min and
eta_p,j>=eta_p have J_p<=N/(eta_p^2 Delta_min). A boxcar's transfer function
has its first zero at frequency of order 1/Delta_j; this is an explicit
averaging-time/bandwidth resource, not a claim that a boxcar is sharply
band limited. Likewise N position readings of gain at most L and noise
at least eta_q have J_q<=N L^2/eta_q^2.

At fixed h, gamma, tau, a, gain, window and noise floor, V_n=O(1/n), so
the entire transcript TV in (8) is O(sqrt(N/n)). If an experiment attains
TV separation at least delta>0, (8) NECESSARILY requires

    h^2 J_q+h J_p >= 4delta^2/V_n
                      =4gamma delta^2/(tau sigma_n).     (10)

For the fixed instrument parameters just stated this is an Omega(n)
number/precision/bandwidth budget. It is not a matching sample-complexity
theorem or a claim that meeting the bound is sufficient.

Changing bandwidth can also change measurement noise. For a boxcar average
of a continuous Gaussian meter with noise power eta^2, the variance is
eta^2/Delta. Its contribution 1/(variance*Delta) is therefore 1/eta^2,
not a free increase with bandwidth. Overlapping averages of one meter have
correlated noise and must not be counted as independent fresh reports.
The continuous-record theorem below covers every such postprocessing.

## 5. Point-sampled momentum: deterministic and adaptive times differ

For deterministic observation times, the direct momentum difference has
E|delta w(t_i)|^2<=V_n. Thus direct noisy momentum samples add
V_n sum_i eta_p,i^-2/2 to the augmented KL in the record-only-control case.
The same O(N/n) KL conclusion follows.

For an ADAPTIVE observation time tau, it is invalid in general to replace
E[Y(tau)^2] by a deterministic-time variance. The bounded derivative in (1)
provides a valid replacement. For any mesh spacing Delta>0, a grid with at
most h/Delta+2 points and |Y'|<=2a gives

    E sup_(0<=t<=h) |Y(t)|^2
       <=2(h/Delta+2)V_n+8a^2 Delta^2.

Choosing Delta=(h V_n/(8a^2))^(1/3) yields

    R_n := 4V_n+6(a h V_n)^(2/3),
    E sup |Y|^2 <= R_n.                                  (11)

The grid argument remains valid if the chosen spacing exceeds h; the
endpoint-inclusive grid only becomes smaller. For a=0 the sources coincide
and should be handled directly.

If at most N direct momentum readings have total precision budget
J_point=sup_history sum_i eta_p,i^-2, arbitrary adaptive timing gives

    D(P_transcript,n||P_transcript,0)
       <= (1/2)[h^2 V_n J_q+R_n J_point].                 (12)

For fixed budgets this tends to zero, at least as fast as O(n^-2/3) in KL
and O(n^-1/3) in TV for the momentum contribution. This is a conservative
uniform bound, not a sharp rate or the claim that adaptivity achieves that
rate. With root's state-feedback contract, use the valid pointwise bound
2R_n+2C_h^2 h^2 V_n for delta w and C_h^2 h^2V_n for position.

This resolves actual sampled Gaussian-noise experiments without silently
assuming that a momentum L2 path bound controls every adaptive point sample.

## 6. A complete continuous Gaussian meter record

Consider ideal continuous meters with their own independent Brownian noises,

    dZ_p(t)=w(t)dt+eta_p dB_p(t),
    dZ_q(t)=phi(q_t)dt+eta_q dB_q(t),                    (13)

where phi is a globally well-defined torus phase sensor with gain L_q.
The noise amplitudes have continuous-meter units; they are not independent
pointwise Gaussian errors at every real time. Controls may depend causally
on the past meter record and act only through the additive w input.

Condition on xi as above. The two observation drifts are causal functions
of the same possible meter history and differ by Y and at most L_q|delta y|.
Under strong well-posedness, Girsanov gives their conditional path KL as
half the time integral of the squared normalized mean differences. Here
the common-history differences are bounded on the finite horizon by (1)
and (4), so the difference-drift exponential is a true martingale under
the usual construction; no unbounded signal-difference Novikov premise is
being suppressed. Local integrability of the actual commanded signals and
well-posedness still remain required.

Integrating over xi and discarding it yields

    D(P_Z,n||P_Z,0)
       <= (V_n/2)[h/eta_p^2+L_q^2 h^3/(3eta_q^2)].       (14)

The position term uses E|delta y(t)|^2<=t^2 V_n and integrates t^2.
Thus even the FULL continuous noisy meter record becomes indistinguishable
at fixed horizon and nonzero noise power. Every discretization, convolution,
averaging scheme and nonlinear adaptive analysis of this already acquired
record is covered by data processing, without pretending the discretized
errors are independent.

For a causal convolution meter, dZ_p=(k*w)(t)dt+eta_p dB, initialized at zero
at time zero, Young's inequality gives the momentum replacement
h ||k||_1^2/eta_p^2 in (14). More general stationary prehistory initializations
need their own jointly coupled sensor memory; they are not free. Bounded
predictable sensor gains can be included by their uniform gain ceilings.

This is standard Gaussian-channel/Girsanov machinery applied to the explicit
native thermal coupling. It is not a new Gaussian information identity.

## 7. Quantized position readout

For PASSIVE trajectories at fixed times t_1,...,t_N, divide the y circle
into K equal bins with fixed origins. Conditional on every other driver,
the common initial y phase is uniform and delta y(t_i) is independent of it.
The probability of a different bin is at most
min(1,K|delta y(t_i)|/(2pi)). A coupling union bound gives

    TV(bin transcript_n,bin transcript_0)
        <= min(1, K/(2pi) sum_i t_i sqrt(V_n)).           (15)

The x bins coincide under this coupling. The result is not obtained from
the Lipschitz expectation theorem: the bin maps are discontinuous, and
uniform phase supplies the needed anti-concentration.

For adaptive bin origins/times or record-driven forces, conditioning on
previous bins can destroy the unconditional uniform-phase argument at the
next query. One universally valid finite-N replacement is a decision-tree
bound. Given all common drivers other than the initial y phase, there are
at most (K^N-1)/(K-1) query nodes. At each node its time, chosen grid and
record-driven command are fixed; the free y coordinate is the initial
phase plus a fixed shift. The set of initial phases that would cause a
source/free bin mismatch at that node has measure at most
K sup_t|delta y(t)|/(2pi). Union over ALL nodes gives

    TV <= min(1, [K/(2pi)] [(K^N-1)/(K-1)] h sqrt(V_n))   (16)

for K>=2 and the record-only additive-control interface. The bound is
loose but rigorous and tends to zero for every fixed adaptive finite tree.
It does not justify an Omega(n) sample lower bound for noiseless adaptive
quantization. Increasing bit-depth, adaptive thresholds and tree size are
separate observation resources. A continuously valued extra observation
that depends on the initial y phase is not covered by the finite-tree count.

## 8. Source, cost and novelty limits

The mathematical source family, force parameters, bath and observation
channels are supplied. No actual field, sensor, preparation, frequency,
noise floor or independent-error law was acquired in this research. Costs
include real observation duration, source preparation, command work, sensor
gain/bandwidth/precision, record count and processing. The lower bounds do
not turn a supplied fine force field into a cheap physical implementation.

The strongest equally informed route has Gaussian likelihood chain rules,
Girsanov, Pinsker, stable-system input subtraction and standard coupling.
It can derive these same transcript guarantees from the same supplied
physical model. The addition is the explicit consequence for the native
low-dissipation/non-Gibbs family: exact path discrimination survives while
fixed-resolution experiment laws, including the specified adaptive controls,
converge to those of an ordinary free thermal model. No speed advantage or
historical priority is claimed.

For primary comparison, Venkat and Weissman, "Pointwise Relations between
Information and Estimation in Gaussian Noise", arXiv:1110.6654 (2012),
Section II.B.3 and its Girsanov proofs, treats likelihood and estimation
identities with Gaussian feedback. Weissman, Kim and Permuter, "Directed
Information, Causal Estimation, and Communication in Continuous Time",
arXiv:1109.0351 (2012), Section IV, makes the causal Gaussian observation
and feedback contract explicit. Their Gaussian information machinery is
an antecedent, not the new scientific claim. The proofs above use direct
conditional Gaussian KL/Girsanov bounds and do not require a claimed
identification of mutual information with ordinary feedback input entropy.
