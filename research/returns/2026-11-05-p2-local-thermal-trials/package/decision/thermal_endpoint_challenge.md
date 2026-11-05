# Independent challenge of the selected thermal intervention endpoint

This note assesses the exact statement communicated by the parent and thermal constructor. It does not reopen the accepted predictive-preparation or passive-acquisition results.

## Assessment

The proposed operation is mathematically compatible with its advertised inputs: a known factorized kinetic Gibbs coordinate, an actual fresh Langevin port, finite initial joint relative entropy including an old classical reference, and an independent physical clock with a bounded density. Conditional Gaussian logarithmic Sobolev and entropy dissipation give a genuine joint replacement statement. A bounded marking kernel then converts that statement into a randomized-ensemble instrument. The common-future-channel contraction is valid and avoids a future-horizon error multiplier.

The potential contribution is **finite physical acquisition of an unconfounded local trial in an environment that need not mix globally**. Local Maxwellization, entropy decomposition, biased selection and Gaussian momentum resampling are established machinery. The useful novelty claim must attach to the complete physical/reference/time/record interface, not to those ingredients or to an asserted new way of identifying arbitrary dynamics.

## 1. Closest primary mathematical comparators

Desvillettes and Villani, *On the trend to global equilibrium in spatially inhomogeneous entropy-dissipating systems: The linear Fokker-Planck equation*, CPAM 54 (2001), 1–42, explicitly study velocity-only collision operators, logarithmic Sobolev inequalities and the degeneracy that leaves infinitely many local equilibria. Their target is global convergence and they add regularity machinery to overcome that degeneracy. The selected operation deliberately stops at the local factorization resource. This is a meaningful change of endpoint; the entropy-production mechanism itself is established.

Primary source: <https://onlinelibrary.wiley.com/doi/abs/10.1002/1097-0312(200101)54:1%3C1::AID-CPA1%3E3.0.CO;2-Q>.

Vladimirov, *Position-momentum conditioning, relative entropy decomposition and convergence to equilibrium in stochastic Hamiltonian systems* (2023), explicitly decomposes joint position/momentum relative entropy into a position term and a conditional-momentum term for nonlinear Langevin systems. It is a particularly close comparator that should be cited in the final result. Its purpose is convergence analysis and higher-order dissipation, rather than a bounded-clock local trial with retained references and a finite meter.

Primary source and full text: <https://arxiv.org/abs/2312.09475>, <https://arxiv.org/html/2312.09475v1>.

There is also a broader established programme relating zero entropy production/loss to local Gibbs structure without demanding a unique global equilibrium. Jahnel and Koppl give a dynamical Gibbs variational principle for irreversible interacting particle systems. Caputo and Parisi treat block entropy factorization under strong spatial mixing. These are relevant alternatives, but their lattice assumptions and targets do not automatically imply the selected physical instrument.

Primary sources: <https://arxiv.org/abs/2205.02738>, <https://arxiv.org/abs/2004.10574>.

## 2. Strong physical/computational alternatives

**Direct Maxwell reset.** Andersen's thermostat assigns fresh Maxwell-Boltzmann velocities at random collisions. If a physical device can actually overwrite the relevant momentum independently while preserving the hidden configuration, that supplies the desired kinetic factor immediately and wins over waiting. A simulated assignment instruction is not evidence that a physical specimen has that port. The manuscript should continue to exclude it only when the encounter interface really excludes it, not merely to protect an advantage.

Original source: Andersen, *Molecular dynamics simulations at constant pressure and/or temperature*, JCP 72 (1980), 2384–2393, DOI <https://doi.org/10.1063/1.439486>; a scanned primary copy is available at <https://users.wfu.edu/natalie/f23phy711/lecturenote/HCAndersen.pdf>.

