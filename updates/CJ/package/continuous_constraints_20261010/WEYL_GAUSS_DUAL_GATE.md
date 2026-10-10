# Weyl reduction of harmonic Gauss-law acquisition: the D=2 gate

Date: 2026-10-10. Companion to `GAUSS_PHYSICS_CAPABILITY.md`. These are exact mathematical reductions and boundaries. A polynomial-time sampler for growing gauge size is not established here.

## 1. Exact reduced density

For D harmonic traceless Hermitian k-by-k coordinate/momentum pairs, let

    m=k²−1, q=Dm,
    G=−i sum_{a=1}^D [X_a,P_a].

The positive dual on the real vector space of traceless Hermitian Lambda is

    v_D(Lambda)=det_R(I+L_Lambda L_Lambda^*)^(−D/2),
    L_Lambda(U)=−i[Lambda,U].

If Lambda has real eigenvalues mu_1,...,mu_k summing to zero, each unordered pair a<b gives two real singular directions of magnitude |mu_a−mu_b|. Thus

    v_D(Lambda)= product_{a<b} [1+(mu_a−mu_b)²]^(−D).

Weyl's change of variables supplies the Vandermonde squared. With respect to induced Euclidean measure on the trace-zero eigenvalue hyperplane, the normalized eigenvalue density is proportional to

    f_{k,D}(mu) = product_{a<b} [(mu_a−mu_b)² / (1+(mu_a−mu_b)²)^D].       (W1)

The eigenbasis is independent Haar; use Lambda=U diag(mu) U*, with Haar U(k) or SU(k). Ordered eigenvalues suffice because Haar U includes permutations. All quotient/permutation/gauge-volume constants cancel in the normalized law.

In the rational tight-frame construction of the companion report, the denominator is `1+4(mu_a−mu_b)²`; rescale the eigenvalues by 2 to obtain W1. There is no substantive change of distributional family or cost.

For ordered eigenvalues, define gaps

    t_j=mu_{j+1}−mu_j >=0, j=1,...,k−1.

Let z_1=0, z_a=sum_{j<a}t_j, and mu_a=z_a−(1/k)sum_b z_b. The induced Euclidean Jacobian is `1/sqrt(k)`; equivalently `delta(sum mu) product dmu` gives the constant `1/k`. Hence normalized gap density is

    p(t) proportional product_{1<=a<b<=k} f_D(t_a+...+t_{b−1}),
    f_D(s)=s²/(1+s²)^D.                                          (W2)

After sampling Lambda, every X_a can be drawn by diagonalizing only Lambda: its diagonal traceless Gaussian directions have their prior covariance, and both real off-diagonal directions for each pair are scaled by `1/sqrt(1+(mu_a−mu_b)²)`. Then sample projected Gaussian momenta using the usual Gauss linear system. This gives the original bilinear target, conditional on having acquired the correct W1 law.

## 2. D=2 integrability, with an elementary envelope

For D=2,

    f_2(s)=s²/(1+s²)² <=1,
    f_2(s)<=1/(1+s²).

Retain only adjacent-pair factors in W2 and bound every other factor by 1. Then

    p_unnormalized(t) <= product_{j=1}^{k−1}(1+t_j²)^−1,
    integral_[0,infinity)^(k−1) p_unnormalized(t) dt <= (pi/2)^(k−1).  (W3)

The density is strictly positive on, for example, all gaps in (1,2), so its normalizer is positive and finite for **every k>=2**. The failure of stable-rank r=2k to exceed m=k²−1 is therefore entirely a failure of that isotropic envelope, not failure of the target to exist.

W3 also gives a native independent half-Cauchy gap rejection sampler in ideal arithmetic. It says nothing favorable about acceptance as k grows. A supplied sampler must charge that probability rather than quietly treating a finite normalizer as an efficiency guarantee. A separate worker is studying stronger proposals; this note makes no claim about that ongoing construction.

## 3. Sharp integrability criterion for the real-D extension

Although integer D counts matrix pairs, the eigenvalue family W1 makes sense for real D. For k>=2,

    Integral f_{k,D}(mu) dmu on sum mu=0 is finite
    if and only if D>1+1/k.                                  (W4)

### Necessity

Restrict to a cone in which every adjacent gap is between R and 2R up to fixed shape ratios, so all pair distances are comparable to R. There are K=k(k−1)/2 pairs and k−1 independent gaps. The large-radius integral is comparable to

    integral^infinity R^(k−2 − 2(D−1)K) dR.

It diverges when `2(D−1)K<=k−1`, equivalently `(D−1)k<=1`. This includes all D<=1. At equality the divergence is logarithmic.

### Sufficiency

Let alpha=D−1>1/k. Since

    f_D(s) = [s²/(1+s²)](1+s²)^−alpha <= (1+s²)^−alpha,

it suffices to integrate the latter product. Decompose positive gap space into the finitely many sectors specifying the order of the k−1 gap magnitudes and how many exceed 1. Within one sector let `t_(1)>=...>=t_(h)>=1` be those large gaps.

