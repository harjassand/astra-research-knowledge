# Mathematical review: Gram-acquired metric closure

31 October 2026. Review of the root's proposed construction.
This is a mathematical reconstruction and sharpening, not a claim of novelty,
physical execution, or a general polynomial-in-r acquisition theorem.

## Assessment

The metric-cover construction is sound under the stated bounded-noise scalar
Gram service, source stability, true contraction semantics, and finite metric
packing of the actual reachable vectors. It avoids Gram inversion, normalized
synthetic probes, and the hidden normalization/variance debt of naive noisy
Gram-Schmidt.

It does NOT resolve the polynomial-in-r problem: the proved cover can have
size (1+O(H/epsilon))^r. Its useful new interface is an acquired finite
nonexpansive abstraction with an explicit original-source measurement bill.
Ordinary metric abstraction and contraction simulation deserve prior credit.
A strong same-data ordinary metric learner can use the same construction.

The main sharpening below proves almost-sure termination and a polynomial
EXPECTED work bound in the packing number, even without a supplied dimension
bound, despite adaptive confidence failures. It relies on precise cache and
word-label bookkeeping.

## 1. Exact source and scalar experiment contract

Let T_a, a in a finite alphabet A of size m, be fixed real-Hilbert contractions.
Let f_i, i=1,...,s, be fixed seeds with ||f_i||<=1. A state label is a pair
(i,w), where w is a literal chronological primitive word, and denotes

v_(i,w)=T_w f_i.

Distinct labels can denote the same Hilbert vector. Every retained center is an
actual label; its vector is never a normalized synthetic combination.
Keep its original exact witness word, not an approximate table trajectory.

For any queried labels u=(i,p),v=(j,q), the source provides fresh bounded
[-1,1] scalar readouts with conditional mean <T_p f_i,T_q f_j>.
IID readouts for each adaptive setting suffice; the same proof also works
with bounded fresh martingale readouts having that exact conditional mean.
Shared unknown biases, gain factors, drifting sources, or uncontrolled history
dependence are outside this contract.

Chronological orientation:
<T_p f_i,T_q f_j>=<f_i,T_p* T_q f_j>.
Prepare f_j, run q, then run p in reverse order with each primitive replaced by
its ACTUAL adjoint, then perform the specified f_i scalar return test.
The total primitive word length is |p|+|q|, plus charged preparation/readout.
Adjoint access and the signed scalar mean measurement are substantive
experimental inputs. Merely preparing quantum states does not automatically
supply their signed amplitude/inner product.

Suppose the union of reachable vectors lies in a real r-dimensional subspace.
The algorithm need not know r. The packing proof can instead use any finite
packing-number bound for the actual orbit. Complex Hilbert dimension r has
real packing dimension at most2r; either charge that exponent or state a
real-Hilbert contract explicitly.

## 2. Cache, thresholds, and exact seed handling

Fix 0<rho<=1. Let

eta=rho²/32.

Cache one estimate for each unordered literal pair of state labels, including
one norm estimate for each label. Do not treat different estimates of the same
pair as independent uncharged evidence. All later uses of the same cached
estimate share its original confidence event.

Also maintain a dictionary of exact literal center labels. If a successor
label is already a center, point its transition to that center with exactly
zero discrepancy and no distance experiment. This prevents one bad cached
norm for a label from being copied into arbitrarily many duplicate indices.

Retain all s seeds as exact initial centers (deduplicate identical literal
labels if any). They need not be mutually separated. This makes the initial
state error zero. If seeds are instead approximately merged, their initial
merge errors must appear separately in later predictions.

Process every center/action pair once. For center c and action a, let y=T_a c,
represented by the appended actual word. Compare y to retained centers via

dhat²(y,c')=Ghat(y,y)+Ghat(c',c')-2Ghat(y,c').

Merge into any c' with dhat²<=3rho²/4. If there is none, append y as a new
center. Then continue breadth-first or any fair finite processing order until
every retained center/action pair has a transition.

When all three scalar estimates in a distance are accurate within eta,

|dhat²-||y-c'||²|<=4eta=rho²/8.

Consequently:
- a merge has true squared distance<=7rho²/8<rho²;
- a new center has squared distance>5rho²/8 from EVERY previous center.

