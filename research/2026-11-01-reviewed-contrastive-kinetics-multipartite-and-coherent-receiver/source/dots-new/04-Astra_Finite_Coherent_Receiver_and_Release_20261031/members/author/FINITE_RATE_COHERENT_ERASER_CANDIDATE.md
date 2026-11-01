# Finite-rate coherent source-output erasure with a finite-bandwidth receiver

31 October 2026. AUTHOR CANDIDATE, independent review pending. Ordinary coherent feed-forward / conditional cavity scattering and coherent-state analysis are credited. No novelty, calibrated hardware, unconditional source-floor violation, or threshold claim. The earlier monitored-phase candidate remains frozen separately.

## 1. Task and actual supplied network

The task is a commuting Z/ZZ graph-phase layer (or diagonal/idle service), with local source qubits that continuously interact with the data. Instead of supplying a high-fidelity photon recorder, route each local emitted field one-way through a data-controlled cavity. The data itself controls the cavity resonance; no detected event or classical feedback is used. The receiver is an actual finite-bandwidth dynamical component, not ideal scattering S=Z.

For one data qubit, one source qubit, and one bosonic cavity, let

    L_s = sqrt(lambda) sigma^-_s,   L_c = sqrt(k_e) a,
    k = k_e + k_i > 0,             chi = k/2,
    H_s = sqrt(lambda) b X_s Z_d,
    H_c = chi Z_d a^dagger a,
    H_cas = Im[L_c^dagger sqrt(eta) L_s].

The actual Lindblad jumps are

    L_out = sqrt(eta) L_s + L_c,
    L_route_loss = sqrt(1-eta) L_s,
    L_internal_loss = sqrt(k_i) a,

omitting zero-rate channels. Here 0<=eta<=1 is actual routing transmissivity, k_e external receiver coupling, k_i internal cavity loss. H=H_s+H_c+H_cas plus the intended commuting data Hamiltonian. Vacuum input fields and cold |0>_s, |0>_c are required; arbitrary data/reference input is allowed. All parameters are real, b>=0. This is the standard unidirectional cascaded network, not a bidirectional field that feeds back to the source. Its source marginal is the ordinary driven damped qubit; downstream coupling does not change it.

The receiver shift chi=k/2 is a paid dispersive/cross-Kerr interaction. It acts on an unbounded cavity number operator and must remain valid over the occupied sectors in a physical implementation. Source/receiver Markov validity, routing isolation, extra loss, calibration, thermal modes, saturation, source preparation, gate errors and subsequent noncommuting consumption are not inferred from these equations. Additional actual errors require receiving. The source drive stays ON throughout [0,T]. Nothing is turned off to obtain the finite-time output; cavity and source are traced at T with their remaining distinguishability charged.

Independent copies can accompany an arbitrary commuting graph layer. Its local output maps factor after removing the intended diagonal unitary. This is not arbitrary continuously controlled universal computation: source-conditioned transverse operations would require extra services.

## 2. Why a finite-width cavity is worth testing

The ordinary lossless one-sided reflection coefficient is

    r_z(omega) = [i(omega-z chi)-k/2]/[i(omega-z chi)+k/2].

At chi=k/2, the two carrier reflections are opposite and their common first-order group delay agrees. Explicitly 1+r_+(omega)^*r_-(omega)=-4i omega^2/k^2+O(omega^4). Thus the receiver need not approximate an instantaneous pi scatterer over every possible source bandwidth. The actual driven source's mostly coherent carrier component can be corrected while its noncoherent field component is separately charged. This statement by itself is NOT a finite-time proof; Sections3–5 supply one without assuming a narrow spectrum or empty terminal cavity.

## 3. Actual finite-source field approaches a coherent field, with a proved vector bound

Fix the data branch Z_d=+1. Write c=sqrt(lambda)b, p(t)=<Q_s>, y(t)=<Y_s>, s(t)=<sigma^-_s>=i y(t)/2; x(t)=0 from the cold initial condition. Exact optical Bloch equations give

    p'=-lambda p-c y,
    y'=4c p-2c-lambda y/2.

