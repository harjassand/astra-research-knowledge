# Normally displayed final: formula text projection

Deterministic text projection of the normally displayed final, preserving its mathematical annotations. This is not an acquired original proof, implementation, or independent review document. Raw visible text and private formula DOM are preserved separately.

New opening: local stationary-state preparation and control

I developed a different operational target: prepare a local part of an unknown many-body stationary quantum state, and estimate its control gradient, using a finite random history of local operations.

The strongest new theoretical step is a geometry argument for one-dimensional chains. It lowers the sufficient reset condition from more than one half to more than one quarter, while retaining finite expected work, an exponential history tail, and finite gradient variance. I also executed two stochastic control experiments, including one at 30% reset, where the original branching argument fails.

There is a consequential limitation: short burn-in outperformed the exact method at the precision tested in both examples. The completed advance is a constructive, rigorously costed operation and a stronger applicability theorem. A practical advantage—and a civilisation-changing consequence—remains unestablished.

The earlier positive matrix debiasing, exact classical batch resource law, timing distinctions and structured alternatives remain intact.

1. The operation and its actual interface

Consider local updates on a known interaction graph: $\mathcal E_e(\theta)
=\alpha\,\mathcal R_e+(1-\alpha)\,\mathcal F_e(\theta).$ 

Here:

 $\mathcal R_e$  completely resets the sites in edge  $e$ , removing their previous correlations.

 $\mathcal F_e(\theta)$  is a separately executable, memoryless local channel. It may be unknown, nonunital and entangling.

The experimenter generates the reset coin externally and can select the local update.

For gradients, the required shifted controls must be physically executable.

This changes the acquisition contract. The primary construction uses live local quantum-channel access. A mathematical decomposition of an unlabelled noisy channel does not supply its reset flag or its residual channel.

That distinction determined the direction. The supplied Uhlmann lead confirms that sample-access algorithms and physical Petz applications already exist; generic physical Petz implementation is therefore not the new destination. Its advertised low-rank regime also cannot simply be imported into the original globally faithful Choi class. arxiv.org

How the finite history works

Start from the sites whose stationary state or observable is wanted. Trace dependencies backward:

Select the next update touching the active set, with the correct incident-edge probability.

If it is a reset, remove that edge’s sites from the active set.

If it is a forward-channel update, add the entire edge to the active set.

Stop when the active set is empty. Reverse the recorded history and execute that finite circuit.

This works at the level of the full Heisenberg operator algebra. A reset eliminates dependence on its previous inputs even when those inputs are entangled. Once every backward dependency has disappeared, the requested output is independent of the arbitrary initial state.

Averaging these finite histories gives the stationary marginal. No global density matrix, channel tomography or chosen burn-in horizon is required.

2. The central new calculation: count clusters as well as sites

A generic  $b$ -site branching bound gives finite work when $b(1-\alpha)<1.$ 

For pair updates, this requires  $\alpha>1/2$ .

I found a stronger potential for uniformly updated nearest-neighbor paths. Let  $A$  be the active set and  $C(A)$  its number of connected runs. Define $W(A)=|A|+\frac{C(A)}{2\alpha},
\qquad
g=2\alpha-\frac12.$ 

The key inequality is $\mathbb E[\Delta W\mid A]\le -g.$ 

It holds throughout $\boxed{\alpha>\frac14.}$ 

The reason is geometric: resets can split a run, remove a short run completely, or erase its endpoints. Counting only occupied sites loses that information.

On the infinite path, an especially compact identity is $\mathcal LW
=-g\bigl(|A|+C(A)\bigr)
-\frac{1-\alpha}{\alpha}G_1(A),$ 

where  $G_1(A)$  counts single-site gaps between runs. Filling those gaps merges runs and supplies the additional negative term.

For  $K$ , the number of relevant events before extinction, $\boxed{\mathbb E K\le \frac{W(A_0)}{g}.}$ 

Writing  $w=1/(2\alpha)$ , the audit also established $\mathbb E K^2
\le
\frac{W_0^2}{g^2}
+
\frac{\bigl((2+w)^2-g^2\bigr)W_0}{g^3},$ 

