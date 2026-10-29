# Independent construction of the actual-channel recovery chain

30 October 2026. This reconstructs root's general agnostic operation, B's
source-copy filter and C's common-frame learning port. It is not restricted to
an actual channel near an exact mixed-isometry model. No quantum processor,
source model or numerical fixture is executed here.

## 1. Mathematical promises and the physical task

Let N:k -> D be fixed and memoryless, with forward entangled-input access.
Its actual mean state is A=N(I/k). Assume some mathematical CPTP R0 has
Bell entanglement fidelity Fe(R0 N)>=1-kappa. Also let the actual mean-state
tail after d0 eigenvalues be tau. R0, a source adjoint, purification, exact
support, eigenbasis and near-perfect model are not given. Neither kappa nor
tau is needed by the algorithm. They are analysis parameters, not certified
performance learned from the training data.

All training Choi outputs/references and the late payload can be kept coherent
until ONE joint compression. This is a one-batch physical CPTP operation with
trusted known gates, not an offline classical-record learner or a reusable
original-frame streaming decoder. Ambient storage is substantive, even when
query complexity and learned matrices are independent of ambient dimension.

## 2. Mean-state tail pays a fixed actual filtered channel

For one threshold c in[a,2a], let Pi=1_[c,infinity)(A). The ideal channel

    F(X)=Pi N(X)Pi direct_sum Tr[(I-Pi)N(X)]|fail><fail|

is TP and has common output support of dimension at most floor(1/a)+1. This
is the support of the ideal filter of the ACTUAL N, not of a nearby N0. For
mean loss t=Tr[(I-Pi)A], split the first d0 eigenvalues from the tail:

    t<=tau+2d0 a.

The same Pi is used on every training and payload carrier in the batch.
Approximate implemented filters may have larger actual support; their entire
composition is compared to this one ideal F with a paid implementation error.
No source-noise-to-ideal-model comparison is repeated N times.

## 3. The Bell-target estimate is linear in loss

Purify the actual encoded Choi state and apply a Stinespring isometry for R0.
Let psi be the resulting unit vector, B the Bell target tensored with identity,
and M the success projector Pi conjugated into that isometry's image. Then

    ||(I-B)psi||^2<=kappa, ||(I-M)psi||^2=t.

Writing u=(I-M)psi, and using that I-M is a projection,

    ||B M psi||^2
      =||Bpsi||^2-2 Re<Bpsi,u>+||Bu||^2,
    <Bpsi,u>=t-<(I-B)psi,u>.

Cauchy gives the pass-only Bell contribution at least

    1-kappa-2t-2sqrt(kappa t) >=1-2kappa-3t.

Extending R0 to map the failure flag to an arbitrary fixed state adds a
nonnegative contribution. The purification and transported recovery remain
proof objects. This calculation avoids a gentle-filter square root followed
by another recovery square root. It applies to an already imperfect recovery,
not merely to an exactly reversible source. It is the central useful general
interface, independently reconstructed here.

## 4. Learning the same actual F in a shared frame

The accepted N1291 reference-safe joint compression identity is used on ALL
program carriers and the payload together. For any fixed unknown identification
of F's support with a known small register, its output is the Haar average over
one common U of independent Choi programs of F_U and the encoded payload F_U.
Training and payload are conditionally independent given U. An external payload
reference is untouched. No independent-per-record frame or new F_U oracle is
granted. A mathematical competitor R0 transported into that small frame has the
same fidelity lower bound.

Set zeta0=2kappa+3t. On the uniform tomography-good event the learned physical
channel Fhat has half-diamond distance at most delta from F_U. The competitor
has fidelity at least max(0,1-zeta0-delta) on Fhat. Ordinary Barnum--Knill
transpose/Petz reversal for the singleton maximally mixed input gives the square
of that nonnegative lower bound. Returning to actual F_U costs at most delta:

    Fe(Petz_Fhat F_U)>=1-2zeta0-3delta.

If zeta0+delta>1, the right side is negative and fidelity nonnegativity suffices;
one cannot square an invalid negative lower bound. Normalized Choi trace distance
and the input-k Choi-to-diamond inequality give

    halfdiamond(Petz_Fhat F_U,id)<=k sqrt(4kappa+6t+3delta).

Uniformity in latent U and independence of its program records from the payload
permit averaging tomography failures at weight beta. Adding full-processor
half-diamond implementation budget gamma gives

    halfdiamond(decoded,id)
      <=k sqrt(4kappa+6tau+12d0 a+3delta)+beta+gamma.

This is the averaged CPTP processor, not a certificate for every tomography
record or every retained random seed. It works on arbitrary logical payloads
and adjoining references through the diamond bound.

## 5. Gap-free learned matrices, rather than an inverse of N

