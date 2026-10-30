# Independent audit: two-round Gaussian quadratic information

30 October 2026. P1 alternative/construction review. These are ordinary derivations and finite checks, not historical-priority clearance.

## Model and conditioning

The input is X~N(0,I_n). The known target is f(X)=X^T A X+b^T X+c, with A real symmetric. An algorithm obtains noiseless scalar linear observations; each vector can depend measurably on previous observations and an independent random seed. Arbitrary vectors and exact real arithmetic are the access model. Linear dependence can be removed, and each nonredundant new vector orthogonalized against the preceding ones.

Inductively, after t such observations, X=m+Z conditional on the full transcript, where m is the observed projection, Z~N(0,Q), and Q is the orthogonal projection onto the unobserved complement. Although Q is random, it is fixed when conditioning on that transcript. The induction chooses the next unit vector u in range(Q), then u^T Z is N(0,1) and the remainder is an independent Gaussian on range(Q-uu^T). Measurable discontinuous direction choices do not add information beyond the observations on which they depend.

The conditional Bayes risk is exactly

`2||QAQ||_F^2 + ||Q(b+2Am)||^2`.                              (1)

The quadratic and linear centered Gaussian terms are orthogonal. This is the critical formula; dropping the linear term is a lower bound only, not an equality in general.

## Signed spectral lower bound

Let lambda_1>=...>=lambda_p>0 be positive eigenvalues and mu_1>=...>=mu_q>0 the magnitudes of negative eigenvalues. Define

`B(k)=2[sum_{j>k}lambda_j^2+sum_{j>k}mu_j^2]`.

For any projection Q of codimension at most k, compression interlacing gives

`||QAQ||_F^2 >= sum_{j>k}lambda_j^2+sum_{j>k}mu_j^2`.

Together with (1), every adaptive hard-k policy has risk at least B(k). The same holds for expected budget k, with piecewise-linear interpolation of B: for a random stopping count K, conditional risk is at least B(K); B is decreasing and convex, so E B(K)>=B(EK)>=B(k). Assume the policy returns almost surely and charge distinct nonredundant scalar observations; repetitions carry no new information.

When A is PSD or NSD and b=0, top-k eigenvector observations attain B(k). There is no adaptive advantage at that same budget, including expected integer budget.

## Two-round construction with one extra observation

Pair the i-th positive and negative eigenvectors for i<=min(k,p,q). Write their eigenvalues as lambda and -mu. Use the orthonormal coordinates

`u=(sqrt(lambda)e_+ - sqrt(mu)e_-)/sqrt(lambda+mu)`,

`v=(sqrt(mu)e_+ + sqrt(lambda)e_-)/sqrt(lambda+mu)`.

In this basis, that two-dimensional block is

`(lambda-mu)U^2+2sqrt(lambda mu)UV`.

Query u. The unobserved v direction has zero quadratic compression. If a sign is exhausted before k pairs are available, query the remaining leading eigenvectors of the other sign. The resulting first-stage projection P has rank at most k; its complement Q leaves compression B=QAQ consisting of the signed tails past k, together with zeros. Therefore

`2||B||_F^2=B(k)`.

Given first-stage mean m, form `t=Q(b+2Am)`. If t=0, no final observation is necessary. Otherwise query `z=w^T X`, where w=t/||t||. Since w is orthogonal to the first-stage range, z=w^T Z. Conditional on the first stage,

`f=C(m)+t^T Z+Z^T B Z`,

where C(m)=m^TAm+b^Tm+c. The linear term is now exactly known. The final Bayes estimator is

`C(m)+||t|| z+tr(B)+(w^T B w)(z^2-1)`.

Its conditional-first-stage mean squared risk, averaging over z and the remaining Gaussian coordinates, is EXACTLY

`2||B||_F^2-2(w^T B w)^2 <= B(k)`.                           (2)

Indeed, if R=Q-ww^T, the terminal conditional risk equals

`2||RBR||_F^2+4z^2||RBw||^2`.

Averaging z^2=1 and decomposing the Frobenius norm gives (2). Thus no cross term has been omitted.

For b=0, t lies in the zero-compression paired directions, hence Bt=0. The achieved risk is exactly B(k). For general b the risk can be strictly smaller. In all cases, at most k+1 observations in two rounds match or improve on the risk of every fully adaptive k-observation policy.