**Isoconfigurational and shooting ensembles.** Molecular simulation has long studied different randomized momenta at one fixed configuration. Widmer-Cooper, Harrowell and Fynewever's 2004 isoconfigurational construction is a direct comparator for separating configuration from dynamical variation. Transition-path shooting commonly replaces velocities by Maxwell-Boltzmann draws before integrating equations. Those approaches have a numerical state-rewrite/simulator interface and, for repeated identical configurations, a stronger restart capability. The selected physical operation instead has an unknown evolving hidden-state distribution shared by its two arms; it does not repeatedly prepare one identical hidden configuration.

Primary sources: <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.93.135701> and the explicit shooting construction in <https://pmc.ncbi.nlm.nih.gov/articles/PMC6374749/>, Section 2.2.

**Random force pulses.** If external signed impulses are supplied, assigning the pulse sign by an independent coin is already an unconfounded physical intervention, even before thermal readiness. It generally targets a different distribution: the old momentum and its hidden-state correlations remain underneath the added kick, and the energy budget differs. The selected result should state its target distribution precisely rather than claiming that all local causal trials previously required equilibration.

## 3. The marking instrument is valid, but its causal target matters

Let `P` be Gaussian with variance `sigma^2`, independent of hidden state `Z`, old reference `R` and the chosen clock after the replacement step. Let `s(P)=sin(P/sigma)` and choose `A in {-1,+1}` with

\[
\Pr(A=a\mid P)=\frac{1+a s(P)}2.
\]

Then `A` is fair and independent of `(Z,R,T)`, and

\[
\mathcal L(P,Z,R,T\mid A=a)
=q_a(P)\,\mathcal L(Z,R,T),
\qquad q_a=G_\sigma(1+a s).
\]

This is exactly the ensemble law of first choosing a fair arm and then preparing its momentum distribution independently of the hidden state. Although the actual device only marks a naturally occurring momentum, equality of the complete joint law makes the intervention interpretation valid for a common future channel.

The arm is not independent of momentum, nor should it be. The result is not an externally selectable deterministic preparation of the plus state on every run. An experiment that insists on plus only must discard or route the other arm and pay its occurrence probability. It is also not a stationary response of the full hidden Gibbs ensemble: the shared `Z` law is whatever law the preparation clock actually produces.

If an outcome is rare, marking alone cannot accelerate its production. Since `q_a/G_sigma<=2`, the event probability under either fair arm is at most twice its unmarked probability, and that arm occurs on only half of the runs. In the general decomposition `G=sum_a w_a q_a`, the pointwise bound is `q_a/G<=1/w_a`; any conditional enhancement is paid by the arm probability. There is no unearned rare-event sampling speedup.

## 4. A stronger ordinary estimator when the future ignores the arm

Suppose the later physical protocol does not use `A`; it merely measures a bounded outcome `Y`. Under the ideal factorization the desired contrast is

\[
\tau=\mathbb E_{q_+}Y-\mathbb E_{q_-}Y
=2\mathbb E[s(P)Y].
\]

Thus the same trials can estimate the contrast directly from the bounded weighted observation `2 s(P)Y`, without generating a Bernoulli arm. This is ordinary change of measure. It is also a strict Rao-Blackwell improvement over the score `2AY` whenever the conditional coin has nonzero variance:

\[
\operatorname{Var}(2AY)-\operatorname{Var}(2s(P)Y)
=4\mathbb E[(1-s(P)^2)Y^2]\geq0.
\]

The identity assumes `Y` is conditionally independent of the marking coin given the physical trajectory. It does not apply when the arm selects a later physical action, in which case the actual coin is operationally relevant. Nor does it make the bounded weight or its metrology free: the weight must be computed, stored until the outcome, and included in the record/reuse accounting. Finite quantization suffices. For `|Y|<=1`, a TV replacement error `delta` contributes at most `4 delta` to this weighted mean; momentum-meter and quantization errors add their explicitly bounded contributions.

