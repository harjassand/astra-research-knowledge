# Synthetic procedures from expired incomplete tasks

Owned new obstruction: lazy cross reconstruction still assumes old task
oracles remain callable. Here each training task permits r anchor values and
at most one further native value, then disappears. Can incomplete episodes
leave a reusable *procedure family*, without a supplied useful basis or a
false claim that a common low-rank world was recognized?

Construction: represent the unknown procedure by a linear graph R over an
observed native anchor profile. Every extra source observation is a linear
constraint on R. Retain its whole compatible affine family, and compile only
the image needed for the next task's *actually measured* anchor profile. This
can reduce later acquisition even before the common representation is unique.
This is theory, not a new source/fixture/callback run. Closest primary
incomplete-vector/subspace-identification work is the immediate next check.

## 1. Known native envelope, not a useful latent representation

H is an explicit M-dimensional F_p space of native functions, with its actual
feature programs and a checked native unisolvent set Z. This can be the full
table space on a finite domain; its cost is then the whole domain size. A
polynomial specialization uses native total degree D<p; no derivative/source
bytecode access is required. All feature evaluation and linear algebra are
paid. Source identities and within-episode stationarity remain contracts.

Choose r<M independent native evaluation rows P=(x_1,...,x_r) from Z. This is
known-feature row selection, not discovery of useful task axes. By paid
inversion of the full Z evaluation matrix, use its cardinal basis: psi_l is
one at x_l and zero at the other Z points, while k_j is one at the j-th
nonanchor Z point and zero at the others. Thus k_1,...,k_m form a native
basis of ker(E_P), m=M-r. Every f in H uniquely has

    f(x)=psi(x)^T a + k(x)^T b,  a=E_P f, b in F_p^m.

The proposed common procedure graph is b=R a, R in F_p^(m by r). It defines
the synthetic r-dimensional space

    U_R=span{g_l: g_l=psi_l+sum_j R_(jl) k_j}.

This is a candidate language. It is not asserted to contain the actual old
tasks just because finite observations admit it. No R, latent a, subspace,
cohort label or useful source sampler is granted.

## 2. Expiring source observations leave linear procedure constraints

On training task t, acquire a_t from r native anchor queries. Select at most
one additional native point y_t before that source expires. Its measured
residual obeys, under the graph hypothesis,

    d_t=f_t(y_t)-psi(y_t)^T a_t = k(y_t)^T R a_t.              (1)

Thus its known design row is a_t^T tensor k(y_t)^T. Stack these real native
observations, solve for an affine family

    R in R_0+K,  K=ker(design matrix).                       (2)

Reject inconsistent constraints as UNKNOWN; do not delete inconvenient old
tasks or silently drop coefficients. A particular solution is merely a
normalization of the family, never evidence of a true unique R. Every
training value is retained/charged, including zero/duplicate profiles and
failed rank attempts. With T episodes, source calls are at most (r+1)T.
All old sources may now disappear; no later use of their oracles is needed.

If each row of R is to be determined separately, a simple sufficient design
uses y_t in Z\P. For every such y_j, collect r anchor profiles spanning F_p^r
and solve the resulting r equations for that row. This costs r(M-r)
successful extra observations, at most one per episode; exposure of useful
profiles is *checked* rather than assumed. Skipped/unsuccessful episodes are
still paid, and there is no bounded completion time without coverage.

The general tensor-row design (1) retains more information than this
separate-row policy. Known-feature experiments may be selected using its
actual current kernel K: profile a is useful iff K a is nonzero. If useful,
choose a nonzero v=Delta R a, Delta R in K. Then h(x)=k(x)^T v is a known
nonzero native function. Search the actual unisolvent set Z using paid known
feature evaluations until h(y)!=0; the new row at y does not annihilate K,
so the one source answer raises constraint rank by one. No extra source
answer is used during this point search. This is a compiled experimental
choice from acquired uncertainty, not a supplied useful-point oracle.

Such a choice does not create useful future profiles or guarantee optimal
online allocation against an adversarial future source sequence. Failed
coverage remains a real cost. The result is the per-useful-profile rank
increment, not a free curriculum.

## 3. What a complete family identifies, and what it does not

