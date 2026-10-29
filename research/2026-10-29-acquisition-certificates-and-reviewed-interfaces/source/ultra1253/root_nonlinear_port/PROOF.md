# A distributed nonlinear pulse as a hidden-coordinate reference

29 October2026. Root initial attack, independently developed before learning
of the closely related Astra N596/N597 contraction. Governing prior was
then read before selecting sustained depth. Mathematical/code challenge
pending. This is a CLASSICAL complex-amplitude model, not an exact quantum
Kerr expectation equation, a built optical instrument or a novelty claim.

## 1. Question and actual access

An unknown real symmetric n-by-n matrix H controls a coherent wave network:

    dot x = -i H x -i kappa(t) (|x_j|^2 x_j)_j + e_0 u(t),
    y(t)=e_0^T x(t).

The complex input u and complex phase-referenced output y use ONE port.
Known scalar kappa can be switched globally between0 and a known nonzero
value; the nonlinearity acts at EVERY physical site. H is NOT switched off
during its pulse. The number n, a spectral band avoiding sampling alias,
and finite source stability/visibility/measurement qualifications are needed.
Repeatable zero-field reset is a real resource; a uniformly damped reset
mode would pay time log(R/error)/damping in this model, rather than granting
an unobserved exact reset. The executed diagnostic idealizes reset to zero.

Complete success in this model would recover the hidden interaction matrix
up to inevitable physical-site signed permutation fixing the port. This
could replace individually addressed interior shunts with a distributed
basis-referencing actuator. Whether that actuator is easier to acquire is
the technological question; its existence is not established here.

## 2. Exact ambiguity of the easier controls

For any orthogonal Q with Q e_0=e_0, H and Q H Q^T have identical linear
one-port responses for EVERY waveform and observation time. Adding arbitrary
nonlinearity/control ONLY at the port does not break this equivalence: its
force has the form e_0 Phi(y,u,port-state), which is Q-equivariant. The
entire controlled trajectory transforms as x->Qx, with unchanged output.
Likewise the isotropic force ||x||^2 x is Q-equivariant. These conclusions
are exact model identities, not low-amplitude or finite-sampling statements.

Thus an easy accessible-port Kerr element cannot supply the proposed
interior coordinate reference. A dense symmetric source class contains
many Q-related matrices which are not signed-permutation equivalent.
Restricted known chains/graphs can already be determined by ordinary
linear gateway methods; that different source promise is granted to them.

## 3. Calibrate modes through the port, without learning hidden coordinates

Assume H has simple eigenvalues lambda_k and e_0 is cyclic. Choose column
signs in H=V Lambda V^T so a_k=V_(0,k)>0. A port impulse gives

    r(t)=sum_k a_k^2 exp(-i lambda_k t).

The ordinary finite Hankel/Prony pencil on2n samples determines its simple
unaliased poles and weights in exact arithmetic. Finite-noise recovery
depends on the Hankel singular-value gap, pole separation and minimum
weight. Those are not certified by knowing n alone. The native diagnostic
actually acquires them from simulated PORT samples; it does not give the
learner lambda,a or V. A physical short-port pulse additionally needs its
edge/amplitude bias budget. Near-dark or colliding modes remain failures.

For acquired lambda,a, arbitrary modal vector z can be prepared with ONLY
that port while kappa=0. Over duration P command

    u(s)=sum_l c_l exp[i lambda_l(P-s)],
    G_(k,l)=integral_0^P exp[-i(lambda_k-lambda_l)t]dt,
    c=G^-1 diag(a)^-1 z.

The modal state at P is exactly z. If distinct lambda are separated by
delta, |G_kl|<=2/delta for k!=l and G_kk=P. Hence P>=4(n-1)/delta gives
G>=P I/2 by Gershgorin, a concrete polynomial-time coherent preparation
interface when delta and a_min are warranted. Moreover

    integral |u|^2 <=2||diag(a)^-1 z||^2/P,
    sup|u|<=2sqrt(n)||diag(a)^-1 z||/P.

These are squared-amplitude/peak-drive bounds in the stated ODE units,
not a conversion into joules or total laboratory reset/control work.

After a pulse, kappa=0 readout gives y(t)=sum_k a_k z'_k exp(-i lambda_k t).
Finite matched Fourier integrals use the complex conjugate of the SAME
Gram G to recover z' (and therefore its identical conditioning bound).
Alternatively any finite nonsingular matrix O_(j,k)=a_k exp(-i lambda_k t_j)
does so. Its actual smallest singular value and quadrature/readout errors
must be paid. No internal state vector is measured by the instrument.

## 4. A finite pulse acquires a cubic map

Prepare REAL z, physical x=Vz, norm<=R. Compare a pulse of strength kappa
and duration t_p with its paired zero-kappa baseline under the SAME H.
Infer their modal endpoints from the one-port field, and define

    C_hat(z)= i(z'_kappa-z'_0)/(kappa t_p).

In the limit t_p->0 this is

    C(z)=V^T (Vz)^(componentwise3).

The limiting identity alone is not an experimental oracle. Here is a
finite-duration bound: norm is conserved during the undriven Kerr pulse;
N(x)=|x|^2x has Lipschitz constant<=3R^2 on that ball and norm<=R^3.
Duhamel and ||exp(-iHt)-I||<=||H||t give, for ||H||<=Lambda,

    ||C_hat(z)-C(z)||
       <= [2Lambda R^3+(3/2)|kappa|R^5]t_p.             (1)

A preparation-state error e_p adds at most3R^2 e_p (with the ball enlarged
to cover it). If each of n complex port readings has error<=eta, paired
readouts add at most2sqrt(n)||O^-1|| eta/(|kappa|t_p).
Spectral/phase/drive calibration enters those actual preparation/readout
errors and must also bound the known baseline. Making t_p small therefore
costs raw precision; it does not remove a fixed instrument floor. No
end-to-end physical confidence bound was acquired by the floating run.

