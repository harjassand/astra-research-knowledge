# Physical scale and finite connector checks

These calculations are separate from the exact harmonic optimum in PHONON_OPTIMUM.md. They do not establish a manufactured material or a new thermal-conductivity measurement.

## Temperature/frequency scale

Let the proof's dimensionless frequency unit be omega_u in rad/s. Its theta=1/2 operating point means
T=hbar omega_u/(2 k_B).

A unit frequency f_u=omega_u/(2pi)=1 GHz corresponds to T=0.0239962 K. At5 GHz it is about0.120 K; at1 THz it is about24.0 K. To put this precise dimensionless construction at300 K requires f_u about12.50 THz, with the optical band from25.0 THz to53.3 THz. A macroscopic low-frequency vibration demonstrator therefore does not demonstrate the thermal benefit at room temperature. The quantum thermal weighting is load-bearing.

The actual3D device also has additional acoustic polarizations; suppressing one scalar spectrum does not establish its whole heat conductance.

## Finite specific modulus

For an axial intercell connector of span a, cross-section A, Young's modulus E and density rho,
K=EA/a and M_connector=rho A a
imply M_connector=K a^2/(E/rho).

With the proof's physical K=3.78663164 m_min omega_u^2 and an assigned backbone mass at least this connector mass,
omega_u a <= sqrt[(E/rho)/3.78663164].
Equivalently,
T a/sqrt(E/rho) <= hbar/[2 k_B sqrt(3.78663164)]
=about1.963e-12 K s.

For an illustrative material wave-speed scale sqrt(E/rho)=5000 m/s and a=100 nm, this chosen dimensionless design requires T no more than about0.098 K under that rod/lumped-mass assignment. This is a scaling illustration, not an acquired material parameter or a proposed part specification. Atomic bonds require an atomistic Hessian and cannot inherit a continuum rod claim unexamined.

Thus a finite positive backbone mass is essential to the theorem's resource interpretation. The ideal construction avoids a vanishing mass, but does not price actual fabrication, strength, contact modes, anharmonicity or lattice geometry.

## Counted internal connector inertia

The support calculation one_probe_support/PHONON_CONNECTOR.md replaces the ideal internal spring k by two series springs2k and gives their midpoint a finite mass delta, reducing the terminal side mass by the same delta. This keeps totalM, backbone mass1, externalK and static internal series stiffnessk fixed.

All three resulting branches are included. For the tested delta/M_side values1%,5%,10%,20%,50%,80%, ideal-contact theta=.5 conductance remains approximately18.7–21.2% below the same rigid-chain comparator. The positive two-mass result therefore survives sizeable finite internal inertia in this specific lumped family. This does not establish robustness to distributed intercell rod mass or full material transport.

The midpoint-node stiffness matrix and numerical work were personally inspected and replayed. A structural rigid-translation zero is enforced when converting eigenvalues to acoustic endpoints; quadrature agreement alone cannot certify a roundoff-shifted endpoint.

