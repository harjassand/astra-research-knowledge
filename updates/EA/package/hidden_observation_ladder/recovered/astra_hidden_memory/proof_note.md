# Hidden observation ladders: an exponential passive–active separation

## Status and scope

This is a research proof candidate developed in the present Astra investigation. The general proofs below are mathematical arguments, not formally verified theorems. The accompanying finite tests support falsification, not independent validation or historical priority. Historical novelty of the combined construction and separation is unresolved.

The candidate contribution is the simultaneous positive, rational stochastic realization of an arbitrarily deep observation ladder, exact time symmetry, fast microscopic mixing, an exponential full-path passive-testing lower bound, and a polynomial-time conservative-field test. Neither hidden dissipation in time-symmetric observations nor fluctuation–dissipation inference is claimed as new by itself.

All microscopic states are **even under the specified physical time reversal**. Entropy production uses ordinary stationary reversal. An auxiliary permutation used to prove observed time symmetry is NOT reclassified as physical time reversal. Odd hidden variables require a different thermodynamic formulation.

All logarithms are natural unless a base is displayed. Entropy production is in nats per unit time, with Boltzmann's constant one. The physical interpretation additionally assumes the stated Markov and local-detailed-balance model.

## 1. Main result

For every integer r >= 1, the construction below produces a finite rational row-generator Q_r on n states, 4r <= n <= 16r, and a balanced observable f in {-1,+1}. Put epsilon = 1/(16r). The stationary measure is uniform.

1. For distinct states i,j,

   7/(8n) <= q_ij <= 9/(8n).

   In particular every reverse edge exists, the maximum exit rate is below 9/8, rate ratios are at most 9/7, and total-variation mixing from any initial distribution is at least as fast as exp(-t/2). Every nonzero eigenvalue is -1 and every Jordan block has size at most three.

2. Its entropy production satisfies

   1/(144r) <= sigma(Q_r) <= 1/(112r).

3. Let Y_t=f(X_t), started in stationarity. Its entire path law is time-reversal invariant. At any k <= 2r observation times its joint law equals that of the stationary symmetric binary chain Z with flip rate 1/2. Nevertheless, for t_0 < ... < t_{2r},

   E[product_{j=0}^{2r} Y_{t_j}]
   = epsilon^(2r) exp(-(t_{2r}-t_0)) product_{j=1}^{2r}(t_j-t_{j-1}) > 0.

4. On an entire continuously observed interval [0,T], including exact jump times,

   TV(Law(Y_[0,T]), Law(Z_[0,T]))
   <= (2/3)(1+T/2) 16^(-r).

   Thus any test distinguishing these two hypotheses with equal-prior success at least 2/3 must observe for T >= 16^r-2. This bound permits arbitrary processing and arbitrary temporal resolution. It concerns a fixed upper bound on observation duration, not an unproved expected-stopping-time assertion.

5. Allow the following conservative field, specified at the level of every microscopic rate:

   q_ij^(h) = q_ij exp[(h/2)(f_j-f_i)]   (i != j),

   with diagonal entries reset to give zero row sums. Start in zero-field stationarity and apply the field at time zero. Then

   chi_r(t) := d/dh E_h[f(X_t)]|_(h=0)
   = 1-exp(-t) - (epsilon^2/2)[1-(1+t)exp(-t)].

   The equilibrium reference has susceptibility 1-exp(-t). This difference can be detected using finite fields +/-epsilon/100, O(r^6 log(1/zeta)) endpoint samples, and polynomial total experiment time, with error probability at most zeta. Mixing between trials is charged explicitly below; no exact derivative oracle is assumed.

The construction is polynomial in r and in its explicit output size. It is not a polynomial-in-log(r) output algorithm for an exponentially long dense matrix.

### Constant-dissipation variant

Multiplying both generators by r gives sigma(r Q_r) in [1/144,1/112], a fixed positive interval. The passive lower bound becomes (16^r-2)/r. Controlled trials have duration 1/r. Maximum microscopic exit rates grow only linearly in r. Therefore the separation does not depend on exponentially small dissipation or exponentially slow mixing.

## 2. A finite Walsh realization

Work on Omega=F_2^d, with uniform measure and characters chi_a(x)=(-1)^(a dot x). Characters are a real orthonormal basis. Multiplication of characters corresponds to addition of their indices over F_2.

