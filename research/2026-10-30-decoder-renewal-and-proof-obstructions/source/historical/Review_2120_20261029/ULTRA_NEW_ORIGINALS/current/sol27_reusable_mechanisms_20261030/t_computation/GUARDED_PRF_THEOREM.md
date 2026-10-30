# Guarded program tapes: a conditional computational obstruction at the full-law target

30 October 2026. Main theorem is CONDITIONAL on an explicitly stated strong
NC1 PRF hypothesis. The rank, source construction, oracle simulation and
learning-to-distinguishing reduction are unconditional mathematical statements.
No cryptographic hardness assumption is asserted to be proved. All earlier
ROOT25/26 inputs remain unchanged.

## 1. The exact missing acquisition question

The input is an unknown full-support law P on binary words of length T, with
GIVEN warranted d,alpha bounding the rank and factor norms of EVERY fixed-cut
FULL-FUTURE centered-logit matrix. A native query specifies ANY prefix and
returns an independent next token, or even an independent complete remaining
future. The learner also has unconditional samples, obtainable at the empty
prefix. It must compile a source-free sampler H with TV(P,H)<=1/64 with
probability>=2/3, in time polynomial in T,d,alpha (or log alpha), and ordinary
metadata lengths. The output need not expose conditional probabilities or
likelihoods; an efficiently runnable unconditional sampler is enough below.
All learners, compiled samplers and distinguishers in this theorem are
CLASSICAL randomized algorithms/circuits. A quantum learner or a quantum
compiled sampler is not excluded by the default classical PRF premise.

Under Assumption1, no such general polynomial-time learner exists. This is
about the actual FULL-LAW output, not recovery of rare logits, latent coordinates
or a counterfactual Fisher tensor. It holds with alphabet2, exact logit rank
<=n+7, polynomial alpha, and polynomial-time samplable native conditionals.
The rank is polynomial, not constant. The construction is not a claim that
ordinary Barrington width5 by itself implies constant chronological logit rank.

## 2. Explicit cryptographic premise and primary antecedents

Assumption1 (public-template Boolean NC1 PRF). There is a security parameter k,
a polynomial key length, and an input length n=n(k) with

    n(k)=poly(k),   n(k)/log k ->infinity,

and a keyed Boolean function F_K:{0,1}^n->{0,1}. A random key gives a function
computationally indistinguishable from a uniformly random Boolean function to
CLASSICAL randomized polynomial-size adaptive oracle distinguishers. Joint
evaluation C_k(K,x) has
a PUBLIC polynomial-size bounded-fan-in Boolean circuit of depth O(log k).
The circuit template, including the locations of key and input wires, is
independent of the sampled secret key.

The nonuniform-circuit version suffices: public templates may be polynomial
advice shared across the two oracle games. If the templates are uniformly
constructible, the reduction is a uniform randomized polynomial-time reduction.
Uniformity is NOT inferred merely from the words 'NC1'. Likewise, security
against nonuniform polynomial-size distinguishers and uniform PPT security
must be matched to the corresponding version of the premise.
An extension to quantum processing would require a matching PRF security
promise against quantum distinguishers making classical oracle queries, at
minimum. Classical LPN/NC1-PRF security alone supplies no such extension, even
though the reduction never needs coherent oracle queries.

This premise is standard cryptographic structure, not an invented hardware
oracle. Naor--Reingold2004 constructs low-depth PRFs under number-theoretic
assumptions. More recently Ding--Jain--Komargodski, arXiv2608.25213v1
(25Aug2026), gives strong NC1 PRFs from standard LPN, polynomial-ratio LWE and
CDH. Its Section3 circuit-model footnote8 explicitly states the result also
holds with the KEY AS PART OF THE CIRCUIT INPUT. Definitions2--3 treat adaptive
oracle distinguishers; Theorem3/Corollaries2--3 give the depth-preserving strong
PRF transformation, and Section6 Theorem5/Corollary9 state the LPN implication.
Projection onto one output bit preserves PRF security when the reference
output is a uniform bit string. A superpolynomial binary domain suffices here;
arbitrary polynomial input length is not needed. We use Assumption1 explicitly
rather than silently importing uniformity, output coding or parameter claims.

