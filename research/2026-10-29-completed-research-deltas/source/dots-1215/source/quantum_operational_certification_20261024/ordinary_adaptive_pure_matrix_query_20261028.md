# An efficient adaptive pure-state matrix estimator with task-sensitive covariance

28 October 2026. Author theorem candidate with a completed finite implementation ledger; independent receiving is pending. This is a new proof candidate in this programme, NOT an independently received theorem. It does not establish global encoder sharing. The purpose is to replace an unimplemented GPS/Keyl measurement by a fully specified adaptive receiver construction after the already received efficient random-purification channel.

## 1. The actual pure-state measurement

Let P=|psi><psi| in complex dimension D>=2. First suppose a known unit vector |0> obeys q=|<0|psi>|^2>=3/4. Choose the irrelevant phase so

    psi=(sqrt(q),b),    ||b||^2=1-q,    d=D-1,    z=sqrt(q)b.

Take the D-dimensional Fourier basis, whose first coordinate is 1/sqrt(D) in every vector. Draw a Haar unitary U on the orthogonal d-space, conjugate the basis by 1 direct_sum U, and measure. If its observed vector is

    phi_v=(|0>+sqrt(d)|v>)/sqrt(D),

record w=sqrt(d)v. This is a known-basis projective measurement, not a collective Hayashi POVM. Averaging the basis draw and outcome, its effective outcome density relative to uniform v on the complex unit sphere is

    p(v)=|sqrt(q)+sqrt(d) v^*b|^2.

Consequently, by the first two complex-sphere moments,

    E w=z,
    E ww^*=q I+[d/(d+1)]((1-q)I+bb^*),
    E ww^T=0,
    Sigma=E[(w-z)(w-z)^*]<=2I.

The outcomes within one random basis need not be independent: only ONE outcome is drawn from each independently drawn basis on a fresh copy.

Use m>=2 copies for these records and set

    zhat=(1/m)sum_i w_i,
    Khat=[1/(m(m-1))]sum_(i!=j) w_i w_j^*.

The sum is Hermitian, E Khat=zz^*, and it can be computed from the vector sum and sum of outer products in polynomial arithmetic, without enumerating pairs.

On l>=m OTHER copies measure the binary projector |0><0|. Write K~Bin(l,q), t=K/l and h=(l+1)/(K+1). Return the Hermitian, not necessarily positive or normalized, matrix

    Phihat = [[t, zhat^*], [zhat, h Khat]].                 (1)

The same K is used in t and h; the same w bank is used in zhat and Khat. Replacing them by independent estimates loses the null-risk cancellations below.

## 2. Exact reciprocal identities and elementary finite bounds

For s=1-q and l>=2,

    E h=(1-s^(l+1))/q,      E h^2<=2/q^2<4.                (2)

The first follows by integrating E u^K=(s+qu)^l. For the second use

    1/(K+1)^2 <=2/[(K+1)(K+2)]

and the beta integral. The same argument for finite differences gives

    E(h-1/q)^2 <=4/l,
    E R^2<=9/l^2,
    R=h-1/q+(t-q)/q^2.                                  (3)

Here are explicit details, rather than an asymptotic delta-method assumption. For l independent Bernoulli variables, the product-space ANOVA/Efron-Stein bound gives

    Var h <= l q s E[(Delta h)(Bin(l-1,q))]^2
           <=6s(l+1)/[q^3(l+2)(l+3)] <= 6s/(q^3 l).

Since (E h-1/q)^2=s^(2l+2)/q^2, q>=3/4 and l>=2 give the first bound in (3). The squared inverse denominator inequality used here is

    1/[(k+1)^2(k+2)^2] <=6/[(k+1)...(k+4)].

For the second bound in (3), the variance in ANOVA orders at least two is at most

    binom(l,2) q^2 s^2 E[(Delta^2 h)(Bin(l-2,q))]^2
      <=40s^2(l+1)/[q^4(l+2)(l+3)(l+4)] <=8/l^2.

Use Delta^2 h(k)=2(l+1)/[(k+1)(k+2)(k+3)] and

    1/[(k+1)^2(k+2)^2(k+3)^2] <=20/[(k+1)...(k+6)].

The first-order coefficient of h is

    l E Delta h = -1/q^2+s^l(lq+1)/q^2.

Thus R's remaining first-order variance is s^(2l)(lq+1)^2 q s/(l q^4). Its squared mean is s^(2l+2)/q^2. Each is at most 1/(16l^2) for l>=2, q>=3/4 (the upper bounds using s<=1/4 are already decreasing from l=2). This proves the conservative 9/l^2 bound. These statements use only finite binomial moments.

