# Exact single-transition thermal zeros do not make an all-order cold bath

This is a second scientific discriminator, derived for the actual new construction. It does not import an Astra spectral-gap theorem onto a different model.

Take nodes a={1,2}, alpha>0. Directly simplifying the product construction gives

    S_2(-w)=alpha(1-w)^2(2-w)^2/[6(w^2+2)(1+w^2)^2], w>0.

It has exact cold zeros at both positive system gaps1 and2. Consider an anharmonic three-level system E0=0,E1=1,E2=3, and bounded Hermitian coupling Q=|0><1|+|1><0|+|1><2|+|2><1|. Its norm is sqrt2 (or divide by sqrt2 if a unit contraction is desired).

A Gaussian unitary dilation with signed frequencies realizes any integrable nonnegative S_2: H_B=int_R w b_w^dagger b_w dw in its stationary vacuum, B=int_R sqrt[S_2(w)/(2pi)](b_w+b_w^dagger)dw. This vacuum is not an energy ground state. Negative-frequency bath excitations can supply system energy, as the engineered damped simulator can. Gaussian influence equivalence means this is a valid reduced-process discriminator for the coupled Lindblad realization too.

In second-order transition amplitude (fourth order in rate), 0->2 can create two bath quanta of energies -w and -(3-w). The two chronological placements have the sum of intermediate energy denominators

    A(w)=1/(1-w)+1/(w-2)=-1/[(1-w)(w-2)].

For w away from1,2 this is nonzero. The on-shell squared spectral weight, omitting only a fixed positive Fourier/rate normalization, is

    I(w)=S_2(-w) S_2[-(3-w)] |A(w)|^2
        =alpha^2 (w-1)^2(w-2)^2 /
          [36(w^2+2)(1+w^2)^2((3-w)^2+2)(1+(3-w)^2)^2].

It is positive on open sets and finite on[0,3], including the removable resonance points1,2. Thus its integral over even the restricted nonresonant window [1/4,3/4] is strictly positive. There is a genuine allowed two-quantum upward channel even though both adjacent one-quantum upward rates vanish exactly. This is not a claimed nonperturbative lifetime, and no practical heating time is inferred from it.

The equal-spaced qutrit E={0,1,2} would have cancelled the two denominators identically off resonance; I rejected that initial example and used the explicitly anharmonic spectrum above. The anharmonicity is load-bearing.

For the actual zero-temperature target S_*, both negative-frequency factors are identically zero. A fixed finite rational surrogate therefore cannot be promoted from selected cold transition rates to an exact all-order zero-temperature reservoir. The finite-horizon full-channel approximation in DERIVATION.md is unaffected: its node count and accuracy grow with the promised horizon. An infrared cutoff or a finite fixture is not an all-time theorem.

Astra's accepted scoped one-emission-notch failure (N1128/U1128-two-photon-notch-failure) is a useful independently encountered warning about complete operations. It concerns a different hard-core ladder and external radiation spectrum; its hypotheses and accepted proof are preserved, and are not asserted to prove this qutrit calculation.
