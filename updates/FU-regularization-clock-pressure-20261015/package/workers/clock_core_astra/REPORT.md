# Finite clock summaries cannot certify relative deadline tails

The source clock certificate cannot be repaired, in general, by retaining any fixed finite number of clock moments or positive Laplace samples. An explicit construction below gives two positive finite-state continuous-time Markov chains with the same number of states, the same retained trace generator, the same mean clock, the same clock-error certificate, and all specified moments and Laplace derivatives exactly equal. Their probabilities of missing a deadline have an unbounded ratio, even as their common normalized clock-error bound tends to zero.

This is an information obstruction within an elementary phase-type family. It changes the admissible continuation: a summary of this kind needs an additional promise about the relevant tail, a verified realization-degree bound with enough identifying data, or a finite-horizon error certificate tied to the actual requested probability. It does not establish a new computational advantage. The construction uses classical rational interpolation; historical priority of this particular combined statement has not been established.

Status: internally derived mathematical result, with exact rational finite checks. No physical benchmark advantage or qualifying new computational operation was obtained.

## Scientific quantity and strongest baseline

For a supplied killed generator \(A\), initial distribution \(\mu\), and first absorption time \(T\), the deadline-miss probability is

\[
S(t)=\Pr(T>t)=\mu e^{tA}\mathbf1.
\]

