# A nonlinear Lyapunov operation inherits its principal linearization

B, 30 October 2026. This is a general obstruction to a proposed escape
from the ROOT26 local/global barrier, not a new quasiconvexity counterexample.
The energy below is already strongly polyconvex. No nonlinear PDE solution,
new model case or numerical trajectory is assumed or executed.

## 1. Literal operation class and theorem

On the normalized flat two-torus consider a local quasilinear rule

    G[u]=L11(u,Du)u_xx+2L12(u,Du)u_xy+L22(u,Du)u_yy+b(u,Du),          (1)

where the Lij are real2x2 output matrices, continuous near (u,A)=(0,0),
and b is locally Lipschitz there. They have no explicit spatial/time
dependence or hidden global state. Let L0 be the canonical triple
(L11(0,0),L12(0,0),L22(0,0)), and assume its Frobenius norm l>0.

Set the SAME already-accepted ROOT26 energy

    F(A)=(det A)^2+epsilon |A|^4, epsilon=2^-100.

**Theorem.** There are arbitrarily small smooth periodic fields u in
every prescribed finite C^r norm for which the instantaneous energy rate
under (1) is STRICTLY POSITIVE:

    D_G E_F(u)=-integral div DF(Du) dot G[u]>0.                       (2)

Consequently (1) cannot be a universal monotonicity proof for this F.
In particular no uniformly parabolic gradient-local rule smooth at zero
can rescue the all-constant-second-order heat mechanism. If a solution
exists through u with the standard energy-identity regularity, its actual
initial energy rate is (2). For merely continuous L, no classical PDE
existence theorem is asserted: the formal variational pairing (2) is
already well-defined, and every smooth-coefficient subclass is included.
Existence or long-time convergence need not be presumed to reject the
required universal dissipation identity.

This allows arbitrary continuous state/gradient dependence of the
principal matrices and arbitrary locally Lipschitz lower-order terms.
It does not cover a zero principal linearization, singular coefficients,
nonlocal/global inputs, extra state, higher-order operators, or fields
restricted away from a neighborhood of the zero gradient.

## 2. Why derivatives of L do not escape the argument

For smooth u and any smooth velocity v,

    d/dt integral F(Du)=integral DF(Du):Dv
                      =-integral div DF(Du) dot v.                  (3)

Thus no derivative of L occurs in (2). A bounded or even very rapidly
varying derivative of L near zero does not enter the estimate: continuity
of L itself is the needed gate. The constant vector b(0,0) contributes
zero, by periodicity, so only b(u,Du)-b(0,0) must be bounded.

The argument is a blow-up inheritance principle for homogeneous energies,
not an assertion that proximity of nonlinear trajectories is free.

## 3. Paid frozen path and uniform constants

Normalize L0/l. ROOT26's accepted twelve-probe theorem supplies one
finite Fourier solution w(s) of that CONSTANT system, for
0<=s<=t0=2^-40, with

    E_F(w(t0))-E_F(w(0))>2^-98.                                    (4)

The same literal proof supplies, uniformly over all normalized triples,

    |w|<30, |Dw|<=180, |D2w|_compatible<=960.                       (5)

There is no nonlinear evolution in this input. It is an imported exact
theorem, not a repeated producer run. Its full governing hashes are
bound in the frozen ROOT26 B foundation review.

For F above, ||F''(A)||op <=(3+12epsilon)|A|^2<4|A|^2. Since
|B1|+|B2|<=2|D2w|_compatible,

    |div DF(Dw)|<=8|Dw|^2 |D2w|_compatible <2^28.                   (6)

Let B be a supplied local Lipschitz constant of b and let omega(r) be a
supplied continuity modulus, in the triple Frobenius norm, satisfying

    ||L(v,A)-L0|| <=omega(|v|+|A|), omega(r)->0.                    (7)

For the theorem alone such bounds exist locally; claiming an effective
counterfield requires actually supplying/acquiring B and omega. No free
coefficient/continuity oracle is asserted.

## 4. Amplitude and spatial scales separate the terms

For an integer k>=1 and amplitude delta>0, use the trial field

    u_(delta,k,s)(x)=(delta/k) w(s,kx).                             (8)

Periodicity makes spatial averaging at kx exactly the same averaging.
Its gradient is delta Dw and its compatible Hessian is delta k D2w.
Homogeneity of F gives div DF(Du)=delta^3 k div DF(Dw). The frozen
principal contribution in (2), divided by delta^4 k^2, is therefore

    l d/ds E_F(w(s)).                                              (9)

The principal-coefficient error is bounded in absolute value by

    2^28 *1920 *omega(210delta) <2^39 omega(210delta),               (10)

because the factor2 on u_xy costs at most2 times the compatible Hessian
norm. The lower-order error after the same division is at most

    2^28 B(30/k^2+180/k) <2^36 B/k.                                (11)

