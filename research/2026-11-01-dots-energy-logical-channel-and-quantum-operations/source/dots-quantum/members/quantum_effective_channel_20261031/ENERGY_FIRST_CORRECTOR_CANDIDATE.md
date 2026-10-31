# Energy-controlled logical reduction using only a first off-diagonal corrector

Status: fresh root derivation, unreviewed. This is the sustained interaction-energy attack. It may avoid the global source mixing resolvent in DARK_SOURCE_LOGICAL_REDUCTION_CANDIDATE.md. No novelty or practical advantage claimed. Same native G, H, g, kappa, psi, centered K, system-only H0 and controls. All norms below are completely bounded where maps are involved. Let b>=||K||, d>=||[H0,K]|| and C>=||sqrt(H) K||. Source energy E0=Tr(H rho0) is a promise on the actual initial input; for all inputs use E0<=h.

Let P_s=|psi><psi| and Q=I-P_s. Define the Hermitian off-diagonal operator

    S=H_Q^(-1) Q K P_s+P_s K Q H_Q^(-1),
    s=||S||=||H_Q^(-1) Q K P_s||<=b/g,
    F(O)=i[S,I_source tensor O], T=P+lambda^(-1/2)F.

P now denotes embedding system observables, not the source projector. F is only an analysis map. Its norm is <=2s.

## Exact algebra: leave the excited-sector defect, then pay its actual occupation

For G=sum D[L_j], L_j psi=0, H=.5sum L_j^dagger L_j,

    G^dagger F+V P=B,
    B(O)=Q i[K,I tensor O] Q+sum_j L_j^dagger F(O) L_j.

B has source support QQ, not merely zero stationary average. Off-diagonal terms cancel because H S_QP=K_QP. Recycling is also QQ because L_j P_s=0, even if Q L_j Q is nonzero. This is the step that prevents supplying a perfect direct-reset bath.

The relative complete bound is

    ||H_Q^(-1/2) B(O) H_Q^(-1/2)||<=beta ||O||,
    beta=2b/g+4s.

The commutator part costs2b/g. For recycling, the CP map with Kraus L_j H_Q^(-1/2) has norm2, since sum H_Q^(-1/2)L_j^dagger L_j H_Q^(-1/2)=2Q; F costs2s. Consequently |Tr(rho B(O))|<=beta E for every reference-extended state and Hermitian observable ||O||<=1.

Let D(O)=<psi|V F(O)|psi>. As in the general dark-coherence derivation, its Schrödinger version is the genuine dissipator with stacked jump

    E_stack=sqrt(2)(H_Q^(-1/2) tensor I) K (|psi> tensor I).

In particular ||D||cb<=4bs. (A direct stack norm bound is also available.) The system generator is L_eff=L0+D. The exact residual is

    L_lambda T-T L_eff
       =sqrt(lambda) B+(V F-P D)
          +lambda^(-1/2)([L0,F]-F D).

The P_s block of A=V F-P D is ZERO and ||A||cb<=8bs. Gentle projection then gives

    |Tr(rho A(O))|<=16bs sqrt(E/g),

because ||rho-P_s rho P_s||_1<=2sqrt(Tr Q rho). This remains true with arbitrary reference. The final residual term is bounded by

    gamma0=2d/g+8b s^2,

using ||[H0,S]||<=d/g and ||F D||<=8b s^2. No full source resolvent, whole-environment bandwidth or h appears in these constants.

## Energy integration and all-in model error

The user's all-rate energy inequality gives

    E(t)<=E0 exp(-lambda kappa t/2)+4C^2/(lambda kappa^2).

All prescribed system-only CPTP instruments, with records retained, leave the unconditional source energy unchanged. Thus across the controlled sequence

    integral E(t)dt<=2E0/(lambda kappa)+4C^2 T_total/(lambda kappa^2),
    integral sqrt(E(t))dt<=4sqrt(E0)/(lambda kappa)+2C T_total/(sqrt(lambda) kappa).

For a system-only control C_j define the acquired complete norm

    nu_j>=||C_j^dagger F-F C_j^dagger||cb.

The safe bound nu_j<=4s needs no optimal norm oracle. For a system unitary U, nu_j<=2||U^dagger S U-S||<=2||U^dagger K U-K||/g. For an acquired decomposition K=sum_i B_i tensor A_i, set S_i=H_Q^(-1)Q B_i P_s+P_s B_i Q H_Q^(-1); then nu_j<=sum_i ||S_i|| ||C_j^dagger i[A_i,.]-i[A_i,.] C_j^dagger||cb. These are sufficient constructed bounds, not assumed optimal calibration. Controls commuting with the actual interaction have zero defect.

Common-intertwiner telescoping gives only two endpoint defects, costing4s/sqrt(lambda). Contractive Duhamel on actual evolved states, with effective backward observables, then yields

    error <= min(2,
      [4s+2 beta E0/kappa+4 beta C^2 T_total/kappa^2
         +32bs C T_total/(kappa sqrt(g))+T_total gamma0+sum nu_j]/sqrt(lambda)
      +64bs sqrt(E0)/(lambda kappa sqrt(g))).

This is a model error bound for complete retained system/reference/control records. It covers arbitrary initial quantum source correlations satisfying the energy promise, not just a prepared dark source. The energy bound is an input promise, not something inferred from an unknown state. Conditional rare measurement outcomes are not promised separately. Source interventions are excluded. Effective stack acquisition, source-reference preparation for that acquisition, ordinary effective Lindblad execution, controls and gate precision remain separate paid costs.

## Optional r_E high-rate substitution

If instead the acquired energy commutator bound is

    |Tr(i[K,H] rho)|<=a_E E+2r_E sqrt(E),

then sqrt(lambda)>=2a_E/kappa implies

    dE/dt<=-(lambda kappa/4)E+4r_E^2/kappa.

Hence integral E<=4E0/(lambda kappa)+16r_E^2 T_total/(lambda kappa^2),
while integral sqrt(E)<=8sqrt(E0)/(lambda kappa)+4r_E T_total/(sqrt(lambda) kappa).
Substitute these quantities into

    error<=4s/sqrt(lambda)+sqrt(lambda) beta integral E
            +16bs/sqrt(g) integral sqrt(E)
            +(T_total gamma0+sum nu_j)/sqrt(lambda).

This form displays the energy-injection resource directly without hiding constants. No transfer to another generator is made. Whether s, beta, r_E and control commutators are cheaper than generic b/g bounds in an actual nonclassical construction remains a task to earn.

## Required checks before acceptance

Independently check the exact G^dagger F QQ recycling identity, the CP orientation of D, relative norm bound, all reference extensions and controlled Duhamel bookkeeping. Test a source with Q L_j Q recycling, not only direct amplitude damping. Compare strong ordinary adiabatic elimination and reservoir construction. This is not yet an independently received theorem.
