# How much syndrome information must become irreversible?

Author: `producer-workspace/classical_capacity`, 29 October 2026. New construction; independent review is separate. The accepted `p2_protection` results remain unchanged. This is a theorem about an acquired completed quantum instrument, not a circuit threshold, entropy-production bound or implemented device advantage.

## 1. Consequence and precise interface

Distance-order suppression does not require making the entire error syndrome classical. After **coherent correction using the full fine syndrome**, only a bounded fault-weight tier must lose its coherence. For a code correcting the acquired fault set through order t, at most **t+1 irreversible sectors** suffice for order d=2t+1, even when the complete fine syndrome remains a quantum output. For odd phase repetition codes this number is optimal for nondemolition syndrome-diagonal conversion. Imperfect conversion has a graded requirement: coherence between tiers separated by Delta can first hurt at order d-Delta, so overlap O(eta^Delta) restores order d.

The mathematical operation retains the logical output, the complete fine syndrome S, all actual classical detector/receiver records, and all quantum memory B that can return. Any subsystem traced in the converter must remain outside every later admitted interaction. A purification which later returns belongs in B/O from the beginning. No marginal calibration law, unread key average or temporarily inaccessible environment establishes that boundary.

Source encoding, syndrome extraction, coherent lookup/correction and the converter are acquired operations. Added source-control noise, direct contact with unprocessed source-imprinted fields, leakage, loss, capture and later reset require their own completed interfaces and budgets. A known logical target has been removed in its correct output frame. The theorem does not construct a compatible gate or an efficient decoder.

## 2. Acquired exposure grading and coherent decoder

Let E_p be the source phase characters attainable at at most p admitted fault locations. Take E_0={0}, E_p+E_q contained in E_(p+q), and the usual saturation at the number N of locations. Define the minimum exposure cost

    w(e)=min{p:e in E_p}.

Characters outside the acquired span are excluded rather than assigned free cost. Require ker(H) intersect E_(2t)={0}. For the accepted binary-subspace exposure sets, E_t+E_t=E_(2t), so this is equivalent to H separating E_t; for a different grading with only the stated containment, the kernel condition is the explicit hypothesis. Put d=2t+1. For each reachable syndrome s choose a minimum-cost leader e_s, with r(s)=w(e_s). The coherent decoder extracts s and performs the prescribed correction. Its action on a source phase error is

    Z^e V|psi> -> Z_L^{lambda(e)}|psi> tensor |He>,

up to known phases absorbed into the bath coefficient. In the phase-code setting lambda(e)=0 exactly when e=e_(He); every error of cost at most t is corrected. The proof only needs the corresponding residual-logical criterion and the stated separation. In a different degenerate code, replace it by its actual logical cosets; no degeneracy conclusion is silently imported.

The exact completed isometry has a fault-subset expansion W=sum_J W_J, with ||W_J||<=a_J=product_(j in J) eta_j. Coefficients can be arbitrary operators on a noncommuting persistent bath, including initially correlated logical/field/bath/reference inputs. Every character in W_J belongs to E_|J|. No stochastic independence or sum of absolute Pauli coefficients is assumed.

Define the tier and its syndrome projector by

    c(s)=min(r(s),t),       P_c=sum_(s:c(s)=c) |s><s|.

Unreachable syndromes can be placed arbitrarily; they have no acquired input support. At most t+1 projectors are nonzero. Let W_J^c=(I_L tensor P_c tensor I_B)W_J after coherent decoding.

**Two support facts.**

1. W_J^c=0 if |J|<c.
2. W_J^c=I_L tensor A_(J,c) if |J|<d-c.

For c<t, an error e in that tier has leader cost c. A nontrivial residual implies e+e_s is a nonzero kernel character. Subadditivity and separation force w(e)+c>=d. For c=t every character has cost at least t, and a nontrivial residual has cost at least t+1=d-t because E_t is corrected. These arguments concern full operator amplitudes and therefore survive all bath correlations.

### General stabilizer extension

The two support facts, and hence Sections 3 and 6-8, do not require commuting phase errors. Let an arbitrary stabilizer code have an acquired Pauli exposure cost w(P), ignoring scalar Pauli phases, with w(PQ)<=w(P)+w(Q). Require that every Pauli in the normalizer but outside the stabilizer have cost at least d=2t+1. Use a minimum-cost Pauli leader E_s for each syndrome, and coherent extraction/correction with residual logical Pauli L(P). If L(P) is nontrivial, E_s^dagger P is a nontrivial normalizer coset, so w(P)+r(s)>=d. All errors of cost at most t are corrected, including degenerate errors differing by a stabilizer. The same capped tiers and support facts follow. A completed fault path must actually have Pauli expansion supported on cost <=|J|; this is an acquired propagation/locality condition, not something granted for an arbitrary controlled circuit.

