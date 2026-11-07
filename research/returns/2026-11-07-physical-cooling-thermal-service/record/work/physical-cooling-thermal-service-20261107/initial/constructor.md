# Independent initial: exact finite thermal collisions with local fault tolerance

Constructor, 7 November 2026. Written before reading any other researcher's new proposal. Prior capital read: `outputs/PROTECTED_QUANTUM_PROCESSING_RESEARCH_DOSSIER.md`; `work/protected-quantum-processing-20261107/principal/THERMAL_SERVICE_THEOREM.md` (supplied SHA256 `bb4e12ae7cc82ed68f94d4b162f6c9a85e08671fd88b805a510ee47058666b40`); prior encoded-port closure, coherent decoder addendum, and quantum-port audit. This is a change of cooling architecture, not a claim about the older N1694 model.

## 0. Result and exact remaining boundary

The proposed replacement is a finite, explicitly Hamiltonian, repeated-interaction refrigerator. Every cooling stroke is an exact energy-conserving exchange with a finite thermal spin. A local hard-core activation rule makes the simultaneously executed strokes mutually disjoint. The *actual finite stroke*, rather than its weak-coupling/short-time Lindblad limit, obeys an exponential energy-moment contraction. A finite-depth erasure argument absorbs fixed local reset, switching, coherent calibration and retained-bath perturbations into its drift. Its error tolerance is independent of the requested storage time; there is no exponentially accurate approximation of an ideal semigroup.

At the accepted DATA premises, Sections 1--7 give a constructive collision-memory theorem, including exponentially many fixed-depth compatible gate bursts, for arbitrary admitted logical/gauge/bath/reference-correlated inputs. Fresh thermal spins and drive/control locations cost O(NK) over K cooling strokes. Their reserve is a real finite bath of O(NK) spins, or a separately charged replenishment service. The theorem is not passive hardware and does not earn an advantage over active FT.

The prior unknown-state encoded WRITE/READ proof can be attached if its active staging primitives are available under this same physical contract. The prior proof explicitly retains noiseless *internal* classical processing. Replacing it by a fully coherent/encoded implementation is a separate source-applicability step, not silently closed here. Logical compatible CNOT/selected-CCZ bursts are supplied without claiming universality from them. The complete universal, physically noisy programme-and-port service remains CONDITIONAL until that FT import and its classical-control treatment are checked.

## 1. Accepted code and local energy inputs

There are N DATA qubits, a stabilizer code of distance d_N >= delta N, a fixed encoder Enc and a canonical frame

    W(|psi>_L |sigma>_G) = E_sigma Enc|psi>.

The fixed representative has weight <= r(sigma). On r(sigma)<r_dec N,

    U(sigma) >= h_conf r(sigma).

The integer U=sum_v u_v is the *actual* commuting local table energy, 0<=U<=u_max N. Each term is nonnegative and vanishes on the code. Changing q qubits affects energy terms with total range <=D_E q. All fixed support/incidence constants count the full projectors/read-neighbourhoods, not merely the Pauli update's support.

The finite catalogue has at most M N directed energy-paired channels a. A channel consists of a bounded-support Pauli and a local spectral projector, giving a lowering partial isometry L_a with

    [U,L_a] = -d_a L_a,     1<=d_a<=D,
    L_a^dagger L_a = Pi_a,high,
    L_a L_a^dagger = Pi_a,low,
    Pi_a,high Pi_a,low = 0.

Splitting each possible local energy decrease by its actual d produces this catalogue; copies are charged separately. Its full DATA supports S_a have size <=q_c, bounded incidence, and conflict graph (S_a intersects S_b) has maximum degree Delta. There are at least kappa U(sigma) high/source channels at each promised syndrome sigma. These are the accepted dense-descent inputs, not new code existence claims.

Set H=J U at a fixed J>0. Temperature beta^{-1}>0 is fixed independently of N and service duration. The bounded locality/degree constants can be enormous. No Euclidean embedding or native three-body implementation follows.

## 2. An exact finite energy-exchange collision

For channel a, bring a fresh two-level spin b_a with

    H_ba = J d_a |1><1|,
    tau_a = diag(1,p_a/(1-p_a))/(1+p_a/(1-p_a)),
    p_a = 1/(1+exp(beta J d_a)).

