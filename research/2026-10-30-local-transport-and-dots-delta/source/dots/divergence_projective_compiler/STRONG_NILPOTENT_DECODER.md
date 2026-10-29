# Removing inverse-degree enumeration when the acquired chart certifies a nilpotent Jacobian algebra

## The honest bottleneck

The formal-degree inverse construction in `ACQUIRED_CHART_THEOREM.md` can be exponentially expensive for a short circuit: triangular quadratic maps can have inverse degree `2^(n-1)`. A small projective chart alone therefore does not imply cheap original-state evaluation. For general acquired polynomial charts, small-circuit inverse acquisition remains unresolved by this work.

There is useful **existing** machinery for a strictly admitted subclass. Van den Essen and Hubbers proved that strong Jacobian nilpotence is equivalent to linear triangularizability: *Polynomial maps with strongly nilpotent Jacobian matrix and the Jacobian Conjecture* (1996), primary text https://www.cs.ru.nl/E.Hubbers/pubs/strnil.pdf . This result is not new here. It supplies an actual way to manufacture a small inverse circuit instead of assuming one.

## Input and acquired certificate

Take the actually acquired chart `psi`. Normalize it at zero:

    F(x)=J0^-1(psi(x)-psi(0))=x+N(x),
    N(0)=0, JN(0)=0.

Require `J0` invertible, then acquire the constant matrix space

    A=span_Q{ JN(a) : a ranges over Q^n }.

For sparse polynomial inputs this is exactly the span of coefficient matrices of `JN`. For circuits, independent evaluation sketches followed by exact/PIT span-membership tests are possible. The acquired span must be checked for completeness; pointwise nilpotence at samples does not certify this condition.

Form the descending spaces

    V0=Q^n,       V_(k+1)=sum_(M in basis A) M V_k.

If `V_l=0`, every length-`l` product from `A` vanishes. If the chain stabilizes nontrivially, this certificate fails. All these operations are ordinary finite-dimensional rational linear algebra. A successful certificate has `l<=n`. It certifies the polynomial mixed-point identity

    JN(X1) JN(X2) ... JN(X_l)=0

with **independent** variable blocks. The weaker identity `(JN(X))^n=0` is insufficient and must never be substituted.

## Small inverse circuit without degree expansion

Start `G0(z)=z` and use untruncated circuit substitution

    G_(k+1)(z)=z-N(G_k(z)).

After at most `l` iterations, the resulting circuit is the polynomial inverse of `F`. Its shared-DAG size is `O(l size(F))` under ordinary composition, up to coordinate/linear-map overhead; there is no inverse-degree truncation or monomial expansion.

Proof: the polynomial divided-difference identity gives

    N(u)-N(v)=B(u,v)(u-v),
    B(u,v)=integral_0^1 JN(v+t(u-v)) dt.

Each coefficient matrix of `B` belongs to `A`. Since `N(0)=0`, also `N(z)=B(z,0)z`. Successive differences of the fixed-point iterates are therefore products of successively more matrices from `A`, ending with `z`. Their difference vanishes after `l` factors. Thus an iterate is an exact fixed point, so `F(G)=Id` as a global polynomial identity. The normalized map has a unique formal inverse because its linear part is identity; the fixed point is that inverse, giving `G(F)=Id` as well. Alternatively, the acquired invariant flag gives direct triangular backward substitution and proves both compositions by induction.

The final inverse of the original acquired chart is `G(J0^-1(y-psi(0)))`. A production certificate should retain the complete coefficient-space/flag verification and the two composition identities, or retain separate valid circuit-identity certificates. Constant Jacobian alone is never the acceptance test.

## What this does and does not buy

For the chain `F_i=x_i+x_(i+1)^2` for `i<n`, `F_n=x_n`, the inverse has degree `2^(n-1)` but is produced by at most `n` untruncated iterations and has a polynomial-size DAG. Unknown linear conjugation preserves the strong-nilpotence property; the matrix-space certificate acquires the needed structure without being given its triangular order.

Such charts can occur in compact raw vector fields: choose a projective field `g`, set `y=F(x)`, and construct

    f(x)=(JF(x))^-1 g(F(x))
        =[sum_(k=0)^(n-1) (-JN(x))^k] g(F(x)).

For quadratic `F`, this has polynomial-size raw arithmetic circuits and degree at most `n+3`, even though `F^-1` has exponential degree. The canonical divergence/cyclic-chart procedure can recover an affine transform of `F`; normalization removes the output affine transform. Thus the small-inverse route is relevant to the actual raw-dynamics acquisition problem, not just to a separately supplied inverse-map exercise.

This is an admitted subclass, not a generic solution to polynomial inversion. Strong nilpotence is an extra **acquired and verified** invariant and can fail on perfectly invertible polynomial charts. The compiler must then retain its slower degree-based route or report the decoder not acquired.

