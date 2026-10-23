# Vanishing screening: finite adverse families and a growing-path obstruction

Owner contribution: `/root/vanishing_screen_lower`, Cycle 3, 2026-10-21 UTC.
The fixed-positive-screen theorem is received and accepted capital; this note does
not re-prove it. Its subject is the joint limit in which the screen parameter is
fixed within each run but may depend on its deterministic horizon.

## 1. Exact contract and conclusions

Fix \(K>0\), \(0<\alpha<1\), and write \(\beta=1-\alpha\). All logarithms
are natural. Each instance has a finite labelled space, strictly positive
probabilities \(\pi,q\), \(D(\pi\Vert q)\le K\), and a fixed symmetric
stochastic proposal matrix \(Q\). Let \(G\) be independence Metropolis--Hastings
with proposal \(q\). The local transition has acceptance

\[
a_\eta(x,y)=\min\{1,(q_y/q_x)^\eta\}
\min\{1,(\pi_y/\pi_x)(q_x/q_y)^\eta\}.
\]

The chain is \(C_\eta=(I+\alpha G+\beta L_\eta)/2\), initialized at \(q\).
Let \(R_\eta(n)\) be the supremum of \(\|qC_\eta^n-\pi\|_{TV}\)
over this class. The instances below depend on \(n\); every transition matrix
remains fixed for its entire run. No adaptive screen or optional horizon is used.

Put \(L=\log n\), \(u_n=\eta_n L\), and \(b_K=1-e^{-K}\). This note proves:

1. If \(u_n\to c<\infty\), then
   \[
   \liminf R_{\eta_n}(n)\ge
   \frac{\beta b_K e^{-c}}{\alpha(1-b_K)+\beta e^{-c}}>0.
   \tag{1}
   \]
   Consequently \(u_n\to\infty\) is necessary for uniform convergence.
   The root's upper argument is needed for sufficiency.
2. A uniform finite-family lower estimate, valid for \(0\le u_n\le C\log L\)
   with any fixed finite \(C\), is given in (8). In particular the elementary
   three-state critical obstruction at \(u_n=\log L+d+o(1)\) is
   \[
   \liminf L R_{\eta_n}(n)\ge
   \frac\beta\alpha(e^K-1)e^{-d}.
   \tag{2}
   \]
3. Growing monotone paths give a strictly stronger obstruction for a nonempty
   parameter range. Define
   \[
   d_*=\frac{2\alpha e^{-K}}\beta,
   \qquad
   \chi(K,\alpha)=
   \begin{cases}
   1,&d_*\ge1,\\
   r\in(0,1):\ d_*=r(1-r)^{(1-r)/r},&d_*<1.
   \end{cases}
   \tag{3}
   \]
   If \(u_n/\log L\to\lambda\in(0,1/\chi(K,\alpha))\), then
   \[
   L R_{\eta_n}(n)\longrightarrow\infty.
   \tag{4}
   \]
   This is a necessary scale for retaining the sharp coefficient \(K\), not a
   matching upper theorem or a claim that \(1/\chi\) is the true threshold.
   For \(K=1,\alpha=1/2\), \(1/\chi=1.08848276573897\ldots>1\).

The ordinary pure-IMH comparator already has coefficient \(K\). Taking \(Q=I\)
also supplies the inherited \(\liminf L R_{\eta_n}(n)\ge K\) independently of
these constructions. Neither the adverse examples nor the fixed-positive-screen
theorem establishes a computational speedup.

## 2. Three-state family and a uniform crossover bound

Fix \(0<b<b_K\), and choose \(M>2\). Set \(p=L^{-M}\) and, on states
\(A,B,*\), let

\[
q_A=\frac p{nL^2},\quad q_B=b,\quad q_*=1-b-q_A,
\qquad
\pi_A=p,\quad\pi_B=p n^{-4},\quad\pi_*=1-p-pn^{-4}.
\tag{5}
\]

The proposal \(Q\) swaps \(A,B\) and fixes \(*\). It is target-independent,
symmetric, and stochastic. All probabilities are positive for sufficiently large
\(n\). The weights satisfy
\(W_A=nL^2\), \(W_B=p/(bn^4)\), and \(W_*\to1/(1-b)\), so eventually
\(W_B<W_*<W_A\). Furthermore

\[
D(\pi\Vert q)
=p\log(nL^2)+pn^{-4}\log\frac{pn^{-4}}b
 +(1-p-pn^{-4})\log\frac{1-p-pn^{-4}}{1-b-q_A}
\longrightarrow-\log(1-b)<K.
\]

