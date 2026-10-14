# Finite-order circulation cancellation: exact scope and cost

Research record for the isolated FO signature-cancellation task. The statements below are internally derived and checked by exact arithmetic where indicated. No external mathematical review, historical-priority review, or proof-assistant verification was acquired.

## Finding

Translation differences give a reusable annihilator for polynomial profile currents. For a quartic energy, the source's eight-traversal third-difference stencil is not traversal-minimal: the four-node integer stencil

\[
\nu=\delta_0-2\delta_v+2\delta_{3v}-\delta_{4v}
\]

annihilates every relevant polynomial circulation and uses six oriented loop traversals. Six is minimal among nonzero integer stencils that cancel the zeroth, first, and second translation moments. The stencil still changes the field. It preserves neither the full current nor the path signature, and its compatible realization can have quartic energy growing like \(|v|^4\) while the input energy stays fixed. It can preserve a selected statistic, such as the mean of one amplitude coordinate, but that preservation is an extra symmetry condition and does not preserve its second moment.

This supplies a compact certificate for a restricted family of new compatible fields. It does not generate every compatible profile, transfer a Jensen inequality back to the input, or close the open N812 arbitrary-gradient moment gate.

## 1. Current pairing and the general finite-order rule

Let \(a:[0,T]\to\mathbb R^d\) be a closed absolutely continuous profile path. Its oriented 1-current acts on a 1-form \(\alpha=\sum_j\alpha_j(a)\,da_j\) by

\[
\langle C_a,\alpha\rangle=\int_0^T\sum_j\alpha_j(a(x))a'_j(x)\,dx.
\]

For a translation vector \(v\), define \(P_\alpha(t)=\langle C_{a+tv},\alpha\rangle\). If the coefficient functions \(\alpha_j\) have total degree at most \(q\), then \(P_\alpha\) is a polynomial of degree at most \(q-1\). Indeed, expand each \(\alpha_j(a+tv)\) in powers of \(t\). Its possible degree-\(q\) coefficient is the constant covector \((\alpha_{j,q}(v))_j\), so its contribution is a constant 1-form integrated around a closed path, hence zero.

Consequently any finite signed integer stencil \(\nu=\sum_\ell c_\ell\delta_{t_\ell}\) satisfying

\[
\sum_\ell c_\ell t_\ell^k=0\qquad(0\le k\le q-1)
\]

obeys \(\sum_\ell c_\ell\langle C_{a+t_\ell v},\alpha\rangle=0\) for every polynomial 1-form of coefficient degree at most \(q\). A physical closed path realizes this signed current by traversing the translated loop \(|c_\ell|\) times, reversing it when \(c_\ell<0\), and joining each translated basepoint to a common basepoint by a connector and its exact reverse. Connector currents cancel. Every traversal and connector can have any strictly positive duration; the circulation statement is unchanged by those choices.

For a degree-\(p\) polynomial integrand \(F\), the profile-space one-form from the two-column Bregman identity has coefficient degree at most \(p-1\). Thus the needed translation moments are \(0,\ldots,p-2\), for every affine background \(B\). In the quartic case this means moments through degree two. For two amplitude coordinates, Green's theorem expresses the same condition as the six signed winding-area moments of monomials of degree at most two. In higher amplitude dimension the direct polynomial current moments remain the appropriate statement.

Combining this cancellation with the source's two-column identity proves \(J_F(B,D\phi_{\rm out})\ge0\) for the constructed output whenever \(F\) is rank-one convex and polynomial of degree \(p\); the positive terms belong to that output. The source's quartic coercivity conclusion also applies when its leading rank-one margin \(\mu_F\) is positive. This is a theorem for the generated field, not a comparison with the input field.

The usual \((p-1)\)-st finite difference

\[
\sum_{k=0}^{p-1}(-1)^k{p-1\choose k}\,\delta_{kv}
\]

is a general construction with total traversal count \(2^{p-1}\). Its role is exact algebraic cancellation of the circulation term. The nonnegative Bregman remainders are evaluated on the newly constructed field and do not cancel.

The same principle extends beyond polynomials when the translated periods lie in a fixed finite-dimensional shift-invariant space. If \(S_hP(t)=P(t+h)\) preserves such a space, its minimal polynomial \(m\) gives an exact stencil \(m(S_h)P=0\). Polynomial periods of degree below \(q\) are the special case \(m(z)=(z-1)^q\). For unrestricted smooth test forms the translation orbit need not be finite-dimensional, so there is no corresponding universal finite stencil.

More generally, a nonzero stencil annihilating moments \(0,\ldots,q-1\) needs at least \(q+1\) distinct translation nodes: with at most \(q\) nodes the corresponding Vandermonde matrix has full column rank. The binomial stencil reaches this support lower bound for \(q=p-1\), but its total variation need not be minimal, as the quartic six-copy construction shows. No general minimum traversal count for higher orders is claimed here.

