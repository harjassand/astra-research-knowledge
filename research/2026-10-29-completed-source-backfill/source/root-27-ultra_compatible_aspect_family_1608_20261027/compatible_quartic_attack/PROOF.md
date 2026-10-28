# Compatible-gradient construction and exact scope

The target is the exact nine-coefficient quartic in `TARGET.json`. Write
A=[[a,b],[c,d]], u=a²+c², v=b²+d², w=ab+cd, q=ad−bc, and

    F(A)=α(u²+v²)+Cuv+Ew²+q(Lu+Mv).

Here α=55220381/10¹⁰, C=114430029/625000000,
E=−801761987/5000000000, L=297124543/10¹⁰,
M=−148562271/5000000000. In particular L+M=10⁻¹⁰ exactly.
No L=−M symmetry reduction is used. The source literal acoustic certificate
has positive shift δ=1/200000 and is replayed by `verify_exact.py`.
It proves strict rank-one convexity, not quasiconvexity.

## Exact background elimination

For any actual periodic gradient X=Dφ with mean zero, homogeneity and
polarization give, for every constant B,

    ⟨F(B+X)−F(B)⟩ = c+b:B+½ B:H:B,
    c=⟨F(X)⟩, b=⟨DF(X)⟩, H=⟨D²F(X)⟩.

The cubic-in-B term vanishes because ⟨X⟩=0. The complete symmetric fourth
tensor also gives D²F(X)[B,B]=D²F(B)[X,X]. Fourier Parseval and the source
strict acoustic inequality therefore imply

    B:H:B ≥ δ⟨|X|²⟩ |B|².

This applies to P1 potentials by H¹ approximation. Consequently every
nonzero compatible gradient here has H positive definite. No artificial
regularization or supplied variational normalization is needed. The exact
minimum over all four unbounded background coordinates is attained at

    B*=−H⁻¹b,
    Δ=c−½ bᵀH⁻¹b.

This reduction is established Astra machinery; its application is not
claimed as a new general theorem.

We also have a useful pointwise lower bound. Since u,v≥0, uv=w²+q², and
C+E−2α>0,

    F = α(u+v)² +(C+E−2α)uv −E q²+q(Lu+Mv)
      ≥ α s²+γq²−ell|q|s ≥ κs²,
    s=u+v, γ=−E, ell=(|L+M|+|L−M|)/2,
    κ=α−ell²/(4γ)>0.

The exact κ is in the replay; its decimal value is about .0041456477952.
Thus c>0 for every nonzero field, justifying the normalized objective Δ/c.
Pointwise positivity alone proves no nonzero-background Jensen inequality.

## An actual compatible profile

`data/EXACT_COMPATIBLE_PROFILE.json` contains a periodic128×128 P1 potential
whose two-component nodal values are integers divided by10⁸. Its exact
node order, triangles and gradients are in `NODAL_INTERFACE.md`.
There are32768 equal-area triangles. Shared nodes make the potential
continuous, so this is an actual W¹,∞ gradient and not an unconstrained
determinant-balanced atomic law. Direct integer sums verify ⟨X⟩=0 and
⟨detX⟩=0. Exact second-moment LDL pivots in `EXACT_REPLAY.json` also verify
full covariance rank for the retained profile.

Rational acquisition of all degree2/3/4 moments gives

    Δ/c = .10576917435931778…,
    l/c = .8942308256406822…,
    l=½ bᵀH⁻¹b.

These decimal values abbreviate the exact fractions in the artifact.
Both Δ>0 and H>0 are checked exactly. The profile is not a negative Jensen
witness. Positive definiteness of H and full covariance rank do not turn
this finite test into a theorem for arbitrary compatible fields.

It does give an exact failure of amplitude-curve convexity. With its fixed
optimal background B*, the actual compatible scaling curve is

    g(s)=⟨F(B*+sX)−F(B*)⟩ = cs⁴−2ls³+ls².

At s=l/(2c), g''=l(2−3l/c)<0 since l/c>2/3. Nevertheless g(s)≥0 for every
real s because 0<l/c<1:

    g(s)=s²[c(s−l/c)²+l−l²/c].