Thus the family is admitted with fixed asymptotic KL slack. It is not singular.

Write \(r=(q_A/b)^{\eta_n}\). The exact local acceptances are \(r\) for
\(B\to A\) and \(n^{-4}r\) for \(A\to B\); the second acceptance factor
is one on the forward edge. The actual full-chain transition probabilities are

\[
x=C(B,A)=\tfrac12(\alpha q_A+\beta r),\qquad
y=C(B,*)=\tfrac12\alpha q_*,
\]
\[
d=x+y=\tfrac12[\alpha(1-b)+\beta r],\qquad
e=1-C(A,A)=\frac{\alpha(1-p)}{2nL^2}+\frac{\beta r}{2n^4}.
\tag{6}
\]

Consider only paths that start at \(B\), first exit \(B\) to \(A\) by time
\(n\), and never subsequently leave \(A\). Their mass is exactly

\[
E_n=bx\sum_{j=1}^n(1-d)^{j-1}(1-e)^{n-j}
=bx\frac{(1-e)^n-(1-d)^n}{d-e}.
\tag{7}
\]

The sum defines the coincident-denominator case without ambiguity. Since
\(d\ge\alpha(1-b)/2\) and \(ne\le\alpha/(2L^2)+\beta/(2n^3)\), the simpler
bound
\(E_n\ge b(x/d)[1-(1-d)^n](1-e)^{n-1}\), together with \(E_n\le bx/d\),
gives a **relative** estimate \(E_n=(bx/d)(1+O(L^{-2}))\), uniform in all
\(\eta_n\ge0\).

For any fixed \(C<\infty\), uniformly for \(0\le u_n\le C\log L\),

\[
r=e^{-u_n}\exp\left[-\frac{u_n}{L}\{(M+2)\log L+\log b\}\right]
=e^{-u_n}\left(1+O_{b,M,C}\left(\frac{(\log L)^2}{L}\right)\right).
\]

Also \(q_A/r\to0\) uniformly on that range. Therefore, with
\(F_b(u)=b\beta e^{-u}/[\alpha(1-b)+\beta e^{-u}]\),

\[
E_n=F_b(u_n)(1+o(1)),\qquad
R_{\eta_n}(n)\ge E_n-p
\ge F_b(u_n)(1-o(1))-L^{-M}.
\tag{8}
\]

The \(o(1)\) in the first formula is relative and uniform on the displayed
range. Choosing \(M>C+2\) makes \(p=o(F_b(u_n))\) throughout that range.
For bounded \(u_n\to c\), any \(M>2\) suffices; then let \(b\uparrow b_K\)
after taking the lower limit to obtain (1). If \(u_n\) fails to tend to
infinity, pass to a subsequence along which it has a finite limit to get a
strictly positive obstruction. This is a statement about the supremum over
instances, not an equality formula for its worst-case risk.

If \(u_n=\log L+d+o(1)\), then \(r\sim e^{-d}/L\), and (8) yields
\(\liminf LR\ge(\beta/\alpha)(b/(1-b))e^{-d}\). Letting
\(b\uparrow b_K\) proves (2). If \(u_n=o(\log L)\), (8) instead gives
\(LR\to\infty\); a fixed \(M>2\) suffices eventually. More generally if
\(u_n/\log L\to\lambda<1\), it gives \(LR\to\infty\).

## 3. A growing path with multiplicative capture and retention

Fix \(b\in(0,b_K)\) and \(v>0\). Suppose \(u_n\to\infty\) and
\(u_n=O(\log L)\). Set

\[
m=\max\{1,\lfloor u_n/v\rfloor\},\qquad p=L^{-M},\qquad
z=\left(\frac{p}{bnL^2}\right)^{1/m}.
\tag{9}
\]

The exponent \(M>2\) will be chosen large enough for the desired scaled
comparison below. On states \(0,1,\ldots,m,*\), put

\[
q_i=bz^i,\quad q_*=1-\sum_{i=0}^m bz^i,\qquad
\pi_i=pn^{-2(m-i)},\quad \pi_*=1-\sum_{i=0}^m pn^{-2(m-i)}.
\tag{10}
\]

Let \(Q(i,i+1)=Q(i+1,i)=1/2\). The two path endpoints have diagonal entry
\(1/2\), all internal diagonal entries are zero, and \(Q(*,*)=1\).
This is a fixed symmetric stochastic matrix on its labelled instance; its
definition never uses an evaluated target value. Its support size is \(m+2\).

