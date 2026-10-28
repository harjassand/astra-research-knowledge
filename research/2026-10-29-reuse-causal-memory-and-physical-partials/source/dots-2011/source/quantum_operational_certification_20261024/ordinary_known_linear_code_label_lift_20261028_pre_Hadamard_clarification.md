# A coherent label lift for known linear-code subsystems behind an unknown mixer

28 October 2026. **New candidate; independent receiving pending.** This is a distinct extension of paid syndrome exploration, not a revision of received repetition-code results. The known classical code/coset circuit and pre-noise control port are SUPPLIED; the physical output mixer and its logical subsystem are learned. General unknown-code discovery and scalable tomography in unbounded width are not claimed.

## 1. Known code, actual extra port, unknown physical instrument

Let C be a supplied full-column-rank binary n-by-k matrix, 1<=k<=n, d=2^n and m=k+1. Its columns are c_i. A known quantum encoder maps |l> to |C l>, using clean ancillary wires and a paid circuit. A supplied complete transversal {e_g:g in {0,1}^{n-k}} includes e_0=0. The map

    x=C l(x) XOR e_(g(x))                                      (1)

is a known bijection between n-bit x and (l,g). A reversible circuit for this bijection (or an explicit finite truth table from which one is compiled) is part of the interface; its actual resources are paid. The transversal need not be linear or consist of minimum-weight errors. In particular l_i(x) can be a nonlinear classical decoding function. Translation by a codeword always gives

    l(x XOR C a)=l(x) XOR a,   g(x XOR C a)=g(x).                (2)

The calibration device exposes the n encoded physical wires BEFORE an unknown noise channel and fixed unknown n-qubit mixer V. It can draw uniform g and apply known X_(e_g) there. This costs n-k fair bits, computation of e_g and at most n physical X gates per block, plus known encoder resources. It is not an operation assumed at an enclosed logical black-box port. There is still one unknown-source call per block. Turn injection OFF for genuine payloads.

At each complete exposed prior history h, allow the actual source

    N_h=(Ad_V tensor id) o sum_f(Ad_Xf tensor F_(f,h)),           (3)

with arbitrary CP maps F_f:M->M' on retained quantum memory and T=sum_f F_f TP. The maps may vary with time/history and preserve coherent memory. They are fixed before current private setting, preparation, injection and readout coins except through the quantum input, exactly as specified in (3). V is fixed for calibration and future service. This is a restricted physical bit-pattern instrument, not a generic environment coupling.

During acquisition assume only the qualitative coordinate CP biases

    H_j=sum_f (-1)^(f_j) F_f is CP, j=1,...,n.                  (4)

No positive numerical bias, stationarity, majority/coset dominance, spectral floor or microscopic instrument is supplied. Independent unequal physical flips with rates at most 1/2, selected by an arbitrary prior memory instrument, are one subclass. General correlated instruments can also satisfy (4). Membership is trusted, not certified from finite observations.

The intended exact decoder uses U|l,g>=V|C l XOR e_g>. For an uninjected payload the complete channel has logical-X/gauge blocks F_(C a XOR e_g); hence D_*=Tr_G Ad_Udagger is always a specified extraction operation. It is the pointwise full-CPTP Bell-loss oracle only if, separately, F_(e_g)-F_(C a XOR e_g) is CP for every a,g. Known-code structure or coordinate positivity does not imply that dominance. Future coordinate positivity is unnecessary after the fixed operators have been acquired; the future fixed-V bit-pattern form remains required for this stated comparator.

## 2. One ordinary calibration block and its exact complete moments

Draw a private setting r uniformly from {0,1,...,k}. For r=0, prepare every logical qubit in a uniform computational basis state l. For r=i>0, prepare logical i in a uniform X eigenstate with known sign s, and the other k-1 inputs in uniform computational basis states. These are ordinary logical product states followed by the known encoder. Always inject an independent uniform e_g. Measure the n physical outputs in independent uniformly random Pauli bases and form the usual product shadow Z_out.

