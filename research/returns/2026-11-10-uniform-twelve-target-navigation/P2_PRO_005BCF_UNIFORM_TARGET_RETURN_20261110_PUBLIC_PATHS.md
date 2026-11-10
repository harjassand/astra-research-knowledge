# P2 completed return — uniform target, twelve body forces

Chat: https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677
User turn: 961071e0-5965-47db-b03b-74448d82fd72. Assistant final: 005bcf67-38a0-5bba-b9e6-6db7273d1e5c. Actual Pro displayed.

Exact held question: work/astra-renewed-pro-programmes-20261103/P2_FULL_UNIFORM_TARGET_TWELVE_BODY_FORCE_COMPILER_PRO_20261110.txt (SHA-256 4fe1bc0212c4c067edb6cd764fb026465c16cdefa7b7ad86bca09e6f6fd4d8de).

The native read was limited to a 20,000-character prefix, included below. The complete available response was copied via the response Copy control and TextEdit accessibility; its formatting is not asserted to be literal native-byte identity. Current-turn user-visible activity could not be fully extracted from the virtualized accessibility history; the chat retains it. The outputs panel showed no ZIP.

## Full response, copied via UI

**Yes, using the twelve-actuator erasure construction in your premises.** A uniform polynomial extension can be obtained by generating the target through shear conjugations and a fixed number of quadratic stages.
The useful change of representation is this:
	1	Every coordinate-plane mode with polarization perpendicular to that plane can be synthesized by **two fundamental shear conjugations**. The necessary shear impulses and inverse synthesis coefficients have polynomial bounds in the frequency cutoff.
	2	Those coordinate-plane modes generate every three-dimensional Fourier polarization in **at most two quadratic stages**, independently of the cutoff.
	3	Each conjugation is performed inside a loop whose complete **physical linearized Euler propagator is exactly the identity**. Polynomial estimates inside a loop therefore do not multiply over the number of loops.
	4	The nonlinear implementation uses short state translations. Its error estimates are uniform on an \(H^1\) ball and yield strong solutions for each actual disturbance; weak–strong uniqueness then supplies the quantifier over every Leray–Hopf realization.
