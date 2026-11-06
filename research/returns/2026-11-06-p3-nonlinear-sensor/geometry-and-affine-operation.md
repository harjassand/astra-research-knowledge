# Native direction geometry and the affine-operation compiler

These are claims in the [complete visible response](P3_NONLINEAR_SENSOR_20261106_COMPLETE_RETURN.txt), including its recovered comparisons and conclusions. No new Capital proof check was performed. The historical published prefix remains available separately.

The exact source class has latent dimension `n≥2`, a nonexplosive finite-activity Markov jump-diffusion, and a finite collection of nonparallel constant jump directions spanning the state space. Drift, diffusion, jump rates and amplitude laws may be unknown and state-dependent. Every direction has positive jump measure arbitrarily close to zero at every state. Observation is a `C³` diffeomorphism of the full state; the stationary observed path law has full support with the stated continuity conditions. This is exact-law information, not an already acquired finite-data oracle.

Choose a basis of native directions and connect basis indices appearing jointly in another direction. The components give the intrinsic direct-sum blocks of the represented direction matroid. Two models with the same observed law differ, after a fixed invertible linear map and translation, only by scalar diffeomorphisms on one-dimensional blocks. Higher-dimensional blocks admit only affine changes. Conversely those scalar transformations are genuine ambiguities in this source class because state-dependent amplitude laws are allowed.

| Direction arrangement | Consequence |
|---|---|
| Coordinate directions alone | Arbitrary scalar recalibration on every coordinate; affine state arithmetic is not identified |
| Coordinates plus one direction involving every coordinate | No remaining nonlinear freedom |
| Four coordinates plus `e₁+e₂` and `e₃+e₄` | Two two-dimensional blocks suffice; global arrangement connectedness is unnecessary |
| Three coordinates plus `e₁+e₂` | Third coordinate retains scalar nonlinear ambiguity |

Drift may couple different blocks; independent trajectories are not assumed. The scalar-recalibration converse does not refute the earlier homogeneous native-Lévy result, whose amplitude-law restrictions differ.

The source first identifies small-jump support tangents from the off-diagonal transition kernel. These form unordered observed line fields. The exact-law conditional kernel and its short-time limit are proof inputs; the finite acquisition theorem must earn their needed geometric accuracy separately.

For smooth representatives `u_l` of the lines, the compiler solves the pointwise linear equations `P_l^perp(∂_k u_l+Γ_k u_l)=0`, with symmetric lower connection indices. There are `n²(n+1)/2` unknown coefficients. With no one-dimensional block, the source proves a unique torsion-free solution, independent of representative scale/sign/order. Existence comes from the true affine pullback; uniqueness uses the same line-preserving block algebra.

Integration transports a frame and chart along paths. The exact connection is flat and the observed domain is diffeomorphic to `R^n`, giving a path-independent chart `H=A g⁻¹+b`. Noisy fitted connections need not be flat. The finite construction uses specified paths and error bounds rather than treating a small residual as a flatness certificate or an approximate transported frame as automatically the derivative of its approximate chart.

Conditioned linear solving, finite-bit integration and finite inverse search remain paid. The source gives operation error at most

`L_H[(1+Σ_i|w_i|) ε+η_inv]`,

for uniform chart error `ε`, inverse Lipschitz constant `L_H` and inverse residual `η_inv`, within the certified domain and required query/integration coverage. Convex-combination chart error is `2L_H ε`; displacement transfer has `4L_H ε`. These bounds support adaptive reuse on one uniform chart-confidence event without promising unrestricted extrapolation.

The exact-law corollaries cover finite adaptive protocols alternating native Markov evolution with specified affine state updates, assuming the same dynamics resume after updates. They identify protocol laws, without supplying actuators or proving an unmodelled environment remains unchanged. Learning future transition laws and sampling trajectories remain separate costs. Affine drift linearity/polynomial degree become invariant under the remaining affine changes, while labelled interaction graphs need not. Counting extra perturbation directions does not pay for their fabrication, rates or observation.

## Sharp failures in the recovered ending

With coordinate directions alone, `F(x₁,x₂)=(x₁+x₁³,x₂)` preserves the declared class after changing amplitude laws and sensor. The same observed process can assign different physical midpoint readings: endpoints `(0,0)` and `(2,0)` yield `(1,0)` in one representation and `(φ⁻¹(5),0)`, `φ(t)=t+t³`, in another, with first coordinate above `1.5`. Arbitrarily small diagonal-direction jumps exclude that transformation. This is an indistinguishability within the declared state-dependent source class, without retracting the earlier homogeneous-source result.

Integer-sized kicks are not a substitute for arbitrarily small jump support: `F_i(x_i)=x_i+ε sin(2πx_i)`, `0<ε<1/(2π)`, commutes with integer translations. Coordinate and common integer kicks can therefore retain nonlinear calibration ambiguity. A replacement rigidity assumption must be earned separately.

For the specified coupled starting campaign, two sources agree until a rare informative-direction event of rate `λ`. The source reuses accepted first-event coupling to obtain `TV(P_T,P̃_T)≤1−exp(−λT)`, hence `T≥λ⁻¹ log[1/(2δ)]` for uniform binary error at most `δ`. This is not a new universal acquisition lower bound, and does not supply stationary prehistory for a modified source for free.

[Finite acquisition, diagnostics and strongest comparators](finite-access-and-diagnostic.md) · [Overview](README.md)
