# Fixed-rate classical record ports from rooted expander animals
30 October 2026. Construction candidate; not independently audited. This is a substantive fixed-rate retention/read mechanism, not a claim that capture and native receiving have already passed review.

## Scope and useful result
A global Hamming-energy estimate charges eta*n noise per n-site record block, which is too costly when the block has only O(1) read ports. That is a weakness of that estimate, not an impossibility result. The FULL-animal proof in `producer-workspace/FULL_ANIMAL_KILLED_BASIN_CANDIDATE.md` localizes to animals containing a designated port. Its sparse source becomes O(1). This supplies a nonlinear, spatially localized port potential. A product of bounded-below port factors can be coupled directly to the native quantum memory Lyapunov observable. In particular, the actual read bit need NOT be immutable or always correct.

This note spells out that transfer and its outstanding capture/global-basin obligations. It does NOT cite classical stochastic trajectories for arbitrary HP noise.

## 1. Actual bounded-body classical hardware
For each record use an odd-degree d regular graph with adjacency second absolute eigenvalue lambda and alpha=lambda/d sufficiently small. Fixed d may be large. The bit at v is a physical two-level system; all nominal classical operations are computational-basis preserving. At rate kappa, v is reset to the majority of its neighbors. An explicit Lindblad implementation is the finite family

 K_(v,a,sqrt-old)=sqrt(kappa) |Maj(a)><old|_v tensor |a><a|_(N(v)),

for all neighbor strings a and old values (equivalently a majority-reset CPTP channel minus identity). All Kraus supports have d+1 sites, and each site belongs to only d+1 update neighborhoods. The number of Kraus labels is a fixed constant. This is an actual bounded-body dissipative primitive, not a free noiseless decoder. Requiring two-body-only primitives instead would create another compiler obligation. Kappa,d are independent of storage time and block size.

The nominal quantum read coupling is diagonal in the classical port Z. It may coherently control a finite native hub operation, or copy the port to a finite native scratch register. A fixed number of readers uses each port. These couplings preserve classical bit values and hence all classical diagonal observables. They do not assume the port is error-free.

The comparison bit b is the ORIGINAL captured/raw bit, used only in the analysis. The classical error support E consists of vertices differing from b. The physical hardware never needs b.

## 2. Majority as monotone disagreement-syndrome recovery
Let sigma(E) be the set of graph edges with unequal endpoint bits. Every active majority update flips one vertex and strictly decreases |sigma|. It changes d edges, with net decrement at least one, so the source animal lemma's move hypothesis holds with k0=d and beta=1/d. Inactive updates have zero effect on diagonal observables.

For a set C of size <=delta n, spectral mixing gives

 |partial C| >= (d-lambda)(1-delta)|C| = h |C|.

Let B(C) be vertices whose neighbors have a majority in C. Since ||A(1_C-|C|1/n)||_2 <=lambda sqrt(|C|),

 |B(C)| <= [alpha/(1/2-delta)]^2 |C| = c |C|.

Choose alpha,delta so c<1/2. At least (1-c)|C| vertices of C are correcting-active. Consequently the number of active hubs associated with this error component is at least

 g_C >= (1-c)|C| >= [(1-c)/d] |sigma(C)|.

Build G0 with the full update read-neighborhood cliques, edge-check supports, and declared nominal local primitives. Use a fixed graph power G so distinct error components have disjoint full component containers J(C). The containers contain error dummy vertices, all disagreement edges affected by relevant hubs, and connected completion edges, exactly as in the source proof. Their size is <=D0|C|. Components separated in this G cannot affect one another's majority decisions. No arbitrary distant NOISE support is made a clique: see section 6.

## 3. Rooted FULL-animal lemma
On the bounded-degree mixed graph H (dummy bit vertices plus edge-check vertices), fix the actual read-port dummy p. For ALL connected animals A containing p, define

 f_A=theta^(u|A|-|A intersection sigma|),
 V_p=sum_(A contains p) f_A,
 W_p=sum_(A contains p) |A| f_A.

The sum is full, not truncated. Choose u,theta by the source proof's beta/h/D0 conditions. In the basin where every error component has size <ell, the same proof yields

 L_majority^* V_p <= -gamma W_p + b.                 (R1)

Here gamma includes kappa and b is independent of n. Specifically:
* Every move completion A -> A union D retains p. Its target animal is in the rooted sum and the 2^k preimage bound only improves after restricting roots.
* Every poor-component completion A -> A union J(C) retains p. The one-component entropy cancellation and distinct-hub charge remain unchanged.
* Sparse rooted animals are counted by A0^m rather than n*A0^m. Thus sum_sparse |A| f_A <=C_sparse, not C_sparse*n.
* W_p>=V_p.

If p is wrong and C is its error component, J(C) is an allowed rooted animal. Therefore

 V_p >= f_(J(C)) >= theta^(-(h-uD0)|C|) >= v0,
 v0=theta^(-(h-uD0)).                              (R2)

