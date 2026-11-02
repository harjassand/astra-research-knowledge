# Exact annealed hole-group gas for the commuting reference

2026-11-02. Constructor derivation, jointly developed with root. **New proposed theorem with explicit interfaces, awaiting independent audit.** It is a generic quantum perturbation result for the commuting stabilizer reference, not yet for the same native clock Hamiltonian. Its admission parameter is beta v, with no exp(beta J) loss.

Read with COMMUTING_REFERENCE_HOLE_IDENTITY.md, EXACT_TRACE_POLYMER_REASSEMBLY.md and COMPRESSED_CHARACTER_CONTACT_LEMMA.md. All local dimensions/dictionary norms remain explicit.

## 1. Reference and source operator expansion

Use H0=epsilon sum_a q_a, with B=beta epsilon, actual valid syndrome subspace, equal sector dimensions, the exact T_plus defect gas, and independent onsite bath if desired. More generally use epsilon_min for activity bounds. Let the bounded-degree local perturbation dictionary have labels lambda, norms <=v, bounded data/bath support and at most b_c affected checks per label.

For each Dyson history, its USED-label connected components A are defined by overlap of actual data/bath supports and affected-check marks. Distinct components have disjoint marks. All chronological interleavings are recovered by sorting, so there is no extra combinatorial factor.

For A with m_A labels, form the exact hole replacement O_A of the prior note. It has local physical support at most b_op m_A and norm

  ||O_A|| <= q0^{m_A}, q0=exp(beta v)-1.

Only its part commuting with every stabilizer contributes to the full trace: different components have disjoint affected-check sets, so a nonzero syndrome change from one cannot be canceled by another. Pinching O_A into the stabilizer commutant is a norm-contractive conditional expectation. Because Pauli conjugation does not enlarge support, the pinched operator remains supported in the same b_op m_A sites.

Expand its data part in local Paulis; retain coefficient operators on its disjoint bath sites, then perform those local bath traces. The coefficient l1 norm is bounded conservatively by

  sum_B |a_{A,B}| <= [4^{b_op} d_B^{b_B} q0]^{m_A}=:q^{m_A}.

Each retained B commutes with all checks. If b_op m_A<d, it is a stabilizer up to a phase incorporated in a_{A,B}; normalize its vacuum eigenvalue to +1. Large words retain their logical matrix and are treated separately at the end.

This source operator expansion is exact and its coefficients are independent of the background syndrome. It does not replace the operator by an unrestricted random hole.

## 2. Exact scalar coefficient before regrouping

For a compatible collection of original source components (A,B_A), let C be the union of released checks. Let a compatible canonical defect collection D represent the original syndrome sigma, with disjoint top supports tau_gamma. For scalar source words, its weight is

  [product_A a_{A,B_A}]
  exp[-B(|sigma|-|sigma intersect C|)]
  product_A chi_{B_A}(sigma).                          (G1)

Bath factors have already been normalized/included above. Equation (G1) follows by replacing the Boltzmann factors on C, not by comparing individual perturbed syndrome weights. It retains exact valid-syndrome constraints through the canonical defect configuration.

## 3. Unique hole-group construction

Make a bipartite contact graph with original source components and reference defect polymers. Join source A to defect gamma precisely when TOP SUPPORT(tau_gamma) intersects C_A. Sources sharing physical/affected marks were already one USED-label component. Keep defect nodes with no source edge as ordinary defect polymers. Each connected component containing a source is a hole group G.

This grouping is unique and reversible. A group stores its original source components, Pauli labels, swallowed defect polymers and their canonical traces. No intermediate decoder history is stored or charged. Let

  m(G)=total distinct source labels,
  M(G)=total swallowed defect mass,
  C_G=union_A C_A,
  tau_G=sum swallowed tau_gamma,
  h(G)=|tau_G intersect C_G| <= min(M,b_c m).

Its internal activity includes all its a_{A,B_A}, its internal character product, and the factor exp[-B(M-h)]. Hence its summed absolute coefficient envelope is

  q^m exp[-B max(0,M-b_c m)].                         (G2)

