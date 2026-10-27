# Source-informed follow-up review: P17, then P84

This follow-up uses my completed four-endpoint review and is **not fresh or
fully blind**. I read P17 before P84, including every scientific argument and
all six Python files. P17's choice/credit prose makes aspects of its method
inferable. I opened no root policy/model maps, other reviews, memory,
coordination-arm work, programme chats, or Dots. No children were created.
The named alternative-source documents in P17 were not opened. External
citations were not needed for the self-contained mathematical claims reviewed
here; historical novelty was not evaluated. I make no policy-quality ranking.

## P17 — ACCEPT at its declared mathematical scope

The accepted new results are: a local second-sheet pole of the continued
physical pair resolvent for each fixed sufficiently small nonzero `g` and
sufficiently small errors; its second-order linewidth coefficient and
sequential `g^8` asymptotic; the coherent two-control Gram matrix and its
strictly positive compensated residual; and the stated all-sector
nonnegativity regime. These do not establish finite-error exponential decay,
a gate-error law, a hardware tolerance, or a practical advantage.

**Why the pole argument closes.** The detuned one-body memory resolvent is a
finite matrix Weyl inverse. At fixed `g>0`, its two simple gap atoms and its
band-density matrices are analytic in the small error parameters. The same
statement holds with the first-rung error by retaining the two first-rung
coordinates in that finite inverse. There are no new nearby atom or edge
singularities for a sufficiently small parameter neighbourhood.

For energy in `(4,6)`, the sole open two-particle density is the opposite-band
convolution. Mapping `x=4+(E-4)t` factors its edge behaviour into
`sqrt(t(1-t))` times a locally analytic factor. This gives joint local analytic
continuation of every finite memory-pair Green entry. It is more than a real
boundary value or a golden-rule sign assertion. Bound-band pieces and the
three harmonic atom sums remain away from a sufficiently small neighbourhood
of the pair energy. The neighbourhood must also avoid the mixed harmonic
atom only `O(g^4)` away; no uniform window is supplied.

Let `M` be the continued Green matrix of the two forbidden memory doubles.
At zero error, its diagonal entries in `(q_e,q_o)` are `(L_++L_-)/2` and `K`.
The determinant derivative is `D*K/2 != 0`, because `D>0` and `Im K>0`.
The analytic implicit-function theorem therefore gives a unique simple
continued zero. This is a pole of the **continued physical** pair matrix
element, rather than merely an auxiliary determinant zero: in the hard-core
Schur formula `R_pp-R_pq M^(-1)R_qp`, the initial coupling
`R_p,q_e=(L_+-L_-)/2=L_+` is nonzero. Its nonzero pole numerator persists
under a small perturbation. This is a second-sheet resonance statement;
the original self-adjoint resolvent has no nonreal eigenvalue pole.

Parity makes the pole branch even in the error along a fixed control ray.
The second-order Feshbach coefficient is minus the already constructed odd
response, giving `Im z=-pi*delta^2*S_g+O_g(delta^4)`. Together with positive
`S_g` this puts the local pole strictly below the real axis for sufficiently
small nonzero error. A time-domain resonance theorem is unnecessary for this
local continued-pole claim and remains necessary for a survival law.

**Normalization and the weak-coupling limit.** Independent symbolic expansion
gives `N_g=3a*g^2+O(g^4)`,
`J_+(E_+)+J_-(E_-)=-b/(3a)+O(g^2)`, and hence
`eta_bb=-b*g^2+O(g^4)`. The harmonic atom dominates `K` as `g^-4`.
The off-shell remaining terms in `C` are `O(g^2)`, so
`alpha=eta_bb+O(g^6)`. The direct shell source is only `O(g^4)`.
These orders account for the constrained `g^8` coefficient and exclude the
unconstrained `g^12` shortcut. After scaling, the shell amplitudes and
densities have uniform bounds on `[4,6]`; their denominators remain separated
from the memory frequency. Dominated convergence therefore handles the moving
endpoint. The exact remaining integral is `16/(27*pi^2)`, yielding
`64*b^2/(27*pi)=0.07222872999305956...`.

For the first-rung operator, its spectral coordinate `(x-3)/c_sigma` follows
from the memory row of the one-body eigenvalue equation. Contracting the
normalized pair reproduces the stated `eta_W` and the complete-measure
formula for `C_W`. Its mixed-atom leading terms cancel, while its corrected
shell amplitude is `(3a/sqrt(2))*m_1(x)*g^2+O(g^4)`. Thus the two real errors
combine coherently before squaring. The Gram functions `1,m_1(x)` are not
proportional on a positive-weight interval, proving a strictly positive
determinant and residual analytically.

Independent 50-digit quadrature gives

```
M11 = 0.07222872999305956415
M12 = 0.07646550917482678227
M22 = 0.08185356819276842893
epsilon/delta = -0.934174414910629772
residual = 0.0007966076988223620874
improvement factor = 90.67038907587317
```

