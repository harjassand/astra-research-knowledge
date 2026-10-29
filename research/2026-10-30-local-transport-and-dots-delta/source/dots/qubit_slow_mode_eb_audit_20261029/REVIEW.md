# Independent receiving review: uniform qubit slow-mode EB residual factorization
2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`.

## Decision
**PASS** frozen `GOVERNING.md` (SHA-256 4797dcb71300f965547787e5011ec3e7d85a5a2e774910a76f82dca54d2d528d). The initial draft's ambiguous phrase “fixed state” was clarified before freezing to mean Psi(sigma)=sigma. It does not mean an arbitrary externally chosen state, nor stationarity under the original channel Phi in the recovery application.

For a CPTP qubit map Psi with s1(T)^2+s2(T)^2<=1 and any of its stationary states sigma, the construction gives EB CPTP F fixing sigma and HP L with id-F=L(id-Psi), ||L||diamond<=19200. The near-+1-mode case has the stronger constant 72. The structural proof is self-contained; self-compatibility is a sufficient, not necessary, condition for its singular-value premise. The actual-prior Holevo application imports the previously received primary universal-recovery theorem. No historical priority, cheap implementation, many-input-qubit tensorization, correlated-barycenter local recovery, or orthogonal pointer-basis classification is received.

## 1. Biased compatibility really implies the singular bound
A broadcast extension makes the two pulled-back binary Pauli POVMs jointly measurable. Choose orthogonal output left singular axes, so their input Bloch vectors a,b are orthogonal with lengths s1,s2. Biases are not discarded. For the four joint effects G_st=(gamma_st I+g_st dot sigma)/2, positivity implies ||g_st||<=gamma_st and normalization gives sum gamma_st=2 and sum g_st=0. Marginal identities give a+b=g_++-g_-- and a-b=g_+--g_-+. Therefore ||a+b||+||a-b||<=2, or 2sqrt(s1^2+s2^2)<=2. No unbiased-marginal assumption is needed. In particular ||T||<=1 and ||wedge^2 T||=s1 s2<=1/2.

## 2. Separated eigenvalues: all real/complex/nonnormal cases
Eigenvalues of wedge^2 T are pairwise products of the eigenvalues of T, with algebraic multiplicity; this remains true for defective matrices. Their moduli are bounded by the exterior-power operator norm. Thus at most one eigenvalue has modulus greater than 1/sqrt(2), and a conjugate pair has modulus at most 1/sqrt(2). If there is no real eigenvalue >=.99, every factor |1-lambda| is positive; at most one needs the crude lower bound .01, and each of the other two is greater than .25. Real eigenvalues near -1 are harmless. Hence |det(I-T)|>=1/1600.

Since ||I-T||<=2, the norm of adj(I-T), the product of the two largest singular values, is at most four. Thus ||(I-T)^-1||<=6400 without eigenbasis conditioning or a diagonalizability assumption. Replacement by sigma is EB CPTP. Its traceless deficit is the identity, so Lmat=(I-T)^-1 gives the required factorization there. The extension to all operators and complete norm are treated below; they give 19200, not an unstated Hilbert--Schmidt-only bound.

## 3. Slow LEFT mode and corresponding RIGHT direction
For real lambda>=.99, a real normalized LEFT eigenvector w exists. In the orthonormal w/w-perp coordinates, T=[[lambda,0],[a,B]]. The zero upper-right block is precisely why a left eigenvector, not a right eigenvector, must be selected. For unit z in w-perp, Tw=(lambda,a), Tz=(0,Bz). The squared wedge area is at least lambda^2||Bz||^2, giving ||B||<=1/(2lambda)<=.51. Consequently lambda-||B||>=12/25 and 1-||B||>=49/100, with no normality assumption. Neumann/resolvent norm estimates justify every inverse of lambda I-B or I-B.

The column norm gives ||a||<=sqrt(1-lambda^2)<=sqrt(2g), g=1-lambda. Let h=(lambda I-B)^-1 a. Then n=(1,h) is a RIGHT eigenvector normalized by w dot n=1. The bound ||h||<=5/16 is conservative: sqrt(.02)<.15 and lambda-||B||>=.48. This explicitly separates the measurement direction w from the generally tilted preparation chord n.

## 4. Endpoint positivity, including nearly pure and exactly pure stationary states
Write the stationary Bloch vector as s=(u,v); t=(I-T)s. The actual CPTP map's outputs on +/-w have first coordinates +/-[1-g q_sign], q_+=1-u, q_-=1+u, and transverse x_sign=(I-B)v+(+/-1-u)a. Positivity yields ||x_sign||^2<=2g q_sign-g^2 q_sign^2<=2g q_sign.

With p=(1+u)/2, the weighted sum p x_+ +(1-p)x_- equals (I-B)v. Weighted Cauchy--Schwarz gives p sqrt(1-u)+(1-p)sqrt(1+u)<=sqrt(1-u^2), so
||v||<=sqrt(2g(1-u^2))/(1-||B||)<=2sqrt(g q_sign)/(1-||B||)<5sqrt(g q_sign).
This sign-sensitive estimate, rather than a uniform O(sqrt g) bound, is the load-bearing protection near |u|=1.

Put y_sign=v+(+/-1-u)h. Direct substitution gives (lambda I-B)y_sign=x_sign-gv, hence
||y_sign||<4sqrt(g q_sign),
using (sqrt2+2g/(1-b))/(lambda-b)<(3/2+2(.01)/(.49))/(.48)<4. With k=1-16g in [.84,1], the prepared endpoint r_sign=s+k(+/-1-u)n has transverse part k y_sign+(1-k)v, of norm at most 5sqrt(g q_sign). Its longitudinal part is +/-[1-16g q_sign]. Available squared radial slack is 16gq(2-16gq)>=26.88gq>=25gq. Both endpoint Bloch vectors therefore lie in the closed unit ball.

This proves F is the physical two-outcome measure-and-prepare map described, not merely a rank-one affine contraction. It is TP, CP and EB by construction, with F(sigma)=sigma. When q=0 the weighted bound forces the relevant transverse component exactly zero. When g=0, ||a||=0 and output positivity forces (I-B)v=0, hence v=0 and h=0. The construction then becomes ordinary dephasing in w and remains valid for any fixed prior along that axis. No inverse of g is used anywhere in this case.

## 5. Correct all-operator residual and complete norm
For D=(I-B)^-1 and Lmat=[[16,0],[(16I-D)h,D]], multiplication gives I-k n w^T=Lmat(I-T). Specifically the lower-left block is 16g h-gDh-Da=16g h-h=-k h because a=(I-B-gI)h; lower-right is I and upper-left is 16g=1-k. This remains exact at g=0.

The three-block triangle bound gives ||Lmat||<=16+(16+100/49)(5/16)+100/49<24. Extend L by L(I)=0 and the real matrix Lmat on Pauli operators. This map is Hermiticity preserving but is not claimed positive. The traceless-space identity extends to ALL operators because both deficits annihilate sigma: writing I=2sigma-s dot sigma gives their action on the identity from their traceless action. This is where stationarity of the specified sigma is essential, and it is supplied in the frozen theorem.

For each column v_j of Lmat, its rank-one map is X -> Tr(sigma_j X)(v_j dot sigma)/2. Its diamond norm is at most ||sigma_j/2||infinity ||v_j dot sigma||1=||v_j||2, including arbitrary ancillary dimension (the trace functional is completely bounded with this norm). Triangle inequality gives ||L||diamond<=sum_j ||v_j||<=3||Lmat||. The same argument gives 19200 in the inverse case and <72 in the slow case. Therefore the all-state, all-finite-reference trace-distance residual implication follows directly, not via a qubit-only unreferenced norm comparison.

## 6. Actual-prior Holevo application
The imported accepted universal averaged rotated-Petz map R for Phi at its actual input mean sigma is a genuine CPTP map after the documented support completion, and R Phi fixes sigma. It need not fix Phi's stationary state or require sigma stationary for Phi. Applying R independently to both outputs of a self-compatible Phi preserves its symmetric extension, so Psi=R Phi satisfies the structural theorem.

The primary dependency (Junge--Renner--Sutter--Wilde--Winter, arXiv:1509.07127v3, Theorem 2.1 and Remarks 2.2/2.4) was directly checked in the received actual-prior review bound here. With natural logs and unsquared fidelity it gives each trace residual <=sqrt(relative-entropy loss). Averaging at the ACTUAL barycenter makes the average loss exactly delta, the actual Holevo loss; Jensen yields sqrt(delta). The structural F is common to all letters, and gives min(1,19200sqrt(delta)). There is no stationarity penalty kappa or iteration/logarithmic loss.

For product mean sigma_A tensor omega_R, universal recovery factors locally as R_A tensor id_R on the supported reference space. Correlated individual letters and differing reference marginals are allowed. F is EB on A only. An arbitrary correlated barycenter is not covered by this local factorization. If sigma is singular, it is pure; positivity of the mean implies each letter factors as sigma tensor its reference marginal, so local replacement has zero error. This endpoint avoids a singular inverse entirely.

## 7. Evidence and nonclaims
Independent `check_independent.py` tested 448 physical channels: symmetric broadcast isometries, highly biased classical two-outcome channels, complex-pair depolarizing examples, an explicitly defective far-mode EB map, eigenvalue -1, exact dephasing, and both sides of the .99 threshold. There were 342 near-mode cases, 141 near-pure fixed states and 213 complex-pair cases; explicit endpoint norms, Choi/PPT positivity, fixed-point identity and full identity-plus-Pauli factorization all passed. Max factorization residual was 4.6e-14. Eighty-four referenced tests passed with reference factorization residual <7.1e-15. The proof, not PPT tests or observed ratios, establishes the theorem and diamond constant.

An initial floating stationary-state solve for an extremely biased classical fixture at gap approximately 1e-11 produced a spurious Bloch norm above one. It was corrected in the diagnostic by the exact analytic stationary-state formula using half-angle squares. This is numerical conditioning, not a rejected physical example or a change to the theorem. Final tests include the near-pure cases without clipping a physical state into the ball.

The author's 2400 and separate parent 900 cases were copied and replayed successfully; those are supplementary, not substitutes for this independent receiving proof. No native acquisition, efficient recovery compiler, universal higher-input-dimensional extension, historical novelty or orthogonal-pointer theorem is claimed. The EB map may prepare noncommuting states, and a conservative constant 19200 is not a useful practical error threshold.
