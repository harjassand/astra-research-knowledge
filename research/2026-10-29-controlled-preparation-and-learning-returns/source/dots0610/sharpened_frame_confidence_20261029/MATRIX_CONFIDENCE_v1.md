# A matrix-martingale certificate for the existing no-reset probe bank
2026-10-29. Author construction, awaiting independent review. This tightens a stated sufficient certificate, not the learning algorithm or source assumptions.

## Same physical experiment, same predictable target
Use the original common randomized product-Pauli bank and 16x9 transfer estimator X_r for each star edge. The source may depend arbitrarily on previous records and retained quantum memory. Current preparation/sign/measurement settings are fresh and private. Define T_r=E[X_r|F_(r-1)] and Tbar=m^-1 sum T_r. Under the original trusted preparation/readout boundary this is the actual predictable occupation-average pair transfer matrix. No reset, stationarity or independent source outcomes are assumed.

For one site let f=(1,3s e_c), where c is uniform in three axes and s uniform in two signs. Put v=f_i tensor f_0, let j=(z_i,z_0) be the uniformly chosen pair of output axes, and w=y_i y_0 in{+1,-1}. Then X=9w v e_j^T. Its operator norm is exactly90 because ||f||²=10 and ||v||²=100. Moreover, conditional on the past,

 E[XX^T]=81 D tensor D <=729 I_16, D=diag(1,3,3,3),
 E[X^T X]=900 I_9.

These identities do not condition on quantum outcomes. The outcome signs square to1, the input feature coordinates are independent fresh coins, and output axes remain uniform. Thus they hold for every current global CPTP source, including arbitrary nonunital and adaptive retained-memory dynamics.

Each column of T is the normalized Pauli coefficient vector of N_pair†(P_a tensor P_b). A unital CP adjoint maps this Hermitian unitary to a Hermitian contraction, so its normalized Hilbert-Schmidt norm is at most1. Therefore ||T||<=||T||F<=3. Centered Z=X-T satisfies ||Z||<=93 and

 E[ZZ^T]=E[XX^T]-TT^T <=729 I,
 E[Z^T Z]=E[X^T X]-T^T T <=900 I.

## Exact sufficient radius
Apply Tropp, 'Freedman's inequality for matrix martingales', arXiv:1101.3039v1, Corollary1.3, to the rectangular martingale sum Z_r. The self-adjoint dilation has dimension16+9=25 and predictable quadratic variation at most900m. Hence for a fixed bank endpoint m and E=n-1 star edges,

 Pr[max_edge ||That-Tbar|| >= e] <=25E exp[-m e²/(2(900+31e))].

Set ell=log(25E/delta). The positive quadratic root

 e=(31ell + sqrt((31ell)²+1800m ell))/m

is a sufficient simultaneous operator radius. The edge union bound needs no independence between edge estimates. For m=1,000,000,E=3,delta=.05 it is approximately.115 rather than the earlier entrywise-amplified.556. This is an application of established matrix concentration, not a new concentration inequality.

Primary source read: https://arxiv.org/html/1101.3039 , Corollary1.3 and proof via block self-adjoint dilation. The displayed Corollary1.3 exponent in retrieved text has a duplicated minus sign. We use the unambiguous negative exponent from Theorem3.1, followed by its printed bound h(u)>=(u²/2)/(1+u/3), to derive the stated negative Bernstein exponent; no inference depends on treating the duplicated sign literally.

## Data-only kernel/gap and improved geometric rounding certificate
The structural promise supplies a fixed C in SO(3) with Mbar vec(C)=0; it is not inferred from a small residual. Let c=vec(C)/sqrt3. Sort singular values of Mhat=That-J as s1<=s2<=...<=s9, with corresponding smallest right singular vector v1. On the concentration event, ||Mhat c||<=e. If s1>e, the promised common-kernel model is rejected at that confidence. If s2>e, its actual occupation gap is at least s2-e>0.

A sharper rounding argument avoids the earlier residual bound2e/(s2-e). If s1<=e<s2, the singular-coordinate expansion gives

 1-|<v1,c>|² <= alpha²=(e²-s1²)/(s2²-s1²).

Thus c is within h=sqrt(2-2sqrt(1-alpha²)) of one of ±v1. Compute r_plus=min_(R in SO3)||R-sqrt3 reshape(v1)||F and r_minus similarly for -v1 using determinant-corrected polar decomposition. If one branch has r_wrong>sqrt3 h, it cannot contain C. The other polar rotation Chat then obeys

 ||Chat-C||F <= r_chosen+sqrt3 h.

This is a confidence statement based entirely on the measured matrix and declared radius; it uses no true simulator frame or true bath access. It may be nontrivial even when the old sufficient sign condition fails. It does NOT itself imply a small operational memory error; propagate the actual proved frame bound into the governing service theorem, or use the model-free guard.

## Stopping, SPAM and scope
A single declared m endpoint uses the displayed delta. For repeated looks, allocate delta_j with sum<=delta to declared endpoints or use a separately justified time-uniform boundary; do not reuse fixed-endpoint delta at every look. An endpoint selected using unaccounted data is not covered.

The quadratic-variation bounds still hold if binary readout distributions are imperfect, but their conditional means may no longer equal the ideal transfer matrices. If per-call actual-versus-ideal full classical-record total variation is bounded by tau_r uniformly at the boundary, then ||E X_actual-E X_ideal||<=180 tau_r, since each X has norm90. For imperfect SPAM, the actual conditional mean need not have norm<=3. Use centered increment bound R=180 (always valid because ||X||=90), or R=min(180,93+180 max_r tau_r) when the declared uniform TV bounds are available. Replace31=93/3 in the radius formula by R/3, then add beta=180 average tau_r to that radius before ideal common-kernel/gap analysis. The second-moment bound900 remains valid because input/output setting coins retain their specified distribution and recorded outcomes remain binary. This is conservative and requires an acquired/trusted SPAM bound; this note does not infer it from these same counts. Correlated setting leakage can invalidate the channel/common-kernel interpretation and is outside the guarantee.

A positive occupation gap certifies excitation of the sampled past average conditional on the structural promise. It does not certify that future channels obey the promise or remain excited. Historical v4 note that its OLD .556 certificate did not stop remains correct; this new matrix bound can change the certificate without changing that frozen record.