and, for  $t\ge W_0/g$ , $\Pr(K>t)
\le
\exp\!\left[
-\frac{2(gt-W_0)^2}{t(3+w)^2}
\right].$ 

These bounds depend on the requested region and reset gap, not the total chain length.

The independent audit verified the cluster calculation and finite endpoints. Its exact enumeration checked all nonempty active subsets on paths of sizes  $2,\ldots,12$ , covering the entire reset interval symbolically: 16,354 drift inequalities and 524,296 increment-range checks, with no violation. The analytic argument supplies the theorem; the enumeration corroborates it.

This is a sufficient threshold, not the critical point. Equal edge weights are substantive. The underlying stochastic process is also established: it is Sturm–Swart’s contact process with double deaths after time rescaling. Targeted research did not locate this precise one-quarter extinction bound, but comprehensive priority review remains open. stochastik.math.uni-goettingen.de

3. Turning preparation into an unbiased control operation

Suppose a local control has a valid physical shift identity $\partial_\theta\mathcal F_\theta
=c\bigl(\mathcal F_{\theta,+}-\mathcal F_{\theta,-}\bigr).$ 

For a Pauli rotation surrounded by parameter-independent noise,  $c=1/2$  and the shifts are  $\pm\pi/2$ .

For a sampled history with  $J$  eligible occurrences:

Select one eligible occurrence uniformly.

Select a sign  $s\in\{-1,+1\}$  uniformly.

Shift only that occurrence.

Execute the finite circuit and measure the desired norm-one observable, obtaining  $X\in[-1,1]$ .

Return $\widehat G=2cJsX.$ 

Then $\mathbb E\widehat G
=\partial_\theta\operatorname{Tr}[O\rho_{\rm ss}(\theta)].$ 

The history distribution is independent of the gate parameter. Its finite moments justify differentiating through the random stopping time and bound the estimator’s variance. Fresh histories preserve unbiasedness conditional on previous optimization decisions.

The finite-circuit stochastic-shift estimator has strong predecessors, and classical perfect sampling has already been combined with unbiased stationary derivatives. The investigated contribution is the local stationary quantum representation with explicit work and variance bounds, including the stronger path regime—not the invention of stochastic gradients. arxiv.org+1

What is actually saved in resources

For a fixed local objective and reset gap, the method has finite expected:

Relevant local channel and reset operations.

Classical history-generation work.

Visited quantum sites.

Gradient second moment.

Address bits, routing, gate durations and measurement costs remain. A fixed lattice still contains its physical hardware. Exact histories have unbounded tails; a fixed history or workspace cap gives a controlled approximation.

Separate local samples also do not provide adaptive access to one shared global quantum sample. Conditional on the current history, the output generally differs from the stationary marginal. The earlier timing and record distinctions remain applicable.

4. Executed control below the old threshold

The second benchmark uses three qubits, equal edge rates and  $\alpha=0.3$ : $\mathcal F_{12,\theta}
=0.9\,\mathcal B_\theta
+0.1\,\operatorname{Ad}_{CZ_{12}},
\qquad
\mathcal F_{23}=\operatorname{Ad}_{CZ_{23}},$ 

where  $\mathcal B_\theta$  prepares $|\Phi_\theta\rangle
=\frac{|00\rangle+e^{i\theta}|11\rangle}{\sqrt2}.$ 

These are directly executable residual operations. Their overlapping updates do not commute, and the stationary state retains pair entanglement.

I derived a closed stationary solution, independently verified against the channel equations. In particular, $\langle X_1X_2\rangle_{\rm ss}
=\frac{13041}{37949}\cos\theta.$ 

The pair marginal has partial-transpose eigenvalue $-\frac{155191}{3111818}\approx-0.0498715,$ 

certifying entanglement.

Stationary gradient experiment

