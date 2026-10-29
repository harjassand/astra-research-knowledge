# Independent whole challenge: analytic potential extension

29 October2026. Reviewer: retained capability-inversion peer. Producer
directory was READ ONLY. No producer function import, model/ODE run,
symbolic Hessian re-expansion or new input case was performed.

**Decision: ACCEPTED at the stated mathematical, exact finite-formula and
saved rational-majorant scopes. No substantive correctness obstruction or
source correction was found.** This is not a novelty, physical feasibility,
trajectory-accuracy or finite-time computational-advantage acceptance.

The reviewed producer snapshot is
`b_conventional/independent_opening/FROZEN.json`; all11 listed hashes match.
Its governing PROOF hash is
`6e60c745799cd5391b7994b1afab593172e21cf616348cf85907996863c72c97`.
The four inherited mathematical input bindings also match. Their old
acceptance is retained; this review does not reopen N675 or its imports.

## 1. Native analytic source qualification and retained coordinates

The general theorem requires a real analytic torus Q with the SUPPLIED
fixed linear extractor LQ=(e^(i phi_j)), compatible analytic value/force
jets, an effective positive strip rho and weighted absolute Fourier norms,
plus coefficient evaluation costs. Those are substantive inputs, explicitly
not asserted for an arbitrary black-box analytic or smooth function.

For the actual curve the compiler acquires them rather than granting them.
Q=(cos phi,sin phi,delta cos2phi) has speed square
v2=1+4delta^2 sin^2 2phi. Its normal acceleration is
Q''/v2-Q'v2'/(2v2^2), so g=-A-Q and f=(1-|Q|^2)/2 obey Q'.g=f' exactly.
The symbolic circle division in the code checks precisely this identity;
the numerical point is not the proof. In the 2^|k| weighted algebra,
||v2-1||=34delta^2 and ||v2'||=128delta^2. The f bound17delta^2/4 is exact.
For g, retaining -Q''-Q first yields12delta; the residual geometric
v2^-1 and v2^-2 terms give exactly the stated positive G bound. The Q',Q''
overpayments4+8delta and4+16delta are valid. No force/geometry table or
uncomputed nonlinear embedding is supplied for this executed family.

For the inherited analytic torus, the retained sQ0 block supplies the
literal linear extractor. Its complex pairs give w0=e^(i theta),
wi=e^(i(theta+x_i)). The phase map is an integer torus automorphism, and
the stated frequency inequality |k'|1<=2|k|1 pays its fixed strip loss.
The duplicated isometry block may change without changing L or readout.
COROLLARY_NORM_ACQUISITION.md explicitly reconstructs small f/g bounds from
the accepted contraction error, including the important baseline
(partial_theta^2+1)Q0=0 cancellation. Thus norm bounds can be acquired by
finite products/derivative strip losses, not by an unnamed analytic norm
oracle. Its halving gate terminates, without a practical speed claim.

An arbitrary smooth source is not admitted. Indeed analytic W composed
with analytic Q has analytic graph value/force; a nonanalytic smooth
compatible jet cannot become analytic by this extension. The old smooth
theorem and the new analytic subfamily remain distinct.

## 2. Global mode extension and the holomorphic source bound

Each Phi_k is a tensor product of angular monomials composed with
w->w exp[(1-|w|^2)/2]. For real coordinates, r^m exp[m(1-r^2)/2]<=1;
its radial derivative vanishes at r=1. Thus the Fourier extension is a
linear bounded radially flat interpolation, as required for the exact jets.

I independently reconstructed its COMPLEX bound. If the two real
coordinates are complexified with imaginary Euclidean displacement delta,
the monomial modulus is bounded by(r+delta)^m and the Gaussian by
exp[m(1-r^2+delta^2)/2]. The maximum solves r(r+delta)=1; its derivative
in delta is r+delta<=1+delta. Hence the logarithmic excess is at most
delta+delta^2/2. Coordinatewise imaginary width h gives the conservative
exp(4h|k|1). With4h<=rho/2 there is a strict margin to the input weight,
so the full sums are holomorphic in a neighborhood of the closed tube,
uniformly over ALL real parts. Smooth termwise convergence is not being
misused as analyticity. Cauchy partial bounds and the finite coordinate
expansion give j!(2n/h)^j as a safe multilinear derivative overpayment.

Exponential truncation uses the remaining rho/2 weight; applying the same
receiver to the tail gives the displayed exp(-rho K/2) times fixed-order
derivative constants. Subsequent interval composition can evaluate the
formula locally. Only the infinite exact formula has the graph jets; no
truncated finite polynomial is called exactly invariant. O(K^n) modes and
input coefficient costs remain explicit.

