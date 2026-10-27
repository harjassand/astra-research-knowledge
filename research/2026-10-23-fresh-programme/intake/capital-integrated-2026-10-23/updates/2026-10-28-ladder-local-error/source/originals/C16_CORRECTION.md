# Correction accompanying the original solo pole proof

The original source is preserved unchanged at `frozen/c31/PROOF.md`. The independent mathematical review is `coordination_review/trial_coord_review/REVIEW.md`.

At original lines 153–158, for x(k)=c-cos(k)cosh(t sin(k)), the correct derivative is

    x'(k) = sin(k)cosh(t sin(k)) - t cos(k)^2 sinh(t sin(k)).

The second term has a minus sign. For 0<t<1 and 0<k<pi, tanh(u)<=u gives

    x'(k) >= sin(k)cosh(t sin(k)) [1-t^2 cos(k)^2] > 0.

Thus the required strict monotonicity survives the correction. This is the correction already assessed in the substantive independent review, not a silent alteration of the original experimental return.

At original lines 443–446, the harmonic inverse is defined on the stated disk, while the Schur inverse formula as an inverse identity additionally requires an invertible Schur matrix. At a physical pole it is an identity between meromorphic continuations. The subsequent isolated-pole argument uses this domain correctly.

The reviewer accepts the scoped local outgoing-pole conclusion with these corrections. No numerical detuning radius, interval-certified density decimal, survival law or device advantage is added.
