# Positivity frontier: exact characteristic theorem and compatibility obstruction

The unrestricted mixed-source/discriminant gate remains **OPEN**. No actual
compatible negative field was found. This worker derived an exact positive
theorem on a different amplitude-unrestricted mixed class and an exact
obstruction to any proof that retains only ordinary minor moments.

For each r>0, let σ=r+1, κ=r(r+2)/3, t=(2r+1)/3. Fix positive integers
m,n and h=σ(m/n)². Every periodic W^{1,4} pair with

    σ f_x+g_y=0,      g_x=-h f_y

is the sum of two independent characteristic profiles:

    f=F(mx+ny)+G(mx-ny),
    g=-(σm/n)F(mx+ny)+(σm/n)G(mx-ny).

No amplitude, concentration, frequency, orientation or smallness restriction
is imposed on F,G. Their canonical coordinate-separated first-potential
projection is constant, so nonzero maps in this class have R=0 and are
outside the N895 tube. The second potential is tied to the first by the two
displayed differential conditions; it is not arbitrary as in N888.

An exact moment representation and a positive-square interaction coefficient
give the sharp restricted discriminant bound

    P² <= 4 ρ_r(h) A Q,
    ρ_r(h)=2(r+2)²h/[9σ(σ²+2σh+t²h²)]
          <= (r+2)/[6(r+1)²] < 1/3.

Consequently every real conformal background satisfies

    E_r(s) >= (1-sqrt(ρ_r(h)))(Q+s²A).

Sharpness at fixed r,h is approached by a mean-zero skew two-valued single
profile; smooth profiles approximate the same supremum. At r=1 and m=n=1,
the ratio bound is exactly 1/8. The exact two-profile example in PROOF.md
has ratio 18/2185 and optimized positive energy 10835/128.

Here fixed h means an admitted h=σ(m/n)² on the square torus. If
sqrt(σ/h) is irrational the exact square-periodic plane has only constants.
The algebraic optimum h=σ/t is admitted only when sqrt(t) is rational;
otherwise rational slopes approach its value as a supremum. The sharp
profile bound itself is a supremum, not nonconstant attainment. Arbitrary
h>0 is separately realized on a rectangular torus with the matching aspect
ratio, as stated explicitly in PROOF.md.

The qualitative characteristic/diagonal class is classical. HKL Theorem 2.3
reconstructs Müller's diagonal gradient-measure theorem; their proof of
Theorem 2.4 verifies the relevant invertible left/right transformations.
This worker does not claim a new qualitative Jensen class or novelty
clearance. The restricted moment formulas and constant have been derived
here; historical originality and external correctness remain UNKNOWN.

The second result is a four-atom law ν with exactly EνV=0 and Eν det V=0,
and even pointwise U=0, c=-εb at every atom. Nevertheless

    ε Pν²/(4 Aν Qν) -> κ/[4σ J_r(diag(1,-σ))] > 0.

Thus the relaxed discriminant ratio is unbounded. For a fully rational
r=1 example the ratio is 274861129984/112607332451 > 1 and its background-one
energy is -93542709149/590295810358705651712. This is **not** a compatible
negative field. Its support reduces to diagonal matrices and classical
gradient-Young-measure structure excludes its realization. It decisively
rejects a moment-only Gram/Schur architecture, rather than the target
inequality. The ordinary minor-support obstruction was inherited; this
explicit law strengthens it to an unbounded-ratio family with all moments
and its non-realizability stated.

The exact unfinished continuation is PROOF.md (17): retain the entire U=0
class through f=ψ_y, g=-σψ_x and control its scalar Hessian cubic against
the unchanged quartic budget. The new theorem covers the wave-equation
slice σψ_xx=hψ_yy. Removing that slice loses characteristic independence;
a new signed interaction identity is required. Solving this restricted
Hessian inequality would still leave the general nonzero-U coupling.

The complex angular lower envelope was also tested and rejected exactly:
its left and right derivatives along a rank-one line at I are 5 and 3,
so it fails rank-one convexity. The coarse finite moment LP returned the
trivial law and supplied no continuum bound. Both failures are preserved
in FAILED_ROUTES.md and the diagnostic files.

The source checkout remains at 2688d7a383502df4fc1e64001d04bb76e6ec05e5.
N895/N888/N885, their decisive proofs, the supplied receiving audits and
the inherited exact scalar row-duality representation were read. No
producer executable was run. The new plane proof needs no Riesz or
compensated-interpolation premise; those tools retain their classical/prior
attribution. No concrete OpenAI Math transfer was found and none is forced.

`python3 check_exact.py` passes 43 exact identity/rational-example checks.
This verifies its enumerated algebra, not the continuum analytic arguments,
historical priority, formal verification, or unrestricted positivity.
One exploratory sampled LP used an already present SciPy dependency tree;
there was no installation, outreach, Git edit, or modification of source
originals. `SOURCES.json` records read paths/hashes and primary reading depth;
`FROZEN.json` hashes the authored files and preserves these exact limits.
