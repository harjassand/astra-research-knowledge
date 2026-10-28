# Acquisition costs and an equally informed comparison

The required output is the connected scalar
`C_beta=log T512(beta)-2log T256(beta)`, followed eventually by final
`T512(96)`. An ordinary comparator is entitled to target this same connected
quantity, share extensive normalizations, use every accepted warm input and
every newly acquired source array, and retain all acquisition work. Comparing
this output only against separately precise absolute free energies would be
unfair. No practical speedup or novelty clearance is claimed.

## Measured local work

`results/cycle6_moments_exact_degree192.json` records25 modular passes per
I/P physical six-cycle. Their wall times are223.787s and207.802s, total
431.589s on the available runtime with BLAS/OMP threads1. The largest
magnetization sector is1751x1751:24.53MB per int64 dense array. Multiple
arrays coexist during sparse multiplication/modular reduction. Process peak
RSS was not instrumented; memory is not reported as a measured peak.

This is a complete small-cycle input to an all-ring operator identity,
not a sampled low-energy calculation. Its192nd-degree Taylor/Chebyshev tails,
closing bond, physical scales5^n, both source sectors, and every omitted
spatial mode are paid in the proof. The accepted open1--6 and twisted4 arrays
are supplied evidence; their earlier acquisition cost is not reclassified as
new work or erased from a lifetime comparison. Source snapshots and hashes
are in `sources/ACCEPTED_INPUTS.json`.

The independent Fraction consumer took.0493s. The richer Chebyshev interval
consumer took7.00s for beta.75,1.5,3,6. It exactly converts the supplied power
moments to Chebyshev moments and pays every omitted coefficient. It does not
acquire new physical spectra by evaluating those arrays at more temperatures.

Additional exploratory work is retained and charged:

- New complete endpoint-spin moments on open2--6 through degree192:
  194.429s, with exact analytic controls on open2/3.
- A numerical SU(2) message proposer and fugacity enrichment: runs.58--3.92s
  for each recorded scalar grid, plus triplet proposals and controls. These
  are discovery data, not certified pressure inputs.
- Four-site exact I/P construction controls and all-source consistency checks.
- Derivation, source reading, failed probes, independent replay and documentation.

The source endpoint-spin arrays are available for a later nontrivial-sector
trial construction. Their cost is included even though the first successful
connected input does not need them.

## New message interface

On the unit-time history measure, the kernels satisfy
K_b=D_sqrt(b) K_1 D_sqrt(b), where D_t multiplies a k-event history by t^k.
This is a kernel/form identity on the finite-message domain; D_t need not
be bounded. The finite norms and full acquisition cost are in NEXT_DEPTH.md.
For scalar messages

    f_(r,a)=D_(sqrt(b)*r) K_1 D_a K_1 v,

Gram entries are literal open4 traces with bond couplings(a,b r s,c),
Rayleigh entries are open5 traces(a,b r,b s,c), and residual entries are
open6 traces(a,b r,b,b s,c). Thus trial rank can grow while the largest
physical readout remains six sites. This is an exact finite acquisition
interface, not a supplied noise model or a claim that these trial families
are complete. Numerical enrichment reduces the recorded scalar variance but
has not acquired a fine pressure interval. The successful connected readout
only uses the simpler existing invariant Krylov message.

## Strong ordinary comparators and remaining debts

MED, BS-CMI, thermal MPOs, QBP/Araki free-energy algorithms, group projections,
Lanczos/Temple and finite-moment tail bounds are established science. The
source original Haldane proof already uses rotation sectors and moment
polynomials. The acquired contribution is the actual spin-two six-cycle
input, full sector-loop readout, exact connected precision bypass and its
independent replay at this particular rung.

For MED, a separate-absolute-logZ bound such as2n delta may overcharge a
connected objective if a correlated primal/dual construction cancels the
bulk. Its effective interactions, solver error and finite-periodic boundary
still need acquisition. We do not claim that MED must solve a harder output.

BS-CMI purity factorization and thermal MPO/QBP methods may also exploit
the same cancellation. They retain actual global-marginal/environment or
local-factor acquisition, temperature constants, norm convention (the true
spin-two bond norm is6), compression errors and periodic loop control. Those
interfaces are not supplied here, and their possible success is not excluded
by the current moment failures.

Six next connected increments at beta1.5,3,6,12,24,48 and final
T512(96) are not acquired. Current mode counts already fail usefully at
beta3. No result at beta96, physical capability, gap, publication, or
comparison advantage is inferred from the first successful connected rung.

Post-certificate next-depth previews are charged too: the simultaneous
rank1--4 two-vector preview took2.76s, and the parent-proposed A5 five-angle
p4/p6 preview took7.13s. Additional triplet grids and moment-count probes,
including failed debug invocations, are retained as numerical feasibility
work. None supplies an accepted next input; see NEXT_DEPTH.md.
