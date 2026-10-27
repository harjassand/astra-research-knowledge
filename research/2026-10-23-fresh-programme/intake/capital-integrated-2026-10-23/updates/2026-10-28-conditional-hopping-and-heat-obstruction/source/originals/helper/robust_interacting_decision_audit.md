# Robust interacting transport comparison: independent audit

Published source pin: `1dc593a750b447be6536bafcf0be156d27767dfe`.

**Verdict:** the stated analytic perturbation inequalities, current normalization and factor of four are correct. They support a uniform comparison of the two fixed controls within the stated conditional-hopping model box, conditional on the complete Pauli norm summaries. I independently checked all stored rational endpoint formulas and source endpoint JSON. I inspected, but did not run or independently duplicate, the principal's commutator/norm regeneration.

## 1. Exact model and sector

The numeric family has `U=4,d=2`, four translation-invariant amplitudes `a_sigma=1+e_sigma`, `|e_sigma|<=epsilon<1`, conditioned on `(n_(i-1),n_(i+2))`, and precisely the source diagonal interactions at either `V=3/2` or `V=0`. Arbitrary additional diagonal terms, uncertain U/d, different transition types or a physical device are not included in these numeric bounds.

The source trials can lie outside the strictly number-neutral observable sector. This does not invalidate the formulas: they lie in the enlarged even-X/Y-parity sector, which the real, number-conserving, diagonal-conditioned hopping preserves. Every odd Pauli word there has at least two X/Y factors, so `S_odd>=d=2`. Actual current and exact response are number neutral. The enlarged trial components can worsen residual costs but do not invalidate the variational inequalities.

At `d=2`, a Pauli word with q X/Y factors has `S` eigenvalue q. Thus the code's q-weighted S norm and 1/q-weighted S+ seminorm have the correct normalization.

## 2. Pairing and S penalty

Let `E_sigma` project onto a direct neutral hopping coherence and the specified environment pattern, with translations included. These are mutually orthogonal occupation-matrix-element sectors, commute with S, and sum to the edge-coherence projection. Their complement contains all unchanged coherences. With `r_sigma=(1+e_sigma)^(-1)-1`,

`f_a=f0+sum_sigma r_sigma E_sigma f0`.

On every current-supported matrix element, the amplitude in `J_a` cancels the reciprocal amplitude in `f_a`. Therefore

**`<J_a,f_a>=<J0,f0>` exactly.**

No strict U(1)-neutrality of the entire trial is needed: the current only pairs with the direct neutral edge part.

Orthogonality gives the exact S-norm difference

`||f_a||_S²-||f0||_S²=sum_sigma[(1+e_sigma)^(-2)-1]||E_sigma f0||_S²`.

Hence it is at most

`edgepen=[(1-epsilon)^(-2)-1]||E_edge f0||_S²`.

This upper bound has the correct sign; positive amplitude errors may make some individual differences negative, which only improves the lower bound.

## 3. Complete commutator perturbation

Write `A_a=A0+sum_sigma e_sigma A_sigma`, and let `Q=I-P`. Then

`Delta=A_a f_a-A0f0`

`=sum_tau r_tau A0 E_tau f0 + sum_sigma e_sigma A_sigma f0 + sum_sigma,tau e_sigma r_tau A_sigma E_tau f0`.

The generic population identities are

`P A0 E_sigma f0=P A_sigma f0`,

`P A_sigma E_tau f0=delta_(sigma,tau) P A0 E_tau f0`.

Their combination leaves coefficient `r_sigma+e_sigma+e_sigma r_sigma=0`, proving `P Delta=0`. The reported 20 checks are precisely these four plus sixteen identities. In the code, `Efield` has denominator `8*den`; consequently `act(Efield,...)` has denominator `32*den`, while `act(f,...)` has denominator `4*den`. The factor eight in the first population comparison is required and correctly present. The second comparisons have equal denominators.

The S+ triangle inequality can be applied after Q. With `rho=epsilon/(1-epsilon)`, the stated sums of the three complete Q-projected commutator norms give

`||Delta||_S+<=b=rho*c10+epsilon*c01+epsilon*rho*c11`.

