# Count-certified quantum prediction through an explicit reachable-space quotient

28 October 2026. **New consolidated candidate; not yet independently received.** The previously frozen full-square, injective and full-algebra-surjective sources are unchanged. This theorem collects those special cases into one finite-confidence CP-lifting certificate. It does not assume that abstract quotient complete positivity supplies a lift, and it makes no novelty or practical advantage claim.

## 1. Acquired interface and candidate witness

Assume a finite stationary native action/outcome library, independent repeatable whole-process starts, and an exact supplied upper bound `r` on the minimal observable rank. A finite pool of normalized legal preparations and future tests, including trace and all eventual terminal tests, is covered by simultaneous probability intervals before any selection. A nonsingular `r×r` core then yields the exact preparation-coordinate representation

    C_z=H^(-1)H_z,    c_0=e_1,    trace(c)=m c,  m=1^T.

The empty preparation is first. The true maps satisfy `m sum_o C_(a,o)=m`. All these are inherited assumptions and consequences of the received positive-gauge source, not learned rank bounds or hidden state oracles. Every preparation, native call and future readout is charged.

Use a fixed orthonormal Hermitian basis for a candidate virtual `d×d` matrix algebra, with real coordinate dimension `D=d²` and trace row `tau`. A candidate consists of:

- A full-column-rank `B:R^s -> R^D`, defining the proposed invariant reachable space `W=image(B)`, where `r<=s<=D`.
- A quotient `P:R^s -> R^r` and right inverse `L:R^r -> R^s`, satisfying `PL=I_r` and `tau B=mP`.
- A virtual initial density `sigma_0=X(Bv_0)>=0`, with `Pv_0=e_1`. Therefore `Tr sigma_0=1` exactly.
- A full-space linear extension `Pbar:R^D -> R^r` such that

      Pbar B=P,       m Pbar=tau.                       (1)

No one of `B,P,L,Pbar` is claimed to be a physical CP interface. The learner selects and verifies them, including their numerical conditioning. The initial density is selected in the same virtual representation; it is not an estimate of physical memory.

There is no hidden extension-existence premise in (1). Given any left inverse `K_B B=I_s`, choose `u` with `m u=1` and set

    Pbar=P K_B + u(tau-m P K_B).                        (2)

Then (1) follows because `(tau-mPK_B)B=0`. The norms of this particular extension, or any improved verified one, enter the error bound below.

## 2. Actual fitted full CP instruments

For every native branch `z=(a,o)`, fit full maps `Wtilde_z:R^D -> R^D`, internal maps `Ttilde_z:R^s -> R^s` and predictive maps `Ctilde_z:R^r -> R^r` satisfying **exactly**

    Wtilde_z B=B Ttilde_z,       P Ttilde_z=Ctilde_z P,
    J(Wtilde_z)>=0,
    tau sum_o Wtilde_(a,o)=tau,
    m sum_o Ctilde_(a,o)=m.                             (3)

`J` is the unnormalized input-first Choi transform. In this basis it is Frobenius-isometric. The last identity is implied by the preceding trace/intertwining constraints and surjectivity of P, but checking it separately is useful. Numerical equality tolerances alone are not proofs: affine repairs must be performed and the final objects checked exactly or by certified interval methods.

For fixed structural witness `(B,P,L,Pbar)`, (3), initialization feasibility and convex residual objectives are linear constraints and LMIs. Searching the structural witness, its dimensions or its quotient is not convex and is not supplied for free. No CP map on an abstract quotient is substituted for the **fitted full Choi matrices** in (3).

## 3. Count-derived correction and theorem

Suppose simultaneous intervals give `|H-Hhat|<=D_H`, `|H_z-Hhat_z|<=D_z`. Compute

    U=Hhat^(-1),  A=|U|D_H,  ||A||_infinity<1,
    M=(I-A)^(-1)|U|,
    E_z=M[D_z+D_H|Ctilde_z|+|Hhat Ctilde_z-Hhat_z|].    (4)

The Neumann inverse bound and exact residual identity give `|C_z-Ctilde_z|<=E_z`. All observable fitting/repair residuals are charged in (4). Define

    G=B L,
    F_z=|G|E_z|Pbar|,      kappa_z >= ||F_z||_F.         (5)

Require verified full Choi margins

    J(Wtilde_z)>=mu_z I,       mu_z>=kappa_z.            (6)

**Certificate theorem.** On the count-confidence event, these finite checks certify an exact virtual quantum instrument reproducing the source's entire legal classical law from the supplied start, with full map errors bounded by (5).

**Proof.** The existential exact maps are

    W_z=Wtilde_z+G(C_z-Ctilde_z)Pbar,
    T_z=Ttilde_z+L(C_z-Ctilde_z)P.                      (7)