## 3. Nearly unbiased mean and finite covariance

The only mean error in (1) is

    E Phihat-P = -[s^(l+1)/q] zz^*,
    ||E Phihat-P||_1 = s^(l+2)<=4^(-l-2).                 (4)

For every Hermitian O, write its blocks as [[alpha,c^*],[c,B]] and put r_O=Tr(P O^2). The claimed finite bound is

    Var Tr(O Phihat) <=24 r_O/m+80 Tr(O^2)/m^2.           (5)

Proof. Define delta_z=zhat-z and the degenerate pair statistic

    W=[1/(m(m-1))]sum_(i!=j)(w_i-z)(w_j-z)^*.

Then Khat=zz^*+z delta_z^*+delta_z z^*+W. Conditional on K, the linear delta_z term and Tr(BW) are uncorrelated. Also

    Var[2 Re(v^*delta_z)]<=8||v||^2/m,
    Var Tr(BW)<=8 Tr(B^2)/[m(m-1)].                       (6)

The latter follows from the degenerate pair variance and
E|v_2^*Bv_1|^2=Tr(B Sigma B Sigma)<=4Tr(B^2). Complex pseudocovariances do not invalidate this upper bound.

Put b0=z^*Bz and v0=c+Bz/q. The law of total variance gives three terms:

    Var_K(alpha t+b0 h),
    E_K Var_w[2Re((c+hBz)^*delta_z)],
    E h^2 Var_w Tr(BW).

For the first, A=alpha-b0/q^2 obeys A^2<=r_O/q^2: it is the real part of <psi|O|chi> with chi=(1/sqrt(q),-b/q) and ||chi||^2=1/q^2. Apply (3) to

    alpha t+b0 h = constant+A(t-q)+b0 R.

This bounds its variance by r_O/m+Tr(B^2)/m^2, using l>=m, qs<=3/16 and q>=3/4. For the second, q||v0||^2<=r_O and ||Bz||^2<=qs Tr(B^2), so (3) and (6) give at most

    (64/3)r_O/m+12Tr(B^2)/m^2.

The third is at most 64Tr(B^2)/m^2 by (2), (6), and m>=2. Their sum is below (5). In particular, if O annihilates psi, the entire first-order term disappears. This is a finite estimator calculation, not a local Fisher-information assertion.

## 4. Acquiring the center and bounding every history

The known-center premise is supplied by a PAID coarse pure-state estimate. The received finite-Clifford pure-state tomography produces a classical |0> with q>=3/4 except probability beta using

    n0=ceil[320 Dplus log(12 Dplus/beta)],
    Dplus=2^ceil(log_2 D)<2D,

with pure-vector backward error at most 1/8. This is the existing finite-confidence construction with infidelity target 1/4. If the tomography is performed in a padded space, project its CLASSICAL estimated vector into the known original D-dimensional space and normalize; its overlap with the true vector cannot decrease. On a zero projection use a fixed vector. This operation does not require access to an unknown source support.

Apply coarse tomography to a first subset of a homogeneous pure bank. The m random-basis and l binary measurements use disjoint remaining copies. Conditional on the actual pure state and coarse record, those remaining copies retain that SAME pure state. No analogous conditional independence across separately drawn purifications is asserted.

The estimator is defined on ALL records: h<=l+1, ||zhat||<=sqrt(d), ||Khat||_1<=3d, hence ||Phihat||_1<=10lD=:M. No supplied success certificate is used. For 0<zeta<=m^-2 choose

    l=max(m,ceil(log_4(4/zeta))),
    beta=zeta/[1000 l^2 D^2 m^2].                          (7)

The good-center mean error is at most zeta/64 by (4). A bad-center history contributes at most (M+1)beta in trace-norm mean and (M+1)^2 beta ||O||op^2 in mean squared error about Tr(P O). Using ||O||op^2<=Tr(O^2), the ideal coarse/fine construction consequently obeys the conservative bounds

    ||E Phihat-P||_1<=zeta/4,
    E[Tr(O(Phihat-P))^2]
      <=24Tr(P O^2)/m+83Tr(O^2)/m^2.                     (8)

The second is a mean-squared-error bound, so it also bounds variance. This handles variation of the small conditional biases without silently assuming they vanish.

All pure copies are counted:

    N=n0+m+l=O(D log(Dlm/zeta)+m+log(1/zeta)).              (9)

In particular, a center costing O(D) copies is not supplied for free. The estimator is generally indefinite and is not projected onto density matrices.

