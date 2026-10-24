# A source-obtained record interface for a recurrent fast hidden controller

This is new scientific construction. Its executable is `fast_switching_event_kernel.py`; it does not recover any missing historical helpers. The retained scientific objects are `fast_switching_record_interface_24sites.json` and `fast_switching_record_posterior_24sites.json`. Numerical results are in `fast_switching_event_kernel_results.json`.

## 1. The operation and its conditions

The operation is an **unnormalized first-event likelihood operator**, followed when required by conditional state inference. It accepts an arbitrary joint input law of the hidden controller and all leaves. For a requested elapsed time and observed mark, it returns a positive product propagation followed by the exact marked guard/reset map, together with an entrywise relative certificate. The input law is a runtime argument. Neither independence of that law nor stationary initialization of the controller is assumed by the certificate.

Let a symmetric two-state controller \(C_s\in\{-1,+1\}\) switch at rate \(\nu>0\) in each direction. Let \(X_1,\ldots,X_n\) have independent finite silent generators \(Q_i\), unchanged by the controller. Independence here describes the generator, not the initial distribution. Marked reaction rules have nonnegative rates and specified reset maps. Let \(V(c,x)\) be the sum of the rates of **all** marked events, including marks other than the requested one. Before the first marked event, the full generator is the independent silent generator killed at rate \(V\).

Assume the source establishes

\[
\bar V(x)=\frac{V(+1,x)+V(-1,x)}2
       =d_0+\sum_i d_i(x_i),\qquad d_0,d_i\ge0,
\]

and obtains a finite bound

\[
h(x)=\frac{V(+1,x)-V(-1,x)}2,\qquad |h(x)|\le A.
\]

The phasewise hazards may be coupled on a connected graph. Only their stationary average has to be additive. In particular, a local multiplicative hazard is not being mistaken for a separable killed semigroup.

Write \(D_i=\operatorname{diag}(d_i)\), and let \(J_j\) be the complete nonnegative jump/reset matrix for the observed mark \(j\). It includes every source branch with that mark; the branch need not be observed. The proposed compact operator is

\[
\bar K_j(t)=e^{-d_0t}
 \left(P_C(t)\otimes_i e^{(Q_i-D_i)t}\right)J_j.
\tag{1}
\]

The true operator \(K_j(t)\) includes the original coupled phasewise killing. Its row sums and application normalizers are event-time **densities**, which need not be at most one. These objects are not asserted to form the first-event family of a conservative reduced marked CTMC. In particular, the killing in (1) is averaged, while the terminal marked jump is exact. A record calculation uses precisely the stated positive operators and their comparison bounds.

## 2. A controller-bridge inequality uniform over every silent leaf path

Fix any leaf path. Its centered killing becomes a measurable function \(h(s)\) with \(\lvert h(s)\rvert\le A\). Define the controller Feynman–Kac kernel

\[
U_{ab}(t)=\mathbb E_a\left[
 e^{-\int_0^t h(s)C_s\,ds}\,1_{\{C_t=b\}}\right],
\qquad
P_{ab}(t)=\frac{1+ab e^{-2\nu t}}2.
\]

For \(t>0\), all four free transition probabilities are positive.

### Upper comparison

Use the orthonormal mass/imbalance basis. The free generator is \(\operatorname{diag}(0,-2\nu)\); the centered potential has off-diagonal entries of absolute value at most \(A\). In the time-ordered expansion, the entrywise absolute value of every term containing at least one potential insertion is bounded by the corresponding term with constant nonnegative off-diagonal entries \(A\). Therefore

\[
\left|\widetilde U(t)-\operatorname{diag}(1,e^{-2\nu t})\right|
\le e^{tM}-\operatorname{diag}(1,e^{-2\nu t}),
\quad
M=\begin{pmatrix}0&A\\A&-2\nu\end{pmatrix}.
\tag{2}
\]

The right side is entrywise nonnegative. Conjugating back to the original basis bounds each absolute entry error by half the sum of its entries. Put

\[
d=\sqrt{\nu^2+A^2},\qquad E=e^{-2\nu t},\qquad
\lambda=d-\nu=\frac{A^2}{d+\nu},
\]

