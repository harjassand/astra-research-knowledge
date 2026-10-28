# Joint recovery of multiple local logical qubits without marginal-composition assumptions

28 October 2026. **New constructive proof candidate; independent review in progress.** The received one-logical mixed-gauge/locality theorem and CPTP-ERM addendum remain immutable. This is not another implementation of that learner: it addresses the distinct obstruction that individually excellent local decoders need not preserve other logical qubits or their entanglement. No new sampled experiment is reported.

## 1. Contract and the failure of naive composition

Let q,n,w be integers with 1<=q<=n and 1<=w<=n, and let 0<epsilon,gamma<=1. There are q logical input qubits, n known physical output qubits on a known line, and a supplied real four-coordinate encoder x. Ordinary training may prepare known q-qubit states, including a known Clifford circuit within the input block, but retains NO reference through the unknown source. Every source call independently resets. Assume the joint encoded channel

    E_x(omega)=U[sum_(alpha in P_q) P_alpha omega P_alpha†
                                      tensor G_alpha(x)]U†, (1)

where P_q is the phase-free q-qubit Pauli set, U is unknown, G_alpha(x)>=0 are unknown matrix-valued quadratics, G=sum_alpha G_alpha, and Tr G(x)=1. U can be taken unitary from the q logical qubits plus n−q gauge qubits to the physical output. Gauge operators may be noncommuting, rank deficient, globally correlated and arbitrarily ill-conditioned. No Pauli label, source environment or hidden gauge basis is supplied or reconstructed.

For each input label i, define exact global logical generators

    B_Xi=U(X_i tensor I_g)U†,  B_Zi=U(Z_i tensor I_g)U†.

Each PAIR is supported on one unknown interval I_i of width at most w, with 1<=w<=n. The true intervals may overlap; generators of distinct logical qubits commute because they are images under ONE common U. The learner receives the input labels and width/geometry promise, not the physical intervals, generator matrices, inter-qubit frame alignment, or any source circuit. The learned generators will NOT be assumed to anticommute or to commute across i.

Let bars denote the uniform four-anchor mixture. The acquisition margins are

    Hbar_Xi>=kappa Gbar,  Hbar_Zi>=kappa Gbar,
    H_P(x)=sum_alpha chi_(P,alpha)G_alpha(x),  0<kappa<=1. (2)

The joint extraction theorem below uses only (1),(2), exact local compatibility and reset access. To compare against the UNRESTRICTED globally optimal CPTP decoder, separately require

    G_I(x)>=G_alpha(x) for EVERY alpha and every unit x.   (3)

This is a genuinely global operator-dominance promise, not inferred from the 2q local margins. A counterexample to that inference is q=4 with scalar probabilities p(I)=.1, p(XXXX)=.3, and p(X_i)=.15 for each single-X error. Every X_i contraction is1 and every Z_i contraction is.1, but the identity correction is worse than correcting XXXX. Local positive contrasts alone do not supply the desired global oracle comparison. Positivity of ALL Pauli contrasts is a sufficient stronger promise for (3), but is not necessary and need not be learned by the algorithm.

Naive separate decoder deployment is invalid even for an identity two-qubit source. A receiver can extract qubit1 perfectly while resetting or discarding qubit2. A different independently tested receiver can extract qubit2 perfectly. Their individual marginal fidelities say nothing about a sequential instrument that preserves both qubits or a Bell state between them. The present construction therefore never deploys the acquired local CPTP maps directly in sequence. It uses their acquired observables to build a joint reversible receiver.

## 2. Ordinary per-logical acquisition with one common physical marginal

Define the proof-only virtual ideal channel and physical marginal

    E0(omega)=U[omega tensor Gbar]U†,
    rho=E0(I_(2^q)/2^q).

To probe logical i, prepare P_(j,s) on that input and I/2 on every other logical input, j=X,Z,s=±; choose an encoder anchor uniformly. These are actual ordinary product-state/mixed-state preparations, not an entangled source reference. The private bits used to prepare the other logical inputs maximally mixed are discarded/ignored by every estimator; its state guarantee is not conditioned on those bits or on individual random-anchor labels. They produce

    r_(i,j,s)=U[(I_(2^q) tensor Gbar
                         +s sigma_(j,i) tensor Hbar_(j,i))/2^q]U†.

