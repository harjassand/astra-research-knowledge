# Continuum coherent packets as certified quantum instruments

28 October 2026. New successor construction. The accepted baseline theorem remains unchanged. No generic efficient solver or physical device point is claimed.

## Purpose and prior work

The question is whether nonlinear source dynamics, all emitted photons, and subsequent detector records can be evaluated with a checkable channel error without constructing a photon-cutoff tensor product.

Superposed coherent states and equation residuals are established methods. Gheeraert, Bera and Florens, NJP 19, 023036 (2017), arXiv:1601.01545v2, already compute squared Schrodinger residuals for multimode coherent packets. Bera, Baranger and Florens, PRA 93, 033847 (2016), arXiv:1601.00531v2, expose physical artifacts of a single-packet ansatz. General variational a posteriori error estimates also predate this work.

The bridge here combines nonlinear Weyl closure, an operator residual on an input code, controlled packet compression, and lossy multiport quantum instruments. Worldwide novelty of individual identities is not claimed.

## Setting

Let h be a one-particle Hilbert space, F(h) its Fock space, and J:C^d -> H_s an isometric input embedding. Inner products are conjugate linear first. Define W(beta)=exp[a†(beta)-a(beta)] and |alpha>=W(alpha)|vac>. Claims are uniform on the declared code, including arbitrary references. They are not full-source diamond claims if the code is a proper subspace.

Use a strongly measurable bounded self-adjoint interaction-picture generator with integrable operator-norm bound H(t)=H_s(t)+sum_l B_l(t) tensor W(beta_l(t)), with adjoint-paired terms. Integrals are strong vector integrals, not a claimed operator-norm Bochner integral. Weyl evolution is strongly continuous but generally not norm-continuous. The source may remain infinite dimensional if its required vector actions and overlaps are evaluable. Unbounded generators need separate domain work. Since sin Phi(f)=[W(if)-W(-if)]/(2i), source and bath sine products are finite Weyl sums even at strong field.

For f_t(omega)=sqrt(rho(omega))exp(i omega t), C(s,t)=<f_s,f_t> evaluates all displacements built from finite combinations of f_t. Finite phase mass suffices. No frequency grid or photon cutoff is intrinsic.

## Exact formulas and residual theorem

The coherent overlap is G(j,k)=exp[-||alpha_j||²/2-||alpha_k||²/2+<alpha_j,alpha_k>]. Moreover

    <alpha_j|W(beta)|alpha_k>
      =G(j,k)exp[-||beta||²/2+<alpha_j,beta>-<beta,alpha_k>],
    W(beta)|alpha>=exp(i Im<alpha,beta>)|alpha+beta>.

H maps a finite packet list to a finite generated list. H² products must be evaluated in full space: squaring projected H loses its exterior component. For source input |0>,|1>, use displaced Fock states D(a)|n>. For delta=b-a,

    <n|D(a)†D(b)|m>=exp(i Im<a,b>)exp(-|delta|²/2)
                    [[1,-delta*],[delta,1-|delta|²]]_(n,m).

Output leakage is untruncated. Higher finite input polynomials use finite displacement matrix elements.

Let V(t):C^d -> H_s tensor F(h) be piecewise absolutely continuous, R=dot V+iHV, and V_exact(t)=U(t)(J tensor |vac>). With internal jumps Delta V_k,

    ||V_exact(T)-V(T)|| <= epsilon,
    epsilon=||V_exact(0)-V(0)||
            +integral sqrt(lambda_max[R(t)†R(t)])dt
            +sum_k ||Delta V_k||.                            (1)

Proof: variation of constants transports residuals and jumps with the exact unitary. Take operator norms, which are unchanged by adjoining any reference identity. A mean-state residual is insufficient.

If V(T) is isometric, its full-output channel half-diamond error is <=epsilon: purified output trace distance is bounded by vector difference norm. Otherwise, for epsilon<1, polar repair V_bar=V(T)[V(T)†V(T)]^(-1/2) gives an isometry and error <=2epsilon. Each singular value of V lies within epsilon of one, so ||V_bar-V||<=epsilon. This is a computational CPTP approximation, not a physical herald or reset.

For fixed packets V=sum_j X_j(t) tensor |alpha_j>, its residual is another finite list R=sum_mu Y_mu tensor |gamma_mu>, and

    R†R=sum_(mu,nu)<gamma_mu|gamma_nu>Y_mu†Y_nu.               (2)

This retains exterior directions, source leakage and input-column coherences. An enclosed numerical matrix Q requires a proved perturbation allowance, e.g. lambda_max(Qhat)+||Q-Qhat||_2. Clipping roundoff eigenvalues is not certification. Kernels, time quadrature and matrix functions need separate bounds; sampled residuals are diagnostics.

## Ultraviolet regularity