Barrington's1989 theorem constructively converts a depth-D fan-in2 circuit to
a width5 permutation branching program of length O(4^D). We consume its
strong product form: for one fixed nontrivial5-cycle pi, the full product is
the identity on a false input and pi on a true input. In particular the action
on an initial basis state distinguishes the two outputs. References:

* Barrington primary author PDF:
  https://people.cs.umass.edu/~barring/publications/bwbp.pdf
* Ding--Jain--Komargodski primary:
  https://arxiv.org/html/2608.25213v1
* Naor--Reingold, DOI10.1145/972639.972643.

The classical PRF-versus-learning connection is established prior. The new
interface being proved is its guarded, full-support, low-FULL-FUTURE-logit-rank
sequential lift, with simulation safe at every inconsistent queried history.
Historical priority of this specific lift is UNKNOWN.

## 3. Public read schedule, secret permutations, and why naive lifting fails

Apply Barrington's construction to the JOINT circuit C_k(K,x), before fixing
K. Let m=poly(k) be the resulting program length. At each instruction j a
PUBLIC tag says either 'read input x_(r_j)' or 'read key K_(r_j)'. The two
permutations of that instruction are fixed by the public compiled template.
After binding K, a key-read instruction therefore applies one SECRET but
fixed permutation. Its public position remains unchanged. Let P_(j,b) be the
permutation for an input-read instruction on bit b, and P_(j,K) the permutation
selected by a key-read instruction. Renumber states so identity sends e1 to
e1, pi sends e1 to e2, and acceptance is state2.

An input-read program tape on INDEPENDENT new input bits is an easy finite-
width sequential object; it is not automatically the original read-many PRF.
Conversely, forcing exact consistency of repeated bits can destroy full support
and expose an invalid-prefix oracle. The construction below keeps consistency
only through large but finite odds and adds a linear, additive mismatch guard.
It does not use a nonlinear Boolean AND flag or a tensor of all remembered bits.

## 4. A full-support source with rational native probabilities

Set s=k^2+20, Lambda=s log2 and beta=log15. The word consists of

    X_1,...,X_n,  C_1,...,C_m,  Y,
    T=n+m+1.

First emit independent uniform input bits X_i. At each program instruction j:

* If it reads input x_(r_j), emit a copy C_j with
  Pr(C_j=X_(r_j))=2^s/(1+2^s). Apply P_(j,C_j) to the5-state program register.
* If it reads a key bit, emit an independent uniform dummy bit C_j. The program
  register applies P_(j,K), IGNORING that dummy bit.

Let M be the number of incorrect copies at INPUT-read instructions. Dummy
bits at key-read instructions never contribute to M. Let q be the final
one-hot program state and f(q)=2 q_2-1 in{-1,+1}. Finally emit Y with

    log[Pr(Y=1)/Pr(Y=0)] = beta f(q)-Lambda M.         (1)

On M=0 the program tape is consistent with (K,X), so f(q)=2F_K(X)-1, and Y
agrees with F_K(X) with probability15/16. On M>=1,

    Pr(Y=1) <=15*2^-s.                               (2)

All next-token probabilities are strictly between0 and1, including after
EVERY inconsistent native prefix. All are exactly rational:

    copy correctness: 2^s/(1+2^s),
    final if f=+1: 15/(15+2^(sM)),
    final if f=-1: 1/(1+15*2^(sM)).                   (3)

The source description consists of the public program and the secret key,
with integer permutations and two fixed computable constants log2,log15 in
its logit realization. No arbitrary real advice or exponential input bit
string is hidden in a parameter. The exact source sampler evaluates the
finite program and samples rational categorical probabilities with O(sm)
denominator bits. It has expected polynomial fair-bit cost; finite polynomial
caps of its elementary rejection coins change its law only negligibly.

At most m instructions are input reads. Therefore

    Pr_P(M>0)<=m*2^-s,
    Pr_P(Y=F_K(X))>=15/16-m*2^-s,  X uniform.         (4)

The target signal is balanced and has constant noisy-label strength on almost
every actual source trajectory. This is not a rare-label TV loophole.

## 5. Exact affine state and all-future logit linearity

Encode a token b by sign(b)=2b-1. Use the column state

    z=(c, x_1,...,x_n, q_1,...,q_5, M),  D=n+7,