For setting 0 the known prepared physical string is x=C l XOR e_g and is uniform over all d strings. For each physical coordinate j retain the actual record

    Y_j=m 1{r=0} (-1)^(x_j) Z_out.                              (5)

For each logical i retain

    Y_Xi=m 1{r=i} s Z_out.                                      (6)

All n+k records come from the SAME block, with their real incompatibility factor m. They can be correlated; no outputs are cloned and no setting's samples are free. The injection and current input labels are averaged within the asserted conditional means, even though their known signs occur in the estimator.

Put C_j=V Z_j Vdagger and B_Xi=V X_(c_i) Vdagger. For any prior conditional memory state omega,

    E[Y_j|past]=C_j Tr H_j(omega)/d,
    E[Y_Xi|past]=B_Xi/d.                                        (7)

Before tracing outgoing memory, the corresponding signed operators are C_j/d tensor H_j(omega) and B_Xi/d tensor T(omega), including arbitrary memory-reference extensions. Indeed uniform x gives

    d^-1 sum_x (-1)^(x_j)|x XOR f><x XOR f|
       =(-1)^(f_j) Z_j/d.

For an X_i setting, averaging the other logical bits and all syndrome representatives gives the signed physical operator X_(c_i)/d: each x has exactly its translated partner x XOR c_i. Every X_f commutes with this translation. The unsigned physical/memory output for EACH setting, after averaging its signs/logical labels and injection, is exactly I_d/d tensor T(omega). This does not imply that an individual readout branch fails to disturb memory.

Under (4), theta_j=Tr H_j(omega) lies in [0,1]. Every finite bank's predictable coordinate contrast is the same fixed C_j multiplied by theta_bar_j/d; the conserved logical-X gap is always 1/d. Different coordinates may be informative at different stages. Their numerical biases remain unknown.

## 3. Finite capped operator acquisition with all physical costs visible

Choose rational 0<epsilon<=1, 0<beta<=epsilon/8 and a supplied finite stage cap S>=0. Let delta be the largest positive dyadic satisfying

    delta^2<=epsilon/[4 k^2(4n+1)^2].                            (8)

Thus delta<=1/4 and delta^2>epsilon/[16 k^2(4n+1)^2]. For stages s=0,...,S use fresh ordinary banks

    a_s=2^(-s)/(16d),
    L=ceil log2[2d(n+k)(S+1)/beta],
    N_s=8 m 3^n L/a_s^2.                                        (9)

All N_s are integers. The conditional squared moment of each record is <=m3^n I: its squared importance factor is m^2, its setting probability is 1/m, and the ordinary product-shadow second-moment bound applies to that setting's actual averaged output. Every centered increment has norm <=2md. With a_s<=1/(16d), matrix Freedman's denominator is <=3m3^n. Therefore a union over n+k matrices, both signs and S+1 stages gives one event Good of probability >=1-beta with

    ||Deltahat_(v,s)-Delta_bar_(v,s)||op<=a_s                    (10)

for every reached bank and v. This is the same actual-record martingale argument as the received local source, not an iid substitution. Correlations across v and arbitrary retained memory are allowed.

For each unresolved v, use finite rational Jacobi to form Q D Qdagger within Frobenius a_s/4 of its empirical rational matrix, with Q EXACT rational unitary. Set e_s=5a_s/4, h=min|D_aa| and retain S_v=Q sign(D) Qdagger at the FIRST passing rational guard

    h>e_s,       2e_s<=delta(2h-e_s).                           (11)

On Good, every retained S_v is within delta in operator norm of its fixed target C_j or B_Xi by the received two-sector sign bound. It is exactly physical on every record. A reached true gap gamma_v>0 with a_s<=delta gamma_v/5 forces the guard. Retain certificates permanently; do not require simultaneous informative banks. ABSTAIN before requesting an unknown payload if any item remains unresolved at S.

