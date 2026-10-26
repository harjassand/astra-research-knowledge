# DC response, time reversal and a static comparator for switched diffusion

These are independently derived finite-dimensional statements. They are not a
claim of a new physical device, nor a claim that the underlying variational and
adjoint methods are new. The literature boundaries are in SOURCES.md.

## Model and quantifiers

Take any finite undirected graph with n fixed-temperature terminals and m
internal nodes. Each contact has a bounded, nonnegative, piecewise-continuous
P-periodic conductance. Write its symmetric graph Laplacian in blocks as

\[
 L(t)=\begin{pmatrix}D(t)&-B(t)^T\\-B(t)&A(t)\end{pmatrix}\succeq0.
\]

Internal temperatures x obey

\[
 C\dot x=-A(t)x+B(t)\theta,\qquad
 q(t)=D(t)\theta-B(t)^Tx,
 \tag{1}
\]

where theta is the constant terminal-temperature vector, q is heat current from
the terminals into the network, and C is a constant symmetric positive-definite
matrix. Ordinary lumped thermal capacities give diagonal C. There are no internal
heat sources, advection, temperature-dependent coefficients, hidden terminals,
or actuator heat/work in this ideal model. All results below hold for every
finite n,m, every such schedule, and every constant theta, subject to a unique
periodic solution. A connected averaged graph is a sufficient hypothesis.

Angle brackets denote one-period averages. Define

\[
 \bar A=\langle A\rangle,\quad\bar B=\langle B\rangle,\quad
 \bar D=\langle D\rangle,\quad X_*=\bar A^{-1}\bar B,
 \qquad Y_*=\bar D-\bar B^T\bar A^{-1}\bar B.
 \tag{2}
\]

Y_* is the established static Kron reduction of the **averaged contact graph**.
It is not the average of the instantaneous Kron reductions. Let x(t)=X(t)theta
be the periodic solution and define Y by average q=Y theta.

Existence detail: for an unforced solution,
\(\frac12\frac d{dt}(x^TCx)=-x^TA(t)x\leq0\).
If a nonzero state retained its C norm over a period, A(t)x(t)=0 almost
everywhere, hence x would be constant and lie in the kernel of bar A. With
bar A positive definite this is impossible. The period map has spectral radius
less than one, and the forced periodic solution is unique. Full connectivity of
the averaged graph also makes Y_* positive definite on the terminal-contrast
space \(\mathbf1^\perp\).

## Theorem 1: exact comparison, including a directional-loss constraint

Let \(Z(t)=X(t)-X_*\), and \(Y_s=(Y+Y^T)/2\). Then

\[
 \boxed{Y_*-Y_s=\langle Z(t)^TA(t)Z(t)\rangle\succeq0.}
 \tag{3}
\]

On \(\mathbf1^\perp\), where Y_* is invertible, there is also the stronger
constraint

\[
 \boxed{Y^TY_*^{-1}Y\preceq Y_s.}
 \tag{4}
\]

In (4), restrict both matrices to the contrast space before taking the inverse.
Equivalently one may use the Moore-Penrose inverse on the full terminal space.
In particular, if \(N=Y_*^{-1/2}YY_*^{-1/2}\) in contrast coordinates,

\[
 (N-I/2)^T(N-I/2)\preceq I/4,
 \qquad (N-I)^T(N-I)\preceq I-\operatorname{sym}N.
 \tag{5}
\]

Thus a normalized skew response cannot remain finite while the symmetric loss
relative to the averaged static graph tends to zero in operator norm:

\[
 \|\operatorname{skew}N\|_2\leq
 \sqrt{\|I-\operatorname{sym}N\|_2}.
 \tag{6}
\]

### Proof

Fix theta and put \(x_*=X_*\theta\), \(z=x-x_*\), and
\(r(t)=B(t)\theta-A(t)x_*\). Equation (1) gives
\(C\dot z=-Az+r\). Constant C and periodicity imply

\[
 \langle z^Tr\rangle=\langle z^TAz\rangle.
 \tag{7}
\]

The instantaneous Dirichlet quadratic form is

\[
 d(\theta,x)=\theta^TD\theta-2x^TB\theta+x^TAx.
\]

Expanding about x_* and applying (7) gives

\[
 \langle d(\theta,x)\rangle
 =\langle d(\theta,x_*)\rangle-\langle z^TAz\rangle
 =\theta^TY_*\theta-\langle z^TAz\rangle.
 \tag{8}
\]

Also \(\theta^Tq-d(\theta,x)=x^TC\dot x\), whose period average is zero.
Hence the left side of (8) is theta^T Y_s theta. Because theta is arbitrary,
(3) follows. Positivity of L also gives Y_s positive semidefinite.

For (4), write W=Y_*-Y. From (1)-(2),
\(W=\langle B^TZ\rangle\) and \(\langle AZ\rangle=0\).
For any terminal vectors u,v, introduce full-node vectors
\(\eta_u=(u,X_*u)\), \(\zeta_v(t)=(0,Z(t)v)\). Then

