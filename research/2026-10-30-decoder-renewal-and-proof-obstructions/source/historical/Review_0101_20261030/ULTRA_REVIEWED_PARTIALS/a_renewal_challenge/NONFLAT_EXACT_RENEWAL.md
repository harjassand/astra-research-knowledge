# Exact universal renewal for an arbitrary full-rank junk spectrum

30 October 2026. A reviewer-owned supplementary theorem derived while
challenging root's flat-spectrum coverage/Schur proof. Root independently
reconstructed the proposed extension; the final written theorem remains
separate from the unchanged root proofs. No numerical case, quantum/source
execution or optimization is used.

## 1. Native class and theorem

Let k>=2, r>=1 and D>=kr. Fix a full-rank junk density matrix sigma on C^r
with eigenvalues p_1,...,p_r>0, sum p_j=1. The native source is

    N_U(X)=U(X tensor sigma)U^*, U:C^k tensor C^r -> C^D
    an arbitrary unknown isometry.                         (N1)

All forward source calls are memoryless uses of the same N_U. A universal
controller may know the spectrum (and the result still holds if it does not).
It can use arbitrary known controls, finite-query adaptive/entangled inputs,
retained unknown quantum memory, instruments and all paid offline programmes.
No free U-dependent advice, unknown adjoint/controlled dilation, source
environment or intervention on the junk input is supplied. Count all native
calls apart from the original encoding of the single unknown payload.

An EXACT heralded success is the unnormalized identity subchannel

    S_U composed N_U = s_U id_k,                           (N2)

for every U and every payload/reference. The scalar s_U may depend on U.
Failure may retain arbitrary quantum history; it need not reset anything.

Let G_j be independent geometric(p_j) variables on {1,2,...}, and put

    T_p=G_1+...+G_r,
    b_p(Q)=Pr(T_p<=Q).                                    (N3)

Then EVERY capped Q-native-query exact controller satisfies, pointwise in U,

    s_U <= b_p(Q).                                        (N4)

Every exact almost-surely terminating universal inverse consequently obeys

    E_U Q_stop >= sum_(j=1)^r 1/p_j >= r^2,                (N5)

for every U; an infinite expectation is allowed. At p_j=1/r this is exactly
root's binomial-tail bound b_p(Q)=Pr[Bin(Q,1/r)>=r] and mean r^2. There is no
assertion of attainment, useful expected cost, a tight minimum-query threshold
or an approximate-decoding lower bound.

Full rank and exactness matter. A positive eigenvalue may be arbitrarily
small, but it cannot be set to zero for free. If sigma has smaller true rank,
apply the theorem to its actual positive spectrum and corresponding smaller
r. When k=1 the logical output is trivial and the theorem is not asserted.

## 2. Strip the fixed positive weights before the polynomial argument

Choose the junk eigenbasis only FOR ANALYSIS and absorb its unknown/public
basis convention into U. Write U_j x=U(x tensor |j>), so a native Kraus
operator is sqrt(p_j) U_j. This does not expose that basis or a flag to the
physical controller. The isometries satisfy U_l^*U_j=delta_lj I_k.

For a fixed Q-query label tuple q and a fixed known-control environment
branch h, write its unnormalized success operator on the physical payload as

    R_qh(U)=[product_(t=1)^Q sqrt(p_(q_t))] Rtilde_qh(U).   (N6)

The entries of Rtilde are holomorphic polynomials of total degree Q in the
queried U blocks, multilinear in the source SLOT variables. All known
controller coefficients, including any dependence on the supplied p, are
fixed at this point. They cannot depend on unobserved q. Born normalizers
do not occur in an unnormalized branch.

Including the native payload label j, the success-channel Kraus operator
is sqrt(p_j) R_qh(U) U_j. The Choi matrix of (N2) has rank one. Every
positive Kraus summand therefore lies in the identity Bell ray, so

    Rtilde_qh(U) U_j = c_qhj(U) I_k                       (N7)

