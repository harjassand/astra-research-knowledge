# Preparation from stationary fluctuations and retained physical memory

29 October 2026. Astra P1 root construction. Earlier files are unchanged.

## 1. Question and predecessor boundary

The bounded stationary counter does not prepare its invariant law from the
baseline. This continuation asks what physical resource upgrades invariance
to actual preparation on one persistent specimen, without learning hidden
dynamics. The independently selected fixed-clock flow construction is retained
as a real alternative. After reading it and its strong existing probability-
flow predecessors, root selected preparation as the central investigation.

Palm transport, Liggett's extra-head matching, Holroyd–Peres allocations,
Last–Thorisson transports, Mörters–Redl embeddings, and Thorisson's
shift-coupling/Cesaro inequality are established mechanisms. They are NOT
claimed as inventions here. The contribution under investigation is their
physical preparation interface, finite-error resource separation, observable
acquisition, and an actual additional operation that removes the obstruction.
The complementary four-state unknown-kernel theorem is a separate result.

## 2. Actual-state preparation inequality

Let S be an invertible measurable map preserving probability mu on a standard
Borel microscopic space. The actual menu is S and, if supplied, S^(-1).
Starting at X_0~mu, any controller ending at its current state has

    X_out=S^J X_0,       |J|<=K,                              (1)

where K is its total number of native calls. The bound allows arbitrary
sensing, computation, calibration information and randomization, even complete
knowledge of X_0 and S. No other physical action, new specimen, overwrite,
reset or copy is supplied. Forward and inverse calls each have unit cost.

Let nu=g mu, g>=0, mu(g)=1, and TV(Law(X_out),nu)<=epsilon. Define

    F_n=E_mu |sum_(j=0)^(n-1)[g(S^j X_0)-1]|.                 (2)

For every n>=1,

    F_n/2 <= E min(K,n)+n epsilon,
    E K >= sup_n [F_n/2-n epsilon].                         (3)

**Proof.** Put A_n(x)=n^(-1)sum_(j=0)^(n-1)delta_(S^j x).
The orbit windows A_n(x), A_n(S^J x) share at least (n-|J|)_+ entries,
counting multiplicity, so their TV distance is at most min(|J|/n,1).
Averaging the actual endpoint coupling and using mu A_n=mu gives
TV(rho A_n,mu)<=E min(K/n,1), where rho=Law(X_out). Contraction gives
TV(nu A_n,mu)<=epsilon+E min(K/n,1). The density of nu A_n is
n^(-1)sum_j g(S^(-j)x). Stationarity translates this sum into the forward
block sum without requiring time reversibility. Multiplication by n proves
(3). This finite-orbit proof is an instance of the classical shift-coupling
inequality, not a new probability identity. It needs no stopping-time
assumption or finite expected K.

If g is visible, each integrand in (2) is acquired from one chronological
baseline record. With R independent warranted baseline blocks, |g-1|<=A,
and empirical mean bar_F_n, Hoeffding supplies the lower confidence limit

    max{0,bar_F_n-n A sqrt(log(1/delta)/(2R))}                 (4)

with coverage at least 1-delta. Inserting it into (3) yields a measured cost
lower bound. Charge R baseline preparations, Rn reads/calls, and timing.
A correlated stationary trajectory does not automatically give independent
blocks. Exact g and the invertible actuation contract remain structural
premises. Choosing several n needs simultaneous coverage or fresh validation.

## 3. Fair visible bits, costly full microscopic preparation

Let Omega={-1,+1}^Z, mu the fair product law, S left shift, and visible
label xi_0. For fixed 0<a<1 choose the strictly positive target density

    g=1+a xi_0.                                             (5)

Forward visible observations are iid fair bits. The microscopic state stores
the full two-sided sequence; an inverse call, when supplied, can expose the
stored past. With B_n=sum_(j=0)^(n-1)xi_j,

    F_n=a E|B_n|,
    E|B_n|=n binom(n-1,floor((n-1)/2))/2^(n-1)
           ~sqrt(2n/pi).                                    (6)

The exact formula follows by counting paths, or summing
E|B_(n+1)|-E|B_n|=Pr(B_n=0).

**Exact boundary.** Any operation using only S and S^(-1) whose output is
exactly nu has E sqrt(K)=infinity. Otherwise min(K,n)/sqrt(n)<=sqrt(K)
and dominated convergence contradict (3) and (6). This remains true with
known dynamics and complete microscopic sensing.

**Finite-error law.** For controllers of error epsilon->0 and mean cost C,

    liminf epsilon C >= a^2/(8 pi).                         (7)

Use n nearest a^2/(8 pi epsilon^2) in (3). Section 5 constructs the same
1/epsilon mean-cost order. The exact leading constant and the optimal hard
deadline are not claimed. Full-state TV bounds all later physical record
laws by data processing when supplied with the same external policy
information. It does not remove endpoint correlations with preparation logs.

## 4. A causal exact preparator using visible matching

Let (X_j) be a stationary microscopic process with visible signs xi_j.
Require equal sign mass in every stationary component:

    E[xi_0 | I]=0,                                         (8)

where I is its time-shift invariant sigma-field. This permits evolving
hidden memory and conserved parameters. A global one-half marginal alone
does not suffice. The initial stationary law is a real preparation premise.

From the current baseline state: finish if xi_0=+1; if xi_0=-1, finish with
probability 1-a; otherwise continue actual native calls until the first
t>=1 with xi_0+...+xi_t=0. Output the actual current X_t. To require a
positive call on every branch, first execute one stationary native call and
use its endpoint as time zero. At a=1/2 the sole dispatch selector is one
fair bit. General selectors, the unbounded running counter, reads and
decision latency retain their costs.

