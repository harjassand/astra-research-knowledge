# An implementable Pauli readout, and a cost of its exact projection law

15 October 2026. Root derivation. This is an internal mathematical result,
not a historical-priority claim or laboratory demonstration. The input's
reciprocal-gamma kernel is user-supplied research, not a new result of this
campaign. Ordinary covariant spin measurements are established prior art.

## 1. Compile a radial positive qubit density without Fourier tomography

Suppose a normalized qubit POVM has density

    M(x) = u(r) I + v(r) n·sigma,  r=|x|, n=x/r,

where u >= |v| and integral 4 pi r² u(r) dr = 1. Put

    w(r)=4 pi r²u(r), a(r)=v(r)/u(r).

Zero-u radii have zero probability and may be assigned any a. The following
ideal sampling operation implements M on a supplied qubit state rho:

1. Draw r from w independently of rho and n uniformly from the unit sphere.
2. Measure n·sigma once; let b in {-1,+1} be the result.
3. Put n0=b n. Independently flip n0 with probability (1-a(r))/2.
4. Return X=r n0.

Writing rho=(I+s·sigma)/2, the pushforward of (n,b) has directional density
(1+s·n0)/(4 pi). The flip makes it (1+a(r)s·n0)/(4 pi).
Multiplying by w gives exactly Tr(rho M(x)) dx. This is a direct one-shot
compiler, whereas characteristic-function estimation plus Fourier inversion
reconstructs a distribution using many independent input copies.

The compiler uses an ordinary random-axis projective measurement. It does
not remove state preparation, continuous random sampling, rotation precision,
readout errors, or radial preprocessing and sampling costs. It is not an
efficient compiler for arbitrary noncommuting tuples.

There is a stronger comparator conclusion than a raw-variance comparison.
The ordinary covariant outcome n0 has POVM density (I+n0·sigma)/(4 pi).
Drawing the independent radius and flipping n0 is a state-independent
classical Markov postprocessing of this outcome. Thus the covariant outcome
statistically dominates X: any decision procedure receiving X can be run
from n0 by the same random postprocessing, for every input state. Under the
same available random-axis measurement, no state-inference task acquires
extra information from the radial compiler. Its exact projection-law format
is obtainable, but it is not a new quantum information-acquisition advantage.
The comparator is credited as an existing covariant spin measurement.

## 2. Reconstruct the supplied gamma example

Let p(r)=C/Gamma(2+r/2), f(r)=r p(r), and

    I(r)=integral_[|r-1|,r+1] f(s) ds.

The radial wave formula for Fourier multiplier exp(i t·sigma) gives, for
r>1,

    u=(f(r+1)+f(r-1))/(2r),
    v=I(r)/(2r²)-(f(r+1)-f(r-1))/(2r).

For 0<r<1,

    u=(f(r+1)-f(1-r))/(2r),
    v=I(r)/(2r²)-(f(r+1)+f(1-r))/(2r).

These signs use characteristic functions integral exp(i t·x) p(x) dx.
In both ranges u-v=f(r+1)/r-I(r)/(2r²). For r>=1,

    I(r)<=2r p(r-1),
    p(r-1)/p(r+1)=(r+3)/2<=r+1,

so u-v>=0, while u+v=f(r-1)/r+I(r)/(2r²)>=0.
On (0,1), f is increasing on [0,2]:

    f'=p[1-(r/2) psi(2+r/2)]>0

because psi(3)=3/2-EulerGamma<1. Thus
2r f(1-r)<=I(r)<=2r f(1+r), which proves both eigenvalue
inequalities there. Limits at r=0 supply the remaining point. Normalization
and the exact all-linear projection law follow from the wave Fourier identity.
This reconstructs the supplied example and supplies its direct compiler.

## 3. A positive variance gap for exact common additive noise

Assume radial mean-zero scalar noise Z with finite coordinate variance s²
and a positive normalized qubit POVM M on R³ satisfying

    integral exp(i t·x) M(dx) = phi_Z(t) exp(i t·sigma).

Twirling if needed preserves this identity and makes M rotation covariant.
Let X be its output on the maximally mixed state and R=|X|. Its first operator
moments are sigma_j and its second scalar moments give

    E R² = 3(1+s²).

Positivity, together with x·sigma <= |x| I, implies

    3 = sum_j Tr(sigma_j integral x_j M(dx))/2 <= E R.

Consequently s²>=2 and

    E(R-3)² <= 3(s²-2).

On the maximally mixed state the characteristic function in any unit direction
is phi_Z(t) cos t. Since X is isotropic, it is also E sinc(tR).
At t0=pi/2 it is zero. Since

    sinc(x)=integral_0^1 cos(ux) du,
    |sinc'(x)|<=1/2,

Cauchy--Schwarz gives

    2/(3 pi) = |sinc(3t0)|
       <= (t0/2) E|R-3|
       <= (pi/4) sqrt(3(s²-2)).

Therefore every such exact all-linear additive-noise POVM obeys

    s² >= 2 + 64/(27 pi^4) = 2.02433418015925...

This is a nonoptimal necessary bound. It does not certify a minimizer or a
sample-complexity lower bound for arbitrary nonlinear estimators.

An ordinary covariant spin POVM, outputting 3n, is unbiased and has
coordinate second moment 3 on the maximally mixed state (equivalent noise
variance 2 for the means). Its characteristic function is sinc(3t), which
does not vanish at pi/2. Thus it does not satisfy the stronger common scalar
convolution law. The gap quantifies a cost of that exact law, rather than an
advantage over conventional mean estimation.

Numerical quadrature of the supplied gamma noise gives s² about
7.63991732090103, hence raw-coordinate second moment about 8.63991732090103.
The comparator's second moment is 3. These values are bounded high-precision
diagnostics, not certified quadrature errors or laboratory sample costs.

## 4. Scope and primary predecessors

The existence/kernel claim is reconstructed from the user's pasted text.
Covariant spin POVMs and their postprocessing are established, for example
Barchielli--Gregoratti, arXiv:1912.09758, and Busch--Heinosaari,
arXiv:0706.1415. The present variance bound concerns exact state-independent
scalar noise in *every real projection*, a different constraint from ordinary
unbiased joint measurement. Historical priority for this particular elementary
gap estimate is UNKNOWN. No practical or exceptional foundational advantage
is established by it.

Primary links:
- https://arxiv.org/abs/1912.09758
- https://arxiv.org/abs/0706.1415
- https://arxiv.org/abs/1802.08343
