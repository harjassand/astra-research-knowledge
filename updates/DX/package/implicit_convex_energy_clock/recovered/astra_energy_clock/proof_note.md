# All-future approximation of convex flows from implicit quadratic energies

Research derivation, 12 October 2026 (Australia/Brisbane)

## Status and scope

This note supplies a complete mathematical derivation of an end-to-end approximation theorem. The proposed contribution is the **finite-bit, all-future compilation**, including latent-variable preservation, equilibrium-selection approximation, and a finite certificate for every future time. Historical priority for this complete combination has NOT been established. No independent proof review or formal verification has been performed.

The Brézis–Ekeland–Nayroles variational principle, dissipation-based backward-Euler error analysis, Hoffman error bounds, and polynomial-time convex quadratic programming are established mathematics, not inventions of this investigation. In particular, Stefanelli [S2] already develops a discrete global-in-time Brézis–Ekeland principle, and Antil–Kaltenbach–Kirk [S3] develop duality-based subgradient-flow error identities. The energy-error mechanism must not be advertised as new.

The result concerns autonomous, finite-dimensional **convex subgradient relaxation**, with the explicit input representation below. It does not assert fast simulation of arbitrary nonlinear, oscillatory, driven, stochastic, or quantum physical systems. Nor does it prove a continuum discretization theorem.

Complexity is polynomial in input bit length and the RECIPROCAL of the requested normalized error. It is not claimed polynomial in the number of accuracy bits.

## 1. Exact input/output contract

Let

\[
Y=\{y\in\mathbb R^D:Ay\le b\},\qquad
q(y)=\tfrac12y^THy+g^Ty,
\]

where all entries of \(H,g,A,b\) are rational, \(H=H^T\succeq0\), and \(Y\) is nonempty. Assume \(q\) is bounded below on \(Y\). Let \(P\) select the first \(d\le D\) coordinates, and define the observed-state energy

\[
F(x)=\min\{q(y):y\in Y,\ Py=x\},
\tag{1.1}
\]

with value \(+\infty\) for an infeasible fiber. The representation is the supplied rational matrices; its latent dimension and all its inequalities are charged as input. No expansion into active regions or explicit formula for \(F\) is assumed.

A bounded-below quadratic on a nonempty polyhedron attains its minimum. The same holds on each feasible fiber. The value function in (1.1) is proper, lower semicontinuous and convex. One way to see lower semicontinuity without eliminating the latent variables is to use the affine minorants supplied by the KKT conditions on each fiber. At a fiber minimizer, those conditions supply a global affine minorant of \(F\) that agrees at that state; outside the closed polyhedral projection \(PY\), separating hyperplanes, together with the global lower bound, give the extended value. Thus \(F\) is the supremum of its affine minorants. The attainment, KKT, and bit-algorithm facts used here are standard convex-QP results [S4].

Let \(x_0\in\mathbb Q^d\cap\operatorname{dom}F\). Consider the unique convex subgradient flow

\[
\dot u(t)+\partial F(u(t))\ni0,\qquad u(0)=x_0.
\tag{1.2}
\]

Let \(y_*\) be a rational minimizer of \(q\) on \(Y\), and \(z_*=Py_*\). Supply or compute a positive rational \(R\) satisfying

\[
\|x_0-z_*\|\le R.
\tag{1.3}
\]

The error scale is \(R\). Absolute accuracy \(a>0\) is obtained by using normalized accuracy \(a/R\); the corresponding reciprocal ratio is charged. This is not a claim of independence from the requested state-space resolution.

### Main theorem

For rational \(0<\epsilon<1\), a deterministic algorithm constructs rational nodes

\[
0=t_0<t_1<\cdots<t_N=T_*,
\]

rational states \(v_0=x_0,v_1,\ldots,v_N=s\), and rational certificates, such that the continuous polygonal curve \(v\), extended by \(v(t)=s\) for \(t\ge T_*\), satisfies

