# A packed guarded source and the parameterized acquisition boundary

30 October 2026. Private mathematical construction. This is a CONDITIONAL
computational obstruction, not an unconditional lower bound and not a
cryptographic experiment. Classical randomized algorithms throughout.

## 1. Target, controlling predecessor, and the extra assumption

For a full-support binary length-T law P write

    ell_P(h) = (1/2) log[P(1|h)/P(0|h)].

At cut t the ENTIRE future next-token logit matrix has entries ell_P(hf),
|h|=t, |f|<T-t. Its maximum real rank is the logit rank. These are NOT
logs of complete suffix probabilities and NOT probability predictive ranks.
The native oracle returns an independent next bit at any submitted prefix.
Prefix tokens, replies, arithmetic, output size, and source-free generation
are all charged. Every prefix is legal because P has full support.

The intended FPT learner has cost

    f(d) * poly(T, alpha, 1/epsilon, log(1/delta), L_in),             (1)

where the polynomial's degree is independent of d. Both training and the
standalone student's one-output cost obey this form. A supplied alpha bounds
the Euclidean norms of both factors of each cut-logit matrix. The usual
interpretation supplies a rank UPPER bound d; one can replace any f by its
nondecreasing envelope over smaller integer ranks.

Mausberg, Learning Low-Logit-Rank Distributions from Conditional Samples
(8 October 2026), at commit78fa048d082b465f0925299958dfb1063f38668a,
already proves T^{O(d)} native acquisition and a guarded, growing-rank PRF
obstruction to joint polynomial acquisition. Its Section 8 expressly leaves
arbitrary FPT dependence open. Its linear mismatch counter stores every
payload bit, so that source has rank n+O(1). We do NOT relabel that theorem
as an FPT lower bound. The source below packs s payload bits per real
coordinate and uses a QUADRATIC whole-word residual as the guard. Only
affine fixed-symbol updates of a lifted state are used.

ASSUMPTION E (explicitly stronger than polynomial PRF security): There are
constants gamma>0, C0 and a uniform Boolean strong PRF family

    F_k : {0,1}^n -> {0,1}

with polynomial-length keys, a known polynomial-size public evaluation
template, and fixed-key Boolean circuit depth <=C0 log n. For EVERY
classical randomized membership-oracle distinguisher running for at most
2^(gamma*n) bit operations, its advantage is <1/20 at EVERY sufficiently
large n (the cutoff may depend on the distinguisher).
The circuit/program description from a key can be obtained in polynomial
time; the simulator used in the proof does NOT know that key. We can decrease
gamma and assume 0<gamma<1/4. A matching nonuniform version gives the matching
nonuniform conclusion. Quantum processing requires a matching quantum-secure
premise, not merely Assumption E.

Assumption E is NOT inferred here from ordinary polynomial-hard LPN, LWE,
DDH, or from the qualitative NC1-PRF existence theorem. Its concrete time
and payload-length relation is load-bearing. The unconditional statement
below is a resource-preserving reduction to breaking this stated premise.

THEOREM: Under Assumption E no learner of form(1) can, for EVERY such P,
return with probability >=2/3 a standalone law Q with TV(P,Q)<=1/64.
In particular the native-only low-logit-rank promise alone does not yield
the requested FPT operation under that premise. The existing XP theorem
and all fixed-d positive results remain consistent with this conclusion.

## 2. Public read program

Barrington's width-five permutation-program construction turns the fixed-key
NC1 circuit into a polynomial-length program. Its strong form permits a
known initial one-hot q in R^5 and known accepting subset (a single selected
coordinate suffices) so that the final q_acc is exactly F_k(X). All choices
of instruction bits, consistent or not, still leave q one-hot.

If the original read schedule is key-dependent, use the established public
sweep construction from Mausberg Section5: replace each instruction by a
sweep of all n payload coordinates, with its actual permutation pair only
at the selected coordinate and identities elsewhere. Add/pad identity
sweeps if needed. Thus there is a PUBLIC polynomial-length read schedule

    i_1,...,i_L in {1,...,n},             L <= poly(n),

and hidden permutation pairs P_{a,0},P_{a,1}, whose evaluation on the
consistent read word gives F_k(X). The compiler does not receive the pairs.
All padding/length bounds are known, independent of the secret key.

