# Companion: finite no-reset forecasting of an unknown initial force

## Purpose and limits

The main retained-device construction uses a long finite hold, measures the surviving force, and treats it as nearly constant over the deployment horizon. This companion supplies an alternative when holding time is especially expensive: estimate the signed initial-force function from a past observation window and certify its continuation.

It is a constructive theorem, but its precision requirement can be severe. It is not the recommended flagship initialization route. The theorem uses measured force residuals, not an oracle for microscopic hidden states, and it does not assume a reset.

## 1. The admissible initial-force class

Let

\[
 g(t)=\int_{[0,\infty)}e^{-\lambda t}d\beta(\lambda),\qquad
 \|\beta\|_{\rm TV}\le C.
\tag{1}
\]

The signed measure \(\beta\) can be \((y_\lambda(0)-x(0))d\nu\), with
\(C\le\sqrt{2BE_0}\). The sign is immaterial. Neither a positive rate floor nor a finite rate ceiling is imposed. For every positive age,

\[
 |g'(t)|\le C/(et).
\]

Choose an observed window \([a_0,a_0+W]\), where \(a_0>0\), and forecast the next interval of length \(L\). Let \(m\ge1\), \(\Delta=W/m\), and

\[
 t_j=a_0+j\Delta\quad(0\le j\le m),\qquad c=1+L/W\ge1.
\]

The observation times are strictly positive, avoiding an assumed finite derivative at the original time zero.

## 2. A polynomial approximation with explicit constants

For every real \(\beta\in[m,cm]\), there is a polynomial \(p_{m,\beta}\) of degree at most \(m\) such that

\[
 \|u^\beta-p_{m,\beta}(u)\|_{L^\infty(0,1)}
 \le c\exp[-m/(c+1)],
\tag{2}
\]

and its monomial coefficients obey

\[
 \sum_{j=0}^m |[u^j]p_{m,\beta}|\le3\chi^m,
 \qquad \chi=3+2\sqrt2.
\tag{3}
\]

### Proof

Use the shifted Chebyshev expansion

\[
 u^\beta=\sum_{k=0}^{\infty}a_kT_k(2u-1),
\]

where

\[
 a_0=\frac{\Gamma(2\beta+1)}{2^{2\beta}\Gamma(\beta+1)^2},
 \quad
 a_k=\frac{2\Gamma(2\beta+1)}{2^{2\beta}\Gamma(\beta-k+1)\Gamma(\beta+k+1)}\quad(k\ge1).
\tag{4}
\]

This follows by substituting \(u=(1+\cos\theta)/2\) into the cosine-series integral. For integer \(\beta\) the series terminates. For noninteger \(\beta\ge1\), the coefficients are absolutely summable; the same integral formula gives their large-index decay.

Let \(p_{m,\beta}\) be the first \(m+1\) terms. Because \(m\le\beta\),

\[
 0\le a_m
 =2a_0\prod_{j=0}^{m-1}\frac{\beta-j}{\beta+j+1}
 \le2\exp\!\left[-\frac{m^2}{\beta+m}\right]
 \le2e^{-m/(c+1)}.
\tag{5}
\]

Here \(a_0\le1\) and \(\log(1-z)\le-z\) give the middle inequality, since the sum of the numerators \(2j+1\) is \(m^2\).

For noninteger \(\beta\), put \(J=\lfloor\beta\rfloor+1\). The coefficients through \(a_J\) are nonnegative, and

\[
 a_{k+1}/a_k=(\beta-k)/(\beta+k+1).
\]

The positive tail beyond \(m\) is bounded by

\[
 \sum_{k=m+1}^{J}a_k
 \le a_m\frac{\beta-m}{2m+1}.
\]

After \(J\), signs alternate and
\(|a_{k+1}|/|a_k|=(k-\beta)/(k+\beta+1)\). The identity

\[
 \frac{(k+\beta)|a_k|}{2\beta}
 -\frac{(k+1+\beta)|a_{k+1}|}{2\beta}=|a_k|
\]

telescopes, giving

\[
 \sum_{k=J+1}^{\infty}|a_k|
 =\frac{J-\beta}{2\beta}a_J
 \le\frac{a_m}{2\beta}.
\]

Consequently

\[
 \sum_{k>m}|a_k|
 \le a_m\left(\frac{\beta-m}{2m+1}+\frac1{2\beta}\right)
 \le\frac c2a_m,
\]

which proves (2). The terminating integer case obeys the same bound.

Finally, \(T_k(2u-1)\) has alternating monomial coefficients, because its roots all lie in \((0,1)\). Their absolute sum equals \(T_k(3)\le\chi^k\). The cosine-series formula gives \(|a_0|\le1\), \(|a_k|\le2\), so

\[
 \sum_j|[u^j]p_{m,\beta}|\le1+2\sum_{k=1}^m\chi^k
 \le3\chi^m.
\]

## 3. A finite data-to-future certificate

Suppose two admissible force functions \(g,\widehat g\), each satisfying (1), obey

\[
 |g(t_j)-\widehat g(t_j)|\le\delta_s\qquad(0\le j\le m).
\]

For \(t\in[a_0+W,a_0+W+L]\), set
\(\beta=(t-a_0)/\Delta\in[m,cm]\), and change variables \(u=e^{-\lambda\Delta}\). After multiplication by \(e^{-\lambda a_0}\), each signed measure still has total variation at most \(C\). Its first \(m+1\) moments are exactly \(g(t_j)\). Equations (2)–(3) give

