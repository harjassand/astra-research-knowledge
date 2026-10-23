# Independent audit: continuum localization argument

This checks the stated one-dimensional Klein–Gordon model only. It is not a decay proof, a device validation, or a source/priority review.

## 1. Scalar periodic-state obstruction

For a time-periodic finite-energy solution of period $T$, let $\Omega=2\pi/T$ and write the temporal Fourier coefficients as $q_n,u_n(x)$. The field equation gives, distributionally,

\[
\left(-c^2\partial_x^2+\omega_c^2-(n\Omega)^2\right)u_n
=gq_n\delta_0.
\]

If $|n\Omega|>\omega_c$, the homogeneous spatial solutions are oscillatory on each half-line and cannot be in $L^2(\mathbb R)$. At equality they are affine and likewise cannot be in $L^2$. Thus finite field energy forces $u_n=0$, and the derivative jump then forces $q_n=0$. Since only finitely many integers satisfy $|n\Omega|<\omega_c$, $q$ has finite Fourier support.

More generally, at any frequency the source-free whole-line spatial equation has no nonzero $L^2$ solution: below cutoff it has only growing/decaying exponentials and no globally matched decaying mode; at cutoff it has affine solutions; above cutoff it has oscillatory solutions. If $N\ge1$ is the highest positive harmonic with $q_N\ne0$, the coefficient at $3N$ of $\gamma q^3$ is exactly $\gamma q_N^3\ne0$. But $q_{3N}=0$, and the field coefficient $u_{3N}$ solves the source-free equation, hence is zero. The oscillator equation at $3N$ is then impossible. If $q$ is constant, the static field minimizer gives the effective quadratic coefficient $\omega_0^2-g^2/(2c\omega_c)>0$; with $\gamma>0$ the only equilibrium is zero.

The argument is sound for finite-energy time-periodic energy-class solutions for which temporal Fourier coefficients and the point-source jump relation are valid. It uses the constant-coefficient full-line field with no bound modes and the strict positivity condition. It establishes nonexistence of nonconstant periodic states, not convergence to zero, a decay rate, or a storage-lifetime bound.

The quoted $a_3\simeq\gamma A^3/(32\Omega_{\rm lin}^2)$ is the usual leading Duffing estimate when the third-harmonic linear denominator is approximated by its weak-coupling value. In the coupled continuum problem, a quantitative coefficient at $3\Omega$ should use the frequency-dependent field self-energy (and outgoing boundary condition if $3\Omega>\omega_c$); the scaling $a_3=O(\gamma A^3)$ is the robust statement away from resonances and thresholds. The outgoing-wave amplitude and total-power factors in the note are consistent: for a prescribed complex point-force amplitude $F$, $u= iF e^{ik|x|}/(2c^2k)$ and the two-side mean flux is $\omega|F|^2/(4c^2k)$.

## 2. Exact circular vector state and angular momentum

Take $J(q_1,q_2)=(-q_2,q_1)$ and $R(\theta)=e^{\theta J}$. With

\[
\delta=(\omega_c^2-\Omega^2)^{1/2},\quad
a(\Omega)=\omega_0^2-\Omega^2-\frac{g^2}{2c\delta},\quad
A^2=-\frac{a(\Omega)}{\gamma},
\]

the profile $G_\delta(x)=e^{-\delta|x|/c}/(2c\delta)$ solves
$(-c^2\partial_x^2+\delta^2)G_\delta=\delta_0$. Its derivative jump is
$G'_\delta(0^+)-G'_\delta(0^-)=-1/c^2$, so the field point-source jump has the required sign and normalization. Substitution then verifies exactly

\[
q=A R(\Omega t)e_1,\quad p=\Omega Jq,\qquad
u(x,t)=gG_\delta(x)q(t),\quad v=\Omega Ju
\]

whenever $0<\Omega<\omega_c$ and $a(\Omega)<0$. The frequency function obeys
$a(0)>0$ by the strict Schur condition and
$a'(\Omega)=-2\Omega-g^2\Omega/(2c\delta^3)<0$; hence it has one root in $(0,\omega_c)$ and the stated nonlinear branch lies above that root. Its tail length is $c/\delta$.

The stated angular momentum is the Noether charge for simultaneous rotations,

\[
L=p\cdot Jq+\int_{\mathbb R}v\cdot Ju\,dx.
\]