The root's weaker separation sigma=rho/sqrt2 is therefore valid. One may
use the slightly sharper sigma=sqrt(5/8)rho throughout. No square-root
calculation is needed by the implementation.

## 3. Packing and work on the simultaneous confidence event

Let P_sigma be the maximum cardinality of a sigma-separated subset of the
actual reachable unit ball. In a real r-dimensional Hilbert ball,

P_sigma <= (1+2/sigma)^r.

With the conservative sigma=rho/sqrt2, use

P=(1+2sqrt2/rho)^r.

Since initial seeds were kept without separation tests, the safe total bound is

N<=s+P.

For one initial seed, all centers, including the seed, are mutually separated
on the good event, so N<=P (and the displayed s+P is harmlessly looser).
For arbitrary s, do not claim N<=P unless seed separation is separately known.

There are at most mN successor candidates. Cached scalar counts satisfy

K_geom <= s+mN+mN².

The first term covers initial seed norms; mN covers candidate norms; mN²
bounds every candidate-to-center cross moment. Repeated literal queries can
only reduce this count.

Every new center appends one action to an older center witness. Therefore a
chain of center creations has length at most N-s, and any tested successor
word has length at most N-s+1<=N when s>=1. Every Gram return word thus uses
at most2N primitive applications. This bound concerns ACTUAL witness words;
it does not replace them by approximate paths in the learned table.

For q fixed norm-at-most-one readouts g_j available through the same specified
moment interface, learn <g_j,c> at all N centers within beta. This adds at most
qN scalar estimates. A newly requested readout later requires its own N
measurements and budget; arbitrary future g is not provided for free.

## 4. One adaptive confidence event

Number distinct scalar-estimation jobs globally by k=1,2,....
Give job k failure allowance

delta_k=delta/[k(k+1)],  0<delta<=1.

The total is delta. Use fresh readouts conditional on all prior choices.
For a [-1,1] mean and requested error t_k, Hoeffding permits

n_k=ceil(2 t_k^(-2) log(2/delta_k))

shots. Geometry jobs use t_k=eta; readout jobs use t_k=beta.
A query may be chosen using all previous data. The conditional failure bound
is still delta_k because the setting is frozen before its own fresh block.

The union bound gives one event of probability>=1-delta on which EVERY
cached estimate in the entire adaptive acquisition is accurate. The same event
governs all later programs; no per-program confidence cost is needed.

This allocation works with an unknown eventual number of centers/jobs.
A fixed known K cap may use delta/K instead, but then an explicit cap is part
of that implementation.

If an already-cached entry is later required at finer precision, new shots
and an additional budget are needed. Keep a versioned refinement or a
confidence sequence. The fixed-rho proof below assumes geometry uses one
frozen cache value per literal pair; readout refinements can be kept separate.

## 5. Off-event center bound: all spurious centers can be charged to bad jobs

Let B be the number of scalar geometry estimates whose errors exceed eta.
For a finite execution prefix, form the set of its retained nonseed centers.

Remove:
1. every center whose own cached norm estimate is bad;
2. both center endpoints of every bad cached cross-Gram estimate.

An endpoint that is not a center removes nothing. A norm job removes at most
one center, and a cross job removes at most two. Exact literal-label
deduplication is essential to this statement: one cached norm cannot be
attached to unbounded duplicate center indices.

Among remaining nonseed centers, every pair was compared when the later
center was added. Its two norm values and its cross value are all good.
It follows that the remaining centers are sigma-separated.

Thus, deterministically for every finite prefix,

N <= s+P+2B.                                           (A)

Bad readout estimates do not affect center growth and can be excluded from B.
Including them gives a looser but still true inequality.

This is stronger than a good-event-only packing argument. One confidence
failure does not remove all control of the geometry.

## 6. Bad-job count has bounded exponential moments

Define E_k=1 if job k is bad, and E_k=0 if acquisition stopped before job k.
Conditional on the history immediately before job k,

Pr(E_k=1|past)<=delta_k.

For t>=0,
E[exp(t E_k)|past] <= 1+(exp(t)-1)delta_k
                   <= exp((exp(t)-1)delta_k).

Induction for B_n=sum_(k<=n)E_k yields

E exp(t B_n) <= exp((exp(t)-1)sum_(k<=n)delta_k).
Monotone convergence gives