\[
\boxed{\sup_{t\ge0}\|v(t)-u(t)\|\le\epsilon R.}
\tag{1.4}
\]

Moreover, \(s\in\arg\min F\), and if \(u_\infty=\lim_{t\to\infty}u(t)\), then

\[
\|s-u_\infty\|\le\epsilon R.
\tag{1.5}
\]

The running time and output bit length are polynomial in the explicit rational input length, the encoding of \(x_0,R\), and \(\epsilon^{-1}\). The algorithm uses a polynomial-time rational convex-QP backend [S4]. This backend is an imported theorem, not implemented in the accompanying prototype.

No unique minimizer, strong convexity, specified spectral gap, or bound on the number of active-region changes is required.

## 2. Basic flow estimates

Put \(m_*=\min F=\min_Yq\) and \(E(x)=F(x)-m_*\). The usual convex subgradient-flow theory supplies an absolutely continuous solution on finite intervals, energy monotonicity, and the subgradient inequalities below. The calculations also establish every quantitative bound used subsequently.

For any \(z\in\arg\min F\), writing \(a(t)=-\dot u(t)\in\partial F(u(t))\),

\[
\tfrac12\frac d{dt}\|u(t)-z\|^2
=-\langle a(t),u(t)-z\rangle
\le-E(u(t)).
\tag{2.1}
\]

Consequently the distance to each fixed minimizer is nonincreasing, and

\[
\int_0^\infty E(u(t))\,dt\le R^2/2,
\qquad E(u(t))\le R^2/(2t)\quad(t>0).
\tag{2.2}
\]

The second inequality uses energy monotonicity. Boundedness of the trajectory, lower semicontinuity, and (2.2) give a cluster point in the minimizer set. Nonincreasing distance to that cluster point gives convergence of the entire trajectory to \(u_\infty\). The selected minimizer need not be the metric projection of \(x_0\) onto the minimizer set.

## 3. A classical action, used as a finite certificate

For an absolutely continuous candidate \(v\) with \(v(0)=x_0\), define

\[
\mathcal A_F(v)=
\int_0^T\{F(v(t))+F^*(-\dot v(t))\}\,dt
+\tfrac12\|v(T)\|^2-\tfrac12\|x_0\|^2.
\tag{3.1}
\]

Fenchel's inequality says the pointwise integrand

\[
F(v)+F^*(-\dot v)+\langle v,\dot v\rangle
\]

is nonnegative. This is the Brézis–Ekeland–Nayroles structure, not a new variational principle [S2,S3].

Let \(a=-\dot u\in\partial F(u)\), and \(c=-\dot v\). Subgradient and Fenchel inequalities give

\[
\begin{aligned}
\tfrac12\frac d{dt}\|v-u\|^2
&=\langle v-u,a-c\rangle\\
&\le F(v)-F(u)-\langle c,v-u\rangle\\
&\le F(v)+F^*(c)-\langle c,v\rangle.
\end{aligned}
\]

Since all partial action integrals are bounded by the full action,

\[
\boxed{\sup_{0\le t\le T}\|v(t)-u(t)\|^2\le2\mathcal A_F(v).}
\tag{3.2}
\]

This implication concerns state norm. It does not automatically bound velocities, stresses, hitting times without a margin, or accumulated observables over arbitrarily long intervals.

## 4. Preserve the implicit energy by a primal–dual lift

Take a rational mesh, \(h_i=t_i-t_{i-1}>0\). Fix a feasible lift \(y_0\in Y\) with \(Py_0=x_0\). It need not minimize its fiber; its energy is an admissible initial upper bound.

For each cell choose primal \(y_i\in Y\), dual \(w_i\in\mathbb R^D\), and \(\lambda_i\in\mathbb R^m_{\ge0}\), subject to the linear equations

\[
Hw_i+g+A^T\lambda_i
=P^T\frac{Py_{i-1}-Py_i}{h_i}.
\tag{4.1}
\]

