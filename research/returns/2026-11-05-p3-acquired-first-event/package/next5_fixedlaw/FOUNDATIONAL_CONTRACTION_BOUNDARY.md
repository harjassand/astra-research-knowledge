# Exact event prediction under a completely known strict contraction

**Status:** completed mathematical construction and exact rational compiler; independent companion to the acquired first-event work. This document does not claim historical priority or a practical physical computer. It preserves the original `next4_theory/FIXED_LAW_CERTIFICATION.md` unchanged.

## 1. The question and the completed consequence

The prior fixed-law construction gives finite-horizon consistency and positive-margin all-time certificates when one stationary Lipschitz law must explain every observation and future trajectory. Its equality boundary is explicit. Can sufficiently strong contraction, complete model acquisition, a known equilibrium, and exact finite rational model data remove that boundary?

They cannot in general. The following construction supplies the entire law and a particularly simple global contraction certificate; the remaining exact event question is still undecidable.

**Theorem 1 — certified contraction with undecidable finite arrival.** There is an effective compiler taking a deterministic two-counter program with `m >= 2` labels, the last label being HALT, to a finite rational continuous piecewise-linear map

\[
G_M:\mathbb R^4\longrightarrow\mathbb R^4
\]

with all of these properties:

1. The map is positively homogeneous, `G_M(0)=0`, and

   \[
   \|G_M(x)-G_M(y)\|_2\le\tfrac12\|x-y\|_2
   \quad\hbox{for all }x,y\in\mathbb R^4.
   \tag{1}
   \]

2. Zero is its unique fixed point, and every orbit satisfies

   \[
   \|G_M^n(x)\|_2\le 2^{-n}\|x\|_2.
   \tag{2}
   \]

3. From any supplied machine configuration, a rational initial state is effectively constructed. The machine halts if and only if that orbit reaches the *known fixed point exactly in finite time*.

4. The same machine halts if and only if the orbit enters the fixed open halfspace

   \[
   x_q-\tfrac34 t>0,
   \tag{3}
   \]

   where the state coordinates are `(t,x_q,x_0,x_1)`.

5. The compiler uses `54m` tetrahedra before global extension and at most `1890m` rational conical cells afterward, keeping redundant cells. Its coefficient sizes are polynomial in the program-description size. The global map has a division-free evaluator, apart from division by fixed rational constants.

Consequently, neither finite arrival at the known fixed point nor all-time avoidance of (3) has a decision algorithm on this supplied, certified class. This is stronger information than an unresolved numerical equality in one optimization method: no alternative total algorithm solves every instance of this class.

There is a matching quantitative positive statement. A hazard separated from the equilibrium by a known positive absolute margin has a finite effective horizon. At contraction `1/2`, a rational piecewise-linear law and rational point initial state can be checked for such a hazard in bit work polynomial in the explicit description and `log(1/margin)`. The negative result occurs precisely where arbitrarily late events have arbitrarily small absolute size.

**Scope of the scientific consequence.** This resolves a foundational question about what a global stability certificate can establish. It does not acquire a law from data, solve general control synthesis, or provide macroscopic computation protected against fixed noise. General continuous piecewise-affine reachability undecidability is classical; the precise contraction reduction below should be treated as an explicit quantitative corollary/boundary unless a deeper priority study establishes otherwise. Section 12 compares the strongest directly relevant primary results.

## 2. The computational premise and its actual encoding cost

A machine has labels `1,...,m`, two nonnegative integer counters, and the following instructions:

| Instruction | Operation |
|---|---|
| `INC(r,j)` | Increase counter `r` by one; go to label `j` |
| `DECJZ(r,j0,j+)` | If counter `r` is zero, go to `j0`; otherwise decrease it by one and go to `j+` |
| `HALT` | Stop |

The last label is the sole HALT. Arbitrary branching targets are permitted. This instruction set contains the universal CM2 instruction set described precisely by Dudenhefner; its halting problem is undecidable [R1]. Multiple stopping labels can be merged. A starting configuration can be built into a finite initialization prelude, so fixing both initial counters to zero does not make the program-halting problem decidable.

For label `i`, put

\[
q_i=\frac{i}{2m}\quad(1\le i<m),\qquad q_m=1.
\tag{4}
\]

Encode a configuration `(i,c_0,c_1)` by

\[
z=(q_i,2^{-c_0},2^{-c_1})\in[0,1]^3.
\tag{5}
\]

