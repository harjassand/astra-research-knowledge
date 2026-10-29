# A controlled macroscopic action despite frozen microscopic kinetics

29 October 2026. Root's stronger receiving construction, continuation 7.
The exact reviewed status and dependencies are recorded at the end.
The classical SSEP action and its large-deviation machinery
are not new. The issue here is their validity for the actual selectively
actuated family, with arbitrary bounded nonlocal frozen amplitudes.

## 1. Actual family and theorem

Use the physical family and initial-law scope of
`RARE_TRANSPORT_WITHOUT_KINETIC_IDENTIFICATION.md`: an N-site ring,
native rates r_i=(s/2)(1+alpha_i(eta,z)cos(theta_i)), own-swap invariance,
|alpha_i|<=a<1, arbitrary frozen z, and actual independent phase
diffusion of physical strength kappa_N tending to infinity. Observe
physical time N^2 T. Independent local sign flips with gamma_N tending
to infinity are a separately supplied alternative. The deterministic
initial occupancies have empirical profile m dx, 0<m<1; phases/signs
and the old retained record can be arbitrary within the stated fresh
future-noise interface.

In a conditional retained-record assertion the complete future
native-and-actuator generator must remain the declared law. Actuator
freshness alone does not suffice if future native innovations have
already been exposed in that record. Visible-history probabilities
integrate over actual future innovations; retaining their records does
not supply a conditional theorem for arbitrary rare future records.

The assertion is for each deterministic visible initial sequence
approaching the flat profile. The hidden-context bounds are uniform;
uniformity across a family of initial visible sequences additionally
needs a common vanishing initial-profile error modulus.

Define the empirical density and integrated spatial current measure

    pi_t^N=(1/N)sum_i eta_i(t) delta_(i/N),
    W_t^N=(1/N^2)sum_i J_i^N(t) delta_(i/N).              (1)

Both start with W_0=0; the density initial limit is m dx. For a precise
Polish ambient space, embed the measures in H^(-3) of the circle and
use D([0,T],H^(-3) x H^(-3)) with its Skorokhod J1 topology. On any
uniform total-variation ball this norm topology agrees with weak
measure convergence: smooth Fourier tests determine the low modes,
and the uniformly bounded Fourier tail is summable in H^(-3). The
LDP has continuous limiting support. Equivalently linearly interpolate between successive native
jump times: at any time the weak density discrepancy is at most 2/N
and the current discrepancy at most 1/N^2 in total variation. This
is a mathematical representation, not a physical operation.

The receiving theorem is a speed-N LDP for (pi^N,W^N) with
good rate function

    I_T(rho,W)=(1/(2s))int_0^T int_circle
           [j+(s/2)partial_x rho]^2/[rho(1-rho)] dx dt, (2)

when W_t(dx)=int_0^t j(u,x)du dx,

    partial_t rho+partial_x j=0, rho(0,x)=m,
    0<=rho<=1, W_0=0,                                  (3)

with the finite-energy interpretation established below. Otherwise
the rate is infinite. At rho=0 or 1, a nonzero numerator costs infinity
and 0/0 is interpreted as zero. The equivalent variational definition
in Section 4 is primary, so no differentiability is silently assumed.

This says that any admitted bounded hidden kinetic context has the
same logarithmic probability cost for a macroscopic transport history
after the supplied control. It does not identify microscopic path
laws, reset z, supply the actuation ports, or prove a practical speedup.

## 2. The inputs and the exact occupation bridge

The phase proof supplies, under the actual law and every fixed smooth
weak current comparison field E(t,x), superexponential replacement of

    int sum_i E(t,i/N) alpha_i delta_i cos(theta_i) dt,  (4)

and of the phase-dependent quadratic compensator. The native rate
has c_min=s(1-a)/2>0. For every phase-independent potential U_N,
the Feynman--Kac numerical range is bounded by

    sup_(||f||=1){bN<U_N,f^2>-N^2 D_native(f)
                                      -N^2 kappa_N D_theta(f)}
    <=sup_(||g||=1){bN<U_N,g^2>-c_min N^2 D_ex(g)}.      (5)