Positivity gives |y|<=2sqrt(p), hence the comparison equation for sqrt(p) gives

    p(t)<=4c^2/lambda^2=4b^2/lambda.

Let D(t)=p(1-p)-|s|^2 be the source density determinant. Direct exact differentiation gives

    D'=lambda(p^2-D),   D(0)=0.

Consequently D(t)<=16b^4/lambda^2. The ACTUAL emitted field mean is beta(t)=sqrt(lambda)s(t). Displacing that field by -beta(t), its expected total photon number is exactly

    N_inc = integral_0^T lambda[p(t)-|s(t)|^2] dt
          = integral_0^T lambda[p(t)^2+D(t)] dt
          <=32b^4 T/lambda.                           (1)

This is the normally ordered field covariance/number identity for vacuum input. It is not an assertion that inelastic power directly equals logical error.

The actual initialized source+field output is pure, call it |Psi_+>. After field displacement, the probability outside |0>_s tensor |vac>_field is at most

    E=(4b^2+32b^4T)/lambda,

because Q_s+N_field >= I-|0,vac><0,vac|. For E<=1 there is a phase theta with

    || |Psi_+>-exp(i theta)|0>_s|beta>_field ||
       <=sqrt(2-2sqrt(1-E))<=sqrt(2E).                 (2)

For E>1 use the trivial vector bound2 instead; all later displayed small-error claims require E<=1. This preserves the essential square-root loss; no squeezed/coherent vacuum matrix elements are dropped.

The negative-data branch obeys EXACTLY

    |Psi_->=(Z_s tensor field-photon-parity)|Psi_+>.

The same theta therefore works for both branches; the comparison has not introduced an unknown data-dependent phase. A data/reference superposition consequently has the same initialized-isometry error bound (2), not a separate state-by-state approximation.

The coherent comparison in (2) still uses the finite-source amplitude beta(t), not an instantaneous constant drive. From the Bloch equation,

    beta(t)=-2ib(1-exp(-lambda t/2))
             +2i lambda b integral_0^t exp[-lambda(t-u)/2] p(u) du.

Thus for beta_0(t)=-2ib on [0,T],

    ||beta-beta_0||_L2 <= 2b/sqrt(lambda)+16b^3 sqrt(T)/lambda.  (3)

Both amplitudes are purely imaginary, so their coherent-state overlap is real positive. Coherent-vector distance is at most their L2 amplitude distance. This explicitly charges both source turn-on transient and finite-rate elastic-amplitude shift.

## 3a. Stronger ordinary exact coherent projection

For this particular two-level source there is a stronger equally informed ordinary method than the moment bound. Project the initialized source/entire-field state directly onto source ground and the CONSTANT coherent pulse beta_0=-2ib. The standard coherent-bra projection of the vacuum-input jump-history dilation obeys

    v'=A v,  v(0)=|0>,
    A=-icX-lambda Q/2 + beta_0^*sqrt(lambda)sigma^- -|beta_0|^2 I/2
     =[[-2b^2, ic],[-ic,-lambda/2-2b^2]].

The fixed source phase change diag(1,-i) makes this matrix real symmetric:

    B=[[-2b^2,c],[c,-lambda/2-2b^2]],
    a(T)=<0|exp(TB)|0>.

Its trace is negative and determinant4b^4>=0; B is negative semidefinite (negative definite for b>0). It is also Metzler. Hence 0<a(T)<=1, real. Both data branches have this SAME real overlap by the exact source-Z/field-parity symmetry. The initialized isometry norm difference from the constant coherent reference is therefore exactly sqrt(2-2a), and

    delta_exact=2sqrt(2-2a(T))                         (4a)

bounds the complete channel difference after ANY common controlled receiver. This includes source turn-on, finite elastic shift, source excitation and the full noncoherent field without estimating them separately. It does NOT claim (4a) is the optimal reduced-channel error or a physical lower bound. The square-root amplitude-to-channel estimate remains conservative.

