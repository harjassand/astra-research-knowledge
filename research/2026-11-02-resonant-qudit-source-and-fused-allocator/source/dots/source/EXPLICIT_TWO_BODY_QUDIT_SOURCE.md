# Explicit finite-qudit autonomous source and invariant algebra

Reconciled proof, 2026-11-01 17:45 UTC. Parent supplied this microscopic apparatus architecture. This file fixes its Hilbert space, generator, cache interface, conditional response bound and resource limitations. No external access used.

## 1. Actual Hilbert space: dimension 8w+6

For a check S=P_w...P_1 of weight w, with P_j acting on distinct data qubits, use ONE apparatus qudit with orthonormal states:
* |idle,c>, c in {+1,-1}: 2 states;
* |g_j,b,c>, |e_j,b,c>, j=1,...,w, b in {0,1}, c in {+1,-1}: 8w states;
* |f,b,c>, b in {0,1}, c in {+1,-1}: 4 states.
Total dimension d=2+8w+4=8w+6. The binary probe exists as an internal multiplicity only in active states; c is the stored cache sign in EVERY state. This is a finite multilevel qudit, NOT a qubit rail or a Fock-space single-excitation sector. Every physical basis state is a legitimate idle, live-stage or final-readout state.

Define Z_cache by Z_cache|state,c>=c|state,c> across the entire qudit. Define A=I-Pi_idle as the active projector. For fixed phase and c, |phase,s_X,c> denotes (|phase,0,c>+s|phase,1,c>)/sqrt(2).

## 2. Time-independent local generator

For each factor j set
 H_j=g sum_(b,c) [|e_j,b,c><g_j,b,c| tensor P_j^b + h.c.].
This is an apparatus-qudit/data-qubit TWO-body Hamiltonian. Its b=0 component is an onsite apparatus transition; its b=1 component is coupled to one data Pauli. There is no full-S controlled jump.

Preparation, with p_+=1-p and p_-=p, is onsite:
 L_(prep,sigma,c)=sqrt(r p_sigma)|g_1,sigma_X,c><idle,c|.
It keeps the cache and prepares the probe with finite polarization 1-2p. Summing Kraus hazards gives
 sum_(sigma,c) L†L=r Pi_idle.
The input cache may be dephased by the resolved c channels; this is allowed and does not change cache-diagonal observables.

Let next_j be g_(j+1) if j<w and f if j=w. Coherence-preserving forward decay is onsite:
 L_(j,c)=sqrt(gamma) sum_b |next_j,b,c><e_j,b,c|.
Its hazard is gamma Pi_(e_j,c). The SAME channel must carry both b amplitudes coherently. Separate which-b-resolved decay channels are a different, noisy device.

Final readout and cache overwrite is also onsite:
 L_(read,s,c)=sqrt(gamma)|idle,s><f,s_X,c|,
with s in {+1,-1}. Then
 sum_(s,c) L†L=gamma Pi_f.
Consequently final response has exactly exponential waiting time of mean 1/gamma, for EVERY final probe/cache state. There is no free detector-latency assumption. The physical output is the local cache c, available to the consumer through controlled cache reads; an external photodetector or reliable external timing controller is not required by this definition.

All Hamiltonians, pumps and decay rates are time independent. Different stage channels are separate channels. A common coherent channel merging distinct stages would require a new analysis of stage-block closure.

## 3. Exact dressed-check and logical invariants, term by term

Let P_(j-1)=P_(j-1)...P_1, P_0=I. Assign prefixes:
 ground g_j: P_(j-1);
 excited e_j: P_j...P_1;
 final f: S;
 idle: I (using S instead would give the same dressing below).

For a data Pauli O commuting with EVERY full measured check, define a diagonal apparatus operator D_p(O):
 on |g_j,b,c>: (-1)^[b omega(P_(j-1),O)];
 on |e_j,b,c>: (-1)^[b omega(P_j...P_1,O)];
 on idle and final: 1.
Here omega(R,O)=0 or 1 records Pauli commutation. The final value is 1 because [S_p,O]=0. Define globally
 O_tilde=O product_p D_p(O).

For the transition |e_j,b,c><g_j,b,c| tensor P_j^b, moving O through P_j^b contributes (-1)^[b omega(P_j,O)]. The change from the ground dressing to the excited dressing is exactly the same sign. Thus [H_j,O_tilde]=0.

Each decay connects equal prefixes, so [L_(j,c),O_tilde]=0. Preparation connects idle to prefix I, and readout connects full prefix S to idle; both endpoint dressings are identity. Hence the preparation and readout jumps also commute with O_tilde. Their adjoints commute as well.

Therefore EVERY Hamiltonian and EVERY onsite jump preserves O_tilde termwise, and L_source^* O_tilde=0. This applies to all stabilizers and protected logical Paulis. It remains true when checks overlap and their partial factors anticommute: the other apparatus dressing factors are diagonal operators on different qudits and do not enter the local sign calculation. No global phase schedule or collision flag is required for this invariant.

The dressing preserves the Pauli commutation algebra: apparatus factors commute with one another and with data O. In particular dressed stabilizers mutually commute. For target s,
 e_s=(I-Z_cache,s S_tilde,s)/2