Because \(m=O(\log L)\),
\[
z=\exp\left[-\frac{L+(M+2)\log L+\log b}{m}\right]
\]
tends to zero faster than any fixed inverse power of \(L\). Thus all
probabilities are positive eventually, \(q_*\to1-b\), and \(\pi_*\to1\).
The terminal weight and all other path weights are

\[
W_m=nL^2,\qquad W_i=W_m(z/n^2)^{m-i}.
\tag{11}
\]

In particular \(W_{m-1}=L^2z/n\to0\), and eventually
\(W_0<\cdots<W_{m-1}<W_*<W_m\). All transitions used below have their
acceptance branch fixed by these inequalities.

### 3.1 Forward KL admission

The terminal contribution is \(p\log(nL^2)\to0\). For \(j=m-i\ge1\),
\(\pi_i=pn^{-2j}\) and
\(\log W_i=\log(nL^2)+j(\log z-2L)\).
Since \(|\log z|=O(L)\) for \(m\ge1\), summing the absolutely bounded
transient contributions gives

\[
\sum_{i<m}\pi_i|\log W_i|
\le p\sum_{j\ge1}n^{-2j}\{O(L)+jO(L)\}=O(pL/n^2).
\]

The star contribution tends to \(-\log(1-b)\). Hence
\(D(\pi\Vert q)\to-\log(1-b)<K\), just as for the three-state family.
The formula remains valid while \(m\) grows; no lower bound on state
probabilities or upper bound on support size was used.

### 3.2 Actual branches and marked forward moves

Write \(s=z^{\eta_n}\). On every forward edge, the first acceptance factor
is \(s\), the second is one (its argument is \(n^2z^{-\eta_n}\)). On the
reverse edge the acceptance is \(n^{-2}s\). A **marked local forward move**
therefore has probability
\[
f=\beta s/4.
\tag{12}
\]
The mark distinguishes it from any global move to the same adjacent state.
We retain self loops, require the next nonself exit to have this mark at
each transient state, and discard every other exit. This defines an actual
event in the mixture construction and cannot count an unexecuted transition.

Let \(e_i=1-C(i,i)\) for \(i<m\), and set
\[
S_q=\frac{bz}{1-z},\quad
D=\frac\alpha2(1-b-S_q),\quad
\delta=\frac\alpha2\left(S_q+\frac{bn^{-2}}{1-n^{-2}}\right)
           +\frac\beta{4n^2},\quad
E=f+\frac\alpha2(1-b)+\delta.
\tag{13}
\]
For sufficiently large \(n\), \(D>0\) and
\[
D\le e_i\le E\quad(0\le i<m).
\tag{14}
\]
Indeed the global exit to the star is accepted and contributes
\(\alpha q_*/2\ge D\). The global mass to higher path states is at most
\(S_q\), while that to lower path states is exactly
\[
\sum_{j<i}G(i,j)=\sum_{j<i}\pi_j/W_i
=q_i\sum_{r=1}^i n^{-2r}
\le\frac{bn^{-2}}{1-n^{-2}}.
\]
The star term is at most \(\alpha(1-b)/2\), and the reverse local exit is
at most \(\beta/(4n^2)\). Adding these to (12) proves the upper bound in
(14). This deliberately loose bound retains all return and competing paths
as excluded-event mass; none is incorrectly counted as a successful capture.

At state \(i\), the next exit is marked forward with probability \(f/e_i\).
For any integer \(h\ge1\), the joint probability that it is marked forward
and occurs in at most \(h\) steps is
\[
\sum_{j=1}^h(1-e_i)^{j-1}f
=\frac f{e_i}\{1-(1-e_i)^h\}
\ge\frac fE(1-e^{-Dh}).
\tag{15}
\]
Thus the timing correction is **multiplicative relative to capture**; no
absolute error of order \(1/n\) is subtracted from a tiny path probability.

Choose \(h=\lfloor n/(2m)\rfloor\). The marked path is completed by
\(mh\le n/2\) with probability at least
\[
b(f/E)^m(1-e^{-Dh})^m
\ge b(f/E)^m[1-me^{-Dh}]_+.
\]
At the terminal state, the exact escape probability is
\[
e_m=\frac{\alpha(1-p)}{2nL^2}+\frac{\beta s}{4n^2}.
\tag{16}
\]
Conditioning on the arrival time, retention until time \(n\) has probability
at least \((1-e_m)^n\ge1-\alpha/(2L^2)-\beta/(4n)\). Therefore the following
fully explicit finite bound holds whenever the positive-probability and weight
ordering conditions above hold:

