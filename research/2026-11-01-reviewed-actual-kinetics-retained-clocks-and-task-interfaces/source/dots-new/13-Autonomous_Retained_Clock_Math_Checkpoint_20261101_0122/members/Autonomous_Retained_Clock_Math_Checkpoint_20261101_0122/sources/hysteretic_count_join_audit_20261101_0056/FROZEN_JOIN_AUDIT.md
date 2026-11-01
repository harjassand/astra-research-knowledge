# Independent audit: frozen hysteretic sampled-path join

Date: 2026-11-01. Auditor: `producer-workspace/audit_sampled_clock_process`.

Frozen source:
`sampled_clock_process_pending_20261101/HYSTERETIC_PATH_COUPLING_ROOT.md`.
SHA-256:
`28afdb7a36927f4f2cca01727274edef91c7ac4d4d27acb5aaf4d88f40be376d`.
Source unchanged. See `COUNT_IDENTITY_PROOF.md` for the separately conditional
stationary count identity; this audit does not assume the unfinished concrete
global current/augmentation construction has passed.

## Verdict

**PASS: the displayed conditional-A finite-horizon jump-matching coupling and its
constants.** This receives the stated scalar/vector bounds, stationary intensity
upper bound, actual augmented stationary law, and domination of the initialized
full future path. It does not earn those concrete premises. No continuous-record
TV claim follows, and none is made by this frozen source.

Two scope qualifications:

1. The claimed epsilon^(1/4) vanishing limit assumes R stays bounded, and
   v(epsilon)=O(sqrt(epsilon)). Both displayed choices of v have this property,
   and the symmetric conditional-A case has R=2/(1-s), hence bounded as s->0.
   With an arbitrary parameter-dependent R tending to infinity, the same
   conclusion is not automatic.
2. A comparison chain initialized with the Z law is not automatically
   initialized with the L law. Section 8 below supplies an explicit
   auxiliary-initial-label symmetry argument that earns the source's general
   parenthetical with R(n+1)s and the actual initial L law. No additional Rs
   is needed, but the construction uses symmetry of this comparison chain;
   simply forgetting the initial-label distinction would not be a proof.

## 1. Correlation replacement and odd-flip bound

Because psi is +1 on A, -1 on B, lies in [-1,1], and Z=sign(psi),

    |Z-psi| <= 1_S,    ||Z-psi||_2 <= sqrt(s).

The constant is 1, not the generic slab constant 2. In particular,

    |E Z_0 Z_Delta-E psi(X_0)psi(X_Delta)|
      <= E|Z_0-psi(X_0)|+E|Z_Delta-psi(X_Delta)|
      <= 2s

by base stationarity. Since Npsi<=1 and r+epsilon>=0,

    E Z_0 Z_Delta <= Npsi(r+epsilon)+2s <= r+epsilon+2s.

Thus P(Z_0!=Z_Delta)>=(1-r-epsilon)/2-s. The L and Z labels agree off S at
each endpoint, so their odd-flip probabilities differ by at most 2s. Therefore

    P(L_0!=L_Delta) >= (1-r-epsilon)/2-3s.

This remains a valid lower bound when its right side is negative.

## 2. Intensity normalization and cluster bound

With x=k Delta/2, the received intensity upper bound gives

    E N_Delta <= (1-s)x.

For symmetric unnormalized basin masses M,
`1-s=2M/Ztot` and `k=2C0/M`. Therefore

    (1-s)k/2 = 2C0/Ztot.

The separately earned identity `E N_t=2cap_m t/Ztot` and trial bound
cap_m<=C0 imply exactly the claimed intensity inequality, with no factor-of-two
error. The count identity and cap/current certificate must remain separately
received.

The elementary inequality `1-exp(-2x)>=2x-2x^2` and the odd-flip estimate give

    E N_Delta-P(N_Delta odd)
      <= (1-s)x-(1-r-epsilon)/2+3s
      <= x^2-sx+epsilon/2+3s
      <= x^2+epsilon/2+3s.

Using the integer count inequality yields precisely

    P_stationary(N_Delta>=2) <= (x^2+epsilon/2+3s)/2.

No independence assumption occurs. Stationary augmentation makes the same
bound available for every translated deterministic bin.

## 3. Actual initial law, grid theorem, and slab charge

Domination of the augmented initial law by R times its stationary law induces
the same domination of the entire future-path law, since both use the same
conditional future-path kernels. Its X marginal is dominated by R pi and evolves
with the actual base semigroup. Thus the accepted state-label path theorem
applies to the actual Z grid without reset or history-conditional mixing.

The trial/vector triangle inequality gives

    d=sqrt(Npsi) v(epsilon)+(1+r)sqrt(s).

Consequently the displayed uniform-step path Pinsker bound is

    delta_grid=min(1,sqrt(R n d^2/[2(1-r^2)])).

Under exact conditional-A initialization, L_0=Z_0=+1. At each later grid point
the mismatch probability is at most the marginal slab probability, bounded by
R s. Hence a union bound over the n later grid times costs R n s, not an omitted
initial-time term. For a general initial law the simple mismatch bound uses
R(n+1)s; matching the comparison initial law must then be treated explicitly.

## 4. Actual and comparison multiple jumps are both charged

Apply full-path domination to the stationary union of n actual cluster events:

    P_actual(any bin has >=2 transitions)
      <= R n (x^2+epsilon/2+3s)/2.

This does not assert the stationary count equality under conditioned
initialization. The R factor is applied to an entire stationary bad event.