The inherited ideal-line rho has finite mass but divergent second frequency moment. Thus t -> f_t is continuous in h but need not have a strong derivative. Moving packets alpha(t)=c f_t are not automatically differentiable; do not insert a nonexistent dot f_t. Fixed packets per smooth segment avoid this: only X_j(t) is differentiated and H(t)V(t) uses the actual kernel. Integrated displacements alpha(t)=integral_0^t u(s)f_s ds are another differentiable choice under suitable continuity assumptions. A useful modulus is

    ||f_t-f_s||² <= (t-s)² integral_0^Omega omega²rho(omega)domega
                   +4 integral_Omega^infinity rho(omega)domega.        (3)

Certified finite-frequency integrals and tail mass, with Omega selected for the time interval, can enclose quadrature without a divergent global derivative. This is representation regularity, not a physical noise rate.

## Packet compression theorem

For an isometry V and orthogonal retained-output projection P, put D=V†(I-P)V and delta²=lambda_max(D)<1. Then

    V_tilde=PV(I-D)^(-1/2),
    ||V-V_tilde||=sqrt[2(1-sqrt(1-delta²))].                  (4)

Proof: V†V_tilde=sqrt(I-D), so the squared difference operator is 2[I-sqrt(I-D)]. V_tilde is isometric. Charge (4) as a knot jump in (1). It scales as delta, not delta²: discarded probability alone cannot bound coherent error.

For bath-only compression let G_B be the retained Gram matrix and C_rj=<beta_r|alpha_j>. The discarded kernel is G_A-C†G_B^+C; contract with X_j†X_k to get D. The exact Moore-Penrose inverse is legitimate on the span. A floating ill-conditioned inverse needs enclosure or validated rank selection. Coefficient-weighted selection is a heuristic; D certifies a chosen projection after the fact.

## Detectors and the kernel-realization bridge

A local scalar rho does not identify collected outgoing ports. Supply a passive output isometry and collection/efficiency maps L_r, with E_r=L_r†L_r>=0 and sum E_r<=I. The complement includes uncollected and intrinsic-loss reservoirs. The E_r need not commute: their dilation has distinct output ports.

Equivalently, on all dynamically visited vectors f_x supply kernels G(x,y)=<f_x,f_y> and D_r(x,y)=<f_x,E_r f_y>. Requiring every finite matrix D_r>=0 and sum D_r<=G suffices to realize bounded forms and compatible passive effects on the quotient/completion of span{f_x}. The full proof is in ../knowledge_and_comparator/DETECTOR_KERNEL_INTERFACE.md, with an actual independent proof reading. This is useful because circuit-transfer kernels can be supplied directly without assigning artificial independent local baths.

No registered photon in ports D has effect Gamma(I-sum_D E_r), with

    K_D(k,j)=exp[-||alpha_k||²/2-||alpha_j||²/2
                 +<alpha_k,(I-sum_D E_r)alpha_j>].           (5)
    I_no,D(rho)=sum_(j,k)K_D(k,j)X_j rho X_k†.                (6)

K_D is a positive-operator Gram matrix, so (6) is CP. For no-click ports N and click ports C,

    K_(N,C)=sum_(D subset C)(-1)^|D| K_(N union D).           (7)

Positivity follows from the physical output dilation, not independent emissions. Pattern maps sum to the reduced source channel. Gamma(I-E1)Gamma(I-E2) must not replace Gamma(I-E1-E2). Numerical cancellation in (7) needs enclosure. Replacing the one-particle factor by I-sum E_r+sum z_r E_r gives joint number-resolved generating kernels. Known passive time/frequency filters are allowed. Nonlinear detectors need another model; correlated classical dark counts require a joint distribution.

Every common supplied detector dilation, instrument, trace or later channel preserves (1). A mathematical completion is not a physical erasure flag.

## Rare events and dependence

For event effect F, p_V(psi)=||F^(1/2)V psi||², and operator error epsilon,

    max(0,sqrt(p_V)-epsilon)² <= p_exact
      <= min(1,(sqrt(p_V)+epsilon)²).                        (8)

For an input-uniform upper bound substitute sqrt(lambda_max[V†FV]). This amplitude bound can be sharper for rare events than assigning a global channel error directly to probability. It is unconditional; normalization on acceptance requires its denominator.

Occupied/empty click marginals q1,q0 imply only max(0,q0-q1)<=w_wrong_only<=min(q0,1-q1). The inherited product w=(1-q1)q0 additionally needs independent matched converters. For q1=.999,q0=.001 the marginals allow w=.001, while independence gives .000001. The kernel computes joint errors instead of assuming the smaller product. This is not a claim that the earlier physical converters exhibit the adverse extremum.

## Boundaries

This interface removes the need to store a Fock tensor or replace the actual bath by Markov loss. Packet number may still grow rapidly and near dependence can defeat floating arithmetic. No small residual at modest cost is guaranteed. The inherited strong-core/weak-continuum representation remains useful for choosing packets or hybrid evaluation and keeps its accepted scope. Accepted undecidability foundations are neither reopened nor contradicted: these are finite-instance checkable certificates, without a uniform efficient-completion promise.

A physical P2 calculation still needs actual circuit and collection kernels, waveform, input state and all additional control/loss channels. The baseline certificate cannot be transplanted to the notch. The accompanying declared mathematical benchmarks are not the baseline operation, device error rates or workload advantages.