## 5. O(n) vector probes, no ambient quartic-tensor oracle

For a real contraction vector g, form a matrix by columns

    M(g)e_l=[C(g+e_l)-C(g-e_l)-2C(e_l)]/6.

This is exact cubic polarization, with finite amplitudes; it requires3n
vector queries, each consisting of paired scalar-port experiments and
n readings (or n matched scalar integrals). Direct expansion gives

    M(g)=V^T diag[(Vg)_j^2] V.                           (2)

If those n diagonal values are distinct, its orthonormal eigenvectors
are precisely the physical coordinate rows of V, up to signed permutation.
The row a identifies the port. Therefore V Lambda V^T is acquired up to
that inevitable gauge. A Gaussian g gives distinct values almost surely
for every fixed V. A quantitative eigengap gamma is still a precision
resource; the run records it rather than assuming it is of order one.

If every cubic-vector query has error<=b, the matrix error is at most
2sqrt(n)b/3. Symmetrizing its real part cannot increase that bound. For
matrix error E<=gamma/4, elementary symmetric-eigenvector perturbation
gives aligned row error<=2sqrt(2)E/gamma, and hence, with exact lambda,

    ||H_hat-P H P^T||<=4Lambda sqrt(2n) E/gamma,          (3)

where P is a port-preserving signed permutation. Eigenvalue uncertainty
adds its operator bound. Neither exact controllability nor (2) makes
small gamma, tiny a_min, losses, extra modes or unknown cross nonlinearities
disappear. This is a finite-precision mathematical receiver conditional
on its explicit calibration/response-error budgets.

## 6. Actual native acquisition and controls

experiment.py separates a hidden forward instrument from a learner. The
instrument exposes ONLY scalar complex return samples. The learner obtains
spectral parameters via its Hankel pencil, computes drives, acquires paired
finite-pulse port records, constructs (2) and recovers H. Hidden matrices
and eigenvectors are used solely to generate model data and score the
allowed-gauge error, never to compute the learner's inverse or tensor.

The fixed six-node sources H and QHQ^T have simple frequencies -2.5,...,2.5,
with Q fixing the port but mixing interior physical coordinates. Prescribed
pulse durations are1e-3,1e-4,1e-5; no adaptive tuning or rerun occurred.
The computation took1.23396s after imports. Each source used113 protocol
calls and684 scalar complex readings, including controls, with703.72
preparation-time units and597.43 readout-time units before any physical
reset/repetition cost. Gram condition was1 and readout condition3.73205.

At t_p=1e-5 the two aligned operator errors were6.40e-8 and7.86e-10.
Their actual slice gaps were6.11e-5 and.00670; the first is already a
substantial error amplifier. Imaginary/antisymmetric finite-pulse components
are retained, not reported as zero. These are floating ODE diagnostics,
not outward numerical-error or physical noise certificates.

The matched control is decisive at the INFORMATION interface. Linear,
port-only nonlinear and isotropic nonlinear experiments agree for the two
sources to about1e-14. A fixed distributed pulse gives a raw complex port
difference4.57e-4. This supports the constructed change in access and its
exact equivariance proof; it is NOT superiority over equally informed
nonlinear fitting or tensor identification, which receive the same pulses.

## 7. Existing capital and the actual selection decision

After the first native computation, N596/N597 and the COMPLETE governing
s41_primitive source were acquired at Astra revision
d5366275f4886a027526b70997e75db2c19e4efa. They ALREADY use a cubic response
contraction to recover physical coordinates beyond linear port ambiguity.
N596's dissipative first-order model has a severe Cauchy inversion barrier;
N597's damped oscillator has an explicit resonance/residue scheme, strong
gap/overlap/damping/hidden-weight premises and an unresolved s41/h16
uniform-stability disagreement. Those source results are not promoted
to accepted premises of this construction. The known generic mechanism
must not be announced as newly discovered here.

The changed interface here is globally switchable known onsite Kerr,
complex coherent/Hermitian dynamics and port-prepared modal probes.
These avoid a high-opposite-frequency residue contraction and permit the
explicit finite polarization(2), but acquire a DIFFERENT powerful actuator
and coherent-time/calibration obligations. The first-order/damped-oscillator
source does not supply that actuator, and this construction does not solve
its original acquisition problem by relabeling it.

The primary Usevich--Dreesen--Ishteva arXiv2109.09584v1 Sections2--3 already
connects special nonlinear Jacobian probes to low-rank Volterra/parallel
Wiener--Hammerstein factor recovery. Its stated FIR-block identification
is not this physical H, but is a strong constructive incumbent. Ordinary
global nonlinear output-error fitting and this same symmetric contraction
are available to an equally informed method. Burgarth--Maruyama0903.0612
already pays limited-gateway tomography under known infecting topology.
Astra N1037 uses individually calibrated internal shunts; N1182 reconstructs
quartics with KNOWN K from thermal variances. Their governing exact source
passages were read; neither has the same input contract.

This initial attack constructs and executes the complete MODEL access
chain rather than supplying an H3/tensor/state oracle. It does not yet
justify prioritizing this route over the stronger current assets: no
specimen with a calibrated distributed global actuator, useful coherent
duration and required raw precision has been acquired; a port-only actuator
provably fails; generic tensor nonlinear identification is existing
machinery; and the finite example has no matched nonlinear-cost advantage.
The next decisive task is an actually feasible basis-referencing actuator
or a robust different mechanism, not a larger noiseless network plot.
Historical priority/practical advantage UNKNOWN; mission100/100 NOT_ACHIEVED.
