# Conditional long-time arbitrary-CPTP-kick memory theorem via one backward spacetime chain

2026-10-29. **Status: a constructive conditional extension, pending independent verification of the deterministic asynchronous dichotomy stated below.** This avoids quantum residual-law induction entirely. It does not cover continuously acting coherent Hamiltonian noise, nor automatically certify the transactional controller compiler.

## 1. Noise, readout, and deterministic contract

Use the ideal atomic asynchronous SSF instruments, independent rate-lambda hub clocks, and exogenous independent local Poisson primitive kick records. Each primitive kick is an arbitrary CPTP map on at most s data qubits and a retained common bath; its channel may be unknown and retain earlier bath/controller information. The maximum primitive rate is ε, and at most z primitive supports touch each data site. The graph G includes full read footprints, check supports, and primitive support cliques, with bounded degree. A bath-only evolution may be retained between events.

Initialize an exact encoded logical input tensor a fixed bath state. A logical reference is unrestricted. No intermediate global recovery or bath reset is performed. The only global minimum-syndrome recovery is a mathematical final decoding channel.

Run the deterministic argument separately in each CSS sector, using fixed sectorwise minimum-weight syndrome representatives R_X and R_Z and final recovery R_X R_Z. A globally minimum full-Pauli-support representative need not be reduced separately in each sector and is NOT used for D1. Constants below are common worst-case constants for the two sector arguments.

Use blocks of R windows of duration T, total τ=RT. Let ℓ be an integer below both the deterministic small-component confinement cutoff and code distance; for the proposed expander family ℓ=c_cut sqrt(N) up to rounding. The error labels below are branchwise mathematical representatives, not hidden classical physical states.

We require the following *deterministic* consequences of ASYNCHRONOUS_WINDOW_WITNESS.md, to be separately audited.

**D0: unconditional finite work.** For any serial Pauli history in one CSS sector in a block, with incoming sector representative E and outgoing sector minimum-syndrome representative R, let U contain incoming error support and all event supports. Every connected component K of U union supp(R) satisfies

    |K| <= C_seed [|E intersect K|+Q_block(K)].          (D0)

Here Q is the sum of actual Pauli bad-event support sizes, multiplicities included, and C_seed=2(1+wΔ) is allowed. If every K has size <ℓ, R is stabilizer-equivalent to the actual outgoing error.

**D1: backward dichotomy on a good block.** Assume all these K have size <ℓ. The incoming error is the chosen sector representative; the outgoing representative is defined by mathematical endpoint reduction of the actual outgoing error. The physical serial trajectory need not end reduced, and no correction is inserted at its boundary. For every nonempty target S in the outgoing representative there is one of:

(F) a set W containing S, each of its G-components meeting S, and a window label j in {0,...,R-1}, such that

    |W| <= C_bad [Q_block(W)+M_j^*(W)];                 (F)

(A) a set W containing S, each component meeting S, such that

    |W| >= c_R |S|,
    |W| <= C_seed [|E intersect W|+Q_block(W)].          (A)

Here c_R=(h/Δ)theta^(-R) grows with R, and M_j^*(W) counts all hubs whose read footprint meets W and have no ring in window j. The actual deterministic missed-candidate term must be bounded by this majorant. Counting Q over the whole block rather than its suffix only enlarges the right side of (F).

These are precisely the containment, component-rooting, seed-density and ancestor-expansion properties used below. Merely a marginal local-stochastic output bound is NOT sufficient.

## 2. First bad block and virtual representatives

Fix one finite primitive/reset schedule, one Pauli-expanded Kraus branch, and one CSS sector. At each block boundary, as long as all enlarged components are smaller than ℓ, replace the accumulated Pauli error by the fixed minimum-syndrome representative. This changes it only by a stabilizer and a scalar phase. Subsequent Pauli insertions and syndrome-controlled corrections therefore follow the same syndrome record and have the same logical action. This is a mathematical relabeling of that branch, NOT a physical recovery at the boundary.

If the final branch has nontrivial logical error in this sector after the fixed terminal recovery, it must have a first block B with an enlarged connected component K of size at least ℓ. Otherwise the repeated stabilizer-equivalent relabeling gives correct logical readout. All preceding blocks of this branch satisfy D1.