The exact constant can be weakened to account for dummy-container conventions; what matters is a positive confinement exponent. A region of wrong bits enclosing the port cannot hide its distant boundary from this nonlinear observable.

The constants in (R1) may be very unfavorable. No practical threshold is asserted. Taking theta small makes the ratio b/v0 small, while the admitted physical noise threshold also becomes smaller.

## 4. Localized broad-noise estimate
For any fixed-body system support Z, possibly with arbitrarily distant legs and a retained shared bath, changing bits on Z changes only <=qd edge labels. The ratio of an affected f_A across its orbit is <=theta^(-qd); an unaffected animal has zero oscillation. Summing the orbit-oscillation bounds using the PER-SITE incident cb budget gives

 noise^* V_p <= C(theta,d,q) eta W_p.                (R3)

This is a Loewner bound by relative-norm/orbit oscillation, not a classical fault-probability claim. An HP perturbation must annihilate identity (or its identity contribution must be separately budgeted); use the same exact trace-annihilation/cb convention as the accepted native noise theorem. A mixed support is charged once for each affected local edge; separation between its legs does not enter. Crucially this drift calculation does not geometrically connect distant legs.

For several record blocks and port factors Z_j=1+K V_j (V_j may sum a fixed number of roots), the analogous product estimate costs

 C eta sum_j [K W_j/Z_j],

not eta times the total classical storage volume. A noise term that also touches quantum DATA is additionally charged to the quantum per-site incident budget. Product orbit ratios are bounded because one term touches only q system sites/blocks. An explicit product-orbit proof is a receiving obligation; it must keep the root sum rather than replace it by a uniform bound over all storage sites.

## 5. Native quantum read coupling, without perfect latches
Take F_Q to be the accepted native quantum comparison observable for the ORIGINAL fixed baseline b (or its source-reference Pauli frame). Consider

 F=F_Q product_j Z_j,   Z_j=1+K V_j.

Only blocks actually read by that quantum code need enter this product; there are O(N), even if the total ATG source has many other raw records. Other blocks receive their own retention estimate.

For each read-dependent native local term, compare the real port-controlled generator to the generator with the analysis bit b hard-coded. On a diagonal test observable this difference vanishes in the correct-port sector and is a bounded local operator in the wrong-port sector. The relative-norm injection has the form

 Delta_read^* F <= J sum_j I_(wrong port j) F.

This requires actual finite native terms/footprints and their weighted relative-norm constants; it is not an appeal to ideal instantaneous correction. Because the controls and classical factors are Z-diagonal, wrong/correct off-diagonal port blocks do not create a square-root loss in this ADJOINT test.

By (R2), in the wrong-port sector,

 K W_j/Z_j >= K v0/(1+K v0).

Choose K=1/v0 and choose the fixed majority rate so gamma/2 dominates J, with room for (R3). Then negative classical drift pays wrong-port injection at every point in the safe basin. The only remaining classical extensive source is at most Kb times the NUMBER OF RECORDS READ, not times their block size. This can be made a sufficiently small constant density. The ordinary native global-energy source and quantum incident-noise source remain as before.

Thus the correct interface is 'a noisy local port with its own rooted negative-drift credit', not 'a perfectly decoded bit delivered every instant'. The comparison native implementation with hard-coded b is an analysis object, not a physical immutable register.

## 6. Global retention and distant noise: obligation and route
One-point port estimates alone do not prevent a block changing its stored phase. Use the unrooted full-animal V_all=sum_p V_p (or an equivalent unrooted sum) and the source killed-basin argument to control emergence of a component of size ell=Theta(n). Its vacuum source is O(n), and the barrier is exp(c n).

For moving/distant q-body perturbations, do NOT add all noise supports as graph cliques. In this classical repetition setting a Pauli term flips at most q vertices. If this creates a component of size ell, it merges at most q*D existing graph components through those added vertices. At least one source component has size >=(ell-q)/(qD), hence supplies an exponentially large unrooted animal. This gives a barrier with a worse constant, without increasing degree. The exact canonical-phase switch must also be excluded: choose the small-component cutoff so strong vertex expansion and disjoint component neighborhoods imply total minority size <n/2-q. Then a bounded-leg transition cannot silently change the reference phase. These constants and the killed-versus-full CP comparison must be audited, not inferred from the local port inequality alone.

After this closure, n=C log(R H/epsilon) gives union control for R records over horizon H; the coherent retained-channel comparison may have polynomial prefactors and a halved exponent. It is not valid to sum eta-sized gentle cuts per raw record. One joint source/support cut is needed.

## 7. Capture: earned deterministic skeleton, NOT completed norm theorem
A simple depth-log n unprotected fanout is rejected. A staged scheduled alternative uses constant-factor growth followed by a fixed number J of parallel majority refresh rounds. If h_(k-1) is the previous error count and z_k the number of bad local locations in the stage, bounded fanout plus spectral majority contraction gives

 h_k <= a h_(k-1)+C z_k,  a<1/2,

