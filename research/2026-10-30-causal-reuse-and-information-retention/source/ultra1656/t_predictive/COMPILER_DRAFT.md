# Proposed complete compiler from global-KL teacher access

NEW DERIVATION, independent whole challenge pending. This is not a claimed accepted
resolution of the canonical programme. It composes the newly proved asymmetric
receiver with fresh-only robust acquisition, rather than assuming conditional P
queries or selected-child coverage. The very conservative Hölder exponent is not
an assertion of practical usefulness.

## 1. Proposed theorem and resources

P is a law on O^T with predictive linear rank<=r at every cut. The learner receives
iid FULL P trajectories; next-token probability/conditional-sample access is only
to a fixed arbitrary-rank Q, with the supplied promise D(P||Q)<=Delta. Accuracy
epsilon and failure probability delta are in(0,1/4). Rank is not a positive-HMM
realization or a singular-value lower bound. Q is not copied into the output.

Let A=ceil[1000(r+O+T+1/delta)]. Subject to the full proof below, the proposed
algorithm has polynomial sample/query/representation/inference complexity in
r,O,T,1/epsilon,1/delta and returns a teacher-free sequential model with

    TV(P,P_hat)<=epsilon+128 A^3 Delta^(1/16384).        (1)

The bound is deliberately weak. Probability values are requested at a polynomial
number of bits; their ACTUAL oracle computation costs must be multiplied in.
No paid-compute, physical or practical predictive advantage follows. A and all
exponents are explicit, independent of r,T. Confidence dependence is polynomial
in1/delta, not claimed logarithmic. The model may solve convex programs per token.

## 2. Parameter choice

Take a dyadic tau_acc between (epsilon/(1024A^2))^4 and twice that value. If Delta>0,
take dyadic tau_noise between A Delta^(1/4096) and twice that value, using rational
power comparisons; for Delta0 take tau_noise0. Put tau=max(tau_acc,tau_noise).
If tau>1/(100A), output uniform independent tokens. The claimed bound then exceeds1
by the calculation in Section6, so this branch is not a hidden learning claim.
Otherwise set the exact rational parameters and explicit sample counts in
FRESH_SPANNERS Section5. In particular Delta<=(tau/A)^4096 holds.

At each cut obtain <=r fresh teacher rows by that acquisition. Append the
uniform-future row. No parent/child is inserted into the spanner candidate set.
Independently draw D fresh projection futures from this basis mixture mu.
Store the basis probabilities on those features, normalized by mu, and the next-
token probabilities at every basis prefix. For every earlier-cut basis row and
symbol, EVALUATE its child future density on the next cut's fresh features and
cache these values as well. The uniform row's restriction is known exactly.
These arrays are finite and of polynomial total size. No child samples or
P-conditional future samples are used. Source sections3/6/7 of Liu--Moitra provide
the ordinary spanner/convex-inference machinery but not this misspecification transfer.

## 3. The compiled generator

Maintain coefficients alpha over the fresh rows plus uniform, with sum alpha1
and |alpha_i|<=C=8(r+1). Initially use (1-tau)Q+tau U. All its needed first-step
and child-feature data are cached at compilation. At each token:

1. Compute raw next-token marginals m_o from alpha and the cached next-token rows.
2. Sample p_hat(o)=max(m_o,b)/sum max(m_o,b), b=tau/O. It is a valid strictly
   positive categorical law with each entry>=a=b/2 on every possible history.
3. Restrict/renormalize the current signed state with beta_i=alpha_i q_i(o)/p_hat(o).
4. Using only the cached next-cut child values, minimize the convex empirical
   generalized KL in ASYMMETRIC_OPERATION(1) over new fresh-row coefficients:
   sum alpha1, |alpha|<=C, and z_alpha(f_j)/mu(f_j)>=tau.
5. Use the minimizer as the next coefficient state. At the empty future take the
   trivial scalar state1. No teacher callback is retained by the generator.

Uniform coefficients1/S always give a strictly feasible point. The gradient and
Hessian on this domain have polynomial bounds: z/mu>=tau, R_i/mu<=S and logs
bounded by B. A conditional-gradient method with linear-program subproblems can
stop at a certified Frank--Wolfe gap<=tau; it is not a free nonconvex/global-fit
oracle. All arrays and coefficient limits are known at inference.