## Comparison and remaining hard consequence

An equally informed conventional method using the same chart can use precisely the same triangular/fixed-point inverse. No advantage over that method is claimed. The useful operation is supplying the previously unknown chart and certifying that a small inverse circuit can be built from it.

After acquisition, arbitrary-time evaluation uses a fixed-size matrix exponential, ratios, and the acquired inverse circuit rather than stepping through the nonlinear trajectory. This is a structural operation-count reduction, not yet a matched numerical speed result. Its bit/precision cost depends on matrix exponential conditioning, distance from denominator zeros, and amplification through the inverse circuit. Exact rational evaluations of a high-degree circuit can themselves have exponentially many output bits. Near a pole or an ill-conditioned inverse, there may be no useful advantage over ordinary numerical evolution or certified continuation.

The unresolved general target is therefore precise: **recover a compact, well-conditioned original-state decoder beyond the verified strong/quasi-translation subclasses, or show a real same-input/time/accuracy advantage after all acquisition and evaluation costs.** Low chart dimension alone does not settle it. No expensive degree bound is silently treated as a supplied practical capability.

## Implemented continuation and strict nonstrong fallback

`strong_decoder.py` now implements complete coefficient-space flag acquisition,
shared-DAG fixed-point inversion, and original-chart affine normalization. Raw
polynomial acquisition followed by this decoder passes in dimensions 2–5. The
decoder-only scaling experiment reaches dimension 16 and inverse degree 32,768:
the final normalized-chain inverse uses 62 reachable nodes but 379 total allocated
nodes. Neither build memory nor intermediate dead DAGs is hidden in the smaller
number. Exact evaluation at the integer target `(3,...,3)` reaches 41,308 bits,
demonstrating why a small arithmetic DAG alone is not a uniform bit-cost result.

Strong nilpotence is not necessary for a small inverse. A separate classical
quasi-translation certificate checks the exact polynomial identity

    (JN)N=0.

Writing `D_N=N·grad`, this implies `D_N N_i=0` and `D_N^2 x_i=0`. The derivation
is locally nilpotent on the polynomial algebra: sufficiently many applications
kill each product of coordinate generators by the Leibniz rule. Its exponential
acts on coordinates as `exp(tD_N)x=x+tN(x)`, and the group law gives
`(Id+N)^−1=Id−N`, globally in both directions. This gives an `O(size(N))` inverse
without acquiring a strong Jacobian flag.

The exact control

    N=(z(x+zy)^2, −(x+zy)^2, 0)

has `(JN)^3=0` and `(JN)N=0`, but its independent-point mixed Jacobian products
do not all vanish. The strong branch rejects it; the quasi branch accepts it.
The raw degree-13 three-variable dynamics generated from this unknown chart also
acquires its four-dimensional projective module and quasi decoder. Both global
inverse compositions are independently verified. This family and its simple
inverse are classical; see [Campbell, Example 3](https://arxiv.org/pdf/math/9907157).

The invertible map `(x+y^2, y+(x+y^2)^2)` fails both selected strong/quasi tests,
so these branches still do not recognize all polynomial automorphisms. The
fallback to formal inversion or an explicit not-acquired result remains needed.

## Closing the conditioning objection on a nontrivial explicit family

`UNIFORMLY_CONDITIONED_FAMILY.md` constructs an even-dimensional oscillatory
projective family with an exponential-degree inverse, but a compact acquired
decoder, denominator uniformly at least `7/8`, bounded original states, and inverse
absolute Jacobian norm below `4/3` on an explicit initial-data ball, for all real
time. This is a uniform initial-state/evaluation conditioning result, not
robustness to unknown generator errors or noisy model identification.

`quadratic_circuit_acquisition.py` implements the raw-circuit front end with a
quadratic search dictionary and fresh PIT. It never receives the chart or inverse.
The dimension-16 raw input has 493 circuit nodes, and acquisition yields 17 chart
coordinates; no inverse expansion is used. Independent coefficient replay of the
serialized input/output now certifies all 34 closure identities across dimensions
2, 4, 8 and 16. The general front end remains Monte Carlo; deterministic replay is
evidence for these saved inputs, not a derandomization theorem.

Actual independent review and receipts are in `audit/NILPOTENT_BRIDGE_REVIEW.md`,
`audit/strong_decoder_replay.json`, and `audit/quadratic_circuit_replay.json`.
The n=16 raw field has only 2,361 expanded terms, so no empirical exponential
advantage over sparse symbolic algorithms is claimed. The meaningful conclusion
is a closed acquisition-to-decoder capability bridge, not a demonstrated new
scientific application or matched superiority over classical inversion methods.