Fix a positive integer p, the packing parameter. It will be a CONSTANT
chosen after a hypothetical FPT algorithm and its polynomial degree are
fixed. Put s=ceil(n/p), N=p*s and pad the payload by N-n extra uniform bits.
The PRF ignores those extra bits. Partition the N-bit payload into p blocks
of s bits. Replace each public read of X_i by a full scan of all s bits of
its block. At its selected bit apply P_{a,b} to q; all other scanned bits
leave q unchanged. The scan count is L and total emitted copy bits m=L*s.
Only the prescribed selected copy bit advances the old program instruction.

## 3. Source on EVERY prefix, including inconsistent scans

Choose integers

    K = n^2+1,       C = 20(n^2+1),       delta0 = 2^(-s-1).

During the first N positions emit independent uniform bits. In block i
maintain

    r_i = delta0 + sum_{j already written} X_{i,j}*2^(-j),
    z_i = r_i^2.

Initially r_i=delta0 and z_i=delta0^2. Writing b at weight w=2^(-j)
updates r_i <- r_i+b*w and z_i <- z_i+2*b*w*r_i+b*w^2, where the right
side uses the OLD r_i. This is a linear map of (1,r_i,z_i).

At the start of every scan of block i set u=r_i and v=z_i. Maintain u as
the residual after subtracting previously emitted scan bits. Before scan
bit j define the INTEGER

    S_j = 2^(s+1)*(u-2^(-j)),

and emit b with odds

    P(b=1|h)/P(b=0|h) = 2^(2*K*S_j).                              (2)

After observing b update

    u <- u-b*2^(-j),
    v <- v-2*b*2^(-j)*u + b*2^(-2j),                              (3)

again using the OLD u on the right. Thus v=u^2 remains exact even on an
arbitrary inconsistent prefix. At scan end add

    2^(2*s)*(v-2*delta0*u+delta0^2)                              (4)

to a scalar G initialized at zero. Then reset u,v from the next block when
its scan starts. Formula(4) is exactly the SQUARE of the integer difference
between the original s-bit block and the observed scan word. Hence G is
a nonnegative INTEGER, is zero iff EVERY completed scan matches its
payload block, and is at least one otherwise. No cancellation of different
wrong scans is possible. The diagonal quadratic lift z_i and the scratch
square v are the essential changed representation.

After the m copy bits emit one label Y with odds

    P(Y=1|h)/P(Y=0|h) = 15^(2*q_acc-1) * 2^(-C*G).                (5)

On G=0 the copies are consistent and q_acc=F_k(X_1...X_n), so the label
agrees with that value with probability15/16. If G>=1 its probability of
being1 is <=15*2^(-C), independently of every secret program transition.
All remaining positions are independent LOCAL fair padding bits.

Choose the length

    T = max(32, N+m+1, 16*(C+K+1)*(L+1)*2^(2*s)).                  (6)

The source stops its nontrivial part after the label; T-padding is only
part of the mathematical source and of a learner's charged output.

## 4. Uniform magnitude, exact rank and finite native source cost

On every legal or inconsistent prefix, 0<r_i<1, 0<z_i<1,
-1<u<1 and 0<=v<1. There are at most L completed scans, each integer
word difference has magnitude<2^s, so 0<=G<L*2^(2*s). The program state
remains one-hot. Thus the copy logits from(2) satisfy

    |ell| = |K*S_j*log2| < 3*K*2^s,

and the label satisfies |ell| <2+(C/2)*L*2^(2*s). Formula(6) bounds all
these magnitudes by T. Every conditional probability is strictly between
zero and one, with rational numerator/denominator using O(T) bits.

The lifted state

    (1, r_1,...,r_p, z_1,...,z_p, u,v,G,q_1,...,q_5)               (7)

has dimension d=2*p+9. Every FIXED time/token update is linear in(7):
input writing, subtraction, square accumulation, resetting scratch, and
the chosen permutation of q. Every next-token logit is a linear readout
of(7), including log15 in(5). Therefore for ANY cut and ANY future word f,
ell(hf) is a fixed linear functional of the state after h. This proves
the full-future cut-logit rank <=d, including cuts before input completion,
within scans, after an error, and after the label. No consistency event is
used in the rank proof.

