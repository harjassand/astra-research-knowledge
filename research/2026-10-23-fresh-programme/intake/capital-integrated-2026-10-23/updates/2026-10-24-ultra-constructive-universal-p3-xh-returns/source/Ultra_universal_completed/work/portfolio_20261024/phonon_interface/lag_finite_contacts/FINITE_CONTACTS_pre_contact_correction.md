# Finite-chain contact check for the two-mass optimum

This is an independent finite-device check of the point-mass/spring model in
`work/portfolio_20261024/physical_opportunity/PHONON_OPTIMUM.md`. It does not
change or strengthen the infinite-periodic-cell theorem.

## Model and exact scattering reduction

Use the optimum's dimensionless parameters

\[
 m_b=1,\quad m_s=M-1=2.3387164232022783,\quad
 K=3.7866316437609973,\quad k_s=2.8019347878118195,
 \quad M=3.3387164232022783.
\]

A finite device has N backbone masses `m_b`, each attached to one side mass
`m_s` by `k_s`; adjacent device backbone sites are joined by K. Each end
backbone is attached by a physical spring `K_c` to a semi-infinite rigid lead
with mass M and spring K. The default is `K_c=K`. Thus each finite device cell
still has mass M, including its side mass; the lead is not an artificial
absorber.

In the lead, `M omega^2=2K(1-cos q)`, `0<=q<=pi`, so the open-channel cutoff is
`Omega=2 sqrt(K/M)=2.129937004646146=c/2`. The outgoing surface Green function
is `g_s=exp(iq)/K`, giving contact self-energy and broadening
\[
 \Sigma=(K_c^2/K)e^{iq},\qquad \Gamma=2(K_c^2/K)\sin q.
\]
With dynamic matrix convention (spring stiffness minus `omega^2` times mass),
the effective on-site term after eliminating a side coordinate is
\[
 d_i(\omega)=s_i-\omega^2\left(m_b+
       \frac{k_s m_s}{k_s-m_s\omega^2}\right),
\]
where `s_i=2K` for interior sites, `s_i=K+K_c` at an end when `N>1`, and
`s_1=2K_c` for `N=1`. Subtract `Sigma` at each device endpoint; the remaining
effective matrix `A_N` is tridiagonal with off-diagonal `-K`. This retains the
physical endpoint spring diagonals. The side-resonance pole at
`omega=sqrt(k_s/m_s)=1.094561652986` is a transmission zero (an isolated point
in the integral).

For identical leads on both sides, the exact single-channel transmission is
\[
 T_N(\omega)=\Gamma_L\Gamma_R |(A_N^{-1})_{1N}|^2
 =\Gamma^2 K^{2N-2}/|\det A_N|^2,
\]
because the endpoint cofactor of a tridiagonal chain has magnitude
`K^(N-1)`. For `N=1`, both self-energies act on the same endpoint. The
reproduction script evaluates the determinant by continuants and integrates
over q, using `omega=Omega sin(q/2)` and the exact Jacobian. It uses
`g(omega)=(omega/sinh(omega))^2` (the source's `theta=1/2`), and reports
`J_N=integral_0^Omega g(omega) T_N(omega) d omega`. With the source's
frequency unit treated as physical, the Landauer conductance is
`k_B/(2 pi) J_N`; if omega is dimensionless with physical scale `omega_0`, the
prefactor is `k_B omega_0/(2 pi)`. There are no propagating lead modes above
Omega.

## Results

At matched contact spring `K_c=K`, the rigid comparison device is a uniform
chain of mass M and spring K. The code recovers `T=1` throughout the open lead
band to maximum interior error below `2e-14`, and gives the same `J=1.440176577374`
for every N. The side-resonator device gives:

| N | `J_side` | `J_rigid` | `J_side/J_rigid` | `J_side/J_bulk-optimum` |
|---:|---:|---:|---:|---:|
| 1 | 0.941692625528 | 1.440176577374 | 0.653873 | 0.830916 |
| 2 | 0.874856367717 | 1.440176577374 | 0.607465 | 0.771942 |
| 4 | 0.859509267889 | 1.440176577374 | 0.596808 | 0.758400 |
| 8 | 0.861707749387 | 1.440176577374 | 0.598335 | 0.760340 |
| 16 | 0.861035805787 | 1.440176577374 | 0.597868 | 0.759747 |

Here `J_bulk-optimum=1.133319342823405` is the ideal infinite-periodic passband
integral. The finite-chain result is a distinct observable: for the chosen
rigid leads, the high optical band above `Omega` is inaccessible, and within
the lead band the finite resonator section has resonances and antiresonances
rather than unit transmission on its bulk pass bands. The finite-device
integrals are about 24% below the ideal bulk optimum for N=4--16, while the
matched rigid-chain device remains ballistic with `T=1`.

For N=8, changing both contact springs equally in the resonator and rigid
comparison devices gives:

| `K_c/K` | `J_side` | `J_rigid` | ratio |
|---:|---:|---:|---:|
| 0.50 | 0.258723040389 | 0.489946105888 | 0.528064 |
| 0.75 | 0.532390264772 | 1.002755501463 | 0.530927 |
| 1.00 | 0.861707749387 | 1.440176577374 | 0.598335 |
| 1.50 | 0.391989333176 | 0.739174745846 | 0.530307 |
| 2.00 | 0.214726097931 | 0.416820325570 | 0.515153 |

The N=16 side-device quadrature at 20,001, 80,001 and 320,001 q-points is
0.861074432669, 0.861035805787 and 0.861035751469, respectively. The matched
rigid transmission is the important end-to-end check on the self-energy sign,
contact diagonal and Landauer normalization.

## Scope

This checks one finite harmonic point-mass chain and a matched-mass rigid-chain
baseline under the stated lead/contact model. The contact-spring sweep is a
sensitivity check, not an optimization over all possible contacts. It does not
model disorder, anharmonicity, finite-volume atomic geometry, real material
contacts, diffusive conductivity, or any experimental/device outcome. No
hardware or material extrapolation follows from these values.

Reproduce with:

```sh
python3 work/portfolio_20261024/phonon_interface/lag_finite_contacts/finite_contact_check.py
```