initialized with c=1, all x_i=0, q=e1, M=0. On the first n emissions, the
time-i token b updates x_i=sign(b)c and leaves other coordinates unchanged.
At an input-read program step j with fixed emitted token b:

    q <- P_(j,b) q,
    M <- M + [c-sign(b)x_(r_j)]/2.                    (5)

At a key-read step, q<-P_(j,K)q and M is unchanged. Every map is LINEAR in z
once the next token and time are fixed; the constant coordinate turns the
usual affine update into a linear one. In particular no product M*x_i, no
history-dependent matrix and no hidden consistency predicate occurs in (5).

For a native prefix h, the next BINARY mean-centered logits are +/-a_h/2,
where a_h is respectively

    0                         during initial inputs/key dummies,
    Lambda*x_(r_j)            at an input-copy step,
    beta(2q_2-c)-Lambda M      at the final Y step.     (6)

These are linear functionals of z_h. For ANY fixed continuation word f, its
token updates have a fixed product A_f, so the next centered logit after hf is

    ell_(hf)(y)=b_(f,y)^T z_h.                        (7)

Consequently the full matrix h,(f,y) at EVERY cut has exact rank<=D. This is
the logit of the NEXT TOKEN after hf, not log P(f|h) and not a logit centered
against a new future law. Equation(7) includes cuts BEFORE all X bits were
emitted: their future fixed tokens simply overwrite the remaining x slots by
known multiples of c. It includes ALL wrong-copy and dummy-token histories,
not just the overwhelmingly likely consistent sublanguage.

## 6. Polynomial factor and bit bounds, without hidden conditioning

Put H=n+m+7. Every native state has |x_i|<=1, q one-hot, c=1, 0<=M<=m, so

    ||z_h||_2 <=sqrt(n+2+m^2)<=H.                     (8)

For future functionals in(7), the5-state register is acted on only by
permutations. An input slot is either unchanged or replaced by +/-c. Over a
fixed future the mismatch coordinate is M plus an affine sum of at most m
terms from(5). Its coefficient on each old x_i has absolute value<=m/2, and
its coefficient on c has absolute value<=m. These bounds remain valid when
future input tokens fill slots not yet acquired at the current cut.

Since log2<1 and log15<3, every coordinate of b_(f,y) has absolute value at
most 3+s(m+1). With D<=H,

    ||b_(f,y)||_2 <=H[3+s(m+1)]
                   <=4(s+1)H^2.

Thus the explicit GIVEN integer

    d=D=n+7,   alpha=10(s+1)H^2                       (9)

warrants the exact GLS bounded-factor definition at every cut. Both are
polynomial in k. No small singular value, eigenbasis, exact function value,
or unknown key is supplied with this metadata. The maximum logit magnitude
is also only polynomial, but the minimum native probability is exponentially
small. This is exactly the gap that native Bernoulli samples cannot ignore
at a deliberately queried wrong-copy context.

## 7. Every native query can be simulated from the ordinary PRF oracle

Let O be an oracle for an arbitrary Boolean function on X. The simulator does
NOT know K or the secret program permutations. Given ANY specified prefix:

1. Complete any still missing original X bits uniformly, when a full future
   rather than only the next input token is requested.
2. Generate remaining copy/dummy bits by the exact visible laws in Section4.
   The public read schedule and the already stored/completed X determine all
   these laws and the visible mismatch count M; no key is needed.
3. At final Y, if M=0 query O(X) and return that label with probability15/16.
   If M>0 return Y=0, WITHOUT querying O at an inconsistent program tape.

With O=F_K, the returned next-token or entire-future distribution differs from
the actual P_K conditional by at most 15*2^-s in TV, UNIFORMLY over every
prefix. The earlier token laws are identical; only the final Bernoulli row on
M>0 is replaced. Therefore a complete future costs at most ONE Boolean PRF
query, at most T returned symbols, and polynomial bit work. No factor depending
on the native probability of the supplied prefix is needed.

For an adaptive learner making at most Q native oracle calls, stepwise
conditional coupling gives total transcript TV<=15 Q*2^-s. This remains true
if the call lengths vary or the learner intentionally queries astronomically
unlikely wrong-copy prefixes. To implement the simulator in fixed polynomial
time, truncate every elementary uniform-integer rejection sampler after k^2
trials. Each trial accepts with probability>=1/2; at most poly(k) coins are
used, so the additional transcript error is poly(k)*2^-k^2. This removes any
expected-time random-bit loophole in the cryptographic reduction. The true
mathematical source itself remains the exact rational law(3).