Equivalently tau_a=diag(1-p_a,p_a). Couple it by

    V_a = g [ L_a tensor |1><0| + L_a^dagger tensor |0><1| ].

The exact identity [H+H_ba,V_a]=0 holds. For a pulse with g tau_col=pi/2, exp(-i tau_col V_a) exchanges the high-system/ground-spin sector with the low-system/excited-spin sector and is identity on the remaining sectors. Free H+H_ba can stay on, because it commutes with V_a. No rotating-wave, weak-coupling, secular or Markov approximation is invoked in this model.

After tracing the used spin, the high->low probability is 1-p_a and low->high probability p_a. The ratio is exp(-beta J d_a). The no-transition Kraus operators are local functions of syndrome projectors. For V_s=exp(sU), the collision's exact Heisenberg action is

    C_a^*(V_s) = V_s [ I
       +(1-p_a)(exp(-s d_a)-1) Pi_a,high
       +p_a(exp(s d_a)-1) Pi_a,low ].             (2.1)

This identity concerns the entire energy algebra, not just one state. The joint nominal collision also preserves the canonical logical factor on the safe module because every local Pauli/syndrome-projector leg does.

## 3. Finite-depth hard-core activation without noiseless decoding

Draw independent candidate bits xi_a with probability h_act=2^{-m}, where the fixed integer m is chosen later. They can be m independent maximally mixed (zero-gap thermal) spins with the all-one projector as the candidate bit. Define

    f_a(xi) = xi_a product_(b adjacent a)(1-xi_b).

The eligible set I(xi)={a:f_a=1} has pairwise disjoint full DATA supports. Its inclusion probability is

    w_a=h_act(1-h_act)^{deg(a)} >= w=h_act(1-h_act)^Delta.

No global coin or feedback decoder is used. The physical controlled interaction is f_a V_a. These terms commute: adjacent terms have f_a f_b=0, while nonadjacent terms have disjoint DATA/bath-spin supports and commuting diagonal activation controls. Their supports include the bounded neighbouring activation registers. Thus exp(-i tau_col sum_a f_a V_a) is exact and has a bounded-depth decomposition by support colouring. Its free Hamiltonian H+sum_a H_ba commutes with the interaction sum.

All activation and thermal spins are fresh each stroke, then isolated permanently from the DATA service. Preparations, their routing, pulse onset/termination and disposal are charged locations. Finite reset errors will enter Section 5; the ideal seed is a product of simple one-spin thermal states, never an interacting Gibbs state containing the unknown payload.

## 4. Exact one-stroke drift

Fix a syndrome sigma and let Delta U be its energy change in one ideal stroke. The bath bits and candidate bits are independent. Since the selected full supports are disjoint, the total energy change is the sum of the selected local changes, evaluated at the original syndrome. Equation (2.1) gives

    E[Delta U | sigma] <= -a_0 U(sigma)+b_0 N,
    a_0=w kappa (1-exp(-beta J)),
    b_0=h_act M D exp(-beta J).                  (4.1)

Choose h_act small enough that 0<a_0<1/2. This is possible after fixing catalogue constants. The formula uses all improving channels; replacing their density by existence of one move would not suffice.

Changing one candidate bit can change the eligibility of at most Delta+1 channels, and changing one thermal occupancy bit can change one transition. Conservative bounded-difference constants are

    c_candidate=2D(Delta+1),       c_thermal=2D.

There are <=M N bits of each kind. The Doob-martingale bounded-difference exponential estimate (obtained by applying the conditional Hoeffding lemma to each revealed bit) gives

    E exp(s[Delta U-E Delta U]) <= exp(C_B s^2 N),
    C_B = M D^2 [(Delta+1)^2+1]/2.               (4.2)

If m independent fair bits implement each xi_a, reveal xi_a itself in (4.2); its distribution is Bernoulli h_act, so no extra factor m is needed in the mathematical random-variable bound. The actual circuit still pays m physical spins per channel.

