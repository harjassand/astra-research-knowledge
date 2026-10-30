# A preparation-to-memory composition contract: pay an initial seed slab
2026-10-30. Ordinary extension of the reviewed positive-record backward witness. This identifies a sufficient initializer; it does not assert that a particular physical factory supplies it.

## Required preparation output
At native-memory start, controllers have the specified clean A0/workspace0/free-lock initialization and zero marks. In that frame, preparation outputs the target encoded state with a Pauli residual E_0 and possibly a retained environment. The E_0 label can be a genuine classical preparation-fault label, or more generally a positive physical record with a common bounded-support error span.

For a Pauli-mixture formulation require, for every fixed DATA set S,

    Pr[S subset supp(E_0)] <= p_init^{|S|}.           (LS0)

Correlations between these initial errors and a retained bath are allowed if the subsequent physical fault/service moment bounds hold uniformly on the allowed initialized joint states. No conditional independence of future storage faults is assumed. The target may be a known encoded stabilizer/Bell state; an arbitrary-input diamond claim requires the preparation residual/environment contract to be logical-input independent.

For the more general coherent-span formulation require an actual positive-record support majorant Q_0(W) common to every Pauli coefficient branch, with fixed-set exponential moments small at a fixed theta. A mere final recovered fidelity is not such a contract.

## Initial moment from local stochasticity
For z>=1, expand the product generating function. Equation (LS0) gives

    E z^{|E_0 intersect W|}
      = sum_{S subset W} (z-1)^{|S|} Pr[S subset E_0]
      <= [1+p_init(z-1)]^{|W|}.                     (1)

No site independence is used. In particular, for any fixed density a>0,

    Pr[|E_0 intersect W|>=a|W|]
      <= [ inf_{z>=1} z^{-a}(1+p_init(z-1)) ]^{|W|}.

The bracket tends to zero as p_init tends to zero; the coarse bound `(e p_init/a)^a` suffices when p_init<a. Bounded-support factory faults only change the multiplicity/geometric constants if a common majorant is supplied instead of literal one-site residual errors.

## Deterministic insertion
Append at global initialization an analysis-only, zero-service slab containing the initial residual as one-site Pauli bad events. It starts from the exact target encoded state. The original deterministic D0 inequality is unconditional and therefore applies to this slab; no physical ideal recovery is inserted.

If the usual backward certificate reaches the initialization boundary, it cannot now declare the incoming error empty. Instead it continues through this slab. Every cutoff-bad component must contain initial error support at fixed density, using D0 and the same virtual minimum-syndrome endpoint reduction as in all other blocks. Equation (1) pays for this terminal fresh seed event. There is no D1/service assumption in the seed slab and no fictitious clock interval.

Equivalently, if a minimum-syndrome representative R_0 is used at the first native boundary, each enlarged component of E_0 union R_0 has |R_0 intersect K|<=|E_0 intersect K| by componentwise minimality, so |K|<=2|E_0 intersect K|. This supplies the same dense-initial-error certificate without assuming that R_0 itself has an LS distribution.

Replace the native terminal-event base by the maximum of its existing value and the initial-density-tail base, enlarge fixed root constants, and count the same bounded-degree connected spacetime animals. For sufficiently small fixed p_init and native noise, the conclusion retains

    memory error <= C N(1+t) exp(-cN),

with changed constants and the declared final decoder. The initialized error model, rather than a recovered preparation score, is what permits composition.

## Subnormalized successful-factory variant
A factory may supply an event G with failure mass eta and only a good-event bound Pr[S subset E_0, G]<=A q^{|S|}. Keep this as a subnormalized positive ensemble rather than conditioning. For nonempty S absorb a fixed A>=1 into q_init=Aq; for the empty set the good mass is at most one. Then

    E[1_G z^{|E_0 intersect W|}] <= [1+q_init(z-1)]^{|W|}.

The same initial certificate applies, and the overall channel error adds at most 2 eta once. No division by a rare event probability or assumption of independent preparation and storage is needed. When combining dependent LS boundary/handoff errors, a conservative positive-power enlargement of the LS parameter is required; do not silently add their rates as if independent.

## Operational obligations not solved by the lemma
- Controllers must really meet the specified initial contract; an unmodeled noisy reset of all controllers is not zero initial marks.
- The Pauli correction/Pauli-frame convention used by the factory must be physically reconciled with the native zero-syndrome decoder. An arbitrary large unknown syndrome byproduct is not LS merely because its corresponding decoded logical state is correct.
- Quantum storage during classical decoding and the reliability/latency of the classical decoder must be charged.
- Extending an LS Pauli factory proof to arbitrary common-bath CPTP records needs a coefficientwise common-span argument, not a Pauli twirl declaration.

This is a concrete proof target: a bounded-resource factory output satisfying (LS0), or its positive-record span analogue, with the native initialization completed. Once that is supplied, the long-time storage proof no longer needs a perfectly encoded DATA assumption.