At  $\theta=\pi/4$ , the exact derivative is  $-0.242994006$ .

 | Quantity | Executed result

 | Sampled histories | 30,000

 | Physical gradient estimate |  $-0.216667$ 

 | Standard error |  $0.029291$ 

 | Mean relevant events |  $8.9591$ 

 | Mean residual-channel invocations |  $6.2806$ 

 | Largest observed history | 94 events

 | Objective and gradient source invocations | 372,684

The gradient estimate is approximately  $0.90$  standard errors from its exact value. This is numerical consistency, not a replacement for the unbiasedness proof.

A separate seven-state absorbing-chain calculation gives the exact mean history length  $80/9$ , consistent with the simulation.

Actual stochastic optimization

Using only Born-valued gradient samples, twelve batches of 1,024 histories moved $\theta:1.2\longrightarrow0.120542.$ 

The exact objective diagnostics improved from $0.124523\longrightarrow0.341152,$ 

against the benchmark maximum  $0.343645$ . These exact diagnostics were not supplied to the optimizer.

Training consumed 73,954 simulated source invocations. Independent held-out evaluation consumed another 35,850, yielding objective  $0.3480$  with standard error  $0.01210$ . The complete second experiment used 482,488 simulated source invocations. These are synthetic local-channel calls, not hardware or fault-tolerant gate counts.

The full record is in   path_stationary_control_results.json.

5. The useful failure: burn-in remains the stronger practical baseline here

The comparison materially limits the claim.

 | Gradient method on the 30% reset benchmark | Bias | Expected source calls | Variance

 | Exact finite-history estimator | 0 | 6.0794 | 25.3049

 | Four-update burn-in |  $0.0033674$  | 2.4155 | 2.8126

 | Eight-update burn-in |  $0.0000546$  | 5.4627 | 9.6010

At the tested precision, short burn-in is more economical. The first, 55% reset experiment reached the same conclusion.

I also preserved a complementary size-biased-history estimator. It bounds the output amplitude by spending more work on longer genealogies; the executed one-qubit comparison showed a variance/work exchange, not a total-work improvement.

These failures matter. Removing bias is useful when the truncation error must be controlled rigorously, but exactness alone has not yet bought better control per source call.

6. What survived the primary-source comparison

The mechanism has substantial foundations:

Classical backward-ancestor perfect sampling already uses resets, reverse clocks, extinction and forward reconstruction. arxiv.org

Quantum coupling from the past already exists, including França’s Gibbs-state construction with spectral access. arxiv.org

High-noise local quantum dynamics already has strong classical simulation results based on spacetime percolation. arxiv.org

The exact double-death ancestry process and stochastic derivative ingredients are prior art.

The potentially distinctive completed object is therefore narrower: a physical local stationary-state and control operation for arbitrary noncommuting local channels, with an explicit executable interface, finite work and variance, and the one-quarter path criterion. Its priority and external proof acceptance remain open.

The competing quantum-memory routes are preserved too. Known Schur compression can retain identical samples compactly, while sample-based Hamiltonian simulation gives a sharp reminder that quantum retention does not guarantee linear batch throughput: its established time- $T$  cost is  $\Theta(T^2/\epsilon)$  in the stated regime. arxiv.org+1

Saved proofs and runnable work

   reset_ancestor_control.md — central construction and scope.

   stationary_gradient_independent_proof.md — complete algorithm, quantum exactness, differentiation and resource proofs.

   path_geometry_independent_proof.md — the one-quarter criterion, endpoints, tails and second moment.

  check_path_stationary_control.py — executed lower-reset control experiment.

   path_stationary_control_experiment.md — interpretation, budgets and burn-in comparison.

   STATUS.md — continuity across the preserved constructions and alternatives.

The strongest live opening is now local stationary control with certified finite dependence on the past. The next decisive obstacle is performance: obtaining that certification while reducing the variance and acquisition cost enough to beat a well-chosen approximate evolution, or extending it to useful dynamics whose reset structure is not directly exposed.path_stationary_control_results.jsonCodeOpen file   reset_ancestor_control.mdDocumentOpen file   stationary_gradient_independent_proof.mdDocumentOpen file4 more