A counter is zero precisely when its encoding is `1`; a positive counter has encoding at most `1/2`. The empty interval between `1/2` and `1` permits a continuous interpolation of the zero test.

The integer values of the initial counters matter. Writing `2^{-c}` as an ordinary rational with an explicit binary denominator costs `c+1` denominator bits, rather than `O(log(c+1))`. Thus the compiler is polynomial in the program description and the *explicit rational initial-state description*, not in the binary length of an arbitrarily large counter supplied in compressed form. No compressed-exponent arithmetic is silently granted.

## 3. A continuous cube simulator with an absorbing output

Construct a map

\[
W:[0,1]^3\longrightarrow\mathbb R^4,
\qquad W(z)=(c,y_q,y_0,y_1),
\]

whose values obey

\[
0\le y_q,y_0,y_1\le c\le1.
\tag{6}
\]

First prescribe it on the control planes `q=q_i`.

At a nonhalting label set `c=1`. For an increment, set `y_q=q_j`, divide the selected encoded counter by two, and leave the other unchanged. For a decrement/zero test, write `z_r` for the selected encoded counter and set

\[
(y_q,y_r)=
\begin{cases}
(q_{j_+},2z_r),&0\le z_r\le1/2,\\[2mm]
((1-u)q_{j_+}+u q_{j_0},1),&1/2\le z_r\le3/4,
\quad u=4z_r-2,\\[2mm]
(q_{j_0},1),&3/4\le z_r\le1.
\end{cases}
\tag{7}
\]

Leave the other counter unchanged. Formula (7) is continuous at both joining points and performs the exact machine instruction on every valid counter encoding. At the HALT plane `q=1`, set all four output coordinates to zero. At the additional plane `q=0`, use the formula for label 1; no valid configuration needs this filler plane.

The control grid is

\[
0,q_1,\ldots,q_{m-1},1,
\]

and each counter grid is

\[
0,1/2,3/4,1.
\]

There are `9m` rectangular bricks. Triangulate every brick by the same six Freudenthal simplices. If its lower corner is `l`, widths are `Delta_1,Delta_2,Delta_3`, and `pi` is a permutation of the coordinate indices, the simplex vertices are

\[
v_0=l,\qquad
v_j=v_{j-1}+\Delta_{\pi_j}e_{\pi_j},\quad j=1,2,3.
\tag{8}
\]

For normalized coordinates `u_j=(z_j-l_j)/Delta_j`, its region is `u_{pi_1} >= u_{pi_2} >= u_{pi_3}` and the barycentric weights are

\[
1-u_{\pi_1},\quad u_{\pi_1}-u_{\pi_2},\quad
u_{\pi_2}-u_{\pi_3},\quad u_{\pi_3}.
\tag{9}
\]

Assign each grid vertex the prescribed control-plane value and interpolate affinely on each simplex. These triangulations agree on every shared face, so the interpolation is globally continuous. The set (6) is convex, so it is preserved by interpolation. On each control plane, the prescribed formula is affine on every counter-grid rectangle. Hence the interpolated map equals that formula everywhere on the plane, including all machine encodings. No approximation of the zero test has occurred.

There are exactly `54m` tetrahedra. Write the formula on a tetrahedron as `W(z)=Az+b`. Each component of a vertex output lies in `[0,1]`. Successive vertices in (8) differ in one coordinate, so each derivative column is an output difference divided by that coordinate's grid width. Therefore

\[
|A_{j,q}|\le2m,\qquad |A_{j,0}|,|A_{j,1}|\le4,
\]

and consequently

\[
\sum_{j,k}|A_{jk}|\le8m+32,
\qquad
\sum_j|b_j|\le8m+36.
\tag{10}
\]

Define the deliberately conservative, explicit integer bound

\[
C_m=16m+68.
\tag{11}
\]

Every matrix `[b | A]` has entrywise absolute sum at most `C_m`, and thus Euclidean operator norm at most `C_m`. This is a sufficient bound; the implementation records substantially smaller actual entry sums in its examples.

## 4. Homogenization without a vanishing-scale division oracle

Let

\[
\mathcal C=\{(t,x_q,x_0,x_1):t\ge0,\ 0\le x_j\le t\}.
\tag{12}
\]

For `t>0`, define

\[
T(t,x)=tW(x/t),\qquad T(0,0)=0.
\tag{13}
\]