Write \(x_i=Py_i\). These variables define a piecewise-affine observed curve \(v\).

For any \(c\in\mathbb R^d\), a feasible relation

\[
Hw+g+A^T\lambda=P^Tc,\qquad\lambda\ge0,
\]

implies, for every feasible \(y\),

\[
\begin{aligned}
\langle c,Py\rangle-q(y)
&=\langle Hw,y\rangle-\tfrac12y^THy+\lambda^TAy\\
&\le\tfrac12w^THw+b^T\lambda.
\end{aligned}
\]

Thus

\[
F^*(c)\le\tfrac12w^THw+b^T\lambda.
\tag{4.2}
\]

No conjugate oracle or enumeration of active patterns is used. Similarly, interpolating two feasible latent states remains feasible and convexity gives

\[
\int_{t_{i-1}}^{t_i}F(v(t))dt
\le\tfrac{h_i}{2}\{q(y_{i-1})+q(y_i)\}.
\]

It follows that the rational quantity

\[
\boxed{
\mathcal J=
\tfrac12\|x_N\|^2-\tfrac12\|x_0\|^2
+\sum_{i=1}^Nh_i
\left[
\frac{q(y_{i-1})+q(y_i)}2
+\frac12w_i^THw_i+b^T\lambda_i
\right]
}
\tag{4.3}
\]

satisfies

\[
0\le\mathcal A_F(v)\le\mathcal J,
\qquad
\sup_{[0,T]}\|v-u\|\le\sqrt{2\mathcal J}.
\tag{4.4}
\]

### Why this is a convex QP

The constraints are linear. Every quadratic term in (4.3) has a positive-semidefinite Hessian: endpoint norm, primal energy terms, and dual energy terms. The remaining terms are affine. Thus minimizing \(\mathcal J\) is a convex QP with

\[
N(2D+m)\text{ variables},\quad ND\text{ equalities},\quad2Nm\text{ inequalities}.
\]

The sparse coefficient count is \(O(N(D^2+mD))\). The matrices defining (1.1) remain explicit and unexpanded.

This is not equivalent to adding arbitrary physical dynamics to the latent variables. The latent states encode quasistatic minimization of an energy; the observed flow is the flow of that minimized energy. Section 10 gives a counterexample to the naive dynamical lift.

## 5. The logarithmic time mesh

Let \(E_0=q(y_0)-m_*>0\). Choose

\[
a=R^2/(2E_0),\qquad0<\eta<1,
\]

and use

\[
h_i=\min\{\eta(a+t_{i-1}),T-t_{i-1}\}.
\tag{5.1}
\]

Before the final truncation, \(t_i=a((1+\eta)^i-1)\). Hence the number of cells is

\[
N=\left\lceil\frac{\log(1+2TE_0/R^2)}{\log(1+\eta)}\right\rceil.
\tag{5.2}
\]

### A small-objective feasible witness

Choose exact proximal states

\[
x_i=\arg\min_x\left\{F(x)+\frac{\|x-x_{i-1}\|^2}{2h_i}\right\}.
\tag{5.3}
\]

Each is obtained by a convex QP in \(y\in Y\), with the observed squared-distance penalty. Let \(y_i\) be a corresponding optimizer. KKT conditions supply \(\lambda_i\ge0\) with

\[
Hy_i+g+A^T\lambda_i
=P^T(x_{i-1}-x_i)/h_i,
\quad \lambda_i^T(b-Ay_i)=0.
\]

Taking \(w_i=y_i\) makes (4.1) feasible and makes (4.2) an equality at \(x_i\).

Put \(e_0=E_0\), and \(e_i=q(y_i)-m_*=E(x_i)\) for \(i\ge1\). The sequence \(e_i\) is nonincreasing. From the subgradient inequality against \(z_*\),

\[
2h_ie_i\le
\|x_{i-1}-z_*\|^2-\|x_i-z_*\|^2-\|x_i-x_{i-1}\|^2,
\]

