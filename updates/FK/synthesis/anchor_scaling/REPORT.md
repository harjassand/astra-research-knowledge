# Anchor geometry, source memory, and the continuum limit

**Disposition: stronger scoped obstruction and scaling map; no temperature-correct anchor repair established.** A geometry-weighted extension of the fixed-slice estimate shows that positive space-time anchor density is not a general requirement for order-one *influence*. In an exact linear comparator, source covariance changes the scale from $r/\sqrt N$ for a coherent mode to $\sqrt{r/N}$ for summable covariance; stationarity alone selects neither behavior. More decisively, for the independently driven symmetric-source update, an exact first-order identity shows that no fixed, moving, or randomly placed mask supplies the finite-temperature quartic response coefficient. The remaining repair must supply a specific source-target cross-moment or change the drift law; its acquisition cost is unresolved.

The proofs and checks here are scoped to the convex lattice SDE in the supplied thermal report. They do not establish a new solver, physical validation, historical priority, or a universal no-go theorem for correlated thermal constructions.

## 1. Model and scope

Let $\mathcal I=\mathbb Z_N\times\Lambda$, where $\Lambda$ is a finite periodic spatial graph. At fixed spacing, take

\[
K=\alpha I+\kappa_\tau L_\tau+\kappa_xL_x,
\qquad \alpha>0,\quad \kappa_\tau,\kappa_x\ge0,
\]

with nonnegative graph Laplacians. Let $A\subseteq\mathcal I$ be any anchor set and $P_A$ its diagonal indicator. The target and reference processes are

\[
dX=-[KX+g(I-P_A)X^3+gP_AY^3]ds+\sqrt2\,dW,
\qquad
dX^0=-[KX^0+g(X^0)^3]ds+\sqrt2\,dW,
\]

where $g\ge0$, the processes share the same $W$, and the source is stationary. For each possible anchor coordinate $a$, assume

\[
B_a\ge \|g(Y_a^3-(X_a^0)^3)\|_2.
\]

The nonlinear comparison below needs no source independence, temporal mixing, or correlation decay. For a random mask drawn before the Langevin run and independently of its trajectory, condition on the mask and use a moment bound uniform over candidate coordinates. Path-adaptive masks need an additional stationarity argument; if anchor selection changes the source law, that law needs its own contract.

## 2. Geometry-weighted nonlinear comparison

For a complex readout vector $v$, write $F_v=v^*X$, $F_v^0=v^*X^0$, and $G=K^{-1}$. Define

\[
D_A(v)=\sum_{a\in A}B_a(G|v|)_a.
\]

Then

\[
\boxed{\|F_v-F_v^0\|_2\le D_A(v).}
\]

Brascamp–Lieb for the even strongly convex reference law also gives

\[
\mathbb E|F_v^0|^2\le v^*Gv,
\qquad
\left|\mathbb E|F_v|^2-\mathbb E|F_v^0|^2\right|
\le 2\sqrt{v^*Gv}\,D_A(v)+D_A(v)^2.
\]

The original $rB/(\alpha\sqrt N)$ estimate follows by taking $v_{(t,x)}=N^{-1/2}e^{i\omega t}$, anchoring every spatial site on $r$ temporal slices, and using the spatial Green row sum $1/\alpha$.

**Proof.** Put $Z=X-X^0$. At nonanchors,

\[
g(X_i^3-(X_i^0)^3)=d_iZ_i,
\qquad d_i=g[X_i^2+X_iX_i^0+(X_i^0)^2]\ge0.
\]

Thus $dZ=-(K+D_s)Z\,ds+f_s\,ds$, where $D_s\ge0$ is diagonal and $f_s$ is supported on anchors. The matrix $-K$ is cooperative because its off-diagonal entries are nonnegative. The comparison principle gives $0\le U(s,u)\le e^{-K(s-u)}$ for the evolution kernel. The stationary pullback representation and Minkowski's inequality yield

\[
\|Z_i\|_2\le\sum_{a\in A}G_{ia}B_a.
\]

Multiplying by $|v_i|$, summing over $i$, and using $G=G^T\ge0$ proves the first claim. The second follows from Cauchy–Schwarz and the covariance inequality for the reference law.

