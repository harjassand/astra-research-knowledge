# Independent reconstruction of the kinetic obstruction

Audit date: 2026-10-16. Source: `/Users/harjas/Downloads/astra_kinetic_investigation`, treated as data with original bytes preserved. Repository context: `3dde9ce74d829a93388e64032d27351b36dd2221`. These are analytic reconstructions and bounded algebra checks, not external peer review, formal verification, or historical priority clearance.

## 1. Second moments and termination are different properties

Let C be a finite transient-state set, A failure and B success. Original off-diagonal rates are q_ij, with total q_i including both absorbing exits. Proposal rates are r_ij, total r_i. Successful original paths must be absolutely continuous with respect to proposal paths. The proposal may suppress A because those paths contribute zero to the success estimator. On success put W equal to the original/proposal path-density ratio and otherwise put W=0.

For a path with holding times t_l, squaring its original density and dividing by its proposal density contributes products of q_ij²/r_ij and exponential factors exp[(r_i-2q_i)t_l]. Thus the transient second-moment operator is

\[
M_{ij}=q_{ij}^2/r_{ij}\ (i\ne j),\quad M_{ii}=r_i-2q_i,
\quad b_i=q_{iB}^2/r_{iB}.
\]

When several success channels have distinct destinations/labels, b is their corresponding sum; the packet uses one aggregated B channel. Tonelli's theorem applies to the nonnegative path expansion and gives

\[
m_i(T)=\mathbb E_{r,i}[W^2\mathbf1_{\{\tau_B\le T\}}]
=\left[\int_0^T e^{Mt}b\,dt\right]_i.
\]

For irreducible Metzler M and b>0, choose its strictly positive right Perron vector v, Mv=αv. If c_- = min_i b_i/v_i and c_+ = max_i b_i/v_i, positivity of the semigroup gives

\[
c_-v\Phi(\alpha,T)\le m(T)\le c_+v\Phi(\alpha,T),
\quad \Phi(\alpha,T)=\begin{cases}(e^{\alpha T}-1)/\alpha&\alpha\ne0,\\T&\alpha=0.\end{cases}
\]

Therefore the eventual-hitting second moment is finite exactly when α<0, and then equals -M^{-1}b. At α=0 it diverges linearly with the observation horizon; at α>0 it diverges exponentially. Every coordinate diverges. Strict positivity of every b_i can be weakened to b≥0, b≠0 with irreducibility, by first replacing b with e^{Mε}b>0.

For embedded chains the same path expansion yields K_ij=P_ij²/R_ij and b_i=P_iB²/R_iB. The second moment is ∑_{n≥0} K^n b. Perron-vector comparisons show finiteness iff ρ(K)<1 under the same irreducibility/source conditions, including periodic chains.