Consequently, as an operator inequality on the promised input energy/radius module,

    F^*(V_s) <= exp(b_id N) exp[s(1-a_0)U],
    b_id=s b_0+C_B s^2.                          (4.3)

All channels preserve the diagonal syndrome algebra, which proves the operator inequality from its values on syndromes. The nominal map acts on logical/syndrome coherences as a physical CPTP map; (4.3) is not a classical-state assumption on the input.

## 5. Local implementation error is a drift term

The physical nominal stroke is a finite-depth Stinespring circuit, or the exact finite-duration commuting-group Hamiltonian just described. Let each primitive's implementation differ from the ideal primitive by a normal HP local map Delta_j of complete norm <=epsilon_j, with Delta_j^*(I)=0 when it is a channel difference. A primitive may include DATA, a bounded number of active thermal/control spins and one retained perturbation bath B. Bath-only CPTP maps have norm one and need not be inverted. An alternative continuous-time model uses local HP, unital-adjoint-zero perturbations N_Z(t), a physical full CPTP propagator, fixed local support, and

    sum_Z integral ||N_Z(t)||_cb dt <= nu N

per stroke. Direct control calibration and timing errors are included in these bounds. This admits coherent faults and common-bath memory; it is stronger than independent Bernoulli gate flags.

The needed circuit fact is **finite erasure locality**. For r inserted local error maps, remove their causal cones and every selected nominal cooling component meeting those cones. The remaining nominal selected components are exact, disjoint and independent of the dirty map. The number of affected DATA sites is <=Lambda r for a fixed, explicitly circuit-computable Lambda. One obtains Lambda by multiplying the maximum support size by the fanout bound at each of the fixed number of circuit layers, adding all energy-read neighbourhoods and the forward/backward activation-control cones. Quantum flips/coherences of activation bits are included in those cones. The discarded resource spins are included until the factorization has been performed. The common bath can couple arbitrary dirty components but does not enlarge their DATA support.

Here is the relative-observable estimate, avoiding a global O(N epsilon) channel approximation. Split U=U_0+U_Q, where U_Q consists of terms meeting the dirty DATA set Q and 0<=U_Q<=D_E|Q|. The untouched components commute with all dirty maps and can be factored out; their affected energy terms do not meet Q. Any HP dirty insertion map E of complete norm c satisfies

    +/- E^*(exp(sU_Q) tensor I_B) <= c exp(s D_E|Q|) I.

The corresponding ideal dirty TP map has adjoint image of exp(sU_Q) at least I. Thus, enlarging once to compare with the full ideal energy factor,

    +/- term_S^*(V_s) <= [product_(j in S)epsilon_j]
       exp(2s D_E Lambda |S|) F^*(V_s).           (5.1)

This is first established at fixed original classical activation/thermal seed. Outside the dirty cone the seed is unchanged; averaging retains the inequality. Conditional coefficient maps can depend on that seed, because their bound is uniform. Signed maps are never declared CP.

Expanding the finite circuit over inserted errors and summing (5.1) gives

    F_actual^*(V_s) <= exp(b_err N) F^*(V_s),
    b_err <= N^{-1} sum_j epsilon_j exp(2sD_E Lambda).
                                                        (5.2)

A looser product bound product_j[1+epsilon_j exp(2sD_E Lambda)] is enough. For continuous-time insertions, the time-ordered complete-norm expansion gives instead b_err<=nu exp(2sD_E Lambda), with the full physical CPTP premise retained. The nominal group has bounded exact support propagation at all partial times: its free commuting terms and mutually commuting controlled-exchange terms each form one bounded-colour circuit group. Therefore the same fixed Lambda applies to a local insertion at any time, independently of N and stroke duration.

Combining (4.3)--(5.2), set b=b_id+b_err. The actual stroke obeys

    F_actual^* V_s <= exp(bN) exp[s(1-a_0)U].      (5.3)

The local constant errors are absorbed by the protection if b/(s a_0) is a small enough fixed energy density. First fix h_act; then take beta J sufficiently large, s sufficiently small and epsilon_j or nu sufficiently small, all fixed independently of N and K. These inequalities do not assert a useful numerical threshold. An error in a global clock that triggers O(N) locations at once violates the local-noise premise; it is not protected by (5.3).

