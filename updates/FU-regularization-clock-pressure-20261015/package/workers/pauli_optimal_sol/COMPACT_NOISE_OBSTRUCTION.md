# Compact scalar noise is impossible, without radial symmetry

This independently expands the Pauli-pair tilted moment mechanism from the supplied source. No noise-coordinate independence is assumed.

Suppose a positive normalized POVM M satisfies the exact scalar-factor identity for the Pauli triple, with a positive scalar noise law ν of compact support. Coordinate projection laws are the corresponding Pauli spectral law plus scalar noise, so each coordinate of M has bounded support. Positivity then confines M itself to a bounded cube. All Laplace transforms and differentiated moments below are therefore genuine finite integrals.

Use the Pauli pair A=σ_z, B=σ_x and write

`Q(s,t)=∫exp(sx1+tx2) M(dx)=mν(s,t) exp(sA+tB)`.

The equality follows from the all-linear marginal contract, now evaluating the one-dimensional Laplace transform of each bounded directional output. Let κ=log mν, μ=κ2(s,0), and normalize the exponentially tilted POVM by

`E_s(dx)=mν(s,0)^−1 exp(−sA/2) exp(sx1) M(dx) exp(−sA/2)`.

Then ∫E_s=I. Define

`K_j(s)=exp(−sA/2) [∂t^j exp(sA+tB)]_(t=0) exp(−sA/2)`.

The first two x2 moments of E_s are

`F=μI+K1`,

`G=(μ²+κ22)I+2μK1+K2`.

Positivity of the operator moment block `[[I,F],[F,G]]` gives its Schur complement

`κ22(s,0)I+K2(s)−K1(s)²≥0`.

For s>0, the closed Pauli exponential formula yields

`K1=(sinh s/s)σ_x`,

`K2=exp(−sσ_z)[(sinh s/s)I+((s cosh s−sinh s)/s²)σ_z]`.

Subtracting `K1²=(sinh²s/s²)I` gives exactly

`K2−K1²=diag(−d(s),d(s))`,

`d(s)=[sinh(2s)−2s]/(2s²)`.

Hence `κ22(s,0)≥d(s)` for every s>0. The left side is the scalar second-coordinate variance under the first-coordinate exponential tilt. If the original compact scalar support has second-coordinate range [a,b], every such tilted law remains supported in [a,b], and its variance is at most `(b−a)²/4`. The right side diverges exponentially as s tends to infinity. This contradiction proves that no compactly supported positive scalar noise law can satisfy the exact Pauli-pair contract.

The argument covers nonradial laws, singular laws, arbitrary dependence between noise coordinates, and nonzero noise means. The optimal radial law's unbounded support is consequently necessary, not an incidental choice of its construction.