## 5. Finite random-basis sampling and receiver compilation

This section supplies an explicit polynomial finite-precision construction. It does NOT equate a discrete random seed with an exact continuous Haar record in total variation. Instead it couples the known unitaries, the observed finite outcomes, and the final numerical matrices.

Fix a fine-bank implementation tolerance theta>0. The target is a coupling with the ideal fine-bank experiment under which the returned matrices differ in trace norm by at most theta, except probability theta. Each implemented record has a deterministic trace-norm cap 2M, including final arithmetic rounding. This suffices for mean error at most O(M theta) and second-moment error at most O(M^2 theta). Choose, conservatively,

    theta<=zeta/[10^6 l^2 D^2 m^2].                       (10)

Other channels, including the coarse measurement, random purification and the known center/binary measurement, receive a total unhalved diamond-error budget at most theta. Their record/output discrepancy is transferred separately using the same deterministic norm cap; continuous-versus-discrete seed labels are not compared as if they had small total variation.

### 5.1 A finite Gaussian-to-unitary coupling

The ideal U in Section1 is the QR unitary of a d-by-d matrix G of independent standard complex Gaussian entries, taking each Gram-Schmidt residual divided by its positive norm. This is Haar distributed by left-unitary invariance. For one basis draw choose rational upper/lower bounds

    B>=sqrt(d log(100 m d^2/theta)),
    a^2<=theta/(100 m d),
    kappa<=min(theta/(100m), theta/(100M), a/(100dB)).

The maximum column norm is at most B except probability at most theta/(100m), by bounding all entry moduli. Conditional on the previous exact Gaussian columns, the next orthogonal residual is a standard complex Gaussian in dimension at least one; therefore its probability of norm below a is at most a^2. All d residuals exceed a except probability at most d a^2. These are PAID failure probabilities, not spectral assumptions on the unknown state.

Couple rounded Gaussian entries to the ideal ones with entry error at most delta on these good events. Put L=1+4B/a and choose

    delta<=kappa a/[100 d^(3/2) L^d].                     (11)

For exact Gram-Schmidt of the two nearby input matrices, let e_j be the difference between normalized column j. The residual comparison and normalized-vector inequality give

    e_j <= (2/a)(sqrt(d)delta+2B sum_(i<j)e_i).

Induction bounds the sum of e_j by kappa/10 with (11); all rounded residuals remain at least a/2. Thus the two QR unitaries differ in operator norm by at most kappa/10. This also gives an explicit polynomial-bit stability bound: log(1/delta)=O(d log(B/a)+log(d/(a kappa))). Arithmetic can be allocated an additional kappa/10 unitary error by the same residual bounds. The apparent exponential L^d costs only polynomially many bits, not exponentially many source calls or gates.

Rounded Gaussians need not be sampled from an exponentially long table. For each real Gaussian coordinate, couple a b-bit uniform quantile to an ideal uniform variable. On the bounded Gaussian interval, the inverse-CDF Lipschitz constant is at most exp(O(B^2)); taking b=O(B^2+log(1/delta)) gives coordinate error delta. Inverse CDF is computed by interval bisection with certified Gaussian-integral series/tail evaluation; both bit count and arithmetic are polynomial in the requested precision and B. Quantiles in the tail or failed rounded-QR guards use a deterministic fallback unitary. There is no unbounded rejection loop.

The known D-dimensional Fourier basis and known center change of basis are synthesized to the remaining kappa budget. Standard elimination into two-level unitaries uses polynomially many known gates and polynomial-bit rotation arithmetic in D and log(1/kappa); embedding the known D-space in qubits is allowed. Nothing requires an efficient arbitrary unknown unitary or a source inverse.

### 5.2 From basis coupling to estimator coupling

On the good Gaussian event, known basis unitaries differ by O(kappa). Their classical outcome distributions can be coupled with mismatch probability O(kappa), by the elementary unitary-channel trace-distance bound. For matched outcomes the recorded vector w differs by O(sqrt(d)kappa). Consequently zhat differs by that amount, Khat differs in trace norm by O(d kappa), and the block estimator differs by O(lD kappa). The choices above, with constants enlarged if necessary, give the stated theta coupling across all m draws. Known-vector arithmetic and final coordinate rotation are assigned the same explicit norm budget. A final clipping to the deterministic 2M ball may be used only as an all-history numerical safeguard; on the certified good implementation event no clipping occurs.

Taking (10) and transferring (8) gives the safe finite IMPLEMENTED bounds

    ||E Phihat-P||_1<=zeta,
    E[Tr(O(Phihat-P))^2]
      <=100[Tr(P O^2)/m+Tr(O^2)/m^2].                    (12)