## 6. From drift to logical protection without hidden mid-stroke paths

Drift alone is not enough: a whole stroke could cross a logical barrier and return to low energy. We therefore also control the actual finite stroke's support expansion.

Choose strict energy/radius and distance margins, e.g.

    r_0<r_dec,   4r_0<delta,
    P=1_(r<r_0N, U<u_cN),
    Q=P 1_(U<=u_iN),

with u_c<h_conf r_0/8 and u_i small enough that D_E C_0 u_i<u_c/8, where C_0=max(1,1/h_conf). Choose alpha_act, alpha_err>0 with

    q_c alpha_act+q_n alpha_err < min[
       r_0/(8c_r), u_c/(8D_E), delta/8].          (6.1)

Here q_n includes the fixed nominal support expansion of a perturbation insertion. Take h_act M<alpha_act/4 and nu<alpha_err/(8e). The number of candidate-active channels has an independent Bernoulli upper tail

    delta_act <= exp[-M N D_Ber(alpha_act/M || h_act)+O(1)].

A continuous fault expansion above alpha_err N has complete-norm tail

    delta_err <= 2 (e nu/alpha_err)^(alpha_err N).

Finite circuit errors have the analogous all-subset expansion tail using sum_j epsilon_j<=nuN. A catalogue/time-normalization constant can be included in nu. Each retained path on Q has DATA operator support <=(q_c alpha_act+q_n alpha_err)N beyond the input canonical representative. Its output energy and radius are strictly within P, by confinement, bounded syndrome spread and (6.1).

For any retained source/target syndrome, its canonical Pauli coefficient has weight <d_N and zero syndrome, hence is a stabilizer up to scalar. Therefore the *whole retained signed map*, including syndrome coherences and arbitrary logical/gauge/B/reference coefficients, factors as

    F_low = id_L tensor C_signed,

with output in P. This support proof is what prevents a logical slip hidden inside one finite stroke. It does not infer logical protection merely from energy drift.

Put delta_step=delta_act+delta_err. Define the positive same-bath comparison

    C(theta)=Tr_L[P F_actual(I_L/d_L tensor theta) P].

C is CP/TNI on the actual gauge/B algebra, and

    ||F_actual - id_L tensor C||_diamond,Q <=2delta_step.
                                                        (6.2)

This follows by applying exactly the same complete contractions to F_actual-F_low. It is a proof comparison, never a physical bath reset. Since P commutes V_s and compression deletes positive output, C inherits (5.3) exactly. The noise floor in (5.3) is not multiplied by the exponentially long requested time.

For a positive subnormalized state with x_k=Tr exp(sU)rho_k, Holder/Jensen for the concave power 1-a_0 gives

    x_(k+1) <=exp(bN) x_k^(1-a_0),
    log x_k <=nu_eq N+(
         log x_0-nu_eq N)(1-a_0)^k,
    nu_eq=b/a_0.                                  (6.3)

These are valid with arbitrary retained B and inert reference. A proof-only filter to Q after the comparison costs at most

    epsilon_filt <=2exp[-(s u_i-nu_*)N/2],
    nu_*=max(log x_0/N,nu_eq)<s u_i.                (6.4)

The filter never increases x. All proof states stay positive, CP/TNI and unnormalized. At K strokes, logical half-trace/half-diamond error is bounded conservatively by

    epsilon_in+epsilon_read+
       K [2delta_step+epsilon_filt].              (6.5)

Thus K can be exp(cN) for a positive fixed c smaller than the displayed tail exponents. The comparison is to the *actual* initial decoded logical/reference state. No logical/bath product premise is needed for admitted Q-supported inputs and moment bounds.

## 7. Repeatable useful gates and encoded recovery

Use any separately proved code-preserving bounded-depth logical gate with actual partial/suffix spread B_g, including the accepted compatible CNOT and selected two-sector CCZ specializations. The collision couplers are idle during the finite logical burst; J U may either be retained and included as a bounded local disturbance or switched off with all switching faults charged. Idle thermal/control spin leakage is included in the local model. A low-energy input Q_pre has a canonical error of weight <=C_0 u_pre N. A low-order finite-burst expansion has total output representative weight

    <= B_g C_0 u_pre N + B_g q_g alpha_g N.

