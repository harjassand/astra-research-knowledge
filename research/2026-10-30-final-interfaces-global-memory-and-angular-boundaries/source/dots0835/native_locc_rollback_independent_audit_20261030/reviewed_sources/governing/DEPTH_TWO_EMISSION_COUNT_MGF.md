# Actual depth-two reset emissions: a physical-window COUNT moment
2026-10-30. New lemma for independent review. It counts bad-mask multiplicity, not merely occupied owner/time cells.

## 1. Statement and required actual instruments

Use the actual native machine and the exact mechanical/semantic ancestry of the companion. Start all mechanical/semantic marks at zero, with the explicit initialized native apparatus and forced first purge stated there. A physical primitive source e is an exogenous Poisson process of rate epsilon c_e, applying a local CPTP map, possibly with retained bath. Sum_e c_e<=nu N. Every nominal complete retirement T_h remains an ACTUAL separately recorded gain of the noisy generator.

The new actual-retirement proof gives finite-support witnesses

    alpha I <= Z_h <= I,
    (L_0-T_h)^* Z_h <= -r Z_h,

with common fixed alpha,r>0. Color their buffered overlap graph with P colors so each nominal local term touches at most one Z support in a color. A primitive kick touches at most b_Z same-color factors and has bounded incident rate budget J_R. At sufficiently small epsilon, the inherited product comparison gives, with rho=r/2,

    (L_epsilon-sum_(h in A) T_h)^* Z_A <= -rho |A| Z_A

for every same-color active set A. This is the actual noisy killed generator, not a fictitious reset subtraction. Let D>=1 bound the multiplicative Z_A cost of any ONE normalized prescribed insertion below. D is finite because primitive maps and actual reset gains have fixed enlarged support.

A depth-two endpoint is allowed to be ANY charged Bob T: an older mechanical defect can still be present when a later Alice semantic birth becomes its canonical LAST parent. If the Bob engine is mechanically clean, only SUCCESS is charged. Every charged reset is assigned to one primitive root by the deterministic rule in the companion. For Bob, take the union of mechanical and semantic birth events and assign its charged reset to the UNIQUE LAST such birth since the preceding T_h, even if an earlier birth also contributed to its mechanical defect. This is an accounting attribution, not a claim that the last birth is the only physical cause. It yields one canonical parent and keeps bounded fanout. Its path has at most two edges: root->Alice T, root->Bob T, or root->Alice T->Bob T. The owner has no T event in each intervening open interval. Mechanical Bob resets are charged; for a mechanically clean but semantically wrong Bob engine ONLY SUCCESS is DATA-changing and charged. Clean rollback is identity even for a wrong program.

A root has at most B=b_A+b_B+b_A c_AB charged reset descendants. Let K bound the total charged footprint mass of all descendants plus that root's direct fault charge. K is a fixed deterministic constant. Let Q_W be the full charged mass whose physical event times lie in any deterministic finite-measure time set W subset [0,t]. Then there is an explicit finite C, depending only on these local constants, such that for every theta>=0,

    || E_record[ exp(theta Q_W) I_record ] ||_diamond
       <= exp[ epsilon C N |W| (exp(theta K)-1) ].       (1)

Notation on the left denotes the positive tilted CP record map, with the prescribed initial zero-mark classical state. Equivalently its effect is bounded by the scalar right side times I, uniformly over every allowed initial DATA/reference/retained-bath state. No independent delay law, independent scheduler, or Poisson replacement for a quantum reset is asserted.

## 2. Arbitrary-color survival with prescribed CP insertions

First consider a deterministic VALID finite family of no-T intervals. For each owner, intervals have disjoint interiors. Suppose there are m intervals with total length ell, and q specified CPTP insertions at their endpoints or intermediate times.

For each spatial color c, let ell_c be the duration sum of its intervals. Pick a color with ell_c>=ell/P. The full event implies the no-T event for that color alone. The established backwards product-witness argument, with all unspecified physical faults retained, bounds its effect by

    alpha^(-m) D^q exp[-(rho/P) ell] I.               (2)

The stronger color-specific bound uses m_c and ell_c; replacing m_c by m only weakens it. The chosen color depends on this deterministic interval family, not on an unknown quantum state. No independence or Holder assertion is needed.

An actual selected reset gain J has J^*(I)<=kappa I with fixed kappa. Thus J/kappa is CP trace-nonincreasing. Complete it to a CPTP map on the same bounded support, for instance by adding the missing-effect Kraus operator. Replacing J by kappa times this completion only increases every subsequent positive event effect. Consequently (2) also handles selected reset gains at a multiplicative kappa each. This normalization is solely an upper-bound device: the original selected event remains an actual gain in the record expansion.

Endpoints are ordered consistently: an ending no-T interval is removed before its selected reset insertion; a newly born interval starts after its birth insertion. Coincident independent event times have zero continuous-time measure. All source/gain labels and erased outcomes may be summed in their actual CP instruments.

## 3. Effective roots, one path per root, and valid disjointness

Call a primitive root effective for W if the root itself lies in W or at least one of its CHARGED descendants lies in W. Let Y_W count DISTINCT effective roots. Deterministically,

    Q_W <= K Y_W.                                      (3)

