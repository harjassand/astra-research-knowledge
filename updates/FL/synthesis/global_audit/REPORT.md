# FL global compatibility: independent mathematical audit

## Finding

The affine-phase modulation identity and its invariant-quartic coercivity corollary survive a cold reconstruction on their stated domains. The divergence calculation is exact for every `C^2` rank-one-convex `F`, every periodic real amplitude `r`, and every compatible affine phase `theta = k·x` when the loop satisfies `V'' = -aV` with `a ≥ 0`. The quartic estimate is

\[
\int [F(B+D\phi)-F(B)]\;\geq\;\frac{\mu_F}{12}\int |D\phi|^4,
\qquad \mu_F=\min_{|R|=1,\,\operatorname{rank}R=1}F(R),
\]

for every constant `B`, when `F` is homogeneous quartic, rank-one convex, and left-\(\mathrm{SO}(2)\)-invariant. Here \(\mu_F\geq0\); the estimate can be noncoercive when \(\mu_F=0\). No counterexample was found to either result, including at negative amplitudes, zero wavevector, zero amplitude gradient, or vanishing leading scalar coefficient.

The theorem controls a substantial family of gradients, including full-rank and internally resonant examples, but it does not resolve the full planar rank-one-convex-to-quasiconvex implication. Its amplitude/phase representation is restrictive. The exact packet assembly rule needs degree-four moment separation, and the exact two-carrier example shows why that condition cannot be dropped. The current N809 global gate therefore remains open.

