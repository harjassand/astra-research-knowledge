**I have not established either of the two outcomes your contract requires: a complete native architecture, or an obstruction covering every allowed architecture.** The accepted finite-horizon compilers do not yet justify the passage to one fixed, spatially repeated, fault-tolerant material processor.

There is, however, some concrete progress. For the **full nonlinear equations**, the stated fault model already gives the required expected dissipation bound and the required **absolute kick-work bound**, including failed computations and rare clusters. The remaining uniform energy-density estimate is substantially stronger. On the computational side, classical reliable cellular constructions provide compatible resource benchmarks, but their application requires a physical fault-transfer theorem that I cannot presently prove for this connected MHD system.

I will distinguish the results proved below from the construction steps that remain unresolved.

## 1. Two of the all-path resource bounds follow from the fault model

These estimates hold for any fixed admissible drive and fixed codelet family with the stated norm bounds. Their constants depend on those fixed descriptions, \(a,T,K_0,\zeta,\gamma\), and a fixed upper bound on \(p\), but are independent of capacity, programme, runtime and the conditional mark law. They do not establish a computational threshold.

Write
\[
b=B-H_*,
\qquad
E(t)=\frac12\bigl(\|u(t)\|_2^2+\|b(t)\|_2^2\bigr),
\]
and
\[
D(t)=\nu(t)\|\nabla u(t)\|_2^2+
      \rho(t)\|\nabla b(t)\|_2^2.
\]
Set
\[
\mu=1-\zeta>0,\qquad
V=(aM)^3,\qquad
N_c=M^3,\qquad
\lambda=\frac pT.
\]

Use the declared pre-jump state at \(s-\), apply the prescribed jump, and use the post-jump state at \(s+\). The following estimates use those actual one-sided states.

### 1.1 The actual non-autonomous energy inequality

Between jumps, the nonlinear MHD terms cancel in joint energy. The terms involving the constant bias also cancel:
\[
\int_{\Omega_M}
u\cdot(H_*\cdot\nabla)b+
b\cdot(H_*\cdot\nabla)u\,dx=0.
\]
Consequently, the actual energy inequality, including the jumps, is
\[
\begin{aligned}
E(t)+\int_0^tD(s)\,ds
\le{}&E(0)+\int_0^t\langle f_*(s),u(s)\rangle\,ds\\
&+\sum_{s\le t}
\left[
\langle u(s-),\xi_u\rangle+
\langle b(s-),\xi_B\rangle+
\frac12\|\xi_u\|_2^2+
\frac12\|\xi_B\|_2^2
\right].
\end{aligned}
\tag{1}
\]
Here
\[
\langle H_*,\xi_B\rangle=H_*\cdot\int\xi_B=0.
\]
The dissipation in (1) contains the actual \(\nu(t)\) and \(\rho(t)\). No replacement by nominal coefficients, and no terms involving their derivatives, are needed.

A drive compatible with \(\operatorname{mean}u=0\) has zero spatial mean. Since \(f_*\) has a fixed finite \(a\)-periodic catalogue, it has a fixed periodic tensor potential \(F_*\) with
\[
f_*=\operatorname{div}F_*,
\qquad
\sup_t\|F_*(t)\|_{L^2(\Omega_M)}^2\le C_fV.
\]
For example, this potential can be defined frequency by frequency on the fixed cell. Thus
\[
\langle f_*,u\rangle
=-\int F_*:\nabla u
\le \frac12D(t)+C V.
\tag{2}
\]
The constant is computably bounded from the finite catalogue and waveform.

At a fault, conditional centering gives
\[
\mathbb E\!\left[
\langle u(s-),\xi_u\rangle+
\langle b(s-),\xi_B\rangle
\;\middle|\;\mathcal F_{s-},i,s
\right]=0.
\tag{3}
\]
This remains valid when the conditional covariance and directions of the mark depend arbitrarily on the pre-jump fields. The quadratic energy increment is at most \(K_0^2/2\).