Exact worst-case source cap is N_base(4^(S+1)-1)/3, with N_base=8m3^n L(16d)^2. If actual declared reached-bank coordinate biases are persistently >=theta_*>0 almost surely and the first sufficient scale is funded, then with gamma_*=min(1,theta_*)/d the first sufficient bank has

    N_s<800m3^n L/(delta^2 gamma_*^2)
       <12800m3^n L k^2(4n+1)^2/(gamma_*^2 epsilon),             (12)

and cumulative calls are <(4/3)N_s. This is O_tilde(m k^2 n^2 12^n/(theta_*^2 epsilon)), not a polynomial-in-n general decoder learner. The first-stage case also satisfies the loose bound. Mere future positive-bias episodes do not bound their arrival cost. Probabilistic completion needs the stated almost-sure excitation premise or a separate failure debit; it is not obtained by conditioning on favorable random averages.

## 4. The coherent label lift: an actual physical reflection without joint diagonalization

Individually learned S_j need NOT commute. Taking a Boolean polynomial in them and calling it a reflection would be invalid. Instead introduce n fresh receiver-owned coordinate ancillas A, all initialized to |0^n>. For each j define the literal controlled-copy unitary

    Q_j(S_j)=(I+S_j)/2 tensor I_(A_j)
            +(I-S_j)/2 tensor X_(A_j),
    W_hat=Q_n(S_n)...Q_1(S_1).                                  (13)

Each Q_j is an exactly unitary Hermitian involution. It can be implemented as H_(A_j), controlled-S_j, H_(A_j); other ancillas are spectators. Let P_i be the KNOWN diagonal phase oracle on A,

    P_i|a>=(-1)^(l_i(a))|a>.                                    (14)

Its reversible classical circuit evaluates (1), phases the i-th logical bit and uncomputes, with clean work returned. Define the learned augmented reflections

    Zhat_i=W_hat^dagger P_i W_hat,
    Xhat_i=S_Xi tensor I_A.                                     (15)

All Zhat_i are EXACT physical reflections and commute with each other, despite arbitrary noncommutation among the S_j. No exact commutation of Xhat_i with them is assumed. Every operator and circuit is finite rational, apart from the explicitly paid physical gate-synthesis approximations.

Let W_* use the true C_j. In the V-rotated computational basis it copies x into A:

    W_* (V|x> tensor |a>)=V|x> tensor |a XOR x>.

Thus Z_i^*=W_*^dagger P_i W_* has eigenvalue (-1)^(l_i(x XOR a)). Together with X_i^*=B_Xi tensor I_A these are the EXACT logical Pauli generators of the augmented identification

    U_tilde|l,g,a>=V|C l XOR e_g XOR a> tensor |a>.               (16)

Equation (2) proves all required anticommutation/commutation relations, for EVERY a, not just the clean-ancilla subspace. U_tilde is a unitary bijection. With A initially zero it agrees with the desired original subsystem U; therefore its exact extraction is D_* on the original source output. The coordinate ancillas are internal receiver workspace, not a supplied environment or protected calibration reference.

Because ||Q_j(S_j)-Q_j(C_j)||op=||S_j-C_j||op, unitary telescoping gives

    ||W_hat-W_*||op<=n delta,
    ||Zhat_i-Z_i^*||op<=2n delta,
    ||Xhat_i-X_i^*||op<=delta.                                  (17)

The ancillas must be retained through the ENTIRE multi-logical extraction. Do not reset them between noncommuting approximate blocks. They and all original physical outputs are discarded only at the end.

## 5. Complete-reference coherent extraction and future reuse

Prepare k fresh mixed receiver qubits. Apply the literal three-controlled-reflection SWAP network for each logical i, using (Zhat_i,Xhat_i,Zhat_i), in a fixed order; retain P,A and every receiver qubit until all k blocks finish. This is an actual unitary/isometric receiver on EVERY accepted record. The true logical blocks swap the k logical factors into the receiver qubits while preserving the entire augmented gauge, independent of block order.

Every controlled-reflection difference is at most the corresponding reflection difference, so the whole physical unitary differs from the true SWAP unitary by

    eta<=sum_i(2||Zhat_i-Z_i^*||+||Xhat_i-X_i^*||)
        <=k(4n+1)delta.                                         (18)