## 3. Exact graph/origin jets and all-space convexity

On the standard torus let P be its tangent projection. Radial flatness,
LQ=i and compatibility give L DE_Q=P and DE_Q^T g=grad E_f, with
P grad E_f=grad E_f. Thus the vector a=E_g-L^T grad E_f obeys
DE_Q^T a=0. Differentiating B=E_f+r.a at r=q-E_Q(Lq)=0 gives g exactly.
The Gaussian multiplier has value1/zero gradient there; the origin
polynomial has value1/zero gradient at |Lq|^2=n and value/gradient0 at q=0.
Extraneous zeros of r are harmless. These calculations prove the exact
value and force jets and both origin conditions without a nearest-point
projection, minimization or inverse map.

I reconstructed all product/chain constants in H(u): the B, DB, D2B
polynomials, both Gaussian derivatives, and the three origin-polynomial
derivatives. |q|<=|r|+M is valid on the ENTIRE real space. H has degree7
with nonnegative coefficients. The elementary exp(-u^2)u^j<=j! bound
therefore controls every position, not a Hessian grid. For fixed Q,L,rho
the bound is linear in F,G. The exact saved C2<0.01 implies the full
Hessian of V lies between0.99I and1.01I. Together with V(0)=gradV(0)=0 it
proves a unique global minimum and quadratic coercivity.

For a complex q with ||Im q||<a, Lq is in the inner half tube. Cauchy pays
the complex gradient of E_f, giving Ac=G+2ell c1F. Writing R=||Re q|| and
u=(R-M)+ gives |Im r|<=a+M, |Re r|>=u, |q|<=u+M+a and
|r|<=u+2M+a. Holomorphic r.r, rather than a Hermitian square, consequently
has the asserted Gaussian modulus. The degree-five Pc majorant and its
factorial envelope are correct. The bound uses one FIXED global tube,
independent of the real position and the small jet parameter. It does not
assert an entire function, polynomial potential or analytic compact support.
Every fixed real derivative decays rapidly at infinity by the same
Gaussian/polynomial argument.

## 4. Literal finite-expression compiler, including ray boundaries

I read all248 lines of compile_extension.py and all49 lines of
compile_tube_bound.py. At the literal delta, factorization
v2=c(1-rz^4)(1-rz^-4) follows from cr=delta^2 and
c(1+r^2)=1+2delta^2. Expanding its square inverse gives
r^|m|[a+b|m|] at frequency4m. Multiplying the finite numerator of g then
reduces to shifted geometric rays. For m>=0 the split N=ceil(-k/4), clipped
at0, places the zero harmonic in the correct tail; the negative split is
ceil(k/4), clipped at1. Each tail has coefficient a+b(N+j), precisely the
saved rational formula. No negative power or missing/duplicated zero mode
remains, including k divisible by4. |zeta|<=1 and r<1 prove all real
denominators bounded away from zero. Thus the evaluator is finite, without
a hidden Fourier-sum/force oracle.

E_Q, E_f and its literal gradient in candidate() match the extension
formula, and the gradient chain is included. The force diagnostic compares
the TOTAL potential gradient with -A, correctly including the harmonic
part. Its point(3/5,4/5,-7delta/25) is exactly on the source curve.
The mpmath values remain diagnostics, with no outward guarantee on their
8.9e-162 displays; the graph-jet theorem supplies equality. The independent
review does not reinterpret them as a certified value/force evaluator run.

## 5. Same-input ordinary comparator and actual prior

The direct defining functions r1=x^2+y^2-1 and
r2=z-delta(x^2-y^2) are regular on the source. Subtracting the polynomial
value gradient leaves a conormal; the stated alpha,beta reconstruct it.
The compiler clears exactly those ideals to check the full jets.
Its Hessian numerator/denominator logic is sound: denominators are positive
constant times powers of1+16delta^2x^2y^2>=1, numerator terms each contain
delta, and0<delta<=1 permits delta^p<=delta. With
t=sqrt(r1^2+r2^2), |q|<=sqrt(1+t)+2t+1<=3t+2, so positive polynomial
Gaussian envelopes and maximum absolute row sums pay the global operator
norm. The ordinary recipe passes the SAME real geometric task.

