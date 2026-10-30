# Independent audit: all observations noisy, strong fixed comparator

30 October 2026. Construction from root; independent derivation and checks here.

## Access model and adaptive protocol

Let U,V be independent standard m-dimensional Gaussian vectors, and let

`F=U^T V/sqrt(m)`.

Thus Var(F)=1. Each scalar linear read has a direction of Euclidean norm one and independent additive N(0,s) noise. Directions may depend on earlier readings. Assume 0<s<=1 for the sharp fixed-design comparison below.

Use m first-stage reads `Y=U+epsilon`, with independent noise covariance s I. Define `alpha=1/(1+s)` and `w=Y/||Y||`; the zero-probability event Y=0 can use any unit vector. Read `Z=w^T V+eta`, with eta~N(0,s) independent of everything before it.

Conditional on Y and Z,

* U has mean alpha Y and covariance (1-alpha) I;
* V has mean alpha w Z and covariance I-alpha ww^T;
* these posterior vectors are independent.

The Bayes predictor is therefore `alpha^2 ||Y|| Z/sqrt(m)`. Since Z conditional on Y is N(0,1+s), its explained variance is

`alpha^4 E||Y||^2 (1+s)/m = alpha^2`.

The mean squared risk is exactly `1-alpha^2`, using m+1 noisy scalar reads. All m first-stage measurements and the final measurement are noisy. No exact coordinate read is hidden in the protocol.

Conditional on a fixed first-stage y, the risk averaged over the final read is

`(1-alpha)[1+alpha^2 ||y||^2/m]`.

This also follows directly by writing both posterior Gaussian vectors and integrating the squared residual. Averaging E||Y||^2=m/alpha gives 1-alpha^2.

## Exact strongest fixed-q comparison

Let q<=2m fixed reads be encoded as a q by 2m matrix M with unit-norm rows. Repeated, nonorthogonal and mixed-U/V directions are all permitted. Set H=M^T M; then H is PSD, rank(H)<=q and tr(H)=q. The covariance of the posterior mean of X=(U,V) is

`P=H(H+sI)^(-1)`.

Write `F=X^T A X`, with `A=[[0,I],[I,0]]/(2sqrt(m))`; hence `A^2=I/(4m)`. The exact fixed-design explained variance is

`2 tr(A P A P)`.

Writing A=S/(2sqrt(m)), with S symmetric orthogonal, Frobenius Cauchy--Schwarz gives

`2 tr(A P A P)=tr(P S P S)/(2m)<=tr(P^2)/(2m)`.

Let t_1,...,t_q be the nonzero eigenvalues of H padded with zeros to q. Their sum is q. For `g_s(t)=t^2/(s+t)^2`, the tangent line at t=1 globally majorizes g_s on [0,infinity) when 0<s<=1. The exact algebraic difference is

`g_s(1)+g_s'(1)(t-1)-g_s(t)`

`=s(t-1)^2(2t+s-s^2)/[(1+s)^3(s+t)^2]>=0`.

Summing and using sum t_j=q yields `tr(P^2)<=q/(1+s)^2=q alpha^2`. Consequently every fixed design has explained variance at most `q alpha^2/(2m)`. Equality is attained by q orthonormal eigenvectors of A. The exact optimum fixed-q Bayes risk is therefore

`R_fixed(q)=1-q alpha^2/(2m)`, for 0<=q<=2m and 0<s<=1.

The conclusion includes independent randomization of the fixed design: condition on its seed, apply the bound, and average. If fixed-design count is independently randomized with each realization q<=2m, the same linear bound applies to expected q. No statement is made here for general counts exceeding 2m or for arbitrary adaptive policies.

## Concrete scale

At m=128 and s=0.01, the adaptive construction uses 129 reads and has risk approximately 0.0197039506. The best fixed 129-read experiment has risk approximately 0.5060226939. All 256 orthogonal fixed reads are needed to reach the adaptive protocol's risk within the q<=256 comparison range.

This is a scalar-linear sensing statement. Implementing the final dense projection by first acquiring every V coordinate changes the acquisition cost, and the theorem does not claim that implementation is free. The known bilinear target has a compact representation and does not require learning an unknown dense matrix.

## General homogeneous selected-pair formula

For a selected (+lambda,-mu) eigenspace pair, the isotropic basis transforms the target into `(lambda-mu)U^2+2sqrt(lambda mu)UV`. The first noisy U read contributes explained variance `2 alpha^2 (lambda-mu)^2`. After all such first-stage reads, one noisy read aligned with the vector `(sqrt(lambda_i mu_i)Y_i)_i` contributes total cross-term explained variance `4 alpha^2 sum_i lambda_i mu_i`. These predictor terms are orthogonal because the final noisy read has zero conditional mean given the first stage.

