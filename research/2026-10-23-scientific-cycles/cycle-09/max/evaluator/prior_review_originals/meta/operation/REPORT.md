# Operation receiver: anisotropic, general-dimensional susceptibility

## Result

For every integer $d\ge2$, strictly positive $P=\operatorname{diag}(p_1,\ldots,p_d)$ with trace one, and $k\ge2$, put

\[
s_P=1-\operatorname{Tr}P^2.
\]

There is a unique $t>0$ satisfying

\[
\sum_{i=1}^d(1-t/p_i)_+=1.
\]

Define

\[
z_i=(1-t/p_i)_+,\quad Z_* =\operatorname{diag}(z_i),\quad
A=\{i:p_i>t\},\quad r=|A|,
\]

\[
t=\frac{r-1}{\sum_{i\in A}p_i^{-1}},\qquad
f_P=\operatorname{Tr}[P(I-Z_*)^2]
=\sum_{i\notin A}p_i+(r-1)t.
\]

Here $r\ge2$; threshold equalities $p_i=t$ have $z_i=0$. Let

\[
C_k=\sum_{n=0}^{k-2}(k-1-n)\Pr(S_n=0),
\qquad \Pr(S_{2n}=0)=4^{-n}\binom{2n}{n},
\]

with odd return probabilities zero. The requested answer is

\[
\boxed{\min_{\zeta\ge0,\,\operatorname{Tr}\zeta=1}
\operatorname{Tr}(\sigma_P H_\zeta^2)
=v_{P,k}=\frac{s_P}{4}k(k-1)+\frac{f_P-s_P}{2}C_k.}
\]

An attained full-prefix optimizer is

\[
\boxed{\zeta_* =\sum_i z_i\bigl(|i\rangle\langle i|\bigr)^{\otimes k}.}
\]

The minimization includes every coherent and entangled prefix density. The displayed optimizer is an analytic witness. Its rank is $r$, and its support is the span of the repeated active eigenvectors.

For an entirely finite expression, with $N=\lfloor(k-2)/2\rfloor$,

\[
C_k=(2N+1)4^{-N}\binom{2N}{N}\left(k-1-\frac{2N}{3}\right).
\]

In particular $v_{P,k}/k^2\to s_P/4$.

## Dimension-independent word reduction and weighted costs

The source's prepend/pop algebra and $U^2=I$ hold for any color dimension. On sufficiently deep words, charge pinching therefore gives the same coefficient

\[
G_1=[C_-,C_+],\qquad
C_i=U_0\cdots U_{i-1}U_iU_{i-1}\cdots U_0.
\]

The same-index terms are $kI-2Q$; they cancel in $H_\zeta$. Distinct endpoint pairs occupy disjoint input charge blocks. This algebra uses neither the color measure nor a bath reset. [S1, §§2–3]

Fix endpoints $i<j$ of charges $0,1$. Cancel matched push/pop factors in the prefix and middle. Such a factor merely permutes its own input color wires and restores the bath, even in a coherent superposition. Write $m,h$ for unmatched prefix pops and pushes, and $e$ for unmatched middle pops. The stack after the prefix is

\[
(a_h,\ldots,a_1,B_m,B_{m+1},\ldots).
\]

The conjugated middle/end operation inserts an input color $w$ at index $e$. The endpoint commutator compares pop-after-insertion with insertion-after-pop. For $e\ge1$, their stacks are

\[
(P_1,\ldots,P_{e-1},w,P_e,\ldots),\qquad
(P_1,\ldots,P_{e-1},P_e,w,\ldots),
\]

with the same extracted $P_0$. At $e=0$, the first extracts $w$, while the second extracts $P_0$ and replaces it by $w$. Undoing the prefix consumes the first $h$ positions. Consequently the three cases remain exactly:

| Condition | Contracted endpoint block, up to an input permutation | Conditional squared cost |
|---|---|---|
| $h>e$ | $I-\mathrm{SWAP}$ on two input colors | $2s_P$, independent of the prefix |
| $h=e$ | $I-\zeta_m$ on one input color | $f(\zeta_m)=\operatorname{Tr}[P(I-\zeta_m)^2]$ |
| $h<e$ | Difference of two placements of an exported input color | Nonnegative; zero on every repeated pure prefix |

