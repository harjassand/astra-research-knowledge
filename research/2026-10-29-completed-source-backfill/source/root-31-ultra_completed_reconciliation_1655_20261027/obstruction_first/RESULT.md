# Spin-two Haldane gap: a counted thermal-input bridge and its exact boundary

The intended result was an explicit positive gap for every sufficiently large
even periodic pure spin-two Heisenberg chain. **That result is not achieved.**
The work constructs a genuine finite-input operation, acquires its normalization,
and demonstrates a substantial ambiguity in the resulting short-ring data. It
does not establish a new physical capability or an algorithmic advantage.

## What changed the distance to the target

The spin-one gap is already a source theorem. OpenAI's periodic proof is pinned
to repository revision `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`; its directory
last changed at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Tasaki's October19
exposition already extends the analytic two-purity criterion to all spins and
identifies spin two as a computational target. Neither the criterion nor that
extension is a contribution here. No rigorous spin-two proof was located in the
versioned primary search; this is not an exhaustive priority clearance.

The difficult bridge is rigorous thermal initialization, not another estimate
of the physical gap. Established QMC/DMRG estimates already put that gap near
0.089 and the correlation length near49 sites. A new numerical extrapolation
would add little. The attempt therefore replaced the source's propagation of
all exponential columns with approximate low-energy vectors **and a checked
count of all omitted eigenvalues**.

The rank-lift verifier checks positivity of

    H - c I + alpha Q Q*.

Its rank bounds the number of energies below c. Polar-isometry residual bounds
then pair the counted low energies with their approximate values; the remaining
trace is bounded by `(D-K) exp[-beta(c+a n)]`. The proof is in DERIVATION.md.
No accuracy or completeness claim from Lanczos is taken on trust. The scalar
inequalities use directed intervals. Matrix residual bounds explicitly assume
the stated IEEE binary64 matrix-product model; this is not an exact-arithmetic
formalization of BLAS.

All ten untwisted/pi-twisted traces at lengths4–8, beta12, passed the verifier.
The reference shift4.76124816 is just a specified normalization of the trace.
For example, at length8:

| twist | trace enclosure | counted low states | omitted tail upper |
|---|---:|---:|---:|
| identity | [178.9132166594513,178.91327753807207] | 9 | <0.00001 |
| pi | [0.061682338997359254,0.06169235104991432] | 6 | <0.00001 |

The entire Hilbert-space dimension390625 is included. Magnetic translation,
including its seam holonomy, reduces the largest matrix to4783. Direct-sector,
independent Kronecker, and signed-translation spectra agree through length6;
the exact identity `Tr H^2=12 n 5^n` supplies another check.

## The normalization is acquired rather than assumed

An initial small SU(2) ansatz search plateaued near−4.75026 and was rejected as
a useful normalization at the desired energy. Ordinary U(1)-resolved infinite
TEBD then produced explicit two-site tensors with bond dimension32. Their
infinite-chain floating energy is about−4.760633; that number is not a finite-ring
certificate.

After rounding tensor entries to integers at scale10^8, the **64-site periodic**
norm and energy were recomputed with arbitrary-precision integer contractions.
The only nonrational coefficient is sqrt(6), bounded by rational endpoints.
The resulting energy per bond is

    [-4.761019703135210,-4.761019703135208].

An independent exact four-site computational-basis replay agrees with the
contractions. Consequently, for a=4.7610, E0(64)<−64a and Z64(b)>1 for every
b>0. The beta12 trace boxes above convert to this acquired shift by the known
positive factor `exp[12*n*(4.76124816-4.7610)]`. No new spectral calculation or
physical acquisition is hidden in that conversion. It does not supply trial
normalizations at arbitrary larger ring lengths.

## What the acquired short traces cannot determine

There is an explicit finite real self-adjoint SO(3)-equivariant transfer model
whose moments lie strictly inside all ten acquired trace intervals, yet whose
spatial purity is at most1/2 at **every even length**, at this beta.

