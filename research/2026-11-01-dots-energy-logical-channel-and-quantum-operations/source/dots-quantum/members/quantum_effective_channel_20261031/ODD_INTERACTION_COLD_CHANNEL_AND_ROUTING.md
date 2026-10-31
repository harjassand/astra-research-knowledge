# Cold-source O(1/lambda) logical reduction by explicit selection rules

Status: new candidate. This is an ordinary energy/adiabatic-elimination refinement and a conditional source-design rule, not a new cooling primitive or an automatic modification of a fixed physical bath. Output is the complete SYSTEM/reference and prescribed SYSTEM-ONLY instrument records; no bath or jump output is promised.

## 1. Exact selection premises

Receive a finite dark source G=sum_j D[L_j], psi, P=|psi><psi|, Q=I-P, H=.5sum L_j dagger L_j, gQ<=H<=hQ and G dagger H<=-kappa H. All encodings, norm bounds, preparation and reflection costs are acquired, not inferred from a norm promise. H0 acts on the system. The Hermitian coupling K is P/Q-ODD:

    PKP=QKQ=0.

For each supplied jump, its output lies wholly in P or wholly in Q:

    either P L_j=L_j or Q L_j=L_j.

Together with L_j P=0 these premises imply L_j dagger F(O)L_j=0 for every source-off-diagonal F(O). They permit recycling QL_jQ, not only direct return to the dark state.

Define S=H_Q^(-1)QKP+PKQH_Q^(-1), s>=||S||, F(O)=i[S,I tensor O]. Let b>=||K||, C>=||sqrt(H)K||, d>=||[H0,K]|| and gamma0=2d/g+8b s^2. Physical evolution is lambda G-i[H0+sqrt(lambda)K,.]. Source initially has E0=Tr(H rho0)=0, hence it is psi and uncorrelated with the possibly arbitrary system/reference state. This is a genuine COLD INPUT premise, not a statement for all initially excited sources. Preparation or a certified cold physical source is paid.

The effective GKSL stack is E_stack=sqrt(2)(H_Q^(-1/2) tensor I)K(psi tensor I). Put D(O)=<psi|i[K,F(O)]|psi> and L_eff=L0+D. This stack orientation and the general first-corrector identities are also directly derived below; there is no inverse of the full source generator in the implementation.

## 2. Why the leading state-dependent defect vanishes

The general first off-diagonal corrector identity is

    G dagger F+VP = Q i[K,I tensor O]Q + sum_j L_j dagger F L_j.

Both terms are zero under the stated premises. Hence G dagger F=-VP exactly. The product of two off-diagonal source operators is block diagonal. Thus

    A=VF-P_embed D

is QQ-supported, since its P block is zero by the definition of D. Its norm is at most8bs, and therefore for a state of source energy E,

    |Tr rho A(O)|<=8bs E/g, ||O||<=1.

The remaining residual R0=[L0,F]-F D is source off-diagonal, with norm at most gamma0. For an off-diagonal operator X of norm a, positivity/Cauchy-Schwarz gives |Tr rho X|<=2a sqrt(Tr Q rho). This is valid after adjoining any reference. Consequently

    |Tr rho R0(O)|<=2gamma0 sqrt(E/g).

The endpoint corrector has |Tr rho F(O)|<=4s sqrt(E/g). Initially it is zero because E0=0. For a system-only instrument, its defect C_j dagger F-F C_j dagger remains off-diagonal. If its acquired complete norm is nu_j, its state expectation is at most2nu_j sqrt(E/g). All records are retained; this does not bound postselected rare outcomes separately.

These support statements, not an appeal to vanishing odd powers in a formal series, are what improve the finite-rate error. They fail in general for merged jumps with coherent P+Q output or for a nonzero QKQ interaction.

## 3. Energy, controls and the complete logical bound

For every state, |Tr i[K,H]rho|<=2C sqrt(E). With the source drift, Young's inequality gives

    E'(t)<=-(lambda*kappa/2)E(t)+2C^2/kappa.

From E0=0, E(t)<=4C^2/(lambda*kappa^2). System-only CPTP instruments leave unconditional source energy unchanged, so the same envelope holds across prescribed controls, including record-dependent feedback.

