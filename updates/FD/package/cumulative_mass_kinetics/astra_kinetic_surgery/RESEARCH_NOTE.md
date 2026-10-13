# ASTRA FRONTIER: cumulative-mass transport for molecular kinetics

Research checkpoint: 13 October 2026.

## Status and retained objective

The North Star is decision-grade, long-timescale molecular kinetics: predicting and ranking residence or escape times in high-dimensional systems with metastability and hidden conformational gates, without treating the physical waiting time as an unavoidable computational cost.

This checkpoint does not establish a civilisation-changing capability, a state-of-the-art performance improvement, or historical novelty. It develops an explicit conserved-current compiler, derives a uniform non-Gaussian sector requiring no equilibrium sampling, and identifies exactly why the simplest shortcut scheme and single-coordinate reductions can fail. The consequential objective is retained; the tractable sector is not a replacement for it.

The intended eventual application is kinetic design of molecules, including ligand residence-time ranking. No particular ligand or experimentally validated force field was simulated here. The mathematical model below is reversible overdamped diffusion, not general inertial molecular dynamics. A mean starting from equilibrium restricted to a specified pre-exit domain is not automatically an experimental dissociation constant or a reciprocal equilibrium reactive flux.

## 1. Candidate comparison and strongest comparators

Three candidates were examined before choosing kinetics.

1. Strongly correlated chemical energetics: reliable reaction decisions beyond tractable multireference calculations. Fault-tolerant quantum phase estimation is a serious comparator, not a fictitious exact classical diagonalizer. Current resource studies include state-preparation, representation and hardware bottlenecks; the present investigation did not find a more credible new operation there.
2. Radiation-tolerant materials: defect removal without accumulated microstructural damage. Grain-boundary sinks and ab-initio-informed machine-learning potentials are existing mechanisms and simulation tools. Initial defect migration is not a complete solution to continued damage or sink evolution. No sufficiently constrained new actuation mechanism was established here.
3. Rare-event molecular kinetics: reliable residence-time decisions despite metastability. This was selected because it permits a direct attack on the object being computed and because known potential/force oracles can support computational rather than speculative physical interventions.

Matched kinetic comparators must include optimized weighted ensemble (WE), variational/controlled committor methods, milestoning where applicable, and specialized elliptic solvers. WE already has strong variance-reduction theory and high-dimensional applications. The February 2026 revision of Ryu et al. reports optimized trajectory allocation for molecular models. Du et al. (2026) combine stochastic optimal control with reactive-flux-preserving sampling. A July 2026 AIMMD preprint by Lichtinger and Covino reports descriptor-free ligand kinetics over approximately 17 orders of magnitude of residence time. Its abstract was retrieved; full text could not be fetched during this run. Its benchmark claims are reported, not independently replicated here.

Therefore neither "longer timescales than ordinary MD" nor "no hand-designed descriptor" is by itself an adequate novelty or advantage claim.

## 2. Failed mechanism: shortcut dynamics plus a small repair certificate

Let transient states have positive invariant masses m_i, and let physical reversible edge conductances be c_ij=m_i k_ij. Ground the absorbing target. Let D be the grounded incidence matrix, C=diag(c_e), and A=D C D^T. Every transient component must connect to the target, so A is positive definite.

The mean hitting-time field solves A u=m. For the initial distribution m/M, where M=sum_i m_i,

    tau = F/M,       F = m^T A^{-1} m.

Add a positive semidefinite reversible shortcut Laplacian S, keeping the masses fixed. Define

    u_+ = (A+S)^{-1}m,
    F_+ = m^T u_+,
    E_s = u_+^T S u_+,
    r   = S u_+.

Then

    F = F_+ + E_s + r^T A^{-1}r.                         (2.1)

Proof: A u_+=m-r, so u=u_++A^{-1}r. Substituting m=(A+S)u_+ in m^T A^{-1}r gives E_s+r^T A^{-1}r.

For any signed physical-edge current z satisfying D z=r,

    r^T A^{-1}r = min_{D z=r} z^T C^{-1}z <= R(z).

Consequently, L=F_++E_s and U=L+R(z) enclose F. Signed currents are mathematical objects; they are not trajectories or probabilities. Routing through a grounded target is legitimate in this variational problem. For overlapping routes, compute the energy of the summed current; summing individual route energies without a congestion argument is not generally valid.

### The factor-two obstruction

