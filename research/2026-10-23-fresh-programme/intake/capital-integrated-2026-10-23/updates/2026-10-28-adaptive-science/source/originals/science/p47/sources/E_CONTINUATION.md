# Phonon family: scientific checkpoint and continuation

## Governing result

FAMILY_THEOREM_v3.md (SHA256 e039c3a8a70181d9b123ae8e4af7b3a7394386512afb12ca89e0bdb55d19b052) is the current governing proof.

For every finite positive temperature theta, K>0 and M>m0>0, the ideal harmonic single-backbone thermal-conductance minimum over all finite positive internal mass/spring networks and backbone allocations m>=m0 is attained by backbone m0, side mass M-m0 and ONE finite spring k_*. The active spectrum/response and tuning are unique; physical isospectral/dark-mode realizations need not be.

The proof supplies an actual attainable endpoint curve, interior existence, a three-root Bose dual, a global analytic resource inverse, and complete positive-star realization of arbitrary finite strict passband unions. Foster/Stieltjes synthesis itself is established prior art. The specialized universal thermal extremal result's historical novelty remains UNKNOWN.

Root reviewed the whole proof and exposition revisions, and ran the numerical construction plus exact interval scripts PASS. The three bounded mathematical support audits cover inverse realization, universal coverage and Jacobian/global inverse; source support records the strongest identified classical ancestry and access limits. These are internal reviews, not external certification.

## Actual objects and precision

attainable_design.py returns the actual optimal two-mass network for general input resources and synthesizes arbitrary strict endpoint data.

Its saved universal_design_example.json uses the ordinary input K=1,M=2,m0=1,theta=1/2, giving
r_*=2.33627398549,
k_*=2.72908806764,
bands[0,1.16000444749] union[2.33627398549,2.84825662767].
Full conductance J/J_rigid is approximately0.93852146. This instantiates the universal theorem; it is not a parameter sweep.

certify_design_example.py and certified_design_example.json prove with exact rational intervals that
2.336273985489<r_*<2.336273985490,
2.7290880676363<k_*<2.7290880676387,
and0.04863839147019<j''(r_*)<0.04863839147314.
CONDITIONING_COROLLARY.md gives the all-resource strict-curvature identity behind the simple scalar root.

The independent three-band object in three_band_star_example.json has squared endpoints alpha=[0,4,16], beta=[1,9,25]. It is realized by a positive two-branch star with exact backbone4/15, total mass256/225, branch squared frequencies(13±sqrt109)/2 and total incident stiffness28/15. Both endpoint matrices and all requested frequencies were reconstructed.

Numerical residuals and exact interval signs have distinct roles. No uniform precision/conditioning bound near resource boundaries is claimed.

## Resource mechanism and physical boundary

TEMPERATURE_RESOURCE_LIMITS.md proves the retuned low-temperature law:
r_*/(2theta)->x_R,
sinh x_R=R^(3/4)sinh(x_R/sqrtR), R=M/m0,
and k_* proportional to theta^2.
The optimized quantum-conductance ratio has an explicit mass-ratio integral and, in the subsequent large-R limit, scales as(3/(2pi^2))lnR/sqrtR.

Retuning spends physical range: quantum pendant variance>=k_B T/k_*, which diverges at least as1/T for fixed mass in that low-T family. At high temperature the optimal internal stiffness diverges. Each fixed finite cell retains its ordinary low-T single-channel and classical full-band limits.

A further exact stiffness threshold follows from the inverse high-frequency coefficient: every network attaining the same optimal response has backbone incident internal stiffness k_*. Its total positive internal spring sum is at least k_*. The one-pendant construction uses exactly k_*; hence exact attainment under a total internal-spring cap kappa_max is possible iff kappa_max>=k_*. This is a point-mass/spring budget, not a fabrication mass or energy claim.

The output remains intrinsic scalar BALLISTIC conductance. Full3D polarizations, contacts, connector geometry, specific modulus, strain, disorder and anharmonicity require the independently owned physical-interface comparison. No specimen, measurement or device advantage was acquired. Main physical mission remains NOT_ACHIEVED.

## Established comparator

PRIMARY_COMPARATOR_NOTE.md gives the equally informed comparator arbitrary finite Foster/Cauer/Stieltjes synthesis, complete spectral information and identical M,m0,K,theta. It can realize the same winning primitive. The analytic result eliminates finite internal-topology search for this objective; it does not claim invention of passive resonance or physical superiority over an incumbent denied the winning operation.

## Next load-bearing construction question

With a genuinely binding finite internal-spring budget kappa_max<k_*, construct the best ATTAINABLE passive spectrum and determine its minimal required active network order. The available foothold is the exact additional coefficient
sum(k_j)=4K[E-A_band^2]/(2A_band^2),
E=sum(beta_j^2-alpha_j^2), A_band=sum(beta_j-alpha_j).
Any continuation must use that cost in an actual positive network construction rather than optimize an unrealizable indicator relaxation.

## Preservation

The earlier governing99f7440a proof/certificates are unchanged. Original family6092 and version2 are also preserved byte-for-byte. All new work is confined to phonon_family. No formal goal, automation, pool expansion, equipment action, public disclosure or packaging was created.

