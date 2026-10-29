# Routing is a load-bearing cost of random matching probes
2026-10-29. New derivation, pending independent review.

Consider n even fixed qubits in a one-dimensional line, initially in a product pure state, and an exact product of singlets on a uniformly sampled perfect matching M. All entangling operations are nearest-neighbour two-qubit gates, no preshared entanglement, measurements, moving physical qubits, nonlocal buses or extra routing register. Arbitrary single-qubit unitaries are free for this lower bound.

Across cut j|j+1 the final entanglement entropy is precisely X_j(M), the number of matching edges crossing that cut. Each of the j sites on the left has a partner on the right with probability (n-j)/(n-1), so E X_j=j(n-j)/(n-1). A two-qubit gate across that cut changes its entropy by at most two bits (conditional entropy bound); all other gates leave it unchanged. Thus any exact preparation circuit has G_j >= X_j/2 gates across cut j, and

E G >= (1/2) sum_j E X_j = n(n+1)/12.

At the middle cut E X_(n/2)=n^2/[4(n-1)]. In a circuit layer at most one nearest-neighbour gate crosses that cut, hence E depth >= n^2/[8(n-1)]. These are average lower bounds over the specified uniform matching, not a worst-case circuit estimate. Local basis rotations of the singlets do not change the bounds. Coherent entanglement assistance and measurement-mediated architectures require separate accounting and are outside this model.

For approximate pure-state preparation with trace distance at most eta for every matching, entropy continuity on the smaller cut side gives S_actual(j) >= X_j - eta min(j,n-j) - h2(eta), using the looser log-dimension version. Consequently E G >= n(n+1)/12 - eta n^2/8 - (n-1)h2(eta)/2. This remains quadratic for small fixed eta. The statement is for a pure implemented output from unitary gates, not an arbitrary mixed preparation.

Consequence: constant-in-n statistical sensitivity of matching survival does NOT mean linear total physical cost on a line. Its n/2 independently addressable singlets and local pair readout are an attractive all-to-all/bus interface, but nearest-neighbour exact preparation alone has quadratic gate cost. A Schur/encoded logical-test comparator must use the same connectivity and calibrated control model. The result does not prove either architecture superior.

A practical randomness note: uniform matching can be sampled recursively by pairing the smallest unpaired site with a uniformly sampled other site. Use rejection sampling for each finite integer, not modulo-biased random integers. Sampling may consume unbounded random bits in the worst case; a finite cap must contribute its rejection probability to abort/bias accounting. If the implemented matching distribution is within total variation eta of uniform, its observed binary pass/fail mean differs by at most eta; a witness e <= C q therefore becomes e <= C(q_implemented+eta). It does not acquire an n factor, but physical preparation and measurement errors are additional.
