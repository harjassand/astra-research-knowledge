**I have not established a full affirmative compiler or an all-control impossibility theorem for this extension.** Taking your compiler for the endpoint \((V,H)\) as an accepted premise, the new arbitrary-\(\Pi\) magnetic-writing step remains unresolved in this analysis.

There is concrete progress beyond the supplied commutator algebra: an exact shear-and-positive-heat calculation produces the noncommuting response singled out in your question, uniformly over unknown positive resistivity profiles. There is also a useful way to formulate preservation of previously written magnetic memory during velocity operations. But neither provides the missing uniformly stable writer for an arbitrary matrix field.

The distinction matters here. A collection of operators whose actions on **constant fields** span the desired Fourier coefficients does not yet give an operation with controlled action on the **whole evolving magnetic field**. I explain that gap below, including the calculations that survive scrutiny.

## 1. The target is well conditioned as an abstract operator

Write
\[
\Psi=\Pi-I,\qquad P_0B=\int_{\mathbb T^3}B(x)\,dx.
\]
Consider the field-space operator
\[
\mathcal N_\Psi B=\Psi(x)P_0B,
\qquad
\mathcal T_\Psi=I+\mathcal N_\Psi .
\]

The target assumptions give
\[
P_0\Psi=0,\qquad \operatorname{div}(\Psi e_j)=0.
\]
Consequently,
\[
\mathcal N_\Psi^2=0,\qquad
\mathcal T_\Psi^{-1}=I-\mathcal N_\Psi.
\]
Both operators preserve divergence and magnetic mean. Moreover,
\[
\|\mathcal N_\Psi B\|_{H^1}
\le \|\Psi\|_{H^1}|P_0B|
\le \|\Psi\|_{H^1}\|B\|_{L^2},
\]
so
\[
\|\mathcal T_\Psi^{\pm1}\|_{H^1\to H^1}
\le 1+\|\Psi\|_{H^1}
\le 1+K+\sqrt3.
\]

For every constant \(H\) and every mean-zero error \(e\),
\[
\boxed{\mathcal T_\Psi(H+e)=\Pi H+e.}
\tag{1}
\]

Thus pointwise singularity of \(\Pi\), noncommuting columns, or a changing sign of \(\det\Pi\) does **not** create an inherent conditioning problem for the desired transformation on the space of fields. The map in (1) is globally invertible and preserves the mean-zero error exactly.

This is an abstract operator calculation. It does not realize \(\mathcal T_\Psi\) through the admitted mechanical force. In particular, inserting \(\Psi P_0B\) into the induction equation would introduce an unauthorized magnetic term. What is missing is a mechanical construction that produces the same effect, or another equally stable transformation, through the actual coupled dynamics.

### Target truncation remains polynomial

The variable Fourier encoding does not obstruct this abstract reduction. With
\[
N=\left\lceil C\,MK/\epsilon\right\rceil
\]
for a sufficiently large fixed constant, Fourier truncation gives
\[
\|(\Pi-\Pi_N)H\|_2+\|V-V_N\|_2\le \epsilon/8
\]
uniformly for \(|H|\le M\).

For each fixed integer \(m\ge1\),
\[
\|\Pi_N\|_{H^m}+\|V_N\|_{H^m}
\le C_m K(1+N)^{m-1},
\]
and fixed-order spatial supremum norms have polynomial bounds as well. The retained catalogue contains \(O(N^3)\) frequencies. Frequencies outside the cutoff can be discarded by exact integer comparisons on the input list.

These observations pay for the finite target representation and smooth reference bounds. They do not pay for magnetic writing.

## 2. An exact positive-heat calculation produces the noncommuting example

Here is a calculation that goes beyond a single ideal-flow response and avoids any inverse heat or evaluation of the actual resistivity.

Set \(\kappa=2\pi\), choose an integer \(Q\ge1\), and define
\[
F=e_3\sin(\kappa Qx_1),\qquad
G=e_2\sin\bigl(\kappa(-Qx_1+x_3)\bigr).
\]
Let \(\mathcal M_F(\alpha)\) and \(\mathcal M_G(\beta)\) denote their ideal induction maps with impulses \(\alpha,\beta\).

Starting from a constant magnetic field,
\[
\mathcal M_F(\alpha)H
=
H+\alpha\kappa QH_1e_3\cos(\kappa Qx_1).
\]

Every field in this expression is independent of \(x_2\). Therefore the spatial pullback in the \(G\)-map acts trivially on it, and the stretching term can be evaluated exactly:
\[
\begin{aligned}
\mathcal M_G(\beta)\mathcal M_F(\alpha)H
={}&H
+\alpha\kappa QH_1e_3\cos(\kappa Qx_1)\\
&+\beta\kappa(-QH_1+H_3)e_2
       \cos\bigl(\kappa(-Qx_1+x_3)\bigr)\\
&+\theta H_1e_2\cos(\kappa x_3)\\
&+\theta H_1e_2
       \cos\bigl(\kappa(-2Qx_1+x_3)\bigr),
\end{aligned}
\tag{2}
\]
where
\[
\theta=\frac{\alpha\beta\kappa^2Q}{2}.
\]

