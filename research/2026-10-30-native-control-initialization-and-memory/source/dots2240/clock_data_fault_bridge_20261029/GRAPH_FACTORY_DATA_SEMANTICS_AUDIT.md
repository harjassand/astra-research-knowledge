# Independent audit: graph-state factory DATA semantics

**20:41 correction/strengthening:** The generic frame-output caution in section4 is unnecessary for this specific graph-state completion. `BARE_GRAPH_STATE_OUTPUT_REPAIR.md` proves U†d_yU<=d_y OR B_y<=A_y and hence the SAME joint syndrome bound for bare physical data. The on-site stabilizer twirl can therefore be applied without a frame decoder. Retain the coherent-syndrome and output-noise cautions, but use the stronger bare-data conclusion.

2026-10-29, from 20:38 UTC. Scope: audit the quantum-state/noise and output conclusions in `autonomous_clock_bridge_20261029/GRAPH_STATE_DATA_BRIDGE.md`. The clean algebra, progress and polynomial-localization proofs are assigned to a separate auditor. This report treats their stated joint flag bound as a hypothesis, not as independently recertified algebra.

## 1. The claimed dressed DATA property really follows

Let U be the specified physical finite-depth dressing. For any actual joint state rho of data D, controllers C and retained bath B, define

    rho_tilde=(U^dagger tensor I_B) rho (U tensor I_B).

This is an exact change of coordinates; it need not be a physically performed measurement or circuit for the mathematical statement. Suppose the root proof establishes, for every finite S,

    Tr[rho_tilde product_(y in S) A_y] <= p^|S|,
    A_y=I-(I-d_y) product_(z in R_y)(I-B_z).

The d_y commute with each other and with every B_z in this frame, and d_y<=A_y. Consequently

    product_(y in S) d_y <= product_(y in S) A_y.

Taking expectations and tracing out controllers and bath gives the genuine data-syndrome law

    Pr(all y in S have graph syndrome -1) <=p^|S|.             (A)

This is not merely a controller property or a classical assumption about unmeasured flags. It is an operational probability statement for the joint commuting graph-stabilizer measurement on the **dressed data**. Coherence between syndrome sectors does not invalidate (A). Arbitrary bath correlations are already included.

The graph stabilizers have a unique common +1 state |G>. Their simultaneous eigenbasis is

    |G_E>=Z_E |G>,  E subset vertices.

Thus (A) says that the diagonal distribution p_E=<G_E|rho_D_tilde|G_E> is p-bounded: sum_(E containing S) p_E <=p^|S|. This is a legitimate noisy-resource-state specification, provided it is named exactly that.

## 2. Do not silently replace this by a stochastic Pauli channel

The actual rho_D_tilde can contain off-diagonal |G_E><G_F| terms. For the one-vertex graph, the pure state

    |psi>=sqrt(1-p)|+>+sqrt(p)|->

has defect probability p but is not the mixture (1-p)|+><+|+p|-><-|. Its Z expectation is 2 sqrt[p(1-p)], versus zero for that mixture. Therefore no claim of a p-strength stochastic Pauli-error state follows without a dephasing/randomization operation or a separate coherent-noise theorem. Tensor products give the same distinction while satisfying the complete product syndrome bound exactly.

One can purify the general state as sum_E |G_E>|phi_E>, with sum_(E containing S)||phi_E||^2<=p^|S|. That is a useful coherent *state* bound. It is not automatically the inclusive **operator-norm** fault-path hypothesis used by a circuit threshold theorem; dimensions and coherent sums cannot be discarded.

This does not invalidate the root's explicitly limited sparse-syndrome factory claim. It limits what can be inferred about subsequent universal computation or unknown-data memory.

## 3. A concrete output repair: graph-stabilizer twirling

If a conventional local-stochastic Pauli-error resource is desired, there is an explicit operation rather than an unexplained decoder oracle. Let independent uniform bits a_y define

    S(a)=product_y S_y^(a_y),
    T_G(rho)=2^(-n) sum_a S(a) rho S(a)^dagger.

