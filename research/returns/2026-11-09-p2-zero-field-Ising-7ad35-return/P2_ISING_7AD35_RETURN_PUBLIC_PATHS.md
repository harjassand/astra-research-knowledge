# P2 zero-field Ising RNC return

Chat: https://chatgpt.com/c/6af094d8-9cc0-83ec-b2c2-4c4beb0539f2
Prompt source: P2_FULL_ZERO_FIELD_ISING_RNC_FINAL_20261109.txt
Prompt turn: 7ad35df3-4f9a-4634-ae1d-cf6a87e1c9f3
Response: 1f69c7e5-0a91-4f23-98e3-b84aa4b8c12d
Displayed model: 5.6 Pro. Collected 9 November 2026 Brisbane.
Source: No producer-supplied ZIP visible.

## Complete visible response

# Verdict

The full statement is unresolved as of 9 November 2026.

There is currently:

- no proved uniform finite-bit RNC sampler covering zero field, arbitrary finite graphs, arbitrary rational heterogeneous $\beta_e\ge 1$, and the requested worst-case work/depth bounds; and
- no lower bound or independently motivated reduction establishing that such a sampler cannot exist.

Chen–Liu–Yin–Zhang explicitly describe general ferromagnetic Ising parallel tractability as unresolved, and their positive theorem requires both a fixed interaction gap and a fixed nonzero-field gap. The newest zero-field results are sequential: Miao covers the uniform-activity tree-uniqueness range with expected arithmetic work, while Feng–Guo–Zhang cover every fixed uniform temperature with a polynomial-time sequential sampler. DROPS (https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.46/LIPIcs.APPROX-RANDOM.2025.46.html)

What can be resolved completely is the exact missing primitive. The requested problem is finite-bit RNC-equivalent to sampling a product Bernoulli vector conditioned on graphic parity constraints.

## 1. Exact RNC-equivalence theorem

For each edge set
$p_e=\frac{\beta_e-1}{\beta_e},\qquad
t_e=\frac{\beta_e-1}{\beta_e+1},\qquad
q_e=\frac{\beta_e-1}{2\beta_e}.$
These satisfy
$p_e=\frac{2t_e}{1+t_e},
\qquad
q_e=\frac{t_e}{1+t_e},
\qquad
\frac{q_e}{1-q_e}=t_e .$
Let $D\in\mathbb F_2^{V\times E}$ be the vertex-edge incidence matrix. For an edge indicator $x\in\{0,1\}^{E}$, the condition $Dx=0$ means every vertex has even selected degree.

The following four sampling problems are equivalent under uniform bounded-fan-in, polynomial-work, polylog-depth randomized reductions that preserve full-joint total variation:

- 
Zero-field Ising
$\mu(\sigma)\propto
\prod_{e=uv}\beta_e^{[\sigma_u=\sigma_v]}.$
- 
$q=2$ random cluster
$\phi(A)\propto
2^{k(A)}
\prod_{e\in A}p_e
\prod_{e\notin A}(1-p_e),$
where $k(A)$ counts all connected components, including isolated vertices.

- 
Weighted even subgraphs
$\pi_{\rm even}(F)\propto
\mathbf 1_{\{DF=0\}}
\prod_{e\in F}t_e .$
- 
Graphic parity-conditioned Bernoulli sampling
$X_e\stackrel{\mathrm{ind}}{\sim}\operatorname{Bernoulli}(q_e),
\qquad
X\ \text{conditioned on}\ DX=0.$

The fourth law is exactly the third law because, conditional on $Dx=0$,
$\Pr[X=x\mid Dx=0]
\propto
\prod_e
\left(\frac{q_e}{1-q_e}\right)^{x_e}
=
\prod_{e:x_e=1}t_e.$
Thus the requested result exists if and only if the following problem has the same finite-bit RNC guarantee:

Given a graph and rational $0\le q_e<1/2$, sample independent Bernoulli edge bits conditioned on all vertex parities being even.

This is the exact frontier. Ordinary Gaussian elimination samples the special case $q_e=1/2$, where the law is uniform on the cycle space. It does not sample the unequal-bias law.

## 2. Even-subgraph $\longrightarrow$ Ising: the complete wrapper

Assume a finite-bit RNC routine
$\textsc{EvenCore}(G,(t_e),\eta)$
that outputs an $\eta$-approximate sample from $\pi_{\rm even}$. Then the requested Ising sampler is:

### Algorithm