so

\[
\sum_ih_ie_i\le R^2/2.
\tag{5.4}
\]

Substitution into (4.3), including telescoping endpoint terms, gives the exact identity

\[
\mathcal J=
\frac12\sum_i\left[h_i(e_{i-1}-e_i)-\|x_i-x_{i-1}\|^2\right].
\tag{5.5}
\]

The individual bracket terms are nonnegative by the subgradient inequality; the first remains so when \(e_0\) is merely an energy upper bound.

Now use (5.1), nonnegativity of \(e_{i-1}-e_i\), and summation by parts:

\[
\begin{aligned}
\sum_i h_i(e_{i-1}-e_i)
&\le\eta a e_0+\eta\sum_i t_{i-1}(e_{i-1}-e_i)\\
&\le\eta a e_0+\eta\sum_i h_ie_i\\
&\le\eta R^2.
\end{aligned}
\tag{5.6}
\]

Thus the global QP has a feasible point with

\[
\boxed{\mathcal J\le\eta R^2/2.}
\tag{5.7}
\]

This calculation is an application of classical dissipation-based error analysis [S1], not a claim to have discovered backward Euler or its energy residual. Its use here is to bound the *size of an acquired finite-bit global optimization problem* by the logarithm of the physical horizon.

## 6. Finite-horizon bit complexity

Set \(\eta=\epsilon^2/32\), and solve the global QP to additive objective error at most \(\epsilon^2R^2/64\), while returning a feasible rational point. By (5.7), the returned point has

\[
\mathcal J\le\epsilon^2R^2/32,
\qquad
\sup_{[0,T]}\|v-u\|\le\epsilon R/4.
\tag{6.1}
\]

Classical convex-QP algorithms provide polynomial bit complexity [S4]. In particular, the QP is feasible and bounded below by zero, so its minimum is attained. Rational minimizers and KKT witnesses have polynomially bounded encodings. One may use exact rational optimization or an appropriately certified additive approximation.

There is no unit-cost operation on unbounded real numbers in this statement. A mesh node has encoding length bounded by the initial-data encoding plus \(O(N\operatorname{bit}(1+\eta))\). Computing nodes by rational multiplication and final comparison is polynomial in their output length. Precision needed for the objective tolerance has only \(O(\operatorname{bit}(R)+\log(1/\epsilon))\) bits, in addition to problem coefficients.

The imported QP algorithm may have a large polynomial running-time exponent. The theorem does not assert a practical speedup for all matrices or constant cost per proximal step.

## 7. A polynomial-bit tail bound without an acquired spectral gap

Obtain a rational global minimizer \(y_*\) and rational KKT multiplier \(\lambda_*\ge0\):

\[
Hy_*+g+A^T\lambda_*=0,
\qquad
\lambda_*^T(b-Ay_*)=0.
\tag{7.1}
\]

For every feasible \(y\),

\[
q(y)-m_*
=\tfrac12(y-y_*)^TH(y-y_*)+\lambda_*^T(b-Ay).
\tag{7.2}
\]

Both terms are nonnegative. The complete latent minimizer set is the rational polyhedron

\[
Y_*=\{y:Ay\le b,\ H(y-y_*)=0,
\lambda_*^T(b-Ay)=0\}.
\tag{7.3}
\]

Its observed projection is precisely \(S=\arg\min F\). The algorithm never eliminates the latent variables to materialize that projection.

### Explicit, crude Hoffman constant

Write (7.3) entirely as inequalities \(By\le c\), using both signs for equalities. Let \(D_0\) be a common positive denominator of entries of \(B\), let

\[
U=\max(1,\max_{ij}|(D_0B)_{ij}|),
\qquad
K=D_0(DU)^{D-1}.
\tag{7.4}
\]

Then

\[
\operatorname{dist}(y,Y_*)\le K\|(By-c)_+\|_2.
\tag{7.5}
\]