For a local temporal Fourier readout at spatial site $x$, the product heat kernel gives

\[
(G|v|)_{(s,y)}
=\frac1{\sqrt N}\sum_tG_{(s,y),(t,x)}
=\frac1{\sqrt N}G_x(y,x),
\qquad
G_x=(\alpha I+\kappa_xL_x)^{-1}.
\]

Therefore any fixed anchor geometry satisfies

\[
\boxed{
D_A(x,\omega)\le\frac1{\sqrt N}
\sum_{(s,y)\in A}B_{s,y}G_x(y,x).
}
\]

The temporal locations disappear from this worst-case bound because it sums absolute influences. Temporal phase cancellation needs assumptions on the forcing or its covariance.

## 3. Massive Green functions and anchor geometry

On a periodic nearest-neighbor graph of degree $z$, write $L_x=zI-A_x$. Then

\[
G_x=\frac1{\alpha+z\kappa_x}
\sum_{n\ge0}\left(\frac{\kappa_x}{\alpha+z\kappa_x}\right)^n A_x^n.
\]

If $R=d(x,y)$, then $(A_x^n)_{xy}=0$ for $n<R$ and $(A_x^n)_{xy}\le z^n$. Summing the walk tail proves the coarse but explicit bound

\[
0\le G_x(y,x)\le\frac1\alpha\rho^R,
\qquad
\rho=\frac{z\kappa_x}{\alpha+z\kappa_x}<1.
\]

If there are at most $k$ anchors per temporal slice, all at least $R_N$ steps from the readout site, then

\[
D_A(x,\omega)\le\frac{Bk\sqrt N}{\alpha}\rho^{R_N}.
\]

Thus moving anchors erase their influence when $Bk\sqrt N\rho^{R_N}/\alpha\to0$. At fixed $B,k,\alpha,\rho$, a distance slightly larger than $\log N/(2|\log\rho|)$ suffices. This is a sufficient worst-case criterion, not a necessary distance law.

For random geometry, suppose each time slice independently chooses one uniformly random spatial site $Y_s$. Define the unit-forcing exposure

\[
E_N=\frac1{\sqrt N}\sum_{s=0}^{N-1}G_x(Y_s,x).
\]

The Green row sum gives

\[
\mathbb E E_N=\frac{\sqrt N}{\alpha|\Lambda|}.
\]

Independence of the *anchor placements* across slices and $(K_x^{-2})_{xx}\le\alpha^{-1}(K_x^{-1})_{xx}\le\alpha^{-2}$ give

\[
\operatorname{Var}(E_N)\le\frac1{\alpha^2|\Lambda|}.
\]

The nonlinear comparison envelope is $BE_N$. At fixed cutoff, $|\Lambda|\asymp\sqrt N$ gives order-one exposure with $N$ total anchors and space-time fraction $1/|\Lambda|\to0$. If $|\Lambda|\gg\sqrt N$, the envelope vanishes in probability. Thus positive *total space-time density is not necessary for order-one possible influence* on one local output. This does not establish a temperature-correct response or simultaneous coverage of every site.

If every spatial site needs a local answer, random placement has a coverage cost. Write $B_R(x)$ for the radius-$R$ ball around $x$. For independent uniform placements, a union bound shows that the following number is sufficient to hit every such ball in one slice with failure probability at most $\delta$:

\[
k\gtrsim\frac{|\Lambda|}{|B_R|}
\left(\log|\Lambda|+\log\frac1\delta\right)
\]

anchors in that slice. This is a coverage requirement, not an optimal algorithmic lower bound. A single known readout can be targeted locally, but doing so does not repair the response coefficient below.

## 4. Stationarity does not control cancellation

The nonlinear comparison uses absolute values. An exact linear forced comparator shows why stationarity alone cannot justify a covariance improvement. Let $Z=K^{-1}P_A\xi$, anchor the single spatial site $x$ at each time in $S$, and read the zero temporal mode at $x$. Then

\[
F_{x,N}=\frac{G_x(x,x)}{\sqrt N}\sum_{s\in S}\xi_s.
\]

For a centered stationary source with covariance $C(h)$,

