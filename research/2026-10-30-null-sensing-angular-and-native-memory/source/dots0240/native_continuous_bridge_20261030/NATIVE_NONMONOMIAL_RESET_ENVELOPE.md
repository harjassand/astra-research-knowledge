# Native partial-gate reset charge without monomial completion
2026-10-30. New proof candidate. This is a full-Hilbert **raw drift lemma**, not the missing native continuous-noise threshold.

## Useful result
The native transactional forest apparatus does not need a syndrome-monomial unitary on dirty workspaces. Every arbitrary partial-gate abort can be paid by removal of a sufficiently large bundle of actual history-defect tokens. A complete terminal reset has no good/dirty cross term whenever its clean input implements a deterministic syndrome correction. Thus the nonmonomial-abort obstruction can be removed without changing the physical generator, adding a clean oracle, or hiding DATA faults in controller resets.

The remaining obstacle is weighted, multiplicative acquisition/service credit. Uniform reset tails alone do not supply it.

## 1. Actual flags and full physical interface
Use exactly the reset-first transactional generator in `transactional_data_bridge_20261029/RESULT.md`, with the full forest frame from `FULL_HILBERT_FOREST_GAUGE.md`. Its actual commuting projectors are

    B_h = I - P_h,

where in the forest frame P_h is the projector onto a consistent ordinary clock/lock block and workspace W_h=0; P_h=0 on inconsistent and abort blocks. These are physical full-Hilbert observables, NOT virtual kick marks. The proved identities are [H_forest,B_h]=0, and individual-reset no-creation B_j J (I-B_j)=0. Every terminal/abort h-reset clears B_h. The forest Hamiltonian acts on controllers only and preserves DATA syndrome.

The forest-transformed payload resets have, for a fixed clock source and ownership mask m, the complete instrument

    E_U(rho)=|Q0,0><Q0,0| tensor Tr_W[U_m rho U_m^dagger].

U_m is a bounded-support unitary; for aborts it may be an arbitrary partial nonmonomial circuit. Every source abort block has B_h=1. Terminal sources are good iff ownership is complete and W_h=0. Other flags are unchanged by these resets, because locks and other clocks/workspaces do not change. Keep workspace Kraus labels separate before summing the complete instrument. Onsite identity-payload resets and lock cleanup remain as already proved in the forest theorem.

## 2. Unary bundles and raw full animals
Attach R identical *analytical vertices* to each actual flag B_h; all R are occupied iff B_h=1. These are not new physical qudits. Let S_h contain every DATA syndrome check which any Pauli on the bounded support of U_m can change, uniformly over masks and source phases; k=max_h |S_h|. Fix R>k. Make T_h union S_h a clique in the augmented animal graph, where T_h is h's R-token bundle. Include any additional fixed connectivity patches required by the original component geometry.

For every nonempty connected animal A define

    f_A = exp(a |A|) theta^{|A|-occupied(A)},
    V = sum_A f_A,    W = sum_A |A| f_A,
    a=c log(1/theta), 0<c<1.

No animal-size cutoff is used. All token/check projectors commute. The graph still has fixed degree and O(N) vertices, although constants grow with R and the native circuit footprint.

## 3. Spectral-envelope lemma for an entirely bad source
Fix all syndrome bits outside S_h and all flags other than B_h. These projectors commute with U_m. On a bad source define the *lower source envelope* x by setting all S_h bits to zero, retaining the fixed exterior, and setting every T_h token to one. Define the *upper target envelope* y by setting all S_h bits to one and T_h to zero. These binary strings need not be realizable code syndromes: the animal polynomial is defined on the full Boolean cube and its scalar monotonicity is all that is used.

As operator inequalities within this fixed exterior block,

    V_source >= V(x) I,
    E_U^*(V_target) <= V(y) I.

The second inequality is simply positivity/unitality of the complete source-normalized reset instrument and V_target<=V(y)I. There is no Pauli twirl and no assertion that E_U preserves the syndrome-diagonal algebra.

The fictitious x->y move removes R occupied tokens and adds at most k check vertices. Its changed set D_h=T_h union S_h is a clique, and its fractional decrease is

    beta_bad=(R-k)/(R+k)>0.