\[
S=(1+A/d)e^{\lambda t}+(1-A/d)e^{-(d+\nu)t}-1-E.
\tag{3}
\]

Then \(S\ge0\), \(\lvert U_{ab}-P_{ab}\rvert\le S/2\), and

\[
\frac{U_{ab}}{P_{ab}}\le 1+\frac{S}{1-E}.
\]

The pathwise bound \(e^{-\int hC}\le e^{At}\) gives a second upper bound. We use

\[
b(t)=\min\left\{e^{At},\ 1+\frac{S}{1-E}\right\}.
\tag{4}
\]

The stable formula for \(\lambda\) in (3) avoids subtracting nearly equal large numbers when the controller is fast.

### Lower comparison

The exact conditional mean under a free controller bridge is

\[
\mathbb E[C_s\mid C_0=a,C_t=b]
 =\frac{a e^{-2\nu s}+b e^{-2\nu(t-s)}}{1+ab e^{-2\nu t}}.
\tag{5}
\]

Its integrated absolute value is \(\tanh(\nu t)/\nu\) for equal endpoints and \(\tanh(\nu t/2)/\nu\) for opposite endpoints. Jensen's inequality consequently yields

\[
\frac{U_{ab}}{P_{ab}}
\ge \exp\left[-A\int_0^t
 \left|\mathbb E[C_s\mid a,b]\right|ds\right]
\ge a(t):=\exp[-A\tanh(\nu t)/\nu].
\tag{6}
\]

This argument uses no leaf rate, number of leaf jumps, modulus of continuity of \(h\), or stationary controller input. It applies to every bounded measurable \(h(s)\), including the random function generated by arbitrarily fast leaf trajectories.

## 3. The all-input event-operator theorem

For every fixed leaf path, multiply the bridge comparison by its nonnegative mean-killing weight \(e^{-\int\bar V}\). Integrate over the independent silent leaf path measures, retaining their endpoints. Because the bounds are uniform over those paths,

\[
a(t)\,e^{-d_0t}\left(P_C(t)\otimes_i e^{(Q_i-D_i)t}\right)
\le e^{t(Q_{\rm silent}-V)}
\le b(t)\,e^{-d_0t}\left(P_C(t)\otimes_i e^{(Q_i-D_i)t}\right)
\tag{7}
\]

entrywise. Right multiplication by the exact nonnegative \(J_j\) preserves the inequality:

\[
\boxed{a(t)\bar K_j(t)\le K_j(t)\le b(t)\bar K_j(t).}
\tag{8}
\]

This is an operator statement. It therefore applies to every joint input distribution, including controller/leaf correlation, correlations among leaves, and correlations with a spectator historical variable on which the operation acts as the identity. Storage of that arbitrary input and contraction against it are separate questions; (8) does not promise that every input has a compact representation.

Structural zero columns produced by a reset are preserved by the same exact \(J_j\). There is no division by a rare output coordinate or a rare observation likelihood in (8).

## 4. Obtaining the conditions directly from the compact rule source

The new `compile_source` pass accepts the existing Boolean guarded-rule IR, with one Boolean controller at site 0. It checks autonomous symmetric controller dynamics, single-site silent leaf writes, and exact equality of the two phase-specific leaf generators. The numerical adapter currently requires positive binary leaf transition rates. The mathematical result above allows arbitrary finite leaves, but that general adapter is not implemented here.

Each Boolean equality guard is converted into its exact rational multilinear polynomial: \(x_i\) for a one-test and \(1-x_i\) for a zero-test. The compiler sums all marked hazards in each phase, averages the resulting polynomials, and checks that every coefficient of degree greater than one vanishes **exactly**. It converts the remaining affine expression into a nonnegative constant and local diagonal terms. A negative singleton coefficient is represented as a nonnegative killing rate on state zero, with the corresponding constant adjustment. A negative final constant is rejected.