provided intermediate errors remain in the small-density basin. Each stage has O(n_k) locations and fixed depth. The deterministic good-span statement remains valid for coherent arbitrary local fault insertions: each retained computational component obeys the same fault-support propagation. 'Every stage has z_k<=epsilon n_k' keeps the record in the original-bit basin. A bad stage needs Omega(n_k) fault insertions, and n_k grows geometrically. A genuine scheduled local-noise norm expansion would then yield a uniform sum of the form sum_k(C eta)^(c n_k), not eta log n.

However two important steps are NOT yet earned here:
1. The actual multirecord mixed-cavity/chronological expansion under signed HP noise, with no exp(eta*total-volume) factor. A classical fault-witness probability cannot replace it.
2. A bad capture stage need not finish near either consensus. It cannot simply be renamed a stable flipped bit. The root has proposed treating the resulting sparse BAD RECORD BLOCKS as permanent bounded-port strong-noise regions, using the already accepted total-strength hot-spot theorem. This is a possible stronger interface, not the original fixed-bad-baseline premise.

Good record blocks also need an INITIAL rooted-moment receiving bound. A globally sparse final error support alone does not imply this. A native warmup can reduce rooted moments using a time-dependent K(t), since W>=V and K'<=gamma K/2; but the quantum memory needs a valid port during that warmup. This physical handoff must be supplied.

## 8. Resources and honest status
Per record: n physical classical sites; O(n) bounded-degree majority terms; constant physical body d+1 and constant fixed rate kappa; O(1) fixed physical read ports. Classical retention is autonomous once the final graph/couplings are installed. Rooted animals are analysis observables, not hardware computations. There is no hidden all-block read operation.

Scheduled capture costs O(n) total new storage and at least O(log n) stages; any extra warmup/transfer must be counted. A graph that rewires a fixed port to log n different layer neighbors violates a fixed physical degree budget and is not granted. A possible nested-prefix expander construction is under examination but not used as a proven resource here.

The paid alternative kappa=Theta(n) and a normalized Hamming potential is unnecessary if the rooted argument passes; it remains a fallback with explicitly growing local rates, not a fixed-rate result.

### Primary context (not imported beyond their actual statements)
Sipser–Spielman, Expander Codes, IEEE TIT 42 (1996), author source https://www.cs.yale.edu/homes/spielman/Research/expanders.html : classical expander decoding machinery. Chilappagari–Vasic, Fault Tolerant Memories Based on Expander Graphs, ITW 2007, https://doi.org/10.1109/ITW.2007.4313061 (institutional abstract https://experts.arizona.edu/en/publications/fault-tolerant-memories-based-on-expander-graphs/) : noisy-component expander memory architecture. Neither reference is being claimed as an arbitrary-HP-noise/native-port theorem. The detailed rooted operator proof above is a transfer of the in-workspace FULL-animal construction and requires its own review.

## 9. Root's logarithmic-moment completion (16:13)
The port credit also controls the factor's logarithm, not only its bad-port indicator. Let L=log(1/theta), choose tau>log A0, and set C_tau=sum_(A contains p) exp(-tau|A|)<infinity. Apply the log-sum/relative-entropy inequality with prior weights 1 and K exp(-tau|A|), compared with weights 1 and K f_A. Because log f_A<=L|A|,

 log Z <= (L+tau) K W_p/Z + log(1+K C_tau).         (R4)

All constants are independent of block size. After reserving enough of the negative W_p credit for actual read faults and HP noise, the remainder therefore supplies -c log Z plus a vacuum constant. Choose theta so v0 is large, then K small while K v0 is large. Both Kb and log(1+K C_tau) can be small. This is the appropriate full joint-log-moment bridge for F_Q product Z_j; a one-point port expectation would not suffice.

## 10. Actual-prefix caution and exact comparison alternative
A wrong port read can be latched and used after the port heals. It is invalid to charge the later DATA payload rate to the CURRENT wrong-port indicator. A shared majority/read ownership mechanism plus false-program tokens is one possible native implementation; its service and dirty credits must be re-earned. The root points to semantic_defect_energy_root and native_locc_continuous_operator assets for bounded tokens created at a wrong read and consumed before DATA action.

There is also a potentially simpler receiving route: compare the entire actual physical native generator term by term to the same gate sequence with b hard-coded. The only differences are the read/prefix terms at the time they sample/control on the wrong bit. Later scratch effects run under the comparison generator and are covered by its already-global all-controller-state Lyapunov inequality, just as after an earlier apparatus fault. This requires the accepted F_Q inequality and relative-norm bounds on the FULL scratch/controller space, not only valid prefix histories. If that premise fails, the token/shared-ownership extension is required. Section 5 is conditional on one of these actual native receiving arguments; it does not skip the delayed-token seam.
