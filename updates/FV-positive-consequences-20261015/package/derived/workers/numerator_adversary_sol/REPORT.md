# Independent numerator adversary and alternate representation

**Status: valid exact reduction and decisive obstructions; no new foundational capability or performance advantage established.**

The occupation numerator can be preserved without reconstructing every committor value: retain a positive boundary mass-load vector alongside the classical Schur complement. This is precisely the information supplied by graph transformation's waiting-time correction, so it is not a new solution to directional mean passage times. A smaller contract containing only capacity and total mass is insufficient even if the capacity is exact. Matching the complete boundary mass-load vector still gives no general deadline guarantee.

This worker independently constructed the statements below before comparing with another worker. No other worker's output was read. All writes are confined to this directory. Capital was read at `a6190a1083f688a7e4bf64adbc5244ef150ff2c4`. The incoming `sources/computation_pasted.txt` was treated as data, not as an independently reproduced benchmark. Memory supplied the user preference for scoped claims and complete costs; no theorem premise was imported from memory.

## 1. Exact input/output contract

Let a finite connected reversible CTMC be supplied through positive masses `w_i` and symmetric conductances `c_ij=w_i q_ij`. Every edge and mass is assumed known unless an explicitly weaker oracle is introduced below. Let `L` be its conductance Laplacian, `s != t`, and `h_s=1,h_t=0,(Lh)_i=0` otherwise. Write

\[
 C=h^TLh,\quad N=\sum_i w_i h_i,\quad Z=\sum_iw_i,
 \qquad T_{st}=\mathbb E_s\tau_t=N/C.
\]

These are singleton first-hit means. A deadline output is, for example, `S_s(T)=P_s(tau_t>T)` to an explicit relative or absolute tolerance. Mean and deadline contracts are distinct. No physical network acquisition, rate calibration, unseen-channel bound, molecular validation, or full LJ38 calculation was performed here.

## 2. Exact mass transport is the sufficient mean contract

Choose retained vertices `R` containing `s,t` and eliminated vertices `I`. Every component of `I` touches `R`, so `A=L_II` is a nonsingular symmetric M-matrix. Define

\[
 H=-A^{-1}L_{IR},\qquad
 K=L_{RR}-L_{RI}A^{-1}L_{IR},\qquad
 m=w_R+H^T w_I.
 \tag{2.1}
\]

The inverse is nonnegative; `H >= 0` and `H 1 = 1`. Consequently `m>0` and `sum(m)=Z`. The harmonic extension is `h_I=Hh_R`, giving the exact identity

\[
 \boxed{N=m^Th_R.}\tag{2.2}
\]

**Stronger mean statement.** The reversible CTMC with conductance Laplacian `K` and masses `m` preserves every mean first-hit time from a retained vertex to any nonempty target subset of `R`. It also preserves the corresponding boundary hitting probabilities.

Proof: for a target set `B subset R`, the original mean vector solves `Lu=w` off `B`, with `u_B=0`. Eliminate `I` in this Poisson equation. The retained equation is `Ku=m` off `B`; this is exactly the reduced CTMC's first-hit Poisson equation. Boundary probabilities follow by the same elimination with zero right-hand side. This statement concerns these means and probabilities, not the passage-time law.

For one eliminated vertex `k`, `d_k=sum_j c_kj`, this is the positive local update