Thus the complete-channel theorem extends to full Pauli noise, arbitrary stabilizer degeneracy and persistent operator-valued baths whenever those premises hold. Fine syndrome extraction, coherent correction and the selected target frame remain supplied. The phase repetition family in Section 5 is a sharpness example, not the extent of this extension. Generalized non-Pauli decoders are not asserted to possess the needed syndrome/cost structure.

## 3. Tier dephasing preserves the complete channel order

Apply the physical tier instrument

    Delta_c(X)=sum_c |c><c|_C tensor P_c X P_c.

The fine S is retained quantumly. C is the actual classical tier record; an orthogonal copy or equivalent discarded detector sector must be permanently retired. Fine-syndrome coherences within a tier remain present. Let Phi be the completed actual map and define the normalized comparison

    R_mix(sigma)=Tr_L Phi(I_L/K tensor sigma),
    P(T)=id_L tensor Tr_L T(I_L/K tensor .).

R_mix is CPTP and retains all declared output records and quantum memory. Its law may differ from a full-syndrome instrument or an earlier unencoded receiver. This mixed-logical-input construction is inherited machinery, including Astra N951; it is not a new invention here.

For a cross path (J,Q) with |J|+|Q|<d, tier measurement keeps only equal tiers c. If either side is logically nontrivial, support fact 2 gives that side's degree at least d-c, while fact 1 gives the other side degree at least c. Their total is at least d, a contradiction. Every surviving low-degree cross map is therefore id_L tensor a common operator map, including the coherent fine syndrome and the actual coarse record.

P is a diamond-norm contraction and ||I-P||<=2. Cross-map norms are at most a_J a_Q. Thus the complete half-diamond error obeys

    epsilon = (1/2)||Phi-id_L tensor R_mix||_diamond
            <= min(1, sum_(|J|+|Q|>=d) a_J a_Q).                 (1)

This is the same normalized distance-order tail previously proved using full measured syndrome. The exact tail is the degree-at-least-d part of product_j(1+eta_j z)^2 at z=1. The present new bridge is the smaller necessary irreversible partition while keeping S quantum, not the tail polynomial or ordinary coherent QEC itself.

## 4. Exact dangerous-coherence criterion

For any specified syndrome conversion M, define its fine off-diagonal block on bath operators by

    M_(s,u)(X)=M(|s><u| tensor X).

All actual records are outputs of M. Draw an edge s--u when there are acquired characters e,f with syndromes s,u, w(e)+w(f)<d, and at least one nontrivial logical residual after the fixed coherent decoder. At this total degree at least one character is correctable, so one residual is identity. Equal syndromes cannot be edges by code separation.

If M_(s,u)=0 on every edge, every low-degree character cross map factors through the logical identity. This is a sufficient all-input, all-record criterion for distance order. It is also necessary for **coefficientwise universal** cancellation over arbitrary operator-valued character amplitudes: a nonzero M_(s,u), multiplied by a nontrivial logical Pauli on one side and identity on the other, is not fixed by P. A particular constrained circuit can have additional cancellations; this statement is not a necessity theorem for every such circuit or for an alternative redesigned decoder.

The condition becomes sharp and directly physical for a nondemolition Schur instrument on S:

    M(|s><u|)=|s><u| tensor sum_y gamma_y(s,u)|y><y|,
    Gamma_y=[gamma_y(s,u)] >=0,  sum_y gamma_y(s,s)=1.        (2)

The bath is a spectator in (2); bath-coupled converters are covered by block superoperators, not by scalar calibration. Distance-order cancellation of all admitted cross amplitudes holds exactly when **gamma_y(s,u)=0 for every dangerous edge and every actual y**. It is insufficient that sum_y gamma_y(s,u)=0. These are finite PSD constraints, allowing a graph/Gram-matrix construction rather than a mandatory full-syndrome measurement. A proper coloring gives one explicit projective converter; a general Gram representation can do better than coloring for some graphs, so chromatic number is not asserted to be the general optimum.

## 5. Sharp necessity for odd phase repetition codes

For the phase repetition code n=d=2t+1 with phase-error cost equal to source support size, each syndrome has precisely two character representatives: a unique minimum-weight leader e_s of weight r(s)<=t and its complement, of weight d-r(s), which acts as a nontrivial logical Z after correction.