## 8. Sampler-only learning already breaks the PRF

Suppose the learner in Section1 exists. Run it with the simulated oracle above
and public metadata(9), epsilon=1/64. Record the set S of all Boolean inputs
queried to O during training; |S|<=Q. After compilation REMOVE all source/oracle
access from the returned program. Run its unconditional sampler once to obtain
a word, and extract its original X and final bit Y. Malformed outputs or any
attempt at another source call cause rejection. If X in S, reject. Otherwise
query O(X) once and accept exactly when Y=O(X).

In the PRF game, except for negligible simulation error, the learner succeeds
with probability>=2/3. Conditional on any successful compiled law H and its
fixed transcript, TV(H,P_K)<=1/64. The bounded acceptance statistic depends
on that fixed S and F_K, so by TV and(4),

    Pr_H[X notin S, Y=F_K(X)]
       >=15/16-m*2^-s-|S|/2^n-1/64.

No assumption that H can evaluate arbitrary-prefix conditionals is made.
Its marginal X must itself be close to uniform because its WHOLE law is close
to P_K; it cannot evade the test by outputting only memorized training queries.
Even granting acceptance0 on every unsuccessful learner run, overall PRF-game
acceptance is at least

    (2/3)*(59/64)-negligible =59/96-negligible.        (10)

In the random-function game the learner may behave arbitrarily, output an
invalid model, memorize S, or fail. For a valid source-free sample with X notin S,
the fresh value O(X) is an independent uniform bit conditional on the entire
training transcript AND the sampler's randomness. Thus random-game acceptance
is at most1/2. Rejecting repeats cannot increase it. This uses strong adaptive
PRF security, not weak/random-input security.

The resulting polynomial-size oracle distinguisher has advantage at least

    11/96-negligible,                                (11)

contradicting Assumption1. Uniformly known expected polynomial compilation/
sampling bounds can also be truncated at a sufficiently large constant multiple
of those bounds, losing arbitrarily small constant acceptance; the positive
gap in(11) survives. A claimed unspecified or nonuniformly unbounded expected
runtime would not be sufficient for a polynomial-time learner theorem.
The executed learner and sampler here are classical, so this distinguisher
has precisely the classical computational access in Assumption1.

No correctness premise in the random-function game was used, and no assertion
that its simulated law has low logit rank is needed. Only the real PRF-key
sources belong to the promised class. This is an ordinary two-game hardness
reduction with a new exact source embedding, not a generic information lower
bound and not a proof that unconditional sample counts must be large.

## 9. Operational conclusion and what would genuinely escape

Subject to Assumption1, native conditional next-token access plus exact bounded
full-future logit rank ALONE is computationally insufficient for a general
polynomial-time teacher-free full-law compiler. Even native full-future samples
and arbitrary prefix preparation do not repair it. The ROOT26 exponential-
search learner remains compatible: it pays the missing computation.

The controlling feature is a finite additive counterfield that hides internal
program values at inconsistent contexts. A logit VALUE supplier would reveal
the final +/-beta program value after subtracting the known -Lambda M guard.
An independently available, calibrated next-outcome ODDS BIAS of +Lambda M
would also remove that guard with polynomial amplitude. Neither is native
conditional sampling. They are actual additional experimental/control operations,
not free temperature names or a claim that a fixed hardware platform provides
them. Removing the guard alone does NOT prove a polynomial whole-law compiler:
off-consistency program values are stronger than ordinary F_K(X) membership,
but an efficient consumer must still be supplied. A separate construction may
quantify that complete acquisition operation; it is not assumed by this theorem.

Low rank is therefore not intrinsically the wrong structural representation;
it is too weak a guarantee of ECONOMICAL ACQUISITION under the native access
contract. A successful scientific operation needs additional native intervention,
problem structure excluding such guards, or a real algorithmic assumption.
The cryptographic premise, the source's engineered nature, and all paid resources
remain explicit. No physical impossibility, all-material lower bound, novel
PRF construction, historical-priority claim or unconditional learning lower
bound is inferred.
