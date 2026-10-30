# Same-access comparison: a certified mixed-source adaptive gap

30 October2026. This compares the completed physical-query controller with
the strongest two-query PARALLEL competitor, rather than only normalized
iid Choi programmes. The general linear-r high-accuracy goal remains open.

## 1. What the parallel class is allowed

The source is the same exact flat qubit encoder of rank r=2. Initially take
D=4, arbitrary unknown U in U(4). Allow arbitrary ancillary systems,
arbitrarily entangled logical inputs to the two parallel N_U calls, general
known preprocessing and postprocessing, and coherent quantum programme
storage. A reference-entangled unknown payload is singly encoded by N_U.
No inverse, junk access or quantum switch is supplied to either side.

The covariance reduction does not assume that an arbitrary preprocessor
literally ignores a payload that was already available. Average over the
unknown physical frame. Before either output is received there is only
ONE physical fundamental representation, the payload. The reduced Choi
operator of the preprocessor, after tracing its memory, must commute with
that irreducible U(D) representation and is therefore I_payload tensor a
logical-query state. Stinespring uniqueness moves any remaining coherent
payload/query correlation into known final memory processing. Thus the
parallel normalizer below permits the complete parallel class at this
covariant minimax task. It is stronger than assuming iid Bell programmes.

## 2. The finite exact dual model

Use root's Choi grouping into three logical legs(final output,query1,
query2) and three physical legs(payload,out1,out2). After the left physical
and right logical covariance averages, permutation operators span each
commutant. Let P_s be a logical S3 permutation, Q_t a physical S3
permutation, c(t) its cycle count, and G_D(s,t)=D^[c(s^-1 t)]. The
performance operator is

  Omega=sum_(a,b in S3) (G_D^-1)_(b,a)
                      r^[c(a)-3]/4 * P_a tensor Q_b.      (1)

The normalization is independently fixed by closing a permutation:

  Tr[(P_s tensor Q_t)Omega]
       =2^[c(s t^-1)] r^[c(t)-3]/4.                      (2)

A parallel deterministic comb C is positive and obeys

  Tr_(logical output) C =rho_(query1,query2) tensor I_phys,
  Tr rho=1.

Take a Hermitian Y=I_(logical output) tensor Y0 such that

  Y-Omega>=0,
  Tr_phys Y0<=lambda I_(query1,query2).                  (3)

Then Tr C Omega<=Tr C Y<=lambda. This is the ordinary Choi weak-dual
argument, without reliance on strong duality, numerical optimality or a
hierarchy cutoff. A dual certificate is an exact global upper bound for
the full continuous source family, not a Haar-sample fit.

Root's `root_comb/PARALLEL_DUAL_CERTIFICATE.json` supplies twelve rational
coefficients in Y0 and lambda=29751457437/68719476736. Logical U(2)^tensor3
has S3 irreps trivial/standard (the third exterior power is zero), while
U(4)^tensor3 has all three. In the rational standard basis(e1-e3,e2-e3),
the Gram metric is [[2,1],[1,2]]. The six Gram-congruent slack blocks in
(3) all have EXACT positive LDL pivots. The two logical-input symmetry
sector values are both exactly lambda. Hence

  Fe_PAR<=29751457437/68719476736=.4329406865435885.       (4)

C whole-read root's code/certificate and reconstructed the dual model.
The separate stdlib `receive_parallel_dual.py` REBUILDS all six blocks
from(1) and the twelve rational coefficients, verifies every saved entry
and LDL pivot, and checks both input-normalization values. It does not
import root's implementation, call a solver or rerun a source/Haar case.
Its actual receipt is PARALLEL_INTAKE.json; this is substantive exact
intake at the stated finite-query/source-family scope.

## 3. The resulting operational inequality

The actual coherent feedback controller's separate exact CPTP certificate
gives

  Fe_AD>=55716029295809/123760695281664>.45,
  Fe_AD-Fe_PAR>=71638340317230378547/4152719834101315534848
              >1/80.                                    (5)

