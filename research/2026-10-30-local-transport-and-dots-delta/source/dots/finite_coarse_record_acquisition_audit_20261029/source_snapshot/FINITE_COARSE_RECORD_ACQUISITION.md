# Finite native coarse-record acquisition without a spectral gap
2026-10-29. Additive author construction; independent receiving pending. This proves a measurement interface, NOT approximate-central decoding.

## Contract and ideal comparator
B=B* has norm<=1 and is a known signed quadratic program Hamiltonian, e.g. B_ab={Delta_a,Delta_b}/2 with four signed normalized-state pairs, total coefficient weight W=4. Fresh ordinary source outputs, controlled register permutations and trusted clean controls are available while the target is stored. No B eigenbasis, source inverse or spectral gap is supplied.

Choose w=4/J with J>=4 a power of two. Partition the spectral circle of circumference4 into J bins. The physical spectrum [-1,1] occupies a half-circle, so this agrees with real-line coarse separation, up to naming a cyclic bin. Let the offset u take L equally spaced values in [0,w), L a power of two. The ideal instrument measures the B-bin sharply and exposes u and the bin as classical records. Offsets are sampled independently of the target.

## Bounded coherent procedure
For dyadic 0<nu<1, set
 g=nu^2 w/256, beta=nu^2/32,
 L=least power of two >=256/nu^2,
 M=least power of two >=4096/g,
 s=least positive odd integer with 2^(-s)<=beta.
Run s coherent QPE instances for exp(+i pi B/2), each with M phase points. Unwrap the estimated phase in [-1/2,1/2) and multiply by4. Coherently compute the median estimated eigenvalue, compute its bin for u, and copy ONLY that bin to a clean retained register. Uncompute the median/comparison and ALL QPE instances/work. Then read the copied bin and forget the work. This is not a measurement of the full eigenvalue.

All loops and precisions are public and bounded. The coherent median retains s log2 M phase qubits until uncomputation; we pay O(s log M) phase workspace rather than reusing the exact-central classical-record O(log M) claim. There remain only three ambient D-dimensional registers (target and two fresh quadratic programs), plus clean phase/selector/control registers.

## Exact-QPE instrument comparison
Standard QPE on eigenphase phi has outcome probability at grid k/M bounded by 1/(4M^2 dist(phi,k/M)^2). Summing both tails gives probability of phase error>=delta at most 1/[2(M delta-2)] when M delta>2. Take delta=g/4; the stated M makes one-run failure below1/16. For s independent coherent QPE registers on a fixed eigenvector, median failure<=2^s(1/16)^((s+1)/2)<=2^(-s)<=beta. The spectrum lies in [-1,1], so phase unwrapping has ample margin; an unwrap error is already part of the circular-phase tail event.

For an eigenvalue at distance>g from every bin boundary, the coherent compute-copy-uncompute isometry has overlap at least1-beta with the ideal clean-work/bin state. Its vector distance is therefore at most sqrt(2beta). On any other eigenvalue the distance is at most2.

For EVERY eigenvalue, the fraction of discrete offsets within g of a boundary is at most 2g/w+1/L. For an arbitrary target/reference input, split it into the good and boundary spectral subspaces for the chosen offset. Triangle inequality, Jensen and uniform offset averaging give a bound on the half-diamond distance of the offset-exposed instruments:
 sqrt(2beta)+2sqrt(2g/w+1/L) <= nu/4+sqrt(3)nu/8 < nu/2.
The bound is uniform over inputs, including reference entanglement. It is not conditional on a successful selected bin and involves no probability normalization. The same statement holds on direct sums or an arbitrary background. Sharp boundary ties are included in the bad subspace.

## Paid source implementation
The received quadratic-program Jordan collision supplies half-diamond error at most4W^2 t^2/n=64t^2/n for one controlled B evolution of time t, with the public small-angle safeguard n>=16|t|. QPE and its uncomputation have total absolute time T<4sM; all inverse QPE Hamiltonian evolutions use NEGATIVE KNOWN COEFFICIENTS with fresh forward source programs, not an inverse source.

Allocate tau=nu/4 to all such evolutions. For each one choose
 n_t=ceil(16|t|)+ceil(64|t|T/tau).
The sum of full-instrument simulation errors is at mosttau, and the total collisions are bounded by16T+64T^2/tau plus two per evolution. Each collision consumes eight source outputs. This is polynomial in1/w,1/nu, with polylogarithmic dependence on the ambient dimension through controlled register permutations. The conservative leading source bound is O(nu^-5 w^-2 polylog(1/(nu w))).

All remaining known rotations (QFT phases, collision rotations and phase comparisons) receive total half-diamond synthesis allowance nu/4. A public bound Q on their number permits operator-norm accuracy nu/(4Q) per rotation; reversible finite-bit comparisons and median circuits are known classical-control circuits. Coefficients and pi-containing angles are approximated to this paid accuracy. This gives total instrument error<nu. It is a bounded theoretical compiler, not an executed hardware circuit or a practical complexity claim.

## Combining with response disturbance
Apply RANDOM_COARSE_RECORD_LEMMA.md to the exact ideal instrument, and pay nu_j for each actual measurement stage by complete-instrument hybrid composition. The ideal record-preserving channel retains
 Fopt >= Fopt(N) - original-response coarse-pinching debit.
The actual finite record channel therefore retains this bound minus sum_j nu_j. This remains an EXISTENCE bound on the optimum recovery available after acquiring the records. No mechanism attaining it is supplied by this lemma; approximate axis consistency is still unresolved.
