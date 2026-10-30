# Exact heralding requires complete latent-sector coverage

30 October 2026. Root construction following the completed positive feedback
cell. This is a new internal theorem candidate until its separate whole
challenge is consumed. It is an EXACT-output obstruction, not an improved
constant-error approximate-recovery lower bound or a historical-priority claim.

## 1. Model and theorem

Fix k>=2, r>=2 and d=kr. Restrict the native source to the full-dimensional
subfamily

    N_U(X)=U(X tensor I_r/r)U*,      U in U(d).

Write U_j x=U(x tensor |j>) for its r mutually orthogonal k-column blocks.
Neither j nor the environment is supplied to the controller. Allow arbitrary
definite-order adaptive/entangled FORWARD calls, known controls, instruments,
ancillas and storage. The single payload is already N_U(rho), with arbitrary
reference. Count ALL native calls used for programme acquisition and during
decoding; the original payload preparation is separate. Initially supplied
U-dependent advice, controlled unknown dilations and inverse calls are absent.

A heralded success is exact when its *unnormalized* logical subchannel is

    S_U(N_U(X))=p_U X                         for every X.       (H1)

The scalar p_U can depend on U. Requiring exact normalized success for every
state/reference already forces a state-independent scalar: a completely
positive map whose Choi output is supported on the identity Bell ray has
exactly the form(H1). A failure output may retain arbitrary history. There
is no assumption that the failure is restoring or that the payload precedes
every queried channel.

For an algorithm using at most Q native calls, let

    c_r(Q)=r! S(Q,r)/r^Q

be the probability that Q independent uniform draws cover all r labels.
The convention is c_r(Q)=0 for Q<r.

**Claim. Every such exact success satisfies p_U<=c_r(Q), for EVERY U.**
In particular no nonzero exact heralded inverse exists with Q<r. For any
fixed alpha in(0,1), a uniformly alpha-successful exact inverse requires
Q=Omega(r log r), more explicitly

    Q >= log[alpha*r/(1-alpha)] / [-log(1-1/r)]              (H2)

when the numerator is positive. For alpha=1/2 this gives
Q>=(r-1)log r. An exact repeat-until-success algorithm that halts almost
surely has expected query count at least r H_r. The sharper possible
2r-1 threshold suggested by the exterior construction is NOT proved here.

## 2. Rank-one Choi output resolves every positive branch

Expand each forward call using its exact Kraus decomposition

    N_U(X)=(1/r) sum_j U_j X U_j*.

These are fresh independent uniform labels, regardless of the input or
entanglement. They are a mathematical decomposition, not accessible flags.
Fix the query-label tuple q=(q_1,...,q_Q), and a known-control Stinespring
environment/measurement branch h. The resulting success Kraus map from
the physical payload to the logical output is R_qh(U). Its entries are
HOLomorphic polynomials of degree Q in entries of the queried blocks U_qt.
Known gates and unnormalized measurement Kraus operators contribute fixed
coefficients. There is no U* in an amplitude: conjugates occur only when
forming the density operator. Adaptive Born normalization must not be
inserted into a fixed unnormalized Kraus branch.

Finite-dimensional finite-query instruments admit finite-dimensional comb
and Kraus realizations, so unrestricted known CPTP preprocessing is covered;
no bounded-memory or iid-programme ansatz is used. Classical finite branch
choices can be deferred. Padding a capped algorithm with discarded calls
gives a fixed Q without increasing success probability.

Including payload label j, the success channel in(H1) has Kraus matrices

    r^[-(Q+1)/2] R_qh(U) U_j.

Its Choi matrix is p_U |Omega_k><Omega_k|, a positive rank-one matrix.
Every positive summand must have that same support. Therefore, for EVERY
q,h,j and unitary U,

    R_qh(U) U_j = a_qhj(U) I_k.                           (H3)

No cancellation between wrong positive branches can enforce exact success.

## 3. An unused block makes the entire branch vanish

Suppose label l never occurs in q. Then R=R_qh is independent of every
entry of U_l. Replace U by U R_l(V), where R_l(V) acts as an arbitrary
known-in-the-proof V in U(k) on block l and as identity on all other
blocks. This preserves unitarity, leaves all queried isometries unchanged,
and changes only U_l to U_l V. Equation(H3) consequently implies

    a_qhl(U) V = a_qhl(U R_l(V)) I_k.

Choose a nonscalar V. Since k>=2 this forces a_qhl(U)=0. Hence

    R_qh(U) U_l=0                for EVERY U in U(d).      (H4)