\[
 \boxed{
 \sup_{a_0+W\le t\le a_0+W+L}|g(t)-\widehat g(t)|
 \le2Cc e^{-m/(c+1)}+3\chi^m\delta_s.
 }
\tag{6}
\]

This bound holds simultaneously for the entire future window. It is a certificate for every pair of functions consistent with the finite data, not just a pointwise forecast formula.

To achieve error \(\epsilon_g\), sufficient choices are

\[
 m\ge(c+1)\log(4Cc/\epsilon_g),\qquad
 \delta_s\le\epsilon_g/(6\chi^m).
\tag{7}
\]

Thus the number of measured force values is logarithmic in accuracy for a fixed forecast-to-observation ratio. The required precision is a high polynomial power of \(\epsilon_g\), with exponent increasing with that ratio. This is not a well-conditioned recovery of the hidden spectrum.

If each measured value and fitted value lie within \(\eta_s\) of a common observation, use \(\delta_s=2\eta_s\).

## 4. Making a passive model with paid initial energy

An arbitrary signed exponential fit to \(g\) need not be compatible with the positive kernel fit or have bounded initial energy. A joint finite-pole fit can enforce both.

On a finite rate dictionary \(\ell_j\ge0\), use variables \(w_j\ge0\), \(c_j\in\mathbb R\), and \(E_j\ge0\), with

\[
 c_j^2\le2w_jE_j,\quad
 \sum_jw_j\le B,\quad\sum_jE_j\le E_0.
\tag{8}
\]

Kernel data constrain \(\sum_jw_je^{-\ell_jt}\), and initial-force data constrain \(\sum_jc_je^{-\ell_jt}\). These are linear observation constraints plus rotated second-order cones. For \(w_j>0\), initialize the corresponding hidden offset at \(c_j/w_j\). Its stored energy is \(c_j^2/(2w_j)\), so (8) enforces the physical budget. Terms with \(w_j=0\) have \(c_j=0\).

Feasibility is constructive. Lump the true measures into rate cells: \(w_j=\nu(I_j)\), \(c_j=\int_{I_j}z_0d\nu\), \(E_j=\tfrac12\int_{I_j}z_0^2d\nu\). Cauchy–Schwarz gives (8). For a dictionary replacing a rate by a relative factor at most \(1+\rho\), the pointwise exponential error is at most \(\rho/e\). Rates below \(\lambda_{\min}\) can map to zero with error at most \(\lambda_{\min}t_{\max}\); rates above \(\lambda_{\max}\) can map to \(\lambda_{\max}\) with error at most \(e^{-\lambda_{\max}t_{\min}}\) on positive observation times. Choosing these errors below the observation slack proves finite-grid feasibility. The dictionary can be large when \(\eta_s\) is very small.

After a feasible fit, put \(z_j=c_j/w_j\) for its nonzero weights. A conic Carathéodory elimination preserves kernel observations, force observations, total mass, and total energy using at most

\[
 N_K+N_g+2
\]

atoms in the scalar case. Indeed, treat each retained mode as the feature vector consisting of its kernel values, its \(z_j\)-weighted force values, \(1\), and \(z_j^2/2\). Linear dependence allows a nonnegative weight adjustment until one weight vanishes. Repetition leaves at most the feature dimension. The procedure preserves the original \(z_j\) of retained atoms and therefore preserves the energy inequality.

## 5. Accessing the initial force on the actual apparatus

Once a kernel certificate is available, the original balance equation gives

\[
 g(t)=\dot x(t)+V'(x(t))+(K*\dot x)(t)-f(t).
\]

A reconstructed history \(\widetilde x\) and fitted positive kernel \(\widehat K\) give a residual estimate. If \(\|K-\widehat K\|_1\le\zeta\), \(\|\dot x\|_\infty\le D_x\), and position error is at most \(\epsilon_x\), then the kernel/history portion of its error is at most

\[
 \zeta D_x+2B\epsilon_x.
\]

The second term follows by integration by parts and does not grow with the fastest rate. Add velocity-estimation error, the known potential-force evaluation error, and applied-force readout error.

At positive ages a backward difference uses no future observation. Under a certified acceleration bound \(A_x\), its error is at most \(A_xh/2+2\epsilon_x/h\). Such a bound is available away from time zero when the applied force is sufficiently regular: \(|g'(t)|\le C/(et)\), \(K\) has total variation at most \(B\), and the known potential is Lipschitz on the certified position range. For example,

\[
 |\ddot x(t)|\le|\dot f(t)|+L_xD_x+2BD_x+C/(et).
\]

This exposes the practical drawback: (7) can demand a much tighter kernel certificate and much finer physical readout than the eventual trajectory error would suggest. The main hold-and-measure route avoids this analytic-continuation conditioning.

## 6. Why an initial budget or an extra observation is indispensable

Kernel knowledge alone does not identify the old signed force. A frozen mode can exert a nonzero constant force forever. If initial hidden energy is unbounded, even a known finite kernel with sufficiently many distinct rates admits signed initial-state combinations that vanish at any prescribed finite set of observation times but are nonzero later. Scaling that null combination defeats any fixed future error tolerance. The total-variation/energy budget and the actual initial-force data are therefore essential resources.

This companion is a self-contained derivation. Its approximation ingredients are classical Chebyshev and moment arguments; no novelty claim is made.