`exact_source_overlap.py` encloses a(T) with a 2x2 rational scaling/squaring certificate, using Euclidean semigroup contraction. For the current frontend sqrt(lambda) is required rational; failure of that frontend restriction is not physical impossibility. The moment proof above is retained as an independent structural argument, but the strongest ordinary exact projection is used when it gives the better finite-rate budget. This is a specified-output overlap, not simulation of the full emitted field.

## 4. Complete comparison survives the actual receiver, without cavity truncation

The source and receiver share only the conserved data Z. Source generation and the subsequent causal controlled passive receiver can be reordered as a mathematical circuit: source interactions on future field time bins commute with earlier receiver interactions, since source/cavity Hilbert spaces are disjoint and both data controls are diagonal. This does NOT assert zero physical cavity response time. The actual receiver acts on the finite field interval and its initial vacuum cavity and retains all output fields and the cavity state at T.

Apply exactly the same controlled receiver unitary, routing beam splitter, and internal-loss dilation to the actual source output and its coherent comparison. Isometries preserve the vector bound, and tracing all environments is contractive. Combining (2) and (3) yields a complete data-channel bound

    ||E_actual(T)-E_coh(T)||_diamond <= delta_TLS,
    delta_TLS = 2[sqrt(2E)+2b/sqrt(lambda)+16b^3 sqrt(T)/lambda],  (4)

for E<=1, capped at2 if desired. The stronger delta_exact in (4a) may replace delta_TLS. No cavity photon-number cutoff, full emission-history simulator, spectral fitting, adiabatic replacement asserted as exact, or arbitrary-environment dilation is used. The proof explicitly compares initialized vacuum/cold inputs. For multiple independent local copies this receives a product of local channels; it is not a uniform circuit-length estimate under arbitrary reuse/control.

## 5. Exact finite-time coherent receiver: endpoint memory and phase retained

In the coherent comparator the incoming amplitude in data branch z is -2ibz. With routing transmissivity eta and receiver total linewidth k, the conditional cavity amplitude obeys

    alpha_z'=-(k/2+i z chi)alpha_z +2ibz sqrt(eta k_e),
    alpha_z(0)=0.

At chi=k/2 set p_c=k(1+i)/2 and zeta=eta k_e/k. The data off-diagonal coefficient satisfies the exact channel identity

    f_coh(T)=exp[-8b^2(1-zeta)T
                 +(4 zeta b^2/p_c)(-3+4exp(-p_c T)-exp(-2p_c T))].  (5)

One derivation keeps the off-diagonal cavity operator proportional to |alpha_+><alpha_-|. Tracing the physical cross-generator gives

    (log f)'=-8b^2-2i chi alpha_-^* alpha_+.

The linear source/cavity feed-forward terms cancel. With alpha_-^*=alpha_+ and the explicit amplitude, integration yields (5), including routing and internal loss. This finite-time expression traces the STILL OCCUPIED cavity and the source/field outputs. It is not a carrier scattering coefficient substituted for an actual gate channel.

For eta=1,k_i=0 and T->infinity,

    f_coh(T)->exp[(-12+12i)b^2/k].                     (6)

There is a nonzero endpoint/transient dephasing floor 1-exp(-12b^2/k) in diamond distance AFTER correcting the deterministic phase, and a deterministic Z phase 12b^2/k. Neither is suppressed merely by increasing lambda. At arbitrary finite T, phase correction uses arg f_coh(T) and is an intended source-blind Z operation whose calibration and implementation errors remain paid. Leaving it uncorrected has error |1-f_coh|, not 1-|f_coh|.

Internal/routing loss reintroduces secular dephasing at rate 8b^2(1-zeta). A fixed nonzero loss cannot support arbitrarily long unencoded coherence. Taking k large reduces the receiver boundary error but also increases the required dispersive shift chi=k/2. This is a real resource tradeoff, not a free receiver-bandwidth limit.

The actual finite-rate operation therefore obeys, after the chosen comparator phase correction,

    ||E_actual-corrected - identity||_diamond
      <= 1-|f_coh(T)| + delta_TLS + epsilon_phase + epsilon_other. (7)