For noninteger expected budget k, randomly choose the first-stage count floor(k) or ceil(k) with the appropriate probabilities. Its expected first-stage count is k, expected risk is at most the interpolated B(k), and expected total count is at most k+1. This is an explicitly randomized construction; no optimal-policy oracle is used.

## Exact information complexity of a quadratic

This part is pointwise and does not need a Gaussian prior. Let A have inertia (p,q,z). A maximal totally A-isotropic subspace L has dimension z+min(p,q). Observe its Euclidean orthogonal complement first, using max(p,q) observations. Since L^T A L=0, f restricted to the unobserved affine fiber is linear. One final observation in direction Q(b+2Am) evaluates it exactly. The paired construction above explicitly builds such L.

The worst-case exact scalar-linear-query count is:

* 0 if A=b=0;
* rank(A) if A is PSD or NSD and b is in range(A);
* rank(A)+1 if A is PSD or NSD and b is not in range(A);
* max(p,q)+1 if A is indefinite.

The upper constructions were just described. For the lower bound, any terminal transcript freezes its queried directions, and its fiber is an affine subspace. Exact constancy of f on this fiber forces its direction L to be totally A-isotropic and perpendicular to 2Ax+b. Thus at least max(p,q) observations are necessary. If exactly that many are used, L is maximal isotropic and contains ker(A).

If b has a kernel component, b perpendicular to L is impossible, so one extra observation is necessary. Otherwise complete the square with y=x+(1/2)A^dagger b. Suppose p>=q>0. On L^{perp_A}, the quadratic form is PSD: its radical is L and its nondegenerate quotient has positive dimension p-q. Therefore every input with y^T A y<0 is impossible to resolve after p observations. This is a nonempty open set. The p<q case uses the positive cone. Consequently the indefinite lower bound max(p,q)+1 is sharp. The same hard-budget lower bound holds for zero-error almost-sure computation under any full-support absolutely continuous input law, including a Gaussian: the obstructing cone has positive probability; conditional laws are absolutely continuous on the realized affine fibers; and a polynomial constant almost surely under such a law must be constant on the full fiber. Full support of every conditional density is not needed and does not follow from full support of the original density.

The expected-budget exact optimum is not classified by this pointwise argument; do not silently promote the hard-count lower bound to an expected-count equality.

## Sharpness of factor two for fully fixed experiments

For independent U,V~N(0,I_m), f=2 U^T V has p=q=m and every nonzero eigenvalue has magnitude one. Querying all m coordinates of U and then the scalar projection of V along U computes f exactly using m+1 observations. Any fixed exact linear experiment needs 2m observations: a fixed unobserved direction must lie in ker(A), which is zero. The ratio tends to two.

More generally, observing k-1 U coordinates and the aligned V projection captures variance 4(k-1), leaving risk 4(m-k+1), for 1<=k<=m+1. The best fixed r-dimensional observation subspace has risk 4m-2r. This illustrates genuine adaptive gradient alignment; it does not by itself establish the optimal adaptive risk for each k.

For a general homogeneous Gaussian quadratic the exact strongest fixed-r risk is `2 sum_{j>r} s_j(A)^2`, where singular values are ordered decreasingly. A fixed projection P captures variance `2||PAP||_F^2`; singular-value interlacing bounds this by the leading r squared singular values, attained by their eigenvectors. This comparator permits every fixed r-dimensional subspace, not just coordinate selection.

## A useful same-budget failure

The paired-then-gradient compiler is not claimed optimal at its own query budget. For f=2 U^T V with m>=2, the exact optimal two-query explained variance is approximately 4.716565402244797. Both the two-read paired-then-gradient construction and the best fixed two-read construction capture only 4.

The improving policy first reads U_1=y. If `4y^2>=2`, read V_1; otherwise read a unit eigenvector of eigenvalue +1 or -1 on an unused pair. The conditional second-read gain is `max(4y^2,2)`.

For completeness this is optimal among all two-read policies. Write A for the involution defining 2 U^T V, and let a=u^T A u be the Rayleigh quotient of an arbitrary first unit direction u. Its first-read gain is 2a^2. The compressed matrix has one eigenvalue -a on the residual direction v proportional to Au-au, and all other nonzero eigenvalues are +/-1. The conditional linear residual is `2 sqrt(1-a^2) y v`. If a candidate second direction has squared v-component s, its gain is at most

