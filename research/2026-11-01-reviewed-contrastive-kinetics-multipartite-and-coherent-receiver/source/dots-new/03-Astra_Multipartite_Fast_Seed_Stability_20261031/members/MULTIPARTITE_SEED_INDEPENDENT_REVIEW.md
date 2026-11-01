# Independent frozen-source review: complete-multipartite fast seed

## Verdict and boundary

**Accepted as an ordinary mathematical proof and independently received exact construction for the stated complete-multipartite family.** No substantive mathematical or code blocker remains. The conclusions are full-orthant irreducibility, positive recurrence and all finite exponential stationary total-count moments for arbitrary strictly positive rates in this family. Executable receiving is restricted to exact positive rational rates and rational t>1.

This is not a proof-assistant formalization, a general one-port/conservative or weak-reversibility theorem, an optimal-constant result, or a historical novelty claim. No web or external retrieval was performed in this continuation. The preceding package's completed source-access failure remains quarantined and is not retroactively cleared or used as a significance premise here. All previously accepted files remain unchanged.

## Exact source binding

Current author manifest `AUTHOR_MANIFEST.json`:
`aa232d64c068a0de1ffb8a5e41af5f5728a241945b4edb5e4c74d02dd82e3e85`.
Its 13 files were verified at exact byte lengths/hashes. Principal current sources:

- `MULTIPARTITE_SEED_THEOREM.md`: `4d96e067d5127034d2d27f99c44b62656cccdc689438f8ba1e13b99ef798e702`.
- `multipartite_seed.py`: `329b43c01ee7a3940b8f76d90db21fd6818bcd4144d74bd88f1d8eb0ab045b0f`.
- `exercise_multipartite.py`: `799e12ea92e09c24907fc2ce80d86a039bc36aba8494b7611a694f56f552e464`.
- `exercise_results.json`: `d094fe1e581d636b69fa5643900e8fadb4ea8b1d2c37d60c5a4f8043dc356b13`.
- `triangle_demo.json`: `34c277fe7552c7e137f1db744133f76090985e1163e900f3cd93a220747e8fe1`.

The historical scope-wording snapshot and correction are bound as provenance only, not a competing current theorem. The final package-relative `independent_audit/AUDIT_MANIFEST.json` binds this receipt, all current/historical author files, independent sources/results, and byte-identical replay outputs; it excludes itself.

## Whole-proof audit

### 1. Raw acquisition and structural scope

The unique count-changing pair identifies A. Normalization combines duplicates and discards validated null channels. Each nonnull internal edge must join a square-free A-free hub to2A or A+X and have its reverse. Every hub must have its own2A pair; every satellite must have at least one arm. This is sufficient for weak reversibility and the later singleton paths, not a supplied communicating-class oracle.

The complement components are acquired directly and then checked as independent parts of the original hub graph, with all cross edges present. No original partition is an input. In particular, deleting an edge from a triangle can yield an admitted K1,2 under a newly acquired partition. The initial overbroad wording about edge deletion was corrected before this frozen review; the mathematical inequalities and code did not change. An actual recognition failure remains UNKNOWN for stability.

The admitted class includes triangles/cliques but excludes free passengers and disconnected hub components. It neither contains nor is contained in the earlier biclique/free-passenger family. Sparse arm incidence is allowed and independently exercised.

### 2. Inventory positivity, max ties and the strict boundary cone

R=N−max(part totals) and P=(1+eta)R−eta A satisfy R<=P<=(1+eta)R. Every internal destination contains A or a cross-part hub, so an internally active positive inventory cannot become zero; at R=0 every internal source is disabled. Core birth/death changes P by exactly plus/minus one.

Globally, an internal jump has |Delta R|<=1 and |Delta P|<=1+2eta<2. Endpoint P-values are at least one, giving |Delta(1/P)|<=6/P². This uses finite differences and remains valid when a maximizing part changes or ties.

In R<N/2 the old dominant part remains a maximizer after every enabled jump. The delicate case A+X_d→hub avoiding d decreases its total by one, but each other part rises by at most one and A>=1 supplies the necessary gap. A reverse cross-hub arm consumes a particle outside d before adding one, so no other part can exceed the decreased dominant total. Destination ties are allowed; the exact boundary table in the independently written mechanism note establishes all channel cases.