Let f be the character with index e_0. Write ell=2r-1. Select characters c_1,...,c_ell and put d_j=f c_j, so that

   {1,f,c_1,...,c_ell,d_1,...,d_ell}

contains 4r distinct characters. Define the real operator A by

   A f = d_1,
   A c_j = d_{j+1}   (1 <= j < ell),
   A c_ell = f,

and A=0 on all other basis characters. Consequently

   A1=A*1=0,  rank(A)=2r,  ||A||_(2->2)=1,
   A^2 c_ell=d_1,  A^3=0,
   ||A||_F^2=2r,  ||A-A*||_F^2=4r.

The last identity uses tr(A^2)=0. These Frobenius norms are unchanged by conversion between the orthonormal Walsh and state bases.

In the ordinary state basis,

   A_xy = (1/n) sum_(source->target) chi_target(x) chi_source(y).

There are 2r summands. Hence |A_xy| <= 2r/n and K:=max_x sum_y |A_xy| <= 2r.

Define J_xy=1/n and

   Q=J-I+epsilon A,  epsilon=1/(16r).

A has zero row and column sums. Every off-diagonal rate lies between 7/(8n) and 9/(8n), so Q is an irreducible generator with uniform invariant measure. Its off-diagonal rate numerators and common denominator can be written as

   numerator(Q)=16r(ones-nI)+nA,
   denominator(Q)=16rn.

Each entry has O(log(r+2)) bits. Constructing all entries requires O(r n^2) elementary character operations. The dense output has O(n^2 log(r+2)) bits.

Since JA=AJ=0,

   exp(tQ)=J+exp(-t)[I-J+epsilon t A+(epsilon^2 t^2/2) A^2].   (2.1)

The asserted spectrum and Jordan bound follow.

### Explicit character indices and reflection

For r=1 use d=2, c_1=e_1, and the character involution Theta given by

   Theta e_0=e_0,  Theta e_1=e_1+e_0.

For r>=2 use

   d=max(4, 3+ceil(log_2(r-1))).

Let f=e_0, g=e_1, h=e_2, k=e_3 as character indices. Define

   Theta f=f,  Theta g=g,  Theta h=h+f,  Theta k=k+g,

and fix the remaining coordinate vectors. This is an involution. Choose r-1 distinct z_j in span{h,e_4,...,e_(d-1)}; this space has at least r-1 elements. Set

   c_j=k+z_j                 (1<=j<=r-1),
   c_r=h,
   c_(2r-j)=f+Theta c_j      (1<=j<=r-1).

Distinctness of the 4r characters follows by their k and g coefficients, then their remaining coordinates. In particular c_j in the first group has k=1,g=0; its reflected partner has k=1,g=1. The middle pair h,h+f has k=0, and is distinct from 0,f. Adding f gives disjoint mates in every group.

This dimension gives 4r<=n=2^d<=16r. The transpose linear map on the physical states induces Theta on characters. Its permutation operator R satisfies

   Rf=f,  Rc_j=d_(ell+1-j),  Rd_j=c_(ell+1-j),
   RAR=A*,  RJR=J,  RQR=Q*.

Uniform stationary reversal has generator Q*. Applying the label-preserving state permutation R does not change the law of the observed path. Therefore Y has exactly the same path law as its stationary reversal.

Again: R is an auxiliary symmetry, not the physical reversal convention used in sigma.

## 3. Hidden thermodynamic cost and mixing

For stationary row-generator Q, let F_ij=pi_i q_ij. Its ordinary entropy-production rate is

   sigma(Q)=sum_(i<j)(F_ij-F_ji) log(F_ij/F_ji).

Put a_ij=nA_ij and w_ij=1+epsilon a_ij. Off the diagonal w_ij is between 7/8 and 9/8. The mean-value theorem gives

   (8/9)(x-y)^2 <= (x-y)log(x/y) <= (8/7)(x-y)^2

for x,y in that interval. Moreover,

   sum_(i<j)(a_ij-a_ji)^2/n^2 = 2r.

Thus

   (16/9)r epsilon^2 <= sigma(Q) <= (16/7)r epsilon^2,

which becomes the stated [1/(144r),1/(112r)].

For mixing use the explicit decomposition

   Q=(1/2)(J-I)+B,
   B=(1/2)(J-I)+epsilon A.