`2[1-(1-|a|)s]^2 + 4(1-a^2)y^2 s`.

This is convex in s in [0,1], hence its maximum is at an endpoint and equals `max(2,2a^2+4(1-a^2)y^2)`. Both endpoints are attainable when m>=2. Averaging and adding first-read gain gives

`2+2a^2+(1-a^2) C`, where `C=E[(4G^2-2)_+]`.

Here `C=8r phi(r)+4[1-Phi(r)] = 2.7165654022447967`, with r=1/sqrt(2). Since C>2, the optimum is a=0, giving 2+C. The k+1 comparison theorem survives: it pays one extra observation to dominate these more intricate k-read effects.

The scalar-read model is material. If a dense linear measurement is implemented by individually acquiring all coordinates, the last projection costs those acquisitions. The theorem does not make a physically expensive dense measurement free. Its construction arithmetic is O(nk) per dense vector implementation after the model and eigenspaces are acquired; preprocessing and numerical precision must be separately charged.

## Source comparison and availability

The established no-adaptation literature for linear Gaussian problems includes Wasilkowski and Wozniakowski (1984), Can adaption help on the average?; Lee and Wasilkowski (1986), Approximation of linear functionals on a Banach space with a Gaussian measure; and Wasilkowski (1986), Optimal algorithms for linear problems with Gaussian measures. Ritter's official chapter reference list verifies these locators:

https://link.springer.com/chapter/10.1007/BFb0103941

The corresponding nonlinear chapter and its public reference list concern principally zero finding and global optimization:

https://link.springer.com/chapter/10.1007/BFb0103942

The public chapter pages and references were read. The chapter bodies are subscription content and were not available. Publisher PDF attempts yielded access/challenge responses, not mathematical fulltext. No inference of novelty from that absence is justified. Targeted searches have not found the exact signed-tail/two-round quadratic theorem, but historical novelty remains unresolved.

The primary abstract of Wasilkowski and Wozniakowski (1984), read at the publisher and author institution, explicitly limits its no-adaptation theorem to linear problems under orthogonally invariant measures (including Gaussian measures):

https://link.springer.com/article/10.1007/BF01410103

https://scholars.uky.edu/en/publications/can-adaption-help-on-the-average/

Arias-Castro, Candes and Davenport, On the Fundamental Limits of Adaptive Sensing (2011, revised 2012), was read from arXiv. Its strongest comparisons concern recovery of an unknown sparse vector from noisy norm-constrained linear measurements; the target, prior/minimax criterion and noise regime differ from a known quadratic scalar target under a Gaussian input. It therefore is a relevant access-model comparator, not a direct source for the signed-tail theorem:

https://arxiv.org/abs/1111.4646

The retrieved Dagstuhl 2002 abstract by Stefan Jaschke, Quadratic Forms of Gaussian Vectors (Quadratic Approximations in Risk Measurement), concerns approximation of the distribution/quantiles of quadratic Gaussian forms. It does not state a sequential observation theorem. This was an investigated but nonmatching lead:

https://drops.dagstuhl.de/opus/volltexte/2021/15236/pdf/DagSemRep-356.pdf

The ingredients—Gaussian conditioning, conditional expectation, eigenvalue interlacing, Sylvester inertia and maximal isotropic subspaces—are established mathematics. The candidate contribution is their explicit information-complexity construction and comparator consequence, if a fuller literature review confirms that it is not already known.

## Executable independent audit

`check_gaussian_quadratic.py` produced `check_gaussian_quadratic_results.json`: 384 final-risk checks using tensor three-point Gauss--Hermite quadrature; 192 paired-compression checks; 576 arbitrary-projection lower-bound checks; 480 pointwise exact reconstructions. All passed. Maximum relative risk discrepancy was 3.51e-15; maximum absolute pointwise reconstruction discrepancy was 2.14e-14. The squared residual is degree four in the conditional Gaussian coordinates, so the quadrature rule is exact in exact arithmetic. This is a finite floating-point implementation check, not a substitute for the ordinary proof.