For every prescribed set of k distinct effective roots, select just ONE witness per root: its own direct event if in W, otherwise one descendant in W and the canonical ancestral path to that descendant. There is no need to select every child. This removes the shared-parent overcount that obstructs a naive product kernel over all descendant emissions.

Why the family is valid:

- every selected Alice marked retirement has its LAST incident primitive root since its previous T; distinct roots cannot share that retirement;
- every selected Bob charged retirement/success chooses its LAST relevant cause since its preceding T (the unique LAST birth of the combined mechanical-or-semantic Bob mark, whether a primitive fault or dirty Alice retirement);
- two selected terminal paths ending at the same owner are separated by the earlier T, so their birth-to-retirement intervals have disjoint interiors;
- a shared intermediate Alice retirement cannot have two different primitive roots; selecting one path for each DISTINCT root therefore selects every intermediate Alice event at most once;
- Alice and Bob are different owner sets. Their intervals may overlap in time; (2) handles those overlaps by its spatial coloring.

Thus m<=2k, there are at most 2k selected actual reset gains and k root insertions, and all same-owner interval disjointness requirements hold BEFORE dropping any constraints. This also covers repeated Bob owners at different times; no distinct-owner-per-root assumption is used.

Set beta=rho/P and C_0=alpha^(-2) D^3, enlarged to cover zero/one-edge paths and fixed finite path-type multiplicities. On any valid k-root witness family, (2) is bounded by a product of k one-root path kernels, each with coefficient C_0, gain intensities, and exp[-beta times its total path delay]. Every other physical fault and nominal evolution remains in the robust killed maps.

## 4. Summable one-root kernel

Let kappa bound the total selected retirement/SUCCESS gain intensity for one owner and let A_1,A_2 bound the finite numbers of possible one-edge and two-edge owner paths from a source. Absorb C_0 into these finite constants if desired. For a root at time tau a dominating kernel is

    g_W(tau) = C_0 1_W(tau)
      + C_0 A_1 kappa integral_(v in W, v>=tau) exp[-beta(v-tau)] dv
      + C_0 A_2 kappa^2 integral_(v in W, v>=tau)
                                   (v-tau) exp[-beta(v-tau)] dv.     (4)

For a two-edge path integrate its actual intermediate Alice reset time u over tau<=u<=v. The survival lengths add exactly: (u-tau)+(v-u)=v-tau. The u integral therefore contributes v-tau. Selected reset densities are actual gains, bounded as in Section 2; they are not assigned an independent exponential waiting distribution.

The C_0 factor also multiplies the depth-zero term: even a direct root with no selected descendant interval can touch another path's larger witness support and incurs a prescribed-insertion cost. Integrating possible roots from the initial time gives

    integral_0^t g_W(tau) d tau
       <= |W| C_0 [1+A_1 kappa/beta+A_2 kappa^2/beta^2]
       = C_1 |W|.                                      (5)

The inequality is valid for disconnected W and arbitrarily old roots. Invalid chronological assignments are discarded while applying (2), then may be restored because the resulting scalar kernels are nonnegative. This ordering matters.

## 5. Poisson factorial expansion gives the COUNT MGF

For the actual finite primitive point configuration up to t,

    exp(theta K Y_W)
      = product_(root x) [1+(exp(theta K)-1) 1_(x effective)].

Expand over distinct selected roots. The k-th factorial term has factor 1/k!. Distinguishing k root points in the exogenous Poisson/Dyson expansion integrates their physical intensities epsilon c_e d tau and inserts their actual local CPTP maps. Every unselected root remains in the noisy propagators; there is no conditioning on an independent lifetime or a rare normalized reset record.

For each selected root, the effective event is the union of the direct/one-edge/two-edge witness alternatives. The quantum jump factorial expansion for the selected actual reset gains expresses this union upper bound as ordered gain integrals. A record with several possible witnesses may be counted repeatedly; this only increases the positive upper bound. Apply Section 3 on the VALID canonical ancestry domain, then enlarge to the unrestricted positive path-kernel domain. Sections 4 and sum_e c_e<=nu N show that the k-th term is at most

    [epsilon nu N C_1 |W| (exp(theta K)-1)]^k / k!.

Summing k gives (1), with C=nu C_1 (or absorb nu into C_1). The same calculation is an operator/effect comparison before choosing an input state, hence implies the tilted CP/diamond bound.

This controls repeated emissions within one time cell and their accumulated support mass. It does not replace that mass by a binary occupied-cell count.

## 6. Consequence and restrictions

For a fixed physical window of length T and any q>0, Chernoff gives

    Pr(Q_W>qN) <= exp[-theta qN
                     +epsilon C N T (exp(theta K)-1)].

After fixing native rates and a service window T, choose epsilon so the second exponent is at most theta qN/2. This gives exp[-theta qN/2] uniformly in the window's location and elapsed runtime, without restarting marks at window boundaries.

Initial dirty engines/semantic marks contribute extra root terms and are not covered by (1). Additive local faults and actual recorded nominal resets are mandatory. This is a stochastic physical-record lemma, not a theorem for arbitrary weak continuous Hamiltonian noise. Constants can be extremely poor. The lemma is a new proof candidate requiring review of the canonical path/disjointness and factorial-gain expansion; it is not labeled independently accepted here.
