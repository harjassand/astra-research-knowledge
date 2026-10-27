# Two-scale entropy asymptotic for a large coherent graph attachment

Status: original exact asymptotic construction, submitted for independent audit. This is a reduction/payment formula, not a whole positivity or postprocessing theorem.

## 1. Actual TP sources and homogeneous convention

For a qutrit input define N=W3 tensor id and E(X)=I3/3 tensor Tr_input X. Let

D(X)=Tr XlogX+Tr EX log(EX)-2Tr NX log(NX).

It is homogeneous and, for trace-one X, equals the normalized deficit used throughout. Fix d>0, A,D0>0 on C3 and an invertible3x3 matrix C. Set

Y_t=[[A+t^2 C D0^(-1)C*,tC],[tC*,D0]],
V=[I;0], X_t=3d Phi_V+I3 tensor Y_t.                      (1)

Y_t>0 by its Schur complement A. Its mass is

n_t=3d+3TrY_t=3t^2 TrG+O(1), G=C D0^(-1)C*>0.

Thus X_t/n_t is the actual TP Choi state of

E_t(rho)=(3d/n_t)VrhoV*+[3TrY_t/n_t]Tr(rho)Y_t/TrY_t.

Put Z=D0 C^(-1). The noise-optimal left inverse is exactly

L_t=[I,-t C D0^(-1)], L_t Y_t L_t*=A,
kappa_t=||L_t||^-2=1/[1+t^2||C D0^(-1)||^2].             (2)

The actual inverse-filter accepted branch has homogeneous deficit kappa_t F_d(A), where F_d(A)=D(3d Phi3+I3 tensor A). Its erased failure branch has zero deficit. No inequality between this accepted value and the original value is assumed.

## 2. The exact leading coefficient

Define the reference-filtered seed

X_Z=(I3 tensor Z)[3d Phi3+I3 tensor A](I3 tensor Z*).       (3)

This seed is generally NOT a TP Choi source. Its input marginal is d(Z*Z)^T+Tr(ZAZ*)I3, which need not be scalar. The received unfiltered qutrit-reset theorem therefore cannot simply be applied to (3).

Let g_1,g_2,g_3 be the positive eigenvalues of G and ell(a,b)=(log a-log b)/(a-b), continuously at equality. Then

D(X_t)=t^(-2)[D(X_Z)+H_d(G)]+O(t^(-4)log t),              (4)

H_d(G)=d^2[(1/6)sum_i 1/g_i+(1/2)sum_{i<j}ell(g_i,g_j)]>0.

The leading logarithmic terms cancel. The strictly positive second term is an actual high-noise BKM contribution, not an optional correction.

## 3. Explicit spectral-scale separation

Use the following orthogonal code/exterior graph frames:

W_h=[I;t^(-1)Z](I+t^(-2)Z*Z)^(-1/2),
W_l=[-t^(-1)Z*;I](I+t^(-2)ZZ*)^(-1/2).

Their concatenation is unitary. Apply this unitary on the reference output of X_t; D is unchanged because N and E act only on the input qutrit. The reset blocks obey

Y_hh=t^2 G+O(1),
Y_ll=t^(-2)ZAZ*+O(t^(-4)),
Y_hl=O(t^(-1)).

The success code components are

W_h*V=I+O(t^(-2)), W_l*V=-t^(-1)Z+O(t^(-3)).

Thus the full high block is an O(1) pure-main perturbation of a strictly positive N,E-fixed baseline of order t^2. The low block is t^(-2)X_Z+O(t^(-4)). The cross block is O(t^(-1)). The same scale bounds hold after N and E.

For completeness, the entropy effect of omitting these cross blocks is O(t^(-4)log t). For a positive block matrix [[H,B],[B*,L]] with H>=c t^2 I, L>=c' t^(-2)I and ||B||=O(t^(-1)), the determinant overlap formula bounds the absolute entropy correction by a constant times