for all j and all U. Every scalar stripped in (N6),(N7) is positive. They
have not been dropped at a vanishing-probability branch by approximation.

If q omits label l, Rtilde is independent of U_l. Right rotating ONLY that
logical k-column block by any nonscalar V in U(k) leaves the query amplitude
unchanged and preserves the family of allowed source isometries. Applying
(N7) before and after that rotation forces Rtilde_qh(U)U_l=0 for every U.
The root proof's polar/entire-function argument extends this polynomial
identity to all complex matrices, including rectangular matrices by taking
the first kr columns of a D-by-D matrix. Since U_l is then freely variable
and Rtilde does not contain it, Rtilde_qh is identically zero.

This is the same exact unused-block lemma, now with the correct weight
handling. Arbitrary finite-query instruments are covered by a finite
success-comb/Kraus realization; source probabilities and conditional
measurement probabilities are not granted as known controller coefficients.
Offline acquisitions and any repeat/abort branches are part of the whole
query instrument and are charged in Q.

## 3. A family rotation replaces the flat-spectrum gauge argument

Fix U,h. Define the raw coefficient map on E=(C^r)^tensor Q by

    Ttilde_Uh |q> = Rtilde_qh(U).

For every W in U(r), U'=U(I_k tensor W) is still an allowed isometry. Raw
multilinearity gives the exact identity

    Ttilde_U'h=Ttilde_Uh W^tensor Q.                       (N8)

For NONFLAT sigma, N_U' generally differs from N_U. It would be WRONG to
call (N8) a Kraus gauge preserving the channel. That preservation is not
needed: universal correctness holds for every U' in the SAME fixed-spectrum
family (N1), with the SAME controller. The unused-block zero consequently
holds for U', which makes Ttilde_Uh annihilate

    span_(W in U(r)) (W C^(r-1))^tensor Q.                 (N9)

Schur--Weyl decomposition identifies this as the sum of all height<r query-
environment components, with full Specht multiplicities. Let Pi_r be the
central symmetric-group isotypic projector onto precisely the components
of Young height r. Then

    Ttilde_Uh=Ttilde_Uh Pi_r.                             (N10)

The ACTUAL coefficient map restores the weights:

    T_Uh=Ttilde_Uh D_p^tensor Q, D_p=diag(sqrt(p_j)).       (N11)

Every tensor power D_p^tensor Q commutes with permutations and hence with
their central projector Pi_r. Thus T_Uh=T_Uh Pi_r too. The physical query
environment amplitudes are ket coefficients (rather than arguments of T),
but Pi_r is real symmetric, so their support is the SAME projector rather
than an uncharged conjugated one. The entire success Stinespring branch,
including the payload's separate junk label, is supported on Pi_r in its
QUERY environments.

The logical ingredient here is universal exactness under rotations of the
family; the probability spectrum need not be uniform. No source experiment
can choose W or measure these environment sectors, and none is being added.

## 4. Adaptive environment marginal and success domination

The canonical Stinespring dilation has complementary channel

    N_U^c(X)=Tr(X) sigma_E,
    sigma_E=diag(p_1,...,p_r).                            (N12)

This is a COMPLETE replacement map on any entangled input: on a retained
reference Z it gives rho_Z tensor sigma_E. At each source call, previous
query environments can be part of Z. Intervening known trace-preserving
controls and later operations cannot change their unconditioned marginal.
Inductively the Q query-environment marginal of the WHOLE completed
experiment is exactly sigma_E^tensor Q. It need not be independent of
the controller's physical carriers; after conditioning on success it is
generally NOT a product and must not be declared known or flat.

The success state is a positive substate of this whole state and is
supported in Pi_r. Therefore

    s_U <= Tr[Pi_r sigma_E^tensor Q]
        = sum_(lambda partitions Q, height(lambda)=r)
                 f_lambda s_lambda(p_1,...,p_r).          (N13)

