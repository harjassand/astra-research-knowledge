# Temporal exposure information for intervention reuse

29 October 2026, Brisbane. Complementary construction and challenge for P1.
This is an ordinary mathematical development at an explicit intervention
interface, not a native physical-system claim. It does not replace the parent's
central research choice.

## 1. What was retrieved and what was not

Current Astra input 5788b3479627421d3a67e1e6fced19f66323e94e01ccdaf4bf094a14547aa8b9,
revision ad7ff1b9d15a774d4b4d8362314c7070cac030e5, was searched with several
targeted formulations of the user's Ultra event-time/paired-path finding.
The exact source was not recovered. An `ultra-receiver/independent_opening`
paired-record hit concerned image covariance and was not reused. No claim is
made to have reviewed or reconstructed the original Ultra result.

The directly relevant retrieved foundation is N991, current capsule
`N991-p3-intervention-response-kernel-acquisition`, plus the governing
`interception_kernel_proof.md` ranges 1–77 and 79–137. The artifact hash is
e0041c04e10d380501deb302bf9b7be3ebfc69ea8cf0ea94979a495a6401660a.
Those passages already give a constant-dose Laplace response record for
independent first-capture controls, a data-acquired weak-dose modulus, and a
finite-net acquisition theorem without finite mean susceptibility. They
explicitly do not supply arbitrary schedules or altered native generators.
The present extension retains that intervention contract and requires stronger
time-resolved exposure information. The scalar Laplace identity is credited.

## 2. Exact stronger counterexample: even total exposure loses order

Let a hidden three-state process have row generator

    K = [[-1,1,0],[0,-1,1],[1,0,-1]],

or its transpose. Reset to the known uniform law pi=(1,1,1)/3. An independent
native death clock has rate one, and each death resets the experiment. Thus
the complete baseline event process is the same rate-one Poisson process in
both models. The same known added killing intensity is u(t)*d(X_t), with
d=(0,1,10). This is an abstract finite CTMC with a specified instrument.

For any fixed duration t, the stationary hidden path of K transposes to the
path of K^T when time is reversed. The total exposure

    A_t = integral_0^t d(X_s) ds

is invariant under that reversal. Consequently the entire joint distribution
of (tau,A_tau), where tau is the independent native death time, agrees between
the two models. All constant-dose survival functions agree as well:

    S_u(t)=exp(-t) pi exp((K-uD)t) 1,

because the scalar expression is unchanged by transposition. With resets,
the whole sequence of independently paired event times and total exposures
also agrees. This is equality of laws, not finite-sample resemblance.

Now apply u=1 until an external rate-one stage clock rings, then u=10 until
a second independent rate-one clock rings. Record whether the system survives
to completion of both stages. The stage clocks are independent of the source;
the protocol is a legal randomized open-loop schedule. Its probability is

    p_K = pi R_1 R_10 1,  R_u=(2I-K+uD)^(-1).

For K^T it equals pi R_10 R_1 1 and differs. Exact fractions and full killed
generator comparisons are saved by `check_temporal_exposure.py`. This implies
that some deterministic pair of stage durations also distinguishes: otherwise
their exponential mixture could not distinguish.

The two exact probabilities are 12461/233430 and 26947/466860. Their difference
is -135/31124, approximately -0.00433748875. The checker also verifies24
constant-dose resolvent controls,10 full killed-generator comparisons, and560
exact rational controls of the temporal approximation inequality below.
It acquires zero native observations and performs zero source preparations.

Hence a full paired (event time,total exposure) record is sufficient for all
constant-dose survival laws yet insufficient for arbitrary schedules. This
does not contradict a qualified claim about a different paired record. It
shows precisely what the intervention class demands from a proposed record.

## 3. Positive interface: retain a susceptibility measure

Fix a finite experimental horizon T and terminal category B in a finite set
of size k, with timeout allowed. The native source can be non-Markovian. For
each of r intervention channels let A_j be a random finite, nonnegative,
atomless measure on [0,T]. Usually A_j(dt)=b_j(t)dt, stopped at native
completion. No finite expectation of A_j([0,T]) and no pointwise ceiling on
b_j are required. Finiteness and atomlessness are mathematical premises.

The intervention has exactly the N991 no-interference/independent-first-hit
contract: until the first capture, it does not change the potential native
path, and channel j adds an independently driven capture clock with
intensity u_j(t)b_j(t). Post-hit behavior is discarded into a hit category.
Its response is therefore

    K_b[u] = E[1{B=b} exp(-sum_j integral u_j dA_j)],
    K_hit[u] = 1-sum_b K_b[u].

The time-resolved joint law of (B,A_1,...,A_r) is sufficient for every declared
nonnegative protocol, without identifying the hidden dynamics. It is extra
information: it is not obtained from a baseline event law or from the
known symbolic expression for an unobserved intensity.

The identity is standard killing/Feynman–Kac. The useful extension below is
an acquired temporal approximation modulus and uniform sample reuse over a
whole protocol class.

## 4. An acquired temporal modulus without bounded rates or finite means

Allow deterministic schedules 0<=u_j(t)<=C_j with total variation at most
V_j. On m equal dyadic bins I_i, define the left-endpoint step approximation
u_j^(m). Write a_ji=A_j(I_i). Pathwise,

    sum_j integral |u_j-u_j^(m)| dA_j
       <= sum_j V_j max_i a_ji = X_m.

