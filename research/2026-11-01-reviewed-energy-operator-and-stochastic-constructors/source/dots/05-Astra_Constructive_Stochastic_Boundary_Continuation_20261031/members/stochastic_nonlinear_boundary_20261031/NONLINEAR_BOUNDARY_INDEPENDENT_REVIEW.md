# Independent hostile review: nonlinear boundary activation

## Status and frozen objects

**ACCEPTED at the exact frozen versions below.** The whole mathematical proof,
byte-identical source replay, and independent finite-certificate challenges pass.
No substantive correction was needed. Acceptance is restricted to the stated
raw architecture and is not inherited from the earlier affine-core packages.

Reviewed, immutable parent objects:

| Object | SHA-256 |
|---|---|
| `NONLINEAR_BOUNDARY_THEOREM.md` | `86f86f243ac1190b3d4e2843860d0f5b8b14526174eab9e67eade7ddfa20ba62` |
| `nonlinear_boundary.py` | `3c9c9bab1de5e6376bee955f77c1e1541419200c70990268765194ec2063d236` |
| `results.json` | `62d883153dda5f50d51b06134b445519e8c61e2f5311a4d109d90b469936cbb3` |

Copies are in `independent_audit/frozen_*`. Running the frozen constructor
reproduced the frozen JSON byte-for-byte. The independent verifier also accepted
the frozen JSON directly, rather than only live constructor objects. The
reviewer did not edit the parent construction or prior accepted packages.

## Mathematical audit

### 1. Nonlinear weights and standalone nonexplosion

The linear equations acquire a useful vector; they are not falsely asserted to
be the dynamics of independent particles in the nonlinear process. For inactive
i, the actual linear conversion/death matrix satisfies `(Qv)_i=-1-d_i L<=-1`;
for hubs the choice of L gives the same inequality. Consequently q_i>=T and all
hub weights equal T.

For the actual pair `2Y_i <-> 3Y_i`, the exact exponential quotient factors are
`q_i r/(r+c)-1` and `q_i^(-1)(1+c/(r-1))-1`. At the acquired radial threshold the
second is at most `-(q_i-1)/(2q_i)`, while the first is at most q_i-1. Thus the
pair's upper bound is exactly

    A_i n(n-1) - B_i n(n-1)(n-2).

It is nonpositive for n>=ceil(2+A_i/B_i); enumerating smaller integers plus zero
is a genuine finite global maximum certificate. This includes every added core
reaction; no nonlinear channel is dropped as a favorable approximation.

The core Lyapunov tail is proved before the activation clock. Since c<=1,
g(r)>=1/r, the core function is normlike. Its generator has a finite global
linear upper bound, so stopped sublevel arguments prove standalone core
nonexplosion. This closes the potential circularity in using stopped Dynkin for
the bounded clock function.

### 2. Bounded return and a genuinely acquired activation clock

For W=r/(r+1), the exact increment denominators are
`(r+1)(r+2)` upward and `r(r+1)` downward. At a hub-empty state,

    sum (y_i)_3 = sum y_i^3 - 3 sum y_i^2 + 2r
                  >= r^3/ell^2 - 3r^2
                  >= r^3/(2ell^2),  r>=6ell^2.

Quadratic births contribute at most kappa_max, immigration at most Lambda,
linear deaths are nonpositive, and conversions preserve r. Using r+1<=2r
gives the claimed `Lambda+kappa_max-mu_min*r/(4ell^2)` upper bound. The generic
K_clock therefore certifies drift <=-1 outside the finite clock head.
Localized stopped Dynkin yields expected time <=W(initial)<1 until either head
entry or hub activation. Nonexplosion was independently established above.

Finite-clock success is not an oracle. Strong connectivity provides a finite
monomolecular event word activating a hub, while remaining below the clock
radius: follow one existing particle toward zero; either a hub is reached
earlier, or its death frees one place for an immigration/conversion path to a
hub. From zero this uses only one service particle. Each word has positive
probability despite competing nonlinear channels, because all its states have
finite rates. The finite killed matrix is transient and its activation
probabilities are strictly positive.

