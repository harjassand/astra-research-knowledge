# Pure initialization and the remaining fixed-source gap

## Status

No construction in this branch achieves high-fidelity recovery of the initial
qubit from the homogeneous once-through tracial partial-SWAP stream with the
requested sublinear retained memory and near-linear processing at the
quartic collision scale. The general question remains open in this work.
None of the restricted negative results below is a general causal-receiver
memory lower bound.

The fixed physical source is unchanged throughout: an arbitrary qubit and
reference, $U_{SE}(\theta)=\exp(i\theta\,\mathrm{SWAP})$, fresh independent
carriers $I/2$, chronological access to the actual outgoing carriers, and
discard of the source. No carrier purifier, preparation label, or coherent
return link is available. All errors use the half-diamond convention.

The accepted all-output reference operation remains inverse-dummy/Petz
recovery, with

\[
 r_N=(1-\sin^4\theta)^N,
 \qquad \epsilon_{\rm Petz}=\tfrac34r_N.
\]

Its reverse-order execution retains the bath. That source-specific
recovery guarantee is not replaced by a source-forgetting statement.

## A fully represented pure-initialized fusion receiver

`pure_adaptive_fusion.py` implements a receiver with memory

\[
 M_J=\mathbb C^2_R\otimes Q_J,
\]

initialized in the invariant singlet on $R,Q_{1/2}$. At every encounter it
applies an SU(2)-covariant unitary to $R,Q_J,E$, then a projective branch
instrument retaining $R,Q_{J\pm1/2}$. The branch outcome is classical.
The unitary mixes the two copies of total receiver spin $J$; the outer
spins $J-1,J+1$ are fixed. This is the same complete covariant projective
fusion family as `online/adaptive_fusion.py`, but it does **not** assume a
tracial conditional receiver baseline.

The simulated object is the complete input-reference/source/receiver Choi
state. The reference is time reversed, so the joint state is SU(2)
invariant. Its multiplicity blocks have dimensions $1,3,3,1$, and contain
20 real Hermitian parameters away from the small-spin boundaries. After
adding a carrier, the multiplicities are $1,4,6,4,1$, with 70 real
parameters. Each fixed-magnetic-number physical slice contains at most 16
exterior bitstrings, regardless of $J$. Thus the matrices do not grow
with the retained spin. Adjacent-spin coherence is retained.

For the maximally mixed input, the source remains independent and tracial:
the complete baseline is $I_S/2\otimes\tau_{M_J}$. This follows because
the source and each fresh carrier are jointly tracial before their
collision, and the subsequent receiver operation acts only on the
receiver and carrier. The receiver marginal has two invariant weights,
one on each of $Q_{J-1/2},Q_{J+1/2}$. These weights are carried by the
full Choi calculation rather than forced to agree.

For a normalized Choi state \(\rho_{AB}\), the code evaluates the exact
transpose-channel/Petz entanglement fidelity

\[
 F_P(\rho)=\frac12\operatorname{Tr}\!left[
 \rho(I_A\otimes\tau_B^{-1/2})
 \rho(I_A\otimes\tau_B^{-1/2})\right],
 \qquad \tau_B=\operatorname{Tr}_A\rho,
\]

with the inverse on the support. This formula also returns a
probability-weighted fidelity for an unnormalized branch. The adaptive
policy tested here chooses its branch basis to increase the expected
post-instrument $F_P$ for the joint source-plus-receiver channel. It uses
the known channel coefficients and previous classical outcomes, not a
measurement of the hidden input. The policy is computed from a finite set
of starting directions and numerical local optimization on the sphere.
It is **not** certified as the global optimum over directions or over
policies.

The actual chosen instrument is CPTP. The implementation checks trace,
branch probabilities, invariance of $F_P$ under adding a tracial carrier
and performing the physical source collision, and data processing under
the chosen receiver instrument. Final readout uses the exact all-decoder
formula in `OPTIMAL_SPIN_READOUT.md`, not an assumption that the final
decoder is Petz.

### Executed histories

The initial singlet can be spent on an exact embedding of the first bath
output into $R\otimes Q_1$. The choice

\[
 \mathbf n=(\sqrt3/2,0,1/2)
\]

makes that larger-spin outcome deterministic. For the tested preservation
policy, the next step deterministically returns to $J=1/2$, exactly
retaining the first two outputs. The joint source/receiver Petz fidelity
is one through these two steps; the receiver baseline is then tracial.
The numerical policy subsequently follows the previously tested tracial
fusion behavior. This is an observed policy choice, not a theorem that
all ways of using the initial purity must do so.

| Angle | Prefix | Retained spin in the recorded history | Joint $F_P$ | Acquired $F_P$ | Optimal final acquired $F_e$ |
|---|---:|---:|---:|---:|---:|
| 0.3 | 1 | 1 | 1 | 0.2557201839 | 0.3154991444 |
| 0.3 | 2 | 1/2 | 1 | 0.2613967404 | 0.3313507272 |
| 0.3 | 100 | 11/2 | 0.3250939304 | 0.3223107544 | 0.4821802627 |
| 0.3 | 600 | 17/2 | 0.3218086011 | 0.3218086011 | 0.4820699124 |
| 0.1 | 100 | 11/2 | 0.8689609418 | 0.2518609206 | 0.2731485576 |