Direct differentiation cancels the interaction torques:
the oscillator contributes $g\,u(0)\cdot Jq$, while the field source contributes $g\,q\cdot Ju(0)=-g\,u(0)\cdot Jq$; all central and gradient terms vanish under $z\cdot Jz=0$ and integration by parts. Thus $L$ is conserved for decaying finite-energy fields. On the circular state, $p\cdot Jq=\Omega A^2$, and

\[
\int |u|^2dx=\frac{g^2A^2}{4c\delta^3},\qquad
L=\Omega A^2\left(1+\frac{g^2}{4c\delta^3}\right).
\]

The normalization and field contribution are correct. The identity $H-\Omega L=-\gamma A^4/4$ follows from the square completion below. Along this stationary branch, differentiating the minimized value gives $d(H-\Omega L)/d\Omega=-L$, and therefore $dH/dL=\Omega$; $L$ is increasing for $0<\Omega<\omega_c$ on the nonzero branch.

## 3. Rotating-frame square completion and stability scope

For $F_\Omega=H-\Omega L$, first complete the two momentum squares:

\[
\frac{|p|^2}{2}-\Omega p\cdot Jq
=\frac{|p-\Omega Jq|^2}{2}-\frac{\Omega^2|q|^2}{2},
\]

and analogously for $(v,u)$. The field quadratic form becomes
$\frac12\int(c^2|u_x|^2+\delta^2|u|^2)\,dx$. For fixed $q$, its unique minimizer with the point source is $u_q=gG_\delta q$. Writing $w=u-u_q$, the cross terms cancel and the reduced $q$-potential is

\[
\frac{a(\Omega)}{2}|q|^2+\frac{\gamma}{4}|q|^4.
\]

When $a<0$, its minimum occurs at $|q|=A$ and has value $-\gamma A^4/4$. Therefore the exact identity is

\[
F_\Omega-F_{\min}
=\frac{|p-\Omega Jq|^2}{2}
+\frac12\int|v-\Omega Ju|^2dx
+\frac12\int(c^2|w_x|^2+\delta^2|w|^2)dx
+\frac{\gamma}{4}(|q|^2-A^2)^2.
\]

The coefficient, sign, and minimizer set (the phase orbit) check. For fixed $\Omega<\omega_c$, $\delta>0$ makes the $w$ term control its $H^1$ norm; the velocity terms control the corresponding momentum differences, while the final term controls radial departure from $|q|=A$. Although written as a quartic in $|q|^2-A^2$, it is quadratic to leading order in radial displacement $r-A$: $\frac{\gamma}{4}(r^2-A^2)^2=\gamma A^2(r-A)^2+O((r-A)^3)$. Thus it supplies a positive local radial gap, alongside the phase-neutral orbit. This is a Lyapunov/orbital-stability argument if the Hamiltonian flow is globally well posed in the stated energy space and conserves $H,L$. It is not attraction or asymptotic stability. The coercivity constants are not uniform as $\Omega\uparrow\omega_c$ because $\delta\downarrow0$.

## 4. Positive fourfold anisotropy

For an additional potential $\epsilon(q_1^4+q_2^4)/4$, the highest Fourier coefficient $a=(a_1,a_2)\in\mathbb C^2$ at harmonic $N$ must satisfy the zero coefficient equation at $3N$,

\[
C_i(a)=\gamma(a_1^2+a_2^2)a_i+\epsilon a_i^3=0.
\]

These are algebraic squares, not Hermitian norms. If exactly one component is nonzero, its equation is $(\gamma+\epsilon)a_i^3=0$, impossible for positive $\gamma,\epsilon$. If both are nonzero, division by each component and subtraction gives $\epsilon(a_1^2-a_2^2)=0$, hence $a_1^2=a_2^2$; either equation then gives $(2\gamma+\epsilon)a_1^2=0$, also impossible. So the same finite-Fourier argument rules out a nonconstant finite-energy periodic solution for every $\epsilon>0$ in this model. At $\epsilon=0$, nonzero complex null vectors such as $(1,-i)$ satisfy $a_1^2+a_2^2=0$ and encode the exact circular state.

The anisotropy leaves the linearized frequencies unchanged and is positive/convex for $\epsilon>0$. The result is an exact periodic-state fragility statement, not a uniform finite-time failure result: it does not exclude long-lived or nonperiodic states when $\epsilon$ is small.

The fixed arithmetic fixture in the frozen note also checks: $c=\omega_c=\gamma=1$, $\omega_0=\Omega=4/5$, $g=2/5$ gives $\delta=3/5$, $a=-2/15$, $A^2=2/15$, $u(0)=q/3$, tail length $5/3$, $L=256/2025$, $F_{\min}=-1/225$, and $H=979/10125$.

