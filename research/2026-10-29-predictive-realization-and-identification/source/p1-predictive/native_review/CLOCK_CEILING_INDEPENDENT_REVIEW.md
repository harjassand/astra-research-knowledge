# Clock ceilings: independent operational challenge and exact construction

This review concerns root's proposed characterization from the supplied exact mean record \((S,w_B,v_R,v_L,c)\). It does not rerun the acquired native records, query a source, or establish historical priority.

**Verdict.** The proposed criterion is sound for positive total eliminated mass, subject to the usual admissibility assumptions on \(S,w_B,v_R,v_L\). There is one required degenerate-case correction: if \(\mathbf1^Tv_R=0\), then necessarily \(c=0\). The inequality \(2c\ge J_{\mathrm{cap}}\) by itself incorrectly admits \(c>0\) in that case.

The operational distinction is substantial: **port departure rates are capped, not preserved exactly**. Increasing \(c\) at fixed mean-record margins can require decreasing a native port departure rate. A one-port equality example below proves that an exact-rate interpretation would be false. Endpoint conditioning itself does not defeat the hidden-clock bound.

## 1. Precise admissibility and criterion

Assume \(S\) is an irreducible Eulerian directed Laplacian on \(m\) ports, with the one-port zero matrix allowed. Let \(w_B>0\), \(v_R,v_L\ge0\), and

\[
 D=\mathbf1^Tv_R=\mathbf1^Tv_L.
\]

Write the positive hidden-rate ceiling as \(\Lambda>0\), and the port-rate ceilings as \(\ell_i\). Define

\[
 F_{ij}=-S_{ij}\quad(i\ne j),\qquad
 a_i=w_{B,i}\ell_i-\sum_{j\ne i}F_{ij}.
\]

Every \(a_i\) must be nonnegative. Seek a nonnegative transport matrix \(M\) with row margins \(v_R\), column margins \(v_L\), and support restrictions

\[
 M_{ij}=0\text{ if }i\ne j,F_{ij}=0,
 \qquad M_{ii}=0\text{ if }a_i=0.
\]

For \(x\ge0,f>0\), put

\[
 z=\Lambda x/f,\quad n=\lfloor z\rfloor,
 \quad
 \psi(x,f)=\frac{f}{\Lambda^2}(n+1)(2z-n).
\]

Set \(\psi(0,0)=0\) and exclude \(x>0,f=0\). The transport objective is

\[
 J_{\mathrm{cap}}=
 \min_M\left[
 \sum_{i\ne j}\psi(M_{ij},F_{ij})
 +\sum_i\psi(M_{ii},a_i)
 \right].                                             \tag{1}
\]

For \(D>0\), a finite positive CTMC with the prescribed mean record, hidden departure rates at most \(\Lambda\), and port departure rates at most \(\ell_i\), exists exactly when the transport set is nonempty and

\[
 2c\ge J_{\mathrm{cap}}.                                \tag{2}
\]

For \(D=0\), the corrected criterion is \(c=0\), and a direct-port realization suffices whenever the other admissibility and cap conditions hold. If the one-port system then has no transitions, it is simply the trivial one-state chain; its absence of native departure trials must not be hidden by an undefined excursion probability.

This theorem preserves \(S,w_B,v_R,v_L,c\). It does not promise to preserve the source's endpoint-marked matrix \(M\), native self-return flows, native holding rates, or entire duration law. The optimization in (1) is allowed to choose a different transport with the same margins.

## 2. Why endpoint conditioning does not evade the clock ceiling

Uniformize the interior process at rate \(\Lambda\): at each independent exponential clock ring, take a transition of the substochastic embedded chain, allowing virtual self-loops. An absorption mark \(J\) and the number \(N\) of clock rings before return depend only on the embedded discrete path. They are independent of the exponential clock durations.

Thus, even conditional on \(J=j\),

\[
 \mathbb E[\sigma\mid J=j]=\frac{\mathbb E[N\mid J=j]}{\Lambda},
\]

\[
 \mathbb E[\sigma^2\mid J=j]
 =\frac{\mathbb E[N^2+N\mid J=j]}{\Lambda^2}.              \tag{3}
\]