I give the construction and its resource accounting below. The powers are deliberately generous. If \(p_0\) denotes the fixed exponent of the supplied erasure compiler, one admissible final choice is
\[ \boxed{p=10^{18}(p_0+1).} \]
A fixed integer \(A\) is obtained by the finite precomputation described in §9. The writing phase uses time polynomials of degree at most two, so the complete compiler retains degree at most three.
Throughout, write
\[ \kappa=2\pi,\qquad B(u,v)=P[(u\cdot\nabla)v],\qquad L_Fv=B(F,v)+B(v,F). \]
**1. The quantitative translation property**
The basic operation used below is a prescribed approximate translation of the state.
Suppose \(b_0\) is a known smooth, divergence-free, mean-zero field, \(G\) is a prescribed increment, and
\[ U(0)=b_0+e_0,\qquad \|e_0\|_{H^1}\le E. \]
For a requested tolerance \(\theta>0\), we construct a force and a rational duration \(d>0\) such that, writing
\[ e_1=U(d)-(b_0+G), \]
every admitted realization satisfies
\[ \boxed{ \|e_1\|_{H^1}\le \|e_0\|_{H^1}+\theta, \qquad \|e_1-e_0\|_2\le\theta. } \tag{1.1} \]
The force depends on \(G\), numerical bounds for \(b_0,E\), and the scalar inputs. It does not depend on \(e_0\) or the disturbance.
The two estimates have different purposes. The first controls repeated operations on an unknown \(H^1\) perturbation. The second preserves the small \(L^2\) error produced by erasure. No assertion of uniform smallness of \(e_1-e_0\) in \(H^1\) is needed.
The construction first establishes (1.1) for coordinate-plane passive modes and then closes it under two explicit quadratic stages.
**2. Polynomial stability of long fundamental-shear loops**
The following estimate is the analytic ingredient needed for long shear impulses.
**2.1 Statement**
Let
\[ Q=e^{-a_dL_{F_d}}\cdots e^{-a_1L_{F_1}},\qquad d\le4, \]
where each \(F_j\) is a fundamental shear, allowing a bounded linear combination of its sine and cosine partners. Set
\[ \mathfrak b=1+\max_j|a_j|. \]
There are fixed effectively computable constants \(c,C>0\) such that
\[ \|Q^{\pm1}\|_{H^m\to H^m}\le C\mathfrak b^{500}, \qquad |m|\le6, \tag{2.1} \]
and
\[ \operatorname{Re} \left\langle Q^{-1}\Delta Qz,(I-\Delta)z\right\rangle \le -c\mathfrak b^{-8}\|z\|_{H^2}^2 +C\mathfrak b^{500}\|z\|_{H^1}^2. \tag{2.2} \]
The crucial point in (2.2) is coercivity. It requires more than Sobolev bounds on \(Q\).
Here is a proof, including the steps that make the constants effective.
**2.2 The physical \(L^2\) estimate**
Temporarily use angular coordinates and take \(F=(\sin y,0,0)\). Fourier transform in \(x,z\), with frequencies \(k,l\), and put
\[ \alpha^2=k^2+l^2,\qquad A=-\partial_y^2+\alpha^2,\qquad H=I-A^{-1}. \]
For \(\alpha>0\), let \(v\) be the normal velocity component and define
\[ q=Av,\qquad \zeta=il\,u-ik\,w. \]
The Rayleigh–Squire reduction gives
\[ q_a+ik\sin y\,Hq=0, \tag{2.3} \]\[ \zeta_a+ik\sin y\,\zeta=-il\cos y\,v. \tag{2.4} \]
The velocity norm is
\[ \|U_{k,l}\|_2^2 = \alpha^{-2} \left(\|A^{-1/2}q\|_2^2+\|\zeta\|_2^2\right). \tag{2.5} \]
The usual reduction and the special stability of fundamental Kolmogorov flow on a cubic torus are also discussed by van Veen and Goto. The polynomial bounds below follow directly from (2.3)–(2.5). <u>[arxiv.org](arxiv.org/html/1512.02570v1?utm_source=chatgpt.com)</u>
For \(\alpha^2\ge2\),
\[ \tfrac12 I\le H\le I, \]
and \(\langle Hq,q\rangle\) is conserved. Differentiating once in \(y\) and using \(|k|\le\alpha\) gives
\[ \|A^{1/2}S_q(a)q_0\|_2 \le C(1+|a|)\|A^{1/2}q_0\|_2. \]
The identity
\[ S_q(a)^*=H S_q(-a)H^{-1} \]
then gives the same polynomial bound in the \(A^{-1/2}\) norm. Equation (2.4) adds at most one further power of \(1+|a|\).
For \(\alpha^2=1\), split \(q\) into its \(y\)-constant component and its orthogonal complement. The latter has the same positive \(H\)-energy. The constant component satisfies a scalar triangular equation, forced only by the controlled nonconstant component. In the case \(k\ne0\), \(l=0\), so no additional Squire coupling occurs.
For \(\alpha=0\), mean-zero divergence-free perturbations are stationary under the inviscid linearization. If constants are included, they produce only explicit linear growth.
Consequently,
\[ \|e^{-aL_F}\|_{L^2_\sigma\to L^2_\sigma} \le C(1+|a|)^2. \tag{2.6} \]
**2.3 Transport factorization on all vector fields**
Componentwise transport does not preserve divergence. To factor the propagator correctly, extend the generator to all vector fields by
\[ L_F^{\rm ext}=F\cdot\nabla+R_F, \]
where
\[ R_Fu = P[(u\cdot\nabla)F] -\nabla\Delta^{-1}\partial_j[(\partial_iF_j)u_i]. \tag{2.7} \]
This agrees with the physical generator on divergence-free fields, and
\[ \operatorname{div}(L_F^{\rm ext}u) =F\cdot\nabla\operatorname{div}u. \tag{2.8} \]
The gradient part therefore has a polynomial \(L^2\) bound, obtained from explicit shear transport in \(H^{-1}\). Its forcing of the solenoidal part is order zero:
\[ PL_F^{\rm ext}\nabla\psi = P\!\left[ \bigl(\nabla F-(\nabla F)^T\bigr)\nabla\psi \right]. \]
Combining this with (2.6) gives
\[ \|Q_F^{\rm ext}(a)\|_{2\to2} \le C(1+|a|)^4. \tag{2.9} \]
Let \(T(a)\) be componentwise shear transport and write
\[ Q_F^{\rm ext}(a)=T(a)K(a). \]
Then
\[ K_a=-\widetilde R(a)K,\qquad \widetilde R(a)=T(a)^{-1}R_FT(a), \]
and, importantly,
\[ K(a)K(r)^{-1} =T(a)^{-1}Q_F^{\rm ext}(a-r)T(r). \]
Thus its \(L^2\) norm is polynomial by (2.9), without an exponential Gronwall estimate.
**2.4 Effective commutator bounds**
For one fundamental shear, \(R_F\) is a finite sum of Fourier shifts composed with Riesz multipliers. Conjugating a coordinate derivative by \(T(a)\) produces either a coordinate derivative or
\[ \partial_y+a\cos y\,\partial_x. \]
Since \(\partial_x\) commutes with \(R_F\),
\[ [\cos y\,\partial_x,R_F]=[\cos y,R_F]\partial_x. \]
Repeated commutators produce finite differences of degree-zero Riesz symbols, multiplied by powers of \(k_x\). A \(j\)-fold finite difference has order \(-j\), which cancels those powers.
For each \(r\le6\), this gives
\[ \|\operatorname{ad}_{\partial}^{\,r}\widetilde R(a)\|_{2\to2} \le C_r\mathfrak b^r. \]
Duhamel’s formula, using the polynomial \(K\)-propagator bound, yields
\[ \|\operatorname{ad}_{\partial}^{\,r}K(a)\|_{2\to2} \le C_r\mathfrak b^{4+6r}. \tag{2.10} \]
Adjoint commutators give the corresponding negative Sobolev bounds.
For scalar multiplication by \(\phi\), the elementary Riesz-symbol difference estimate gives
\[ \|[\phi,R_F]\|_{H^{-1}\to L^2} \le C\|\phi\|_{H^5}. \]
After transport conjugation and Duhamel,
\[ \|[\phi,K]\|_{H^{-1}\to L^2} \le C\mathfrak b^{21}\|\phi\|_{H^5}. \tag{2.11} \]
All constants here can be computed by differentiating rational Fourier symbols through a fixed order, using their homogeneous derivative bounds away from zero, and checking finitely many shifted small frequencies.
**2.5 Conjugated viscosity**
Put
\[ A_T=T^{-1}\Delta T. \]
It is a scalar divergence-form elliptic operator, applied componentwise. For one shear its ellipticity is at least \(c\mathfrak b^{-2}\), and its coefficient derivatives have polynomial bounds.
Expand
\[ [A_T,K] = \sum a_{ij}[\partial_i\partial_j,K] +\sum[a_{ij},K]\partial_i\partial_j +\text{first-order terms}. \]
The derivative commutators use (2.10). The coefficient commutators use (2.11), together with
\[ \partial_i\partial_j:H^1\to H^{-1}. \]
Hence
\[ [A_T,K]:H^1\to L^2 \]
has polynomial norm, and
\[ Q^{-1}\Delta Q=A_T+K^{-1}[A_T,K]. \tag{2.12} \]
Integration by parts for \(A_T\), followed by Young’s inequality for the first-order remainder, gives the required \(H^1\) Gårding estimate.
For a product of \(d\) factors, retain a scalar second-order part and an \(H^1\to L^2\) remainder. A sufficient set of exponents is
\[ \begin{array}{c|c} \text{Quantity}&\text{Exponent of }\mathfrak b\\ \hline H^{\pm6}\text{ propagator norm}&46d\\ H^1\to L^2\text{ viscosity remainder}&25+15d\\ \text{Gårding lower-order coefficient}&50+32d\\ \text{inverse ellipticity}&2d. \end{array} \]
For \(d\le4\), these imply (2.1)–(2.2). This proves polynomial viscous stability inside the loops used below.
**3. Uniform synthesis of passive coordinate-plane modes**
Consider a plane with angular coordinates \(x,y\), and let \(e_\perp\) be its perpendicular coordinate direction. On fields
\[ e_\perp\phi(x,y), \]
the physical linearized Euler evolution under either in-plane shear is exactly scalar transport.
Define
\[ (T_\theta\phi)(x,y) =\phi(x,y+A\sin(x+\theta)), \]\[ (S_\psi\phi)(x,y) =\phi(x+B\sin(y+\psi),y). \]
Starting with the fundamental seed \(g=e^{iy}\),
\[ S_\psi T_\theta g = e^{\,iy+iA\sin(x+B\sin(y+\psi)+\theta)}. \tag{3.1} \]
**3.1 Polynomially conditioned Bessel coefficients**
For \(n\ge0\), set
\[ K_n=8(n+1)^2+\frac n2+\frac14,\qquad X_n=\pi K_n. \]
Then
\[ \boxed{J_n(X_n)\ge \frac1{16(n+1)}.} \tag{3.2} \]
For completeness, let
\[ u_n(x)=\sqrt{\frac{\pi x}{2}}J_n(x). \]
The Bessel equation becomes
\[ u_n''+u_n=\frac{n^2-\frac14}{x^2}u_n. \]
Using the classical large-argument asymptotic as the boundary condition at infinity gives
\[ u_n(x)= \cos\!\left(x-\frac{\pi n}{2}-\frac\pi4\right) + \int_x^\infty \sin(t-x)\frac{n^2-\frac14}{t^2}u_n(t)\,dt. \]
Iteration bounds the error from the cosine by
\[ \exp\!\left(\frac{|n^2-\frac14|}{x}\right)-1. \]
At \(x=X_n\), the cosine is exactly \(1\), while
\[ 24(n+1)^2\le X_n\le36(n+1)^2. \]
This proves (3.2). The classical asymptotic and its differentiated form are recorded in DLMF §10.17; the displayed Volterra estimate supplies the uniform bound used here. <u>[dlmf.nist.gov](dlmf.nist.gov/10.17?utm_source=chatgpt.com)</u>
The corresponding physical shear impulse is rational:
\[ X_n/\kappa=K_n/2. \tag{3.3} \]
**3.2 Two phase projections**
For a desired frequency \((m,n)\), \(m\ne0\), put
\[ q=n-1,\qquad A=X_{|m|}, \qquad B= \begin{cases} X_{|q|}/m,&q\ne0,\\ 0,&q=0. \end{cases} \]
The Jacobi–Anger expansion gives
\[ \frac1{(2\pi)^2} \int\!\!\int e^{-i(m\theta+q\psi)}S_\psi T_\theta g \,d\theta\,d\psi = d_{m,n}e^{i(mx+ny)}, \tag{3.4} \]
where
\[ d_{m,n}=J_m(A)J_q(mB), \]
with the second factor equal to \(1\) when \(q=0\). This is a direct use of the Bessel generating function. <u>[dlmf.nist.gov](dlmf.nist.gov/10.12?utm_source=chatgpt.com)</u>
For \(|m|,|n|\le N\), writing \(P_N=N+2\),
\[ |d_{m,n}|^{-1}\le256P_N^2, \qquad |A|+|B|\le C P_N^2. \tag{3.5} \]
The physical impulses are rational signed multiples of
\[ K_{|m|}/2,\qquad K_{|q|}/(2m). \]
Their signs are chosen to implement the displayed pullbacks.
If \(m=0,n\ne0\), exchange the plane coordinates.
**3.3 Finite phase quadrature**
Use the uniform grid
\[ \theta_a=2\pi a/Q,\qquad \psi_b=2\pi b/Q. \]
The discrete average has the exact alias expansion
\[ \sum_{\substack{p\equiv m\pmod Q\\ \ell\equiv q\pmod Q}} J_p(A)J_\ell(pB)e^{i(px+(1+\ell)y)}. \tag{3.6} \]
For each fixed \(r,s\), \(s\ge1\), differentiation of \(e^{iz\sin\theta}\) and Parseval give
\[ \sum_\ell(1+|\ell|)^{2j}|J_\ell(z)|^2 \le c_j(1+|z|)^{2j}, \qquad c_j=2^{2j+1}(j!)^2. \]
Applying this to the two alias classes in (3.6) yields
\[ \|\Phi_{m,n,Q}-e^{i(mx+ny)}\|_{H^r} \le C_{r,s}P_N^{4r+2s+2}Q^{-s}, \qquad Q\ge4P_N. \tag{3.7} \]
The constants are explicit finite combinations of factorials and powers. For example, with
\[ K_r'=2\cdot260^r(1+c_r), \]
one may use
\[ C_{r,s} = 256\cdot2^s c_{r+s} \left(K_r'37^{2r+s}+260^r37^{r+s}\right). \]
Taking real and imaginary parts uses only fundamental real sine and cosine seeds. A unit real mode requires at most \(2Q^2\) conjugated seeds, and their coefficient sum satisfies
\[ \sum|\text{synthesis coefficients}|\le512P_N^2. \tag{3.8} \]
In particular, increasing \(Q\) does not enlarge that sum.
For the compiler, use the fixed order \(r=10\). The dynamical estimates need only \(H^6\), but the stronger synthesis accuracy costs no change of principle.
**3.4 Rational computation**
Replace
\[ \sin(x+\theta) =\cos\theta\sin x+\sin\theta\cos x \]
by rational approximations to its two coefficients. This field remains exactly in the prescribed twelve-dimensional force space.
The rounded shear and its inverse use the **same stored rational coefficients**. Their homogeneous physical propagators therefore cancel exactly.
All required numbers are computable with certified rational arithmetic. For example,
\[ J_n(X_n) = \int_0^1 \cos\!\left(X_n\sin(\pi t)-n\pi t\right)\,dt, \tag{3.9} \]
and the integrand has derivative bounded by \(C(N+2)^2\). A rectangle rule gives a polynomial evaluation procedure at any inverse-polynomial requested accuracy. The integral formula is DLMF 10.9.2. <u>[dlmf.nist.gov](dlmf.nist.gov/10.9?utm_source=chatgpt.com)</u>
Use rational arctangent series for \(\pi\), Taylor bounds for sine and cosine, and interval arithmetic for reciprocals. Bound (3.5) supplies a certified nonzero denominator. No special-function or norm oracle is used.
Weights are stored with their \(Q^{-2}\) normalization, so their rounding errors also obey a coefficient-sum bound.
**4. Physical implementation of a passive translation**
This section converts the spatial synthesis into an operation on the actual nonlinear equation.
**4.1 One return loop**
Let a desired conjugated seed be \(SG\), where \(S\) is a product of two shear propagators.
Perform the following sequence:
	1	The inverse shear word \(S^{-1}\).
	2	A low-mode seed injection with prescribed impulse.
	3	The shear word \(S\).
Every shear segment uses a carrier
\[ w(t)=\frac{a}{\ell}\, q\!\left(\frac{t-t_0}{\ell}\right)F, \qquad q(z)=6z(1-z). \tag{4.1} \]
Its impulse is \(a\), and \(w\) vanishes at both ends. Only one shear orientation is active at a time, so \(B(w,w)=0\).
The ideal physical force is
\[ f=w_t-\nu\Delta w+g, \tag{4.2} \]
where \(g\) is the fundamental seed injection, supported where \(w=0\). Since
\[ -\Delta F=\kappa^2F, \]
rationally approximating \(\kappa^2\) makes every coefficient of (4.2) an ordinary rational polynomial of degree at most two.
Let \(Q(t)\) be the inviscid physical propagator generated by \(w\), starting at \(I\). At the end of the loop,
\[ Q=I \tag{4.3} \]
exactly.
**4.2 The reference and its residual**
For a known starting background \(b_0\), define the analysis reference
\[ \beta_t+L_w\beta=g,\qquad \beta(0)=b_0. \tag{4.4} \]
At a loop endpoint, \(\beta\) equals its starting value plus the corresponding conjugated seed increment.
The reference for the nonlinear equation is \(w+\beta\). Its residual is exactly
\[ \nu\Delta\beta-B(\beta,\beta), \tag{4.5} \]
apart from the paid rational approximation of the carrier force.
Put
\[ U=w+\beta+Qz. \]
Then
\[ \begin{aligned} z_t={}& \nu Q^{-1}\Delta Qz -Q^{-1}L_\beta Qz -Q^{-1}B(Qz,Qz)\\ &+Q^{-1}\!\left(\nu\Delta\beta-B(\beta,\beta) +h+\text{rounding error}\right). \end{aligned} \tag{4.6} \]
The reference \(\beta\) need not be computed by the compiler. Its equation defines an explicit linear-control reference for the proof, and the bounds on it follow from the shear estimates and the synthesis coefficient sums. The output force is still precisely (4.2).
**4.3 A concrete numerical envelope**
Let \(H\) be an integer containing fixed multiples of all the following bounds:
	•	the frequency cutoff, mode count and coefficient sum;
	•	\(\|b_0\|_{H^6}\), the error-radius bound \(E\), and \(\theta^{-1}\);
	•	\(\nu^{-1}\) and the reciprocal allotted time;
	•	the fixed constants in §§2–3.
Choose
\[ Q_{\rm grid}=H^{100},\qquad d_{\rm leaf}=H^{-50000}. \tag{4.7} \]
Use coefficient precision at least \(H^{-1000}\), and a \(\kappa^2\)-enclosure sufficiently narrow to give carrier-force error at most \(H^{-200000}\) times the carrier amplitude.
There are at most \(CH^{201}\) loops. Their impulses are bounded by \(CH^2\). Inside any loop, the sharper exponents in §2 give, after enlarging the fixed lower bound for \(H\),
\[ \|Q^{\pm1}\|_{H^m\to H^m}\le H^{1000}, \qquad |m|\le6, \tag{4.8} \]
and the transformed viscosity has coercivity at least
\[ \mu=\nu H^{-32}. \tag{4.9} \]
The reference satisfies
\[ \sup_t\|\beta(t)\|_{H^6}\le H^{1030}. \tag{4.10} \]
The exponent in (4.10) includes transport of the existing general three-dimensional background. It is not obtained solely from the passive scalar formula.
For
\[ \mathcal E=\|z\|_{H^1}^2,\qquad Z=\|z\|_{H^2}, \]
the Gårding estimate, the usual \(H^1\)-\(H^2\) Navier–Stokes estimate, and Young’s inequality give the coarse bound
\[ \mathcal E'+\mu Z^2 \le H^{13000}(1+\mathcal E+\mathcal E^3), \tag{4.11} \]
for disturbances and carrier-force rounding error whose combined \(L^\infty L^2\) norm is at most two.
Starting with \(\mathcal E(0)\le H^2\), (4.7) closes the bootstrap with a large margin. Integration of (4.6) also gives
\[ \|z(d_{\rm leaf})-z(0)\|_2 \le H^{5000}\left( d_{\rm leaf}^{1/2} +d_{\rm leaf}^{3/4} +d_{\rm leaf} \right). \tag{4.12} \]
The viscosity contribution uses the integrated \(H^2\) bound from (4.11); the quadratic contribution uses Hölder’s inequality with that same bound.
Both (4.11) and (4.12) give errors much smaller than \(\theta\), since \(H\ge\theta^{-1}\).
At every loop boundary \(Q=I\). Thus the transformed perturbation is continuous across resets, and the energy inequalities accumulate over total elapsed time. There is no product of one polynomial loss per quadrature sample.
After accounting for the finite synthesis error and rebasing to the ideal Fourier increment \(G\), this proves (1.1) for passive planar increments.
**4.4 Leaf resources**
Divide the leaf duration into equal rational segment lengths. The inverse segment width is at most \(CH^{50201}\). Formula (4.1) then gives
\[ \sup_t\|f(t)\|_{W^{1,\infty}}\le H^{102000}. \]
All other numerical resources fit within \(H^{10^6}\). Bit operations, output bits and working memory fit within
\[ C(L+H)^{10^6}. \tag{4.13} \]
The distinction between \(L\) and \(H\) is retained: large input denominators may enlarge arithmetic work, while the physical bounds depend on numerical envelopes.
**5. All Fourier polarizations in two quadratic stages**
Define
\[ \mathcal B(u,v)=\kappa^{-1}B(u,v). \]
Its Fourier algebra has rational coefficients.
Let level zero consist of the passive modes
\[ e_i\cos(\kappa k\cdot x),\quad e_i\sin(\kappa k\cdot x), \qquad k_i=0. \]
For \(a\perp m\), \(b\perp n\), \(k=m+n\), put
\[ C=P_k\bigl((a\cdot n)b+(b\cdot m)a\bigr). \]
Writing \(\mathcal B(u)=\mathcal B(u,u)\), direct trigonometric expansion gives
\[ C\cos(\kappa k\cdot x) = \mathcal B(a\cos m+b\sin n) +\mathcal B(b\cos n+a\sin m), \tag{5.1} \]
and
\[ C\sin(\kappa k\cdot x) = \mathcal B(a\sin m+b\sin n) +\mathcal B(a\cos m-b\cos n). \tag{5.2} \]
Here the abbreviated phases include \(\kappa\). Difference-frequency terms cancel. Replacing one polarization by its negative reverses the quadratic direction.
**Three nonzero coordinates**
For \(k=(a,b,c)\), define
\[ t_{12}=(b,a,0),\quad t_{13}=(c,0,a),\quad t_{23}=(0,c,b),\qquad C_{ij}=P_kt_{ij}. \]
Each \(C_{ij}\) is obtained at level one from passive modes: use frequencies
\[ m=k-k_i e_i,\qquad n=k_i e_i \]
and polarizations \(e_i,e_j\).
The determinants
\[ a(a^2-b^2-c^2),\qquad b(a^2-b^2+c^2),\qquad c(c^2-a^2-b^2) \tag{5.3} \]
cannot all vanish when \(abc\ne0\).
Choose a pair \(t,u\) with nonzero
\[ D=k\cdot(t\times u)\in\mathbb Z. \]
For any rational \(v\perp k\),
\[ v=\alpha P_kt+\beta P_ku, \]
where
\[ \alpha=\frac{k\cdot(v\times u)}D,\qquad \beta=\frac{k\cdot(t\times v)}D. \tag{5.4} \]
Because \(|D|\ge1\),
\[ |\alpha|+|\beta|\le CN^2|v| \]
for \(|k|\le N\).
**Two nonzero coordinates**
Take \(k=(a,b,0)\), \(ab\ne0\). The \(e_3\) polarization is passive, and
\[ C_{12} = \frac{b^2-a^2}{a^2+b^2}(b,-a,0). \tag{5.5} \]
This supplies the other polarization when \(a^2\ne b^2\).
For the exceptional case \(a^2=b^2\), put
\[ \ell=(a,b,1),\qquad a_\ell=(1,0,-a). \]
This is a level-one polarization:
\[ a_\ell = \left(1-\frac{2a^2}{a^2+b^2-1}\right)C_{13}(\ell) -\frac{2ab}{a^2+b^2-1}C_{23}(\ell). \tag{5.6} \]
The denominator is a positive integer and the two coefficients have magnitude at most two.
Interact \(a_\ell\) at \(\ell\) with \(e_1\) at \(-e_3\). The output at \(k\) is
\[ P_k(2a,0,-a^2)=(a,-b,-a^2). \]
Adding the passive \(a^2e_3\) direction gives the missing polarization
\[ (a,-b,0). \tag{5.7} \]
This uses level two.
Axial frequencies already have both transverse passive polarizations. Coordinate permutations finish the construction.
Thus every target mode has a rational certificate of fixed size and depth at most two. Source frequencies are bounded by \(N+1\); intermediate sum and difference frequencies remain \(O(N)\). Coefficient bounds are polynomial in \(N\). A convenient aggregate bound is
\[ \sum |\text{certificate coefficients}| \le CM(N+2)^4. \tag{5.8} \]
This is an explicit finite algebraic construction; no saturation search of growing depth is required.
**6. Implementing a quadratic stage in the nonlinear equation**
Suppose translations by two pure Fourier fields \(a,b\) are available. Each has zero self-interaction:
\[ B(a,a)=B(b,b)=0. \]
Consequently, for \(\xi=a+b\) or \(a-b\), the quadratic direction can have either sign.
To create a prescribed multiple of \(\mathcal B(\xi,\xi)\), perform:
	1	Translation by \(A\xi\).
	2	An unforced interval of length \(h\).
	3	Translation by \(-A\xi\).
The holding time is fixed from numerical bounds:
\[ h=H^{-1000}. \tag{6.1} \]
Choose a rational approximation to
\[ A=\sqrt{\frac{|\lambda|}{\kappa h}}, \tag{6.2} \]
with the sign of the interaction selected through \(\xi=a\pm b\).
**No inverse of a target coefficient is used.** Arbitrarily small rational \(\lambda\) gives a small amplitude in a prescribed slot.
During the hold use the reference
\[ b(t)=b_0+A\xi-tA^2B(\xi,\xi). \tag{6.3} \]
Let
\[ y(t)=b_0-tA^2B(\xi,\xi). \]
Its exact residual under zero applied force is
\[ \begin{aligned} R &=b_t-\nu\Delta b+B(b,b)\\ &=A L_\xi y+B(y,y)-\nu A\Delta\xi-\nu\Delta y. \end{aligned} \tag{6.4} \]
Since \(hA^2\) is bounded by the prescribed coefficient, \(y\) has a polynomial bound independent of the small holding time. Hence
\[ \|R\|_{H^1}\le \operatorname{poly}(H)(1+A). \tag{6.5} \]
For the perturbation \(v=U-b\), direct integration by parts gives
\[ |\langle L_bv,(I-\Delta)v\rangle| \le C\|b\|_{W^{2,\infty}}\|v\|_{H^1}^2. \tag{6.6} \]
The smooth residual is estimated through
\[ \int_0^h\|R(t)\|_{H^1}\,dt. \]
Both this integral and the integrated coefficient in (6.6) are bounded by a polynomial times
\[ h+hA. \tag{6.7} \]
They become small with \(h\), while \(hA^2\) retains the desired quadratic increment.
For the stated envelope, \(A\le H^{501}\), the temporary known backgrounds are bounded by \(H^{600}\), and one can use
\[ \int_0^h\|R\|_{H^1}\,dt\le CH^{-495}, \qquad \int_0^h\|b\|_{W^{2,\infty}}\,dt\le CH^{-498}. \tag{6.8} \]
The perturbation’s \(H^1\) estimate and integrated equation then give (1.1), after allocating tolerances to the insertion, hold and removal.
At each completed operation, rebase the reference to the **ideal finite Fourier increment**. Synthesis errors enter the \(H^1\) perturbation. Subsequent algebraic interactions are formed from the exact rational Fourier certificate, so there is no uncontrolled differentiation of accumulated approximation errors.
**Fixed-depth resource recurrence**
For a child translation use the envelope
\[ H_{\rm child}=(CH)^{1000}. \]
It contains the temporary backgrounds, insertion amplitudes and allocated reciprocal tolerances.
A sufficient resource recurrence is
\[ q_0=10^6,\qquad q_{j+1}=2000q_j. \tag{6.9} \]
Thus
\[ q_2=4\cdot10^{12}. \tag{6.10} \]
The two stages in §5 therefore preserve polynomial resources with one fixed exponent.
Across different completed target modes, the reference returns to a partial target sum. The large temporary envelope is used down the fixed recursion tree; it is not repeatedly exponentiated across the target’s modes.
**7. The complete compiler**
Here are the actual input-dependent steps.
**7.1 Canonicalize and truncate**
Compute
\[ N=\left\lceil\frac{16M}{\epsilon}\right\rceil. \]
Canonicalize signs of wavevectors, combine duplicate retained modes exactly, and discard modes with \(|k|>N\). Let the result be \(V_N\).
The promised \(H^1\) bound gives
\[ \|V-V_N\|_2\le\epsilon/8. \tag{7.1} \]
There are at most \(C N^3\) retained real sine/cosine components.
Large encoded wavevectors are tested by binary integer arithmetic and discarded directly. There is no enumeration up to their magnitude.
Let \(J\) be the number of nonzero retained real components.
**7.2 Erase and preserve a small state during waiting**
Use the supplied erasure construction in its active-time form. Its existing \(H^1\) bootstrap gives, at the active endpoint,
\[ \|U\|_{H^1}\le K,\qquad K=5M+1. \tag{7.2} \]
Indeed, its perturbation is bounded by \(4M\), its excursions vanish at the endpoint, and its endpoint reference correction can be bounded by one. This bound is independent of the erasure accuracy.
Choose the rational number
\[ e=\min\left\{\frac{\epsilon}{32},\frac{\nu^2}{CK}\right\}, \tag{7.3} \]
where the fixed \(C\) includes the constants below. Invoke erasure with accuracy \(e/4\) and allotted time \(\tau/2\).
If \(\eta_{\rm erase}\) is its returned budget, set
\[ \boxed{ \eta=\min\{\eta_{\rm erase},\,e/8,\,1/8\}. } \tag{7.4} \]
During an unforced waiting interval of length at most one,
\[ \|U(t)\|_2\le e/2. \]
Bootstrap \(\|U(t)\|_{H^1}\le2K\). Interpolation gives
\[ \|U(t)\|_3\le C\sqrt{eK}. \]
By (7.3), the enstrophy estimate absorbs the nonlinear term:
\[ |\langle B(U,U),\Delta U\rangle| \le C\|U\|_3\|\Delta U\|_2^2 \le \frac{\nu}{4}\|\Delta U\|_2^2. \]
The disturbance contributes
\[ \frac{\nu}{4}\|\Delta U\|_2^2+C\eta^2/\nu. \]
This closes the bootstrap and gives
\[ \|U(t)\|_{H^1}\le2K \tag{7.5} \]
throughout the waiting interval.
**7.3 Compile the writing phase**
Set
\[ \rho= 2+\lceil M\rceil+\lceil\nu^{-1}\rceil +\lceil\tau^{-1}\rceil+\lceil\epsilon^{-1}\rceil, \]
and independently define the per-component tolerance
\[ \theta= \frac{\epsilon}{100(J+1)(2K+1)}. \tag{7.6} \]
Then choose the integer top-level envelope
\[ H_{\rm top}=(C\rho)^{1000}. \tag{7.7} \]
Since \(N\le C\rho^2\), the certificate bounds, all ideal partial-background bounds, \(2K\), and \(\theta^{-1}\) fit inside this envelope.
For each retained real component of \(V_N\):
	1	Compute its depth-at-most-two rational certificate from §5.
	2	Apply the translation construction of §§4–6.
	3	Allocate its total error budget \(\theta\) among its finitely many child operations.
	4	Rebase to the ideal partial target sum.
All slot lengths are chosen from the numerical envelopes. Tiny target coefficients affect amplitudes, never inverse time scales.
Let \(d_{\rm write}\) be the exact sum of the rational durations produced. The choices above give
\[ d_{\rm write}\le \tau/4. \tag{7.8} \]
Concatenate the actual durations without padding inside a translation or quadratic operation.
Place this phase on
\[ [\tau-d_{\rm write},\tau]. \]
All unused time is assigned to the preceding small-state waiting interval.
If \(J=0\), the writing phase can be omitted.
**7.4 Endpoint estimate**
At the start of writing, the reference is zero, the actual state has \(L^2\) norm at most \(e/2\), and its \(H^1\) norm is at most \(2K\).
Applying (1.1) successively gives
\[ \|U(\tau)-V_N\|_2 \le e/2+J\theta \le \epsilon/32+\epsilon/100. \tag{7.9} \]
Together with (7.1),
\[ \boxed{\|U(\tau)-V\|_2<\epsilon.} \tag{7.10} \]
The complete force is fixed before execution. Every reference background in the construction is a known partial target expression; none depends on the actual initial state or disturbance.
**8. Every Leray–Hopf realization and the endpoint trace**
The estimates above first apply on the local strong-existence interval for the actual force and the actual \(L^\infty_tL^2_x\) disturbance.
During each leaf, the transformed \(H^1\) estimate prevents loss of regularity. During each hold, (6.4)–(6.8) do the same. The waiting estimate supplies continuation between erasure and writing. Thus, for every admitted initial state and disturbance, a strong solution exists throughout the constructed evolution.
Weak–strong uniqueness then identifies every corresponding Leray–Hopf realization with that solution. The local \(H^1\) theory and weak–strong uniqueness are standard; the estimates here provide the needed continuation bounds for these particular large controls. <u>[math.fau.de](math.fau.de/wp-content/uploads/2023/03/wiedemann-NSE-final.pdf?utm_source=chatgpt.com)</u>
At \(\tau\), the strong solution has a continuous \(H^1\), hence \(L^2\), trace. Its value equals the requested one-sided energy trace. Therefore (7.10) holds with exactly the endpoint convention in the question.
**9. Finite precomputation and final resource bounds**
It remains to make the fixed constants and computational accounting explicit.
**9.1 Fixed precomputation**
Perform once the following finite rational bound computation:
	1	Retain the supplied erasure program, its fixed preprocessing tables, \(A_0,p_0\), and its active-endpoint \(H^1\) certificate.
	2	Compute Sobolev, product and interpolation upper bounds through the fixed orders used above. Fourier-shell estimates such as\[ \#\{k:|k|_\infty=m\}\le26m^2 \]turn the required convergent sums into rational upper bounds.
	3	Expand the shear-generator commutators through order six. Differentiate the rational Riesz symbols to the required fixed order; use their homogeneous derivative bounds outside the shifted-zero region and evaluate the remaining finite integer frequencies directly.
	4	Differentiate the explicit compositions of at most four shear maps through order seven to bound the scalar viscosity coefficients. These are finite chain-rule calculations.
	5	Compute the Bessel alias constants through the fixed synthesis order ten, and bound phase sensitivity by finite differentiation of (3.1).
	6	Compute rational upper bounds for the finite algebraic formulas (5.1)–(5.7) and the energy estimates.
No supremum or PDE oracle occurs in these steps. Fourier-symbol bounds use explicit rational formulas; spatial derivative bounds use finite differentiation and \(|\sin|,|\cos|\le1\).
Let \(C_{\rm pre}\) be an integer exceeding the sum of these majorants, the erasure constants, and the recorded operation count, storage and output size of this fixed preprocessing. Define, for example,
\[ C=(2C_{\rm pre})^{10^6}. \tag{9.1} \]
This fixes the constant used in the envelope choices. The precomputation terminates independently of all variable inputs, and its cost is included in the final constant.
**9.2 Digital resources**
After canonicalization there are \(O(N^3)\) target components. Each has a fixed-depth certificate. The leaf arithmetic consists of rational operations, certified elementary-function approximations, and explicitly bounded loops.
The writing cost is bounded by a fixed polynomial with exponent covered by
\[ 1000q_2+10 <10^{18}. \]
The erasure call uses \(e^{-1}\le C R^3\), so its original exponent is enlarged only by a fixed factor.
With
\[ p=10^{18}(p_0+1), \qquad A=(2C)^{p^2}, \tag{9.2} \]
all compiler bit operations, memory bits, total output bits, interval counts, polynomial degrees and individual rational bit lengths are bounded by
\[ A(L+R)^p. \tag{9.3} \]
Exact coalescing of a long rational target list is charged through \(L\). Subsequent numerical envelopes use the promised \(H^1\) bound and the cutoff, so large encoded denominators do not enlarge physical resource bounds.
**9.3 Physical resources**
For a leaf, the peak force is bounded by \(H^{102000}\). The fixed-depth recurrence (6.9), the top-level envelope (7.7), and the supplied erasure bound imply
\[ \sup_{0\le t\le\tau}\|f(t)\|_{W^{1,\infty}} \le AR^p. \tag{9.4} \]
Since \(\tau\le1\),
\[ \int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt \le AR^p. \tag{9.5} \]
The erasure budget and (7.3)–(7.4) give, conservatively,
\[ \eta^{-1}\le C R^4\le AR^p. \tag{9.6} \]
Every applied spatial field is a rational linear combination of the original twelve fundamental shears. Every emitted time coefficient is an ordinary rational piecewise polynomial. The writing controls have degree at most two, and the complete construction has degree at most three.
The resulting compiler therefore satisfies the variable-target contract with fixed \(A,p\). Its uniformity comes from the bounded number of shear factors per return loop and the two-stage polarization construction; target frequency increases the number and numerical size of operations only polynomially.

## Native response prefix (truncated by reader)

**Yes, using the twelve-actuator erasure construction in your premises.** A uniform polynomial extension can be obtained by generating the target through shear conjugations and a fixed number of quadratic stages.

The useful change of representation is this:

1. Every coordinate-plane mode with polarization perpendicular to that plane can be synthesized by **two fundamental shear conjugations**. The necessary shear impulses and inverse synthesis coefficients have polynomial bounds in the frequency cutoff.
2. Those coordinate-plane modes generate every three-dimensional Fourier polarization in **at most two quadratic stages**, independently of the cutoff.
3. Each conjugation is performed inside a loop whose complete **physical linearized Euler propagator is exactly the identity**. Polynomial estimates inside a loop therefore do not multiply over the number of loops.
4. The nonlinear implementation uses short state translations. Its error estimates are uniform on an \(H^1\) ball and yield strong solutions for each actual disturbance; weak–strong uniqueness then supplies the quantifier over every Leray–Hopf realization.

I give the construction and its resource accounting below. The powers are deliberately generous. If \(p_0\) denotes the fixed exponent of the supplied erasure compiler, one admissible final choice is
\[
\boxed{p=10^{18}(p_0+1).}
\]
A fixed integer \(A\) is obtained by the finite precomputation described in §9. The writing phase uses time polynomials of degree at most two, so the complete compiler retains degree at most three.

Throughout, write
\[
\kappa=2\pi,\qquad
B(u,v)=P[(u\cdot\nabla)v],\qquad
L_Fv=B(F,v)+B(v,F).
\]

## 1. The quantitative translation property

The basic operation used below is a prescribed approximate translation of the state.

Suppose \(b_0\) is a known smooth, divergence-free, mean-zero field, \(G\) is a prescribed increment, and
\[
U(0)=b_0+e_0,\qquad \|e_0\|_{H^1}\le E.
\]
For a requested tolerance \(\theta>0\), we construct a force and a rational duration \(d>0\) such that, writing
\[
e_1=U(d)-(b_0+G),
\]
every admitted realization satisfies
\[
\boxed{
\|e_1\|_{H^1}\le \|e_0\|_{H^1}+\theta,
\qquad
\|e_1-e_0\|_2\le\theta.
}
\tag{1.1}
\]

The force depends on \(G\), numerical bounds for \(b_0,E\), and the scalar inputs. It does not depend on \(e_0\) or the disturbance.

The two estimates have different purposes. The first controls repeated operations on an unknown \(H^1\) perturbation. The second preserves the small \(L^2\) error produced by erasure. No assertion of uniform smallness of \(e_1-e_0\) in \(H^1\) is needed.

The construction first establishes (1.1) for coordinate-plane passive modes and then closes it under two explicit quadratic stages.

## 2. Polynomial stability of long fundamental-shear loops

The following estimate is the analytic ingredient needed for long shear impulses.

### 2.1 Statement

Let
\[
Q=e^{-a_dL_{F_d}}\cdots e^{-a_1L_{F_1}},\qquad d\le4,
\]
where each \(F_j\) is a fundamental shear, allowing a bounded linear combination of its sine and cosine partners. Set
\[
\mathfrak b=1+\max_j|a_j|.
\]
There are fixed effectively computable constants \(c,C>0\) such that
\[
\|Q^{\pm1}\|_{H^m\to H^m}\le C\mathfrak b^{500},
\qquad |m|\le6,
\tag{2.1}
\]
and
\[
\operatorname{Re}
\left\langle Q^{-1}\Delta Qz,(I-\Delta)z\right\rangle
\le
-c\mathfrak b^{-8}\|z\|_{H^2}^2
+C\mathfrak b^{500}\|z\|_{H^1}^2.
\tag{2.2}
\]

The crucial point in (2.2) is coercivity. It requires more than Sobolev bounds on \(Q\).

Here is a proof, including the steps that make the constants effective.

### 2.2 The physical \(L^2\) estimate

Temporarily use angular coordinates and take \(F=(\sin y,0,0)\). Fourier transform in \(x,z\), with frequencies \(k,l\), and put
\[
\alpha^2=k^2+l^2,\qquad
A=-\partial_y^2+\alpha^2,\qquad H=I-A^{-1}.
\]
For \(\alpha>0\), let \(v\) be the normal velocity component and define
\[
q=Av,\qquad \zeta=il\,u-ik\,w.
\]
The Rayleigh–Squire reduction gives
\[
q_a+ik\sin y\,Hq=0,
\tag{2.3}
\]
\[
\zeta_a+ik\sin y\,\zeta=-il\cos y\,v.
\tag{2.4}
\]
The velocity norm is
\[
\|U_{k,l}\|_2^2
=
\alpha^{-2}
\left(\|A^{-1/2}q\|_2^2+\|\zeta\|_2^2\right).
\tag{2.5}
\]
The usual reduction and the special stability of fundamental Kolmogorov flow on a cubic torus are also discussed by van Veen and Goto. The polynomial bounds below follow directly from (2.3)–(2.5). :chatgpt-content-reference{index="0"}

For \(\alpha^2\ge2\),
\[
\tfrac12 I\le H\le I,
\]
and \(\langle Hq,q\rangle\) is conserved. Differentiating once in \(y\) and using \(|k|\le\alpha\) gives
\[
\|A^{1/2}S_q(a)q_0\|_2
\le C(1+|a|)\|A^{1/2}q_0\|_2.
\]
The identity
\[
S_q(a)^*=H S_q(-a)H^{-1}
\]
then gives the same polynomial bound in the \(A^{-1/2}\) norm. Equation (2.4) adds at most one further power of \(1+|a|\).

For \(\alpha^2=1\), split \(q\) into its \(y\)-constant component and its orthogonal complement. The latter has the same positive \(H\)-energy. The constant component satisfies a scalar triangular equation, forced only by the controlled nonconstant component. In the case \(k\ne0\), \(l=0\), so no additional Squire coupling occurs.

For \(\alpha=0\), mean-zero divergence-free perturbations are stationary under the inviscid linearization. If constants are included, they produce only explicit linear growth.

Consequently,
\[
\|e^{-aL_F}\|_{L^2_\sigma\to L^2_\sigma}
\le C(1+|a|)^2.
\tag{2.6}
\]

### 2.3 Transport factorization on all vector fields

Componentwise transport does not preserve divergence. To factor the propagator correctly, extend the generator to all vector fields by
\[
L_F^{\rm ext}=F\cdot\nabla+R_F,
\]
where
\[
R_Fu
=
P[(u\cdot\nabla)F]
-\nabla\Delta^{-1}\partial_j[(\partial_iF_j)u_i].
\tag{2.7}
\]
This agrees with the physical generator on divergence-free fields, and
\[
\operatorname{div}(L_F^{\rm ext}u)
=F\cdot\nabla\operatorname{div}u.
\tag{2.8}
\]

The gradient part therefore has a polynomial \(L^2\) bound, obtained from explicit shear transport in \(H^{-1}\). Its forcing of the solenoidal part is order zero:
\[
PL_F^{\rm ext}\nabla\psi
=
P\!\left[
\bigl(\nabla F-(\nabla F)^T\bigr)\nabla\psi
\right].
\]
Combining this with (2.6) gives
\[
\|Q_F^{\rm ext}(a)\|_{2\to2}
\le C(1+|a|)^4.
\tag{2.9}
\]

Let \(T(a)\) be componentwise shear transport and write
\[
Q_F^{\rm ext}(a)=T(a)K(a).
\]
Then
\[
K_a=-\widetilde R(a)K,\qquad
\widetilde R(a)=T(a)^{-1}R_FT(a),
\]
and, importantly,
\[
K(a)K(r)^{-1}
=T(a)^{-1}Q_F^{\rm ext}(a-r)T(r).
\]
Thus its \(L^2\) norm is polynomial by (2.9), without an exponential Gronwall estimate.

### 2.4 Effective commutator bounds

For one fundamental shear, \(R_F\) is a finite sum of Fourier shifts composed with Riesz multipliers. Conjugating a coordinate derivative by \(T(a)\) produces either a coordinate derivative or
\[
\partial_y+a\cos y\,\partial_x.
\]

Since \(\partial_x\) commutes with \(R_F\),
\[
[\cos y\,\partial_x,R_F]=[\cos y,R_F]\partial_x.
\]
Repeated commutators produce finite differences of degree-zero Riesz symbols, multiplied by powers of \(k_x\). A \(j\)-fold finite difference has order \(-j\), which cancels those powers.

For each \(r\le6\), this gives
\[
\|\operatorname{ad}_{\partial}^{\,r}\widetilde R(a)\|_{2\to2}
\le C_r\mathfrak b^r.
\]
Duhamel’s formula, using the polynomial \(K\)-propagator bound, yields
\[
\|\operatorname{ad}_{\partial}^{\,r}K(a)\|_{2\to2}
\le C_r\mathfrak b^{4+6r}.
\tag{2.10}
\]
Adjoint commutators give the corresponding negative Sobolev bounds.

For scalar multiplication by \(\phi\), the elementary Riesz-symbol difference estimate gives
\[
\|[\phi,R_F]\|_{H^{-1}\to L^2}
\le C\|\phi\|_{H^5}.
\]
After transport conjugation and Duhamel,
\[
\|[\phi,K]\|_{H^{-1}\to L^2}
\le C\mathfrak b^{21}\|\phi\|_{H^5}.
\tag{2.11}
\]

All constants here can be computed by differentiating rational Fourier symbols through a fixed order, using their homogeneous derivative bounds away from zero, and checking finitely many shifted small frequencies.

### 2.5 Conjugated viscosity

Put
\[
A_T=T^{-1}\Delta T.
\]
It is a scalar divergence-form elliptic operator, applied componentwise. For one shear its ellipticity is at least \(c\mathfrak b^{-2}\), and its coefficient derivatives have polynomial bounds.

Expand
\[
[A_T,K]
=
\sum a_{ij}[\partial_i\partial_j,K]
+\sum[a_{ij},K]\partial_i\partial_j
+\text{first-order terms}.
\]
The derivative commutators use (2.10). The coefficient commutators use (2.11), together with
\[
\partial_i\partial_j:H^1\to H^{-1}.
\]
Hence
\[
[A_T,K]:H^1\to L^2
\]
has polynomial norm, and
\[
Q^{-1}\Delta Q=A_T+K^{-1}[A_T,K].
\tag{2.12}
\]

Integration by parts for \(A_T\), followed by Young’s inequality for the first-order remainder, gives the required \(H^1\) Gårding estimate.

For a product of \(d\) factors, retain a scalar second-order part and an \(H^1\to L^2\) remainder. A sufficient set of exponents is
\[
\begin{array}{c|c}
\text{Quantity}&\text{Exponent of }\mathfrak b\\ \hline
H^{\pm6}\text{ propagator norm}&46d\\
H^1\to L^2\text{ viscosity remainder}&25+15d\\
\text{Gårding lower-order coefficient}&50+32d\\
\text{inverse ellipticity}&2d.
\end{array}
\]
For \(d\le4\), these imply (2.1)–(2.2). This proves polynomial viscous stability inside the loops used below.

## 3. Uniform synthesis of passive coordinate-plane modes

Consider a plane with angular coordinates \(x,y\), and let \(e_\perp\) be its perpendicular coordinate direction. On fields
\[
e_\perp\phi(x,y),
\]
the physical linearized Euler evolution under either in-plane shear is exactly scalar transport.

Define
\[
(T_\theta\phi)(x,y)
=\phi(x,y+A\sin(x+\theta)),
\]
\[
(S_\psi\phi)(x,y)
=\phi(x+B\sin(y+\psi),y).
\]
Starting with the fundamental seed \(g=e^{iy}\),
\[
S_\psi T_\theta g
=
e^{\,iy+iA\sin(x+B\sin(y+\psi)+\theta)}.
\tag{3.1}
\]

### 3.1 Polynomially conditioned Bessel coefficients

For \(n\ge0\), set
\[
K_n=8(n+1)^2+\frac n2+\frac14,\qquad X_n=\pi K_n.
\]
Then
\[
\boxed{J_n(X_n)\ge \frac1{16(n+1)}.}
\tag{3.2}
\]

For completeness, let
\[
u_n(x)=\sqrt{\frac{\pi x}{2}}J_n(x).
\]
The Bessel equation becomes
\[
u_n''+u_n=\frac{n^2-\frac14}{x^2}u_n.
\]
Using the classical large-argument asymptotic as the boundary condition at infinity gives
\[
u_n(x)=
\cos\!\left(x-\frac{\pi n}{2}-\frac\pi4\right)
+
\int_x^\infty
\sin(t-x)\frac{n^2-\frac14}{t^2}u_n(t)\,dt.
\]
Iteration bounds the error from the cosine by
\[
\exp\!\left(\frac{|n^2-\frac14|}{x}\right)-1.
\]
At \(x=X_n\), the cosine is exactly \(1\), while
\[
24(n+1)^2\le X_n\le36(n+1)^2.
\]
This proves (3.2). The classical asymptotic and its differentiated form are recorded in DLMF §10.17; the displayed Volterra estimate supplies the uniform bound used here. :chatgpt-content-reference{index="1"}

The corresponding physical shear impulse is rational:
\[
X_n/\kappa=K_n/2.
\tag{3.3}
\]

### 3.2 Two phase projections

For a desired frequency \((m,n)\), \(m\ne0\), put
\[
q=n-1,\qquad A=X_{|m|},
\qquad
B=
\begin{cases}
X_{|q|}/m,&q\ne0,\\
0,&q=0.
\end{cases}
\]
The Jacobi–Anger expansion gives
\[
\frac1{(2\pi)^2}
\int\!\!\int
e^{-i(m\theta+q\psi)}S_\psi T_\theta g
\,d\theta\,d\psi
=
d_{m,n}e^{i(mx+ny)},
\tag{3.4}
\]
where
\[
d_{m,n}=J_m(A)J_q(mB),
\]
with the second factor equal to \(1\) when \(q=0\). This is a direct use of the Bessel generating function. :chatgpt-content-reference{index="2"}

For \(|m|,|n|\le N\), writing \(P_N=N+2\),
\[
|d_{m,n}|^{-1}\le256P_N^2,
\qquad |A|+|B|\le C P_N^2.
\tag{3.5}
\]
The physical impulses are rational signed multiples of
\[
K_{|m|}/2,\qquad K_{|q|}/(2m).
\]
Their signs are chosen to implement the displayed pullbacks.

If \(m=0,n\ne0\), exchange the plane coordinates.

### 3.3 Finite phase quadrature

Use the uniform grid
\[
\theta_a=2\pi a/Q,\qquad \psi_b=2\pi b/Q.
\]
The discrete average has the exact alias expansion
\[
\sum_{\substack{p\equiv m\pmod Q\\
\ell\equiv q\pmod Q}}
J_p(A)J_\ell(pB)e^{i(px+(1+\ell)y)}.
\tag{3.6}
\]

For each fixed \(r,s\), \(s\ge1\), differentiation of \(e^{iz\sin\theta}\) and Parseval give
\[
\sum_\ell(1+|\ell|)^{2j}|J_\ell(z)|^2
\le c_j(1+|z|)^{2j},
\qquad
c_j=2^{2j+1}(j!)^2.
\]
Applying this to the two alias classes in (3.6) yields
\[
\|\Phi_{m,n,Q}-e^{i(mx+ny)}\|_{H^r}
\le C_{r,s}P_N^{4r+2s+2}Q^{-s},
\qquad Q\ge4P_N.
\tag{3.7}
\]

The constants are explicit finite combinations of factorials and powers. For example, with
\[
K_r'=2\cdot260^r(1+c_r),
\]
one may use
\[
C_{r,s}
=
256\cdot2^s c_{r+s}
\left(K_r'37^{2r+s}+260^r37^{r+s}\right).
\]

Taking real and imaginary parts uses only fundamental real sine and cosine seeds. A unit real mode requires at most \(2Q^2\) conjugated seeds, and their coefficient sum satisfies
\[
\sum|\text{synthesis coefficients}|\le512P_N^2.
\tag{3.8}
\]
In particular, increasing \(Q\) does not enlarge that sum.

For the compiler, use the fixed order \(r=10\). The dynamical estimates need only \(H^6\), but the stronger synthesis accuracy costs no change of principle.

### 3.4 Rational computation

Replace
\[
\sin(x+\theta)
=\cos\theta\sin x+\sin\theta\cos x
\]
by rational approximations to its two coefficients. This field remains exactly in the prescribed twelve-dimensional force space.

The rounded shear and its inverse use the **same stored rational coefficients**. Their homogeneous physical propagators therefore cancel exactly.

All required numbers are computable with certified rational arithmetic. For example,
\[
J_n(X_n)
=
\int_0^1
\cos\!\left(X_n\sin(\pi t)-n\pi t\right)\,dt,
\tag{3.9}
\]
and the integrand has derivative bounded by \(C(N+2)^2\). A rectangle rule gives a polynomial evaluation procedure at any inverse-polynomial requested accuracy. The integral formula is DLMF 10.9.2. :chatgpt-content-reference{index="3"}

Use rational arctangent series for \(\pi\), Taylor bounds for sine and cosine, and interval arithmetic for reciprocals. Bound (3.5) supplies a certified nonzero denominator. No special-function or norm oracle is used.

Weights are stored with their \(Q^{-2}\) normalization, so their rounding errors also obey a coefficient-sum bound.

## 4. Physical implementation of a passive translation

This section converts the spatial synthesis into an operation on the actual nonlinear equation.

### 4.1 One return loop

Let a desired conjugated seed be \(SG\), where \(S\) is a product of two shear propagators.

Perform the following sequence:

1. The inverse shear word \(S^{-1}\).
2. A low-mode seed injection with prescribed impulse.
3. The shear word \(S\).

Every shear segment uses a carrier
\[
w(t)=\frac{a}{\ell}\,
q\!\left(\frac{t-t_0}{\ell}\right)F,
\qquad q(z)=6z(1-z).
\tag{4.1}
\]
Its impulse is \(a\), and \(w\) vanishes at both ends. Only one shear orientation is active at a time, so \(B(w,w)=0\).

The ideal physical force is
\[
f=w_t-\nu\Delta w+g,
\tag{4.2}
\]
where \(g\) is the fundamental seed injection, supported where \(w=0\). Since
\[
-\Delta F=\kappa^2F,
\]
rationally approximating \(\kappa^2\) makes every coefficient of (4.2) an ordinary rational polynomial of degree at most two.

Let \(Q(t)\) be the inviscid physical propagator generated by \(w\), starting at \(I\). At the end of the loop,
\[
Q=I
\tag{4.3}
\]
exactly.

### 4.2 The reference and its residual

For a known starting background \(b_0\), define the analysis reference
\[
\beta_t+L_w\beta=g,\qquad \beta(0)=b_0.
\tag{4.4}
\]
At a loop endpoint, \(\beta\) equals its starting value plus the corresponding conjugated seed increment.

The reference for the nonlinear equation is \(w+\beta\). Its residual is exactly
\[
\nu\Delta\beta-B(\beta,\beta),
\tag{4.5}
\]
apart from the paid rational approximation of the carrier force.

Put
\[
U=w+\beta+Qz.
\]
Then
\[
\begin{aligned}
z_t={}&
\nu Q^{-1}\Delta Qz
-Q^{-1}L_\beta Qz
-Q^{-1}B(Qz,Qz)\\
&+Q^{-1}\!\left(\nu\Delta\beta-B(\beta,\beta)
+h+\text{rounding error}\right).
\end{aligned}
\tag{4.6}
\]

The reference \(\beta\) need not be computed by the compiler. Its equation defines an explicit linear-control reference for the proof, and the bounds on it follow from the shear estimates and the synthesis coefficient sums. The output force is still precisely (4.2).

### 4.3 A concrete numerical envelope

Let \(H\) be an integer containing fixed multiples of all the following bounds:

- the frequency cutoff, mode count and coefficient sum;
- \(\|b_0\|_{H^6}\), the error-radius bound \(E\), and \(\theta^{-1}\);
- \(\nu^{-1}\) and the reciprocal allotted time;
- the fixed constants in §§2–3.

Choose
\[
Q_{\rm grid}=H^{100},\qquad
d_{\rm leaf}=H^{-50000}.
\tag{4.7}
\]
Use coefficient precision at least \(H^{-1000}\), and a \(\kappa^2\)-enclosure sufficiently narrow to give carrier-force error at most \(H^{-200000}\) times the carrier amplitude.

There are at most \(CH^{201}\) loops. Their impulses are bounded by \(CH^2\). Inside any loop, the sharper exponents in §2 give, after enlarging the fixed lower bound for \(H\),
\[
\|Q^{\pm1}\|_{H^m\to H^m}\le H^{1000},
\qquad |m|\le6,
\tag{4.8}
\]
and the transformed viscosity has coercivity at least
\[
\mu=\nu H^{-32}.
\tag{4.9}
\]
The reference satisfies
\[
\sup_t\|\beta(t)\|_{H^6}\le H^{1030}.
\tag{4.10}
\]

The exponent in (4.10) includes transport of the existing general three-dimensional background. It is not obtained solely from the passive scalar formula.

For
\[
\mathcal E=\|z\|_{H^1}^2,\qquad Z=\|z\|_{H^2},
\]
the Gårding estimate, the usual \(H^1\)-\(H^2\) Navier–Stokes estimate, and Young’s inequality give the coarse bound
\[
\mathcal E'+\mu Z^2
\le H^{13000}(1+\mathcal E+\mathcal E^3),
\tag{4.11}
\]
for disturbances and carrier-force rounding error whose combined \(L^\infty L^2\) norm is at most two.

Starting with \(\mathcal E(0)\le H^2\), (4.7) closes the bootstrap with a large margin. Integration of (4.6) also gives
\[
\|z(d_{\rm leaf})-z(0)\|_2
\le
H^{5000}\left(
d_{\rm leaf}^{1/2}
+d_{\rm leaf}^{3/4}
+d_{\rm leaf}
\right).
\tag{4.12}
\]
The viscosity contribution uses the integrated \(H^2\) bound from (4.11); the quadratic contribution uses Hölder’s inequality with that same bound.

Both (4.11) and (4.12) give errors much smaller than \(\theta\), since \(H\ge\theta^{-1}\).

At every loop boundary \(Q=I\). Thus the transformed perturbation is continuous across resets, and the energy inequalities accumulate over total elapsed time. There is no product of one polynomial loss per quadrature sample.

After accounting for the finite synthesis error and rebasing to the ideal Fourier increment \(G\), this proves (1.1) for passive planar increments.

### 4.4 Leaf resources

Divide the leaf duration into equal rational segment lengths. The inverse segment width is at most \(CH^{50201}\). Formula (4.1) then gives
\[
\sup_t\|f(t)\|_{W^{1,\infty}}\le H^{102000}.
\]
All other numerical resources fit within \(H^{10^6}\). Bit operations, output bits and working memory fit within
\[
C(L+H)^{10^6}.
\tag{4.13}
\]

The distinction between \(L\) and \(H\) is retained: large input denominators may enlarge arithmetic work, while the physical bounds depend on numerical envelopes.

## 5. All Fourier polarizations in two quadratic stages

Define
\[
\mathcal B(u,v)=\kappa^{-1}B(u,v).
\]
Its Fourier algebra has rational coefficients.

Let level zero consist of the passive modes
\[
e_i\cos(\kappa k\cdot x),\quad
e_i\sin(\kappa k\cdot x),
\qquad k_i=0.
\]

For \(a\perp m\), \(b\perp n\), \(k=m+n\), put
\[
C=P_k\bigl((a\cdot n)b+(b\cdot m)a\bigr).
\]
Writing \(\mathcal B(u)=\mathcal B(u,u)\), direct trigonometric expansion gives
\[
C\cos(\kappa k\cdot x)
=
\mathcal B(a\cos m+b\sin n)
+\mathcal B(b\cos n+a\sin m),
\tag{5.1}
\]
and
\[
C\sin(\kappa k\cdot x)
=
\mathcal B(a\sin m+b\sin n)
+\mathcal B(a\cos m-b\cos n).
\tag{5.2}
\]
Here the abbreviated phases include \(\kappa\). Difference-frequency terms cancel. Replacing one polarization by its negative reverses the quadratic direction.

### Three nonzero coordinates

For \(k=(a,b,c)\), define
\[
t_{12}=(b,a,0),\quad
t_{13}=(c,0,a),\quad
t_{23}=(0,c,b),\qquad C_{ij}=P_kt_{ij}.
\]
Each \(C_{ij}\) is obtained at level one from passive modes