B is itself a valid uniform-stationary generator: its off-diagonal rates are at least 3/(8n). Implement the first term by an independent Poisson clock of rate 1/2 which resets the microscopic state to an independent uniform state (including resets to the same state). Two copies can be coupled at the first reset. Hence TV distance to stationarity is at most exp(-t/2), from any starting law. This proves mixing without a spectral-nonnormality assumption.

## 4. Observation depth

Let D be multiplication by f. In the Walsh basis,

   D1=f, Df=1, Dc_j=d_j, Dd_j=c_j.

An observation moment is a scalar matrix product of D and propagators, between constant vectors. Formula (2.1) reduces its non-equilibrium terms to words in A and D, interspersed with operators diagonal in the Walsh basis.

A nonzero scalar word which contains A must leave f and return to f through

   f --A--> d_1 --D--> c_1 --A--> d_2 --D--> ...
     --D--> c_ell --A--> f.

Any repeated D can only move back and forth within one pair. It cannot skip a rung. The constant vector communicates with the ladder only via D1=f. Therefore every closed scalar word containing A uses at least 2r occurrences of A and at least 2r+1 observations. This also covers an A^2 term in a propagator: it counts as two A occurrences, not as one shortcut.

It follows that every moment involving at most 2r time points equals its value for J-I. Every subset of a set of k<=2r observations obeys the same statement; the Fourier expansion on {-1,+1}^k then gives equality of the complete k-point joint laws.

At exactly 2r+1 points, an odd moment has one possible surviving ladder path. It uses the term epsilon h_j A from every propagator and all intermediate D operators. All states on that path are nonconstant. This gives

   E product_(j=0)^(2r) Y_(t_j)
   =epsilon^(2r) exp[-sum_j h_j] product_j h_j.   (4.1)

The equilibrium binary chain has zero odd moments. This proves strict observed non-Markovianity and the exact first discrepancy.

The more general fact needed next is important: allowing any number of observation projections, all scalar perturbation coefficients with 1,...,2r-1 insertions of A are zero. Matching a fixed number of moments alone would NOT prove a full-path information bound.

## 5. Full passive-path testing lower bound

We compare Q with Q_0=J-I. Give the observer the additional independent Poisson reset times from Section 3. This can only increase distinguishability. Conditional on these times, segments start from independent uniform states and evolve under B or B_0=(1/2)(J-I).

### A single segment

On a segment of length t, take any finite list of observation times. For a label record y_0,...,y_k, its probability is a scalar product of propagators and the diagonal projections

   Pi_+= (I+D)/2,  Pi_-=(I-D)/2.

Expand the B=B_0+epsilon A propagators by the time-ordered Duhamel series, grouping terms by total number j of A insertions across the entire segment. The order-zero term is the B_0 probability. Every order 1<=j<2r term is zero for each record, by the scalar-word property in Section 4.

For clarity, one can bound the sum of absolute record probabilities at order j before exploiting any cancellation. Row probability vectors use the l1 norm. Markov propagation contracts this norm. Summing the two projection branches preserves the aggregate l1 norm, even for signed vectors. Inserting A costs at most K=max_x sum_y |A_xy|. Integrating ordered insertion times over a segment gives t^j/j!. Consequently

   TV(segment laws) <= g_r(t),
   g_r(t):=(1/2)sum_(j>=2r) (epsilon K t)^j/j!.   (5.1)

This estimate is uniform in the number and location of sampled times. Finite rational-time cylinder events generate the cadlag observed-path sigma algebra; passing to refining rational grids extends (5.1) to the full continuously observed segment. All chains here have finite jump counts on bounded intervals almost surely.

### Regeneration controls arbitrarily long records

For E exponential of rate lambda=1/2,

   E[g_r(E)]
   =(1/2)sum_(j>=2r)(epsilon K/lambda)^j
   <= (1/2)sum_(j>=2r)(1/4)^j
   =(2/3)16^(-r).   (5.2)

In an observation interval of length T, the expected number of segment starts is 1+lambda T. Couple the segment outputs separately conditional on all reset times. Product-law TV is at most the sum of segment TVs. For the final truncated segment use monotonicity of g_r and its full exponential length.

The event that a given segment starts before T depends only on preceding reset lengths, not its own next length. Therefore the expected sum of these upper bounds is exactly bounded by

   (1+lambda T) E[g_r(E)].