For completeness, this particular bound follows directly from linear algebra. If \(p\) is the metric projection of \(y\) onto the polyhedron, the vector \(y-p\) is a nonnegative combination of linearly independent active row normals, say \(B_I^T\alpha\), \(\alpha\ge0\). Every independent row submatrix of the integer matrix \(D_0B\) has Gram determinant a positive integer, hence at least one. Its largest singular value is at most \(DU\). Consequently its least singular value is at least \((DU)^{-(D-1)}\), and that of \(B_I\) is at least \(1/K\). Therefore

\[
\begin{aligned}
\|y-p\|^2
&=\alpha^T(B_Iy-c_I)\\
&\le\|\alpha\|\|(By-c)_+\|\\
&\le K\|y-p\|\|(By-c)_+\|.
\end{aligned}
\]

This is a deliberately loose, computable Hoffman bound. Hoffman's principle itself is prior work [S5]; no algorithm for the optimal Hoffman constant is asserted.

Let \(\overline H=\sum_{ij}|H_{ij}|\ge\|H\|_{2\to2}\). At a feasible \(y\) with gap \(e=q(y)-m_*\le E_0\), equation (7.2) gives

\[
\|H(y-y_*)\|^2\le2\overline H e,
\qquad
[\lambda_*^T(b-Ay)]^2\le E_0e.
\]

The original feasibility constraints have zero violation. Using (7.5), and noting \(\|P\|\le1\), gives

\[
\boxed{
\operatorname{dist}(x,S)^2
\le C^2(F(x)-m_*),\qquad
C^2=K^2(2\overline H+E_0),
}
\tag{7.6}
\]

whenever \(F(x)-m_*\le E_0\). For (7.6), take an optimal lift of \(x\). Such a lift need not have small norm: the violation estimate and projection inequality do not assume a bound on latent coordinates.

Although \(K\) and \(C\) can be exponentially large numerically, their **binary encoding lengths are polynomial** in the input and KKT-witness lengths. KKT witnesses are acquired by rational QP/LP algorithms in polynomial time. Thus no missing condition-number oracle has been introduced.

## 8. Finish the whole future, including the selected equilibrium

Choose

\[
T_*=8C^2/\epsilon^2.
\tag{8.1}
\]

Equations (2.2) and (7.6) give

\[
\operatorname{dist}(u(T_*),S)\le\epsilon R/4.
\tag{8.2}
\]

Obtain a finite-horizon candidate \(v\) satisfying (6.1). Compute the metric projection \(s\) of \(v_N\) onto \(S\) by the convex QP

\[
\min_{y\in Y_*}\ \tfrac12\|Py-v_N\|^2,
\qquad s=Py_{\rm opt}.
\tag{8.3}
\]

This is done in the original latent variables, not by expanding the projected minimizer polyhedron. Since a distance-to-set function is 1-Lipschitz,

\[
\|v_N-s\|\le\epsilon R/2.
\tag{8.4}
\]

Change only the last endpoint of the polygonal candidate from \(v_N\) to \(s\), and extend it constantly after \(T_*\). On the last interval, the change is at most \(\|v_N-s\|\); on earlier intervals it is zero. Therefore the modified candidate has error at most \(3\epsilon R/4\) through \(T_*\). For \(t\ge T_*\), Fejér monotonicity relative to the *particular fixed minimizer* \(s\) gives

\[
\|u(t)-s\|
\le\|u(T_*)-s\|
\le\|u(T_*)-v_N\|+\|v_N-s\|
\le3\epsilon R/4.
\]

This proves (1.4), with slack. Letting \(t\to\infty\) proves (1.5).

Since \(\log(1+T_*)\) is polynomial in input length and \(\log(1/\epsilon)\), equation (5.2) makes the number of cells polynomial in input length and \(\epsilon^{-1}\). More explicitly,

\[
N=O\left(1+\epsilon^{-2}
\log\left(1+\frac{16 E_0C^2}{\epsilon^2R^2}\right)\right).
\tag{8.5}
\]

