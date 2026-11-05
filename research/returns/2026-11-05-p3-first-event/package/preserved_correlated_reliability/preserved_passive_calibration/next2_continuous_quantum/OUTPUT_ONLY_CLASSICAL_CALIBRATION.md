# Output-only local Hamiltonian calibration with finite classical optical measurements

Working construction for the parent research run. The physical finite-local-oscillator acquisition lemma is supplied by the parent; this note completes the response inversion, finite classical forward computation, and an access-matched exposure lower bound. All earlier results remain separate.

## 1. Concrete consequence and scope

A single inaccessible, continuously evolving quantum source can reveal all coefficients of a bounded-degree local Hamiltonian through ordinary measurements of its calibrated local Pauli output ports. No source preparation, source unitary control, source readout, coherent field collector, or receiver quantum memory is needed for this calibration operation. The optical measurement windows have a fixed duration chosen from the dynamical bounds; their duration does not shrink as the requested coefficient accuracy improves.

The construction uses positive-duration output correlations, their time reversals, a globally convergent nonlinear inverse, and an explicit finite connected-cluster computation. It does not replace the coherent archive needed to recover an arbitrary first quantum payload. That archive remains a separate, potentially prohibitive resource if the calibration is used in the earlier deferred-decoder construction.

For fixed local arity and candidate degree, every positive known reset rate admits the construction. Weak monitored coupling, low detection efficiency, high local degree, and stringent accuracy incur the costs displayed below. The particularly clean regime is sufficiently strong local reset, where the coefficient precision and simultaneous-learning exposure dependence match a passive-output lower bound up to logarithms and fixed local constants. No practical superiority is claimed from polynomial notation alone.

## 2. Model and acquired resources

There are n qubits and a known complete list of distinct, nonidentity Pauli candidates:

\[
H(\theta)=\sum_{P\in{\cal P}}\theta_P P,\qquad
|\operatorname{supp}P|\le k,\qquad M=|{\cal P}|.
\]

The coefficients are static for the entire acquisition. Assume J>0, k>=1 and a nonempty candidate list; J=0 or an empty list is the trivial known-zero problem. The promised parameter domain is

\[
\Theta_J=\left\{\theta:\max_i\sum_{P:i\in\operatorname{supp}P}|\theta_P|\le J\right\}.
\]

Let d bound the number of candidate terms touching any site. A known geometric lattice with bounded interaction range and all allowed Pauli axes is one example. A complete list of all k-site supports need not have bounded d. The complete candidate list and absence of omitted interactions are premises, not consequences of the short observation.

The calibrated source-field couplings are

\[
L_{i,a}=\frac{\sqrt r}{2}\sigma_{i,a},\qquad a=X,Y,Z,
\]

with independent vacuum input fields, r>0 known, and Markovian source generator

\[
{\cal L}_H=-i[H,\cdot]+r\sum_i({\cal R}_i-\mathrm{id}),\qquad
{\cal R}_i(\rho)=I_i/2\otimes\operatorname{Tr}_i\rho.
\]

The source's initial state is arbitrary, and may be entangled with an inaccessible reference. The maximally mixed state is stationary for every allowed H. The Pauli axes, output phases and relative gains, time scale, and detector efficiencies must be calibrated. Additional unknown noise, drift, hidden terms, non-Markovian memory, or an unobserved port model are not inferred away.

All 3n ports are measured concurrently. Fixed known optical detection efficiency \(\kappa>0\) is allowed. The hardware is a finite coherent local oscillator, balanced splitter and two photon counters per monitored port, with ordinary classical integration windows. The full acquisition therefore pays O(n) optical channels and total local-oscillator flux O(n/w) at fixed efficiency, not a fixed aggregate optical interface independent of source size. Finite detector bandwidth, timing, port crosstalk and gain/phase errors must meet a per-experiment moment-bias budget; they are not free consequences of the Markov model. The constant-loss model must apply to the measured modes, or actual filter distortion must be charged to that bias. This is not a theorem of fixed aggregate optical bandwidth.

The calibrated operator-valued port model is a supplied experimental resource. Photon rates can be checked without knowing H because their intensities are scalar, but intensity measurements alone do not establish the Pauli operators, their axes, purity, independence, or absence of other couplings. Acquiring or certifying that whole model is not solved by this protocol.

The construction never measures a source Pauli directly. Pauli operators below label known output-port quadratures.

## 3. One common two-window experiment

Choose a window length w with q=rw<=1. Use adjacent windows [0,w] and [w,2w]. For target P of weight b, choose any i in its support and a single-site Pauli B_i anticommuting with P_i. Define the signed Hermitian Pauli

\[
Q=iPB_i.
\]

The support of Q is the support of P. On sites other than i, Q_j=P_j; its overall sign can be assigned to one measured factor.

For ideal unit-efficiency homodyne notation, let