The verifier reconstructs the killed matrix and activation-rate right-hand side
from raw reactions, verifies **both** rational linear systems, and checks the
minimum probability and maximum mean. No supplied t/p values are trusted.
The renewal bound is valid uniformly, including starts outside the head: group
each cycle as an initial return-or-activation segment (mean <=1) followed, if
needed, by a head exit (mean <=t_max). Conditional failure probability is at most
1-p_min. Truncating the number of cycles and summing geometric tails proves
`E tau_H <= (1+t_max)/p_min` without assuming this expectation finite first.
The earlier independent-immigrant argument would be invalid here and is not
used.

### 3. Dirichlet patch, one-sided excess, and cubic leakage

All head equations use the actual nonlinear core. Subtracting the base boundary
value produces `(-Q_R)w_R=1+L_core h0` with zero exit values. The acquired forcing
radius makes the positive part vanish beyond a finite set: the core quotient is
<=-1 there and h0>=1. A positive finite killed resolvent, and exit before hub
activation, give the **one-sided** bound `w_R<=M*C_act` uniformly in R. No lower
bound on w_R is needed.

Both added nonlinear channels change r by one and leave all hub counts fixed.
The only newly dangerous outside entrances into the inactive head are therefore
cubic deaths at r=R. Their total intensity is at most mu_max R^3; linear deaths
add at most d_I R. Exponential `T^R g(R)` dominates this polynomial leakage.
The recorded monotonicity test is correct:

    [T^(r+1) g(r+1)/(r+1)^3] / [T^r g(r)/r^3]
       = T [r/(r+c)] [r/(r+1)]^3.

Both r-dependent factors increase. The scalar witness is only a sufficient tail
witness, not a hidden substitute for the actual head search or its costs.

The implementation accepts only after checking every inactive composition at
r=R. Active states with 1<=r<=R are covered separately, including r=1. Star
reactions never enter the hub-empty patch, and complete positive hub rows give
a strictly negative coefficient for **each** satellite coordinate. Neutral
reactions preserve V exactly, even at arbitrarily high order.

### 4. Full-chain recurrence and stationary moments

The four regions (head, inactive fringe, finite active service layers, tail)
exhaust the state space. Positive head coefficients and exponential growth
outside make V normlike. Its global Foster bound gives nonexplosion even with
high-order neutral jumps: bounded V-sublevels contain finitely many count
states and therefore have bounded total rates. Finite-set return and the
weak-reversibility communication paths then imply classwise positive
recurrence.

The moment conclusion does not illegally assume pi(V)<infinity. From stopped
exponential Dynkin, `P_t V<=aV+b` with a<1. Invariance and concavity imply
`pi min(V,n)<=pi min(aV+b,n)`. The difference of these two truncations is bounded
below by -b; Fatou yields `(1-a)pi V<=b`. A fixed T controls exponents strictly
below log T. Arbitrary finite exponential moments follow by a new terminating
mathematical construction for each larger rational T, not by pretending that
one executed T=2 certificate controls all exponents.

## Independent computational evidence

`verify_nonlinear.py` independently derives raw partition compatibility,
monomolecular connectivity, both restoring rates for every inactive phase,
linear weight equations, nonlinear polynomial maxima, tail constants, head
equations, complete fringe coverage, the actual clock matrix and both solutions,
forcing support, one-sided excess, scalar radius, all active layer coefficients,
and the full original generator. Its verification does not call the submitted
`recognize`, `construct`, `solve`, `value`, or `generator`; the constructor is used
only to propose receipts.

Seven cases passed, totaling **3,080** additional exact full-generator
states (separate from the original 420):

| Case | T | R | Head states | Active service rows | Exact states |
|---|---:|---:|---:|---:|---:|
| Original nonlinear example | 2 | 4 | 4 | 30 | 336 |
| Larger exponential base | 4 | 4 | 4 | 30 | 336 |
| Smaller exponential base | 3/2 | 4 | 4 | 30 | 336 |
| Unequal hubs and return to inactive phase | 2 | 3 | 3 | 16 | 224 |
| Two satellites and degree-seven neutral pair | 2 | 4 | 4 | 30 | 1,008 |
| Permuted species / reacquired roles | 2 | 4 | 4 | 30 | 336 |
| Two nonlinear inactive phases | 2 | 3 | 6 | 25 | 504 |

