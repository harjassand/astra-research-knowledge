# Learning a Pfaffian-moment boundary law without reconstructing its bulk

2026-11-04. Status: scoped mathematical construction; independent review is recorded separately in AUDIT.md. No priority or transformative-consequence claim.

## 1. Contract

Let P be a probability distribution on k ordered spins x_i in {-1,+1}. Assume all odd moments vanish and every even moment obeys
E_P product_(i in S) x_i = Pf(C_S),
where C is the antisymmetric matrix with C_ij=E_P x_i x_j for i<j, and Pf(empty)=1. Call this the Pfaffian-moment promise. No unknown parameters beyond the pair correlations are supplied. We are given independent samples of all k spins in their correct boundary order.

A physical instance is the joint law of spins in cyclic order on a single face of a finite zero-field planar Ising network with free boundary conditions. In particular this includes ferromagnetic disk networks, with arbitrary hidden volume and arbitrary finite coupling magnitudes. This application uses the established boundary Pfaffian identity, not an asserted new Ising identity. A face-order promise is necessary; arbitrary interior spins, nonplanar networks, magnetic fields, or a weakly nonintegrable perturbation need not satisfy it. The proof below only uses the stated moment promise and positivity of P.

The operation produces an IMPROPER sampler: its learned law need not itself be a physical planar network or satisfy the Pfaffian-moment identity. With confidence at least 1-alpha over training data, its output distribution has TV distance at most epsilon from P. Training, stored representation, and per-output computation are polynomial in k, 1/epsilon and log(1/alpha), independent of the hidden bulk size and its inverse-problem condition number. This is not a certificate that arbitrary data satisfy the promise.

## 2. Fourier representation

For any antisymmetric matrix A, define a possibly signed mass function
p_A(x)=2^(-k) sum_(S even) Pf(A_S) product_(i in S) x_i.
Its total mass is one, its odd moments vanish, and its even moments are Pf(A_S), by Fourier orthogonality. Under the promise, p_C=P. Marginalization to an ordered subset I gives p_(A_I), regardless of whether p_A is nonnegative.

## 3. Derivative lemma

Let M be a set of r disjoint index pairs (i,j), i<j, and let U be their 2r endpoints. Define partial_M as differentiation once with respect to every independent upper-triangular variable A_ij in M. Then, evaluated at C,
partial_M p_C(x) = sigma_M 2^(-2r) (product_(i in U) x_i) p_(C_(U complement))(y),
where sigma_M in {-1,+1} depends only on the crossing parity among the fixed pairs, and
 y_l = (-1)^(number of pairs (i,j) in M with i<l<j) x_l
for l outside U.
Consequently ||partial_M p_C||_1=1. A mixed derivative containing two pairs with a shared endpoint is zero.

Proof. Expand every Pfaffian as its signed sum over perfect matchings of S. Differentiation retains exactly the matchings containing M and deletes those selected pair weights. A Pfaffian matching sign is its crossing parity in the given linear order. Crossings between fixed pairs produce the constant sigma_M. For a remaining pair (l,h), its crossings with a fixed pair occur precisely when exactly one of l,h lies strictly between that fixed pair's endpoints. The product of these signs is therefore the product over remaining endpoints l of the displayed sign multiplying x_l. This gives the Fourier series for the indicated spin-flipped marginal, multiplied by 2^(-2r) and the endpoint monomial. Since C_(U complement) is a true marginal of P, its mass is nonnegative and sums to one. Summing the absolute value over the 2^(2r) endpoint assignments gives norm one. Overlapping selected pairs cannot occur in a perfect matching, proving the zero derivative assertion. QED.

## 4. Uniform perturbation bound

Let Delta be any antisymmetric matrix, not necessarily preserving physicality, and set
D=sum_(i<j) |Delta_ij|.
Then
||p_(C+Delta)-P||_1 <= exp(D)-1.

Proof. The Pfaffian Fourier polynomial is multilinear in each pair variable. Its exact Taylor expansion about C contains one term for each nonempty matching M, namely (product_(e in M) Delta_e) partial_M p_C. The derivative lemma and triangle inequality give the sum over nonempty matchings of product |Delta_e|. Enlarging to all subsets of pairs bounds this by product_(i<j)(1+|Delta_ij|)-1 <= exp(D)-1. QED.