Use the common analysis intertwiner T=P_embed+lambda^(-1/2)F. Exact residual:

    L_lambda T-T L_eff=A+lambda^(-1/2)R0.

Duhamel is evaluated on ACTUAL evolved states and effective backward observables; the latter remain contractions. The initial endpoint vanishes, the final endpoint is energy-weighted, and the control defects are treated once each. Integrating the preceding bounds yields

    error <= min(2, [8sC/(kappa sqrt(g))
       +32bs C^2 T_total/(kappa^2 g)
       +4C(gamma0*T_total+sum_j nu_j)/(kappa sqrt(g))]/lambda).

This is complete trace-norm error on the retained system/reference/control-record output. The compared effective evolution is genuinely CP. T is only a proof device, not a state-preparation oracle. No source reset occurs between controls. No H0 bandwidth enters admission except through d, while its actual execution remains paid.

For initially excited inputs one must keep the initial/final endpoint energy terms and the transient energy integrals; in general they retain O(sqrt(E0)/sqrt(lambda)). Do not promote this cold O(1/lambda) estimate to arbitrary source inputs. Source controls may inject energy and violate the envelope; they are excluded unless separately accounted for.

## 4. A conditional algebraic source redesign, and its actual price

Suppose a starting centered K has PKP=0 but may have QKQ, and jumps may have mixed output. Define NEW jumps and NEW coupling

    L_(j,0)=P L_j, L_(j,1)=Q L_j,
    R=P-Q,
    K_odd=(K-R K R)/2=PKQ+QKP.

These generally CHANGE the physical generator and interaction. They are not a change of unraveling of the same G. Nevertheless

    sum_(j,a) L_(j,a) dagger L_(j,a)=sum_j L_j dagger L_j=2H,
    G_split dagger H=G dagger H,
    K_odd P=KP.

The second equality follows from PHP+QHQ=H in the recycling term. Thus the same H, gap and H-energy drift certificate survive, and the leading effective stack is identical. The new source/interaction obey the selection premises. Its injection norm is ||sqrt(H)K_odd||=||sqrt(H)QKP||, so removing QQ interaction can also remove a large irrelevant energy bound. Certified upper norms and actual block normalizations remain distinct.

### Acquired quantum-circuit interface

Given an acquired stacked jump block encoding of normalization alpha_L, append a flag, apply H_flag, controlled-R to the OUTPUT source, then H_flag. The flag0/1 branches are exactly P L_stack and Q L_stack with unchanged normalization alpha_L. Retain the flag as a new jump color. This is a coherent routing operation, not a normalized measurement of P. A reflection R is acquired from the actual psi-preparation circuit U_psi as U_psi(2|0><0|-I)U_psi dagger; its preparation/unpreparation, source-register zero test and controlled gates are paid.

Given a K block encoding of normalization alpha_K, a two-arm LCU for K and -RKR gives K_odd/alpha_K. The coefficient sum is one; no free normalization by the smaller ||K_odd|| is assumed. It costs the supplied K query, controlled source reflections and the signal preparation/unpreparation. The minus sign is an acquired circuit phase. It is NOT automatically a physical ability to reverse the sign of a native Hamiltonian. Finite query errors and reflection synthesis errors are subdivided across actual calls.

These interfaces can feed the already acquired native-source SIMULATION theorem without a new lambda-dependent Trotter schedule: H and the free kernel are unchanged and the extra queries are actual bounded-cost circuit operations. This statement uses the existing full theorem, not a claim that the source's physical hardware was changed for free. Its large practical costs remain as audited. The cheaper logical operation is normally obtained by simulating its effective stack directly, using ordinary methods.

### Physical-engineering boundary

A passive bath does not supply coherent jump-output routing merely because L_j are known mathematically. Implementing the NEW dissipators may require new environment couplings, monitoring/feedback, or control resources. These are not granted here. Similarly positive-time averaging of K and RKR gives the EVEN part, not K_odd. Producing the odd part by that route requires a sign-reversed branch -RKR or an acquired counter-Hamiltonian; ordinary parity kicks alone do not establish it. Finite pulse widths and source/control bandwidth would require their own error analysis, which may reintroduce lambda dependence. No lambda-independent PHYSICAL implementation follows from the algebraic formulas. All work here is theoretical and involves no equipment or external action.

