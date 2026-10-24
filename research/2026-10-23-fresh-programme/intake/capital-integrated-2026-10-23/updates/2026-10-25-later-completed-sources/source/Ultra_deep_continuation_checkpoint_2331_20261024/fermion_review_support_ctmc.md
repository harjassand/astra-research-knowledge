# Independent audit: canonical contraction and block observables

24 October 2026. Bounded proof/complexity check of `fermion/CANONICAL_CONTRACTION.md` §§3,6 and `fermion/BLOCK_CANONICAL_OBSERVABLES.md` §§3–5. Constructor files were not edited. No novelty or physical-performance claim.

## Result

**PASS at the stated fixed-parameter scope.** I found no gap in the connected-support/Möbius evaluator, tilt stopping, fixed-density Fourier identity, or arbitrary-accuracy exact fallback. The auxiliary-variable stability-closure step is already explicit in the canonical proof and has been checked against the cited proposition; no constructor repair is outstanding.

### Connected support, KP, and finite computation

The dimer activity representation is a hard-core polymer gas on the contracted graph, with compatibility exactly vertex-disjointness. Insert a marker $u^{|C|}$ and define
\[
\ell(S;u)=\sum_{T\subseteq S}(-1)^{|S|-|T|}\log\Xi_T(u).
\]
Summing over connected $S$ isolates exactly those log-clusters whose union of supports is $S$. A cluster's incompatibility graph is connected, so its union support is connected; its $u$-degree is at least the size of that union. Truncating modulo $u^L$ therefore retains exactly clusters of total polymer size below $L$. The formal logarithm automatically includes repeated polymers and their factorial/multiplicity coefficients. The subset recurrence for $\Xi_T$ is the standard disjoint-polymer recursion and costs only $\exp(O(L))$ per explored support. At fixed degree, connected supports of size below $L$ number $m\exp(O_D(L))$; total work is polynomial in $m$ and $1/\eta$ for $L=O(\log(m/\eta))$.

For the canonical inner sector, apply the same argument at each evaluated $z$ to rational-function activities $A_C(z)/b(z)^{|C|}$. The fixed angular sector and Cauchy-disc margin keep $b(z)=1+2z$ bounded away from zero. The count $(4D)^{s-1}$ and activity bound $|w_C(z)|\le(2a)^s$ give the per-vertex size-tilted sum
\[
\sum_{s\ge2}(4D)^{s-1}(2a)^s3^{5s}=\frac{x^2}{4D(1-x)}=S,
\qquad x=8D3^5a.
\]
A polymer $C$ of size $q$ is incompatible only by meeting one of its $q$ vertices, so $qS\le q$ verifies the KP inequality for $a_{KP}(C)=q$. The dummy-root KP bound gives a volume factor $m$; the extra size tilt $4|C|$ bounds the discarded tail by at most $m e^{-4L}$ (the looser stated bound is valid since $S\le1$). Cauchy on the larger log-sector disc gives the derivative-tail bounds. This is an application of the established Kotecký–Preiss/Mann–Minko framework, not a new cluster theorem.

### Tilt, Fourier, fallback, and bit costs

For fixed density margin $\delta$, the reference mean $m\,2r/(1+2r)$ at the two rational endpoints differs from any target $\delta m\le k\le(1-\delta)m$ by at least $\delta m/2$. The correction $|Q'|\le mS/s_0$ is at most $\delta m/512$, so the full mean brackets $k$. Real-rootedness writes $Z(r)=\prod_{j=1}^{m}(1+\lambda_jr)$ with $\lambda_j>0$, hence
\[
\mu'(r)=\operatorname{Var}(K)/r\le m/(4r_{lo}).
\]
With a maintained certified bracket, width $r_{lo}/(16m)$ puts the midpoint mean within $1/64$ of $k$; alternatively $|\widehat\mu-k|\le1/8$ plus the $1/32$ estimator error puts the true error below $5/32<1/4$. If a sign is uncertified at a midpoint, that same accurate estimate is already within $1/8$, so the stopping rule terminates. Since $r_{hi}/r_{lo}=O_\delta(1)$, this takes $O_\delta(\log m)$ evaluations. A differentiated cluster tail is $O(m e^{-4L}/s_0)$, so $L=O(\log m)$ suffices for the fixed $1/32$ accuracy.

