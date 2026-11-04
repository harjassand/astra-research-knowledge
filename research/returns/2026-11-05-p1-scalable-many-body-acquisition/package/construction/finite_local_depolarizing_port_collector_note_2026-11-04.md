# Finite local acquisition of pure depolarizing output ports

## Scope and conclusion

This note completes the finite physical acquisition interface needed by the continuous-Hamiltonian reverse-reset decoder developed in `agent_independent/continuous_hamiltonian_reverse_reset_decoder.txt`. The result is conditional on the actual calibrated pure-vacuum, losslessly coherently delivered Markov output ports specified below, and on programmable finite-dimensional cascaded receivers. It does not infer such ports from a reduced master equation.

For fixed local dimension q, each site and time bin can be collected into a locally initialized q²-level chronological receiver. All control matrices reduce to fixed matrices multiplied by two explicit scalar waveforms. The receiver output is then converted by a constant-dimensional isometry into a synthetic reset flag and an exported copy of the old source qudit. Photon counting, exact photon arrival-time resolution, and access to a microscopic source SWAP are unnecessary. The complete acquired source–receiver channel, including arbitrary reference systems, has a chosen error η with finite amplitude, finite slew, finite program length, finite coefficient precision, and finite endpoint gates.

Combined with a local coherent-dilation splitting estimate, the entire acquisition interface has polynomial cost in n, inverse target accuracy, inverse mixing margin, and the specified Hamiltonian norms. The polynomial bounds here are deliberately conservative. They establish an algorithmic interface and do not establish favorable hardware economics or a microscopic finite-bandwidth implementation of the Markov model.

## 1. Actual source interface and local collector

Let W₀=I and W₁,…,W_{q²−1} be a trace-orthogonal generalized Weyl basis, with Tr(Wμ†Wν)=qδμν and Tr Wμ=0 for μ≠0. The actual, phase-calibrated vacuum ports have coefficients

\[
L_\mu=\frac{\sqrt r}{q}W_\mu,\qquad \mu=1,\ldots,q^2-1.
\]

Their reduced generator is r(Rτ−id), where τ=I/q and Rτ(ρ)=τ Trρ. Its noise-only channel over duration t is

\[
\mathcal E_t=e^{-rt}\,\mathrm{id}+(1-e^{-rt})\mathcal R_\tau.
\]

The physical photon-count rate of these particular traceless Weyl ports is

\[
c=r(1-q^{-2}),\qquad \sum_\mu L_\mu^\dagger L_\mu=cI.
\]

This physical rate c is distinct from the reset parameter r in the equivalent finite-channel decomposition below.

Apply the established N1732 receiver construction to this q-dimensional noise-only source on a bin [0,Δ]. Use a guide regularization e∈(0,1), and write

\[
P=\Phi_q,\quad Q=I-P,\quad a(t)=(1-e)e^{-rt},
\]

\[
\rho_t=a(t)P+[1-a(t)]I/q^2
=\lambda_0(t)P+\lambda_1(t)Q,
\]

\[
\lambda_0(t)=\frac{1+(q^2-1)a(t)}{q^2},\qquad
\lambda_1(t)=\frac{1-a(t)}{q^2}.
\]

All guide matrices commute. Consequently the N1732 gauge W(t) is the identity. Its source no-jump coefficient is G=−cI/2, so the receiver Hamiltonian H_M(t) is exactly zero. On the virtual reference–source space let Aμ=I⊗Lμ. Since PAμP=0, the receiver coefficients are explicitly

\[
C_\mu(t)=-\left[
QA_\mu Q+
\sqrt{\lambda_1(t)/\lambda_0(t)}\,PA_\mu Q+
\sqrt{\lambda_0(t)/\lambda_1(t)}\,QA_\mu P
\right]^T.
\]

The transpose uses the fixed computational basis on the receiver's two q-level registers. These registers initially form their own local Bell state. They are initially independent of the source and any reference. No dense n-body guide is ever formed.

The uniform positive floor is μ=e/q². With ℓ=√r/q, s=Σμ||Lμ||²=c, g=||G||=c/2, and b=2g+s=2c, the N1732 bounds give

\[
\|C_\mu(t)\|\le M:=\sqrt{r/e},
\]

\[
\|\dot C_\mu(t)\|
\le \frac{2cq^2\sqrt r}{e^{3/2}}
\le \frac{2q^2r^{3/2}}{e^{3/2}}.
\]

