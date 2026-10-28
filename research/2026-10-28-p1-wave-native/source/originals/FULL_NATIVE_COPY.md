**I constructed a compatible positive current, auxiliary equation, corrected energy, and physical calibration for a class of nonflat variable-coefficient waves. I then closed its initial-energy and wall-flux budgets, extended positive current conservation beyond quadratic coefficients, and proved two obstructions that constrain the next mechanism.**

**This does not yet prove a new sharp physical local-smoothing estimate.** The remaining difficulty is now explicit: recovering physical concentration from the enlarged lift while paying—or finding a different way around—the resolving-window cost and the rigidity of the positive auxiliary background.

The proofs and executed programs are saved:

- [Astra_P1_Curved_Wave_Proofs.pdf](https://chatgpt.com/library?file_id=libfile_cb0c4eb48c8881919ea3e8de75ff89f8&account_id=personal) — **117 pages, 24 proof chapters**, including the construction, counterexamples, independent derivations, and literature comparison.
- [Astra_P1_Wave_Machinery_20261027.zip](https://chatgpt.com/library?file_id=libfile_c78611fcb3388191a4cc92c3aba3ed91&account_id=personal) — **108 files**, containing all research notes, acquired sources, actual programs, and their outputs. **All 31 executable checks pass.**

## 1. The obstruction and the change of mechanism

I began with the manuscript’s actual lifted-current construction. Spatially varying pencil coefficients introduce a concrete defect before any concentration estimate is attempted.

Writing the original imaginary displacement schematically as
\[
q^\nu(x,w)=\frac12\sum_l w_l^{T}C_\nu(x)w_l,
\qquad
\psi^\nu=x^\nu-iq^\nu,
\]
the naive lifted differentiation gives
\[
D_{la}\psi^\nu
=(C_\mu w_l)_a\,\partial_\mu q^\nu.
\]
This vanishes for the constant pencils in Appendix E and generally survives when the coefficients vary.

Correcting the graph vector fields repairs their annihilation of \(\psi\). It does **not** automatically repair the mixed conjugate accelerations responsible for current conservation. The archive contains an explicit variable symmetric pencil with a constant physical solution whose naive positive lifted current has nonzero divergence. The defect lies outside the current’s range, which also rules out repairing that example by multiplying the current by a positive scalar weight.

The successful construction changes the lift and the determinant calculus. It retains velocity as an auxiliary spatial coordinate and identifies an exact conserved null-phase coordinate. This produces a real Monge–Ampère energy on the enlarged space. The additional dimension and calibration costs remain part of the result.

### The wave class

The principal completed construction concerns
\[
g=2\,dt\,dU+|dq|^2-q^T K(t)q\,dt^2,
\qquad K(t)=K(t)^T,\quad q\in\mathbb R^d.
\]

Here \(K\) may be anisotropic and matrices at different times may fail to commute. The physical wave coefficients vary in \(q\), and the physical curvature is nonzero when \(K\ne0\). This is a Lorentzian plane-wave class with a null coordinate \(t\); it is not a theorem for arbitrary Riemannian wave operators.

For a compact positive null-frequency band,
\[
\Phi(t,U,q)
=(2\pi)^{-1/2}\int e^{i\rho U}\psi_\rho(t,q)\,d\rho,
\]
the equation becomes
\[
i\partial_t\psi_\rho
=-\frac1{2\rho}\Delta_q\psi_\rho
+\frac{\rho}{2}q^TK(t)q\,\psi_\rho.
\]

The proofs use smooth band-limited null-frequency data with sufficient transverse decay, and explicitly add a transported positive regularizer when the auxiliary Dirichlet problem needs a strictly positive density.

## 2. A coherent current and an exactly passive background

The associated classical flow is
\[
q'=v,\qquad v'=-Kq,\qquad
U'=\frac12(q^TKq-|v|^2).
\]
Consequently
\[
\boxed{W=U+\frac12q\cdot v}
\]
is exactly conserved.

Propagating the field and its analyzing window by the same quadratic Schrödinger evolution gives an exact coherent transform. After unitary dilations, **all positive-frequency amplitudes evolve in one common Hilbert space**. They are summed before applying the positive quadratic form that produces the density.

For a positive transported window operator \(\Gamma_t\), the resulting density is
\[
\mu(t,W,q,v)
=\langle \mathcal F(t,W,q,v),\Gamma_t\mathcal F(t,W,q,v)\rangle,
\]
where \(\mathcal F\) contains the full frequency integral. Thus the construction retains the off-diagonal frequency interference. It satisfies
\[
\partial_t\mu+v\cdot\nabla_q\mu-Kq\cdot\nabla_v\mu=0.
\]

On the enlarged spatial base
\[
x=(q,v,W)\in\mathbb R^{2d+1},
\]
define
\[
B(t)=
\begin{pmatrix}
0&I&0\\
-K&0&0\\
0&0&0
\end{pmatrix},
\qquad
M(t)=
\begin{pmatrix}
K&0&0\\
K'&K&0\\
0&0&0
\end{pmatrix}.
\]
Then
\[
B'+B^2=-M,\qquad \operatorname{tr}B=0.
\]

The lift uses the explicitly constructed torsion-free affine connection
\[
\Gamma^i_{00}=(Mx)^i,
\]
with other coefficients zero. For
\[
V=(1,Bx)=(1,v,-Kq,0),
\]
we have \(\nabla_VV=0\). Therefore
\[
\boxed{
A=\mu\,V\otimes V\ge0,
\qquad
\operatorname{div}_\nabla A=0.
}
\]

This connection is curved:
\[
R^i{}_{0j0}=M^i{}_j.
\]
It is the connection used by the auxiliary energy; it is distinguished throughout the proofs from the physical spacetime’s Levi-Civita connection.

The passive background is also constructed:
\[
\boxed{
b=\frac{\Lambda}{2}W^2,\qquad
H_\nabla b=\Lambda\,dW\otimes dW,\qquad
A:H_\nabla b=0.
}
\]

The density still depends on \(W\), carrying null-frequency interference. Passivity means that the current direction annihilates the background Hessian. It does not require discarding that dependence.

## 3. The auxiliary energy closes, including its wall terms

The cancellation that makes this lift useful is valid even for the generally nonsymmetric matrix \(M\).

For
\[
H_\nabla\phi
=D^2_{t,x}\phi-((Mx)\cdot\nabla_x\phi)E_{00},
\qquad D=D_x^2\phi,
\]
the exact identities are
\[
\operatorname{div}_\nabla\operatorname{cof}(H_\nabla\phi)
=
\left(0,-\operatorname{cof}(D)M^T\nabla_x\phi\right),
\]
and
\[
\boxed{
\operatorname{divdiv}_\nabla\operatorname{cof}(H_\nabla\phi)
=-(\operatorname{tr}M)\det D.
}
\]

The first divergence retains anisotropy. The second divergence reduces it to the trace. This provides the needed integrated cancellation without requiring pointwise cofactor conservation.

On suitable moving spherical fibers, solve
\[
D_x^2(b+u)>0,\qquad
\det D_x^2(b+u)=\Lambda\mu,\qquad
u|_{\partial\Omega_t}=0.
\]
An explicit strictly convex subsolution verifies the hypotheses of the classical smooth real Monge–Ampère Dirichlet theory. The existence assertion is therefore tied to an established theorem and a checked interface. [math.jhu.edu](https://math.jhu.edu/~js/Math742/cns1.pdf?utm_source=chatgpt.com)

Define
\[
X=\int_{\Omega_t}(-u)\mu,
\]
\[
E=\Lambda^{-1}\int_0^1\int_{\Omega_t}
u\,\det D_x^2(b+\theta u)\,dx\,d\theta,
\qquad F=X+E.
\]
The rank-one background gives
\[
\boxed{
\frac d{d+1}X\le F\le
\frac{2d+1}{2d+2}X,\qquad E\le0.
}
\]

The complete energy identity is
\[
\boxed{
F''+\int_{\Omega_t}A:\Sigma
=
B_A-B_C+2(\operatorname{tr}K)E,
}
\]
where \(\Sigma\ge0\) is the positive Schur completion of the endpoint Hessian, \(B_A\) is the current wall flux, and \(B_C\) is the cofactor wall flux.

Both fluxes use the **full moving spacetime normal**, including its time component. For
\[
\Omega_t=\{|x|^2<R^2\cos(\omega t)\},
\]
a sufficient bound on \(\omega^2\) in terms of \(\lambda_{\max}(\operatorname{sym}M)\) makes \(B_C\ge0\). Hence, when \(\operatorname{tr}K\ge0\),
\[
F''+\int A:\Sigma\le B_A.
\]
A negative trace has an explicit finite comparison cost.

### The wall flux is bounded for the actual coherent density

Retaining \(W\) dependence matters here. A previous estimate obtained by extending a density constantly in an appended passive coordinate cannot be reused unchanged.

For
\[
a(t)=\cos(\omega t)>0,\qquad
C=\frac12\|\mu\|_\infty^{1/(2d)},\qquad
m_0=\int\mu,
\]
and
\[
J(t)=\int\mu\bigl(|v|^2+|Kq|^2\bigr),
\]
the direct full-space coarea calculation proves
\[
\boxed{
\frac1{R_0}\int_{R_0}^{2R_0}B_{A,R}(t)\,dR
\le
8C\left[
R_0^2\frac{a'(t)^2}{a(t)}m_0+J(t)
\right].
}
\]

One **fixed radius**, selected after integration over the time interval, therefore has a finite budget for corrected energy, positive dissipation, cofactor-wall flux, and the favorable curvature term. The operator construction below supplies the required mass, supremum, and moment bounds. No moment in \(W\) is needed.

This closure consumes a density supremum. Its energy-only bound also follows from the comparison barrier; its additional content is the positive dissipation and wall budget. I have not relabeled it as a sharp frequency gain.

### A nonflat vacuum special case

Take
\[
K(t)=
\begin{pmatrix}
1&t\\
t&-1
\end{pmatrix},
\qquad |t|\le\frac14.
\]
Direct calculation gives
\[
\operatorname{Ric}=0,\qquad
R^{q_1}{}_{tq_1t}=1,
\]
and
\[
[K(s),K(t)]
=
2(t-s)
\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

Thus this four-dimensional physical background is nonflat, Ricci-flat, and has noncommuting curvature profiles. The explicit choice \(\omega^2=5/2\) gives favorable walls. Its corrected energy has **zero curvature bulk term** because \(\operatorname{tr}K=0\).

This is a concrete curved propagation case for the complete construction.

## 4. The resolving operator is explicit—and its free cost is sharp in order

The physical recovery map was a major remaining obligation. A conserved positive density is useful only if it controls a specified wave observable.

For the Gaussian \(g_L\) in the common rescaled Hilbert space, the finite projection calculation proves
\[
\boxed{
\|P_{N,M}\Phi_t\|_{L^p_{U,q}}
\le
C\left(\frac LN\right)^{d(p-2)/(4p)}
\|\sqrt{\mu_t}\|_{L^p_{W,q,v}},
\qquad
\frac{M^2}{NL}\lesssim1.
}
\]
Here \(P_{N,M}\) is an explicit cutoff to null frequency comparable to \(N\) and transverse frequency at most \(M\). The proof does not assume that quadratic propagation preserves exact transverse Fourier support. For \(M\asymp N\), take \(L\asymp N\).

To make this calibration valid throughout an interval, I constructed a positive operator covering the entire backward resolving-window orbit.

Remove its scalar phase and parametrize the normalized orbit by Hilbert arclength:
\[
h(s),\qquad 0\le s\le\ell,\qquad \|h'(s)\|\le1.
\]
Extend it constantly to \(\ell+1\), then set
\[
\boxed{
\Gamma_0
=
2\int_0^{\ell+1}
\left(
|h(s)\rangle\langle h(s)|
+
|h'(s)\rangle\langle h'(s)|
\right)\,ds.
}
\]

A one-sided Sobolev inequality proves
\[
\Gamma_0\ge |h(s)\rangle\langle h(s)|,
\qquad
\operatorname{tr}\Gamma_0\le2+4\ell.
\]
This is an explicit object, with an elementary domination proof.

For
\[
H_K(t)=\frac12P^2+\frac12Q^TK(t)Q,
\]
Gaussian variance computes the orbit speed exactly:
\[
\|\dot h(t)\|^2
=
\operatorname{Var}_{g_L}H_K(t)
=
\frac18\left\|LI-\frac{K(t)}L\right\|_F^2.
\]
Therefore
\[
\boxed{
\Gamma_t\ge |g_L\rangle\langle g_L|,
\qquad
\operatorname{tr}\Gamma_0
\le
2+\sqrt2\int_I
\left\|LI-\frac{K(t)}L\right\|_Fdt.
}
\]

The coherent density made from this operator has exact mass
\[
\int\mu=\operatorname{tr}\Gamma_0\,\|\Phi_0\|_2^2.
\]
Its derivative windows are pure second Hermite excitations. That fact gives explicit second-moment bounds; at \(L=N\ge1\), the physical window moments add **no further frequency power beyond the trace cost**.

### A lower bound for every positive transported window operator

The cost cannot be removed merely by replacing Gaussian mixtures with more general positive windows.

Already in one free transverse dimension, suppose
\[
U_t=e^{-itP^2/2},
\qquad
g_N(q)=(N/\pi)^{1/4}e^{-Nq^2/2},
\]
and a positive trace-class operator satisfies
\[
U_t\Gamma_0U_t^*
\ge\beta|g_N\rangle\langle g_N|
\]
throughout an interval of length \(T\). Then
\[
\boxed{
\operatorname{tr}\Gamma_0
\ge
\frac{\beta}{\sqrt\pi e^4}
\left(
\left\lfloor\frac{NT}{2\pi}\right\rfloor+1
\right).
}
\]

The proof is decisive. In the energy variable \(E=p^2/2\), a bounded multiplier turns samples of the backward Gaussian orbit into
\[
f_j(E)
=
N^{-1/2}e^{it_jE}\mathbf1_{[N,2N]}(E),
\qquad
t_j=t_0+\frac{2\pi j}{N}.
\]
These vectors are exactly orthonormal. Summing their diagonal expectations against the positive filtered operator gives the trace lower bound.

Together with the upper construction, this establishes the order
\[
\boxed{\text{required positive-window trace}\asymp 1+NT}
\]
for fixed-strength universal pointwise calibration in the free one-dimensional case.

Its scope is precise: it constrains positive operator domination on the whole Hilbert space. It does not rule out local smoothing, derivative-assisted calibration, restricted amplitude classes, or other interference-preserving constructions.

## 5. Two further limits prevent a premature smoothing claim

### Global lifted norms are conserved

The lifted density moves by
\[
(W,z)\longmapsto (W,S(t,t_0)z),
\]
which preserves volume. Therefore
\[
\|\mu_t\|_{L^r(W,q,v)}
=
\|\mu_{t_0}\|_{L^r(W,q,v)}.
\]

The physical wave’s focusing is encoded in projection and calibration from this larger space. Global phase-space transport alone supplies no time-averaging gain. A stronger estimate must exploit that projection or a more selective concentration functional.

### The positive quadratic background cannot simply gain velocity directions

I also classified every time-dependent quadratic background
\[
b(t,x)=\frac12x^TP(t)x+l(t)^Tx+c(t)
\]
whose covariant Hessian is positive semidefinite and exactly annihilates the phase current.

Positivity and the null pairing force \(H_\nabla b\,V=0\). The coefficient equations then give
\[
P'=-PB,\qquad PB=B^TP,\qquad M^TP=0,
\]
together with the corresponding linear and constant conditions.

If \(K\) is invertible **even at one time** in the connected interval, the complete family is
\[
\boxed{
b=\frac\alpha2W^2+\beta W+\gamma t+\delta,
\qquad \alpha\ge0.
}
\]
Its Hessian has rank at most one.

This proof does not assume that \(b\) itself is transported. It rules out a specific shortcut: treating the added position or velocity directions as quadratically passive while retaining positivity and exact annihilation in this connection. The flat case admits higher-rank passive velocity backgrounds, so the curvature hypothesis has real content.

Nonquadratic backgrounds, controlled nonzero pairings, and different lifts remain available directions.

## 6. Beyond quadratic coefficients: an exact positive completion

For
\[
g=2dt\,dU+|dq|^2-2V(t,q)dt^2,
\]
the local Gaussian evolution has an exact residual built from
\[
R_3V(t,q,r)
=
V(t,q+r)-V(t,q)-\nabla V(t,q)\cdot r
-\frac12r^TD_q^2V(t,q)r.
\]

The coherent transport residual satisfies
\[
\|\mathscr R\|_2
\le
C_d\|D_q^3V\|_\infty
N^{-1/2}L^{-3/2}\|\Phi\|_2.
\]
At the full recovery scale \(L=N\), this is \(O(N^{-2})\), with the derivative norm retained.

The key repair is a reusable amplitude-residual lemma. If
\[
Da+\mathcal A a=b,\qquad \mathcal A^*=-\mathcal A,
\]
and
\[
T=\int\|a\|^2W\otimes W,\qquad
R=2\operatorname{Re}\int\langle a,b\rangle W,
\qquad e=\int\|b\|^2,
\]
then
\[
\boxed{
R\in\operatorname{range}T,\qquad R^TT^+R\le4e.
}
\]

Thus singularity of the positive tensor does not force division by an uncontrolled smallest eigenvalue. With one added coordinate \(s\), construct
\[
\widetilde T=
\begin{pmatrix}
T&-sR\\
-sR^T&d_0+s^2\operatorname{div}R/2
\end{pmatrix}.
\]
An explicit smooth choice of \(d_0\) makes
\[
\boxed{\widetilde T\ge0,\qquad
\operatorname{div}\widetilde T=0.}
\]
The original time density is unchanged. The additional face flux is charged explicitly.

A second transport identity controls \(\operatorname{div}R\) using third and fourth spatial derivatives, a third spatial/time derivative, and propagated position/momentum budgets. At \(L=N\), the resulting integrated **scalar** completion budget is \(O(N^{-1})\). This is not a smallness claim for every component of the enlarged tensor; polarization velocities can be large.

The general-potential affine connection is constructed explicitly in the proofs. The remaining open interface is an effective auxiliary determinant energy for that completed current.

There is also a limited coupled-field extension: spatially uniform Hermitian mixing under a common scalar principal wave operator is absorbed by unitary evolution, while spatial variation produces a quantified residual. Arbitrary matrix principal symbols and nonlinear interacting fields remain outside the proved scope.

## 7. Failed repairs were resolved into explicit formulas and counterexamples

The natural velocity-integrated current is conserved on the physical Brinkmann spacetime. Its auxiliary energy, however, differs from the enlarged phase-space energy.

The complete calculation gives
\[
F''+\int A:\Sigma
=
B_A-B_C+(\operatorname{tr}K)E-2J'+L-Q,
\]
where \(J,L,Q\) are explicit null-gradient segment integrals.

I derived these terms independently and checked them in moving-domain examples where they do not vanish. A proposed compact-variation simplification fails on a Dirichlet wall: the executed example has the exact nonzero boundary gap
\[
\frac{83\pi}{6480}.
\]
That simplification was rejected; the raw identity retains the derivative boundary terms.

A useful special case survives. Rank-one curvature and actual evenness of the density in \(U\) eliminate all three corrections. An oscillator ground-state superposition over a smooth null-frequency band realizes the hypotheses while retaining genuine cross-frequency interference. This supplies a check on the full spacetime mechanism, while the principal construction allows arbitrary symmetric \(K(t)\) by changing the lift.

## 8. Literature, novelty, and physical consequence

The literature comparison changes which claims are defensible. In three spatial dimensions, the relevant critical full-gain thresholds are different:

| Geometry | Critical exponent relevant to the comparison |
|---|---:|
| Euclidean wave target in the supplied construction | \(3\) |
| General positive-cone/Riemannian wave problem | \(10/3\) |
| General mixed-sign cinematic-curvature FIO problem | \(4\) |

Beltran–Hickman–Sogge’s variable-coefficient result and the January 2026 Gan–He–Li–Wu revision distinguish these settings. The latter reaches the sharp general-manifold range in odd dimensions. I also checked the October 2026 even-dimensional refinement and its additional quadratic-cone hypothesis. [arxiv.org](https://arxiv.org/abs/1801.06910?utm_source=chatgpt.com)

The Minicozzi–Sogge examples show how curved geodesic families compress in ways excluded by the Euclidean geometry. [arxiv.org](https://arxiv.org/abs/math/9912202?utm_source=chatgpt.com) Starting from that example, I derived a small compact extension with a strictly convex escape function. It is globally nontrapping while preserving the local compression. Thus small smooth perturbation plus nontrapping does not justify the arbitrary-background Euclidean claim.

The targeted search of OpenAI’s remaining release did not reveal a complete spatially variable replacement. That was bounded coverage, not an exhaustive absence claim.

Historical attribution also matters. Metaplectic propagation, Gaussian polarizations, quadratic approximation, and classical Monge–Ampère solvability are established ingredients. Holland–Sparling’s 2026 plane-wave work already develops the relevant representation and imaginary-polarization structures. Those ingredients are reused here. [arxiv.org](https://arxiv.org/abs/2603.28206?utm_source=chatgpt.com)

The distinctions are:

| Question | Present result |
|---|---|
| **Proved mathematical scope** | Explicit coherent current, passive background, real auxiliary energy, calibration, and finite budgets for the curved quadratic class; positive current completion beyond it. |
| **Historical novelty** | The combinations and identities have been derived and checked here. Priority has not been established by exhaustive literature search or external review. |
| **Physical consequence** | A rigorous concentration instrument for structured curved propagation, including a nonflat vacuum example, and a quantified route toward limited mode mixing. No improved focusing, controllability, or other physical capability has yet been demonstrated. |

## Provenance, verification, and continuation

The OpenAI source was pinned to
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`.
The supplied PDF matched Git blob
`0472605895a485dd0441ada1257485d325f16f55`.
The work used the actual current and energy construction, including the relevant quaternionic and constant-pencil appendices; a separate check verifies the source-specific fourth-column conservation identity.

Astra was read selectively, beginning with `00_START_HERE.txt`, at revision
`e1e2272165c8548326c31bb11817c28f871d21e9`.
The relevant governing passages are preserved with the proofs.

The acquired prior quantum-control native summary and source receipt are also preserved. **The receipt states that the original proof/program archive was not acquired; those missing originals have not been recovered or represented as reverified.** The wave arguments do not import the old control assumptions.

The 31 checks include exact rational polynomial identities, moving-boundary balances, nonreal quaternionic Hessians, noncommuting profiles, the Ricci-flat example, operator calibration, and passive-background classification. Numerical Gaussian and coherent-state checks supplement the analytic proofs. The checks rerun with:

```bash
python3 research/run_all_checks.py
```

**The strongest continuation is now a specific mathematical problem:** construct a concentration or calibration functional that uses coherent polarization dependence, its Gaussian heat identities, or the explicit null-gradient energy corrections to control the physical projection. It must account for the proved \(NT\) positive-window cost, retain the true moving-wall terms, and avoid assuming additional quadratic passive directions that curvature forbids. For nonquadratic coefficients, it must also preserve the residual and completion bounds already established.

That is the remaining mechanism needed to turn this constructed instrument into a stronger physical wave estimate.