The two-inactive-phase case in `two_inactive_challenge.py` really executes the
dimension-dependent generic construction: K_clock=24, a 300-state killed clock,
and two exact 300-dimensional systems. The complete resulting certificate is
independently verified before testing its full generator. Its successful head
has only six states; the much larger acquisition clock is not hidden. Solved
clock fractions reach 4,769 bits. Construction, verification, and full-generator
checks took about 340 seconds in this execution (an observation, not a bound).
A budget of 299 gives UNKNOWN for this required 300-state clock.

An additional **2,401** exact inactive compositions at total counts 24 through72
verify the dimension-sensitive falling-factorial estimate and the actual W
drift <=-1. The smallest observed Jensen slack is912. These radial checks are
not counted as full-generator state tests and do not replace the all-r proof.

The verifier rejected altered clock probabilities, exit means, clock radius,
nonlinear tail bound, fringe coverage, forcing bound, and head value. Raw
weakly reversible mutations were rejected for a missing inactive restoring pair,
a restoring pair on a hub, and a hub lacking direct death. A clock budget of 5
returns UNKNOWN for the required 6-state system. A head budget of 2 preserves
the failed first solve, then returns UNKNOWN at the required 4-state patch.

A separate independent Gaussian elimination reconstructs the R=2 patch and its
positive quotient `2775046/4141725` at 2A. This holds along the whole satellite
ray, so no finite global additive Foster constant can repair that particular
patch. It is a genuine failure of the first proposed Lyapunov function, not a
claim of instability of the chain.

### Optional sharp radial evidence, not a change to the generic constructor

For one inactive phase, exact W drift is

    [Lambda+kappa*r(r-1)]/[(r+1)(r+2)]
      -[d+mu*(r-1)(r-2)]/(r+1).

For the demo rates, multiplying LW+1 by the positive denominator yields

    P(r)=(-100r^3+111r^2+419r-399)/10.

P(2)=83/10>0, P(3)=-843/10<0. Its forward difference is
`(-300r^2-78r+430)/10`, negative and decreasing for r>=2. Therefore K=3 is the
smallest threshold for this exact radial test. An independently solved 3-state
clock gives `C_act=21273/1240`. This is optional diagnostic evidence only; the
frozen constructor and its accepted receipts retain generic K=6.

## Retained scope and accounting

No general weak-reversibility, historical novelty, or operational claim is
accepted. The theorem still requires the strongly connected monomolecular
subcore, positive direct hub deaths, complete satellite rows, and a positive
2-to-3 / 3-to-2 restoring pair for every inactive phase. Extra arbitrary nonlinear
service reactions are not covered.

The nonlinear example's non-complex-balance and non-strong-endotacticity
comparisons check algebraically. They exclude those immediate shortcuts, not
all existing recurrence theorems or the possibility of prior art. The tools
(bounded-return drift, finite killed chains, geometric trials, Foster estimates)
are conventional; the paid compatibility composition is what this audit checks.

Clock and head budgets are separate, and neither is a bound on every operation:
nonlinear maximum enumeration, forcing enumeration, scalar-radius acquisition,
raw partition search, exact matrix arithmetic, and failed trials also cost work.
Reported fraction sizes are sizes of the final solved values, not a measured
maximum over every intermediate elimination numerator and denominator. Dense
exact solves can be expensive even when the successful patch is small. This is
not a polynomial-time algorithm or a full universal resource certificate.

## Verdict

Accepted: the actual finite clock is acquired without particle-lineage
factorization, the nonlinear Dirichlet excess is uniformly controlled, and the
finite collar search terminates under the exact stated structural assumptions.
The frozen original example, its failed first patch, nonlinear/dimensional
challenges, and honest UNKNOWN outcomes are all supported by ordinary exact
receipts in `independent_audit/`. No simulation is used as recurrence evidence.
The separate protected-token proposal is **not** reviewed or accepted by this
receipt and makes no change to these frozen objects.