**Theorem.** The controller terminates almost surely under (8) and outputs

    Law(X_out)=(1+a xi(x))mu(dx).                            (9)

Native reversibility, visible Markov closure and hidden resetting are not
required. The proof is a physical realization of the known Palm matching
mechanism, not a new extra-head theorem.

**Complete matching.** On a two-sided sign sequence match each minus at i
to the first j>i with sum_(k=i)^j xi_k=0. The partner is a plus. Intervals
are nested or disjoint and no plus has two partners. An unmatched minus
cannot have an unmatched plus to its right: the last downward crossing of
the level of that plus gives the plus a partner. Thus, if both unmatched
types existed, the last unmatched plus would be a finite integer. On this
translation-invariant event its distribution would have to be translation
invariant, impossible for a probability on Z. At most one sign is unmatched.
The stationary intensity of matched minuses equals that of matched pluses
by mass transport. On every invariant event (8) makes unmatched intensities
equal; as one is zero both vanish. Countability then gives complete matching
almost surely. Its forward matching time is a stopping time.

**Microscopic, not just sign, law.** Give every time site one unit of source
mass. A plus keeps its unit; a minus keeps 1-a and sends a to its matched
plus. Column masses are 1+a at pluses and 1-a at minuses. For the equivariant
transport k(omega;i,j), shift theta_j of the complete microscopic trajectory,
and any nonnegative measurable F, stationarity and Tonelli give

 E sum_j k(omega;0,j)F(theta_j omega)
   =E F(omega)sum_i k(omega;i,0)
   =E[(1+a xi_0)F(omega)].                                 (10)

The implemented random row is k(omega;0,.). Taking F to depend on X_0 proves
(9). A stationary two-sided extension is a proof object, not an executed
past or a microscopic copy. For a complete Markov native state, subsequent
native evolution starts from the genuine law (9).

## 5. Finite tolerance and finite hidden memory

For iid signs, conditional on dispatch from a minus, let H count further
native calls until the running sum returns from -1 to zero. Ballot counting
gives

 Pr(H=2k+1)=Catalan_k/2^(2k+1),
 q_N:=Pr(H>N)=binom(N,floor(N/2))/2^N.                       (11)

Cap that waiting at N and, on an unfinished branch, output the actual state.
Coupling to the exact process gives

 TV(Law(X_out^N),nu)<=epsilon_N=(a/2)q_N,
 C_N=1+(a/2)sum_(j=0)^(N-1)q_j,       K_N<=N+1.             (12)

The 1 charges the initial native call. Hence

 epsilon_N~a/sqrt(2 pi N),   C_N~a sqrt(2N/pi),
 epsilon_N C_N -> a^2/pi.                                  (13)

Together with (7), this proves the sharp mean-cost order Theta(1/epsilon)
for fixed a at the declared orbit menu. The supplied hard deadline is
O(1/epsilon^2). Conditioning only on finishing before the cap does not give
an exact nu sample; (12) concerns the complete unconditional output.

For a finite counterpart, take a uniformly random balanced cyclic string
of length L=2m, and rotate it. Each orbit has equal sign masses, so nu does
not change conserved orbit weights. The same matching prepares nu exactly
with positive-call cap L and mean

    C_L=1+(a/2)[4^m/binom(2m,m)-1].                         (14)

Indeed, for a uniform balanced bridge its first return length R has
E R=1/Pr(B_(2m)=0)=4^m/binom(2m,m). One derivation uses the return
generating function U(z)=(1-z^2)^(-1/2) and first-return function
F(z)=1-1/U(z): the coefficient of z^(2m) in z F'(z) U(z) equals 1.
Conditional on initial minus the same mean holds by sign symmetry. Additional
native calls after the charged initial step are R-1 on a branch of mass a/2.

For n near L/2 the block sum is hypergeometric with E|B_n| of order sqrt(L),
so (3) forces exact mean cost Omega(a sqrt(L)), even with inverse calls and
full-state knowledge. Formula (14) attains that order. Every fixed-length
forward baseline record approaches iid as L grows. This is not equality of
finite-record laws at each L or an acquired bound on hidden memory length.

## 6. Actual scope and further construction

The initial law and component condition (8) cannot be bootstrapped from the
later invariant counter. If an old record D is retained, conditional use
requires its corresponding stationary baseline/component premise. Completion
time, selector and observed preparation history generally correlate with
the endpoint. A marginal preparation statement does not make them independent.

The orbit lower bound does not cover an action that changes stored orbit
information. SELECTIVE_MEMORY_THERMALIZATION.md supplies and charges such
an action and its full-record scope. The record-geometry complement supplies
a separate four-state unknown-kernel obstruction, including uniform rapid
mixing. Those results have distinct premises; no rates transfer automatically.

Primary sources read: Holroyd–Peres, Ann. Probab. 33 (2005), 31–52,
https://arxiv.org/pdf/math/0306402 (introduction, discrete allocation and
tail statements); Last–Thorisson, Ann. Probab. 37 (2009), 790–813,
https://arxiv.org/pdf/0906.2062 (framework and invariant-field condition);
Mörters–Redl, https://www.mi.uni-koeln.de/~moerters/papers/Shift-revision.pdf
(Theorems 1–4, examples, transport equivalence and proof setup).
The primary author-hosted shift-coupling source is
https://hermann.hi.is/iid/csr/samples/chapter7.pdf; full-book source
https://interacting.math.cnrs.fr/HT_book-1-7.pdf. Read scope and the choice
between constructions are recorded separately. Priority of the complete
physical assembly is not established. N675 is untouched.