The desired response
\[
\Pi_\theta(x)H
=
\bigl[I+\theta\cos(\kappa x_3)e_2e_1^T\bigr]H
\tag{3}
\]
is the only low-frequency fluctuation in (2). Every other fluctuation has frequency at least \(Q\).

Now apply positive heat for a duration \(t\). For an arbitrary unknown resistivity profile satisfying
\[
\rho_-\le \rho(s)\le1,
\]
put
\[
d=\int_0^t\rho(s)\,ds.
\]
Then
\[
\rho_-t\le d\le t,
\]
and the heat propagator is exactly \(e^{d\Delta}\). The four nonconstant terms in (2) receive the respective factors
\[
e^{-\kappa^2Q^2d},\quad
e^{-\kappa^2(Q^2+1)d},\quad
e^{-\kappa^2d},\quad
e^{-\kappa^2(4Q^2+1)d}.
\]

It follows that
\[
\begin{aligned}
&\left\|
e^{d\Delta}\mathcal M_G(\beta)\mathcal M_F(\alpha)H
-\Pi_\theta H
\right\|_2\\
&\qquad\le
CM\left[
|\theta|t+
\bigl(Q(|\alpha|+|\beta|)+|\theta|\bigr)
e^{-c\rho_-Q^2t}
\right].
\end{aligned}
\tag{4}
\]

The choices can be made uniformly without knowing \(d\):

- Take \(t\le \epsilon/[CM(1+|\theta|)]\), within the available time.
- Take \(\alpha=1\).
- Approximate \(2\theta/(\kappa^2Q)\) by a rational \(\beta\) to the required accuracy.
- Take \(Q\) polynomially large in \(M,1+|\theta|,\rho_-^{-1},t^{-1},\epsilon^{-1}\).

For example, a sufficiently large fixed multiple of \(Z^4\), where
\[
Z=2+M+|\theta|+\rho_-^{-1}+t^{-1}+\epsilon^{-1},
\]
suffices. The exponential tail can be certified by an elementary bound such as \(e^{-x}\le2x^{-2}\). Rational approximation of \(\kappa^{-2}\) has ordinary finite-bit cost.

The columns in (3) do not commute when \(\theta\ne0\):
\[
C_1=e_1+\theta\cos(\kappa x_3)e_2,\qquad C_3=e_3,
\]
and
\[
[C_1,C_3]
=\theta\kappa\sin(\kappa x_3)e_2.
\]

**What this proves:** positive diffusion permits a resistivity-blind passive reference construction beyond a single ideal transported frame. The argument does not even require temporal Lipschitz regularity during the heat interval.

**What remains unpaid:** (2) uses ideal induction maps at higher spatial frequencies, followed by assigned heat evolution. A physical implementation must generate those operations with the twelve mechanical actuators, control Lorentz feedback, preserve the needed velocity bounds, and tolerate rough disturbances. Those requirements are not consequences of (4).

In particular, compressing a shear in time does not reduce its integrated strain. For the first shear above, that strain is of order \(Q\). A generic energy comparison would therefore give an exponential factor in \(Q\). That estimate is not a lower bound or an impossibility result, but I have not replaced it here by the polynomial coupled estimate required for this operation.

## 3. Why actions on constants do not add up to an arbitrary writer

Suppose a proposed operation has the expansion
\[
T_j=I+\delta A_j+O(\delta^2).
\]
Knowing \(A_jH\) for constants does not determine its effect after earlier operations. Indeed,
\[
T_2T_1H
=
H+\delta(A_1+A_2)H+\delta^2A_2A_1H+\cdots.
\tag{5}
\]
The term \(A_2A_1H\) acts on the magnetic fluctuation already created by the first operation.

Repeating small operations does not automatically remove this issue. It generally approaches an evolution generated by the \(A_j\), whose action on constants need not be the desired additive sum. The construction needs either a stable global design for the entire response matrix or an operation that selectively uses the conserved mean.

A useful candidate class makes the difficulty explicit. For a constant vector \(p\) and a smooth scalar function \(\phi\), define
\[
\mathcal G_{p,\phi}B
=
\operatorname{curl}\!\left(\phi\,p(p\cdot B)\right).
\tag{6}
\]
Since
\[
p\cdot\mathcal G_{p,\phi}B=0,
\]
one has, on smooth fields,
\[
\mathcal G_{p,\phi}^2=0.
\]
Thus its formal transformation is
\[
I+\mathcal G_{p,\phi},
\qquad
(I+\mathcal G_{p,\phi})^{-1}=I-\mathcal G_{p,\phi}.
\]