Apply it to D only, leaving C+B retained. Orthogonality of the stabilizer characters gives EXACTLY

    (T_G tensor Id_CB)(rho_tilde)
      =sum_E |G_E><G_E| tensor tau_E,

where tau_E are positive subnormalized controller-bath states and Tr(tau_E)=p_E. In particular,

    rho_D,out=sum_E p_E Z_E |G><G| Z_E,
    sum_(E containing S) p_E <=p^|S|.

Every syndrome probability is unchanged. The bath may retain the error label and arbitrary correlations with it: independence from the bath is not asserted. The averaged output data is nevertheless exactly a p-bounded stochastic Z-error graph state. Keeping the random seed as side information instead of discarding it leaves a conditional coherent-state description; the claimed dephased output is the ensemble channel with the seed ignored.

### Concrete local implementation and charges

Up to an irrelevant global phase,

    S(a)=product_y X_y^(a_y) Z_y^( XOR_(z adjacent y) a_z ).

Thus after frame decoding this twirl requires fresh unbiased classical randomness, nearest-neighbor classical parity communication, and on-site Pauli operations; it requires no extra entangling data gate. Bounded graph degree makes the classical neighborhood size constant. There is no need to measure graph stabilizers, postselect, decode a logical code, or assume a global syndrome-processing oracle.

The exact identity presumes the twirl operations are applied faithfully after the stated state has been produced. Noise during randomization, random-bit generation, local communication, or output storage is additional physical noise and must be bounded in an implementation theorem. A retained adversarial bath is not automatically harmless during a finite-duration output protocol. Do not advertise the ideal twirl as an autonomous hardware improvement or free trusted interface.

## 4. Frame/output audit: mathematically valid, physically not free

A finite-depth local U means U^dagger is a mathematically local decoder and maps a local bare observable to a bounded-support physical observable. The reduced state Tr_CB[U^dagger rho U] is therefore well-defined and locally accessible *given the ability to implement those dressed observables*. The bare reduced state Tr_CB[rho] need not be close to a graph state, even in a clean process: pending Stinespring encodings entangle data and auxiliaries. Reading bare data at an arbitrary time is not the stated output.

The actual factory has fixed always-on couplings. Physically applying a finite-duration U^dagger decoder requires either switching/refocusing those couplings or proving that their simultaneous evolution and noise are accounted for by the output circuit. Merely writing a finite-depth unitary does not acquire this control. Likewise, specifying dressed local measurements does not supply arbitrary measurement instruments or a reliable output port. Their supports can overlap; a requested sequence of incompatible measurements must be implemented in its intended order. The root document already disclaims a free output interface; retain that disclaimer prominently.

No global-empty-clock postselection is needed for the mathematical frame definition, the syndrome bound, or the ideal twirl in that frame. If a physical extraction proposal introduces draining/postselection instead, it needs a separate time/success-probability analysis.

## 5. Exact scope of acceptance

Conditional on the separately checked combined-flag estimate, the root construction establishes a **dressed graph-state factory with p-bounded syndrome defects** uniformly in size/runtime after its stated local preparation time. That is genuine DATA progress beyond controller sparsity. It does not establish high global fidelity: only the elementary lower bound F>=max(0,1-np) follows from (A), and an extensive number of defects is allowed.

With the explicit *ideal* frame decoder and local stabilizer twirl, it additionally produces a graph-state ensemble with exactly p-bounded stochastic Z errors. The required physical output controls and their errors remain charged interfaces. Neither version proves scalable unknown-payload quantum memory, a universal fault-tolerance theorem, practical advantage, or a two-site-lease implementation.

The ordinary finite-depth CZ preparation comparator remains decisive. This result's potential contribution is the noisy finite-rate controller/data contract, not invention of graph-state preparation. No decoder is being smuggled in as an oracle.