The $(m+1)$-point roots-of-unity formula is exact for degree $m$. Inner values have a relative KP evaluator, and nonnegative coefficients give $|Z(re^{i\theta})|\le Z(r)$. The Poisson-binomial point-mass lower bound $a_m=3/[4(m+1)^2]$ makes division by the target probability safe. The outer bound $e^{-\delta m/8}$ may be replaced by the rational upper bound $2^{-\lfloor\delta m/8\rfloor}$. If this is too large relative to $\epsilon a_m$, the exact branch enumerates at most $9^m$ empty/up/down configurations. The failed-branch inequality implies
\[
m=O_\delta(\log(1/\epsilon)+1),
\]
because $\log(m+1)$ is absorbed into the linear $\delta m$ term outside a $\delta$-dependent constant range. Therefore $9^m=(1/\epsilon)^{O_\delta(1)}$, the required fallback for arbitrarily small $\epsilon$; no fixed outer-arc error is silently discarded.

All interval tests, $r_{lo},r_{hi}$, $x,S$, and $2^{-\lfloor\delta m/8\rfloor}$ are rational when the declared parameters are rational. For rational-complex input entries, a size-$O(L)$ activity has numerator/denominator bit length polynomial in $L$ and total input bit length; subset-DP products, formal-log divisions through order $L$, and sums retain polynomial bit length. Root-of-unity nodes can be enclosed by certified dyadic complex balls to $O(\epsilon a_m/m)$ absolute $z$-accuracy. The derivative bound $\sum_k k c_k r^k\le mZ(r)$ controls the Fourier error; if the dyadic point is slightly off-radius, nonnegative coefficients give the same bound up to a constant factor for the $O(\epsilon a_m/m)$ radial perturbation. Exact determinant enumeration also has polynomial bit length per determinant and only $O(m)$ extra summation bits. No exact-transcendental or real-root oracle is needed.

The same mechanism carries to §§4–5 of the block note: $Z_0=\prod_B B_B$ is a positive rational coefficient polynomial; its variance-margin test gives endpoint mean bracketing; roots of each $B_B$ give the Poisson-binomial arc estimate; and the forest estimate is absolute and remains valid at a block reference zero. The claimed $9^m$ fallback is polynomial in $1/\epsilon$ at fixed maximum block size and fixed $\nu$, because a failed outer-tail test forces the number of coarse blocks to $O_{b,\nu}(\log(1/\epsilon)+1)$. If these margins are not fixed, their dependence must remain in the complexity statement, as the file says.

### Stability check and primary support

For Eq. (7)'s root-location step, $p(y)=\det(\operatorname{diag}(y)-H)$ is real stable for Hermitian $H$. Borcea–Brändén Proposition 2.2 supplies coordinate differentiation and specialization. The canonical proof already handles the positive direction $\partial_{U_i}+\partial_{V_i}$ by introducing $t$ through $y_{U_i},y_{V_i}\mapsto y_{U_i}+t,y_{V_i}+t$, differentiating in $t$, and specializing at zero. That is the needed stability-preserving closure, and the explicitly positive leading coefficient rules out the zero polynomial. I checked this existing argument; it is not a proposed repair. The complementary principal-set indexing and factor check in (7) are correct: for disjoint $|I|=|J|=k$, exactly $2^{n-2k}$ subsets $A$ contain $I$ and avoid $J$, while the $2F$ chiral minor contributes $4^k|\det F[I,J]|^2$; $2^{-n}2^{n-2k}4^k=1$.

Primary references: Kotecký–Preiss, [“Cluster expansion for abstract polymer models”](https://doi.org/10.1007/BF01211762) (1986); Mann–Minko, [“Algorithmic Cluster Expansions for Quantum Problems”](https://doi.org/10.1103/PRXQuantum.5.010305) (2024), especially Theorem 2 and Lemmas 4–8; Borcea–Brändén, [“Applications of stable polynomials to mixed determinants”](https://arxiv.org/abs/math/0607755), Propositions 2.2 and 2.4.
