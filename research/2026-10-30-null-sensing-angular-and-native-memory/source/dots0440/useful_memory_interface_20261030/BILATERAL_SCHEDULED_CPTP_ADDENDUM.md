# Scheduled bilateral buffer: retained-bath CPTP addendum
2026-10-30. Frozen ordinary proof filling the common-span step of BILATERAL_BELL_BUFFER.md. It does not claim a native asynchronous LOCC compiler.

## Verdict

The scheduled circuit claim can be made rigorous without Pauli twirling, independent noise, instantaneous global decoding, or a persistent syndrome baseline. Use genuinely measured classical gates, bounded-depth/fanout local classical processing, a declared finite-latency classical channel, and measured Pauli control. On every actual fault record whose count is below the deterministic per-round threshold, ALL coherent Pauli coefficient histories end in one common relative-correctable Bell-target span. Exact final bilateral syndromes plus relative recovery factor the logical Bell state from the entire retained bath. A uniform bad-record bound delta gives output trace-norm error at most 2 delta.

## 1. Assumptions actually used

1. A CSS [[n,k,d]] family with d>=d0 n and the deterministic single-shot contraction used in the parent file:

       |e+f(H e+D)|_R <= alpha |e|_R+beta |D|,
       A|e|_R+B|D|<=C n,       alpha<1.                 (1)

   Here reduction is modulo STABILIZERS, not minimization over every same-syndrome error. Use both CSS sectors, with constants enlarged so their combined relative Pauli representative has weight below d/2.
2. A fixed number of decoder iterations, implemented by a finite-depth circuit of bounded-fanin, bounded-fanout, bounded-locality classical gates. All constants can be extremely large but are independent of n. Local CSS extraction is likewise a bounded-depth bounded-incidence Clifford circuit, with fresh ancillas and measured readout.
3. A physical round of duration tau independent of n, including the DECLARED classical-message propagation time, idle intervals, local computation, and applied Pauli mask. An O(n)-wire parallel classical channel is a resource, not a conclusion. If tau grows, its fault count must be recalculated.
4. Actual fault records F specify local fault locations/times. At each charged location the fault is an arbitrary CPTP interaction on a bounded set of system wires and an arbitrary retained bath. The bath can correlate faults across rounds and adapt to all past records. No uncharged bath/system interaction is allowed. The source's initial error support has the same sort of charged record.
5. The fault record is an honest positive instrument. Its bad-event mass is bounded uniformly for arbitrary initial gauge states and references. Exogenous local Poisson faults or a suitable circuit local-stochastic location law are examples. A small diamond-norm perturbation with no such record decomposition is not asserted to satisfy this theorem.

The primary deterministic result is Gu–Tang–Caha, arXiv:2306.12470, Theorem 4.20: alpha decreases geometrically with the fixed iteration count, beta is constant, and the admissible radius is linear for this family. Theorems 3.5 and Corollary 3.6 give the repeated-round induction and correlated-error union bound. The noisy-classical/CPTP extension below is our derivation, not a quoted theorem of that source.

## 2. Explicit nominal classical CPTP gates

For each finite local Boolean map f, implement its classical gate as

       Gamma_f(rho)=sum_x <x|rho|x> |f(x)><f(x)|.       (2)

Inputs/outputs may be tuples of a fixed number of local wires, and a tuple can retain/copy the input if needed. All unused scratch is reset by a measure-and-prepare channel. The Stinespring dilation retains a copy of x in an environment register. Hence the definition remains valid when input wires are entangled with the bath. This gate does not preserve or communicate quantum coherence in a purported classical wire.

A classical send channel measures the sender's bit/tuple and prepares the same computational-basis string at the receiving port; losses or corruptions are charged local classical faults. A measured controlled Pauli on data is

       Lambda(rho_CD)=sum_m P_m <m|rho_CD|m> P_m†.      (3)

Each correction-bit gate controls only its declared local data qubit(s). These are actual CPTP maps, not instructions to assume an ideal external classical computer. Errors in these maps are charged like errors in any other gate.

Equations (2)-(3), local quantum operations, and classical send channels are LOCC across the two laboratories. A coherent CNOT between distant quantum registers is not a classical send channel. If fault interactions use an entangled bath shared across the laboratories, the robustness theorem below still applies, but the resulting faulty physical operation need not be LOCC as a resource-theory statement. Strict LOCC resource accounting can instead use local quantum baths and arbitrary shared classical noise; this does not weaken the deterministic support proof.

