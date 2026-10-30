# Occupation-normalized dormant return: a new joint resolvent profile

30 October 2026. Personal working proof, NOT independently reviewed. The proposed inequality addresses the low-A continuation omitted by ACTUAL_DORMANT_FORCING_INTERFACE.md. It is still a local first-connector statement, not a complete section-cycle recurrence theorem.

## Claim

Use the nonbalanced extension of NONBALANCED_DORMANT_EXTENSION_V1.md, with fixed positive coefficients, a0>=2, m=a0+2. Start active with d>=1, B=b>=q, and set `x=1+A`, `n=a+c+d`. Stop at clearing, first connector birth, or first d=0 entrance. Define

`V=E[(1+A_out)^-m; d=0 entrance]`,
`U=E integral_0^tau A_t dt` (physical time).

The proposed uniform estimate is

`V <= C (b)_q x^-2 U`.                                      (R)

The incoming A is used on the right. The process is NOT stopped when A falls below a fraction of its incoming value. All constants may depend on fixed rates and a0, but not n, composition, or b>=q.

This makes dormant-feedback leakage relative to the actual useful A-occupation small at large incoming A, including paths which revisit low A. In contrast, an unweighted O(n^-delta) return estimate can be much larger than U and is insufficient.

## 1. A denominator that remembers both depletion and growth

For fixed s>=2, put

`D_x=x^3+nd`, `phi_s=x^-s/D_x`.

Choose eta<1 close to one, put `z=1+A+eta c`, and define

`psi_s=z^-s/(z^3+nd)`, `F_s=C1 phi_s+C2 psi_s`.

Since z>=x, `phi_s <= F_s/C1 <= C phi_s` after fixed coefficients are chosen. This last comparison only uses psi_s<=phi_s, not an assumed relationship between c and a. The denominator has an earned interpretation: x^3 is the clearing hazard multiplied by the distance x over which A changes, while nd is the reservoir-driven A-production scale.

The following drift bound is the central technical claim:

`(Q-k0(a)_2)F_s <= -c x^(-s-1)`                          (D)

on all sufficiently large active positive-d shells, with d=0 treated as cemetery value zero. Here Q contains the six fast reactions and no connector jumps. Finite shells may be handled by actual finite-state stopped values and a larger constant, independently of (D).

## 2. Finite-difference verification of the claimed drift

All differences below are finite differences, not diffusion substitutions. For u bounded below by 1+a0, the change of `u^-s/(u^3+nd)` under u->u+1 at fixed d has relative decrement between c_s/u and C_s/u. A decrement of u by one or two has relative increase at most C_s/u whenever enabled. Increasing d decreases the function.

The only potentially harmful denominator change is d->d-1. For d>=2 its relative increase is at most `n/[u^3+n(d-1)]`. If d>=u, combine the exact factor d/(d-1) with `(u/(u+1))^s`, s>=2: simultaneous u->u+1,d->d-1 has a relative decrease at least c_s/u. If d<u and n<=C u, the denominator change is O(1/u^2), hence the same conclusion holds for large u. Remaining bounded u,d,n form a finite set. A transition from d=1 to d=0 is killed and contributes only negatively.

For u=z, we always have n<=C_eta z+d. Thus reactions 2 and 6 (z->z+1,d->d-1) have negative drift of order respectively `ad psi_s/z` and `d(d-1) psi_s/z` outside a fixed finite set. Reactions 3 and 4 change z by respectively `-(1-eta)` and `+(1-eta)`, with fixed d. Choose 1-eta sufficiently small to absorb reaction 3's positive coefficient using reaction 2. This yields

`Q_(2,3,4,6) psi_s <= -c d(a+c+d-1) psi_s/z`.

On active large shells the factor a+c+d-1 is comparable to n. The inequality includes a=c=0,d>=2 through reaction 6.

For phi_s split the state space:

- If c<=M x, then n<=C_M x+d. Reactions 2 and 6 have the same favorable simultaneous-change bound for large states. The only positive contribution is reaction 3, at most C d phi_s. In this region z and x, their denominators, and phi_s and psi_s are comparable with constants depending on M. Choosing C2/C1 large absorbs that contribution in the strict psi_s drift, leaving a negative margin of order `nd phi_s/x`.
- If c>M x, reaction 4 contributes at most `-c cd phi_s/x`, and reaction 3 contributes at most C d phi_s. For d>=x, reactions 2 and 6 are favorable, with reaction 6 supplying `-c d(d-1)phi_s/x`; choosing M large therefore gives the required `-c nd phi_s/x`. For d<x, their possible positive denominator terms are bounded by `C(ad+d^2) n phi_s/(x^3+nd)`. When x is large, n<=c+2x and the ratio of this bound to `cd phi_s/x` is O(1/x). When x is bounded and n grows, d<x stays bounded, so the positive terms are bounded multiples of phi_s whereas the negative cd term grows with c. Thus the same negative margin follows above a fixed shell threshold. The psi_s contribution remains nonpositive.