This bounds adaptive physical-query algorithms, not only iid programmes.
There is no assumption that the query inputs, payload or retained quantum
memory are classically known or repreparable. The unconditioned marginal
(N12), not an independence assumption about those accessible systems, pays
the upper bound.

## 5. Exact biased-RSK probability and stopping-time implication

The ordinary word-RSK/Schur--Weyl identity says that the weight of a Young
shape lambda for iid letters with probabilities p_j is
f_lambda s_lambda(p). Its height is the longest STRICTLY decreasing
subsequence length. With exactly r symbols, height r is equivalent to the
appearance of the single ordered pattern (r,r-1,...,1).

Greedily wait for r, then r-1, down to1. Independence of the successive word
letters makes the waits independent geometric(p_r),...,geometric(p_1).
Thus (N13) is exactly b_p(Q), proving (N4). In particular the finite-Q
distribution is independent of how the spectrum labels were ordered: sums
of independent geometric variables commute in distribution. Its probability
generating functions are

    E z^T_p = product_j [p_j z/(1-(1-p_j)z)],
    sum_(Q>=0) b_p(Q) z^Q = E z^T_p/(1-z),  |z|<1.        (N14)

For a variable-length exact inverse, success by time Q is an exact positive
subinstrument. Pad its stopped branches to Q source calls on discarded
dummy inputs, keeping the already produced logical output. The resulting
capped controller satisfies (N4), so

    Pr_U(Q_stop<=Q)<=b_p(Q).

There is no claim that the actual unmeasured quantum Schur sector produces a
classical flag path with that waiting time. This is stochastic domination
obtained separately at each Q. Summing its tail proves (N5). It permits
arbitrary retained failure history and does not assume a restoring cell.

Two additional transparent necessary bounds follow, without asymptotics:

    b_p(Q)<=binomial(Q,r) product_j p_j,
    b_p(Q)<=1-(1-p_min)^Q.                               (N15)

The first is the union bound over the positions of the full decreasing
pattern; the second follows since T_p includes a geometric(p_min) wait.
In particular fixed nonzero exact success requires quadratic rank at least,
and also enough calls to see a very rare positive eigenmode in this precise
unambiguous sense. None of these inequalities is transferred to fixed-error
approximate recovery by replacing zero with epsilon in the polynomial proof.

## 6. Ordinary predecessors and exact boundaries

One-sided quantum rank testing already supplies the full-height Schur
projector, Schur polynomial probabilities and its rank-squared sample scale:
O'Donnell--Wright1501.05028v1, Sections2.3--2.5 and6.1, especially
Proposition6.1. These classical/representation ingredients are credited,
not invented here. The biased geometric-wait description is ALSO explicit
in the proof of their Lemma6.2(i), and the uniform specialization in
Proposition6.4. It is not a new probability law. The native link (N6)--(N13)
is the operation obstruction:
every exact universal recovery must put its SUCCESS on that environment
support even with coherent adaptive query inputs. The environments remain
unavailable to the controller.

Probabilistic unitary inversion1810.06944v3 and success-or-draw2011.01055v2
give genuine exact/heralded or restoring constructions under their UNITARY
query contract. They are granted as such. Applying their d=kr version would
require coherent access to all kr input dimensions of U; N_U supplies only
k dimensions and internally samples the junk. Neither a supplied full U
nor its adjoint is acquired here. The existing exact exterior-hole decoder
is also compatible: its tiny finite success probability need not attain
the spectral tail bound, and its failure was not a restoring draw.

No generic no-memory theorem, quantum sample-only lower bound for approximate
decoding, useful practical decoder, or hardware limitation follows. Exact
renewal can be singular as p_min goes to zero; approximate methods may
legitimately ignore sufficiently small probability mass if they acquire the
needed operation and its error. This theorem does not supply or exclude
that operation. Historical priority of this native spectrum-dependent
reduction is UNKNOWN; no complete literature absence was established.