Start with W_B=K, m_B=|K|>=ℓ. D0 applies even though this component is not small. If

    Q_block(K)>=|K|/(2C_seed),

stop: this is already a fresh-density certificate. Otherwise set

    S_{B-1}=E_{B-1} intersect K.

Then |S_{B-1}|>=m_B/(2C_seed), and this target is in the actual reduced representative at the preceding boundary.

## 3. A single backward chain, not an error-branching tree

At block b<B apply D1 to S_b.

* If (F) holds, stop with the fresh set W_b.
* If (A) holds and Q_block(W_b)>=|W_b|/(2C_seed), stop with that fresh set.
* Otherwise set S_{b-1}=E_{b-1} intersect W_b and continue. Then

    |S_{b-1}|>=|W_b|/(2C_seed).

For every nonterminal ancestral step,

    |W_b|>=c_R |S_b|.

Choose the constant R so that

    γ:=c_R/(2C_seed)>1.                                (6)

Consecutive ancestral slices then grow geometrically backward:

    |W_b|>=γ |W_{b+1}|.

The initial representative is empty, so this chain cannot continue through the initial boundary with a nonempty target. It must terminate in a fresh-density alternative. No sum over separate independently chosen residual distributions is taken, and no union of all branch residual supports is used.

## 4. Terminal fresh density controls the entire spacetime volume

Let b_* be the terminal block and M=|W_{b_*}|. If this is not the initial root, W_{b_*} contains its target S_{b_*}, while that target has size at least |W_{b_*+1}|/(2C_seed). Thus

    |W_{b_*+1}|<=2C_seed M.

The geometric expansion of all subsequent backward-ancestral slices gives

    V:=sum_{b=b_*}^B |W_b|
       <= K_vol M,
    K_vol=1+2C_seed/(1-1/γ).                            (7)

If the root itself is terminal, V=M and the same bound holds. Also V>=|K|>=ℓ.

Each component of an earlier W_b meets S_b, and S_b is contained in the later W_{b+1}. Add a vertical edge between the same data site in consecutive block layers. Therefore

    A={(v,b):v in W_b, b_*<=b<=B}

is a connected set in the bounded-degree spacetime graph G times the block-time line: the root K is connected, and every earlier component attaches vertically to the already connected later union. The target subsets need not be recorded in the final certificate. Their existence proves connectedness and (7).

This is the essential entropy estimate. A single terminal fresh event controls a connected spacetime animal whose entire volume is at most a constant multiple of the terminal layer. There is no arbitrary-volume expansion or Pauli-label multiplicity in the counting.

## 5. Positive fixed-certificate tail

For a fixed terminal set W of M sites and block b, let N_f(W,b) count dominating primitive kick events whose declared support touches W. Then

    Q_block(W)<=s N_f(W,b),
    E[t^(s N_f)]<=exp[u M(t^s-1)],  u=ε z τ.

Let h0 M bound the number of hubs with read footprint touching W. The independent ideal clock law gives

    E[t^(M_j^*)]<=(1+q(t-1))^(h0 M),   q=exp(-lambda T).

Primitive fault clocks and ideal hub clocks are independent. Both quantities are actual positive record variables. Let

    a0=min{1/(2C_seed),1/C_bad},
    p=max{u,q},
    r0=exp[(1+h0)sqrt(p)] p^(a0/(2s)).

Choosing t=p^(-1/(2s)) in exponential Markov gives, for each fixed j,

    P[s N_f(W,b)+M_j^*(W)>=a0 M]<=r0^M.                (8)

Both kinds of terminal event imply this one. A Q-only terminal event may be assigned any fixed window label. There are at most R possible labels to union-bound. No conditioning on a data-dependent or rare syndrome record is used.

## 6. Spacetime counting and long-time bound

Let A_st be a fixed connected-animal counting constant for G times the time line. At a fixed endpoint block B the number of size-V connected spacetime animals containing a chosen root site in layer B is at most A_st^V. Sum over N possible root sites. Overcounting animals which extend outside the permitted time interval is harmless.