For any two syndromes with r(s)>r(u), the pair (complement of e_s, e_u) has degree d-r(s)+r(u)<d and a nontrivial/identity logical pair. Conversely equal-weight tiers have no dangerous edge. The dangerous graph is therefore the **complete multipartite graph with t+1 parts indexed by leader weight**.

This is a necessity for an actual physical local-noise family, not only formal independent coefficients. Apply product_j exp(-i theta Z_j), then the fixed coherent decoder and a fixed Schur converter. The (s,u) output block has a leading bad/good coefficient proportional to theta^[d-r(s)+r(u)]. The reverse good/bad coefficient has strictly larger degree d+r(s)-r(u), and the bad/bad coefficient also has larger degree. The leading term cannot cancel. A logical superposition/reference input witnesses it. Since the fine syndrome and actual y are retained, cancellation between output blocks or records cannot hide the term. Nonzero gamma_y(s,u) consequently prevents O(theta^d) complete-channel suppression.

Choose one syndrome from each tier. For any fixed converter satisfying (2) **and achieving the stated O(theta^d) complete-channel order**, its discarded Stinespring environment has orthogonal support for these t+1 inputs. Indeed zero accessible off-diagonal partial trace implies orthogonal supports of the two complementary environment states (equivalently their fidelity is zero). Hence its purified Stinespring environment dimension and Kraus rank are at least t+1. Projective tier dephasing attains t+1, with Kraus operators P_c (or |c>_C tensor P_c if C is reported).

The lower bound is not on a bare detector supplied in a mixed state. For example, three controlled unitaries I,X,Z on one maximally mixed detector qubit give gamma(c,b)=Tr(U_c (I/2) U_b^dagger)=delta_(c,b), hence dephase three tiers with a two-dimensional physical detector. Its Stinespring description includes the mixed supply's purifier, giving a four-dimensional detector/purifier space and a rank-three channel, consistent with the bound. If that purifier can return, it belongs to the accessible output and cannot be omitted. No lower bound on the number of newly prepared pure detector qubits or actual reset heat follows from the Kraus-rank statement alone.

This is a minimum irreversible-sector/Kraus-rank statement **with fine syndrome retained and a fixed coherent decoder**. It is not a bound on Shannon entropy of the rare tier distribution, heat, energy, reset time, detector gate count, or all possible correction architectures. Permanently discarding the entire syndrome is a conventional alternative and changes the retained-output task. Reversible uncomputation using an acquired error history or a more powerful recovery likewise changes the interface.

## 6. Quantitative imperfect conversion with all records

Allow a general CPTP M on S and B, independent of the logical system. Its output O contains every returning subsystem and actual record. For distinct tiers define the complete off-diagonal transmission norm

    alpha_(c,b)=|| X -> M(P_c X P_b) ||_diamond <=1.          (3)

The inequality follows from an isometric dilation and trace-norm contraction; an arbitrary reference is already included. This definition tests operator-valued bath inputs, not just selected states. At a fixed completed interface it is a physical property to acquire or derive.

Let A_p=sum_(|J|=p) a_J and

    H_d=sum_(p+q>=d) A_p A_q,
    L_(c,b)=sum_(p+q<d) A_p A_q
       * 1{ (p>=d-c and q>=b) or (p>=c and q>=d-b) }.

The two alternatives cannot both occur in this low-total-degree region. Decompose only by the t+1 tier projectors. P_c W_J has norm at most a_J; if neither alternative holds, both logical sides are identity by the support facts. The cross-map/normalization bound gives

    epsilon <= min(1, H_d + sum_(c!=b) alpha_(c,b) L_(c,b)). (4)

High-degree terms are bounded before the tier decomposition, avoiding an unnecessary tier count there. No absolute sum of Pauli/bath coefficients occurs. In particular

    L_(c,b) <= sum_(m=d-|c-b|)^(d-1) [z^m] product_j(1+eta_j z)^2.

For eta_j<=eta and fixed N,t, residual tier coherence alpha_(c,b)=O(eta^|c-b|) preserves O(eta^d). A uniform alpha only gives the sufficient structure O(eta^d+alpha eta^(t+1)). Constants and N-dependence remain in (4); these asymptotic powers are not uniform scalable thresholds.

