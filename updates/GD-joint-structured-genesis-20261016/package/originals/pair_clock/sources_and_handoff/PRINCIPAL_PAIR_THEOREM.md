# Asynchronous memory with two checked edges per correction

Principal theorem reconstruction, 16 October 2026. Status: internally derived conditional theorem with complete arguments for the new local constructions and a direct application of the preserved LSS, HT, stopped torus and homology lemmas. External mathematical correctness and historical priority remain unestablished. Finite tests and investigator verdicts are not proof premises.

The surviving extension replaces the eight checked edges and one or two written faces of the original vertex sweep by two checked outgoing edges and one written face. This known Toom type operation admits a new continual-noise proof through a finite service envelope. A separate completion admits arbitrary rare local CPTP faults and structured continuous Hamiltonian noise without a full patch depolarizing floor.

## Explicit generator and two separate statements

Use the periodic 4D cubical toric code with one qubit per plaquette, 6L^4 physical qubits and six logical qubits. In the primal sector define X edge stabilizers S_e and, for every vertex v and direction pair i<j, set

    Pi_(v;ij) = (I-S_(v,i))(I-S_(v,j))/4,
    J_(v;ij) = sqrt(kappa) Z_(v;ij) Pi_(v;ij).

Here Z_(v;ij) is the Pauli on the positive plaquette based at v. The two stabilizers each contain that plaquette, so the Pauli toggles both tested bits. Use dual Z checks and an X face action in the other sector. Each jump has exactly 11 qubit support and writes one face. The active generator G_pair is the sum of all 12L^4 correction dissipators and the declared independent single face Pauli noise terms.

**Statement A, original active pair jumps with Pauli noise.** There exist fixed b in N and epsilon,A,c>0, independent of L,T, such that for sufficiently large M and L=bM, whenever

    max(lambda_X+lambda_Y,lambda_Z+lambda_Y) <= epsilon kappa,

one fixed perfect decoder satisfies

    ||Dec_L exp(T G_pair) Enc_L-Id||_diamond
       <= min(2,A L^4(1+kappa T)exp(-cL)), all T>=0.         (1)

All six logical qubits and arbitrary untouched references are included. Code initialization and final decoding are ideal. The constants are qualitative and need not match those of the original vertex sweep.

**Statement B, completed pair channels with general proposal faults.** Complete each pair action into the channel C_(v;ij) in UNIVERSAL_PAIR_CLOCK_ENVELOPE.md, adding kappa D[I-Pi_(v;ij)] to each active dissipator. Fix a bounded patch catalog independently of L. For sufficiently small total local CPTP fault proposal rate nu per fine owner cell relative to kappa, the generator

    G_C = kappa sum_(v,ij,sector)(C_(v;ij)-Id)
             + sum_(x,a) nu_(x,a)(N_(x,a)-Id)

obeys the same form of (1) for a compatible family L=b_q M. Each N_(x,a) is any CPTP map on its declared patch. The constants are uniform over channels and spatial variation below a fixed rate ceiling. There are 12L^4 correction channel streams and 24L^4 correction dissipators, all of 11 qubit support. This is a different generator from Statement A on syndrome coherences.

## Proof of the new local interfaces

For A, the definite-syndrome Pauli family is invariant under every Q Pi dissipator. At a Pauli branch, its projector is scalar zero or one, independently of logical amplitudes and reference entanglement. A vertex's six eligible face transitions can be realized by one independent rate kappa base stream selecting its first eligible pair and six independent rate kappa extra streams accepting all other eligible pairs. Every eligible face receives exactly rate kappa. The ternary envelope in workers/local_operation_inventor/PAIR_RULE_DERIVATION.md dominates every such history. With all envelope predecessors zero, even outgoing degree is at most four, and two base rings suffice to remove it. Its certificate site service has Gamma(2,kappa) law and moment 4 at kappa/2; directed path counting gives 16^H. The old state update rule, explicit monotonicity and full fixed guard forcing proof are in that derivation and BLOCK_TRANSFER.md.

For B, use the six **physical** pair channel clocks in each CSS sector; the virtual selection for A is not a coherent branch coupling. The 127 state ticket envelope in UNIVERSAL_PAIR_CLOCK_ENVELOPE.md has a SEPARATE copy for each sector, serviced only by matching sector clocks. Opposite sector correction operations commute with its syndrome checks and cannot spend its coupons; arbitrary fault proposals reset both sector copies on their boundary boxes. This explicit routing is essential: sharing tickets between sectors has an exact finite counterexample. Each copy is monotone and depends only on physical pair labels, times and fault locations. Between its full resets, actual incident edges cannot be added by any upstream action without causing another full reset. A full coupon phase visits all six matching sector pair labels and removes at least two outgoing edges if any remain. Two phases clear a center with no actual incoming edges at progress marks. This proves support domination for every Pauli history on one common schedule. After all four predecessor certificates clear permanently, two full coupon collections dominate clearance; their exponential moment is at most 4096 at kappa/2, giving the path factor 16384^H.

Both envelopes preserve the four healthy coordinate halfspaces and the healthy lower height halfspace. Every update reads old inputs at fine infinity distance at most one. A target has 11 possible influencing anchors, at most seven types for A and six for B, with at most five old inputs per type. Thus 512 bounds the structural choices per backward event. With Delta=Cb/kappa and m=floor(Rb/2), the three primitive flags are current slab birth, truncated lower height certificate failure and an ordered m mark dependency chain ending at any target time. Their marginals are bounded explicitly in the two derivations. Fix C and R, hence coarse dependence and the attractive forcing map, before the LSS/HT tolerances, b and finally noise rate. This gives arbitrarily rare fixed-range bad flags with independent slabs, uniformly over all initial configurations and exterior histories. No implemented service register, coarse grid or global clock is introduced.