A direct jump between distinct ports has \(N=0\). A genuine self-return has \(N\ge1\).

For any nonnegative integer-valued \(N\) of mean \(z\), let \(n=\lfloor z\rfloor\). The pointwise inequality

\[
 (N-n)(N-n-1)\ge0
\]

implies

\[
 \mathbb E(N^2+N)\ge(n+1)(2z-n).                         \tag{4}
\]

Equality holds precisely when \(N\) is supported on \(n,n+1\), with their probabilities fixed by \(z\). Multiplying (3)-(4) by the channel flow \(f\), where its hidden mass is \(x=f\mathbb E\sigma\), gives \(\psi(x,f)\).

Conditioning on the eventual endpoint therefore changes embedded-path probabilities, but it cannot create a faster independent holding clock. Equivalently, the endpoint-conditioned Doob transform of a transient CTMC retains the original holding-rate diagonal on states with positive conditioning probability. Uniformization proves the needed bound directly without relying on that alternate description.

## 3. The diagonal channel and the native port clock

An actual native diagonal return flow \(f_i\) obeys

\[
 0\le f_i\le a_i,
 \qquad f_i\le\Lambda M_{ii}.                            \tag{5}
\]

The first inequality is the port clock cap, because the total departure flow is \(\sum_{j\ne i}F_{ij}+f_i\). The second follows from \(N\ge1\) for a self-return.

For fixed \(x\), the function \(\psi(x,f)\) is nonincreasing in \(f\). Within a segment of fixed integer \(n\), its derivative with respect to \(f\) is

\[
 -n(n+1)/\Lambda^2\le0.
\]

For \(f\ge\Lambda x\), the \(n=0\) expression is the constant \(2x/\Lambda\). Consequently

\[
 \min_{0<f\le\min(a_i,\Lambda x)}\psi(x,f)
 =\psi\bigl(x,\min(a_i,\Lambda x)\bigr)
 =\psi(x,a_i).                                         \tag{6}
\]

There is no hidden instantaneous self-jump in (6). Its realization uses the actual flow \(f_i=\min(a_i,\Lambda x)\), whose mean clock count is at least one. When \(x=0\), use \(f_i=0\).

## 4. Equality construction with shared phases

For an off-diagonal channel use its prescribed flow \(f=F_{ij}\). For a diagonal channel use \(f=\min(a_i,\Lambda x)\). Let \(z=\Lambda x/f=n+\theta\), where \(0\le\theta<1\).

If \(n\ge1\), construct \(n\) serial phases, all with rate \(\Lambda\) and stationary flow \(f\). After phase \(n\), return directly with probability \(1-\theta\), or take one additional phase of rate \(\Lambda\) with probability \(\theta\). The extra phase has stationary flow \(f\theta\). This shares the common prefix and uses at most \(n+1\) hidden states. If \(\theta=0\), omit the extra state.

If \(n=0\), take a direct port-to-port transition with flow \(f(1-\theta)\), and a one-phase route with flow \(f\theta\). This case only occurs off diagonal. Zero-flow edges and states are omitted.

Give each phase stationary mass equal to its flow divided by \(\Lambda\). Every hidden rate then equals its cap; the channel mass is \(x\), its second contribution is \(\psi(x,f)\), and the port departure rates satisfy their ceilings. Equal row and column sums of off-diagonal \(F\) ensure stationarity at ports for any chosen diagonal flows. Positive hidden phases inherit irreducibility from the port graph.

The transport polytope is compact, and each term in (1) is continuous and convex piecewise linear in its mass argument. A minimizer exists. Applying this construction to it attains equality in (2).

## 5. Every larger residual is attainable when hidden mass is positive

It is not sufficient to assert that an arbitrary slow exponential can be inserted at fixed mean: an equality case may leave no faster clock to compensate for the extra mean. The following constructions handle that obstruction explicitly.

### 5.1 A positive off-diagonal mass

Fix a channel of flow \(f>0\), mean \(\mu=x/f>0\), and minimal conditional second moment \(q_0=\psi(x,f)/f\). Define

\[
 r_0=\min(\Lambda,1/\mu),\qquad q_E=2\mu/r_0.
\]