Strict distance/radius/energy margins identify the same canonical logical gate at the endpoint. With integrated local disturbance mu_g N and mu_g<alpha_g/(8e), the discarded signed tail is <=2(e mu_g/alpha_g)^(alpha_gN). Applying the same positive logical-average repair gives error at most twice that tail. Peak pulse strength and all switching/timing precision are finite constants independent of N and K; coherent fractional calibration error must separately satisfy the integrated bound and is not reduced merely by a faster pulse.

After a burst, apply k_c cooling strokes, where

    k_c >= log[(s u_post-nu_eq)/(
                    s u_pre/2-nu_eq)] /[-log(1-a_0)]

and nu_eq<s u_pre/2. This is a fixed constant number of finite collisions. Equation (6.3) restores the pre-gate moment. A proof filter and CP/TNI repair give an additive exponentially small error per burst, so G bursts and K storage strokes satisfy one telescoping estimate of the form

    error <=epsilon_in+epsilon_read
       +K epsilon_cycle+G epsilon_burst,
    epsilon_cycle,epsilon_burst <=poly(N)exp(-c_0N).

Every used cold/control spin is discarded once and never recoupled; the same actual perturbation bath B is retained. The construction never physically decodes and reinitializes the memory between storage intervals.

The accepted greedy energy decoder plus Clifford unencoder is robust on the combined low-energy+interface error span. Its coherent implementation has waiting-inclusive circuit size S_D=O(N^4); the writer has S_E=O(N^3). Unknown reference-entangled input must arrive at encoded ports. Bare unknown input before redundancy has its irreducible fixed error floor, and an unencoded final output has the same endpoint problem. Prior encoded-port staging gives exponentially small internal errors at polynomial paid resources under its stated primitives. Its own noiseless-classical premise is recorded in Section 0 and is not erased by the coherent outer decoder.

## 8. Explicit full resource boundary and strongest comparator

Let L_c N be the counted elementary locations in one cooling stroke, d_c its fixed compiled depth and tau_c its physical duration. Each stroke uses <=M N thermal exchange spins, <=m M N random zero-gap spins and <=c_auxN additional local controller/routing cells. A once-through finite-bath realization for K strokes and G logical bursts has

    peak active DATA+cooling workspace <=C_active N,
    thermal/random source reserve <=C_source N K,
    cooling-control locations <=L_c N K,
    compatible-burst locations <=L_g N G,
    cooling/burst physical time =K tau_c+G tau_g,
    source transport/disposal events <=C_source N K.

Add the actual encoded-port block/workspace/location/time cost W_port,L_port,T_port. If the intended input/output error is exp(-cN), the prior threshold compilation takes accuracy parameter ell=O(N) and gives polynomial overhead in N, not cost zero. Gate routing, code-description acquisition, noise in classical decisions, all waiting and clock/drive hardware belong in these constants or the explicit port terms. A fixed hardware timer with independent local pulse jitter is covered; a perfectly reliable, free, global computer is not part of this construction.

Each exchange is energy-conserving for DATA+spin, so the spent spin carries exactly the signed heat taken from DATA for that collision. It can absorb at most J D in absolute energy. Hence gross absolute exchanged energy <=J D M N K. This is an upper bound on gross exchange, not an assertion of net refrigeration work. Initial Gibbs-spin energy is <=J D M N K; its free-energy value depends on the available ambient reservoir. Used-spin erasure or re-equilibration, refrigerator efficiency, transport and drive dissipation must be charged for a cyclic machine. Providing a finite initial spin reserve avoids assuming a perfect cyclic reset but pays O(NK) bath size. No autonomous finite bath can absorb unbounded entropy for free.

The strongest matched comparator gets the *same* local collision/reset spins, fast bounded-body control, hard-wired finite-depth circuits, quantum ports, code access, routing, clocks and classical hardware. It can run conventional active FT, measurement-free local correction (Hong--Guo--Lucas), or stronger qLDPC FT at their hypotheses. For a circuit of L logical locations and total error epsilon, concatenated FT uses polylog(L/epsilon) overhead per logical location; when L=exp(cN), this is polynomial in N. If our polynomial encoded staging is charged, neither an asymptotic total-resource nor numerical advantage is established. The claim earned is a finite physical implementation theorem at a local-noise contract, not a civilization-scale capability advantage.