The stronger tube contrast is also genuine. Its z coefficient is
beta=delta(x^2-y^2)(4/v2^2-1). At x=R,y=i/(4delta R), v2=0, with a
nonzero generic double-pole coefficient. The entire Gaussian is nonzero,
and the origin polynomial does not cancel these poles generically. Their
imaginary distance tends to zero as R tends to infinity. Therefore this
particular ordinary formula has no uniform global complex tube, even
though its real Hessian is controlled. This is not a theorem excluding
other ordinary constructions, including the producer's own composition.

I directly read the controlling PRIMARY statements:

* [Cieliebak--Eliashberg, Chapter8](https://math.stanford.edu/~eliash/Public/Site/Eilenberg_Lectures_files/stein7.pdf),
  Cor8.16/8.17 supply global analytic jets and a finite common zero set for
  properly embedded real analytic submanifolds. Prop8.20/Theorem8.22 give
  approximation on a COMPACT set, not a full-space norm bound.
* [Johanis, Theorem1](https://www2.karlin.mff.cuni.cz/~johanis/papers/10b-whitney.pdf)
  supplies positive-continuous-tolerance derivative approximation; for the
  full R^D its approximant is entire. Taking tolerance<=1/2 ensures that
  both derivatives needed here are included. Real scalar second Frechet
  differential norm controls the Hessian operator norm.
* [Tao1707.02389v3](https://arxiv.org/abs/1707.02389v3) is the controlling
  ordinary natural-well universality prior. Its abstract/version were
  refreshed; the old source/universality import is retained at its accepted
  scope, not newly re-audited here.

The supplied Cartan+division+fine-approximation COMPOSITION does supply
qualitative all-space C2-small jet interpolation: local conormal generators
plus global defining functions generate the smooth squared ideal; a smooth
partition patches finitely indexed coefficients; fine approximation with
coefficient-weighted tolerance controls their products at infinity. The
origin multiplier is paid by a stricter tolerance and by the old compact
extension's fixed-support multiplier norm. It supplies no explicit bound
or fixed-tube norm by itself. Thus qualitative analytic universality/global
C2 interpolation are NOT new absence claims in this packet.

## 6. Old analytic-torus corollary and physical-clock limits

With the accepted analytic contraction and exact linear extractor, the
small f/g jet bounds acquire both a uniformly small Hessian and a small
supremum on one fixed global complex tube. The old invariant torus retains
its speed, energy, quadratic position readout and dimension. Global strict
convexity gives an analytic compact level V=1/2; the encoded acceleration
is normal to that whole hypersurface, so its speed-one curves are its
geodesics. This inference is conditional on the OLD admitted analytic
source; it does not promote arbitrary smooth dynamics or execute a
universal coefficient table.

Root's separate root_analytic_limits/PROOF.md is consistent and I
independently reconstruct its interpretation. For two trajectories,
E=(|delta q|^2+|delta p|^2)/2 obeys |E'|<=eta E. Thus phase-flow Lipschitz
growth is at most exp(eta|t|/2). A positive source Lyapunov exponent lambda
encoded at speed epsilon requires eta>=2epsilon lambda. If a fixed complex
tube of radius a has supremum delta, Cauchy's real directional Hessian
bound2delta/a^2 gives delta>=a^2 epsilon lambda. The actual theorem permits
clock slowing and makes no contradictory rate claim. These are not general
computation/precision lower bounds; a universal source need not have positive
Lyapunov exponent. No attracting error-correcting basin or hardware gain
follows from exact Hamiltonian geometry.

## 7. Independent executable receipt and final boundary

verify_static.py imports only the standard library and NONE of the producer
programs. In0.0056005s after those imports it checks all11 producer bindings,
all4 inherited bindings, the source norms, reconstructs the exact degree7
Hessian majorant and its linear F/G dependence, and exactly reconstructs
the degree5 tube majorant. All saved rational bounds match. It also checks
441 formal square-inverse coefficients and1029 shifted-ray coefficients,
including5 zero-harmonic boundaries. These controls corroborate the literal
compiler bookkeeping; the preceding all-input proof reconstruction, not
their finite count, supports the review decision.

The original8.48968s producer symbolic/model/evaluator run was NOT repeated.
No independent full symbolic Hessian-coefficient expansion, propagation,
trajectory, physical data, new isometry or empirical benchmark is claimed.
The scalar read-only checks add no new science case. Tiny delta2^-204 and
conservative admissibility bounds do not qualify useful mechanics.

Preserve the explicit evaluator/global analytic norm as positive mathematical
capital. Historical priority, physical implementation, robust finite-time
computation and practical advantage remain UNKNOWN/NOT_ACQUIRED. No repair
to the frozen producer files is requested, and no more model run is needed.