A mixture of a zero-duration direct transition and an exponential of rate \(r_0\), with positive-duration probability \(p=\mu r_0\le1\), has mean \(\mu\) and second moment \(q_E\ge q_0\). Any value between \(q_0\) and \(q_E\) is obtained by mixing this law with the adjacent-Erlang equality law; both component laws have mean \(\mu\).

For any \(q\ge q_E\), set

\[
 r=2\mu/q\le r_0\le\Lambda,
 \qquad p=\mu r\le1.
\]

The direct/exponential mixture then has exactly the required mean and second moment. The total channel flow \(f\), hidden mass \(x\), and native port rate remain unchanged. Increasing \(q\) by \(2\Delta c/f\) supplies any desired extra residual \(\Delta c\).

### 5.2 Only positive diagonal mass is available

Choose one diagonal channel with mass \(x>0\) and capacity \(a>0\). Let

\[
 f_0=\min(a,\Lambda x),\quad
 C_0=\frac12\psi(x,a),\quad C_E=x^2/f_0.
\]

The equality law has residual contribution \(C_0\). A single exponential of mean \(x/f_0\), which respects the ceiling, has residual contribution \(C_E\). Mixtures of these equal-mean laws at flow \(f_0\) attain every \(C\in[C_0,C_E]\).

For \(C\ge C_E\), choose instead

\[
 f=x^2/C\le f_0\le a,
 \qquad r=x/C\le f_0/x\le\Lambda.                        \tag{7}
\]

A single exponential phase of rate \(r\), carrying stationary flow \(f\), has mass \(f/r=x\) and residual contribution \(f/r^2=C\). This preserves all supplied mean-record margins and lowers the port departure rate within its cap. It supplies arbitrary additional residual without a zero-time self-return.

At positive total hidden mass, at least one of these two cases applies. Their mixture weights and rates remain finite for each finite requested \(c\). Neither argument bounds the required minimum rate away from zero.

## 6. Exact native port rates would invalidate the upward closure

Consider one port of weight one, hidden rate ceiling \(\Lambda=2\), prescribed hidden mass \(v_R=v_L=1\), and port ceiling \(\ell=2\).

The minimum is attained by a single hidden state with flow two and rate two. Its mean excursion time is \(1/2\), and

\[
 c=1/2.
\]

If the native port departure rate were also required to equal two exactly, the excursion flow would be fixed at two. The hidden mass condition would force mean duration \(1/2\). Because every positive excursion has at least one clock ring and no hidden clock exceeds two, equality forces exactly one exponential phase of rate two. Thus \(c\) would be fixed at \(1/2\); no larger value is possible.

Under the actual cap-only theorem, \(c=2\) is realized by flow \(1/2\) and a hidden exponential of rate \(1/2\). Both ceilings hold, the hidden mass remains one, and the port rate decreases from two to \(1/2\). The executable constructs both chains exactly.

This is a boundary on the retained information, not a failure of the cap-only theorem. The earlier realization result that preserved native \(F\) and port holding rates must not be transferred to this theorem without adding the corresponding constraints.

## 7. Required zero-mass correction

Take two ports,

\[
 S=\begin{pmatrix}1&-1\\-1&1\end{pmatrix},\quad
 w_B=(1,1),\quad v_R=v_L=(0,0),
\]

and set \(\Lambda=1\), \(\ell=(1,1)\), and supplied \(c=1\). The only feasible transport is \(M=0\), so \(J_{\mathrm{cap}}=0\), and the uncorrected inequality \(2c\ge J_{\mathrm{cap}}\) passes.

Nevertheless the record is impossible: \(\mathbf1^Tv_R\) equals total hidden stationary mass. With positive stationary weights, zero total hidden mass means no hidden states, which forces \(c=0\). Thus the criterion must explicitly distinguish \(D=0\) from \(D>0\), unless positivity of eliminated mass is already an announced premise.

## 8. Nontrivial rational optimizer and full-generator controls

The executable `CLOCK_CEILING_CONSTRUCTION_CHECKS.py` uses only rational arithmetic for mathematical claims. It assembles the complete generators and independently eliminates their hidden blocks, reconstructing \(F,M,S,v_R,v_L,c\) and checking every native rate. It then compares full killed means with the reduced mean formulas. No root compiler, optimizer, acquired record, random source, or numerical linear algebra package is used.

