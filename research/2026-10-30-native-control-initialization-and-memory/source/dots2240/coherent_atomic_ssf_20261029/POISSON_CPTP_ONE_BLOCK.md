# A rigorous one-block ideal-SSF theorem for arbitrary local CPTP kicks

2026-10-29. This is a constructive non-Pauli theorem for a restricted noise model. It is not a continuous coherent-Hamiltonian threshold and does not establish indefinite memory without additional recovery.

## Statement and explicit model

Let a stabilizer code have distance d on N data qubits. For CSS use the full pair of syndrome sectors. Ideal local evaluations, at independent Poisson hub times, measure the needed stabilizers and apply a bounded-support Pauli correction only when it strictly decreases total syndrome weight. Each correction has support at most w; each data qubit touches at most Δ stabilizer checks. Ties and all decisions are fixed functions of the measured record. In fact the following proof needs no lower bound on the hub clock rate and applies to any locally finite schedule of these ideal instruments.

Noise consists of *exogenous, state-independent primitive Poisson events*. Each event applies an arbitrary CPTP channel supported on a declared set of at most s data qubits, together with an arbitrary retained common bath. Different events may use different unknown channels and may retain all earlier bath memory. The declared local support types have bounded incidence: at most z primitive processes touch each data site; each has rate at most ε. A rate bound can equivalently be implemented by independent dominating Poisson processes and predictable state-independent thinning. For state-dependent thinning one must retain a CP instrument at each dominating event; it is enough that the full event, including its no-action branch, is an arbitrary local CPTP channel. No hidden postselection is permitted.

Start with an exact encoded logical input, arbitrarily entangled with a reference, tensor a fixed bath state. At time τ apply one fixed minimum-weight Pauli recovery for the complete syndrome, then decode. This is a mathematical terminal decoder, not a physical operation assumed between blocks.

Construct a fixed graph G on data sites by making each stabilizer support, full hub read footprint, correction support type, and primitive noise support type a clique. Let its maximum degree be bounded independently of N, and let A_G>=2 be a constant such that the number of connected vertex sets of size m is at most N A_G^m.

Define

    C=1+wΔ,        α=1/(2Cs),        u=ε z τ.

If u<α, set

    r=A_G (e u/α)^α.

For r<1 the decoded logical channel obeys

    ||E_dec-id_L||_diamond <= 2 min{1, N r^d/(1-r)}.       (1)

The statement is uniform over the unknown CPTP kick channels and retained bath dimension, subject to existence of the channels. Their individual channel norms are one; their strength is charged through primitive rate ε, not a small Hamiltonian norm.

## Proof, first part: a branch-uniform deterministic certificate

Fix only the primitive kick times/supports and the hub evaluation schedule. Expand each local system-bath Kraus operator in data Pauli operators and bath coefficients. This is an algebraic expansion, not a stochastic Pauli replacement. A term of the resulting ket expansion follows a definite Pauli history and a compatible ideal syndrome record. Every accepted correction decreases that history's total syndrome weight by at least one.

Let U be the union of the actual nontrivial Pauli insertion and correction supports for one such history. Let E be its final Pauli error. Choose R to be the fixed minimum-weight Pauli representative of E's complete syndrome, and let K be a connected component of U union supp(R) in G. All actual insertion and correction supports belong to single components because those supports are cliques.

Replay only the events inside K. Every relevant check has the same syndrome contribution: a check cannot meet erroneous sites in two different components, because its support is a clique. Thus correction syndrome decreases inside K agree with the actual history. With the initial syndrome zero, the total decrease D_K is at most the sum of noise-induced syndrome increases. If Q_K is the sum of Pauli insertion support sizes in K, multiplicities included, then

    D_K <= Δ Q_K,
    |U intersect K| <= Q_K+w D_K <= C Q_K.

No small-error confinement estimate or SSF packing lemma is used here.

Syndrome equality of E and R holds componentwise. Replacing R inside K by E inside K preserves the total syndrome. Minimum weight therefore implies

    |supp(R) intersect K| <= |supp(E) intersect K| <= |U intersect K|,
    |K| <= 2 C Q_K.                                    (2)