\[
\operatorname{Var}(F_{x,N})
=\frac{G_x(x,x)^2}{N}
\sum_{s,s'\in S}C(s-s').
\]

For $r=|S|=\sqrt N$, a unit-variance common mode $\xi_s=\zeta$, with $C(h)=1$ at every lag, gives variance $G_x(x,x)^2$, independent of $N$. Unit-variance iid forcing gives variance $G_x(x,x)^2/\sqrt N\to0$. The two sources have identical one-coordinate marginals and are both stationary. The common mode is a nonmixing temporal degree of freedom; its preparation and retention are part of the source.

Thus the $\sqrt N$ anchor count can retain an order-one output in an exact linear comparator even though its temporal fraction tends to zero; with one spatial anchor per selected slice, total space-time density also tends to zero as $|\Lambda|\to\infty$. The attained effect uses the shared zero-frequency source mode and is not a temperature-correct result for the nonlinear update.

More generally, if $C\in\ell^1(\mathbb Z)$, then every set $S$ obeys

\[
\operatorname{Var}(F_{x,N})
\le G_x(x,x)^2\frac rN\sum_h|C(h)|.
\]

In this linear additive comparator, unit-scale forcing with uniformly summable covariance needs $r=\Omega(N)$ for order-one variance. A zero-frequency covariance atom permits $r=\Theta(\sqrt N)$. These exact statements are not transferred to the nonlinear sampler: its random comparison kernel depends on the target path, and a source-covariance improvement needs assumptions that control that dependence.

## 5. Exact first-order failure for independent symmetric sources

Consider the supplied finite-lattice update with an independently driven, centered symmetric source at $\lambda=0$, where $g=\lambda/6$. The source may have correlations among its own coordinates; the assumptions used here are independence from $X^0$ at zero coupling and $\mathbb E Y_a^3=0$. Let $Q=I-P$, $C=K^{-1}$, and assume translation invariance so $C_{aa}=c_0$. Differentiating the stationary covariance equation gives

\[
KC_1+C_1K=-\frac{c_0}{2}(QC+CQ),
\qquad
C_1=\left.\frac{d}{d\lambda}\mathbb E[XX^T]\right|_{0^+}.
\]

For a normalized plane wave $v_q$ with $Kv_q=k_qv_q$, the Lyapunov solution is

\[
\boxed{
v_q^*C_1v_q
=-\frac{c_0}{2k_q^2}
\left(1-\langle v_q,Pv_q\rangle\right).
}
\]

Indeed,

\[
C_1=-\frac{c_0}{2}\int_0^\infty e^{-Kt}(QC+CQ)e^{-Kt}\,dt.
\]

Both terms in the plane-wave matrix element equal $\langle v_q,Qv_q\rangle e^{-2k_qt}/k_q$. On a homogeneous lattice a plane wave has constant coordinate magnitude, so $\langle v_q,Pv_q\rangle=f=|A|/|\mathcal I|$. Any mask locations with the same density therefore have the same first-order diagonal response. Random masks independent of $X^0$ replace $f$ by their expected fraction; state-dependent feedback masks are outside this identity.

Under the matched-mode identification $k_q=\eta^2+\Omega(q)^2$, the physical quartic oscillator-lattice coefficient supplied with the task is

\[
\left.\partial_\lambda\chi_\beta(i\eta,q)\right|_{0^+}
=-\frac{c_\beta}{2[\eta^2+\Omega(q)^2]^2},
\qquad
c_\beta=\frac1{|\Lambda|}\sum_p\frac{\coth(\beta\Omega(p)/2)}{2\Omega(p)}.
\]

At finite $\beta$, $c_\beta>c_\infty$, where $c_\infty=|\Lambda|^{-1}\sum_p(2\Omega(p))^{-1}$. In the long-target limit $c_0\to c_\infty$. Since $0\le1-f\le1$, no anchor count or geometry in this independent symmetric-source update matches the physical coefficient at first order. This is an exact perturbative counterexample to repair by anchor counting, not a claim that perturbation theory solves the interacting system.

For a general source-target coupling, define $R_{ij}=\mathbb E[Y_i^3X_j^0]$ on anchor rows. Differentiation gives

