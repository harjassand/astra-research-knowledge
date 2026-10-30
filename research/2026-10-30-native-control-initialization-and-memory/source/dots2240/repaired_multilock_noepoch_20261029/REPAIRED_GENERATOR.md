# No-epoch two-site recovery architecture with explicit corrupt-clock repair
Date: 2026-10-29. Preserves earlier pair-lease and isolated-hub results as separate constructions.

## Physical sites and fixed parameters
Use a bounded-degree bipartite interaction graph of private recovery hubs h and data-resource sites r. Hub h has a fixed support R_h=(r_1,...,r_k), private finite workspace W_h initially |0>, and a finite clock alphabet. A resource has its payload data and one lock register. A resource belongs to only boundedly many hubs. All k, workspace dimensions, circuit lengths and graph degrees are fixed independent of total system size/runtime. A 'two-body' term acts on one hub qudit and one adjacent resource qudit; internal hub registers are not claimed to be elementary qubits.

Fix a unitary recovery circuit U_{h,1},...,U_{h,L} on W_h and R_h. Each gate acts on the private workspace and at most one resource r(h,t). Hub-only gates can use an arbitrary member of R_h as an ownership-checked partner. The intended recovery channel is obtained by initializing W_h=0, applying the circuit, then resetting W_h. Its actual data Kraus operators are <s|U_L...U_1|0>. The explicit [[5,1,3]] circuit in the previous module is one finite example, not an assumed arbitrary jump oracle.

## Alphabet
Hub phases:
- A_i, 0≤i≤k: acquiring a prefix of resources; A_k is also computation position G_0.
- G_t, 1≤t≤L: computation prefixes.
- Q_i, 0≤i≤k: quarantine/cleanup verification prefixes.
- R_(p,j): a distinct abort-repair label for each ordinary phase p and each resource j with a nontrivial consistency test below.

Lock labels at resource r:
- f: free;
- o_h: owned by incident hub h;
- z_h: cleanup-excited label associated with owner h.

There are no epochs. All labels refer only to boundedly many incident hubs/resources.

## Consistency tests C_(h,p,j)
A_i is consistent iff r_j has exactly o_h for j≤i, and has neither o_h nor z_h for j>i. G_t is consistent iff every resource has exactly o_h. Q_i is consistent iff r_j has neither o_h nor z_h for j≤i; later resources are unrestricted. Every R label is bad by definition.

Each failed test is a projector involving only the hub phase and one resource's lock. In particular, 'missing expected ownership' includes free, another owner's label, and one's own cleanup label z_h. 'Unexpected own ownership' includes both o_h and z_h.

## Hamiltonian transitions, each with its adjoint
All amplitudes are fixed positive finite constants.
1. Acquisition: |A_i,f> ↔ |A_(i+1),o_h> on hub h and r_(i+1).
2. Computation: U_{h,t+1}⊗|G_(t+1)><G_t|⊗|o_h><o_h| on its actual target resource, with G_0=A_k. **Every gate includes this actual ownership projector**, not just the first gate or acquisition.
3. Verification: |Q_i><Q_(i−1)|⊗(I−|o_h><o_h|−|z_h><z_h|) on r_i.
4. Cleanup: |z_h><o_h|⊗P_(hub does not claim resource). The hub claims r_j in G_t, or in A_i with j≤i. It claims nothing in Q or R phases. This permits cleanup during quarantine, abort, or an inconsistent unexpected-lock configuration.
5. Abort drive: |R_(p,j)><p|⊗C_(p,j), where C is the failed local consistency test for the original phase p. Every destination R_(p,j) is distinct. The reverse uses the SAME original failed-test projector, so cannot restore a consistent original phase from R.

No term contains a projector over multiple resources. The hub stage, rather than a high-body all-lock condition, certifies acquisition in clean trajectories.

## One-site resets, label-resolved channels
- Terminal: for each workspace basis s, sqrt(κ_T)|Q_0,0><G_L,s|.
- Abort: for every R label and workspace s, sqrt(κ_R)|Q_0,0><R,s|.
- Ready: for every workspace s, sqrt(κ_A)|A_0,0><Q_k,s|.
- Lock cleanup: sqrt(κ_Z)|f><z_h| on each resource.
- Workspace refresh: in every A_i and Q_i, sqrt(κ_W)|p,0><p,s| for each s, including s=0 in the complete-overwrite version.

Within a terminal reset, all syndrome channels have the SAME κ_T and remain separate dissipative channels. Summed loss is κ_T|G_L><G_L|⊗I_workspace. A coherently summed reset operator is not interchangeable with these channels. The same complete-instrument convention is used for abort/ready resets. A/Q amplitude damping omitting s=0 is also possible, but the complete overwrite supplies particularly simple clock-diagonal losses and is the version fixed here.

A/Q refresh fixes a clean workspace exactly; the s=0 self-loop emission has no state effect there. Its pumping/entropy cost is part of the maintained reset resource, not free equilibrium dissipation.

## Finite-rate monitoring, separately declared
For the healing-progress theorem use the scheduler's label-resolved on-site monitor+reset construction. It resolves hub CLOCK POSITIONS and resource LOCK LABELS, never workspace/syndrome/Kraus labels. Its Hamiltonian coupling and reset instruments are one-site in this qudit convention. Since history projectors are clock-block-diagonal, these monitors preserve all clean history subspaces. Finite positive strengths are used; no infinitely fast measurement or classical-clock limit is assumed. See `producer-workspace/LOCAL_HEALING_CERTIFICATE.md` and the monitor construction cited there.

## Former traps explicitly removed
- Faulted A_0 with one's own first lock o_h: a failed unexpected-owner test enables abort; cleanup is also enabled because A_0 claims nothing.
- Faulted Q_k with an unchecked own lock: ready reset to A_0 does not pretend to heal it; it remains an unexpected-own-lock defect and has the same abort/cleanup exits.
- Stale epoch alias: no epochs exist. Every completed recovery enters Q_0, cleans its own tags, verifies absence, and only then returns A_0.
- Corrupt computation counter: its gate cannot touch a resource unless that resource actually carries o_h, so it cannot attack a consistent executing neighbor's reserved data.

## Thermodynamic and noise interface
This is a driven open-system effective model with maintained one-site reset/pump instruments and fixed coherent phase references where gates require them. A time-independent rotating-frame generator is NOT an equilibrium passive self-correcting device or a closed finite battery. Reset power and entropy export per cell are finite at fixed activity; total required capacity scales extensively with cell count. A microscopic autonomous hot/cold-reservoir realization has not been derived here.

Finite-temperature upward transitions and imperfect reset/control channels are additional local perturbations, not silently suppressed to zero. For upward jumps with rates u_a and normalized operators, their local generator diamond-norm budget is ≤2Σ_a u_a. The alphabet and number of channels per cell are fixed, so this is a local, size-independent budget. The resulting noisy data threshold is NOT supplied by the clean repair algebra.