For the last inequality apply the visible variational bound to
f(.,theta) at each fixed theta and integrate its squared norm. This
does not suppose the evolving visible and phase laws factorize.
The right side is exactly an ordinary SSEP occupation problem with a
fixed positive rate. Consequently the standard one-/two-block
variational estimate transfers, with the actual order of limits:

    lim_(epsilon down to 0) limsup_N (1/N)log P(
      int_0^T (1/N)sum_i |Av_(epsilon N)[eta_j eta_(j+1)](i)
                       -[Av_(epsilon N)eta](i)^2| dt>delta)
        =-infinity.                                   (6)

Integer symmetric blocks may be used; their boundary discrepancies
vanish in the indicated limits. Smooth bounded weights multiply the
same estimate, and summation by parts/discrete convolution moves the
block average onto the weight with an O(epsilon) error. Thus (6)
replaces weighted (eta_i-eta_(i+1))^2 by twice the local mobility
chi(rho)=rho(1-rho), first at block scale epsilon and then epsilon=0.

The ordinary reversible proof of (6) is Theorem 3.2 in Bertini et al.,
math/0512394, whose source proof uses the exchange Dirichlet form.
Equation (5) is the specific interface needed to use that established
result here. A statement that its path theorem applies directly to
the nonlocal joint generator would be incorrect. The occupation
observable, variational form and initial-law transfer are the parts
that are being transferred.

Arbitrary initial phases acquire an exp(hN) joint density ceiling
through the actual active initial layer; the bounded occupation
integral in that layer is negligible. This factor is used only for
superexponential estimates. The comparison-likelihood L2 identity
transfers (6) to every fixed weak field. It supplies the same inputs
to the ordinary martingale proof of

    partial_t rho=(s/2)rho_xx-partial_x[s chi(rho)E],
    j=-(s/2)rho_x+s chi(rho)E.                          (7)

`record_geometry/TILTED_HYDRODYNAMIC_RECEIVER.md` reconstructs that
receiving step. Only smooth bounded deterministic fields E are used in lower
bounds, and they are mathematical comparison measures. The theorem
does not assume a physical actuator for E.

## 3. Conservation closes current compact containment

At every finite N, exactly,

    eta_i(t)-eta_i(0)=J_(i-1)(t)-J_i(t).                (8)

Write w_i=J_i/N and Q_N=N^-1 sum_i w_i. Any two w_i differ by at most
one, by summing (8) along an arc of at most N sites. Therefore

    ||W_t^N||_TV=(1/N)sum_i |w_i(t)|<=|Q_N(t)|+1.       (9)

This deterministic bound is the useful one-dimensional connection:
the spatial current's total variation cannot grow independently of
its circulation. It is not a claim that microscopic current counters
are bounded.

For a smooth density test G, its martingale has jumps O(N^-2) and
quadratic variation at most C_G T/N. Its drift is a uniformly bounded
discrete heat term plus the integrated phase residual (4) with
E_i=N[G((i+1)/N)-G(i/N)]. For a smooth current test H, its martingale
has the same jump and bracket orders. Its unmodulated drift is

    (s/2)sum_i H_i(eta_i-eta_(i+1))
       =(s/2)sum_i eta_i(H_i-H_(i-1)),                  (10)

which is uniformly bounded, and its remaining drift is (4).

An exponential martingale and Doob's inequality imply, for every
fixed b>0, over a time interval of length h,

    P(sup|M_(t+u)-M_t|>delta, 0<=u<=h)
       <=2 exp[-bN delta+C b^2 N h exp(Cb/N)].           (11)

Use a deterministic interval grid and the superexponential bound on
the supremum of each accumulated phase residual. Let N grow, then
h decrease, then b increase. For each smooth test this proves

    lim_(h down to 0) limsup_N N^-1 log P(
          sup_(|t-u|<=h)|test_t-test_u|>delta)=-infinity.
                                                               (12)

The same argument with H=1 gives exponential tightness of sup_t|Q_N|.
Equation (9) gives compact containment of W in weak signed measures;
the density already takes values in a compact set of positive
measures of mass at most one. These are compact sets in H^(-3).
A countable separating family of smooth
tests, (12), and the standard exponential Arzela--Ascoli diagonal
argument give exponential continuous tightness of the pair. The
deterministic interpolation errors above remove the finite-N jumps.
The proof claims continuous *limiting* support, not that finite
uninterpolated jump paths are literally continuous with high probability.

