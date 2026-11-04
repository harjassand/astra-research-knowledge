# Progress for root

Chosen whole question: Can finite-time equilibrium observations provide a universally valid, finite certificate for a material's macroscopic Green–Kubo transport coefficient, without an externally supplied relaxation bound?

Strongest derived mechanism: a two-dimensional passive reversible Ornstein–Uhlenbeck construction. Set Σ=[[1,ρ],[ρ,1]], Q=diag(1,λ), and dZ=−QΣ⁻¹Z dt+sqrt(2Q)dW in its exact invariant N(0,Σ) distribution. Observe J=Z₁. Every model has Var(J)=1 and quadratic variation [J]t=2t. The reference ρ=0 is the same scalar unit OU for every λ. Nevertheless, its Green–Kubo integral is K=1+ρ²/λ. The full-path relative entropy against the ρ=0 model is exactly −m log(1−ρ²)/2+B(1+λ)ρ²/[4(1−ρ²)] for m independent trajectories with total dimensionless duration B. Scalar-path entropy is no larger. Let ρ→0 and λ=ρ²/(M−1): observations become arbitrarily close to a fixed fast-OU reference while K=M is arbitrarily large.

Earned consequence: any upper confidence bound uniformly honest with coverage 1−α over this passive equilibrium class must equal infinity with probability at least 1−α even on the simple reference signal. An adaptive procedure has the same obstruction: it can terminate with a finite bound on the reference with probability at most α. This is a clean exact counterexample, not a universal transport solver or a demonstrated material discovery capability.

Physical assumptions actually used: equilibrium with a heat bath, detailed balance for velocity process, positive quadratic energy, fluctuation–dissipation, finite second moments, and exact stationary initialization. It does NOT establish impossibility given a fully known microscopic generator or all conservation/locality assumptions of an isolated many-body Hamiltonian. Exact equilibrium starts are granted for free, so no hidden initialization burden helps the impossibility; physically producing them can itself require the slow relaxation time.

I am verifying the formulas and producing a proof, reproducible numerical example, conditional tail certificate, and comparisons against cepstral transport estimation, STACIE, and stronger-access transient-subtraction methods. The original universal endpoint is invalid under the stated access model; the restricted certificate will not be promoted as solving it.


## Final strengthened Gibbs join saved

`GIBBS_CDF_JOIN.txt` now uses fixed **log contrast c**, `q_i^- >= (q_i^+)^c`, with no fixed ordinary odds ratio. It independently derives heavy-prefix partition counting from the uniformly pinned sampler: `d=alpha/(128m)`, additive marginal estimates with fresh TV-`d/2` samples, empirical heavier branch true mass at least `63/128`, and `|log(Zhat_C/Z_C)| <= 3alpha/128`. Cut masses follow as `Z_D/Z_empty`; retain pinning constants in the original weight. Positive rational outputs and all sample/random-bit costs are finite. The rational mass floor has `O(m+L)` bit length. The previous odds-normalized Rao--Blackwell requirement is explicitly removed.

The join also supplies row-Dobrushin mixing and physical generator gap, exact target-versus-approximate-computational-initialization distinction, revised safe rejection cap, global CDF bias/confidence ledger, and fresh-versus-shared static preprocessing requirements. The cut-enumeration/omitted-union part remains root's proof obligation. Main full proof file remains `transport_no_go.md`; its universal constructive endpoint is explicitly refuted, and numerical figure has been visually inspected.