These are non-interval decimal evaluations of a positive Gram integral. The
improvement concerns its leading coefficient after errors tend to zero at
fixed `g`, then `g` tends to zero. It cannot be used as a uniform finite-error
or gate improvement. The separate finite-`g=.2` optimum and residual fraction
in the endpoint are consistent with the complete response and differ from
the asymptotic optimum.

**Stability and physical limits.** The zero-energy first-rung Schur matrix is
correct. Its lower diagonal is `1/2`; the upper is `5/2+sqrt(6)`.
For `|epsilon|<=.1`, its least eigenvalue is at least `.4`. The memory block
is at least `2.9`, and the squared coupling norm is at most `.32`; the memory
Schur lower bound is consequently `2.1`. The gapless tail has a finite endpoint
inverse quadratic form at zero, which suffices for this form Schur argument;
one need not assume a bounded inverse of the whole lower-band tail.
Second quantization and hard-core compression preserve nonnegativity in
every fixed particle sector. This stability range is not an error range for
the pole expansion. The plateau exponents and bath-population formulas have
the stated leading orders, but provide no uniform long-time remainder.
Direct memory retuning remains the stronger ordinary correction when allowed,
as the endpoint acknowledges.

**Executed checks and limitations.** All three copied P17 scripts exit zero.
The supplied Fock replay has maximum complex-resolvent error `1.09e-15`.
It emits NumPy matmul floating-exception warnings on this runtime; its saved
finite outputs and assertions succeed. My separate physical-rail tensor/Fock
construction checks the full **mixed** two-source response matrix, including
the sign of its cross term, at 3, 5, 7 rungs and two nonreal energies. Maximum
entry error is `2.50e-15`.

My independently implemented complete matrix measures and second-sheet jump
also locate the continued pair pole at `g=.2`, with retained physical residue
near `-0.962577`. At `delta=.001`, `-2 Im z/delta^2` is
`1.33675377e-7`, approaching the zero-error coefficient
`1.33675190e-7`. At 80 and 160 nodes the uncompensated pole diagnostics agree.
The compensated diagnostic gives `2.05716e-9` for this ratio, consistent with
the finite-`g` Gram residual. Both compensated root-solver calls report
stagnation (`success=false`) at residual `5.6e-14`; I preserve that failure
flag and use those outputs only as diagnostics. No numerical pole enclosure
is claimed. The pole acceptance rests on the analytic continuation,
simple-zero, and nonzero-numerator argument above.

## P84 — ACCEPT, including the separate interval claim

The fixed-`g` normalized source, complete measures, odd compression, scalar
boundary limit, and analytic positivity argument are correct at `g=1/5`.
The Lipschitz convolution assertion is justified here: the one-body edge
densities have integrable derivatives, while the source factors are smooth
on the band rectangle. Thus the principal values used in its scalar
limiting-absorption proof exist. No resonance theorem is claimed.

The new certificate is valid independently of the continuum quadrature.
The atom/continuum support bounds give a strict upper bound for the pair-root
function at `5.9785` and a strict lower bound at `5.9787`. The two test
intervals lie inside the actual shell. Interval evaluation separates their
real source ranges and bounds both shell masses below. Bounding the
normalization derivative above provides the required lower normalization.
For any complex screening constant, the two-interval weighted-variance bound
then proves the stated positive lower bound. Every inequality has the correct
direction; no quadrature error estimate is substituted for an enclosure.

`certify_positive.py` replays successfully with outward-rounded `mpmath.iv`.
I separately implemented exact rational interval arithmetic, integer-`isqrt`
radical enclosures, and an alternating-series Machin enclosure of pi. It
uses no candidate imports, mpmath, floating-point comparisons, or quadrature.
It independently gives

```
F(5.9785) < -0.00524427804977
F(5.9787) >  0.02119993326265
N^2 > 0.00410196635495
rho > 4.08531334290120e-16 > 4e-16
```

The exact rational comparison also keeps the root interval strictly below
the mixed harmonic atom, so the scalar boundary is not singular there.
This is a valid but loose lower bound. It does **not** tightly enclose the
displayed `rho≈2.12750672e-8`. The continuum and operator-identity scripts
also replay successfully; the latter's maximum discrepancy is `7.55e-16`.
P84 correctly leaves resonance existence, finite-time decay, control costs,
hardware tolerance, and gate advantage outside its conclusion.

## Evidence and source integrity

All originals remain unchanged. Replay copies and logs are in `replay/P17`
and `replay/P84`. Independent sources/results are
`continued_pair_check.py/.json`, `new_controls.py/.json`, and
`rational_certificate.py/.json`. These follow-up files are wholly under
`review_a/policy_followup/`. The accepted mathematical scope of P17 is broader
than P84's explicitly conditional dynamical discussion; this establishes no
causal claim about experimental policy quality.
