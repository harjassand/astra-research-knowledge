# Ordinary construction, scientific consequence and allocation decision

29 October 2026. This wave acquired an actual analytic extension operation;
it did not identify a justified civilisation-scale lead. The mathematical
constructor and analytic-target corollary are preserved without converting
their regularity improvement into computational or physical advantage.

## 1. The first question and the result that survives

The question was whether the compact smooth cutoff in the earlier natural
Hamiltonian construction was an essential obstruction to REAL-ANALYTIC,
globally near-harmonic natural potentials. It is not, for the analytic-torus
source subfamily with acquired exponential Fourier bounds.

PROOF.md supplies an explicit operator which extends every compatible value
and force on that retained torus to a globally real-analytic correction,
with a computable whole-space Hessian bound. The formula has exact graph
jets and vanishing value/gradient at the origin. Its dependence on supplied
jets is linear. It uses no nearest-point inverse, convex envelope, isometry
oracle or fitted numerical potential. Coefficients and their exponential
tail bounds are paid inputs, acquired by the prior explicit analytic
isometry contraction for its finite-Fourier source.

Thus the earlier analytic torus computational subfamily can be embedded in a
globally analytic strictly convex natural well at the same dimension and
with the same quadratic position readout. This does not upgrade the old
arbitrary SMOOTH compact-flow theorem to all those same sources. An analytic
potential on an analytic embedding cannot reproduce arbitrary nonanalytic
force data. A global real C^r bound alone is not an analytic strip bound.

The correction has Gaussian-decaying tails times bounded analytic functions
and polynomials; all fixed real derivatives decay rapidly at infinity. It
does not have compact support. Entire holomorphic extension to all complex
positions is not asserted. For general analytic input Fourier coefficients,
such an extension would be much more restrictive.
The stronger formula (17) in PROOF.md pays a SINGLE fixed global complex
tube, uniform in the real position, on which the correction is bounded and
tends to zero with the input jets. Qualitative Cartan extension and fine
approximation do not alone acquire that tube norm. The analytic-target
natural wells can therefore approach the harmonic well in this stronger
analytic Banach norm, with exact invariant dynamics and readout retained.

## 2. The strongest ordinary mechanism is not missing

The scalar mode extension is the ordinary tensor-product Poisson extension
on a polydisk, composed with the analytic radially flat map

    w_j -> w_j exp[(1-|w_j|^2)/2].

It is not a new integral transform. The additional graph Hermite correction
and Gaussian residual give a directly evaluable assembly and bound for this
particular coordinate interface. Historical priority for that combination
is UNKNOWN. Nothing here establishes a faster method than an equally
informed analytic-extension specialist could construct.

