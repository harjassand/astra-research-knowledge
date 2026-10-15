# Critical storage: an exact reduced calibration and a three-mode refutation of its extension

15 October 2026. Source repository pin: `0c789ca775808e23e57138b56a393ad1e58cb15c`.

## Result first

1. The free phase/normal velocity can be eliminated exactly on the circular Fourier state family. This gives an algebraic, evaluable required-supply storage, valid for **all coefficient paths in that family**, not only monotone radial paths. It has an explicit finite-width approximation and cost.
2. That storage **cannot dominate all compatible strips even when both endpoint traces are circular**. A concrete compatible perturbation with only physical Fourier modes `{1,2,4}` strictly lowers its incoming action. An exact algebraic second-variation identity and a conservative finite-amplitude remainder certify the strict improvement. This is a symmetry-breaking counterexample to extending our restricted calibration, not to quasiconvexity.
3. Optimizing the supplied heat primitive over free normal jets gives `+infinity` and `-infinity` already at the zero profile. Worse, these divergences occur along zero-trace compatible collars whose W1,4 derivative energy and G action tend to zero. An action-only or W1,4-energy-only penalty cannot repair that primitive optimization.
4. The reusable alternative operation is a **compatible mode-instability compiler**: conjugate an exponential Fourier extremal into a constant-coefficient second variation, search integer relative modes, then turn a negative algebraic symbol into a finite-strip polynomial-cutoff competitor with a certified quartic remainder. This advances the actual storage evaluation problem by rejecting an otherwise exact but false reduced calibration and generating strict certified primal improvements.

The full critical-trace required supply remains unidentified. No convergent full-space primal/dual algorithm, uniform rough-ball Lipschitz estimate, or strict coercivity is claimed. Historical novelty and external mathematical review remain unestablished.

## 1. Definitions and trusted prerequisite

Write A=[[a,b],[c,d]], u=a²+c², v=b²+d², j=ad−bc, and

G(A)=3(u+v−2j)²+(35/24)u²+j²−(5/2)ju.

The source heat certificate gives all-background quasiconvexity of this G using d1=4897/5000, d2=5103/5000 and a closed quadratic two-form Ω. Its exact compatible-jet identity is

d1 D²G(A)[A_x,A_x]+d2 D²G(A)[A_y,A_y]+Ω_A(A_x,A_y)=ZᵀQZ≥0.

Closedness, the primitive α=(1/4)i_EΩ, periodic Stokes and elliptic heat decay yield the compatible Jensen inequality. We use that already-supplied result for closed-loop lower bounds; the new calculations below do not duplicate the full heat Gram verification. The copied JSON is used directly to check the two coefficients needed for our primitive obstruction.

For general B define f_B(A)=G(B+A)−G(B)−DG(B):A and

p_B(U)=inf_{T>0, Φ(0)=0, Φ(T)=U} ∫_0^T E_y f_B(DΦ) dx,

where E_y is normalized average on R/(2πZ), Φ is W1,4 and U∈W3/4,4. The source proves finiteness, mean invariance and strong continuity. This report's construction and counterexample take **B=0**, so f_0=G. The mean of every displayed trace is zero. For any actual incoming path I and return path R, closed-loop QC gives

−J(R) ≤ p_0(U) ≤ J(I).

Neither endpoint of that bracket alone is asserted to be a dominating storage. In particular, the negative action of an arbitrary return is not a storage formula.

## 2. Exact finite-Fourier state system

Fix an integer n≥1. Let R_θ be positive planar rotation, J=R_{π/2}, and define the two-real-dimensional trace family

E_n={U_z(y)=R_{ny}z : z∈R²}.

Allowed reduced trajectories are Φ(x,y)=R_{ny}z(x), with arbitrary W1,4 z(x). This means the whole path remains in E_n, a restriction stronger than merely imposing endpoint traces in E_n.

At r=|z|>0 write z=rR_θe1, p=r′, t=rθ′, q=nr. Left rotational invariance gives

G(DΦ)=L(p,q)+C(p,q)t²+(107/24)t⁴,