The original full-animal completion A->A union D_h therefore gives, after choosing c>(1-beta_bad)/(1+beta_bad) and theta sufficiently small,

    V(x)-V(y) >= c0 sum_{B connected: D_h subset B} f_B(x),
    c0=(1-theta)/2.

Since only k source check bits were erased, f_B(x)>=theta^k f_B(source). Hence on EVERY bad source state, including arbitrary DATA/workspace/reference entanglement,

    V - E_U^*V >= c0 theta^k sum_{B: D_h subset B} f_B.

This is a Loewner inequality, not a branchwise scalar inequality. It pays the worst arbitrary CP DATA effect of the partial circuit and the compulsory removal of the actual h flag.

Exactly the same proof holds for W: in the completion charge, |A|<=|A union D_h|. Thus

    W - E_U^*W >= c0 theta^k sum_{B: D_h subset B} |B| f_B.

A fixed bounded reset footprint may be enlarged to contain a common S_h; adding nonexistent possible flips only weakens constants.

## 4. Complete terminal resets have no good/dirty cross block
It remains to combine the preceding bad-source bound with clean terminal correctness; simply adding diagonal bounds would otherwise be invalid.

Fix a terminal ownership mask. If it is incomplete, the whole source is bad. If complete, let G be the W_h=0 source projector. Let O be either V_target or W_target, evaluated after h's flag has been cleared. For every definite global DATA syndrome s and fixed exterior flags, the intended clean channel sends that syndrome to ONE deterministic corrected syndrome f_h(s), including identity on inactive/tie sectors. Therefore the Stinespring isometry U_m restricted to |s> tensor |0> has range inside a single eigenspace of O tensor I_W. This holds for any unitary completion of the intended isometry; its dirty action need not be monomial.

Consequently U_m G is an invariant subspace of the Hermitian O tensor I_W, so

    G U_m^dagger (O tensor I_W) U_m (I-G)=0.

This is precisely the off-diagonal block of the *complete* reset adjoint. Source V and W themselves commute with G. Thus their terminal decrements are exactly block diagonal good/bad. On G the decrement is the intended deterministic SSF decrement; on I-G the spectral-envelope estimate applies. Masks also have no cross terms because the reset and its forest unitary preserve the lock labels and O is lock diagonal.

The argument does not require logical-basis monomiality: syndrome-sector degeneracy and an arbitrary retained reference are spectators. It does require deterministic syndrome output on each clean input syndrome, as satisfied by the fixed truth-table SSF map. A general clean channel whose definite-syndrome output is a coherent superposition of different syndromes would not satisfy this lemma.

## 5. Nonpayload resets
For data-free resets that can only remove flags, no classical approximation is needed. Individual no-creation implies that for every finite flag set F, the zero subspace of Q_F=product_{h in F}B_h is invariant. Hence the complete normalized channel obeys E^*(Q_F)<=Q_F. On each unchanged DATA syndrome block, every f_A is a polynomial in the B_h with nonnegative coefficients (including repeated unary tokens, reduced using B_h^2=B_h). Therefore E^*V<=V and E^*W<=W. The actual source projectors and rates are retained in the generator.

## 6. Exact raw native drift, and what is still missing
Define d_h=(I-Phi_h^*)V>=0, with flags held fixed. Let G_h^T be the actual good terminal source projector, and for every bad terminal/abort source b let Q_b be the positive envelope charge from section 3. Then on the entire forest-frame Hilbert space,

    L_native^* V <= -sum_h kappa_h G_h^T d_h -sum_b kappa_b Q_b <=0.

The analogous statement holds for W. No large-reset limit, independent clock schedule, classicalized malformed mask, or effective Lindblad replacement is used. Acquisition, computation and cleanup Hamiltonians have zero raw drift because they preserve syndrome and every B_h.

Augmented flag/syndrome animal coverage can use these Q_b in endpoint sectors, but arbitrary dirty flags and active DATA demands may be far from an endpoint. The generic continuous local-noise orbit estimate is still N^*V<=eta C W. The raw endpoint-only descent is NOT enough to absorb it. One still needs an actual phase-aware multiplicative CP service credit for the acquisition/lock network, or an independently proved native redesign. Uniform actual-reset tails and fixed-horizon CP averaging do not close this gap.

**Scope:** this is a new analytic lemma for audit. Native Poisson CPTP results remain distinct; generic continuous native robustness remains OPEN.