E exp(t B) <= exp(delta(exp(t)-1)).                    (B)

In particular B<infinity almost surely, E B<=delta, and Chernoff gives the
usual Poisson-type upper tail. An elementary factorial-moment proof also gives

E binom(B,b) <= delta^b/b!,
Pr(B>=b) <= delta^b/b! for each integer b>=1.           (C)

To prove that inequality, expand the binomial coefficient into products of
distinct E_k and condition successively on the latest index. Each product
expectation is at most the corresponding product of delta_k.

Useful ordinary-moment bounds:
E B²<=delta+delta²;
E B³<=delta+3delta²+delta³;
E B⁴<=delta+7delta²+6delta³+delta⁴.

These bounds do not assume independence of the adaptively selected jobs.

## 7. Almost-sure termination without a known rank bound

If infinitely many centers were added, apply (A) to longer finite prefixes.
It would force B=infinity, contradicting (B). Hence only finitely many
centers are added almost surely. With a finite action alphabet and fair
processing, finitely many centers entail finitely many center/action jobs.
Each scalar block has finite shot count. The algorithm therefore terminates
almost surely.

The implementation does not need r or P to choose its actions; they enter
the resource theorem. If the source orbit lacks finite packing at rho, this
termination theorem is unavailable. A user-imposed finite resource cap can
return UNKNOWN without claiming absent structure.

Let M=s+P. From (A),

N<=M+2B.
For delta<=1 and M>=1, each fixed moment E(N+1)^j, j<=4, is O_j((M+1)^j).

This establishes meaningful expected work as well as termination. It is not
a uniform deterministic resource cap: rare confidence failures can enlarge
the finite table. If a known rank/packing cap is supplied, impose a center cap
M+2b with overflow probability at mostdelta^b/b!; all paths then have a
literal finite budget and overflow returns UNKNOWN.

## 8. Full expected scalar and primitive costs

For geometry t_k=eta=rho²/32,
n_k=O(rho^-4 log((k+1)/delta)).
For q readouts at precision beta,
n_k=O(beta^-2 log((k+1)/delta)).

Write K<=s+mN+mN²+qN. All logs can be bounded by
O(log((m+q+s+1)(N+1)/delta)). Including preparation/readout and all actual
return-word lengths gives pathwise primitive work

O( [ (m+1)(N+1)^3 rho^-4
      +q(N+1)^2 beta^-2 ]
    log((m+q+s+1)(N+1)/delta) ).                       (D)

The harmless +1 covers small alphabets and seed costs. This is conservative;
many cached moments or short words can make actual work smaller.

To take expectations, use N<=M+2B and the first four bounded moments of B.
For example,
log((N+1)/(M+1))<= (N+1)/(M+1),
so the extra logarithm is controlled by one additional polynomial moment.
Consequently the EXPECTED full primitive work is

O( [ (m+1)(M+1)^3 rho^-4
      +q(M+1)^2 beta^-2 ]
    log((m+q+s+1)(M+1)/delta) ).                       (E)

The same expression bounds work on the all-good event with N<=M.
Scalar shots omit one factor of N from the word-length charge.
Classical distance arithmetic is O(mN²); cache storage is O(K) estimates,
transition storage O(mN), readout storage O(qN), and parent-link witness
storage O(N). Writing literal words individually instead would cost up to
O(N²) symbols. Index and numerical bit costs remain additional.

The log and sample-budget arithmetic can be upper-rounded with rational or
integer bounds. The theorem does not require exact-real matrix algebra.

## 9. Uniform future-word guarantee

Let c_0 denote the exact center of input seed f_i. Follow the acquired
deterministic transition table under word w=a_1...a_L and let c_t denote the
center after t steps. Let x_t=T_(a_t)...T_(a_1) f_i.

On the simultaneous good event, every table edge has true discrepancy<rho.
Since every native T_a is nonexpansive,

||x_t-c_t|| <= ||T_a(x_(t-1)-c_(t-1))||
                +||T_a c_(t-1)-c_t||
             <= ||x_(t-1)-c_(t-1)||+rho.

Exact seed preservation gives ||x_0-c_0||=0, hence ||x_L-c_L||<=Lrho.
For any measured readout ||g_j||<=1,

