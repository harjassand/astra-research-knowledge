# Focused review of the proposed preparation hierarchy extension

29 October 2026. Existing Astra P1 record-geometry reviewer. This reviews
root's proposal in the accompanying input snapshot, before the governing
FAST_MIXING_PREPARATION_HIERARCHY.md is written. Original completed files
are unchanged. No new fixtures or broader test campaign were introduced.

## Verdict

Both proposed extensions are correct at the four-state, one-native-kernel
interface. The full-sensing hard-cap obstruction is a valid polynomial
continuation argument. The independently selected full-state target followed
by actual hitting gives an exact finite-mean preparation, with the stated
uniform bound. The finite-error K^n guarantee also transfers jointly with
an arbitrary pre-existing record, provided the native kernel contract and
fresh preparation randomization remain valid conditional on that record.

The record qualification matters. Fresh preparation phases, target keys,
clock records and labels generated during preparation are not automatically
covered by a claim about pre-existing information.

## 1. Universal hard caps remain impossible with full state sensing

Fix lambda in the physical interval. Let one controller, whose decision rule
and independent seed law do not depend on delta, observe the entire state
(Y,H). It may use all previously observed states, arbitrary independent
randomization and computation, but its only state-changing action remains
another P_delta,lambda call. Suppose it stops within L calls.

For each possible finite state history, integrate over its controller seeds.
The resulting probability of stopping at that history is a delta-independent
number. Its physical path probability is a product of at most L entries of
P_delta,lambda, each affine in delta. Summing finitely many such histories
therefore makes

    m_0(delta)=E_delta Y_tau

a polynomial of degree at most L. Applying one fresh native call after
stopping gives

    m_1(delta)=E_delta Y_(tau+1),

a polynomial of degree at most L+1. This remains true with a continuously
distributed seed: only its finitely many history-dependent stopping
probabilities enter the coefficients. Zero-call branches cause no difficulty.

If exact target service requires m_0=a and m_1=0 throughout the physical
delta interval, the polynomial identities hold at delta=1 as well. At that
mathematical witness, P_1,lambda is the deterministic swap. Consequently

    Y_tau+Y_(tau+1)=Y_tau+H_tau=Y_0+H_0

pathwise, regardless of the full-state stopping rule. The initial uniform
law has zero expectation of Y_0+H_0. Hence m_0(1)+m_1(1)=0, contradicting
a!=0. Full-state sensing cannot supply a universal exact hard cap.

The witness is not being added to the physical operation menu. The exact
claim on the strictly positive physical interval entails a polynomial
identity, which is refuted by evaluating the same finite expression at a
different parameter. This is a legitimate mathematical continuation witness.

The limitation must remain explicit: the same controller is used across
unknown delta. A kernel-dependent external input or an uncharged calibration
law depending on delta can spoil the polynomial premise. Any bounded
calibration performed as part of the same finite-call protocol is already
included in the finite-history argument. Additional actual actuators or
between-call state changes are outside this proof.

## 2. The full-state hitting escape is exact and has finite mean

For a=1/3 the full target probabilities, in order
(−,−),(−,+),(+,−),(+,+), are

    nu=(1/6,1/6,1/3,1/3).

Draw R independently with this law. Execute at least one actual native call
and then stop at the first full-state equality X_t=R. A noninvasive H sensor,
together with the existing Y read, supplies the required equality test.

Every physical transition probability to the chosen R is at least 3/32,
uniformly in the current full state, R, previous history and admissible
parameters. Thus, conditionally on any starting information independent of
the new target draw,

    P(tau>n)<= (29/32)^n,   n>=0,
    E tau<= sum_(n>=0)(29/32)^n=32/3.

The output is exactly X_tau=R, so it has full law nu. This proof actually
allows any initial microscopic law; the stationary baseline is unnecessary
once the full-state target and the uniform hitting bound are supplied.

The target selector has genuine finite expected random-bit cost. One simple
implementation draws two fair bits, rejects outcome 11, and maps two of the
other three outcomes to Y=+1 and one to Y=−1. It uses 8/3 fair bits on
average. One independent fair bit chooses H, for a total of 11/3 expected
bits. Both the selector and the native hitting time have unbounded worst
duration. These costs do not produce an exact hard deadline.

If each actual native call, equality read and controller step has a warranted
bounded physical duration, the finite expected bit and call counts transfer
to finite expected physical time with those actual costs included. Otherwise
the count bound alone is the accepted statement.

This escape uses the known full four-state target. It is not a theorem that
an H sensor alone can generate an unknown microscopic stationary law on a
general state space; exact target generation and hitting a prescribed full
state can be entirely different problems there.

## 3. Joint transfer with a pre-existing record

Let Z be any record available before preparation, with arbitrary alphabet
and arbitrary correlation with X_0. Suppose that conditional on the full
operational state and Z, the subsequent calls still have the declared
Markov kernel P and the compiler draws its fresh phase bits independently
of Z and the initial state, as required by its literal construction.

For the N=2 comparator, each compiled microscopic matrix entry is at least
9/512. Hence its Dobrushin contraction coefficient is at most

    r=119/128,

and its invariant law is nu. For every conditional starting law rho_z,

    TV(rho_z K^n,nu)<=r^n TV(rho_z,nu)<=r^n.

Retaining the actual marginal law of Z and drawing a reference endpoint
independently from nu gives

    TV(Law(Z,X_n),Law(Z) times nu)
       = integral TV(rho_z K^n,nu) Law(Z)(dz)
       <= r^n.                                    (1)

There is no factor depending on the number of retained old-record values
because this is a uniform all-start microscopic contraction, not merely an
unconditional density or projected-moment estimate. Z may, in particular,
identify the initial state completely.

For unknown but fixed native parameters the statement is uniform. It also
permits a latent parameter correlated with Z by first conditioning on both:
all members have the same nu and the same contraction bound. The reference
keeps the joint parameter/old-record law while refreshing only the endpoint
to nu. The actual kernel contract must hold under this conditioning.

Equation (1) transfers by data processing to any subsequent common physical
service channel, including a policy chosen using Z and adaptive later label
reads. The reference uses the same old record, policy and source parameters.
An operation count n selected from Z before preparation gives the bound
E[r^(n(Z))] instead. A stopping count selected from new preparation outcomes
does not follow from this fixed-count argument.

### Precisely what is not covered

The old record must not reveal the supposedly fresh phase randomness. If a
randomization key is generated in advance, retained in Z, and later used by
the compiler, then conditional on Z the kernel is generally a fixed-key
kernel rather than K. Averaging the key can preserve nu while conditioning
on it does not. One cannot apply (1) using that averaged kernel.

Nor does (1) assert that the endpoint is independent of the new preparation
transcript D, such as its last label, phase bits or completion time. A
transcript containing the final label is visibly correlated with X_n.
If a later policy is allowed to condition on D, the claimed common service
channel must include an actual matched joint endpoint/transcript guarantee;
discarding D in the proof does not establish one.

The full-state hitting method has a particularly clear old-record property:
if its new target R is independent of Z, then X_tau=R makes the output
exactly independent of Z, even from a correlated starting state. It is of
course correlated with its retained new target R and generally with its
hitting transcript. Keeping those distinctions explicit resolves the
pre-existing-record transfer issue.

## 4. Acceptance scope

The proposal's two main claims are accepted. The joint finite-error transfer
is accepted with the conditional native-kernel and fresh-randomization
premises stated above. No additional numerical tests are needed for these
extensions. This is an internal review of the supplied proposal; the future
governing file should be separately pinned once its actual text exists.