\[
X_{j,a}^{\mathrm{front}}
 =w^{-1/2}\int_0^w dY_{j,a}(t),\qquad
X_{j,a}^{\mathrm{back}}
 =w^{-1/2}\int_w^{2w}dY_{j,a}(t).
\]

The measured record obeys
\(dY_{j,a}=\sqrt r\,\operatorname{Tr}(\sigma_{j,a}\rho_t^c)dt+dW_{j,a}\).
This notation is only a way of writing the moments. Section 9 gives finite-local-oscillator observations with exactly the same means.

Form two products from the same record:

\[
Y_P^{\to}=
\left(\prod_{j\in\operatorname{supp}P}X_{j,Q_j}^{\mathrm{front}}\right)
X_{i,B_i}^{\mathrm{back}},
\qquad
Y_P^{\leftarrow}=
X_{i,B_i}^{\mathrm{front}}
\left(\prod_{j\in\operatorname{supp}P}X_{j,Q_j}^{\mathrm{back}}\right).
\]

Use the normalized, antisymmetric observation

\[
Y_P^{\mathrm{odd}}
=\frac{Y_P^{\to}-Y_P^{\leftarrow}}
       {2q^{(b+1)/2}}.
\]

Every candidate product uses the same recorded two windows. There are no M separate source experiments: each repetition supplies all M classical estimators, at O(kM) arithmetic cost. The logarithm of M enters the simultaneous statistical guarantee. A known Pauli sign is handled classically.

## 4. Exact regression, time reversal, and a positive linear coefficient

Let \({\cal J}_A(X)=(AX+XA)/2\). Multichannel output regression expresses an ordered output moment through propagators \(e^{t{\cal L}_H}\) and the Jordan insertions \(\sqrt r\,{\cal J}_A\). Integration over distinct port/time modes gives the preceding product means. After division by \(q^{(b+1)/2}\), the absolute value of the resulting source effect is at most one, uniformly over the source state: Jordan maps have operator norm at most one, the adjoint channel is a contraction, and the normalized integration volume is one.

Let \(G_P(H)\) be the stationary mean of \(Y_P^{\mathrm{odd}}\). Normalized Hilbert-Schmidt adjoints satisfy

\[
{\cal L}_H^\dagger={\cal L}_{-H},\qquad
{\cal J}_A^\dagger={\cal J}_A.
\]

The noise is self-adjoint and the Hamiltonian commutator changes sign. Reverse the trace word and the time coordinates t->2w-t. This turns the forward product into the reverse product and proves exactly

\[
\mathbb E_{I/2^n}Y_P^{\leftarrow}(H)
=\mathbb E_{I/2^n}Y_P^{\to}(-H).
\]

Consequently G is odd in H, so every even Hamiltonian order cancels. This uses stationarity; nonstationary initial-state effects are handled by the paid forgetting intervals below.

At H=0 the mean is zero. A first-order Hamiltonian insertion has nonzero final Pauli trace only if its Pauli is P. Thus the response derivative is diagonal in the complete candidate family:

\[
G_P(H)=w C_b(q)\theta_P+R_P(H).
\]

All first-order contributions have the same sign. An insertion must occur after the front measurement at site i. With front time x, back time z, and insertion time u in units of w, the exact coefficient is

\[
C_b(q)=
2\int_1^2dz\int_0^1dx\ e^{-q(z-x)}
\int_x^zdu\ [A_q(u)]^{b-1},
\qquad
A_q(u)=\int_0^1e^{-q|u-t|}\,dt.
\]

Every integrand is positive. For 0<q<=1,

\[
2=C_b(0)\ge C_b(q)\ge c_b:=C_b(1)>0.
\]

There is also a useful exact numerical-free lower bound:

\[
C_b(q)\ge2e^{-2bq}.
\]

Indeed, every one of the b site-wise noise lengths in the original positive regression integral is at most two in units of w. Replacing their exponential product by \(e^{-2bq}\) leaves the zero-noise integral, whose value is two. This bound is close to the exact coefficient when q is small and is much better there than using the uniform c_b. In the finite-time contraction certificate below, C_b(q) may therefore be replaced by the computable lower bound \(2e^{-2bq}\); this can certify a larger weak-window experiment without numerical quadrature.

The noise length at site i is z-x. On each other site j it is the absolute difference between the insertion time and that site's front measurement time; integrating those times gives \(A_q(u)^{b-1}\). This proves the formula without taking a time derivative or a vanishing measurement window.

For the common adjacent-window schedule,

| b | c_b |
|---|---:|
| 1 | 0.6681289718 |
| 2 | 0.4041133844 |
| 3 | 0.2592800494 |
| 4 | 0.1736661755 |

These are quadrature values of an explicit one-dimensional-reducible integral, not experimental simulations. The coefficients can instead be enclosed by interval quadrature at any finite needed precision.

