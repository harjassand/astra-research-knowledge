# A qualified finite operation beyond reset-family closure

The bounded attack produced a general local entropy receiver and exact
computational acquisitions. The civilisation-level mission is NOT_ACHIEVED.
Physical implementation and external priority are not established.

## Current operation

Let A,B be qutrits, L=C^r, Omega=sum_i|ii> unnormalized, p=P_Omega/3,
A0=P_Omega tensor C, C>=mI>0. Let H be ANY PSD density operator on ABL,
TrH=1, with ell=Tr[((I-p)tensor I)H]. For ell>0, the current receiver is

    0<eps<=m ell²/(2^14 r²)
        => Delta(A0+epsH)>=eps ell/2,
    Delta(X)=TrXlogX+Tr(EX)log(EX)-2Tr(NX)log(NX),
    N=W3_A tensor id, W3(Z)=(TrZ I3-Z^T)/2,
    E=I_A/3 tensor Tr_A.

No reset form, rank, commutation, Schmidt alignment or upper condition
number is required. At ell=0, positivity keeps H inside the isometric
support and Delta=0 exactly. The rational endpoint has polynomial bit
length in the supplied m,ell and log r. Acquisition of the full H,C and
their PSD/order information remains charged.

The original general-direction construction is in POSITIVE_RAY_OPERATION.md.
Root independently derived its finite proof. The independent boundary
reviewer then strengthened its exponential k-radius to the displayed
quadratic radius in `../quantum_boundary_review/GENERAL_POSITIVE_RAY.md`.
I whole-read and independently challenged that proof: PEER_CHALLENGE.md
records acceptance at the exact mathematical scope. Ownership is preserved;
the stronger theorem is not relabelled as solely producer work.

This is a finite positive-admixture qualifier near the ORIGINAL A0. It
does not permit reapplying the operation around an arbitrary previously
accepted state, or prove unrestricted Werner–Holevo contraction.

## Actually acquired sources, margins and cost

`acquire_quadratic_radius.py` verifies rational input PSD/order conditions
by Schur elimination, compiles the scalar endpoint/margin and retains every
source entry. The two acquired cases are:

| Case | r,ell | eps | Certified normalized CMI excess, nats |
| --- | --- | --- | --- |
| Exact TP source outside old reset/bath closure | 1,8/9 | 1/20736 | 4/559881 |
| General coherent density direction, nonuniform physical marginal | 2,1582/2127 | 625681/74123329536 | 494913671/1418944228131135 |

The first uses H_star=[I9+(E01+E10)tensor diag(1,-1,0)/4]/9 and C=1.
Its physical off-diagonal block has nonzero square, unlike every seed and
closure member in the old reset/bath package. Root separately reconstructs
the original fixture in `../parent/general_quantum_direction/`.
The second uses full-rank H=(I18+uu^T)/(18+u^Tu), u=(1,...,18), C=diag(1,2).
All matrices and exact margins are in outputs/QUADRATIC_RAY_INPUT_R1.json
and R2.json, with a compact aggregate QUADRATIC_RAY_ACQUISITION.json.

The normalized source is rho=(A0+epsH)/(3TrC+eps). An antisymmetric
qutrit isometry V has W3 as BOTH complementary channels, yielding

    I(Q1:Q2|reference)-log3=Delta(rho).

The first source is already TP Choi. The second needs the explicit
nine-Weyl flagged twirl, retaining the same deficit while enlarging the
reference6->54; the controlled choices/classical label are not free.
`acquire_positive_ray.py` independently checks all18 complementary-channel
components on 9 matrix units, both isometry projectors, all 9 twirl units
and the exact adjoint leakage identity. No reviewer code is imported.

Exact input/receiver work took .00847s and .04183s after imports, with
82 and 328 supplied C,H matrix entries. Maximum recorded reduced rational
numerator/denominator bits were 18/40 and 72/95; Schur-recorded ratios used
6 and 22 bits. These maxima exclude unreduced arithmetic temporaries.
Whole consuming run was .05774s excluding imports. Peak RSS was not measured.
Separate ordinary eigensolver diagnostics give normalized excesses about
7.82511e-5 and4.93370e-6; they are NOT directed entropy enclosures or
physical error bars. No runtime advantage follows from these observations.

## Strong comparison and closure limits

CLOSURE_INVARIANT.md proves a robust near-isotropy invariant for the
DECLARED reset/ray/white/bath/flagged/isometric package. It is a diagnosis
of that package, not a barrier for all known science. Root's exact ordinary
comparator rho_cc=(1/3)sum_i|ii><ii| has physical signal rank2 and
Delta=log(4/3)>0, immediately breaking the invariant when established
classical seeds are admitted. No claim that anisotropy itself is an
unavailable capability survives that comparator.

An equally informed ordinary analyst may use every standard entropy,
pinching, matrix-log and SDP technique used here. The local theorem gives
a uniform sign certificate from qualified scalar/matrix data; the finite
eigensolver is a different, instance-value query. These are not a matched
runtime separation. Generic machinery and the squashed-entanglement
interpretation are established, not new inventions.

The shortest GLOBAL consequence remains sharply scoped: unrestricted
Delta positivity, if established, would give E_sq(alpha3)=log3/2 via the
antisymmetric isometry and a finite nine-Weyl flag. This programme has not
acquired that global operation or a valid arbitrary-state composition.
The exact positive-ray extension is genuine movement beyond the old reset
normal form, with its local radius and acquisition costs intact.

## Source and auxiliary scope

Task-first Astra entry, current index, N1096 packet and governing sources
were acquired at 8d51d60762b3ee28c10aaaa56e1b92da119dc1cc. No old search pin
is silently relabelled current, no archive was loaded, and no Capital or
protected-producer interaction occurred. Current source/hash receipts are
under source_cache/. N1096 provides the earlier rank-one reset/flat-main
and structured noncommuting-bath family; its hypotheses remain distinct.

The exact primary conjecture is [Carlen–Lieb–Reuvers2016,v3,
Sec4 Theorem4.4/Conjecture4.5](https://arxiv.org/html/1403.3816v3).
An initial v2 cache is older and is NOT used as the governing conjecture.
[Fawzi–Fawzi2022,Secs3–4](https://arxiv.org/html/2203.03394v1) supplies
the stronger ordinary SDP/squashed-entanglement context and its own stated
convergence limitations. Those historical sources do not certify the
absence of every later world result. World priority remains UNKNOWN.

Preserved auxiliary work includes the original weak-reset theorem and
exact nonflat/full-rank reset fixtures; the independently strengthened
relative-order condition Y<=(I_B tensor C)/192 belongs to the reviewer.
WHITE_CURVE_COMPLETION.md records an entire-white bridge feeding the
existing bath lift; it is not needed by the new general-ray theorem.
The earlier 600-point orbit diagnostic and 92 variational runs prove no universal
statement. They did not produce a certified negative deficit.

Unrestricted contraction: NOT_ESTABLISHED here. Physical channel,
tomography and CMI measurement: NOT_ACQUIRED. General practical/method
advantage and historical novelty: UNKNOWN. Civilisation-level capability:
NOT_ACHIEVED.

## Reproduce

From the workspace root, run the existing scientific Python runtime on
`acquire_positive_ray.py`, then `acquire_quadratic_radius.py` in this folder.
The first emits its own exact C,H inputs and the9-unit normalization replay;
the second reads them and writes the current quadratic-radius acquisitions.
`acquire_weak_reset.py` separately reconstructs the earlier reset fixtures.
These scripts write only this folder's outputs. Timings exclude imports
and can change on replay; theorem acceptance and source provenance are
recorded separately from original acquisition status strings.
