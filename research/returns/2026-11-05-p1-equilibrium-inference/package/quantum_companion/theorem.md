# Exact acquisition law for fully scrambling tracial collision layers

Working companion derivation, 5 November 2026. This is a scoped extension of existing radiative random-circuit machinery. Weinstein, Kelly, Marino and Altman, PRL 131, 220404 (2023), arXiv:2210.14242v2, already give the independently initialized inverse-circuit decoder, its operator-survival formula, mixed-versus-pure environment distinctions, and local-circuit recovery transitions. The addition proved here is an exact finite-size coherent-partial-SWAP law, a converse for every decoder, and a keyed diamond-norm comparison with source forgetting. It is not a new scrambling mechanism or a solved quantum memory law.

## Model and result

An arbitrary unknown qubit, including its reference, occupies source site 1 of n spins. Other source spins start tracial. Cycle j applies an independently uniform n-qubit Clifford C_j to the source and then parallel partial SWAPs U=cos(theta)I+i sin(theta)SWAP between every source spin and a fresh tracial carrier. All outgoing carriers and all Clifford labels are available to the receiver. The source and the purifications/preparation labels of tracial ancillas are inaccessible. Carriers never return. The decoder is otherwise an arbitrary CPTP operation, with arbitrary initialized workspace and classical feedback.

Let s=sin(theta), c=cos(theta), b=s^4, and define

    kappa = ((1+3b)^n-1)/(4^n-1),
    eta   = ((1+3c^2)^n-1)/(4^n-1),
    q_T   = (1-kappa)^T,     a_T=1-q_T.

All ensemble statements refer to the physical randomized channel retaining its complete classical key. They are not assertions about every fixed schedule.

For 0<theta<pi/2:

1. Initialize n tracial dummy source spins. Traverse the stored output layers backwards, applying inverse collisions followed by C_j^dagger on the dummy source. Return dummy site 1. This physical decoder yields exactly the averaged qubit channel a_T id+(1-a_T)R_tau and half-diamond error 3q_T/4.
2. Every decoder, even a global key-conditioned one with all outputs, has half-diamond error at least (3/4)(1-sqrt(a_T)).
3. The keyed channel from the unknown qubit to the final source has half-diamond distance d_src from the keyed tracial replacer satisfying

       (3/4)eta^T <= d_src <= min(3/4,(3/2)eta^T).

Thus, putting alpha=4 epsilon/3 in (0,1), optimal acquisition cycles satisfy

    ceil(log(1/(2alpha-alpha^2)) / -log(1-kappa))
      <= T_opt(epsilon)
      <= ceil(log(1/alpha) / -log(1-kappa)).

These bounds match the leading coefficient of log(1/epsilon). They do not solve minimum receiver memory or give a decoder faster than the inverse reader.

The obstruction is also typical below its exponential timescale. For each fixed key define A_K as the mean of the three exported squared Pauli norms. Since E A_K=a_T, the probability that a fixed-key channel even admits a decoder of half-diamond error <=epsilon is at most

    a_T/(1-4epsilon/3)^2.

This follows from the fixed-key Bell-fidelity bound and Markov's inequality. Independently, the probability that the fixed-key source distance exceeds delta is at most (3/2)eta^T/delta. In particular, at fixed nontrivial angle, source forgetting after one cycle and failure of every radiation decoder for T exponentially large but o(1/kappa) hold simultaneously with probability tending to one as n grows. This is stronger than discarding a key or averaging over unknown scrambling, although it still does not assert an obstruction for every key.

## Proof of the export law

Conjugating a one-site source Pauli by a partial SWAP produces four Pauli terms with squared coefficients c^4, s^4, c^2s^2, c^2s^2. The s^4 term has source identity and transfers the original Pauli to the carrier. Identity stays identity. For each fixed outgoing carrier-Pauli label, the map from input source-Pauli labels to surviving output source-Pauli labels is injective on its nonzero domain: carrier identity leaves the source label unchanged; a nonidentity carrier label b sends input b to source identity and sends the other two nonidentity inputs to distinct nonidentity labels. An input identity cannot emit a nonidentity label.

Hence each full bath-Pauli history starting from one source Pauli identifies at most one final source Pauli. Distinct histories are orthogonal and cannot interfere. Histories starting from distinct source Paulis cannot merge to the same bath history and final source Pauli. Clifford source gates preserve this injectivity.

Squared coefficients therefore evolve as a stochastic Pauli process. A source string of weight w becomes source identity at the next collision layer with probability b^w. Source identity is absorbing. A fresh uniform Clifford makes every nonzero source Pauli uniform among 4^n-1 labels. The conditional extinction probability is

    sum_{w>=1} binom(n,w)3^w b^w/(4^n-1)=kappa.

Thus the ensemble-mean surviving squared norm is q_T. All three initial logical Paulis have mean exported norm a_T and their exported Gram cross terms vanish.

For fixed key K, write the carrier channel on m=nT output qubits as

    Gamma_K((I+r dot sigma)/2)=2^{-m}(I+sum_mu r_mu B_mu,K).

Its average output is tracial. The physical inverse reader is its tracial Petz map D_K=2^{m-1}Gamma_K^dagger. Its Pauli-transfer matrix equals the Gram matrix 2^{-m}Tr(B_mu B_nu), which is diagonal by the history argument. Uniform Clifford averaging equalizes the diagonal entries to a_T. No extra logical twirl is needed. This proves claim 1.