In particular, if both endpoints are physical laws, their TV distance is at most D. For D<=1, half of exp(D)-1 is at most D; for D>=1 use TV<=1. This is a uniform polynomial stability statement without inversion of a latent graph. Convexity of the physical correlation-matrix set is NOT assumed.

## 5. Polynomial evaluation of every signed prefix mass

For an ordered prefix of length j and an assignment a in {-1,+1}^j, let A be the corresponding j by j principal submatrix of the learned pair matrix. If j is odd, append a zero row/column and a dummy spin equal to 1, giving even size ell=j+1. Otherwise ell=j. Put J_uv=1 for u<v, J_vu=-1, J_uu=0, and let D_a be diagonal with entries (-1)^u a_u (one-based indexing, including the dummy if present). Then
p_A(a)=2^(-j) Pf(J-D_a A D_a).
For j=0 the mass is one.

Proof. Every even principal Pfaffian of J equals one, by its standard first-row recurrence (the alternating sum of an odd number of ones is one). In the Pfaffian expansion of J+B, choosing an even set S of endpoints assigned to B contributes
(-1)^(sum_(i in S) i - |S|/2) Pf(B_S) Pf(J_(S complement)).
Take B=-D_a A D_a. Its principal Pfaffian is (-1)^(|S|/2 + sum_(i in S)i) (product_(i in S)a_i) Pf(A_S), cancelling the first sign. Summing S yields the Fourier expression. The appended zero row ensures subsets containing the dummy contribute zero; no extra factor of two is introduced because the desired denominator remains 2^j. QED.

Thus all signed prefix masses can be evaluated by an ordinary polynomial-time Pfaffian algorithm, even if the learned matrix lies outside the physical correlation variety.

## 6. Sampling from a signed approximation by positive-flow clipping

Let q be any signed mass of total one on k bits whose prefix sums can be evaluated, and let P be a true distribution with ||q-P||_1<=eta. At a sampled prefix a, evaluate its two signed child masses q(a,-1),q(a,+1). Replace them by their positive parts and sample proportionally. This defines a true sampler Q with
TV(Q,P)<=eta/2.

Proof. Every reached prefix has strictly positive signed mass: the root has mass one, and only a child with positive mass can be selected. Its children sum to the parent's signed mass, so their positive parts have a strictly positive sum. Thus a zero-denominator fallback is never reached in exact arithmetic. At a reached prefix a, write R_a=sum_b max(q(a,b),0). Since R_a>=q(a)>0, the sampling probability of a positive child b equals
[q(a,b)/q(a)] [q(a)/R_a].
The second factor is at most one. Multiplying down a path and telescoping the first factors shows Q(x)<=q(x) for every reachable leaf, while all unreachable leaves have Q(x)=0. Consequently 0<=Q(x)<=q_+(x) for all x, and sum Q=1. If nu=sum_x max(-q(x),0), then sum q_+=1+nu. Therefore
||Q-q||_1 = sum_(q>=0)(q-Q) + sum_(q<0)|q| = 2nu.
For the sharper comparison with P, use positive parts directly. Since Q<=q_+ and P>=0, we have (Q-P)_+ <= (q-P)_+ pointwise. Both Q-P and q-P have total mass zero, so
TV(Q,P)=sum_x (Q(x)-P(x))_+ <= sum_x (q(x)-P(x))_+ = ||q-P||_1/2.
This is stronger than the triangle-inequality estimate and does not require computing nu.
QED.

This is a general signed-prefix repair lemma, not dependent on Pfaffians. It avoids projecting the noisy pair matrix onto a physical correlation variety or evaluating the global positive-part normalization. Exact prefix evaluation is important to the domination proof; the finite-bit implementation below uses exact rational Pfaffians.

## 7. Statistical and bit complexity

Assume k>=2, 0<epsilon<=1, 0<alpha<1. Let m=binom(k,2) and choose
h=epsilon/(8 m).
Estimate every C_ij by the empirical average of x_i x_j from the SAME N independent full-boundary samples. Hoeffding and a union bound give simultaneous error at most h with probability at least 1-alpha provided
N >= (2/h^2) log(2m/alpha).
Thus N=O(k^4 epsilon^(-2) log(k/alpha)). Independence across pairs is not needed.

