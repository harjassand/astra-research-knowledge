# Independent challenge of the strengthened boundary receivers

Reviewed actual files `../quantum_boundary_review/PROOF.md` and
`../quantum_boundary_review/GENERAL_POSITIVE_RAY.md`. Verdict: ACCEPTED at
their stated mathematical scope. No physical acquisition, unrestricted
contraction, historical priority or ordinary-method separation is inferred.

For the weighted reset theorem I independently checked the noncommuting
supported log upper bound from PHP<=eps A, weighted-logC coefficients
1/3+3-2=4/3, fY coefficients8/3-4=-4/3, and binary pinching losses
3h2(1/9)+6h2(1/3)=12log(3/2). At1/192 the elementary rational receiver is
28/81-1/96=869/2592=1/3+5/2592. Singular support compression is valid.

For the general density-direction theorem I reconstructed the finite
inequalities, not just the leakage asymptotic. The weighted logs leave
(1/2)Tr(QHlogC)>=0. NH is a density operator, so its supported increment
is at most log(1+t), independently of kappa. Its kernel entropy slog s
cancels against the binary coherence h2(s), leaving

    Delta/t >=(ell/2)log(1/t)-elllog(24r/ell)-ell-2t.

At t<=ell²/(2^14r²), this is at least
(5/9-1/8192)ell>ell/2; the exact surplus is4087/73728.
Scaling m back gives Delta>=epsell/2 in the original units. The endpoint
has polynomial rational bit length; the old inverse-leakage k cost is
superseded, not silently retained as the current best bound.

I independently challenged Choi/isometry signs and normalization.
`acquire_positive_ray.py` uses no reviewer imports and checks both marginal
channels on all9 matrix units (18 exact components), V*V=I,VV*=P_antisym,
all9 Weyl-twirl units and the adjoint leakage identity. Thus the entropy
offset is log3 and raw Delta is divided by the WHOLE source trace.

`acquire_quadratic_radius.py` consumes the theorem with fresh rational PSD
checks. It reproduces eps1/20736, raw margin1/46656 and normalized margin
4/559881 for the exact source outside the reset/bath closure. The second
non-TP fixture explicitly charges reference6->54. Floating entropy controls
are recorded separately and are not a proof premise. No gap was found.