They are proof objects, not supplied source maps. From `Pbar B=P` and `PL=I`,

    W_z B=B T_z,       P T_z=C_z P.                    (8)

Thus W is invariant and its quotient dynamics are exactly the acquired dynamics. Because `tau G=m`, both trace identities give

    tau sum_o(W_(a,o)-Wtilde_(a,o))
       =m sum_o(C_(a,o)-Ctilde_(a,o))Pbar=0.            (9)

Full-space TP is preserved. The Choi error is bounded in both operator-order directions by `kappa_z I`; (6) proves CP on the entire matrix algebra. Finally,

    tau W_(z_H)...W_(z_1)Bv_0
       =m C_(z_H)...C_(z_1)e_1.                       (10)

The right side is the actual word probability. Positive virtual states and instrument normalization extend the identity to all classical feedback policies. No invariant section `L` is needed, and no quotient identity outside W is assumed. QED.

The known-zero/zero-radius limiting case is harmless. Finite uncertainty normally needs strict Choi interior. A chosen full-map repair in an unobservable direction is not an error relative to an identified physical plant: the exact virtual extension is existential. What must be charged is its changed observable residual and verified final Choi/structural constraints. This distinction does not permit claims about physical memory.

## 4. Contractive native error

The joint outcome-memory channel of each action has half-diamond distance at most

    t=min(1, (d/2) max_a sum_o kappa_(a,o)).             (11)

One direct proof uses the CP majorants with Choi matrices `kappa_z I +/- J(Delta_z)`, giving `||Delta_z||_diamond<=d kappa_z`, then sums branches. This is a norm estimate on the virtual model, not experimental certification of a physical ancilla interface.

The direct-sum positive state indexed by the **complete observed history** obeys the hybrid bound

    (1/2)||Omega_H-Omega_tilde_H||_1<=min(1,Ht),
    TV(full native transcript)<=this cq-state bound.            (12)

The argument is blockwise CPTP contractivity, uniform over controllers selected after the data. It never divides by a history probability.

When all relevant margins are positive, put `epsilon=max_z kappa_z/mu_z<=1`. Each exact full instrument has the state-independent CP-mixture decomposition

    W_z=(1-epsilon)Wtilde_z+epsilon R_z,

where residual branches are CP and their sum is TP. Omega includes the retained virtual memory as well as the complete classical record. Hence (12) can also use `1-(1-epsilon)^H`. An independent abort coin delta before each native attempt, with gamma=1-delta, yields

    b_native <= min(1, gamma t/delta,
                         gamma epsilon/(delta+gamma epsilon)). (13)

For M adaptive invocations retaining virtual memory, the bounds are `min(1,M gamma t/delta,1-(1-b_mix)^M)`. The geometric term requires the CP-mixture coefficient; it cannot be inferred from the additive half-diamond bound alone.

These statements certify only the actual source's declared classical word law. They do not identify physical memory, certify arbitrary physical coherent control, or compare its state with an external coherent reference.

## 5. A final readout needs no positive exact off-reachable lift

For a **truly final** action a, acquire each outcome row `g_(a,b)` on the core preparations. Such a row needs no operation after the terminal readout. The rank promise must include these tests: a newly introduced terminal observable can distinguish previously invisible modes.

Fit a valid full virtual POVM `Btilde_(a,b)` and predictive rows `gtilde_(a,b)` such that their effect-coordinate rows satisfy

    btilde_(a,b) B=gtilde_(a,b) P,
    Btilde_(a,b)>=0,      sum_b Btilde_(a,b)=I.

Consequently `sum_b gtilde_(a,b)=m`; check this exactly. From count row bounds and the fitted residual define

    f_(a,b)=D_g(a,b)+|gtilde_(a,b)-ghat_(a,b)|,
    beta_(a,b)>=||f_(a,b)|Pbar|||_2.                   (14)

For the orthonormal basis the exact linear effect row

    b_(a,b)=btilde_(a,b)+(g_(a,b)-gtilde_(a,b))Pbar

differs in operator norm by at most beta and restricts to the correct `g_(a,b)P` on W. **This exact full effect need not be PSD outside the reachable states.** Its actual probabilities on the positive reachable history states are the source's probabilities by (10) and the terminal quotient identity.

To see why positivity outside W is unnecessary, insert the fitted POVM applied to the exact virtual native history state as an intermediate law. The first comparison costs at most `one-half sum_b beta_(a,b)` by positivity and total trace of the exact history states. The second comparison contracts the native cq-state error because the **fitted** measurement is CPTP. Thus

    TV(full transcript including its final readout)
       <= min(1,b_native+t_final),
    t_final=(1/2) max_a sum_b beta_(a,b).               (15)