The principal exact optimizer has

\[
 \Lambda=2,\quad w_B=(2,3),\quad\ell=(1,1),
 \quad F_{01}=F_{10}=1,\quad a=(1,2),
\]

\[
 v_R=(1,11/6),\quad v_L=(7/12,9/4),\qquad
 M=\begin{pmatrix}1/4&3/4\\1/3&3/2\end{pmatrix}.
\]

Every feasible transport is parameterized by

\[
 M(t)=\begin{pmatrix}t&1-t\\7/12-t&5/4+t\end{pmatrix},
 \qquad0\le t\le7/12.
\]

All objective breakpoints are \(0,1/12,1/2,7/12\). Direct evaluation of its linear pieces gives a minimum

\[
 J_{\mathrm{cap}}=43/12
\]

throughout \(t\in[1/12,1/2]\). The selected \(t=1/4\) therefore is a global optimizer, not merely an arbitrary feasible transport.

Its two fractional duration laws have mean uniformized clock count \(3/2\), and another channel has a direct-zero atom with positive-duration probability \(2/3\). The shared-prefix equality construction uses **eight total states**. Every hidden rate is exactly two, and the actual port rates are \((3/4,1)\). It has

\[
 c=43/24,
 \quad b_R=(3,29/6),\quad b_L=(31/12,21/4),
 \quad \mathbf1^Tw=47/6.
\]

The exact full-generator equilibrium target means are

| Port target | Mean |
|---|---:|
| \(\{0\}\) | \(163/35\) |
| \(\{1\}\) | \(229/116\) |
| \(\{0,1\}\) | \(43/68\) |

The code also realizes additional residuals \(1/64\) and \(7/8\) on the same off-diagonal channel, verifying all rates, the unchanged margins, and the target means. The smaller increment exercises the equal-mean mixture, while the larger one exercises the slow-exponential/direct construction. Four diagonal constructions cover equality, interior mixture, and reduced-flow regimes, including the native-rate boundary above.

## 9. The directed Erlang witness and the meaning of a clock limit

For the earlier two-port directed family, \(w_B=(1,1)\), \(F_{01}=F_{10}=1\), \(v_R=(1,0)\), \(v_L=(0,1)\), and

\[
 c_n=(1+1/n)/2.
\]

Its transport is forced: \(M_{01}=1\) and all other entries vanish. If \(\Lambda<n\), equation (3) and \(\operatorname{Var}N\ge0\) imply

\[
 2c\ge1+1/\Lambda>1+1/n=2c_n.
\]

Therefore the record is impossible under that clock ceiling. Conversely, when \(\Lambda\ge n\), the original \(n\)-phase Erlang chain of rate \(n\) is a realization. Thus the exact condition is

\[
 \Lambda\ge n
\]

when port caps are at least one. The executable checks 25 rational ceiling comparisons and constructs the full equality generators for \(n=1,2,3,7,16\), including their target means.

A fixed clock bound therefore prevents approaching the free-clock conditional-variance floor by indefinitely increasing phase count. This is a statement about a mathematical rate resource. It does not supply clock calibration, hardware, energy, instrument precision, or experimental access.

## 10. Scope and comparison

The receipt `CLOCK_CEILING_CONSTRUCTION_CHECKS.json` records three optimizer/inflation generators, four diagonal generators, five complete Erlang generators, 25 ceiling comparisons, all exact matrices for the nontrivial constructions, and both scope counterexamples. All controls passed. The proof supplies the general statement; the finite controls check implementation, equality cases, and the operational boundary.

The convex transport objective is ordinary piecewise-linear optimization and can be handled by a strong conventional solver. The exact two-port optimization here needs only its complete finite set of breakpoints. Given the mean record, direct Schur elimination remains the preferable mean-query evaluator when a positive clock-constrained realization is unnecessary. The addition under review is the necessary-and-sufficient interface-to-realization criterion and its explicit equality construction. No acquisition advantage, solver speedup, physical implementation, or priority claim is established by this review.