## 2. A traversal-minimal quartic stencil

For quartics take

\[
\nu=\delta_0-2\delta_v+2\delta_{3v}-\delta_{4v}.
\]

Its first three scalar moments vanish:

\[
1-2+2-1=0,\qquad -2+6-4=0,\qquad -2+18-16=0.
\]

Its positive and negative multiplicities are both three, so its path uses six translated loop traversals. Algebraically it is the stencil \((1-z)^3(1+z)=1-2z+2z^3-z^4\), after omitting the zero coefficient at \(z^2\). Unlike the usual third difference, it includes the untranslated input loop exactly once.

This count is minimal if the operation is required to use integer numbers of copies of one fixed loop. Aggregate repeated translation nodes and cancel any common positive/negative atoms. The positive and negative atomic measures then have the same integer mass \(N\), first moment, and second moment. If \(N=1\), both are the same point mass. If \(N=2\), either one side is a double atom, forcing the other side to have zero variance and be the same atom, or both sides consist of two unit atoms. In the latter case their common sum and sum of squares determine the same unordered pair, so the measures again agree. A nonzero stencil therefore has \(N\ge3\) and total variation \(2N\ge6\). The displayed stencil attains the bound. This is a minimum for loop-copy count, not for geometric distance, connector action, total elapsed time, or energy.

The stencil does not annihilate higher-degree tests. For the counterclockwise unit square \(\Gamma=\partial([0,1]^2)\),

\[
\int_{\Gamma+t e_1} r^4\,ds=(t+1)^4-t^4=4t^3+6t^2+4t+1,
\]

and the weighted sum at \(t=0,1,3,4\) is exactly \(-48\). Thus the current is nonzero, despite its quartic-relevant cancellations. The centered translate of the same stencil at nodes \(-2,-1,1,2\) has the same residual.

This is a general limit, not an artifact of the square. A finite-length path current is a compactly supported vector-valued measure. If it paired to zero with every polynomial 1-form, each component measure would have all polynomial moments zero. Polynomial density on its compact support then forces every component measure, hence the current, to be zero. Every nonzero output current therefore has some finite-degree polynomial detector; a nonzero current cannot annihilate every polynomial degree.

## 3. A selected statistic can be preserved, but energy cannot be controlled uniformly

Use the periodic target profiles

\[
\psi_1(y)=(\cos y,\sin y),\qquad
\psi_2(y)=(\cos 2y,\sin 2y),\qquad
\phi(x,y)=r(x)\psi_1(y)+s(x)\psi_2(y).
\]

For \(a=(r,s)\), orthogonality of the Fourier modes gives

\[
\mathbb E_y|\phi_x|^2=|a'|^2,\qquad
\mathbb E_y|\phi_y|^2=r^2+4s^2,
\]

so Jensen's inequality yields

