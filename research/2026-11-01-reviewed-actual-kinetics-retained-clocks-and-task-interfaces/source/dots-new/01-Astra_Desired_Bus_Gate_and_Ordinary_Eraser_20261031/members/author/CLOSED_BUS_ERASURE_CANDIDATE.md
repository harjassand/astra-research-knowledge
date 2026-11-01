# Ordinary closed-bus entangler with a finite receiver

31 October 2026. Author mathematical construction, not independent review, hardware acquisition, novelty, or architectural advantage. This is a **desired-operation** consumer: the bus itself supplies the entangling phase; no independent ZZ gate is assumed. The strongest ordinary geometric-bus / no-knowledge quantum eraser supplies the mechanism. The earlier finite-source coherent receiver is a separate frozen candidate.

## 1. Supplied physical model and exact operation

Let B be a bounded data observable, initially take B=Z1+Z2. A linear oscillator and vacuum Markov ports have

    H(t)=Delta a†a + [epsilon(t) a†+epsilon(t)* a] B,
    L_j=sqrt(kappa_j) a,  kappa=sum_j kappa_j.

The spin-dependent force, its complex phase and finite-slew envelope, all ports, oscillator linearity, the specified bath state, and the receiver are physical inputs, not produced by an admission theorem. B commutes with itself throughout the operation. There are no other data-dependent oscillator terms. The force vanishes outside [0,T]. Arbitrary data/reference inputs are allowed. Later sections separately treat arbitrary initial apparatus states, continuing data errors, imperfect readout and genuine termination of the interaction.

The driven conditional displacement alpha solves

    alpha'=-(kappa/2+i Delta)alpha-i epsilon, alpha(0)=0.

Define

    I=integral |alpha|² dt,
    Phi=-Re integral epsilon alpha* dt
       =Im integral alpha* alpha' dt + Delta I.

Assume the actual drive closes alpha(T)=0. In a unitary dilation of the passive oscillator/ports, the exact joint operation is

    U(T)=exp(i Phi B²) D(B v) U0(T),

where U0 is the data-independent passive evolution and v has terminal oscillator component zero and outgoing-port components v_j(t)=sqrt(kappa_j)alpha(t), up to the common port-sign convention. Thus ||v||²=A=kappa I. The displacement is conditional on B, not on a sampled jump history. This identity follows by moving the drive into the interaction picture of U0: its commutator at any two times is a scalar times B², so the Magnus series terminates after its second term. The Weyl displacement equation gives the stated alpha and phase. In particular the joint identity, not just a reduced-state equation, is controlling.

All outgoing displacements occupy one normalized mode u=v/sqrt(A), possibly spread over several ports. D(Bv)=exp[-i sqrt(2A) B P_u], with P=(a-a†)/(i sqrt2). Measuring P_u with outcome p and applying exp[+i sqrt(2A) p B] cancels it. Since B=Z1+Z2, this is two local Z rotations, not an entangling correction. No timestamp stream or instantaneous feedback is needed. The gate is exp(i Phi B²); Phi=pi/8 gives exp(i pi Z1Z2/4), up to a global phase.

### Warm apparatus and pre-existing correlations

The joint factorization is an operator identity, not a coherent-state assumption. For complete access to the displacement mode and exact quadrature measurement/correction, it yields the intended data gate for **any initial apparatus state**, even initially data–apparatus-correlated states: after correction each instrument outcome is U_gate tensor the environment quadrature instrument, preceded by I_data tensor U0. Summing outcomes leaves the data marginal transformed by U_gate. Thus exact erasure does not require bus cooling. It does require the stated linear, state-independent force model over the occupied sectors. A warm or nonlinear physical mediator may violate that model.

Incomplete access is different. A missing mode remains coupled to B. Its actual quadrature state and correlations matter; the vacuum formulas below must NOT be used for an arbitrary warm bath. For initially product data/apparatus, after cancellation of the measured part, a lost mode of displacement norm sqrt(L) gives a random unitary exp[-i sqrt(2L) B P_loss] averaged over its actual quadrature distribution. If its known mean is physically corrected, a second-order integral remainder gives

    ||E_loss-id||diamond <= L diam(B)² Var(P_loss).