If (1)'s design rank is mr, R is unique and yields explicit native programs
g_l after all old sources have expired. No old function had to be completed
while its source existed. This is acquired synthetic preparation/evaluation,
not a retained oracle alias.

Conditional identifiability theorem: suppose there is a compatible world in
which all training functions lie in some common subspace U of dimension<=r.
If the observed anchor profiles span F_p^r, then dim U=r and E_P:U->F_p^r
is an isomorphism. Consequently U=U_R for one graph R. If the design has full
rank, (1) forces that same R in EVERY compatible rank<=r world. The family is
therefore learned within that class without supplying its basis or an
anchor-injectivity promise; the observed profile rank supplied injectivity.

Proof: the profile rank implies dim E_P U>=r, while dim U<=r. Hence E_P U
has rank r and zero kernel on U. Its inverse is a graph in the chosen H
splitting, which must satisfy all observed equations. Full design rank makes
that graph unique.

This does not finitely recognize the common-rank hypothesis in general.
Specifically take M>r+1, T>r, profiles of rank r and a compatible graph R_0.
Choose a task whose removal leaves profile rank r. Keep all other functions
equal to their R_0-graph functions, and add to this task a nonzero H-function
h vanishing at its r anchors and its one extra measured point. Such h exists
by the dimension inequality. The unchanged other tasks span U_(R_0); h is
in ker E_P, while U_(R_0) intersects that kernel only in zero. The altered
world therefore has task-span rank r+1 with the identical recorded data.
With T<=r, rank<=r is automatic, so that rank-violation example does not
apply. These alternative worlds must not be ruled out by calling R an
observed universal law. A dense/heterogeneous old source is not silently
removed; it can make the proposed family inconsistent or make its future
completeness fail.

## 4. Reuse before R is unique: acquire the target quotient, not all of R

For a new source f first acquire its actual profile a=E_P f. The family of
candidate functions compatible with (2) is

    F(a)=psi^T a + k^T R_0 a + {k^T Delta R a: Delta R in K}.

Compute the native coefficient subspace V_a=K a in F_p^m and its actual
dimension s(a). This is paid matrix algebra on acquired constraints. If s=0
the old evidence already gives a complete function for this profile, despite
possibly leaving much of R unknown. If s>0, construct s native points whose
evaluation matrix on k^T V_a has full rank, using actual known feature
evaluations on Z and exact row selection. Query f at these points and solve
for the unique candidate in F(a). Anchor values are already fixed; points in
P give zero rows and cannot be falsely counted as informative.

This uses r+s(a) target values, before guards. Once a and family F(a) are
fixed, s(a) is also the sharp worst-case number of *additional* field-valued
native answers needed to identify its member: the family has p^s distinct
functions, while an adaptive q-answer tree has only p^q leaves. Uniform
input gives success <=p^(q-s) when q<s. This is not a global r+s lower bound
for learners allowed a different joint/interleaved policy; the earlier
coefficient-first query tax remains a warning against that inference.

If the new source really lies in one of the common graphs in (2), this fit
recovers it. Otherwise the fit is a proposal. Fresh independent native
guards against a declared valid H disagreement bound may validate it or
return UNKNOWN. For degree<=D native polynomials, a fixed false candidate
passes q new uniform F_p^n probes with probability <=(D/p)^q. This remains
true even if no common old world exists: soundness is checked on the actual
new source, not inferred from an unrecognized rank promise. No old replay
tape instantiates these fresh guards.

On a successful exact branch, retaining the whole fitted native program
permits the reusable update R a=b, reducing K by exactly s(a) dimensions.
Correctness of any probabilistically validated update needs the allocated
whole-lifetime first-error budget; an accepted wrong program can poison later
constraints. Arbitrary incompatible new tasks may instead be rejected or
handled by a separately paid generic fallback. Neither option is free.

## 5. Amortized accepted-task acquisition without old oracle persistence

Let the retained training equations leave K_0 of dimension d_0. For each
subsequent target apply the preceding profile-conditioned acquisition and
validation. If a candidate is accepted correctly, retain its exact native
function and add R a=b. Rank-nullity gives

    dim K_next = dim K_current - dim(K_current a)
               = dim K_current - s(a).                     (3)

Consequently the SUM of additional fitting answers s(a) over all correctly
accepted tasks is at most d_0, even if R is never fully identified. For A
accepted targets the fitting cost is at most

    r A + d_0,