For a certificate animal, its terminal block and terminal slice are determined by its earliest nonempty layer. By (7), its terminal event has probability at most r0^(V/K_vol). Therefore, with

    r=A_st r0^(1/K_vol),

one obtains

    P[there exists ANY Pauli branch first cutoff-bad in this sector in block B]
      <= R N sum_{V>=ℓ} r^V
      <= R N r^ℓ/(1-r),                               (9)

provided r<1. In writing the union, keep only animals obeying (7); all others need not be counted. The simple total animal count still upper-bounds their number.

There is no 4^(all faults) factor: every branch supplies some fixed geometric certificate, and its terminal event depends only on physical primitive counts and physical no-ring clock cells. The same certificate event may cover arbitrarily many coherent branches.

For L observed complete blocks, union over the possible first bad block gives

    P[Bad_record,sector]<=min{1, L R N r^ℓ/(1-r)}.
    P[Bad_record,either sector]<=min{1, 2 L R N r^ℓ/(1-r)}.              (10)

Choose R first so (6) holds, then T sufficiently large and ε sufficiently small that r<1. All choices are independent of N. This yields exponential-in-sqrt(N) lifetime up to polynomial factors when ℓ is proportional to sqrt(N).

## 7. Quantum conclusion and exact scope

On the complement of Bad_record, every compatible Pauli-expanded Kraus branch is restored by the SAME final minimum-syndrome recovery. The correctable-span lemma therefore restores arbitrary coherent superpositions of these branches, including same-syndrome interference and the retained bath. Primitive and ideal hub schedules are exogenous, so Bad_record has a probability independent of the encoded logical input. Averaging the CP record instruments yields

    ||E_dec,Lτ-id_L||_diamond
       <=2 min{1, 2 L R N r^ℓ/(1-r)}.                    (11)

This is a conditional long-time extension of the ideal comparator to arbitrary local CPTP kicks on independent Poisson locations. It does not assume an invariant quantum local-stochastic residual distribution. It does not insert full syndrome dephasing, twirling, ideal global recovery between blocks, or bath resets.

Continuous coherent Hamiltonian perturbations remain outside this positive-record argument: their Dyson insertion labels are not physical Poisson outcomes, and the terminal-event union bound is not a norm union bound. General signed HP noise is likewise not covered by (11). The independent-switching inclusive norm and occupied-cluster sieve remain separate tools for that unresolved problem.

For the actual transactional controller, one must separately supply: coefficientwise correct branch semantics; bounded primitive/emission mass accounting; and a *joint positive fixed-certificate* replacement for (8), including physical no-service and marked-emission records. Marginal liveness or independent Pauli-branch tails do not suffice. The ideal Poisson no-ring calculation must not be silently applied to the controller.

## Verification checklist

1. D0 includes the incoming error support in U and is unconditional.
2. D1's W contains the target, and every W component meets it, in BOTH alternatives.
3. D1 ancestral enlargement obeys the incoming-representative seed bound, not merely a virtual-initial error bound.
4. The first-bad-block representative substitution is a stabilizer equivalence, not a real reset.
5. Terminal W need not be geometrically larger than its successor; the factor 2C_seed in (7) accounts for this.
6. Only consecutive *ancestral* slices have the γ expansion; the terminal slice uses containment instead.
7. Clock majorants and primitive counts are bounded jointly for each fixed W, block, and window before any conditioning.

8. The deterministic proof is sectorwise; the two sectors are union-bounded only at the final positive-record step.

Items 1–3 are the crucial interface to the independent deterministic audit. The remainder is the proposed new spacetime certificate argument.

### Deterministic readout times between block boundaries

For the IDEAL atomic model, the same argument applies at any deterministic observation time t: use the completed full blocks and a final partial block. A first bad root component in the partial block needs only D0; all earlier blocks still use D1. Its Q-only terminal count is dominated by the full-duration τ count. Thus L may be replaced by ceil(t/τ), with t=0 handled separately. No evolution past the requested observation time is inserted. This observation does not itself compile physical unfinished-transaction readout.