## 3. Common-record support lemma

Fix an actual fault record F_j in one round, with K_j charged locations. Purify all baths and all ideal measurement/classical channels. Expand every local fault isometry in a Pauli operator basis on its bounded system support, retaining operator-valued coefficients on the bath. This is a linear expansion, not a probabilistic Pauli model.

Fix one term of the resulting expansion and one fine measurement history. All of the following then hold:

### Extraction

The nominal extraction circuit is Clifford. Commute the Pauli faults through its fixed depth. Its measurement Kraus operator equals an ideal local stabilizer-measurement Kraus operator, with a bounded set of output-bit flips and a bounded-support data Pauli before/after the ideal snapshot. Products of faults enlarge these sets by a union, not an uncontrolled light cone. Full local projectors preserve the coherent common-syndrome span W described in BILATERAL_BELL_ALGEBRA_AUDIT.md.

Thus the two readouts differ by

       H(e+a_j)+D_j,

for some data mask a_j and readout mask D_j supported in COMMON record-dependent envelopes of size at most c_a K_j and c_D K_j. An equivalent placement with a_j=0 and all data errors after the snapshot is also valid. The envelopes depend on physical locations and fixed circuit light cones, not on a Pauli coefficient or on the unknown common syndrome.

### Classical processing and transmission

A nominal classical wire is in a computational-basis state in each Pauli coefficient history. A Pauli X changes its bit, Z changes only a coefficient phase, and (2) maps each basis input to the prescribed basis output while recording the input. Therefore each surviving coefficient term follows an ordinary deterministic Boolean history. Arbitrary coherent faults do not evade this statement: they were expanded into these histories while their coefficients remain in the bath.

Compare this history with the fault-free local decoder circuit supplied the SAME noisy syndrome input. A changed intermediate wire can affect only its bounded forward light cone. Since depth and fanout are fixed, the eventual correction-bit difference g_j is contained in the union of O(K_j) bounded cones. This remains true for nonlinear Boolean gates, arbitrary input strings, and faults adapted to the common syndrome. No probability is assigned to the comparison histories.

### Data during and after computation

Further local data faults and faulty Pauli-control gates contribute a post-snapshot data mask b_j of common support at most c_b K_j. Moving a Pauli past a Pauli correction creates only a phase, which is absorbed into the bath/gauge coefficient. Idling faults during the declared communication delay are included here.

Consequently EVERY coefficient history on F_j satisfies, with fixed constants,

       |a_j|<=c_a K_j, |D_j|<=c_D K_j,
       |b_j|+|g_j|<=c_b K_j.                            (4)

The output relative error is e+a_j+f(H(e+a_j)+D_j)+b_j+g_j, up to common Pauli/gauge changes. Equation (4) is uniform across all histories. Fresh reset of round scratch prevents an uncharged corrupted classical state from persisting into later rounds.

## 4. Deterministic safe-record induction

Let r_j be stabilizer-reduced relative Pauli weight at the beginning of round j. Equations (1) and (4) give, for EVERY compatible coefficient history,

       r_(j+1)<=alpha(r_j+c_a K_j)+beta c_D K_j+c_b K_j
                =alpha r_j+C_K K_j.                    (5)

The recurrence can be applied to a minimum stabilizer representative because stabilizers leave the syndrome and the nominal decoder output unchanged. Its action on a signed sector can introduce a syndrome-dependent phase; that phase goes into the gauge/bath coefficient and has no effect on (5).

Choose f,z0>0 and set z=max{z0,C_K f/(1-alpha)}. Assume

       r_0<=z0 n; K_j<=f n for all j,
       A(z+c_a f)+B c_D f<C,     2 z n<d.              (6)

Adjust the final strict inequality for the sum of the two CSS-sector bounds, if (1) is stated sectorwise. Induction gives r_j<=z n for every coefficient history and every round. This proof requires no statistical independence between rounds or between coefficient histories. It is a support statement on ONE common safe actual record.

There is no need to assume the physical Pauli history itself has small accumulated weight. Only its representative modulo stabilizers is small. The accumulated stabilizer factors remain harmless gauge phases.

