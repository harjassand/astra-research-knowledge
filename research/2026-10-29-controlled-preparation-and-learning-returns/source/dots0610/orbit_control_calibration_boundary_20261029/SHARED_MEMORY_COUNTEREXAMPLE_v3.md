# Fresh endpoint tests still fail under a shared source-control memory

2026-10-29. Exact counterexample. This does not violate the isolated-control
hypotheses of the received orbit theorem; it shows why those hypotheses cannot
be discarded or inferred from the proposed cheap calibration data.

Let V encode a logical qubit into the correct four-qubit singlet sector P.
Let F be one shared bath bit accessible to encoder, source and decoder. All
component maps below are time independent. No operation receives the private
matching, permutation, logical pad or role key as a classical input.

1. Encoder: apply V to the logical qubit and reset F to |0>.
2. Source: identity on ALL physical data, and X on F.
3. Decoder: apply the exact inverse of V on P, then apply logical Z iff F=1,
   and reset F to |0>. Complete the decoder arbitrarily and trace preservingly
   off P, for example by maximally mixed logical replacement.

The acquired observables are all perfect, regardless of prior history:
- Encoder membership: its physical output is exactly in P.
- Encoder/decoder round trip with the source bypassed: F stays0, so the logical
  channel is exactly identity, including on reference-entangled inputs.
- Matching-storage test: the source is exactly identity on physical data, so
  every prepared matching singlet passes. Only F changes, which that test does
  not read; the next encoder resets it anyway.
- Physical permutations and their inverses can be perfect and private. On a
  service, their inverse cancels them because the physical source is identity.

But every actual service is logical Z: E setsF=0, source setsF=1, D appliesZ.
Fresh interleaving of all three cheaper calibration modes never detects it.
Adding logical Pauli pre/post pads does not help: conjugation changes Z only
by a sign, hence the logical channel is still Ad_Z with Bell loss and
half-diamond error both1.

The source's full joint good branch is exactly id_P tensor Ad_XF. It is the
subsequent decoder's coupling to F that turns that otherwise perfect branch
into a logical error. Thus knowing D E=id does not permit the algebraic
substitution D (id_P tensor B) E=id_logical tensor B when E,D share B's memory.
This identifies the precise invalid step in an unrestricted-memory extension.

The example does not assert that such an F exists in a particular device.
It establishes an observational ambiguity when shared endpoint/source memory
has not been excluded. It does not use a gratuitous classical key leak; the
bath responds to the actual component sequence. If the intended private
control boundary already forbids all such shared-memory coupling, then the
example is excluded by that explicit physical assumption, not by calibration.

A full-path logical two-basis test detects the channel: Z-basis inputs pass,
X-basis inputs all fail, so q_full=1/2. This is an exact and equally informed
conventional alternative. It needs no microscopic reconstruction of F.