### 3. Fast inverse drift, including adverse cross-hub arms

Dominant-part forward captures contribute negative inverse drift at rate at least k_- A M, with per-jump magnitude at least eta/(3P²). A cross-hub amplification contributes at most−3b_h/(8P²). Reverse arms returning to the dominant part contribute at most2eta s_h/P²; eta=b_-/(16s_+) leaves at least b_h/(4P²) negative drift from that same source. Those order-NR adverse terms are not dropped.

Completeness supplies the exact cross-source product sum M(R−A). Every other adverse inverse source is bounded by its constant times R², so its total contribution is at most6S. Combining gives the claimed boundary inverse inequality with gamma. The independent global bound6SN²/P² is used outside that cone. Neither estimate uses a stationary law, mixing time, lineage factorization or fluid limit.

### 4. Interior angular term and actual core death

The raw A-generator identity gives the positive reverse coefficient s_h+b_h and the negative bound F0 A N. Thus the negative epsilon A/(N+1) correction produces the claimed angular inequality.

The core decomposition retains the full h in both lambda(t−1)h and−D A h. This is important near t=1: replacing the angular positive death cost by epsilon mu A before absorption would be too crude. In the actual proof h>=1−epsilon>=1/2 and epsilon F0<=D/4 leave−D A/4.

At R>=2 the inverse death increment costs at most mu; the phase death increment costs at most epsilon mu. At the sole singularity A=R=P=1, the destination is evaluated at h0=4t and its full positive death increment is charged by4mu. No protected last-copy assumption is made. Birth decreases both unweighted correction terms. The safe B=2lambda(t−1)+5mu therefore gives the master estimate exactly. At R=0 the displayed immigration drift is exact and negative.

### 5. Region join, finite exception and all moments

The acquired delta<=1/4 makes the boundary inverse term pay B+6S with unit slack. In the complement, P>=R>delta N bounds the inverse term by6S/delta². Either A is at least delta N/2 and actual death pays linearly, or M>=(N−A)/q and Q>=M(R−A) provide the required quadratic hub rate. The stated kappa and ceiling N_* follow.

On active states h<=2, not merely h<=H=4t; this is exactly why scaled drift<=−1 implies the specified zeta=min(1,lambda)/2. The separate inactive-face drift handles h0. The finite-head coefficient follows directly from the raw rate sum, the linear core rates, N_*² and bounded destination h. No head state is enumerated.

Nonexplosion has the ordinary Poisson-immigration comparison N(t)<=N(0)+Poisson(lambda t), followed by bounded rates on finite count sublevels. The reversible path0→A→2A→hub→A+X→X exists for each satellite and remains enabled after arbitrary nonnegative translation, proving full-orthant irreducibility.

Localized integrating-factor Dynkin, nonexplosion and Fatou give the semigroup W bound. Tight occupation averages then supply an invariant probability; irreducibility yields positive recurrence and uniqueness. Fatou on those averages yields pi(W)<=C_F/zeta without assuming prior invariant-generator domain membership. Since h>=1/2, pi(t^N)<=2C_F/zeta. The formulas exist for every t>1 and positive rate vector, so the all-exponential conclusion is not inferred from finitely many tests.

## Polynomial-bit claim: accepted only for the compact representation

With explicit binary rational inputs, raw rate sums have numerator/denominator bit length bounded polynomially in total input length. All graph/coordinate/incidence scans are polynomial on the explicitly supplied vectors. After these scans the scalar formulas have fixed arithmetic depth: products, sums, divisions by proved positive quantities, minima and one ceiling. Exact rational arithmetic therefore produces polynomial-bit constants in polynomial bit complexity.

The named14 blocks are q,eta,c0,gamma,D,epsilon,B,delta,kappa,Cint,Nstar,zeta,H,and the CF block including moment rescaling. They are not14 machine instructions. Qualitative recognition still computes raw rational summaries; its zero formula-block count only omits the requested-t Foster stage, not all arithmetic. There is no hidden rate-ratio or t−1 loop.