For completeness, a rank<=d real matrix with entries in[-T,T] admits
factors of norms <=sqrt(d*T): choose a maximum-volume actual row basis,
whose coefficients for any actual row have modulus<=1, then rescale its
coordinate/value factors. This is the established maximum-volume lemma,
not a supplied singular-value promise. We can supply the explicit integer

    alpha=d*T+1.                                                  (8)

Native conditional coins are computable from the input prefix and the
secret program. Exponents in(2),(5) have O(T) magnitude, but only
O(log T)=O(s+log n) description bits. Even an EXACT native source need not
allocate the full numerator/denominator: a Bernoulli race between weights
2^(-a) and1 samples probability1/(1+2^a). A 2^(-a)-coin stops on the first
one in at most a fair bits, using fewer than2 bits on average. The race
accepts a1-weight proposal with probability at least1/2 on each round.
For label odds15*2^(-a), implement the small race weight as
2^(-(a-4))*(15/16); for odds2^(-a)/15 use2^(-a)*(1/15).
Here a>=C on a guarded label, so a-4>=0. The unguarded label uses four
bits directly. These are ordinary positive Bernoulli races. They give
<10 expected fair bits per reply and polynomial(n) expected bit work
apart from the explicitly submitted prefix tokens. Their counters have
O(log T) bits. No numerical logit VALUE is used.
For the worst factor1/15 race, a power-two coin uses at most2 expected
bits and uniform0..14 rejection uses64/15; a round therefore uses at
most1+(2+64/15)/2=62/15 bits on average. Renewal with acceptance probability
at least1/2 gives the uniform bound124/15<10. This pays the local loops.

The security simulator below is simpler still: it replaces each copy coin
by its majority bit, with a uniformly negligible per-query error.
One full prefix/reply consumes at most T submitted/returned symbols.
The public source has a compact O(poly(n)) description apart from its
declared padding length; the hidden key is not given to the learner.

## 5. Almost-all-mass hidden computation

If all preceding scan bits match, then u-2^(-j) has the sign of the jth
payload bit and magnitude at least delta0. Hence |S_j|>=1 and a scan
error has conditional probability <=2^(-2*K). A union bound yields

    Pr(any scan error) <=m*2^(-2*K).                               (9)

In particular the meaningful label occupies almost all generated mass.
This is not a rare-event or rare-coordinate lower bound. On G=0, Y is
the hidden Boolean label with constant independent noise1/16. The first
n payload bits are exactly uniform, regardless of every later operation.

## 6. Key-free native-query simulation

Given membership access to an arbitrary Boolean function H, simulate input
and padding queries with fair bits. At a copy query compute S_j from the
parsed original payload and submitted scan prefix and return1 iff S_j>0.
The integer S_j is ODD on EVERY prefix, since its numerator contains the
midpoint offset1 and all subtracted terms are even. Thus S_j cannot be0,
and the discrepancy from(2) is at most2^(-2*K), even on inconsistent scans.
This requires neither a hidden program nor H nor an exponential-size
rational denominator.
At the label, compute the exact integer G from the submitted payload and
all submitted scan words. If G=0, query H(X_1...X_n) and return that label
with independent noise1/16. If G>0 return0. Thus EACH arbitrary native
prefix query uses at most ONE ordinary H-membership query. This includes
prefixes which had negligible probability under the source.

For H=F_k, the label simulation is exact on G=0 and differs by at most
15*2^(-C) on G>0. With the preceding copy replacement, a uniform conservative
per-query discrepancy is16*2^(-2*K). An adaptive q-query transcript therefore
has TV at most16*q*2^(-2*K). The source's active word has polynomial(n)
length. Parsing, integer G and majority-coin arithmetic require only
polynomial(n) work per request; a padding query can return a fair bit
immediately. Reading/writing submitted prefix tokens remains charged to
the learner's bit runtime. The polynomial overhead's degree is independent
of p, apart from its fixed input/description cost. A transcript complete-suffix
request is simulated one next-token query at a time, charging its tokens.
The simulator records all payloads submitted to H.
Its approximate query table can contain zeros and need not itself satisfy
the structural promise. Only its uniformly coupled, CAPPED query transcript
is used; no robustness theorem for an out-of-class teacher is assumed.

## 7. Standalone-sampler distinguisher