Removing the extra reset-time information by data processing proves

   TV(P_Q^[0,T],P_Q0^[0,T]) <= (2/3)(1+T/2)16^(-r).   (5.3)

No optional-stopping identity for path likelihoods is assumed.

For equal-prior binary testing, maximal success is (1+TV)/2. Success at least 2/3 requires TV>=1/3, giving T>=16^r-2. Any adaptive statistic or computational procedure based on the path up to that fixed horizon obeys the same bound.

With M independent stationary windows of total duration T, the same argument yields an upper bound (2/3)(M+T/2)16^(-r). Independence is not an uncharged reset oracle: acquiring windows in a single experiment requires waiting or a physically available reset mechanism.

## 6. Conservative intervention and the short response loop

Define, for i!=j,

   q_ij^(h)=q_ij exp[(h/2)(f_j-f_i)],

and set q_ii^(h)=-sum_(j!=i)q_ij^(h). The zero-field microscopic generator is Q. This is a specified intervention model, not an inference from passive observations. In dimensionless thermal units it changes state energy by -h f while holding symmetric kinetic factors fixed. It can be applied using the visible label alone; its effect on every hidden transition is nevertheless a physical assumption.

Let P_t=exp(tQ), Q* the stationary adjoint, and S=(Q+Q*)/2. Differentiating the rates gives an operator V with

   <1,Vg>_pi = -<Sf,g>_pi.

Duhamel differentiation from zero-field stationarity therefore yields

   chi(t)=-integral_0^t <Sf,P_s f>_pi ds.   (6.1)

For the construction,

   Sf=-f+(epsilon/2)(d_1+c_ell),
   P_s f=exp(-s)(f+epsilon s d_1).

These characters are orthonormal, so

   <Sf,P_s f>=exp(-s)(-1+epsilon^2 s/2),

and integration proves the exact susceptibility formula in the main theorem. At t=1 the difference from equilibrium is

   c_* epsilon^2,
   c_*=(1-2/e)/2 > 1/8.   (6.2)

The observable has C(t)=E[f(X_0)f(X_t)]=exp(-t) for every r. Thus the complete two-point correlation gives the equilibrium prediction, but the response differs by inverse-polynomial size. The field accesses a short adjoint-sensitive loop; unforced observation must traverse the entire ladder.

## 7. Finite fields, sampling, and actual elapsed time

The derivative in (6.1) is not supplied as an oracle.

For |h|<=1, k=1,2,3, and either generator hypothesis,

   ||d^k Q^(h)/dh^k||_(infinity->infinity)
   <=2e max_i exit_i(Q) <7.

Every real-h propagator is a Markov contraction in sup norm. The ordered-integral formula for the third derivative at t=1 gives

   ||d^3 exp(Q^(h))/dh^3|| <= 7+3(7^2)+7^3=497<500.

For m(h)=E_h f(X_1), write D(h)=[m(h)-m(-h)]/(2h). Taylor's theorem gives

   |D(h)-chi(1)| <= (500/6)h^2.

Choose h=epsilon/100. The difference of the two central-difference biases is at most epsilon^2/60. Using (6.2),

   D_eq(h)-D_r(h) >=(13/120)epsilon^2 >epsilon^2/10.   (7.1)

The reference's exact mean is

   m_eq(h)=tanh(h)[1-exp(-cosh(h))].

It is odd in h, so D_eq(h)=m_eq(h)/h. This expression can be evaluated to the needed inverse-polynomial precision with polynomial bit cost.

Let a=h epsilon^2/80=epsilon^3/8000. Estimate each of m(+h) and m(-h) to absolute accuracy a. The resulting slope error is at most epsilon^2/80. Each endpoint observation lies in {-1,+1}. Hoeffding gives a sufficient per-sign sample count

   N=ceil[(2/a^2)log(8/zeta)] = O(r^6 log(1/zeta)).

With independent stationary trials, the two estimates jointly fail with probability at most zeta/2. A threshold D_eq(h)-epsilon^2/20 separates the hypotheses with room to spare.

Exact resets are unnecessary. Before each trial, turn the field off and wait

   L >= 2 log(8N/zeta).

The Doeblin coupling from Section 3 makes the next trial's initial law within zeta/(8N) of uniform, regardless of the past. Coupling the sequential experiment to 2N independent stationary trials fails with probability at most zeta/4. The total error is therefore below zeta, including elementary numerical evaluation errors chosen inside the remaining slack.