\[
 \langle\eta_u^TL\zeta_v\rangle=-u^TWv,
 \quad\langle\eta_u^TL\eta_u\rangle=u^TY_*u,
 \quad\langle\zeta_v^TL\zeta_v\rangle=v^T(Y_*-Y_s)v.
\]

Cauchy-Schwarz for the positive-semidefinite integrated L form yields

\[
 |u^TWv|^2\leq (u^TY_*u)\,v^T(Y_*-Y_s)v.
\]

Taking the supremum over u in contrast space gives
\(W^TY_*^{-1}W\preceq Y_*-Y_s\). Expand W=Y_*-Y to obtain (4).
Completing squares proves (5), and taking norms followed by the skew projection
proves (6). Conservation and invariance under common temperature shifts give
\(\mathbf1^TY=0\) and \(Y\mathbf1=0\), justifying restriction to contrasts.
This completes the proof.

### What this comparison says physically

The thermal Dirichlet form has units W K. It is **not** electrical power or total
heat flux. Close to a common temperature T0, it is T0 squared times the leading
entropy-production rate. A direct cooling consequence holds for every two-level
terminal pattern: let theta=T0*1+Delta*1_H, with H any hot-terminal subset and
all other terminals at T0. Then

\[
 \sum_{i\in H}\langle q_i\rangle
 =\Delta\,\mathbf1_H^TY\mathbf1_H
 \leq\Delta\,\mathbf1_H^TY_*\mathbf1_H.
 \tag{9}
\]

The case of one hot terminal and equal-temperature sinks is included. For
arbitrary several distinct terminal temperatures, (3) is a quadratic comparison;
it does not order every individual current. Routing and isolation can still be
useful. Nor does the theorem claim that averaged contact values are feasible
under every actuator/material constraint. They are feasible in the declared
convex conductance comparator class. A nonlinear barrier-lowering budget can
exclude its averaged conductance vector; see the explicit source boundary in
SOURCES.md.

For the one-body, three-terminal topology with a total static contact budget G,
the ordinary comparator is globally optimal for worst-hot-port cooling. If its
three contacts have conductances k_i>=0 summing to G, its terminal matrix is
\(\operatorname{diag}k-kk^T/G\). Its trace is
\(G-\sum_i k_i^2/G\leq2G/3\), so its smallest diagonal is at most 2G/9.
The uniform allocation k_i=G/3 achieves that value for every terminal. By (3),
no periodic switching schedule on this topology, at the same mean total budget,
can exceed this worst-port optimum. Thus the comparator is not a weak selected
static fixture. If the installed independent contacts can instead all remain
closed at their full conductance without a mean-conductance restriction, that
all-on static incumbent is stronger still. This latter comparison requires
simultaneous closure to be mechanically feasible and does not account for any
unmeasured actuator holding costs.

Periodicity is essential to the full-cycle comparison. A pre-cooled body can
absorb extra heat during a finite initial transient. The storage boundary terms
in the proof then do not vanish. This construction does not count expendable
cold preparation as a repeated-cycle gain.

### Continuum counterpart

The same argument is not tied to a lumped numerical fixture. On a bounded
Lipschitz domain with positive bounded time-independent volumetric capacity
c(x), let symmetric kappa(x,t) be bounded, uniformly elliptic and P-periodic.
The heat equation is c partial_t u = div(kappa grad u). Impose a time-independent
Dirichlet trace f in H^(1/2), and use the unique weak periodic solution. Let u_*
be the static solution with the averaged tensor bar kappa and the same trace.
For the averaged inward heat-flux Dirichlet-to-Neumann operator Lambda and its
static counterpart Lambda_*,

\[
 \langle f,(\Lambda_*-\operatorname{sym}\Lambda)f\rangle_{\partial\Omega}
 =\left\langle\int_\Omega
   \nabla(u-u_*)^T\kappa(x,t)\nabla(u-u_*)\,dx\right\rangle\geq0.
 \tag{9a}
\]

Here the angle brackets on the right are time averages and the left pairing is
the boundary duality pairing. The inward heat flux is n dot kappa grad u with
outward unit normal n. The proof repeats (7)-(8) using integration by parts and
the vanishing periodic storage integral. Coercivity plus Poincare's inequality
gives a unique periodic solution. Smooth data give the classical proof; standard
energy-space approximation extends it to the stated weak data. For any finite
set of admissible boundary basis functions, the integrated energy-form
Cauchy-Schwarz proof also gives (4) for the resulting boundary response matrix
on its nonconstant subspace. Constant terminal values on touching boundary
patches require admissible traces or regularized junctions; singular ideal
boundary jumps are not silently assumed. This corollary excludes advection,
capacity modulation, internal sources and nonlinear coefficients just as (1)
does.

## Theorem 2: reversal transposes the DC response

Reverse the entire periodic schedule: A^R(t)=A(P-t), and likewise B,D. Capacities
stay fixed. Then

\[
 \boxed{Y^R=Y^T.}\tag{10}
\]

To prove it, let x solve (1) for theta. Let \(z(t)=x^R_u(P-t)\) be the reversed
schedule's periodic solution driven by terminal vector u, played backwards.
It satisfies \(-C\dot z+Az=Bu\). Integration by parts, constant symmetric C,
periodicity, and A=A^T yield