For lost-mode photon occupation N, Var(P_loss)<=N+1/2+sqrt[N(N+1)] (after subtracting its mean). This is a sufficient energy receiving bound, not a Gaussian identification. With arbitrary initial data–apparatus correlations, use a joint state-norm estimate instead; no input-independent reduced channel follows merely from the lost-mode marginal. Infinite-temperature/uncalibrated field modes do not receive a finite error budget for free.

## 2. Vacuum receiver, exact complete channel and optimal ordinary erasure

For initial vacuum apparatus, split v into the actually measured mode amplitude sqrt(A_c) and its orthogonal inaccessible remainder of squared norm L=A-A_c. Beam-splitter detector inefficiency, loss, finite temporal capture and mode mismatch all count in this split. Exact homodyne/correction of the measured mode leaves

    rho_mn -> exp[i Phi(m²-n²)] exp[-L(m-n)²/2] rho_mn.   (1)

Here m,n are B eigenvalues; this is a complete channel identity, not fidelity for one input.

At fixed physical displacement and inaccessible field, homodyne already erases every accessible-mode coherence optimally among measurements followed by diagonal phase correction: for a POVM M_y, the additional factor obeys

    |sum_y exp[i(theta_y(m)-theta_y(n))] <n v_c|M_y|m v_c>| <= 1

by Cauchy–Schwarz and POVM completeness. Homodyne attains equality simultaneously for every pair. No better decoder or measurement of the same collected mode removes the remaining vacuum lost-field overlap. This is a scoped receiver optimum, not a no-go for encoded gates, active coherent reinteraction with the bus, squeezed input, or a different architecture.

For B=Z1+Z2 the distinct eigenvalues are -2,0,2 (zero has multiplicity two). Define a=exp(-2L), w=1-a, q=1-a^4. The complete diamond distance of (1), after removing the intended gate, is exactly

    d(L)= q,                         if q>=2w,
          4w²/(4w-q),               if q<2w,             (2)

and d(0)=0. The small-loss regime used in the certificate is therefore exactly d=1-exp(-8L), not merely a worst-coherence lower bound. Unmonitored bus operation is the same formula with L=A.

Proof: write the Schur kernel C_mn=exp[-L(m-n)²/2]. C is positive and C-J has at most one negative eigenvalue. For a pure data/reference input sum_m |m>|v_m>, the output difference is isometrically the matrix diag(sqrt(p))(C-J)diag(sqrt(p)), p_m=||v_m||²; an arbitrary reference cannot increase the optimum. Its trace norm is minus twice its smallest eigenvalue. Since off-diagonal entries of C-J are nonpositive, the minimizing eigenvector can be chosen nonnegative. Optimizing jointly over p and that vector reduces, by sum_m sqrt(p_m) x_m<=1, to

    d=2 max_{r>=0,sum r=1} sum_mn (1-C_mn) r_m r_n.

Duplicate eigenvalues combine. For fixed total extreme weight, the positive extreme-pair term is maximized at r_-=r_+=x. The objective is 8w x-4(4w-q)x², 0<=x<=1/2. Its maximum is exactly (2). This proves the full diamond formula, including the large-loss branch.

There is also an unrestricted postprocessing optimum in the small-loss regime of (2), not just the diagonal-decoder bound. Give an arbitrary recovery joint access to the data and all collected field, while keeping the lost field unavailable. Feed half of a Bell state encoded in the B=±2 subspace. Before recovery the partial transpose on the reference has trace norm 1+exp(-8L), because the two data/collected-field branch vectors are orthogonal. A local CPTP recovery cannot increase this norm. The target Bell projector has partial-transpose operator norm 1/2, so its recovered overlap is at most [1+exp(-8L)]/2. Testing this projector gives complete-error lower bound 1-exp(-8L). Homodyne attains that full diamond distance when q>=2w. Thus in the certified small-loss region, no deterministic decoder, even with arbitrary joint operations on the collected field and the unencoded data **after this fixed physical gate**, can improve the worst-case error. Encoding before the operation, changing its trajectory, reusing the lost field, or replacing the physical interaction are outside this statement.