L(p,q)=(107/24)p⁴−(29/2)p³q+19p²q²−12pq³+3q⁴,
C(p,q)=(107/12)p²−(29/2)pq+6q².

The discriminant of C as a quadratic in p is −(15/4)q². Hence C is positive definite, and **every phase velocity is eliminated by the exact minimum t=0**. This is not a numerical minimization.

Put a=107/24, b=29/2 and h(k)=L(k,1). Let κ be the unique positive root of

P(k)=107k⁴−232k³+152k²−24=0.

Our exact rational isolating interval is

890923272145/10¹² < κ < 890923272146/10¹².

Set c=h(κ)/κ. Then the polynomial identity

h(p)−cp=(p−κ)² [a p²+(2aκ−b)p+3/κ²]

holds modulo P(κ)=0. The quadratic factor is positive definite; the verifier checks this using rational interval bounds, not floating eigenvalues. Thus L(p,q)≥c q³p for every real p and q≥0. Consequently

S_n(U_z)=(c/4)n³|z|⁴

satisfies S_n(z_1)−S_n(z_0)≤J(Φ) for every reduced trajectory, including phase rotation, nonmonotone radius and crossings through r=0. At r=0 the pointwise inequality follows directly from G([z′|0])=(107/24)|z′|⁴.

Numerically κ=0.8909232721454511 and c/4=−0.0154195263461755. These decimals are illustrations; the algebraic root and positive-factor certificate are the definition and proof.

### Exact attainment as an infimum and finite cost

For a target radius R>0 and 0<ε<R, use a linear seed from 0 to ε over width 1/n, followed by r′=κnr from ε to R. The action is exactly

S_n(R)+n³ε⁴(137/120−c/4),

and width is

T=(1+κ⁻¹ log(R/ε))/n.

The error tends to zero, proving S_n is the reduced required supply. This gives a logarithmic-width realization for any requested positive additive error. No finite optimizer from zero is asserted.

The negative real root k_- of P lies in (−318411269741/10¹²,−318411269740/10¹²). Repeating the positive-factor identity gives the reduced available-storage endpoint (h(k_-)/(4k_-))n³R⁴=−7.27140247594587 n³R⁴. The corresponding optimized return has positive action 7.27140247594587 n³R⁴. A small terminal linear cap has exact coefficient 2597/120 and an O(n³ε⁴) remainder. These produce a valid but wide **full-space bracket**, not an identification of full p_0.

## 3. Exact symmetry-breaking refutation

Take n=1, R=1. On x≤0 the reduced extremal is Φ₀=e^{κx}R_y e1. Its gradient in the rotating frame is e^{κx}diag(κ,1). The full Euler–Lagrange residual is

3κ DG(diag(κ,1))_1 + J DG(diag(κ,1))_2
  = ((107κ⁴−232κ³+152κ²−24)/2,0)=0.

For a compactly supported perturbation

H(x,y)=e^{−κx}R_y ζ(x,y),

the Hessian's homogeneity cancels the exponential weights. If H0=D²G(diag(κ,1)), the second variation is the constant-coefficient form with columns

[ζ_x−κζ | ζ_y+Jζ].

This gives a reusable 2×2 Hermitian Fourier symbol: set ζ=e^{iξx+imy}v, use columns [(iξ−κ)v | (imI+J)v], and evaluate H0. A negative eigenvalue is a candidate only until compactification and remainder control are done.

### An exact negative direction

Use m=3 and the real polarization

ζ(x,y)=η(x)(4cos(3y),−3sin(3y)).

The physical perturbation R_yζ has only frequencies 2 and 4. Thus the perturbed potential has only frequencies 1,2,4.

After averaging over y, the second variation density is

αη′² + γηη′ + βη²,

α=(2033/4)κ²−(1653/2)κ+358,
β=(2033/4)κ⁴−2088κ³+3541κ²−2916κ+936.

The unneeded constant γ drops out because ∫ηη′=0. Set s=x+10 and η=s(10−s) for −10≤x≤0, zero elsewhere. This is an admissible Sobolev cutoff. Then ∫η′²=1000/3 and ∫η²=100000/30. Rational interval evaluation at the isolated algebraic root gives