## 9. Source and obstruction accounting

Primary predecessors verified at least at their relevant statements before this freeze:

* Hong--Guo--Lucas, arXiv:2403.10599v3, Sections 3--4 and Appendix E. They already obtain finite-depth, measurement-free implementations of thermal qLDPC memory; Appendix E.2 constructs a Gibbs sampler, E.3 tunes rates in the presence of errors, E.4 treats circuit costs. The broad idea of implementing thermal correction by a finite circuit is theirs and older engineered-dissipation work, not new here. The candidate new operation is the exact energy-conserving hard-core finite collision plus a direct arbitrary-local-fault drift proof; priority of that conjunction is NOT ESTABLISHED.
  https://arxiv.org/html/2403.10599v3
* Merkli, arXiv:2105.00023v2, Theorem 1.1, equation (1.30), proves a uniform-in-time O(|lambda|^(1/4)) reduced superoperator approximation for the specified finite-level spin-boson-type system, assuming form-factor regularity and spectral/Fermi-golden-rule conditions. Its constants depend on spectral parameters, with Proposition 1.2 exposing temperature dependence. It does not give uniform code-size complete local error bounds on the present degenerate logical subsystem and all changing control paths. A fixed global approximation error is not an arbitrarily accurate encoded service theorem. This collision construction does not import it.
  https://arxiv.org/html/2105.00023v2
* Ong--Parameswaran--Placke--Hahn, Phys. Rev. A 114, 042445 (21 October 2026), DOI 10.1103/25wc-17zy. The accessible publisher abstract states fixed-point error scaling O(J^2) for weak-coupling collision thermal-state preparation and discusses randomized-drive variance. A fixed-point Gibbs approximation neither preserves an arbitrary unknown logical state nor proves its repeated-gate service channel. Full-text theorem applicability has not yet been checked here; no theorem is imported from this abstract.
  https://journals.aps.org/pra/abstract/10.1103/25wc-17zy
* The old encoded-port proof directly verifies Christandl--Fawzi--Goswami arXiv:2408.05260v3 Lemma 40 and Lemmas 41--42. Its source-specific classical assumption remains visible. Source caches and new FT/classical-control applicability checks will be recorded under `constructor/sources/` after this freeze.

Decisive counterexamples/tests:

1. Gibbs fixed-point accuracy alone permits complete logical dephasing within every degenerate syndrome sector. It cannot certify a quantum memory.
2. A single global error of probability p that applies a logical Pauli to all DATA gives a fixed logical floor; marginal per-qubit p is not the local complete-noise contract.
3. Global low final energy alone does not rule out a whole-stroke logical slip; Section 6 explicitly controls activity and insertion support.
4. Taking h_act of order one can activate an extensive update set outside the correctable span; making the stroke exact does not repair that. Choose h_act below a code-dependent fixed threshold.
5. A finite reservoir reused without reset can accumulate system/bath information and return it. Here each thermal spin has one contact only, and O(NK) reserve/renewal cost is explicit.
6. A local reset channel with small reduced-state error but arbitrary hidden correlations with the payload/future reservoir is insufficient. The primitive is a complete local reset error bound, or a product thermal-spin reserve plus explicitly local perturbations.
7. No finite-temperature bath plus energy-conserving unitaries supplies arbitrarily pure bare unknown inputs. Quantum information must enter at protected encoded ports or retain the floor.

Status: **CONSTRUCTIVE THEOREM at accepted DATA + finite local circuit/Hamiltonian + fresh product thermal spin reserve + physical complete local-noise premises**, pending hostile checking of the erasure-locality/relative-observable lemma. **CONDITIONAL** full arbitrary-programme encoded-port service until same-contract FT import/classical-control treatment is verified. **NOT ACHIEVED** physical demonstration, useful numerical thresholds, Euclidean layout, novelty/priority, complete-resource advantage, or recovery of the older three-body N1694 contract.
