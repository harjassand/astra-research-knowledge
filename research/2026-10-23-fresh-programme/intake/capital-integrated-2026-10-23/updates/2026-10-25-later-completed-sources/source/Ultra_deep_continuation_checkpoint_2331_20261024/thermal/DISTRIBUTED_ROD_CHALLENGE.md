# Distributed rods restore a finite full-channel width

This is an independent mathematical audit of the distributed realization
selected by the physical-interface owner `/root/passive_lag`, after the
owned positive point-mass construction in `NONLOCAL_KERNEL_CONSTRUCTION.md`.
It does not replace that construction or the physical owner's proof.
The conclusion is affirmative for the counted scalar rod model: a small,
fixed connector mass can restore finite intrinsic thermal channel width.
This is a failure of the proposed vanishing-conductance realization, not a
claim that all nonlocal realizations fail or that a device was operated.

## 1. Full positive field model and its resources

There is one point mass `m>0` per cell of length `a`. For every
`l=1,...,N-1`, a separate uniform longitudinal rod connects vertices `l`
cells apart. Its length is `l a`, its axial stiffness is

`kappa_l=12K(N-l)/[N^2(N^2-1)]`,

and its cross-section is `A_l=kappa_l l a/E`. All rods have the same finite
wave speed `c=sqrt(E/rho)`. Each edge is counted once per cell. Consequently

`sum l^2 kappa_l=K`,
`sum rho A_l l a=K a^2/c^2`,
`M_total=m+K a^2/c^2`.

The static long-wave stiffness and the complete mass per cell are both
fixed as `N` grows. This is a genuine distributed-inertia calculation,
although scalar axial fields, ideal joints and collision-free routing are
still model assumptions. If a prescribed total mass is required, choose
`m=M_total-K a^2/c^2>0` once; no mass adjustment with `N` is needed.

Set

`x=omega a/c`, `mu=K a^2/(m c^2)`,
`B=12mu/[N^2(N^2-1)]`, `b_l=B(N-l)`.

Away from all rod Dirichlet frequencies `l x in pi Z`, the exact scalar
vertex equation is

`D(x,q)=-x^2+sum_(l=1)^(N-1) T_l(x,q)=0`,
`T_l=2 b_l l x [cos(l x)-cos(l q)]/sin(l x)`.

This follows by solving each rod's wave equation with its two Bloch
endpoint displacements, not by replacing the rod with a lumped spring.
The standard two-end map is

`EA(omega/c)/sin(omega L/c) * [[cos(omega L/c),-1],[-1,cos(omega L/c)]]`.