For the contrast bound, marked rules are grouped by their leaf guard scope. Each individual scope is enumerated, its exact minimum and maximum half-contrast are computed, and group extrema are summed. Overlap between groups can make this bound conservative, but cannot invalidate it. The compiler neither enumerates a global assignment nor asserts independence of overlapping hazards. A guard-scope budget of eight protects the local enumeration. Polynomial expansion costs at most \(O(qs2^s)\) rational operations for \(q\) rules with at most \(s\) guarded leaves; local contrast enumeration has the same type of bound. The check is sufficient, not a complete search over all possible hidden additive representations.

### Connected coupled example

For each edge \((i,j)\) of a leaf cycle, use

\[
h_{ij,+}(x)=\kappa x_i x_j,
\qquad
h_{ij,-}(x)=\kappa(x_i+x_j-x_ix_j).
\]

The plus phase has an AND hazard and the minus phase an OR hazard. Both have the same observed edge mark; both reset the pair to \(00\), retaining the hidden controller. The OR is represented by three disjoint guards, so all source rates and runtime contractions remain nonnegative. Their mean is \(\kappa(x_i+x_j)/2\), while their half-difference is \(-\kappa\,1_{\{x_i\ne x_j\}}/2\). On an even \(n\)-cycle, the obtained bound \(A=n\kappa/2\) is attained by an alternating configuration. Neither phase's total killing is additive across leaves.

## 5. Repeated identified events can preserve CP width exactly

Suppose the current approximate state law is a positive mixture of \(R\) product laws over the controller and leaves. Propagation by (1), before \(J_j\), preserves the product form within each component. For one component let its propagated, **unnormalized** controller row be \(p(c)\) and leaf rows be \(v_i\).

Assume every leaf on which the observed mark's hazard or branch choice depends is reset to the same fixed public leaf values in every branch. Extra fixed leaf resets are allowed. Let \(S\) be the entire reset scope, and let \(h_j(c,x_S,d)\) include the source branch hazard and its controller reset to \(d\). The controller output row is

\[
g(d)=\sum_c p(c)\sum_{x_S}
  \left[\prod_{i\in S}v_i(x_i)\right]h_j(c,x_S,d).
\tag{9}
\]

The inactive leaves retain their propagated product rows. All active leaves are pinned to their common reset values. The component event-density mass is

\[
\left[\sum_d g(d)\right]\prod_{i\notin S}(v_i\mathbf 1),
\tag{10}
\]

times its incoming weight and any common scalar. Normalize \(g\), the inactive leaf rows, and the global component weights only after retaining all these masses. In particular, a numerically rounded controller row must not be normalized while discarding its mass.

Every input component produces one output component. Thus any sequence of marks satisfying this reset condition preserves at most \(R\) components, even when scopes overlap, controller phase is never observed, and the controller is never externally reset. Zero-weight components may be discarded; the executable demonstration uses strictly positive weights throughout. Its exact rational probabilities and normalized weights are retained.

For binary leaves, one update costs \(O(R(n+q_js))\) scalar operations when the observed mark has \(q_j\) guarded branches of scope at most \(s\), using positive product evaluation of each guard. Storage is \(O(Rn)\) scalar entries plus the compact rule interface. These are scalar-operation and representation-width bounds; bit complexity also depends on numerical precision and rational sizes. The executable rounds only via outward interval enclosures and charges their multiplicative spread.

This closure concerns the **current controller/leaf state**. Erasing a leaf's current state does not erase its historical count contribution. An unresolved-count TT with historical allocation labels cannot automatically be treated as the same fixed-width CP family. Arbitrary branch-dependent leaf resets can also create extra product branches. The compiler's `fixed_reset_schema` rejects such a mark for the fixed-width executor.

## 6. Numerical and whole-record certificates

The executable evaluates positive binary propagators using directed decimal intervals. Their lower endpoints are exact rational numbers. If the retained product propagator is \(\widehat B\), multiplying the maximum upper/lower ratio of each local matrix entry and scalar gives a computable \(c_{\rm prop}\ge1\) with

\[
\widehat B\le\bar B\le c_{\rm prop}\widehat B.
\]

The exact jump map preserves this order. Consequently the retained mark operator satisfies

\[
a\widehat K_j\le K_j\le b c_{\rm prop}\widehat K_j.
\tag{11}
\]

