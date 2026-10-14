# Exact scope of the smooth-bump query argument

## 1. A family inside the published interface

Fix a nonnegative, nonzero \(\psi\in C_c^\infty((-1,1))\). Write

\[
B=\|\psi'\|_\infty>0,\qquad P=\|\psi\|_\infty,
\qquad J=\int_{-1}^1\psi(u)\,du>0,
\]

and let \(\varphi\) be the standard one-dimensional Gaussian density. Set \(L=\sigma=1\), which is an allowed fixed ratio in R16/N687. For a width \(w\le 1/4\), a center \(c\in[-1/4,1/4]\), and a sign \(s\in\{-1,+1\}\), define

\[
q_{c,s}(t)=s\frac{w}{B}\psi\!\left(\frac{t-c}{w}\right),\qquad
g_i(x)=q_{c_i,s_i}(x_i),\qquad g=(g_1,\ldots,g_d).
\]

This is conservative. For example, with \(\Psi'=\psi\), take

\[
F(x)=\sum_{i=1}^d s_i\frac{w^2}{B}
\Psi\!\left(\frac{x_i-c_i}{w}\right).
\]

Then \(\nabla F=g\), \(F\in C^\infty\), and \(Dg(x)\) is diagonal with entries \(s_i\psi'((x_i-c_i)/w)/B\). Therefore

\[
\sup_x\|Dg(x)\|_{op}\le 1,
\]

so \(g\) is globally 1-Lipschitz. The function values are exact whole-vector queries, just as in the published model. No higher derivative bound is assumed; the family merely happens to be smooth.

The Gaussian mean in coordinate \(i\) is

\[
\mu_i=s_i\frac{w^2}{B}\int_{-1}^1\psi(u)\varphi(c_i+wu)\,du.
\]

For \(|c_i|\le 1/4\) and \(w\le 1/4\), the argument of \(\varphi\) stays in \([-1/2,1/2]\). Thus

\[
|\mu_i|\ge c_\psi w^2,
\qquad c_\psi=\frac{\varphi(1/2)J}{B}>0.
\]

Also \(|\mu_i|\le \varphi(0)Jw^2/B\). Thus the choice below makes \(\|\mu\|_2\) bounded above and below by positive constants independent of \(d\).

Take \(w=\kappa d^{-1/4}\) with \(\kappa^2 c_\psi\ge1\). For all sufficiently large \(d\), \(w\le1/4\) and \(\|\mu\|_2\ge1\). Centers separated by \(3w\) have disjoint bump supports. A fixed interval of center choices therefore contains

\[
m=\Theta(1/w)=\Theta(d^{1/4})
\]

possible centers per coordinate, all with the same order of Gaussian mean magnitude.

## 2. Deterministic-query lower bound

Consider an algorithm whose query locations are deterministic functions of past replies and which uses at most \(k<m\) value queries. Run it on the zero field. This fixes the all-zero transcript path and its query vectors \(x^{(1)},\ldots,x^{(k)}\). For each coordinate \(i\), the scalar sequence \(x_i^{(1)},\ldots,x_i^{(k)}\) intersects at most \(k\) of the \(m\) disjoint candidate support intervals. Choose an unhit center \(c_i\) independently for every coordinate.

The two fields using these centers with all signs positive and all signs negative both return zero on every query along this path. By induction they give the same full transcript and the algorithm has the same output law \(Q\) on both. Their target means are \(\mu\) and \(-\mu\), with \(\|\mu\|_2\ge1\). The exact equal-covariance Gaussian distance is

\[
\operatorname{TV}\big(N(\mu,I_d),N(-\mu,I_d)\big)
=2\Phi(\|\mu\|_2)-1\ge 2\Phi(1)-1>0.68.
\]

If \(Q\) were within \(\epsilon\) of both targets, the triangle inequality would bound their distance by \(2\epsilon\). Thus no such deterministic-query sampler can satisfy the target for \(\epsilon<0.34\) with fewer than \(m=\Omega(d^{1/4})\) queries.

This is a deterministic-query result. It does not apply if the query locations use random Gaussian seeds. In that case there is no single all-zero path on which to choose the centers before the algorithm runs.

## 3. Randomized-query check: one query is enough on this family asymptotically

Use the actual randomized interface: draw \(G,Z\sim N(0,I_d)\) independently, query \(g(G)\) once, and return

\[
X=g(G)+Z.
\]

The target is \(N(\mu,I_d)\). For each coordinate, put \(V_i=g_i(G_i)-\mu_i\); then \(V_i\) is centered, the \(V_i\)'s are independent, and

\[
|V_i|\le 2Pw/B,\qquad
v_i:=\mathbb E V_i^2\le \mathbb E g_i(G_i)^2
\le C_\psi w^3.
\]

The last bound uses \(|g_i|\le Pw/B\), support length \(2w\), and \(\sup\varphi=\varphi(0)\). Constants below depend only on \(\psi\).

More generally, for independent centered variables \(V_i\) with \(|V_i|\le b\), write \(v_i=\mathbb E V_i^2\). If \(b\le\sigma\), the same argument gives the reusable smoothing bound

\[
\chi^2\big(\mathcal L(V+\sigma Z)\|N(0,\sigma^2 I_d)\big)
\le \exp\!\left(\frac{e}{2\sigma^4}\sum_i v_i^2\right)-1.
\]

This criterion depends on the squared coordinate variances and independence, rather than on the Euclidean norm of one realized fluctuation. It does not apply to general dependent coordinates or unbounded centered values.

Let \(Z_i\sim N(0,1)\) be independent of \(V_i\). For \(p_i\), the density of \(V_i+Z_i\), direct Gaussian integration gives

\[
\int_{\mathbb R}\frac{\varphi(x-v)\varphi(x-v')}{\varphi(x)}\,dx
=e^{vv'}.
\]

\[
1+\chi^2(\mathcal L(V_i+Z_i)\|N(0,1))
=\mathbb E_{V_i,V_i'}e^{V_iV_i'},
\]

where \(V_i'\) is an independent copy. Since \(\mathbb E[V_iV_i']=0\), and \(|V_iV_i'|\le 4P^2w^2/B^2\le1\) for sufficiently large \(d\), Taylor's remainder yields

\[
\chi^2(\mathcal L(V_i+Z_i)\|N(0,1))
\le \frac e2\mathbb E[(V_iV_i')^2]
=\frac e2v_i^2
\le C_\psi w^6.
\]

The joint output and target are products across coordinates. Product chi-square therefore satisfies

\[
1+\chi^2(\mathcal L(X-\mu)\|N(0,I_d))
=\prod_{i=1}^d\left(1+\chi_i^2\right)
\le \exp(C_\psi d w^6).
\]

With \(w=\kappa d^{-1/4}\), this gives \(\chi^2=O(d^{-1/2})\), hence

\[
\operatorname{TV}(\mathcal L(X),N(\mu,I_d))
\le \tfrac12\sqrt{\chi^2}=O(d^{-1/4}).
\]

The constant target mean norm and the many candidate centers do not force the randomized query count to grow with \(d\): for every fixed \(\epsilon>0\), this one-query sampler meets the error once \(d\) is sufficiently large. The Gaussian output noise masks the sparse, small coordinate fluctuations in the full joint law.

## 4. What this does and does not settle

The construction falsifies the attempted extension from deterministic query paths to a randomized query lower bound. It is not a general randomized lower bound and does not expose a defect in the R16 proof. The one-query sampler is proved only for this independent-coordinate bump family. The general N687 sampler remains source-derived and unreviewed; the N687/N688 checkpoint still requires an acquired positive full-law completion and a charged every-execution polylogarithmic query bound.
