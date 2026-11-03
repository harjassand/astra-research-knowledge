# Independent gauge-side audit: what passes and what remains conditional

2026-11-03. This is separate from the completed ungauged proof package.

## Local rescaled moment algebra passes

For compact links with [E_l,U_p]=s_pl U_p,

 [E_l^2,U_p]=U_p(2s_pl E_l+1).

Thus, for e_l=gE_l and B_p=(U_p-1)/g, electric evolution gives

 i[H,B_p]=(i/a)U_p sum_(l in p)(s_pl e_l+g/2).

The plaquette magnetic force on e_l is bounded using |sin F_p|<=|U_p-1|. A matter derivative bound ||partial_l h||<=J_l contributes gJ_l. Therefore the stated Dini inequalities and the Gronwall bound are valid on finite-energy domains, first on a core and then by approximation. There is no finite electric-bandwidth assumption.

Uniformity in volume is conditional on an actual uniform J_max and incidence bound. The current finite-volume auxiliary cutoff and interaction range grow with volume, so their J_max can also grow. It must be inserted, not silently replaced by a volume-independent microscopic constant.

## Finite-volume smooth-detector criterion passes

The global-tree, finite-charge construction in `FINITE_TIME_QUANTUM_LINK_GATE.md` has a legitimate finite-volume derivative bound: after physical finite momentum cutoff, all onsite charges are bounded integer matrices, and conjugation by the local tree paths is smooth in the link angles.

The static norm perturbation, rank-one Riesz projector, smooth cutoff detector F=chi P, and electric commutator estimate are consistent. The detector is zero outside its curvature chart and has bounded derivatives there; it is not an added hard wall. Since only electric energy fails to commute with it, the displayed Duhamel estimate follows from the conserved electric quadratic-form bound. The probabilities of leaving the admissible set or exciting the instantaneous matter ground sector are correctly bounded by the detector norm error.

The explicit tree-gauge wavepacket can be normalized by Haar factorization. Its globally neutral matter ray makes the residual root gauge choice harmless. The kinetic estimate charges the cycle matrix and tree charge generators, and the magnetic estimate uses at most four small non-tree angles per plaquette. Gauge-vacuum energy is not incorrectly discarded. These statements concern the fully gapped finite-volume matter block, not a local mirror projector in the exposed chiral device.

## The new local magnetic-fast-gap extension needs an additional premise

`LOCAL_MAGNETIC_FAST_GAP_AND_BERRY_TERMS.md` contains a mathematically valid partition-of-unity inference IF its local Schur comparison is established:

 ||[h(A,phi)-G_patch h0(phi_patch)G_patch dagger]v||
   <=C_mag epsilon ell ||v||.

However, that estimate is not automatic for the ACTUAL tree-gauged discontinuous rotor coefficients. Local gauge conjugation translates rotor angles inside cochain floors. Arbitrarily small residual links can cross a rounding wall and change a controlled mass or matching by order one. Different overlapping stencil trees need not correspond to one common transformed rotor configuration. A uniform gap for every globally consistent phi does not itself imply norm-Lipschitz control of those inconsistent shifted stencil data.

After physical momentum cutoff, bounded charge matrices restore smooth link dependence, but the rotor coefficients are then matrices rather than the original classical-phi free fast family. The old fiberwise static gap cannot simply be transferred to that different operator by assertion.

Therefore the local magnetic-gap conclusion should remain CONDITIONAL on a proved actual gauging that satisfies the local comparison, or on an independently acquired matrix-rotor fast-gap input. The issue was sent to its constructor and root. It does not invalidate the finite-charge finite-volume detector theorem above, or any ungauged package result.

The Berry/Born–Huang warning in the magnetic note is correct: projecting electric kinetic energy onto a fast ground ray produces both a Berry connection and a positive orthogonal-derivative scalar term. A small excitation bound does not remove these contributions or certify the target gauged response.

Resolution: the constructor confirmed that no actual completion avoiding the differing floor translations had been supplied, and withdrew the unconditional magnetic-fast-gap application at the first line and in the conclusions of its note. The valid result is the conditional localization lemma; the actual gauged-background premise remains open. Root was informed.