The Pauli-query intervention in C_COHERENT_FEEDBACK Section5 makes its
logical composite a Pauli channel without touching the encoded payload.
Thus its all-input/reference halfdiamond error is at most1-Fe_AD.
For EVERY parallel controller, the Bell-input error is at least1-Fe,
and the Haar average satisfies(4). Therefore its worst-source complete
halfdiamond error is at least1-lambda. This is a strict full-throughput
minimax adaptive-versus-parallel error gap, not only a comparison of
average bit prediction or two floating solver outputs.

The upper(4) also obstructs a uniformly better parallel method in any
ambient D>=4: restrict its unknown source to a fixed public4-dimensional
subspace, then embed a D=4 source output there. All extra known workspace
and final processing were already allowed by the D=4 comparison. The
positive controller itself works at every D>=4 with the same coefficients.
The literal certified comparison is rank two, not all ranks; its exact
all-r family is a separate positive result, not a uniform claim of
parallel dominance.

## 4. Strong ordinary high-accuracy alternative and the live gate

A's `a_ordinary/FLAT_RDS_RECOVERY.md` gives an admitted SAME-access
high-accuracy alternative. RDS produces one joint random-dilation frame;
the exact flat mean removes generic inverse-mean filtering. Known-amplitude
amplification needs2r+1 ideal reflected-code calls. Paying their
copy-programmed supplier gives O(k^2 r^2/epsilon) original source calls,
all acquired offline, with a consumed protected quantum programme and
online collision gates. Its actual all-input accuracy and offline timing
are stronger than our two-query cell. Comparing its near-perfect guarantee
to our error near.55 would be an unmatched speedup claim.

Pure isometry inversion is also given full strength:2401.10137v3 permits
four adaptive forward qubit-isometry queries for exact code-range inversion
at arbitrary D. A subsequently read the ACTUAL covariant conversion's
off-code action in AppendixA.4 Eqs208--225, and C directly read those
same primary passages. Its unflagged map is

  D_V(X)=v V*XV +[TrX-v Tr(Pi_V X)]I/k,
  v=(k^2 F_UI-1)/(k^2-1).

On I_E/r tensor N(rho), this gives
(v/r^2)rho+(1-v/r^2)I/k. The exact four-query pure inverse therefore has
Fe=1/k^2+(1-1/k^2)/r^2 on that mixed input. Its published outside flag is
a replacement branch, not a restoring draw. This scopes THAT specified
conversion, not every possible coherent retention of its garbage. Four
forward dilation-isometry slots must also be acquired from the original
source; they are not four free original N calls. Its stated generic CG
gate cost is polynomial in the isometry dimension, not free polylogD.
This pays a real strong route rather than stopping at an underdetermined
abstract code-range promise. RDS storage/retrieval lifts and known unitary inversion's
success-or-draw constructions do not by themselves supply the required
mixed-payload restoring history. Their state/operation timing contracts
are maintained, not dismissed because they use familiar vocabulary.

Quantum adaptivity already has published advantages for pure unitary
inversion (2109.08202v3/2401.10137v3). No first quantum-adaptivity or
historical-priority claim follows from(5). Mixed-channel adaptivity is
also established: Bavaresco--Murao--Quintino2011.08300v2 Theorem1 gives
a strict two-query sequential-versus-parallel advantage for discrimination
of two mixed qubit channels. Our earned scope is unknown flat REVERSIBLE
quantum-payload recovery, full throughput and a uniform complete-channel
receiver, not a first mixed-channel adaptive separation. The paid mixed-source circuit,
all-r positive controller family and its exact causal resource distinction
are the earned result. The next actual gate is a scalable coherent-history
controller, not a better rank-two fit. Unknown-state cloning, pretending
the coherent Pauli label is a classical record, or upgrading N1104's
iid-Choi lower to arbitrary queries would avoid that gate incorrectly.