I₂=(1000/3)α+(100000/30)β < −16000.

This is an exact sign certificate. The floating values β≈−7.63208 and the m=3 symbol's lowest eigenvalue≈−0.610936 are not used as proof.

### Finite-amplitude, finite-width field

Set λ=10⁻¹⁶. Since the angular perturbation changes sign under a relative angle shift π/3 while the baseline rotating-frame gradient is constant, the first and third averaged action coefficients vanish exactly. Therefore

J(Φ₀+λH)−J(Φ₀)= (λ²/2)I₂+λ⁴ J(H).

The elementary bound |G(A)|≤15|A|⁴ holds for all A. On the width-10 support, κ<0.9, η≤25, |η′|≤10, |ζ/η|≤4 and |(∂y+J)(ζ/η)|≤9. Hence |DH|≤260e⁹. Using e<11/4 gives the exact conservative estimate

|J(H)|≤150·260⁴·(11/4)³⁶ <10²⁸.

Now start the incoming path with a linear seed of radius ε=10⁻⁹ over width 1, then the exact exponential up to radius 1. Its exponential duration log(10⁹)/κ exceeds 10, so the perturbation fits in its final width-10 portion and vanishes at both ends of that portion. The seed overhead is less than 2·10⁻³⁶. The total action therefore obeys

J_total < c/4 −8000·10⁻³²+10²⁸·10⁻⁶⁴+2·10⁻³⁶
        < c/4 −7·10⁻²⁹.

Every endpoint condition is exact; the entire field is W1,4 and periodic, and its total width is 1+log(10⁹)/κ. The conservative gap is tiny but strictly certified. It is an existence/refutation certificate, not a claim of numerical conditioning or practical optimality.

Thus

p_0((cos y,sin y)) < S_1((cos y,sin y)).

In particular, the exact reduced S_1 fails domination on this incoming strip. This is the decisive reason not to promote the reduced mode elimination to a profile-only storage for all paths. G's closed-loop QC and the source's finite-storage theorem remain consistent and untouched.

## 4. A stronger obstruction to optimizing the actual heat primitive

The copied exact JSON gives, on b=d=0,

Ω_02=(788811/20000)a²+(98601/2500)c².

For zero profile U=0 and normal jet M(cos y,sin y), the normalized primitive circulation is

C_α M⁴,  C_α=1577619/160000.

Reversing winding changes its sign. Therefore raw sup/inf over just the first Fourier normal jets is already ±infinity at U=0.

This is more than a change-of-jet example. Let ψ(s)=s(1−s)² and define, on a width δ collar,

Φ_M(x,y)=Mδ ψ(x/δ)(cos y,sin y).

Both profile traces are zero. The initial normal jet is M(cos y,sin y); the terminal normal jet is zero. Exact integration gives

J(Φ_M)=M⁴δ[107/420−29δ/840+19δ²/1386+δ⁴/2145].

Take δ=M⁻⁶. Then J→0 and ∫|DΦ_M|⁴→0, but the initial circulation is C_αM⁴→infinity. Negative winding gives the negative divergence with the same norm bound. Consequently no finite bound of the form

|circulation|≤C(U)+K∫|DΦ|⁴,

or with any penalty remaining bounded as that derivative energy tends to zero, can hold on these compatible collars. An analogous action-only bound fails too. A primitive-gauge change does not help because closed-loop integrals are gauge invariant.

This excludes raw free-jet optimization and bounded energy penalties for this primitive. It does **not** exclude a time-integrated heat construction, a strengthened state carrying jets with appropriate regularity/cost, a different boundary functional, or variational required supply.

## 5. Continuum and a posteriori error contracts

The restricted calibration extends continuously only along E_n; it is not assigned to arbitrary traces as a storage. The three-mode counterexample is already a continuum compatible field, so it needs no frequency extrapolation.

For legitimate full-space upper/lower bounds, use actual incoming/return paths. Their exact polynomial or exponentially weighted polynomial integrals can be evaluated with outward-rounded intervals. Quartic G makes a strong derivative approximation contract explicit:

|J(Φ)−J(Ψ)|≤60 (||DΦ||₄+||DΨ||₄)³ ||DΦ−DΨ||₄.