Swallowed defect traces attach to source label/check ports at occupied top leaves. Together with the connected source-label components, the group is connected in a fixed bounded-degree augmented space-scale graph. Its vertex/finite-label count is O(m+M). Rooted group entropy is at most A0^(m+M), with all local Pauli expansion overhead already either in q or A0, not counted twice.

## 4. Exact remaining pair factors

Ordinary defect polymers retain their hard-core incompatibility. Between groups, or a group and an ordinary defect, forbid:

- overlapping/incompatible original defect polymers;
- overlapping original source marks;
- a released check of one group containing an occupied top defect of the other object (which would have made them one group).

All these are finite geometric hard-core contacts on stored source ports/defect traces. There is no need to swallow a remote stabilizer filling or an entire time column.

Apart from these exclusions, the remaining interaction is exactly the character phase. For group G and ordinary defect gamma it is

  h(G,gamma)=product_{A in G} chi_{B_A}(tau_gamma).

For two groups G,H it is

  h(G,H)=[product_{A in G}chi_{B_A}(tau_H)]
          [product_{A in H}chi_{B_A}(tau_G)].

Forbidden pairs have h=0; otherwise h is +/-1. Thus |h|<=1. Every phase in (G1) appears exactly once as an internal factor or one of these symmetric pair factors. Distinct ordinary defects have no character phase.

The result is an exact scalar complex-measure gas in the sector where every original source word is stabilizer-scalar. No fixed-syndrome activity bound is used.

## 5. The free-hole capacity bound: never factor exp(B b_c m)

For fixed m, summing M with entropy gives

  sum_{M>=0} A0^M exp[-B max(0,M-b_c m)]
       <= C_B [C0]^{m},

provided B>log A0 with fixed margin. Split at M=b_c m. The first part is a finite geometric sum of at most b_c m unpenalized defects; the second is a decaying tail. C0 depends on local geometry/b_c and the chosen cold margin, not exponentially on B.

For KP it is useful to keep a joint charge a(m+M). Choose lambda>0 and impose

  B > log A0+a+lambda,
  q [A0 exp(a+lambda)]^(1+b_c) < small constant.        (G3)

Writing M=b_c m+r when M>b_c m, and using M<=b_c m otherwise, shows that the rooted entropy-weighted activities have an exponentially small tail in u=m+M. By strengthening the strict inequalities, all rooted sums can be made arbitrarily small and bounded by C exp(-lambda u). The source admission depends on q=const[exp(beta v)-1], not exp(B)q.

## 6. KP hard-core rows

A fixed object of total stored size u has O(u) source ports and defect-trace vertices. Every hard-core incompatibility listed above has a bounded-local contact with one of these vertices. The rooted sum over conflicting objects is therefore at most delta_hc u, where delta_hc is made small by (G3) and the ordinary defect cold bound. This is ordinary connected-animal counting in the augmented graph, not a filling-volume estimate.

## 7. KP character rows: asymmetric multiscale control

Retain each ORIGINAL connected source component's word B_A inside a group. Do not infer a small physical diameter for the entire hole group.

For a fixed source word B_A and a neighbor's defect syndrome tau, use the exact decoder pairing

  chi_{B_A}(tau)=(-1)^{sum_i[(J_{0:i})^* B_A,c_i(tau)]},

