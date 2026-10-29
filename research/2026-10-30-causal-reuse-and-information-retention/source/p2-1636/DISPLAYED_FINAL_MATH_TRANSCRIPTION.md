# Normally displayed final: formula text projection

Deterministic projection of the normally displayed final and its mathematical annotations. This is not an acquired original proof, code or independent review. Original visible text and private DOM remain preserved separately.

I developed a causal mechanism for reusing syndrome registers, together with a more general bound based on physical accuracy. The intended capability is repeated correction with a smaller supply of clean memory, while preserving the information carried by returning environments.

The construction works under additional, explicit assumptions about the noise generator and the protection of the archive. It has a working finite implementation; it does not yet supply a practical device advantage or a noisy-control threshold.

1. A register that is actually returned for reuse

After each correction round, a reversible operation transfers the coherent syndrome into an archive and returns the temporary syndrome register to  $|0\rangle$ . The next round receives that actual register. The archive retains the history’s correlations with the bath and arbitrary reference systems.

I derived a bound allowing an unknown, repeated finite-bath interaction, interrupted at up to  $r$  positions by arbitrary interactions with other retained memory. Those exceptional interactions can revisit the same memory, fail to commute, and appear in coherent combinations. Their locations do not have to be detected.

The binary specialization has an exact answer. If ordinary rounds emit the same unknown coherent syndrome, the required archive dimension is $D_{n,r}
=
\sum_{k=0}^{r}
(n-2k+1)
\left[
\binom nk-\binom n{k-1}
\right],
\qquad r\le \lfloor n/2\rfloor .$ 

An incremental Schur construction implements the compression during the correction loop. Within the requirement to preserve this entire history family reversibly, the dimension is also necessary.

For illustration, the formula gives:

 | Correction rounds | Permitted departures from the repeated generator | Archive qubits

 | 1,000 | 0 | 10

 | 1,000 | 1 | 20

 | 1,000 | 2 | 29

These are resource calculations, not 1,000-round device simulations. Each row additionally requires the reused syndrome qubit, the source, control and arithmetic workspace, and reliable holding of the archive. Here  $r$  counts changes to the interaction structure; it is not the number of observed logical errors.

2. The stronger opening: accuracy changes the memory requirement

An exact-only approach has a serious failure.

Even with one unknown parameter, no active bath, and bounded total interaction time, varying the timings can produce a syndrome family whose exact span has dimension  $2^n$ . Thus “few unknown physical parameters” alone does not justify small exact storage.

I then derived an approximate causal construction. Its archive size depends on how many representative physical models are needed to cover the unknown model class at the required whole-program accuracy.

With no exceptional interactions, the bound is $m_{\mathrm{archive}}
\le
\left\lceil
2\log_2 d+\log_2 N_\delta
\right\rceil ,$ 

where  $d$  is the active bath dimension and  $N_\delta$  is a covering number defined using the accumulated sensitivity of the actual physical operations.

For a bounded,  $p$ -parameter Hamiltonian family, this yields a bound of the form $m_{\mathrm{archive}}
=
O\!\left(
p\log(1+L/\delta)+\log d
\right),$ 

where  $L$  measures the integrated sensitivity to those parameters.

The compressor does not first estimate the unknown coupling. It works for the declared model family. The error proof compares the complete recycled circuits and retains any imperfectly cleared intermediate register in the actual evolution. It grants no fresh bath or intermediate initialization.

This is the most promising conceptual result of the investigation: the physical accuracy requirement can make a reusable controller possible even when exact universal compression requires the entire raw history. The general construction is analytic; its efficient, robust synthesis remains unresolved.

3. What the executable construction establishes

The implemented example runs 12 correction rounds, with two interactions involving the same noncommuting, reference-entangled memory. Its physical source has a dirty-input completion that can flip the logical state. That action remains present throughout the simulation.

The positive run produced:

Complete history–bath–reference reconstruction error of approximately  $4.42\times10^{-16}$ .

Logical Bell fidelity approximately  $1$  throughout.

Return of the reused syndrome register to zero within floating-point tolerance.

Separate checks cover an exact rational restoration identity and four exact modular span ranks.

The negative case matters equally. When a compiler allowing no exceptional interaction encounters one, its supposedly cleared register has nonzero probability  $1/2$ . Continuing the real circuit with that register reduces logical Bell fidelity to  $1/2$ . The construction therefore preserves the earlier dirty-input failure rather than concealing it in a reference process.

4. What is inherited, and what remains unacquired

Unknown repeated tensor-network states already admit logarithmic compression, and efficient Schur transforms are established constructions. Those predecessors redirected this investigation toward live reuse, returning-memory interventions, and accuracy-dependent control; their underlying compression results are not new Astra discoveries. hub.hku.hk+1 Standard non-Markovian fault-tolerance machinery also remains prior. arxiv.org

The strongest ordinary alternatives remain consequential. A known generator can permit an even smaller archive. Echo or delayed recovery can outperform this scheme for suitable error algebras. Conventional reset can use simpler operations and shorter latency.

The current construction additionally assumes a valid model class, coherent recovery, an isolated archive, and sufficiently accurate compression gates. The inherited bridge does not establish those conditions. Measuring the syndromes, introducing independent entropy repeatedly, or allowing uncontrolled bath access to the archive can eliminate the saving. No reset-energy advantage, practical computing advantage, or hardware threshold has been established.

The next substantial opening is to make the sensitivity-based controller efficient and robust while accounting for its own noise and holding costs. Increasing the finite check count would not resolve that problem.

The complete proofs, comparisons, and evidence boundaries are saved in:

The previous bridge’s reported review scope remains unchanged. These new results have not received an independent analytic review.   THEORY.mdDocumentOpen filecheck_causal_reuse.pyCodeOpen filechecks.jsonCodeOpen file   CONTINUITY.mdDocumentOpen file