On a cone over a cube tetrahedron, this is exactly the linear map with matrix `[b | A]`. Thus (13) specifies a finite continuous positively homogeneous piecewise-linear map from `C` to `C`. Continuity at the origin follows also directly from (6).

For any two points of the convex cone, split their joining segment at the finitely many linear-piece boundaries. The variation on each segment piece is at most `C_m` times its length. Summing gives

\[
\|T(v)-T(w)\|_2\le C_m\|v-w\|_2
\quad(v,w\in\mathcal C).
\tag{14}
\]

Formula (13) is convenient for the proof but is **not** implemented as division by the shrinking state `t`. The exact evaluator compares `x_j` with fixed grid multiples of `t`, chooses the brick, and computes

\[
v_j=(x_j-l_jt)/\Delta_j.
\]

After sorting these three values, the scaled barycentric weights are

\[
t-v_{\pi_1},\quad v_{\pi_1}-v_{\pi_2},\quad
v_{\pi_2}-v_{\pi_3},\quad v_{\pi_3}.
\tag{15}
\]

Their weighted sum of the four fixed vertex outputs equals `T(t,x)`. Only fixed rational grid widths are divided. The branching conditions are homogeneous rational linear inequalities. Arbitrarily fine exact comparisons remain a real precision cost; eliminating division does not remove that cost.

## 5. Global extension with an explicit nonexpansive interface

An assertion only on the encoded subset or cone would not establish global contraction. Let `Pi_C` be the Euclidean metric projection onto (12).

Given `v=(t_0,x_1,x_2,x_3)`, for a fixed candidate `t>=0` the closest other coordinates are `clip(x_j,0,t)`. The remaining scalar convex problem is

\[
\min_{t\ge0}(t-t_0)^2+
\sum_{j=1}^3\bigl(\operatorname{clip}(x_j,0,t)-x_j\bigr)^2.
\tag{16}
\]

If `t_0+sum_j max(x_j,0)<=0`, the answer is the origin. Otherwise, for the set `I` of coordinates above the optimum `t`,

\[
t=\frac{t_0+\sum_{j\in I}x_j}{1+|I|}.
\tag{17}
\]

Enumerate the eight possible sets `I`, retaining the candidate with `t>=0`, `x_j>=t` for `j in I`, and `x_j<=t` for `j not in I`. Then clip the remaining coordinates. Boundary ties give the same projection. This is a finite exact rational procedure, with division only by integers `1,...,4`.

A fully explicit conical presentation uses at most 35 cells: eight sign patterns for the zero-projection region and 27 assignments of each coordinate to the classes `x_j<=0`, `0<=x_j<=t`, or `x_j>=t`. Every formula on such a cell is linear with rational coefficients. The nonzero projection matrices are symmetric idempotent matrices; the zero-region matrix is zero.

For completeness, nonexpansiveness follows directly from projection optimality. For `p=Pi_C(v)` and `q=Pi_C(w)`,

\[
\langle v-p,q-p\rangle\le0,
\qquad
\langle w-q,p-q\rangle\le0.
\]

Subtracting yields

\[
\|p-q\|_2^2\le\langle p-q,v-w\rangle
\le\|p-q\|_2\|v-w\|_2,
\]

so `Pi_C` is globally 1-Lipschitz. It fixes the cone and is positively homogeneous.

Now set

\[
a=(2C_m)^{-1},\qquad
G_M=aT\circ\Pi_{\mathcal C}.
\tag{18}
\]

Equations (14) and (18) prove (1) globally. Composition gives a rational linear formula on the intersection of each projection cell with the preimage of each conical simplex. Keeping empty and redundant intersections produces at most `35*54m=1890m` cells, with an explicit rational inequality description. The code emits this full presentation on request. No region-feasibility oracle is needed to construct it.

Because `G_M(0)=0`, inequality (1) proves (2). If `v` is any fixed point, `||v||<=||v||/2`, so `v=0`. This establishes stability directly rather than asking an algorithm to verify an unknown stability property.

## 6. Exact simulation and the undecidable event

Let a machine run start at configuration `z_0` encoded by (5), and set

\[
v_0=(1,z_0).
\]

Until and including its first arrival at the HALT label,

\[
G_M^n(v_0)=a^n(1,z_n).
\tag{19}
\]