## 5. Exact common-span factorization after final relative recovery

Let B=range W, W|s>=Omega_s. Define the final relative-correctable family

       E_z={E: some representative E_tilde modulo S has
                  weight(E_tilde)<=z n},   2 z n<d.

If E,E' in E_z have the same relative syndrome, choose their small representatives. Their product has zero syndrome and weight at most 2 z n<d, so it is a stabilizer. Hence E and E' differ by a stabilizer, up to phase. This statement is independent of the unknown common syndrome.

Choose any deterministic exact recovery R_delta for each syndrome delta appearing in E_z. For example use a minimum-physical-weight syndrome representative. Since an E_z representative exists for these deltas, it has weight at most z n. For every E in E_z with syndrome delta,

       R_delta E is a stabilizer, up to phase.          (7)

Now apply the following FINAL ideal LOCC decoder, solely to define the protected encoded output:

- measure full local syndromes a,b;
- apply R_(a+b) on Bob;
- apply a matched full signed-sector decoder on both sides;
- discard gauge/syndrome registers.

For each term (I tensor E) W|gamma>, the final syndrome measurements select the component with a=s and b=s+delta. Equation (7) acts there as a scalar chi_E(s). The scalar can depend on s and on the coefficient history, but it multiplies only the gauge/bath amplitude. Equation (3) of the algebra audit then gives

       final_decoder [(I tensor E) W|gamma>]
           = |Phi_k> tensor |xi_(E,gamma)>.             (8)

Keep all final syndrome records and every environment register in xi. Equation (8) holds termwise with the SAME Phi_k. Therefore it holds for arbitrary coherent sums of Pauli coefficient histories, common-syndrome superpositions, and retained-bath states. It also holds if different histories give the same final syndrome, precisely because their difference is a stabilizer rather than a logical Pauli.

For each safe actual fault record F, the decoded output CP map consequently has the form

       rho_GR -> |Phi_k><Phi_k| tensor T_F(rho_GR),     (9)

where T_F is a CP, possibly trace-decreasing map to the remaining gauge/bath/reference registers. This is an exact factorization, not merely a fidelity estimate per sampled Pauli error. Input raw physical Bell pairs correspond to W|+>^r, and bounded-source-fault histories give the allowed initial relative-error span, so no encoded initializer is inserted.

## 6. Positive-record failure bound

Suppose the combined source/buffer positive instrument obeys, uniformly over allowed gauge/reference inputs,

       || instrument{Z_source>z0 n or some K_j>f n} ||_diamond
          <= delta_L
          <= eta_source+C(L+1) exp(-c n).              (10)

Here Z_source is a COMMON source-record support majorant bounding every initial Pauli coefficient history; it is not the unobserved weight of a selected Pauli term. For an exogenous fault-location process the first bound is simply a uniform probability bound. In the general instrument formulation positivity permits an unconditional union bound; no restart conditioned on a rare measurement outcome is used.

After discarding gauge and bath, (9) says the good part has output Phi_k tensor rho_R^good. The bad part has reference marginal rho_R^bad. Trace preservation and lack of operations on R imply rho_R^good+rho_R^bad=rho_R. Therefore

       ||rho_LR^out-|Phi_k><Phi_k| tensor rho_R||_1
            <=2 Tr(rho_bad)<=2 delta_L.               (11)

This also establishes a diamond-distance bound of 2 delta_L from the GAUGE-input channel (encoded by W) to the constant logical-Bell-output channel, including arbitrary gauge references, when (10) is uniform. It is not the arbitrary-logical-input identity-channel theorem for a quantum memory.

Actual noisy final decoding or bare extraction has not been smuggled into (11). The final map is the declared mathematical encoded-output decoder. A finite noisy use stage can instead be appended and charged, if separately analyzed. The remaining autonomy problem is the physical asynchronous LOCC service/message compiler, not retained-bath coherence in this scheduled circuit proof.

## 7. Audit status

This addendum closes the parent's 'plausible common-span' statement under the explicit assumptions above. It establishes an ordinary scheduled noisy-circuit Bell buffer from physical Bell sources, with faulty finite-depth classical processing and arbitrary local CPTP faults on a common positive fault record. The active single-shot comparison is constructive and strong. It does not promote this circuit to the existing reviewed autonomous generator, and it does not promise unprotected bare-port accuracy.
