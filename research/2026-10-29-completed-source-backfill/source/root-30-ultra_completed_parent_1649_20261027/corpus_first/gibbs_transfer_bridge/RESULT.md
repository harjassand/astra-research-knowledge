# Actual positive Gibbs transfer, with an acquired compiler applicability test

The actual spin-two gate has an exact positive periodic transfer with no
spurious readout modes. This closes a real algebraic interface left open by
the local CP map's non-EB witness. It does not acquire an efficient cold
long-ring contraction or the required thermal purities.

The completed construction and tests are:

- An explicit exact unitary identifies the acquired Cartesian real-spin source
  with the standard bipartite Marshall gauge. For 0<=delta<=1/2 the actual
  quadratic gate has nine entrywise nonnegative product factors, minimal for
  delta>0. A positive similarity makes every factor rational at rational
  delta. No reset, depolarization, or scalar normalization is discarded.
- The factors give an entrywise nonnegative T_N with the exact all-size identity
  Tr(T_N^m)=Z_(2m),N(beta), beta=Ndelta. There is no overcomplete-image
  projection or extra hidden-mode trace. The 9^N history dimension and the
  spatially powered 25^m virtual dimension remain.
- The exact exponential gate separately has a minimal 25-term nonnegative
  matrix-unit factor. Its minimal rank follows from an exact generator-word
  span check through degree four. It supports the same trace identity with
  25^N histories. The peer's newer exact-exponential 589043-slice representative
  budget is not combined with the quadratic gate's nine factors.
- The attempted uniform relative-entry local compression has an exact
  obstruction. At delta=.001 and delta=64/2387589, a 25-by-25 minor in one
  actual 225-by-225 tensor cut remains invertible below 25% componentwise
  relative perturbation. Rank below25 cannot meet the proposed approximately
  3.27e-12 local budget for the representative quadratic n128,beta64 input.
  Exact support fooling sets have sizes24 and21. Their tensor products impose
  24^m/21^m positive-rank lower bounds on uncontracted boundary products.
  None of these is a global closed-trace compression impossibility.
- Transplanting a one-spin physical PSD product frame is decisively excluded
  for a cold-state reconstruction. An independently built ordinary spin-two
  AKLT tensor of bond dimension3 gives an exact finite periodic trial on
  every even n>=4, with energy per bond strictly below -4.5. Consequently,
  at beta64 the actual Heisenberg Gibbs state is at trace distance greater
  than **3039/64000=0.047484375** from every fully separable state. At beta96
  the lower bound is **4639/96000**. The finite-ring transfer normalization,
  independent four-site vector replay, rational log5 bound, and variational
  argument are all preserved. No64-site trial energy was transferred to
  another ring length.

This last conclusion concerns mixtures of physical one-spin PSD products.
The acquired worldline factors are nonphysical matrices, so their positivity
survives it. Entangled block frames, thermal MPOs, or scalar-only transfer
methods also escape that particular exclusion. They still need an actual
task-specific tail or relative-trace certificate at the target temperature.

The ordinary comparator is strong: Marshall positivity and arbitrary-spin
SSE/cluster QMC predate this work, and current public code already implements
the exact spin-two Hamiltonian without a million-slice discretization.
Thermal MPO/transfer and renormalization methods can exploit actual environments
instead of the uniform-entry contract tested here. No speedup over these
methods, new tractability class, or novelty of positivity/AKLT/energy witnesses
is asserted. The pinned implementation and primary comparison sources are in
`SOURCES.md`.

`PROOF.md` gives the complete acquired mathematics. The seven-code replay
checks the symbolic gate, source conjugacy, periodic orientation, exact support
and inverse minors, distinct exponential factor, and finite-ring AKLT formula.
SVD data are explicitly diagnostic; they are not used as certificates.

The cold inputs
S(L,beta)=Z_(2L)(beta)/Z_L(beta)^2 and
T(2L,beta)=Z_(2L)(2beta)/Z_(2L)(beta)^2 are **NOT_ACQUIRED**. The spin-two
uniform gap is **NOT_ACHIEVED**. The useful endpoint is an actual positive
representation plus precise reasons why two natural finite-frame/local
compression transplants do not finish the long-ring task. All earlier
completed folders remain frozen; this folder is the complete owned extension.
