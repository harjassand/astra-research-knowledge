# Branch-scoped port-response certificate

This is a finite-dimensional mathematical statement. It does not certify that a physical device follows the postulated branch.

## General operation and theorem

Split a steady network into modeled local coordinates \(x\in\mathbb R^n\), an accessible port \(z\in\mathbb R^m\), and hidden exterior coordinates \(y\). Let the full potential be
\[
  E_h(x,z,y)=U_h(x,z)+V(y,z).
\]
Assume \(U_h,V\) are twice continuously differentiable. On a convex port set \(D\), suppose a selected exterior branch \(y(z)\) obeys
\[
  V_y(y(z),z)=0,\qquad V_{yy}(y(z),z)\succ0.
\]
The physical operation is to clamp \(z\) on that branch, acquire its port-current relation
\(j(z)=V_z(y(z),z)\), and solve the reduced local equations
\[
  F_h(x,z):=(U_{h,x}(x,z),\ U_{h,z}(x,z)+j(z))=0.                 \tag{1}
\]
The hidden dimension does not occur in the prediction once \(j\) is acquired. This is exact only for equilibria on the *same selected branch*. The implicit-function theorem gives
\[
  D j(z)=V_{zz}-V_{zy}V_{yy}^{-1}V_{yz},                         \tag{2}
\]
evaluated at \((y(z),z)\). This port derivative may be negative even though the full coupled equilibrium is stable.

**Certified-error statement.** Let \(\Omega\subseteq\mathbb R^n\times D\) be convex. Suppose \(F_h\) is strongly monotone on \(\Omega\) with modulus \(\mu>0\), that an exact root \(w_h\in\Omega\) and an approximate root \(\widehat w_h\in\Omega\) exist, and that a calibrated port relation satisfies \(\sup_{z\in D}\|j(z)-\widehat j(z)\|_2\le\epsilon\). If \(\widehat w_h\) solves (1) with \(\widehat j\), then
\[
  \|w_h-\widehat w_h\|_2\le\epsilon/\mu.                       \tag{3}
\]
For an \(L\)-Lipschitz target \(g(w)\), its absolute error is at most \(L\epsilon/\mu\). If both endpoints of a contrast are predicted from approximate ports, the contrast error is at most \(2L\epsilon/\mu\); a directly measured exact baseline needs only one term.

**Proof.** Since \(F_h(w_h)=0\) and \(\widehat F_h(\widehat w_h)=0\), the only nonzero component of \(F_h(\widehat w_h)\) is \(j(\widehat z_h)-\widehat j(\widehat z_h)\), whose norm is at most \(\epsilon\). Strong monotonicity gives
\(\mu\|w_h-\widehat w_h\|^2\le\langle F_h(w_h)-F_h(\widehat w_h),w_h-\widehat w_h\rangle\le\epsilon\|w_h-\widehat w_h\|\), proving (3). Differentiating \(V_y(y(z),z)=0\) gives \(y'(z)=-V_{yy}^{-1}V_{yz}\), then (2). The full Hessian is positive definite on the chosen branch if and only if \(V_{yy}\succ0\) and the reduced Hessian \(D F_h\succ0\), by its Schur complement. This proves local stability, not global minimality or immunity to switching.

## Explicit nonconvex fixture

Take scalar \(x,z,y\), \(k=4/5\), \(y_0=\sqrt{1-k}=1/\sqrt5\), and \(j_0=-ky_0\). Set
\[
 V(y,z)=\tfrac14(y^2-1)^2+\tfrac{k}{2}(y-z)^2,
 \qquad U_h(x,z)=\tfrac12x^2+\tfrac12(x-z)^2+\tfrac32z^2-hx-j_0z.
\]
At fixed \(z\), the exterior equation is \(y^3-(1-k)y-kz=0\). For \(z\in[0,1/5]\), the positive branch \(y(z)\ge y_0\) is unique on \([y_0,\infty)\), with
\[
 D(z)=V_{yy}=3y(z)^2-(1-k)\ge2(1-k)=2/5,
 \quad j(z)=k(z-y(z)),
 \quad j'(z)=k-\frac{k^2}{D(z)}\ge-4/5.
\]
Thus \(j'(0)=-4/5<0\): the exterior port is locally *negative differential*, outside the globally convex/monotone resistor-network case. Yet the coupled reduced Hessian is bounded below by
\[
 \begin{pmatrix}2&-1\\-1&4+j'(z)\end{pmatrix}
 \succeq \begin{pmatrix}2&-1\\-1&16/5\end{pmatrix},
\]
whose least eigenvalue is \(\mu=(26-\sqrt{136})/10=(5.2-\sqrt{5.44})/2\approx1.433809621\). The full selected-branch Hessian is therefore positive definite for every drive considered here.

Eliminating \(x\) yields \(x=(h+z)/2\) and
\[
 f_h(z)=\tfrac72 z+j(z)-j_0-\tfrac h2=0,
 \qquad f_h'(z)\ge\tfrac{27}{10}.
\]
For \(0\le h\le1\), \(f_h(0)=-h/2\) and \(f_h(h/5.4)\ge0\), so a unique selected-branch root lies at \(0\le z\le h/5.4<1/5\).

The second derivative of the port relation is
\[
 j''(z)=\frac{6k^3 y(z)}{D(z)^3}.
\]
It decreases as \(y\) increases on this branch, since the derivative of \(y/(3y^2-1+k)^3\) has numerator \(-15y^2-(1-k)<0\). Hence the exact global bound on \([0,1/5]\) is
\[
 M=j''(0)=\frac{6k^3y_0}{[2(1-k)]^3}\approx21.466252584.
\]
If port-current samples on a grid of step \(\Delta\) each have certified absolute error at most \(\eta\), piecewise-linear interpolation obeys the standard Taylor-remainder bound
\[
 \sup|j-\widehat j|\le\eta+M\Delta^2/8=:\epsilon.          \tag{4}
\]
Equation (3) gives a full-state error bound. The scalar equation gives the tighter target bound
\[
 |\widehat x_h-x_h|=\tfrac12|\widehat z_h-z_h|
 \le\epsilon/5.4.                                               \tag{5}
\]
The numerical constants in (4) are *supplied by the explicit simulator model*. Real port samples alone do not certify a derivative or curvature bound between samples.

## Branch-selection obstruction

At \(z=0\), the exterior has stable branches \(y_+=y_0\) and \(y_-=-y_0\), with respective port currents \(j_+=-ky_0\) and \(j_-=+ky_0\). They differ by \(2ky_0\approx0.715541753\). The positive branch disappears in a saddle-node fold at
\[
 z=-z_f,\quad z_f=\frac{2(1-k)}{3k}\sqrt{\frac{1-k}{3}}
 \approx0.0430331483;
\]
the negative branch disappears at \(+z_f\). A quasistatic descending and ascending sweep therefore gives distinct port currents at the *same* \(z=0\). A single-valued port table without preparation and branch labels cannot predict both. Equations (1)–(5) apply only while the controlled experiment stays on the calibrated branch. Finite numerical sweeps diagnose the fold but do not prove absence of noise-driven switching before it.

## Executable check

Run `python3 port_branch.py` from this folder. It writes `RESULTS.json` and asserts its analytic bounds. It simulates 21 port clamps on \([0,0.2]\) with deterministic injected errors \(\pm10^{-4}\), a held-out drive \(h=1\), and two 801-state quasistatic sweeps. These are simulator calls, not acquired physical measurements. Its assertions are numerical consistency checks; the inequalities above are the mathematical proof.
