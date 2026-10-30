# Full-source noisy-parity boundary for reusable quantum recovery

30 October 2026. Root construction. Mathematical reduction; independent whole
challenge pending. **Conditional computational barrier, not a hardness proof.**
No quantum device, source or cryptographic solver has run. Existing frozen
ROOT25/26 results are unchanged.

## A small-description structured source

Let s be an unknown n-bit string and 0<eta<1/2 a fixed known noise rate. Set
D_eta=(1-eta) id+eta Ad_Z and define the qubit-input channel

    N_s(rho) = 2^-n sum_y |y><y| tensor
                   Z^(s dot y) D_eta(rho) Z^(s dot y).             (1)

The dot product is binary. This is an unknown Clifford encoding with arbitrary
mixed junk, in the particularly simple case of maximally mixed n-qubit junk,
followed by logical phase noise. The Clifford consists of at most n controlled-Z
gates, controlled by the junk bits. The public output split is flag y plus one
physical qubit. Its ideal eta=0 version is exactly reversible. The actual eta>0
channel has optimal entanglement fidelity 1-eta, proved below. Its mean output
is the full maximally mixed state of dimension 2^(n+1); no small effective-rank
promise is implied. Its circuit has only O(n) classical description bits.

The native source supplies arbitrary forward uses of (1), including coherent
INPUTS, inputs entangled with retained registers, adaptivity, and interleaving.
It supplies neither a coherent output flag, an inverse dilation, an environment,
nor intervention on y. All calls are independent uses of the same channel.

## Exact simulation from classical random examples

An LPN example is an independent pair (y,b), with y uniform, b=s dot y xor e,
and e an independent Bernoulli(eta) bit. Given such a CLASSICAL pair, output
the classical register |y><y| and apply the KNOWN gate Z^b to the submitted
qubit. Averaging produces exactly (1), as a completely positive map, including
its action tensored with the identity on any reference. Replacing every native
call by a fresh example therefore simulates every adaptive quantum source
algorithm exactly. Induction over its intervening completely positive maps
proves the full interactive statement. Quantum inputs do not turn this
classically sampled flag into a coherent example oracle.

In the other direction a call on |+> followed by flag measurement and X
measurement of the output yields exactly an LPN example. Thus native forward
access to this family and classical random LPN examples are interconvertible,
one example/call at a time, for a quantum algorithm.

## Any near-optimal reusable decoder predicts the hidden parity

Let R be any CPTP map from flag plus physical qubit to a qubit, represented
by an efficiently executable reusable circuit. It may have been acquired
by any source algorithm. After acquisition no unknown source is used to
execute R. Define R_y(tau)=R(|y><y| tensor tau). This is a qubit channel even
if the implementation of R coherently processes its flag input. Put

    a_y = F_e(R_y Ad_(Z^(s dot y))),
    b_y = F_e(R_y Ad_(Z^(s dot y xor 1))).

For every qubit channel R_y, a_y+b_y<=1. Indeed its normalized Choi state
has trace one, and these are its overlaps with two orthogonal Bell states
(the phase-transpose convention does not matter for Z). Therefore

    F_e(R N_s) = E_y[(1-eta)a_y+eta b_y]
               <= eta+(1-2eta) E_y a_y <= 1-eta.                 (2)

The ordinary decoder that applies Z^(s dot y) and discards y attains 1-eta.
Thus the upper bound is the exact optimum, with no recovery optimality
oracle or comparison algorithm being assumed.

If the acquired decoder satisfies

    F_e(R N_s) >= 1-eta-epsilon,

then its conditional Bell overlaps obey

    E_y a_y >= 1-epsilon/(1-2eta).                              (3)

There is an executable noisy predictor for s dot y: prepare a KNOWN Bell
pair, feed one half and the SPECIFIED classical flag y into the acquired R,
and Bell-measure its output against the retained half. Label the I and Z
Bell outcomes by 0 and 1; label the other two outcomes arbitrarily. On input
y its correct-label probability is at least a_y. Its average prediction
error is consequently at most q=epsilon/(1-2eta). This uses R, not N_s;
choosing a decoder's input flag is allowed by a classical circuit description.