Liu et al., *Applied Mathematical Modelling* 104 (2022),
[DOI 10.1016/j.apm.2021.11.023](https://doi.org/10.1016/j.apm.2021.11.023),
Eqs. 10,12 give this classical axial-rod map; Eqs. 55-57 retain eliminated
fixed-end modes in the assembled mode count. The formula and the pole
warning have also been independently checked in `sources_support/ROD_DYNAMIC_STIFFNESS_AND_GRAPH_COUNT.md`.

## 2. Narrow intervals near many different rod resonances

Assume `N>=12` is a multiple of 12 and `0<mu<=1/100`. For each integer

`2N/3 <= n <= 3N/4`,

let `x_n=pi/n` and

`I_n=[x_n+b_n/x_n, x_n+2b_n/x_n]`.

Every point in these intervals has `x=x_n+delta` with

`0<delta<=3mu/N^2`.

At the selected wave-number grid `q_j=j pi/n`, `j=0,...,n`, the nth rod
will dominate `D` and alternate its sign. The rest of this section proves
that domination with elementary uniform bounds.

Write `R_n=sum_(l!=n) T_l`. At `x=x_n`, pair indices `n-ell,n+ell` for
`1<=ell<=N-1-n`. Their trigonometric numerators are identical because

`cos((n+-ell)x_n)=-cos(pi ell/n)`,
`cos((n+-ell)q_j)=(-1)^j cos(j pi ell/n)`.

If `a_l=l(N-l)`, then
`a_(n-ell)-a_(n+ell)=2(2n-N)ell`. Since
`sin(pi ell/n)>=2ell/n`, the sum of all paired absolute contributions is
at most

`4pi B(2n-N)(N-n) <= (pi/2) B N^2`.

The unpaired indices are `1<=l<=2n-N`, so `l/n<=2/3`. The chord bound
`sin(pi l/n)>=3sqrt(3)l/(4n)` and
`sum_(l=1)^(2n-N) (N-l)<=3N^2/8` give an unpaired bound

`(2pi/sqrt(3)) B N^2`.

Thus, uniformly in the sampled `q_j`,

`|R_n(x_n,q_j)| <= (pi/2+2pi/sqrt(3)) B N^2 <64mu/N^2`.       (1)

The last inequality holds already at `N=12`; the factor
`N^2/(N^2-1)` decreases thereafter.

Here is a separate uniform off-centre estimate; it does not presume that
the exact cancellation persists away from the pole. For `l!=n`, put

`h_l=min(l,|l-n|)`.

For `0<=delta<=3mu/N^2`, the centre inequality
`|sin(pi l/n)|>=2h_l/n` and the Lipschitz bound on sine imply

`|sin(l(x_n+delta))| >= (2-9mu/4)h_l/n >= h_l/n`.             (2)

Also `0<l(x_n+delta)<3pi/2`. In particular no other rod pole lies in this
shift segment. Differentiating the individual rod expression at fixed `q`
gives

`|dT_l/dx| <=4 b_l l [1/|sin(lx)|+l x/sin^2(lx)]`.

Each positive value of `h_l` occurs at most three times. Therefore
`sum 1/h_l<=3N` and `sum 1/h_l^2<=pi^2/2`. Using `n<=3N/4` in (2),

`sum_(l!=n)|dT_l/dx|`
` <=[108+(81/4)pi^3] [N^2/(N^2-1)] mu <768mu`.

Combining this with (1) yields

`|R_n(x,q_j)| <[64mu+2304mu^2]/N^2 <0.06 x_n^2`.             (3)

The final constant uses `mu<=1/100` and
`x_n^2>=16pi^2/(9N^2)`. The margin is deliberately loose.

## 3. Alternating signs and the full propagating count

Let `epsilon=n delta`. Then `0<epsilon<1` and
`x^2<1.002 x_n^2`. The nth rod term has the exact forms

`T_n(x,q_j)=2 b_n n x cot(epsilon/2)` for even `j`,
`T_n(x,q_j)=-2 b_n n x tan(epsilon/2)` for odd `j`.

Since `cot(epsilon/2)>=3/(2epsilon)` on this small interval and
`delta<=2b_n/x_n`, the even term is at least `1.5 x x_n`, hence at least
`1.5 x_n^2`. The odd term is nonpositive. Equation (3) now gives

`D(x,q_j)>0` for even `j`, `D(x,q_j)<0` for odd `j`.

These are signs of the exact field secular equation. Continuity in `q`
gives at least `n` distinct roots in `(0,pi)` for every `x in I_n`.
The degree of this trigonometric polynomial is **N-1**, not `n`; the signs
give a lower bound and do not exhaust all its roots.

The connection to propagating modes can be checked without trusting a
cleared-denominator polynomial. Prescribe the vertex amplitude to be one
and eliminate each rod by its exact boundary-value solution. Differentiating
the stationary elastic-minus-inertial action with respect to `omega^2`
gives minus the complete positive kinetic norm:

`dD/d(x^2) <0`.

In physical normalization its numerator is
`-m-sum_l integral_rod rho A_l |U_l(s)|^2 ds`.
No interior-field derivative remains because the solved fields make the
action stationary at fixed endpoint data. Thus a nonpole root is an actual
simple frequency eigenvalue of the full fiber. A root at positive `q` has
its time-reversed root at `-q` with opposite group velocity. Except for
critical frequencies, each pair supplies one right mover, whether the
positive-q mode moves forwards or backwards.

The critical-frequency exception has measure zero: locally the zero set
is an analytic frequency branch by `D_(x^2)<0`, and a flat branch would
make `D(x,q)` identically zero in `q`. Its nonzero `(N-1)`th harmonic
forbids that at a nonpole `x`. At an exact rod pole the eliminated equation
is not used. Those isolated frequencies cannot remove the open-interval
channels just constructed; additional vertex-zero rod modes do not occur
away from rod poles. Consequently

`N_R(x)>=n` for almost every `x in I_n`.                     (4)

This is the complete ideal right-moving count, with repeated crossings
retained. It is not a band union counted once and is not a finite-contact
transmission claim.

## 4. Summed width and finite-temperature consequence

The intervals are disjoint. Indeed the centre gap is at least
`16pi/(9N^2)`, whereas any upper offset is at most
`16mu/[3pi(N^2-1)]`, strictly smaller than that gap. Moreover

`sup union I_n <=3pi/(2N)+3mu/N^2=:X_N`,

and

`sum_n n |I_n|`
` =12mu/[pi N^2(N^2-1)] sum_n n^2(N-n)`
` >=12mu/[pi N^2(N^2-1)] * N^4/108`
` =mu N^2/[9pi(N^2-1)] >=mu/(9pi)`.

The independent arithmetic receipt is
`multichannel_support/DISTRIBUTED_ROD_INTERVAL_AUDIT.md`; an initially
malformed intermediate display there is superseded by its appended
correction, not used here.

For dimensionless temperature `theta_bar=(k_B T/hbar)a/c`, let

`J_bar=int_0^infinity N_R(x) [x/(2theta_bar)/sinh(x/(2theta_bar))]^2 dx`.

The Bose weight is decreasing. Equations (4) and the summed width give

`J_bar >=mu/(9pi) g_(theta_bar)(X_N)`.

Thus at every fixed positive temperature,

`liminf_(N->infinity) J_bar >=mu/(9pi)>0`,
`liminf J_physical >=(c/a)mu/(9pi)`.

The thermal conductance is `k_B J_physical/(2pi)` in the same ideal
Landauer convention as the earlier work. This finite floor persists even
when `mu` is small and the rod mass is a small fixed fraction of the
complete mass. The selected low-frequency modes alone prevent the
point-mass `1/N` heat collapse; nothing is inferred about the uncounted
higher-frequency contribution or a globally best physical design.

The explanatory mechanism is explicit: every narrow interval shrinks like
`mu/N^2`, but it carries order `N` right-moving crossings, and order `N`
different rods furnish disjoint intervals. The finite intrinsic width is
therefore restored by the same connector fields that provide the nonlocal
static coupling. Their total mass need not diverge. Physical material
advantage, feasible routing, finite-device contacts and anharmonic heat
transport remain separate questions.

## 5. A finite numerical challenge, separate from the proof

`verify_distributed_rod_signs.py` evaluates the exact rod expressions at
55 decimal digits. It checks every selected `n,j` at both interval endpoints
and the midpoint for `N=12,24`, `mu=.01`, and for `N=24`, `mu=.000001`.
It also challenges three separated selected `n` values at `N=120,mu=.01`.
All 1,155 frequency/wave-number samples passed, along with the resource
identities, pole separation, derivative/rest bounds and interval arithmetic.
The smallest positive even-grid margin was greater than `.989 x_n^2`;
the smallest negative odd-grid margin in magnitude exceeded `.999 x_n^2`.
Results are saved in `distributed_rod_sign_checks.json`. These are finitely
many high-precision numerical tests; the uniform claims rest on Sections 2-4.

## 6. Sequence-scope closure: all integers N, not only multiples of 12

The first version proves the finite lower bound on the explicitly assumed
subsequence `N in 12 Z`, whereas Section 4 writes an unrestricted `liminf`.
Root identified that quantifier gap. Here is its direct closure; no earlier
proof or diagnostic is removed.

For arbitrary integer `N>=13`, select
`ceil(2N/3)<=n<=floor(3N/4)`. Every estimate in Sections 2-3 only uses
`2N/3<=n<=3N/4` and `N>=12`, so it is unchanged. The interval separation
and maximum endpoint bound are also unchanged. The number of selected
integers is at least `N/12-1`; therefore the summed weighted width is at
least

`mu/(9pi) * [N^2/(N^2-1)] * (1-12/N)`.

For these general integers the corresponding finite-temperature bound is

`J_bar >=mu/(9pi) * [N^2/(N^2-1)] * (1-12/N) g_(theta_bar)(X_N)`.

Taking `N` through all integers now proves the same unrestricted positive
`liminf` stated in Section 4. The sharper finite `mu/(9pi)` width bound
continues to hold on the original multiple-of-12 subsequence. No finite
computation is needed for this extension.

## 7. Jointly retuned cold designs acquire many thermal channels

Keep the physical quantities `m,K,a,c` fixed, hence keep
`mu=Ka^2/(m c^2)>0` and the complete mass `m+Ka^2/c^2` fixed. Retain the
exact scalar continuum rod fields, their endpoint joint law and every
propagating Bloch crossing. Now take a **family of different designs**
`N=N(theta_bar)` with

`theta_bar ->0`, `N theta_bar ->infinity`.

This is precisely the range/temperature scaling that made the ideal
point-mass Fejer spectrum satisfy `J_bar/J_Q,bar ->0`. In the distributed
rod model, however,

`X_N/theta_bar <=3pi/(2N theta_bar)+3mu/(N^2 theta_bar) ->0`.

The general-integer width bound in Section 6 and continuity of the Bose
weight at zero therefore imply

`J_bar >=mu/(9pi) [1-o(1)]`,

and, since `J_Q,bar=pi^2 theta_bar/3`,

`J_bar/J_Q,bar >=mu/[3pi^3 theta_bar] [1-o(1)] ->infinity`.

The design changes jointly with temperature; the extra near-resonant rod
crossings remain thermally populated. This does not describe cooling one
fixed device. At each fixed finite `N`, positivity and the nearest rod
ensure a connected scalar graph with one acoustic zero, a positive
long-wave stiffness and only one sufficiently low-frequency right-moving
channel. Thus the usual fixed-design limit is instead
`J_bar/J_Q,bar ->1` as `theta_bar->0`. The growing-range limit and the
fixed-design cold limit do not commute.

This conclusion relies on the full ideal axial continuum model already
stated, and does not claim that every material admits arbitrarily thin,
arbitrarily long rods, or that finite-device contacts have unit
transmission. Within that counted model it directly reverses the proposed
point-mass cold-design scaling, rather than merely modifying its constant.
