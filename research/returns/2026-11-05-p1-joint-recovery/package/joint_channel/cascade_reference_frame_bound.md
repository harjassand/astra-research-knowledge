# An all-width reference-frame lower bound for the matched cascade

5 November 2026. The sine-state/path-spectrum optimization is established phase-reference machinery. The source-specific deduction here is its application to the unavoidable initial twirl of the physical matched cascade, followed by the explicit finite-angle lift. This does not give an unrestricted causal-receiver converse or an attaining SU(2) extraction scheme.

## 1. Statement

Let k receiver qubits undergo the specified same-angle cascade after each source collision, with arbitrary pure or mixed initialization, arbitrary independent classical labels, and arbitrary final decoding. For fixed k and N theta^4 -> t>0, the established limiting channel is exp(tG_(k+1))P_SU(2). Its best half-diamond reference-preserving recovery error obeys

\[
\boxed{\epsilon_{k,t}\ge h_k:=\frac{1-\cos(\pi/(k+2))}{2},\qquad t>0.}
\tag{1}
\]

This holds for every integer k>=0 and every initialized frame. Hence

\[
h_k=\frac{\pi^2}{4(k+2)^2}+O(k^{-4}).
\tag{2}
\]

An accurate family of these weak-angle matched cascades must therefore have k=Omega(epsilon^-1/2). This strengthens the k^-4 floor obtained from the more general weak-processing witness, while remaining a necessary condition for this particular mechanism.

## 2. Relaxations

Grant the actual source together with the frame immediately after the initial collective twirl. A decoder given these systems can simulate the later G evolution and final readout. Its optimum Bell fidelity upper bounds the physical receiver's fidelity.

Next replace full SU(2) twirling by only U(1) rotations about z. Haar invariance gives P_SU(2)P_U(1)=P_SU(2), so full twirling is a postprocessing of U(1) twirling. This second relaxed problem has an exact solution.

## 3. Exact source-granted U(1) calculation

Pure frames suffice: a mixed frame can be decomposed into pure frames and the decomposition label granted. Write the k-qubit pure frame in its k+1 excitation-number sectors as

\[
|\psi\rangle=\sum_{h=0}^{k}\sqrt{p_h}|\psi_h\rangle,
\qquad p_h\ge0,\quad\sum_hp_h=1.
\]

The normalized vectors psi_h lie in orthogonal charge sectors. Multiplicity within a sector is arbitrary. Put p_h=0 outside 0,...,k. For a Bell input on R,S, the twirled state is an orthogonal direct sum of the unnormalized pure states

\[
|\Psi_h\rangle=\frac1{\sqrt2}\left(
\sqrt{p_h}|0\rangle_R|0\rangle_S|\psi_h\rangle_M
+\sqrt{p_{h-1}}|1\rangle_R|1\rangle_S|\psi_{h-1}\rangle_M
\right),\quad h=0,...,k+1.
\tag{3}
\]

The granted receiver can read this total-charge label without disturbance. The two receiver vectors in each block are orthogonal. The largest Bell overlap obtained by a trace-preserving local decoder on that block is

\[
(\sqrt{p_h}+\sqrt{p_{h-1}})^2/4.
\]

It is achieved by mapping the two receiver vectors isometrically to the output-qubit basis. Optimality is the elementary two-Schmidt-coefficient Bell-overlap bound, or the two-dimensional conditional-min-entropy SDP. Summing the blocks gives the exact optimum

\[
F_{U(1)}(p)=\frac12+\frac12\sum_{h=0}^{k-1}\sqrt{p_hp_{h+1}}.
\tag{4}
\]

Write a_h=sqrt(p_h). The sum in (4) is the Rayleigh form of the (k+1)-vertex path adjacency matrix divided by two. Its largest eigenvalue is cos(pi/(k+2)), with normalized eigenvector

\[
a_h=\sqrt{\frac2{k+2}}\sin\frac{(h+1)\pi}{k+2}.
\]

Therefore

\[
\boxed{F_{U(1)}^{\max}=\frac{1+\cos(\pi/(k+2))}{2}.}
\tag{5}
\]

The charge-block isometries preserve both input populations and multiply input coherence by lambda=sum_h sqrt(p_h p_(h+1)). Their decoded channel is exactly

\[
\rho\longmapsto\frac{1+\lambda}{2}\rho+
\frac{1-\lambda}{2}Z\rho Z.
\]

Its half-diamond error is (1-lambda)/2. The sine frame therefore also attains exactly h_k in half-diamond distance for the relaxed source-granted U(1) task, proving that this relaxed benchmark is sharp in the requested error convention.

This does not attain a full-SU(2) frame, nor extract the qubit after the actual source is discarded. A successful physical half-diamond decoder has Bell fidelity at least 1-epsilon, so the relaxations and (5) prove (1).

Classical initialization labels do not improve the bound: apply it in each branch. Idle independent ancillas carrying no collective charge do not enlarge the k+1 charge values, although all such coherent systems still count physically. The use of the granted source is confined to the converse relaxation.

## 4. Explicit finite-angle version

Use the independently audited finite-angle lift in `joint_root/cascade_finite_angle_bound.md`. Set n=k+1 and

\[
R_p=e^{2n\theta}(2n\theta)^p/p!,\qquad
\bar g_n=3n^2(n-1)^2/8+n(n-1)(n-2)/4,
\]

