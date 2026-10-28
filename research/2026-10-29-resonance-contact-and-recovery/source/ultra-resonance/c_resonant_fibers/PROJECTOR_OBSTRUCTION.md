# Exact resonance is the wrong stable object near a weak interaction scale

This is an explicit source-level counterexample and a constructive repair.
It is not computational hardness, a new two-particle bound-state discovery,
or a claim that the finite source cannot be solved by ordinary methods.

## 1. Native flux family and exact algebra

Keep the SAME actual density interaction, with N divisible by four, but use

    H(lambda,phi)=H0(phi)+lambda V,
    H0(phi)=-J sum_j [e^(-i phi)c_j^dag c_(j+1)+h.c.],
    V=sum_j [n_j n_(j+1)+(1/3)n_j n_(j+2)], A_int=4/3.

The one-particle dispersion, up to the equivalent Fourier sign convention,
is `-2J cos(k-phi)`. An unordered two-particle momentum transition at fixed
total K has energy difference

    -4J cos(K/2-phi)[cos(k-K/2)-cos(p-K/2)].                (1)

At phi=0 all K=pi transitions are resonant. At any phi with
`0<|phi|<pi/N`, no total lattice momentum has `cos(K/2-phi)=0`; only the
forward/exchange transitions remain resonant. In particular the exact
time-average projector jumps discontinuously at phi=0. A quarter total flux,
phi=pi/(2N), already displays this while the one-body Hamiltonian norm changes
by at most2J|phi|. `check_resonance.py` verifies this distinction exactly at its
N8 source, not using a near-zero numerical tolerance.

The jump alone would be only a formal obstruction. The next calculation
shows an actual order-one wrong dynamical prediction if the exact projector
is used uniformly as the weak-coupling approximation.

## 2. An explicit bounded query with a wrong secular prediction

Restrict to the vacuum and the two-particle K=pi subspace. With the same pair
representatives as PROOF.md, put

    w_k=2cos(k)/sqrt(N),
    chi=sum_k w_k b_k^dag|vac>,
    Psi=(|vac>+chi)/sqrt(2),
    Q=|vac><chi|+|chi><vac|.

The identity `sum_(representatives)cos(k)^2=N/4` gives ||chi||=1. Q has
norm1 and both state components have even fermion parity. This is a
specified pair-coherence query, not a particle-number-superselected
measurement granted without a phase reference.

The first-range interaction here is `|w><w|`. The second-range interaction
is `(1/3)|w2><w2|`, with `w2_k=2sin(2k)/sqrt(N)`, orthogonal to w.
Equivalently chi consists only of nearest-neighbor real-space pairs, so the
second-range interaction annihilates it. Since `H0(0)=0`, at
`t=pi/(2lambda)` the exact zero-flux expectation is zero:
the chi component gains phase `exp(-i lambda t)=-i`.

Now let phi(lambda)=lambda^2, with `0<lambda^2<pi/N`. Coefficients are
numerical in a fixed energy unit, with hbar=1. In the two-particle sector
`||H0(phi)-H0(0)||<=4J|phi|`. Duhamel gives

    |<Q>_true at phi(lambda)| <=4pi J lambda.               (2)

By contrast, the exact time average of V under H0(phi(lambda)) is diagonal
in pair momenta, with diagonal `(4/N)[cos(k)^2+(1/3)sin(2k)^2]`, at most
4A_int/N. Keeping the free micromotion,
the naive first-order secular prediction has pair phases bounded by

    |phase_k|<=2pi A_int/N+2pi J lambda.

Consequently

    <Q>_naive >=cos(2pi A_int/N+2pi J lambda)               (3)

when that upper phase bound is less than pi. For every N>=16, taking lambda
sufficiently small gives a discrepancy tending to at least
`cos(2pi A_int/N)>=sqrt(3)/2`, even though phi(lambda)->0 and the exact
dynamics approaches the resonant answer. For example lambda<=1/(400J),
together with the gap condition, gives a strict discrepancy greater than4/5 by
`cos x>=1-x^2/2` and pi<22/7.

Thus exact finite-volume resonance selection does NOT uniformly approximate
the actual weakly perturbed family. No assumed kinetic closure or unknown
quantum state appears in this example. It also does not claim all late-time
methods fail: exact two-body propagation or ordinary degenerate perturbation
theory handles it cheaply. Its lesson is about the representation/ordering
of scales.