If every K has size strictly less than d, the restriction of E R to each K has zero syndrome and support smaller than code distance; it is therefore a stabilizer up to phase. The same fixed terminal recovery consequently restores the logical identity on this Pauli branch.

If any branch is not restored, some K has size m>=d. Let N_f(W) count *primitive kick events whose declared support touches W*, whether or not their Pauli component is nontrivial. Then

    Q_K <= s N_f(K),     N_f(K)>=α |K|.                  (3)

Thus failure of ANY Pauli branch implies the following event involving ONLY the primitive location record:

    Bad = {there exists connected W subset G,
           |W|>=d and N_f(W)>=α|W|}.                    (4)

The quantifier over all W absorbs every possible Pauli choice, measurement branch, bath Kraus label, correction history, and recovery support. There is no global 4^(number of faults) union bound. Using full declared kick supports merely makes the envelope conservative.

## Proof, second part: a genuinely positive probability calculation

For fixed W of size m, the dominating count N_f(W) is Poisson with mean at most u m. Standard exponential Markov optimization with exp(t)=α/u gives

    P[N_f(W)>=αm]
       <= exp[-αm log(α/u)+αm-u m]
       <= (e u/α)^(αm).

This is a statement about actual exogenous classical event records, not quantum error amplitudes. The event records are independent of the logical input. Connected-animal counting and a union bound now give

    P[Bad] <= N sum_{m=d}^N r^m <= N r^d/(1-r).         (5)

On a fixed primitive record outside Bad, EVERY compatible Pauli branch is corrected by the same recovery. The common correctable-span argument therefore shows that the complete channel for this record, after summing actual syndrome/Kraus outcomes, acts as identity on the logical subsystem and some channel on the bath/record subsystem. Since all kicks and ideal evaluations are CPTP, this record-conditioned channel is trace preserving. It remains so even though the bath is shared and retains earlier correlations.

Averaging over primitive records gives

    E_dec=(1-p_bad) id_L+p_bad E_bad

for a CPTP logical channel E_bad (the hub schedule may be averaged too). Hence the diamond distance is at most 2p_bad, proving (1).

## Scope and why this is not the desired full coherent memory theorem

* This genuinely permits coherent Kraus superpositions, arbitrary local non-Pauli CPTP kicks, and retained common-bath memory. No Pauli twirl is inserted.
* The class is a Poisson *channel-kick* model. Its generator has the form sum_a ε_a(Φ_a-id), possibly with bath memory between events. Arbitrary continuous local Hamiltonian drift is not of this form at bounded rate. Neither is every Lindblad generator automatically a finite-rate CPTP-kick generator. The theorem must not be relabeled as arbitrary bounded Hamiltonian/HP noise.
* The elementary proof is for one fixed observation block, from the exact codespace. Its small parameter is ετ. It is not uniform for τ growing indefinitely at fixed ε.
* The proof does not exploit SSF contraction; it would work for any bounded-support syndrome-decreasing feedback. This makes it robust to the separate audit of the stronger asynchronous contraction theorem, but also explains why it does not establish a stationary finite-noise residual law.
* One could physically apply the ideal global minimum-weight recovery at each boundary and then iterate, even with a retained bath. That is a different, stronger controller architecture and is NOT assumed here.
* Without such boundary recovery, a safe record supplies a *space of possible coherent residual errors*, not a single observed Pauli residual or a cheaply bounded union-support envelope. Taking the union of residual supports over all branches can be much larger than any individual residual. The invariant quantum error-space contract needed for autonomous iteration remains open.
* For general local CPTP channels on a common retained bath, an initial arbitrary system-bath correlation is handled only through a specified preparation channel. The claimed logical diamond channel begins from the encoded logical subsystem tensor a fixed bath state. No bath reset is needed during the block.

## Relation to the original witness proof

Equation (2) is the unconditional finite-work / component enlargement argument in Section 6 of ASYNCHRONOUS_WINDOW_WITNESS.md, specialized to zero initial error and proved above. It needs code distance and bounded support, not the FGL small-error cutoff. This narrowly isolates the portion which does extend to arbitrary quantum channels on classically sampled locations. The more ambitious multiwindow contraction and long-time residual induction are deliberately not imported.