For q<1/4 the complete secret is recoverable in polynomial time. For each i,
draw fresh uniform y, independently run the predictor at y and y xor e_i,
and xor the two predicted bits. The true xor is s_i. Since both input
marginals are uniform, the union bound makes the xor correct with probability
at least 1-2q>1/2, regardless of how prediction errors depend on y. Independent
pairs and majority vote recover every bit with failure at most delta using

    O(n log(n/delta)/(1-4q)^2)

predictor invocations. No unproved Goldreich-Levin oracle or pointwise noise
assumption is needed. Reset the executable decoder's private workspace per
invocation; no consumed unknown quantum programme is granted.

For example eta=1/10 and epsilon<=1/20 imply q<=1/16. A polynomial native
algorithm that with probability >=2/3 produces such an efficient reusable
decoder for every s would give a bounded-error polynomial quantum algorithm
for LPN with CLASSICAL random examples at noise 1/10. This is a conditional
boundary under the matching quantum-LPN assumption. It is not unconditional,
not an inference from a failed span algorithm, and not the different LSN
single-codeword problem.

The reduction also applies to a claimed reusable recovery whose half diamond
error to the identity is <=eta+epsilon: its Bell overlap is then at least
1-eta-epsilon. Conversely the known-s phase decoder has half diamond error
exactly eta. Thus this is a near-optimal all-input recovery boundary too.

## Two paid operations remove this obstruction

At eta=0, measuring |+> outputs gives noiseless linear equations. Ordinary
Gaussian elimination learns s from O(n+log(1/delta)) uniform examples and
stores its n bits. Bell-difference methods also work, but are unnecessary
for this public flag family. Exact/noisy calibration must not be conflated.

If an upgraded source permits intervention on its RANDOM junk flag, choosing
y=e_i and measuring the |+> output repeatedly learns s_i by ordinary majority.
The complete reusable decoder then costs O(n log(n/delta)/(1-2eta)^2)
interventional calls. This is a DIFFERENT source operation, not supplied by
the native model. Merely seeing a flag, querying coherent logical inputs,
retaining the output register, or storing all past examples does not supply it.

A coherent quantum example state sum_y |y>|s dot y>/sqrt(2^n) is likewise
different from the flagged channel (1). Known noise-robust Fourier learners
for such examples therefore do not refute this reduction. Finding how to
construct one of these stronger operations from realistic apparatus would
be a substantive mechanism; naming it an available oracle would not.

## Controlling priors and novelty status

- Cross, Smith and Smolin, Quantum learning robust to noise, PRA92 012327
  (2015), https://arxiv.org/abs/1407.5088: coherent noisy example access
  differs from classical random examples. Its positive result cannot be
  imported into (1) without constructing that missing coherent source.
- Poremba, Quek and Shor, Learning Stabilizers with Noise, ITCS2026,
  https://arxiv.org/abs/2410.18953, Definition4.1/Remarks4.2--4.4: known
  code and one noisy random codeword. Explicitly not many identical copies.
  Its assumption is NOT used in this reduction.
- Hinsche, Eisert and Carrasco, PRX Quantum7 020337 (2026),
  https://arxiv.org/abs/2505.15770 and DOI10.1103/6frk-891j: exact mixed
  strong-stabilizer acquisition is ordinary prior, not this programme's
  discovery. No exact-stabilizer learner is called noise robust by default.
- Tang and Steckmann, https://arxiv.org/abs/2610.03307v1: a PURE state before
  Pauli noise is an essential promise. Maximally mixed n-qubit junk in (1)
  does not satisfy it. Root read its mixed/strong/weak distinctions and
  quartic Fourier mechanism; the full robust-algorithm transfer is not claimed.

The channel-to-decoder reduction above is internally constructed; historical
priority has not been established. It is not an operational cryptographic
attack, a new efficient noisy learner, a physical decoder demonstration or a
civilisation-level result. Its research value is to isolate an actual missing
operation, including coherent INPUT access, before resources are spent trying
to remove a source-computational barrier by improving another span estimate.