One precision edit belongs in any later reuse of the geometric extension: the origin should be stated to lie **strictly inside** the positively oriented strictly convex loop. If “containing the origin” includes a boundary point, the asserted globally positive constant \(\det(V,V')\) need not exist. This does not affect the theorem, whose actual sufficient hypothesis is the explicit equation \(V''=-aV\).

## Reconstructed positive identity

Let \(\Omega\) be a periodic cell, or a bounded domain with zero trace for \(r\). Let \(\theta=k\cdot x\), \(W=V'\), and \(\phi(x)=r(x)V(\theta)\). Then

\[
D\phi=P+Q,\qquad P=rW\otimes k,\qquad Q=V\otimes\nabla r.
\]

At each point both `P` and `Q` have rank at most one. For each spatial coordinate `i`, define the scalar flux component

\[
\mathcal A_i(\theta,r)=\int_0^r DF(B+sW(\theta)\otimes k)[V(\theta)\otimes e_i],ds.
\]

The `r`-derivative of the flux gives `DF(B+P)[Q]`. Its phase derivative is

\[
\sum_i k_i\int_0^r \left\{sD^2F(B+sW\otimes k)[W'\otimes k,V\otimes e_i]
  +DF(B+sW\otimes k)[V'\otimes e_i]\right\}ds.
\]

Using `W'=-aV` and `V'=W`, the first term becomes the negative acoustic term and the second is the `s`-derivative of `F(B+sW⊗k)`. Thus

\[
\operatorname{div}\mathcal A=DF(B+P)[Q]+F(B+P)-F(B)
-a(\theta)\int_0^r sD^2F(B+sW\otimes k)[V\otimes k,V\otimes k]ds.
\]

The integral of the divergence is zero: the flux is periodic on the torus, and on the bounded-domain version `A=0` at `r=0`. Expanding the rank-one Bregman remainder

\[
R_F(B+P,Q)=F(B+P+Q)-F(B+P)-DF(B+P)[Q]
\]

then gives the exact identity

\[
\int [F(B+D\phi)-F(B)]
=\int R_F(B+P,Q)
+\int a(\theta)r^2\int_0^1 tD^2F(B+trW\otimes k)[V\otimes k,V\otimes k]dt.
\]

Each term is nonnegative. The first uses convexity of `t ↦ F(B+P+tQ)`; the second uses `a ≥ 0` and convexity along the rank-one direction `V⊗k`. This is an actual-potential proof; it does not replace compatibility with moments.

The sign of `r` causes no hidden restriction. For any continuous `g`,

\[
\int_0^r sg(s)ds=r^2\int_0^1 tg(tr)dt,
\]

which follows by `s=tr` and holds for `r<0` as well as `r>0`. At `r=0`, both sides vanish. The identity includes `k=0` and `∇r=0`; no division by either is used.

For general `C^2` integrands, the proof is stated for smooth amplitudes, so the gradients range over a compact subset of matrix space and no global growth condition is needed. For quartic integrands, strong `W^{1,4}` approximation passes each polynomial term in `L^1`, giving periodic `W^{1,4}` amplitudes and zero-trace `W^{1,4}_0` amplitudes on bounded Lipschitz domains. No such extension was inferred for arbitrary `C^2` growth.

## Complete invariant-quartic coercivity

Assume `F` is a homogeneous quartic, rank-one convex, and invariant under output rotations. Rank-one convexity implies `F(R) ≥ 0` for rank-one `R`, since `t ↦ F(tR)=t^4F(R)` is convex. Compactness of the unit rank-one set therefore gives \(\mu_F\geq0\).

For a rank-one `Q`, write

\[
f(t)=F(C+tQ)=At^4+Lt^3+C_2t^2+Dt+E,\qquad A=F(Q)\geq0.
\]

Since `f'' ≥ 0` on the whole real line, `C_2 ≥ 3L^2/(8A)` when `A>0`. Direct completion gives

\[
f(1)-f(0)-f'(0)-A/3
=\frac{3}{8A}(L+4A/3)^2+C_2-\frac{3L^2}{8A}\geq0.
\]

If `A=0`, `f''(t)=6Lt+2C_2 ≥ 0` for all `t` forces `L=0` and `C_2 ≥ 0`, yielding the same inequality without division. Consequently `R_F(C,Q) ≥ F(Q)/3`.

For the acoustic term on the circular carrier `V=(cos θ,sin θ)`, `W=V'` is the orthogonal unit vector. At fixed `B,k,V,W`,

\[
g(s)=D^2F(B+sW\otimes k)[V\otimes k,V\otimes k]=A_2s^2+L_2s+C'_2\geq0.
\]

Output-rotation invariance supplies the leading coefficient: `F((W+sV)⊗k)=(1+s^2)^2F(W⊗k)`, so `A_2=4F(W⊗k)`. When `A_2>0`,

\[
\int_0^r sg(s)ds-\frac{A_2r^4}{36}
=\frac{r^2(L_2+4A_2r/3)^2}{8A_2}
+\frac{r^2}{2}\left(C'_2-\frac{L_2^2}{4A_2}\right)\geq0.
\]

If `A_2=0`, global nonnegativity of `g` forces `L_2=0` and `C'_2 ≥ 0`, so the acoustic lower bound `A_2r^4/36=0` still holds. Hence the two terms in the exact identity are bounded below by

\[
\frac{\mu_F}{3}|\nabla r|^4+
\frac{\mu_F}{9}r^4|k|^4.
\]

Because `V,W` are orthonormal, \(|D\phi|^2=|\nabla r|^2+r^2|k|^2\). For `x=|∇r|^2`, `y=r^2|k|^2`,

\[
\frac{x^2}{3}+\frac{y^2}{9}-\frac{(x+y)^2}{12}=\frac{(3x-y)^2}{36}\geq0.
\]

This proves the `μ_F/12` inequality for all affine `B`, with no bound on the affine optimizer. It covers the entire left-`SO(2)`-invariant homogeneous quartic cone subject only to rank-one convexity; no nine-coefficient positivity classification is used. The constant `1/12` is not claimed optimal.

The estimate survives critical two-dimensional concentration templates \(\phi_\rho(x)=\rho^{1/2}\phi(x/\rho)\) on rescaled zero-boundary domains: the fourth-power gradient integral is invariant under this scaling. This says the template class remains controlled; it does not represent arbitrary concentrated compatible profiles.

## Independent exact checks

The source packet was copied before execution into `source-copy/global`. The copied verifier passed all nine listed exact groups, and its regenerated JSON is byte-for-byte identical by SHA-256 to the supplied result. Separately, `independent_checks.py` uses a distinct exact Laurent-polynomial implementation and verifies:

- The 8-by-8 acoustic Gram identity for `G` as a polynomial in arbitrary `A=(a,b,c,d)` and input-direction parameters `s,t`. The top-left 6-by-6 block has leading principal minors \(107/2,642,1605/8,8445/16,2815/8,26865/4\); the remaining Schur complement is zero. Thus the Gram is positive semidefinite, rank six. Output-rotation invariance reduces any rank-one direction to the tested `e_1⊗(s,t)`.
- On rank-one matrices, \(G=3|A|^4+(35/24)u^2\), so \(\mu_G=3\). The same exact calculation recovers `G(I)=-1/24`, `G(diag(1,-1))=1271/24`, and the determinant-balanced finite-measure mean energy `-1350/1297`. This is a non-polyconvexity witness, not a gradient counterexample.
- For \(\phi=(1+\tfrac12\cos x)(\cos y,\sin y)\), the covariance diagonal is \(1/16,9/16,1/16,9/16\), the mean affine coefficient is zero, \(\mathbb E G(D\phi)=8139/1024\), and \(\mathbb E|D\phi|^4=33/16\). The largest variance captured by a unit rank-one matrix is `9/16`, or `9/20` of total variance `20/16`.
- For the internally resonant two-coordinate amplitude \(r=1+\tfrac13\cos x+\tfrac14\cos y+\tfrac15\cos(x+y)\), the exact cubic vector is nonzero, the covariance and affine Hessian are positive definite, and full affine minimization gives \(\Delta_G=3646241010554033/507189555936000\), exceeding \(\mathbb E|D\phi|^4/4=27691873/51840000\). This tests an actual nonzero optimizer rather than only evaluating at `B=0`.
- For `F=(det A)^2`, the two compatible carrier packets have individual energies `17/128` and `17/32`, while their sum has energy `75/256`; the interaction is `-95/256`. This rules out adding the individual optimized margins without a separation condition. Since `F` is polyconvex, the negative interaction is not a negative Jensen gap.

These checks are exact finite arithmetic and internal review. They do not certify the analytic estimates, establish novelty, or constitute external or proof-assistant validation.

## Assembly and variable-phase boundaries

For a homogeneous quartic and centered blocks whose joint moments through degree four equal independent phase averages, the packet formula is sound. If `C_i=E[X_iX_i^T]`, `H_i=E[D^2F(X_i)] ≥ 0`, `b_i=E[DF(X_i)]`, and `c_i=E[F(X_i)]`, the degree-four cross term is \(\tfrac12\sum_{i<j}\operatorname{tr}(H_iC_j)\). Completing all affine-background squares gives this nonnegative covariance interaction plus the nonnegative disagreement penalty \(\tfrac12\sum_i(B_i-B_*)^TH_i(B_i-B_*)\), in addition to the individual optimized gaps. Fourier primitive-relation separation through degree four implies the required moment equality. This is a valid restricted assembly rule, not a decomposition theorem for arbitrary gradients.

The failure outside that rule is concrete, but limited: for \(\phi_1=r(x)(\cos y,\sin y)\), \(\phi_2=s(x)(\cos2y,\sin2y)\), with `r=1+½ cos x`, `s=1-½ cos x`, the optimized determinant-square interaction is negative while the total Jensen gap remains nonnegative.

For a nonlinear phase \(\theta(x)\), differentiating the same flux introduces

\[
E_F=\sum_i\int_0^r sD^2F(B+sW\otimes\nabla\theta)
[W\otimes\partial_i\nabla\theta,V\otimes e_i]ds.
\]

Rank-one convexity does not sign this mixed-Hessian pairing. In the invariant cone at `B=0`, the exact source identity reduces it to a signed phase-curvature divergence. The supplied convex quartic \((u+v-2q)^2\), phase \(\theta=x+\sin y\), and smooth positive amplitude fourth power \(1-\tfrac12\sin(2y)\) give mean defect (+1/4); reversing the sine changes its sign. This prevents extending the affine-phase proof by simply discarding the curvature term. The example is not a Jensen-gap counterexample.

## N809/FK scope comparison

The pinned capital checkout is `3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d`, matching `FL_PIN.json`'s cumulative PR83 head; its main revision is `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871`. N809's original `ADAPTIVE_AFFINE_STABILITY.md` proves an all-affine quartic law estimate only near a **simple transverse** acoustic contact: full 35-coefficient planar quartics, centered determinant-balanced finite-fourth-moment laws, relative (L^2) and (L^4) closeness to a fixed rank-one line, and a rank-three PSD Finsler remainder whose kernel is that line. It has no amplitude cap or positive moment floor. The proof explicitly says rank-two tangent contacts and large-transverse fields are excluded.

`SCOPED_NOTICES.json` records N809 as an `unreviewed_scoped_update`: the new theorem supersedes an earlier moving-Schur obligation in the simple transverse sector only. Tangent contacts, large-transverse profiles, global Morrey, and external analytic/priority review remain open. The N809 review and capability gates are both `open`. Their exact remaining obligations include a concentration-stable compatible estimate at rank-two tangent contacts or an exact compatible negative optimized gap; for global left-\(\mathrm{SO}(2)\) quartics, compatibility-to-nine-moment PSD completion or an exact separating compatible profile; and independent validation/application of the additional multi-constraint theorem.

The FL identity complements this scope: it gives unconditional all-background positivity for the restricted affine-loop family, including examples far from rank-one lines. It neither proves nine-moment PSD completion for all compatible gradients nor constructs a negative compatible profile. It does not discharge the tangent-contact gate, validate the separate multi-constraint theorem, or turn the supplied loop identities into the full nine-coefficient quasiconvexity implication. The gate status therefore remains open. The embedded `global_PASTED_SOURCE.txt` prompt is treated as provenance/narrative data; its broader “near every rank-one line” wording is not used to override the exact N809 proof and notice.

No earlier general quasiconvexity result was imported as a premise. The N809 proof was read only to compare its local spectral/law scope and its stated blockers.

## Costs, access, and limits

Inputs were supplied local source files and the pinned capital checkout; no new external data, measurements, or third-party manuscripts were acquired. Exact replays used the existing `work/FE-hidden-gate/venv/bin/python` environment with SymPy; no dependency was installed. The copied producer verifier checked 35 quartic monomials in its stated nine groups. The independent implementation checked an 8-by-8 rational Gram and three exact Laurent/Fourier examples. Wall time was a few seconds; this is not an operation-count or performance claim. Exact rational bit-operation count, energy cost, and model/token cost are unknown. There is no physical experiment, paid acquisition, or external reviewer in this audit.

The source's exploratory carrier search was not rerun and no optimizer output is used as proof. We did not independently rederive every ancillary Section 4 or frequency-graph count. Mathematical correctness beyond the analytic reconstruction and exact scope tested here, historical priority, and external validation remain unknown.