Suppose(1) exists. Set epsilon=1/64, delta=1/3, and run it using the
simulator, with parameters T,d,alpha from(6)--(8). The output law is a
standalone sampler, with no H or native source access after training.
Run it once. Reject unless every scan matches its payload block and the
first n payload bits X were never submitted to H during training. Query
H(X) once and accept iff the emitted Y equals H(X).
Malformed or nonterminating output code, and outputs other than length-T
binary words, are rejected within the declared time cap. The standalone
generation machine has only fair bits, not another oracle interface.

For H=F_k, a TV-accurate returned sampler has this acceptance event with
probability at least

    15/16 - 1/64 - m*2^(-2*K) - q/2^n.

The source's uniform X pays the last term, even for adaptively chosen
training payloads. Multiplying by the learner's success2/3 gives overall
acceptance >=59/96-o(1), provided q<=2^(gamma*n) and gamma<1. The coupling
error16*q*2^(-2*K) is negligible. Failed learner outputs contribute at least0.

For a random Boolean H, conditioned on the training transcript and sampler
coins, the value H(X) is a fresh unbiased bit whenever the verifier has not
already rejected. Acceptance is therefore at most1/2. The advantage is
at least11/96-o(1), exceeding1/20 for large n. There is no test of student
conditional probabilities or numerical density values in this reduction.

## 8. Why this excludes ANY f(d), rather than only polynomial f

For each fixed p,

    log2(T) <=2*n/p+O(log n),   alpha<=d*T+1,   d=2*p+9.            (10)

All public template lengths and source/simulation overheads contribute
only fixed polynomial factors in n,T. If a learner and its standalone
sampler obey(1), there is a CONSTANT c_* independent of p such that the
whole distinguisher has time

    f_*(2*p+9) * T^(c_*) * poly(n),                               (11)

for fixed epsilon,delta. The computable f_* may be arbitrarily large.
Choose a fixed integer p>4*c_*/gamma AFTER the algorithm is fixed.
Then(10)--(11) are <=2^(gamma*n) for all sufficiently large n, since
log f_*(2*p+9) is a CONSTANT while n grows. This contradicts Assumption E.
No bound on the growth of f is used.

If a proposed learner has only an expected FPT training/generation bound,
cap it at a sufficiently large constant multiple of that bound and reject
on overrun. Markov's inequality reduces the above constant advantage by
an arbitrarily small fixed amount. Runtime in the random-function case
must also be capped: that simulator need not be a member of the low-rank
class. This completion prevents a bad-source nontermination loophole.

The existing T^{O(d)} algorithm is consistent: its T exponent grows with p,
so the product of its exponent and n/p need not become small. There is
no contradiction with fixed-d polynomial learnability.

The padding is not an information supplier. Without it the same source
has active horizon T0=N+m+1=poly(n), logit bound B<=T from(6), and supplied
factor bound alpha=d*T+1. All rank/simulator/full-law arguments continue
to hold. Their resource bound is then f(d)*poly(T0,alpha), with
log2 alpha<=2n/p+O(log n). Padding only places it inside the controlling
primary's convention |ell|<=horizon and alpha<=poly(horizon).

In fact the same argument excludes the more general resource bound

    f(d)*(T+alpha)^h(d)*poly(L_in),       h(d)=o(d),                (12)

at the fixed accuracy/confidence above. For d=2p+9, choose a sufficiently
large fixed p so that2*h(2p+9)/p and any fixed simulation overhead are
below gamma. Then let n grow. Thus the construction supplies, under the
stated quantitative premise, a rank-linear necessity for the polynomial
exponent, rather than just a failure of one monomial approximation.

## 9. Scientific disposition and ordinary alternatives

The unconditional construction is the state/guard/simulator/cost reduction.
The NO-FPT conclusion requires the quantitative PRF premise inSection1.
No claim is made that ordinary polynomial LPN/LWE implies that premise, or
that it is experimentally acquired. The original FPT problem remains
unconditionally unresolved here. No apparatus or physical device is used.

The changed target is substantive: exact low-logit rank plus a bounded
factor does not, under that premise, supply a condition-free FPT discovery
compiler. A successful stronger operation must pay additional structure
or access not uniformly simulated by Boolean membership in this source,
or allow a rank-dependent polynomial exponent. This is a whole-law,
high-mass obstruction rather than a requirement to resolve discarded tails.