This follows inductively: every such point is in the cone; projection fixes it; positive homogeneity factors out `a^n`; and the control-plane map executes the exact instruction.

If HALT is first reached at step `H`, then the point at step `H` remains nonzero and has `x_q=t=a^H`; its next image is zero. If the machine never halts, its first coordinate is `a^n>0` at every finite step. Hence

\[
M\text{ halts}\quad\Longleftrightarrow\quad
\exists n\ G_M^n(v_0)=0.
\tag{20}
\]

For the fixed observable

\[
\ell(t,x_q,x_0,x_1)=x_q-\tfrac34t,
\tag{21}
\]

every nonhalting encoded label has `q_i<1/2`, so

\[
\ell(G_M^n(v_0))\le-\tfrac14a^n
\]

before halting, while

\[
\ell(G_M^H(v_0))=\tfrac14a^H>0.
\tag{22}
\]

After that point the orbit is zero. This proves the equivalence with the halfspace event (3). The target boundary contains the equilibrium. A target at positive distance from the equilibrium has the finite-horizon treatment in Section 8, so that stronger positive premise cannot be dropped silently.

The reduction from counter halting proves Theorem 1. Exact rational simulation semidecides the positive event: run until the target is reached. There can be no computable bound, in the complete finite input description, on the first event time of all instances that eventually have an event. Such a bound followed by finite exact simulation would decide halting.

All-time safety for (3) is not even recursively enumerable on this family. If both a finite violating trace and some sound complete effectively enumerable collection of safe certificates existed, dovetailing their searches would decide the two-counter halting problem. Thus any sound effective certificate system must omit some safe instances, fail to terminate on them, or impose an additional restriction.

By choosing a fixed universal two-counter program, the same argument gives a **single** fixed rational contraction whose exact event problem is undecidable as the rational initial counter encoding varies. This existence corollary uses the standard universal-machine premise. The package supplies a compiler for arbitrary finite programs, not a minimal universal program listing or a measured universal-machine implementation. The expanded initial-state encoding cost from Section 2 still applies.

## 7. An efficiently approximable event value with undecidable zero test

The preceding result can be stated as a direct limitation of value-based scientific prediction. Define

\[
V_M(x)=\sup_{n\ge0}\ell(G_M^n(x)).
\tag{23}
\]

The orbit converges to zero, so the supremum is always nonnegative. Since `||ell||_2=5/4`, each iterate observable has Lipschitz constant at most `(5/4)2^{-n}`. Therefore

\[
|V_M(x)-V_M(y)|\le\tfrac54\|x-y\|_2.
\tag{24}
\]

The function is also positively homogeneous. For

\[
V_{M,N}(x)=\max\{0,\ell(x),\ell(G_Mx),\ldots,
\ell(G_M^{N-1}x)\},
\]

we have the uniform quantitative approximation

\[
0\le V_M(x)-V_{M,N}(x)
\le\tfrac54\,2^{-N}\|x\|_2.
\tag{25}
\]

Thus additive accuracy `epsilon` costs only `O(log(||x||/epsilon))` exact map evaluations. Section 9 pays their bit complexity. Nonetheless, at an encoded initial point,

\[
V_M(v_0)=
\begin{cases}
0,&M\text{ never halts},\\
a^H/4,&M\text{ first halts at }H.
\end{cases}
\tag{26}
\]

The exact positive-versus-zero test is undecidable. A convergent algorithm with a known geometric error modulus does not imply a total equality/positivity decision algorithm. This distinction persists with one entirely known law, fixed state dimension, and a Lipschitz constant for the value independent of the program.

There is also a conventional Bellman representation. On the Banach space of continuous positively homogeneous real functions with norm

\[
\|u\|_* = \sup_{\|x\|_2=1}|u(x)|,
\]

put

\[
(\mathcal Bu)(x)=\max\{0,\ell(x),u(G_Mx)\}.
\tag{27}
\]

Then

\[
\|\mathcal Bu-\mathcal Bw\|_*\le\tfrac12\|u-w\|_*.
\]

Its unique fixed point is `V_M`, and iteration from zero gives the finite-prefix maxima above. This is an infinite-dimensional function-space Bellman operator. It is not a finite-state monotone MDP operator, so the specialized positive decidability results in [R3] are unaffected. The construction gives an explicit case in which rapidly convergent value computation and exact event classification have different computability status.

## 8. The resolution-aware positive theorem

