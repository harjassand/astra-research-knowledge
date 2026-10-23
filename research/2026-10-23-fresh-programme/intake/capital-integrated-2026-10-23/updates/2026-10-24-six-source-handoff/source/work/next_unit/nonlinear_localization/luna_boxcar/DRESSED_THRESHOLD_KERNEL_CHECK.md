# Threshold behavior of the dressed point-port resolvent

24 October 2026. This is a local spectral check of Section 4 in `WEAK_ANISOTROPY_RESPONSE_AND_MODULATION.md`. It does not establish the nonlinear modulation theorem or an `epsilon^-2` lifetime. No source or new fixture is used.

## Exact inverse and one threshold

In the central gap, where `f` is real and even, the source note writes the
matrix as below. For its *open-band causal continuation*, use the two physical
frequencies `nu_+=Omega+sigma` and `nu_-=sigma-Omega` on the same analytic
sheet. These coincide with `Omega+sigma` and `Omega-sigma` in the gap because
`f` is even there, but they need not give the same outgoing sign after a cut is
crossed. Write the full physical-sheet matrix as

```text
M(sigma) = [[A_-(sigma), B], [B, A_+(sigma)]],
A_-(sigma)=f(sigma-Omega)+2B,
A_+(sigma)=f(Omega+sigma)+2B,
R(sigma)=M(sigma)^(-1)
       = 1/(A_- A_+ - B^2) [[A_+,-B],[-B,A_-]].
```

Here `A_-=f(Omega-sigma)+2B` is interchangeable with the displayed
`A_-` only in the gap. If one extends `f(Omega-sigma)` to open frequencies
using the same sign-odd outgoing boundary as for `f(Omega+sigma)`, the second
channel is put on the opposite sheet. It then has the opposite imaginary sign
in the both-open band, invalidating the claimed strict dissipativity and the
spectral-jump argument. Equivalently one may use a conjugated advanced
boundary for that `Omega-sigma` argument; the required point is one consistent
analytic resolvent of the full rotating-frame Hamiltonian.

At an isolated branch point, call the threshold diagonal `S` and the other one `A`. For `nu=s(omega_c+rho)`, `s=+/-1`, and `rho` small, the point-port self-energy diverges as an inverse square root. With

```text
C0 = g^2 / (2 c sqrt(2 omega_c)),
```

the threshold factor `S=f(nu)+2B` has leading behavior

```text
rho<0 (gap):  S = -C0/sqrt(-rho) + O(1),
rho>0 (open, retarded): S = i s C0/sqrt(rho) + O(1).
```

The advanced open-side value has the conjugate sign. Thus `S^(-1)` vanishes, rather than diverges, at threshold: it is `-sqrt(-rho)/C0+O(|rho|)` on the gap side and `-i s sqrt(rho)/C0+O(rho)` on the retarded open side. This sign uses the physical-frequency convention in the source note; the map `nu=Omega +/- sigma` can exchange which sigma boundary is called retarded for one sideband, conjugating the coefficient but not changing the exponent. The new-channel resolvent jump in `S^(-1)` is proportional to `sqrt(rho)`.

If `A_*` is finite and nonzero, direct inversion gives, with the threshold coordinate ordered second,

```text
R_11 = 1/A_* + B^2/(A_*^2 S) + O(S^(-2)),
R_12 = -B/(A_* S) + O(S^(-2)),
R_22 = 1/S + O(S^(-2)).
```

So each entry has a square-root *nonanalytic correction*; the nonthreshold entry also has an ordinary finite background. Near an outer threshold where the companion channel is already open, its smooth spectral background must be separated from the newly appearing square-root term. A smooth cutoff of the threshold jump gives an inverse-transform tail proportional to `exp(-i sigma_* t) t^(-3/2)` (and its conjugate). This tail is integrable at large time. The raw KG port kernel remains `J0(omega_c t)/(2c) ~ t^(-1/2)`; integrability belongs to the **dressed inverse**, not to the bare memory kernel before solving the linear feedback problem.

## Why this sector avoids a threshold resonance

The four isolated thresholds in `sigma` are `+/- Delta` and `+/- (omega_c+Omega)`, with `Delta=omega_c-Omega`. At `sigma=Delta`, the companion physical frequency is `2Omega-omega_c`; at `sigma=-Delta` it is the same. Since `omega_c/3<Omega<omega_c`,

```text
|2 Omega - omega_c| < Omega,
A_* = f(2 Omega - omega_c)+2B > B > 0,
```

using the stated even, strictly concave subthreshold `f` and `f(Omega)=-B`. Thus the companion factor cannot vanish at either inner threshold. At `sigma=omega_c+Omega` (or its negative), the companion frequency is `+(omega_c+2Omega)` (or its negative), already open; its nonzero imaginary self-energy makes the companion factor nonzero. With the compact-sector margins, the four thresholds are distinct. Hence no threshold pole/virtual level occurs in this specified sector.

