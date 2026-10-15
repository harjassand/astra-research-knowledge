# Compact-noise theorem: independent proof comparison and one-sided refinement

Date: 2026-10-15. This file is append-only continuation evidence; it changes no frozen proof.

## 1. Frozen proofs and authorized read order

The operator-adversary PL proof was frozen before the parallel saved proof was read:

- `operator_adversary/COMPACT_NOISE_PROOF_PL.md`, SHA-256 `d4faf34610df74b94508852da54c12a8a3b4b7f0dc3df479541dc2a7c28db147`.

Root then authorized reading:

- `quantum_functional_astra/COMPACT_NOISE_COMMUTATIVITY.md`, SHA-256 `b26fc0183066ba380b30049d352b6c7d547942cdb75a4f798e7a6967b726eb24`.

The latter was read in full and its hash verified. Root had already reported its first-moment/Sylvester mechanism before this cross-read; that report was not used to derive the different PL continuation.

**Audit verdict: no material gap found in either route.** Both establish the arbitrary-Hilbert compact-noise commutativity theorem at the level of the written analytic arguments. External correctness and historical priority remain UNKNOWN.

## 2. Shared measure-theoretic step checks

Both proofs use the full state-independent identity

`M_hat(t)=nu_hat(t)exp(iA(t))`

for all real directions. Scalarization and characteristic-function uniqueness identify every output projection with a positive scalar-noise convolution of the corresponding bounded spectral law. This supplies genuine support and moment statements, including for weakly countably additive POVMs and nonseparable Hilbert spaces.

When the scalar noise in the `B` coordinate is bounded, so is the output in that coordinate. The positively tilted and normalized operator measure consequently has a bounded first `B` moment. Differentiation of the Laplace identity is justified by the uniform scalar Taylor remainder on that bounded coordinate, weighted by the already established positive exponential moment in the `A` coordinate. No continuation of an unbounded distributional test is needed.

Both routes therefore obtain

`sup_{s>=0}||J_s||<infinity`,

`J_s=integral_{-1/2}^{1/2}exp(svA)B exp(-svA)dv`.

The opposite sign convention in the PL file gives exactly the same operator after changing `v` to `-v`.

## 3. Spectral-gap proof audit

For genuine spectral projections `H=E_A([c+delta,infinity))` and `L=E_A((-infinity,c])`, the compressed restrictions reduce `A`. Let `X=HBL` and let `D(Z)=A_HZ-ZA_L` on operators from `L H` to `H H`. The semigroup formula

`exp(-tD)Z=exp(-tA_H)Z exp(tA_L)`

has norm at most `exp(-t delta)`: the scalar cut location `c` cancels between the two factors. This is valid for infinite-rank blocks and continuous spectrum.

If `Y_s=HJ_sL`, differentiating the exponential inside the bounded operator integral gives

`s D Y_s=[exp(sD/2)-exp(-sD/2)]X`.

After multiplication by `exp(-sD/2)`,

`[I-exp(-sD)]X=sD exp(-sD/2)Y_s`.

The direct triangle inequality therefore gives

`(1-exp(-s delta))||X|| <= 2s||A||exp(-s delta/2)||Y_s||`.

The uniform first-moment bound makes the right side tend to zero. Thus `HBL=0` for every positive spectral gap.

As `delta` decreases to zero, `E_A([c+delta,infinity))` increases strongly to `E_A((c,infinity))`. Multiplication by the fixed bounded `BL` preserves that strong limit. Taking adjoints supplies the other off-diagonal block, so `B` commutes with every spectral cut `E_A((-infinity,c])`, hence with `A`.

This is not a finite compression argument. Only actual reducing spectral subspaces of one original operator are used; the exponential identity for the original pair is never transferred to a smaller matrix tuple.

The quantitative block estimate in the Astra file follows from the same inequality and is correct. Replacing `2||A||` by the spectral diameter after a scalar shift is legitimate because conjugation and the Sylvester difference are shift invariant. A nonzero separated spectral block forces exponential growth of the tilted first moment. This supplies more explicit information than the qualitative PL proof.

## 4. One-sided refinement of the frozen PL proof

The frozen PL proof states the sufficient directional assumption `E exp(sZ_A)<infinity` for every real `s`. This is stronger than necessary. The Astra proof correctly needs only every positive exponential moment, and the PL route can independently use that same weaker hypothesis.

Indeed, its symmetrized conjugation integral is even:

`J(-s)=integral_{-1/2}^{1/2}exp(usA)B exp(-usA)du=J(s)`.

Thus the positive-axis uniform bound obtained from actual moments automatically bounds the whole real axis. The imaginary-axis unitary bound and entire exponential-type bound depend only on bounded `A,B`, not on negative scalar-noise exponential moments. The elementary quadrant argument then applies unchanged, forcing `J` to be constant and consequently `[A,B]=0`.

Therefore the strengthened directional theorem is:

**If the scalar noise in the `B` direction is bounded, and the scalar noise in the `A` direction has every positive exponential moment, then the corresponding bounded observables commute.**

No negative exponential moment is needed. Finiteness at an unbounded sequence of positive tilts already suffices: for `0<s<t`, Jensen/Hölder gives `E exp(sU)<= [E exp(tU)]^(s/t)`. This conclusion does not follow from all ordinary moments alone in the present proofs.

This refinement is saved separately to preserve the original PL freeze hash.

## 5. Fixed-pair compact support and existential commutation

The Astra proof's quantifier distinction is correct and should be retained in any integrated statement:

- For every fixed exact positive pair `(M,nu)` with bounded observables, `M` is compactly supported if and only if `nu` is compactly supported.
- A tuple admits at least one such compact exact pair if and only if its operators commute pairwise.
- A commuting tuple can also be paired with noncompact scalar noise, yielding noncompact output; commutation does not force every representation to be compact.

For the nontrivial fixed-pair implication, if the output coordinate is in `[ell_j,r_j]` and the spectral summand is in `[min sigma A_j,max sigma A_j]`, positivity of the convolution law forces the noise coordinate into

`[ell_j-max sigma A_j, r_j-min sigma A_j]`.

This uses positive scalar convolution and support, not entire-function division. The finite product of the resulting bounded coordinate intervals contains the joint noise law.

## 6. Recommended retained form

Use the Astra spectral-gap proof as the shorter primary analytic proof, with the independently frozen PL proof retained as corroborating capital. Retain the positive-exponential-moments-only directional hypothesis and the fixed-pair versus existence distinction.

The resulting theorem strengthens the supplied source in a different direction from endpoint-tail attainability: exact scalar convolution for genuinely noncommuting bounded observables necessarily has unbounded noise and output. It does not prohibit bounded-output unsharp joint measurements under weaker contracts, and does not prevent bounded classical decoders from extracting information from the unbounded exact output.

No approximate-contract error bound or operational advantage is established by either proof. The result is an exact qualitative obstruction, with a quantitative spectral first-moment witness when a separated nonzero block is given. Historical priority remains open despite the targeted primary-source comparison saved separately.