Poisson compensation therefore yields
\[
\mathbb E E(t)+\frac12\mathbb E\int_0^tD(s)\,ds
\le
E(0)+CVt+\frac12\lambda N_cK_0^2t.
\tag{4}
\]
The codelets have fixed local norms, and the preparation condition implies
\[
E(0)\le C_{\mathrm{init}}V.
\]
Since \(N_c=V/a^3\), we obtain
\[
\boxed{
\mathbb E E(t)+\frac12\mathbb E\int_0^tD(s)\,ds
\le C V(1+t).
}
\tag{5}
\]

In particular,
\[
\boxed{
\mathbb E\int_0^t
\left[
\nu(s)\|\nabla u(s)\|_2^2+
\rho(s)\|\nabla B(s)\|_2^2
\right]ds
\le C V(1+t).
}
\tag{6}
\]

This calculation counts every fault. It does not condition on correct decoding or exclude large clusters. For fixed \(M\), the total clock rate is finite, so bounded time intervals contain finitely many faults almost surely. Stopping the energy process first, and then removing the stopping, justifies the expectation calculation without assuming a global strong solution.

### 1.2 The absolute kick-work bound is also available

Conditional centering alone controls signed energy injection. The zero-integral condition gives the additional estimate needed for absolute work.

Let \(D_i\) be a fixed enlargement of cell \(i\) containing every allowed support of a mark in that cell. These enlargements can be chosen with a capacity-independent overlap bound. Define
\[
g_i(s)=
\left(
\|\nabla u(s)\|_{L^2(D_i)}^2+
\|\nabla b(s)\|_{L^2(D_i)}^2
\right)^{1/2}.
\]

Subtracting local averages and applying local Poincaré gives
\[
\begin{aligned}
|\langle u,\xi_u\rangle|+|\langle B,\xi_B\rangle|
&=
|\langle u-u_{D_i},\xi_u\rangle|
+
|\langle b-b_{D_i},\xi_B\rangle|\\
&\le C aK_0\,g_i.
\end{aligned}
\tag{7}
\]
This step removes pairing with a potentially large, nearly constant local velocity. It also removes the constant magnetic bias exactly.

Bounded overlap implies
\[
\sum_i g_i(s)
\le
C M^{3/2}
\left(
\|\nabla u(s)\|_2^2+\|\nabla b(s)\|_2^2
\right)^{1/2}.
\tag{8}
\]
Let \(W_{\rm kick}(t)\) denote precisely the absolute kick-work sum in the question. Compensation, followed by Cauchy–Schwarz in probability and time, gives
\[
\begin{aligned}
\mathbb E W_{\rm kick}(t)
\le{}&
C\lambda aK_0M^{3/2}
\sqrt{\frac{t}{\mu}
      \mathbb E\int_0^tD(s)\,ds}\\
&+\frac12\lambda K_0^2M^3t.
\end{aligned}
\tag{9}
\]
Inserting (6), using \(V=a^3M^3\), and absorbing fixed architecture constants yields
\[
\boxed{
\mathbb E W_{\rm kick}(t)\le C V(1+t).
}
\tag{10}
\]

Thus **expected dissipation and absolute kick work already have the requested extensive bounds** under the stated energy semantics. Neither calculation uses computational success, independent mark directions, Gaussianity, or a fixed noise subspace.

## 2. Uniform nonlinear energy density remains an additional requirement

Estimate (5) gives
\[
\mathbb E E(t)\le CV(1+t).
\]
It does not give
\[
\sup_{t\ge0}\mathbb E E(t)\le CV.
\tag{11}
\]

The usual global Poincaré estimate has
\[
\lambda_1=\left(\frac{2\pi}{aM}\right)^2.
\]
Applied to (4), it gives an absorbing upper bound of order
\[
\frac{V}{\lambda_1}=O\!\left(V(aM)^2\right).
\tag{12}
\]
That upper bound is too large for the contract. It is not a lower bound and therefore cannot serve as an impossibility proof.

