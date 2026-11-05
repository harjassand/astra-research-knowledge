# A physical positive block reader from the Yangian slow sector

5 November 2026. This is a complete finite-block operation with its source-specific recovery formula, memory cost, and processing bill. It improves on measuring every consecutive pair's singlet/triplet label. It does not solve arbitrary-accuracy memory optimization: the explicit three-carrier operation below has a nonzero error floor. Numerical larger-block projectors are reported separately and do not supply a proved asymptotic hierarchy.

## 1. An explicit three-carrier projector

For three consecutive physical output carriers, write D_ij=sigma_i dot sigma_j and

    P = I/4 -(D_12+D_23)/6 + D_13/12.

This is an orthogonal rank-two projector. To see this without numerical diagonalization, couple sites 1 and 3 first. The joint-spin sectors are:

* j_13=0, total j=1/2: D_13=-3 and D_12+D_23=0, hence P=0;
* j_13=1, total j=1/2: D_13=1 and D_12+D_23=-4, hence P=1;
* j_13=1, total j=3/2: all D_ij=1, hence P=0.

Thus P selects the spin-one-half doublet obtained by coupling the outer triplet to the middle carrier. Its complement has rank six. It is also the ground doublet of the open three-site antiferromagnetic XXX Hamiltonian.

Measure only the binary projective instrument {P,I-P}, retaining the full quantum state within the selected subspace and the classical outcome. In particular, do not measure the further spin labels inside the six-dimensional complement; their coherence is retained. A fixed three-qubit Schur basis change, a flag computing this one predicate, and the inverse basis change implement the measurement.

The operator P arises as the isolated quarter-rank spectral cut of the lowest three-site Yangian mode. Its leading positive-instrument energy is E4=1/4, compared with E4=3/4 for measuring the singlet/triplet label of an adjacent pair with the third carrier untouched.

## 2. Exact source-specific block acquisition

Set x=sin(theta)^2 and apply the original three chronological emitter collisions, followed by this binary instrument. For an incoming source Pauli, let b be the normalized squared Hilbert-Schmidt weight exported to source identity, and h the weight remaining source-traceless, including the full binary classical record. Direct contraction gives

    b = x^2 (x^4+30x^3-60x^2-12x+54)/18,

    h = (1-x)^3 (4x^3+24x^2+27x+9)/9.

The full-source-plus-output norm loss is

    1-b-h = x^2 (7x^4-6x^3-6x^2+4x+6)/18.

One derivation expands U_3 U_2 U_1, applies

    Y_a = (I_S tensor P) W_a (I_S tensor P)
          +(I_S tensor (I-P)) W_a (I_S tensor (I-P)),
    W_a = U (sigma_a^S tensor I) U^dagger,

then evaluates

    b = Tr[(Tr_S Y_a/2)^2]/8,
    b+h = Tr[Y_a^2]/16.

SU(2) covariance makes these contractions independent of a and their cross Gram matrices proportional to delta_ab. The displayed polynomials were obtained by exact symbolic Pauli arithmetic; the code is three_block_symbolic.py.

For L independently processed three-carrier blocks, old source-identity information persists. Its overlap with the new exported contribution vanishes because the latter has zero trace on the new block. The scalar Gram identities extend to arbitrary old source/memory coefficients, not just product logical states. Consequently

    a_L = b (1-h^L)/(1-h),
    q_L = h^L.

These are exact for every 0<theta<pi/2 and every integer L>=1, for the actual fixed emitter and arbitrary input/reference.

## 3. Physical final recovery

For a projective compression instrument with branch isometry V_x:range(P_x)->Q_x, the average output in branch x is I_(Q_x)/d. Its Petz channel is simply the conditional isometric embedding

    Y_x -> V_x^dagger Y_x V_x

into range(P_x) in the original block Hilbert space. This follows directly from the reference-state factors I/d and I_(Q_x)/d; no inverse with a large condition number is required.

Petz reversal composes in the reverse order for these consistent reference states. The complete reader therefore:

1. Retrieves the last stored compressed block and its classical branch label.
2. Embeds it into its original physical block subspace using fresh zero workspace.
3. Applies the original inverse partial-SWAP gates to a dummy qubit initialized at I/2, in reverse chronological order through this block.
4. Discards the decompressed block and repeats for earlier blocks.
5. Returns the dummy qubit.

This is the Petz map of the actual compressed output channel. Covariance makes the logical channel exactly depolarizing with visibility a_L. Hence its half-diamond error is

    epsilon_Petz(L,theta) = (3/4)(1-a_L).

The operation does not access the original source, incoming-carrier purifiers, or preparation labels.

## 4. Exact packed-memory and processing bill

To avoid treating fractional qubit dimensions as free storage, collect three of the above blocks at a time, i.e. nine chronological carriers. There are eight classical binary-label patterns. The largest conditional quantum dimension is

    6^3 = 216 < 2^8.