**Theorem 2 — a positive absolute margin gives a finite horizon.** Let `F` be an explicitly supplied rational continuous piecewise-affine map with known rational fixed point `x_*` and certified global contraction factor `0<q<1`. Let `x_0` be rational, `R>=||x_0-x_*||` a known rational upper bound, and `h(x)=w^T x+b` an affine observable with known rational norm upper bound `L>=||w||_2`. For `rho>0`, the event

\[
\exists n\ge0:\quad h(F^n(x_0))\ge h(x_*)+\rho
\tag{28}
\]

is decidable by evaluating the finite prefix before the smallest integer `N>=0` with

\[
LRq^N<\rho.
\tag{29}
\]

**Proof.** For every `n>=N`, contraction gives

\[
|h(F^n(x_0))-h(x_*)|\le LRq^n<\rho.
\]

The event is consequently confined to `0,...,N-1`. Rational region membership, map evaluation, and the threshold comparison in that prefix are exact finite calculations. The strict inequality in (29) handles equality at a finite threshold correctly. If `LR=0`, the event is impossible from the outset. ∎

For `q=1/2`, one may take

\[
N\le 1+\max\{0,\lceil\log_2(LR/\rho)\rceil\}.
\tag{30}
\]

The horizon depends on the *value* of `1/(1-q)` when `q` varies toward one. There is no uniform polynomial-in-bit-length horizon for arbitrarily weak contraction. Fixed `q=1/2` avoids that issue.

The theorem applies, for example, to the target `ell>=rho` for `G_M`. It also solves the promise problem “no `ell>0` ever” versus “some `ell>=rho`” for supplied `rho>0`. An orbit with a positive excursion below `rho` is outside that promise, not certified safe by it.

A target point distinct from `x_*` is similarly decidable: choose the positive radius `||target-x_*||` or a strictly smaller effective rational lower bound, and inspect a finite prefix. The theorem does not solve exact finite arrival at `x_*`; that is the case in Theorem 1.

## 9. Acquisition, computation, memory, and physical precision

The premise here is deliberately stronger than empirical access: the entire finite rational map, its initial point, and its contraction certificate are supplied exactly. There is no statistical model-learning or experimental sample cost in this mathematical problem. The result therefore also obstructs any universal exact-event procedure whose promised job includes this fully known subclass. It does not infer a global contraction prior from finite data or remove the state-observability and stationarity premises of the earlier fixed-law theorem.

For `G_M`, the cube compiler and global extension have `O(m)` cells with constant-size rational matrices and inequalities; coefficients use `O(log m)` bits up to fixed constants. The direct evaluator uses at most `O(m)` grid comparisons (binary search can reduce the control-grid part), a constant-size projection active-set enumeration, three-coordinate sorting, and fixed rational linear arithmetic. The retained evolving state has four rational coordinates. The program, grid values, and coefficients require `O(m log m)` bits. Neither the finite state dimension nor the piece count bounds the precision needed over arbitrary time.

For a general explicit rational piecewise-affine description of bit size `S`, let `D` be a common multiple of all coefficient denominators. One can take `log D<=O(S)`. Starting with common denominator `Q`, after `n` evaluations the coordinates can be represented over denominator `Q D^n` (augment by a constant coordinate for affine pieces). Numerator and denominator bit lengths grow at most polynomially, and linearly in `n` up to input-size factors. Region comparisons are rational linear comparisons. Hence a finite prefix of length `N` has bit work polynomial in `S`, the initial bit size, and `N`, without treating exact real arithmetic as unit cost. At contraction `1/2`, Theorem 2 and (25) therefore give polynomial bit work in the supplied description and the required number of accuracy bits.

This efficient approximation is fully consistent with undecidability: the required exact decision has no fixed positive gap. If the compiled machine halts after `H` steps, its flag has magnitude `a^H/4`. A direct readout whose absolute error is bounded by `2^{-b}` must have

\[
2^{-b}<a^H/4,
\quad\hbox{so}
\quad b>2+H\log_2(1/a)
\tag{31}
\]

to distinguish that positive flag from zero by this error bound. The uniform sufficient scale `a` is not optimized. Equation (31) is an exact cost for this encoding/readout criterion, not a universal lower bound on all possible algorithms for special programs.

For an implementation obeying

\[
\widetilde x_{n+1}=G_M(\widetilde x_n)+e_n,
\quad\|e_n\|_2\le\eta,
\]