The absolute prescribed-work bound is closely tied to (11). If (11) were established, then
\[
\begin{aligned}
\mathbb E\int_0^t\int_{\Omega_M}|f_*\cdot u|\,dx\,ds
&\le
\|f_*\|_{L^\infty_{t,x}}
V^{1/2}\int_0^t
\bigl(\mathbb E\|u(s)\|_2^2\bigr)^{1/2}ds\\
&\le C Vt.
\end{aligned}
\tag{13}
\]
Using only (5) gives a bound growing roughly as \(Vt^{3/2}\). The integration-by-parts argument in (2) controls signed work; it does not justify moving an absolute value inside that argument.

So the energetic work remaining is quite specific: **prove a uniform-in-time nonlinear energy-density bound for the chosen architecture, for every admitted mark law and every energy-admissible realization**. Once that is available, (13) supplies the remaining prescribed-work estimate.

### 2.1 The slowest Fourier modes do not give the earlier obstruction

There is a useful positive comparison for the linearization about \((0,H_*)\):
\[
u_t=\nu(t)\Delta u+(H_*\cdot\nabla)b+f_*,
\qquad
b_t=\rho(t)\Delta b+(H_*\cdot\nabla)u.
\tag{14}
\]

Let
\[
\kappa=\frac{2\pi n}{aM}\ne0
\]
and use \(L^2\)-normalized Fourier coefficients. A localized zero-integral kick satisfies
\[
\begin{aligned}
\xi_\kappa
&=
V^{-1/2}e^{-i\kappa\cdot x_i}
\int \xi(x)
\left(e^{-i\kappa\cdot(x-x_i)}-1\right)dx,\\
|\xi_\kappa|
&\le C V^{-1/2}|\kappa|.
\end{aligned}
\tag{15}
\]
The fixed support and \(H^m\) bound also give, by integration by parts,
\[
|\xi_\kappa|\le C V^{-1/2}|\kappa|^{-m}.
\tag{16}
\]
After summing the \(M^3\) clock intensities, the modal quadratic-variation rate is therefore bounded by
\[
Q_\kappa
\le Cp\min\{|\kappa|^2,|\kappa|^{-2m}\}.
\tag{17}
\]

The Alfvén coupling in (14) cancels in joint modal energy. Diffusion damps that energy at rate at least \(c|\kappa|^2\). Hence the noise contribution to a uniform modal energy bound is
\[
Cp\min\{1,|\kappa|^{-2m-2}\}.
\tag{18}
\]
Its Fourier-lattice sum is \(O(V)\). The fixed forcing catalogue contributes \(O(V)\) as well, because its nonzero physical frequencies are fixed independently of \(M\). The initial energy is \(O(V)\). Consequently the linear system satisfies
\[
\sup_{t\ge0}\mathbb E
\left(\|u(t)\|_2^2+\|b(t)\|_2^2\right)
\le CV
\tag{19}
\]
for the admitted coefficient histories and adaptive centred marks.

The relevant cancellation is that long-wave noise power vanishes quadratically with \(|\kappa|\), matching the small diffusive damping rate. A vanishing spectral gap by itself therefore does not yield the desired universal negative.

### 2.2 Centering still permits nonlinear stress rectification

The linear calculation cannot be promoted to full MHD merely by invoking conditional centering.

Take a smooth incoming state, a smooth admissible velocity kick \(\xi\), and apply \(\sigma\xi\), with \(\sigma=\pm1\) equiprobably. Let \(u^\sigma(d)\) denote the ensuing local strong solution and \(u^0(d)\) the solution without the kick, with the same drive and coefficient history.

For a smooth solenoidal test field \(\phi\),
\[
\left.\frac{d}{dd}\right|_{d=0+}
\left[
\frac12\sum_{\sigma=\pm1}
\langle u^\sigma(d),\phi\rangle
-\langle u^0(d),\phi\rangle
\right]
=
\int_{\Omega_M}(\xi\otimes\xi):\nabla\phi\,dx.
\tag{20}
\]
Terms linear in \(\xi\), including diffusion, cancel under averaging. The quadratic Reynolds stress remains. A magnetic-only symmetric kick gives the opposite sign in this velocity response.

