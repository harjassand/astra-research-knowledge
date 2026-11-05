# Exact boundaries for specific weak-stream receivers

These results concern the [actual homogeneous tracial partial-SWAP source](README.md). Each excludes a specified architecture; none establishes the unresolved optimal causal memory/processing tradeoff. The [full report](package/weak_stream_memory.tex) preserves proofs, constants and all excluded cases.

## Measuring total spin and discarding multiplicity

For a covariant input-qubit to N-qubit channel with tracial average output, a receiver that **measures** total spin J, keeps only the irrep Q_J and discards multiplicity has, even after any final decoder,

```text
epsilon >= (3/4)[1-sum_(J>0) w_J (J+1)/(3J)],
w_J=(2J+1)[binom(N,N/2-J)-binom(N,N/2-J-1)]/2^N.
```

The asymptotic floor is `1/2-1/sqrt(2pi N)+O(1/N)`, about `.498075` at N=43,462. The actual two-carrier Pauli signal includes a singlet–triplet cross term; measuring the label destroys payload information. Efficient Schur circuitry implements a basis change but does not make ordered-stream multiplicity/coherence discardable. Coherent adjacent-spin registers and general coherent multiplicity processing are outside this exclusion. [Proof and two-carrier calculation](package/schur/SCHUR_BOUNDARY.md).

## Consecutive pair labels

Measuring every consecutive pair's singlet/triplet label still loses information even when both quantum blocks and all classical outcomes are retained. For `x=sin(theta)^2`, the exact recovery statistic after K pairs is

```text
p_K=b(1-h^K)/(1-h),
b=x^2(2-x)^2/2, h=(1-x)^2(1+2x),
p_infinity <= (2-x)^2/[2(3-2x)] <= 2/3.
```

Every final decoder has `epsilon >= 3[1-sqrt(2/3)]/4`, about `.137628`. The per-pair loss is quartic in the weak angle and accumulates on the acquisition scale. Adaptive coherent rotations before measuring the label are outside this theorem. [Exact fusion/loss proof](package/schur/FUSION_THEORY.md).

## Reverse-decoded blocks retaining the Bell purifier

The physical block proposal stores b actual outputs, prepares a local Bell pair R,A, reverse-decodes the block with R, discards its b carriers and retains **both** R and A. Any final collective decoder on all retained pairs is permitted. This locally prepared purifier is not access to an incoming carrier purifier.

The [symmetric Petz Gram proof](package/online/purified_block_gram.txt) gives exact one-block p_b,q_b and `p_K=p_b(1-q_b^K)/(1-q_b)`. Any final decoder obeys `epsilon>=3[1-sqrt(p_K)]/4`; the RLD metric cannot replace the symmetric Gram here. Unequal predetermined blocks cannot beat the largest `p_b/(1-q_b)` among them.

If `b=o(theta^-4)`, that ratio tends to zero. When `b theta^4 -> alpha>0`, it tends to `(1-exp(-alpha))^2/[1-exp(-2alpha)/3]`. High precision requires the individual block to reach the quartic logarithmic scale; the apparent `b+2ceil(N/b)` memory bill does not supply square-root-memory recovery. At `.1`, indefinitely many b=40,000 blocks still have error at least `.0140607`. Other block instruments, retained block modes and adaptive choices beyond this proof are not excluded. [Recorded finite verification](package/online/purified_block_verification.json); the [earlier dummy-only obstruction](package/online/block_petz_obstruction.txt) retains its narrower scope.

## All deterministic nonselective covariant one-qubit updates

The [complete CPTP characterization](package/online/covariant_qubit_cptp_obstruction.txt) allows any time-dependent SU(2)-covariant map from retained qubit plus current carrier to one retained qubit. Memory is initially tracial; fresh pure implementation ancillas, resets and measurements are allowed when discarded inside each update. No specimen-correlated outcome or second coherent register survives.

Writing the adjoint Pauli map as `alpha sigma_M+beta sigma_E+gamma(sigma_M cross sigma_E)`, complete positivity is exactly `-1/2<=z=alpha+beta<=1` and `(alpha-beta)^2+4gamma^2<=(1+2z)/3`. Uniformly in horizon and such controls,

```text
|B_N| <= min{1,sin(theta)^2[1+8/(3-cos(theta))]},
epsilon >= (3/4)[1-sin(theta)^2(1+8/(3-cos(theta)))]_+.
```

At `.1` the error floor is `.712699`. Retaining the first emitted carrier attains visibility `sin(theta)^2`, so the quadratic visibility scale is matched, without claiming the upper coefficient sharp. Retained outcomes/feedback, oriented noncovariant pure memory and additional coherent registers are not covered. The supplied [295-channel finite checks](package/online/covariant_qubit_verification.json) have recurrence residual about `1.33e-15`; they are mathematical diagnostics, not physical experiments or general-instrument simulations. No scientific execution or new Capital audit occurred. [Package and provenance](SOURCES.json).
