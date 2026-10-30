# Persistent noisy baseline in the local GPT controller
2026-10-30. New deterministic proof candidate and operational boundary; not an already-reviewed native initialization theorem.

## Main result

A fixed sparse error in a SHARED syndrome baseline need not be a valid global syndrome. It can be treated as sparse quenched defects of the GPT potential. The existing finite local table, after XORing the baseline into its input, still admits unconditional finite work and a physical-window contraction with an additive static-defect term. The native backward witness can terminate at a dense initial-defect certificate. This is a substantive possible preparation-latency escape, not an invocation of scheduled single-shot decoding.

However, every reader of a potential view must use the SAME fixed baseline value. The proof does not supply a noise-resistant baseline register or the protocol for switching/reconciling the final Pauli frame. Those are load-bearing physical interfaces.

## 1. Exact local feasibility: local full rank versus global consistency

The explicit GPT circuit chooses, for each potential view v, a BASIS H_v of its local check space, with kernel C_local. Hence H_v has full row rank as a map from the w=Delta² data bits in Q(v). Every local vector z_v has a preimage, and

    t_v(z_v)=min{|r|: H_v r=z_v}

is defined on the ENTIRE local syndrome alphabet. Local metacheck violations are absent after choosing this basis. The concatenation of the bases at different views may still be globally inconsistent, because different views overlap or duplicate stabilizers. The source table handles such concatenations by outputting no correction.

Let s0 be the true syndrome of an unknown but fixed initial code coset. Write the actual later error relative to that coset as e. The fixed recorded baseline is

    m0_v = (s0)_v XOR eta_v.

Then the difference presented to the table is

    y_v = H_v e XOR eta_v.

Set B={v:eta_v !=0}, and let D be the union of the complete Q(v) over v in B. B is a set of defective POTENTIAL VIEWS; D is their bounded-size DATA footprint. Both are fixed in time in this analysis. Define the global biased potential

    U_eta(e)=sum_v t_v(H_v e+eta_v).

It is an integer, nonnegative, and stabilizer invariant. No globally valid syndrome with value eta is required.

## 2. Three elementary identities

For every e,f,

    |U_eta(e+f)-U_eta(e)| <= 2|f|,                   (A)
    |U_eta(e)-U(e)| <= w |B|,                       (B)
    U_eta(e) <= 2|e|+w|B|.                         (C)

For (A), a minimum representative of z_v plus f restricted to Q(v) is a candidate for z_v+H_v f; interchange the two syndromes for the reverse inequality. Each data bit belongs to two potential views. For (B), unchanged views cancel and each t_v lies between zero and w. Equation (C) follows from (B) and the ordinary U(e)<=2|e|.

A strictly U_eta-decreasing view-supported correction has support at most w and decreases U_eta by at least one. The existing lookup table has exactly this property even with its globally-incompatible-input default: on a compatible input it executes a strict decrease, and on an incompatible input it executes nothing. Alternatively one may fill all concatenated-input entries by minimizing this same well-defined U_eta change. The latter is optional, not necessary for the argument.

## 3. Active density away from defective views

Let b be a fixed upper bound on the number of hubs h whose affected-energy-view set V_h contains a fixed view v. Every hub outside this bounded neighborhood of B sees the exact uncorrupted local tuple H_v e, and its lookup/acceptance behavior equals the ordinary GPT behavior.

For any error to which the ordinary small-error active-density theorem applies,

    g_eta(e) >= g_0(e)-b|B|
             >= kappa U(e)-b|B|
             >= kappa U_eta(e)-(kappa w+b)|B|.       (AD-eta)

Here g_eta counts ACTUALLY active hubs, including the incompatible-input no-op rule. This is not a claim of density inside the defective neighborhood. All localizations below include D in their support sets, so the same inequality applies componentwise with B restricted to that component. Reducedness and the original GPT correction radius are unchanged.

For a reduced error supported in a small component,

    U_eta(e) >= h|e|-w|B|.                          (CONF-eta)

In particular, a zero-noise terminal configuration cannot have arbitrarily large reduced error compared with its baseline defects while remaining in the safe small-component regime.