For
\[
\phi=e_1\sin(\kappa x_2),
\]
the right side is
\[
\kappa\int \xi_1\xi_2\cos(\kappa x_2)\,dx.
\tag{21}
\]
Compact solenoidal fields can have \(\int\xi_1\xi_2\ne0\), for example by taking the curl of an anisotropic compact vector potential and rotating it.

Thus zero conditional mean does not eliminate a first-order long-wave stress response. This is a concrete reason that the nonlinear energy theorem requires further work.

It also falls short of a universal obstruction. Sustaining such a response would require controlling its interaction with the driven state, compensating Maxwell and Reynolds stresses, and nonlinear saturation. Periodicity of the drive does not imply periodicity of the encoded state: the initial material may contain a hierarchy and macroscopic correlations. A Bloch or homogenized response around a periodic background would therefore need its own justification before it could support an all-architecture argument.

## 3. Freezing a finite compiler does not yet construct a reusable local cell

A finite local truth table has fixed arithmetic complexity. One can therefore contemplate freezing a sufficiently large finite-capacity implementation once. The outstanding issue is its embedding into the connected fluid.

The unit-torus guarantees concern a whole periodic state. When different symbols occupy adjacent cells:

- Cellwise magnetic means are no longer separately conserved.
- The pressure is the pressure of the large connected torus.
- Fluid and magnetic fields cross the intended cell boundaries.
- Fields left in routing regions and buffers can return during subsequent periods.
- Cleanup must renew a physical state class that permits the next update.

A one-period estimate inside a protected core does not prove that its surrounding buffer is reusable. Repetition requires a renewal estimate for the complete module, including the parts that are absent from the logical decoder.

### 3.1 A concrete scope check using Bloch modes

A possible construction would use fixed carriers modulated by cell-dependent envelopes. For a linear \(a\)-periodic stage, Bloch quasimomentum \(\theta\) is preserved. A theorem for \(a\)-periodic inputs describes the \(\theta=0\) sector. Arbitrary material words excite the other sectors as well.

There is a simple illustration: translation by one cell and the identity agree on every \(a\)-periodic field, yet they implement different operations on a nonuniform material word. Agreement on periodic inputs alone cannot certify neighbor transfer.

The two-frequency memory formula also changes for modulated carriers. In one spatial direction, suppose the same envelope is shifted to carriers \(n\) and \(2n\). Its physical frequencies are \(n+\theta\) and \(2n+\theta\). Put
\[
r=\left(\frac{2\pi}{a}\right)^2
\int_{\rm hold}\rho(s)\,ds.
\]
For the diffusion part of the operation, the recombination multiplier is
\[
\begin{aligned}
m(\theta)
&=
\frac{4e^{-r(n+\theta)^2}-e^{-r(2n+\theta)^2}}3\\
&=
1-r\left(\frac43n\theta+\theta^2\right)
+O\!\left(r^2(n+1)^4\right).
\end{aligned}
\tag{22}
\]
At \(\theta=0\), the first-order carrier decay cancels. For general envelopes, first-order evolution remains. Symmetric positive and negative carriers remove the \(n\theta\) term, while envelope diffusion remains.

A fixed Boolean restoration margin might absorb such a defect. Equation (22) therefore diagnoses the scope of this proposed extension; it does not obstruct other representations. Completing this approach would require a carrier-and-envelope calculus uniform over the relevant Bloch bands, followed by canonical codelet reshaping. Otherwise repeated nonlinear products can broaden envelope spectra and change the required resolution with runtime.

### 3.2 The pressure estimate needs the actual stress envelope

Let
\[
E_j(t)=\int_{Q_j}\bigl(|u|^2+|b|^2\bigr)\,dx.
\]
The supplied Green-function estimate gives, away from the nearest cells,
\[
|\nabla p_{\rm far}(x,t)|
\le
C a^{-4}\sum_{j\ne i}
\frac{E_j(t)}{(1+|i-j|)^4}
+
C(aM)^{-4}\sum_jE_j(t),
\qquad x\in Q_i.
\tag{23}
\]
If every \(E_j(t)\) is bounded by a fixed constant, the right side is bounded uniformly in \(M\).