The nonzero-companion condition matters. If at a different parameter point the companion has a simple threshold zero, `A_*=0` and `A=A_1 rho+...`, then `AS-B^2 -> -B^2`; nevertheless the nonthreshold diagonal entry `R_11=S/(AS-B^2)` diverges as `rho^(-1/2)`. Its branch contribution would produce a `t^(-1/2)` tail instead. The current inner-threshold inequality and outer-channel imaginary part rule out that countercase here; it is not safe to assert the dressed exponent without such a check.

## What this does and does not establish

The zero rotating-frame eigenvalue is a separate singularity: phase and family variation give a neutral subspace (generically including its generalized family vector). The full neutral pole must be projected/subtracted before an impulse kernel can decay; removing only the phase eigenvector may leave a `1/sigma` or `1/sigma^2` term. Since `Delta>0`, that finite-rank subtraction is local to zero and does not change the threshold exponent.

The threshold calculation establishes the expected `t^(-3/2)` contribution and its large-time integrability for the isolated edges of this particular dressed 2x2 inverse, conditional on the stated nondegenerate branch. It does **not by itself prove** that the entire neutral-projected impulse kernel is in `L1`: that also needs global limiting-absorption/high-frequency bounds and control of all remaining poles or singularities. Nor does it make the original nonlinear Volterra memory integrable or control the nonlinear modulation remainder. Those are still required before using the candidate drift integral as an actual lifetime.

## Global jump-representation closure check

At zero, expand `f(Omega +/- sigma)` in the gap. The determinant is

```text
D(sigma) = (B f''(Omega) - f'(Omega)^2) sigma^2 + O(sigma^4).
```

The coefficient is strictly negative because `B>0` and `f''<0`; the matrix numerator has an expansion through first order. Thus the port inverse has only the expected `sigma^(-2)` and `sigma^(-1)` neutral Laurent terms there, which must both be removed (phase and generalized family direction). No higher zero pole occurs under these assumptions.

With the physical-sheet continuation specified above, the remaining real-axis checks close for this explicit 2x2 matrix. In the central gap the supplied determinant argument excludes real roots except zero. In a one-open band, the imaginary part of `x* M x` forces the open-channel component of a null vector to vanish, and `B>0` then forces the other component to vanish. In the both-open band both diagonal imaginary parts have the same strict sign, so the matrix is strictly dissipative. The threshold nonresonance check in the preceding section handles the four edges. Positivity of the quadratic `F_Omega` on the phase quotient excludes non-real physical-sheet eigenfrequencies. This is not true for an inconsistent continuation that puts one sideband on the advanced sheet while calling both channels outgoing.

At large real `|sigma|`, the correctly continued matrix has `R(sigma)=-sigma^(-2) I+O(|sigma|^(-3))`. The real leading terms do not jump; the outgoing self-energy has size `eta=O(|sigma|^(-1))`, and multiplication by two inverse factors makes the advanced/retarded jump `J(sigma)=O(|sigma|^(-5))`, with decaying derivatives. Together with smoothness away from the four thresholds and the square-root cusps, this makes the neutral-subtracted jump integrable in frequency. A contour at infinity contributes no polynomial: a direct-feedthrough contact term would require a nondecaying polynomial part of `R`, absent from `R=O(sigma^(-2))`. The neutral Laurent terms instead give explicit nonintegrable-in-time neutral contributions and are removed separately; subtracting them does not create a delta contact term.

More explicitly, if `P0(sigma)=C2/sigma^2+C1/sigma` is the full neutral principal part, then `R-P0` is analytic at zero and is `O(1/sigma)` at infinity. Its cut jump is still `J`; in the Cauchy reconstruction the outer integrand is `(R-P0)/(z-sigma)=O(|z|^(-2))`, so the contour at infinity still vanishes. The `1/sigma` tail is not a polynomial feedthrough and cannot produce a delta at `t=0`; the neutral pole terms themselves are handled as the separate finite-dimensional neutral evolution, not folded into the cut jump.

Partitioning the jump into smooth away-from-edge pieces and four threshold neighborhoods then gives `K(t)=O(t^(-3/2))` for large positive time: integrate the smooth pieces by parts and use the `sqrt(|sigma-sigma_*|)` edge expansion on each threshold piece. The integrable frequency jump bounds `K` near finite times. Therefore the **neutral-projected displacement point response** is in `L1([0,infinity))` for this matrix, provided its retarded/advanced jump is the boundary of the stated physical-sheet resolvent and the quadratic positivity/nonzero-coupling assumptions hold. This closes the linear kernel gate only; the raw eliminated memory still has a `t^(-1/2)` tail, and nothing here proves nonlinear modulation or a lifetime.