For finite H, replace b_native by the corresponding native hybrid/common-mixture bound. This avoids an artificial strict-positivity floor for a nearly perfect terminal test. If desired, subtracting beta from the fitted effects can additionally certify a true full virtual POVM, but it is not needed for (15).

**Terminal-only restriction:** after this readout, all relevant memory is discarded and no later source interaction is claimed. The shortcut must not be used for repeated memory-retaining macro readouts or sequential quantum payloads; their post-measurement instruments require native CP certificates. Nor does it give a physical reference guarantee. The received terminal-test recovery lemma can use eta from (15), under its independent-future-datum chronology, to derive additive Bell-risk regret `((d+1)/d)(2eta+planner_slack)` for its finite policy class.

An exact diagnostic illustrates the distinction. Under Bloch shrinkage alpha=4/5, a physical sharp-Z terminal effect has virtual lift `(I+Z/alpha)/2`, whose minimum eigenvalue is `-1/8`. Reachable virtual Bloch vectors have length at most alpha, so all actual terminal probabilities remain valid. The fitted sharp-Z POVM is PSD and each operator error is `1/8`; (15) applies even though robust exact-effect PSD certification fails. This is a gauge/example check, not new acquisition.

## 6. Witness existence, finite search and its actual cost

Any fixed finite-dimensional physical CP realization with **strictly positive Choi matrices for every declared native branch except structurally known zeros with zero-width uncertainty**, under the acquired-core premises above, supplies an interior witness of this form: take W to be its reachable Hermitian span, quotient by the states annihilated by all declared future tests, use the observed preparation basis, and fit its full maps. This is an existence statement, not access to the unknown realization. It covers proper reachable-space quotients without asserting that an arbitrary abstract quotient map has a CP lift.

A useful normal form makes the search obligation explicit. Choose a full invertible coordinate matrix R whose columns consist of: a section of the r observable preparation coordinates, a basis for the unobservable reachable kernel, and a complement of W. The latter two sets can be chosen traceless, so

    tau R=(m,0,0),       sigma_0=R e_1.

In these coordinates every native full map has block form

    [[C_z, 0, A_z],
     [D_z, E_z, B_z],
     [  0,   0, F_z]].                                (16)

Full TP adds the linear identities `m sum C_z=m` and `m sum A_z=0`. Choi positivity is still checked in the physical virtual basis after conjugation by R. The matrix form does not pretend that a section is invariant: D_z can be nonzero. Nor does it make the full-algebra quotient claim: A_z can be nonzero.

A sound practical procedure tests a **declared finite** list of dimensions/witnesses and solves/verifies the fixed-witness fit. Exhaustion without acceptance means UNKNOWN. Conventional HQMM fitting may propose candidates, but a generic numerical fitted model need not have the required exact rank/kernel structure; those equations must be enforced or repaired and recertified.

There is also a deliberately inefficient eventual procedure in this all-declared-uncertain-native-interior class: enumerate bounded-height coordinates R and free blocks in (16), enforcing its affine trace identities, while acquiring successively narrower simultaneous count intervals. At any fixed nondegenerate interior witness, sufficiently close candidates retain invertibility and native Choi margins, and sufficiently accurate Ctilde/count bounds pass (4)-(6). Initial-state positivity must not be silently lost in rounding. If the exact initial state is singular, a sufficiently small invertible trace-preserving depolarizing similarity makes it full rank while preserving strict native Choi positivity and every word probability; this is a virtual coordinate construction, not physical preprocessing. Exact-algebraic Hermitian coordinates, or a fixed rational basis with its explicitly charged Choi-conversion norm, permit finite arithmetic witnesses. For continued sampling, use a summable allocation of failure probabilities across stages; a fixed-N confidence event is not automatically time-uniform. Exact known nonzero boundary branches can be accommodated by the sound finite certificate only when their structural constraints are genuinely verified; the depolarizing-similarity/rational-enumeration argument does not automatically preserve such extra boundary constraints. An unknown identically zero branch is a boundary case, not an interior branch merely because it was omitted from a list of nonzero maps: finite nonzero confidence width does not certify its exact zero Choi matrix by this scalar-ball test. Strict Choi interior alone also does not discover the stipulated nonsingular legal preparation/test core.

This is not a uniform runtime bound. No dimension upper bound, Choi floor, inverse-core singular-value bound, or structural-search resolution is obtained from rank alone. The declared finite search used by the earlier qubit fixture is the only executed count acquisition here. No new count experiment is claimed by (16).

For a fixed candidate an explicit conditioning bill is

    kappa_z <= || |BL| ||_2 || |Pbar| ||_2 ||E_z||_F,
    ||E_z||_F <= ||M||_2[||D_z||_F
              +||D_H||_2 ||Ctilde_z||_F+||R_z||_F],
    R_z=Hhat Ctilde_z-Hhat_z.

