# Full-qutrit reusable receiver verification from fresh unentangled holdout

27 October 2026. Local post-cutoff construction at root request. Independent receiving requested. No historical novelty claim.

## 1. What is verified

Fix a classical reusable decoder, independently of all holdout data, and a stationary memoryless qutrit-input source. The resulting accepted CP trace-nonincreasing map is M, with a qutrit accepted output. Rejection is a distinguished erasure flag. This verification theorem requires NO reversible-main/reset decomposition of the underlying source.

Let C=(id tensor M)(P_Phi3) be the NORMALIZED-convention Choi operator, where Phi3 is a unit maximally entangled vector. Put

 a=Tr C, f=<Phi3|C|Phi3>,
 D_M(rho)=M(rho)+[Tr rho-Tr M(rho)]|erase><erase|,
 G_a(rho)=a rho+(1-a)Tr(rho)|erase><erase|.

Here 0<=a<=1 is the actual average acceptance, not an assumed signal probability. All diamond distances below are complete, unhalved norms.

Choose a fresh known normalized qutrit projective 2-design state psi uniformly according to its design weights, send psi through the source and fixed decoder, and record rejection, accepted match, or accepted mismatch. On acceptance, the local output test is {P_psi,I-P_psi}. No entangled preparation or shared quantum reference is used. Let b be the unconditional mismatch probability.

The exact 2-design average gives

 s=E Tr[P_psi M(P_psi)]=(a+3f)/4,
 b=a-s=3(a-f)/4.                                      (1)

Positivity and the pure-state trace-distance bound imply

 ||C-aP_Phi3||_1<=2 sqrt[a(a-f)].

The accepted map difference has diamond norm at most3 times the normalized Choi trace norm. Its erasure-trace companion costs at most the same diamond norm. Therefore

 ||D_M-G_a||_diamond<=6||C-aP_Phi3||_1
                    <=sqrt(192ab).                  (2)

In particular, if q=b/a and a>0, then q<=nu^2/192 implies

 ||D_M-G_a||_diamond<=nu a.                           (3)

This is a full-qutrit complete statement, not a qubit-subspace fidelity witness. It certifies the actual acceptance a; it does not identify a with an unknown original source parameter p.

## 2. Explicit finite-confidence decision rule

Inputs: 0<nu<=1, desired throughput floor p0 in (0,1], and confidence beta in (0,1). Define

 L=ln(4/beta),
 m=ceil(2304 L/nu^2),
 Ncap=ceil(5m/(4p0)).

Run fresh independent holdout trials until either m accepted trials have been obtained or Ncap source calls have been used. If the cap is reached without m acceptances, return INCONCLUSIVE. Each holdout trial uses the source exactly once. If m acceptances occur, let N be their stopping time and B the number of accepted mismatches among those m. Compute

 a_L=2m/(3N),
 q_U=min{1,(2B+2L)/m}.

Return CERTIFIED only if

 a_L>=p0/2   and   q_U<=nu^2/192.                     (4)

Otherwise return INCONCLUSIVE. No claim of non-recoverability is made on inconclusive data. The decoder is not retrained on these holdout samples.

### Soundness, including arbitrary bad training

With probability at least1-beta, any issued certificate simultaneously establishes

 a>=a_L>=p0/2,
 ||D_M-G_a||_diamond<=nu a.                           (5)

This holds for EVERY fixed accepted CP map M, not merely maps satisfying a training success promise. Thus it also holds after conditioning on any earlier random classical training output and then averaging: there is no assumption that a bad-training event is directly observable.

Proof of the confidence statements. Conditional on acceptance, the marks of successive accepted trials are iid Bernoulli q=b/a. Their waiting times may be random, but the accepted marks have this exact iid law. Equivalently, imagine continuing indefinitely until m acceptances even on paths that the actual capped algorithm would abandon; every certificate uses an initial segment of this hypothetical experiment.

For B~Bin(m,q), with mu=mq, the exponential-moment bound at parameter -1 gives

 Pr[B<mu/2-L] <= exp[-(1/2-e^-1)mu-L] <=e^-L.

Consequently q<=q_U except on probability at most e^-L.

For the negative-binomial stopping time N, the event a_L>a means N<2m/(3a). At any such deterministic endpoint n, the expected number of acceptances is at most2m/3. Applying the binomial upper-tail exponential bound at parameter ln(3/2) gives

 Pr[a_L>a] <=exp[-m(ln(3/2)-1/3)] <=exp(-m/15).

The last inequality follows from ln(3/2)>2/5. If a=0, no certificate is possible. Since m>=15L, the union failure probability is at most2e^-L=beta/2<beta. Capping and issuing certificates only on a subset of these events cannot increase this false-certificate bound. Combining with (1)--(3) proves (5).

### Completeness for small-mismatch devices

If the actual fixed device satisfies

 a>=p0,  q=b/a<=nu^2/1536,                            (6)

then it is certified with probability at least1-beta.

Indeed Ncap trials have mean acceptance at least5m/4. The multiplicative Chernoff lower tail gives

 Pr[N>Ncap]<=exp(-m/40).

Also the upper-tail moment at ln2 gives

 Pr[B>2mq+2L]<=e^-L.

On the latter good event,

 q_U<=(4mq+6L)/m<=nu^2/384+nu^2/384=nu^2/192.

Since m>=12p0, the cap obeys Ncap<=4m/(3p0), so every completed run has a_L>=p0/2. The two bad-event probabilities sum to at most2e^-L<beta, because m>=40L. This proves completeness.

Condition (6) is a sufficient small-mismatch margin, not an assertion that every decoder of diamond error nu a must pass this particular witness. This asymmetry is explicit.

## 3. Actual-throughput resource accounting

The cap Ncap is deterministic on every path and scales as

 O(log(1/beta)/(nu^2 p0)).

For a>0, the uncapped waiting time for m acceptances has expectation m/a; the capped procedure therefore has expected source cost at most m/a. Moreover

 Pr[N_uncapped>ceil(5m/(4a))]<=exp(-m/40).

Thus small-mismatch devices satisfying (6) are certified using

 O(log(1/beta)/(nu^2 a))

source calls with probability at least1-beta, and have the same expected-order cost, while all paths retain the deterministic p0 cap. These are distinct claims: the actual-a bound is not asserted as a deterministic cap on every random path.

The held-out source calls are additional to training and are fully charged. Accepted and rejected trials both count. Afterwards the same classical decoder can be deployed repeatedly without consuming holdout systems. Joint many-use approximation still accumulates the certified one-use error; the confidence event is a single shared event, not independently resampled per datum.

## 4. Boundaries

This verifies the stationary qutrit accepted/erased map actually tested. It does not certify a hidden source decomposition, adversarially time-varying future behavior, a quantum capacity, a scalable gate implementation, or equality of a with a source's nominal throughput. Candidate selection on this same holdout would require a separately charged uniform/multiple-testing argument. The reference-independent 2-design witness and the Choi-to-diamond conversion are both essential.