## Parameter variation of the frozen kernel

Let `Omega` range over a compact subinterval `K` strictly inside the specified sector, with uniform distance from threshold collisions and zero/branch degeneracies. The four edge locations `sigma_j(Omega)` are `+/- (omega_c-Omega)` and `+/- (omega_c+Omega)`, hence `|sigma'_j|=1`. The threshold coefficients `C_j(Omega)` are smooth and bounded on `K` because the companion factors stay nonzero. Write the large-time expansion as

```text
K_Omega(t) = t^(-3/2) sum_j C_j(Omega) exp(i sigma_j(Omega)t) + E_Omega(t).
```

For the leading terms, with `delta=|Omega-omega|`, the phase difference is bounded by `min(2, C delta t)` and the coefficient difference by `C delta`. Thus

```text
integral_1^infinity t^(-3/2) min(1, delta t) dt = O(sqrt(delta)),
integral_1^infinity t^(-3/2) delta dt = O(delta).
```

The first estimate follows by splitting at `t=1/delta`: the pieces are `delta integral_1^(1/delta) t^(-1/2)dt` and `integral_(1/delta)^infinity t^(-3/2)dt`. Consequently the leading edge sum is generally only `1/2`-Hölder in `L1`, not Lipschitz. In fact its parameter derivative contains `i sigma'_j C_j exp(i sigma_j t)t^(-1/2)`; if a nonzero edge coefficient survives in the chosen port, this derivative is not integrable. Distinct edge frequencies prevent an identically cancelling sum generically. A special port with all relevant `C_j=0` is an exception, not the generic matrix response.

This splitting proves `||K_Omega-K_omega||_1 <= C_K sqrt(delta)` for the full frozen family only with a parameter-uniform remainder estimate, for example `||E_Omega-E_omega||_1 <= C_K delta`, or a uniformly integrable parameter derivative after the leading edge terms have been removed. The finite-time portion `0<=t<=1` also needs uniform parameter continuity (a uniform Lipschitz bound suffices). Uniform `O(t^(-5/2))` decay of `E_Omega` alone is insufficient: it bounds each remainder but says nothing about its variation with `Omega`. Such derivative bounds are plausible here after using edge-centered coordinates: the next square-root-jump term has transform `O(t^(-5/2))`, and differentiating its moving phase costs one factor `t`, leaving an integrable `O(t^(-3/2))` tail; smooth interior and high-frequency pieces also need uniform derivative bounds. This is a sufficient-condition check, not an independent proof of those parameter estimates from the bare asymptotic statement.

Two related envelope integrals are explicit. If a parameter drifts at speed at most `C epsilon^2`, then a moving edge's accumulated phase displacement over lag `s` is `O(epsilon^2 s^2)`, so

```text
integral_0^infinity (1+s)^(-3/2) min(1, epsilon^2 s^2) ds = O(sqrt(epsilon)).
```

Split at `s=epsilon^(-1)`: the early part is bounded by `epsilon^2 integral_0^(epsilon^(-1)) s^2(1+s)^(-3/2)ds = O(sqrt(epsilon))`, and the tail is `O(sqrt(epsilon))`. For coefficient variation alone, `|C(Omega(s))-C(Omega(0))| <= C min(1,epsilon^2 s)`, and

```text
integral_0^infinity (1+s)^(-3/2) min(1, epsilon^2 s) ds = O(epsilon),
```

by splitting at `s=epsilon^(-2)`. These are estimates for frozen-kernel envelopes under a prescribed slow parameter path. They do not identify the true nonautonomous propagator or control its causal memory, moving neutral projection, or nonlinear errors, and imply no lifetime theorem.

## Finite localized field profiles at a channel edge

Perform the edge cancellation on the complete unprojected Green matrix first. Then subtract the finite-rank phase/family principal part from the completed point/profile matrix elements. Do not replace `R_jj` by a neutral-subtracted `R_jj` inside the Schur formula while leaving its companion `G_j` factors untouched; that is not the full neutral projection and can manufacture spurious singular terms. The genuine neutral residues are spatially localized bound profiles and are analytic across these nonzero-frequency edges.

This check extends the edge cancellation to a finite set of localized source/observation profiles, not to a weighted-space scattering theorem. Fix one channel `j` at a threshold and write

```text
G_j(x) = G0 exp(-lambda |x|),  G0 = 1/(2 c^2 lambda),
R_jj = -1/(g^2 G0) + r2 lambda^2 + O(lambda^3),
R_jk = r1 lambda + O(lambda^2)  (k != j).
```