### The order b+1 is necessary for stationary sign information in a hard family

For the single-interaction family \(H_\theta=\theta P\), with P of weight b, all stationary local quadrature moments of order at most b are invariant under theta->-theta. To see this, expand any regression word in Hamiltonian insertions. Noise is diagonal in the Pauli basis, a Jordan insertion multiplies by its single-site Pauli or gives zero, and a Hamiltonian insertion multiplies by P or gives zero. A term of odd Hamiltonian order can have a nonzero final trace only if the product of its measured single-site Paulis equals P up to phase. Fewer than b measured factors cannot cover its support. With exactly b, there must be one factor on each support site, with that same Pauli axis. Every intermediate product then commutes with P, so the first Hamiltonian commutator is zero. Every odd order therefore vanishes. The finite-dimensional moment is analytic, so this is an exact sign ambiguity, not just the absence of a first derivative.

The (b+1)-point response above is thus of minimal correlation order for obtaining signed information uniformly over this stationary hard family. This is a restriction on moment order, not a lower bound against arbitrary processing of the full classical record, which contains higher moments implicitly.

## 5. Two uniform expansions

Use the Pauli coefficient l1 norm. A nonidentity Pauli A of weight v is an eigenvector of the noise with eigenvalue -rv. The Hamiltonian commutator sends it to Paulis with total absolute coefficient at most

\[
2\sum_{P:[P,A]\ne0}|\theta_P|\le2Jv.
\]

All Jordan insertions in this construction map a Pauli to a Pauli or zero and have l1 norm at most one.

### 5.1 Damping-aware bound, useful when w=1/r

Set \(\alpha=2J/r\). Consider a term with l Hamiltonian insertions in one propagator segment. For each Pauli path, drop the final damping factor and extend each waiting interval before an insertion to infinity. Its integrated transition weight is bounded by the product of