The inherited finite tomography uses h=kr and h^2 settings. Rational sample
counts give raw Hermitian error at most 2he in operator norm. The affine TP
repair doubles that bound to a_ridge=4he. With

    C=(B+2a_ridge I)/(1+2h a_ridge),

the estimate has exactly the normalized Choi marginal. The exact rational
acceptance test requires C>=a_ridge I/[2(1+2h a_ridge)]; failure substitutes a
physical depolarizing channel. Therefore every accepted estimate, including
bad statistical records, has a paid inverse condition for S=Fhat(I/k):

    S>=k a_ridge I/[2(1+2h a_ridge)].

With e=delta/(10 k h^2), this implies ||S^(-1/2)||^2<=5h/delta+4r.
The actual learned Petz Kraus matrices use adjoints of these known finite
matrices. They are not supplied unknown-channel adjoints or an original-frame
decoder oracle. Matrix square roots, dilation synthesis and its reference-safe
error belong to gamma.

## 6. Independent source-copy filter challenge

I reconstructed all of B_SPECTRAL_PORT, including its controlled primitive.
For one fresh A copy and K=|1><1| tensor SWAP, the reduced partial-swap channel
and the controlled A evolution have identical zeroth/first derivatives. Both
second derivatives have diamond norm at most four at EVERY real time. Integrating
their difference gives full-diamond error at most 4u^2 per step and 4T^2/m for
m fresh steps, including control off-diagonals and arbitrary references.

The finite threshold grid has disjoint radius-g intervals. Only eigenvalues
above a/2 can spoil a threshold, at most 2/a. Its finite atom count, not a
continuous-Haar argument or observed spectrum, pays the gap failure probability.
Coherent QPE with a majority flag and uncomputation has isometry error at most
sqrt(2p_wrong) on each eigenvalue; spectral orthogonality makes this uniform
for superpositions and references. Measuring full phase records would invalidate
the filter, but B measures only the binary flag after uncomputing. Forward and
inverse controlled evolutions use separate fresh copies; an inverse of the
actual noisy DME channel is not assumed.

The explicit source-copy sums, phase-estimation lattice tail and known partial-
SWAP control circuit are polynomial in the stated gap/error parameters and
log D. I find no mathematical error in their declared ideal-control scope.
Their large number of source copies and all protected registers remain paid.

## 7. Uniform growing-rank compilation and concrete error allocation

C replaces fixed-rank GT enumeration by one easy highest-weight basis vector,
inverse small-register Schur transform and ONE common sampled unitary on all
carriers. Schur irreducibility gives the desired mixed irrep, without enumerating
its potentially enormous dimension. The finite Gaussian/polar supplier is
compared to Haar in averaged-channel diamond norm, not total variation of a
discrete law against a continuous law. Its Box--Muller tail, smallest-singular-
value small ball, exact rational LDL fallback, resolvent continuity and binomial
matrix approximation check independently. UNITARY_PORT.md supplies a concrete
known-unitary gate completion uniformly in growing r, up to the irrelevant
overall phase. All relative controlled phases are preserved.

Use a KNOWN support bound dbar=floor(1/a)+1 and its padded power of two r;
no actual-rank oracle is required. Ambient registers may be padded to at least
r, with their actual qubit/control costs. The matched symmetric-group basis
between the two Schur transforms is essential; an arbitrary untracked basis
change is not free. Corrected high-D Schur and ordinary small-d BCH controls
are the primary predecessors. Their costs are polynomial in carrier number,
r, log D and precision; r itself is polynomial in the accuracy target.

For example, if M=N_training+1, assign B's full per-filter error
zeta=gamma/(2M). Its entire batch contributes at most gamma/4 in half-diamond.
Assign C's whole compression budget gamma/4 and leave gamma/2 for known
tomography/recovery controls. Set B beta_gap=4q. This is a literal finite
allocation, rather than an uncharged O(gamma) approximation. Bad thresholds
add at most q in half-diamond since their processor remains CPTP.

## 8. Noise-oblivious schedule and scope

Take a=epsilon^2/(192k^2d0), delta=epsilon^2/(48k^2), beta=gamma=epsilon/4,
q=epsilon/8. Then k sqrt(12d0 a+3delta)=epsilon/(2sqrt2), and the sum of
accuracy, tomography, controls and bad-threshold charges is below epsilon.
Splitting the remaining square root yields

    halfdiamond(decoded,id)
      <=epsilon+k sqrt(4kappa+6 tail_d0(A)).

This operation does not require numerical kappa or tail as inputs. It does not
verify them, acquire an optimal intrinsic rank, produce a reusable offline
original-frame decoder, or implement an opaque inverse. Its quantum-control and
coherent-memory assumptions are strong. Costs are large polynomial ideal
algorithm bounds, not native apparatus performance or a practical advantage.
Strong ordinary recovery SDP after small tomography is fully admissible.