\[
KC_1+C_1K=-\frac{c_0}{2}(QC+CQ)-\frac16(PR+R^TP),
\]

and hence

\[
v_q^*C_1v_q
=-\frac{c_0(1-f)}{2k_q^2}
-\frac{\operatorname{Re}(v_q^*PRv_q)}{6k_q}.
\]

Matching the physical derivative requires, mode by mode,

\[
\boxed{
\operatorname{Re}(v_q^*PRv_q)
=\frac{3}{k_q}[c_\beta-c_0(1-f)].
}
\]

The surviving repair operation is therefore precise: construct or certify the temperature-correct source-target cross-moment map across the requested modes, or change the drift to supply the same insertion. No such map is constructed here. Acquiring it from the target thermal state may already require the response information the sampler was meant to avoid; a shared long-range source mode must be charged as a correlated state, not treated as a free independent snapshot.

## 6. Continuum spacing and anchor counts

For a scalar Euclidean lattice with fixed finite spatial cutoff and time step $a$, the discretized action

\[
S_a(q)=\sum_t\left[\frac{(q_{t+1}-q_t)^2}{2a}
+\frac{am^2q_t^2}{2}+\frac{a\lambda q_t^4}{24}\right]
\]

maps to

\[
K_a=\frac1aL_\tau+a(m^2I+\kappa L_x),
\quad
\alpha_a=am^2,
\quad
\kappa_{\tau,a}=a^{-1},
\quad
\kappa_{x,a}=a\kappa,
\quad
g_a=\frac{a\lambda}{6}.
\]

With explicit spatial mesh $h$, the gradient convention gives $\kappa_{x,a}=a\kappa/h^2$. Thus the mass floor vanishes, temporal stiffness diverges, and quartic drift coefficient vanishes as $a\to0$. Holding all three fixed is not the continuum limit of this action.

The global eigenvalue bound $K_a\ge am^2I$ is too crude for source moments. Coordinate-wise Brascamp–Lieb gives

\[
\operatorname{Var}(X_i)\le(K_a^{-1})_{ii}=c_{a,T},
\qquad
\mathbb E|X_i|^6\le96c_{a,T}^3.
\]

At fixed physical target length $T=Na$ and finite spatial cutoff,

\[
c_{a,T}
=\frac1{N|\Lambda|}\sum_{n,p}
\frac1{am^2+4a^{-1}\sin^2(\pi n/N)+a\kappa\lambda_p}
\longrightarrow
\frac1{|\Lambda|}\sum_p\frac{\coth(T\Omega(p)/2)}{2\Omega(p)},
\quad
\Omega(p)^2=m^2+\kappa\lambda_p.
\]

For compact source period $\beta$, let $c_{a,\beta}$ and $c_{a,T}$ be the source and target diagonal Green values. Applying the coordinate sixth-moment bound to each field gives

\[
B_a\le\sqrt{96}\,g_a\left(c_{a,\beta}^{3/2}+c_{a,T}^{3/2}\right)=O(a).
\]

This uses centered even strongly convex source and target actions and fixed finite spatial cutoff. For a dimensionless spatial graph Laplacian the decay factor has a finite limit,

\[
\rho_a=\frac{z\kappa_{x,a}}{\alpha_a+z\kappa_{x,a}}
=\frac{z\kappa}{m^2+z\kappa}.
\]

Its lattice decay length does not depend on temporal spacing and is of order $\sqrt{\kappa/m^2}$ in physical units when the spatial mesh is fine. Spatial continuum limits and ultraviolet renormalization are outside this result.

With physical Fourier normalization $\widehat F=\sqrt a\,F_N=(a/\sqrt T)\sum_t e^{-i\omega t}X_{t,x}$, full-spatial-slice anchors obey

\[
\|\widehat F-\widehat F^0\|_2
\le\frac{rB_a}{m^2\sqrt T}
=O\!\left(\frac{ra}{\sqrt T}\right).
\]

At fixed $T=\beta$, an order-one physical Fourier-amplitude correction requires $ra\not\to0$, equivalently $r/N\not\to0$. For this full-slice geometry and normalization, positive temporal anchor density is necessary to keep the comparison envelope from vanishing. The first-order result says this is still insufficient for the independent source.

