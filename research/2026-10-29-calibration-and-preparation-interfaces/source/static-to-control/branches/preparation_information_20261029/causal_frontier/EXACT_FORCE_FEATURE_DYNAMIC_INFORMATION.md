# Exact dynamical force records defeat a static bounded-force information ceiling

29 October 2026. Consequential challenge to an overly broad n^2 trial claim.
Ordinary proof independently checked in
alternative_frontier/RELATIONAL_PAIRING_AND_DYNAMIC_INFORMATION_INDEPENDENT_REVIEW.md.
No physical record was acquired; the reviewed original is preserved in
reviewed_versions/EXACT_FORCE_FEATURE_DYNAMIC_5ffae82b.md.

## 1. Why this distinction matters

The static Gibbs phase assay in NATIVE_REFERENCE_FRAME_IDENTIFIABILITY.md
has per-preparation Fisher information c I1(c)/I0(c)=O(n^-2) when n u=A
is fixed. That bound concerns a single instantaneous prepared-state readout.
It cannot be extended to the complete controlled dynamical force-feature
path. The following explicit score has a fixed finite-horizon distinguishing
gap under the same bounded-force actuator, even though the static feature
mean is only O(1/n).

## 2. Two native phase hypotheses

Use the same potential U_0(x)=-(A/n)cos(nx), so the actual actuator force
is -A sin(nx) and its amplitude is the fixed A. Prepare the DRIVER in its
Gibbs law and hold this potential. Let

    phi_+=pi/2,       phi_-=-pi/2,
    f(t)=sin(nx_t+phi_+/-).

The declared additional observation is the exact CONTINUOUS scalar f path.
This was allowed as an optional force-feature interface in the root's
proposal. There is no lab-frame x readout. The receiver y,w may be recorded
as well, but is unnecessary for this distinguishing statistic.

The driver dynamics are

    dx=v dt,
    dv=[-gamma_d v-A sin(nx)]dt+sqrt(2gamma_d tau)dW.

Let z=nx+phi and theta=phi (psi=0). Then z'=n v and

    dv=[-gamma_d v-A sin(z-theta)]dt+sqrt(2gamma_d tau)dW.

The feature f=sin z has C1 paths with f'=n cos(z)v. Ito's rule gives

    d f' =[-n^2 sin(z)v^2-gamma_d f'
                       -n A cos(z)sin(z-theta)]dt
                    +n cos(z)sqrt(2gamma_d tau)dW.        (1)

## 3. A common observable score

Define the measurable exact-path functional

    H_h = [f'(h)-f'(0)+gamma_d(f(h)-f(0))]/n
             +(1/n)int_0^h f(t) f'(t)^2/[1-f(t)^2]dt.     (2)

Off the zeros of cos z, the quotient f'^2/(1-f^2) equals n^2v^2. The
exceptional times have Lebesgue measure zero almost surely, since each
stationary phase has a smooth density and Fubini applies. Define the
integrand arbitrarily at those times; the integral is unchanged. Endpoint
derivatives exist from the C1 path and the endpoint exceptional event has
probability zero. Thus (2) uses ONLY the exact force-feature path, not a
hidden x coordinate or an unobserved Brownian increment.

Substituting (1) yields

    H_h=-A int_0^h cos(z)sin(z-theta)dt
                   +sqrt(2gamma_d tau)int_0^h cos(z)dW.

For theta=+pi/2 the drift is +A cos^2(z); for theta=-pi/2 it is
-A cos^2(z). Hence

    E_+ H_h=+A h r(c)/c,
    E_- H_h=-A h r(c)/c,
    c=A/(n tau),        r(c)=I1(c)/I0(c).                 (3)

The identity E cos^2(z)=r(c)/c follows from Gibbs integration by parts;
equivalently it is the circular-location Fisher identity already proved
in the companion note. Since r(c)/c->1/2, the expectation gap tends to A h.

For 0<c<=1, I1(c)>=c/2 by its positive series and I0(c)<=exp(c), so
r(c)/c>=1/(2e). The gap is at least A h/e whenever n>=A/tau.

Both second moments satisfy

    E_+/- H_h^2 <= 2A^2h^2+4gamma_d tau h.                (4)

This is just the bounded drift in (3), Ito isometry, and
(a+b)^2<=2a^2+2b^2. The same score/moment TV inequality used in the root's
thermal separation therefore gives

    TV(Law_+[f_0:h],Law_-[f_0:h])
       >= A^2 h/[8e^2(A^2h+2gamma_d tau)]                (5)

for all n>=A/tau. The lower bound is positive independently of n. Therefore
the static O(n^-2) information bound does NOT control a full dynamic trial
with this exact force-feature observation. A fixed number of such ideal
trials can have a fixed distinguishing advantage.

## 4. What resource changed

The statistic differentiates an exact continuous feature path and resolves
its n-dependent oscillations. It is not a finite-noise finite-bandwidth
measurement protocol. Formula (2) involves cancellation and a quotient near
feature extrema; instrument errors, sampling cadence and smoothing must be
analyzed before treating it as an available operation.

There is no contradiction with the Gaussian-sensor transcript bounds in
FINITE_RESOLUTION_TRANSCRIPT_THEOREMS.md: those bounds attach explicit
spatial gain, noise, bandwidth and count to a specified receiver-side
interface, and their feedback controls do not act on x/v. The present
reference potential DOES act on the hidden x/v driver and the new score
uses an exact additional force-feature record. Nor is there a contradiction
with (6)--(8) of the companion phase note: those statements explicitly
restrict each trial to a static prepared-state readout.

An equally informed conventional route can use ordinary kinetic force
inference from this high-resolution path and its derivatives. The score
is an explicit instance of that route. Its value here is as a decisive
scope correction: bounded actuator force alone does not bound dynamic
information, and a small mean intervention response need not mean the
complete controlled experiment is statistically weak.
