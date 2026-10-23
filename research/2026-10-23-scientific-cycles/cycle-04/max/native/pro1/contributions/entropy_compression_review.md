# Focused independent review: conserved charge, entropy flow and arbitrary-rank compression

Reviewer: `/root/coherent_stability`  
Date: 22 October 2026 (Brisbane)  
Scope: the actual `ENTROPY_AND_SCOPE.tex`, equations E1--E10, using the model, initializer and corrected-drift definitions in `COHERENT_INPUT_ESCAPE.tex`. This review does not repeat the earlier corrector audit and does not certify `FINITE_BAND_ESCAPE.tex` or the subsequently inserted `IID_INFORMATION.tex` from their summaries.

## Verdict

**Internal mathematical acceptance of E1--E10 under the stated fixed iid input, actual `tau_pi`, finite-entropy and propagation assumptions.** No load-bearing gap was found in the charge conservation, treatment of correlated outputs, normalized tail entropy, exact head/tail mixture, or the comparison with arbitrary non-coordinate finite-rank projections.

The conclusion is substantial and precise: for a fixed qutrit iid input with entropy greater than `3/2`, at fixed `0<=beta<=1/8`, every asymptotically lossless finite-rank approximation of the averaged final bath from the actual `tau_pi` has exponentially growing rank. This closes subexponential-rank bath compression for this high-entropy iid route. It is not a capacity converse for arbitrary correlated codes.

Two wording repairs are recommended:

1. In E6, specify that the chosen `nu` obeys the stronger `nu>=3delta/2` bound valid on this angle interval. The weaker, still valid `4delta/5` drift bound would not alone yield the displayed `epsilon+delta/2` entropy coefficient. The proof itself already uses the correct stronger bound.
2. In the same-device pure-color counterexample F3, `span_{k<=n} S1^k P_{<=a}E` is spanned by vertex basis vectors. Its compression is a **non-radial coordinate compression**, not a non-coordinate compression. The example still correctly separates ballistic depth from information/rank growth.

For terminology, `H=L+C` is unbounded; it is a corrected depth with a bounded correction, not a bounded depth operator. The proof treats its domain correctly.

## 1. Charge conservation is exact, including the root

Let `N=|1><1|+|2><2|` on a port and let `L` be Fock depth. A basis state with a color input undergoes a child move: its bath depth increases by one and its output color number decreases from one to zero. An input zero at positive depth undergoes the reverse change. At either vacuum seed, the `R` operation exchanges seeds with color number zero and depth zero unchanged.

Hence the unitary `U` preserves each eigenspace of the nonnegative self-adjoint charge

\[
 T=I_{\rm port}\otimes L+N\otimes I_E.
\]

This proves more than a formal core commutator: `U` commutes with the spectral projections of `T`, preserves its domain and commutes strongly with it. The linear combination `V=alpha U+i beta I` has the same property. For `n` slots, each interaction commutes with

\[
 T_n=L+\sum_{j=1}^nN_j,
\]

because it also commutes with the unused ports' number operators. Thus the whole ordered block conserves `T_n` exactly.

For finite initial mean depth, conservation also proves finite final mean depth: the non-bath part of `T_n` is bounded between zero and `n`. In particular, no unbounded-expectation subtraction occurs in E3--E5.

Writing `q=rho_00` and `q'_j=<0|omega_j|0>` gives the sign