Their average is the SAME rho for every i,j. For X_(i,j)=(r_+−r_−)/2,

    X_(i,j)=B_(j,i)|X_(i,j)|,
    kappa rho<=|X_(i,j)|<=rho,  [B_(j,i),rho]=0.            (4)

The other q−1 logical maximally mixed inputs simply join the proof gauge when viewing this as a single-logical calibration problem. Its four error-conditioned gauge matrices are I_(other logical)/2^(q−1) tensor the appropriate sums of G_alpha. No exponential list of these matrices is acquired.

For a candidate local CPTP map D_i to one qubit, let ell0_i be the Bell loss of D_i E0 when only logical i is variable and all other logical inputs are maximally mixed. Let r_i be the actual two-axis noisy calibration excess over its unknown common ideal baseline. The received local analysis gives

    (kappa/2)ell0_i<=r_i<=ell0_i.                          (5)

Only the acquisition/tournament part of the received theorem is imported here. Its full single-logical encoder optimization and single-logical source-optimum assumption are NOT silently applied; the only encoder optimization will use the actual JOINT decoder later.

### Explicit finite local module

For each i, use the received colored coarse overlap locator, fresh local CPTP-ERM banks, and spectrum-valued comparison tournament. The disjoint-marginal cancellation follows by conjugating X_(i,X) with exact local B_Zi, even when other logical supports overlap. Let

    M=n−w+1,  c=min(w,M),
    R_max=min(M,2w−1),  c1=min(w,R_max),
    eta=epsilon/(16384 q^2),  m0=kappa^2/512,
    m=kappa^2 eta/256,  zeta_ERM<=m.                       (6)

Allocate strictly positive beta_0,beta_A,beta_Q per logical module, with q(beta_0+beta_A+beta_Q)+beta_C<=epsilon/8. Use the fixed caps

    N0=ceil[(80*4^w/m0)log(24*4^w*M/beta_0)],
    N1=ceil[(80*4^w/m)log(48*4^w*R_max/beta_A)].            (7)

Each coarse phase costs2cN0 calls. Each fine phase costs at most4c1N1. Different logical modules use separate source calls; the factor q is charged. Within one color, disjoint physical patch estimators may share a source output, with the exact correlated-marginal/own-record-only contract of the received theorem. Collective quantum memory and cross-copy controls remain paid.

For R_max>=2, let h=ceil(log2 R_max), L=log[2(R_max−1)/beta_Q], and use

    t=kappa eta/(4h^2),
    Npair=ceil[2048 h^2 L/(kappa^2 eta)].                  (8)

The same backward-observable tolerance xi<=kappa*t/4096 and physical spectrum-valued comparison are used. The local ERM bound gives r_min<=22m/kappa=22kappa eta/256<kappa eta/8. The balanced tournament gives

    r_selected<=2r_min+t h^2<kappa eta/2,
    ell0_i<=eta.                                         (9)

For R_max=1 skip comparison formulas and calls. All local candidates are exactly physical by the received rational Choi repair, even on bad histories. After all modules, freeze every selected D_i. No separate marginal holdout is being promoted to a joint-channel certificate: the following operator and reversible-composition proof is essential.

## 3. Turn acquired local channels into controlled reflections

Let A_(j,i)=D_i†(sigma_j), a known local Hermitian contraction. From (9),

    a_(j,i)=Tr rho(A_(j,i)−B_(j,i))^2
        <=2[1−Tr rho B_(j,i)A_(j,i)]<=4eta.               (10)

Compute a known local Hermitian C_(j,i) with certified operator-norm backward residual <=sqrt(eta)/2 from A_(j,i), and let B'_(j,i)=sign C_(j,i), with arbitrary kernel completion. This is a finite known-matrix construction: use a known exactly unitary backward diagonalization and signed rational spectral labels, rather than declare floating eigenvectors exact. The resulting reflection is an actual exact-reference control; its universal-gate approximation is paid in the whole-process budget.

Because rho commutes with the TRUE reflection B, choose a joint eigenbasis of rho,B and an eigenbasis of C. For b in {±1}, every opposite-sign eigenvalue c has |b−c|>=1. Summing the squared overlaps with the rho weights gives

    Tr rho(B−sign C)^2<=4Tr rho(B−C)^2.                   (11)