Proof: within each bin the deviation is at most the variation on that bin.
Multiply by its exposure mass, sum over bins, then bound by the largest
bin mass times total variation. Atomlessness removes endpoint conventions.

For nonnegative x,y, |exp(-x)-exp(-y)|<=1-exp(-|x-y|). Coupling the same
native category and a single survival threshold therefore gives

    sup_{u in the declared BV class} TV(K[u],K[u^(m)])
       <= E Z_m,    Z_m=1-exp(-X_m).

Every finite atomless measure on a compact interval has max_i A(I_i)->0
along refining equal partitions. Thus Z_m->0 almost surely, and bounded
convergence gives E Z_m->0, even when E A([0,T])=infinity.

The bounded random variable Z_m is measured from resolved bin exposures.
Its empirical average plus a Hoeffding confidence radius is a valid upper
bound. A dyadic-resolution search with summable failure allocations and
increasing sample counts stops almost surely at any positive tolerance rho.
For example, stage q can use m=2^q, delta_q=delta_disc/2^(q+1), and n_q large
enough that sqrt(log(1/delta_q)/(2*n_q))<=rho/(q+1). Fresh independent
replicates at each stage suffice; every replicate and exposure integration
is charged. On the joint confidence event, the selected m has E Z_m<=rho.

There is no source-uniform bound on the required m, stage count, samples,
measurement bandwidth or elapsed acquisition. An atom in A can prevent this
particular modulus from tending to zero. That is a failure of this method,
not a universal impossibility of predicting an atomic source.

## 5. Uniform reuse avoids an exponential dose net under the stronger access

After choosing m, acquire n fresh independent records (B_l,a_l), where a_l
has d=rm nonnegative bin exposures. Prepare the positive empirical kernel

    Khat_b(v) = (1/n) sum_l 1{B_l=b} exp(-v dot a_l),
    Khat_hit(v)=1-sum_b Khat_b(v),   0<=v_ji<=C_j.

This evaluates every grid protocol from the same acquired records. It keeps
the joint distribution of native outcome and exposures, not their separate
marginals. It is a positive probability law at every query.

For every subset S of native categories, consider
f_(S,v)(B,a)=1{B in S}exp(-v dot a). The level sets at t>0 are the intersection
of the fixed mask B in S with a halfspace v dot a<=-log(t). For fixed S the
VC dimension is at most d+1; there are 2^k masks. Layer-cake integration
then transfers uniform indicator deviations to uniform f deviations.

One conservative explicit bound, for n>=d+1 and n*beta^2>=2, is

    P[sup_v TV(Khat(v),K(v))>beta]
      <= 4*2^k*(2*e*n/(d+1))^(d+1)*exp(-n*beta^2/8).

To see the TV identity, let delta_b be the native-coordinate probability
errors and delta_hit=-sum delta_b. Then TV=max_S |sum_(b in S)delta_b|.
For the probability inequality, a ghost sample and Chebyshev give the usual
factor-two symmetrization at n*beta^2>=2. Conditional paired Rademacher
swaps give two-sided probability <=2 exp(-n beta^2/8) for each of at most
2^k(2en/(d+1))^(d+1) label patterns. A union bound completes the proof.

Combining with the independently selected temporal grid gives, with the
allocated confidence, uniform TV error at most rho+beta for EVERY allowed
bounded-variation schedule, including schedules chosen after inspecting the
data. Native state count does not appear in this statistical bound. Temporal
resolution, number of control channels, precision and path-acquisition cost
do appear. This is an all-amplitude statement for the declared nonnegative
capture family, not a perturbative response expansion.

For approximate nonnegative exposures a_tilde, a certified per-record bound
sum_ji C_j |a_tilde_ji-a_ji|<=xi adds at most min(1,xi) to the query error.
A bound sum_j V_j max_i |a_tilde_ji-a_ji|<=zeta adds at most min(1,zeta) to
the discovery-modulus error. Neither bound follows from sample count.

Preparation stores n*(rm+one category) values plus metadata and precision.
A direct consumer uses O(nrm) arithmetic per arbitrary grid schedule and
O(n) exponentials; batching can use ordinary matrix multiplication. The
equally informed empirical Feynman–Kac estimator is this same strong route.
No computational advantage over it is claimed. An empirical finite list is
also not automatically a small time-homogeneous CTMC or a physical simulator.

## 6. Novelty boundary and further obligation

PSR action-observation closure, causal-state/transducer prediction,
change-of-measure likelihood records, conditional coarse path actions, and
VC uniform convergence are established. The candidate addition here is the
specific time-resolution modulus coupled to a retained exposure record, and
the precise distinction between constant-dose and scheduled interventions.
Historical priority is not established. The exact reversal witness is a
supplied mathematical construction, not an acquired native source.

This result earns operational relevance only where resolved susceptibility
integrals can actually be acquired with known error. The known formula for
an intensity is not such acquisition. General interventions that change the
native generator need further path-likelihood information or a controlled
predictive closure; neither is supplied by the first-capture theorem.

Primary reading scopes and current Astra receipts are in
`SOURCE_AND_COLLISION_NOTES.md` and the adjacent JSON receipts.
