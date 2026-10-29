## Completed: protection governed by the transitions that can carry information out

I pursued a stronger question than extending the eraser: **can protected gates and repeated transfer to fresh encodings remain certifiable when a driven, returning bath gives the physical oscillator unbounded energy support?**

The resulting **bounded-edge protection principle** answers yes at an explicit interaction and control interface. It removes the global noise-norm and invariant-cutoff obstruction encountered in the earlier representation. Both the functional-analysis review and the separate driven-bath/returning-memory challenge accepted the construction at its stated scope.

### The principle

Arrange the protected space into error grades \(P_0,\ldots,P_q\), with \(P_0\) the fresh encoding. Suppose the interaction moves only between adjacent grades, and escape requires crossing the final boundary. Bound those transitions while propagating the motion within each grade—and beyond the protected boundary—unitarily.

For a common edge-norm envelope whose integral over block \(j\)’s **whole physical lifetime** is \(\Theta_j\), the complete-channel comparison satisfies

\[
\boxed{
\epsilon_{\mathrm{dyn}}
\le
\min\!\left\{1,\;
\sum_j\frac{\Theta_j^{\,q_j+1}}{(q_j+1)!}
\right\}.
}
\]

The comparison includes the retained bath, retired blocks and arbitrary references on the declared encoded input domain. Holding and handoff exposure count. An already occupied syndrome cannot obtain a fresh protection order merely by restarting a clock.

The proof follows successive incoming sources through the grades. Once amplitude escapes, its subsequent evolution has norm one; its Hamiltonian need not have a finite global norm. A sharper theorem retains the actual time-ordered edge integral.

This is established in :chatgpt-content-reference{index="3"}[BOUNDARY_CONTROLLED_RENEWAL.md](producer-workspace/BOUNDARY_CONTROLLED_RENEWAL.md), including the exact all-Fock propagator construction. No finite Fock-cutoff approximation is substituted for that existence proof.

### What the construction makes possible

For the two-mode family with \(N=(q+1)^2\) photons per fresh block, the active interaction may be

\[
V=a^\dagger C_a+aC_a^\dagger+
  b^\dagger C_b+bC_b^\dagger ,
\]

where the coefficients are bounded operators on the **complete supplied memory**. They may be driven and noncommuting. The required envelope is

\[
\Theta_j\le
\bigl[\sqrt{N+q}+\sqrt{N+q+1}\bigr]
\int_j\bigl(\|C_a(t)\|+\|C_b(t)\|\bigr)\,dt .
\]

The actual oscillator may leave that number band. The band bounds the interaction **on the protected source space**.

Combined with the constructed logical controls and handoff, this supplies a conditional \(H,T,\mathrm{CNOT}\) circuit interface with renewed logical support. A retired oscillator may return through a bounded spin bus and exchange energy with it. Bath reset, conserved bath charge and permanent retirement are unnecessary for this construction.

There is a meaningful conditional scaling consequence: if the acquired lifetime exposure \(G\) stays below the sufficient regime \(e\sqrt6G<1\), the designated exchange-noise contribution can decrease exponentially in \(q\), while fresh photon supply grows quadratically in \(q\). That does **not** establish corresponding scaling for control duration, preparation or readout.

### Hard challenges and actual readout

The independent physical challenge retained complete outputs and used two different representations:

| Challenge | Computed complete isometry error | Boundary estimate |
|---|---:|---:|
| Driven bus, exact infinite-space displacement kernels, \(G=0.08\) | 0.0184163 | 0.0198125 |
| Returning old oscillator, initially 0 photons | 0.00118343 | 0.002592 |
| Returning old oscillator, initially 64 photons | 0.000970960 | 0.002592 |

In the returning-oscillator comparison, the global interaction norm grew from approximately \(0.201\) to \(0.748\), while the boundary estimate stayed fixed. The old oscillator changed occupation, and the active source populated states beyond the admitted band. These are floating-point diagnostics supporting the analytic argument, not interval certificates or device error rates. The :chatgpt-content-reference{index="4"}[physical review](producer-workspace/INDEPENDENT_REVIEW.md) records the constructions and limitations.

I also completed the operation-level readout bridge. Direct mode counting gives the logical answer for arbitrary coherent admitted syndromes, including the count-conditioned returning-memory update. Under the specified vacuum attenuation and counting model, **zero or one missed photon cannot produce an accepted wrong bit**; an explicit failure flag remains possible.

For the same-actual-record correct-or-flag comparison, the exact half-diamond distance reduces to the norm of a positive accepted-wrong effect. For \(q=1\), it is exactly

\[
\epsilon_{\mathrm{silent}}=\eta^3(1-\eta)^2 .
\]

Destructive flags remain a separate cost and grant no free retry. The missed detection field must genuinely be retired for the thinning model. These distinctions and the independent review are preserved in :chatgpt-content-reference{index="5"}[ACTUAL_RECORD_FLAGGED_READOUT.md](producer-workspace/ACTUAL_RECORD_FLAGGED_READOUT.md).

### What this adds—and what remains physical work

Graded error spaces and canonical error-transparent Hamiltonians are established machinery, as is non-Markovian norm-based fault tolerance. The advance here is the constructed boundary-controlled, complete-memory comparison joined to gates, renewal and actual readout; historical priority for the general formulation is not established. :chatgpt-content-reference{index="0"}

The strong conventional comparison also remains explicit: current finite-energy GKP fault-tolerance work includes preparation, gate and detection noise under its stated independent-Markovian conditions. This construction handles coherent returning memory at a narrower supplied-control interface; it does not establish superiority over that framework. :chatgpt-content-reference{index="1"}

The consequential remaining operational bridge is acquiring **grade-preserving logical and inter-block controls throughout their execution**, with calibrated imperfections and durations that keep exposure useful as protection grows. Fresh encoding, coherent capture where required, holding, collection and reuse still carry their real costs. Directly replacing a bounded spin coefficient by an unrestricted oscillator annihilator needs another estimate.

Proofs, corrections, useful failures, exact checks and actual reviews are saved in place. :chatgpt-content-reference{index="6"}[README.md](producer-workspace/README.md) indexes the tranche. The executable :chatgpt-content-reference{index="7"}[boundary_budget.py](producer-workspace/boundary_budget.py) evaluates time-ordered budgets with exact rational arithmetic, including the loss of protection order for an already occupied syndrome; its physical inputs remain premises.

The completed result makes it possible to certify protected computation in a driven, returning-memory setting that defeated the earlier global-support method, while keeping the implementation frontier explicit.