## 3. Finite-bandwidth passive receiver and finite observation time

The numerical consumer uses one output port, total kappa. Its outgoing displacement e^{i omega t} f(t) is sent through a passive **two-port** filter cavity with equal port coupling rates beta and detuning chosen for carrier omega. Its total energy linewidth is 2 beta. One transmitted port is measured; the prompt reflected port is uncollected. In the carrier frame its transmitted displacement envelope z obeys

    z'=-beta z+beta f, z(0)=0.

This is the actual transfer beta/(beta+i nu), not a brick-wall or compact-bandwidth fiction. The filter preserves global energy when both ports and its stored state are retained. The measured displacement over [0,T+W] has squared norm

    A_c=eta_d kappa F_W, F_W=integral_0^(T+W) |z|² dt,
    L=kappa I-A_c.                                      (3)

This charges prompt reflection, detector inefficiency and the still-stored filter displacement at the observation endpoint; the latter eventually exits but is not silently counted as measured. The data force is off from T onward, so the remaining apparatus evolves independently of data. Nevertheless the data must wait for the required readout/correction, with its own continuing errors charged.

Homodyne must measure the actual normalized transmitted temporal mode over this interval, with its complex carrier/envelope, not an arbitrary bucket quadrature. A shaped local oscillator and one integrated scalar suffice **if supplied**. Actual detector electronic response, local-oscillator slew, mode overlap, dynamic range and electronics noise are additional receiver specifications. A single-pole optical filter does not by itself certify an ideal homodyne apparatus or zero electronics error. If the implemented normalized mode is u_hat, replace A_c by eta_d |<u_hat,v_transmitted>|²; the orthogonal remainder is lost. No narrow-source-linewidth assumption is used.

The finite-slew gate below takes

    Delta=0, kappa=1/5, T=2pi, omega=1,
    alpha(t)=(1/sqrt6) sin²(t/2) exp(i t), 0<=t<=T.

Then alpha=alpha'=0 at both endpoints, I=Phi=pi/8, and the force epsilon=i alpha'+i kappa alpha/2 is continuous and zero outside [0,T]. Its piecewise derivative is globally bounded, so the actual control is Lipschitz:

    |epsilon| <= sqrt[( (1/2+1/10)²+1 )/6] < 0.477,
    |epsilon'| <= (5/2+3/20)/sqrt6 < 1.083.              (4)

These are conservative analytic bounds, not measured actuator performance. The maximum conditional bus occupation from the driven displacement is ||B||² max|alpha|²=2/3 photons. This does not bound a separately warm initial bus occupation.

For f(t)=(1/sqrt6)(1-cos t)/2, D=beta²+1, r=exp(-beta T), the exact filter trajectory and integrated capture are

    z(t)=1/(2sqrt6) [1-(beta² cos t+beta sin t)/D-exp(-beta t)/D],
    z(T)=(1-r)/(2sqrt6 D),
    F_infinity=1/24 [T(1+beta²/(2D))-(1-r)/(beta D²)],
    F_W=F_infinity-(1-r)² exp(-2 beta W)/(48 beta D²).  (5)

To derive the energy formula, integrate z'=beta(f-z) over the full pulse and ringdown: integral z²=integral f z. The final subtraction in (5) is the actual unmeasured tail. A high rate of detector sampling is not inferred from the mean emitted photon number; all bandwidth enters (3)-(5) or an actual mode-response calibration.

## 4. Finite record, calibration, continuing errors, and release

In the vacuum exact no-knowledge quadrature, p has density pi^(-1/2) exp(-p²), independently of the data input. With an ADC step h, nearest-neighbor quantization has |delta p|<=h/2 away from saturation. The complete correction error is at most

    diam(B) sqrt(A_c/2) h.

