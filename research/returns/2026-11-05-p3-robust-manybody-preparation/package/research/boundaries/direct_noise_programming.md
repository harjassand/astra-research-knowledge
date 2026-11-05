# Directly program noisy preparation without estimating its noise to output accuracy

Research note, 2026-11-05. This is a subsidiary construction for the broad preparation result. Bernoulli factories and rational probability factories are established mathematics; the contribution here is a fully explicit finite-deadline interface and resource deduction for a specified physical preparation task. It does not claim universal acquisition of unknown SPAM or a total physical advantage.

## 1. Operational contract and the distinction that matters

A local factory has finitely many actual settings. Their complete output states include its final selector, reset, switching and noise. Fixed but unknown parameters determine those states. A finite family of actual assay templates yields independent binary outcomes with probabilities p_1,...,p_d. Each invocation uses fresh probes and fresh noise. The output state coefficients must be known rational functions of these observable probabilities on a declared compact parameter domain. A requested setting is delivered by the same complete actual routine used in the model and acquisition.

We require a strictly positive rational distribution w(p) over settings which realizes the desired local state. Its numerator, denominator and positivity conditions must hold on a slightly larger parameter box than the actual one. This is an observable finite-template contract, not an ideal coin oracle: every p-coin is one paid invocation of an actual assay template, including its initialization, control, readout and capture. A full classical implementation must protect the selection, arithmetic and captured outcomes to the allocated failure probability; the main construction supplies that separately. Any remaining final selector error belongs inside the actual factory map.

Preparing an accurate mixed state requires sampling w(p); it does not require reporting p to the same accuracy. Reusing one random parameter estimate for all sites can produce correlations and is not the operation proved here. Every coin below uses fresh assay trials. The fine assay and ensemble records are discarded or reset when claiming the reduced target state. If they are retained, their actual joint classical-quantum extension must be stated; the reduced-state claim is not a conditional target-state claim.

## 2. Explicit exponentially accurate affine coin

Let an actual binary assay have success probability p. Let f(p)=alpha p+b be affine and suppose f(p) belongs to [delta,1-delta] throughout the declared actual parameter interval, with delta>0. Draw n independent assay outcomes, let K be their sum, and return a known-probability coin with success probability clip_[0,1](alpha K/n+b).

If alpha=0 this is a known coin. Otherwise, put

M=max(0,-min(b,alpha+b),max(b,alpha+b)-1).

The resulting success probability f_n(p) obeys

|f_n(p)-f(p)| <= 2 M exp(-2 n delta^2/alpha^2).                 (1)

Proof: E[alpha K/n+b]=f(p) exactly. Clipping changes the value only when |K/n-p|>=delta/|alpha|. The absolute clipping discrepancy is at most M; Hoeffding's inequality proves (1). If M=0 the coin is exact for every n. This argument remains valid if the actual p interval includes 0 or 1. The mathematical outer interval used to define f may extend beyond physically possible p values.

The random estimate K/n has root-n fluctuations, but the marginal coin bias is exponentially small: unbiased affine expectation, followed by clipping only on an exponentially rare event, is the mechanism. This is not an assertion that the noise parameter was estimated exponentially accurately.

For rational alpha,b the last known-probability coin is rational. A fair-bit comparison against its binary expansion has geometric stopping tail; truncation is included in the classical error budget. Exact rational arithmetic costs polynomial in log n and the fixed coefficient bit lengths. No ideal real arithmetic is needed.

## 3. Positive rational probability sampler with a finite deadline

Let p=(p_1,...,p_d) lie in an inner rectangle. Affinely map a larger outer rectangle to z in [0,1]^d. The actual z coordinates belong to [delta,1-delta], where delta>0. Suppose J desired probabilities w_j(z) are rational, sum to one, and are strictly positive everywhere on the outer cube, with no poles there.

Choose a common denominator D_0. It has constant sign on the cube because it is continuous and nonzero. Multiplication by D_0 if necessary yields polynomials

w_j=P_j/Q,       P_j>0,       Q=sum_j P_j>0.

For example if w_j=N_j/D_0, take P_j=N_j D_0 and Q=D_0^2. All of these are known polynomial expressions in the observable assay coordinates; their values are not acquired numerically on each invocation.

### 3.1 Constructive positive Bernstein coefficients

Write P(z)=sum_alpha a_alpha z^alpha. Its degree-D tensor Bernstein coefficient at k=(k_1,...,k_d) is

c_k = sum_alpha a_alpha product_l ((k_l)_(alpha_l)/(D)_(alpha_l)),

where (u)_a is a falling factorial, with the ratio zero for k_l<alpha_l, and D at least every coordinate degree. This identity follows by writing each monomial in the Bernstein basis.

For sampling with and without replacement from D labels, the collision coupling gives

| (k)_a/(D)_a - (k/D)^a | <= a(a-1)/(2D).

Every factor lies in [0,1], so