The close primary analytic-interpolation source was read directly:
Cieliebak--Eliashberg, *Symplectic Geometry of Stein Manifolds*, draft
12 October 2007, Chapter 8, especially Corollaries 8.16--8.17 and
Proposition 8.20/Theorem 8.22. Their stated approximation is over a compact
set, while jet extension is global. Their compact statement alone must not
be cited as a uniform Hessian theorem over all Euclidean space.
[Primary text](https://math.stanford.edu/~eliash/Public/Site/Eilenberg_Lectures_files/stein7.pdf).

An equally informed ordinary COMPOSITION already supplies qualitative global
control. Here is the complete reduction, making its imported information
and absent quantitative costs explicit. Let N be the compact analytic
embedded torus, and let Wc be the earlier smooth compactly supported
extension, analytic in a neighborhood of N. Such a local analytic extension
is obtained from its analytic normal coordinates and jets, before cutoff.

1. Cartan-type analytic jet extension (the cited Corollary 8.16) gives a
   global analytic F with the same first jet on N. Apply the same result
   to the components of the local analytic normal coordinate map to obtain
   finitely many global analytic r_i vanishing on N whose differentials
   span its conormal. Add the finite global analytic defining functions
   of Corollary 8.17, so the COMMON zero set is exactly N.
2. R=Wc-F vanishes to second order on N. Local Hadamard division gives
   R=sum_(i,j) r_i r_j h_ij with smooth coefficients near N. Away from N,
   sum r_i^2>0 permits the same form. A smooth locally finite partition
   of unity patches the coefficients, keeping the same FINITE family of
   pairs i,j. This is ordinary division by the squared regular submanifold
   ideal, not an analytic division oracle for the coefficients.
3. Approximate each h_ij and its derivatives through order two by global
   analytic a_ij, with pointwise tolerance chosen below a positive multiple
   of [1+sum ||D^a(r_i r_j)||, a<=2]^{-1}. Whitney fine approximation pays
   this variable tolerance. Then Fa=F+sum r_i r_j a_ij has exactly the same
   first jet on N and is arbitrarily uniformly C^2-close to Wc on ALL of
   R^D. To preserve the origin conditions, multiply by the known polynomial
   2z-z^2, z=|Lq|^2/n; it is one with zero derivative on N and vanishes to
   second order at zero. Use the correspondingly stronger fine tolerance
   outside the fixed compact support. Its cost on Wc is a fixed finite
   C^2 multiplier, so the total still tends to zero with the input jets.

The fine approximation import is classical, not hypothetical. Johanis,
*A remark on the approximation theorems of Whitney and Carleman--Scheinberg*,
Comment. Math. Univ. Carolin. 56 (2015), Theorem 1, gives approximation of
derivatives with arbitrary positive continuous tolerance on an open subset
of R^D; for the full R^D its approximants are entire. This applies to the
smooth COEFFICIENTS above, not to interpolation of arbitrary analytic jets
by an entire ambient function.
[Author's primary manuscript](https://www2.karlin.mff.cuni.cz/~johanis/papers/10b-whitney.pdf).

This argument has finite geometric imports but gives no explicit numerical
operator norm, coefficient acquisition or complexity by itself. The direct
formula in PROOF.md acquires that interface in the retained-coordinate
case. It would be wrong to claim that qualitative analytic extension or
even qualitative global C^2-small interpolation was unavailable before
this wave.

Tao, *On the universality of potential well dynamics*, 1707.02389v3, is the
controlling ordinary dynamical prior. It supplies natural potential-well
universality under a strongly adapted one-form criterion and the clock
extension. The previous near-harmonic geometry and its exact readout were
already acquired in this project. This wave changes the regularity/evaluator
interface for analytic inputs; it does not discover natural-well universality.
[Primary paper](https://arxiv.org/abs/1707.02389v3).

## 3. Same-input actual constructive comparison

compile_extension.py acquires the compatible jets of the FULL family

    Q(phi)=(cos phi,sin phi,delta cos 2phi),
    phi'=1/sqrt(1+4delta^2 sin^2 2phi).

The force is computed from its exact unit-speed acceleration. Cleared
Laurent/polynomial identities establish compatibility symbolically, rather
than supplying a force table for free. The Fourier constructor sums all
infinite geometric rays using a square root, exponentials and rational
operations; no hidden Fourier truncation or approximation oracle remains
in this finite-expression input.

The equally informed ordinary construction uses the exact algebraic
defining functions r1=x^2+y^2-1 and r2=z-delta(x^2-y^2). Write its compatible
force minus a polynomial value extension as a conormal combination
alpha grad r1+beta grad r2. The explicit alpha,beta in the compiler are
rational, with denominator powers of 1+16delta^2 x^2 y^2 >=1 globally.
Then

    Wordinary=(2R-R^2) exp[-r1^2-r2^2]
                    [f_extension+alpha r1+beta r2],
    R=x^2+y^2,

has exactly the same values/forces and origin conditions. This is a
straightforward, stronger source-specific conventional alternative.

Its GLOBAL Hessian gate is also paid. After clearing the positive
denominator, every Hessian numerator vanishes to at least first order in
delta. For 0<delta<=1 replace delta^p by delta and every monomial in the
position variables by a power of |q|. With t=sqrt(r1^2+r2^2),

    |q| <= sqrt(1+t)+2t+1 <=3t+2.

The resulting polynomial has nonnegative coefficients. Weighting its j-th
coefficient by j! bounds the full Gaussian tail. Maximum absolute row sum
pays the Hessian operator norm. No spatial grid is used for either method.

The literal common selected input is delta=2^-204. It is selected by the
conservative ordinary bound, not claimed as a useful mechanical amplitude.
The whole-space Hessian bounds are <2.130e-50 for the Fourier constructor
and <5.349e-7 for the ordinary formula, both below the requested 0.01.
These incomparable conservative upper bounds establish admissibility;
their ratio is not a performance, optimality or physical advantage.
The ordinary finite formula does not automatically meet the additional
bounded-complex-tube contract. Its denominator
v2=1+16delta^2 x^2 y^2 vanishes at x=R,y=i/(4delta R), arbitrarily near
real positions as R grows. These are genuine generic poles: the coefficient
of z in its jet bracket is beta=delta(x^2-y^2)(4/v2^2-1), with a nonzero
double-pole coefficient there. Multiplication by a nonzero entire Gaussian
does not remove them for generic z. This distinction is about the acquired
uniform analytic norm, not superiority on the real trajectory task. The
Poisson/Hermite construction itself is an informed composition of ordinary
mechanisms; no absence or historical originality is inferred.

The combined exact algebra, two global bound compilations and 160-digit
finite-expression diagnostics took 8.489680250000674 seconds including
imports on the existing local scientific Python runtime. No separate
timing ratio is inferred. At the exact circle point (3/5,4/5), both forces
agree with the prescribed force to <8.90e-162 in that numerical diagnostic.
The exact general jet identity, not this decimal check, proves equality.
There were no trajectories, random draws, universal-source/isometry
execution, physical data or apparatus. Local CPU was free; primary-source
reading, derivation and model reasoning were not wall-time metered.

## 4. Decision relative to the strongest existing asset

The attempted shortcut was that upgrading the old potential's regularity
would by itself create a qualitatively new predictive or computing
capability. The construction succeeds mathematically, but that strategic
inference fails. Analyticity does not supply robust initialization, generic
invariant basins, bounded physical precision, or a finite-time algorithm
for an asymptotic question. The ordinary extension composition already
delivers its qualitative reach; the matched source-specific constructor
also achieves the actual finite input.

Preserve the explicit extension and analytic-target consequence as useful
mathematical capital. It does NOT justify displacing the strongest acquired
positive operation on the current evidence: conditional product-phase
Gibbs preparation actually produces a requested state under its stated
resource contract. Its physical/local-controller and reservoir gates are
real and remain open at their own scopes, but this analytic representation
does not remove them or deliver an alternative device. No new hardware
capability has been acquired here.

Priority would change if this representation exposed a finite, robust
computation/actuation that the strongest ordinary construction cannot
already provide, or a new dynamical theorem with consequential finite-time
content. Neither is established by the present analytic upgrade. There is
no justified 100/100 route from this wave. This is a completed positive
constructor plus an informed scoped failure of the promotion hypothesis,
not a catalogue or a claim that no other opening is possible.