On that event D<=m h=epsilon/8<=1, so ||q-P||_1<=exp(D)-1<=2D<=epsilon/4. The clipped sampler therefore has TV error at most epsilon/4 before coin-implementation error. Allocate at most epsilon/4 further error to capped coin generation; the combined bound is below epsilon with slack. For k=1 the promised law is exactly uniform; k=0 is trivial.

Store the m empirical integer sums and N, requiring O(k^2 log(N+1)) bits. Training can accumulate them in O(N k^2) elementary updates. All empirical entries are rationals with denominator N and absolute value at most one. Every prefix Pfaffian has degree at most ceil(k/2), and its numerator is bounded by a factorial number of products of O(N)-size integers. Hence its reduced numerator and denominator have bit length O(k(log N+log k)); factors 2^j add O(k) bits. Standard exact rational/fraction-free Pfaffian elimination has polynomial bit complexity, including singular or zero-pivot cases by pivoting or returning zero for a zero row. No algebraic-number or global-field problem occurs.

Evaluating two prefix masses at every depth costs O(k^4) rational arithmetic operations conservatively (using cubic Pfaffian elimination separately at each step). The final conditional probability is a ratio of two nonnegative rational prefix masses with polynomial bit length. Exact rejection-based rational Bernoulli simulation has polynomial expected bit cost. For bounded worst-case bit runtime, first handle probabilities 0 and 1 deterministically; otherwise reduce the rational coin to 0<a<b and draw ceil(log2 b) unbiased bits, rejecting integers >=b. Each trial succeeds with probability greater than 1/2. Cap each of the k coins after R=ceil(log2(4k/epsilon))+1 trials. On cap exceedance choose a deterministically specified child with strictly positive signed mass, for example the first such child in the fixed bit order. This preserves the invariant that every reached prefix has positive signed mass, so subsequent denominators remain nonzero. A union bound bounds the total cap probability and hence extra TV error by epsilon/4. Thus per-output worst-case runtime and stored description are polynomial in the declared parameters.

The training confidence statement concerns the learned sampler's law: on one good training event, every later call uses the same accurate distribution. It is not a separate alpha error on each output.

## 8. Limits of the operation

- This is an iid-sample learning theorem, not a method for obtaining independent physical equilibrium samples. Mixing or experimental decorrelation costs are NOT paid by the sample bound.
- The correct boundary order and Pfaffian-moment model promise are inputs. This procedure does not test planarity, zero field, equilibrium, or approximate Wick validity.
- It learns a sampler for the observed boundary law, not the hidden bulk graph, edge couplings, free energy or partition normalization.
- TV accuracy gives additive bounded-observable and event-probability accuracy, not relative accuracy for rare evidence.
- It does not give a context-independent coarse-graining replacement. An external environment or conditioning on a rare boundary event can amplify TV error arbitrarily. The operation therefore falls short of the original universal multiscale-composition ambition.
- A proper physical reconstruction, sharp sample complexity, efficient certification of misspecification, and performance on non-generated scientific measurements remain open here.

## 9. Established comparisons and priority boundary

The planar boundary Pfaffian identity is established mathematics. Galashin and Pylyavskyy give a complete description of boundary correlation matrices via the positive orthogonal Grassmannian and solve the inverse problem for reduced networks: https://arxiv.org/abs/1807.03282 ; published Duke Mathematical Journal 169 (2020), 1877–1942, https://doi.org/10.1215/00127094-2019-0086 . Their exact reconstruction is the correct baseline, not exponential brute-force enumeration. This document does not claim a new boundary identity or exact inverse theorem.

The operation tested here is noisy, bulk-independent, improper sampling with a uniform TV guarantee, avoiding conditioning of graph recovery. Whether this precise guarantee is new has NOT been established. General planar Ising learning already exists: Johnson, Oyen, Chertkov and Netrapalli, *Learning Planar Ising Models*, JMLR 17(214), 2016, https://jmlr.csail.mit.edu/papers/v17/15-579.html . That work treats selecting a planar model on the observed variables; a latent boundary law generally has higher-order effective interactions and is a different input contract.

Modern general Ising TV-estimation methods must also be compared: Daskalakis, Kandiros and Yao, *Estimating Ising Models in Total Variation Distance*, COLT 2026, https://proceedings.mlr.press/v336/daskalakis26a.html . This result addresses observed Ising models under specified interaction/functional-inequality regimes, not automatically an arbitrary hidden-volume boundary marginal. No superiority claim follows merely from that difference.