The total experiment duration is

   O(N[1+log(N/zeta)])
   =O(r^6 log(1/zeta)[1+log(r/zeta)]).

All wait times can be rounded upward to integers with polynomially many bits. Only two field values, zero, and endpoint observations are required. For an explicit precision budget, allow absolute errors at most epsilon^3/10^8 in each field amplitude and in each unit-time endpoint. On the relevant field range, Duhamel bounds each mean error by 7 times the field error plus 7 times the time error. The resulting slope error is at most 14(epsilon^3/10^8)/h < epsilon^2/1000. Evaluating the equilibrium reference to slope accuracy epsilon^2/1000 also fits within the decision slack. Thus control precision requires O(log(r+2)+log(1/zeta)) bits, not exponentially accurate settings.

The sample-count constants are intentionally loose and large. This is a polynomial-versus-exponential theorem, not a practical low-sample claim. The code does not simulate this very large conservative sample budget.

If a physical implementation has energy -h f, the absolute externally switched work is at most 2|h| per on/off trial. This observation does not include sensor, actuator, or model-construction energy. No total experimental-efficiency claim is made.

## 8. The observed process has intrinsically positive ordinary hidden cost

A large entropy production in one chosen realization could be an irrelevant hidden subsystem. The following observable witness rules that out here.

At integer times from -r to r, define

   F_+=product_(j=1)^r Y_j,
   F_-=product_(j=1)^r Y_(-j).

Condition on Y_0=-1. All moments needed for the separate means and the unconditional product have order <=2r and equal equilibrium values. With

   mu=exp(-r/2)                 if r is even,
   mu=-exp(-(r+1)/2)            if r is odd,

one obtains

   E[F_+|Y_0=-1]=E[F_-|Y_0=-1]=mu,
   Cov(F_-,F_+|Y_0=-1)=-tau_r,
   tau_r=epsilon^(2r) exp(-2r)>0.   (8.1)

For any reversible hidden chain with deterministic observation, stationary past and future are independent and identically distributed conditional on its present microscopic state. Hence, for any fixed mu,

   E[1_(Y_0=-1)(F_--mu)(F_+-mu)] >=0.   (8.2)

Our observed expectation equals -tau_r/2. This already excludes every finite reversible exact realization, with no fixed hidden-state count.

To exclude even sequences of vanishing-cost exact realizations, we use a self-contained comparison.

### Additive reversibilization comparison

For any finite stationary generator G, let G*=D_pi^(-1)G^T D_pi and R=(G+G*)/2. The comparison chain R is reversible, has the same stationary law, and has exactly the same exit rates. Its stationary microscopic path law satisfies, on length L,

   KL(P_G^L || P_R^L) <= L sigma(G)/4.   (8.3)

If sigma is infinite there is nothing to prove. Otherwise the jump-path likelihood formula cancels holding-time terms and gives rate

   sum_(i!=j) F_ij log[2F_ij/(F_ij+F_ji)].

For x,y>0,

   x log(2x/(x+y))+y log(2y/(x+y))
   <=(1/4)(x-y)log(x/y).

To check this, put u=(x-y)/(x+y). Dividing the difference by (x+y)/2 gives

   -log(1-u^2)-u arctanh(u).

It vanishes at zero, is even, and its derivative for u>=0 is u/(1-u^2)-arctanh(u), itself nonnegative because its derivative is 2u^2/(1-u^2)^2. Summing proves (8.3).

This particular comparison and the conditional past/future covariance principle were already present in the recent hidden-dissipation-floor source listed below. They are reproved here; its broader unreviewed theorems are not imported.

### A strictly positive all-dimension floor

Suppose G is any finite all-even hidden exact realization of our observed path law. Apply (8.3) on [-r,r]. The test

   Z=1_(Y_0=-1)(F_--mu)(F_+-mu)

has range width at most 4. Its expectation under G is -tau_r/2 and under its reversible comparison is nonnegative. Thus observed TV is at least tau_r/8. Pinsker and data processing imply

   (r/2)sigma(G) >= KL(P_G||P_R) >= tau_r^2/32,

so

   sigma(G) >= epsilon^(4r) exp(-4r)/(16r) >0.   (8.4)

