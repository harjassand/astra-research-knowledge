# Direct polyconvex closure of the principal quartic

The quartic

    F=u²+v²+3w²+16q²+4q(u−v)

is **polyconvex**, with a uniform compatible-gradient Jensen gap. Here
u=a²+c²,v=b²+d²,w=ab+cd,q=ad−bc for A=[[a,b],[c,d]]. This removes this
specific F from the unresolved QC target. It does not settle the full
nine-coefficient rank-one-convex/quasiconvex cone.

The independent path used a strong ordinary alternative: global
determinant-affine SOS support, rather than flow dissipation. The applicable
primary method is [Fantuzzi et al., *Polyconvexity with Moments and Sums of
Squares*, arXiv2604.11124v1](https://arxiv.org/html/2604.11124v1), §2.
The method is established; the exact support for this candidate was acquired
and reconstructed here.

## The actual construction

Set

    kappa(A)=(28297/5000)(u−v)+(57213/2000)q.

There is an explicitly saved rational 26-by-26 R with R>I/200 such that

    F(A+X)−F(A)−DF(A):X−kappa(A)det X = Z(A,X)^T R Z(A,X),

where Z contains all 16 products A_iX_j and all 10 products X_iX_j,i<=j.
The215 polynomial coefficient equations are exact. All 26 exact LDL pivots
of R−I/200 are positive. The matrix and constants are in
`EXACT_POLYCONVEX_SUPPORT.json`; the complete analytic proof is
`POLYCONVEX_PROOF.md`.

Consequently every bounded Lipschitz Omega, constant A, and
phi in W^(1,4)_0(Omega;R²) satisfy

    integral [F(A+Dphi)−F(A)]
       >= (|A|²/200) integral |Dphi|²+(1/400) integral |Dphi|⁴.

The same holds periodically. Mean gradients and determinant cancellation
remove the two support terms. A finite-valued convex lift is the supremum of the
explicit affine minor supports; its finiteness is proved using two graph
points with any desired average determinant. No compatible-gradient search,
restricted bandwidth, heat monotonicity or free acquisition oracle is used.
No efficient evaluation algorithm for that lift is asserted or needed.

For every fixed background B this also supplies the ordinary whole-profile
storage

    P_B(U)=DF_1(B).E U+(kappa(B)/2)E det(U,U').

It dominates every smooth compatible strip, with moving means retained.
N830's finite-jet rigidity permits exactly such a local storage for
polyconvex inputs. Its broader coefficient-linear-selection no-go is not
contradicted.

## Two structural interfaces beyond this one input

For a homogeneous planar quartic, any polynomial minor-support selector is
necessarily homogeneous quadratic. Otherwise scaling(A,X) simultaneously
makes its highest or lowest nonquartic term dominate with the wrong sign
for one sign of det X. Every homogeneous SOS residual then uses exactly
the 26 features above; increasing the polynomial degree cannot enlarge that
SOS existence class. Left-SO(2) averaging reduces the selector to
span(u,v,w,q), and the candidate's extra exact symmetries reduce it to
span(u−v,q).

`exact_interface.py` compiles any rational nine-vector to215 exact rational
equations with a26-by-26 PSD Gram and four multiplier coefficients, or two
when the extra symmetries hold. The general case has355 scalar unknowns;
this case has353. `EXACT_SUPPORT_INTERFACE.json` is the executed exact
interface for this F. Compilation is not a feasibility or QC decision.

This characterizes **polynomial SOS support**, not all polyconvexity. The
primary paper's Remark 2.1 explicitly leaves the2-by2 quartic gap between
polyconvexity and SOS polyconvexity open. No infeasible SOS is treated as
non-polyconvexity. No general bit bound, exact optimum or numerical
convergence guarantee is supplied.

A separate weighted-homogeneity argument proves that a homogeneous planar
quartic has a convex polynomial lift of any degree **if and only if**
H−c(det A)² is convex for some c>=0. For the present F, the diagonal Hessian
minor at I is

    (68−2c)(20−2c)−(64−4c)²=−12[(c−14)²+32]<0.

Thus the acquired strict SOS support coexists with failure of every convex
polynomial lift. The proof extends the weighted-scaling/Hessian mechanism
of the primary paper's Proposition 2.4; neither that mechanism nor the
existence of such representation gaps is claimed new.

## Retained failure and ordinary comparison

The cleared symmetric-bridge audit exactly excludes the constant-SPD
spatial heat/closed-quadratic/bilinear-SOS method for this F with all
nonnegative determinant-square removals. That was a sufficient-method
failure. The direct proof here resolves its QC status without repairing
that flow. The root's broader output-coupled-flow work is separate.

One short diagnostic tested whether the successful support might cover
the entire normalized trace-free orientation sector. At r=1.5,L=4 in
u²+v²+2r w²+tq²+Lq(u−v), ordinary full acoustic8 and support26 SDPs gave
minimum t values about11.2311116 and11.4395467. These floating results are
neither exact boundaries nor a non-polyconvexity/QC witness. They are
retained to prevent an unjustified universal extrapolation. No further
optimization of the F16 fixture was performed.

## Evidence and limits

`verify_support.py` is a standalone stdlib-only checker reading the final
rational JSON. It independently rebuilds the literal F polynomial and
its derivative, verifies the entire identity, reconstructs the shifted
LDL factorization, and checks the negative Hessian minor. It also replays
all 215 equations in the exported exact interface. No optimizer, numerical
Gram, SymPy generator or saved floating arrays are imported. Its receipt is
`VERIFY_SUPPORT.json`.

Initial acquisition used ordinary PSD/affine projection in NumPy:
62iterations in about.161s, followed by rational reconstruction in.176s.
The original exact support check took.043s; the final receipt records the
expanded check. Maximum pivot bit length is 263. Timings are in-process
measurements after interpreter/import startup. The analytic proof is
distinct from these finite verification checks. World novelty,
external specialist review and proof-assistant elaboration remain UNKNOWN.
No physical capability is claimed.

Fresh Astra main was pinned to
`6360a39d9488a041f259181e38c37e638b83c609`, explicitly newer than the initial
access pin `63867607218adef378d727987fd92aa7dc42eb5c`. N794/N797/N800/N830,
the relevant N803 and FR corrections, and the cleared symmetric audit were
read selectively. Their known slice closures, singular-face results,
contact-shear operation and universal-selector obstructions were preserved.
The exact source/read scopes are in `SOURCE_MANIFEST.json`.

No developing opportunity-route folder was read or influenced. No shared
source, Capital checkout, frozen earlier branch or external application was
modified. The larger nine-coefficient Morrey destination remains open.
