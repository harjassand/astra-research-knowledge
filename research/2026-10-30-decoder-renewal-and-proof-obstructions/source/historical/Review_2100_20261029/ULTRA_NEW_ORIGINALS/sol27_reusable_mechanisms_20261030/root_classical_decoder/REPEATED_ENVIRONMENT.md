# Repeating a random environment removes the parity acquisition barrier

30 October 2026. Root construction, using ordinary denoising and binary linear
algebra. This is an explicit SOURCE UPGRADE, not an operation claimed available
from the iid native channel. No apparatus is changed or physical experiment run.

Use the source family in NATIVE_NOISY_PARITY.md, with the same hidden n-bit s,
fixed eta<1/2, public classical flag y, and independently refreshed phase noise.
Permit one additional operation: BEGIN draws an independent uniform y and
holds that random environment fixed for r consecutive logical-input calls;
each returned output carries the same y. END releases it. The learner cannot
choose y. Holding the environment and refreshing the independent noise are
separate assumptions. A fixed error bit across the whole block would NOT work.

Choose

    m = n + ceil(log2(2/delta)),
    odd r >= 2 log(2m/delta)/(1-2eta)^2.                         (1)

For each of m independent blocks, submit |+> r times, measure X and majority
vote the r output bits. Store its public y and majority label. Each label is
wrong with probability at most exp[-r(1-2eta)^2/2]<=delta/(2m), by Hoeffding.
Thus all stored equations y dot s=label are correct except with probability
delta/2. Independently, the m by n uniform binary coefficient matrix fails
to have column rank n with probability less than 2^(n-m)<=delta/2: for each
nonzero z, Pr(all y dot z=0)=2^-m, then union bound over 2^n-1 choices.

Gaussian elimination now obtains s with success at least 1-delta. It also
checks rank and consistency; a failure can return an explicit ABORT. Rank and
consistency alone do not certify correctness if every label is adversarially
flipped to another parity. Their probabilistic guarantee comes from the
stated independent noise and uniform independent blocks, not from a checksum.

The full bill is m*r upgraded logical source calls, m environment holds, and
polynomial classical elimination work (a literal bit algorithm uses O(m n^2)
bit xors and O(mn) stored bits). Only one prepared logical qubit is needed at
a time in calibration; no unknown payload waits for calibration and no quantum
programme is retained. Once acquired, the n classical bits describe a reusable
decoder: reversibly compute s dot y into one work bit, controlled-Z the physical
qubit, uncompute and discard the flag. A sequential circuit uses at most
2n CNOTs and one controlled-Z, O(n) two-qubit gates, and one work bit. Since
the actual flag is classical, direct classical parity/feedforward also works.
The subsequent N_s followed by the decoder is exactly D_eta, for every input
and retained reference: F_e=1-eta and half diamond error eta, the exact optimum.
The one-time statistical failure delta does not become an independent fresh
failure per later payload: conditioned on correct acquisition every payload
uses the correct circuit; on failed acquisition no claim is made.

This is weaker than choosing y=e_i and weaker than coherent environment
access. It still cannot be manufactured by sorting polynomially many iid
native examples: collisions among polynomially many uniform n-bit flags
occur with probability at most Q(Q-1)/2^(n+1). Seeing outputs is not holding
an environment fixed. This collision observation is a scoped diagnostic,
not a general LPN lower bound or a proof that every possible iid algorithm
must use collisions.

Ordinary comparison is decisive here. No new majority or linear-system
algorithm is claimed. With iid noiseless examples, plain elimination already
learns s. With iid noisy examples, full-source equivalence makes this exactly
LPN for quantum computation on classical examples. With the explicit repeat
operation, ordinary denoising and elimination solve it. The useful research
question therefore changes from improving an iid span estimate to obtaining
a stable, independently re-noised environmental condition in an actual
encoding apparatus. Whether present equipment supplies that operation is
UNKNOWN. Arbitrary mixed junk, unflagged environments and general unknown
Cliffords have not been upgraded by this construction.
