# Completed finite receiver illustration

This is a completed numerical execution of a finite receiver, not a laboratory
demonstration or a precision certificate for the nonlinear theorem. Run

    python output/selection_independent_principle/finite_receiver/run.py

It produces `results.json` and `retained_records.npz`. The source simulator
alone knows its full Hamiltonian and Gaussian covariance. The receiver function
gets two 32-bit ADC reports and one fresh 24-bit coin word; it returns one arm.

## Operation actually executed

The four-dimensional source has

    H=(p^2+r^2+x^2+0.04 y^2+0.06 xy)/2,
    dx=p dt, dy=r dt,
    dp=(-x-0.03y-p)dt+sqrt(2)dW,
    dr=(-0.03x-0.04y)dt.

Its conditional initial covariance is Gibbs. A fair old reference R chooses
opposite initial mean shifts with exact relative entropy D0=1. The simulator
samples the source at the private trigger by its analytic Gaussian transition;
this saves computer time but grants no physical waiting shortcut.

The simulated clock is exponential with rate 0.003564 and timeout 0.01 at
H=1292.13529349. Of 100000 attempts, 99070 arrived before timeout. Finite PRNG
draws emulate the continuous clock: they do not certify physical privacy or a
bounded-density timing law. Such a clock remains a supplied hardware contract.

Two independent canonical pointers interact sequentially for b=ell=0.0001,
with the explicit smooth Hamiltonian

    H_int=-w(t)xP, w(t)=[1-cos(2 pi t/b)]/b.

Their Gaussian initial variances are v_Q=4e-14 and v_P=2.6666667e-8, with mass
and gain one. The complete coupled source/pointer linear SDE is propagated
during each window, including the actual p-only backaction w(t)P. Detached
pointer readout has Gaussian SD 1e-7 and a 32-bit ADC on [-16,16]. No ADC
overflow occurred. This is an explicit Hamiltonian meter simulation, not a
noiseless or instantaneous momentum oracle.

If the ADC words are n0,n1, the finite receiver computes

    p_hat=(n0-n1)*10000/2^27,
    a=clip(1/2+p_hat/4,0,1).

Its integer threshold is

    floor(clip(2^26+2500(n0-n1),0,2^27)/8).

Comparison against a uniform 24-bit word gives the arm. No sine evaluation,
exact-real arithmetic, source covariance or hidden-state input enters this
operation. A conservative implementation uses at most 256 temporary bits and
1024 elementary Boolean operations per label. The physical hardware is charged
a fixed 0.00002 latency; its gate rates/errors are not validated by Python.

The source then evolves passively for 0.5 and a third finite pointer, of width
0.001, supplies a one-bit position outcome through its own ADC. Only arm,
outcome and abort flags enter the retained records. Diagnostic aggregate
statistics are produced by the separate simulator harness. Fine preparation
reports do not enter the retained instrument output or its future policy.

## Numerical results and their limits

The matched ideal comparison replaces p at the second-window endpoint with
the law

    q_A(dp)=Gamma(dp)[1+A clip(p/2,-1,1)],

with a fair arm independent of the contemporaneous passive hidden/reference
marginal. Both then undergo the same finite delayed future-channel definition.
For this law E[A p]=(2 Phi(2)-1)/2=0.477249868.

| Diagnostic | Actual | Ideal | Monte Carlo scope |
| --- | ---: | ---: | --- |
| E[A R] | -0.000585 | -0.003270 | Paired difference 0.002685, SE 0.004480 |
| E[A p_launch] | 0.481440 | 0.474112 | Paired difference 0.007328, SE 0.003957 |
| E[2 A outcome] | 0.141254 | 0.142647 | Paired difference -0.001393, SE 0.006274 |
| E[R matched-hidden-score] | 0.898505 | 0.898505 | Strong old-reference information remains in hidden state |

The matched hidden score uses the simulator's time-dependent mean direction;
it is not available to the receiver. Actual mean absolute momentum-estimation
error was 0.010425 (RMS 0.013083). The analytic sufficient bound is 0.027058.
These statistics demonstrate the finite algorithm and a nontrivial retained
hidden/reference correlation. They do not certify full joint TV from samples.

At the declared ideal model parameters, the theorem's sufficient error sum is

    0.03 thermal + 0.006764384 metrology + 0.01 backaction
      + 2^-24 coin + 3.91e-14 overflow = 0.046764444.

The Gaussian overflow bound uses the declared structured-family envelope:
absolute mean <=2 and readout variance <=3. This envelope is not inferred from
the absence of observed overflows. Parameter, clock, pointer-preparation,
release, logic/reset and physical-model errors remain additional terms.
The covariance/ODE computations are floating, not interval-validated.

## Execution bill

The expected clock occupancy per attempt, including timeout, is 277.777778;
maximum clock occupancy is 1292.13529349. Successful attempts additionally pay
0.0002 preparation metrology, 0.00002 fixed logic, 0.5 future experiment and
0.001 terminal readout. Cold-pointer and source initialization are extra.

The 100000 independent Monte Carlo replicas correspond to expected total
physical clock occupancy 27,777,777.78 time units and maximum 129,213,529.35.
There is no claim of free iid reuse of one retained source. The short computer
runtime is not an experimental speedup.

Each pointer's target temperature is 2.6666667e-8 times the source temperature,
with trap stiffness 666666.667 and mass one. A separately supplied critically
damped cold-OU preparation service at damping 1632.99316 has a calculated
finite reset duration 0.0244949 from the ambient same-trap Gaussian, with
ideal-model TV residual <=1.34e-7 before trap release. Three sequential resets
would occupy 0.0734847 per trial. This cold reset is an accounted optional
service contract; the program samples its target Gaussian and does not build
a refrigerator or simulate finite trap release. The nonequilibrium free-energy
resource of each pointer is 16.43985 source kT, a lower accounting bound, not
an assertion of actual refrigerator work. Cooling infrastructure, finite
switching/release and their errors remain unexecuted resources.

The interaction coefficient peaks at 20000 and its slew at 6.28319e8 in these
units. Gaussian pointer momenta imply an expected-action contract, not a hard
samplewise source-force cap. The two preparation pointers have expected force
action 0.0008 and satisfy the required Gaussian exponential-integrability
condition. At a proposed physical scale, classical pointer/white-noise validity
must also be checked against hbar and the finite bath/sensor bandwidth.

Unexecuted resources are explicit in `results.json`: source factory preparation
and initial-KL calibration; fresh physical arrival and random-bit ports; cold
pointer reset and finite trap release; gains, noise and backaction calibration;
finite ADC/logic/routing rates; isolated workspace erasure and protection;
continuous thermostat operation; and actual future metrology/occupancy.
The model has a complete finite numerical receiver. These remaining physical
contracts prevent describing the run as a completed laboratory capability.

The future measurement here is arm-invariant. At equal access, retaining a
fine continuous weight could give a stronger ordinary statistical estimator.
The run demonstrates the one-bit arm interface, not a variance advantage over
that comparator or the nonlinear theorem's entire physical scope.