and initial state error `delta_0`, contraction gives

\[
\|\widetilde x_n-G_M^n(x_0)\|_2
\le 2^{-n}\delta_0+2\eta(1-2^{-n}).
\tag{32}
\]

If the scalar readout adds error at most `nu`, the induced flag uncertainty is at most

\[
\tfrac54\bigl(2^{-n}\delta_0+2\eta(1-2^{-n})\bigr)+\nu.
\tag{33}
\]

A fixed nonzero error floor eventually exceeds the halt signal in (22). Normalizing the flag by `t=a^H` would require the equivalent growing gain and absolute precision, so it does not recover a fixed-noise physical capability. Exact equality to the equilibrium cannot be established from an arbitrary finite-precision readout alone without an additional promise. This package contains no thermal, optical, protected-memory, or finite-bandwidth implementation.

## 10. A finite ReLU corollary, with its size cost retained

The boundary is not tied to a special comparator instruction language. A rational continuous homogeneous piecewise-linear map has a finite bias-free ReLU representation. One route is the established max–min representation of a continuous piecewise-linear scalar function by its finitely many linear components [R4], applied to each coordinate, followed by

\[
\max(u,v)=v+\operatorname{ReLU}(u-v),\qquad
\min(u,v)=u-\operatorname{ReLU}(u-v).
\]

An effective finite construction enumerates the chambers of the rational hyperplanes on which pairs of distinct linear components agree, uses a rational point in each chamber, and forms its max–min expression. For `K` distinct components, even the crude enumeration of all `2^{K(K-1)/2}` sign patterns is finite; strict homogeneous feasibility can be checked by rational linear feasibility after scaling every strict inequality to have margin at least one. This gives a finite algorithm, not a small-network guarantee. Signed intermediate values can be carried by positive/negative ReLU channel pairs. Internal width and depth are not bounded by the four-dimensional recurrent state.

For any resulting network realization `F` of a positively homogeneous map, compute a rational layer-norm bound

\[
B=\prod_j\max\{1,\textstyle\sum_{r,s}|(W_j)_{rs}|\}.
\]

Scaling the final layer by `1/(2B)` gives a displayed product-of-layer-norm bound at most `1/2`. For any positive scalar `c`, homogeneity gives

\[
(cF)^n(x)=c^nF^n(x).
\tag{34}
\]

Thus zero hitting and the sign of every homogeneous linear flag are unchanged. Theorem 1 consequently persists for recurrent application of a finite rational bias-free ReLU module with a directly checkable conservative layer-norm contraction certificate. This is a mathematical corollary of the construction and existing representation theorem; the package does not execute the potentially enormous max–min-to-network compiler, claim a fixed hidden width, or claim a new neural-network universality result.

## 11. Executed finite construction

`contracting_machine.py` implements the program parser, exact rational machine dynamics, cube interpolation, division-free cone map, explicit metric projection, matrix compiler, and complete global-region emitter. `verify_contraction_boundary.py` reproduces the finite diagnostics using only Python's standard library and writes `execution_record.json`.

The executed programs have 2, 3, and 6 labels and cover both increment instructions, both decrement/zero tests, halting, and a simple provably nonhalting run. The exact checks include all 35 projection matrices being symmetric and idempotent, all compiled tetrahedron vertex formulas, control-plane interpolation values, encoded instruction transitions, and emitted global pieces. The generic mathematical proof, rather than random tests, establishes continuity, coverage, and global contraction.

| Executed quantity | Result |
|---|---:|
| Exact projection matrices checked | 35 |
| Cube tetrahedra across the three programs | 594 |
| Exact tetrahedron-vertex checks | 2,376 |
| Exact control-plane samples | 3,179 |
| Exact encoded machine transitions | 891 |
| Full global cells emitted for the 3-label example | 5,670 |
| Rational global contraction pair diagnostics | 250 |
| Rational homogeneity diagnostics | 250 |

For the three-label countdown program, the initial first counter is `n` and the second is zero. It reaches HALT after `2n+1` map steps and zero one step later. Its scale is `a=1/232`.

