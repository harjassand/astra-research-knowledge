# Prior, access and complete costs

30 October 2026. Companion to PROOF.md. There is no new source/model or
quantum-controller execution in this package.

## The controlling working predecessors

1. Yoshida, Niwa, Utsumi, Takagi and Murao,
   [Random dilation superchannels](https://arxiv.org/html/2512.21260v2),
   Theorem 2/(31)--(37), Theorem 3/Fig. 2(a)/(38)--(39), and Lemma 6/
   Fig. 6/(45)--(50). These give the exact random-purification and
   common-phase pure-state conversions used here. The normalized Choi
   vector is a special pure-state input to those ordinary operations.
   Their proof explicitly warns that its P-CTC illustration is not an
   actual store-and-retrieve circuit for arbitrary open channels. Our
   whole-bank conversion retrieves NO open channel and uses NO P-CTC.

2. The accepted N1104 iid-Choi lower bound, retained read-only at
   ../../sol28_active_inverse_and_alternatives_20261030/c_active_inverse/
   source_entry/mixed_flag_quadratic_choi_program_lower_bound.md.
   It states logical k=3. PROOF section 4 derives the actual k=2/all-k
   version, with the Hilbert--Schmidt SU(kr) concentration normalization
   already supplied in that theorem. The external primary input is
   [Meckes--Meckes1210.2681](https://arxiv.org/html/1210.2681), the
   log-Sobolev inequality used in their Theorem 15 argument. This is a
   dimension port of that accepted proof, not reopening its premise.

3. The earlier full-throughput flat inverse in ROOT28 a_ordinary/
   FLAT_RDS_RECOVERY.md remains available: O(k^2 r^2/epsilon) original
   queries, a consumed quantum programme, zero original-source queries
   online after preacquisition, and all O(r) reflection/controller steps
   plus their actual programmed collisions. The present theorem applies
   even to a different joint processor of its entire specified bank. It
   does not prove DME optimal, an optimal epsilon law or online latency.

4. Yoshida--Murao,
   [Optimal complex conjugation of unknown isometry channels](https://arxiv.org/html/2607.29054v1),
   Corollary 11/(140)--(144), was read directly again in this work. It
   supplies a real deterministic approximate k->D conjugate channel from
   at most k(rD-k)/epsilon parallel source calls, known CG circuit cost
   polynomial in rD and inverse accuracy. At D=kr its bill is quadratic
   in r. It is not the D->k inverse, nor an acquired coherent inverse
   block or restoring branch. Its parallel circuit is admitted at its
   actual stronger input access, not forced inside the bank class.

5. Optimized qubit PBT and the forward storage/retrieval port in ROOT28
   a_ordinary/FORWARD_SAR_PORT_AND_LIMIT.md remain admitted. The optimized
   PBT resource uses genuinely entangled logical inputs to the open RDS
   service. It must not be relabelled as a maximally mixed-input bank.
   The specified pure-isometry off-code converter and its exact mixed-
   payload ceiling remain closed as recorded there and in
   OFF_CODE_ISOMETRY_MAP.md. This package does not repeat that derivation.

6. C's frozen ROOT28 single logical-spin programme is a granted stronger
   comparator beyond the bank. Its exact fidelity bound shows that
   concentrating the input in one Schur sector is not by itself a cure.
   It is not a theorem for all logical profiles or all adaptive inputs.

These are ordinary state/channel manipulation mechanisms. No generic
novelty is claimed for Bell sampling, gate teleportation, Schur controls,
postselection, input filtering or random purification. The new scoped
consequence is the access-class reduction and its finite full-error
composition. Historical priority for that consequence remains UNKNOWN.

## The output and input resources of the new constructions

| Construction | Original source / Choi use | Other acquired input | Result and full error |
|---|---:|---|---|
| Whole bank | Q Choi copies, each from one forward N call | Public V0; known random-purification and conditional-sample controls | Exact ideal B_Q(U), one common V and theta, neither exposed |
| Literal RDS factory with uniform actual query marginal | Q Choi copies | Known preprocessor/postprocessor | Entire post-query state, including retained public records/workspace; no open-channel retrieval |
| Arbitrary known offline parallel query state | Q ceil(chi/delta) Choi copies | Its known reference-side contraction; arbitrary known matrix cost allowed | Same entire programme, half trace error <=delta |
| Known block probes, physical Bell route | M=ceil(sum m_i k^(2m_i)/delta) Choi copies | Supplied known probe preparation for every trial; Bell measurements | Whole common-frame programme, half trace error <=delta |
| Known block probes, explicit matrix route | M=ceil(sum m_i k^m_i/delta) copies; optionally sum m_i chi_i | Complete known probe coefficient matrices and their contraction dilations | Same programme, same delta; no efficient succinct-matrix promise |

The second row's source-query marginal is the one JUST BEFORE the native
N calls. A maximally mixed external input does not establish this for an
arbitrary undocumented preprocessor. PROOF section 2 checks the actual
controlled-permutation preprocessor in the primary RDS figure.

The capped Bell route prepares one common M-copy purification first.
Its queue never asks a later independently generated bank to share the
old random frame. Every abort is completed by a fixed known output,
not a heralded service loss. Conditional-on-completion programme quality
is exact in the ideal construction; the unconditional full-throughput
error is at most delta. With a downstream e-error decoder and a further
controller simulation error zeta, the result has error at most
e+delta+zeta, uniformly in U and including references. The Fano bound
must be applied to that TOTAL error, below 1-1/k.

If G_i is the known gate count to prepare probe i, the Bell route has
at most M trials and gate work bounded by

    purification_cost(M,r,kD,zeta/constant)
      + conditionalisation_cost(M,log(krD),zeta/constant)
      + M max_i[G_i+O(b log k)]

plus routing, initialization/discard and synthesis at a precision divided
over that finite gate list. It stores M common-frame Choi carriers of
O(log(krD)) qubits each, all accepted output probes/references, queue
records and the stated Schur/control workspace. This is not a classical
learning method or an acquired laboratory primitive. The retained
ROOT25 finite uniform-Schur/twirl port pays a conservative polynomial
dependence on M,r,1/zeta, not a fixed-r irrep enumeration.

The ideal copy-only filters used for lower bounds may have expensive
classical descriptions and gate decompositions. The copy lower bound
allows them, which strengthens the reduction. No efficient construction
from a succinct arbitrary global probe is thereby claimed.

## Consequence and remaining target

The specified common-frame reflection bank has an Omega(r^2) source
bill at any fixed useful decoding error even if its final processor is
fully collective. Constant-width known entangled RDS input blocks have
the same rank scaling. More generally a known offline parallel source-
query marginal must have Q chi=Omega(r^2), where
chi=k^Q ||rho_queries||_op, to escape this particular reduction.

This changes the proposed remedy: a joint decoder of the same bank is
not the missing operation. Nontrivial global logical input profiles and
unknown-payload-correlated future queries are real unexcluded resources.
The result is not a general adaptive quadratic bound, not a claim that
such profiles suffice, and not a rejection of the root's three-carrier
active history. A generic subquadratic-rank approximate inverse remains
UNACQUIRED. Improvements in accuracy dependence, gate depth or programme
storage are not ruled out by the rank-only copy bound.

## Actual work

Read the retained primary RDS definitions/proofs and visually inspected
its actual Fig. 2(a), plus the new conjugation primary Corollary 11.
Reconstructed all-k entropy/concentration and the exact state channels
analytically. The new conjugation HTML retrieval took 0.242 seconds and
856,995 bytes, recorded in source_entry/CONJUGATION_RECEIPT.json. Other
sources and reviewed control ports were reused read-only. No source
calls, simulated quantum records, scientific optimizer, numerical query
case or model evolution was run. The result depends on no numerical
diagnostic.
