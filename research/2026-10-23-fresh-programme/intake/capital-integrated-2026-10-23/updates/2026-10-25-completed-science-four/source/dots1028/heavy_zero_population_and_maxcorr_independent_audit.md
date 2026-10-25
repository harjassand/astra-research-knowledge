# Independent audit: heavy zero-population payment and full maximally-correlated entropy theorem

2026-10-25. Verdict: PASS. Reviewed the original source envelope in `wh3_aligned_zero_population_balanced_face.md`, the proof and exact script in `heavy_zero_population_scalar_theorem.md` / `heavy_zero_population_scalar_certificate.py`, and the combined receiver `wh3_maximally_correlated_inputs_entropy_theorem.md`. No concavity of the full matrix objective is assumed.

## 1. Original source-to-scalar receiver, including complex phases

After diagonal local phase changes, a top vector in the correlated span has coefficients u_i=sqrt(lambda_i)≥0. For positive Schmidt weights, X is Hermitian with 0≤X≤I and Xu=u. Its diagonal x_i satisfies lambda_i≤x_i≤1. The actual pair block K_ij is the sign-conjugated principal X block divided by two, and v_ij=(u_j,−u_i). For the omitted index k, direct use of Xu=u gives

v_ij* K_ij v_ij=(1−2lambda_k+lambda_k x_k)/2,
||v_ij||²=1−lambda_k.

This formula holds even for complex Hermitian X: the cross term is 2u_i u_j Re(X_ij), and the same real part occurs on removing row and column k from u*Xu=1. Consequently scalar spectral Jensen on each actual pair gives exactly g≥sum_k f_(lambda_k)(x_k). A conjugation average is permissible but is not needed for this receiver. No noncommuting source data are silently replaced by an independently chosen diagonal.

For each light weight l≤1/2, the given derivative f_l' is nonnegative and decreasing on [l,1], so f_l is increasing and concave. Its endpoint chord slope is exactly h(l)=log(1−l)−l log l/(1−l). Balanced weights therefore give g≥sum F(lambda_i), the previously certified pure-projector anchor.

For a heavy weight a, put S=X−uu*≥0. The top relation implies Su=0. With Q=I−uu*, S=QSQ and ||Qe0||²=1−a=t, so S00≤t TrS. Therefore the two light diagonal increments obey sum_light(x_i−lambda_i)≥a(x_0−a)/t. The light concave chords are LOWER bounds, and replacing their two positive slopes by their minimum weakens the bound in the correct direction. This proves exactly the original envelope L. The argument is valid for complex S as well.

## 2. Heavy scalar proof

The lower chord payment h(l)≥l(1−2l) is correct. After multiplication by 1−l, the derivative is G(l(1−l)), with G(z)=−log z−3+6z. G decreases then increases, ends below zero at z=1/4, and has exactly one zero on (0,1/4). The primitive starts and ends at zero and is nonnegative. For c≤b and b+c=t≤1/2, the difference of the two polynomial payments is (b−c)(1−2t)≥0, so their minimum is the c payment.

F''(l)=1/l−1/(1−l) is convex on (0,1/2), because its second derivative is 2/l³−2/(1−l)³≥0. Thus the symmetric light pair has the stated quadratic lower bound with m=4a/[t(1+a)]. Expansion of c(1−2c) gives at/2−(2a−1)d−2d². Completing the square has positive coefficient m−2k, bounded below by 2a(1+a²)/[t(1+a)]. Using z²≤tz gives exactly the displayed K(a) coefficient. Its difference from 3a²/8 is a(1−a)(3a²+3a−1)/[8(1+a²)]≥0.

