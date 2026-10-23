# Threshold behavior of the dressed point-port resolvent

24 October 2026. This is a local spectral check of Section 4 in `WEAK_ANISOTROPY_RESPONSE_AND_MODULATION.md`. It does not establish the nonlinear modulation theorem or an `epsilon^-2` lifetime. No source or new fixture is used.

## Exact inverse and one threshold

Write the rotating-frame matrix on a chosen causal boundary as

```text
M(sigma) = [[A_-(sigma), B], [B, A_+(sigma)]],
A_-(sigma)=f(Omega-sigma)+2B,
A_+(sigma)=f(Omega+sigma)+2B,
R(sigma)=M(sigma)^(-1)
       = 1/(A_- A_+ - B^2) [[A_+,-B],[-B,A_-]].
```

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