\[
 \operatorname{Tr}L(\tau_j-\tau_{j-1})
 =(1-q)-(1-q'_j)=q'_j-q.
\]

The signs in E3 are therefore correct. The actual bath remains correlated with earlier outputs, but the next input of `rho^{tensor n}` is independent of both the current bath and those earlier outputs. Its bath marginal evolves by the stated fixed channel `Phi_rho`. Equivalently, the summed equality follows from the whole-block charge without asserting any output independence.

## 2. All entropies used are finite

For fixed port density `rho`, purify it in a three-dimensional system and retain that purifier together with the three-dimensional outgoing port. This is a Stinespring environment of dimension at most nine for the reduced bath channel. An isometry preserves input entropy, and the environment entropy is at most `log2 9`. Consequently

\[
 S(\Phi_\rho(\xi))\le S(\xi)+\log_2 9
\]

whenever `S(xi)` is finite. Iterating establishes finite bath entropy after every finite number of uses. Each output port and the finite collection of all output ports automatically have finite entropy as well.

The initial reduced state of all ports and bath is `rho^{tensor n} tensor tau_0`. Even if one analytically purifies the input, its reduced ports-plus-bath evolution is still a unitary evolution of this density. Thus its joint entropy is exactly

\[
 nS(\rho)+S(\tau_0).
\]

No physical purifier is being supplied for free by this entropy calculation, and no communication operation is claimed from this averaged-state identity.

## 3. Entropy flow retains all outgoing correlations

For a qutrit density `omega` of zero probability `q'`, pinching the zero/color sectors and then maximizing the two-dimensional color entropy gives

\[
 S(\omega)\le h_2(q')+1-q'\le2-q'.
\]

Apply ordinary subadditivity to the entire output `B_1...B_n`:

\[
 S(B_1...B_n)\le\sum_j S(\omega_j)
 \le n(2-q)-\operatorname{Tr}L(\tau_n-\tau_0).
 \tag{R1}
\]

No equality with a sum of independent output entropies is assumed. Correlations can only lower the joint entropy relative to this upper bound.

Subadditivity across all output ports versus the bath then gives

\[
 nS(\rho)+S(\tau_0)
 \le S(B_1...B_n)+S(\tau_n).
\]

Combining with (R1) proves E5 with all signs as stated:

\[
 S(\tau_n)\ge S(\tau_0)+n[S(\rho)-2+q]
               +\operatorname{Tr}L(\tau_n-\tau_0).
\]

If `H=L+C`, `||C||<=M`, has corrected drift at least `nu I`, then finite mean depth permits telescoping and

\[
 \operatorname{Tr}L(\tau_n-\tau_0)\ge n\nu-2M.
\]

This proves E2. With `delta=1/2-q` and `epsilon=S(rho)-3/2`, its rate coefficient is exactly

\[
 c_\rho=\epsilon-\delta+\nu.
\]

For `beta<=1/8`, the previously checked spectral-window bound supplies `nu>=3delta/2`, so `c_rho>=epsilon+delta/2>0`. The correction norm `M` may depend on the fixed input and angle but is constant in `n`, which is sufficient. No initializer is varied to obtain this bound.

A direct additional consequence of (R1), without a new assumption, is

\[
 \limsup_n\frac{S(B_1...B_n)}n
 \le2-q-\nu\le\frac32-\frac\delta2.
\]

This is an output-entropy statement for the fixed iid input, not a bound on every code's output entropy.

## 4. Exact initializer tail: mass and normalized entropy

In the actual two-seed representation, each eigenvalue of `tau_pi` at a vertex of depth `ell` is

\[
 \lambda_\ell=\frac13\,6^{-\ell},
\]

with multiplicity `2^{ell+1}`. The depth distribution is therefore

\[
 \Pr(L=\ell)=\frac23\,3^{-\ell},\qquad
 \Pr(L>a)=3^{-(a+1)}.
\]

Its mean depth is `1/2`, and

\[
 S(\tau_\pi)=\log_2 3+\frac12\log_2 6.
\]

Let `zeta_{0,a}` be the normalized tail at depths larger than `a`. At depth `a+1+k`, its eigenvalues are

\[
 \frac{(1/3)6^{-(a+1+k)}}{3^{-(a+1)}}
 =2^{-(a+1)}\,\frac13\,6^{-k}.
\]

Every such eigenvalue has `2^{a+1}` times the multiplicity of the corresponding depth-`k` eigenvalue of `tau_pi`. Thus the normalized tail has exactly the spectrum of

\[
 \frac{I_{2^{a+1}}}{2^{a+1}}\otimes\tau_\pi,
\]

and consequently

\[
 \boxed{S(\zeta_{0,a})=a+1+S(\tau_\pi).}
 \tag{R2}
\]

This calculation retains the original two seed vertices. It shows why the extra entropy is `a+1` color bits; there is no missing or duplicated seed bit.

## 5. The analytic head/tail decomposition does not change the physical initializer

Choose `a_n=ceil(log_3(n+1))` and `u_n=3^{-(a_n+1)}`. Then

\[
 0<u_n\le\frac1{3(n+1)}.
\]

Because the actual initializer is diagonal in depth, it has the exact convex decomposition

\[
 \tau_\pi=(1-u_n)\sigma_{0,n}+u_n\zeta_{0,n}.
\]

Linearity of the unchanged `n`-step channel gives E8 exactly. This is an analytic decomposition of one fixed physical initializer. Neither component is physically prepared, and no projection or successful outcome is credited.

Every one-step bath coefficient changes depth by at most one, including the depth-zero root exchange. Therefore the evolved head `sigma_n` is supported in

\[
 P_n=P_{\le a_n+n},\qquad
 D_n=\operatorname{rank}P_n=2(2^{a_n+n+1}-1),
\]

with `log2 D_n=n+O(log n)`.

Applying the finite-environment entropy bound to the normalized tail and using (R2) gives

\[
 S(\zeta_n)\le a_n+1+S(\tau_\pi)+n\log_2 9.
\]

The entropy of the binary mixture is at most its average component entropy plus `h2(u_n)`, so

\[
 S(\tau_n)\le S(\sigma_n)+e_n,
\]

where

\[
 e_n=h_2(u_n)+u_n[a_n+1+S(\tau_\pi)+n\log_2 9]=O(1)=o(n).
 \tag{R3}
\]

Thus E9 has a valid, explicitly controlled remainder. In particular, the small tail cannot hide a linear entropy contribution here. That is an additional fact supplied by the actual initializer and finite environment; it would not follow from trace closeness alone.

## 6. Arbitrary non-coordinate projections: the range comparison is valid

Let `Q_n` be any finite-rank orthogonal projection, of rank `k_n`, such that `Tr(Q_n tau_n)->1`. It need not commute with `L`, `P_n` or `tau_n`.

From the exact positive mixture,

\[
 1-\operatorname{Tr}(Q_n\sigma_n)
 \le\frac{1-\operatorname{Tr}(Q_n\tau_n)}{1-u_n}\longrightarrow0.
 \tag{R4}
\]

Let `Qtilde_n` project onto `ran(P_n Q_n)`. This range is finite-dimensional and closed, and

\[
 \operatorname{rank}\widetilde Q_n\le\min(k_n,D_n).
\]

The positive contraction `P_n Q_n P_n=(P_n Q_n)(P_n Q_n)^*` has range contained in that subspace. Hence

\[
 0\le P_nQ_nP_n\le\widetilde Q_n.
\]

Since `sigma_n=P_n sigma_n P_n`,

\[
 \operatorname{Tr}(\widetilde Q_n\sigma_n)
 \ge\operatorname{Tr}(P_nQ_nP_n\sigma_n)
 =\operatorname{Tr}(Q_n\sigma_n).
 \tag{R5}
\]

Equations (R4)--(R5) give `v_n=1-Tr(Qtilde_n sigma_n)->0`. This is the necessary noncommutative comparison. Replacing `Q_n` by `P_nQ_nP_n` and pretending the latter was a projection would be invalid; the actual proof correctly uses its range projection.

## 7. The finite-dimensional entropy bound gives the claimed rank exponent

For all sufficiently large `n`, `k_n>=1`. Pinch `sigma_n` into the two orthogonal blocks defined by `Qtilde_n`. Pinching cannot decrease entropy in this finite-dimensional support. If `r_n=rank Qtilde_n`, the block entropy formula and maximal entropy in each block give

\[
 S(\sigma_n)
 \le h_2(v_n)+(1-v_n)\log_2 r_n
                   +v_n\log_2(D_n-r_n).
\]

Zero-mass/zero-dimensional blocks are omitted. Replacing `r_n` by `k_n`, and `D_n-r_n` by `D_n`, yields E10:

\[
 S(\sigma_n)\le1+\log_2 k_n+v_n\log_2D_n.
 \tag{R6}
\]

If `k_n>D_n`, the simpler bound `S(sigma_n)<=log2 D_n<=log2 k_n` supplies the same conclusion. Thus no hidden assumption that `Q_n` lies inside the finite head support is being made.

Because `log2 D_n/n->1` and `v_n->0`, (R3) and (R6) imply

\[
 \frac{S(\tau_n)}n\le\frac{\log_2 k_n}n+o(1).
\]

Combining with E6 proves

\[
 \boxed{\liminf_n\frac{\log_2\operatorname{rank}Q_n}n\ge c_\rho>0.}
\]

No speed of convergence of the lost mass is required: the finite-head logarithmic dimension grows only linearly, so any `v_n->0` is enough.

This also rules out approximation by arbitrary low-rank density matrices in vanishing full trace norm. If `omega_n` has support `Q_n`, then

\[
 1-\operatorname{Tr}(Q_n\tau_n)
 \le\frac12\|\tau_n-\omega_n\|_1.
\]

Conversely, a projection of mass at least `1-epsilon_n` gives a normalized projected density within full trace distance at most `2sqrt(epsilon_n)`. Thus the projection formulation captures vanishing-error finite-rank state approximation with the full/half norm factors explicit. It is not an unrestricted statement about arbitrary encoder/decoder channels without a reference-preservation requirement.

## 8. Reusable abstract form and why entropy alone fails

The proof supplies the following reusable interface. Suppose

\[
 \tau_n=(1-u_n)\sigma_n+u_n\zeta_n,
\]

where `u_n->0`, `sigma_n` has finite support dimension `D_n` with `log D_n=O(n)`, and

\[
 h_2(u_n)+u_nS(\zeta_n)=o(n).
\]

If `liminf S(tau_n)/n>=c>0`, every sequence of finite-rank projections capturing mass tending to one has lower rank exponent at least `c`. The proof is precisely (R3)--(R6). Here finite propagation and the exact `tau_pi` tail verify those hypotheses without changing the initializer.

A counterexample shows why the additional hypotheses cannot be omitted. On one fixed separable Hilbert space, choose an orthogonal projection `Pi_n` of rank `M_n=2^{n^2}`, orthogonal to `|0>`, and set

\[
 \xi_n=(1-1/n)|0\rangle\langle0|+\frac1n\frac{\Pi_n}{M_n}.
\]

Then

\[
 S(\xi_n)=h_2(1/n)+n,
 \qquad\langle0|\xi_n|0\rangle=1-1/n.
\]

A rank-one projection captures asymptotically all mass despite a positive linear entropy rate. In the head/tail view, `u_nS(zeta_n)=n`, violating the tail condition; in the entire-support view, `log D_n` is quadratic, violating the support-growth condition. Therefore a bare entropy lower bound or an unsupported infinite-dimensional continuity argument would not establish E7. The actual proof avoids this failure.

The supplied pure-color example F3 independently shows, on the same device, that ballistic depth need not force extensive entropy. Its polynomial-rank span is a thin non-radial coordinate subspace, as noted in the wording repair.

## 9. Scope and scientific status

The result concerns the averaged bath under one fixed product input `rho^{tensor n}` and the fixed actual `tau_pi`. It excludes an asymptotically lossless subexponential-rank final-bath projection for that ensemble, even if the projection is not diagonal in the vertex basis. It does not infer a lower bound on every logical code's environment information, exclude an exponentially small exceptional input subspace, or bound protocols exploiting temporal correlations or recovery with an extensive environment.

No new bath-return claim, free purifier, horizon-dependent initialization, successful-branch credit or physical device performance is implied. The capacity floor remains intact. The proof closes the intended high-entropy iid low-environment-compression route and supports the next temporally correlated operation without settling it.

This is a source-complete internal review, not external certification or an originality claim. The entropy tools are standard; the independently checked model-specific inputs are charge conservation, the corrected positive drift, finite propagation, and the exact stationary-initializer tail.

## 10. Observed resources

The review read and recomputed the actual E1--E10 derivations, with the exact initializer and charge definitions from the main source. No new numerical experiment or old audit replay was needed. Full inference, reading, discovery, energy and monetary totals were not independently metered. No purchase, hardware credit, outreach, sharing change or source upload was performed by this reviewer.

At a read checkpoint, `ENTROPY_AND_SCOPE.tex` was 12,042 bytes with SHA256 `d2247500b90ed14cfeace8038d56dbbbc90059ad73c8aaabc92c155c46aed3ef`, and `COHERENT_INPUT_ESCAPE.tex` was 18,367 bytes with SHA256 `ac3a3110116d708ce326a7214d6b1db291935a39ad6c2df25ecf638bd18bbf6f`. The owner may subsequently make the stated wording repairs or add separately reviewed material; this review's acceptance is specifically of the E1--E10 arguments reconstructed above.