\[
\boxed{\quad
R_{\eta_n}(n)\ge
b\left(\frac fE\right)^m
[1-me^{-D\lfloor n/(2m)\rfloor}]_+
\left[1-\frac\alpha{2L^2}-\frac\beta{4n}\right]_+-p.
\quad}
\tag{17}
\]

The bound is witnessed by the actual event \(X_n=m\). It uses deterministic
time \(n\) throughout. There is no application of a fixed-count law to an
expected or optional count.

### 3.3 Logarithmic capture exponent

Let \(d_b=2\alpha(1-b)/\beta\). From (9),
\[
\log s=-\frac{u_n}{m}
-\frac{\eta_n}{m}\{(M+2)\log L+\log b\}.
\]
Here \(u_n/m\to v\); the second term is \(O(\log L/L)\). Multiplying it
by \(m\) still gives \(O((\log L)^2/L)=o(1)\).
Also \(m\delta\to0\). Consequently
\[
\log\{b(f/E)^m\}
=-m\log(1+d_b e^{u_n/m})+\log b+o(1)
=-\phi_{d_b}(v)u_n+O(1),
\tag{18}
\]
where
\[
\phi_d(v)=\frac{\log(1+d e^v)}v.
\tag{19}
\]
The \(O(1)\) term includes integer rounding of \(m\); an exact limiting
prefactor is not asserted. The waiting and retention factors in (17) are
\(1-o(1)\), multiplicatively. If \(u_n/\log L\to\lambda\in(0,\infty)\)
and \(M>\lambda\phi_{d_b}(v)+2\), subtraction of \(p\) is negligible, so
\[
R_{\eta_n}(n)\ge L^{-\lambda\phi_{d_b}(v)+o(1)}.
\tag{20}
\]
If \(\lambda\phi_{d_b}(v)<1\), this proves \(L R\to\infty\). Taking a
large fixed \(M\) is part of specifying the admitted family; it does not
change the kernel during a run or use a target evaluation to set a screen.

## 4. Optimization and a certified separation