\[
\mathbb E_y|D\phi|^4\ge
\bigl(\mathbb E_y|D\phi|^2\bigr)^2
\ge (|a'|^2+|a|^2)^2.
\]

For any absolutely continuous connector from \(0\) to \(R e_1\), let \(u=|a|\) and \(w=|a'|\). The exact scalar bound

\[
(u^2+w^2)^2\ge \frac{16\sqrt3}{9}u^3w
\]

follows by minimizing \((1+x^2)^2/x\) at \(x=1/\sqrt3\). Since \(|u'|\le w\), every positive-duration connector, whatever its parameterization, has unnormalized quartic cost

\[
\int\mathbb E_y|D\phi|^4\,dx
\ge \frac{16\sqrt3}{9}\int u^3|u'|\,dx
\ge \frac{4\sqrt3}{9}R^4.
\]

Use the centered stencil \(\delta_{-2v}-2\delta_{-v}+2\delta_v-\delta_{2v}\). There is one connector and its reverse for each nonzero node, so their total cost alone is at least

\[
\frac{8\sqrt3}{9}(1+16+1+16)|v|^4
=\frac{272\sqrt3}{9}|v|^4.
\]

The input loop can be held fixed while \(|v|\) grows, so this operation has no uniform unnormalized energy-distortion bound in terms of input energy. At a fixed total cell length \(L\), a direct Hölder bound also gives, for each connector of duration \(\tau\le L\), \(\int\mathbb E_y|\phi_x|^4\,dx\ge |t v|^4/\tau^3\ge |t v|^4/L^3\). Hence the normalized quartic cost still diverges with \(|v|\) when the cell length is fixed. If one allows the period to grow and then normalizes by that period, arbitrary flat waiting at zero can dilute averages; that changes the comparison contract and is not an energy-preserving operation.

Here is an exact statistic example with all durations fixed and positive. Let \(\Gamma\) be the figure-eight that traverses the unit square in the positive quadrant and then the unit square in the negative quadrant, both based at the origin, with unit time on each edge. Its first amplitude coordinate has mean zero and second moment \(5/12\). Apply the centered six-traversal stencil with a straight connector and retrace for each translated loop, again with unit duration in each connector direction. The six loops take 48 time units and the four connector pairs take 8, so the output period is 56. The output mean of \(r\) is still exactly zero: loop offsets cancel under the absolute multiplicities, and opposite connector pairs cancel. Its second moment is instead

\[
\frac{116+20/3}{56}=\frac{46}{21}.
\]

The unmodified input, padded by 48 units at the zero profile so it has the same period 56, has second moment \((10/3)/56=5/84\). Therefore the construction preserves the selected mean while changing the second moment to a different exact value. It preserves no general amplitude statistic automatically.

## 4. Current cancellation is not full path-signature cancellation

For a fixed translation direction \(v\), the Fourier transform of the output current is

\[
\widehat C_{\mathrm{out}}(\xi)=
\left(\sum_\ell c_\ell e^{-it_\ell\xi\cdot v}\right)
\widehat C_\Gamma(\xi).
\]

Because \(\sum c_\ell=0\), every such output vanishes on the whole hyperplane \(\xi\cdot v=0\); retraced connectors do not change the current. This is a structural range restriction, not just a low-order Taylor condition. For example, the third finite difference of a circular loop in a direction \(u\not\parallel v\) has zero polynomial-current moments through degree two, but its Fourier current is nonzero at small nonzero \(\xi\perp v\): the multiplier \((1-e^{-i\xi\cdot u})^3\) is nonzero there, and a circle of radius \(R\) has

\[
\widehat C_{\mathrm{circle}}(\xi)
=-i\pi R^2J\xi+O(|\xi|^2),
\]

where \(J(\xi_1,\xi_2)=(-\xi_2,\xi_1)\); the transform is nonzero for every sufficiently small nonzero \(\xi\). Thus a fixed-direction stencil is not onto even the zero-moment compatible-current class. Each such loop is realizable by a compatible finite-profile potential; the failure is in the proposed current representation, not in gradient compatibility.

There is also an exact Chen-signature check for the six-copy, basepoint-preserving stencil on the unit square. Attach each translated square to the origin by a horizontal straight connector and retrace it after the loop. In the tensor convention \(S(\ell)=\exp(\Delta x)\exp(\Delta y)\cdots\), the concatenated path signature is the identity through levels 1–4, but its level-5 coefficient on the word \(x y x x x\) is exactly \(8\). The connector/loop path is therefore not a full retracing, even though its low-degree current tests vanish. The rational tensor multiplication is independently reproducible in `checks.py`.

## 5. Consequence for the N812 compatibility gate

The incoming circulation identity has the form

\[
J_F(B,D\phi)=\text{nonnegative Bregman remainders}
 +\text{profile-current circulation}.
\]

The stencil kills the last term for polynomial \(F\) of the chosen degree, and therefore certifies the **new output field**. The positive remainders are evaluated on that new field. Translating, reversing, repeating and connecting loops changes the profile path and its gradient law; the preceding energy bound proves that the change can be arbitrarily large. There is no implication from \(J_F(B,D\phi_{\rm out})\ge0\) back to \(J_F(B,D\phi_{\rm in})\).

N812's open G-FL-N812-REVIEW and G-FL-N812-CAPABILITY gates ask for full nine-moment completions (or a separator) for genuinely connected compatible gradients outside the certified profiles, with exact all-background optimization, certified acoustic rank-one convexity, and independent analytic/historical review. The closed hull of known moment certificates does not itself establish inclusion of arbitrary compatible-gradient moments. This cancellation operation supplies no such inclusion or decomposition: its output has a different current, its fixed-direction range is proper, and its cost is uncontrolled uniformly. It neither closes nor refutes the global compatibility question.

## 6. Exact verification and limits

`checks.py` uses the prescribed bundled Python environment, SymPy exact polynomial integration, and a hand-built truncated tensor algebra over `Fraction`. It checks all monomial coefficient 1-forms of degree at most three on the translated unit square; both six-copy stencils' translation moments; the degree-four residual; the exact equal-period mean/second-moment values; and the level-5 signature witness. The run output is preserved in `EXACT_CHECKS.log`.

The analytic arguments are the translation-degree lemma, integer-stencil lower bound, connector action bound, Fourier range obstruction, and the consequences of the cited N812 gate. Exact code checks finite identities; it does not certify the ambient rank-one-convexity or global compatibility claims in the incoming record. No external sources were consulted for this narrow algebraic investigation, and novelty remains UNKNOWN.