## 4. No-noise finite-work sanity check

Start with a residual e0 and hold eta fixed; assume no further physical faults. Every accepted move lowers U_eta. Therefore there are at most

    U_eta(e0) <= 2|e0|+w|B|

accepted moves, with total correction-support mass at most w times that expression. If this entire footprint remains within the ordinary correction radius, a terminal configuration with no accepted move satisfies

    U(e_final) <= b|B|/kappa,
    |e_final|_reduced <= b|B|/(kappa h).

The first inequality uses g_eta=0 in the stronger first two terms of (AD-eta). This establishes a deterministic O(|eta|) residual for a small defect seed, rather than assuming that an invalid syndrome can be globally decoded. The conservative finite-work footprint supplies one sufficient condition for remaining within the radius.

## 5. D0 with a static-defect charge

In each physical block include D, the incoming error support, and every actual event support in the execution graph. Include Q(v), full read footprints, and all fault supports as cliques. A move that can improve U_eta must touch the incoming/current error or the defective-view footprint; a region with neither has zero biased potential throughout its affected views.

On a localized execution component, let Q be the bad Pauli support mass, with multiplicities, and b_K the number of defective views whose Q(v) lies in that component. By (A) and (C), the accepted-move count is at most

    2|E_in intersect K|+w b_K+2Q(K).

The execution support has size at most

    (1+2w)(|E_in intersect K|+Q(K))+(w+w²)b_K.

Append the usual sectorwise minimum physical-weight syndrome representative only as a mathematical gauge. Componentwise same-syndrome replacement doubles this bound at most. One safe constant is

    C_seed,eta=2(1+3w+w²),
    |K| <= C_seed,eta [|E_in intersect K|+Q(K)+b_K].  (D0-eta)

There is no service assumption in D0. A large component caused by baseline defects alone is already a dense initial-defect witness.

## 6. Candidate persistence and physical-window contraction

Pack true active hubs whose complete affected-view neighborhoods avoid B. Their number is at least

    kappa_p U_eta,start - C_eta b_W

after changing fixed packing constants. Their full RAW difference-syndrome dependencies remain unchanged until an actual move/fault changes them, because the baseline is fixed and shared. Any such correctly evaluated candidate executes a strict decrease unless a dependency has already changed. A biased move can resolve a packed candidate, but it still consumes at least one unit of U_eta; this is sufficient for the counting argument.

Thus, with the same C_res=dw+1 and changed fixed constants,

    kappa_p U_eta,start <= C_res D_U+dQ+M+C_eta b_W,
    U_eta,end <= U_eta,start-D_U+2Q,

and therefore

    U_eta,end <= (1-a)U_eta,start+A Q+B_M M+C_B b_W. (WIN-eta)

Here M is the actual-good-service miss majorant already used by the native compiler. No new ideal syndrome measurement or perfect scheduler is inserted. The baseline's immutability is what permits candidate persistence.

## 7. Rooted D1: the endpoint-defect alternative must be added

For a target S in the final reduced representative, use the source nested future-support sets with D added at every time:

    U_i = supp(E_i) union D union union_(events k>=i) supp(F_k).

Take only their components meeting S. This preserves nesting, exact localization and component rooting. Let x_i be U_eta on this restricted trajectory, and b_i the number of defective views in its selected components. The source suffix-footprint proof becomes, with fixed C0,C1,C2,

    |W_i| <= C0 x_i+C1 Q_suffix(W_i)+C2 b_i.        (SUF-eta)

For example C0=max(w,1/h), C1=2C0+1 and C2=w(1+1/h) suffice: use CONF-eta to bound final error weight, add the explicit D footprint, and use the accepted-decrease budget.

There is a small but important endpoint case. At the final slice W_R=supp(E_final) union D in the selected components, put e_R=|E_final intersect W_R| and b_R=|B restricted W_R|.

- If w b_R >= h e_R/2, then

      |W_R| <= e_R+w b_R <= (2w/h+w)b_R.

  This is a fresh STATIC-defect-density certificate, with every component rooted at S.