When \(d\ge1\), \(\phi_d(v)>1\) for finite \(v>0\), and its infimum is
one as \(v\to\infty\). When \(0<d<1\), the derivative has the sign of
\[
g(v)=\frac{vde^v}{1+de^v}-\log(1+de^v).
\]
Its derivative is \(g'(v)=vde^v/(1+de^v)^2>0\), its right limit at zero
is \(-\log(1+d)<0\), and its limit at infinity is \(-\log d>0\).
There is a unique minimum. Put \(r=de^v/(1+de^v)\) there. The critical
equation gives \(rv=-\log(1-r)\), and hence
\[
\inf_{v>0}\phi_d(v)=r,\qquad
d=r(1-r)^{(1-r)/r},\qquad
v=-\frac{\log(1-r)}r.
\tag{21}
\]
The logarithm of the expression for \(d\) has derivative
\(-\log(1-r)/r^2>0\); it maps \(r\in(0,1)\) continuously and strictly
increasingly onto \(d\in(0,1)\). This proves uniqueness and continuity.

Letting \(b\uparrow b_K\) sends \(d_b\downarrow d_*\). For every strict
\(\lambda<1/\chi(K,\alpha)\), continuity supplies a **fixed**
\(b<b_K\) and finite \(v>0\) with \(\lambda\phi_{d_b}(v)<1\), proving
(4). Improvement beyond the three-state threshold occurs precisely in this
construction when
\[
\frac{2\alpha e^{-K}}{1-\alpha}<1,
\quad\text{equivalently}\quad
\alpha<\frac1{1+2e^{-K}}.
\tag{22}
\]
For \(\alpha\ge1/3\), this can also be written
\(K>\log(2\alpha/(1-\alpha))\); for \(\alpha<1/3\), every \(K>0\)
satisfies it. Equality gives no strict improvement by this path calculation.

### An exact example at \(K=1,\alpha=1/2\)

Take \(b=63/100\), \(v=\log16\), \(M=4\), and
\[
\eta_n=\frac{27}{25}\frac{\log\log n}{\log n}.
\tag{23}
\]
This \(b\) has strict KL slack: \(e>65/24>100/37\), where the first
inequality follows from the first five terms of the exponential series and
the second is the integer inequality \(2405>2400\). Thus \(b<1-e^{-1}\).
Here \(d_b=37/50\), and
\[
\lambda\phi_{d_b}(v)
=\frac{27\log(321/25)}{25\log16}<1
\tag{24}
\]
because the equivalent integer comparison is
\[
321^{27}<25^{27}16^{25}.
\]
The accompanying executable checks the integer comparison exactly. The
exponent is approximately \(0.9942947902838462\); therefore this family has
\(L R\to\infty\) even though the screen exceeds the elementary scale by
the fixed factor \(27/25>1\). The divergence is very slow. Moderate-size
matrix diagnostics must not be advertised as having observed its asymptotic
divergence.

At the boundary \(b\uparrow1-e^{-1}\), numerical solution of (21) gives
\[
d_*=2/e=0.7357588823428846\ldots,\quad
\chi=0.9187099984271229\ldots,
\]
\[
1/\chi=1.0884827657389706\ldots,\qquad
v_{\rm opt}=2.7318003027848617\ldots.
\]
These decimals are diagnostics; (21) is the defining mathematical result.

## 5. Information, comparisons, failures, and what remains open

The constructor specifies \(q,Q\) publicly. A run needs iid proposal draws,
known proposal masses, target ratios at visited/proposed states, mixture coins,
and acceptance coins. The target normalizer is irrelevant to each MH ratio.
The proof and diagnostic executable contain complete target tables to verify
the adverse family; this is mathematical ground truth, not additional access
quietly given to the sampler. If a user instead possesses the complete finite
target table, direct finite sampling is a stronger ordinary method, and these
examples make no claim of operational superiority in that different contract.

Failed or insufficient approaches that changed this construction:

* The one-edge family does establish the necessary convergence scale and its
  exact crossover event, but does **not** justify a universal sharp-K
  threshold at \(u\sim\log\log n\). The growing path explicitly defeats that
  conjecture in (23)--(24).
* Divergence of a linear \(qL/q\) bound alone would not establish adverse
  finite-time TV. Here (17) is an actual event with all competing exits and
  subsequent retention accounted for.
* An absolute timing-error subtraction could swamp critical capture. The
  marked-exit calculation (15) supplies the needed relative correction.
* A path event without return accounting would be incomplete. The construction
  gives target-increasing edges and bounds every reverse exit; the terminal
  global and local escape probabilities are explicit in (16).
* Numerical examples at accessible horizons do not identify the worst-case
  asymptotic coefficient. Floor effects, KL slack, and slow exponents matter.
  Diagnostics verify finite admitted chains and bound consistency only.

No new family beyond these two is claimed. The consequential remaining lower/
upper question is whether the optimized growing-path obstruction captures the
true sharp coefficient-preserving screen scale, or whether other admitted
transport mechanisms force a larger scale. This note does not settle that
question, does not establish historical novelty, and makes no claim about
time-varying screens, nonreversible local kernels, deterministic schedules,
empirical KL, or ideal-real numerical guarantees.

## 6. Replay and source binding

From the directory containing these files, run
`python vanishing_lower_checks.py`. The script uses paths relative to its own
location, so the same command works after extraction into a different directory.
It records exact integer checks, high-precision
finite transition matrices, full deterministic matrix-power laws, the finite
event bounds, precision/stationarity residuals, and its measured resources.
Its JSON outputs distinguish rigorous symbolic/exact-integer claims from
non-interval numerical diagnostics. Full proof and source hashes are recorded
in `vanishing_lower_receipt.json` after the final edit. Parent packaging and
private delivery remain the root's responsibility.

The completed replay evaluated 16 actual finite chains twice, with reserved
decimal precisions 90 and 120 (total working precision up to 392 and 422,
respectively). Each replay used 3,100 matrix squarings/products and 16
row-matrix products; it did not simulate the astronomical horizons one step
at a time. The largest observed TV difference across precisions was below
\(1.08\times10^{-91}\). The four growing-path examples used horizons
\(2^{20},2^{80},2^{320},2^{1000}\) and one, one, two, two edges. Their
\((\log n)TV\) values were approximately 0.02944, 0.09698, 0.29343,
0.43074. These are admitted diagnostic examples and **do not numerically
demonstrate** the eventual divergence in (24), whose exponent is very small.

Successful replay wall times were approximately 0.412 and 0.608 seconds, with
peak process RSS about 12 MiB; exact records accompany the outputs. One
earlier numerical assertion used an unjustified retained-precision tolerance
at the largest horizon and failed; its precise correction is preserved in
`vanishing_lower_failed_checks.txt`. Full mathematical discovery/model cost
is not available and is not identified with replay time. This construction
required no external compute purchase, hardware, intervention, or outreach.