For each pattern, a fixed nine-qubit unitary can map its retained subspace into eight qubits tensored with a known zero in the ninth. Measure the three binary labels, apply this conditional encoding, and discard/reset the known-zero qubit. This is a deterministic nine-to-eight-qubit quantum compression with three classical bits. It retains all within-branch coherences.

For N=9K used carriers, equivalently L=3K triple blocks, the retained quantum storage is 8K qubits. The current nine-carrier buffer, reusable measurement ancilla, and final dummy add only a fixed number to the peak when the fixed-size updates fit the service schedule:

    M_peak = 8N/9 + O(1) qubits.

The recorded outcomes require N/3 classical bits. Unused endpoint carriers can be ignored, or an incomplete final group of at most eight carriers can be retained raw with constant additional space.

All encoding and decoding unitaries act on at most nine qubits, with a finite branch set independent of N and theta. Standard finite-dimensional unitary decomposition supplies a fixed finite number G_9 of elementary gates for each ideal packed-group encoder/decoder. No native high-spin interaction is assumed. In addition, the final reader uses exactly N inverse emitter-angle partial-SWAP gates. Thus ideal addressed processing is O(G_9 N), with G_9 a fixed, potentially large constant.

For a discrete universal gate set, choose each synthesized block operation's channel error O(delta/K), giving total additional error at most delta by the hybrid argument. This costs O(N polylog(N/delta)) gates for this fixed block size, in addition to the inverse-collision gates and paid routing. The final reverse pass has a sequential dummy-qubit dependency and its service time must be paid. The O(1) additive memory term above applies to ideal fixed-angle operations with adequate interarrival service. For a fixed finite universal gate set, let tau_block(N,delta) be the synthesized bounded-speed service time of a packed-group operation. At fixed carrier spacing Delta, provision P=ceil(tau_block(N,delta)/(9 Delta)) independent nine-carrier processors or the corresponding quantum queue. This costs O(P) additional coherent cells and must not be treated as O(1). For fixed block size and bounded-speed parallel local service, the finite-control bill is therefore 8N/9+O(polylog(N/delta)) coherent qubits, plus any routing cost. Alternatively, if the physical source schedule permits spacing at least tau_block/9, the extra collection time and source/receiver protection exposure must be counted. No ability to change a fixed arrival clock is assumed.

## 5. Accuracy boundary of this actual operation

As L grows,

    a_infty(theta)
      = (x^4+30x^3-60x^2-12x+54)
        / [2(4x^4+12x^3-33x^2-4x+30)].

Its weak-angle expansion is

    b=3theta^4+O(theta^6),
    h=1-(10/3)theta^4+O(theta^6),
    a_infty=9/10+O(theta^2).

In fact a_infty<=9/10 for all x in [0,1]. Subtracting it from 9/10 gives

    x(31x^3-42x^2+3x+24)
      / [10(4x^4+12x^3-33x^2-4x+30)].

The denominator is positive for 0<x<=1 since 1-h>0. The cubic numerator factor has positive Bernstein coefficients 24,25,12,16 on [0,1]. Thus the physical Petz reader's error floor is at least 3/40=0.075, approached as theta tends to zero.

Even an arbitrary final decoder on these processed blocks has the all-decoder bound

    epsilon_opt >= (3/4)(1-sqrt(a_L)),

so its asymptotic weak-angle error is at least

    (3/4)(1-sqrt(9/10)) = 0.0384875... .

For the explicit Petz operation, define

    epsilon_infty(theta)=(3/4)(1-a_infty(theta)).

Then

    epsilon_Petz(L,theta)
      = epsilon_infty(theta)+(3/4)a_infty(theta)h^L.

For any target epsilon>epsilon_infty(theta), taking

    L >= log[(3/4)a_infty(theta)/(epsilon-epsilon_infty(theta))]
         / (-log h)

and rounding L up to a multiple of three attains the target with the packed eight-ninths memory bill. Targets below the floor are not attained by this operation. At a fixed target error, its extra acquisition time can outweigh the eight-ninths storage factor; this construction is not claimed to improve the optimized all-output memory upper bound in every parameter regime.

## 6. What larger positive cuts currently establish

Direct optimization over invariant balanced rank-d/2 projectors gives numerical leading instrument energies

    n=6: E4 approximately 0.2088325,
    n=7: E4 approximately 0.1083515.

These are actual positive projective instruments with one-qubit saving per block. They are upper bounds from concrete matrices, not certified global optima. Their fixed-n weak-angle block limits are

    a_infty -> n/[n+(4/3)E4],

giving approximately 0.95565 and 0.97978 respectively. The corresponding physical Petz error floors are approximately 0.03326 and 0.01517. Their matrices and optimization code are saved locally.

No uniform n,theta bound or closed causal recycling rule has been proved from these examples. A dimension-saving instrument at one cut cannot be iterated as though the retained register were a fresh homogeneous block; its representation and logical correlations have changed. The missing endpoint is a proved family of compression/recycling operations and a matching width-dependent converse at the quartic acquisition horizon.