|<g_j,T_w f_i>-yhat_j(c_L)|<=Lrho+beta.                (F)

Taking rho=epsilon/(2H), beta=epsilon/2 gives error<=epsilon for every word
of length<=H, simultaneously. The words may be selected after all training
and adaptively using prior computed predictions. There is no union bound over
the word family: (F) is a deterministic consequence of the single edge and
readout event.

After acquisition, execution of one length-L word uses L table lookups and
one readout lookup, with no source calls. The word's explicit input length
L and output numerical precision remain charged. A compressed word/program
needs a separate exact table-composition or circuit evaluator and its real
cost; it should not be called constant-time automatically.

This theorem concerns queried scalar inner products. It does not by itself
give total variation or a full physical-state simulator.

## 10. Cumulative extension to new operations/readouts/seeds

At the SAME rho and unchanged source:
- Add a new action by evaluating it on every existing center.
- Any newly added centers are expanded under ALL currently admitted actions.
- Keep old edge transitions. They retain their same discrepancy guarantee.
- New readouts require center measurements, but no new state centers solely
  to compute those scalar readouts.
- New seeds may be retained exactly, increasing the separate seed count s.

Every old moment and transition remains usable only while its source binding,
adjoint semantics and measurement calibration remain valid.

If the final finite action library has orbit rank r_final/packing P_final,
the same global center proof applies with that final orbit. Do not use the
old rank bound after a new operation activates new directions.

Continue the job index and confidence allocation across extensions rather
than restarting a full delta allocation each time. If there are infinitely
many requested new actions/readouts, no finite total task or total-cost bound
is claimed; each finite prefix has its charged bound.

For a stricter rho_new<rho_old, old merges may be too coarse.
Recheck/reassign all old center/action edges under the new threshold, acquire
finer scalar accuracy and charge new estimates. Old centers remain valid
actual vectors. Old nonseed separations are stronger than required at the
new smaller rho, but old edge precision is not automatically upgraded.

## 11. Supplied global orbit-gap corollary

Assume additionally that every two DISTINCT reachable vectors are separated
by at least gamma>0. This is a GLOBAL supplied structural fact, not something
certified by finitely many sampled pair distances.

Choose rho<gamma. On the good event, every merge has true distance<rho<gamma,
so every merge identifies EXACTLY THE SAME Hilbert vector.
A candidate equal to an existing center always passes the merge test, since
its estimated squared distance<=rho²/8<3rho²/4.
Every accepted transition is therefore an exact quotient transition.

The learned deterministic transition table reproduces the exact reachable
vector for every finite word, at every horizon. Only readout estimation remains:

|<g_j,T_w f_i>-yhat_j(c_w)|<=beta
for ALL finite words w on the single acquisition event.

There is no Lrho accumulation and no per-later-program statistical debit.
The reachable orbit is finite by packing; its cardinality is at most
(1+2/gamma)^r for one real r-dimensional unit ball. Mandatory duplicate seed
labels can inflate table indices unless deduplicated, but do not change
physical orbit cardinality. On the good event, nonseed duplicates never arise.

The condition is meaningful for sources with finite separated observable
orbits. It excludes arbitrarily fine continuous rotations. It must not be
advertised as a conclusion from low rank or successful finite acquisition.

## 12. Remaining limitations and comparison discipline

- This acquires a finite metric abstraction, not an orthonormal minimal
  realization and not a new proof that low rank alone gives polynomial work.
- Cover size is exponential in r at fixed rho. For fixed H the safe
  worst-case M is (1+O(H/epsilon))^r. A conventional spectral learner with a
  well-conditioned frame may be dramatically cheaper.
- A conventional metric-state learner supplied the same adjoint Gram service,
  records, confidence budgets and retention rights can use the same table.
- Without actual signed Gram/adjoint-return measurements the acquisition
  theorem is unavailable. Replacing these by passive trajectory statistics
  changes the source interface and may introduce severe rarity costs.
- The measured primitive length grows with acquired witness depth; source
  experiments are not unit-cost table entries.
- Separate source drift, finite apparatus bias and calibration uncertainty
  require their own deterministic/error debits. They are not covered by
  an IID bounded-shot confidence allocation.
- Arbitrary controller policies using new unmeasured output variables or
  coherent operations are outside the fixed alphabet/readout contract.