All original optimization variables, coefficients, matrix dimensions, mesh arithmetic, and requested state accuracy are charged. This completes the algorithmic theorem.

## 9. The all-future certificate is simpler than the construction bound

The large Hoffman constant is needed to prove a polynomial-size construction exists. A verifier need not recompute the future flow or use a tight convergence rate.

A returned finite primal–dual path with action upper bound \(J\), together with a certified minimizer \(s\), proves an all-future error bound

\[
\boxed{\sqrt{2J}+\|v_N-s\|.}
\tag{9.1}
\]

Here the last endpoint is changed to \(s\) and the path is extended constantly, exactly as above. All terms except the final square root are rational. Sufficient separate squared inequalities can be checked exactly; no floating-point proof of a strict inequality is necessary.

If the candidate already terminates at a minimizer, the finite action alone certifies the entire infinite future, because the constant tail has zero Fenchel gap.

### Robust observable and safety consequences

For any supplied vector \(c\), uniform state error \(\epsilon R\) implies

\[
\left|\sup_{t\ge0}c^Tu(t)-\max_{0\le i\le N}c^Tv_i\right|
\le\epsilon R\|c\|.
\tag{9.2}
\]

The maximum of a linear functional along a polygonal curve with constant tail occurs at a node. Thus rational linear safety inequalities can be certified for every future time when they hold on the nodes with the stated margin. A rational upper bound such as \(\|c\|_1\) can replace \(\|c\|_2\) for an entirely rational checker.

This is margin-based verification. It does not decide exact boundary contact. At an inverse-polynomial normalized margin it is polynomial-time; exponentially small margins still incur the charged reciprocal-accuracy cost.

## 10. Explicit counterexamples and representation failures

### 10.1 Finding a minimizer is not simulating relaxation

Take

\[
F(x,y)=\tfrac12x^2+\max(0,x-y),\qquad (x(0),y(0))=(1,0).
\]

This belongs to (1.1) via the three-variable energy \(q(x,y,z)=x^2/2+z\), constraints \(z\ge0\), \(z\ge x-y\), and observed coordinates \((x,y)\).

Before the hinge becomes inactive,

\[
x(t)=2e^{-t}-1,\qquad y(t)=t.
\]

Let \(\alpha\in(0,1)\) be the unique root

\[
2e^{-\alpha}=1+\alpha.
\]

After time \(\alpha\),

\[
x(t)=\alpha e^{-(t-\alpha)},\qquad y(t)=\alpha.
\]

Thus

\[
u_\infty=(0,\alpha),\qquad\alpha\approx0.374822528183623.
\]

But \(\arg\min F=\{(0,y):y\ge0\}\), and the metric projection of the initial point is \((0,0)\). Jumping straight to that minimizer destroys the selected endpoint.

For a sufficiently large implicit step \(h\), the first proximal state is exactly

\[
(x_1,y_1)=\left(\frac1{h+2},\frac1{h+2}\right).
\]

Every subsequent equal-sized proximal step keeps \(y_i=1/(h+2)\). Hence taking any fixed number of equal steps with \(h=T/N\) and sending \(T\to\infty\) converges to the wrong selected endpoint. The geometric time allocation is doing real work.

### 10.2 A naive latent dynamical lift is wrong

Let

\[
F(x)=\min_z\left\{\tfrac12(x-z)^2+\tfrac12z^2\right\}=x^2/4.
\]

The observed flow is \(x(t)=e^{-t/2}\) from \(x_0=1\). If instead both \(x,z\) follow the gradient of the lifted quadratic, starting at \((1,1/2)\), then

\[
x'=-x+z,\qquad z'=x-2z.
\]

The initial first derivative of \(x\) agrees, but the second derivative is \(1/2\), whereas that of \(e^{-t/2}\) is \(1/4\). The two systems are not the same. The primal–dual compilation preserves energy minimization rather than inventing latent dynamics.

