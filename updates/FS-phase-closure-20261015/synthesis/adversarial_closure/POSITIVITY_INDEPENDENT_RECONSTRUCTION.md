# Independent reconstruction: positive and unique fixed-direction amplitude minimizers

15 October 2026. Internal adversarial reconstruction. External correctness and historical novelty remain UNKNOWN. No original or repository file was changed.

Repository actually read: `/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-phase-closure-20261015`, HEAD `846f185763ed3a27310fad4ce9471ba324d1e5f4`. Incoming proof routes are `sources/phase_density/PHASE_DENSITY_COMPATIBILITY.md` Sections 2–5 and `CHECKPOINT.md`. Earlier finite-jet/strict-storage results remain distinct.

The root routed a proposed logarithmic-Caccioppoli positivity argument for independent attack. The proof below was reconstructed from the exact hypotheses and calculation, not accepted from worker agreement. No smoothness of the minimizer or uniform ellipticity is imported.

## 1. Exact theorem

Let Omega be a bounded connected Lipschitz domain in R2, or a connected flat two-dimensional torus. Let `n in C1` be a prescribed unit vector field with bounded `Dn`. Let `F:R^(m x 2)->R` be a C1 homogeneous quartic polynomial, rank-one convex, with

    mu=min{F(R):rank R=1, |R|=1}>0.

For a nonempty admissible class with `M>0`, minimize

    E(r)=integral F(D(rn)),
    r>=0, integral r^4=M,

and, on a bounded domain, prescribe a nonnegative trace `g`. The incoming direct-method proof supplies an attained minimizer `r in W1,4`.

Then:

1. Every such minimizer is strictly positive at every interior point, for its continuous Sobolev representative.
2. It satisfies a local multiplicative Harnack bound whose constant depends on the integrand, `mu`, `n,Dn`, its finite Lagrange multiplier and the balls, and is independent of `epsilon` in `r+epsilon`.
3. The nonnegative minimizer is unique for the specified mass and boundary data.
4. On the torus, it is bounded away from zero globally. The same is true on the closed bounded domain when the prescribed continuous trace has a strictly positive minimum.

The planar dimension is used through `4>2`. The same argument works in spatial dimensions below four with corresponding hypotheses. This proof does not establish the critical- or higher-dimensional version.

## 2. Attainment and density convexity: audited inputs

For fixed `x`, changing `z=grad r` changes `n tensor z+rDn` by a rank-one matrix. Thus

    L(x,r,z)=F(n tensor z+rDn)

is convex in `z`. Quartic growth and `F(n tensor z)>=mu|z|^4` give

    L(x,r,z)>=(mu/2)|z|^4-C r^4.

At fixed fourth mass this bounds a minimizing sequence in `W1,4`. Rellich compactness gives strong `L4` convergence, so the mass survives. Convexity in the gradient and strong convergence of amplitudes give the lower-semicontinuity needed for attainment. The negative `Cr^4` term is controlled by strong `L4`; global nonnegativity or quasiconvexity of `F` is unnecessary.

The correct density domain is `{rho>=0:rho^(1/4) in W1,4}`. It is convex: fourth-root interpolation of two nonnegative amplitudes is a Lipschitz composition, with its gradient controlled by the two amplitude gradients. The mass and fixed density trace `g^4` are affine constraints. It is unnecessary to assert an unconstrained standard Sobolev class for `rho`.

The proof below retains `mu>0` as an explicit hypothesis and does not rely on the incoming assertion that all non-polyconvex invariant-cone members have this property.

## 3. Removing the obstacle and deriving a legal multiplier

A homogeneous quartic polynomial obeys `F(-A)=F(A)`. For any signed Sobolev amplitude `h`,

    D(|h|n)=sign(h)D(hn) almost everywhere off {h=0}.

On `{h=0}`, its Sobolev gradient is zero almost everywhere, so the energy equality persists there. Therefore

    E(|h|)=E(h), integral |h|^4=integral h^4.