These are complete individual classical histories, not estimates of the
average channel fidelity over all histories, and not a physical-device
simulation. The fixed seeds, numerical policy, and full checkpoints are
saved in the accompanying JSON files. The angle-0.3, 600-collision bath
would support the accepted full-bath Petz fidelity above 0.99. The chosen
small-memory policy has discarded most of that capability.

### Costs and scope

The ideal retained quantum space has dimension $2(2J+1)\le2(N+2)$, hence
logarithmically many encoded qubits, plus carrier buffering and coherent
arithmetic workspace. A physical implementation requires coherent CG
transforms, the controlled two-dimensional multiplicity rotation, and
the branch measurement. Efficient Schur/CG circuitry supplies a basis
change; it does not prove that this receiver preserves the payload.
Bounded local controls require the incoming spacing or buffer to pay for
the gate depth. Source waiting, receiver protection, initialization,
calibration, and accumulated gate error must all be charged. No compiled
large-scale control circuit or calibration experiment was executed here.

The matrix representation and candidate operation are useful, but their
small memory cost cannot be combined with an acquisition guarantee that
has not been proved. Pure nonmyopic controls, fresh pure workspace,
general covariant instruments, coherent rather than measured branches,
and general receivers remain outside the negative conclusion of this
diagnostic.

## Large-spin rational rotor: no established intertwiner

The unitary rational spin-$J$ Lax operator

\[
 R_J(u)=\frac{uI+i(\boldsymbol\sigma\cdot\mathbf J+1/2)}
 {\sqrt{u^2+(J+1/2)^2}}
\]

is physically well defined. A crossed spin expression has a normalization
defect that can decrease for large $J$. Neither fact supplies an
intertwining identity that transfers this source's initial logical qubit
to the receiver. The exact ordinary fusion identities use shifted
spectral parameters. The homogeneous real-angle collision family does
not provide those shifts. No replacement physical intertwiner, uniform
error bound in $J,N,\theta$, or appropriate initialization was derived.
The small-cutoff rotor diagnostics therefore cannot exclude a larger
rotor construction, and large-$J$ normalization proximity cannot establish
one.

## Coherent sparse flags: two missing operations

The crossed-filter completion

\[
 K=\frac{cI-2is\Phi}{\sqrt{1+3s^2}},\qquad
 L=\frac{2s(I-\Phi)}{\sqrt{1+3s^2}},
 \qquad W=|0\rangle K+|1\rangle L
\]

is an isometry and obeys

\[
 L^\dagger L\le qI,\qquad q=\frac{4s^2}{1+3s^2}.
\]

Keeping the flags coherently, together with Bell workspace, is a valid
candidate receiver. The probability distribution obtained by measuring
its flags at the end has a standard adaptive Bernoulli upper-tail bound
because the conditional chance of a new one is at most $q$. Consequently
an abstract typical flag subspace can have dimension

\[
 \sum_{k\le K}\binom Nk
\]

with $K$ of order $qN+\sqrt{qN\log(1/\delta)}+\log(1/\delta)$.

Two necessary results are absent. First, recovery of the actual payload
from the flags and workspace after discarding each spent carrier has not
been proved. Second, sparse occupation does not itself implement an
efficient causal compression circuit: naive coherent combinatorial
ranking or sparse-position routing can be superlinear with bounded local
gates. A fully coherent history retains success/failure off-diagonal
operators and is **not** covered by the classical-failure obstruction in
`CLASSICAL_SPARSE_FAILURE_BOUND.md`.

## Resolved material retained

The following separate completed statements remain at their actual scopes:

- `SCHUR_BOUNDARY.md`: ordered bath multiplicity/adjacent-spin coherence;
  the measured-J Schur-compression obstruction; the exact crossed-filter
  representation and its exponential all-success cost.
- `FUSION_THEORY.md`: a concrete spin-growth instrument, its physical
  implementation conditions, the ordinary-fusion spectral-shift gap, and
  the all-decoder loss caused by measuring every consecutive pair's
  singlet/triplet label.
- `OPTIMAL_SPIN_READOUT.md`: the exact optimal final covariant readout
  from a qubit times a spin, including coherent adjacent-sector decoding.
- `CLASSICAL_SPARSE_FAILURE_BOUND.md`: an all-continuation bound for
  measured/dephased success/failure histories that discard the success
  carrier into the specific folded statistic.
- The saved fixed-J and rotor scans are finite diagnostics only.

## Primary machinery

- Bacon, Chuang, Harrow, *Efficient Quantum Circuits for Schur and
  Clebsch-Gordan Transforms*, PRL **97**, 170502 (2006),
  https://arxiv.org/abs/quant-ph/0407082 .
- Bisio, D'Ariano, Perinotti, Sedlak, *Memory cost of quantum protocols*,
  PRA **85**, 032333 (2012), https://arxiv.org/abs/1112.3853 .
- Yang, Nepomechie, Zhang, *Q-operator and T-Q relation from the fusion
  hierarchy*, Phys. Lett. B **633**, 664–670 (2006),
  https://arxiv.org/abs/hep-th/0511134 ; its fused product explicitly
  contains shifted spectral parameters.

The accepted source-specific acquisition theorem is in
`output/tracial_acquisition/partial_swap_theory.txt`. The present record
does not claim to resolve the fixed-source causal-recovery question.