The uniform floor follows from unitality; it has no exponential dependence on the bin duration.

### Completed endpoint operation

Put a₀=e^{−rΔ}. Let λ₀⁽⁰⁾=[1+(q²−1)a₀]/q² and λ₁⁽⁰⁾=(1−a₀)/q², and let λⱼ⁽ᵉ⁾ be the regularized guide eigenvalues at Δ. The endpoint contraction is

\[
F=f_0P+f_1Q,\qquad
f_j=\sqrt{(1-e)\lambda_j^{(0)}/\lambda_j^{(e)}}.
\]

Complete F with its failure branch, and supply the prescribed fixed receiver state on failure. This is a deterministic completely positive trace-preserving channel. The N1732 theorem gives its error against the canonical Stinespring channel of EΔ as

\[
\eta_{\rm reg}
\le 2\sqrt{2\left(1-\sqrt{1-e+e/q^2}\right)}+2e
\le 2\sqrt{2e}+2e.
\]

The guarantee includes the residual source and arbitrary reference, rather than only a Bell-input fidelity. This is why it composes across interacting sites and bins. The exact successful guide identity is a mathematical comparison, not an exact heralded recovery promise for the locally initialized physical receiver.

For any desired local total error 0<η≤1, choose e=η²/256. Then η_reg≤η/4, leaving explicit budgets for the following finite implementation steps.

## 2. A complete finite control budget

### Finite mesh

The inherited sufficient linear-interpolation mesh bound for channel error ζ is

\[
m_{\rm mesh}\ge
\frac{2b(g+5s)\Delta^2}{\zeta\mu^2}
=\frac{22c^2q^4\Delta^2}{\zeta e^2}.
\]

With ζ=η/4, take

\[
m_{\rm mesh}
=\max\left\{1,\left\lceil
\frac{88c^2q^4\Delta^2}{\eta e^2}
\right\rceil\right\}.
\]

Thus m_mesh=O_q(1+r²Δ²η^{−5}). Each mesh sample uses fixed q²×q² matrices and two scalar factors. Evaluation of exponentials and square roots to the chosen finite precision has polynomial bit cost. The fixed-q matrix dimension does not grow with n.

### Finite turn-on and turn-off

It remains necessary to start and finish at zero coupling with finite slew. For a cascaded source and receiver, the jumps are Jμ=Lμ+Cμ and the cross Hamiltonian is

\[
H_{\rm cross}=\frac{1}{2i}\sum_\mu(C_\mu^\dagger L_\mu-L_\mu^\dagger C_\mu).
\]

If two receiver coefficients have norm at most Mμ and differ by δμ in operator norm, direct expansion of the dissipator and commutator gives

\[
\|\mathcal L_C-\mathcal L_{\widetilde C}\|_\diamond
\le \sum_\mu(6\ell_\mu+4M_\mu)\delta_\mu.
\]

A receiver Hamiltonian discrepancy adds 2||δH_M||. The dissipator estimate used here is

\[
\|D[A]-D[B]\|_\diamond
\le2(\|A\|+\|B\|)\|A-B\|.
\]

Let the first and last ramp durations be τ, with

\[
\tau=\min\left\{\Delta/4,\frac{\eta e}{160cq^2}\right\}.
\]

Replace the interpolated waveform by a straight ramp from zero to its value at τ and a straight ramp from its value at Δ−τ to zero. Its amplitude remains at most M. On either ramp, the difference from the original bounded waveform is at most 2Mμ. Hence the generator difference is bounded by

\[
B_{\rm ramp}=12s/\sqrt\mu+8s/\mu
\le20cq^2/e.
\]

The two ramps together contribute at most 2τ B_ramp≤η/4 in channel diamond norm, using contractivity and the Duhamel bound for time-dependent Markov semigroups. Inserting the ramp endpoints adds at most two intervals to the mesh. The slew is bounded by

\[
\max_\mu\|\dot C_\mu^{\rm finite}\|
\le\max\left\{\frac{2cq^2\sqrt r}{e^{3/2}},\frac M\tau\right\}
=O_q\left(\frac{\sqrt r}{\eta\Delta}+\frac{r^{3/2}}{\eta^4}\right).
\]

The peak is at most 16√r/η. These are finite Markov coefficients, not a bound on an ultraviolet-complete system–field Hamiltonian.

### Coefficient precision and calibration

