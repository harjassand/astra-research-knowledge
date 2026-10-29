# Receiving review of the actual selective-averaging governing proof

29 October 2026. Independent review by the existing record-geometry role.
No new agent, tests, predecessor edits or external review were used.

## Reviewed actual inputs

Root document:

    new_science/continuation5_20261029/GAP_FREE_SELECTIVE_AVERAGING.md
    SHA256 9df1e444eefdf5223a97e48cbbe5145339d4b00ae6521bd7f9208482e7b5eeae

An exact snapshot is saved beside this review as
REVIEWED_GAP_FREE_SELECTIVE_AVERAGING_9df1e444eefd.md.

Companion continuous-rate acquisition interval checked:

    record_geometry/LOCAL_MOBILITY_MOMENT_ACQUISITION.md, Section8
    SHA256 5ea1dd67a4f53681153eb70f49b3af627022addac129e7c54793f2aba94a33e0

This acceptance is attached to those actual contents. It does not review
the forthcoming physical receiver or finite-acquisition integration.

## Verdict

**Accepted at the stated scope.** I found no substantive mathematical
mismatch or required correction in the governing proof. Its compressed
constant, density/observable orientation, restricted circle extension
and TV receiving statements are supported. The supplied hidden bath,
the projected initial-law interface and record qualifications remain
load-bearing conditions.

## 1. Compressed second-order constant

The hidden energy identity correctly gives

    Ev <= -J <= eta sqrt(Eu Ev),

including the zero-energy cases without division by zero. The full
dissipation inequality completes the square to yield

    (1-eta^2) Eu <= ||x||^2/2.

Consequently Ev<=eta^2||x||^2/[2(1-eta^2)]. Testing the visible error
against the backward visible evolution contributes an additional factor
eta and an integrated energy at most ||y||^2/2. The stated constant

    eta^2/[2 sqrt(1-eta^2)]

is therefore correct. No spectral gap of a, C or A was introduced in
this calculation. A component of b along ker(C) is already excluded
by the relative form premise. The bound controls the compressed
operator with visible input; it is not silently promoted to a full
microscopic operator comparison.

## 2. Nonautonomous orientation

For the defined forward density evolution U_a(t,s),

    partial_s U_a(t,s)=U_a(t,s) a_s.

Since each a_s is self-adjoint, w(s)=U_a(t,s)*y obeys
w'=a_s w and w(t)=y. Its energy integral equals
(||y||^2-||w(0)||^2)/2. This confirms the sign and operator ordering
in Section3. No commutation of generators at different times is needed.

The adjoint of the density evolution is the observable evolution.
Orthogonal projection commutes with taking adjoints, so the norm
comparison transfers exactly as stated. Conditioning on a history of
state-dependent controls would not create this prescribed evolution;
the root document explicitly excludes that inference.

## 3. The continuous circle extension actually asserted

For A=kappa H+B with H the nonnegative hidden Laplacian and B bounded,
self-adjoint and nonnegative, the bounded perturbation is self-adjoint
on D(H) and has the same closed form domain D(H^(1/2)). The stated
commutation/HP=0 conditions put visible initial data in D(H), keep the
P/Q decomposition compatible with that domain, and make a,b bounded.
The regular-data energy proof is therefore legitimate in this receiver.

Finite Fourier spaces form a core for the periodic Laplacian form.
Compressing the bounded native form preserves nonnegativity and the
assumed cross-form inequality on those spaces. Their Galerkin form
approximation gives the asserted strong semigroup limit. The uniform
norm estimate passes to each fixed visible input in that limit.

Positive piecewise-constant multiples of the same H and finitely many
bounded native modes share this domain. The finite concatenated
forward/backward energy proof is valid. The draft appropriately avoids
claiming this for arbitrary unbounded nonautonomous generators.

## 4. Selective bath and genuine receiving laws

Section5 uses C>=kappa H only in the energy seminorm. It therefore
allows a large kernel of H when b has no component in that kernel and
the inverse-energy bound is finite. This is the correct condition;
there is no hidden full-gap assumption in equations (7)-(8).

With conditional expectation P onto all visible functions, the
compressed physical kernel is positive and stochastic. The assumed
visible generator a supplies the other positive law. For an actual
initial density g0(Y), both terminal visible densities differ by the
compressed density operator applied to g0-1. L1<=L2 proves the factor
1/2 in equation (10). Its useful version requires finite ||g0-1||_2;
without it one retains the trivial TV bound. This is not a claim for
arbitrary microscopic initial preparations.

For equation (11), centered initial/terminal readout indicators give
each joint-probability error at most delta_mem times the product of
their standard deviations. Summing and using
sum sqrt(p(1-p))<=sqrt(k-1) yields the stated
delta_mem sqrt((a0-1)(b0-1))/2. The equilibrium start, finite readout
alphabets and two-time objective are correctly retained. No growing
trajectory or arbitrary retained calibration transcript is covered by
that cardinality calculation.

The separate relative kinetic calibration error is correctly referenced
to the **true** a form and preserves the same equilibrium. Adding its
operator bound to delta_mem is legitimate. Changing equilibrium
ratios is explicitly excluded from that budget.

## 5. Continuous-rate interval: the harmonic mean has the right denominator

The companion supplier obtains a true-rate interval m in[L,U], L>0.
For a chosen fitted rate z in[L,U], the worst error measured relative
to the **true** rate is

    max_(m in[L,U]) |z/m-1|
       =max(z/L-1, 1-z/U).

Equalizing the two endpoint errors gives

    z=2LU/(L+U),
    worst relative error=(U-L)/(U+L).                 (1)

Thus the harmonic mean is the correct fit for a relative form bound
with the true generator on the right. The arithmetic midpoint would
instead equalize absolute endpoint deviations and gives a different,
larger worst relative error.

The supplier's earlier inequalities also check:

    alpha E g <= E lambda <= (alpha+Lambda)E g,
    Var(lambda) <= (alpha+Lambda)^4 Var(g)/alpha^2,

for g=lambda/(alpha+lambda) and 0<=lambda<=Lambda.
The second follows from the inverse map's Lipschitz constant on its
actual bounded interval. Dividing by the lower true mean yields the
stated variance-to-mean bound. Zero lower confidence mean correctly
falls back to the supplied cap rather than dividing by zero.

Each of the two resolvent calls must use its own fresh independent
clock, as required by the original acquisition interface and by the
supplier's fresh-call premise. Reusing a single duration would measure
a different second moment. Clock, sensor and execution biases remain
additional to sampling radii.

## Acceptance boundary

This is an internal mathematical receiving review of the pinned text.
It establishes neither historical novelty nor physical implementation.
The next physical-family and acquisition documents must separately
justify local factorization, actual bath access, conditioning after
calibration, initial preparations, finite selectors and timing costs.