On constants,
\[
\mathcal G_{p,\phi}H
=
(\nabla\phi\times p)(p\cdot H).
\tag{7}
\]
On a general field, however,
\[
\mathcal G_{p,\phi}B
=
(\nabla\phi\times p)(p\cdot B)
+\phi\,\nabla(p\cdot B)\times p.
\tag{8}
\]
The second term differentiates the previously written magnetic memory.

There is also a rough-data issue: \(\mathcal G_{p,\phi}\) is generally unbounded \(H^1\to H^1\). For instance, with \(p=e_1,\phi=1\),
\[
\mathcal G_{e_1,1}B
=
(0,\partial_3B_1,-\partial_2B_1).
\]
Taking \(B=e_1\sin(\kappa n x_2)\) makes the ratio
\[
\frac{\|\mathcal G_{e_1,1}B\|_{H^1}}{\|B\|_{H^1}}
\]
grow proportionally to \(n\).

This does not obstruct a construction using smoothing or physical frequency separation. A finite Fourier cutoff would make the operator bounded with a polynomial norm. But that cutoff, its approximation error, and its physical realization must themselves be supplied. Formal nilpotence alone does not provide a robust operation on the admitted \(H^1\) ball.

### Positive diffusion and unknown resistivity introduce separate obligations

The supplied double-commutator identity resolves a spanning calculation. A usual group-commutator realization involving \(D\), however, would contain a negative diffusion-time factor. That factor is unavailable.

Positive conjugated heat operations offer alternatives, but their implementation must establish:

1. the desired signed effect without inverse heat;
2. uniform accuracy for every admitted \(\rho(t)\);
3. controlled action on existing magnetic memory;
4. polynomial amplification bounds for rough errors;
5. realization through the actual momentum equation with twelve actuators.

The example in Section 2 addresses the first two issues for one response, at the passive reference level. It does not settle the remaining three or extend to arbitrary \(\Pi\).

## 4. Preserving smooth magnetic memory during velocity operations

There is a useful extension of the reference calculations behind the accepted velocity machinery.

Suppose a known smooth matrix field \(\Sigma(x)\) represents the intended magnetic memory:
\[
B_{\rm mem}=\Sigma(x)H.
\]
During a closed velocity word \(w\), use the proof reference
\[
B_*(t)=\mathcal M_w(t)(\Sigma H).
\tag{9}
\]
If the underlying ideal induction map returns to the identity, then
\[
B_*(t_{\rm end})=\Sigma H
\tag{10}
\]
for every \(H\), without evaluating \(H\).

Write the velocity reference as \(u_*=w+v\), where \(v\) includes the actual-viscosity proof corrector. Define
\[
\mathcal B(a,b)=P[(a\cdot\nabla)b],
\qquad
C_ab=(a\cdot\nabla)b-(b\cdot\nabla)a.
\]
The source terms in the comparison include
\[
R_u=\nu(t)\Delta v-\mathcal B(v,v)+\mathcal B(B_*,B_*),
\tag{11}
\]
and
\[
R_B=\rho(t)\Delta B_*-C_vB_*.
\tag{12}
\]

The additional terms associated with the smooth magnetic memory have polynomial bounds in fixed-order norms of \(\Sigma\), the bound on \(H\), and the geometric bounds for a partial word. For example,
\[
\|C_vB_*\|_2
\le C\|B_*\|_{W^{1,\infty}}\|v\|_{H^1}.
\tag{13}
\]
No high regularity of the unknown initial velocity is needed for (13). The rough terms already present in the velocity comparison still require the accepted energy framework.

For the rough magnetic discrepancy \(e\), a useful product estimate is
\[
\|C_ve\|_{H^{-3/4}}
\le C\|v\|_{H^1}\|e\|_{H^1}.
\tag{14}
\]
Under the local pulled-back propagator bounds used in the supplied construction, the relevant smoothing kernel has the form
\[
\|\mathcal U(t,s)\|_{H^{-3/4}\to H^1}
\le P(t-s)^{-7/8}.
\tag{15}
\]
Its time singularity is integrable. Over a reset duration \(\delta\), this produces a factor \(P\delta^{1/8}\), rather than a fixed loss for every completed word.

The resulting comparison has the schematic form
\[
E_{\rm out}
\le
\bigl(1+P\delta^{1/8}\bigr)E_{\rm in}
+P\delta^{1/8},
\tag{16}
\]
after closing the local coupled bound and enlarging the polynomial envelope \(P\). For a known polynomial number \(J\) of such operations, choosing
\[
\delta^{1/8}\le \frac{\zeta}{CPJ}
\tag{17}
\]
keeps their accumulated contribution within a prescribed polynomial error budget.