### 10.3 Dissipation does not encode an unobserved forcing signal

For \(x'=u(t)\) on \([0,N]\), let the input be either identically zero or a unit pulse in one of \(N\) unit intervals. Assume access only through queries of the interval values. The terminal state is zero or one. Any randomized algorithm achieving error below \(1/3\) with success at least \(2/3\) on each input requires \(\Omega(N)\) expected queries in the worst case.

Indeed, couple runs with the same random tape. If interval \(j\) is not queried on the zero-input transcript, the transcript on pulse \(j\) is identical. Correctness on the two inputs forces the probability of querying \(j\) on the zero input to be at least \(1/3\). Summing over \(j\) gives expected queries at least \(N/3\). The pulse has bounded total input and bounded work, so those scalar budgets cannot remove the acquisition obstruction. If the pulse location is supplied explicitly in binary, that is a different, easier access model.

### 10.4 Persistent oscillation needs a different output representation

A rotation \(x'=Jx\), \(J^T=-J\), can retain unit norm forever. Backward Euler damps it, and an eventually constant output cannot uniformly approximate its trajectory to error below one. The example does NOT prove rotations cannot be fast-forwarded: their matrix-exponential representation is easy. It proves that the energy-clock polygonal/constant-tail representation cannot simply be transferred to persistent oscillatory systems. A general extension must preserve phase rather than count only dissipated energy.

## 11. Additional model-stability calculation and its boundary

Let \(F,G\ge0\) be proper convex energies with a common minimizer \(z\), zero minimum, and

\[
(1-\delta)F\le G\le(1+\delta)F,\qquad0<\delta<1.
\]

Let \(x,y\) be their flows with common initial state, \(\|x_0-z\|\le R\). Then

\[
\tfrac12\frac d{dt}\|x-y\|^2
\le F(y)-F(x)+G(x)-G(y)
\le\delta(F(x)+F(y)).
\]

The distance-energy budget gives \(\int F(x)\le R^2/2\) and \(\int F(y)\le R^2/[2(1-\delta)]\). Therefore

\[
\sup_{t\ge0}\|x(t)-y(t)\|^2
\le\delta\left(1+\frac1{1-\delta}\right)R^2.
\tag{11.1}
\]

This is an elementary consequence of established convex-flow inequalities, not a separately established original result. It shows what an energy-approximation certificate would buy. It does NOT provide an algorithm for acquiring such a global approximation or claim preservation of arbitrary future inputs.

Convexity cannot simply be dropped. For

\[
F(x)=(x^2-1)^2/4,\qquad G_\delta(x)=F(x)(1+\delta\tanh x),
\]

there is the same multiplicative comparison and the same zero minima. Starting at zero, the first gradient flow remains zero, while the second moves monotonically toward \(-1\): on \((-1,0)\), both terms in \(G'_\delta=F'(1+\delta\tanh x)+\delta F\operatorname{sech}^2x\) are positive. The small energy distortion does not prevent order-one trajectory separation.

## 12. What the physical pathway does and does not establish

The input class includes finite-dimensional convex models with quadratic stored energy, unilateral linear constraints, polyhedral dissipation terms represented by epigraph variables, and internal variables minimized quasistatically. Fixed rational positive-definite mass matrices can be incorporated by replacing the observed norm and endpoint quadratic by the associated Hilbert norm, and replacing the dual velocity by minus the mass matrix times the velocity. All constraints and objectives remain rational and convex; the tail constant obtains the corresponding explicit norm-conversion factor.

These are mathematical inclusion statements. They do not identify a validated model of a particular device, prove an adequate spatial mesh for a PDE, or establish experimentally useful parameter values. Inertial waves, turbulence, metastable nonconvex dynamics, evolving constitutive laws, unknown forcing, and nonlinear state-dependent metrics are outside the theorem.

The potential technological use is certified long-time behavior and margin-based safety of an already validated convex relaxation model, without resolving every physical time scale or every active regime. The unproved escalation is a comparably acquired certificate preserving oscillatory phase and nonconvex branch selection without hiding the original simulation or control problem inside an oracle.

## 13. Implemented evidence

`energy_clock.py` constructs the exact sparse rational action QP, verifies supplied candidates, checks rational PSD matrices and KKT minimizers, and computes the explicit crude tail constant. It does not contain a general QP optimizer.

`verify.py` implements a specialized proximal formula for the hinge example, rounds its states to a 32-bit dyadic grid in a way that preserves dual feasibility, and verifies the resulting action with exact rational arithmetic.

Executed result:

- 535 cells; terminal time approximately 21.09754613646308.
- The path terminates at the exact minimizer \((0,805659543/2147483648)\).
- The finite action upper bound is approximately \(9.5720456943098\times10^{-6}\).
- The exact rational comparison \(2J\le1/40000\) passes. Thus the candidate has error at most 0.005 for EVERY future time, not only at sampled times.
- The exact action implies a slightly smaller displayed bound of approximately 0.00437539614.
- A rational Taylor-series bracket places the true selected second coordinate near 0.374822528183623. The returned endpoint differs by less than 0.000341931742.
- An independent sparse-QP assembly check on an eight-cell prefix has 64 variables, 24 equalities and 32 inequalities; its exact objective matches the direct action calculation.
- A second exact compiler check covers latent elimination for \(F(x)=x^2/4\).
- Exact assertions also verify the fixed-large-step failure in Section 10.1.

The stored certificate can be replayed from `hinge_certificate.json.gz`. Approximate decimal displays are not used as proof of the stated rational inequalities. These finite computations do not prove historical novelty, validate a physical model, or replace the general proof.

## References and dependency status

[S1] R. H. Nochetto, G. Savaré, C. Verdi. *A posteriori error estimates for variable time-step discretizations of nonlinear evolution equations.* Communications on Pure and Applied Mathematics 53 (2000), 525–589. Author abstract consulted. Imported context: dissipation-based, variable-step backward-Euler error analysis, without extra regularity or adjacent-step-ratio requirements.

[S2] U. Stefanelli. *The Discrete Brezis-Ekeland Principle.* Journal of Convex Analysis 16(1) (2009), 71–87. DOI 10.68381/jca16004. Journal abstract consulted. Imported context: convex global-in-time functionals on discrete trajectories, the backward-Euler minimizer, and a posteriori error applications.

[S3] H. Antil, A. Kaltenbach, K. L. A. Kirk. *Duality-Based A Posteriori Error Identities for Subgradient Flows Based on the Brézis–Ekeland–Nayroles Principle.* arXiv:2608.17845v1, submitted 18 August 2026. Abstract consulted. Imported context: existing primal/dual variational error identities for time-dependent convex integral functionals. This overlap prevents claiming the action-error mechanism as a new primitive.

[S4] M. K. Kozlov, S. P. Tarasov, L. G. Khachiyan. *The polynomial solvability of convex quadratic programming.* Original Russian announcement, Doklady Akademii Nauk SSSR 248(5) (1979), 1049–1051; expanded/translated journal record, DOI 10.1016/0041-5553(80)90098-1. Standard polynomial-bit rational convex-QP optimization is the computational import. It was not reimplemented or formally verified here.

[S5] A. J. Hoffman. *On approximate solutions of systems of linear inequalities.* Journal of Research of the National Bureau of Standards 49(4) (1952), 263–265. DOI 10.6028/jres.049.027. NIST journal record consulted. The particular loose determinant bound needed here is proved in Section 7, rather than assumed to be an efficiently computed optimal Hoffman constant.

The Astra and OpenAI mathematical repositories were searched selectively for relevant gradient-flow/proximal material. No repository theorem is a premise of this result, and these targeted searches are not a claim to have cleared all repository or external prior art.