On saturation |p|>R use any fixed declared correction; its contribution is at most 2 Pr(|p|>R), bounded by 2 exp(-R²)/(R sqrt(pi)). This Gaussian tail is specific to the vacuum receiving model. For warm input, an actual second-moment/energy envelope gives only the corresponding Chebyshev bound unless more is known. Because the quadrature generator commutes with the interaction, its law is unaffected by the conditional displacement; pre-existing correlations still require an envelope valid for every admitted joint input.

Local correction exp(i theta Z_j) can reduce theta modulo pi up to a global phase. Parallel physical Z controls of duration tau_z therefore require coefficient at least pi/(2 tau_z), plus calibration and timing accuracy. This is not a free Pauli frame for subsequent noncommuting gates. The scalar readout calculation, electronics delay, mode calibration, bus parameter drift, extra drive Hamiltonians, preparation and transfer errors require an independent total complete-error allowance. The numerical example supplies such an allowance but does not derive it from hardware.

If each data qubit also has continuous Markov dephasing gamma D[Z_j] through the whole duration S=T+W+tau_z, these channels commute with the bus operation/measurement/correction; their total diamond contribution is <=4 gamma S. For different continuing data noise, use a separately proved complete bound over the actual control sequence, not this commuting formula.

At T the *driven displacement* of the original bus is zero and the spin-dependent force is exactly off. The only remaining conditional operation is on the already emitted field, subsequently erased up to (3). After the finite local Z correction, all remaining bus/filter evolutions are data independent. Consequently the returned data can enter noncommuting gates; no source reset or mathematical trace followed by reuse is hidden. This interface relies on the paid ability to deliver the specified force envelope and to keep it zero afterward. Residual couplings invalidate this release and must be bounded. An arbitrary warm initial bus is also safe at full access because the global operator factorization is controlling, not a claim that the bus became vacuum.

Small calibration errors can be budgeted directly: an actual residual terminal displacement r adds |r|² to inaccessible vacuum displacement energy; in a warm apparatus its quadrature energy is needed instead. A phase error deltaPhi costs <=diam(B²)|deltaPhi|=4|deltaPhi| in complete norm. At exact quadrature but fractional gain error e, the vacuum residual coefficient is L_eff=L+A_c e². At homodyne angle theta (zero means the information-bearing quadrature), with correction coefficient k, put mu=sqrt(2A_c)cos theta and nu=sqrt(2A_c)sin theta. Gaussian integration gives

    L_eff=L+mu²/2+(k-nu)²/2,
    Phi_eff=Phi+k mu/2.

Thus measuring the wrong quadrature incurs both measurement dephasing and an unwanted B² phase; it is not repaired merely by a better local correction. Independent added record noise of variance sigma² adds k² sigma² to L_eff. These formulas assume that noise is independent of data/field; correlated controller faults require joint receiving.

## 5. Gate phase versus exposure: exact ordinary limitation

For any absolutely continuous closed alpha with square-integrable derivative, set E=integral |epsilon|² and Gamma=Im integral alpha*alpha'. Integration by parts gives

    E=J+(kappa²/4+Delta²)I+2 Delta Gamma, J=integral |alpha'|².

Rotate alpha by exp(-i Gamma t/I). Its derivative energy is J-Gamma²/I. The Dirichlet Poincare inequality yields

    E >= Phi²/I + (kappa²/4+pi²/T²)I.                  (6)

This is exact for a prescribed Phi,T,kappa and arbitrary detuning. If |epsilon|<=g, E<=g²T. With K²=kappa²/4+pi²/T², necessity gives

    g²T>=2K|Phi|,
    I >= 2Phi²/[g²T+sqrt(g^4 T²-4K²Phi²)].             (7)

The integrated-energy equality trajectory is alpha=C sin(pi t/T) exp(i Omega t), with Omega=Phi/I-Delta. Its force generally jumps at endpoints: it is valid for the bounded-amplitude ideal control model but NOT a free finite-slew implementation. The finite-slew sin² trajectory in Section 3 instead has J/I=4/3 and E=I(4/3+1/100), paying an explicit extra shape cost. No finite-time pulse is asserted to have compact frequency support.