At a fault, however, the change in stress contains
\[
\begin{aligned}
\delta(u\otimes u-b\otimes b)
={}&u\otimes\xi_u+\xi_u\otimes u+\xi_u\otimes\xi_u\\
&-b\otimes\xi_B-\xi_B\otimes b-\xi_B\otimes\xi_B.
\end{aligned}
\tag{24}
\]
Its size depends on the actual incoming local field as well as \(K_0\).

Even the desired global estimate \(\mathbb E\sum_jE_j\le CV\) would not, by itself, provide the pathwise cell bounds used in (23), or the probability tails needed for reliable computation. The mark laws may be spatially inhomogeneous and state dependent.

The summable pressure-gradient tail is useful. It does not supply local recovery or stochastic fault containment.

## 4. Independent clocks must be transferred into a logical fault theorem

For an elementary cell-period box,
\[
\Pr(\text{at least one ring})=1-e^{-p}\le p.
\tag{25}
\]
These events are independent for disjoint clock boxes. This statement concerns fault occurrences, before accounting for the fluid response.

A useful sufficient physical interface would be a witness estimate. For example, suppose a particular native construction proved that:

1. Every defective decoded elementary update has a witness among at most \(c\) specified clock boxes.
2. Each clock box can witness at most \(d\) defective updates.
3. This holds uniformly over preparation errors, coefficient histories, marks and energy-admissible realizations.

For a set \(A\) of \(k\) defective updates, at least \(k/d\) distinct witness boxes must contain events. Summing over witness choices gives
\[
\Pr(A\subseteq\mathcal F)
\le c^k p^{k/d}
=\bigl(c\,p^{1/d}\bigr)^k.
\tag{26}
\]
That would turn a sufficiently small fixed physical \(p\) into a fixed local-stochastic error parameter for a cellular theorem. The mark directions could remain adversarial.

**No estimate of this kind has been established here for the MHD processor.** A fault can leave a field outside the code neighborhood for more than one update. A cluster can increase the range and duration of its effects. Pressure and diffusion also prevent an exact finite propagation argument.

The bounded-witness formulation is only one sufficient route. A construction could instead prove suitable cluster tails and use a reliability theorem adapted to them. It would be incorrect to demand strict finite-range fault effects from every allowed architecture and then declare impossibility when that demand fails.

The raw Poisson law does provide strong cluster-count tails. For a fixed space-time region of mean count \(\Lambda_A\),
\[
\Pr(N_A\ge n)\le
\left(\frac{e\Lambda_A}{n}\right)^n,
\qquad n\ge\Lambda_A.
\tag{27}
\]
What remains unknown is the conversion from cluster count into the physical extent, lifetime and logical effect of the damage.

The accepted bounded-disturbance services do not perform that conversion. A positive event density is compatible with arbitrarily large clusters; an expected disturbance size cannot be substituted into a deterministic small-disturbance contract.

## 5. Classical overheads provide a benchmark, with initialization still to be checked