including prepass/terminal terms. The adjoint probe has at most C m_A K_adj^i sites at height i. A nonzero correction contact there requires the neighbor's swallowed or ordinary defect mass >=c2^i. Its total group size is at least that mass, so the exponential u-tail from (G3) gives a rooted density <=C exp[-c'lambda 2^i]. Consequently the source-to-neighbor-defect character row is bounded by

  C m(G) sum_i K_adj^i exp[-c'lambda 2^i].             (G4)

For a fixed root defect syndrome tau_G of mass M(G), use the polynomial local filling of each ORIGINAL neighbor source word B_A. A nontrivial pairing puts that component's physical anchor in a polynomial(m_A) neighborhood of an occupied root base check. Rooted group counting with that anchor and its exponential total-size tail gives

  C M(G) sum_{u>=1} poly(u) exp[-lambda u].            (G5)

The same estimates cover ordinary-defect roots. For two group phases use |ab-1|<=|a-1|+|b-1|. Together (G4)-(G5) are linear in m(G)+M(G), and tend to zero with the chosen cold/source margins. They fit the remaining portion of the KP charge a u.

The row-weight constant K_adj need not equal the column lift constant. Actual nonzero corrections, not zero halos, are what carry the high-level ancestry cost.

Thus the scalar gas has an absolutely convergent normalized cluster expansion at sufficiently small beta v and sufficiently cold B, with no exponential-in-B source admission loss.

## 8. Actual static witness extraction by exponential tilt

For a fixed base-check set T, let N_T(sigma)=|T intersect supp sigma|. Defect top supports are disjoint in every represented configuration, including across groups. Multiplying each defect-bearing object's activity by

  exp[t |T intersect tau_object|]

therefore represents the scalar-source contribution to Tr[e^{t N_T}e^{-beta(H0+V)}]. If exceptional logical words have been truncated, this scalar gas is not by itself guaranteed to define a positive probability law. Reserve enough exponential u-tail slack so the tilted gas obeys the same KP criterion. Interpolate this activity tilt. The rooted log-ratio bound, anchored at the base checks of T, gives

  |Z_small,t/Z_small,0| <= exp(delta_t |T|),

where delta_t can be made small by the admitted margins; pure source objects with no swallowed defects do not contribute. Let r_t,r_0 be the relative exceptional-matrix bounds for the tilted numerator and untilted denominator, with r_0<1. The ACTUAL positive Gibbs moment is then at most exp(delta_t |T|)(1+r_t)/(1-r_0). Only now apply Markov:

  Pr(T subset syndrome) <= exp[-(t-delta_t)|T|](1+r_t)/(1-r_0). (G6)

Choose fixed t larger than the decoder witness entropy and choose lambda/margins accordingly. This yields the actual full-Gibbs rare-bad consumer for the scalar-source gas, accepting virtual defects at a source-controlled floor. It is not a ground-gap statement or a volume-error estimate.

## 9. Exceptional logical words at fixed beta

An original source component can have a non-scalar logical word only if m_A>=d/b_op. Mark such a component; its group activity retains the same envelope, and all surrounding scalar pin factors have modulus<=1. The already-established exceptional-matrix-root method can be reused once its pinned charge is checked against the present source-group rows, giving a volume-anchored tail poly(n)(Cq)^(d/b_op). At fixed beta this is small at large n and supplies the correction to the full physical Gibbs trace/marked numerator. It is NOT uniform for arbitrary beta with fixed v, since q itself grows with beta; no all-beta claim is made.

## 10. Audit boundary and native limitation

The exact regrouping, free-capacity bound and two KP contact estimates are the proposed closure. They need an independent detailed audit, especially the Pauli coefficient/pinching step, unique source/defect group reconstruction, and marked moment bound.

Most importantly, the native clock H is not H0. Its raw local terms cannot be turned into the positive commuting H_C hole identity without paying clock self-pressure. The proved dynamic-flux and time-point-pin lemmas suggest how to transfer the mechanism, but do not yet provide arbitrary native matrix-unit replacements with the required beta-v activity. This note earns, if audited, a materially improved commuting-reference quantum perturbation theorem and a concrete target for native transfer, not the requested final native-memory operating window.

## Fresh audit clarification on exceptional roots

In a decoder frame every centralizer Pauli B, including a logical word, obeys D(sigma)^dagger B D(sigma)=chi_B(sigma) B_L. Thus the compressed-adjoint forward character bound applies to exceptional logical roots too. The reverse polynomial-filling row is needed only for ordinary scalar background sources. Both tilted and untilted exceptional ratios must be proved with reserved activity slack before a positive Gibbs probability is claimed.