## 4. The upper functional and identification of the action

For a smooth deterministic field E(t,x), the actual current
exponential martingale has logarithm

    log Z_E=N[<W_T^N,E_T>-int_0^T <W_t^N,partial_t E_t>dt]
             -int_0^T N^2 sum_i r_i(e^(E_i delta_i/N)-1)dt.
                                                               (13)

Discrete summation by parts, the phase replacement and (6) identify
the limiting normalized log likelihood with

    J_E(rho,W)=<W_T,E_T>-int <W_t,partial_t E_t>dt
       -(s/2)int rho partial_x E dxdt
       -(s/2)int chi(rho) E^2 dxdt.                    (14)

At the upper-bound step replace rho by its spatial block smoothing
only in the nonlinear term. That functional is continuous in the
weak path topology. For each given path, its smoothed values tend
to (14): rho is bounded in [0,1], and spatial approximation of the
identity converges in space-time L1. The occupation bad-event exponent
can be made arbitrarily large by decreasing the block scale after
taking the volume limsup. It is not necessary to assert that the
occupation error is superexponential at each fixed macroscopic scale.

Because E Z_E=1, a neighborhood of a specified path has upper exponent
at most -J_E there. Optimize over E. Finite covers of compact sets,
then exponential tightness, give the closed-set LDP upper bound with

    I(rho,W)=sup_(smooth E) J_E(rho,W),                 (15)

subject to the limiting continuity and initial conditions (3). Paths
violating those conditions have neighborhoods eventually impossible,
by the exact finite continuity relation and deterministic initial
profile. The support density condition follows from 0<=eta_i<=1.

Here is the finite-energy identification needed both for (2) and the
lower approximation. Write D=s/2 and define the distribution

    A=partial_t W+D partial_x rho.                     (16)

If (15) is finite, weighted Hilbert-space duality gives a function
A in L2(dxdt), vanishing where chi(rho)=0, with

    I=(1/(2s))int A^2/chi(rho).                         (17)

Indeed the linear part of (14) is bounded in the norm
[int chi(rho)E^2]^(1/2); optimizing scalar multiples of E supplies
that bound and the Riesz representation. Since chi<=1/4, weighted
finite energy implies ordinary L2 energy for A.

Continuity then becomes the forced heat equation

    partial_t rho=D rho_xx-partial_x A, rho(0)=m.        (18)

Its weak L2 energy estimate, obtained by testing smooth regularizations
with rho-m, is

    (1/2)||rho_t-m||_2^2+(D/2)int_0^t||rho_x||_2^2 du
        <=(1/(2D))int_0^t||A||_2^2 du.                 (19)

Thus rho has a square-integrable spatial weak derivative and
j=A-D rho_x belongs to L2. Since W_0=0, (16) gives
W_t=int_0^t j du. This proves the displayed representation (2)
without assuming it in advance.

The integral A^2/chi(rho) is jointly convex and lower semicontinuous
in (rho,A), with its stated boundary convention. To see convexity,
use concavity of chi and weighted Cauchy--Schwarz. Uniform action
bounds give L2 bounds for A, rho_x and j by (17)--(19); continuity
and these bounds give compactness in the weak path topology.
Weak lower semicontinuity of the convex integral establishes that
(15) is a good rate function. This also justifies optimizing the
finite-cover upper bound over compact action levels.

## 5. Smooth-path lower bounds use actual comparison laws

Let rho,j be smooth, with rho bounded away from 0 and 1, satisfying
(3), and define the deterministic comparison field

    E=[j+(s/2)rho_x]/[s chi(rho)].                      (20)

It is smooth and bounded. Under the comparison rates
r_i exp(E(t,i/N)delta_i/N), the reconstructed weak-tilt hydrodynamic
law (7), uniqueness of its bounded parabolic solution, occupation
replacement and vanishing current martingale imply

    (pi^N,W^N) -> (rho,W) in probability.               (21)

The normalized likelihood (13) converges in probability to

    J_E(rho,W)=(s/2)int chi(rho)E^2=I(rho,W).           (22)