Native junta membership learners get their actual FPT guarantees; this
source is not a junta in O(d) original input variables. Exact weighted-
automaton learners get exact field-valued membership plus equivalence
counterexamples; native Bernoulli samples are weaker. Gaussian-input FPT
ReLU learners get their Gaussian geometry and network-size/Lipschitz
parameter dependence; they do not provide arbitrary-prefix logistic
recurrence acquisition. The known XP/native compiler remains the strongest
unconditional matched general route in the controlling source. Numerical
nonlinear fitting remains a legitimate practical comparator, with no
general guarantee claimed either way.

The accompanying finite exact program control validates the packed-square
state/compiler for an explicitly supplied noncryptographic permutation
program. It is not evidence for Assumption E, not a PRF instance, not a
full learner run, and not an empirical complexity separation.

## 10. A quantitative conventional instantiation, with its assumption paid

The explicit Assumption E is enough for the theorem. It can also be
obtained from the following specified stronger number-theoretic premise;
this subsection is a reduction of assumptions, NOT a hardness proof.

ASSUMPTION D4: There is a polynomial-time parameter generator for finite
field subgroups with modulus bit length O(lambda), prime subgroup order
Q>=2^(c0*lambda) for fixed c0>0, and the usual random nonidentity generator.
For some cD>0 and EVERY classical randomized algorithm of time
2^(cD*lambda^(1/4)), its advantage on the corresponding DDH challenge is
<lambda^(-2) at EVERY sufficiently large lambda (the cutoff may depend
on the algorithm). The security parameter is public.
Efficient generation and both quantitative bounds are part of the premise.

The primary Naor--Reingold JACM2004 Theorem4.1 has an explicit time/advantage
reduction: a group-valued PRF distinguisher of time t and advantage e gives
a DDH distinguisher of time poly(lambda,n)*t and advantage e/n, where n
is the number of input coordinates. Section4.2/Theorem4.5 provides
fixed-key TC0 evaluation after polynomial preprocessing. We use those
constructive facts, not only qualitative PRF existence. The n-coordinate
hybrid proof is unchanged when the independently chosen group parameter
lambda is polynomially larger than n.

Take lambda=n^4. Build the n-input Naor--Reingold function in that group,
and hash its ordinary binary group encoding to ONE bit by an independent
pairwise-independent affine binary hash h, included in the key (it may
even be public). The key and all preprocessing have polynomial(n) length.
Fixed-key TC0 evaluation plus that affine parity is contained in NC1,
with circuit size polynomial(n). The subgroup's encoding length is also
polynomial(n); neither an infinite-precision arithmetic gate nor a group
encoding oracle is granted.

Here is the quantitative Boolean-output check, instead of assuming a
particular group-encoding bit balanced. For a uniform group element U and
fixed h put b_h=Pr(h(U)=1)-1/2. Pairwise independence gives

    E_h b_h^2 <=1/(4*Q),       E_h |b_h| <=1/(2*sqrt(Q)).

For a truly random group-valued function, values on distinct adaptive
inputs are independent uniform group elements conditional on h. Coupling
each newly exposed output to a fair bit therefore bounds the TV from a
random Boolean function, for at most q queries, by q/(2*sqrt(Q)). Repeated
queries reuse the same coupled answer. This also holds when h is public.
For q<=2^(gamma*n) this error is negligible since Q>=2^(c0*n^4).

A Boolean PRF distinguisher of constant advantage and time2^(gamma*n),
after subtracting that negligible hash discrepancy, would consequently
give DDH advantage >=1/(40*n) in time poly(n)*2^(gamma*n), say. Choose
0<gamma<min(1/4,cD/2). For sufficiently large n this is below the D4 time
limit2^(cD*n), whereas1/(40*n)>lambda^(-2)=n^(-8). This contradicts D4
and supplies Assumption E. The constants40 and1/4 merely reserve slack.
To view this as a DDH algorithm at every security parameter, run the
reduction when lambda is a perfect fourth power and reject otherwise.
It violates D4 on infinitely many such powers; the stated every-sufficiently-
large-parameter security quantifier excludes that too.

The 2026 generic low-depth weak-to-strong PRF theorem is NOT silently used
for this quantitative instantiation. Its displayed shattering condition
allows polynomial query numbers and does not directly pay2^(gamma*n)
queries. Nor does ordinary polynomial DDH security imply D4. The result
is conditional on the stated subexponential-time finite-field hardness,
or directly on E, with no claim of unconditional complexity separation.
