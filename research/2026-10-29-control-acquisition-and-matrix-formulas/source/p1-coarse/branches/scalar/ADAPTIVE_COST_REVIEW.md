# Independent review: adaptive experiment cost for the slow positive pair

28 October 2026. Scope: the new primitive-application cost theorem, adaptive
stopping, prediction reduction, and matching direct experiment. This review
does not reopen the accepted support obstruction or echo compiler.

Reviewed artifacts and SHA256:

- ADAPTIVE_EXPERIMENT_COST.md:
  11f41e16d27d72ac5973f5cab5c7aaf0c4b76c33fce072907ca317159b0125fc
- core/adaptive_cost_obstruction.py:
  a6bd0d77c3105f5eb28b931259e14f4a5d7f337be925a39457bb9a8d28305ee6
- results/ADAPTIVE_COST_OBSTRUCTION.json:
  50d37e1ef7e989c46d95127b308aeb7520a609404fc527d2b3f170bd3a495264

## Verdict

The theorem is valid for fresh independent Bernoulli word queries. The
constants 2/(3e), 49/100, 64 and 320/e are sound. The lower bound covers
arbitrary adaptive finite word lengths and almost-surely finite stopping.
Finite expected receiver-call count is unnecessary. The matching order
concerns this known two-hypothesis family and this receiver. The charged
quantity is aggregate primitive applications, not unrestricted parallel
elapsed time.

## 1. Information per query

Let 0<e<=1/4, k a nonnegative integer, and g(x)=x^k. The responses are

    f_A(k)=[1+(1-2e)^k]/2,   f_B(k)=(1-e)^k.

For k=0,1 their difference d_k is zero. For k>=2, convexity gives d_k>=0.
On [1-2e,1], 0<=g''(x)<=k(k-1). Expanding at 1-e and averaging the two
Taylor remainder formulas cancels the linear terms, so

    d_k <= e^2 k(k-1)/2.

Writing y=(1-e)^k and using 0<=1-2e<=(1-e)^2 also gives

    d_k <= (1+y^2)/2-y = (1-y)^2/2 <= 1/2.

These are all-length proofs. Since q_X=1/4+f_X/2 lies in [1/4,3/4],
q_A-q_B=d_k/2 and q_B(1-q_B)>=3/16. The elementary inequality log x<=x-1
gives KL(Bern(p)||Bern(q))<=(p-q)^2/[q(1-q)], using natural logarithms.
Consequently

    KL_A,B(k) <= (4/3)d_k^2
              <= (1/3)min{(ek)^4,1}
              <= ek/3.

The last step follows by splitting ek<=1 and ek>=1. Zero-length queries
have zero information and zero charged cost, consistently with this bound.

## 2. Adaptive stopping without an integrability gap

Fix one algorithm with source-independent private randomness. At call t it
chooses finite k_t measurably from its previous transcript. Conditional on
this history, the observation is a fresh Bernoulli variable with mean
q_X(k_t). Let N be its almost-surely finite stopping time, C=sum_{t<=N} k_t,
and let its final decision be measurable from the stopped transcript.

Include the private random seed in the transcript and pad a stopped run
with a common deterministic dummy symbol. Let P_X^n denote this transcript
through n receiver calls. The seed, common query policy and common stopping
policy contribute zero conditional KL. The finite chain rule gives

    KL(P_A^n||P_B^n)
      = E_A sum_{t<=min(N,n)} KL_A,B(k_t)
      <= (e/3) E_A sum_{t<=min(N,n)} k_t
      <= (e/3) E_A C.

If E_A C is infinite, the claimed lower bound is automatic. Otherwise the
display holds for every n even when E_A N is infinite; a finite expected
number of calls is not being assumed.

An especially direct stopping proof uses the finite-transcript event

    E_n={N<=n and the final decision is A}.

Termination and error <=1/3 under each hypothesis imply

    P_A(E_n) -> a>=2/3,   P_B(E_n) -> b<=1/3.

Pinsker at each finite n gives

    2[P_A(E_n)-P_B(E_n)]^2
       <= KL(P_A^n||P_B^n) <= (e/3) E_A C.

Taking the limit proves E_A C>=2/(3e). This avoids optional-stopping or
uniform-integrability assumptions about a log-likelihood martingale.
Equivalently, relative entropy on increasing finite-transcript sigma-algebras
converges to full transcript relative entropy, validating the source note's
stopped-transcript KL statement. The finite-event argument suffices without
invoking that general result.