\[
\frac{|({\cal K}_H)_{A',A}|}{r\,\operatorname{wt}(A)}.
\]

Each column of this nonnegative transition matrix sums to at most alpha. Identity inputs have no positive-order Hamiltonian term. Hence the l-th Dyson term of any one segment has l1 operator norm at most \(\alpha^l\), uniformly in its duration.

There are b propagator gaps in a stationary (b+1)-point regression word. Distributing l insertions over those gaps gives

\[
\big|G_{P,l}(H)\big|
\le {l+b-1\choose b-1}\alpha^l.
\]

The same inequality before odd antisymmetrization bounds both directions. Only odd l survive in G. The bound is independent of n and does not discard the physically useful depolarizing damping.

For H,H' in \(\Theta_J\), let
\(\Delta J=\max_i\sum_{P\ni i}|\theta_P-\theta'_P|\).
Telescoping one insertion in an l-th order word introduces the factor \(l\Delta J/J\). Summing odd l>=3 proves

\[
|R_P(H)-R_P(H')|
\le\frac{\Delta J}{J}\, b\alpha
\left[
\frac{(1-\alpha)^{-b-1}+(1+\alpha)^{-b-1}}2-1
\right].
\]

At w=1/r the diagonal coefficient is \(c_b/r\). Since
\(\Delta J\le d\|\theta-\theta'\|_\infty\), a sufficient normalized remainder bound is

\[
\rho_{\rm damp}=
\max_{1\le b\le k}
\frac{2db}{c_b}
\left[
\frac{(1-\alpha)^{-b-1}+(1+\alpha)^{-b-1}}2-1
\right].
\tag{1}
\]

For small J/r the leading term is
\(4d\,b(b+1)(b+2)(J/r)^2/c_b\).
Unlike the unsymmetrized response, the leading inverse error is quadratic in J/r.

### 5.2 Finite-time bound, valid at every r>0

Put \(a=\max(1,k-1)\), \(x=4aJw\), \(p_b=b/a\). The union of all measured sites has size b. After l previous nonzero commutator insertions, its enlarged support has size at most b+(k-1)l. The total length of all propagator gaps is at most 2w. Discarding damping, summing all placements, and integrating over the ordered time simplex gives the degree-l bound

\[
\big|G_{P,l}(H)\big|
\le\frac{(p_b)_l}{l!}x^l.
\]

It is valid with a=1 when k=1 as a loose upper bound. For x<1, summing the odd remainder after telescoping yields

\[
\rho_{\rm time}=
\max_{1\le b\le k}
\frac{4db}{C_b(q)}
\left[
\frac{(1-x)^{-p_b-1}+(1+x)^{-p_b-1}}2-1
\right].
\tag{2}
\]

Either (1) or (2) can be used as the contraction certificate. A simple universal choice, avoiding optimization, is

\[
C_*=\max_{1\le b\le k}\frac{b}{c_b},\qquad
A_k=64a\sqrt{C_*},\qquad
w=\frac1{r+A_k\sqrt d\,J}.
\tag{3}
\]

Then q<=1 and \(x\le1/(16\sqrt{dC_*})\). Since \(p_b\le2\), the bracket in (2) is at most \(16x^2\) for x<=1/2. Thus \(\rho_{\rm time}\le1/4\). This establishes an accuracy-independent window for every r>0. More economical windows can be chosen by explicitly checking (1) or (2) with the known quantities.

Formula (3) is conservative. In particular it is not a claim that arbitrarily weak ports yield inexpensive acquisition. Their reduced signal is paid through q below.

## 6. A globally convergent, finite nonlinear inverse

Let \(\lambda_P=w C_{|P|}(q)\), \(\lambda_*=\min_P\lambda_P\), and let D_lambda be the diagonal matrix of these coefficients. Suppose the measured vector y has

\[
\|y-G(\theta_*)\|_\infty\le\delta,\qquad
\delta=\lambda_*\eta/32.
\]

Suppose a classical evaluator supplies \(\widetilde G(\theta)\) with the same absolute error delta for every queried \(\theta\in\Theta_J\). Section 7 constructs this evaluator.

Start from theta_0=0 and iterate

\[
z_t=\theta_t+
D_\lambda^{-1}\big(y-\widetilde G(\theta_t)\big),\qquad
\theta_{t+1}\in\arg\min_{\theta\in\Theta_J}
\|\theta-z_t\|_\infty.
\]

The projection is a finite linear program: represent absolute values by auxiliary variables, impose the per-site l1 budgets and minimize the sup distance. No unsupported claim of nonexpansive projection in this norm is needed. Since the true parameter is feasible, any nearest projection has distance to it at most twice the unprojected distance. The positive coefficients C_b(q) can be enclosed by finite interval quadrature; their normalization error must also be allocated. For example a relative diagonal error of order eta/J is sufficient within fixed constants. None of these steps assumes exact real arithmetic.

If either contraction certificate is at most 1/4, then

\[
\|\theta_{t+1}-\theta_*\|_\infty
\le\frac12\|\theta_t-\theta_*\|_\infty
+4\delta/\lambda_*.
\]

After

\[
t_{\rm inv}\ge
\left\lceil\log_2(2J/\eta)\right\rceil_+
\]

iterations, the error is at most 3eta/4 before additional arithmetic errors: the initial error contributes at most eta/2 and the accumulated response errors at most eta/4. The remaining eta/4 can pay finite LP, diagonal-normalization and arithmetic errors. The iteration corrects the full nonlinear response; it does not declare the cubic term to be zero.

## 7. Polynomial forward evaluation by connected sets

Literal enumeration of l nested-commutator words has as many as (d l)^l candidates. With l logarithmic in inverse accuracy, that observation alone gives only a quasipolynomial bound. The following connected-set construction supplies a polynomial algorithm.

Fix one response P and let R be its measured site set, |R|=b. Form the interaction overlap graph: each candidate Pauli is a vertex, intersecting supports are adjacent, and an auxiliary root is adjacent to all terms touching R. The maximum graph degree is at most kd.

For a finite set S of interaction vertices, write \(H_S=\sum_{P\in S}\theta_PP\), and define its Boolean-lattice connected contribution

\[
\Phi_P(S)=
\sum_{T\subseteq S}(-1)^{|S|-|T|}G_P(H_T).
\]

If S has any component disconnected from the root, the output response is independent of that component, and its alternating subset sum cancels. Thus only root-connected S contribute.

Expand the response into Hamiltonian Dyson words. A word with distinct interaction set U occurs in \(G_P(H_T)\) exactly when U is a subset of T. The alternating subset sum is one if U=S and zero otherwise. Consequently Phi(S) is precisely the sum of all words whose distinct interaction set is S, including arbitrarily many repetitions of its terms.

The full response equals the sum of these contributions. Summing only root-connected sets of size at most L omits only words of Hamiltonian order greater than L. Therefore its error is bounded by either of the explicit tails

\[
E_{b,L}^{\rm damp}
=\sum_{\substack{l>L\\l\ {\rm odd}}}
{l+b-1\choose b-1}\alpha^l,
\qquad
E_{b,L}^{\rm time}
=\sum_{\substack{l>L\\l\ {\rm odd}}}
\frac{(p_b)_l}{l!}x^l.
\]

Use whichever expansion is certified. For example, at alpha<=1/4,
\(E_{b,L}^{\rm damp}\le2^b2^{-L-1}\).
At x<=1/4 and \(p_b\le2\),
\(E_{b,L}^{\rm time}\le4\,2^{-L-1}\).
The actual odd tails are substantially sharper and are finite scalar computations.

There are at most \((4kd)^l\) root-connected vertex sets of size l: choose a plane rooted spanning tree (at most \(4^l\) shapes) and at most kd neighbor labels per edge. A rooted ordering shows that a set of size l acts on at most b+(k-1)l source qubits.

For each subset T of each retained set S, compute \(G_P(H_T)\) on those qubits. It suffices to propagate finite moment equations. During a front window, use one operator register \(M_U\) for every subset U of the b selected channels:

\[
\frac{dM_U}{ds}
=w{\cal L}_{H_T}M_U+
\sum_{j\in U}{\cal J}_{Q_j}M_{U\setminus\{j\}},
\]

where s=t/w runs from zero to one in each window. The initial empty-subset register is the maximally mixed state and all other registers are zero. The q-normalization makes every insertion coefficient one in these dimensionless equations. At w=1/r the evolution generator is L/r. Propagate one additional back-channel register, take its trace, and repeat with the reversed arrangement. The number of operator coordinates is at most \(2^{b+1}4^{b+(k-1)L}\).

An exponential action by a certified Taylor series, or any equivalent finite linear algebra algorithm, computes the moment to prescribed absolute error. The matrix l1 norm is polynomial in L at fixed local parameters. Each term is explicit from the candidate Paulis and coefficients; no unknown source operation is invoked during classical inversion.

If N_L is the number of retained connected sets, calculate each subset response to error at most \(\delta/(2N_L2^L)\) and choose L so that the chosen tail is at most delta/2. Inclusion-exclusion cancellation therefore does not hide a precision cost: the additional number of bits is O(L log(kd)+log(1/delta)). The total cost is exponential in L with constants depending on fixed k,d, and L=O(log(1/delta)). It is polynomial in n, inverse coefficient accuracy, and the stated numerical parameters at fixed k,d and fixed access ratios.

This is a deliberately transparent worst-case construction. It can be much slower than a direct sparse local calculation, but it is an actual finite compiler rather than an appeal to simulating the full 2^n source.

An executable implementation of the combinatorial compiler is supplied in connected_set_demo.py, with recorded results in connected_set_demo.json. It accepts an arbitrary real Pauli dictionary, grows rooted connected sets, caches all distinct subset responses, compresses each subset to its relevant site union, and evaluates the moment equations in a sparse Pauli representation. An independent full-system density-matrix implementation supplies a dense untruncated reference. The single executed example has three qubits, five terms, candidate degree four, J=0.75, r=4, w=1/4, and fixed cutoff L=3. The target ZZI uses 26 root-connected sets and 26 distinct cached subset responses; XII uses 20 root-connected sets and 25 subset responses. Their differences from the dense reference are approximately \(7.33\times10^{-8}\) and \(1.37\times10^{-7}\), respectively. The returned analytic truncation bounds are 0.0548 and 0.00863; these conservative bounds are substantially looser than the observed errors.

The program records subset requests and cache hits, actual sparse exponential-action and matrix-right-hand-side counts, maximum local dimensions, and transparent arithmetic-work proxies. It uses floating-point SciPy exponential routines. This executes the rooted-set compiler structure; it does not implement the theorem's certified finite-arithmetic backend, certify the observed tiny errors, or simulate physical acquisition. No larger matrix or parameter sweep was run.

## 8. Acquisition from one continually evolving source

Insert a discarded-output forgetting interval before each two-window experiment. A sufficient known entropy-forgetting bound is

\[
\|\rho(t)-I/2^n\|_1
\le2\sqrt{n\log2}\,e^{-rt/2},
\]

uniformly over the initial source state. The Hamiltonian preserves relative entropy to I/2^n; independent local depolarization supplies the decay. For calibration statistics, this source-state bound is sufficient even if the source is entangled with another register.

For completeness, write \(D(\rho\|I/2^n)=n\log2-S(\rho)\). Convexity gives
\[
\frac d{dt}D(\rho_t\|I/2^n)
\le r\sum_i[D({\cal R}_i\rho_t\|I/2^n)-D(\rho_t\|I/2^n)]
\le-rD(\rho_t\|I/2^n).
\]
The last inequality is \(\sum_i S(\rho_{\bar i})\ge(n-1)S(\rho)\), obtained by applying strong subadditivity to the chain rule for conditional entropies. The Hamiltonian contributes zero. Starting with D<=n log2 and applying Pinsker gives the slightly stronger coefficient \(\sqrt{2n\log2}\), so the displayed factor two is conservative. Only the source-state inequality is used here; no unsupported conversion of an induced trace norm to diamond norm is made.

Conditional on every previous classical result, the next source input is some density matrix. Since the normalized response effect has norm at most one, choosing

\[
T_{\rm burn}\ge
\frac2r\log\frac{2\sqrt{n\log2}}{\delta_{\rm mix}}
\]

makes its conditional mean differ from the stationary response by at most \(\delta_{\rm mix}\). There is no requirement that the entire experimental record be within O(1/N) total variation of independent samples. Martingale concentration controls the sample means with the allowed small conditional bias.

Stationarity is not simply assumed to follow from a short arbitrary observation. The actual discard duration above is paid, and r remains a calibrated dynamical premise.

## 9. Finite local oscillators, loss and finite counters

### 9.1 General finite-local-oscillator identity

This section records the parent's acquisition lemma so the statistical interface is explicit. Mix each selected output window with a fresh coherent local oscillator of real phase, using a balanced splitter. Define mu as its calibrated mean detected photon number in that window, after any local-oscillator attenuation. Let D_j be the two-counter number difference. With known total source collection/detection efficiency kappa, the statistic \(D_j/\sqrt{\kappa\mu}\) has exactly the ideal unit-efficiency quadrature mean, and products on distinct port/time windows have exactly the required product means. No infinite-local-oscillator limit is taken. If a common detector loss also attenuates the local oscillator, its incident photon budget must be increased accordingly; it is not counted as unattenuated mu.

For a forward product of m=b+1 factors, after the additional q-normalization, a state-independent second-moment bound is

\[
V_b(q,\kappa,\mu)=
\left(\frac{2}{\kappa q}+1+\frac1{4\mu}\right)^{b+1}.
\tag{4}
\]

The odd difference has the same upper bound by
\((A-B)^2/4\le(A^2+B^2)/2\).
At q=mu=kappa=1, \(V_b=3.25^{b+1}\).

The reason finite mean photon counts suffice is that each original Pauli port has scalar intensity \(L^\dagger L=rI/4\). Source photon counts in disjoint windows are Poisson with mean q/4, independently of H and the source state. After efficiency loss and addition of the local oscillator, the sum of the two counter readings is Poisson with mean \(\mu+\kappa q/4\).

### 9.2 Preferred matched local oscillator

Choose the detected local-oscillator mean
\[
\mu=\kappa q/4.
\]
Equivalently, use a continuous local oscillator with detected photon flux \(\kappa r/4\), independent of w. After splitting and displacement, the two detected jump operators for source Pauli A are
\[
J_\pm=\frac{\sqrt{\kappa r}}{2\sqrt2}(A\pm I)
=\pm\sqrt{\kappa r/2}\,\Pi_{A,\pm}.
\]
Their combined effect is \(J_+^\dagger J_++J_-^\dagger J_-=RI\), where \(R=\kappa r/2\). Thus each port produces a state-independent Poisson clock of conditional Pauli projections, with signs recording the outcomes. This is the standard displaced-photodetection unraveling; no novelty is claimed for that identity. It does not actuate the source or change its unconditional generator: measurement is applied downstream to the outgoing field, and the loss channels remain part of the original source dynamics.

Let \(m=Rw=\kappa q/2\), let T_j be the total number of detected events in a selected window, and let D_j be the signed count. The exact source-normalized observation factor is now simply
\[
D_j/m.
\]
Indeed, the signed jump superoperator is \(R{\cal J}_A\), and division by m gives the same insertion \({\cal J}_A/w\) used in the regression proof. Therefore all previous response and inversion formulas apply without change.

Each forward product uses distinct physical ports: at the only repeated source site, Q_i and B_i are different axes. Its totals T_j are independent Poisson variables with mean m, uniformly in the source state and H. Because \(|D_j|\le T_j\), the improved second-moment bound is
\[
\boxed{
V_b^{\rm match}(q,\kappa)
=\left(1+\frac1m\right)^{b+1}
=\left(1+\frac{2}{\kappa q}\right)^{b+1}.
}
\tag{4a}
\]
The reverse product obeys the same bound, and their odd average also does. For q=kappa=1 this gives \(3^{b+1}\), in place of the general mu=1 bound \(3.25^{b+1}\). More significantly, shortening w no longer increases the required oscillator flux.

### 9.3 Finite counters and statistical guarantee

Cap each such total count at an integer K, flag overflow, and assign zero to the odd statistic if any of its at most 2(b+1) selected forward/reverse modes overflows. Overflow in any unrelated port does not discard this coefficient's observation. This retains a bounded statistic

\[
|Y_P^{\rm odd}|\le
B_b=\left(\frac{K}{\sqrt{\kappa\mu q}}\right)^{b+1}.
\]

For the preferred matched setting this is \(B_b=(K/m)^{b+1}\). Use (4a) as its variance bound. If \(\pi_K=\Pr[\operatorname{Pois}(\mu+\kappa q/4)>K]\), which is \(\Pr[\operatorname{Pois}(m)>K]\) in the matched setting, its mean truncation error is at most
\(\sqrt{2V_b(b+1)\pi_K}\). Choose K using this actual Poisson tail to make the error a fixed allotted fraction of delta. K grows logarithmically, or more slowly, in inverse target bias.

Given bounds V=max_b V_b and B=max_b B_b, Freedman's inequality gives a sufficient repetition count of the form

\[
N\ge128\left[
\left(\frac{V}{\delta^2}+\frac{B}{\delta}\right)
\log\frac{2M}{\zeta}
\right],
\tag{5}
\]

is sufficient after allocating at most delta/8 each to forgetting, counter truncation and physical moment bias, and at most delta/2 to statistical fluctuation. All these are errors of the normalized response G. The confidence is at least 1-zeta simultaneously for all coefficients. All photon counts, empty windows and overflow events are part of the acquisition. B contributes only polylogarithmic factors in accuracy for fixed k and fixed q,kappa,mu; the leading precision dependence is eta^-2.

The physical exposure is at most
\[
T_{\rm acq}=N(T_{\rm burn}+2w)
\]
plus actual reset-free hardware overhead and detector dead time. Data processing costs O(kMN), and the subsequent inverse pays the connected-set and LP costs above. The total number of monitored channels is 3n, with 6n counters before any detector fanout needed to handle service limits. At fixed mu the total detected local-oscillator photon budget in counted windows is O(nNmu), and its window flux is O(nmu/w). If the total local-oscillator transmission/detection efficiency is eta_LO, the incident budget is divided by eta_LO. The allocation O(nNmu/kappa) is conservative only when eta_LO>=kappa.

In the preferred matched setting, the exact detected local-oscillator budget for the two counted windows is \(3n\kappa rwN/2\), and the flux over all ports is \(3n\kappa r/4\). Source photons contribute the same detected mean within these windows. The incident local-oscillator budget is \(3n\kappa rwN/(2\eta_{\rm LO})\), bounded by \(3nrwN/2\) if eta_LO>=kappa. If the local oscillator is left continuously on through the forgetting intervals to avoid optical switching, its additional exposure is also paid: total detected local-oscillator photons are \(3n\kappa rT_{\rm acq}/4\), rather than just the counted-window budget. Its incident budget is again divided by eta_LO. These costs are finite and explicit; they are not a single fixed-bandwidth apparatus for arbitrarily large n.

### 9.4 Detector service in the matched setting

The matched total event rate R is independent of w. For a detector dead time d_0, use L equally split labelled rails in each arm and sum their signed counts. A sufficient per-product bias allowance is
\[
(b+1)\frac{R d_0}{L}\left(1+\frac{d_0}{w}\right).
\]
Here the detector must have recovered from pre-protocol blindness, for example by paying a forgetting/guard interval of at least d_0. The bound assumes misses only remove downstream photon events; uncalibrated background or afterpulsing is a different detector model.

To prove the allowance, dominate missed counts in one window by the number C_j of same-rail ordered pairs of total port arrivals separated by at most d_0 in its interval enlarged by a d_0 prefix. Ignoring the detector-arm signs only enlarges this count. Poisson arrivals and independent rail assignment give \(E C_j\le R^2(w+d_0)d_0/L\). For a forward product, different factors use distinct ports, so C_j is independent of all other total-count variables T_l. Telescoping products with \(|D_j|,|\widetilde D_j|\le T_j\) and \(|D_j-\widetilde D_j|\le C_j\) gives
\[
E\left|\prod_jD_j/m-\prod_j\widetilde D_j/m\right|
\le\sum_j E\left[(C_j/m)\prod_{\ell\ne j}(T_\ell/m)\right],
\]
which is the displayed bound. The odd average obeys it as well. First compare the unclipped physical and ideal moments this way; then clip the physical observation separately. Observed totals are bounded by true totals, so the same Poisson overflow and variance bounds apply. This ordering avoids multiplying the service-error allowance by the counter-cap magnitude B_b. The number of rails, routing loss and delay, and any required guard time are actual hardware costs.

For w=1/r with a certified strong-noise inverse, q=1 and
\[
N=\widetilde O_{k,d,\kappa}\left(\frac{r^2}{\eta^2}
\log\frac{M}{\zeta}\right),\qquad
T_{\rm acq}=\widetilde O_{k,d,\kappa}\left(\frac r{\eta^2}
\log\frac{M}{\zeta}\right).
\]
The tildes include the paid forgetting and counter-cap factors. At weak ports, (4) displays the additional \((rw)^{-b-1}\) cost. That dependence is not claimed optimal.

## 10. Passive-output exposure lower bound

An exact solvable subfamily shows that precision and simultaneous-learning exposure cannot generally be improved to a Heisenberg rate in this access model.

Consider one qubit with \(H_\theta=\theta Z\) and the same known isotropic depolarization rate r. Start from I/2 and purify it by a Bell reference. Strengthen the receiver by giving it all outgoing fields, the final source and the initial reference. Its final global state is pure; any allowed passive-output measurement is a processing of this stronger state.

For two parameters separated by Delta, their pure-state overlap a(T) is the trace of a cross-Hamiltonian master equation. The invariant span of I,Z gives

\[
a''+ra'+\Delta^2a=0,\qquad a(0)=1,\quad a'(0)=0.
\]

For \(|\Delta|\le r/2\), put \(s=\sqrt{r^2-4\Delta^2}\) and
\(\gamma=(r-s)/2\). The exact overlap is

\[
a(T)=e^{-rT/2}\left[
\cosh(sT/2)+(r/s)\sinh(sT/2)
\right]\ge e^{-\gamma T}
\ge e^{-2\Delta^2T/r}.
\]

The s=0 expression is understood by continuity. Equal-prior binary discrimination therefore has error

\[
p_e=\frac{1-\sqrt{1-a(T)^2}}2
\ge\frac14e^{-4\Delta^2T/r}.
\]

For n independent qubits with independent equally likely coefficients ±2eta, Delta=4eta. This hard family is admitted by the local budget only when 2eta<=J. Their strengthened output ensemble is a tensor product. Optimal whole-string guessing probability is exactly \((1-p_e)^n\): product Helstrom measurements achieve it, and a tensor product of the one-qubit discrimination dual certificate proves the matching upper bound.

Consequently, for eta<=min(J/2,r/8), a learner whose maximum coefficient error is at most eta with probability at least 2/3 must have

\[
T\ge\frac{r}{64\eta^2}
\log\frac{n}{4\log(3/2)}
\]

whenever the right-hand side is positive. The one-qubit exact Helstrom formula also gives the positive constant lower bound
\(T\ge[r/(64\eta^2)]\log(9/8)\).
Thus the asymptotic simultaneous-learning requirement is
\(\Omega((r/\eta^2)\log n)\).

For success probability 1-zeta, the same argument replaces log(3/2) by -log(1-zeta), giving
\[
T\ge\frac{r}{64\eta^2}
\log\frac{n}{4[-\log(1-\zeta)]}
\]
whenever positive. At small fixed or vanishing failure probability this gives the corresponding log(n/zeta) dependence.

Equivalently, the exact global pure-state Fisher information is

\[
{\cal I}_\theta(T)
=8\left[\frac Tr-\frac{1-e^{-rT}}{r^2}\right]
\le8T/r.
\]

This is a lower bound for fixed passive source dynamics. Allowing interventions on the source, changing its couplings, or error-correcting it during sensing changes the problem and can invalidate the rate comparison. The near-optimality statement concerns precision and n at fixed local/access ratios in the certified regime, not every displayed dependence or classical runtime.

## 11. Existing machinery and what is actually added

- Guţă and Kiukas establish stationary quantum-output identifiability, gauge structure, quantum Fisher information and local asymptotic statistics. Output-only identification is therefore not itself a new idea. Their continuous-time primary source is https://arxiv.org/abs/1601.04355; the discrete-time companion is https://arxiv.org/abs/1402.3535.
- Hägele and Schefczik derive exact higher output moments and cumulants, and their later collaborators use quantum polyspectra for parameter extraction. Output regression and fitting higher optical correlations are established machinery: https://arxiv.org/abs/1611.02077 and https://doi.org/10.1103/PhysRevResearch.3.033123. The associated implementation is https://github.com/MarkusSifft/QuantumCatch.
- Rigorous Time-dependent Hamiltonian Learning via Continuous Weak Measurements uses known separable source probe preparations and local inverse problems: https://arxiv.org/abs/2607.16047. It is a strong nearby alternative when those preparations are available.
- Near-Optimal Learning of Local Lindbladians constructs efficient finite-time response estimators and coefficient inversions, requiring random product-state inputs and Pauli measurements of source outputs: https://arxiv.org/html/2606.20535v3. It also treats a larger unknown-noise model and does not require the same known bounded-degree candidate graph. Its statistical and access strengths must be acknowledged.
- Efficient Lindbladian Learning from Constant-Time Pauli Responses is another directly relevant inverse-response construction: https://arxiv.org/abs/2607.25795. A finite response or an eta^-2 rate alone cannot count as this work's added operation.

The completed connection here is a quantitatively invertible, finite-duration classical-output response under the declared Pauli-port model, with no source preparation/control/readout; an explicit local classical forward compiler; finite loss and local-oscillator costs; one-record parallel acquisition; and an access-matched exposure lower bound. The exact time-reversed odd response is useful because it cancels every even Hamiltonian order before inversion.

This is a constructed theorem and protocol, not an assertion of exhaustive historical priority. Existing output-fitting software may be far better numerically on particular devices. Any practical advantage requires actual rates, efficiencies, graph degree, calibration tolerances, counter bandwidth and the forward-computation cost to be evaluated. The source Hamiltonian and noise promises remain substantive.

