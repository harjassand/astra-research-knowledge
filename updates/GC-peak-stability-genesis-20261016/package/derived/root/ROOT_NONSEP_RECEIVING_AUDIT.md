# Root receiving reconstruction of the homogeneous compatible-positivity tube

2026-10-16; source pin `9dbe934e5475f415c2d160a6c0715534aafa546b`. Internal analytic reconstruction, not external verification. Candidate proof: `workers/gc_nonsep_genesis/PROOF.md`, SHA256 `c564e52914d70ba14000e1abadb17ac7432b04d19fd62cb0bfb159b6c8713b36`. The independent receiving report is `workers/gc_nonsep_adversary/A0_RECEIVING_AUDIT.md`.

The supplied theorem required a separated anchor with nonzero horizontal derivative. The new theorem is a relative neighborhood of the entire nonconstant coordinate-separated space, including pure vertical profiles, for the unchanged integrand and every scalar conformal background. This distinction changes the admitted function class. It does not settle unrestricted quasiconvexity.

## Exact analytic receiving argument

Fix r>0, sigma=r+1 and kappa=r(r+2)/3. Decompose f=f0+eta by coordinate averages, so f0=F(x)+H(y), and both coordinate slice averages of eta vanish. Define the real scalar Fourier correction p by p_hat=sigma mn eta_hat/(n²+kappa m²), and set g0=g+p. The zero mode is zero. If e=sigma eta_x-p_y and k=p_x, then e_y-kappa k_x=0 distributionally. This sign identity and slice cancellation give the exact orthogonal decomposition

    A(f,g)=A(f0,g0)+<e²+kappa k²>.

In particular, the full acoustic coefficient controls both anchor and perturbation; it is never replaced by a strictly positive horizontal Gram floor. The residual controls ||R_x eta_x||2 with factor Ca=max(1,kappa^-1/2)/sigma. All Fourier operators preserve real gradients and are bounded on the rough W1,4 class.

The precise classical input is the second-order Riesz bound on compact-type Lie groups, applied to a flat anisotropic torus at p=4. A diagonal matrix has bound3; the symmetric cross matrix has norm1/2 and bound3/2. See [Bañuelos–Baudoin, Theorem4.1(i)](https://arxiv.org/abs/1109.5751). This supports the uniform anisotropy constants actually required, rather than an unsupported Euclidean-to-torus import.

I reconstructed the cubic compensation step: for A=eta_x and B=eta_y, the multiplier A_tau=tau²n² A/(m²+tau²n²) satisfies ||A_tau||4<=3tau||Deta||4/2. The initial L2 difference is at most ||R_x A||2, and the dyadic difference is at most 3||R_x A||2/(4tau). Telescoping the absolute cubic costs

    1+3/2+(3/2)²+(21/8)(3/2)²=341/32<11.

The terminal cubic vanishes in L3. Hence <|eta_x|³><=11||R_x eta_x||2||Deta||4², with no finite cutoff. This is an explicit version of compensation already available qualitatively from N885; generic compensation is not newly claimed.

The exact conformal cubic is

    P=2aU²-(r+2)a²U+r c²U-2bcU-kappa a³-kappa ac²,
    U=sigma a+d.

For all terms except a³, expand once and pair one acoustic factor in L2 and the other factors in L4. The two exceptional first variations <a0² eta_x> and <a0² e> vanish by slice averages, without differentiating a0. The remaining a³ variation is controlled by the absolute cubic lemma and ||a0||2<=sqrt(A)/sigma. This last estimate is valid even when a0=0. The result is |P-P0|<=CP epsilon sqrt(A)(R+t+epsilon), R=||Df0||4, epsilon=||Deta||4, t=||Dg0||4.

The quartic derivative bound |DJ_r(V)|<=LJ|V|³ with LJ=6r/(r+2)+(2/3)r(r+1)+1+2r gives loss at most64LJD delta(R⁴+t⁴). Applying the inherited separated reserve to (f0,g0), retaining the exact acoustic residual, and using Young's inequality costs at most16CP²delta²(R⁴+t⁴)/mu. Thus

    delta<=min(1,1/D,alpha/(256LJD),sqrt(alpha mu)/(8CP))

makes both losses at most alpha/4 and proves

    E_r(f,g,s)>=alpha(R⁴+t⁴)/2+mu s² A(f,g)/2>0

for epsilon<=delta R and R>0. Subtracting this bound from the exact quadratic in s proves the restricted discriminant inequality; the A=0 case is handled directly, without division. Coordinate projection/complement norms at most2/3 give an actual ball of radius delta||Dh0||4/5 around every nonconstant separated h0.

At r=1 the independently reconstructed constants are mu=1/12288, L=9, D=10, CP=140 and LJ=19/3. Delta=1/40000000 satisfies the two absorption inequalities. The small radius is explicit and sufficient; optimization or a large radius has not been established.

## Adjudication

The analytic argument has no detected gap at the audited hash. Separate worker calculations corroborate the polynomial identities and rational absorptions; finite checks are not the universal proof. The result covers arbitrary g and real scalar s, every nonconstant separated anchor, and no derivative/frequency cutoff. It does not cover all affine backgrounds, all compatible first potentials, or a neighborhood of the constant anchor. A neighborhood at the constant anchor would, by scaling, imply the unrestricted scalar-conformal problem.

The separate positive counterfamily in gc_nonsep_adversary disproves same-g fixed-fraction energy domination at a pure vertical anchor. It does not refute the new theorem, whose compatible correction and retained acoustic term are essential. HKL's triangular-support theorem covers qualitative one-profile cases; the new relative tube admits mixed perturbations. The exact historical priority of this restricted theorem remains UNKNOWN.