Its spin-zero list J has414796422 eigenvalues counted with multiplicity; its
spin-one list N has585203636, repeated three times. The actual file stores only
50 groups with integer multiplicities and rational eigenvalues. Exactly two
largest eigenvalues are11/10; every other modulus is below1.069. The model
therefore needs no large matrix allocation. Its I/P moments are J_n+3N_n and
J_n−N_n. Their inclusion in the thermal boxes is checked with exact rational
arithmetic, not optimizer residuals.

The model also has **positive twisted traces for all integer lengths n>=4**.
Directed checks cover4–740, followed by a monotone analytic tail from741.
Every SO(3) twist is covered because the spin-one character lies in[−1,3],
between the two checked endpoint traces. Rescaling to a=4.7610 preserves this,
and the model obeys the acquired even-ring normalization. Thus short I/P traces,
these symmetry/positivity properties, and that normalization do not alone force
the spatial concentration needed by the two-purity criterion.

This is a **fixed-temperature spatial-interface** ambiguity. It does not
construct the actual local spin-two history kernel, a common all-temperature
Hamiltonian family, or an alternative local quantum chain. Temperature lifting,
additional twists, and additional Hamiltonian identities remain possible repairs.
Even if qualitative simplicity of the leading mode is supplied, replacing one
11/10 by11/10+epsilon for any0<epsilon<=10^-8 stays inside every acquired
interval and preserves all trace positivities. The mode becomes simple, while
its spatial gap can be arbitrarily small. No uniform finite seed length follows
from these snapshot inputs plus qualitative simplicity.
The first attempted witness failed positivity at unacquired odd lengths; it is
preserved as a rejected intermediate. Only the repaired file is used above.

## Strong ordinary repairs and the remaining operation

The source's other initialization also uses the cyclic2pi/3 twist. It rejects
this particular spin0/spin1 witness, so the witness is not a no-go for the full
source method. There is nevertheless a robust limitation to bare mass peeling
at moment8 and beta12: the A4-trivial moment is a positive group average and
is at least Z8(I)/12>14.9094, independently of the uncomputed cyclic trace.
Even the identity contribution to an icosahedral60 average exceeds2.9818.
An optimized higher-moment argument is not ruled out by those inequalities.

Full-column exact computation, symmetry-resolved spectrum validation, QMC with
improved estimators, thermal MPOs, and renormalization-based convex relaxations
are the equally informed comparators. The 2026 bulk-gap SDP hierarchy of Xu et
al. supplies certified **upper** bounds; it does not certify positivity of this
gap. Ground-energy bounds do not count low states or provide a thermal trace
tail. A tensor truncation error or an MPS energy likewise cannot replace the
positive-lift check. The short even-ring pi twist has a very small partition
ratio; ordinary sign-free untwisted QMC is not automatically an equally cheap
certified acquisition of that ratio. No lower bound against improved sampling
or tensor methods is asserted.

The next scientifically meaningful operation is a certified relative trace or
spectral exclusion for substantially longer rings at the required low temperature,
with a usable MPS normalization at those same lengths. A compressed positivity
certificate must control the discarded space; projection into a favorable
variational space is insufficient. The present dense Cholesky check still scales
with the explicit symmetry-sector dimension and does not close that interface.

## Full cost and replay

Recorded script wall times include637.21s for the full numerical spectra used
to select candidate counts,413.76s for all ten tail validations,4.62s for TEBD,
and104.22s for the exact64-site contraction. The failed SU(2) searches, LP
repairs, independent checks, and source work are additional costs. Jobs used
at most two BLAS threads. Peak memory was not instrumented; each largest dense
complex array is about366MB, and the verifier holds several. The fixed-dimension
rank-lift reduction has not been compared at matched precision against an
optimized full-column implementation. No speedup is established.

`verify_bridge.py` independently replays exact moment inclusion, all-length
positivity, the algebraic variational inequality, and shift conversion. It passed.
It explicitly does not repeat the dense matrix residual calculations or full
integer contractions. Their full commands and the actual used cores are listed
in DERIVATION.md. No independent scientific audit or hardware test is claimed.