The finite procedures use polynomial gates, storage, random bits and classical operations in N,D,log(1/zeta); their large constants are not a practical-hardware claim. An explicit implementation/coupling proof, not a claim that the original GPS/Hayashi POVM is efficiently implementable, underlies this statement. Independent receiving must verify this ledger before it is treated as a programme import.

## 6. Mixed-state and ordinary loss-state consequence

For a d0-dimensional state rho of rank<=r, use the received random-purification channel ONCE on N actual copies. Its ideal output is a mixture of N identical pure copies in the known product space C^(d0) tensor C^r, each reducing EXACTLY to rho. Use D=d0*r in Sections1–5; padding is needed only for the coarse Clifford computation, whose classical estimate is projected back as above. All fine measurements and final partial trace use the original product dimension. For d0*r=1 the state is known and no query is needed.

Apply the pure estimator and trace out the known r-dimensional factor. With Otilde=O tensor I_r,

    Tr(P Otilde^2)=Tr(rho O^2),
    Tr(Otilde^2)=r Tr(O^2).

The target mean Tr(P Otilde)=Tr(rho O) is the SAME for every random purification. Thus averaging the pure-state MSE bound adds no latent-purification variance. Trace-norm contraction for Hermitian operators handles the bias. With the actual N-copy purification error paid in (10), the implemented Hermitian output obeys

    ||E rhohat-rho||_1<=zeta,
    E[Tr(O(rhohat-rho))^2]
       <=100[Tr(rho O^2)/m+r Tr(O^2)/m^2],                (13)

The same inequalities also bound variance. The deterministic cap is (9), with D=d0*r. The rank-at-most case is the received continuous extension of the same purification channel, not a supplied source environment. Coarse/fine independence is invoked only conditional on the ONE common purification and earlier receiver records.

For an ordinary loss density T_x, every input copy is supplied by the ordinary six-state source experiment and receiver-local anti-state preparation. Use the same paid retained output frame throughout, with d0=2k and rank(T_x)<=min(2k,3R). For a fixed decoder Choi C, ||C||<=2 and Tr C=k, so O=3C^T/2 gives

    |E ellhat-ell|<=3zeta,
    Var ellhat<=100[3ell/m+(9rk/2)/m^2].                (14)

The factor3 in the mean is the operator norm bound; the output estimate need not be a physical loss density. All n0+m+l source calls, stored outputs, local ancillas, adaptive receiver bases, failed records, finite controls and common-frame compiler cost count. The source inputs at this chosen x remain ordinary and unentangled.

This is a SCOPED LOCAL MATRIX-QUERY theorem candidate. It does not supply an all-decoder confidence event from second moments alone, does not acquire the true-denominator SLD norm for free, does not bound how many x settings a global learner needs, and does not prove rank-weighted cross-encoder amortization. PSD projection would change the mean/covariance and is not included. The fixed-design task lower bound and coarse-model coverage traps are unaffected. The strongest equally informed conventional learner can use this same ordinary-input, collective-receiver procedure.

## 7. Source comparison and evidence status

Adaptive measurements near a known pure-state center are established. Li, Ferrie, Gross, Kalev and Caves, [Fisher-symmetric informationally complete measurements for pure states](https://arxiv.org/abs/1507.06904), study local Fisher-symmetric measurements; Vargas, Pereira and Delgado, [Near-optimal pure state estimation with adaptive Fisher-symmetric measurements](https://arxiv.org/html/2412.04555v1), give a three-stage adaptive scheme. We do not claim invention of adaptive pure-state tomography or infer our finite constants from an asymptotic Fisher theorem. The particular coupled block estimator and finite covariance are derived in Sections1–3.

The efficient random-purification import is [Pelecanos–Spilecki–Tang–Wright, Theorem1.1 and Section3.3](https://arxiv.org/html/2511.15806v1). Its separate discussion leaves efficient Hayashi implementation open; the GPS-based unbiased estimator and July2026 directional estimator are not silently reclassified as efficient. The present construction instead measures known random bases one pure copy at a time after that paid collective purification step. A general priority/novelty comparison is not claimed.

The companion script evaluates 77 finite binomial cases and 600 exact-moment covariance cases, including null-observable fixtures, plus random-basis diagnostics. These support but do not replace the analytic proof; they are not hardware execution or full QR-circuit certification. Source, arithmetic and all-history implementation review remains an independent receiving task. No generic global encoder-acquisition claim is made.