Equations (9)–(17) explain why preservation of a **known smooth magnetic prefix** is a more tractable interface than arbitrary magnetic writing. They also explain why the joint eraser should not simply be run after writing nonconstant memory.

This calculation does not assemble the missing programme. A complete writer would have to provide the sequence of prefixes \(\Sigma\), polynomial bounds for their fixed-order norms, the intervening magnetic operations, and a common timing and disturbance ledger. Those are precisely the data that the current arbitrary-\(\Pi\) construction lacks.

## 5. I did not obtain a valid negative answer

Several tempting restrictions fail to give an obstruction under your contract.

### Ideal-frame geometry is insufficient

A single ideal volume-preserving flow maps the constant frame to commuting columns with determinant one. Resistive evolution is not restricted to that class. The calculation in Section 2 already shows how positive heat can retain a noncommuting coarse response while removing unwanted fine-scale components.

Likewise, determinant one is not preserved by componentwise heat evolution of a matrix field. A restriction based on ideal transported frames therefore needs an additional argument before it can constrain the resistive system.

I also investigated representing a target through a single highly oscillatory volume-preserving map followed by heat. That route did not yield a quantitative construction for arbitrary \(\Pi\). Uniformly bounded precursor frames retain strong geometric restrictions under suitable weak limits, so general coarse responses require growing gradients or concentration. Polynomial growth is permitted by your contract, however. This gives no superpolynomial lower bound and no all-control negative.

### The coupled ensemble need not have one prescribed kinematic velocity

For a constructed reference, it is legitimate to use one chosen velocity and study its induction response simultaneously on \(e_1,e_2,e_3\).

For an arbitrary admissible mechanical control, the actual velocity may depend on \(H\) through the Lorentz term. Thus the three experiments with initial means \(e_1,e_2,e_3\) need not share the same velocity trajectory.

A restriction proved only for a prescribed passive velocity would therefore need a further argument to become an obstruction to every coupled mechanical control.

### Failure of a polynomial estimate is not a resource lower bound

An estimate such as
\[
\|\mathcal U(t,s)\|
\le
\exp\!\left(C\int_s^t\|\nabla u(r)\|_\infty\,dr\right)
\]
can make a particular construction unsuitable for the required disturbance tolerance. It does not establish that every controller incurs that growth.

I found neither an invariant separating some admissible \(\Pi\) from all reachable responses nor a lower bound forcing superpolynomial physical resources.

## 6. What the additional literature supplies

The nearby controllability results I checked do not fill this gap.

Rissel’s Theorem 1.2 concerns smooth known initial and target data for a two-dimensional ideal system in a doubly connected domain, with localized controls in both equations and a zero first-cohomology condition on the magnetic data. It supplies neither this mechanical-only response operator nor the simultaneous unknown-profile compiler. 

Rowan’s *A subsequentially fast dynamo on \(\mathbb T^3\)* provides another relevant control-based construction for induction. It builds prescribed kinematic velocities producing growth, including a construction covering a countable collection of diffusivities through subsequences of times. Its state- and diffusivity-dependent control arguments do not provide a common finite-time arbitrary-frame writer or a realization through the coupled momentum equation. 

These results offer useful mechanisms and comparisons. I have not found a theorem in them that can be substituted for the missing operation.

## 7. The precise remaining constructive task

One sufficient route would be a robust mechanical realization of
\[
B\longmapsto B+(\Pi_N-I)P_0B
\tag{18}
\]
on the relevant bounded set, with a polynomial velocity bound and a polynomial disturbance budget throughout the operation.

Because of (1), such a service would fit naturally between the accepted common erasure stage and a velocity-writing stage that preserves the resulting smooth magnetic memory. It would not require observing \(H\). But proving that the actual mechanical dynamics realize (18) is a new theorem; defining the operator does not construct it.

Other routes remain possible—for example, a stable evolution whose terminal response on constants is \(\Pi_N\), or a single quantitatively controlled microstructure construction followed by positive diffusion. Any such route must provide all of the following together:

- a physical operation using only the twelve momentum fields;
- uniformity over the unknown time-dependent diffusivities;
- simultaneous action on all three flux directions;
- polynomial control of already-written magnetic memory and rough errors;
- Lorentz and induction estimates for the actual coupled trajectory;
- the ordinary rational output and complete resource ledger;
- an all-weak endpoint transfer.

**I cannot presently provide that operation, universal constants \(A,p\), or the resulting full endpoint proof.** The exact positive-heat example rules out a simple ideal-geometry dismissal, while the abstract operator calculation shows that arbitrary \(\Pi\) is not intrinsically ill conditioned as a field-space target. The unresolved step is its uniformly stable physical realization under the stated control and resource restrictions.