- 
Compute every $t_e=(\beta_e-1)/(\beta_e+1)$.

- 
Obtain
$F\leftarrow\textsc{EvenCore}(G,(t_e),\epsilon/2).$
- 
Independently for every $e\notin F$, include $e$ in $A$ with probability $t_e$. Every edge of $F$ is included in $A.

- 
Compute the connected components of $(V,A)$.

- 
Assign each component an independent fair sign and give every vertex in that component the same sign.

- 
Output the resulting $\sigma$.

This is the completion-and-coloring operation used by Miao; importantly, it starts with an even-subgraph sample rather than producing one. Miao proves that the completion followed by fair component coloring gives the Ising law and contracts total variation. arXiv (https://arxiv.org/abs/2611.04786)

### Direct proof

Consider the joint weight
$\Psi(F,A)\propto
\mathbf 1_{\{DF=0,\ F\subseteq A\}}
\prod_{e\in A}t_e
\prod_{e\notin A}(1-t_e).$
For fixed $F$, every missing edge is independently added with probability $t_e$, exactly as in Step 3.

For fixed $A$, every even $F\subseteq A$ has the same weight. Therefore $F\mid A$ is uniform on the cycle space of $(V,A)$.

That cycle space has dimension
$|A|-n+k(A).$
Consequently the $A$-marginal is proportional to
$2^{|A|-n+k(A)}
\prod_{e\in A}t_e
\prod_{e\notin A}(1-t_e).$
Using $p_e=2t_e/(1+t_e)$, this is proportional to
$2^{k(A)}
\prod_{e\in A}p_e
\prod_{e\notin A}(1-p_e),$
which is exactly the $q=2$ random-cluster law. Fair component coloring is then the Edwards–Sokal map to Ising. Chen et al. likewise separate the random-cluster sampler from the component-coloring postprocessing. DROPS (https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.46/LIPIcs.APPROX-RANDOM.2025.46.html)

## 3. Ising $\longrightarrow$ even subgraphs

The reverse reduction establishes genuine equivalence, not merely sufficiency.

Given an approximate Ising sample $\sigma$:

- 
For every monochromatic edge, open it independently with probability
$p_e=1-\frac1{\beta_e}.$
Close every bichromatic edge.

- 
This produces the corresponding approximate $q=2$ random-cluster sample $A$.

- 
Sample a uniformly random member $F$ of the cycle space of $(V,A)$.

The joint calculation above shows that the resulting $F$ has the weighted even-subgraph law.

A uniform cycle-space sample is an NC operation: compute an $\mathbb F_2$ nullspace basis for the incidence matrix of $(V,A)$, draw one fair coefficient per basis vector, and XOR the chosen vectors. Standard parallel finite-field linear algebra gives polynomial Boolean work and polylogarithmic depth.

Therefore any requested Ising sampler would itself solve the graphic parity-conditioned Bernoulli problem.

## 4. Full finite-bit accounting for the wrapper

The transformations around EvenCore satisfy the strong model in the question.

Write a rational coin probability as $r=a/b\in[0,1]$. Choose
$L=\left\lceil \log_2\frac{8\max\{1,m\}}{\epsilon}\right\rceil .$
Draw an $L$-bit integer $U$ uniformly from
$\{0,\ldots,2^L-1\}$, and return one exactly when
$bU<a2^L.$
This uses exactly $L$ random bits and no rejection. Its success probability differs from $a/b$ by less than $2^{-L}$. Coupling all at most $m$ completion coins gives total error at most
$m2^{-L}\le \epsilon/8.$
All arithmetic involves $O(B+L)$-bit integers. Multiplication, comparison, addition, rational transformation, sorting of labeled edges and scheduling have bounded-fan-in polynomial-size, polylog-depth Boolean circuits.

Connected components can be obtained, for example, by repeated Boolean matrix squaring in $O(\log^2 n)$ bounded-fan-in depth and polynomial work. Fair component colors require at most $n$ additional random bits.

Hence, apart from the missing core:

- total wrapper work and random bits are polynomial in $n+B+\epsilon^{-1}$;
- depth is polynomial in$1+\log(n+B+2)+\log(\epsilon^{-1});$
- every execution has a fixed finite gate count;
- no real arithmetic, rejection loop, oracle or postselection occurs;
- the TV guarantee applies to the entire joint spin vector.

Edges with $\beta_e=1$ have $p_e=t_e=q_e=0$ and can be deleted. If $m=0$, the algorithm outputs $n$ independent fair signs. Disconnected graphs and isolated vertices are already handled by component coloring. The empty graph produces the empty spin vector.

Thus a valid EvenCore would immediately yield the exact type of constants $C,c$ requested, enlarged only by universal circuit overhead.

## 5. Why the cited positive results do not supply EvenCore

### Chen–Liu–Yin–Zhang

Their ferromagnetic theorem assumes a fixed constant $\delta>0$,
$\beta_e\ge1+\delta,
\qquad
\lambda_v\le1-\delta .$
Their random-cluster theorem correspondingly assumes $p_e\ge\delta$ and the same nonzero-field gap. At $\lambda_v=1$, their low-temperature condition contains the bound
$(1-p_{\min})\log n
\le
\frac{1-\lambda_{\max}}{27}=0,$
so the stated proof does not extend by direct substitution. DROPS (https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.46/LIPIcs.APPROX-RANDOM.2025.46.html)

Their explicit field-dynamics parameters also contain
$\theta\propto
\exp\!\left[-140(1-\lambda_{\max})^{-2}\right]$
and a number of field-dynamics rounds proportional to
$\left(\frac e\theta\right)^{5(1-\lambda_{\max})^{-2}}.$
Therefore the complexity is not uniform as the field gap vanishes. DROPS (https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.46/LIPIcs.APPROX-RANDOM.2025.46.html)

Their contracting-interaction theorem covers some zero-field instances, but requires the interaction spectrum to fit inside a fixed-width interval below one. Adding a diagonal shifts all eigenvalues without reducing their spread, so arbitrary strong or dense ferromagnetic instances are not brought into this regime. DROPS (https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.46/LIPIcs.APPROX-RANDOM.2025.46.html)

Their formal computation model is a CRCW PRAM measured in rounds and processors, not the bounded-fan-in Boolean, fully charged finite-bit model requested here. DROPS (https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.46/LIPIcs.APPROX-RANDOM.2025.46.html)

### Miao

Miao proves, for uniform $\beta$ and maximum degree $\Delta$,
$1<\beta\le\frac{\Delta}{\Delta-2},$
an expected-work bound
$O\!\left(n+m\log^3(n/\epsilon)\right).$
The cycle proposal has expected exploration length, and the polymer insertion-deletion process executes a polynomial number of sequential state-dependent updates. The computation model explicitly counts arithmetic operations and generation of uniform and geometric random variables. arXiv (https://arxiv.org/abs/2611.04786)

Capping such a routine can turn expected work into worst-case polynomial sequential work while charging the timeout probability to TV. It does not convert the sequential chain into polylogarithmic parallel depth, and the nonbacktracking certificate is proved only in the stated temperature range. The spin-recovery lemma is postprocessing after an even-subgraph sample. arXiv (https://arxiv.org/abs/2611.04786)

### Feng–Guo–Zhang

The revised result cited by Miao gives an all-temperature zero-field sampler for every fixed uniform $\beta>1$, but it remains a sequential random-cluster Glauber algorithm with constants depending on $\beta$. It is neither an RNC construction nor uniform for binary-input heterogeneous $(\beta_e)$. arXiv (https://arxiv.org/abs/2611.04786)

## 6. Adding and symmetrising a field provably fails

Let
$M(\sigma)=\sum_{v}\sigma_v,
\qquad
\mu_h(\sigma)\propto\mu_0(\sigma)e^{hM(\sigma)}.$
If one samples from $\mu_h$ and independently flips all spins with probability $1/2$, the resulting law is
$\nu_h(\sigma)
=
\mu_0(\sigma)
\frac{\cosh(hM(\sigma))}
{\mathbb E_{\mu_0}[\cosh(hM)]}.$
It is not $\mu_0$.

This obstruction is quantitatively severe even on an edgeless graph. There $\mu_0$ is uniform. Put
$a=\tanh h.$
The symmetrised field law is a half-half mixture of product measures with magnetization means $na$ and $-na$. For
$\mathcal A=\{|M|\ge na/2\},$
Chebyshev’s inequality gives
$\nu_h(\mathcal A)\ge1-\frac4{na^2},
\qquad
\mu_0(\mathcal A)\le\frac4{na^2}.$
Therefore
$d_{\rm TV}(\nu_h,\mu_0)
\ge
1-\frac8{na^2}.$
To make this at most $1/2$, one necessarily needs
$n\tanh^2 h\le16,
\qquad
h=O(n^{-1/2}).$
The corresponding field activity gap is
$1-\lambda=1-e^{-2h}=O(n^{-1/2}).$
Substituting this scale into Chen et al.’s explicit $\theta$ and field-dynamics horizon gives
$\log T^{\rm FD}=\Omega(n^2),$
rather than polynomial work and polylogarithmic depth. DROPS (https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.46/LIPIcs.APPROX-RANDOM.2025.46.html)

So field symmetrisation does not bridge the zero-field endpoint.

## 7. Pinning a spin also does not simplify the core

For a connected component choose a root $r$. It is true that one may:

- sample the zero-field law conditioned on $\sigma_r=+1$;
- multiply the entire component by one fair global sign.

That recovers the unconditioned law.

But under Edwards–Sokal, for any random-cluster configuration $A$:

- the unconditioned number of compatible component colorings is $2^{k(A)}$;
- fixing the root component to $+$ leaves $2^{k(A)-1}$ colorings.

The factor $1/2$ is independent of $A$. Therefore the random-cluster edge law after pinning the root is exactly the same zero-field random-cluster law. Pinning breaks the final global color symmetry but does not sample the clusters.

## 8. Why a negative answer is not currently justified

A lower bound against this sampler would be a substantial parallel-complexity result. Barriers for Glauber, Swendsen–Wang, field dynamics or the cycle chain rule out those trajectories only; they do not rule out a different global algorithm.

The perfect-matching analogy also does not currently provide the required reduction. Chen et al. describe a methodological connection through the sequential canonical-path history, while simultaneously stating both parallel questions as unresolved. That is not a reduction from perfect-matching sampling to zero-field ferromagnetic Ising sampling. DROPS (https://drops.dagstuhl.de/storage/00lipics/lipics-vol353-approx-random2025/html/LIPIcs.APPROX-RANDOM.2025.46/LIPIcs.APPROX-RANDOM.2025.46.html)

Likewise, assuming merely $\mathrm{RNC}\ne\mathrm P$ says nothing about this particular sampling problem unless one first proves an appropriate NC hardness reduction. No such full-model reduction is presently available.

# Final determination

$\boxed{\text{The requested uniform zero-field Ising RNC sampler is currently an open problem.}}$
The exact unresolved primitive is
$\boxed{
X_e\ \text{independent Bernoulli}\!\left(
\frac{\beta_e-1}{2\beta_e}
\right)
\ \text{conditioned on}\ DX=0\pmod 2.
}$
Everything before and after that primitive—including random-cluster completion, cycle-space sampling, connected components, finite-precision rational coins, fair component coloring, disconnected graphs, isolated vertices and unconditional TV accounting—has a fully charged finite-bit NC implementation. A claimed complete sampler based only on the cited theorems would therefore be missing precisely this parity-conditioned weighted cycle-space sampler.

## Visible activity — Worked for 52m 49s

Assessed the problem
Reviewed the literature
Examined dependencies and tested augmentation ideas
I’ll verify the cited results’ exact scope, then test random-cluster, high-temperature, and cut-based constructions against every finite-bit RNC requirement.
Searched 7 websites
Explored spin recovery and structural algorithms
Evaluated parallelization
Tested auxiliary representations and compared latent formulations
Checked complexity connections
Compared and clarified related reductions
Traced reduction limits
Assessed the bottleneck
Mapped structural barriers, checked current status, and sought counting route
Tested hardness routes
Explored recursive and parallel sampling approaches
Assessed parallel sampling
Assessed parallel sampling
Assessed parallel sampling
Searched 83 websites
Assessed parallel sampling
Assessed and evaluated parallel sampling
Assessing parallel sampling
Assessed parallel sampling
Assessed parallel sampling
Assessed parallel sampling
Assessed parallel sampling possibilities
Evaluated parallel sampling viability
Assessed parallel sampling
Assessed parallel sampling
Assessed parallel sampling and algorithmic status
Assessed the open problem
Searched 82 websites
Assessed the algorithmic status
Assessed parallel sampling
Assessed the algorithmic status
Assessed the algorithmic status
Searched 19 websites
The external-field symmetrization shortcut fails because its localization cost blows up as the field gap vanishes. The core reduces to biased independent edge bits conditioned on even vertex parities.
The finite-bit reductions are bidirectional and NC-clean. I found neither an all-temperature polylog-depth sampler for the parity-conditioned core nor a qualifying full-model lower bound.