Gaussian quantum-state tomography cannot be substituted without a proof translating measurement models and probability laws. A Pfaffian-amplitude vector and a fermionic Gaussian state's occupation probabilities are not interchangeable. Further comparison with Pfaffian/determinantal point-process learning and exact samplers remains necessary before any priority claim.

## 10. Independent detector noise, with its cost charged

Suppose an observed spin is Y_i=X_i Z_i, where the detector signs Z_i are independent of X and of one another, with known nonzero means t_i=E Z_i. Then observed even moments remain Pfaffian: C^Y_ij=t_i t_j C^X_ij and Pf((diag(t) C^X diag(t))_S)=(product_(i in S)t_i) Pf(C^X_S). Odd moments remain zero. Thus the noisy boundary law itself lies in the same promised family.

If the aim is instead to learn the underlying X law, assume |t_i|>=tau>0 and known rational detector means. Estimate each C^Y_ij to error at most tau^2 h and divide by t_i t_j. Then the recovered pair estimates have error at most h, so the preceding proof applies unchanged. The sufficient sample count becomes O(k^4 tau^(-4) epsilon^(-2) log(k/alpha)). Bit complexity also charges the encoding lengths of the known t_i and log(1/tau). Estimated deconvolved entries need not remain in [-1,1], which is permitted by the signed reconstruction. Without known nonzero detector means, recovery of the original law is not asserted. Correlated detector errors do not generally preserve this identity.

## Additional primary comparisons

The classical boundary identity originates in Groeneveld, Boel and Kasteleyn, *Correlation-function identities for general planar Ising systems*, Physica A 93 (1978), 138–154: https://www.sciencedirect.com/science/article/pii/0378437178902145 .

Edelman, Jeong and Schaub, *Sampling Pfaffian point processes and the symplectic Arnoldi method*, May 2026, give an exact sampler from specified valid Pfaffian point-process kernels: https://arxiv.org/abs/2605.01202 . Exact Pfaffian-kernel sampling is therefore not a new principle claimed here. Its kernel input, point-process convention and guaranteed physicality must be distinguished from noisy empirical spin-pair moments and an improper repaired sampler.

Nietner, *Free Fermion Distributions Are Hard to Learn*, 2023, revised 2024, proves limitations for broader free-fermion measurement distributions: https://arxiv.org/abs/2306.04731 . This reinforces the need to state the particular CLASSICAL spin-moment promise above; Wick identities for quantum amplitudes do not supply it. The present proof does not challenge that hardness result.

## Operational distinction from latent parameter recovery

Even the two-boundary-spin model illustrates why graph-parameter conditioning is the wrong required resource for this task. Its correlation is c=tanh(J), so recovering J from c has derivative 1/(1-c^2), unbounded as c approaches one. Its joint law has probabilities (1+c)/4 on each equal-spin assignment and (1-c)/4 on each unequal assignment, so two such laws have TV distance |c-c'|/2. Stable law learning can therefore remain possible where uniform absolute coupling recovery is ill-conditioned. This example is explanatory, not a new inverse-problem lower bound.

The ideal learned clipped law also has a polynomial-time probability evaluator: multiply its k explicitly computable rational transition probabilities along the queried assignment, returning zero if an encountered transition is zero. The actual bounded-runtime, capped-coin law likewise has an exact polynomial-time evaluator. For a nontrivial reduced coin a/b with ideal bit probability p=a/b, its cap probability is f=(1-b/2^ceil(log2 b))^R; its implemented probability for that bit is (1-f)p+f times the indicator that this bit is the designated positive-mass fallback. Deterministic coins remain unchanged. These quantities and their product have polynomial bit length. The resulting probability is nonnegative and exactly normalized by construction. Thus the output is a compact normalized probabilistic program, not merely a signed density formula. This does not make arbitrary posterior queries efficient, nor does it produce a physical reduced network.

The meaningful established scope is bulk-independent noisy learning of a boundary generative law under an exact structural promise. Relative to exact correlation-to-network reconstruction, the additional proved interface is a uniform sampling/evaluation guarantee from finite empirical data without requiring a physical projection or stable recovered couplings. Whether this is an already-known consequence in the relevant literature remains unresolved; no priority is inferred from the retrieved comparisons. No consequential physical deployment or practical advantage is demonstrated, and the civilisation-changing goal remains unmet.