The time average of (9) exceeds l*2^-58 by (4). First choose a FINITE
integer k>2^96 B/l. Then choose delta small enough that all inputs lie
in the local coefficient neighborhood and

    omega(210delta)<l*2^-100.                                     (12)

The sum of (10),(11) is less than l*(2^-61+2^-60)<l*2^-59, uniformly
in s. Averaging (2)/(delta^4 k^2) over0<=s<=t0 is consequently positive,
so at least one of the actual trial states (8) has positive rate (2).
No assumed sign of each individual frozen time derivative was used.

Finally, k is fixed before delta shrinks. All Fourier modes of w are in
[-4,4]^2, hence for each finite r the C^r norm of (8) is at most a known
constant times delta k^(r-1). Further shrinking delta gives an arbitrarily
C^r-small counterfield without changing any preceding estimate.

These deliberately large bounds prove the quantifiers. They are not an
economical physical counter-preparation or a new search algorithm. For
the common scalar-heat linearization L0=(aI,0,aI), the already-acquired
rational STATIC_CURRENT witness supplies a single explicit time-state
instead of (4)'s averaged-time selection, without a new dynamics run.

## 4a. A literal finite counterfield for scalar heat linearizations

If L0=(aI,0,aI), a>0, no unknown positive time in(4) must be located.
Use the already-acquired rational static state w_star from ROOT26's
STATIC_CURRENT.md, with exp(-t)=7/8. Its exact heat energy rate exceeds
1/64: the determinant contribution is93530955/4294967296>1/48, while
the absolute norm-fourth contribution is<10 and is multiplied by2^-100.
The same explicit Fourier state has

    |w_star|<4, |Dw_star|<12, |D2w_star|_compatible<=32,
    |div DF(Dw_star)|<2^16.

Thus the SINGLE rational-trig field u=(delta/k)w_star(kx) works whenever

    integer k>2^28 B/a,
    omega(16delta)<a*2^-30,

and delta keeps all inputs in the coefficient neighborhood. The lower
error is<2^20 B/k<a/256 and the principal error is<2^22omega<a/256.
The normalized positive rate remains>a/128. These inequalities can be
satisfied by rational delta from a supplied effective modulus. They
describe the actual counterfield, not only a nonconstructive nonlinear
trajectory limit. No new static-moment or dynamics run is required.

## 5. The reusable principle is not limited to quartics

For any C2 homogeneous energy of degree p>1, the same construction has
principal energy rate delta^p k^2. Principal coefficient perturbations
remain o(delta^p k^2), and Lipschitz lower-order terms cost at most
O(delta^p k). Therefore any nondissipative principal frozen flow witnessed
at a smooth field passes to its nonlinear relatives by amplitude and
frequency scaling. One needs the actual frozen-flow counterfield; the
principle does not manufacture one or turn rank-one positivity into it.

For nonhomogeneous energies the first nonzero homogeneous tangent term,
if its expansion and remainder are warranted, is the relevant object.
A quadratic regularizer can change this local argument. No claim about
all nonlinear Lyapunov functions or all regularized energies is made.

## 6. Consequence for the next operation

The obvious next experiment, replacing constant diffusion matrices by
smooth learned or optimized functions of Du while keeping a nonzero
small-gradient diffusion, cannot bridge the ROOT26 gap for this F. The
entire continuum of such coefficient functions is rejected analytically;
there is no need to enlarge an SDP dictionary or fit more source cases.

In particular consider the ordinary viscosity-regularized variational
flow G[u]=div DF(Du)+nu Delta u with any FIXED nu>0. Quartic homogeneity
makes F''(0)=0, so its principal linearization is nu times heat. The
explicit Section4a counterfield therefore proves that this regularization
cannot retain monotonicity of the ORIGINAL E_F, however small nu is.
It does dissipate E_F+(nu/2)integral|Du|^2, which is a different Lyapunov
functional. There is an especially short exact counterfamily here: with
the frozen w_star from Section4a and u=delta w_star, let
e=D_heat E_F(w_star)>1/64 and J=integral|div DF(Dw_star)|^2<2^32. Then

    D_G E_F(delta w_star)=nu delta^4 e-delta^6 J.

Any positive delta with delta^2<=nu*2^-39 gives rate>nu delta^4/128.
No new moment computation or parameter case is needed for this bound.
Removing nu afterward would require actually paid uniform
convergence/compactness and limit interchange; global nonlinear descent
has not been supplied by writing a strictly parabolic regularization.

A genuinely different operation must change a premise: a degenerate or
singular small-gradient principal rule, a restricted invertible-gradient
domain, a nonlocal/enlarged-state dynamics, or an additional proof resource
such as the already available polyconvex decomposition. GEOMETRIC_ESCAPE
classifies the scalar isotropic rank-one tangency route and compares it
with an actual established singular geometric diffusion. It does NOT
assume that such a diffusion dissipates the desired non-PC energy.
