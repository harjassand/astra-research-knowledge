# Shared-bath local signs do not by themselves yield local stochastic faults

Status: new analytic obstruction, not independently reviewed. This challenges a proposed many-operation consequence; it does not change any accepted global logical-channel theorem. No novelty claim or lower bound against all randomized compilation is intended.

## Binding distinction from the accepted global-sign theorem

A single GLOBAL sign reverses all K terms together. Every branch then has the SAME quadratic effective dissipator, so the accepted global-sign theorem compares the two branches to one fixed target. Independent LOCAL signs generally change the off-diagonal entries of the leading Gram matrix branch by branch. Their average generator may have diagonal Gram matrix, but the average finite-time channel does not follow from that average generator. This note corrects that proposed local-sign inference; it does not contradict the accepted global-sign theorem or its reset-free epoch composition.

## 1. Exact bounded, rapidly mixing source

Take one stationary classical telegraph source eta(t) in {+1,-1}, flipping at rate lambda. It has mixing time of order 1/lambda. Couple n system qubits through

    H(t)=sqrt(gamma lambda) eta(t) sum_{i=1}^n xi_i Z_i,

where the xi_i are fresh independent fair private signs chosen once at the start of a fixed epoch of duration t>0. Set H0=0. Each local coupling has fixed diffusion strength gamma>0. Define the common integrated phase

    W=sqrt(gamma lambda) integral_0^t eta(s) ds.

Conditional on W and the signs, the system unitary is tensor_i exp(-i xi_i W Z_i). Averaging the signs, independently for each site, gives EXACTLY

    tensor_i [(1-p(W)) Id_i + p(W) Ad_Zi],  p(W)=sin^2 W.

Averaging W therefore yields a Pauli channel, but its Pauli fault probabilities are correlated by the common latent W. For any specified k sites S, the probability that every site in S has a Z fault, irrespective of faults elsewhere, is

    Prob(S subset fault set)=E[sin^(2k) W].

This is an operationally identifiable Pauli-channel coefficient, for example by a system-reference Bell experiment. It is not an arbitrary choice of unraveling.

## 2. Exact finite-rate polynomial lower bound

Assume sqrt(gamma lambda)*t>pi/2. The event of exactly one telegraph flip has probability lambda*t*exp(-lambda*t). Conditional on initial sign plus, the unnormalized flip-time density is lambda*exp(-lambda*t) du on (0,t), and W=sqrt(gamma lambda)(2u-t). Initial sign minus gives the same uniform phase density after reflection. Thus the unconditional law of W contains the positive density

    f_one(w)=lambda exp(-lambda*t)/(2 sqrt(gamma lambda))

throughout (-sqrt(gamma lambda)t, sqrt(gamma lambda)t).

For every sufficiently large integer k, the interval

    I_k=[pi/2-1/(2sqrt(k)), pi/2+1/(2sqrt(k))]

lies inside that support. On this interval cos(v)>=1-v^2/2>=1-1/(8k), so Bernoulli's inequality gives

    sin^(2k)(pi/2+v)>= (1-1/(8k))^(2k)>=3/4.

Consequently

    E[sin^(2k)W] >= [3 lambda exp(-lambda*t)/(8 sqrt(gamma lambda))]/sqrt(k).

The positive coefficient may be extremely small at rapid rate. It is nevertheless independent of device size k. For ANY proposed local-stochastic parameter p_eff<1 depending on gamma,lambda,t but not n, this lower bound exceeds p_eff^k for sufficiently large k. Hence no uniform-in-device-size local-stochastic fault bound follows from rapid mixing and independent private signs alone.

This is an exact finite-rate proof; it does not exchange a diffusion limit with n tending to infinity. At rates where sqrt(gamma lambda)t equals pi/2 modulo pi, the no-flip atom gives the still stronger lower bound exp(-lambda*t) for every k.

## 3. Diffusion limit and why the tempting generator argument fails

The ordinary telegraph diffusion limit has a common Gaussian integrated phase W with variance proportional to gamma*t. For any fixed positive variance, its density near pi/2 is positive and the same interval argument gives c(t)/sqrt(k). Thus the obstruction is not exclusively an exponentially rare microscopic no-flip artifact.

For each fixed sign vector, the limiting generator is proportional to D[sum_i xi_i Z_i]. The sign average of that GENERATOR has only diagonal terms, sum_i D[Z_i]. But the implemented finite epoch averages exp(t L_xi), which is generally not exp(t E L_xi). The latter replacement is exactly the unjustified operation. Sign cancellation of a leading Gram matrix alone does not establish independent local errors over a finite epoch.

## 4. A finite number of independent-sign epochs is not a universal repair

For a Brownian shared field with independent increment phases W_1,...,W_N, choose independent local signs in each epoch. Conditional on those phases, each qubit's total Pauli-Z fault probability is

    p_N=(1-product_j cos(2 W_j))/2.

Sites are independent conditional on the common vector, so the k-site inclusion probability is E[p_N^k]. Near W_1=pi/2 and W_2=...=W_N=0, one has p_N>=1-O(sum_j deviations_j^2). The joint Gaussian density is positive there. Restricting each deviation to a sufficiently small constant/sqrt(k) yields E[p_N^k]>=c_N k^(-N/2) for fixed N. Thus any fixed finite sign-refresh budget retains a common-tail obstruction to an all-subset exponential local-fault bound. This paragraph concerns the exact Gaussian limiting model; Section2 already supplies the independent finite-rate obstruction for one epoch.

## 5. What this does and does not rule out

It rules out deriving a device-size-independent local-stochastic bound merely from: bounded local interactions, rapid source mixing, independent private local signs, and a finite epoch/refresh schedule. No source-output leakage or sign leakage is needed; signs may be perfectly private and perfectly implemented. The source is simpler than an interacting reservoir, so generality cannot remove the counterexample.

It does NOT rule out local reservoirs with spatially decaying correlations, bounded-degree shared neighborhoods, refreshed signs whose rate scales with an explicitly priced accuracy/support requirement, direct measurement/recovery, or a weaker and task-specific correctable correlated-noise model. Nor does it give a computational hardness result or a lower bound against the strongest ordinary randomized-compiling construction with the same additional resources.

A meaningful next positive theorem must acquire a locality/tail property strong enough to control high-order joint errors, or prove that the intended recovery tolerates these shared-tail faults. A leading two-point response/Gram matrix and its diagonalization are insufficient. Global trace-distance bounds that grow with n do not answer this local-fault question.