These statements are literal word identities; colors can take any of the $d$ values. In the last case both contractions against $|u\rangle^{\otimes k}$ extract the same $u$, with the same overlap with $w$. Thus cancellation holds before mixing. The changed bath coordinate is at most $j-1<k$.

Conditional on a charge word, input colors have density $P^{\otimes q}$, invariant under input wire permutations. Hence the first cost is

\[
\operatorname{Tr}[P^{\otimes2}(I-\mathrm{SWAP})^2]
=2(1-\operatorname{Tr}P^2).
\]

For the second, contraction of the input/bath swap gives the marginal $\zeta_m$, without a transpose. Both endpoint orientations have the displayed cost; arbitrary export sectors need only nonnegativity. No commutation of arbitrary $H_\zeta$ with $\sigma_P$ is used.

For a Hermitian density $Z$,

\[
f(Z)=\sum_i p_i(1-Z_{ii})^2
+\sum_{i<j}(p_i+p_j)|Z_{ij}|^2.
\]

Pinching therefore improves the objective and preserves feasibility. Strict convexity and the simplex KKT equations give exactly $Z_*$ above. This proves a lower bound for every marginal, including marginals of entangled states. The single density $\zeta_*$ has all marginals $Z_*$ and cancels every export sector, so all local bounds are attained simultaneously.

## Fair-walk summation

Charge patterns still have probability $2^{-k}$. The prefix height $h$ has the law of a fair-walk maximum $M_i$, while the middle deficit has the independent law of $M_\ell$, where $\ell=j-i-1$. The endpoint orientation and its adjoint together have probability $1/2$. Thus

\[
v_{P,k}=\frac12\sum_{i+\ell\le k-2}
\left[2s_P\Pr(M_i>M_\ell)+f_P\Pr(M_i=M_\ell)\right].
\]

There are $k(k-1)/2$ index pairs. Symmetry under $i\leftrightarrow\ell$ makes the strict-comparison sum half the total minus the collision sum. The collision sum is $C_k$: reflection gives

\[
\Pr(M_n=a)=\Pr(S_n=a)+\Pr(S_n=a+1),
\]

whose time generating functions have squared-sum generating function

\[
\sum_{a\ge0}\left(\sum_{n\ge0}\Pr(M_n=a)x^n\right)^2
=\frac1{(1-x)\sqrt{1-x^2}}.
\]

Coefficient comparison and summing times through $k-2$ yield the stated $C_k$, and therefore the boxed formula. The calculation preserves the source's charge probability contract. [S1, §5]

## Operator dual, support, and the failed scalar transfer

Use the source convention

\[
T_k(X)=\operatorname{Tr}_A[(X\otimes I)G_1],\quad H_*=H_{\zeta_*}.
\]

The blocks of $H_*$ are input permutations composed with $I-\mathrm{SWAP}$, $I-Z_*$, or zero. Hence $[H_*,\sigma_P]=0$. This is special to the optimizer: already at $k=2$, a coherent marginal $Z$ with $[P,Z]\ne0$ gives $[H_\zeta,\sigma_P]\ne0$. In general the real gradient uses $T_k((\sigma_PH+H\sigma_P)/2)$.

Put

\[
D=P(I-Z_*)=\min(P,tI),\qquad R=tI-D\ge0.
\]

Define nonnegative coefficients, with independent prefix and middle walks,

\[
c_{k,m}=\frac12\sum_{i+\ell\le k-2}
\Pr\bigl(m_i=m,\ h_i=e_\ell\bigr),
\]

where $m_i=-\min_{a\le i}S_a$, $h_i=S_i+m_i$, and $e_\ell=-\min_{a\le\ell}\widetilde S_a$. Then

\[
\sum_m c_{k,m}=C_k/2,\quad
c_{k,m}>0\ (0\le m\le k-2),\quad c_{k,k-1}=0.
\]

Indeed the all-pop prefix with $i=m,\ell=0$ alone gives $c_{k,m}\ge2^{-m-1}$.

The exact dual is

\[
\boxed{B:=T_k(\sigma_PH_*)
=v_{P,k}I_F+\sum_{m=0}^{k-2}c_{k,m}R^{(m)}\ge v_{P,k}I_F,}
\]

\[
(B-v_{P,k}I)\zeta_*=0.
\]

To see the critical contribution, pair $I-Z_*$ with the raw input/bath block: it gives $(\operatorname{Tr}D)I-D^{(m)}=f_PI+R^{(m)}$, since $\operatorname{Tr}(DZ_*)=t$. Input/input sectors give their constant cost; export sectors vanish. This proves the operator identity, including arbitrary bath coherences.