These facts are classical second-moment/change-of-measure machinery. See [Kuruganti and Strickland (1996), §3.2, equations (6)–(7)](https://www.informs-sim.org/wsc96papers/036.pdf).

## 2. Exact two-state thresholds

There are two internal states with q_12=q_21=1, success exit κp, failure exit κ(1-p), where κ>0 and 0<p<1. Absorption is an independent Exp(κ) clock, followed by an independent success mark of probability p. Hence h_1=h_2=p. Let a=(1+δ,1-δ), 0<δ<1, and choose p≤1/(1+δ). Approximate Doob rates are r_12=a_2/a_1, r_21=a_1/a_2, r_iB=κ/a_i, with failure exits removed. Their B hazards are uniformly at least κ/(1+δ); proposal absorption is almost sure with finite expected duration and jump count.

Rebuilding M directly gives

\[
\det M=\frac{(\kappa+2)[\kappa-4(1+\kappa)\delta^2]}{1-\delta^2},\quad
\operatorname{tr}M=\frac{-2-2\kappa+(6+4\kappa)\delta^2}{1-\delta^2}.
\]

Both off-diagonals are positive, so the two eigenvalues are real. The trace is increasing in δ² and is negative at δ²=κ/[4(1+κ)]. Below this boundary the determinant is positive and trace negative; above it the determinant is negative. Consequently

\[
\mathbb E_r W^2<\infty\ \Longleftrightarrow\
\delta^2<\frac{\kappa}{4(1+\kappa)}.
\]

Equality gives a zero Perron eigenvalue and infinite eventual second moment. The proposition is valid despite positive success and failure exits at every original transient state and certain finite-mean proposal termination.

For eventual hitting one can integrate out holding times. Normalizing the approximate routing yields R_12=a_2/(a_2+κ), R_21=a_1/(a_1+κ). The embedded second-moment matrix has zero diagonal and

\[
\rho(K)^2=\frac{(1+\kappa)^2-\delta^2}{(1+\kappa)^4(1-\delta^2)},
\]

\[
1-\rho(K)^2=\frac{\kappa(\kappa+2)\{(1+\kappa)^2-[(1+\kappa)^2+1]\delta^2\}}
{(1+\kappa)^4(1-\delta^2)}.
\]

It follows that embedded variance is finite exactly for

\[
\delta^2<\frac{(1+\kappa)^2}{(1+\kappa)^2+1}.
\]

The boundary tends to 1/2 as κ↓0. Solving the 2×2 renewal equations gives the packet's normalized moment limit (1-δ²)/(1-2δ²), for δ²<1/2. This is a routing-specific repair and is not a general guarantee.

## 3. Three-state branching threshold

Take q_ij=1 for each distinct internal pair among three states and the same absorbing exits as above. Set a=(1+δ,1,1-δ). Original total rate is 2+κ. For embedded routing,

\[
K_{ij}=\frac{\sum_{\ell\ne i}a_\ell+\kappa}{(2+\kappa)^2a_j}\quad(i\ne j),\qquad K_{ii}=0.
\]

The exact factorization is

\[
\det(I-K)=\frac{(\kappa+3)^2[\kappa(\kappa+2)^2-(\kappa^3+4\kappa^2+7\kappa+4)\delta^2]}
{(\kappa+2)^5(1-\delta^2)}.
\]

The characteristic polynomial of a positive-off-diagonal, zero-diagonal 3×3 matrix is x³-Ax-B, with A,B>0. It has exactly one positive root by Descartes' rule, namely the Perron root. Its value at x=0 is negative, so the sign at x=1 determines which side of 1 that root lies on. Therefore

\[
\mathbb E_R W^2<\infty\ \Longleftrightarrow\
\delta^2<\frac{\kappa(\kappa+2)^2}{\kappa^3+4\kappa^2+7\kappa+4}.
\]

The boundary is asymptotic to κ. Equality diverges. The packet's rational positive vector with Kv>v is also a sufficient exact certificate at κ=10^{-6}, δ=10^{-2}; the floating Perron root is unnecessary for the sign decision. The copied source script verifies both determinant identities and that certificate.

## 4. General irreducible routing theorem and exact exceptions

Fix a finite irreducible row-stochastic matrix S with zero diagonal. Regard S_ij as internal CT rates, giving internal total rate 1 at every state. Add success and failure rates κp and κ(1-p) at every state. For a>0, let hhat_i=pa_i, with p chosen so these approximations are at most one and p<1. Define

\[
R^\kappa_{ij}=\frac{S_{ij}a_j}{(Sa)_i+\kappa},\quad
R^\kappa_{iB}=\frac{\kappa}{(Sa)_i+\kappa},\quad
K^\kappa_{ij}=\frac{S_{ij}[(Sa)_i+\kappa]}{(1+\kappa)^2a_j}.
\]

If some row has two positive entries S_ij,S_iℓ with a_j≠a_ℓ, then ρ(K^0)>1. Indeed,

\[
(K^0\mathbf1)_i=(Sa)_i\sum_j S_{ij}/a_j\ge1,
\]

with equality exactly when a is constant on the support of that row. The hypothesis gives strict inequality in at least one row. Multiplication by the strictly positive left Perron vector proves ρ(K^0)>1. Spectral continuity gives ρ(K^κ)>1 for all sufficiently small κ>0. The success source is κp²[(Sa)_i+κ]/(1+κ)²>0, so eventual second moment diverges from every starting state. Each proposal step has success probability at least κ/(max a+κ)>0, and hence finite expected jump count. This is a moment failure, not a termination failure.

The quantifiers matter:

- The branching-and-distinct-destination-values condition is sufficient. Branching alone and nonconstant a alone are insufficient.
- If each row's destination support has constant a, K^0=S. A nonconstant a may have this property on a periodic graph.
- Example: four states with rows 1,2 routing equally to 3,4, and rows 3,4 routing equally to 1,2. For a=(1+δ,1+δ,1-δ,1-δ), the chain is irreducible and branching with period two, but K^0=S. Its κ>0 Perron-square threshold is exactly the repaired two-state threshold.
- Directed deterministic cycles also fail the strict-row hypothesis. For a cycle of length m, ρ(K^κ)^m=∏_i(1+κ/a_i)/(1+κ)^{2m}. These can be stable at small error; absence of branching does not guarantee stability for arbitrary large error.
- Periodicity does not invalidate the theorem when a genuinely changes routing within a row. For the same four-state graph with f=(1,-1,0,0), the local coefficient below is 1/2>0.
- Positive absorption at every state is already present in the countermodels. A uniform escape lower bound independent of the error regime is an additional restriction and removes the κ↓0 argument.
- Reducible routing requires component/reachability analysis; irreducibility cannot simply be dropped while retaining an every-start conclusion.

## 5. Local coefficient and critical escape scale

Fix S and f, and put a=1+δf for |δ| small enough to preserve positivity. Relative committor error on transient states is |δ|‖f‖∞; δ is the error itself only when ‖f‖∞=1. Let π be the stationary law of S. Then

\[
\sigma_S^2(f)=\sum_i\pi_i[(Sf^2)_i-(Sf)_i^2]\ge0.
\]

At κ=0 the row expansion is

\[
K^{0,\delta}\mathbf1
=\mathbf1+\delta^2\{Sf^2-(Sf)^2\}+O(\delta^3).
\]

The first matrix derivative annihilates 1. Since the eigenvalue 1 of an irreducible stochastic S is simple, its first normalized eigenvector correction is zero. The second eigenvalue coefficient is π times the displayed row coefficient. This remains valid for periodic S: its other unit-modulus eigenvalues are distinct from 1. At δ=0, K^{κ,0}=S/(1+κ), so the κ derivative is -1. Hence

\[
\rho(K^{\kappa,\delta})=1-\kappa+\sigma_S^2(f)\delta^2
+O(\kappa^2+\kappa|\delta|+|\delta|^3).
\]

If σ²>0, the implicit-function theorem gives a local unique critical curve κ_crit(δ)=σ²δ²+O(|δ|³); locally the unstable side is κ<κ_crit. Constants depend on the fixed S,f. This is not a graph-size-, mixing-gap-, or acquisition-uniform estimate. σ²=0 is exactly row-support constancy of f because π_i>0.

For the triangle normalized to internal total rate 1, σ²=1/2. Restoring total rate 2 replaces normalized escape by κ/2 and gives κ_crit∼δ², agreeing with the exact threshold. The independent audit also checks a zero-diagonal nonuniform rational S; the packet's original row-identity test has positive diagonals and verifies that algebra on a broader discrete-time fixture.

## 6. Work/second-moment inequality

Let P* be the original full trajectory law conditioned on eventual success, probability p>0. For a proposal Q supporting P*, define L=dP*/dQ and W=pL. Let C≥1 be a common measurable full-path cost, such as the number of explicitly generated primitive jumps. Then

\[
\mathbb E_{P^*}\sqrt C=\mathbb E_Q[\sqrt C\,L]
\le\sqrt{\mathbb E_Q C\,\mathbb E_Q L^2}.
\]

Squaring gives exactly the packet's inequality. Its equality proposal is

\[
\frac{dQ}{dP^*}=\frac{C^{-1/2}}{\mathbb E_{P^*}C^{-1/2}},
\]

assuming the displayed moments are finite. For C≥1 the inverse-root normalization is finite and positive. The optimizer need not admit a simple Markov sampler, and constructing or sampling it has not been charged by the inequality.

In the two-state network, successful-path total jump count N is geometric on {1,2,...}, with q=κ/(1+κ). Since qN converges to Exp(1) and its square roots are uniformly integrable, (E√N)²∼π/(4q). Thus bounded normalized second moment forces expected explicit path work of order 1/κ. The conclusion concerns full-path production; it does not rule out returning an analytically contracted answer or a known committor without constructing a path. It is not a variance-only or universal sample-complexity bound.

The inequality and optimal proposal have direct primary-source prior art: [Cugini, Atif and Subaşı, arXiv:2603.13495v1, Theorem 1, equations (7), (9), (10)](https://arxiv.org/html/2603.13495v1#S2). Their target law p becomes P*, their cost becomes C, and their weight p/q becomes W/p. No new inequality is established by changing the domain to successful kinetic trajectories.