For a fixed physical Fourier mode and finite spatial cutoff, $a\,v^*K_a^{-1}v=O(1)$. The second-moment inequality in Section 2 then shows that $ra\to0$ also forces the physical response-covariance change $a|\mathbb E|F_N|^2-\mathbb E|F_N^0|^2|$ to vanish.

If the target interval also grows, the same envelope allows $r\asymp\sqrt T/a$, with fraction $r/N\asymp1/\sqrt T\to0$, to remain order one. Positive density is therefore not a uniform necessity across continuum and long-target limits. One anchor per slice near one known spatial readout has the same temporal scaling with $1/m^2$ replaced by the corresponding massive spatial Green value; total space-time density can then vanish as spatial volume grows. Neither statement certifies the cross-mode thermal law.

The grid check uses $m=\lambda=\beta=1$, $a=1/16,1/32,1/64$, and $T=1,4,16$. At $T=1$, $c_{a,T}$ moves from $1.0815985$ to $1.0819531$ toward $c_T=1.0819767$; at $T=16$, it moves from $0.4997562$ to $0.4999849$ toward $c_T=0.5000001$. It also confirms $B_a\propto a$ and anchor fractions $1,1/2,1/4$ for $r=\sqrt T/a$. These values validate discretization algebra and the moment envelope only; they are not quantum response measurements.

## 7. Resource and comparator audit

For $N$ temporal sites and $M=|\Lambda|$ spatial sites, a local update costs $O(NM)$ arithmetic per sweep, before mixing, effective sample size, precision, and verification. Updating a source on $r$ complete slices costs at least $O(rM)$ source-coordinate work per draw. At fixed physical $T=\beta$, avoiding a vanishing amplitude envelope requires $r=\Theta(N)$, so the sparse-slice arithmetic advantage disappears. On a growing target interval, $r=\Theta(\sqrt T/a)$ is a sublinear temporal fraction, but the independent-source first-order mismatch remains; a coherent source mode has its own correlation and preparation cost.

One random site per slice costs $O(N)$ source coordinates, while its local geometric exposure scales as $\sqrt N/M$ at fixed cutoff. Extending this to every local output requires spatial coverage and can restore an $O(NM)$ acquisition cost. Source autocorrelation, cross-moment estimation, thermal preparation, and uncertainty in the shared source are additional. No equal-input, equal-accuracy speedup is demonstrated.

The strongest same-information comparator here is the exact first-order thermal coefficient: it uses the same $H,\beta,\lambda$ and mode $q$, and it falsifies the anchor update before sampling error matters. Direct imaginary-frequency, direct-frequency diagrammatic, and certified spectral-function methods are listed in the supplied source report; they were not rerun or benchmarked here. The one-loop contraction already contains the missing $c_\beta$; using it is a perturbative correction, not a new all-coupling solver.

## 8. Validation and claim limits

The new **geometry_checks.py** implementation does not import or execute the supplied producer code. It checks:

- exact rational nonnegativity, row sum, and walk-decay bound for a 13-cycle massive Green matrix;
- exact rational moving-anchor and random-placement exposure formulas at $N=100,400,1600$;
- exact rational common-mode and iid source-variance scalings in the linear comparator;
- the finite Lyapunov identity for three nonuniform masks and every Fourier mode, with maximum floating-point discrepancy $1.25\times10^{-16}$;
- finite-spacing convergence and anchor scaling in the one-dimensional harmonic-action grid.

The analytic claims above are proved directly; the finite checks are consistency witnesses. The supplied report's deterministic oscillator and $64^3$-lattice calculations remain source-derived and were not independently replayed. No original research script was executed. No physical device, complete thermal response solver, or priority review is claimed.

The broad loss of boundary influence for positive massive Green functions is established mathematical territory. The contribution here is the geometry- and covariance-resolved scope boundary: moving or random anchors can preserve or erase influence depending on Green exposure, while the independent replacement source misses the needed thermal cross-moment at first order. The surviving operation is temperature-correct cross-moment acquisition; its cost and feasibility remain open.