The two creation reactions decrease x and z by at most two and increase d. Their total positive contribution is bounded by C a F_s. Clearing contributes `-k0(a)_2 F_s`. The preceding linear/reverse-seed margin is of order `nd phi_s/x`. For large a, half the clearing term absorbs C a F_s; for bounded a and large n, the nd term absorbs it. Hence

`(Q-k0(a)_2)F_s <= -c [a^2+nd/x] phi_s`.

For large a, a and x are comparable, giving `[a^2+nd/x]phi_s >=c x^(-s-1)`. For bounded a and large n, nd>=n and the same lower bound holds. This proves the asserted asymptotic drift (D), subject to independent checking of the displayed regional finite-difference constants.

## 3. Upper dormant forcing value

Take s=a0. The only dormant-entry reaction is reaction 2 at d=1. Its terminal reward rate is

`k2 a (2+A)^-m <= C x^(-a0-1)`.

The negative drift (D), after scaling F_s by a fixed constant, pays this reward rate. Stopped Dynkin therefore gives

`V <= C x^-a0/(x^3+nd)`.                              (V)

One may add connector killing: it reduces the dormant payoff and only improves the super-solution. The operational connector hazards depend on b, but this upper estimate is independent of them. Small shells have finitely many active composition inputs. Their first-connector V is bounded above by its no-connector value; using those actual finite-state values extends (V) uniformly in b>=q.

## 4. Lower bound for the SAME episode's A-occupation

Set deterministic operational time

`t0=epsilon x/(x^3+nd)`.

Stop additionally when A leaves a fixed factor band around its incoming value, when a creation or clearing occurs, or at a connector event. Before this stop, d cannot increase; therefore d<=d_initial. Fast rates are bounded by `C[x^2+nd]`. The expected number of fast events before t0 and this stop is at most `C epsilon x`. Since each changes A by at most two, Markov's inequality bounds factor-band exit probability by C epsilon. Creation/clearing hazard is at most Cx^2, giving total event probability at most `C epsilon x^3/(x^3+nd)<=C epsilon`.

The operational rates of actual immigration and activation are at most constants uniformly in b>=q, because a0>=2:

`lambda_I^op=kI/[(A)_a0(b)_q]`,
`lambda_T^op=kT A b/[(A)_a0(b)_q]`.

They contribute at most C epsilon to early stopping. Choose epsilon fixed and small enough that, with probability at least 1/2, none of the listed exits occurs before t0. B remains fixed; A is comparable to its input. Restoring physical time gives

`(b)_q U = E integral A/(A)_a0 ds >= c x^(1-a0)t0`

and hence

`(b)_q U >= c x^(2-a0)/(x^3+nd)`.                      (U)

For bounded initial A, replace the factor-band exit by a fixed-width band and reduce epsilon; the same fixed-constant bound holds. This argument pays the genuine episode, including the competing connector hazards. It neither conditions on an unusually slow observed path nor assumes fast equilibrium.

Combining (V) and (U) gives (R).

## 5. Consequence and strict boundary

If the dormant continuation Green has the earned uniform bound `G_D<=M_theta exp(theta r) f_m(A)`, then its incoming forcing from a positive-D first episode is at most

`C_theta (b)_q (1+A_in)^-2 U exp(theta r)`.

Unlike the stopped-high-A version, no low-A boundary term is discarded. At the section b=q this is a fixed-constant vanishing leakage as A_in grows. Unbounded high-b histories still require actual phase enumeration. The proposed dormant Green bound still needs independent review, and complete-cycle coefficient-one drift, bad-to-bad correction, and complementary residual closure remain unproved. This local comparison alone does not establish recurrence of the full nonbalanced network.

Numerical support is falsification only: unit-rate finite-shell solves through n=256 show the maximum of `(1+A_in)^2 V/U` (operational normalization b-factor removed, a0=2) increasing toward approximately 0.31, with largest value at `(a,c,d)=(255,0,1)`. No finite grid proves the uniform inequality or validates all parameter choices.