This lower bound is not sharp and is much smaller than sigma(Q_r). It is uniform over all finite hidden dimensions and rates. It proves that positive ordinary hidden cost belongs to the complete observed process, not merely to a dispensable independent hidden subsystem.

## 9. An architecture-independent response certificate

The general link between fluctuation–dissipation violations and entropy production is established prior mathematics. The following finite-state specialization explains exactly what the measured response can certify.

Let G be any finite stationary generator, f bounded, and use the same conservative perturbation rule. Center f for its covariance, and define

   C(t)=Cov_pi(f(X_0),f(X_t)),
   Delta(t)=chi(t)-[C(0)-C(t)],
   M=(max f-min f)/2.

Then

   |Delta(t)|^2 <= (M^2/2) sigma(G) t Var_pi(f).   (9.1)

Proof. Put A_a=(G-G*)/2, S=(G+G*)/2, P_t=exp(tG). Equation (6.1) and differentiation of C give

   Delta(t)=-integral_0^t <A_a f,P_s f>_pi ds.

Write J_ij=F_ij-F_ji and traffic T_ij=F_ij+F_ji. Stationarity gives divergence-free currents. Therefore

   <g,A_a f>_pi
   =(1/2)sum_(i<j) J_ij(f_i+f_j)(g_i-g_j).

The identity is unchanged on adding a constant to f. Center at the midpoint of its range. Using sigma>=2 sum J_ij^2/T_ij and Cauchy–Schwarz yields

   |<g,A_a f>| <= M sqrt[sigma E(g)],
   E(g)=(1/2)sum_(i<j)T_ij(g_i-g_j)^2.

Finally,

   integral_0^t E(P_s(f-pi f))ds
   =(Var_pi(f)-||P_t(f-pi f)||_2^2)/2
   <=Var_pi(f)/2.

A second Cauchy–Schwarz inequality proves (9.1).

For balanced binary observations, M=Var(f)=1. Hence

   sigma(G)>=2 Delta(t)^2/t.   (9.2)

For our response at t=1 this gives the polynomial lower bound 2 c_*^2 epsilon^4 for every all-even hidden model matching both correlation and conservative-field susceptibility. Finite-field statistical certification additionally needs a controlled Taylor remainder, such as the charged exit-rate bound used in Section 7. We do not promote a finite difference to a universal exact derivative oracle.

This does not estimate the actual entropy production to a fixed relative error. It certifies a strictly positive lower bound. Identifying an exact dissipation value for arbitrary hidden systems is not achieved.

## 10. Four-state illustration

For r=1 the ladder is already nontrivial. For readability, here use epsilon=1/4 rather than the smaller epsilon=1/16 used in the uniform constants of the main theorem:

                 [ -10,   4,   4,   2 ]
   Q = (1/16) *  [   2, -12,   4,   6 ]
                 [   4,   6, -14,   4 ]
                 [   4,   2,   6, -12 ],

   f=(+1,-1,+1,-1),  pi=(1/4,1/4,1/4,1/4).

The complete observed law is time symmetric and C(t)=exp(-t), yet

   E[Y_0 Y_s Y_(s+t)]=(st/16)exp(-(s+t)),

and

   chi(t)=1-exp(-t)-(1/32)[1-(1+t)exp(-t)].

This example illustrates the mechanism; the main 16^r passive bound uses epsilon=1/(16r), not this illustrative epsilon.

## 11. A structured robustness corollary

The equal numerical rung amplitudes are not essential. Replace the 2r nonzero Walsh entries of A, in ladder order, by a_0,...,a_(2r-1) in [1/2,1], with a_j=a_(2r-1-j). The same character permutation gives A*=RAR, and A^3=0 still holds. Strict positivity and the same regeneration bound hold because K<=sum_j a_j<=2r.

The first nonzero moment is multiplied by product_j a_j. All shorter scalar words still vanish exactly. The passive full-record bound remains unchanged. The Frobenius calculation now uses sum_j a_j^2 in [r/2,2r], giving

   1/(576r) <= sigma(Q) <= 1/(112r).

The susceptibility correction is multiplied by a_0^2, because Af=a_0 d_1 and the only inner-product contribution is the d_1 term. Thus its gap is at least c_*epsilon^2/4>epsilon^2/32. The same field h=epsilon/100 gives a finite-field slope gap of at least (1/32-1/60)epsilon^2>epsilon^2/100. Estimating slopes to epsilon^2/1000 and thresholding at D_eq-epsilon^2/200 yields the same O(r^6) sample exponent, with modified constants.

