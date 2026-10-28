# Sources and comparison scope

The common cleared scientific-access revision remains
`63867607218adef378d727987fd92aa7dc42eb5c`. This is a parent-authorized
cross-route construction after both initial sol8 choices were recorded.
The old corpus-first EA/frame work and all earlier folders remain frozen.

The governing local input is the peer's acquired real-spin reflection-positive
gate in `obstruction_first/continuation/local_gibbs_gate.py`, together with
`data/actual_cp_instrument_delta001.npz`. Both were read without edits and
copied into this folder's `sources/` for offline replay. The snapshot manifest
records original paths and exact bytes. The source module SHA256 is
`caf574429549526c65d62e17d850f513193a387522b137e626df3d3a37199231`; the NPZ
SHA256 is `a381234dcc61800caf621bfa2f129ff8929f0be451b7d7dd6e3c17fa79b3fee7`.
An explicit exact unitary check, rather than spectrum matching alone, identifies
that model with the standard spin-two bond used here.

The long-ring target contract is the all-spin thermal criterion discussed in
[Tasaki's current primary exposition](https://haltasaki.github.io/writings/AI/OpenAI_Haldane.html)
and its [continuous-time text](https://haltasaki.github.io/writings/AI/OpenAI_Haldane_CT.pdf),
read by the peer with the October19 correction/version retained there. Its
Theorem6.2 requires spatial S(L,beta) and temporal T(2L,beta), preserving the
factor two in the second ring size. The analytic criterion and its all-spin
extension are prior input, not a theorem invented in this folder. Neither
required cold input is asserted from this folder's local positive factor.

The strongest ordinary comparison for sign-free numerical thermodynamics
includes general-spin cluster and directed-loop stochastic series expansion:

- [Todo and Kato, Cluster algorithms for general-S quantum spin systems,
  cond-mat/9911047v2](https://arxiv.org/abs/cond-mat/9911047v2),
  Phys. Rev. Lett.87,047203(2001). The peer preserved/read the primary paper;
  its spin-two gap estimate is numerical, not the missing rigorous lower gap.
- [ALPS directed-loop SSE implementation documentation](https://alps.comp-phys.org/documentation/methods/qmc/sse_old/)
  explicitly supports arbitrary spin and cites the established directed-loop
  algorithms. This is not a newly sign-free problem.
- [StochasticSeriesExpansion.jl](https://github.com/lukas-weber/StochasticSeriesExpansion.jl),
  pinned current main `0ee4bb3e78ad90306d594978e0ad405edebe8961` (retrieved
  October28). The README and actual `src/models/magnet/magnet.jl` are preserved.
  The latter's Git blob is `72278f25add99c718530db25bd74847417246c78` and was
  verified from the saved bytes. Its `generate_bond_hamiltonian` implements
  the target with S=2,J=1,d=0, zero fields/anisotropies. The implementation,
  rather than the prose formula in its docstring, was used for that match.
  The code uses an ordinary SSE/abstract-loop framework; it was inspected,
  not installed or benchmarked here. SSE has no million-slice Trotter debt.

Thus the acquired positive local factor is an exact implementation interface,
not a new solution of a sign problem or an efficiency advantage over SSE.
Statistical QMC output does not by itself provide the deterministic interval
and all-mode counting contract needed for the rigorous bootstrap. Conversely,
this folder supplies no theorem that an appropriately certified QMC method
cannot provide that contract.

The ordinary deterministic comparison also includes thermal MPO/transfer
compression and stronger energy relaxations, including the peer-reviewed
thermal area-law algorithms and current matrix-exponential-decay work retained
by the peer, and
[Kull et al., Lower Bounding Ground-State Energies ... Through the Renormalization Group,
2212.03014v3](https://arxiv.org/abs/2212.03014v3).
These methods can exploit the actual state/environment instead of preserving
every rare local tensor entry. The local rank test here is therefore not
a lower bound on those methods. No acquired cold spin-two relative-trace
enclosure from such a method is supplied in this folder, and no claim that
the methods must fail is made. The peer's distinct vacuum-Krylov/tail route
also addresses a trace-specific interface and is not reproduced here.

The physical-frame witness uses established operations:

- [Affleck, Kennedy, Lieb and Tasaki, Valence Bond Ground States in Isotropic
  Quantum Antiferromagnets, CMP115,477--528(1988)](https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-115/issue-3/Valence-bond-ground-states-in-isotropic-quantum-antiferromagnets/cmp/1104161001.pdf)
  supplies the valence-bond construction framework. Here its ordinary spin-two
  Clebsch-Gordan tensor is simply a trial for the different Heisenberg
  Hamiltonian. The exact finite-ring norm/energy formula is derived and checked
  in the owned code; no AKLT gap theorem is transferred to Heisenberg.
- [Dowling, Doherty and Bartlett, Energy as an Entanglement Witness for Quantum
  Many-Body Systems, quant-ph/0408086v3](https://arxiv.org/abs/quant-ph/0408086v3),
  Phys. Rev. A70,062113(2004), is recognized primary prior art for the energy
  entanglement-gap/thermal-witness principle. The present application is a
  quantified test of a proposed physical product-frame compiler, not a new
  entanglement-witness principle.

The exact support fooling-set and inverse-minor arguments are elementary
nonnegative-factor/rank tools. The scientific contribution claimed here is
their acquired application to the actual positive local tensor and the
separate cold physical-frame exclusion. No exhaustive novelty search,
publication claim, independent full audit, hardware validation, or practical
speedup is claimed.