Graph transformation already preserves mean passage times and endpoint branching probabilities; PyGT documents both this contract and partial graph transformation. Its statistics implementation also computes passage distributions using eigendecomposition. These are prior methods, not candidate discoveries. [PyGT](https://pygt.readthedocs.io/en/latest/), [PyGT statistics](https://pygt.readthedocs.io/en/latest/stats.html).

The relevant general baselines also include matrix-exponential actions, which avoid forming the whole exponential, and rational Krylov or interpolatory model reduction. Interpolation at zero is ordinary moment matching, and interpolation at positive shifts is an established extension. [Al-Mohy and Higham](https://eprints.maths.manchester.ac.uk/1591/), [pyMOR interpolation tutorial](https://docs.pymor.org/latest/tutorial_interpolation.html), [Beattie and Gugercin](https://arxiv.org/abs/1409.2140).

For the counterexample family here, the strongest equally informed baseline is simpler: a direct positive exponential-mixture formula evaluates a deadline in linear time in the number of phases. Comparing the construction only with a dense matrix exponential would manufacture an advantage.

The scientific issue is therefore whether a substantially smaller retained summary contains enough information to certify a relative error in \(S(t)\). The following theorem answers negatively for a specified, widely used class of summaries.

## The finite information contract

Fix a highest moment order \(r\ge2\). Let \(s_1,\ldots,s_J>0\) be distinct Laplace query points, with multiplicities \(m_1,\ldots,m_J\ge1\). The available excursion information is:

- moments through order \(r\);
- Laplace-transform derivatives of orders \(0,\ldots,m_j-1\) at \(s_j\);
- the exact excursion endpoint probabilities.

Write

\[
L=\sum_{j=1}^{J}m_j,\qquad n=r+1+L.
\]

The zeroth moment is included in \(n\). The query locations may depend on the deadline below; their number and derivative multiplicities are bounded. All statements concern these ordinary linear statistics, not arbitrary real-valued encodings of an entire generator.

## Theorem

For every integer \(M>n+1\), there are two CTMCs \(Q^{(0)}_M,Q^{(1)}_M\), each with \(n+3\) states, a common initial source \(a\), and a common absorbing target \(b\), such that:

1. Every nonabsorbing state is reachable from \(a\) and can reach \(b\).
2. For the retained set \(R=\{a,b\}\), both chains have
   \[
   K=\begin{pmatrix}-1&1\\0&0\end{pmatrix}
   \]
   and exactly the same mean-clock correction \(\alpha\).
3. Their complete excursion-kernel moments through order \(r\), and all the specified positive-shift kernel derivatives, coincide exactly. Their first \(r\) full passage-time moments also coincide.
4. Their source-certificate values are identical and satisfy
   \[
   V_M=\frac{2}{nM^3}\sum_{i=1}^{n}(i+1)^2\longrightarrow0,
   \qquad \mathbb ET_M=1+O(M^{-3}).
   \]
5. At the deadline \(t=M\), their survival ratio satisfies
   \[
   \frac{S^{(1)}_M(M)}{S^{(0)}_M(M)}
   \ge \frac{\exp\{M/(n+1)-1\}}{6nM^{n+2}}
   \longrightarrow\infty.
   \]

The lower bound is uniform over the locations of the finitely many positive Laplace queries. When the query points are rational, both generators have rational entries.

### Explicit positive interpolation construction

Let

\[
x_i=i+1\quad (i=1,\ldots,n),\qquad
D(x)=\prod_{j=1}^{J}(1+s_jx)^{m_j}.
\]

The empty product is one. Define the Lagrange polynomials at the fast nodes by

\[
\ell_i(x)=\prod_{k\ne i}\frac{x-x_k}{x_i-x_k},
\qquad
c_i=\frac{D(x_i)}{D(M)}\ell_i(M).
\]

For every rational function \(f=p/D\) with \(\deg p\le n-1\), polynomial interpolation gives

\[
f(M)=\sum_{i=1}^{n}c_if(x_i). \tag{1}
\]

In particular, (1) holds for \(f(x)=x^k\), \(0\le k\le r\), because \(\deg(x^kD)\le r+L=n-1\). It also holds for

\[
f(x)=\frac{x^k}{(1+s_jx)^{k+1}},
\qquad 0\le k<m_j,
\]

because multiplication by \(D\) produces a polynomial of degree \(L-1\le n-1\). Taking \(f=1\) proves \(\sum_i c_i=1\).

Set

\[
C_M=\max\{1,|c_1|,\ldots,|c_n|\},\quad
\varepsilon_M=\frac{1}{2nC_M},\quad q_M=M^{-3}.
\]

Define two discrete distributions of exponential means:

\[
\nu_0=\frac1n\sum_{i=1}^{n}\delta_{x_i},
\qquad
\nu_1=\sum_{i=1}^{n}\left(\frac1n-\varepsilon_Mc_i\right)\delta_{x_i}
       +\varepsilon_M\delta_M.
\]

Every fast weight in \(\nu_1\) is at least \(1/(2n)\), the added weight is positive, and total mass is one. Thus this is a pair of probability distributions, not a signed formal representation. Equation (1) gives equality of every statistic listed above.

For later use, \(M>x_i\) and \(s_j>0\) imply \(D(x_i)/D(M)\le1\). The integer-node denominator in \(\ell_i\) has absolute value at least one, while each numerator factor is less than \(M\). Hence

\[
|c_i|\le M^{n-1},\qquad
\varepsilon_M\ge\frac{1}{2nM^{n-1}}. \tag{2}
\]

This bound does not deteriorate when the positive query locations change with \(M\).

### From interpolation to phase-type excursions

Given \(\nu\), draw an exponential mean \(x\sim\nu\), then let the excursion duration \(H\mid x\) be exponential with mean \(x\). Its transform and moments are

\[
F(s)=\mathbb E e^{-sH}=\int\frac{1}{1+sx}\,\nu(dx),
\qquad
\mathbb EH^k=k!\int x^k\,\nu(dx).
\]

Differentiation gives

\[
F^{(k)}(s)=(-1)^kk!\int\frac{x^k}{(1+sx)^{k+1}}\,\nu(dx).
\]

Consequently \(\nu_0\) and \(\nu_1\) give exactly equal first \(r\) excursion moments and all queried transform derivatives. All excursions end at the same target, so endpoint-conditioned and unconditional statements coincide.

### CTMC realization and equality of the source certificate

The source waits for \(X\sim\operatorname{Exp}(1)\), then goes directly to \(b\) with probability \(1-q_M\). With probability \(q_M\) it selects one exponential phase according to \(\nu\), waits in that phase, and jumps to \(b\). Therefore

\[
T=X+JH,\qquad J\sim\operatorname{Bernoulli}(q_M),
\]

with independent \(X,J,H\). For phase weights \(w_i\) and means \(x_i\), the nonzero row-generator entries are

\[
Q_{aa}=-1,\quad Q_{ab}=1-q_M,\quad Q_{ai}=q_Mw_i,
\quad Q_{ii}=-1/x_i,\quad Q_{ib}=1/x_i.
\]

To give both chains exactly \(n+3\) states, split the first baseline phase into two identical positive phases, each with weight \(1/(2n)\). This changes no law or statistic, and all listed phases remain reachable.

For \(R=\{a,b\}\), direct block elimination yields

\[
K=\begin{pmatrix}-1&1\\0&0\end{pmatrix},\qquad
\alpha_a=1+q_M\mathbb EH,\quad\alpha_b=1.
\]

The nonzero excursion-kernel entry is \(q_MF(s)\), so its matched moments and derivatives follow from the preceding calculation. The full passage transform is

\[
\mathbb Ee^{-sT}=\frac{1-q_M+q_MF(s)}{1+s},
\]

which also shows equality of the requested full-passage transform derivatives and first \(r\) moments.

For completeness, the clock-error identity does not have to be imported from the supplied source. The source time-change coupling is

\[
\widehat T=(1+q_M\mathbb EH)X.
\]

Using \(\mathbb EX=1\), \(\mathbb EX^2=2\), and independence,

\[
\mathbb E(T-\widehat T)^2
=\mathbb E(JH-q_M\mathbb EH\,X)^2
=q_M\mathbb EH^2
=2q_M\int x^2\nu(dx).
\]

The cancellation of the two \(q_M^2(\mathbb EH)^2\) terms is exact. Since \(r\ge2\), both models have the same \(V_M\), giving item 4. In particular each lies within \(\sqrt{V_M}\) in \(W_2\) of the same reduced exponential law, and the two original laws are within \(2\sqrt{V_M}\) of each other in \(W_2\).

### Deadline separation

For \(x>1\),

\[
\Pr\{X+\operatorname{Exp}(1/x)>t\}
=\frac{x e^{-t/x}-e^{-t}}{x-1}.
\]

Here \(\operatorname{Exp}(1/x)\) is parameterized by its rate. Equivalently,

\[
S(t)=\left(1-q_M-q_M\sum_i\frac{w_i}{x_i-1}\right)e^{-t}
     +q_M\sum_i\frac{w_ix_i}{x_i-1}e^{-t/x_i}. \tag{3}
\]

Since every \(x_i\ge2\) and \(q_M<1/2\), every coefficient in (3) is nonnegative. In the baseline \(x_i\le n+1\), and \(x_i/(x_i-1)\le2\), so

\[
S^{(0)}_M(M)\le (1+2q_M)e^{-M/(n+1)}\le3e^{-M/(n+1)}.
\]

In the second model, the slow branch alone contributes

\[
S^{(1)}_M(M)\ge q_M\varepsilon_Me^{-1}.
\]

Combine these inequalities with (2) to obtain item 5. The proof is entirely within positive, finite-state, absorbing CTMCs. No infinite-support mixing measure, heavy-tailed law, numerical underflow, or invalid generator is needed.

## Consequences for reduced representations

### A known compact range of holding rates is still insufficient

The failure does not require an unboundedly slow microscopic holding rate. In the construction, fix the added mean at \(M_0=2(n+1)\) and let the deadline be \(t\), independently. Use \(q_t=t^{-3}\). All holding and phase-to-absorption rates then lie in the fixed range \([1/(2(n+1)),1]\); the source-to-phase branching rates become small, but every holding time remains uniformly bounded in mean. The same interpolation matches all queried information, and the coefficient bound gives \(\varepsilon\ge1/(2nM_0^{n-1})\), even if positive query shifts depend on \(t\). As above,

\[
V_t=O(t^{-3}),\qquad
\frac{S_1(t)}{S_0(t)}
\ge \frac{\varepsilon}{3t^3}
     \exp\left\{t\left(\frac1{n+1}-\frac1{M_0}\right)\right\}
=\frac{\varepsilon}{3t^3}e^{t/[2(n+1)]}\longrightarrow\infty.
\]

Thus bounded holding rates alone do not repair an all-time relative-error contract. If a strictly positive lower bound is imposed on every nonzero transition rate as well, take \(q\) fixed instead: the two fixed chains still have an unbounded survival ratio as \(t\to\infty\), and their common \(V\) can be chosen as small as desired when constructing the pair. This latter statement does not assert \(V\to0\) while one fixed transition-rate lower bound is held unchanged.

### No uniform relative estimator from this summary

Both chains yield identical summaries. At a deadline where \(S_1/S_0>(1+\delta)/(1-\delta)\), the intervals

\[
[(1-\delta)S_0,(1+\delta)S_0],\qquad
[(1-\delta)S_1,(1+\delta)S_1]
\]

are disjoint. Thus no algorithm that receives only this summary can guarantee relative error at most any fixed \(\delta<1\) over the full class. Likewise no fixed multiplicative factor works uniformly. Exact arithmetic or a more powerful optimizer cannot recover discarded information.

The result also covers any bounded deterministic adaptive sequence of positive-shift transform queries after the moments are supplied. Choose the baseline phase count using the maximum query budget; the interpolation argument remains valid if fewer queries are made, since the relevant numerator degrees are then smaller than the interpolation degree. Run the query rule on the baseline, collect its finite transcript, and construct the alternative using those query locations. Every response is unchanged, so the deterministic query rule follows the same transcript. This statement assumes the summary access model; it does not apply to an algorithm that additionally reads the complete generator or receives the slowest pole.

### Endpoint information does not resolve the obstruction

To obtain two absorbing endpoints, split every absorbing transition in fixed proportions \(\rho\) and \(1-\rho\), using the same \(0<\rho<1\) in both models. Endpoint choice is then independent of \(T\). All endpoint probabilities, endpoint-conditioned clock moments, and corresponding matrix-kernel queries coincide. Yet

\[
\Pr\{T>M,\text{ eventual endpoint}=b_1\}=\rho S(M)
\]

has the same unbounded ratio. Choosing a small \(\rho\) makes this a rare-endpoint deadline-miss event. This is a statement about the joint event, not a failure to preserve the eventual endpoint probability itself.

### A small boundary need not have a small temporal realization

The complete Schur excursion transform is a sufficient exact representation, but that representation is established state elimination. In the alternative model,

\[
F(s)=\sum_{i=1}^{n}\frac{w_i}{1+sx_i}+\frac{\varepsilon_M}{1+sM}
\]

has \(n+1\) distinct simple poles, each with a nonzero positive residue. No pole cancels. Any exact \(k\)-dimensional linear state-space realization has a transfer denominator dividing a degree-\(k\) characteristic polynomial, so \(k\ge n+1\). An exact phase-type representation is subject to the same lower bound.

Thus an exact memory kernel can have the full eliminated temporal order despite there being only one nonabsorbing retained state. This is a direct application of standard rational realization theory, not a new reduction method.

### Infinite-time relative accuracy requires exact tail structure

For positive exponential mixtures, if

\[
S(t)\sim c e^{-\lambda t},\qquad \widetilde S(t)\sim\widetilde c e^{-\widetilde\lambda t},
\]

then \(\widetilde S(t)/S(t)\sim(\widetilde c/c)e^{-(\widetilde\lambda-\lambda)t}\). A relative band \(1\pm\delta\), \(\delta<1\), valid for every \(t\ge0\), requires \(\widetilde\lambda=\lambda\) exactly and the corresponding coefficient ratio inside the band. For polynomial-times-exponential tails the dominant polynomial order must agree too. This explains why a finite horizon and a specified probability scale are usually the operationally meaningful target.

## Exact replay and numerical illustration

Run `python3 replay.py` from this directory. `REPLAY.json` contains the full rational generators, weights, moments, kernel queries, bit lengths, and results. Nine cases passed. They include moment orders 2, 4, 6, and 8; fixed positive shifts; and shifts shrinking as \(1/M\) and \(1/M^2\). A ninth case keeps all holding rates between one eighth and one while the deadline is 1000. Generator block inverses independently check \(K,\alpha,V\), full-passage moments, and transform derivatives. Both chains in the first case were also compared with 90-digit matrix-exponential actions.

| Matched information | Deadline | Common bound \(\sqrt V/\mathbb ET\) | Numerical \(\log_{10}(S_1/S_0)\) | Exact rationally certified ratio |
|---|---:|---:|---:|---:|
| First 2 moments | 1,000 | 0.000139044 | 101.7164 | \(>10^{58}\) |
| First 4 moments and 3 positive-shift derivative values | 10,000 | 0.00000842615 | 464.8828 | \(>10^{303}\) |
| First 6 moments and 4 values at fixed and shrinking shifts | 10,000 | 0.0000108628 | 329.0269 | \(>10^{204}\) |
| First 8 moments and 4 positive-shift derivative values | 10,000 | 0.0000124900 | 278.9968 | \(>10^{170}\) |
| First 2 moments with holding rates in [1/8, 1] | 1,000 | 0.000139044 | 52.5386 | \(>10^{25}\) |

For the first displayed case, \(S_0(1000)\approx1.18631\times10^{-118}\) and \(S_1(1000)\approx6.17446\times10^{-17}\). The displayed probabilities use 90-digit arithmetic and the analytic formula; their rounded decimal values are not themselves interval certificates.

The separate ratio certificate uses only rational arithmetic. From \(2<e<3\),

\[
\frac{S_1(M)}{S_0(M)}
\ge \frac{q_M\varepsilon_M}{3}\exp\{M/(n+1)-1\}
>\frac{q_M\varepsilon_M}{9}\,2^{\lfloor M/(n+1)\rfloor}.
\]

The last quantity is rational and the replay compares it exactly with powers of ten. Finite checks validate these instances and the implementation; the preceding proof supplies the general quantifiers.

## Supply cost and computational disposition

The fixture inputs are explicit sparse rational generators. Across the saved cases, their largest numerator or denominator bit length ranges from 36 to 190. The physical task in the supplied source instead inherits a kinetic network and a rate model. Neither this proof nor a transfer-function reduction acquires missing molecular states, transition channels, rate uncertainties, or the validity of the Markov approximation.

Given the full star-model input, reading its rates and weights costs at least linear time in its number of phases. Equation (3) then evaluates one deadline with \(O(n)\) exponentials and arithmetic operations, with arithmetic precision charged separately. Exact interpolation uses \(O(n^2+nL)\) rational arithmetic operations in the direct implementation; large rational bit lengths must still be charged. General shifted-block solves can cost much more and can introduce fill and conditioning costs. None of those costs is removed by calling the result a Bernstein or phase-type kernel.

Phase-type moment fitting is already an established subject, and optimal probability bounds under moment constraints are part of the classical moment problem. The present construction specializes those ideas to the exact pGT clock interface and adds explicit positive-shift interpolation and a common vanishing clock certificate. [Osogami and Harchol-Balter algorithms](https://www.cs.cmu.edu/~osogami/code/momentmatching/index.html), [Bertsimas and Popescu](https://www.mit.edu/~dbertsim/papers/MomentProblems/Optimal-inequalities-in-probability-theory-A-convex-optimization-approach-SIAM15.pdf).

The result does not rule out useful reductions for a specified kinetic model. It rules out promoting a finite clock-summary contract to a universal relative-tail guarantee. A credible next construction must supply the information this counterexample removes, state a finite horizon or exact tail promise, and compare the complete pipeline with matrix-exponential actions, graph transformation, spectral representations, and rational model reduction using the same input. For a known finite realization degree, sufficiently many exact identifying data can determine the rational law; the theorem deliberately concerns a budget below that identification threshold.

## Files and provenance

- `replay.py`: executable exact construction and checks.
- `REPLAY.json`: nine complete rational fixtures and results.
- `PRIMARY_SOURCES.md`: verified sources and the role of each source.
- `sources/RECEIPTS.json`: acquisition URLs, statuses, timestamps, and content hashes.
- `fetch_sources.py`: replayable acquisition of primary documentation and author pages.

The source stimulus was `../../sources/clock_pasted.txt`. Its general stopped-clock theorem was treated as a supplied claim; the particular identity needed here was proved directly above. This memo makes no historical-priority, physical-validation, or computational-speedup claim.
