# Independent audit of the conditional local-healing certificate

## Verdict

The bounded two-step projected-path argument, finite monitor constants, and operator contraction check under the FULL-HILBERT-SPACE hypotheses stated in LOCAL_HEALING_CERTIFICATE.md. This is a conditional theorem: the implementation matrices still need to establish those hypotheses globally.

## Operator assumptions in precise form

For each bad projector B and each jump J, require

 (I-B) is invariant under J, equivalently B J(I-B)=0,
 [J^*J,B]=0.

Together with [H,B]=0 these imply D_J^*(B)<=0: J^* B J has no good-sector rows/columns, and on the bad sector it is bounded by J^*J. The phrase 'never creates bad' must mean this operator condition, not an inspection only of selected basis arrows.

The bundled abort reset with loss kappa P_R tensor I_workspace and destination Q_0 is a valid uniform healing event because Q_0 is good for every resource configuration. Resolving workspace outcomes as separate jumps prevents accidental coherent rank-one loss. Unique test destinations and no selected off-diagonal loss block give the required short-time coherent-step probability.

## Finite path and padding

After the Gamma clock record, each bad nonabort branch has its two-step test/reset path. Abort inputs use a reset plus an idle check. Inputs that have already healed use only harmless checks; the good sector is absorbing by the operator hypotheses. An idle check may require no ordinary local jump and the same measured clock labels after delta; its probability has the same bounded-local-generator estimate and is safely >=1/4 for the displayed small delta. Thus using p_0 for two steps is conservative.

The complete recorded-instrument comparison costs <=3(4B epsilon), which is <=p_0^2/2 under epsilon<=p_0^2/(24B). The dephasing and exact-reset-monitor probability factors and window counts are consistent. The reset-monitor flush can start from arbitrary monitor/clock entanglement and may itself heal the hub; that only helps because goodness is absorbing.

## Operator contraction

Positivity gives 0<=T_t^*B<=B, hence the evolved observable is supported in the bad subspace. The uniform success bound on all bad-supported density matrices therefore proves T_T^*B<=(1-c)B exactly. Iteration and the stated initial Tr(rho B) prefactor are valid, including initial good/bad coherences.

## IMPORTANT: occupation is not automatically a trajectory first-entry time

The line identifying this operator bound with a first-healing-time tail needs a narrower definition or an additional branch condition. In general, a jump can take a bad input to a coherent superposition of good and bad while satisfying every monotonicity condition above.

Example: B=|1><1|, H=0, J=sqrt(kappa)|+><1|. Then J^*J=kappa B is clock-diagonal, J annihilates the good state, and L^*B=-(kappa/2)B. Starting in |1>, bad occupation decreases at first order in time. But after the first jump the trajectory is |+>, not wholly good; with finite clock monitoring a second event is needed to project it fully good. The probability of exact first entry into the good subspace is only second order at short times. Without monitoring it never occurs at finite time on that jump branch.

Even resets with definite local clock destinations can leave other resource registers in a superposition whose branches have different values of a multi-resource B. Thus local destination labels alone do not settle this interpretation.

Safe formulations:

- Call Tr(rho_t B) the probability that a bad-projector test at time t fails, or simply bad occupation.
- Separately define an operational healing witness (e.g. the certified abort-to-Q_0 event, or an appropriate resolved monitor record). The explicit path construction gives a uniform geometric bound for failure of such witnesses in successive blocks, but do not attach the initial Tr(rho B) prefactor without proving that relation.

This caveat does NOT invalidate the local operator contraction or its use as a Lyapunov/healing observable.