This follows from the source bound |DG(A)|≤60|A|³ and Hölder. It allows a numerical Fourier/FEM path to be converted to a certified primal bound if its derivative error is genuinely bounded. It is not an energy-to-gradient coercivity estimate.

For trace perturbation W=U+δU around a smooth finite-Fourier U, use the periodic Poisson extension EδU(t)=e^{−t|D_y|}δU and a connector of width τ:

Φ(x,y)=U(y)+(1−t/τ)EδU(t,y),  t=τ−x.

Its initial trace is U and terminal trace W. Write

H=8τ||U_y||₄⁴+64∫₀^τ E|D EδU|⁴dt+64τ⁻³||δU||₄⁴.

The product rule, |a+b|⁴≤8(|a|⁴+|b|⁴), and L4 contraction of Poisson extension give ∫|DΦ|⁴≤H. Reflection gives the reverse connector with the same derivative norm. Consequently

|p_0(W)−p_0(U)|≤15H.

This is an explicit **paid extension-tail** contract. For finite Fourier δU, all extension terms are finite sums of exponentials and angular polynomials and are evaluable. For rough continuum δU, a certified bound on its displayed extension integral and L4 norm must be supplied. The Besov trace-extension estimate makes H→0 by a suitable τ→0 when δU→0 in W3/4,4. No finite sample determines that tail automatically. No rough-ball uniform Lipschitz claim is made.

Combining this connector with the incoming/return bracket transports certified full-space bounds to nearby continuum traces. The width of that bracket is not proved to converge to zero; this is the honest remaining obstruction after the reduced formula has been disproved.

## 6. Prior-art comparison and scope

- J. C. Willems, “Dissipative dynamical systems, Part I: General theory,” Arch. Rational Mech. Anal. 45 (1972), 321–351, DOI https://doi.org/10.1007/BF00276493. The required-supply/available-storage framework and extremal storage interpretation are prior art. The publisher abstract was inspected; the author's PDF endpoint timed out, so no claim of full-text verification is made. Our new contribution is not the Bellman/storage definition.
- Giuseppe Bruno and Federico Pasqualotto, “Quasiconvexity for the Dacorogna–Marcellini Energy,” https://arxiv.org/html/2608.06367v1, particularly Sections 2–3. Their heat monotonicity and exact-two-form correction method is prior art. It does not justify deleting the normal jets of an open-strip primitive. We use the source's specific G heat certificate only for its already-proved QC premise.
- Ariel Barton, “Trace and extension theorems relating Besov spaces to weighted averaged Sobolev spaces,” https://arxiv.org/abs/1604.00058. This is primary trace-extension literature, not a new regularity theorem supplied here. The standard p>1 trace/extension machinery underlies the paid Poisson-extension contract; our numerical evaluation still needs a verified tail.
- Repository sources: `updates/FT-direction-transport-20261015/RESEARCH_HANDOFF.md`, `synthesis/cartesian_elimination/G_CRITICAL_STORAGE_SCOPE.md`, `root/G_HEAT_IMPLICATION_AND_COMPATIBILITY.md`, and `synthesis/nonlinear_qc/G_QUASICONVEXITY_PROOF.md`, all under the same pinned update prefix. The source already establishes finite continuous storage and primitive jet dependence. This report strengthens the latter to energy-unboundedness, constructs an exact reduced calibration, and then refutes its full-space extension with a finite compatible three-mode field.

## 7. Replay and next mathematical operation

Run `python verify.py` in this directory. It checks phase elimination, algebraic factorization, root isolation, positive quadratic cofactors, seed/collar integrals, actual Ω coefficients, the EL identity, exact second-variation coefficients, a rational negative bound, and finite-amplitude remainder arithmetic. SymPy is the only dependency; floating numbers are descriptive, not acceptance gates.

Next useful work is to use the constant-coefficient symbol as a compiler for further certified primal improvements, or to build a genuinely full-state HJB/subsolution certificate including the destabilizing frequencies. Restricting to the circular state family again, or merely computing its radial optimum more accurately, cannot solve the original storage problem.
