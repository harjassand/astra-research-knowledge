# Shortcuts excluded by the live pulse construction

1. **Positive common-span projection is not exact logical preservation.** Take an already encoded logical qubit with no syndrome or controller defect. Let its actual channel be (1-zeta)Id+zeta Ad_XL. The common correctable-span projector is identity on both outputs. Its leakage is zero, yet the logical channel is not Id and its diamond distance from Id is 2zeta. A small bad logical term survives projection. The explicit CP logical-factor repair in the revised lemma retains and pays this error; it does not assert projection removed it.

2. **Mean energy is not exponential warm control.** A positive spectral mixture puts probability 1/N on E=N and the rest on E=0. Its mean energy is 1, but log Tr exp(sE)rho=sN-log N+o(1). The numerical fixture uses N=1000,s=.1 and obtains log moment 93.09. The actual lemma uses hard spectral support followed by PFP compression.

3. **Fixed expansion without cooldown is not arbitrary repetition.** If a gate bound merely says r_next<=2r and introduces fresh pN support, its iteration can grow as 2^L(r_0+pN), exhausting a fixed bank basin after O(log(1/p)) commands. The actual accepted moment ODE returns to the fixed e,b cuts after each paid cooldown; this, not transversality alone, closes the cycle.

4. **Global BN-radius is wrong for bank register.** Tensoring B distance-d bank codes does not multiply distance: a logical operator on one bank still has weight d=Theta(N). Thus a global radius proportional BN could include an uncorrectable complete bank when B is large. The pulse and cooling construction must impose per-bank/per-matching-group cuts and pay the number of bank-time groups.

5. **No support-union over coherent masks.** A superposition of sparse errors at every possible location need not have a single sparse union. Error correction uses the linear span of individually sparse coefficients. Taking the set union would falsely convert a correctable coherent error to an extensive defect; selecting a classical realized mask would falsely discard coherence.
