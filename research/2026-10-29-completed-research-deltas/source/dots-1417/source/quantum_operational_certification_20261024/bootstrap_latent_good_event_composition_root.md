# Latent-good-event composition for a protected calibration bootstrap

27 October 2026. Root derivation, pending independent receiving. This is a compositional lemma, not a completed hardware architecture or a historical novelty claim.

## Contract

An exact causal receiver frame has a common unknown output support of dimension k covering **all** warm, programme, carrier and payload calls. Its full reference/interactive identity gives one mathematical latent frame U across the entire experiment. The source is stationary and independently reset. Warm calibration finishes before programme acquisition and produces classical h. Freeze a seed encoder and decoder from h, but continue updating the quantum frame on every source call.

Let G be a measurable event of (U,h) such that Pr(G^c)<=beta. Conditional on every (U,h) in G, the seed channel after independent private Pauli framing has iid Pauli error probability at most p0. This statement is a consequence of a proved common-frame/source model and a confidence argument; marginal validation alone never establishes independence of hardware faults. G need not be a physically readable flag.

Programme data preparations are fixed independently of h; only the reference-transfer seed is h-dependent. Let a concatenated code of L levels correct the seed transfers with conditional logical Pauli error p_L, uniformly on G. Each of n programme samples consists of one physical data-source call followed by three such reference transfers through the same source. The full encoder family, hence also the seed-codeword carriers, is contained in the supplied common support. Additional imperfect operations are assumed to have a **whole interactive** implementation discrepancy at most nu in unhalved norm.

## Lemma 1: unconditional complete comparison

Compare the actual ideal-hardware bootstrap with a mathematical protocol replacing each of the 3n decoded reference-transfer channels by the identity, retaining the classical warm record h. The persistent frame quantum memory and its coherent paths stay private and are traced from the compared output; they are not an exported warm history. This comparison is not an implemented bypass. All actual carrier calls remain charged. The latent-frame representation permits tracing ignored carrier outputs in the comparison, or supplying dummy calls to preserve the declared horizon.

For fixed good (U,h), every encoded transfer is a Pauli channel and its unhalved diamond distance to identity is 2p_L. A causal hybrid, valid for arbitrary entangled inputs, intervening adaptive known operations, stored programme data and all external references, gives distance at most 6n p_L. Conditional bad histories contribute at most 2. Integrating the **same** warm measure on the two sides yields

    || Actual - Ideal-reference || <= 2 beta + 6n p_L + nu.

No physical measurement of U or of G is used. This is an unconditional bound. Conditioning on a rare accept transcript does not preserve beta or nu automatically. A separately stated accepted-normalized result must pay its actual acceptance denominator. In a no-abort statement, an unsuccessful warm stage uses a specified fixed seed/fallback and still outputs a channel; its potentially poor performance is covered by beta only if the warm success promise proves that mass bound.

The event G concerns the WARM stage only. In the ideal-reference experiment, conditional on U,h, the subsequent n samples are iid exact Gamma_U, independent of h except through U. The full-rank noisy physical programme bank is never passed to an exact low-rank theorem. The exact low-rank learner analyzes only the ideal bank; complete comparison then transfers its entire output process.

## Lemma 2: same-frame deployment needs no second learning factor

Suppose the ideal Gamma learner outputs an explicitly executable pair (x,D) in the persistent frame and, uniformly in U and any warm posterior, satisfies

    E(1-f) <= (1+gamma)(1-a) + e,
    f = F_e(D E_(x,U)),
    a = max_(x,D) F_e(D E_(x,U)).

The maximum a is independent of U. Since x,D are feasible, f<=a pointwise. The final M payloads are encoded by the selected x and recovered with the same D, in the same retained quantum frame. Fresh independent private pre-source Paulis, known matching output undo, and discarded keys produce

    Delta_M = 2 [1 - E f^M].

In particular, neither an independently reset frame nor a tensor power of the averaged marginal appears. For a>=f>=0,

    a^M-f^M <= M a^(M-1)(a-f),
    M a^(M-1)(1-a) <= 1-a^M.

Therefore

    Delta_M <= (1+gamma) 2(1-a^M) + 2 M e.

The same bound holds for causal use of the recovered ports because their exact ideal-reference law is an input-independent mixture of Pauli error sequences. Adding Lemma 1 once gives

    Delta_actual,M <= (1+gamma) 2(1-a^M)
                      + 2 M e + 2 beta + 6n p_L + nu.

There is NO extra factor M on the last three terms: they already compare complete protocols. Conversely, n must be chosen for local target e of order epsilon/M. The guarantee does not permit arbitrary cross-use encoder/rate-changing comparators; the comparator family remains one chosen supplied encoder per payload with unrestricted collective decoding under the same private-frame interface.

A possible allocation is e<=epsilon/(8M), beta<=epsilon/8, p_L<=epsilon/(24n), nu<=epsilon/4. These four contributions sum to epsilon. Exact constants in an upstream finite learner may be more conservative.

## Concatenation size and qualification

For the five-qubit distance-three stabilizer code under the stated iid Pauli law,

    p_(l+1) <= 10 p_l^2,
    p_L <= (10 p0)^(2^L)/10.

If 0<10p0<1, choosing

    2^L >= log(12n/(5 epsilon)) / log(1/(10p0))

is sufficient for p_L<=epsilon/(24n) whenever the right side is positive; take L>=0 and round up. Thus each reference uses 5^L carrier calls. For fixed p0 bounded below threshold, this is O(log(n/epsilon)^(log_2 5)). Total calls are bounded by

    H = N_warm + n (1 + 3*5^L) + M.

The expression is a cap unless the physical protocol explicitly pads early fallbacks. It includes only source calls: local code synthesis, trusted private frames, syndrome extraction, frame quantum memory over H steps, preparation and relative phase control, and all known decoder operations must be separately charged. No claim that these components self-correct their own arbitrary correlated faults follows.

The seed-success promise is substantive. If all supplied encoders erase quantum information, the method cannot manufacture a quantum link. A protocol with no suitable seed may correctly reject, but rejection is not successful preservation under broad arbitrary noise.