Suppose each implemented receiver coupling differs from its finite target by at most ξ uniformly, with ξ≤M. Allowing the perturbed amplitude to be M+ξ gives the conservative bound

\[
\eta_{\rm cal}\le
\Delta(q^2-1)(6\ell+6M)\xi
+2\Delta\|\delta H_M\|.
\]

For zero unintended receiver Hamiltonian, it suffices to choose

\[
\xi\le\min\left\{M,
\frac{\eta_{\rm cal}}
{\Delta(q^2-1)(6\ell+6M)}\right\}.
\]

Take η_cal≤η/8. The specification includes coherent phases and channel labels. Agreement of a measured reduced Lindbladian alone does not certify this port calibration.

Actual source-coefficient uncertainty can also be budgeted at the joint source–receiver generator: for a source-coupling error νμ and fixed receiver bound Mμ, the same expansion yields a contribution at most (4ℓμ+6Mμ+2νμ)νμ per channel, plus 2||δH_S|| for Hamiltonian error. Integrate these bounds over the relevant physical horizon. These are actual coefficient uncertainties; hidden loss or a mixed input field is outside this error model and requires its own analysis.

### Endpoint gates and total local error

Prepare the receiver Bell state, realize the contraction completion, and apply the finite environment isometry below with constant-dimensional gates, with total channel error at most η/8. A unitary approximation of operator error θ causes channel error at most 2θ; standard finite universal gate synthesis at fixed q therefore suffices. Initialization error is part of this endpoint/initialization budget. The allocations are

- guide regularization and completed endpoint idealization: ≤η/4;
- finite interpolation: ≤η/4;
- two finite ramps: ≤η/4;
- actual coefficient error: ≤η/8;
- initialization and endpoint gate error: ≤η/8.

Their sum is at most η. These budgets can be reallocated; none is silently taken to zero.

## 3. Constructing the reset/export instrument from the collected memory

The exact noise-only channel has a minimal Weyl Kraus representation

\[
K_0=\sqrt{p_0}I,\quad
K_\mu=\sqrt{p_1}W_\mu\quad(\mu\ne0),
\]

\[
p_0=\frac{1+(q^2-1)a_0}{q^2},\qquad
p_1=\frac{1-a_0}{q^2}.
\]

A known fixed-q basis transformation places the canonical collected environment into this Kraus-label basis. The desired nonminimal dilation is

\[
V_{\rm reset}|\psi\rangle
=\sqrt{a_0}|\psi\rangle_S|0\rangle_F
+\sqrt{1-a_0}|1\rangle_F|\Phi_q\rangle_{SA}|\psi\rangle_B.
\]

The no-reset environment is a one-dimensional sector, while the reset environment has q² states indexed by (a,b). The isometry from the q²-dimensional Weyl-label environment to this 1+q²-dimensional direct sum is explicit. Its entries are

\[
u_{0,0}=\sqrt{a_0/p_0},\qquad u_{0,\mu}=0\quad(\mu\ne0),
\]

\[
u_{ab,\mu}=\frac1{\sqrt q}\overline{(W_\mu)_{ab}}
\quad(\mu\ne0),
\]

\[
u_{ab,0}=\frac{\sqrt{1-a_0}}{q\sqrt{q p_0}}\,\delta_{ab}.
\]

The isometry entries obey u†u=I: nonidentity column orthogonality is the Weyl trace-orthogonality relation; identity-to-nonidentity inner products vanish by Tr Wμ=0; and the identity column has squared norm [a₀+(1−a₀)/q²]/p₀=1. The transformed reset Kraus operators are

\[
R_{ab}=\sqrt{(1-a_0)/q}\,|a\rangle\langle b|,
\]

which proves the displayed reset/export dilation on every unknown input, including inputs entangled with other sites and references.

Measuring only F yields a reset with probability 1−e^{−rΔ}, independently of the input. On that branch, B contains the old source qudit, and S–A is a fresh Bell pair. Discarding A leaves S in τ independently of B and the former source reference. On the no-reset branch the source is unchanged. This is exactly the mixed-τ SWAP/reset instrument required by the reverse-reset history analysis. Its flag is synthetic: it is a Kraus decomposition of the acquired finite channel and is not the physical photon-count record. The actual physical c and synthetic reset rate r must not be identified.

Applying this finite gate and flag measurement after an η-accurate complete collector produces the complete flagged instrument to the same error η by contractivity. The construction does not need an identity photon port, a photon-number measurement, or time-tagged photon capture.