If `h` has the prescribed nonnegative trace `g`, so does `|h|`. Consequently a nonnegative minimizer is also a minimizer over all signed amplitudes with that trace and mass. This is the reason that no obstacle multiplier appears; it is not an assumption that the minimizer is already positive.

The energy is Frechet differentiable on the amplitude Sobolev space: quartic derivative growth bounds `DF(A)` by `C|A|^3`. The mass derivative is

    DC(r)[phi]=4 integral r^3 phi.

It is nonzero on the zero-trace variation space. Indeed `M>0` and continuity of the planar amplitude give a positive interior region; a compactly supported nonnegative test there makes the derivative positive. One can also obtain this directly from nontriviality in `L4` and approximation.

For completeness, choose one zero-trace test `psi` with nonzero mass derivative. For any other variation `phi`, an implicit scalar correction to `r+t phi+s(t)psi` preserves the mass. Signed competitors are allowed, and all preserve the trace. Differentiating minimality gives a finite scalar `lambda` such that

    integral [L_z(x,r,grad r).grad phi+L_r(x,r,grad r)phi]
       =4 lambda integral r^3 phi                         (E)

for every zero-trace Sobolev variation. The periodic version permits every periodic variation.

For nonzero Dirichlet trace, `phi=r` is generally illegal. Thus `lambda=E(r)/M` cannot be inferred in that case. On the torus, or for zero trace, testing with `r` is legal and Euler homogeneity gives that identity.

## 4. Logarithmic Caccioppoli estimate with all lower terms

Convexity in `z` gives

    L_z(x,r,z).z >= L(x,r,z)-L(x,r,0)
                   >= c|z|^4-Cr^4.                       (1)

Quartic derivative growth and bounded `Dn` give

    |L_z|+|L_r|<=C(|z|^3+r^3).                            (2)

The constants may absorb the fixed bounds for `n,Dn`. No Hessian lower bound or uniform ellipticity is assumed.

Fix a compactly supported smooth cutoff `eta>=0`. For each `epsilon>0`,

    phi=eta^4/(r+epsilon)^3

is a legal zero-trace `W1,4` test: the inverse-power composition and its derivative are bounded at that fixed epsilon. Its gradient is

    4eta^3 grad eta/(r+epsilon)^3
       -3eta^4 grad r/(r+epsilon)^4.

Insert this into (E), rearranging the negative derivative term to the left. With `z=grad r`,

    3 integral eta^4 L_z.z/(r+epsilon)^4
      =4 integral eta^3 L_z.grad eta/(r+epsilon)^3
       +integral eta^4 L_r/(r+epsilon)^3
       -4lambda integral eta^4 r^3/(r+epsilon)^3.

By (1), the left side controls `integral eta^4|grad log(r+epsilon)|^4` up to a bounded `integral eta^4` term. The cutoff term on the right is bounded by a constant times

    eta^3 |grad log(r+epsilon)|^3 |grad eta|
       +eta^3 |grad eta|.

The `L_r` term is bounded by `C eta^4(|grad log(r+epsilon)|^3+1)`, and the multiplier term by `4|lambda|eta^4`. Young's inequality absorbs the cubic logarithmic factors into a fixed fraction of the left side. Hence

    integral eta^4 |grad log(r+epsilon)|^4
       <= C integral (|grad eta|^4+eta^4),                 (3)

with a constant independent of epsilon. Boundedness of the multiplier, not its sign, is used.

## 5. Morrey, positivity, and the precise Harnack scope

On a ball compactly contained in Omega, choose a cutoff equal to one on a slightly smaller ball. Estimate (3) bounds the `L4` gradient of `log(r+epsilon)` there uniformly. The planar Morrey-Poincare oscillation bound uses only that gradient, so

    oscillation_B log(r+epsilon)<=C_B

uniformly in epsilon. Exponentiating and taking epsilon to zero gives

    sup_B r <= exp(C_B) inf_B r.                          (4)

