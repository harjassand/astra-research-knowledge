# Independent midpoint sharpening of the future-memory floor

28 October 2026. This supplements the weaker, already valid floor in `approximate_onsite_memory_bound_independent_20261028.md`; it is not by itself a receiving receipt.

Take unknown signs s_i and a controlled logical rotation Rz(2s_i theta): its gauge-0 branch is identity, its gauge-1 branch is Rz(2s_i theta). Choose the EXISTENTIAL, source-specific fixed on-site witness frame Rz(s_i theta). Its X generator lies halfway between the two exact conditional X generators. Both branch differences have operator norm

    tau=2 sin(theta/2).

The Z generator is exact. Thus all source completions satisfy the SAME supplied approximation bound tau, although their hidden witness axes differ. The approximation promise never required those unknown witnesses to coincide across statistically indistinguishable sources.

Fresh gauge preparation |0...0> during every prescribed calibration call makes the complete training channel identical across sign vectors, including for arbitrary coherent/adaptive probes and retained calibration ancillas. Fresh gauge |1...1> at the specified future boundary is the same accessible gauge output for every sign, so a frozen full-CPTP decoder on ALL logical/gauge outputs reduces to one arbitrary logical CPTP decoder with sign-independent ancillas.

The sign-average future logical channel is product Z dephasing with

    p=sin²(theta)=tau²(1-tau²/4).

For tau<=1/4 we have p<1/2, so identity is its most likely Pauli branch. Every frozen full-CPTP decoder therefore has at least one source completion with expected Bell loss at least

    1-[1-tau²(1-tau²/4)]^q.                            (M1)

The informed source oracle has zero loss. This improves the small-q-tau² coefficient from 1/4 to 1 while retaining the same Theta(min(1,q tau²)) order and all original scope restrictions. It does not require a common supplied witness frame across completions, and no such witness is acquired during training.

The separate exact-rational check uses stereographic parameters c=(1-r²)/(1+r²), s=2r/(1+r²), so Rz(theta)=c I-i s Z and Rz(2theta)=(c²-s²)I-2i c s Z have rational complex entries. It verifies both squared generator differences equal tau² I, the midpoint probability formula, the largest-Pauli-probability claim and finite-q normalization exactly. No source/RNG draws or sampled experiment occurs.