## 4. Local coherent-dilation splitting for an interacting Hamiltonian

Now consider n sites with known possibly time-dependent H(t)=Σ_X h_X(t). Define

\[
\chi=\max_i\sup_t\sum_{X\ni i}\operatorname{osc}(h_X(t)),
\qquad \operatorname{osc}(h)=\lambda_{\max}(h)-\lambda_{\min}(h).
\]

χ includes on-site Hamiltonian terms. The actual total photon rate is R=nc≤nr. It is a scalar rate, so the vacuum-output expansion has state-independent Poisson event count m with mean RΔ. Its marked event histories and event times occupy mutually orthogonal field sectors. Every normalized marked event is a local Weyl unitary. For any such local W_i,

\[
\|[H(t),W_i]\|
\le\sum_{X\ni i}\operatorname{osc}(h_X(t))\le\chi.
\]

This follows by centering each h_X at the midpoint of its spectral interval; disjoint terms commute. Duhamel's identity gives

\[
\|U(t,s)W_i-W_iU(t,s)\|\le\chi|t-s|.
\]

The same bound holds for a local reset isometry J_i because disjoint terms intertwine and each touching centered term contributes twice its norm. However, the actual Weyl-port proof suffices and avoids changing the physical dilation.

Within a bin, move all Hamiltonian evolution to its end, leaving the actual marked noise-only events in their original time sectors. For a history containing m events, a telescoping sum bounds the conditional isometry difference by χΔm. Squaring and integrating orthogonal histories therefore gives

\[
\|V_{\rm continuous}^{\rm bin}-V_{\rm split}^{\rm bin}\|
\le\chi\Delta\sqrt{R\Delta+(R\Delta)^2}.
\]

Consequently K=T/Δ bins obey the complete channel bound

\[
\|\mathcal V_{\rm continuous}-\mathcal V_{\rm split}\|_\diamond
\le2\chi T\sqrt{R\Delta+(R\Delta)^2}.
\]

This local refinement was independently supplied by the reverse-reset collaborator and audited here for the actual Weyl jumps. An independent global-norm fallback uses ||H J−J H||≤2Λ, where Λ=sup_t||H(t)||, and gives the earlier 4ΛT bound. No comparison between the decomposition-defined χ and 2Λ is required. No derivative bound on H(t) is needed for this splitting inequality itself. Efficient classical description and Hamiltonian simulation of the specified H(t) remain separate requirements of the decoder.

For χ>0, an adequate integer choice for splitting target η_split is

\[
K\ge\max\left\{1,RT,
\frac{8\chi^2RT^3}{\eta_{\rm split}^2}\right\},
\qquad \Delta=T/K.
\]

Indeed RΔ≤1 and the resulting error is at most η_split. If χ=0, this splitting error is zero. R=0 provides no emitted information and is not an acquisition regime.

## 5. Total interface resources and composition

There are B=nK local collector uses. Set η_loc=η_collect/B, choose e=η_loc²/256 for every use, and apply the preceding local construction. The complete-channel telescoping bound is then η_collect, with no factor exponential in n. The physical continuous-H source need not be controlled or paused: its field is processed by the receiver designed for the split comparison, and the coherent-dilation estimate plus contractivity transfers the guarantee back to the actual source.

A straightforward hardware schedule uses nK preinitialized q²-level receiver banks, each active on its assigned incoming interval, with zero-coupling endpoints. Banks can lie sequentially on each lossless output line and have schedules shifted by their known propagation delays. Endpoint operations and synthetic-flag measurements can be delayed until all acquisition ends. This avoids assuming instantaneous computation or instantaneous switching on a bank that is still interacting with the field. Equivalent recycling implementations may reduce live collector hardware but must price routing, delay, and storage. The simple construction already uses only polynomially many protected local systems.

For fixed q, sufficient resource bounds are:

| Resource | Bound or explicit requirement |
|---|---|
| Local receiver banks | nK, each q² levels; O(nK) qudits plus constant-size ancillas |
| Retained exports and flags | At most nK old-state qudits and nK classical flags |
| Bell preparations and endpoint conversions | O(nK) constant-dimensional operations, each with its assigned finite error |
| Control intervals | O_q(nK[1+r²Δ²η_loc^{−5}]) |
| Peak individual port coupling | ≤16√r/η_loc |
| Slew | O_q(√r/(η_locΔ)+r^{3/2}/η_loc⁴) |
| Simultaneously active ports | n(q²−1) with the simple bin schedule |
| Coefficient precision | The explicit ξ bound above; logarithmically many bits in the polynomial inverse tolerance |
| Classical control computation | Fixed-size matrices and elementary scalar functions per sample |
| Physical collection time | T plus the specified transport and processing latency |
| Protected storage lifetime | Collection, transport, and the subsequent inverse-history decoding runtime |