Applying retained rational matrices to rational CP rows is also enclosed. The implementation selects lower propagated rows and retains their exact masses; multiplying the local upper/lower ratios gives a per-application factor \(c_{\rm apply}\). Exact positive guard contraction, exact normalization, and exact rational serialization add no uncharged error.

The current numerical adapter uses 45-digit interval arithmetic and rejects an operation if a required positive local entry is unresolved. Very short times or extreme rates may require greater precision; the whole-workload mathematical certificate does not by itself certify that the current fixed-precision adapter can execute every positive lag in that workload. The executed records have resolved support and their reported numerical spreads are charged explicitly.

Let \(R_0\) be the projective spread already certifying the acquired input law. After \(m\) observed events with lags \(t_\ell\), the final spread is at most

\[
R_{\rm final}=R_0\prod_{\ell=1}^m
 \frac{b(t_\ell)c_{{\rm prop},\ell}c_{{\rm apply},\ell}}{a(t_\ell)}.
\tag{12}
\]

The normalized posterior TV distance is at most

\[
\frac{\sqrt{R_{\rm final}}-1}{\sqrt{R_{\rm final}}+1}.
\tag{13}
\]

The common-positive-operation/projective argument also bounds arbitrary later common conditioning. It is the established Hilbert-metric mechanism, not a newly claimed metric theorem. Formula (12) explicitly charges each new approximate record operator. It does not claim one initial approximation certificate covers an unlimited number of newly approximated operations without accumulation.

A useful coarse analytic envelope requires no lower bound on inter-event lags. With \(\lambda=d-\nu\), put \(c=A^2/(2\nu)=\lambda(1+\lambda/(2\nu))\). The even part of \(S/(1-E)\) is bounded by \(e^{ct}-1\), since

\[
\frac{1-e^{-(2\nu+\lambda)t}}{1-e^{-2\nu t}}
\le 1+\frac{\lambda}{2\nu}.
\]

Its odd part is at most \((A/\nu)e^{ct}\). Thus

\[
b(t)\le(1+A/\nu)e^{A^2t/(2\nu)},
\]

and, writing \(T=\sum_\ell t_\ell\),

\[
\log R_{\rm analytic}
\le m\left[A/\nu+\log(1+A/\nu)\right]+A^2T/(2\nu).
\tag{14}
\]

The bounded-potential alternative also gives \(\log R_{\rm analytic}\le2AT\). The executable uses the sharper individual bounds (4) and (6). The dependence on \(A\) is substantive: for the cycle \(A\) grows with its size, so demanding a fixed small error for larger sources can require a faster controller. This is a controlled fast-controller class, not a dimension-free accuracy claim for arbitrary rates.

### Certifying an entire workload before its records are known

The callable **workload_certificate** validates the fixed-reset schema for every admitted mark. With an event budget \(M\) and total lag budget \(T\), it returns one certificate covering all admitted mark sequences of length at most \(M\), all positive event lags with sum at most \(T\), and every common exact subsequent conditioning operation. Its inexpensive outward evaluation uses

\[
\rho\le\min\left\{
\frac{2MA+A^2T/2}{\nu},\ 2AT\right\},
\qquad
R_{\rm workload}\le R_0 C_{\rm num}e^\rho,
\]

where \(C_{\rm num}\) is a supplied multiplicative numerical-error budget for the whole workload. The default \(C_{\rm num}=1\) refers to mathematical exact averaged operators. A finite-precision execution must separately certify that its cumulative numerical spread stays inside its chosen budget. The exact posterior-TV bound is again (13). Thus storage width is fixed for the whole admitted workload and the error can be assessed before the observed record is available. The function reports eligibility of the supplied kinetic source; it never changes \(\nu\) to meet a tolerance. A terminal censored no-event tail is not included in this API's event-lag budget and needs a corresponding additional operator bound.

This workload claim concerns at most \(R\) positive product components, not uniformly bounded rational bit lengths. At precision \(p\), local interval evaluation and rounded retained rows cost at least the corresponding \(p\)-bit arithmetic. Exact normalization also carries representation-dependent rational sizes. Longer records can require more precision or larger rational integers even when their number of factors and mixture components stays fixed.

## 7. Executed construction and independently checked limits