Assign each pair of eigenvalues to the largest adjacent gap contained between them. Its distance is at least that gap. Let c_j be the number of pairs assigned to t_(j), and C_l=sum_{j<=l}c_j. Deleting the l largest gaps cuts the ordered eigenvalue list into l+1 nonempty consecutive clusters of sizes n_1,...,n_(l+1). Pairs assigned to these gaps are exactly cross-cluster pairs, so

    C_l=(k²−sum_a n_a²)/2
       >= l(2k−l−1)/2.

The inequality uses `sum n_a² <= (k−l)²+l`, maximized by one large cluster and l singletons. Therefore, for every l<=h<=k−1,

    2alpha C_l >= alpha l(2k−l−1) >= alpha lk > l.

The integrand on the sector is bounded by `product_j t_(j)^(−2alpha c_j)`. Set u_j=log t_(j), with u_1>=...>=u_h>=0, and then v_l=u_l−u_(l+1)>=0 (u_(h+1)=0). Including the dt Jacobian, the integral is bounded by

    product_{l=1}^h integral_0^infinity exp[−(2alpha C_l−l)v_l] dv_l
      = product_{l=1}^h (2alpha C_l−l)^−1 < infinity.

The small gaps range over a bounded set, and all omitted pair factors are at most 1. Summing finitely many sectors proves sufficiency. This is a direct proof, not an appeal to an unverified matrix-integral convergence theorem.

## 4. A genuine D=2 precision obstruction

The original stable-rank finite-output proof transfers Gaussian small-singular-value estimates with an L² bound for the configurational tilt

    w(X)=det[F(X)F(X)^T]^(−1/2).

For D=2 that L² quantity is **infinite for every k**, even though W4 proves the target's normalizer finite. In minimal physical coordinates q=2m. Since `F(rX)=rF(X)`,

    w(rX)² = r^(−2m)w(X)².

On any open angular cone of full-rank F, the near-origin contribution to the Gaussian prior integral of w² has radial factor

    r^(q−1) r^(−2m) dr = dr/r.

It diverges logarithmically. Such an angular cone exists: take one traceless diagonal X with distinct eigenvalues and a second Hermitian X having every off-diagonal entry nonzero. Their common Hermitian commutant is scalar, hence their common traceless commutant is zero and F has full row rank. Full row rank persists on a neighborhood.

More generally, the same radial obstruction forces `E_prior w^p=infinity` for p>=D. Thus D=2 cannot inherit the earlier L² precision theorem by sharpening its stable-rank constant. Possible replacements include a quantitatively certified L^p estimate with 1<p<2, or a direct analysis conditioned on a bounded dual variable plus polynomial small-ball bounds. Neither replacement is proved in this note.

## 5. Exact Cauchy identity and the closest checked antecedent

For real mu and

    C_ab=1/[1+i(mu_a−mu_b)],

Cauchy's determinant identity gives

    det C = product_{a<b} (mu_a−mu_b)²/[1+(mu_a−mu_b)²].          (W5)

Consequently

    f_{k,2}(mu)=det C * product_{a<b}[1+(mu_a−mu_b)²]^−1.        (W6)

The additional product in W6 is not constant or a one-body weight. Squaring det C would give Vandermonde to the fourth power, which is the wrong ensemble. The alternating permutation expansion of det C is not a positive mixture sampler.

[**Kazakov, Kostov and Nekrasov, D particles, matrix integrals and KP hierarchy**, Nucl. Phys. B 557 (1999), arXiv:hep-th/9810035](https://arxiv.org/pdf/hep-th/9810035), eqs. (3.1)–(3.2), already use the Cauchy identity for the D=1 pair factor with an external one-body potential. Their grand canonical formulation becomes a Fredholm determinant. This is a close classical antecedent for the determinant manipulation; the extra D2 interaction is not supplied by it.

[**Vescovi and Zarembo, Loop equations for generalised eigenvalue models**, SciPost Phys. 17 (2024) 017, arXiv:2402.13835](https://arxiv.org/html/2402.13835), eq. (1.1), formulates general difference-type measures; eqs. (4.63) and (6.1) identify the Hoppe measure `mu(s)=s²/(1+s²)` with a confining Gaussian potential. Our D2, zero-external-potential, trace-fixed model belongs to the wider difference-measure class but is not that solved Hoppe ensemble. The paper does not supply a polynomial independent sampler for this particular case.

A conventional Cauchy random-matrix ensemble instead has an individual eigenvalue weight such as `product_a (1+mu_a²)^−gamma` times Vandermonde squared. That is different from W1's pair-difference denominator. Neither a Cauchy random-matrix draw nor a standard Student eigenvalue law can be substituted without a derivation.

## 6. Applied interpretation and remaining gate

The exact physics identification remains Harmark–Orselli arXiv:1409.4417, §5.2, eqs. (5.15)–(5.18): zero-coupling classical Spin Matrix Theory. D=2 is their detailed flavor-SU(2) case; gauge k is independent and can grow. This is a more consequential parameter match than choosing D=9 solely for the original matrix-model analogy.

The reduction closes a real mathematical gap: the relevant D2 ensemble is normalizable at all gauge ranks and has a directly accessible k−1-dimensional positive rational eigenvalue density. It also precisely locates the remaining gates: charged large-k eigenvalue acquisition, verified precision near singular Gauss matrices, and comparison against specialized matrix-model methods. None can be waived by noting that eigenvalue dimension dropped or that the partition function is finite.