Since E_s <= F_+, a relatively tight certificate R(z)<=epsilon L implies

    F <= (1+epsilon)L <= 2(1+epsilon) F_+.

Thus this particular scheme cannot both make auxiliary exit times arbitrarily shorter and certify the original mean using only a small residual correction. It must reconstruct the removed large waiting-time contribution, rather than merely bound it away.

This is NOT a computational lower bound, a no-go theorem for WE, or a claim that preconditioning cannot help. Auxiliary elapsed time is not the same as computational work. The obstruction concerns the stated shortcut-plus-small-repair mechanism.

### Inexact solver accounting

For any trial field v, not necessarily an exact shortcut solution,

    d = m-A v,
    L(v) = 2m^T v-v^T A v,
    F = L(v)+d^T A^{-1}d.

A feasible current D z=d gives F<=L(v)+z^T C^{-1}z. Approximate divergence conservation alone is insufficient: the remaining defect must also be repaired or rigorously bounded.

## 3. The surviving mechanism: transport the source, not the trajectory

Use coordinates (s,y) in [0,1] x Y, where Y is a transverse domain with periodic boundaries, or an unbounded domain with suitable decay. Initially take unit isotropic diffusion. The generator is

    L f = m^{-1} div(m grad f).

The surface s=1 absorbs; s=0 reflects. The initial distribution is m divided by its total mass. Assume smooth positive m, a nonexplosive process, appropriate reflecting/decaying transverse boundary conditions, and finite energies below.

Write

    m(s,y)=w(s) p_s(y),       integral p_s(y)dy=1,
    M(s)=integral_0^s w(t)dt,       Z=M(1).

Suppose v_s(y) is any finite-action transport velocity satisfying

    partial_s p_s + div_y(p_s v_s)=0.                    (3.1)

This is a relationship between conditional densities; it does not assert that the bath equilibrates rapidly in physical time.

Define the computational source current

    J_s(s,y)=M(s)p_s(y),
    J_y(s,y)=M(s)p_s(y)v_s(y).

Its divergence is exactly

    div J = w p_s + M partial_s p_s + M div_y(p_s v_s)
          = m.                                         (3.2)

This current accounts for the source at every configuration, not only for a transition path or a selected basin.

### Transport-action residence-time bound

Define

    tau_0 = (1/Z) integral_0^1 M(s)^2/w(s) ds,
    K(s)  = integral |v_s(y)|^2 p_s(y)dy.

Then

    tau_0 <= tau <= tau_0
        + (1/Z) integral_0^1 [M(s)^2/w(s)] K(s) ds.       (3.3)

In particular, K(s)<=kappa throughout gives

    tau_0 <= tau <= (1+kappa)tau_0.                      (3.4)

No spectral gap or conditional mixing-time assumption is present. The formula does not imply that K, w, or v are easy to acquire.

### Proof

Let A=-div(m grad) with the stated boundaries. If A u=m, then F=<m,A^{-1}m>=Z tau. The standard primal variational principle says

    F = sup_phi [2 integral m phi - integral m |grad phi|^2].

Take

    phi(s)=integral_s^1 M(t)/w(t)dt.

Changing integration order gives integral m phi=integral M^2/w, and its gradient energy is the same. Therefore F>=integral M^2/w.

For any current div J=m with zero reflecting normal flux, the standard dual principle gives

    F <= integral |J|^2/m.

Substituting (3.2) gives integral (M^2/w)(1+K), proving (3.3). These primal/dual principles are established mathematics. The application and explicit compiler developed here require a separate novelty investigation; no priority claim is made.

### Mobility is not free

For constant block diffusion diag(D_s,D_y), with D_s>0 and D_y positive definite, replace tau_0's integrand by M^2/(w D_s), and replace the transverse penalty by (M^2/w) E[v_s^T D_y^{-1}v_s]. The dimensionless relative penalty is D_s E[v_s^T D_y^{-1}v_s]. Slow physical mobility is charged. The absence of a spectral-gap assumption is not permission to ignore diffusion coefficients.

## 4. An acquisition-free non-Gaussian sector

Consider the explicit structural model

    U(s,y)=V(s)+U_0(y-b(s)),                              (4.1)

with m=exp(-beta U), unit isotropic diffusion, y periodic or unbounded, and a normalizable transverse bath. U_0 may have strong interactions, many metastable wells, and non-Gaussian statistics. Let

    w(s)=exp(-beta V(s)),
    f_0(y)=exp(-beta U_0(y)),
    Z_0=integral f_0(y)dy.