The continuous representative makes this a pointwise assertion. If an interior point were zero, (4) would force a neighborhood to be zero. The zero set is therefore both open and closed relative to the connected domain. It cannot be the whole domain because `M>0`; hence it is empty.

This proof gives a local Harnack ratio for each fixed constrained critical point with finite multiplier. It does not give a uniform constant over arbitrary varying masses, boundary data, multipliers or direction fields. It does not assert a global boundary Harnack estimate when `g` vanishes.

## 6. Uniqueness without dividing at a zero boundary

Let `r0,r1` be two nonnegative minimizers with the same mass and trace. Both are positive in the interior. Their fourth-root mean is admissible, and density convexity makes its energy at most the common minimum. Hence equality holds in the integrated pointwise convexity inequality.

On each interior point, the weights of both amplitudes are positive. The normalized gradients differ by `n tensor(a1-a0)`, with `ai=grad log ri`. The one-dimensional convex-quartic remainder gives

    F(C+Q)-F(C)-DF(C):Q >= F(Q)/3
                          >=(mu/3)|Q|^4

for a rank-one `Q`. Thus the affine gradient slice is strictly convex. Equality in the perspective interpolation forces `a0=a1` almost everywhere in the interior. Locally the logarithms are Sobolev functions, so `grad log(r1/r0)=0`. Connectedness makes their ratio constant, and equal positive mass fixes that constant to one.

This avoids a division by a reference that may vanish at the boundary. It also explains why connectedness is essential: disconnected components can admit separate amplitude scalings with a common total mass.

## 7. Consequences for the affine replacement and weak flux dual

For the incoming translated smooth affine test, choose the target translation so that `g=|Bx+c|` is bounded away from zero on the boundary. Planar `W1,4` continuity extends to the closure of a bounded Lipschitz domain. The proved interior positivity and positive boundary trace then give `min_closure r*>0`.

The actual minimizer can consequently serve as a rough positive Picone reference. For any real competitor `s` with the same boundary and fourth mass,

    phi=s^4/r*^3-r*

is a legal zero-trace Sobolev test. The exact Picone identity and (E), with mass difference zero, give

    E(s)-E(r*) >= (mu/3) integral r*^4 |grad(s/r*)|^4.      (5)

No `C1` regularity of `r*` or illegal identity `lambda=E/M` is needed. Thus positivity closes this comparison gate for the translated affine-boundary replacement. It still supplies no sign of the minimized value relative to `|Omega|F(B)`.

On a fixed phase torus, positivity is global. Write `sigma=r*^4`, `a=grad r*/r*`, and `j=partial_a f_k(a)`. Then `j in L^(4/3)`, while `f_k(a)` and `a.j` are integrable. Testing (E) with variations `delta rho/(4r*^3)` gives in distributions

    -div j/4-f_k^*(j)=lambda.

The right side and conjugate are integrable, so the divergence has an `L1` representative. Periodic integration by parts is legitimate against fourth-power Sobolev amplitudes, which are bounded and have `L4` gradients in the planar setting. This gives an exact **weak-flux** dual certificate and `E(r*)=lambda M`.

This is not a smooth-flux or uniformly pointwise numerical certificate. Convolution of a weak flux may give residual convergence in `L1` without its essential infimum converging to lambda. Constructing or approximating the minimizer with a certified uniform residual is an additional regularity/acquisition problem. The full direction-field optimization, arbitrary-phase quasiconvexity sign, physical interpretation and efficient complexity remain open.

## 8. Review disposition

No decisive gap was found in the proposed planar positivity route under the exact theorem above. Its crucial gates are quartic evenness, `mu>0`, bounded direction derivatives, nontrivial mass, legal signed mass-constrained variations, connectedness and `4>d`. Stronger claims that remove these gates, use a boundary-vanishing reference without control, or promote a weak optimal flux to an acquired smooth certificate have not been proved here.