Thus a proposed proof requiring convexity along every amplitude scaling
would fail on this target and this genuine compatible field. This is not
negative Jensen, negative heat dissipation, or a contradiction of QC.

## Continuum aspect-ratio construction

Let barφ(x)=∫₀¹φ(x,y)dy and ψ=φ−barφ. For this uniform diagonal P1 mesh,
barφ is the linear interpolation of nodal row averages. To check this,
integrate the two affine triangles in one vertical strip: the quadratic
terms in the strip coordinate telescope when summed over the periodic
row index. On column i the remaining derivative is exactly

    barφ'=Σ_j[φ(i+1,j)−φ(i,j)].

For every t>0 define the potential on the rectangular periodic cell
[0,1]×[0,t] by

    φ_t(x,y)=barφ(x)+t ψ(x,y/t).

It is continuous and periodic, with actual gradient law

    X_t=[barφ'+t ψ_x | ψ_y].

After the change of variables y=tz, each original triangle still has
normalized weight1/(2n²). This is a compatible deformation, not an
arbitrary transformation of matrix moments. Using rectangular cells is
legitimate for periodic tests of quasiconvexity; a negative periodic gap
would also yield a compactly supported test by tiling and cutoff.

At t→0 the law has a two-stage rank-one Jensen description: first
average the zero-mean second-column fluctuation at each x, then average
the first-column fluctuation over x. The finite-t correlations are kept
in the construction; this limiting observation is not used to drop them.

Each atom is affine in t, so c(t), b(t), H(t) have degrees at most4,3,2.
The exact M2 polynomial has positive constant term, zero linear term and
nonnegative quadratic term. The acoustic bound above gives detH(t)>0
for all t>0. With adj denoting the matrix adjugate, put

    P(t)=2c(t)detH(t)−b(t)ᵀadjH(t)b(t),
    Δ(t)=P(t)/(2detH(t)).

P has degree12. `aspect_family.py` acquires its exact rational coefficients
from all32768 triangles. It also acquires

    Q(t)=P(t)−(41/200)c(t)detH(t).

The exact signed Sturm sequences for both P and Q have degrees12,11,…,0.
Both have positive value at0 and zero roots on(0,∞). The stored variations
at0+ and+∞ are6 and6 for each. Since c(t)>0 and detH(t)>0,

    min_B ⟨F(B+X_t)−F(B)⟩ > (41/400)⟨F(X_t)⟩  for every t>0.

The same inequality holds after every nonzero common amplitude scaling
of the potential, with the background still optimized freely. The
numerical aspect minimum near t=.55332385 has Δ/c≈.102519985; the exact
uniform bound .1025 is proved independently of that numerical estimate.

This is a continuum, all-background exclusion of a counterexample within
one explicitly acquired compatible geometric family. It proves neither
quasiconvexity of F on all profiles nor a barrier against other multiscale
constructions.

## Verification and scientific boundary

`verify_exact.py` does not trust the optimizer. It first substitutes
t=1/2,1,2, then independently reacquires integer atom moments and exact
positive LDL factors. These agree with the family polynomials and their
cleared gaps. SymPy independently checks each signed Euclidean remainder
in both Sturm sequences and counts positive roots. The source acoustic
checker is whole-read and actually executed against its pinned source.

No negative Jensen value was found. The ordinary baseline is the same
exact target with direct compatible Fourier/P1 optimization, not an
unconstrained law, a rank-one-direction test, or a finite SOS certificate.
Fourier/P1 testing, background elimination and Sturm's theorem are not
new mechanisms. The acquired profile, its exact stronger-proof failure,
and the continuum geometric certificate are the scoped outputs here.

The unresolved operation is control of arbitrary correlations among
compatible gradients, including scale-dependent changes of the profile.
A positive result for this fixed aspect family supplies no compactness
or finite-search completeness theorem. A genuine negative result would
need an actual compatible field with Δ<0; this work does not supply it.