plus their real guards. Each accepted target has a closed native program;
there are no deferred calls to an expired source. This is a conditional
potential bound on the actual learned procedure family, not a promise that
an arbitrary stream will be accepted.

The result does not require asserting a true common-rank world in advance.
Every constructed candidate belongs to the current F(a), so its exact
function is compatible with at least one current R. Adding a correctly
accepted candidate therefore leaves a nonempty family and decreases its
dimension by (3). The class-completeness hypothesis matters for how many
real targets pass. A candidate outside the actual source will be rejected
except within its allocated error budget. On the simultaneous no-false-accept
event the same accounting holds, even in a heterogeneous world.

Rejected trials remain paid: a rejected target can consume r+s(a)+q native
values without reducing K, and this work must be added separately. There is
no bound on the number of such trials or on useful future coverage. The
source-query theorem must not be reported as an unconditional success or
total-lifetime advantage for an arbitrary source sequence.

If the initial training contains E_0 actual extra observations with design
rank h_0, then d_0=mr-h_0. Its rT_0+E_0 paid values plus accepted-target fit
cost obey the explicit accounting

    r(T_0+A) + mr + (E_0-h_0),

before guards and rejected trials. The term E_0-h_0 exposes duplicate/useless
training work. Earlier experience prepays actual independent constraints;
it does not remove the information needed to identify a procedure. The
common native envelope, cardinal-feature compilation, matrix-family
selection, linear algebra and future program evaluation are still paid.

## 6. Real cost and next challenges

The representation unknowns number r(M-r), not zero. The one-extra policy
needs at least that many scalar extra constraints to identify arbitrary R
after actual anchor profiles are known; (1) provides an exact rank test and
can attain this dimension when coverage permits. All r anchor values of
every trial and all useless trials remain charged. A simple full-row
completion uses at least r(M-r) episodes and r(r+1)(M-r) native values.
This can cost substantially MORE than completing r persistent basis tasks;
the gain here is feasibility under expiration/per-source caps, not an
unearned total-query victory.

Dense R-family storage/linear algebra can cost polynomially in mr with large
constants, and feature evaluation, Z construction, rank tests, arithmetic
precision and synthesized g_l evaluation are all additional. Retaining an
affine K of high dimension can itself be expensive; cap it and return
UNKNOWN rather than call it a cheap learner. No useful exposure rate, cheap
latent sampler, nonlinear task generator or source-reset ability is inferred.

Closest incumbent must be given the same partial records, anchor policy,
native features, finite source access and computation. An ordinary
multi-task/subspace-completion learner can plausibly implement (1)--(2).
The substantive question is whether the profile-conditioned quotient and
actual experiment-rank compiler change its interface or merely instantiate
that conventional operation. The next primary check will decide that before
any implementation or favorable numerical source is chosen.

## 7. Primary comparison after construction

Pimentel-Alarcon, Boston and Nowak's *Deterministic Conditions for Subspace
Identifiability from Incomplete Sampling* has a direct common-anchor pattern
in Theorem1/Example2. Its main input is projected subspaces; Corollary2 and
its proof explicitly recover those projections from repeated incomplete
columns. Thus the separate-row completion above is a concrete special case
of established subspace recovery, with measured finite-field ranks replacing
their genericity assumptions. [Primary paper](https://arxiv.org/pdf/1410.0633).

Pimentel-Alarcon and Nowak's *The Information-Theoretic Requirements of
Subspace Clustering with Missing Data*, Sections2--4, already treats
individual incomplete columns, explains the extra-observation constraint
count, and gives false-subspace examples. Theorem2 has generic real-subspace
and sampling assumptions; it must not be imported as a finite-field or
open-world certificate. Its conventional recovery viewpoint can adopt the
explicit R-family/linear-objective compiler here.
[Primary paper](https://proceedings.mlr.press/v48/pimentel-alarcon16.pdf).

The useful retained result is paid profile-conditioned acquisition and its
exact family-dimension accounting, not a new claim to invent subspace
recovery. A separate follow-on, `GUARDED_PROCEDURE_FAMILY.md`, drops the
assumption that actual sources are in H for selective distributional
accuracy; its coverage and computational limitations remain explicit.