For a fixed unobserved fraction 1-eta of vacuum output and otherwise this same one-pass force model, (7) gives L>=(1-eta)kappa I_min. It constrains entanglement generation and lost-field exposure together, rather than suppressing an independent nuisance source. It is NOT a universal no-go: active feedback changing the interaction, squeezed/loss-correlated input, codes, multiple bus modes, additional Hamiltonians or altered observation access change the premise. An energy/admission theorem does not supply those missing resources.

## 6. Exact comparison and scientific selection

The exact rational certificate uses beta in {1,2,4,8,16}, W=1/beta, eta_d=999/1000, h=1/100000, R=5, gamma=1/10000, tau_z=1/100, and an additional supplied complete-error allowance 1/1000. The force bounds (4) and local-Z coefficient bound pi/(2tau_z) are explicit. All exponentials/pi/square roots in the certificate are rationally enclosed; floating simulations are diagnostics only. Failures remain in the grid.

At beta=8, the vacuum lost-field diamond error is about 0.00384195. Including continuing data noise, ADC/saturation, finite correction time, and the supplied extra allowance, the bound is below 0.007418, meeting a 0.01 target. The same gate-producing bus with the emitted field discarded has exact bus-only diamond error 1-exp(-pi/5), approximately 0.466512. This is an exact same-source ordinary-measurement advantage, NOT a new invention or a broad architectural optimum. The comparison is also stronger than leaving this particular pulse unchanged: for **every** closed trajectory in this fixed-B vacuum force class with the same gate phase, T=2pi, kappa=1/5 and force cap g=0.477, (7) gives I>=0.11007418 and an unmonitored complete-error lower bound greater than 0.1614815. Thus reoptimizing a bounded force envelope within this class cannot reach the 0.01 target without an additional resource. This lower bound does not cover changing B during the gate, multi-mode/encoded schemes, squeezed input or coherent reuse of the emitted field.

Crucially the ordinary method already produces the useful entangler and, under full access, tolerates an arbitrary warm linear bus. The observable energy admission is not needed for this exactly Gaussian construction. Its possible future role is to receive actual non-Gaussian imperfections or continuing correlated auxiliary sources that do not close in this linear model. Such use must be attached to a real physical component and a complete error budget; more source classes alone are not a capability result.

The unresolved consequential boundary is acquiring the spin-dependent force, faithful linearity, sufficiently low inaccessible quadrature noise, and matched-mode observation/local controls at the same time. Simply refining an exact evaluator does not solve it. Known ordinary coherent-reuse/spin-echo, no-knowledge feedback, squeezed-bus, encoded and avoidance architectures must receive the same available hardware/services before claiming superiority.

## Primary precedents (ordinary methods are credited)

- Szigeti et al., [Ignorance Is Bliss](https://arxiv.org/html/1401.4493), equations (5)-(7): Hermitian-coupling no-knowledge homodyne correction and the residual inaccessible fraction. The finite one-mode calculation above is a commuting, exactly closed-bus specialization, not a claim to invent noise cancellation.
- Leroux et al., [Unitary cavity spin squeezing by quantum erasure](https://eapg.mit.edu/wp-content/uploads/2018/03/pra_85_013803-cavity-squeezing-q-eraser.pdf), Section IV: coherent-pulse reuse/spin echo and measurement/feedback erasure preserve a useful collective interaction, with unobserved loss limiting it. Its physical model is not identical to the force model here.
- Louis et al., [Loss in hybrid qubit-bus couplings and gates](https://arxiv.org/html/0804.3240): exact oscillator-assisted gate loss analysis and a symmetrization route to simpler qubit errors. Its architecture is a serious alternative, not a comparator denied access to the bus.
- Barrett and Milburn, [Quantum information processing via a lossy bus](https://arxiv.org/abs/quant-ph/0607206): an earlier entangling-gate route using weak qubit-bus coupling, homodyne and local operations. Only the accessible abstract is relied on here; no priority claim concerning the present exact envelope is made.

Source access: one Stanford mirror timed out and one old arXiv HTML endpoint returned a cache miss; neither was denied. The MIT primary PDF and arXiv primary sources above were accessible. No denied-source retry, equipment, purchase, publication or outreach occurred.