\[
 c'_{ij}=c_{ij}+\frac{c_{ik}c_{kj}}{d_k},\qquad
 \boxed{w'_j=w_j+\frac{c_{kj}}{d_k}w_k.}\tag{2.3}
\]

No full microscopic committor reconstruction is needed. But acquiring `K,m` can cost as much as exact graph transformation; (2.1) is not an unexplained free oracle.

**One-boundary exception.** If an eliminated connected component meets `R` at only `r`, all its harmonic values equal `h_r`. Its full mass can be added to `w_r` without acquiring its internal conductance values. The only required dynamical premise is the supplied topology/connectivity and positivity ensuring eventual exit. Identifying/verifying that premise and summing its masses still costs input access. Any equally informed comparator can use this shortcut. A tree of arbitrarily slow, heavy dangling leaves is therefore an easy exact-mean case, rather than a reason to claim new numerical power.

For a general component `D` with boundary `B`, the necessary load is

\[
 \mu_b=\sum_{i\in D} w_i\Pr_i(X_{\tau_B}=b),\qquad
 \mu\ge0,\quad \sum_b\mu_b=W_D.
 \tag{2.4}
\]

This is the unique linear boundary functional representing the component's occupation numerator for every boundary potential: `N_D=mu^T h_B`. Its total mass alone supplies one scalar constraint on this vector, not its allocation.

The exact mean-preserving reduction is prior capability. The original graph-transformation paper gives an exact transition/waiting-time method assuming the full state/transition database [Trygubenko and Wales, 2006](https://arxiv.org/abs/cond-mat/0603830). PyGT documents preservation of mean first passage times and branching probabilities, including block elimination with stable single-node fallback [PyGT](https://pygt.readthedocs.io/en/latest/), [GT documentation](https://pygt.readthedocs.io/en/latest/GT.html). The present formulas are the reversible conductance/load form of that capability, not a novelty claim.

## 3. Exact response and total mass cannot determine the numerator

Take `w_s=w_t=1,w_z=M`, a direct edge `c_st=c0>0`, and edges `c_sz=a,c_zt=b`. For any `p in (0,1)` and fixed `k>0`, choose

\[
 a=\frac{k}{1-p},\qquad b=\frac{k}{p}.
\]

Then `h_z=p` and eliminating `z` produces the same edge `ab/(a+b)=k` for every `p`. Hence even the **entire exact two-terminal Schur complement** and `Z` are fixed, while

\[
 C=c_0+k,\quad Z=M+2,\quad
 \boxed{T_{st}=\frac{1+Mp}{c_0+k}.}\tag{3.1}
\]

The possible means fill the open interval `(1/(c0+k),(M+1)/(c0+k))`. The supremum of their ratio is `M+1`, unbounded over supplied masses. Exact Kron response plus total hidden mass therefore cannot certify a relative directional mean. The missing datum is the oriented mass split `(Mp,M(1-p))`.

**Both connections can be weak, with identical deletion budgets.** Alternatively set `a=delta p,b=delta(1-p)`. The pair `p,1-p` has identical `C=c0+delta p(1-p)`, `Z`, and total removable conductance `S=delta`. For

\[
 c_0=1,\quad M=10^{12},\quad\delta=10^{-12},\quad p=10^{-12},
\]

the two numerators are exactly `2` and `10^12`, and the directional means have ratio exactly

\[
 \boxed{5\times10^{11}.}
\]

Their capacity differs from the direct edge by less than `10^-24`. A tiny conductance deletion certificate cannot certify a tiny occupation error. `results.json` records the common exact rational capacity, common partition mass, deleted-conductance budget and both means.

## 4. A sharp mass-boundary envelope

Suppose exact reduced boundary values `h_R` are known, but a component's load vector `mu` is not. Positivity gives

\[
 W_D\min_{b\in B}h_b\ \le N_D\le
 W_D\max_{b\in B}h_b.
\tag{4.1}
\]

Summing over components yields

\[
 N_- =w_R^Th_R+\sum_DW_D\min_{B_D}h,
 \quad N_+=w_R^Th_R+\sum_DW_D\max_{B_D}h.
\tag{4.2}
\]

The width is exactly the supplied mass-weighted boundary oscillation

\[
 \boxed{N_+-N_-=\sum_DW_D\operatorname{osc}_{B_D}h.}\tag{4.3}
\]

For two boundaries this envelope is universally sharp even with an exact fixed component Schur response: the family in section 3 takes `p` arbitrarily close to either endpoint while preserving that response. An isocommittor boundary gives zero width; a one-boundary component is a special case. Approximate isocommittor geometry can therefore justify mass aggregation, but its certified oscillation must be acquired rather than inferred from edge weakness.

Certified intervals `ell_r <= h_r <= u_r` can replace exact values: use `sum w_r ell_r + sum W_D min ell_b` for the lower bound and `sum w_r u_r + sum W_D max u_b` for the upper bound. These must enclose the *original* boundary values; a capacity-accurate minor does not automatically provide that premise.

With an independently valid `0<C_-<=C<=C_+`, obtain

\[
 T_{st}\in[N_-/C_+,N_+/C_-],\qquad
 \frac{T_+}{T_-}=\frac{N_+}{N_-}\frac{C_+}{C_-}.
\tag{4.4}
\]

This is a usable conservative output contract, not a theorem that the envelopes are narrow on physical networks. Obtaining exact boundary values through full Schur reduction retains its cost.

## 5. Adjoint/residual certification and its weak-mass obstruction

Let `I=V minus {s,t}`, `A=L_II`, and choose any trial `g` with terminal values `1,0` and any trial adjoint `v` on `I`. Set

\[
 r=(Lg)_I,\quad q=w_I-Av,\quad
 \widehat N=w^Tg-v^Tr.
\]

Because `h_I-g_I=-A^-1 r`,

\[
 N-\widehat N=-q^TA^{-1}r.\tag{5.1}
\]

If `j` is any edge flow whose divergence equals `q` at interior vertices, with arbitrary terminal discharges, let `D_q=sum_e j_e^2/c_e`. Thomson minimization and Cauchy-Schwarz give the goal certificate

\[
 \boxed{|N-\widehat N|\le
 \sqrt{D_q\,[\mathcal E(g)-C_-]}.}\tag{5.2}
\]

Here `C_-` is any valid lower capacity bound. The energy identity is `r^TA^-1r=E(g)-C`. A spanning-tree transport flow can be built by summing signed source loads down a rooted tree in linear time after the tree is supplied. This certificate can be checked with a graph pass, but acquiring a useful adjoint/flow may require a second solve and full input. It is classical goal-oriented primal/dual estimation, not a newly discovered variational principle.

The section-3 weak node exhibits why an energy-only argument fails. Its grounded adjoint matrix is the scalar `A=delta`, so

\[
 w_I^TA^{-1}w_I=M^2/\delta.
\]

The trial `g_z=1/2` has excess energy at most `delta/4` over the direct-edge lower bound. Their product still permits an occupation error `M/2`, independent of how small `delta` is. The inverse-mass norm cancels the apparent weak-edge gain. An exact local adjoint removes this uncertainty but acquires the same exit-allocation information used by positive load elimination.

The residual correction is signed: subtracting two terms of order `M` can be numerically dangerous when the true numerator is order one. Positive mass transport is therefore the stronger baseline for these adversarial cases. A failed naive solve or poorly implemented residual correction would not establish an advantage over stableGT.

## 6. Exact means do not preserve deadlines

Use `w_s=w_t=1,w_z=M`, edges `c_st=1,c_sz=delta>0`, and no `zt` edge. Then

\[
 C=1,\quad N=M+1,\quad Z=M+2,\quad
 \mathbb E_s\tau_t=M+1,\quad \mathbb E_t\tau_s=1
\]

for every `delta`. The exact mass-load reduction produces two states with source mass `M+1`, so its source passage law is exponential with mean `M+1`. The original transient generator on `(s,z)` is

\[
 Q_T=\begin{pmatrix}-(1+\delta)&\delta\\
 \delta/M&-\delta/M\end{pmatrix}.
\]

Its Laplace transform and variance are

\[
 F_s(\lambda)=
 \frac{\lambda+\delta/M}
 {\lambda^2+\lambda(1+\delta+\delta/M)+\delta/M},
 \qquad
 \operatorname{Var}_s\tau_t=(M+1)^2+2M^2/\delta.
\tag{6.1}
\]

For fixed `M`, as `delta -> 0` the law converges to `Exp(1)` despite its constant larger mean; the rare long visits destroy uniform integrability. As `delta -> infinity`, the law converges to `Exp(mean M+1)`.

The executed fixture `M=10^6,delta=10^-12,T=100` gives

| Quantity | Value |
|---|---:|
| Exact directional mean | `1000001` |
| Mean-preserving two-state survival at `T` | `0.9999000050998232` |
| Original three-state survival, closed form | `9.999999999989997e-13` |
| Original survival, SciPy `expm` | `9.99999999999e-13` |
| Ratio of reduced to original survival | `9.999000051008234e11` |

The two numerical evaluations check the closed-form model; neither is a rounding-certified molecular prediction. This is not a failure of PyGT's stated mean contract. Its documentation separately provides first-passage distributions through eigendecomposition [PyGT statistics](https://pygt.readthedocs.io/en/latest/stats.html).

**A positive mean-plus-deadline contract when branch entry is rare.** There is a useful alternative to forcing both outputs into one reduced CTMC. Suppose every discarded component meets a retained core at a single root, and no target lies inside a discarded component. Aggregate all its mass for the exact mean computation, as in section 2. For the deadline computation instead retain the core's original masses, and record the branch-entry hazards

\[
 \lambda_r=\frac{\sum_{z\text{ in discarded components}}c_{rz}}{w_r}.
\]

The trace path on the core has exactly the original core dynamics; each branch excursion returns to the same root and adds a nonnegative delay. A pathwise operational-clock coupling therefore gives `tau_original >= tau_core`. The two times agree unless a branch-entry clock rings before the core's target hit. Thus, with `Q_core,B` the target-killed core generator and initial core distribution `alpha`,

\[
 0\le S_{\rm original}(T)-S_{\rm core}(T)\le p_T,
 \quad
 p_T=\int_0^T\alpha e^{(Q_{\rm core,B}-\operatorname{diag}\lambda)u}\lambda\,du.
 \tag{6.2}
\]

Only the first branch-entry race is used, so no excursion-duration distribution or internal branch rates are required. The supplied one-boundary topology, aggregate masses and entry hazards remain indispensable. This is a classical coupling/killing construction, not a novelty claim.

For one source root of mass `w_s`, a direct target edge `c0`, aggregate dangling mass `W` and total branch conductance `Delta`, the reduced output contract is

\[
 \mathbb E_s\tau_t=(w_s+W)/c_0,\quad
 e^{-c_0T/w_s}\le S_s(T)\le
 e^{-c_0T/w_s}+\frac{\Delta}{c_0+\Delta}
 (1-e^{-(c_0+\Delta)T/w_s}),
 \tag{6.3}
\]

with the upper endpoint clipped at one. This returns an exact mean and a valid deadline envelope using different clocks for the two computations. It does not assert that one two-state CTMC realizes both. On the same `M=10^6,delta=10^-12` fixture at `T=20`, the deadline lower endpoint is about `2.06115362244e-9` and the upper endpoint about `2.06215362244e-9`: relative width `0.0004851652`, while the mean remains exactly `1000001`. At `T=100` the same absolute bound is useless for relative accuracy. This states the actual acceptance gate: `p_T <= epsilon S_core(T)` is sufficient for a multiplicative deadline enclosure. Tiny edge conductance alone supplies no uniform relative-tail guarantee.

For a general core, computing `p_T` and `S_core` still requires reduced killed/matrix-exponential operations. Reading a full explicit graph to establish the one-boundary structure costs `O(n+m)`; a supplied aggregate interface avoids those internal-rate queries and is equally available to the comparator.

**Executed outward arithmetic for the scalar hybrid contract.** The final receipt also contains a separate `hybrid_rational_arithmetic_certificate`. For `x>=0`, set `L=sum_(j=0)^K x^j/j!` and `R=[x^(K+1)/(K+1)!]/[1-x/(K+2)]`, where `K+2>x`. The positive series and geometric tail prove `exp(-x) in [1/(L+R),1/L]`. These endpoints were calculated with exact rational arithmetic, then converted to 60-digit decimal endpoints using outward-rounded division. Degrees 128 and 256 were used at the two deadlines. No floating exponential assumption is used in this enclosure. At `T=20` the certified interval is

\[
 [\,2.06115362243855782796594038015582097637580727559910369297224\times10^{-9},
 \quad2.06215362243649567434354510755392579019408818365315195792445\times10^{-9}\,],
\]

with endpoint ratio below `1.000486`. The exact mean `1000001` is returned separately. At `T=100` the certified relative interval remains extremely wide, as predicted. This arithmetic certifies the stated finite analytic contract conditional on the supplied graph structure and coefficients; it is not physical validation, formally verified software, or a performance win over the directly available two-by-two exact passage calculation.

**Unbounded exact representation order even for dangling leaves.** Attach `k` leaves of masses `w_j` to `s`, retaining the direct `st` edge, and write `r_j=c_sj/w_j`. Eliminating the leaves in the Laplace equation yields the scalar dynamic-mass representation

\[
 F_s(\lambda)=\frac1{
 1+\lambda\left[1+\sum_{j=1}^k
 \frac{w_jr_j}{\lambda+r_j}\right]}.
\tag{6.4}
\]

Every mean is determined by the total leaf mass, but the law retains the rate distribution. If the positive `r_j` are distinct, multiplication by `P(lambda)=product_j(lambda+r_j)` yields a denominator of degree `k+1`. At each root `-r_j` of `P`, the denominator equals `-w_j r_j^2 product_(l!=j)(r_l-r_j)`, which is nonzero. Thus no numerator/denominator cancellation occurs. Any exact finite CTMC realization of this first-passage law requires at least `k+1` transient states. A scalar memory function can represent it, but evaluating its unstructured sum costs `O(k)` and acquiring it requires those rates. A finite-horizon approximate compression would need a separate error theorem, which is not supplied by the mean contract.

## 7. Precision: positivity strengthens the comparator

An undirected spanning-tree/forest formula is

\[
 T_{st}=\frac{
 \sum_{F\in\mathcal F_{st}} W(S_F)\prod_{e\in F}c_e}
 {\sum_{T\in\mathcal T}\prod_{e\in T}c_e}.
\tag{7.1}
\]

Here `F` ranges over spanning two-component forests separating `s,t`, `S_F` is its `s` component, and `W(S_F)=sum_(i in S_F)w_i`. This is a classical matrix-tree/Green-function identity, not a proposed enumeration algorithm. It follows by expanding the cofactors of the grounded inverse in `u=L_(V minus t)^-1 w`; the cofactor indexed by `s,i` sums precisely forests with `s,i` on the side opposite `t`. Tree/forest first-passage representations are established in the primary literature [Pitman and Tang, 2018](https://arxiv.org/abs/1603.09017).

If every conductance is perturbed multiplicatively by a factor in `[1-eta,1+eta]` and every mass by a factor in `[1-zeta,1+zeta]`, then, for `n>=2`, positivity and the degrees `n-2,n-1` give

\[
 \frac{(1-\zeta)(1-\eta)^{n-2}}{(1+\eta)^{n-1}}
 \le \frac{T'_{st}}{T_{st}}\le
 \frac{(1+\zeta)(1+\eta)^{n-2}}{(1-\eta)^{n-1}}.
\tag{7.2}
\]

This is a data-perturbation result, not an automatic forward-rounding theorem for an arbitrary implementation. It shows that relative coefficient accuracy of order `epsilon/n`, with exponent range represented correctly, can protect the mean independently of the rate dynamic range. Positive star-mesh/load arithmetic can be enclosed with directed intervals; cancellation-prone formulas or underflowing ordinary floats need separate treatment. Physical uncertainty in coefficients and missing edges remains outside an arithmetic certificate.

## 8. Complete costs and an acquisition lower bound

For explicit input of total encoding length `L_in`, worst-case reading/verification costs `Omega(L_in)` bits. Connected-component detection and mass summation are `O(n+m)` arithmetic/input work and storage, or streaming plus an adjacency/union-find representation. A supplied one-boundary aggregate `(root,total mass)` eliminates the need to acquire internal rates for means, but this is a stronger interface promise credited equally to the comparator.

General positive elimination costs `O(sum_k d_k^2)` arithmetic operations, where `d_k` is the degree at elimination, and may fill to `O(n^2)` storage and `O(n^3)` arithmetic. Tree leaf elimination is linear. Exact block elimination reuses the same factorization for the mass right-hand side; it is not a cheap operation solely because its final vector is short. Several reward loads add right-hand-side solves. Bit costs depend on coefficient encoding, precision, exponent range, integer growth and fill. With `p`-bit arithmetic each positive update must pay its arithmetic cost and any interval certification overhead; an `O(log(n/epsilon))` mantissa-precision implication of (7.2) does not erase exponent or input-accuracy costs.

The mass-boundary envelope costs a graph pass once the component boundaries, masses and certified retained potentials are available. The latter may already cost a full reduced solve or exact Schur preparation. The adjoint certificate requires the primal values, adjoint trial, all residual coefficients and a flow; a useful certificate can cost another full solve. Exact deadline elimination generally needs frequency-dependent memory or additional states, not just a mean load. Parsing, normalization, ordering, rates/masses, numerical enclosures and output reconstruction are all charged.

**A simple access lower bound.** Promise `n` leaves, each of mass `M`, attached by conductance `delta` to either `s` or `t`, with direct `st` conductance one and terminal masses one. Supply `C=1,Z=nM+2` for free. An endpoint oracle reveals where a queried leaf is attached. Distinguish (a) every leaf is attached to `t`, with `T_st=1`, from (b) exactly one unknown leaf is attached to `s`, with `T_st=M+1`. A deterministic algorithm must inspect every leaf in the worst case. For a uniform random special leaf and equal prior between the cases, `k` distinct queries have error at least `(1-k/n)/2`; success at least `2/3` requires `k>=n/3`. Arbitrarily small `n delta` changes none of this. Thus capacity and partition-mass supply cannot remove worst-case acquisition of heavy-leaf orientation. One-pass graph transformation is already optimal up to constants for this oracle family.

No end-to-end scientific speed comparison, energy measurement or memory-usage comparison was executed in this worker. The theorem gives no general advantage over equally informed stable graph transformation/PyGT. It can identify a useful contract or structural shortcut when that information is physically accessible.

## 9. Executed evidence and reproducibility

`check_models.py` uses exact `fractions.Fraction` arithmetic to check 100 independently seeded small connected graphs (3 to 8 vertices, conductance decimal scales from `10^-8` to `10^8`, mass scales from `10^-5` to `10^5`). All passed:

- 100 positive-elimination invariance checks, including six ordered source/target pairs among three retained vertices and all retained initial vertices;
- 100 mass-boundary envelope checks;
- 100 goal-adjoint/transport-flow certificate checks;
- 100 coefficient-perturbation checks;
- 63 explicit tree/forest sum identities on sufficiently small sparse cases.

These finite tests support implementation consistency; the proofs above provide the mathematical statements. They are not scientific benchmark cases.

The unmodified `PyGT/GT.py` was fetched from commit `fa0e106958d9948209daff04360290d50de82572`, SHA-256 `724658303c878a474aee2a8ab7ba2722116deb1f8595052cf4de90092b3b8446`, with its MIT license retained. `vendor/SOURCE.json` records the exact source URLs and hashes. It was executed on the two weak unequal-hitting models and on three one-boundary models with `delta=10^-12,1,10^12`. All five means matched the exact rational oracle to at most `2.22e-16` relative float error. This executes an actual stableGT implementation on the decisive examples; it does not benchmark large-network performance or provide a float-rounding enclosure. The source's block path and cancellation-avoiding single-node path were also read [pinned PyGT source](https://github.com/tomswinburne/PyGT/blob/fa0e106958d9948209daff04360290d50de82572/PyGT/GT.py).

Runtime used the shared environment: Python 3.14.3, NumPy 2.3.5, SciPy 1.17.0. No packages were installed and no environment/configuration edits were made. The recorded submillisecond fixture times include the exact small oracle and exclude source acquisition/import; they are explicitly not a performance comparison.

Reproduce without a network request:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-positive-consequences-real-capabilities-v1/.venv/bin/python /Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-positive-consequences-real-capabilities-v1/workers/numerator_adversary_sol/check_models.py
```

`results.json` is the complete executed receipt. The decisive next gate is an acquired physical network/output contract where a certified mass-aware approximation or finite-horizon memory compression demonstrably costs less than matched stableGT, spectral/Schur/Krylov passage methods, with the same rate/mass information and accuracy. This worker does not claim that gate has been crossed.
