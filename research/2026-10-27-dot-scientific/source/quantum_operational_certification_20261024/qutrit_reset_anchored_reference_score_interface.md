# Exact infinitesimal test for the anchored reference-filter comparison

Status: exact derivative receiving; no general score positivity or negative witness is asserted.

Fix d>0 and A=diag(a_1,a_2,a_3)>0. Let X=3d Phi3+I3 tensor A. For a positive reference filter Z_epsilon=(I+epsilon P)^(1/2), the derivative of the homogeneous deficit at epsilon=0 is Tr(P Q), where

Q=Tr_input[XlogX-2(NX)log(NX)]
  +(Tr_input X)log(Tr_input X)-log3 Tr_input X.

Matched diagonal covariance makes Q diagonal. A negative coordinate Q_i would immediately refute the anchored filter comparison with lambda_min(Z_epsilon*Z_epsilon)=1 when P is that coordinate projector. Through the large coherent-attachment theorem it would then produce a finite actual-source failure of the accepted-only GLS entropy payment.

## Exact local spectral formula

Let H=diag(a_1,a_2,a_3)+d J3 and O_ij=diag(a_i,a_j)+(d/2)J2 (the output off-diagonal sign is removed by a fixed diagonal unitary). For f(x)=xlogx,

Q_i=(f(H))_ii+3 f(a_i+d/3)
    -2 sum_{j!=i}(f(O_ij))_(i,i).                       (1)

The input/off-pair scalar spectator terms cancel exactly. The local first moments and total spectral masses in (1) agree, so its entropy integral has no uncharged affine terms.

Using Sherman-Morrison in the resolvents gives the exact convergent rational integral

Q_i=d integral_0^infinity [s/(a_i+s)^2]
       g_1(x_i(s),x_j(s),x_k(s)) ds,
x_j(s)=d/(a_j+s),                                      (2)

g_1(x,y,z)=-3/(3+x)-1/(1+x+y+z)
          +2/(2+x+y)+2/(2+x+z).

This is the same scalar zero-geometry kernel already received in `arbitrary_weight_three_block_pure_success_value_theorem.md`. Since every x_j(s) decreases, the kernel has at most one negative-to-positive crossing and is positive eventually. However, a single crossing does not determine the sign of its weighted integral (2); an actual compensating comparison is still needed.

If the two companion reset weights agree, a_j=a_k=b, the crossing, when positive, occurs exactly at s=d-b, independently of a_i. Explicitly

g_1(x,y,y)=2(1-y)(x+3y)/[(x+3)(x+y+2)(x+2y+1)].

When both companion weights satisfy a_j,a_k>=d, all three companion ratios are below one throughout s>0, and (2) is pointwise nonnegative. This is only a sufficient region, not a proof for arbitrary anisotropic A.

## Scope distinctions

The score test is at the UNFILTERED maximally entangled qutrit-reset seed. Global reference-filter monotonicity at arbitrary already-filtered seeds is false even when A=0: the pure-state reference-filter spectral gradient is log[4h_i TrH/(3(h_i+h_j)(h_i+h_k))], which can be negative in small directions of an anisotropic H. That failure does not refute the weaker anchored comparison, whose unfiltered pure-seed deficit is zero.

The high-noise anchored comparison is separately guarded by BKM data processing under the inverse contraction, as analyzed by the Schur branch; no extrapolation from that limit to finite noise is justified.

Diagnostic `qutrit_reset_reference_filter_score_probe.py` found no negative score in its bounded targeted anisotropic optimization. This is not a sign certificate. The exact formulas (1)-(2), not the sampling outcome, are the useful receiver.
