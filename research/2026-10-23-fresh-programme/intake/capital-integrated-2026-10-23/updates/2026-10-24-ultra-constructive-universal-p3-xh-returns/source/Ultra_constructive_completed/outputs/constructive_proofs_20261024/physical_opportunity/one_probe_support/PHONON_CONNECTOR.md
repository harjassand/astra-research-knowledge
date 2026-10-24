# Finite midpoint-connector inertia check

This finite model tests whether the two-mass optimum's θ=0.5 reduction is
fragile to a massive connector. It keeps the parent design's backbone mass
`m_b=1`, total mass `M=3.3387164232022783`, intercell spring
`K=3.7866316437609973`, and internal spring parameter
`k=2.8019347878118195` fixed. The original spring is replaced by two springs
of `2k` in series. A point connector of mass `δ` sits between them, and the
terminal mass becomes `M_side-δ`. The total mass and static series stiffness
therefore remain fixed. This is a point-mass/spring perturbation, not a
fabrication or support model.

## Three-mass spectrum

In physical coordinates `(x_backbone,x_connector,x_terminal)`, the
within-cell stiffness matrix at zero wave number is

`K0 = [[2k,-2k,0],[-2k,4k,-2k],[0,-2k,2k]]`,

and the mass matrix is `diag(1,δ,M_side-δ)`. Its mass-normalized form is
`D0=M^{-1/2}K0M^{-1/2}`. For `s=4K sin^2(q/2)`,

`D(q)=D0+s e_1 e_1^T`,

where the backbone coordinate is the first coordinate. Let the ordered
eigenvalues of `D0` and `D0+4K e_1e_1^T` be `α_0≤α_1≤α_2` and
`β_0≤β_1≤β_2`. Rank-one interlacing gives the three pass bands

`[sqrt(α_0),sqrt(β_0)]`,
`[sqrt(α_1),sqrt(β_1)]`,
`[sqrt(α_2),sqrt(β_2)]`.

The script diagonalizes both symmetric matrices, checks the interlacing and
mass sum, and integrates all three bands with 240-point Gauss–Legendre
quadrature. A separate 4096-panel composite Simpson calculation agrees to
`2.22e-16` or better across this sweep. The high optical branch is included
even when its thermal contribution is tiny.

## Results at θ=0.5

The two-mass ideal cell has `J=1.133319342823`; the same-total-mass rigid
comparator has `J=1.440176577374` and cutoff
`2 sqrt(K/M)=2.129937004646`. The connector-mass sweep is:

| `δ/M_side` | pass bands (frequency endpoints) | total `J` | highest-band contribution | `J/J_rigid` | `J/J_ideal` |
|---:|---|---:|---:|---:|---:|
| 1% | `[0,1.003276098]`, `[2.001702927,4.249177867]`, `[21.982799494,21.984875240]` | 1.135015422080 | 3.23e-19 | 0.788109 | 1.001497 |
| 5% | `[0,1.016615096]`, `[2.009550261,4.199431975]`, `[9.996651282,10.022430868]` | 1.141480517167 | 2.09e-8 | 0.792598 | 1.007201 |
| 10% | `[0,1.033815496]`, `[2.021886060,4.118242077]`, `[7.218089911,7.301142341]` | 1.148684927846 | 8.67e-6 | 0.797600 | 1.013558 |
| 20% | `[0,1.069917928]`, `[2.056385646,3.883705015]`, `[5.322745055,5.610612659]` | 1.159469881013 | 6.20e-4 | 0.805089 | 1.023074 |
| 50% | `[0,1.186873797]`, `[2.276162193,3.279028640]`, `[3.847042734,4.792335596]` | 1.169669842290 | 1.36e-2 | 0.812171 | 1.032074 |
| 80% | `[0,1.281146524]`, `[2.722656133,3.871945660]`, `[4.020197923,4.699795179]` | 1.170433098867 | 8.81e-3 | 0.812701 | 1.032748 |

Across the tested positive connector masses, the finite connector raises `J`
by about 0.15–3.27% relative to the ideal two-mass cell, while `J` remains
about 18.7–21.2% below the rigid comparator. The third branch moves down as
connector inertia grows and is fully counted; it is negligible at the smallest
fractions and contributes at the percent scale for the largest fractions.

This supports robustness only for the stated lumped series-spring family and
tested mass fractions. It does not price distributed beam/rod modes, joint
compliance, finite specific modulus, geometric constraints, disorder,
anharmonicity, or contact resistance. Run `python3 phonon_connector.py` from
this directory to reproduce the values.