No commutation of C with rho, source eigenvalue floor, or spectral gap of A or C is required. Weighted Hilbert–Schmidt triangle inequality and (10) give

    delta_(j,i):=Tr rho(B_(j,i)−B'_(j,i))^2
        <=4(sqrt(a_(j,i))+sqrt(eta)/2)^2<=25eta.           (12)

The learned pairs may violate all exact Pauli relations. We do not project them onto an assumed common algebra or infer their cross-commutators vanish. Each controlled reflection is still a unitary, which is enough for the next physical circuit.

## 4. Joint coherent SWAP receiver and the full reference proof

Prepare one receiver ancilla A_i in I/2 for each logical i. This costs q resets plus q private random bits and at most q conditional X gates, discarding those preparation records. Equivalently these mixed states can be purified locally for proof; no part of that purification enters the source. Keep the original physical register until all extraction circuits finish.

For each i, define the always-unitary gates

    C_Z(B)=((I+B)/2) tensor I_A+((I−B)/2) tensor X_A,
    C_X(B)=I_physical tensor |0><0|_A+B tensor |1><1|_A.

Apply, in a fixed order over i, the three gates

    C_Z(B'_Zi),  C_X(B'_Xi),  C_Z(B'_Zi).                  (13)

The corresponding ideal gates with B_Zi,B_Xi perform SWAP between logical i and A_i under the common U. Actual (13) is a literal unitary even for incompatible learned reflections. It acts only on the learned width-w patch and its one ancilla; patches may overlap and earlier extracted outputs are not discarded. At the end discard the physical register and keep ALL q ancillas as the joint recovered output.

### Which ideal marginal is invariant, exactly?

For the global entanglement-fidelity calculation, start with a q-qubit maximally entangled state |Phi>_(R,L), where the ENTIRE reference R is retained only in the proof. Purify Gbar on a gauge reference E and each receiver I/2 on a private reference S_i. Apply U to L and the gauge. The reduced state on the physical register P and ALL receiver ancillas A is

    rho_PA=rho tensor I_A/2^q
          =(U tensor I_A)[I_(L,A)/2^(2q) tensor Gbar](U† tensor I_A).

Every IDEAL elementary CNOT in (13) acts only on the encoded logical factors L and A, identically on the gauge. Therefore every ideal elementary prefix leaves THIS SAME rho_PA exactly invariant. This is an unconditioned reduced-state identity for maximally mixed Bell halves plus the stipulated gauge tensor structure; it is not a claim about arbitrary payload marginals, conditioning on ancillary coin records, or the actual approximate prefix. The references R,E,S remain in the global pure-state proof throughout.

If delta_Zi,delta_Xi are as in (12), the squared state-vector errors of the three elementary gates, evaluated after their ideal prefixes, are respectively

    delta_Zi/2,  delta_Xi/2,  delta_Zi/2.                 (14)

For example C_Z(B')−C_Z(B)=(B'−B) tensor (I−X_A)/2, and the fresh/invariant maximally mixed ancilla contributes trace1/2. No independence of learned generator errors or their supports is used.

Telescope the difference of the full actual and ideal unitary products, placing ideal gates BEFORE each error and actual gates AFTER it. Later actual gates preserve vector norm. Cauchy–Schwarz over the3q elementary errors gives

    ||psi_actual−psi_ideal||^2
        <=3q sum_i(delta_Zi+delta_Xi/2).                  (15)

The ideal final state has the full maximally entangled |Phi>_(R,A) as a tensor factor. Projecting the actual pure state onto its orthogonal complement and then tracing P,E,S gives a JOINT global Bell-loss bound

    ell0_joint<=3q sum_i(delta_Zi+delta_Xi/2)
              <=(225/2)q^2 eta.                         (16)

This preserves entanglement across logical inputs and with the whole reference R in the stated fidelity sense. It is not a product of separately certified marginal fidelities. The q^2 error amplification is an explicit conservative coherent-crosstalk/hybrid cost, not hidden independence. Classical exact compatibility of the learned reflections is unnecessary.

## 5. Global comparator transfer, separate from acquisition

For any joint physical decoder, Bell-outcome probabilities on its output for half a global Bell pair and arbitrary gauge state define a proof-only gauge POVM {T_alpha}_{alpha in P_q}. The noisy-source Bell success is

    F_e(D E_x)=sum_alpha Tr[G_alpha(x)T_alpha].             (17)

Under the SEPARATE global dominance (3), this is at most Tr G_I(x), attained by the common ideal joint logical decoder. Thus the unrestricted full-CPTP optimum at x is ell_star(x)=1−Tr G_I(x). Moreover

    ell(D E_x)−ell_star(x)
      =sum_(alpha!=I)Tr[(G_I−G_alpha)T_alpha]
      <=Tr[G(x)(I−T_I)]<=4ell0_joint.                     (18)

The last step uses the four-real-coordinate positive quadratic domination G(x)<=4Gbar. Neither the number4^q of proof Pauli labels nor a gauge eigenvalue enters this transfer. Those labels are NOT enumerated or measured by the learner.

Combining (6),(16),(18), the learned joint decoder satisfies, for every encoder,

    ell(D E_x)−ell_star(x)<=450q^2 eta
                         =450epsilon/16384<epsilon/20.  (19)

Without (3), the actual joint extraction bound (16) still holds relative to E0, but unrestricted noisy-source near-oracle recovery is NOT established. The q=4 counterexample in Section1 is retained as a decisive boundary.

## 6. A genuinely global ordinary encoder test

Freeze the entire joint decoder after all local acquisitions and sign controls. To learn x, use known q-qubit random stabilizer states |s>=C|0^q>, where C is a uniformly sampled known Clifford. Prepare |s> inside the input block, apply the supplied encoder/source and joint decoder, apply C† to the recovered q-qubit output, and test whether all readouts are zero. This is an ordinary known input, possibly entangled WITHIN the q logical inputs, never with a protected source reference. The readout is a global fidelity test, not q independent marginal pass/fail scores.

The uniform stabilizer ensemble is an exact projective two-design. A direct check is available: write a state in the Pauli basis; random Pauli signs kill distinct cross terms, Clifford conjugation is transitive on nonidentity Paulis, and sum_(P!=I)(Tr rho P)^2=d−1 for a pure state. Hence E[(Tr rho P)(Tr rho Q)]=delta_(P,Q)/(d+1) for nonidentity P,Q, giving E[rho tensor rho]=(I+Swap)/(d(d+1)), d=2^q. For any TP joint channel T the actual Bernoulli error therefore has mean

    e_D(x)=[d/(d+1)]ell(D E_x).                           (20)

The factor is between1/2 and1, not exponentially small. Since the encoder has four real coordinates, e_D(x) is still a nonnegative ten-feature quadratic. Use the received ordinary Bernoulli active design at additive tolerance epsilon_e=epsilon/8 and failure beta_C. Its Bell-risk additive penalty is at most2epsilon_e=epsilon/4. Together with (19) and gamma<=1, its good-event risk is at most(1+gamma)ell_star+7epsilon/20.

For a conservative explicit cap one may take

    J=ceil(log2[128/(gamma epsilon)]),
    b=smallest odd integer >=8log(112J/beta_C),
    N_count<=56b[J+8*2^20*40/(gamma epsilon)].             (21)

Uniform Clifford randomness is not a free oracle: sample an ordered symplectic basis over F_2^(2q), choosing each successive nonzero vector inside the previous pairs' symplectic orthogonal complement and its partner uniformly from the affine hyperplane with symplectic product1. The partner is sampled directly by finite linear algebra, without rejection. Then sample Pauli signs. Nonzero-vector rejection has failure probability at most1/4 per attempt; cap all retries to fit the whole-process random-bit discrepancy. Symplectic elimination compiles each known Clifford with polynomial(q) elementary gates. All input Clifford preparations, inverse-output Cliffords, q final readouts, classical seeds and physical routing are charged. If the hardware permits ONLY product-state logical inputs and local product readouts, (20) is not supplied by that weaker access model; its global qualification/fast encoder cap must be replaced and is not asserted here.

## 7. Full cap, controls, and the diamond boundary

A deterministic complete source cap is

    N_total<=q[2cN0+4c1N1+(R_max−1)Npair]+N_count+1,       (22)

with the comparison term zero when R_max=1. It counts every failed acquisition history and one final payload. Each source call now carries a q-logical-qubit input block and emits n physical output qubits: q*N_total logical input-qubit uses and n*N_total output-qubit exposures, in addition to the supplied encoder-selector/control registers. Do not confuse block-call counts with single-qubit transmissions. The deployed JOINT decoder is invoked only N_count+1 times in this schedule; local acquisition and candidate comparisons use their separately charged local receiver controls. The rate is

    coarse: O_tilde(qw4^w/kappa^2), with log(nq) confidence,
    fine: O_tilde(q^3 w4^w/(kappa^2 epsilon)),
    selection: O_tilde(q^3 w/(kappa^2 epsilon)),
    encoder: O_tilde(1/(gamma epsilon)).                  (23)

For fixed w this is polynomial in q, n,1/kappa,1/epsilon rather than dense tomography/synthesis exponential in the TOTAL logical block size. It is conditional on the strong local-compatible-algebra and global-dominance promises, not a generic scalable coding theorem. Coarse measurement invokes O(qn) local estimators, and each collective Bures bank pays its full memory and cross-copy routing. Processing logical modules sequentially avoids retaining all source banks simultaneously, but not their source/control cost.

Each deployed joint decoder invocation uses3q controlled width-w reflections and4q ancilla Hadamards, plus q mixed-ancilla preparations, retaining n+q data qubits until extraction finishes. Generic known local reflection synthesis costs O(poly(w)4^w) per control before precision overhead. Overlapping supports are acted on sequentially, not assumed disjoint. A nearest-neighbor architecture must allocate an ancilla near each chosen patch or pay its actual routing; a conservative O(q(n+q)) SWAP budget per joint invocation on the full n+q-qubit line can gather/position the q DISTINCT labeled ancillas, with physical data positions tracked and restored as needed so earlier extracted outputs and later physical supports are not silently permuted. A concrete witness places all q labeled ancillas in an end block: SWAP the current ancilla beside its learned patch, execute its three controlled reflections, then reverse the routing permutation. This costs at most2(n+q) routing SWAPs per logical index, restores physical and earlier-output positions, and leaves the recovered ancilla block contiguous. It is O(nq) under q<=n, but not free adjacent ancilla placement. Global encoder-qualification Clifford readout on q distributed output qubits needs additional paid routing and polynomial(q) gates. The final payload may leave logical outputs distributed unless a fixed endpoint layout is required.

Allocate one linked complete-operational discrepancy nu<=epsilon/8 across ALL local estimators, finite SDP/sign controls, ancilla mixtures, random Clifford draws, adaptive training, and payload. Together with the statistical failure allocation in Section2 and bounded loss on every bad history, the averaged joint Bell loss is <=(1+gamma)ell_star+epsilon. Numerical backward error in (12) is already paid before this implementation allowance.

**Untwirled service:** global Bell loss is a genuine joint entanglement-fidelity statement, but it is NOT a dimension-free diamond guarantee on arbitrary q-logical states. A conservative general conversion is ||T−Id||_diamond<=min(2,2*2^q*sqrt(ell(T))). That exponential dimension factor is not suppressed.

**Optional changed averaged service:** after choosing x and the joint decoder, share an internal random q-qubit Pauli key (2q bits), apply its Pauli before the encoder and its inverse after recovery, and discard the key rather than export it to the external reference. This is an additional paid whole-logical Pauli twirl, with at most2q local Pauli gates plus classical coordination per payload. The averaged channel is a possibly CORRELATED global Pauli channel with the same Bell loss, so its unhalved diamond error is EXACTLY2ell. This statement is about the changed averaged channel, not every key-conditioned channel or a record that exposes the key; no protected quantum reference is used. Without those extra controls/discarded randomness retain only the untwirled bound above.

The strongest equally informed conventional learner has this same local tomography/ERM, spectral-control, reversible-swap and global-validation construction. There is no priority claim or quantum advantage over that learner. The substantive bridge is compatible multi-logical extraction with an explicit global-reference/crosstalk ledger. Approximate source locality, drift/no-reset sources, absence of global dominance, product-only global validation and improved q-dependence remain separate open boundaries.

## 8. Evidence status

This manuscript is a proof candidate, not a new count-acquired pilot. Independent reviewers are checking the sign-rounding inequality, invariant ideal-prefix marginal with the entire reference retained, actual overlapping-patch circuit, global Pauli comparator, and global ordinary two-design test. Any prescribed-matrix checks will be labeled zero-source algebra diagnostics. The received one-logical theorem, its stronger conventional ERM addendum and both completed pilots are unchanged.