An additional useful primary comparison is Gács’s **1986** paper, *Reliable Computation with Cellular Automata*. Its Theorem 2 uses fixed space and time factors \(P_G,T_G\), and hierarchy depth
\[
k=\left\lceil
\log_2\!\left(r+s+\log_2\delta^{-1}\right)
\right\rceil,
\]
with encoded size \(P_G^{r+k}\) and simulated observation time \(T_G^kh\), under its legal-initialization and fault hypotheses. [cs-web.bu.edu](https://cs-web.bu.edu/faculty/gacs/papers/GacsReliableCA86.pdf?utm_source=chatgpt.com)

Choosing
\[
P_G^r\asymp S',\qquad
T_G^s\asymp J',\qquad
\delta=\frac{\epsilon}{J'+1}
\]
gives \(k=O(\log Bsize)\), hence
\[
P_G^{r+k}\le C S' Bsize^{\log_2P_G},
\qquad
J'T_G^k\le C J'Bsize^{\log_2T_G}.
\tag{28}
\]
Per-time guarantees can then be combined by a union bound.

This is a compatible resource benchmark. Its legal clean-past formulation must still be justified from an explicitly emitted initial word; it cannot be silently supplied as physical prehistory. I have not completed that initialization audit together with a fluid encoder.

For the physical comparison, I also checked the additional forced Navier–Stokes computation constructions documented in the OpenAI mathematics repository. They realize prescribed geometric maps and computation detectors using constructed smooth forces and stated smooth solution classes. Those results do not provide the fixed material alphabet, native random-fault recovery, unknown-coefficient robustness or all-path MHD energy theorem required here. [GitHub](https://github.com/openai/math/blob/main/lean/docs/376.md?utm_source=chatgpt.com)

## 6. All-weak semantics are a proof obligation, but not a universal negative

It would also be too strong to claim that your contract necessarily requires a general global strong-regularity theorem on every failed path.

Suppose a candidate architecture had a smooth clean reference trajectory
\[
(v,H_*+c)
\]
on one period, with
\[
\int_0^T
\left(\|\nabla v(t)\|_\infty+\|\nabla c(t)\|_\infty\right)dt
\le L_*
\tag{29}
\]
uniformly in capacity.

Compare any energy-admissible weak realization with the same force and coefficient history. For
\[
q=u-v,\qquad r=b-c,\qquad
\mathcal E=\frac12(\|q\|_2^2+\|r\|_2^2),
\]
the coupled relative-energy cancellations give, between jumps,
\[
\frac{d}{dt}\mathcal E
+\nu(t)\|\nabla q\|_2^2
+\rho(t)\|\nabla r\|_2^2
\le
C\left(\|\nabla v\|_\infty+\|\nabla c\|_\infty\right)\mathcal E.
\tag{30}
\]
At a jump,
\[
\sqrt{2\mathcal E(s+)}
\le \sqrt{2\mathcal E(s-)}+K_0.
\tag{31}
\]
Thus \(k\) faults during that period give
\[
\|(q,r)(T)\|_2
\le
e^{CL_*}
\left(\|(q,r)(0)\|_2+kK_0\right).
\tag{32}
\]

This comparison does not require the faulty trajectory itself to remain strong. It is therefore possible in principle to combine controlled reference dynamics with energy-admissible semantics on damaged paths.

But (32) is global. It does not identify which cells are damaged, whether the damage recovers, or how many future logical updates can be affected. Iterating it without a restoring mechanism also introduces an uncontrolled exponential factor in the number of periods. The native recovery and localization theorem remains necessary.

## 7. The unresolved construction has four distinct parts

The research and calculations above leave the following work outstanding.

**First, a reusable native update mechanism.** One fixed force must implement a fixed universal local transition rule on arbitrary neighboring material symbols, with a fixed decoding margin. Registers, routing fields, velocity remnants and buffer regions must return to a controlled physical class after each period. The estimates must be uniform in \(M\) and in the admitted coefficient histories.

**Second, a physical fault-transfer theorem.** It must quantify how bounded kicks and arbitrarily large rare clusters affect that mechanism, including incoming stress, pressure tails, transport and recovery. It must produce probability estimates strong enough for a specified reliable computation scheme, uniformly over the conditional mark laws and weak realizations.

**Third, the uniform nonlinear energy bound.** The all-path estimates (6) and (10) are available. The missing bound is \(\sup_t\mathbb E E(t)\le CV\), from which the required absolute prescribed-work bound would follow. Neither the global Poincaré loss nor the short-time rectification identity proves that every architecture violates this bound.

**Fourth, the complete material compiler and decoder.** Once the physical mechanism exists, the hierarchy, initialization, addresses, synchronization, observation schedule and decoding must be explicitly instantiated with the requested binary costs. The classical comparison indicates a plausible resource scale; it does not supply this material construction.

I therefore cannot provide justified values of \(p_0,\gamma,C,q\), a force catalogue, and a finite material alphabet satisfying the complete contract. Nor have I proved that all such choices fail.

The strongest established results here are the full nonlinear, all-path dissipation and absolute kick-work bounds, together with the scope checks above. The missing result is a native, reusable MHD processor with a proved stochastic fault-transfer law and a uniform nonlinear energy-density bound.