\[
 \langle z^TB\theta\rangle
 =\langle z^T(C\dot x+Ax)\rangle
 =\langle x^T(-C\dot z+Az)\rangle
 =\langle x^TBu\rangle.
\]

Combining this with symmetric D in the port currents proves (10).

Consequently any schedule equal to its reversal up to a phase shift has
symmetric DC response. Every schedule consisting of one constant A phase and
one constant B phase per period has this property, even with unequal durations.
Thus two phases cannot create DC circulation, regardless of internal dimension,
contact strengths, or heat capacities. This is a terminal statement; a sampled
internal monodromy matrix need not be symmetric. For a genuine two-terminal
closed network, conservation already enforces a symmetric DC matrix regardless
of phase count. Three or more terminals are needed for linear DC circulation.

## Construction: a fixed-capacity body with sequential reciprocal contacts

A single internal body of capacity C contacts n terminals in cyclic order,
each exclusively with conductance g for time P/n. It stays at the same spatial
node in this ideal circuit; only contacts change. Let

\[
 z=gP/(nC),\quad r=e^{-z},\quad
 a=\frac{C(1-r)^2}{P(1-r^n)}.
\]

If d=(j-i) mod n belongs to 1,...,n-1, then

\[
 \boxed{Y_{ji}=-a r^{d-1},\qquad
 Y_{jj}=a\sum_{d=1}^{n-1}r^{d-1}.}\tag{11}
\]

Proof: the body's post-contact temperatures obey
\(x_i=r x_{i-1}+(1-r)\theta_i\). Their unique cyclic solution is
\(x_i=(1-r)\sum_{k=0}^{n-1}r^k\theta_{i-k}/(1-r^n)\).
Contact i supplies heat \(Q_i=C(x_i-x_{i-1})\). Expanding this expression and
dividing by P gives (11).

The exclusive-contact operation also has an exact nonuniform extension. Let
phase i have arbitrary positive duration tau_i and conductance g_i, put
r_i=exp(-g_i*tau_i/C), P=sum_i tau_i, and R=product_i r_i. For i!=j,

\[
 -Y_{ji}=\frac C P\frac{(1-r_j)(1-r_i)}{1-R}
       \prod_{k\text{ strictly between }i\text{ and }j\text{ cyclically}} r_k.
 \tag{11a}
\]

The diagonal is fixed by row sum zero. This follows from the same cyclic scalar
recurrence; it is not a small-perturbation assertion. For three ports, the ratio
of each adjacent forward coefficient to its reverse is 1/r_k, where k is the
third contact. Therefore the orientation survives arbitrary positive unequal
contact strengths and durations in the zero-leak model. Leakage, parasitic
capacity and actuator effects require their own model and are not covered by
that robustness claim.

For n=3, forward transfer coefficient f=a, reverse b=ar, so f/b=exp(z).
The matrix is a genuine nonreciprocal three-port DC response. But as z tends to
infinity at fixed g,C, both f and the directional excess f-b tend to zero.
This is not a zero-cost ideal circulator and does not pump heat at equal port
temperatures. A static uniform star with conductances g/3 has off-diagonal
transfer g/9 and hot-port extraction coefficient 2g/9. It dominates the switched
star's symmetric part by (3).

## Exact finite-leakage extension

Let the active contact conductance be g_on and every inactive contact be g_off,
all identical, with equal phase durations. Put

\[
 G=g_{on}+(n-1)g_{off},\quad
 \alpha=(g_{on}-g_{off})/G,\quad
 Y_*=(G/n)(I-\mathbf1\mathbf1^T/n).
\]

Let Y0 be (11) with g=G. The leaky response is exactly

\[
 \boxed{Y_{leak}=\alpha^2Y_0+(1-\alpha^2)Y_*.}\tag{12}
\]

Proof: the body's instantaneous equilibrium in phase i is
\(\alpha\theta_i+(g_{off}/G)\sum_j\theta_j\). On contrast inputs, the body's
temperature is alpha times that of the exclusive-contact G model. Since the
total conductance is constant and all phases have equal durations, its average
temperature is zero on contrast inputs. The constant leakage part of the port
coupling therefore contributes only its static term. The modulated part
contributes alpha squared times the exclusive-contact transfer. Expanding the
diagonal term G/n gives (12); common-mode invariance extends it to all inputs.

For n=3, write \(h=(1-\alpha^2)G/9\). Then f=alpha^2*a+h and
b=alpha^2*a*r+h. At any fixed nonzero leakage ratio, increasing P without bound
returns f/b to one, rather than producing arbitrarily good isolation. The
numerical study optimizes the complete finite-rate formula, not a truncated
high-frequency expansion.

Finally, splitting the same total C and g into k phase-staggered identical
parallel bodies, each with C/k and g/k and the same P, leaves z unchanged and
adds k copies of Y/k. It can smooth ripple, but cannot improve this DC frontier
with matched aggregate capacities and conductances. Increasing each copy's g
while shrinking C would spend additional contact resources.