At fixed local χ and r, the bin count is O(1+nrT+nχ²rT³/η_split²); hence nK=O(n+n²rT+n²χ²rT³/η_split²). If the reverse-reset theorem gives T=O(log(n/ε)/(r−β)) with an inverse-polynomial positive margin r−β, then all these costs are polynomial. The η_loc-dependent amplitude and program exponents can be severe; they are sufficient upper bounds and have not been optimized by a geometric mesh.

Noiseless protected storage is an explicit ideal resource. An implementation with storage or gate noise must allocate its total error across the entire time and operation count, or use a specified fault-tolerant storage architecture. In particular the decoder cannot postpone the quantum-memory lifetime cost until after the claimed readout. This note supplies the acquisition interface; the parent decoder note supplies the reverse-Hamiltonian simulation and its computational bill.

## 6. Why a stationary mirror alone is insufficient

A stationary transposed absorber should not replace the construction without an initialization and recovery argument. For a Hermitian-jump representation of unital depolarizing noise, the stationary mirror has jumps L_S−L_Rᵀ and opposite transposed Hamiltonian. Its Bell state is dark, but the full cascaded semigroup is also unital and has a maximally mixed stationary state. A dark Bell state therefore does not establish attraction from a locally initialized receiver or transfer of an arbitrary unknown source/reference input. This is consistent with existing coherent-absorber formulations that start in a purification of the stationary source state. The finite guide regularization, local product initialization comparison, and completed endpoint operation are what supply the missing operation here.

## 7. Provenance, comparison, and claim boundaries

The receiver theorem and its finite mesh bound are inherited machinery, not a newly claimed theorem. This note specializes them to fixed-q depolarizing segments, gives explicit waveforms and ramps, and supplies the finite environment isometry that realizes the exact reset/export instrument used by the new decoder. The locality-improved coherent-dilation splitting bound is independent collaborative work, with the actual Weyl-port version checked here.

Ordinary direct source SWAP would be preferable if such access were available. It is not granted by an output-only interface. Storing an entire exponentially represented Stinespring history and invoking a generic recovery map is also not an efficient construction. The intended additional consequence comes from the separate reverse-reset decoder theorem, which uses a polynomial record and reverses the known local dynamics. This note alone does not claim arbitrary-H recovery outside that theorem's r>β sufficient regime, a universal advantage over quantum repeaters or ordinary error correction, a collection-efficiency threshold, or practical device economics.

### Governing source

- Astra Research, N1732 governing card: https://github.com/harjassand/astra-research-knowledge/blob/main/knowledge/current/packets/N1732.json
- Complete governing source, `P1_CAUSAL_TRANSDUCTION_COMPLETE_RETURN.txt`: https://github.com/harjassand/astra-research-knowledge/blob/main/research/2026-11-04-causal-state-interface-constructions/source/P1_CAUSAL_TRANSDUCTION_COMPLETE_RETURN.txt
- Relevant source sections: guide and receiver construction, lines 101–184; local initialization and complete-isometry comparison, 186–208; completed endpoint and diamond guarantee, 212–254; uniform unital floor and finite resource bounds, 354–406. The source reports a completed derivation; the original large report, archive and audit attachments were not independently reacquired for this note.

### Primary contextual research

- Mankei Tsang, “Quantum reversal: a general theory of coherent quantum absorbers,” Quantum 9, 1650 (2025): https://quantum-journal.org/papers/q-2025-02-26-1650/ ; manuscript https://arxiv.org/abs/2402.02502 . The construction's initial joint pure state purifies the source stationary state, so its stationary absorber statement does not itself supply locally initialized arbitrary-input acquisition.
- Beni Yoshida and Alexei Kitaev, “Efficient decoding for the Hayden–Preskill protocol” (2017): https://arxiv.org/abs/1710.03363 . The decoder and access model are relevant ordinary comparisons; their small-message dependence must not be relabeled an efficient decoder for an arbitrary n-qudit payload.

Prepared 2026-11-04 by the interface-theory collaborator. Mathematical interface note; no experimental performance claim.