## 3. A detuning-resolved fiber, rather than a zero/nonzero decision

Use phi=c lambda with c fixed. The original K=pi pair Hamiltonian divided by
lambda converges, without discarding its small kinetic splitting, to

    L_c=D_c+sum_r a_r|w_r><w_r|,
    (D_c)_kk=-4J c sin(k).                                 (4)

This resolves the ratio phi/lambda. It is a finite real diagonal matrix plus
a fixed-rank interaction, so its amplitudes do not require a many-body
state reconstruction. In the continuum the cyclic measure of D_c in w is

    (2/pi)cos(k)^2 dk,  -pi/2<k<pi/2.

Under x=sin k this is `(2/pi)sqrt(1-x^2) dx`, a semicircle. Its orthogonal
polynomials are the Chebyshev U polynomials. Up to harmless signs,
`f_r(k)=cos(k)U_(r-1)(sin(k))`, so the w_r are the corresponding orthogonal
vectors. The pair channel is therefore a half-line Jacobi matrix with
off-diagonal entries2J|c| and boundary on-site entries a1,...,aR.

In the nearest-range subclass a2=0, only boundary entry1 remains. Solving
its geometric bound-state equation gives

    E_b=1+4J^2 c^2,
    boundary residue=1-4J^2 c^2,
    existence iff |c|<1/(2J).                              (5)

At the threshold the residue vanishes. A small ABSOLUTE detuning is therefore
not the right input qualification; the coherent regime is selected by its
ratio to the interaction. This is the standard nearest-neighbor interacting
hard-core/two-fermion bound-pair mechanism, not a new threshold result.
Valiente--Petrosyan2009, arXiv:0903.4574, its hard-core special case, already
gives `E=V+J_K^2/V` and `|J_K/V|<1` with `J_K=2J cos(K/2)`.
Kornilovitch's arXiv:2305.02548 supplies the broader finite-range lattice
two-body Green-function framework. These are strong ordinary alternatives.

## 4. The same repair extends the actual finite-density construction

This is not restricted to using a two-particle example as a surrogate for
finite density. For the full density-interaction source in PROOF.md, choose
the EXACT A0 dispersion as H0 and put the small detuning in the perturbation:

    H0(c lambda)+lambda V
      =H0(0)+lambda [V+(H0(c lambda)-H0(0))/lambda].         (6)

The extra one-body term COMMUTES with H0(0). Thus its entire contribution is
retained, while the only nonresonant primitive is still the explicitly
bounded density-interaction primitive b_N. Its perturbation norm is at most
`N[A_int+2J|c|]`, using
`|e^(i c lambda)-1|<=|c lambda|`. The same integration-by-parts argument gives

    error_U <=lambda b_N[1+2N(A_int+2J|c|)tau].            (7)

Inside the paired band the exact new on-site energy is
`-4J sin(c lambda)sin(k)/lambda` times N_k. It adds to the Bloch field

    h_z(k) +=2J [sin(c lambda)/lambda] sin(k).              (8)

Keeping this sinc coefficient gives an exact finite-lambda secular source;
replacing it by c has the explicit error
`|sin(c lambda)/lambda-c|<=|c|^3 lambda^2/6`. The paired-band quantum
product-marginal estimate is UNCHANGED: the extra on-site evolution cancels
when the exact state is compared with its mean-field product rays.

The REAL stability bound is unchanged as well. The detuning field is the
same rotation for the two compared solutions, and its contribution drops
out of the error-norm derivative. Label analyticity acquires the extra
explicit factor `exp(4J|c|sinh(eta)tau)`, so it still admits a compact
quadrature with paid c-dependent degree. The fixed executed consumer is
c=0; no additional detuning solver/grid/fixture was run or claimed.

This constructs the better mathematical question: which detuning-resolved
coherent fibers stay low-dimensional and mean-field admissible at the actual
interaction scale? Literal exact conservation is too fragile a selector.
The finite-N weak-coupling and initial-state costs in PROOF.md still apply;
this is not a justification of generic finite-temperature, fixed-coupling,
chaotic or thermodynamic-limit-first dynamics. A source-aware ordinary
degenerate-perturbation/pre-relaxation method can make exactly this repair.
No new generic predictive advantage is established.
