# Two stronger quantum-entropy boundary receivers

The independent challenge accepts the producer's weak-reset and finite
positive-ray theorems at their stated scopes, and constructs two stronger
receivers. Both strengthened proofs have received a completed independent
whole-proof review, including the noncommuting steps and CMI normalization:
[archived peer challenge](sources/peer_challenge.md).

## 1. Arbitrary coherent resets without a condition-number penalty

Use qutrits A,B, any finite logical L, the UNNORMALIZED Omega=sum_i|ii>,
W3(Z)=(TrZ I3-Z^T)/2, N=W3 tensor id, E=I3/3 tensor Tr_A and
Delta(Z)=TrZlogZ+Tr(EZ)log(EZ)-2Tr(NZ)log(NZ), in nats. For

    X=P_Omega tensor C+I_A tensor Y, C>=0,C!=0,Y>=0,
    Y<=(I_B tensor C)/192,

the strengthened certificate is

    Delta(X)>=(869/2592)TrY>TrY/3       if Y!=0.

There is no reference-dimension, reset-rank, commutation, spectral-flatness
or condition-number restriction. For singular C the displayed order forces
Y into its logical support. It does not cover reset leakage outside that
support. Keeping the exact weighted logC terms removes the old kappa² loss;
using actual binary pinching probabilities improves the radius512 to192.
No nonunitary filter or presumed congruence invariance of Delta is used.

The actual unflagged CPTP channel is
Lambda(M)=[M tensor C+Tr(M)Y]/(TrC+TrY). Its normalized Choi state is
X/[3(TrC+TrY)]. The antisymmetric qutrit isometry therefore gives

    I(Q1:Q2|reference)>=log3+(869/7776)p_reset,
    p_reset=TrY/(TrC+TrY).

A discriminating exact rational input has C eigenvalues1,10000 and a
complex, full-rank coherent Y with operator Schmidt rank4. It obeys the new
relative-order certificate, while ||Y||>=20.3556 exceeds the old permitted
1/(512*10^8) by more than1.04e12. Even ||Y||<=m/192 would miss this point;
the weighted order matters. Its certified CMI excess is.00134829 nats;
ordinary dense and mp65 calculations give.02313928. A direct54-state
extension reproduces CMI-log3=Delta(rho) within1.56e-14 numerically.

Additional exact inputs exercise kappa1e8, a flat main with arbitrary reset,
and singular aligned logical support. These are finite controls of the
implementation. The all-dimensional theorem comes from
[PROOF.md](PROOF.md), not from extrapolating those inputs.

## 2. Every positive direction with polynomial-bit finite radius

For the ORIGINAL A0=P_Omega tensor C, C>=mI,m>0, let H>=0 be any density
operator on ABL and ell=Tr[((I-P_Omega/3) tensor I)H]. If ell=0, the deficit
is exactly zero. If ell>0,

    eps<=m ell²/(2^14 r²)
      implies Delta(A0+epsH)>=eps ell/2.

The proof retains the weighted support logs and the NEGATIVE small-kernel
entropy. They yield the finite estimate

    Delta/t>=(ell/2)log(1/t)-ell log(24r/ell)-ell-2t,
    t=eps/m.

This removes both the producer's kappa factor and its exponential output-
precision dependence on inverse leakage. The r²/ell² radius remains explicit.
Rational input gives an endpoint of O(bits(m)+2bits(ell)+log r) bits.
The derivation is in [GENERAL_POSITIVE_RAY.md](GENERAL_POSITIVE_RAY.md).

For the root/producer's source outside the declared reset/bath closure,
H_star=[I9+(E01+E10) tensor diag(1,-1,0)/4]/9, the new exact endpoint is

    eps=1/20736, Delta>=1/46656,
    I(Q1:Q2|reference)-log3>=4/559881.

Its allowed eps is50.568 times the earlier finite-ray endpoint. The
off-diagonal reference block has nonzero square, preserving the structural
separation from the declared reset/bath closure. This does not classify
every independently known positive source family.

A separate arbitrary r2 density direction has a NONUNIFORM physical
marginal. Its endpoint is about1.18791e-5, versus2^-32 for the old receiver.
An explicit nine-Weyl flag grows reference6 to54. The complete486-state
extension's CMI agrees with mp70 Delta(rho) within9.49e-15. The flag and
reference growth are charged; no unflagged physical-marginal correction is
assumed. The exact normalized CMI certificate is3.49376e-7 nats.

## Accepted review and boundary

Independently checked: N*(P_sym)=(3/4)(I-P_Omega/3), both complementary
channels on all9 matrix units, the Choi factor3, entropy pinching and Davis
compression, the old finite theorem's inequalities, both stronger finite
proofs, singular aligned support, rational constants and actual CMI offsets.
The peer independently reconstructed both stronger proofs and consumed their
endpoints with separate exact PSD inputs and no imports of this code.

The original general leakage asymptotic is valid for C>0, but is not itself
a uniform radius. The new finite inequality supplies that missing operation.
Its premise always uses the ORIGINAL A0; iteration through arbitrary accepted
states is not proved. The weighted reset receiver is dimension-uniform in
finite L; the general-ray receiver explicitly pays r².

No unrestricted W3 result or global squashed-entanglement infimum is proved.
The broader quantifier is visible in
[CLR v3, Sec.4 and Conjecture4.5](https://arxiv.org/html/1403.3816v3).
Current N1096's flat rank-one/two-level and structured common-bath boundaries
remain intact. No historical-priority clearance, practical advantage over
equally informed ordinary matrix methods, physical channel, tomography or
CMI measurement is acquired.

Exact matrices, factor certificates, ordinary controls, independent review
versions and replay are preserved. [COSTS_AND_REPLAY.md](COSTS_AND_REPLAY.md)
states what the numerical controls do and do not establish.
