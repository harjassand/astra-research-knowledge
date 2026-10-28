# Whole review of the positive uniform-stiffness access bound

**ACCEPTED at its stated zero-start, fixed-duration controlled-path
scope.** I whole-read root_thermal_tomography/POSITIVE_SHIFT_BOUND.txt
and independently derived its extension of A's already accepted
finite-alternative path comparison. No model, recurrence, trajectory,
numerical bound or source code was rerun. This is not a new review of
A's separate local stationary/Fisher theorem, which is not used here.

## 1. Common-feedback reference and adaptation

The same parameter-independent predictable policy must be used under
both hypotheses, as stipulated. Its input is only the observed port
history and independent randomness with common prior. Fixed schedules
and the stated bounded regular feedback satisfy the declared
well-posedness admission; arbitrary singular feedback is not granted.

On an alternative path let Z_H solve the hidden LINEAR equation driven
by the actual X_p and the same hidden Brownian noise. The error
E=Z_H-X_H solves the displayed causal ODE. Since the controlled shift
is a scalar multiple of identity, even for a random feedback path,

    Phi(t,s)=exp[-Q0(t-s)] exp[-int_s^t lambda_r dr].     (1)

This follows pathwise from commuting Q0 and the scalar shift. Given
the augmented record U=(X_p,Z_H) and controller randomness, lambda is
the same observable functional and the error ODE reconstructs X_H.
The port correction F_t is therefore adapted to that record. Using a
known alternative parameter in this LAW COMPARISON does not grant an
experimenter an unknown hidden variable or an implementable actuator.

The reference controlled harmonic law need not be Gaussian. Ordinary
adapted drift-change entropy/Girsanov only needs the common diffusion,
admissible reference law, localization and finite control energy.
Those premises remain available under the stated well-posedness and
nonexplosion assumptions. Controller output values need not coincide
under the two laws: their POLICY, not their realized histories, is
the common input.

## 2. Gain, moments and entropy coefficient

M-matrix structure gives B>=0 and exp(-Q0t)>=0. Nonnegative shifts
make the scalar factor in (1) at most one. Thus, pathwise,

    F_t^2<=a^2 r0 int_0^t k0(t-s) X_v(s)^6 ds,
    r0=int_0^infinity k0=g0/b0.                         (2)

Weighted Cauchy gives the first inequality, and the block-inverse
identity gives the last equality. Integrating over t and using
Fubini yields the squared gain r0^2, including for feedback because
the damped RANDOM kernel was first bounded by the deterministic
positive baseline kernel. No independence between lambda and X is
assumed in (2).

In Ito's radial-moment recursion the additional drift contributes
-2m lambda_t ||X||^(2m), which is nonpositive. From zero the same
induction as A's accepted source gives

    sup_t E||X_t||^6
       <=(theta/kappa0)^3 n(n+2)(n+4).                 (3)

No stationary covariance or controlled-reference Gaussian law is
used to obtain this uniform moment. Localization removes the bounded
Girsanov controls using nonexplosion and finite energy; no positive
sixth-moment exponential/Novikov assumption is inserted. Combining
(2),(3) with diffusion sqrt(2theta) gives exactly

    D(P_a||P_0)
       <=a^2 theta^2 n(n+2)(n+4)/(4kappa0^3)
                                      *(g0/b0)^2*T.    (4)

The initial laws are both zero, so no initial KL is missing. Granting
the independent controller seed does not evade (4): condition on the
common seed, apply the same bound, then average. The logged shift is
a measurable function of that seed and port history. Finite exposure,
independent detector noise and subsequent processing cannot add KL.
If noisy readouts control lambda, their independent noise can be
included in the common seed and granted to the ideal observer.

## 3. Quantifiers and scientific consequence

Equation (4) is a fixed-duration bound, also valid with a deterministic
total duration budget across zero-start runs by the conditional
chain rule. If a future version permits unbounded adaptive stopping,
the cost would have to be an appropriate expected total duration and
the stopped-transcript entropy justified; one must not replace a
random duration by a pointwise deterministic lower bound. No such
optional-stopping strengthening is needed for this accepted claim.

For a=Delta, Pinsker requires KL>=2(1-2p)^2 for both testing errors
at most p. The saved n32/theta1/Delta1/2 constant is A's SAME already
qualified coefficient, yielding the stated total native-time lower
above 7.4499e22. This review did not recompute that source or reinterpret
native units as laboratory seconds.

At fixed theta, Delta and the K3 path class, g0=1/F_(2n+2), b0 bounded
away from zero and kappa0=1. The polynomial n factor in (4) cannot
remove the exponential depth cost. When a quartic box contains
Delta e_v (Delta<=A), a uniform coefficient guarantee with error
strictly below Delta/2 and the stated risk implies the same testing
task. Mixtures cannot bypass this two-point implication.

This is an access-wide obstruction for NONNEGATIVE UNIFORM shifts,
not merely a poor variance statistic or ill-conditioned interpolation.
It coexists with exact finite-temperature variance injectivity.
It does not give the optimal exponent, bound the n4 star's sufficient
1e37 plan, or prove an economical or impossible instrument. Negative
shifts, additive drive, changed bath, additional ports and fresh
stationary preparations change the experiment and remain excluded.
Uniformity is essential to the scalar commuting propagator in (1);
the proof is not silently extended to arbitrary nonuniform controls.

There is no dissipation/work lower bound in this argument. Allowing
unrestricted nonnegative-shift control cost only makes the information
bound stronger; any physical accounting is a further admission issue.
Ordinary adapted Girsanov, positive kernels, block inversion and Ito
moments remain credited. Historical novelty and practical superiority
are not inferred.