At uniform radius eta and bounded residual slope these are `K_z eta`, with the displayed inverse, section, extension, basis and fit norms inside K_z. Hoeffding costs `N>=log(2K_prob/beta)/(2 eta²)` episodes per fixed setting. Positivity requires `K_z eta<=mu_z`; target clock accuracy additionally requires the d-weighted sum in (11) to be small relative to delta/gamma. Terminal rows pay (14). Total resets and native calls sum the actual per-setting budgets and lengths. Dimension `d`, subspace dimension s, all candidate tests, SDP/verification arithmetic, bit precision and subsequent potentially exponential policy planning remain separate costs.

## 7. Attempts to break the construction

**Non-splitting and unreachable directions.** The exact checker `reachable_quotient_cp_exact_check.py/.json` uses the qubit Pauli basis and

    W(I)=I,  W(X)=aX,  W(Y)=aY+cZ,  W(Z)=aZ+bX,
    a=1/4, b=c=1/8.

The reachable space from `(I+Z/2)/2` is span{I,X,Z}; Z-test-and-reset branches give observable rank two. The full Choi matrix has lower bound I/4. There is no invariant section of its quotient, because the Z eigenvector has an unavoidable bX defect. There is also no quotient extension agreeing on W and intertwining on the whole algebra: an outside Y creates the unavoidable cZ term. Thus neither earlier special-case interface applies to this **same full map**. The present candidate does. The checker verifies a nonzero trace-zero observable perturbation, exact corrected invariant/quotient/TP identities, and exact Choi positivity. Its Frobenius correction radius is below 0.000180. The arbitrary perturbation tests the correction identities, not consistency with a separately sampled core table. These are zero-sample algebraic checks, not a separation of stochastic process classes: another realization may exist.

**Initial/rank/core defects.** Omitting initial positivity, using a rank estimate instead of the architectural upper promise, or allowing terminal effects outside the observed quotient breaks the word-law proof. The theorem explicitly checks or assumes each. Full-space trace compatibility in (1), not trace only on a few test states, is what protects the repaired maps in (9).

**Uncharged approximate invariance.** Small numeric residuals in (3) cannot simply be ignored; a tiny hidden leakage can accumulate at long horizons. The certificate requires actual structural equalities for its final fitted model. Full-space CP of the fitted maps alone does not correct this.

**CP boundary is a genuine obstruction.** Choi interior is not just a technical convenience. If an action's branch-summed Choi floor is mu>0, its channel decomposes into weight d*mu of complete depolarization plus a residual CPTP channel. All nontrivial observable eigenvalues therefore have modulus at most `1-d*mu`. An observable exact undamped rotation cannot have such a witness in any finite dimension. Exact trusted boundary maps can be treated separately only with genuine structural information; the present uncertain-interior argument does not learn them for free.

**Physical-reference and terminal-reuse overclaims.** The full abstract CP extension is not a recovered physical environment. The terminal shortcut proves an output law once, not post-measurement memory. Both tempting extrapolations are excluded.

## 8. Conventional comparison and unresolved work

This is an explicit robust witness in the CP-realization programme of Monras–Winter, TQC 2014, Sections 3–6: reachable subspaces, unobservable quotients, semidefinite-representable lifting cones and the distinction between quotient CP and a full CP lift are already central there. The present statement requires an actual fitted full lift and charges its count uncertainty; it does not solve their general lifting problem merely by changing terminology. [Primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol027-tqc2014/LIPIcs.TQC.2014.99/LIPIcs.TQC.2014.99.pdf).

Srinivasan–Gordon–Boots (AISTATS 2018) and Adhikary–Srinivasan–Gordon–Boots (AISTATS 2020) already learn Kraus/Choi HQMM representations without microscopic environmental reconstruction. Those are legitimate candidate generators and comparators. The same count-confidence and controller-risk certificate can wrap a conventional learner that supplies the verified witness; no algorithmic/statistical separation or historical novelty is established. [2018 primary paper](https://proceedings.mlr.press/v84/srinivasan18a/srinivasan18a.pdf), [2020 primary paper](https://proceedings.mlr.press/v108/adhikary20a/adhikary20a.pdf).

The material advance over the earlier bounded certificate is the explicit correction through a **proper reachable-space quotient**, together with the final-readout relaxation. What remains is finding an affordable well-conditioned witness, handling genuine CP boundaries or absent resets, and connecting an acquired declared library to useful terminal circuits and paid planning. The previous aggregate fixture's 9.6-billion-reset cost is unchanged and is not repaired by this algebraic generalization.