For every density $\zeta$, the exact projection identity is

\[
\operatorname{Tr}(\sigma_PH_\zeta^2)
=v_{P,k}+2\operatorname{Tr}[\zeta(B-v_{P,k}I)]
+\operatorname{Tr}[\sigma_P(H_\zeta-H_*)^2].
\]

It proves the dual bound and complementarity directly. With $E_0=\operatorname{span}\{|i\rangle:p_i\ge t\}$,

\[
\ker(B-v_{P,k}I)=E_0^{\otimes(k-1)}\otimes\mathbb C^d.
\]

Support in this kernel alone is insufficient for optimality; equality also requires $H_\zeta=H_*$. The minimizing observable is unique, while its representing density need not be.

The old scalar identity holds exactly when all $p_i\ge t$. Strictly excluded colors $p_i<t$ give positive slack. A zero eigenvalue of $Z_*$ at $p_i=t$ gives zero slack, so rank deficiency by itself does not imply a nonscalar dual. Full support requires $(d-1)/(\sum_i p_i^{-1})<p_{\min}$; equality is the boundary.

## Exact diagnostics

| $P$ | $t$ | $\operatorname{diag}Z_*$ | $f_P$ | $v_{P,k}$ |
|---|---:|---|---:|---|
| $(4/5,3/20,1/20)$ | $12/95$ | $(16/19,3/19,0)$ | $67/380$ | $67k(k-1)/800-603C_k/7600$ |
| $(1/2,1/3,1/6)$ | $1/5$ | $(3/5,2/5,0)$ | $11/30$ | $11k(k-1)/72-11C_k/90$ |
| $(9/10,1/10)$ | $9/100$ | $(9/10,1/10)$ | $9/100$ | $9[k(k-1)-C_k]/200$ |

The first two have $R=\operatorname{diag}(0,0,29/380)$ and $\operatorname{diag}(0,0,1/30)$, respectively. The third has $R=0$. Their $(v_{P,2},v_{P,3})$ values are respectively

\[
(67/760,2613/7600),\quad(11/60,121/180),\quad(9/200,9/50).
\]

For sorted three-color probabilities, the support transition is exactly

\[
p_3=\frac{p_1p_2}{p_1+p_2}.
\]

Below it the support has size two; above it the support is full. At the boundary example $P=(2/5,2/5,1/5)$, $Z_*=(1/2,1/2,0)$, $t=1/5$, $f_P=2/5$, $R=0$, and

\[
v_{P,k}=4k(k-1)/25-3C_k/25.
\]

`verify.py` constructs $G_1$ directly from the deep-stack $C_i$ words, then contracts matrices. It checks $k=2,3$ for all fixed diagnostics and this boundary example, including the dual matrix and the projection identity for complex coherent competitors. Maximum observed absolute error was $5.56\times10^{-16}$. These finite checks support the all-$k$ proof; they do not replace it.

## Scope, sources, and cost

This is the specified bulk susceptibility, with a retained two-seed root and sufficiently deep initial words. The finite prefix represents the coefficient; it is not a bath cutoff or physical initializer. No preparation, nonlinear transfer, coding, or capacity claim follows. In particular,

\[
-\log_2\sigma_P=kI+\sum_{a=0}^{k-1}\sum_i(-\log_2p_i)|i\rangle\langle i|_a
\]

contains color terms absent from the source's uniform two-color entropy interface.

**Sources read:** [S1] `SHARP_TEMPORAL_GROWTH.tex`, especially §§2–5; its included `INHERITED_OPERATOR_CODING.tex` and `INHERITED_COMPRESSION.tex`; the frozen `PROTOCOL.txt` and `OPERATION.txt`. No other receiver/evaluator work was read. The transferred operation guided the sector organization; its prior invention/review cost is outside this receiver's observed execution.

**Cost:** Start observed at 2026-10-22 03:39:05 UTC. Completion and elapsed time are recorded in `TIMING.json`. One verification script execution used 0.523407 measured CPU seconds and 0.073406 measured wall seconds for its timed computational portion; the execution tool reported 0.095724 wall seconds for the process. Internal timers begin after imports, so startup/import CPU is unmeasured. No expensive search or subagents were used. Inference tokens, inference cost, and total authoring/review cost are unknown.