Their sum is `2 alpha^2 sum_i(lambda_i^2+mu_i^2)`, namely alpha^2 times the variance energy in the selected pairs. Selected unpaired eigenvectors contribute `2 alpha^2 lambda_i^2`. This proves an attained risk formula. It does not establish a comparison against every adaptive noisy policy for arbitrary A.

## General quadratic: full orthonormal noisy quality with fewer reads

This extension includes an arbitrary linear term and holds for every finite s>=0. Choose a first-stage orthonormal matrix U such that its orthogonal complement has zero compression `QAQ=0`. With a maximal isotropic complement, the number of first reads is r=max(p,q), where (p,q,z) is the inertia of A.

Complete U to an orthogonal coordinate basis and write the target as

`a^T H a+2a^T C v+b_U^T a+b_Q^T v+c`,

where a and v are independent standard Gaussian coordinate vectors and the v-quadratic block is zero. Read every coordinate of a with independent noise variance s: `Y=a+epsilon`. Set alpha=1/(1+s), mu=alpha Y and v0=1-alpha. The first-stage posterior mean of the target is

`C0=c+mu^T H mu+v0 tr(H)+b_U^T mu`.

Its residual linear coefficient in the unobserved v coordinates is `t=b_Q+2C^T mu`. If t is nonzero, make one further noisy unit-direction read

`Z=(t/||t||)^T v+eta`,

and output the exact conditional predictor `C0+alpha ||t|| Z`. If t=0, the final read is unnecessary. Independence of the a posterior and v given Y, and zero conditional mean of Z given Y, show that the first- and second-stage gains are orthogonal.

Because mu~N(0,alpha I), the first-stage gain is

`2 alpha^2 ||H||_F^2+alpha ||b_U||^2`,

and the final gain is

`alpha E||t||^2=alpha ||b_Q||^2+4 alpha^2 ||C||_F^2`.

Since the remaining diagonal block is zero, `||A||_F^2=||H||_F^2+2||C||_F^2`. Therefore total explained variance is exactly

`2 alpha^2 ||A||_F^2+alpha ||b||^2`,

and the risk is exactly

`2(1-alpha^2)||A||_F^2+(1-alpha)||b||^2`.

This is the same Bayes risk as observing every coordinate of any full fixed orthonormal basis with noise variance s, using at most r+1 reads instead of n. All first-stage and final reads are noisy. This compares with that explicit full orthonormal experiment; it does not claim optimality against all noisy adaptive policies or all fixed designs at every noise level.

An approximate residual vector `t_hat` can be handled without relative normalization accuracy. If the last direction is `w=t_hat/||t_hat||` and the decoder uses `C0+alpha ||t_hat||Z`, its risk exceeds the exact-gradient construction's conditional-first-stage risk by exactly `alpha ||t-t_hat||^2`. This identity follows by expanding the decoder MSE using `E[Z^2|Y]=1/alpha` and `E[(f-C0)Z|Y]=t^T w`. If `t_hat=0`, skipping the read has the same stated excess. This assumes C0 is computed exactly for the chosen model; errors in the model itself are covered separately by the L2 transfer lemma.

## Scope of the noise restriction

The global tangent majorant needs s<=1. At s>1 it fails near t=0, and spending several reads on the same direction can outperform orthogonal designs in the fixed benchmark. Thus the exact fixed formula should not be extended to all noise levels without a new allocation analysis.

For example, m=1, s=2 and two repeated observations of one eigenvector give explained variance 1/8, while two orthogonal eigenvector observations give 1/9. This directly falsifies extending the orthogonal-design optimum beyond its proved range.

## Executable checks

`check_noisy_uv.py` writes `check_noisy_uv_results.json`. It passed 27 conditional-risk tensor Gauss--Hermite checks, 21 exact-rational tangent evaluations, 360 arbitrary/repeated fixed-design bound checks and 90 optimal fixed-design attainment checks. The conditional residual is a polynomial of degree two in its Gaussian posterior coordinates and final noisy read, so the tensor three-point rule integrates its square exactly in exact arithmetic. Maximum absolute conditional-risk discrepancy was 1.23e-15. The script also verifies the s=2 counterexample and reports the m=128 numerical comparison. These are finite implementation checks supplementing the algebra above.