Z_0 need not be known. The normalized conditional density is a translation of f_0/Z_0, and v_s=b'(s). Formula (3.3) becomes

    tau_0 <= tau <= tau_0
       + [integral M(s)^2/w(s) |b'(s)|^2 ds]/M(1),       (4.2)

where now M(s)=integral_0^s w(t)dt and tau_0 is formed from w alone.

Every occurrence of Z_0 cancels. No call to an equilibrium sampler or to a bath partition-function estimator is required to evaluate (4.2). Indeed, the algorithm need not evaluate U_0 at all, provided the exact structural representation (4.1) is a valid input assumption.

This is not weak coupling: U_0 can be arbitrarily interacting and barriers can be arbitrarily high. It is nevertheless a strong geometric restriction. Conformational populations are transported together; they do not undergo arbitrary s-dependent reweighting. The bound can be wide if |b'| is large. The restricted mean need not describe other initial preparations, inertial kinetics, or a real ligand without model validation.

A selected-design decision is immediate: disjoint intervals for two specified models establish their residence-time ordering. A ratio threshold r is certified if the lower endpoint for model A exceeds r times the upper endpoint for B.

### Complete one-dimensional query accounting for a simple enclosure

Let ell(s)=log w(s) have a supplied, valid Lipschitz constant L on [0,1]. Suppose |b'|^2<=kappa is a supplied or analytically certified global bound. Partition [0,1] into N equal cells and evaluate ell at each midpoint with error at most zeta. Let w_tilde be the corresponding positive step function.

For delta=zeta+L/(2N),

    exp(-delta) w_tilde <= w <= exp(delta) w_tilde.

The cumulative masses have the same multiplicative enclosure. Therefore

    exp(-4delta) tau_tilde <= tau_0 <= exp(4delta) tau_tilde.

For the full translated-bath model,

    exp(-4delta) tau_tilde <= tau
       <= (1+kappa) exp(4delta) tau_tilde.               (4.3)

The upper/lower ratio is (1+kappa)exp(8delta). With zeta=0, obtaining an additional quadrature ratio at most 1+epsilon requires

    N >= 4L/log(1+epsilon).

This is O(1+L/epsilon) potential evaluations for small epsilon, plus a linear number of positive arithmetic operations, and no bath queries. It is not a uniform complexity statement without a supplied regularity bound. Energy-oracle and finite-precision arithmetic costs remain part of the implementation. Exponentials and positive sums can be evaluated by relative-error arithmetic with explicit error budgets; an interval implementation is not included in this checkpoint.

The step-function expression is exact: if a cell has width h, weight w_i and entering cumulative mass H_i, its contribution to the numerator is

    H_i^2 h/w_i + H_i h^2 + w_i h^3/3.

The output magnitude can be exponentially large while the 1D query count need not scale with that magnitude. This is not proof of superiority to the strongest specialized method on the same structured class; those methods also have access to its simplifying representation.

## 5. Removing the normalized-density input: a cumulative-mass map compiler

For a general model, neither w(s) nor p_s need be available. The following formula defines a feasible current directly from an unnormalized density oracle and a full-dimensional map.

Let x=T(s,z) be an orientation-preserving C^2 diffeomorphism from [0,1]xY onto the entire modeled pre-exit domain. The image of s=1 is absorbing, and the other boundaries are reflecting/periodic/decaying. Write

    J_T=det DT>0,
    mu(s,z)=m(T(s,z)) J_T(s,z),
    H(s,z)=integral_0^s mu(t,z)dt,
    mbar(s)=integral mu(s,z)dz,
    M(s)=integral H(s,z)dz,
    t(s,z)=partial_s T(s,z),
    eta(s,z)=DT(s,z)^{-T} e_s.

Let the physical diffusion tensor be Dcal(x)>0. Define

    a(s)=integral mu eta^T Dcal eta dz.

The trial potential is

    phi(T(s,z))=integral_s^1 M(t)/a(t)dt.

The cumulative-mass current is

    j(T(s,z))=H(s,z) t(s,z)/J_T(s,z).                   (5.1)

The change-of-variables identity for divergence gives div_x j=m exactly, because partial_s H=mu. Source matching is therefore built into the representation. It is not an approximate neural divergence penalty.

Set

    F_L=integral_0^1 M(s)^2/a(s) ds,
    F_U=integral_0^1 integral [H(s,z)^2/mu(s,z)]
                         t^T Dcal^{-1}t dz ds.

Then

    F_L/M(1) <= tau <= F_U/M(1).                        (5.2)

There is also an explicitly nonnegative width formula:

    F_U-F_L = integral [j+m Dcal grad phi]^T
                         (m Dcal)^{-1}
                         [j+m Dcal grad phi] dx.        (5.3)

Proof: the primal source pairing and gradient energy both equal F_L. Since div j=m, integration by parts gives integral j.grad phi=-F_L. Expanding the square proves (5.3), and the standard primal/dual bounds give (5.2).

A constant rescaling of m rescales both F endpoints and M equally. No equilibrium normalizer is an input. With a tractable reference density rho(z), mu/rho and H/rho permit writing the integrals as reference expectations. Drawing reference samples is easy; obtaining certified concentration and useful importance-weight moments is not assured.

A single thin path does not supply T. A map covering only observed transition tubes does not certify an omitted part of configuration space. Multichart or branching constructions must conserve source and normal current at their interfaces. An approximation to H must either be evaluated as a rigorously bounded integral of the exact definition, or have its divergence error accounted for separately.

## 6. What makes a map useful: geometry AND conditional mass

In the density-factorized special case mu(s,z)=w(s)rho(z), define

    A_s=E_rho[eta^T Dcal eta],
    B_s=E_rho[t^T Dcal^{-1}t].

Then

    F_L=integral M^2/(w A_s),
    F_U=integral (M^2/w)B_s.

Since eta.t=1, Cauchy-Schwarz implies A_s B_s>=1. A supplied bound A_s B_s<=1+epsilon yields F_U<= (1+epsilon)F_L. High energy barriers remain in 1/w but do not explicitly worsen this relative enclosure. Acquiring such a map can still contain the original difficulty.

For a general map, let

    p_s(z)=mu(s,z)/mbar(s),
    q_s(z)=H(s,z)/M(s),
    g(s,z)=t^T Dcal^{-1}t,
    A_s=E_{p_s}[eta^T Dcal eta].

The local upper/lower integrand ratio is

    Lambda(s)=A_s integral q_s(z)^2 g(s,z)/p_s(z) dz.     (6.1)

The distribution q_s is cumulative source mass along map fibers, whereas p_s is instantaneous conditional equilibrium mass. Ordinary density fitting is not the entire objective.

If g<=G_s, then

    Lambda(s)<=A_s G_s [1+chi^2(q_s || p_s)].             (6.2)

This exposes two distinct failure modes: large metric distortion and poor conditional mass overlap. The actual relative width is a residence-weighted average of Lambda-1; a supremum bound is sufficient but can be loose.

For p=N(0,I_n) and q=N(0,a^2 I_n),

    1+chi^2(q||p)=[a sqrt(2-a^2)]^{-n},     0<a<sqrt(2),

and the integral diverges for a>=sqrt(2). A 10% width mismatch (a=1.1) at n=1000 produces approximately 6.219696549e9. This is an overlap/energy diagnostic, not a measured runtime or a universal sample-complexity lower bound.

### Why a centerline cannot repair the problem

A current through a tube of cross-sectional area A(s), with conductivity bounded above by kappa(s), has resistance at least integral ds/[kappa(s)A(s)] for unit axial current. In d dimensions a narrow tube may have A proportional to radius^(d-1). A finite-width thermal representation is therefore essential; a single plausible molecular trajectory is insufficient.

## 7. An exact obstruction from genuinely changing gates

The translated-bath sector transports existing populations without arbitrary reweighting. It does not solve a gate whose occupancy changes along the escape coordinate.

For a one-dimensional transverse coordinate on the line, let P_s(y)=integral_{-infinity}^y p_s(t)dt. With zero flux at infinity, the continuity equation forces

    p_s(y)v_s(y)=-partial_s P_s(y).

Thus the transport action is

    K(s)=integral [partial_s P_s(y)]^2/p_s(y)dy.          (7.1)

If a gate interval of length ell has p_s<=delta while |partial_s P_s|>=c there, then

    K(s)>=ell c^2/delta.                                (7.2)

An exponentially depleted gate can therefore reappear explicitly as a large transport cost. This does not prove exponential computational complexity: a large resistance can be reconstructed by quadrature if its full thermal geometry is known. It does show why merely translating an unknown bath is not a solution to general hidden-gate kinetics. The retained problem is to acquire and integrate those finite-width gate currents without paying the original sampling cost.

## 8. Diagnostics actually executed

The accompanying verify.py ran in this session. It uses SymPy exact rational arithmetic for the finite graph tests.

- 24 connected finite graphs, 2 through 6 transient states, with 240 exact assertions covering the shortcut identity, feasible signed routing, bounds, inexact primal fields, factor-two inequality and fixed-mass conductance monotonicity.
- Four two-exit fixtures and one hidden-trap fixture. All underlying fixture expressions and bracket checks are exact rational calculations; displayed decimals are rounded.
- A symbolic variable-width Gaussian map checks div j=m and the analytic bracket [1/3,(1+n gamma^2)/3]. This is a manufactured geometry test, not a molecular application.
- An arbitrary-function translated-bath symbolic test checks source conservation and partition-function cancellation without assuming a Gaussian bath.
- The Gaussian overlap diagnostic is evaluated analytically.
- A 64-cell step-function calculation for w=1+s uses exact rational arithmetic. Its enclosure comparison against the known log(2) expression is a numerical check of an analytically justified bound, not a fully implemented interval-arithmetic backend.

Representative graph outputs, in arbitrary time units:

| Case | Exact original mean | Auxiliary mean | Certified lower | Certified upper |
|---|---:|---:|---:|---:|
| Equal exits | 1,000,000 | 1,000,000 | 1,000,000 | 1,000,000 |
| 10% exit asymmetry, sink route | 1,010,100.989695 | 1,000,000.005000 | 1,000,000.010000 | 1,010,101.010101 |
| Hidden trap | 500,002,000,000 | 2,000,000.500000 | 2,000,001.000000 | 500,002,000,000 |

The hidden-trap fixture has mass one at each of two transient states, conductance 10^-6 from state 1 to the sink, conductance 10^-12 between the states, and artificial shortcut conductance one between them. The broad interval correctly refuses to certify the accelerated residence time as physical.

These are algebra and adversarial tests. They establish neither general proof correctness by themselves nor practical superiority. An explicit small graph should be solved by a specialized direct/sparse linear solver; the present method has no demonstrated advantage there.

## 9. Full resource and assumption ledger

### Inputs and model

A potential/unnormalized-density oracle is not a calibrated kinetic model by itself. Mobility, temperature, absorbing boundaries, source preparation, constraints, and the adequacy of overdamped dynamics must be specified. Force-field/model uncertainty is distinct from numerical error. The bounds certify the specified model and initial law, not biological efficacy or measured kinetics automatically.

### Representation acquisition

The exact translated-bath representation is an input premise. Inferring it from finitely many potential evaluations over an unrestricted unknown function class is not free. For general models, finding an invertible, source-covering map with small Lambda may be as hard as the original kinetic problem. No polynomial acquisition guarantee has been proved.

### Computation and precision

A general map evaluation requires energy values, map Jacobians and derivatives, cumulative one-dimensional integration, and transverse integration. A generic dense d-dimensional Jacobian has material algebraic cost; a tractable architecture must be charged for its restrictions. Training, unsuccessful searches, independent validation, precision and tail bounds all count. Sample averages without validated uncertainty do not turn the exact formulas into certified numerical output.

### Preparation and physical control

The proposal is computational. It does not require a laboratory to prepare an equilibrium specimen, implement arbitrary nonlocal jumps, or supply independent physical replicas. But converting its model-defined equilibrium initial average into an experimental residence time requires a preparation/model argument. No claim is made about quantum state preparation or physical barrier removal.

### Energy

No physical energy-saving device has been constructed. Computational energy would need to include all training, integration and validation. No energy or hardware-speed advantage was measured.

### Comparator fairness

The translated-bath and Gaussian manufactured examples are favorable to specialized direct mathematics and one-dimensional reduction; they are not evidence of scientific advantage. Every method in a future comparison should receive identical potential/force access, model, target, source, precision requirements and any supplied transport structure. Charge WE/committor acquisition and also charge the candidate's map training and validation. Compare total calls, wall time and confidence/coverage, not only simulated physical time.

## 10. Novelty and priority ledger

Established ingredients include Dirichlet/Thomson principles, reversible potential theory, divergence-preserving changes of variables, conditional-expectation coarse-graining, and functional a posteriori error estimates. Learned auxiliary fields for rigorous elliptic error majorants are prior art. Committor control, flux-preserving sampling, descriptor learning and variance-optimal trajectory allocation are also prior art.

The candidate to investigate is the concrete combination of cumulative-source current compilation, geometry/conditional-overlap training objectives, and kinetic decision validation without equilibrium sampling as a compulsory input. Its exact special cases and the shortcut obstruction were derived here, but no exhaustive priority search or independent proof audit was completed. A rediscovery remains possible. No theorem from the optional Astra or OpenAI repositories is a mathematical premise.

## 11. Decisive continuation, preserving the objective

Do not restart the domain search. The next substantive task is a resource-accounted gate experiment: a reversible high-dimensional potential with several competing exit channels, an independently adjustable gate barrier, and many coupled spectators. It must not be a product model supplied in useful coordinates. Hide the useful map from every method, but expose the same energy/force oracle.

Develop a multichart or branching cumulative-mass representation with exact source conservation. Optimize the actual residence-weighted primal/dual gap, not just density likelihood or transition-path appearance. Obtain numerical confidence with held-out reference integration and rigorously accounted quadrature/tails. Test whether map discovery and overlap control avoid exponential cost when the gate barrier and spectator count increase independently.

Success requires cheaper correctly covered lifetime intervals or reliable kinetic ranking than optimized WE and current committor/path-sampling baselines at matched total cost. A modest implementation improvement is not the North Star. Failure is scientifically informative if it locates the cost in map topology, gate conductance acquisition, conditional overlap, initial-law specification or model error. Preserve that failure and replace the representation rather than retreating to more certificates on a supplied easy map.

## References and source-access ledger

These references establish comparators and mathematical lineage, not the novelty of this checkpoint.

- Ryu et al., *Reducing Weighted Ensemble Variance With Optimal Trajectory Management*, arXiv:2504.21663, v3, 9 February 2026. https://arxiv.org/abs/2504.21663
- Aristoff et al., *Weighted ensemble: Recent mathematical developments*, J. Chem. Phys. 158, 014108 (2023), arXiv:2206.14943. Original mathematical discussion/results; PDF and relevant pages inspected. https://arxiv.org/abs/2206.14943
- Du et al., *Rare Event Analysis via Stochastic Optimal Control*, arXiv:2604.13213v3 (2026). Full HTML inspected. https://arxiv.org/html/2604.13213v3
- Lichtinger and Covino, *Accelerated descriptor-free path sampling for protein-ligand binding kinetics*, arXiv:2607.15101 (16 July 2026). Search-index abstract retrieved; full-text fetch failed. Benchmark claims not independently checked. https://arxiv.org/abs/2607.15101
- Kang, Trizio and Parrinello, *Computing the committor with the committor to study the transition state ensemble*, Nature Computational Science 4, 451-460 (2024), arXiv:2401.05279. https://arxiv.org/abs/2401.05279
- den Hollander and Jansen, *Berman-Konsowa principle for reversible Markov jump processes*, arXiv:1309.1305; Markov Processes and Related Fields (2016). Primary variational-potential-theory lineage. https://arxiv.org/abs/1309.1305
- Fanaskov, Rudikov and Oseledets, *Neural functional a posteriori error estimates*, arXiv:2402.05585 (2024). Abstract and full HTML accessed. https://arxiv.org/html/2402.05585v1
- Li and Zhang, *Non-intrusive Least-Squares Functional A Posteriori Error Estimator: Linear and Nonlinear Problems with Plain Convergence*, arXiv:2407.13253. https://arxiv.org/abs/2407.13253
- Legoll and Lelievre, *Effective dynamics using conditional expectations*, Nonlinearity 23 (2010), arXiv:0906.4865. Abstract inspected; do not interpret the citation as an exhaustive comparison with all subsequent coarse-graining work. https://arxiv.org/abs/0906.4865
- Kanasugi et al., *Enabling Chemically Accurate Quantum Phase Estimation in the Early Fault-Tolerant Regime*, arXiv:2603.22778v2 (2026). Candidate-selection resource study; not a demonstrated deployed capability. https://arxiv.org/abs/2603.22778
- Suarez-Recio et al., *Early Stages of Self-Healing at Tungsten Grain Boundaries from Ab Initio Machine Learning Simulations*, arXiv:2505.13744v2 (2025). Candidate-selection physical-mechanism study. https://arxiv.org/abs/2505.13744

Optional research-repository READMEs were inspected only for orientation. This was not an exhaustive audit of their contents or novelty overlap.