Trace-norm contraction gives, for any decoder R_K,

    ||Gamma_K(sigma_mu)||_1 <=2sqrt(a_mu,K),
    F_ent(R_K Gamma_K)<=[1+sum_mu sqrt(a_mu,K)]/4.

Jensen over the retained keys gives F_ent<=(1+3sqrt(a_T))/4. Bell-projector testing bounds half-diamond error below by 1-F_ent. This proves claim 2 for unrestricted decoding and therefore for every causal receiver as well.

## Proof of keyed source forgetting

Tracing a tracial carrier applies single-site depolarization with visibility c^2. For fixed keys, each initial logical Pauli remains one source Pauli with amplitude

    t_mu(K)=c^{2 sum_j w(P_mu,j)}.

After undoing the known total source Clifford, the channel is a positive-diagonal qubit Pauli channel tensored with n-1 tracial spins. Its exact half-diamond distance from the replacer is

    max((t_X+t_Y+t_Z)/4,max_mu(t_mu)/2).

A Bell input attains the diamond norm for each key, so the keyed norm is the average of this expression. Fresh Clifford transitivity gives E t_mu=eta^T. The expression is bounded below by sum t_mu/4 and above by sum t_mu/2, proving claim 3. Keys have not been discarded.

## Scaling and actual comparison

At fixed theta in (0,pi/2), kappa~[(1+3sin^4 theta)/4]^n and eta~[(1+3cos^2 theta)/4]^n. One cycle can make the source exponentially insensitive to the input while every receiver needs exponentially many cycles to acquire that input from the outputs. For fixed n and weak theta,

    kappa=[3n/(4^n-1)]theta^4+O_n(theta^6),
    -log eta=[3n4^{n-1}/(4^n-1)]theta^2+O_n(theta^4).

At n=1 this reduces to the preserved single-source quartic law. With the same n carrier ports and no source scrambling, inverse recovery of the first qubit instead has error 3(1-sin^4 theta)^T/4. Changing source dynamics changes the acquisition rate exponentially; a receiver forbidden to control the source cannot make that comparison into a control advantage.

The inverse circuit is the strongest concrete ordinary comparator and is already nearly optimal here. The closest 2023 paper proves the same physical mechanism for local Haar/Clifford source layers with random full SWAP emissions, including inverse-reader fidelity 1-3P_survival/4. The present coherent partial SWAP replaces the effective operator death probability by sin^4 theta and makes the finite fully scrambling model exactly soluble. These are scoped additions.

## Optional local-circuit mapping

For independent uniform two-qubit Clifford gates in a brickwork source circuit, averaged Pauli support follows exactly the same occupation process as the 2023 full-SWAP model at effective death probability p=sin^4 theta. Conditional on at least one occupied input to a gate, the Clifford output occupies both sites with probability 3/5 and each one-site choice with probability 1/5. After collisions,

    P11=(3/5)(1-p)^2,
    P10=P01=(1-p)(1+3p)/5,
    P00=p(2+3p)/5.

This is an equality of ensemble second-moment support dynamics, not an equality of full physical output channels. The inherited inverse decoder has error 3P_survival/4 and every decoder has error >=(3/4)(1-sqrt(1-P_survival)). The 2023 numerical critical point may be translated only at its stated numerical scope. A rigorous elementary region is p>3/8: expected offspring 8(1-p)/5<1 implies P_survival(T)<=[8(1-p)/5]^T and therefore exponential convergence. No unproved exact critical point is asserted.

## Execution bill and limitations

Each cycle consumes n fresh tracial carriers and a uniform Clifford key of O(n^2) bits. Source-junk and bath purifications must remain inaccessible. This is a driven-source family requiring source-side Clifford control; it is not a statement about arbitrary uncontrolled Hamiltonians. Koenig and Smolin give O(n^3) classical sampling/compilation and O(n^2) elementary Clifford gates using Gaussian elimination. A conservative nearest-neighbour routing implementation uses O(n^3) bounded-strength gates per source layer. A cycle must last long enough for that circuit before its collision layer.

The displayed decoder stores nT output qubits and uses n dummy qubits, T inverse Clifford circuits and nT inverse partial SWAPs. Peak core memory nT+n excludes routing/protection. Keys cost O(Tn^2) classical bits. A concrete shifting-store implementation adds O(nT) routing cells and O(nT^2) swaps, with O(nT^2) carrier-cycle storage volume; different memory architectures may improve this bill. There is no free arbitrary-address memory assumption.

Preparation, gates, routing and storage defects add in half diamond by the channel hybrid bound. A total defect nu increases the attained error by at most nu; a forward-channel defect can weaken the converse by at most that defect. For G primitives, error nu/G per primitive is sufficient. No fixed physical noise floor, fault-tolerance overhead, energy budget or finite-temperature robustness is invented without a hardware model. All ancillas are reset or discarded after a run; there is no catalytic reuse claim. The optimal memory law from the original one-source programme remains open.

## Primary sources

- Weinstein, Kelly, Marino, Altman. https://arxiv.org/html/2210.14242v2 ; DOI 10.1103/PhysRevLett.131.220404.
- Koenig, Smolin. https://arxiv.org/pdf/1406.2170 ; DOI 10.1063/1.4903507. Their page 2 explicitly records O(n^2) Gaussian-elimination Clifford synthesis and O(n^3) runtime.
- Preserved Astra joint_recovery_continuation.pdf, libfile_0f71dee9ed588191b8aaba8ca648e868, for the original tracial ledger and one-source carrier law. The many-source extension is proved separately above.