t^(-2) integral_0^infinity ds/[(c t^2+s)(c' t^(-2)+s)]
 =O(t^(-4)log t).

The relevant logarithmic determinant argument has norm O(t^(-2)) uniformly, so -logdet(I-Q) is bounded by a constant times TrQ for all sufficiently large t. The strict positivity of A,D0,G supplies the required lower bounds. This controls the cross correction rather than silently discarding coherences.

The low-block entropy is t^(-2)D(X_Z)+O(t^(-4)log t) by homogeneity and the strict-positive finite-dimensional expansion. The high-block calculation follows next.

## 4. High-noise BKM payment

For the reference-only baseline B=I3 tensor G, define

Q_B(H)=integral_0^infinity Tr[H(B+sI)^(-1)H(B+sI)^(-1)]ds.

The deficit and its first variation vanish at every positive reference-only baseline. In the BKM metric, physical identity and physical-traceless parts are orthogonal. N fixes the former and scales the latter's squared metric by1/4, because W3 acts by minus transposition divided by2 there and the baseline is physical identity.

Consequently the quadratic deficit of a perturbation H is (1/4)Q_B(H-EH). Here the leading high main is H=3d Phi3, so

H_d(G)=(1/4)Q_(I3 tensor G)[3d(Phi3-I9/9)].              (5)

The higher Taylor terms are O(t^(-4)); O(1) baseline corrections and O(t^(-2)) success-code corrections do not change the leading quadratic coefficient. Diagonalizing G by matched covariance in (5) gives exactly (4)'s diagonal and off-diagonal logarithmic means. This also proves its strict positivity.

## 5. Throughput-charged comparison: exact asymptotic interface

Equation (2) gives

t^2 kappa_t -> k0=lambda_min(Z*Z).

Therefore the candidate accepted-only comparison has limiting gap

t^2[D(X_t)-kappa_t F_d(A)]
 -> D(X_Z)+H_d(G)-k0 F_d(A).                            (6)

The combined coefficient in (6), not either term separately, is the correct finite-dimensional pressure test. No positivity of the filtered seed, no order monotonicity under reference filtering, and no postselection monotonicity is claimed.

For isotropic Z=zI, homogeneity gives D(X_Z)=|z|^2 F_d(A)=k0F_d(A), so the asymptotic gap is precisely the strictly positive BKM payment. This explains why isotropic scalar attachment tests cannot disprove the charged comparison.

A useful exact reduction, not an extra sign claim: hold arbitrary invertible Z and A fixed, choose D0=rI and C=r Z^(-1). Then G=r Z^(-1)Z^(-*) while Z and k0 remain fixed, and H_d(G) decreases as1/r. Consequently a universal accepted-only comparison would imply the separate strong reference-filter inequality D(X_Z)>=k0F_d(A) after this ordered double limit. If that filtered inequality were decisively false, finite sufficiently large r and then finite sufficiently large t would yield an actual TP failure of the accepted-only comparison. No such failure is asserted here.

## 6. Normalized scale and reproducible checks

Since n_t~3t^2 TrG, the normalized actual deficit satisfies

Delta(X_t/n_t)=[D(X_Z)+H_d(G)]/[3TrG t^4]+O(t^(-6)log t).

The homogeneous t^(-2) scale must not be reported as the normalized TP deficit scale. The normalized accepted identity weight is likewise of order t^(-4); this is not a high-throughput limiting construction.

`large_graph_attachment_entropy_asymptotic_check.py` evaluates the exact original source at high precision with rational noncommuting A,D0,C. The predicted coefficient is8.1020538896970950016872270309744852; direct t^2D(X_t) converges to it (at t=3000, discrepancy approximately0.0002196642). The accepted coefficient is0.6657100547338930530, so this instance is not a comparison counterexample. The scalar calibration A=D0=C=I,d=1 gives coefficient F_1(I)+2=2.6795961471815898916.

## Received aligned-seed large-coherence value corollary

The later theorem `aligned_filtered_seed_cq_dilation_value_theorem.md`, independently received in `aligned_filtered_seed_cq_dilation_independent_audit.md`, supplies a legitimate value receiver for the non-TP low seed when[A,Z*Z]=0. Indeed its main reference Schmidt Gram isZZ* and its reset isZAZ*; their commutator vanishes exactly when[A,Z*Z]=0. Hence D(X_Z)>=0.

Under the strict positivity/invertibility hypotheses of the present expansion, H_d(G)>0. Therefore its full leading coefficient D(X_Z)+H_d(G) is strictly positive, and the actual TP channel has strictly positive deficit for all sufficiently large attachment t. No explicit uniform threshold is asserted: the existing fixed-parameter remainder supplies the eventual sign.

This is not a throughput-charged comparison. It receives an actual large-coherence value regime even when the small-perturbation GLS tube bound is inapplicable. The finite reset need not be physical-CQ: the alignment condition concerns only A andZ*Z, not all of C,D,G simultaneously. No arbitrary nonaligned filtered-seed positivity is inherited.

## Stronger received consequence: eventual accepted-only GLS payment

The later independently received `mean_dominant_reference_score_and_commuting_filter_order.md` (`mean_dominant_commuting_filter_order_independent_audit.md`) strengthens the preceding corollary. Under[A,Z*Z]=0 it gives

D(X_Z)>=k0 F_d(A), k0=lambda_min(Z*Z).

Therefore the actual GLS accepted-only comparison gap has strictly positive leading coefficient:

D(X_t)-kappa_t F_d(A)
=t^-2[D(X_Z)+H_d(G)-k0 F_d(A)]+O(t^-4 log t),
D(X_Z)+H_d(G)-k0 F_d(A)>=H_d(G)>0.

Consequently D(X_t)>=kappa_t F_d(A) for every sufficiently large t, with all parameters fixed. The accepted term is exactly the deficit of the actual noise-optimal left-inverse accepted branch, not an abstract lower surrogate. Separate normalization of the entire source divides both terms by the same positive n_t and preserves the inequality.

This receives an asymptotic actual-source region of the earlier open accepted-only GLS target. No uniform attachment threshold and no all-t comparison is asserted. G,C,D need not commute; only the low-seed alignment condition[A,Z*Z]=0 is used. In particular A scalar permits genuinely noncommuting compressed-resolvent paths at finite t.

## Later whole qutrit-seed closure: arbitrary noncommuting large-attachment VALUE

The independently received `arbitrary_qutrit_filtered_seed_whole_value_theorem.md` / `arbitrary_qutrit_filtered_seed_whole_value_independent_audit.md` now pays D(X_Z)>=0 for EVERY invertible Z and arbitrary A>=0, without[A,Z*Z]=0. It applies to the exact non-TP low seed in this expansion because its reference dimension is3 and it is a pure main plus I3 tensor reset. No dimension enlargement or free filter monotonicity is used.

Thus under the present faithful/invertible fixed-parameter hypotheses, the leading coefficient D(X_Z)+H_d(G) is strictly positive for arbitrary C,D0,A, and the original actual TP source has positive deficit for all sufficiently large t. The received O(t^-4 log t) homogeneous remainder proves the eventual sign. The normalized TP deficit still scales as t^-4.

This removes the alignment restriction from the earlier VALUE corollary only. The accepted-only coefficient is D(X_Z)+H_d(G)-k0F_d(A); whole-seed positivity alone does not pay its subtraction. The earlier eventual accepted-only statement remains restricted to the received anchored-filter classes (in particular[A,Z*Z]=0). No arbitrary coherent-reset theorem at all coupling strengths follows.