A symmetric two-state CTMC with correlation decay rate k has flip rate k/2.
Its count in a width-Delta bin is Poisson(x), regardless of initial state. Since
`1_{J>=2}<=J(J-1)/2`, its multiple-jump probability is at most x^2/2. A union
bound gives n x^2/2. The separate reference-process charge in the source is
necessary and correct.

## 5. Coupling construction and what timing error means

Diffusion/finite-jump path spaces in this application are standard Borel, so
regular conditional path laws given a finite grid are available. Couple the
actual Z grid to the CTMC grid with mismatch probability at most delta_grid.
Extend this coupling using the actual conditional (X,L) path law given the Z
grid and the CTMC conditional path law given its grid. Their correct path
marginals are preserved.

On the complement of the grid mismatch, actual L/Z mismatch, actual cluster,
and comparison cluster events, the actual retained path and CTMC have the same
initial state and endpoints in every bin and at most one transition each per
bin. Endpoint parity therefore forces their transition counts in each bin to
agree, either both zero or both one. The transitions have the same order and
directions, and each corresponding pair of jump times lies in the same bin,
with absolute difference at most Delta.

Thus the total failure probability is bounded by

    delta_grid + R n s
      + R n (x^2+epsilon/2+3s)/2 + n x^2/2,

capped at 1, exactly as in the frozen source. On successful paths, one can also
construct an increasing piecewise-linear time change matching corresponding
jump times and fixed endpoints, with uniform displacement at most Delta. This
does not claim equality of the real jump times, equality of holding times, or
TV closeness of their exact continuous-time laws.

Deterministic-bin endpoint jumps need consistent conventions and no uncharged
atoms. The stationary finite-intensity count theorem gives zero probability of
a jump at any fixed time; domination preserves this for conditional-A starts.
The CTMC also has no such atoms. This supplies a route to the source's stated
endpoint premise without a new numerical experiment.

## 6. Scaling check

Suppose H=n x is bounded, R=O(1), s=O(epsilon), and
v(epsilon)=O(sqrt(epsilon)). As x->0,

    d^2=O(epsilon+s),
    delta_grid=O(sqrt(epsilon+s)/x),
    R n s=O(s/x),
    R n (x^2+epsilon+s)=O(x+(epsilon+s)/x),
    n x^2=O(x).

Taking x of order epsilon^(1/4) makes the total failure O(epsilon^(1/4)) and
the scaled timing error `k Delta=2x` vanish. The unscaled mesh
`Delta=2x/k` need not vanish if k itself tends to zero; the frozen source correctly
says scaled timing error. No unbounded mean-passage-time conclusion follows.

## 7. Computational scope and remaining obligations

The corrected O(nJ) finite-accumulator arithmetic bound, plus precision costs,
is appropriately stated. A bounded real-valued range is not treated as fixed
finite state count. The analytical formulas do not require simulating a rare
trajectory solely to evaluate them; this is not a promise that acquiring their
actual inputs or proving global model validity is cheap.

**Action/target/reason/outcome for open concrete obligations:** receive the actual
stationary augmentation, global committor/current/intensity certificate, trial
scalar/vector certificate, preparation domination, and outward numeric
enclosures / target the author's separate concrete construction / because this
join is conditional and cannot manufacture those premises / the finite-horizon
conditional-A theorem passes, while the concrete construction remains unapproved
by this audit.

No helper agents, external retrieval, source mutation, numerical substitute for
proof, permission denial, or retry occurred.

## 8. General initial law: explicit matching-label coupling without extra slab cost

This argument completes the matching-initial-label receipt for the symmetric
comparison chain. Retain the auxiliary initial mark M=L_0 along with the actual
raw-label record `(Z_0,...,Z_n)`. In the comparison law keep the SAME joint
initial distribution of `(M,Z_0)` and use the usual symmetric transition Q_i for
Z, independent of M given the current Z.

The accepted entropy proof works unchanged with histories enlarged to include
M. The future X transition still uses P_Delta conditional on the current full
state, the vector error is the same, and conditional Jensen still averages to
the same actual deterministic-time marginal. There is no initial KL term
because the whole initial pair has the same joint law. Thus

    KL(actual (M,Z-grid) || comparison (M,Q-grid))
       <= R n d^2/(1-r^2).

Conditional maximal coupling given the common initial pair preserves that pair
exactly, with total mismatch probability bounded by the same delta_grid. Complete
the comparison grid to its actual symmetric CTMC law and call that path Q_t,
so Q_0=Z_0. Define the new comparison path

    Y_t = M Z_0 Q_t.

It starts at M. Given any initial pair (M,Z_0), global sign symmetry of the CTMC
makes Y have exactly the CTMC law started at M, independent of Z_0. Consequently
its unconditional law is the correct CTMC initialized with the actual L_0 law.

On the event L_0=Z_0 the sign multiplier is 1, so this transformation makes no
change at all. On the complementary event the already charged L/Z grid-mismatch
event occurs at time zero; it is included in R(n+1)s. On the complement of that
grid-mismatch event and the entropy-coupling failure, the full L grid therefore
matches the new Y grid. Multiplying a CTMC path by a constant sign does not
change its jump count, so the reference cluster bound is unchanged.

This proves the same finite-horizon jump-matching result for a general dominated
augmented initial law, replacing R n s by R(n+1)s, with the comparison chain's
initial law exactly equal to the actual L_0 law. It does not require a new density
bound after conditioning on M, and it charges no unproved initial independence.