The certificate stores a rational coefficient/base and an integer exponent, plus a symbolic binomial head-size expression. Expanding t^(N_*+1), evaluating t^N on binary-encoded huge states or enumerating the head is not generally polynomial-output work and is not done. Pointwise tests cancel t^N and compute the exact rational scaled generator. No global memory/time or hostile-input admission guarantee is claimed.

## Independent receiving and tests

`independent_audit/independent_multipartite_receiver.py` does not import the constructor. It independently reconstructs raw normalization, port, complement components, every hub/arm/amplification incidence, rate summaries, all scalar/factored quantities and every work field. It uses a separate breadth-first complement traversal, while the constructor uses its own traversal. Generic exact-parser scaffolding was locally reused from the reviewer's earlier receiver, but no earlier theorem or good inventory is a premise. Exercise drivers import the candidate only to obtain receipts for this independent receiver.

Executed independent controls:

- Five separately built raw fixtures: sparse non-CB triangle, sparse K2,1,1, sparse K4, K2,2 and minimal K1,1, including unequal rational rates.
- 1,049 ordinary states and250 targeted states around the cone split, large inventories and huge counts. Exact local/inverse/A/master/Foster tests cover11,443 enabled internal jumps and166 actual destination ties.
- 63 qualitative and108 numerical semantic leaf corruptions rejected, including all charged-work fields;24 coordinate permutations and18 exact-domain controls.
- Eight structural UNKNOWN controls, including free passenger, unit P4, disconnected edges, inconsistent nonadjacency, omitted amplification, uncovered arm, nonreversibility and an active-active channel. Unit-rate excluded graphs are explicitly ordinary detailed-balanced controls, not instability examples.
- An admitted triangle-edge-deletion/repartition case; duplicate splitting and a null row preserve normalized mathematics while correctly changing input-work accounting.
- t=1+10^(-200),3/2,1000 and10^100 all produce exact numerical certificates with zero rate-dependent iterations;16 additional exact huge-threshold state checks pass.
- Fresh interpreter stress: candidate import changes the documented decimal-conversion guard4300→0. At mu=10^(-5000), both receivers accept the122,417-byte receipt with49,947-bit retained scalars and5018-digit exponent cutoff. At one reverse rate10^1500, both accept a125,362-byte receipt with74,827-bit retained scalars and10512-digit cutoff. Eight further exact state checks pass. No Foster power or head is expanded.

Fresh wire tests corroborate implementation behavior, not the asymptotic complexity proof or a service resource cap. The global interpreter setting is explicitly trusted-research behavior.

All five staged replay outputs are byte-identical: author exercise, triangle receipt, independent mechanism controls, independent receiving exercise and fresh-process wire controls. The author totals also reproduce:1916 states,27388 assertions,11264 enabled internal jumps,57 destination ties,739 outside-head Foster checks,171 corruptions,24 permutations and11 domain controls.

A local development mismatch in the independent receiver's family-label string was caught by exact comparison and repaired before its first accepted control run; no main source or mathematical formula was changed. There were no denied operations, external transfers or source retries in this continuation.

## Significance and negative-control scope

The sparse perturbed triangle has an internal complex tree. Complex balance would force detailed balance across each bridge; its unit amplification pairs give bc=bd=cd=a², while the rate2 leaf gives ab=2bc. These conditions are incompatible. The all-unit version is already an ordinary product-Poisson case.

The radial-only t^N(1+1/P) obstruction is valid for every positive rate vector when at least three parts are equally occupied and A=0: every enabled reverse jump strictly decreases P, while eventual geometric immigration drift is positive. This proves only that template fails. The interior angular term pays an order-N negative contribution on that ray.

The independently written free-passenger note gives the exact asymptotic positive drift lambda(t−1) for extending this particular formula to an omitted free passenger. That excluded network is covered by the preceding biclique theorem and has a unit-rate product-form control. Neither obstruction claims instability or exclusion of all ordinary methods. Matching-inventory drop-two examples remain valid and do not contradict this different deficit inventory.

The main t=2 cutoff is600861655025994950. These are conservative proof constants, not practical mixing estimates. The accepted boundary is this raw structural family and compact exact construction, with no historical novelty or fresh literature-clearance claim.