is a positive projector. Overlap can spoil individual reports but does not spoil the exact dressed source invariants.

## 4. Cache and activity observable algebras

Let Pi_c project onto cache c across all apparatus phases. Hamiltonians commute with Pi_c. Each jump maps one specified input cache block to one specified output block (decays/preparation preserve c; readout writes s). Hence for EVERY cache-block-diagonal observable F, L_source^*F is again cache-block diagonal.

Since e_s is cache-block diagonal, so are e^(tL_source^*)e_s and any time-integrated finite-patch source corrector built from it. A Boolean cache input read has the form U_read=sum_c Pi_c tensor V_c on a separate consumer register. It commutes with every such source corrector. Cache-basis dephasing similarly leaves it unchanged. This statement does not authorize a consumer to overwrite caches or to perform noncommuting cache rotations; those would be different operations.

Likewise, Hamiltonians conserve active/idle labels, and jumps map definite active source blocks to definite destination blocks. The active-block-diagonal observable algebra is invariant. Initial coherences between active and idle blocks cannot affect the counting/e_s estimates; no physical perfect dephasing operation needs to be inserted.

More finely, regard idle, each live pair {g_j,e_j}, and final f as stage blocks. H is block diagonal in these blocks. Separate decay channels move one block to the next. The stage-block-diagonal observable algebra is invariant, so arbitrary initial interstage coherences do not affect completion populations. Within each live g/e block, all quantum coherence and environment entanglement remain present and are covered by the observability theorem.

## 5. Uniform active-cycle response, now including actual readout

For a live stage, the no-completion gauge calculation in TWO_BODY_STAGE_COMPLETION_OBSERVABILITY.md gives
 T_stage=1/(g+B+gamma),
 p_stage=gamma g²/[100(g+B+gamma)³],
 P(tau_stage>n T_stage | any past)<= (1-p_stage)^n.
B bounds the incident commutator ||U†H_env U-H_env||. Other apparatus onsite baths commute with the target U and do not enter B. Neighboring two-body Hamiltonians give B<=2 sum_(incident q)||H_q||, independent of total memory size. Noncommuting data-noise baths remain separately priced perturbations.

Let theta>0 satisfy theta<gamma and (1-p_stage)exp(theta T_stage)<1, and set
 M_stage=p_stage exp(theta T_stage)/[1-(1-p_stage)exp(theta T_stage)],
 C=M_stage^w * gamma/(gamma-theta).
For every initially active apparatus state, including arbitrary partial stages and coherent mixtures, the time to completed readout obeys
 E[exp(theta tau_active)|past]<=C,
 S(t):=min{1,C exp(-theta t)} bounds its survival,
 tau:=integral_0^infinity S(t)dt <=(log C+1)/theta.
A partial initial stage requires no more than w live-stage completions plus the final onsite readout. Conditional tower bounds, not independent completion times, give this estimate. The exact final readout hazard gamma supplies the last factor.

These S and tau meet the explicit premises of UNIFORM_FINITE_TIME_CACHE_REFRESH.md. A cycle started by the idle pump begins in the proper prepared g_1 state. A collision-free good-preparation cycle has the exact parity instrument: each completed stage contributes its controlled single-factor unitary, and final X readout/cache write gives data Kraus (I+sS)/2. The bad preparation branch instead flips the reported sign. Initial arbitrary partial probes are first flushed by the last-window argument; they are not assumed correctly initialized.

This correct-instrument statement concerns the SOURCE generator. Additional consumer data updates or physical data noise during extraction must be included through the joined model's separate admission, not silently treated as collision-free source dynamics.

## 6. Reservoir, hardware and comparator charges

This is an explicit time-independent finite-dimensional GKSL architecture with two-body source Hamiltonians and onsite reservoirs. It is not a derivation of those reservoirs from a particular dipole selection rule, thermal bath, or laboratory pump.

Required physical resources include:
* all 8w+6 apparatus levels and their state connectivity;
* an energy/entropy supply sustaining directed preparation and decay, and cache/readout entropy disposal;
* the phase reference or stationary reservoir structure that prepares the X-polarized probe and measures its X basis;
* indistinguishable b=0/1 decay paths with matched amplitudes/phases in each collective L_(j,c). Which-b information in emitted radiation dephases the probe and is physical error, not harmless clock noise;
* fixed coupling strengths g,r,gamma, geometry and bounded incident degree;
* all local perturbations, including transitions between arbitrary qudit levels, finite reset purity, cache faults, reservoir imperfections and readout deviations.

No reliable external runtime controller is used, but none of these stationary resources is free. The apparatus is not a passive detailed-balance memory. Same-resource active parity extraction receives the identical qudit, couplings, pump/reset purity, baths, cache, wiring and any phase-reference resources.

Finally, 'two-body source Hamiltonians plus onsite source baths' does not mean the complete memory controller is two-body. Any three-body classical Boolean consumer or other controller primitive remains separately specified and charged. The root owns the full source/controller/barrier join; this file establishes the source architecture and its algebra/response interface.