The companion diagonal is nonzero at all four edges in this sector, so these expansions follow by inverting the 2x2 matrix with the threshold diagonal `-g^2 G0+O(1)`. The constants and remainders are uniformly bounded and smooth in `Omega` on the chosen compact set: thresholds remain separated and the companion factors stay bounded away from zero. For fixed `x,y`, put `a=|x|`, `b=|y|`, `d=|x-y|`. The same-channel field kernel has the exact decomposition

```text
G_j(x-y) + g^2 G_j(x) R_jj G_j(y)
= G0 [exp(-lambda d)-exp(-lambda(a+b))]
  + g^2 G0^2 [r2 lambda^2+O(lambda^3)] exp(-lambda(a+b)).
```

The apparent `1/lambda` term cancels. Its expansion starts at
`(a+b-d)/(2c^2) + g^2 r2/(4c^4) + O(lambda)`: finite constant plus powers of `lambda`, with no inverse square root. The cross-channel field term is finite too: `G_j(x) R_jk G_k(y)=O(1)` because `G_j=O(lambda^(-1))`, `R_jk=O(lambda)`, and the nonthreshold `G_k` is regular. The point-coordinate response is `R_jj=O(lambda)`; the point-to-field/profile response `g R_jj G_j(y)` is finite. Transposition gives the reverse pairing. Thus none of these entries has an edge `lambda^(-1)` term.

For profiles `phi(x)=P(|x|) exp(-kappa |x|)` with bounded polynomial coefficients and `kappa>=kappa_0>0`, all moments `m_n(phi)=integral |x|^n phi(x) dx` are finite uniformly, and

```text
F_phi(lambda) = integral phi(x) G_j(x) dx
              = [m_0(phi)-lambda m_1(phi)+lambda^2 m_2(phi)/2+...]
                /(2 c^2 lambda).
```

The free same-channel profile pairing starts with `m_0(overline(phi)) m_0(psi)/(2 c^2 lambda)`. The scattering correction `g^2 R_jj F_overline(phi) F_psi` starts with its negative, since `g^2 R_jj=-2c^2 lambda+O(lambda^2)`. The `1/lambda` terms therefore cancel for arbitrary such profiles, including ones whose zeroth moment vanishes (where there is no leading pole to begin with). The remainder has an expansion in nonnegative powers of `lambda`. Cross-channel profile pairings are finite by the same `G_j R_jk G_k` estimate. Hence all these finite matrix elements have at most square-root edge cusps in `sigma` after the full neutral pole is removed; there is no residual `1/sqrt(|sigma-sigma_*|)` term for a phase/family derivative profile or a localized observer of this form. The neutral `sigma=0` principal part must be subtracted from the whole finite matrix of profile/point pairings, not just from `R_jj`. Since the four edges stay a positive distance from zero on the compact set, that subtraction does not alter their local expansion.

First-order state resolvent blocks add analytic factors of the Laplace/frequency variable at each edge (`sigma_*` is finite and nonzero), so these factors preserve the nonnegative-`lambda` expansion. For the wave state `(u,v)`, the uncoupled block pattern is `[[sG,G],[s^2G-I,sG]]`; in the coupled problem the full second-order Green matrix replaces `G`. Retain the `-I` in the velocity-from-displacement block: it cancels the polynomial part of `s^2G` at high frequency and is an instantaneous contact term in time. It has no continuum jump and no long-time tail. Keeping it, and the corresponding finite-dimensional identity terms, prevents mistaking a polynomial feedthrough for a threshold singularity. At an edge, multiplication by `s` or `s^2` is smooth and cannot restore a `1/lambda` pole after the full Green cancellation.

For the stated even exponential-polynomial profiles, their spatial Fourier transforms are rational combinations of `(kappa +/- i k)^(-n)` and decay at least as `|k|^(-2)`. The free KG jump paired between two such profiles is proportional to `k^(-1) phihat(k) psihat(-k)`, hence `O(|k|^(-5))`. A profile-to-point element has the cruder bound `F_phi=O(|k|^(-2))`, while `Rqq=O(|k|^(-2))`, so its second-order jump is at worst `O(|k|^(-4))`; profile-profile point-coupled terms decay at least as fast as `O(|k|^(-6))`. With the at-most `s^2` factors in first-order blocks, the worst high-frequency jump is therefore `O(|sigma|^(-2))`, still integrable, with its first two frequency derivatives decaying sufficiently for two integrations by parts on the smooth high-frequency piece. These estimates are uniform for bounded polynomial coefficients and `kappa>=kappa_0>0`. Combining this with the edge `sqrt(rho)` jumps gives `O(t^(-3/2))` large-time decay for each of these finite profile matrix elements, after full neutral subtraction; smooth interior and high-frequency pieces decay at least `O(t^(-2))`. The `-I` contacts are kept separately at `t=0`. This supplies the finite-profile linear kernel gate needed by a Duhamel construction, but says nothing about a moving-frequency nonautonomous propagator or a nonlinear lifetime.