Now apply polynomial density, with its precise proof included. If a complex
polynomial P in d-by-d matrix entries vanishes on U(d), fix a unitary W
and any Hermitian H. The entire function z -> P(W exp(zH)) vanishes on
the imaginary axis, hence everywhere. In particular it vanishes at z=1.
Polar decomposition writes EVERY invertible complex matrix as W exp(H).
Thus P vanishes on GL(d,C), and therefore identically on all matrices.

Apply this entrywise to the polynomial matrix R(M) M_l in(H4). It is zero
for EVERY complex matrix M, with no remaining orthogonality constraint.
Because R is independent of M_l, one can vary those k columns arbitrarily
while holding every queried column fixed. Thus R(M)=0 identically.

This is stronger than merely declaring success impossible when the datum
label was unseen: the ENTIRE fixed query branch is zero if ANY one of the
r source labels was absent, including when the datum label was seen.
The crucial extra step is the holomorphic extension off the unitary locus.
It would be invalid with supplied U* calls or U-dependent initial advice.

## 4. Coverage bounds, capped and variable length

All non-covering query tuples have zero success Kraus matrices. Each fixed
query tuple, with its uniform scalar weight removed, specifies an ordinary
isometric-source circuit with known instruments. Its conditional success
probability is at most one. Summing its original probability r^-Q over
the covering tuples yields p_U<=c_r(Q), uniformly in U and payload.

For a transparent necessary bound, let Z count missing labels after Q
uniform draws, and mu=E Z=r(1-1/r)^Q. Then

    E Z^2=mu+r(r-1)(1-2/r)^Q <= mu+mu^2.

Cauchy--Schwarz on Z 1_{Z>0} gives

    Pr(Z>0)>=mu^2/E Z^2>=mu/(1+mu),
    c_r(Q)<=1/(1+mu).

Combining alpha<=p_U<=c_r(Q) proves(H2). Since
-log(1-1/r)<=1/(r-1), the stated alpha=1/2 simplification follows.
This elementary moment bound is sufficient; no independence of the
empty-bin events or sharper coupon asymptotics is presumed.

For a variable-length exact algorithm, partition the success instrument by
its finite stopping time. Positivity of the total exact Choi output makes
each finite-time success component exact. The same fixed-branch proof
applies at each stopping prefix. Couple all native calls to an infinite
sequence of iid uniform labels, extending it after a stop if necessary.
There is zero success probability before their first complete coverage
time tau_r. If the algorithm succeeds almost surely, Q_stop>=tau_r on
this joint experiment, so

    E Q_stop >= E tau_r
             = sum_(m=0)^(r-1) r/(r-m) = r H_r.           (H5)

The expectation can be infinite. No finite worst-case exact deterministic
inverse follows. Nontermination with positive probability is not an
almost-sure success service and is not covered by(H5)'s conclusion.

## 5. The actual change in the scalable search

The earlier received N1104 collision theorem already supplies
Omega(r log(1/epsilon)) for uniform approximate decoding and excludes
finite exact deterministic decoding. Those are NOT new conclusions here.
The coverage result concerns EXACT heralding, for which the earlier
throughput bound allowed a positive success even below r queries.

It excludes a fresh, memoryless constant-query exact success-or-draw cell
at arbitrarily large r, even if one hopes to repeat it many times. A
history-retaining construction can still become successful after enough
queries and might attain r log r expected cost. This is close to linear
up to a logarithm, and remains potentially much better than the present
quadratic source-to-reflection route. It is not constructed by this theorem.

No quantitative approximate-error version of the polynomial-zero argument
is claimed. The two-query adaptive cell is approximate and remains valid.
The all-r inverse at O(r), or O(r log r), queries with useful error remains
OPEN. Its successful operation can use coherent growing history, tolerate
small success error, or exploit a different permitted mechanism.

The ordinary pure-unitary success-or-draw predecessor
Quintino--Dong--Shimbo--Soeda--Murao, PRL123,210502(2019), already proves
the separate d-1 threshold for exact probabilistic inversion of a FULL
unknown d-dimensional unitary. That cannot simply be identified with this
discarded-junk subsystem task. The exterior-hole positive construction in
C_FIRST_OPERATION.md uses2r-1 queries and succeeds with a small nonzero
probability. It is consistent with the present necessary condition and
does not acquire a restoring failure.

All steps here are mathematical. No source, solver, quantum circuit,
cryptographic instance or physical experiment was run. Public priority of
this particular coverage argument is UNKNOWN; independent whole challenge
is recorded separately when actually completed.