## 5. Explicit recycling qutrit and strongest ordinary comparator

Let source basis0,1,2, psi=0, H=P1+P2. For fixed0<p<=1 choose

    L0=sqrt(2p)|0><1|,
    L1=sqrt(2(1-p))|2><1|,
    L2=sqrt(2)|0><2|.

Then G dagger H=-2p P1-2P2<=-2p H, g=h=1, kappa=2p. There is genuine excited-state recycling for p<1. With system qubit,

    K=|1><0| tensor sigma_minus
      +(1/2)|2><0| tensor sigma_plus + adjoint,
    H0=Z/3,

one has b=s=C=1 and d=2/3. The effective jumps are sqrt(2)sigma_minus and (1/sqrt(2))sigma_plus, independent of p. At p=1/2, gamma0=28/3 and the cold no-control bound is (232/3)/lambda for time1. Thus lambda10^6 gives model error<0.000077334, with a remaining positive budget in a0.0001 logical task. These are conservative proven constants, not fitted finite-matrix errors.

The effective operation is STANDARD generalized amplitude damping: total population relaxation rate5/2, stationary ground probability4/5, damping eta=exp(-5T/2), composed with the commuting unitary exp(-iTZ/3). Four exact Kraus operators are sqrt(4/5) diag(1,sqrt(eta)), sqrt(4/5)*sqrt(1-eta)|0><1|, sqrt(1/5) diag(sqrt(eta),1), and sqrt(1/5)*sqrt(1-eta)|1><0|, each followed by that unitary.

A direct ordinary circuit uses two ancillas. Prepare a branch coin4/5, implement amplitude damping with one controlled Ry on a fresh zero ancilla followed by its CNOT to the system, and conjugate the damping by X in the heating branch. Include the final system Z rotation. A standard decomposition uses at most five CNOTs and four single-qubit rotations, with actual angle synthesis paid; no source history or rapid-rate simulation is needed. Classical angles depend on T and the stated coefficients, not lambda. Approximating all constant-many gates in operator norm so their sum is<=epsilon_gate/2 gives channel diamond error<=epsilon_gate. The branch/output ancillas are private and discarded. This circuit acts on unknown qubit inputs and preserves arbitrary external references.

The fixture therefore does NOT establish a new cooling capability or quantum speedup. The direct ordinary ancilla circuit is the winner for the admitted logical task. A small full36-dimensional Liouville exponential is another strong ordinary exact finite-rate competitor for the qutrit model. The useful tests are: recycling does not affect the leading logical stack when full return is earned; the cold support selection gives a finite O(1/lambda) certificate; and a changed-generator redesign must have its access/control cost paid.

At p→0 the H-drift certificate degenerates even though the path1→2→0 still returns. A different Lyapunov operator can certify that return. No claim that1/p is a necessary physical or computational cost is made.

For a comparison model replace L0,L1 by the SINGLE coherent-output jump sqrt(2)(sqrt(p)|0>+sqrt(1-p)|2>)<1|. This has the same H and H drift and the same leading effective stack, but generally L dagger F L is nonzero. Splitting it recovers the preceding model and removes that defect. Any observed error improvement compares two different physical generators, not two algorithms for the same unchanged bath.

## 6. Ordinary prior components and exclusions

General effective-operator/adiabatic-elimination and symmetry filtering are established. Reiter-Sorensen arXiv:1112.2806v2, SectionII equations3-5 and SectionIII.1, uses excited-to-ground decay in its displayed effective-operator setup; QLQ recycling cannot be silently treated as satisfying that premise. Broader elimination machinery remains a strong baseline. Le Regent-Rouchon arXiv:2303.17308v2 treats the Heisenberg formulation. Zanardi, Symmetrizing Evolutions, arXiv:quant-ph/9809064, explicitly uses group symmetrization to filter Hamiltonian components. These precedents preclude calling the present projection/algebra or ordinary ancilla operation a discovered new primitive. A limited search establishes no priority claim.

The cold certificate and circuit-access redesign are scoped mathematical constructions. They do not supply a free physical source modification, a full arbitrary-source-output process, a generic cheap projector, an optimized optimal-norm block encoding, or a practical win over the direct effective operation. The central resource question remains whether an actual application supplies the required cold source and engineered/accessed operators at a cost justified by the logical task.