**Sharp graded necessity in repetition codes.** This scaling is also necessary for the tier-dependent Schur family, even if the meter depends on the small noise parameter. Use the physical scalar-bath product rotation from Section 5, let a=cos(theta), b=sin(theta)>0, and take two syndrome leaders of weights r>v. Their good and bad amplitudes are g_r=a^(d-r)(-i b)^r and h_r=a^r(-i b)^(d-r). Apply the channel difference D=Phi-P(Phi) to the logical matrix unit |0><1|. Its retained fine-syndrome block (r,v), separately in each actual y, has coefficient gamma_y(r,v) times

    C_(r,v)=h_r conjugate(g_v)-g_r conjugate(h_v)-2 h_r conjugate(h_v).

The trace norm of that off-diagonal block is a valid lower bound on the diamond norm (matrix-unit input trace norm is one). Direct summation over the actual y gives

    epsilon_P >= (alpha_(r,v)/2) |C_(r,v)|,
    |C_(r,v)| >= a^(d+r-v) b^(d-r+v)
       * [1-(b/a)^(2(r-v))-2(b/a)^(d-2v)].                 (7)

The bracket is positive and tends to one at small theta. Moreover, any comparison id_L tensor R has half-diamond error at least epsilon_P/2, since ||I-P||<=2. Thus an O(theta^d) complete-operation comparison requires alpha_(r,v)(theta)=O(theta^(r-v)). Together with (4), this gives necessity and sufficiency of the graded overlap orders within this converter/code/noise family. It does not optimize a new decoder or arbitrary channels which erase/change the fine syndrome.

For a scalar instrument (2) depending only on tiers,

    alpha_(c,b)=sum_y |gamma_y(c,b)|.

If p(y|c)=gamma_y(c,c), positivity gives

    alpha_(c,b) <= sum_y sqrt(p(y|c)p(y|b)).                (5)

Thus actual-record distinguishability controls retained coherence through a Bhattacharyya/fidelity overlap. Efficient real diagonal measurements attain equality. For bath-coupled meters, an analogous sufficient bound follows from uniform operator effect bounds M_y^*(I) restricted to each tier; a fitted marginal confusion matrix does not qualify it. If the record has a decision event identifying c with error at most delta on all inputs in tier c, and at most delta false positives on all inputs in tier b, a safe dimension-independent bound is alpha_(c,b)<=2 sqrt(delta). This follows by splitting the instrument into the event and its complement and bounding the two Stinespring cross maps. Scalar known likelihoods can give the sharper overlap in (5).

## 7. A finite meter construction with the graded overlap

Use t fresh independent pointer qubits, one for each threshold j=1,...,t. Coherently compute whether c>=j and prepare pointer state |p_0>=|0> or

    |p_1>=kappa|0>+sqrt(1-kappa^2)|1>,   0<=kappa<=1.

Measure each pointer in its computational basis and keep the entire actual t-bit word y; permanently retire the measurement purifications. No pointer outcome controls the already completed source correction. For tiers c,b the two unary strings differ at |c-b| positions. Their efficient measurement has nonnegative scalar cross coefficients and therefore

    sum_y |gamma_y(c,b)| = kappa^|c-b|.                   (6)

Taking kappa<=C eta meets the graded condition. A single differing threshold has one-sided classification error kappa^2, so this construction does not require a uniform O(eta^(2t)) readout error for the whole tier. It pays t pointer preparations, controlled preparations, actual readouts and no-return purifications per call, plus the coherent tier computation and uncomputation/control support. Those controls can be costly: minimum exposure weight need not be efficiently computable. Independent fresh pointer supply is a sufficient implementation assumption for (6); recycling contaminated pointers does not inherit the product overlap.

Finite reversible implementation is explicit: for q fine-syndrome bits, tabulate c(s), compute its binary value into b=ceil(log2(t+1)) zeroed work bits by at most b*2^q syndrome-pattern-controlled NOTs, apply the threshold-controlled pointer preparations, and reverse that lookup to return those b work bits to zero. A direct truth-table implementation of the thresholds uses at most t(t+1) b-bit-pattern-controlled rotations. This is an existence/count upper bound for ideal multiqubit-controlled primitives, not a calibrated decomposition into native gates. It exposes the exponential lookup cost instead of treating tier computation as free. Structured codes may admit better circuits.

At kappa=0 an optimized joint tier pointer needs only t+1 orthogonal states, rather than the unary construction's 2^t-dimensional workspace. No claim is made that the unary finite-error meter minimizes that dimension or energy. If the complete fine syndrome can instead be safely reset/discarded, ordinary coherent error correction already supplies full dephasing without reading any syndrome; that is a strong conventional option.

