# Constructive next route: two steps restore coverage
2026-10-29. Observation only; one-step reduction remains open.

For Φ=Ad_X∘ADγ, η=1−γ, the affine Bloch map squares to (ηx,ηy,η²z−γ²). Thus Φ² is generalized amplitude damping with γ_eff=1−η² and stationary q=η/(1+η). At γ=1/2 this gives γ_eff=3/4, q=1/3. The accepted thermal CP-coverage formula is positive for Φ² even though Φ has no CPTP EB minorization weight.

The thermal theorem therefore bounds dephasing loss by two-step relative entropy loss. It does NOT yet bound it by the one-step actual-prior Holevo loss: no general monotonicity of successive entropy losses is assumed. Closing that comparison would be new load-bearing work. This observation does not alter the exact obstruction.

Petz/KMS symmetry is exact: with σ=diag(η/(1+η),1/(1+η)), each Kraus operator satisfies σ^(1/2) K_j† σ^(−1/2)=K_j. Thus the unrotated Petz transpose is Φ itself and its composition with Φ is Φ². This is not permission to use an unrotated-Petz Umegaki recovery remainder: such a general statement is not supplied.

A floating diagnostic (check_two_step_loss.py) sampled16,000 states with reference dimensions1–4, half near stationary products. Maxima of L(Φ²)/L(Φ) were about1.57310,1.77003,1.62369,1.59342 respectively. No factor2 violation was observed; factor1.5 is already false in these samples. These are exploratory diagnostics, not a universal inequality or directed-rounding certificate. Here LΨ(ρ)=D(ρ||σ⊗ρ_R)−D(Ψρ||σ⊗ρ_R).