The epsilons must be actual complete bounds for the supplied phase-control/other apparatus. Equation(7) is a sufficient bound, not an optimal lambda requirement or an experimental feasibility claim. The phase operation can also be incorporated into the requested diagonal target; that does not erase calibration costs.

## 5a. Variance-sensitive exact-data-channel receiving (stronger than a generic vector bound)

The full source+field approximation above can be received more sharply for THIS dephasing task; it is not licensed to replace sqrt(N_inc) by N_inc for arbitrary outputs. Let |psi> be the actual positive-data source/field output including all receiver input vacua, and |psi0> its constant-coherent reference. Their overlap a is the exact real number in Section3a, so

    |psi>=a|psi0>+sqrt(delta)|chi>,  <psi0|chi>=0,
    delta=1-a^2.

The negative-data source branch is R|psi>, R=Z_s times field parity. Let U_± be the actual finite-time conditional receiver dilations, retaining final cavity, routing-loss and internal-loss fields. Their common-space relative branch operator O=R U_-^dagger U_+ is unitary (a contraction would suffice). Then

    f=<psi|O|psi>,   f0=<psi0|O|psi0>=f_coh(T).

Write r=|f0|. Orthogonality and ||O||<=1 give

    |<chi|O|psi0>|, |<psi0|O|chi>| <= sqrt(1-r^2).

Expansion therefore proves the exact ordinary geometric bound

    |f-f0| <= delta(1+r)+2sqrt(delta(1-delta))sqrt(1-r^2).  (8)

This controls the COMPLEX coherence, not merely its real part or an assumed stochastic Pauli probability. A qubit dephasing channel with coefficient f differs from one with coefficient g in diamond norm exactly |f-g|: factor out a diagonal phase and use (identity-Ad_Z)/2 for the upper, and input |+> for equality.

After a paid known phase correction arg(f0), a simpler sufficient bound is

    |1-exp(-i arg f0) f|
       <= [sqrt(1-r)+sqrt(delta(1+r))]^2.              (9)

WITHOUT adding any phase correction, if R0>=|1-f0| then 1-r^2<=2R0 and

    |1-f| <= R0+2delta+2sqrt(2delta R0).               (10)

This is the bound used by the stronger exact budget grid. It scales with the reference receiver error, the exact nonreference weight delta, and their geometric mean; it does not assert arbitrary channel errors are linear in the noncoherent photon count. Prematurely tracing the cavity/field and reusing an unjustified overlap operator would invalidate this derivation. In the present actual cascade the full relative isometry construction supplies O.

## 6. Same-task baseline and what has actually changed

Without access to the output field/receiver, the exact original damped-source channel tends at fixed diffusion to f_bare(T)=exp(-8b^2T), a nonzero dephasing floor. With the specified coherent receiver, the lossless coherent comparator instead has bounded-in-T loss of order b^2/k, plus the finite-source remainder (4), whose current sufficient bound grows like sqrt(T/lambda). This does not prove unlimited-time protection at fixed finite lambda or arbitrary gate fault tolerance. It earns a finite-time, finite-source, finite-receiver known-model operation with no photon measurement service and no implicit final ringdown.

Strong ordinary methods remain owners of the mechanism. No-knowledge feedback already cancels Hermitian Markovian decoherence given its actual monitored output and feedback service. Standard all-optical/coherent feed-forward and conditional photon-cavity phase gates supply the component principles here. An equally informed ordinary calculation can use the same cascade and gets the same result; there is no proof of advantage over those methods. The useful work is the actual finite-source-to-coherent-field receiving bound and inclusion of receiver endpoint/loss/phase costs, not a new cancellation principle.

This is more operational than further source-family coverage: it replaces a difficult classical observation/error-free record assumption by an explicitly specified quantum receiver and identifies its paid cross-Kerr/loss requirements. It still does NOT build that receiver or show that the cross-Kerr service is cheaper than observation, dynamical decoupling or ordinary correction in a real architecture. Calibration and physical validity remain the decisive missing evidence.

## 7. Exact sufficient operating budget, costs and failures