For the heavy coordinate, D=1−2a+ax satisfies 0<D≤tx on [a,1]. Since a≥t, the expression for f_a''' is nonpositive. Hence f_a''≥f_a''(1)=a(2a−1)/t, and integrating backwards from f_a'(1)=0 yields the claimed quadratic lower bound at x=1. The substitution Kz≥Kz²/t is a weakening on z∈[0,t]. Minimizing the sum of the two quadratics gives M K t²/(Mt+2K), which simplifies to the displayed R(a). The combined remaining term is exactly B(a).

B''≥4/3 and the supporting quadratic at 2/3 yield B>−6/1000 using the certified constants. Independently differentiating R gives

R'(a)=−3a(66a³−98a²+47a−8)/[2(11a−4)²].

The cubic has increasing derivative after its unique derivative minimum on [1/2,1], starts negative and ends positive, and has one zero. Thus R has one maximum and no interior minimum there. The endpoint argument on [11/20,4/5] is valid. Outside this interval the derivative signs and strong convexity give the asserted B lower bound. Consequently L>3/1000 throughout the stated heavy domain.

The b=0 or c=0 endpoints follow by continuous extension of l log l and h(l). As a tends to one, x∈[a,1] tends uniformly to one, the potentially singular heavy terms have coefficients t and are O(t|log t|), and the chord payment vanishes. The limiting envelope is log(4/3).

## 3. Exact certificate replay

Replayed `heavy_zero_population_scalar_certificate.py` unchanged, exit 0; all ten Boolean comparisons passed. The log series uses exact Fraction arithmetic, and its omitted absolute tail bound is valid for every positive rational argument used. Sign-sensitive coefficients are handled correctly in the interval linear combination. Floating diagnostics in the JSON are not proof premises. Also independently checked the exact symbolic R' factor above.

## 4. Low-Schmidt-rank anchors and support endpoints

For correlated inputs with a rank-two top vector, the marginal is diagonal and hence commutes with the reduced top projector. The supplied rank-two anchor theorem therefore applies. Its source-preserving phase twirl eliminates couplings to the unused correlated coordinate. In this zero-population class its p and q populations are both zero, so its scalar estimate in fact gives g≥log(4/3). For a rank-one correlated top vector, the relevant output rays both have eigenvalue 1/2 after top normalization and the marginal eigenvalue is 1/3, again giving g=log(4/3).

During the faithful-X receiver these quantities are supported and finite. No continuity in a changing Schmidt rank is needed to fill a gap: positive rank-three weights use the balanced/heavy proof, and zero weights use the lower-rank anchor theorem directly.

## 5. Full-value maximally-correlated spectral receiver

For X>0, lowering the current top eigenvalue until it merges with the next, then lowering the cumulative top eigenspace, stays in the same correlated span. Every top vector of every intermediate matrix is therefore one of the anchors just proved nonnegative, after local diagonal phase adjustment.

The input support is fixed throughout. Each output 2x2 pair is a sign-conjugated positive principal submatrix of X divided by two, hence remains positive definite; the output support is precisely the six offdiagonal matched rays. All reference diagonal entries are positive. Thus the entropy derivative is valid on fixed supported algebras. A formal extension of log NA by zero outside its support is harmless only because each tested output variation is supported there; it is not being used as an unsupported logarithmic identity.

For a top eigenvalue L, the derivative in its rank-one projector equals the normalized top anchor: the log L terms cancel with coefficients 1+1−2. Summing over an orthonormal top eigenspace gives a nonnegative derivative with respect to increasing its common level. Therefore lowering cannot increase Delta. There are finitely many spectral merging steps, ending at mu J, mu=lambda_min(X).

The endpoint is exact: J has three unit eigenvalues, EJ has nine eigenvalues 1/3, and NJ has six eigenvalues 1/2. Hence Delta(J)=3log(4/3), so

Delta(A)≥3 lambda_min(X) log(4/3).

For singular X, replace X by X+epsilon I3 within the same correlated class. The proved bound applies, and finite-dimensional entropy continuity passes to epsilon=0. Reference isometric embeddings merely add zero eigenvalues; local physical/reference basis changes preserve the channel entropy budgets by covariance. There is no problem with a larger reference or missing correlated coordinates.

Conclusion: the full target is proved pointwise for all maximally-correlated inputs, including arbitrary three-level correlated spectra and noncommuting reference modular structure. This remains a proper support class, not an arbitrary-input or arbitrary-population theorem.