|c_k-P(k/D)| <= C_P/D,

C_P = (1/2) sum_alpha |a_alpha| sum_l alpha_l(alpha_l-1).

If P>=m>0 on the cube, any D>=max(coordinate degrees,2 C_P/m) has c_k>=m/2>0. One may instead enumerate degree elevations until all coefficients are positive; strict positivity guarantees termination. The degree, coefficient count, offline search and coefficient bit lengths are fixed apparatus/template costs. They can be prohibitive and are not suppressed as practical resources.

Choose one common D for all P_j and C>=max_(j,k)c_(j,k). Let Q_min>0 be a certified lower bound on Q over the cube. One ideal attempt is:

1. Draw j uniformly in {1,...,J}.
2. For each coordinate l, draw D independent z_l coins and count K_l.
3. Accept j with known probability c_(j,K)/C; otherwise restart.

The probability of accepting j on an attempt is P_j(z)/(JC). Thus the accepted label has exactly law w_j(z), and the attempt acceptance probability is Q(z)/(JC)>=a_0:=Q_min/(JC)>0. This is an explicit positive Bernstein race, a special case of established rational Bernoulli-factory methods.

### 3.2 Finite implementation and error

Implement each z_l coin by the clipped-affine construction using n fresh actual assay trials. Suppose each such coin differs from its ideal value by at most eta. Cap the race after B attempts and output an arbitrary fixed label if no attempt accepts. A coupling gives

TV(actual label,w(p)) <= (1-a_0)^B + B d D eta + epsilon_arithmetic.  (2)

This does not condition an external experiment on success. Every invocation returns an output by its deadline; timeout contributes to the declared approximation error.

For R output factors and total desired label error epsilon, choose B=O(log(R/epsilon)) and n=O(log(R/epsilon)) using (1)-(2). Constants depend on d,D,a_0,delta,the affine slopes and coefficient sizes. The total number of actual assay-template invocations is

O(R d D log^2(R/epsilon)).                                      (3)

Known-probability and arithmetic precision are paid separately and need only O(log(R/epsilon)) bits, in addition to fixed coefficient bit lengths. Site-dependent apparatus is allowed if these constants have declared uniform bounds. A family with increasing templates or increasing degree requires charging that growth. In particular a depth-h classical regenerator whose microscopic polynomial degree grows with h cannot be treated as a fixed-degree source.

## 4. Complete scalar complementary-source example

This explicit example shows the preparation consequence without a generic tomography premise. It is a specified homogeneous apparatus model, not arbitrary independent unknown reset and meter noise.

The two actual physical output routines produce

sigma_s=(I+s kappa Z)/2,       s in {+1,-1},

where fixed unknown kappa>r>0 includes every error in each complete final preparation routine. A fresh additional local operation has Pauli-Z contraction kappa. This matching is the declared homogeneous-source condition. A stationary actual binary measurement/capture has expectation c+A z on an input with Z coordinate z, with unknown A>0 and offset c. Its range is physical, so |c +/- A|<=1. The model includes actual noisy preparations and readout; no ideal reference state or ideal output port is supplied.

One explicit primitive realization includes a noisy final selector. Let a raw selector flip its requested bit independently with probability p_c, and let the quantum Pauli noise at a reset or added local gate have Z contraction lambda_q. Define the complete actual reset routine on requested bit b by

R_b = (1-p_c) Lambda_q(|b><b|) + p_c Lambda_q(|1-b><1-b|).

This actual replacement map outputs sigma_s with kappa=(1-2p_c)lambda_q and s=(-1)^b. For the added probe operation use a nominal-zero raw-selector-controlled X followed by the same quantum Pauli noise:

T(rho)=(1-p_c)Lambda_q(rho)+p_c Lambda_q(X rho X).

Its Z contraction is again kappa. These equations specify the actual noisy primitive maps, not additional ideal output routines. The logical controller's chosen requested bit is protected up to its separately paid error budget, while the final raw-selector noise is explicitly retained in R_b and T. Symmetric raw-selector noise, the shared quantum contraction, stationarity and independent refresh are genuine restrictions of this example. Arbitrary asymmetric selector noise does not satisfy these equations automatically.

Generate an independent fair software sign s with protected classical control. Prepare sigma_s, measure Y in {+1,-1}, and return the contrast bit (1+sY)/2. Its probability is (1+m_1)/2, m_1=A kappa. Running the same template with one added local operation before measurement gives another actual contrast coin with mean m_2=A kappa^2. The offset c cancels because s is fair. Both assays consume fresh qubits and records. The actual requested-sign output maps are the sigma_s above, so any selector asymmetry which invalidates that relation is outside this scalar example; it must be included and acquired for a general application.

The desired state tau_r=(I+r Z)/2 is delivered by selecting the actual + routine with probability

w_+ = (1+r/kappa)/2 = (m_2+r m_1)/(2m_2),

