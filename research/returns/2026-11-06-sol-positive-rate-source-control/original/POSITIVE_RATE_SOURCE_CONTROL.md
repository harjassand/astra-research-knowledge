# A positive bulk rate does not repair the missing uniform source cutoff

This consequence uses the completed r1 quantum-expander construction in
`../r1/CONTINUATION.md`, read in full. It tests a possible restriction of a
source-forgetting proposal, not the computability of channel capacity.
The physical channel below is fixed, rational, ordinary and explicitly
contains its transmitting qubit. That qubit is counted in its input/output
dimensions and rate; it is not a free identity wire appended to a hard
zero-capacity instance.

Let E_8:C^8->C be full erasure. Define the one fixed physical channel

    N = id_2 tensor E_8 tensor E_8 tensor E_8 tensor E_8,
    N: C^8192 -> C^2.

Its normalized Choi matrix is Phi_2 tensor (I_8/8)^tensor4, with the
one-dimensional erasure outputs omitted. This is an explicit rational
matrix. Q(N)=1: the output dimension bounds Q by one bit and fixing the
four discarded inputs leaves an ordinary perfect qubit channel. No
capacity oracle is needed for this control.

For each odd D>=3, take four independent copies of r1's stationary source
on the eight-dimensional erased inputs. Write their common n-site state
as sigma_D^(n). Its memory starts at I_D/D and uses the eight-unitary
quantum-expander isometry. In addition use independent maximally mixed
qubit inputs. The actual ordinary input to N^tensor n is

    rho_D^(n) = (I_2/2)^tensor n tensor (sigma_D^(n))^tensor4.

These are compatible stationary inputs. The maximally mixed qubits can
be prepared with their ordinary input-purifying reference held by Alice;
that reference is not a Bob-side resource. The true channel complement
receives exactly the four erased input records. Consequently, for every
n, with no asymptotic replacement,

    S(B^n)=n,
    S(E^n)=4 S(sigma_D^(n)),
    I_c(rho_D^(n),N^tensor n)=n-4 S(sigma_D^(n)).       (1)

For each fixed D, r1 proves S(sigma_D^(n))<=2 log_2 D. Thus the full
physical coherent-information rate of every source in this family is
exactly one bit per call. In particular its bulk rate is positive and
known, uniformly in the unknown finite memory dimension.

Nevertheless, for any selected n choose the least odd
D>=max(3,(10/9)^n). The same proved purity estimate gives

    S(sigma_D^(n)) >= 2 n log_2(10/9)-1,
    I_c(rho_D^(n),N^tensor n)
       <= [1-8 log_2(10/9)] n+4
       < -0.216024 n+4.                              (2)

For n>=19 this actual n-use coherent information is negative, although
the source's asymptotic rate is exactly +1. The environment entropy
excess is at least 8 n log_2(10/9)-4. The fourfold retained-memory map
has the same dimension-independent Hilbert--Schmidt contraction bound
on traceless operators as a single copy: decompose its Hilbert--Schmidt
space into identity/traceless tensor factors, each nonidentity sector
containing at least one contracting factor. Its degree is the fixed
8^4 and its memory dimension is D^4.

There is also one source with an arbitrarily long entirely negative
initial segment. Given an integer N>=1, choose an odd D with

    D^2 >= (256/3) (5/4)^N.

This is an effective finite integer choice. Use the original expander
bound lambda^2<=25/32, put q=4/5, and note (25/32)/q=125/128.
For EVERY 1<=n<=N its boundary purity obeys

    Tr[(tau_D^(n))^2]
      <= D^-2 + (25/32)^n
      <= q^n [3/256+(125/128)^n]
      <= (253/256) q^n < q^n.

Hence S(sigma_D^(n))>n log_2(5/4), and (1) yields

    I_c(rho_D^(n),N^tensor n)
       < [1-4 log_2(5/4)] n < -0.287712 n
       for every 1<=n<=N.                         (3)

The same fixed finite source then has rate +1 in the limit. Thus even
searching all initial source blocks does not fix this source-only cutoff
from the stated dimension-independent data. This is a source diagnostic,
not a channel detection-delay theorem: another input detects this fixed
channel's known capacity immediately.

Across selected horizons D changes; no single fixed finite source is
claimed to have linear excess forever. This establishes that restricting
to known positive source rates does not provide a uniform sublinear
environment-excess envelope or a good-block cutoff from physical channel
dimensions, this bulk-rate margin and this memory contraction bound alone.

It does not obstruct a capacity evaluator which chooses different inputs:
the particular channel N already has one-bit one-use capacity. Nor can
it be added to the hard zero-capacity family without destroying its
zero-capacity promise. It therefore closes a source-bound loophole only.
The missing ordinary-capacity gap or terminating upper evaluator remains
unearned. No additional numerical experiment or worker was used.