This is robustness inside an explicitly structured family, not an open neighborhood in the full space of all rate matrices. Arbitrary microscopic perturbations can add shorter observation paths and invalidate the passive exponential lower bound.

## 12. What failed, and what remains open

* Eigenvalues alone were rejected as a route to hidden thermodynamic certification. Recent primary work gives a counterexample to a proposed eigenvalue-only bound. Our result instead uses the observable operator algebra and positive probabilities.
* Equality of low-order moments is not enough to claim full-record indistinguishability. The regeneration/Duhamel proof in Section 5 is essential; it bounds arbitrary continuously observed records.
* An abstract signed realization would not define a physical stochastic process. The Walsh lift produces strictly positive rational rates with uniform margins.
* An orthogonal similarity to the transpose would not by itself prove equality of observed path laws. The construction supplies an actual label-preserving state permutation.
* Exact linear response is not a free measurement. Section 7 replaces it by finite fields, charged samples, mixing waits, and precision requirements.
* The field law is an intervention assumption. Passive paths alone do not determine how kinetic rates respond to an applied field.

The theorem supplies an explicit hard family and a specified efficient diagnostic, not a universal efficient inference algorithm. The most direct next mathematical objective is a characterization of observable/control algebras which admits efficient, robust thermodynamic certificates for broad model classes without reconstructing hidden states. No such general characterization is proved here.

Experimental realization of the dense rate architecture, robustness to uncontrolled microscopic model errors, optimal active sample complexity, and a sharp value of the all-dimension hidden cost remain open in this investigation. The exponential lower bound is not asserted to be tight. Exact low-order equalities are constructed identities; generic perturbations can create easier passive signatures.

## 13. Reproducibility and provenance

`test_lift.py` checks 6,376 counted exact finite assertions (r=1,...,32, with dense integer tests through r=9). `test_response.py` adds 40 exact state-space/graph assertions and eight floating response diagnostics. Floating exponentials and entropy values are not interval-certified. The proof does not rely on their floating accuracy.

`export_model.py` emits explicit rational matrices, observable labels, and the reversal permutation. No microscopic simulation, statistical Monte Carlo assay, or theorem-prover formalization is claimed.

Research capital was consulted selectively:

* Astra task-first entry `00_START_HERE.txt`, at main revision `3a9880bf4b1913a1b9e522f15414092e57c66eec`.
* OpenAI math searches at revision `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

No theorem from either repository is a premise of this construction. Their stored claims are not treated as independently validated.

### Primary prior sources and exact use

1. Dominic J. Skinner and Jörn Dunkel, *Improved bounds on entropy production in living systems*, arXiv:2011.08765; PNAS 118 (2021), e2024300118. https://arxiv.org/abs/2011.08765
   Prior hidden thermodynamic inference, including nonzero bounds for apparently time-symmetric coarse-grained observations. No novelty claimed for that phenomenon alone.
2. Leticia F. Cugliandolo, David S. Dean and Jorge Kurchan, *Fluctuation-Dissipation theorems and entropy production in relaxational systems*, arXiv:cond-mat/9705002; Physical Review Letters 79 (1997), 2168–2171. https://arxiv.org/abs/cond-mat/9705002
   Prior relation between response violations and entropy production. Section 9 is a self-contained finite-state calculation, not a claim that the general relation is new.
3. Naoto Shiraishi, *Second largest eigenvalue does not bound stationary entropy production*, arXiv:2609.34352v1, 28 September 2026. https://arxiv.org/html/2609.34352v1
   Primary counterexample used to reject an eigenvalue-only direction. None of its proof is needed for the new construction.
4. Anonymous, *An architecture-independent dissipation floor for alternating-renewal observations*, Evidence Press research candidate v1.1, 3 October 2026; source `PAPER.tex`. https://github.com/ipitchford/hidden-dissipation-floor
   Prior exact additive-reversibilization path comparison and conditional past/future tests. Those tools are reproved in Section 8. Its broader claims and internal checks are not imported as externally validated theorems.

The selective search did not establish historical priority for the combined separation theorem. Absence of a matching search result is not evidence of novelty.