This estimator is a useful way to eliminate an unnecessary physical/randomization operation when only an arm-invariant response contrast is wanted. It preserves the genuine contribution: thermal structure has *earned* the absence of hidden confounding needed to interpret the weighted correlation causally.

## 5. A sharp local signal choice under the same metrology sensitivity

The sinusoidal arms are analytically convenient but do not maximize their opposite momentum means under the same Lipschitz sensitivity. For every bounded marking function `s` with `|s|<=1` and Lipschitz constant at most `L`, the largest attainable mean contrast among fair equal-kinetic-energy arms is attained by

\[
s_*(p)=\operatorname{clip}(Lp,-1,1).
\]

Proof: replace any feasible `s` by its odd part. This leaves `E[P s(P)]` unchanged, preserves the amplitude and Lipschitz bounds, and enforces both `E[s]=0` and `E[P^2s]=0`. For odd Lipschitz `s`, `|s(p)|<=min(L|p|,1)`, so pointwise maximization of `p s(p)` gives the clipped linear function. Gaussian integration by parts yields

\[
\mathbb E_{q_+}P
=\sigma^2L\,\operatorname{erf}\!\left(\frac1{\sqrt2\sigma L}\right).
\]

At the sinusoid's Lipschitz constant `L=1/sigma`, this gives `0.682689... sigma`, compared with `exp(-1/2) sigma=0.606531... sigma` for the sinusoid. Both have the same mean-error bound `L E|P_hat-P|` for finite momentum metrology. The clip can be evaluated by ordinary finite comparisons and arithmetic. This is a modest implementation improvement, not the main scientific consequence. A smooth approximation can be used if a particular electronics contract demands smoothness.

## 6. Thermodynamic and interface checks that must remain visible

- Equal kinetic energies do not make the labelled preparation thermodynamically free. The arm carries mutual information with momentum. For the sinusoidal example, `I(A:P)=0.26175224...` nats, equal to the average conditional free-energy increase divided by `k_B T` in the ideal marginal. The finite initialized memory, retained label and eventual reset/erasure are resources. A blind reset of a fair arm bit has the usual one-bit entropy bill; access to correlated side information can change the optimal reset cost and must be specified.
- The fresh thermostat must be fresh relative to `R`. An old bath or memory with inaccessible correlations is not automatically the declared Langevin resource.
- The random start-time theorem needs an actual independent time distribution with a density cap. A finite list of possible times does not inherit the continuous bound. A timeout must produce a declared failure branch; forcing the experiment at a timeout atom would require a separate argument.
- A finite two-position momentum estimate can depend on future noise. This does not break the proof if the actual and ideal marks are coupled on the same physical meter-window path and a Lipschitz marking error is bounded. It does break a careless argument that treats the estimate as independent sensor noise at the earlier time.
- The meter-window state change must be carried through the common future channel. Calling the state at the end of the window the same prepared state at its beginning would silently add a freezing operation.
- A Girsanov backaction estimate needs the actuator disturbance in the noisy momentum direction with the stated action bound. An unknown perturbation in an unnoised hidden direction does not receive that path-KL bound automatically.
- The old reference may include earlier outcomes, but a newly retained fine momentum record is intentionally correlated with momentum. It can be included in the output instrument, not in the pre-existing independent reference factor. A proof that silently promotes it to the latter is false.
- Reuse requires the updated entropy/action/record ledger, plus outcome exposure. It does not create independent hidden specimens. A rare future event still costs its actual observation time or a separately constructed acceleration method.

## Recommendation

Keep the result, with the acquisition-to-instrument bridge as its contribution. Cite the closest conditional-momentum entropy literature explicitly. Offer the direct weighted estimator for arm-invariant outcomes and the actual mark when the arm routes later operations or a one-bit output interface is wanted. Do not sell the operation as a new thermostat, a general response simulator, a sampler of identical hidden configurations, a rare-event accelerator, or a universal substitute for a real impulse actuator. Under these limits, the main construction survives this independent challenge.