## Explicit application of the inherited global lemmas

The microscopic changes enter the global proof only through that forcing inequality, fresh fixed guards, and the old input causal bound. Let zeta=1 when a fine cell is fully healthy and define theta_0=1, theta_(z,n+1)=(1-B_(z,n))phi(theta_n shifted z) for the same five halfspace eroder phi. Monotonicity gives zeta>=theta. On infinite space the independent slab couplings from LSS dominate native bad flags by rare iid deaths. HT Corollary 9.5 bounds the anchored spacetime zero component of the upper invariant iid death process. The common future death coupling bounds the entire cold history by that stationary history.

The finite torus lemma is a statement about this native B driven theta and phi, so it does not depend on whether the microscopic alphabet was binary, ternary or tickets. Stop at the first inserted zero making a k-connected component of diameter ell=M/128, k=4R+4. Every older component had diameter less than ell; the newly merged component lies within ell+k of its inserted anchor. For every nonforced zero, its needed older zero parent in each forcing set belongs to the same component. For each deterministic prospective anchor, copy all primitives in its fixed enlarged injective torus patch into infinite space and extend independently outside. The closed witness replays there. No adaptive conditional copying or torus stationarity is used. The inherited anchored tail and a union over NM^4 deterministic anchors give C_1 NM^4 exp(-c_1 M).

At any physical time in a slab, a positive envelope site on a good target flag traces through old positive inputs to an initially positive site, unless it encounters the excluded m mark chain or an excluded local birth. The initial site lies within coarse radius R. A bad target flag is a forced theta zero at the next layer. Hence all occupied fine cells throughout slab n lie in N_R({theta_n=0}) union {theta_(n+1)=0}. The only needed microscopic property is that every positive output without a fault has an old positive input at distance at most one; both new envelopes have it. Adjacent fine vertices map to coarse spacetime zeros at distance less than k. A physical syndrome component of diameter L/32 forces coarse diameter at least M/32-2R-1, exceeding ell for large M. This verifies the whole slab interface for the new envelopes, including transient and pre-jump defects.

Use the inherited component filling decoder with r=L/32 and rho=L/8. Every changed old syndrome component meets the bounded physical event patch. All affected old and new components, their fillings and the event chain F therefore lie in one embedded box of side 2r+O(q)<rho. Unaffected fillings cancel. The closed chain F+D(s)+D(s+boundary F) is a boundary in that contractible box. Thus the decoded homology of the **entire accumulated chain** cannot change while syndrome components remain small. Pair corrections write only one face, so A meets this premise directly; bounded patch faults in B meet it for fixed q and sufficiently large L. Vanished syndromes and component splits, merges and cancellations are included.

For A, average the input-independent Pauli branch law. Good branches are stabilizers after recovery, and twice the bad probability bounds the unhalved diamond distance. For B, condition on physical clock/location schedules without Kraus outcomes. On a common good schedule expand each fault Kraus operator in local Paulis. Each surviving Pauli summand follows a legal pair rule trajectory, has trivial recovered homology and is scalar on the entire code. The recovered Kraus sum is scalar as well; conditional trace preservation gives the identity logical channel. Average schedules to obtain twice the bad probability. Union the CSS sector escapes, take N=ceil(T/Delta)+1 and absorb fixed b,C into A,c. This proves the two conditional statements from their stated premises.

## Structured coherent extension of B

For a supplied bounded patch Pauli catalog, combine gamma_a D[P_a]-i h_a[P_a,.] into the exact unitary proposal of PAULI_NOISE_COHERENT_COMPILER.md at rate gamma_a+h_a squared/gamma_a. If the summed rates per owner cell fit B's ceiling, (1) follows without a full patch depolarizing floor. Rank deficient matched baths are allowed; drift outside their dissipative span is not admitted by this proof. The exact general Choi criterion in EXACT_POISSON_RATE_CRITERION.md supplies a larger stated class of local generators. Arbitrary pure Hamiltonian drift and arbitrary imperfect correction jumps remain open. The original active pair generator A does not inherit B's coherent tolerance.

## Historical and external review obligations

The two edge predicate and single face operation are inherited. Pastawski et al., arXiv:1010.2901v2, has an X/Z inconsistency when its printed Eqs. 29,33,38 are combined literally: the edge check and face action then commute. This statement defines the anticommuting check/action convention explicitly and credits the intended geometric rule, also stated consistently in Drechsler et al., arXiv:2610.05589v1 Definition 6.2. The latter proves synchronous/Floquet memory and identifies its time independent transfer as open; it does not validate this proposed proof.

An external specialist must review the new service envelopes, especially the between-reset coupon invariant, the independent certificate construction and uniform fixed guard forcing; then check the exact interfaces to LSS, HT, stopped replay, whole slab cover and accumulated homology. The original LSS full text remains inaccessible in the saved source retrievals and is an explicit standard theorem import. Historical priority of this asynchronous result requires broader primary-source scrutiny. The old rule, quantum channel completion, error-span argument, Choi criterion and Lindblad gauge identities are not claimed as new inventions.

The result remains an ideal 4D memory theorem. The support reduction does not give a useful numerical threshold, a 3D device, noisy preparation/readout, leakage protection, energy/entropy/reset accounting or practical fault tolerant computation. The resource table and direct embedding tradeoff are in workers/local_operation_inventor/RESOURCE_AND_GEOMETRY.md.