For an open neighborhood O of this path, restrict
P(O)=E^E[Z_E^-1 1_O] to the event
|N^-1log Z_E-I|<epsilon, which together with O has comparison
probability tending to one. It gives the lower exponent -I-epsilon.
Let epsilon decrease. This lower bound starts from the actual initial
visible configuration and arbitrary initial phase law. The active
initial layer is used only inside replacement/hydrodynamic estimates;
it is not an exp(hN) transfer of a finite-action probability.

## 6. Every finite-action path admits a cost-preserving smooth approximation

The flat initial profile makes a direct construction possible. Take
a finite-action pair rho,j with A=j+D rho_x. For delta in (0,1), set

    rho^delta=(1-delta)rho+delta m,
    j^delta=(1-delta)j, A^delta=(1-delta)A.              (23)

This preserves continuity and the initial profile, keeps the density
strictly inside (0,1), and has cost at most (1-delta)I. The last fact
follows from chi((1-delta)rho+delta m)>=(1-delta)chi(rho).

Convolve rho^delta,j^delta,A^delta spatially with a smooth nonnegative
approximation of the identity on the circle. It preserves continuity,
the constant initial density, and positivity. Jensen's inequality
for A^2/chi(rho) does not increase the cost.

Extend the resulting density as m and current as zero to negative
times. Their continuity equation holds distributionally across t=0
because the density trace there is m. Convolve in time with a smooth
probability kernel supported on [epsilon,2epsilon], using past values:

    rho^(delta,epsilon)(t)=int k_epsilon(u)rho^delta(t-u)du,
    j^(delta,epsilon)(t)=int k_epsilon(u)j^delta(t-u)du.  (24)

These paths are exactly flat with zero current near time zero, smooth
on [0,T], and uniformly positive for fixed delta. All operations are
linear on the continuity equation. The associated A is convolved in
the same way. Jensen and the zero cost of the negative-time extension
show that their cost on [0,T] is at most the pre-convolution cost.
There is no need to invent an endpoint extension beyond T, since only
past values enter (24).

Spatial and time convolutions tend to the identity in the indicated
L2 energies. The integrated currents converge uniformly in time in
L2; the densities converge in the weak continuous path topology by
(18)--(19). Let the smoothing scales decrease and then delta decrease.
Lower semicontinuity and the preceding upper bound show convergence
of costs to I. Hence every finite-action path in an open set can be
approximated inside that set by paths to which Section 5 applies.
This proves the open-set lower bound for all finite-action paths.

Sections 2--6, with the explicit classical occupation and reconstructed
weak-tilt inputs, close the density/current path LDP rather than only
a conditional compensator calculation. The source of the additional
physical uniformity is the independent phase/sign estimate (4), whose
constant does not grow with hidden context complexity or its range.

## 7. Actual reviews, corrections and receiving extensions

The existing record-geometry role accepted the proof after explicitly
reconstructing its occupation and tilted-hydrodynamic input. The
existing physical-mechanism role separately challenged current
tightness, the finite-energy argument, smooth approximation and
physical scope. Their reviews and exact input snapshots are retained
in `record_geometry/RECEIVING_ACTION_REVIEW.md` and
`physical_mechanism/receiving_review/HOSTILE_MACRO_ACTION_REVIEW.md`.
These are internal mathematical reviews, not external peer review or
an apparatus validation.

The final receiving dependency is
`record_geometry/TILTED_HYDRODYNAMIC_RECEIVER.md`, SHA-256
`ae8dbab399e9378a8ce8d2e8a87bac07a5f4b4c409db5329db50274e01f660f5`.
Its earlier reviewed text is preserved; the current version corrects
three displayed plus signs and clarifies the complete conditional
future generator. Root corrected the initial-profile quantifier and
the same conditional-generator scope in the present receiving files.
Final version receipts pin those changes separately.

`INDEPENDENT_CONTROL_OPENS_ZERO_RATE_GATES.md` proves the extension
to amplitude one by joint-form coercivity. The grouped operation in
`CONTROL_GRANULARITY_AND_BANDWIDTH.md` provides the same action when
max_g n_g/gamma_g tends to zero, including a sufficiently fast common
clock. Those are explicit receiving extensions; arbitrary reciprocal
implementation errors retain their separately stated positive-rate
scope. The full common-clock spatial action in the slower regime is
still a separate, unproved candidate.