- Otherwise CONF-eta gives x_R >= h e_R/2 >= h|S|/2.

In the latter case apply WIN-eta over R windows. If some x_i is at most a large fixed multiple of Q_suffix+M_i+b_i, SUF-eta supplies the fresh alternative. Otherwise the x_i contract by a fixed theta<1. Since x_0<=4|W_0| (each data site belongs to two energy views),

    |W_0| >= (h/8) theta^(-R) |S|.

Enlarge to original execution components meeting S and use D0-eta. This is the source ancestral alternative with fixed changed constants and an extra static-defect charge. Choose R so that the resulting c_R/(2C_seed,eta)>1.

At any root/ancestral step, if Q+b_W is not dense, D0-eta gives an incoming-representative target of fixed density. Otherwise stop at a fresh Q/static-defect certificate. This is still one backward chain, not a branching tree and not an assumed residual-noise distribution.

## 8. Why a static random baseline is payable for long times

If the baseline corruption bits are local-stochastic at sufficiently small fixed rate, a bad view/its DATA footprint is a bounded-range bounded-incidence enlargement of those bits. For a fixed DATA set W, b_W is dominated by a fixed multiple of the number of initially corrupted baseline bits in a fixed O(|W|) neighborhood. Its exponential moment consequently has the same small-parameter fixed-set form as an initialization seed charge.

For example, when each baseline bit belongs to one view and W meets at most c|W| relevant bits,

    E exp(theta b_W) <= [1+p0(exp(theta)-1)]^(c|W|).

Bounded duplicates change c and the coefficient multiplying theta. Neither site independence nor independence from future physical faults is required if the native actual-record estimates remain uniform and the combined positive measure is handled by Holder/Cauchy-Schwarz.

A backward certificate terminating on a late copy of b_W is paid by this SAME initial random defect set. It is not asserted to be a newly independent fault. The event may be union-bounded over root times, as in the ordinary native memory proof. The total spacetime volume is still controlled by its terminal slice because the ancestral expansion remains geometric.

This supplies a candidate bound of the familiar form C N(1+t)exp(-cN), after decreasing the fixed baseline/native thresholds and retaining a linear component cutoff. Any pre-existing e0 can separately be charged through INITIAL_SEED_SLAB.md. Promoting this to a native theorem requires an independent check of this modified deterministic contract and its actual baseline implementation.

## 9. An explicit obstruction to inconsistent baseline copies

A common potential is essential. Consider one classical DATA bit e and two owners. Owner A regards target zero as correct and flips e whenever e=1; owner B regards target one as correct and flips whenever e=0. Each locally believes its correction decreases its own nonnegative energy by one. Alternating successful evaluations produce infinitely many flips even with no noise. There is no shared strictly decreasing U_eta.

This toy example is not a counterexample to a properly shared-baseline GPT controller. It refutes the attempted proof that independently corrupted per-hub baseline copies can simply be absorbed into a single fixed eta without a consistency mechanism. The finite-work argument would already fail.

## 10. Operational boundary: what is and is not supplied

The mathematical proposal protects an unknown signed code coset while an expensive Pauli-frame computation is pending. It works because the local syndrome DIFFERENCE, not its validity as a global syndrome, is processed by a bounded finite table.

The actual native implementation still needs:

1. One shared, time-independent baseline value for each potential view during the protected wait. If physical program bits drift, their effects must be included in a new dynamic-baseline fault theorem. A nominal Hamiltonian coefficient hardwired from m0 is not automatically a fault-tolerant classical memory.
2. Bounded-range access to those shared values by every reader, including them in full read locks/dependencies and the forest-frame support/incident budgets.
3. A physical initial syndrome-record instrument with a certified sparse mismatch eta and compatible clean controller initialization. General CPTP factory faults need the same positive-record/common-span treatment as elsewhere.
4. A charged mode change when the eventual full Pauli frame is applied or reinterpreted, so the target stabilizer signs and actual physical DATA frame remain consistent.

Fixed quenched disagreement is therefore mathematically manageable. A noisily stored evolving baseline register is not solved by declaring it fixed, and independently copied baseline bits are not a substitute for shared consistency.