Two optional strengthenings do not affect the claimed order. The same
per-query KL bound holds with A and B exchanged, giving E_B C>=2/(3e).
Data processing to the decision gives the sharper
KL>=kl(2/3,1/3)=log(2)/3, hence E_A C>=log(2)/e. The original constant is
valid and does not require either change.

## 3. Target separation and confidence scope

For integer m>=4, e=1/m and H=5m,

    f_A(H)>=1/2,
    f_B(H)=(1-1/m)^(5m)<exp(-5)<1/100.

Thus the amplitude gap exceeds 49/100. The exponential inequality follows,
for example, from a positive partial sum of the series for exp(5) exceeding
100.

A predictor returning hat_f(H) with absolute error <=1/5 with probability
>=2/3 under each source can be thresholded at the known midpoint. Its two
success intervals are disjoint because 2/5<49/100. A pointwise guarantee at
this H suffices; a simultaneous all-word guarantee is stronger.

The probability must concern actually delivering an accurate answer.
Always reporting [0,1] is a valid confidence interval at zero cost, but it
does not meet the accuracy task. A procedure that almost always declines
also need not satisfy the testing premise. Conditional correctness whenever
a narrow certificate is emitted is insufficient without a sufficient
unconditional probability of producing a usable correct answer. The source
note's explicit error <=1/5 and success probability >=2/3 formulation is
adequate.

This is a worst-case obstruction across sources as e tends to zero. It does
not deny arbitrarily long reuse for a fixed acquired source, or guarantees
under additional uniform stability or detector assumptions. The first
acquisition cannot have a cost bound independent of this slow source scale.

## 4. Matching direct execution

At H the Bernoulli mean gap is d_H/2>49/200. Its midpoint is distance
d_H/4>49/400 from either mean. With n=64 independent trials, one-sided
Hoeffding gives, under either source,

    P(error) <= exp[-2n(d_H/4)^2]
             = exp[-n d_H^2/8]
             < exp[-64(49/100)^2/8] < 1/3.

The exponent is 1.9208, yielding a bound about 0.1465. The charged cost is
64H=320/e. There are also 64 resets and readouts; fixed per-trial overhead
independent of e preserves the order. Both lower and upper procedures may
know e and the two candidate models, so the comparison is equally informed.

Within this two-hypothesis promise, successful identification also provides
the entire exact formula k -> f_A(k) or k -> f_B(k). Therefore the upper
construction can supply an all-word predictor on its success event. It is
not an upper bound for learning a larger hidden-operator class merely
because that class contains this pair.

The reciprocal-integer restriction only simplifies the constant. For
general 0<e<=1/4, H=ceil(5/e) has the same separation and 64H<=336/e.

## 5. Material scope and literature boundary

Every adaptive choice of finite k is allowed, but the receiver still consists
of reset, one unknown power, and one independent binary observation of the
declared mean. Different preparations, coherent combinations of words,
intermediate-state measurements, changed noise laws or changed evolution
speed require a new information bound. An exact scalar receiver would
distinguish the known pair at k=2 because d_2=e^2>0; it is a stronger
instrument than the noisy binary receiver here.

The cost is aggregate primitive execution work. Interpreting it as elapsed
physical time requires a serial device or explicit fixed parallel capacity.
Unlimited parallel receivers can trade more applications for less elapsed
time. Omitted reset, readout and computation costs only strengthen the lower
bound as a work bound.

The proof method is established adaptive change of measure. A primary
reference is Kaufmann, Cappe and Garivier, On the Complexity of Best-Arm
Identification in Multi-Armed Bandit Models, JMLR 17 (2016), Lemma 1 and
Remark 2. They relate adaptive expected sample counts, KL divergences and
testing events at almost-surely finite stopping times:

https://www.jmlr.org/papers/volume17/kaufman16a/kaufman16a.pdf

This review proves the countably many lengths and charged-length version
directly; the paper's finite-arm statement is not used as an unqualified
substitute. The substantive addition is the source-specific information per
application and its matching operational interpretation, not a new general
sequential-testing principle.

## Verification scope

Independently derived: all-length envelopes, adaptive finite-prefix argument,
probability-to-amplitude factors, confidence reduction, and matching cost.
I read the exact rational check script and recorded output. Its 57 finite
checks and exponential partial-sum checks agree with these formulas. They
support the examples but do not replace the all-length or stopping proof.
No unrelated accepted experiments were rerun and no reviewed source artifact
was modified.