## 4. What the acquired events give

FRESH_SPANNERS plus RESOURCE_QUALIFICATION pay, with total failure<delta:

* At every cut the fresh teacher rows approximate all but tau P-mass of actual
  target conditional futures by feature-feasible signed states of mass1, coefficient
  bound C, and L1 error e<=9tau. This is P-weighted, not uniform conditional closeness.
* Every state feasible for a cut's finite program has negative FULL-density
  mass<=v=a tau. It need not be pointwise positive away from the features.
* Uniform asymmetric-gradient integration error<=tau holds for ALL candidate,
  comparison and arbitrary-child coefficient states in their bounded boxes.
  Thus data-dependent projection choices and adaptive generated histories are covered.

The feature-positive proxy premise is obtained with a Markov bound under the
FIXED P prefix law, independently of the projection features. The KL analysis
also averages under that law. It does not condition on a prefix selected by the
previous basis, which was the failed fresh-only argument.

## 5. Full sequence error, not only a local module

Use delta_L=theta_floor a^L, theta_floor=tau/[4(r+1)], and define the unnormalized
potential Phi_L(p,z)=sum p log[p/max(z,delta_L)]. Initialization satisfies
Phi_T<=Delta-log(1-tau)<=Delta+2tau. At the terminal empty future it is0.

The exact transition identity in ASYMMETRIC_OPERATION(4) retains the NEGATIVE
token KL. Projection adds log Z_w plus bounded approximation/sketch terms.
Importantly log Z_w<=v+O b+v/a+theta_floor<=4tau UNIFORMLY, rather than using an
upper bound that cancels the token KL. Therefore the exact-data receiver gives

    D(P||P_hat)<=Delta+2tau+T[6tau+12 B tau].          (2)

Bad histories add at most B times their P-mass, already included here. The KL
chain rule on the actual strictly positive compiled token conditionals identifies
the sum of token KLs with D(P||P_hat). This completes the SEQUENTIAL propagation:
there is no recursively worsened teacher error, state inverse or unqualified
child coverage left in(2). With paid oracle/arithmetic/optimization precision
reserve, the conservative version is

    D(P||P_hat)<=Delta+40T(B+1)tau.                   (3)

The rounding/normalization and signed negative-mass bills are explicit terms;
they are not called a generic contraction. B may be chosen globally as

    B=log[(S_max C/a+2)/(theta_floor a^T)], S_max=r+1.

## 6. From(3) to the stated Hölder form

For A>=1000, tau<=1/(100A), the displayed expression satisfies
B<=A log(A/tau). Hence40T(B+1)tau<=160 A^3 sqrt(tau), using
tau log(A/tau)<=2A sqrt(tau). Pinsker yields

    TV(P,P_hat)<=sqrt(Delta/2)+10 A^2 tau^(1/4).

The dyadic choice of tau gives(1) with room in its constants. If the uniform
fallback branch is taken, tau_noise>1/(100A) (tau_acc cannot cause it), so
Delta^(1/16384)>(1/(200A^2))^(1/4);128A^3 times this is>=1. The fallback is thus
correct at the stated, possibly vacuous, error bound. As Delta->0 the guarantee
is nonvacuous, but the exponent makes its practical noise tolerance very poor.

Because tau>=tau_acc, the largest resource count is bounded by a fixed polynomial
in A and1/epsilon, independently of how tiny Delta is. T appears in the polynomial
and log floor, NEVER in the exponent of Delta or epsilon. This is the intended
condition-free form. Explicit finite-precision and source-operation handling are
separate below; unverified runtime of a numerical package is not part of the claim.

## 7. Actual execution versus theorem state

At this writing the GENERAL derivation is proposed and awaits independent whole
challenge. It is not validated by a successful small optimization or a data hash.
The formal polynomial budgets are enormous and are not a practical sampler claim.
An executable resource/inequality receiver and a teacher-call-gated engineering
compiler are the next discriminating work, without confusing their diagnostics
with proof of(1). Ordinary spectral/TT/conditional learners retain their actual
resources; no numerical advantage over a strong fitted model is asserted.