The new source has 24 leaves, 146 rules, controller rate \(\nu=10^6\), and cycle rate \(\kappa=3/2\). These are supplied synthetic kinetic parameters; no empirical evidence for a physical fast gate is claimed. Its full state space has \(2^{25}=33,554,432\) configurations. The source pass obtains \(d_i=(0,3/2)\), \(d_0=0\), and \(A=18\). The finite positive interface at \(t=1/10\) uses one controller matrix and 24 leaf matrices followed by the retained exact rules. Its all-input single-event posterior-TV bound is approximately \(1.30499595\times10^{-5}\); the propagator's numerical relative spread beyond one is at most \(2.05\times10^{-42}\).

The executor loads the existing 256-component relative-certified correlated entrance without redoing its acquisition, and checks that its retained leaf transition rates exactly match the new source’s silent generators. As an explicit new future kinetic model, it then applies the coupled recurrent cycle source, with initially known controller state one. It conditions on marks `edge_0`, `edge_1`, `edge_2`, `edge_0`, each following a lag \(1/10\), with no intervening marked event. Controller phase is unobserved and is not reset. All four updates retain exactly 256 product components over controller and leaves. The final whole joint posterior-TV certificate is

\[
5.2200301614510805\times10^{-5}.
\]

Separately, the source-certified workload comprising any of the 24 edge marks, at most four events, and total elapsed event-lag at most \(2/5\), has fixed CP width and analytic-plus-inherited posterior-TV bound at most \(5.22004636167946\times10^{-5}\) for exact averaged-operator execution. This covers unlisted records as well as the executed one; numerical-error budgets are handled as stated above.

The four-event joint density lies in the outward interval approximately

\[
[9.97628103475728,\ 9.97836433026945]\times10^{-6}.
\]

The final hidden-controller-on probability is in \([0.0552143956249,0.0553187962282]\), and site 23's active probability is in \([0.5175274959002,0.5176318965035]\). These intervals include the operator approximation and inherited entrance uncertainty. The exact rational approximate law, not merely these reports, is available in the posterior JSON.

An independent reference expands only a separate three-leaf source, with 16 joint controller/leaf states. It forms the **original coupled** killed generator, uses positive scaled uniformization and interval matrix squaring to handle the large controller rate, and appends the exact marked reset. All 16 input rows are checked: all 64 positive event-operator entries lie inside the proposed entrywise sandwich, and all 192 structural zero entries agree. This finite reference is an implementation check; the all-input/all-source claim rests on (2)–(8) and the source checks.

The interface has an independent loader which validates the saved rational factors, compact kinetic source, additive-mean cancellation, mark/reset rules, and certificate consistency without reevaluating any propagator exponential. The final posterior loader verifies its exact weight normalization and local probabilities. The numerical run completed in about 1.94 seconds in this workspace; that execution time is a report for this source, not a general performance theorem.

## 8. Relation to established machinery

Two-state Poisson/Feynman–Kac representations and endpoint calculations are established. Leschke, Rothlauf, Ruder and Spitzer, *The free energy of a quantum Sherrington–Kirkpatrick spin-glass model for weak disorder*, Appendix B, explicitly treats the two-state formula and its extension to a time-dependent integrable field: <https://arxiv.org/pdf/1912.06633>. Paulin's *Concentration inequalities for Markov chains by Marton couplings and spectral methods*, Proposition 2.4, Theorem 2.9 and Corollary 2.11, supplies a general concentration route for inhomogeneous Markov chains: <https://arxiv.org/pdf/1212.2015>. Therefore a fast-switching concentration or averaging principle is not the claimed invention.

The constructive result here is the combination of an exact compact-source test for cancellation of coupled killing in the stationary mean; a source-only, path-uniform entrywise comparison for the complete event/reset operator; a retained positive rational interface valid for every entrance law; and an explicitly checked reset condition that supports fixed-width recurrent record inference with accumulated relative error. Network-free simulation, conventional retaining programmes, tensor methods and renewal/event methods can adopt this algorithm. No architecture-necessity claim follows from its existence. The scope above specifies when this particular inference can be obtained and reused before global state expansion.