| Initial counter `n` | HALT arrival | Zero arrival | Minimum `b` with `2^{-b}` below the halt flag | Largest coordinate denominator bit length observed |
|---:|---:|---:|---:|---:|
| 0 | 1 | 2 | 10 | 8 |
| 1 | 3 | 4 | 26 | 25 |
| 2 | 5 | 6 | 42 | 42 |
| 5 | 11 | 12 | 89 | 92 |
| 20 | 41 | 42 | 325 | 343 |
| 100 | 201 | 202 | 1,582 | 1,680 |

All exact assertions passed under Python 3.12.14 in the recorded run. The emitted global description has SHA-256 `9d299dfc5ea636a166f7530f63e39f25306fa92788d80942bba57431528b3256`. Timing is recorded as an execution fact, not a general runtime guarantee. No finite run demonstrates undecidability; that conclusion is supplied by the universal reduction. No proof-assistant certification is claimed.

## 12. Primary comparison and the exact incremental status

The important existing approaches are not bypassed by relabeling the problem.

**Classical continuous dynamical universality.** Blondel, Bournez, Koiran, and Tsitsiklis explicitly discuss the already known undecidability of point-to-point reachability, including reaching the origin, for continuous piecewise-affine and saturated-linear systems; their 2001 paper then establishes harder global stability/mortality results [R2]. Therefore the broad statement “a small continuous dynamical law can have an undecidable event” is not new. Homogenization followed by positive scaling is a natural way to turn an angular simulator into a contracting map; this report makes no claim that the observation was absent from earlier work.

**Special Bellman structure gives stronger positive results.** Varonka and Watanabe prove reachability decidability for their finite-state Bellman-operator class when the target is not the fixed point, or initial and target points are componentwise comparable, and resolve all cases in dimension two [R3]. Their conditions include monotone action structure absent here. Our construction does not settle their remaining higher-dimensional fixed-point question and should not be read as a result for those operators.

**Piecewise-linear neural representation.** The max–min representation used for the ReLU corollary is existing exact machinery [R4]. The neural conclusion is a rescaling consequence, not a claimed new representation theorem.

**What this completed package adds to the accumulated work.** The earlier fixed-law result leaves exact equality unresolved while completing positive-margin certification. This package supplies a full explicit family proving that no universal algorithmic repair of that equality boundary is possible under global contraction alone, even after the entire rational law is revealed. It also gives the exact source of the obstruction, the finite global compiler, the contraction proof, the per-step precision cost, and the efficient positive-margin/approximate-value counterpart. These deductions sharpen what the earlier certificate can promise; they do not replace the acquired first-event operation, and they do not independently establish a civilisation-changing practical capability.

### References

[R1] Andrej Dudenhefner, *Certified Decision Procedures for Two-Counter Machines*, FSCD 2022, Theorem 6 and the instruction definitions preceding it. [Primary proceedings page](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSCD.2022.16); [full primary PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol228-fscd2022/LIPIcs.FSCD.2022.16/LIPIcs.FSCD.2022.16.pdf).

[R2] Vincent D. Blondel, Olivier Bournez, Pascal Koiran, and John N. Tsitsiklis, *The Stability of Saturated Linear Dynamical Systems Is Undecidable*, Journal of Computer and System Sciences 62 (2001), 442–462, DOI 10.1006/jcss.2000.1737. [Author-hosted primary PDF](https://web.mit.edu/~jnt/www/Papers/J085-01-vb-satur.pdf). The introduction explicitly distinguishes point-to-point reachability from the global properties proved in that paper.

[R3] Anton Varonka and Kazuki Watanabe, *On Piecewise Affine Reachability with Bellman Operators*, MFCS 2025, DOI 10.4230/LIPIcs.MFCS.2025.92. [Primary proceedings page](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2025.92); [full author manuscript](https://arxiv.org/html/2502.19923v2).

[R4] Sergei Ovchinnikov, *Max–Min Representation of Piecewise Linear Functions*, arXiv:math/0009026, Theorem 4.1. [Primary manuscript](https://arxiv.org/abs/math/0009026); [full PDF](https://arxiv.org/pdf/math/0009026).

The primary comparison also checked Blondel and Tsitsiklis, *Complexity of Stability and Controllability of Elementary Hybrid Systems*, Automatica 35 (1999), 479–489, [author-hosted PDF](https://web.mit.edu/jnt/www/Papers/J071-99-vb-hybr.pdf). Its general piecewise-linear constructions are not interchangeable with the globally continuous Euclidean contraction proved here. Failure to locate an identical prior statement is not evidence of priority.