## 8. Useful failures and completed-call reuse

**Retained random phase key.** For t=1, randomly apply the tier phase (-1)^(k c), k uniform. Forgetting k dephases the two tiers. Retaining its actual classical value gives gamma_k(0,1)=(-1)^k/2, so the marginal sum is zero but alpha_(0,1)=1. The key can undo the phase. The complete-record channel consequently has the lower t+1 order. This is the same physical key-retirement boundary emphasized by Astra U1052, now a syndrome-specific exact witness.

**Returned purification.** A coherent copy |s>|0>_D -> |s>|c(s)>_D looks like tier dephasing only after tracing D. If D returns, the inverse controlled copy erases it and restores all intertier coherence. For the repetition code the full accessible channel has a term of order t+1. No later data interaction is needed to witness the complete-channel failure; allowing later interaction can use that correlation. No-return is therefore an operation premise, not an assertion that a physical environment is metaphysically destroyed.

**Noisy feedback is a different error.** Equations (4)-(6) assume the fine coherent correction has already occurred. They do not qualify a circuit which uses a mistaken coarse/readout label to choose a source correction. A wrong applied logical Pauli with probability delta can contribute order delta even at zero field-noise strength. If a particular wrong correction is still correctable later, its actual completed decoder must be analyzed; it cannot be assigned that worst case automatically.

**Composition.** For calls satisfying (4) on their complete joint inputs and outputs, including all returning memory, a hybrid argument gives total half-diamond comparison error at most sum_i epsilon_i under arbitrary CPTP processing and actual-record adaptation between completed calls. R_mix can differ by history and call, with uniform conditional bounds. Initial logical/bath correlations are allowed. Returning old fine syndromes and bath are charged in the next input; traced detector purifications are not permitted to return. Interventions inside a call require a separate causal-comb contract. A completed-call diamond bound alone does not establish those stronger timings.

## 9. Relation to known machinery and scientific reach

The [information-disturbance result of Kretschmann--Schlingemann--Werner](https://arxiv.org/pdf/quant-ph/0605009) and [approximate-QEC framework of Beny--Oreshkov](https://arxiv.org/pdf/1103.0649) optimize recovery against complementary-channel leakage; [Beny's perturbative QEC](https://arxiv.org/pdf/1102.3809) characterizes leading-order correctability. Those are broader general frameworks and conventional alternatives when redesigning the recovery is allowed. Here the coherent recovery and acquired error grading are fixed, the fine syndrome is deliberately retained, and the question is which particular record coherences obstruct a specified order. The graph, optimal repetition-code tier count and graded finite-meter law make this question constructive without hiding records or bath coefficients. No claim is made to replace general approximate-QEC optimization or establish historical priority for all related ideas.

Coherent/measurement-free QEC is established. [Heussen--Locher--Muller](https://arxiv.org/pdf/2307.13296) and [Veroni--Paler--Giudice](https://arxiv.org/html/2412.15187v2) supply strong fault-tolerant and scalable conventional constructions using coherent feedback plus fresh/reset resources. Deferred measurement by itself preserves the purification and does not prove the present complete-output suppression. Conversely, discarding/resetting the full syndrome is often simpler and may be better operationally. The new object is the least irreversible syndrome partition required by the specified completed error order while the remaining syndrome stays accessible quantumly.

Astra N1000's terminal-QND elimination explicitly traces ancillas after all readout, retains actual words before justified reduction and does not promote calibration mixtures to arbitrary future-memory guarantees. Its physical terminal boundary and U1052's fresh/private-key retirement are close ancestry. The source-specific reviews and missing original numerical archives retain their stated scopes. This construction does not re-review accepted undecidability foundations or predecessor compiler results.

The theorem makes it possible to design and audit partial syndrome-conversion interfaces, to assign different precision requirements to different pairs of fault grades, and to detect when a claimed improved error order depends on silently discarding a returning environment or an actual key. Immediate hardware is unnecessary for those consequences. Operational advantage still requires comparing the costs of coherent lookup, fine-syndrome storage, tier computation, meter supply, retirement and reset with full conventional syndrome measurement/reset under the same assumptions.

## 10. Evidence and status

`record_principle_checks.py/json` contains exact algebraic graph, graded-channel, finite-pointer and returned-record challenges. The general proof above supplies all-input and operator-norm claims; finite execution does not replace those derivations or infer device noise rates. `SOURCE_READ_SCOPE.json` records primary and governing-source passages actually read. Independent review, if performed, must be separately authored and pinned.
