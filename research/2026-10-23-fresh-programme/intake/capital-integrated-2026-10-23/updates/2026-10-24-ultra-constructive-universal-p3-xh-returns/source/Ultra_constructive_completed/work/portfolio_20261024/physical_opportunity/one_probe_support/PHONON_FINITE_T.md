# Finite-temperature check at one spring setting

This is a bounded quadrature check for the one-side-resonator model with
`m=M=K=1` and `k=4`. It is not an optimization over `k` or over internal
networks; those are separate questions. The quantity compared is ballistic
Landauer heat conductance against a rigid chain with the same total mass 2 per
backbone cell and the same intercell spring.

## Bands and conductance

For Bloch variable `s=4 sin^2(q/2)`, the mass-normalized matrix and eigenvalue
equation are

`D(q)=[[s+k,-k],[-k,k]]`,  `lambda^2-(s+2k)lambda+sk=0`.

At `k=4`, the pass bands are

`[0,A] U [B,C]`, where `A=sqrt(6-sqrt(20))=1.236067977500`,
`B=sqrt(8)=2.828427124746`, and
`C=sqrt(6+sqrt(20))=3.236067977500`.

For `theta=kBT/(hbar omega_0)`, `omega_0=sqrt(K/m)=1`, and
`g(x)=x^2 exp(x)/(exp(x)-1)^2`, the normalized conductances are

`Gtilde_side = integral_0^A g(omega/theta)domega + integral_B^C g(omega/theta)domega`,

`Gtilde_rigid = integral_0^sqrt(2) g(omega/theta)domega`.

The physical conductance is `(kB omega_0/2pi) Gtilde`. Both acoustic and
optical bands are included. `phonon_finite_t.py` evaluates these intervals by
composite Simpson quadrature and independently by 160-point Gauss-Legendre
quadrature; their maximum absolute discrepancy in the reported cases is below
`2e-12`.

| `theta` | resonator `k=4` | rigid total-mass chain | relative change |
|---:|---:|---:|---:|
| 0.5 | 1.0943885219 | 1.1613358709 | −5.7647% |
| 1.0 | 1.3854786027 | 1.3401067659 | +3.3857% |

Thus this parameter setting lowers the modeled conductance at `theta=0.5`,
while it raises it at `theta=1`. This verifies one finite-temperature
comparison only; it establishes neither an optimal setting nor a uniform
temperature advantage. It is also only a harmonic, ballistic one-dimensional
model calculation, not evidence for a fabricated material or a measured
thermal device.

Reproduce with `python3 phonon_finite_t.py` from this directory.