\[
\eta_n=1-\theta^2+R_3,\qquad
E_n=R_5+\tfrac12\theta^8\bar g_n^2e^{\theta^4\bar g_n},\qquad
\Delta_n(\theta,N)=\tfrac12\{NE_n+2^n\eta_n^N\}.
\]

Under 0<theta<=1, eta_n<1, and theta²(1+n(n+1)/2)<=2, for every integer N>=1 the actual physical cascade obeys

\[
\boxed{\epsilon_{\rm physical}(k,\theta,N)
\ge\left[h_k-\Delta_{k+1}(\theta,N)\right]_+.}
\tag{6}
\]

Indeed, initialization, tracing S, and final decoding contract the lifted half-diamond distance. Bell overlap changes by at most Delta, and the limiting exp(Ntheta^4G)P channel has Bell fidelity at most 1-h_k. The same bound holds for theta-dependent initial states and final decoders, because the lift is uniform over inputs and postprocessing.

When a proposed family has target error epsilon and a proved lift error Delta, (6) requires

\[
k+2\ge\frac{\pi}{\arccos(1-2(\epsilon+\Delta))},
\tag{7}
\]

whenever epsilon+Delta<1/2. In particular, if Delta=o(epsilon), then

\[
k\ge\frac{\pi}{2\sqrt\epsilon}(1+o(1))-2.
\]

These are simultaneous finite-parameter statements, not an interchange of width and angle limits. The sufficient lift regime is conservative and may require theta to be much smaller than a power of k and epsilon.


### A joint asymptotic regime with no unknown lift term

Fix constants 0<A<=B<infinity and put L=log(1/epsilon). Suppose epsilon tends to zero, the physical parameters satisfy

\[
A L\le N\theta^4\le B L,
\qquad
\theta=o\!\left(\frac{\epsilon^{7/2}}{L}\right),
\tag{8}
\]

and a family of the specified matched cascades attains half-diamond error at most epsilon. Then

\[
\boxed{k+2\ge\left(\frac\pi2+o(1)\right)\epsilon^{-1/2}.}
\tag{9}
\]

To justify the joint quantifiers, choose any fixed C>pi/2. Cases k>C epsilon^-1/2 already obey (9). In the remaining cases n=k+1=O(epsilon^-1/2), uniformly in the initialization and decoder. The displayed lift has

\[
NR_5=O(L n^5\theta)=o(\epsilon),\qquad
N\theta^8\bar g_n^2e^{\theta^4\bar g_n}
=O(L\theta^4n^8)=o(\epsilon).
\]

Moreover n^3 theta=o(1), so eta_n<=1-theta^2/2 for all sufficiently small epsilon. Its transient obeys

\[
2^n\eta_n^N
\le \exp\!\left(O(\epsilon^{-1/2})-
\frac{A L}{2\theta^2}\right)=o(\epsilon).
\]

All lift hypotheses eventually hold, hence Delta_n=o(epsilon) uniformly throughout these cases. Equation (7) proves (9). The exponent 7/2 is a sufficient regime from the deliberately conservative Taylor estimate; no sharp angle threshold is claimed. This corollary is a width lower bound for this architecture, not a high-fidelity construction.

## 5. Paid resources and what is still missing

The matched cascade uses k retained active qubits, k+1 qubits while a carrier is present, and kN receiver two-qubit partial-SWAP encounters. Thus, in a family where the lift is negligible and N is of order theta^-4 log(1/epsilon), the necessary active-collision count for this mechanism is at least order

\[
\theta^{-4}\epsilon^{-1/2}\log(1/\epsilon).
\]

This counts its actual prescribed encounters, not a universal circuit lower bound. Frame preparation, coherent workspace, final-decoder synthesis, routing, and any buffering have to be added. The sine amplitudes above attain only a source-granted one-axis reference benchmark and do not supply those physical tasks for the original cascade.

A matching all-k initialized frame and source-erased decoder has not been proved. The exact directed continuity laws and low-loss extensive observables do not yet provide a noncommutative logical-qubit algebra with bounded recovery error. In particular, conservation of one energy-like quantity cannot certify preservation of an arbitrary inaccessible reference. The validated finite-width entanglement-transmission example provides robust floating-point evidence that the family is not uniformly entanglement breaking, but its semigroup fidelity is not interval certified and it does not establish error tending to zero. The finite-angle lift is an exact theorem and applies to any separately certified limiting fidelity.

## 6. Primary attribution

The path-spectrum/sine-state optimization is prior phase-reference machinery. D. W. Berry and H. M. Wiseman, *Optimal States and Almost Optimal Adaptive Measurements for Quantum Interferometry*, Phys. Rev. Lett. 85, 5098 (2000), https://arxiv.org/abs/quant-ph/0009117 , Eqs. (9)-(10), gives the corresponding optimal phase sharpness and sine amplitudes. The present novelty claim is limited to the cascade-specific converse obtained by the two relaxations and the finite-angle lift, not the sine optimization.

For bounded-reference decoding and relational implementations, see S. D. Bartlett, T. Rudolph, R. W. Spekkens, P. S. Turner, *Quantum communication using a bounded-size quantum reference frame*, New J. Phys. 11, 063013 (2009), https://arxiv.org/abs/0812.5040 , https://doi.org/10.1088/1367-2630/11/6/063013 . That decoding framework supplies context for the source-granted relaxation; it does not prove transport from the actual discarded source into this physical receiver.