and the - routine with the complementary probability. This gives sigma_+ w_++sigma_- w_- = tau_r exactly. Unknown meter visibility A cancels. Neither kappa nor A is estimated to output accuracy.

Take a declared actual bound m_1,m_2 in [0.8,1], target r=1/2, and an outer mean rectangle [a,b]^2 with a=0.7,b=1.1. These bounds hold, for example, for kappa,A in [0.95,1]. Define

z_i=(m_i-a)/(b-a) = 5 p_i-4.25,

where p_i=(1+m_i)/2. Actual z_i belongs to [1/4,3/4]. Although b exceeds one, it is only a mathematical positivity extension, not a physical coin probability.

The two numerator polynomials P_+=m_2+r m_1 and P_-=m_2-r m_1 are affine in z_1,z_2, and their four Bernstein corner coefficients are strictly positive because a>r b. Set C=b(1+r). One attempt chooses sign uniformly, flips one z_1 coin and one z_2 coin, and accepts the sign with probability (m_2(corner)+/-r m_1(corner))/C. Total acceptance is m_2/C>=a/C, and accepted sign law is exactly w_+.

Each transformed z coin is implemented by the clipped-affine construction. Here alpha=5,b_affine=-4.25,delta=1/4,M=4.25, so

eta_n <= 8.5 exp(-n/200).

A B-attempt deadline gives

TV(actual sign,w) <= (1-a/C)^B + 2B eta_n + epsilon_arithmetic.    (4)

For R sites or independent factors, taking (4)<=epsilon/R uses O(R log^2(R/epsilon)) actual local assays; final outputs use one additional fresh noisy preparation per factor. Sum of factor trace-distance errors is at most sum of label TV errors by channel contraction and telescoping of product states. The same holds for a correlated external ensemble of desired factor labels provided every local factory call uses fresh independent assays and noise, conditional on the fixed apparatus parameters.

All assays and sign computation can precede the final output resets. With R local factory sites, use common fixed n and B, store the resulting labels in the paid protected classical controller, and trigger one final actual reset at every site after the deadline. This produces a simultaneous output layer and avoids assuming that previously prepared quantum outputs wait noiselessly during acquisition. Probe qubits may be reset and reused at their future output sites. Every probe reset, measurement, extra gate, classical storage interval, final reset, record erasure and timing operation is charged. A serial or geographically routed deployment instead needs its actual additional holding and transport channel inside the output map.

This is an actual finite operation with nonzero fixed physical error. The advantage over estimating all local kappa to inverse-R accuracy is a task-specific metrology saving. Existing Bernoulli-factory methods are strong comparators and may be used by any competing preparation method. No universal quantum speedup or total resource advantage is claimed.

## 5. What is and is not acquired

The factory distribution is a rational function of observable coin parameters. Those parameters need not be stored as accurate numerical estimates. Constant-resolution commissioning is still needed to justify the declared domain, stationarity, memorylessness and physical parameter correspondence. Verifying the validity of a noise family is different from estimating its parameters within that family; this construction does not solve unrestricted model testing.

Arbitrary uncharacterized SPAM has gauge ambiguity. A simultaneous rotation of all prepared states and measurement axes leaves all internal probabilities unchanged while rotating the delivered state relative to an external target. Independent unknown preparation and detector visibilities may also be inseparable from their product. Thus a broad use of Section 3 requires an identifiable control frame and actual assay templates. Generic six-palette applications need their own proof that all actual output vectors are rational functions of observable finite-template probabilities. Positivity alone does not supply this physical oracle.

For a growing-depth regenerator, its operational reference-tree output can be treated as an additional observable parameter only if fresh actual assays reproduce it with a paid error budget. An ideal-leaf reference law cannot silently replace noisy known-zero leaves. If a contraction estimate makes the replacement error O(alpha^h), that error and the full tree cost must be charged. The present note makes no claim that such a growing-tree oracle has been completed for a generic six-palette factory.

## 6. Primary comparators

- S. Nacu and Y. Peres, Fast simulation of new coins from old, Annals of Applied Probability 15 (2005), 93-115. https://arxiv.org/pdf/math/0309222 . Analytic Bernoulli factories with exponential tails, and approximate doubling construction in Section 6.
- M. Huber, Nearly optimal Bernoulli factories for linear functions. https://arxiv.org/abs/1308.1562 . Constructive linear factory and flip complexity.
- G. Morina, K. Latuszynski, P. Nayar and A. Wendland, From the Bernoulli factory to a dice enterprise via perfect sampling of Markov chains, Annals of Applied Probability 32 (2022), 327-359. https://arxiv.org/abs/1912.09229 . Rational multivariate probability transformations are established.
- Quantum error pre-compensation, https://arxiv.org/pdf/2309.01434 . Positivity of an inverse state and optimization over physical input states are prior methods. The present finite sampling construction addresses a different implementation question after a positive, observable local mixture has been established.