For the k-input Bell state with ANY augmented gauge and its coherent memory purifier, the ideal output lies wholly in the correct logical Bell subspace. Projecting the actual vector onto its orthogonal complement and using (18) bounds its probability by eta^2. Purification/linearity then gives the uniform certificate

    ell_0(g)<=k^2(4n+1)^2 delta^2<=epsilon/4                     (19)

for every augmented gauge state. This is not an unframed dimension-free diamond conversion. The bound directly controls the complete-reference failure event. It also holds for every actual original gauge with A=0.

The received complete-memory CP-domination theorem can consume (19), after the source has been expressed in the fixed U_tilde Pauli/gauge form. Appending clean A does exactly that. Future finite adaptive reuse still needs fresh privately retired frames, no retained gauge/receiver records, the SAME common causal controller, its initial input/memory contract and paid whole-schedule errors. Its comparator is the PARTICULAR exact-extraction process. No collective optimum, ideal computation, error threshold or perpetual service follows.

For one future source-memory state, the received Bell-block comparison gives excess over exact D_* at most (19). A full-CPTP oracle label additionally requires the explicit future CP dominance in section 1. Arbitrary positive coordinate biases during training do not supply it.

## 6. Resource and acceptance ledger

Calibration pays all known encoding, n-k injection bits, e_g computation, up to n extra X gates, k preparation bits, the private uniform (k+1)-setting sampler, n output readouts, output-axis sampler, n+k empirical d-by-d matrices, all finite rational fits, and every elapsed bank. Rejection samplers have explicit finite caps; their exhaustion/approximation discrepancies lie in the calibration implementation allowance. There is no extra unknown-channel call for injection and no inaccessible source inverse. Arbitrary n-qubit learned reflection synthesis can cost exponentially in n.

Service uses n coordinate ancillas, k mixed receiver qubits and the classical decoder's clean work. One invocation of controlled Zhat_i uses W_hat, a controlled P_i and W_hat^dagger. Controlled P_i is implemented by the known reversible decoder, one controlled-Z on its i-th logical output, and uncomputation; it does not require free access to l_i on unknown data. In the 3k-reflection SWAP network there are exactly 2k such Z invocations and k X invocations. A sufficient unsimplified bill is:

* 4kn controlled learned coordinate reflections, plus k controlled learned logical-X reflections;
* 8kn Hadamards for their copy/un-copy blocks, plus 4k receiver-basis Hadamards;
* 4k executions of the supplied reversible classical decoder/inverse circuit and 2k controlled-Z gates;
* initialization, storage, routing and disposal of all P,A,receiver and classical work.

These are structured unitary calls, not elementary native-gate counts; each must be synthesized and charged. Common W computations can potentially be optimized but are not assumed free. The original P and A are discarded only AFTER the entire service, and the learned receiver's discarded systems are not returned as extra controller information.

Let nu_cal bound the full retained calibration-record discrepancy, including accepted frozen matrices and stopping. Let nu_svc uniformly bound the complete one-service implementation discrepancy at its actual memory. With nu_cal+nu_svc<=epsilon/4, Good transfers to a false-certificate probability at most beta+nu_cal, and

    E[1_accept(ell_actual-ell_exact/current_oracle)]
       <=epsilon/4+beta+nu_cal+nu_svc<epsilon.                   (20)

The oracle label retains its separate dominance premise. Conditional acceptance divides bad mass by Pr(accept); no posterior record-wise guarantee is asserted. A nominal proved fast-completion record event transfers with nu_cal, not by substituting a favorable physical memory trajectory. The routine can abstain and has not received an unknown payload before acceptance.

The equally informed conventional learner receives the SAME known encoder, transversal/decoder circuit, physical port, labels, structural error model and controls, and can execute this exact method. The construction learns the unknown OUTPUT realization of a known redundant-code subsystem; it does not discover a generic new code, improve the code's intrinsic noise rate, or establish a practical advantage.
