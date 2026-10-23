# Focused independent challenge: absorbed first-hit p-energy

Reviewer: `/root/critical_budget`. Scientific date: 22 October 2026,
Australia/Brisbane. Status: the complete proposed lemma supplied by the
principal in the task message is accepted algebraically. Binding to the
principal's final full proof is pending; this note does not claim to have
reviewed a file that was not yet supplied.

## Object checked

For native C, let A={W<h}, B=A^c, E subset B, b=q(A), e=q(E).
On S=A union E retain actual rows from A while killing exits to B\E,
and make E absorbing. Apply this operation separately to G,L and combine
`P^E=(I+alpha G^E+beta L^E)/2`. Let
`theta=c eta in (0,1/2)`, `p=1/(1-theta)`, `D=diag(q^theta)`.

The principal's claimed energy coefficient is

\[
 \Gamma=\frac12+\frac{2^{p-1}}2(1+\Delta+\alpha e),
 \qquad \Delta=[\beta F(c)-\alpha(1-b)]_+.
\]

The claimed first-hit bound, starting from the unnormalized q restriction
to A, is

\[
 P_{q|A}(\tau_B\le N,X_{\tau_B}\in E)
 \le b^{1-\theta}e^\theta\Gamma^{N/p}. \tag{R1}
\]

Here `q|A` means the restricted subprobability, not the conditional
probability normalized by b. This convention should be explicit in the
final source to avoid an erroneous extra b.

## Independent checks

### Actual G diagonal and transformed columns

Every proposal from A to B is accepted. Thus the **actual** G diagonal
satisfies `G_yy<=b` for y in A, because each killed row `G[A,A]` has mass b.
For the q-density operator of G^E the column sums are:

- For y in A: at most `G_yy+(b-q_y)<=2b`.
- For y in E: exactly `1+b`. The 1 is the newly absorbing row at y;
  every x in A contributes q_x since `G_xy=q_y`.

Both are at most 2. The row masses are b+e on A and 1 on E. Jensen in the
unnormalized q measure therefore gives

\[
 \|vDG^ED^{-1}\|_p^p\le2^{p-1}
 \left[(b+e)\sum_A|v_x|^p+\sum_E|v_x|^p\right]. \tag{R2}
\]

No arbitrary column norm of G is substituted, and no original rejection
mass is discarded in calculating the A rows.

### Local absorption does not break the column bound

For x!=y, `L_xy(q_x/q_y)^theta<=Q_xy` when theta<=eta. In each transformed
column y in E there is a newly absorbing diagonal 1 and incoming A entries
bounded by Q_xy. Symmetry/stochasticity gives a sum at most 2. In columns
in A, the original local diagonal is at most 1 and incoming off-diagonal
terms likewise sum to at most 1. Removing E-to-A transitions only helps.

The actual transformed A rows have sum at most 1+F(c), by retaining the
original rejection diagonal and using the usual scalar transport penalty.
The absorbing E rows have sum exactly 1. Consequently

\[
 \|vDL^ED^{-1}\|_p^p\le2^{p-1}
 \left[(1+F(c))\sum_A|v_x|^p+\sum_E|v_x|^p\right]. \tag{R3}
\]

The transformed local matrix need not be stochastic; the proof uses its
explicit row and column sums.

### Lazy convexity yields the claimed common coefficient

Convexity of the p-th power norm, with weights 1/2, alpha/2, beta/2, gives
an A-energy multiplier

\[
 \frac12+\frac{2^{p-1}}2[\alpha(b+e)+\beta(1+F(c))]
 =\frac12+\frac{2^{p-1}}2[1+\beta F(c)-\alpha(1-b)+\alpha e]
 \le\Gamma.
\]

The E multiplier is `1/2+2^(p-1)/2<=Gamma`. Thus each actual absorbed step
increases total p-energy by at most Gamma. For initial submeasure q|A,
the transformed p-energy is exactly b, because p(1-theta)=1. Holder on E
then gives (R1). The absorbed E mass after N steps is exactly the probability
of a first B-hit in E by N, not a law that evaluates a fixed horizon at a
random stopping count.

### Endpoint error accounting

At c=c_* and h=u^-4, the binary-KL lower bound on q(B) gives
`Delta=O_K(h log(1/h))`. For N of order loglog n (equivalently order u),
`N Delta=O(log u/u^3)->0`. Also `N theta=O((loglog n)^2/log n)->0`.
The principal's bad set E has a uniform upper proposal mass of order
`n^-1 (log n)^4` times a polynomial in loglog n. Hence `Ne->0`,
`Gamma^(N/p)=1+o(1)`, and

\[
 e^\theta\le\exp[-c_*u+o(1)].
\]

Replacing an upper bound for e by equality is unnecessary; only this upper
inequality is used. If e=0, the hitting mass is exactly zero.

### Full smoothing and all return paths

For every j<=N, use the actual `g_j=C^(n-j)f` and its own anchor z_j. The
union defining E includes all j, including j=0. Every first hit into B\E
therefore contributes at most delta to `|g_j-z_j|`; every hit into E costs
at most its mass, controlled by (R1) plus the initial q(E). The stationary
comparison costs the actual high-tail mass plus the anchored square-root
error, weighted by the corresponding first-hit mass. The later propagation
is the full C^(n-j), so post-hit returns are retained. Paths still in A at
N cost at most their geometrically bounded total mass.

The union is allowed to depend on f: its proposal-mass bound is uniform in
0<=f<=1, and the finite hit inequality holds for every E subset B. This does
not alter the kernel or leak an observable to the sampler.

## Verdict and limits

No mathematical gap was found in the supplied absorbed-operator lemma or
its stated asymptotic error accounting. The key improvement is that mass
already absorbed in E stays in the same p-energy estimate. It avoids the
divergent sum of separate first-hit norms at the endpoint.

The final theorem still requires source-bound checking of the precise
cutoffs, horizon, uniform remainder, the one-KL subsequence reduction, and
matching lower dependency. The contributor's joint-budget lemma supplies
the needed separation, but principal acceptance and final source binding are
separate actions. No numerical experiment or historical-novelty assessment
was performed.