Dropping population coordinates inside each summand is legitimate here only because the total population cancellation is proved exactly. It is not an approximation of a small unbalanced residual.

The source lower functional then yields

`D_a(3/2)>=D0_low-4[edgepen+2||A0f0||_S+ b+b²]`.

The derivation uses `||A_a f_a||_S+<=||A0f0||_S++b`, the exact pairing identity and the S penalty above. All signs and factors agree with the code.

## 4. Upper bound and current factor

For the fixed even source trial g0, set `r0=J0-A0g0`. The upper functional obeys

`U_a<=U0+2||r0||_S+ c+c²`,

where `c` bounds `||delta J-sum_sigma e_sigma A_sigma g0||_S+`.

The direct-edge currents have orthogonal flip patterns. Under full product trace,

`||delta J||_S+²=(1/(2d))E_env[(delta a)²]<=epsilon²/4`

because `d=2`. Thus the current contribution is exactly bounded by `epsilon/2`, and

`c=epsilon*cU`, `cU=1/2+sum_sigma||A_sigma g0||_S+`

is correct. Converting the upper functional for kappa to D requires factor four:

**`D_a(0)<=D0_upper+4[2||r0||_S+ epsilon*cU+(epsilon*cU)²]`.**

The principal code includes this factor. The actual-current covariance remains `b_J=E_env[a²]/2`, with `chi=1/4`; no nominal-current replacement is used in the perturbation estimate.

## 5. Exact arithmetic and safe displayed numbers

I independently parsed the artifact, recomputed all four epsilon rows with `fractions.Fraction`, and matched every lower endpoint, upper endpoint and difference exactly. I also matched the stored nominal lower/upper endpoints directly against the pinned source JSON at their respective controls. Results are in `ROBUST_DECISION_ANALYTIC_CHECK.json`.

For `epsilon=1/100`, safe outward-rounded 18-decimal bounds are

**`D_a(3/2)>=0.552042800224893174`,**

**`D_a(0)<=0.524990652212544690`,**

**`D_a(3/2)-D_a(0)>=0.027052148012348484`.**

The nearest binary floats for the lower endpoint and improvement round slightly upward; they should be labelled diagnostics or replaced by the outward values above. The exact rational fractions in the artifact are the authority.

Verified artifact SHA256:
`3de65a6097467c3b673db82f14a3c62d8a01f1446e329b65c80509a17022aebb`.

Verified source NPZ hashes:

- `V1half.npz`: `89960d84f24ce8baa47835665c2635bc6a65f6faaa8ce04dcceee552533a4167`.
- `V0.npz`: `721a1ba1275291b4bedd74f1a94d8dcf184db0c4a1a86772f8214602f1641b16`.

Read-only metadata inspection confirmed both source archives have 3,088 f-word and 3,024 g-word rows and maximum footprint eight. I did not count reflected expansions as new source input or call these inputs freshly acquired inverse solutions.

## 6. Thermodynamic and finite-size scope

The earlier conditional-hopping audit supplies the structural thermodynamic extension: exact local continuity, unchanged susceptibility, finite-range bounded dynamics, actual current covariance, positive connected swap graph, parity Schur lower bound d, and the source's regularized thermodynamic/Stieltjes identification. Nothing in these inequalities imports a global population gap or replaces the original physical dephasing.

A conservative explicit footprint count is available. A footprint-eight source field becomes footprint at most ten after an edge/environment projection; a commutator with a length-four conditional hopping term has footprint at most thirteen. This covers every complete lower residual word; upper fields have smaller footprint. Thus the source's `n>2W` stabilization criterion gives a conservative common **`n>=27`** for the periodic finite-response certificates, provided the source convention and the full length-four interaction support are used as inspected. The infinite D follows from the inherited extension, not an extrapolation of these rings.

The conclusion is a robust **two-control comparison**, with strict improvement for every allowed hopping table. It is not a global optimum or continuous-control regret theorem, uniform inverse-complexity theorem, new physical transport law, physical acquisition, finite-time diffusion guarantee, or superiority over ordinary methods with the same access. The source witnesses are supplied scientific data, their regeneration/certification costs remain charged, and acquisition of the four-amplitude box plus model/switching/calibration contracts remains a separate physical task.