`certify_scalar_budget.py` compares a full exact rational grid, retaining failed sufficient budgets. It does not infer feasibility from the grid. It bounds the uncorrected phase AND dephasing using the stronger variance-sensitive receiver, so no free final phase gate is hidden in the following example. With q=(1+kT/32)^(-16)>=exp(-kT/2),

    |log f_coh| <= R=8b^2(1-zeta)T
                  +(4sqrt(2) zeta b^2/k)(3+4q+q^2).

Since Re log f_coh<=0 for this actual coherent channel, |1-f_coh|<=|log f_coh|<=R. Integer square-root ceilings enclose all roots. The unchanged source's earlier exact rational dephasing bracket gives diamond-error lower bound

    2 max(0,4b^2T-8b^2/lambda) max(0,1-8b^2T).

The declared example lambda=4096, b=1/5, T=1, k=128, chi=64, zeta=0.998001, and an explicitly SUPPLIED remaining complete-error allowance 0.001 satisfies a sufficient total error below0.01. The unchanged source error is at least0.21749375. Exact values are in the JSON. This is not superiority over equally equipped coherent feedback or a measured hardware operating point. Source coupling c=64/5, source rate4096, one local bosonic receiver per data qubit, receiver rate128, dispersive shift64, and the combined routing/external-coupling efficiency0.998001 are all real requirements. For example separate routing0.999 and external-coupling fraction0.999 yield that product, but neither efficiency is acquired here. The 0.001 residual apparatus allowance must actually cover preparation, calibration and controls; it is NOT established by this calculation.

The full grid includes source rates64,256,1024,4096,16384,65536,10^6 and receiver rates2,8,32,128,512; many fail the same0.01 sufficient target, and their records are preserved. A failed upper bound is not a lower bound or hardware impossibility. A successful symbolic supplied-input budget is not a calibrated device. Expected source count<=4b^2T does not erase the growing interaction norm c=sqrt(lambda)b, source bandwidth or cold preparation. Heat/power needs the physical energy/frequency implementation; jump counts are not heat by themselves. Receiver finite occupancy/dispersive validity, independent local ports, source/cavity preparation and later target-readout instruments remain specifically unpaid physical evidence.

## 8. Executed evidence and boundaries

`check_coherent_cascade.py` verifies the determinant identity and exact coherent-amplitude/log-coherence differential equation symbolically. It evaluates the FULL finite-source cascaded cross-generator with always-on drive, source and finite cavity, at multiple loss/rate/time settings, comparing cutoffs8 and12 and the analytic coherent expression. These are floating diagnostics only: agreement of two cutoffs is NOT an infinite-mode certificate. The analytical comparison (4), not that diagnostic, removes the cavity truncation from the theorem.

The receiver acts continuously while source coupling, intended diagonal gates and source emissions remain on. Initial preparation and later noncommuting readout/transfer remain separate. The physically supplied Markov source and cross-Kerr cavity are prerequisites, not obtained from an abstract generator certificate. No experiment, equipment, publication, purchase or outreach has occurred.

### Primary ordinary literature actually inspected

- Gough and James, *The Series Product and Its Application to Quantum Feedforward and Feedback Networks*, https://arxiv.org/html/0707.0048 , especially definitions/series cascade and Section6 all-optical/direct-feedback examples. The same L->S L transformation is established machinery.
- Szigeti, Carvalho, Morley and Hush, *Ignorance is bliss: General and robust cancellation of decoherence via no-knowledge quantum feedback*, https://arxiv.org/html/1401.4493 . Measurement-feedback cancellation is a strong ordinary alternative with its own physical information/control assumptions.
- Saiphet et al., *Time-delayed quantum feedback and incomplete decoherence suppression with no-knowledge measurement*, https://arxiv.org/html/2010.06904 . Feedback delay and noncommuting controls cannot be silently ignored.
- Besse et al., *Parity Detection of Propagating Microwave Fields*, https://arxiv.org/html/1912.09896 . Established photon-conditioned cavity/transmon phase operations and their finite-bandwidth/loss/assignment requirements, not a claim that their apparatus implements our actual source-data cross-Kerr network.
