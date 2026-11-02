# Removable full-trace witnesses through local duality

Date: 2026-11-02. This extends RESULT.md without assuming a local-stochastic law for physical Gibbs syndromes.

## Algebraic data

A and B are three-term cochain complexes in degrees 0,1,2. Fixed binary cochain maps F:A->B, G:B->A and homotopy H satisfy

I_A+GF=d_A H+H d_A.

All relevant coordinate row/column norms are uniformly bounded. In top degree 2 this becomes the equality on **all vectors**, not just valid syndromes,

I_{A^2}+G^2 F^2=d_A^1 H^2.

The decoder on valid inputs is R_A(s)=G^1 R_B(F^2s)+H^2s.

## Required dual full-trace certificate

For each valid dual input u, a deterministic complete run of R_B has a bounded-degree ambient space-scale trace whose connected components (or an explicitly specified deletion-closed component grouping) have the following properties:

1. Removing any union of complete original trace components reproduces the complementary run, including all component-dependent nonlinear decisions. Identical labeled active components make identical choices. This is a component-consistency/deletion-closure hypothesis, NOT bounded-radius dependence of a whole component choice.
2. Each selected union carries its original input subset u_C and a correction r_C, additive across disjoint selected unions, with d_B r_C=u_C. This identity must be established through the full correction trace including terminal processing, not by assuming u_C was valid beforehand.
3. In particular, terminal processing must be represented by a bag containing every occupied terminal input whose joint correction is used. If the terminal decoder acts globally on a constant-sized reference problem, include that entire problem as one bounded bag. A selected union then sees the original terminal input or zero, never an unproved-valid fragment. Normalize the zero-input terminal correction to zero.
4. All zero/nonzero tests or active-graph dependencies needed for deletion consistency are represented by fixed ambient bounded stencils. The charged spatial shapes of whole nonlinear components may be arbitrarily large, but have size proportional to their occupied input mass. Constant layers are zero-preserving. No uncharged global state or tie-break is permitted.
5. The certificate has entropy/height/distance estimates in its original scale coordinates; its total charged size is O(selected input mass), using the established contraction/packet accounting. Lifted physical correction supports are bounded separately and are not automatically counted as space-scale trace vertices.

Item 2 may instead be supplied by local correction/coarse-graining identities plus the terminal-bag property. It is the property ultimately needed below. If a dual trace theorem has only an ancestor witness and not a deletion-closed full trace, this extension does not apply.

## Physical linear prepass: retain cancelling gates

Let L=F^2. Build a bipartite prepass from physical input coordinates j to output row gates i whenever L_ij=1. For a particular physical input s, activate:

- each occupied input j;
- every row gate incident to at least one occupied input, **even if its XOR output is zero**;
- every incident occupied input wire of each activated row gate.

Join each nonzero output row to the corresponding initial occupied input of the dual full trace for u=Ls. Also join an active prepass gate to its corresponding initial dual input position whenever that position is already present as a charged dual stencil vertex, even if its value is zero. Zero-output row gates remain as connectors; they are not silently erased. Incidental zero vertices do not recursively activate additional gates.

The ambient prepass has bounded degree from both row and column sparsity. It has O(|s|) active sites. Its complete-component property is exact: if C is a union of connected components of this augmented prepass+dual trace, let tau=s restricted to its physical occupied leaves. Then each row of L has either all of its occupied input contributors selected or none. Consequently

L tau = u restricted to the selected dual input leaves,

L(s+tau)=u+Ltau,

including rows with cancellations. Omitting zero-output gates would make the first equality false in general (two cancelling physical inputs could be separated).

The same prepass may include H^2 stencils, at O(|s|) extra cost, if one wants explicit correction-wire bookkeeping. It is not necessary for the validity proof: H is fixed linear and can be applied algebraically after selection.

## Validity and deletion proof, with no circular validity assumption

Fix any union C of complete connected components of the augmented full trace. Let tau be its selected physical occupied input. By the prepass property, u_C=F^2tau is exactly the corresponding selected dual input. By the dual complete-trace correction identity, there exists the selected correction r_C with d_B r_C=u_C; this conclusion came from original trace/terminal processing, not a decoder guarantee on an assumed-valid restricted input.

Define a physical correction

a_C=G^1 r_C+H^2 tau.

Then

d_A a_C=G^2 F^2tau+d_A H^2tau=tau.

Thus every such physical leaf set tau is a valid physical coboundary. The complementary input s+tau is valid too. Component deletion consistency plus the exact linear prepass gives the complementary dual run, and fixed linearity gives the corresponding physical correction decomposition. No equality of Gibbs measures is used.

This also handles a prepass component whose dual output is zero: its physical leaf set is a coboundary with correction H^2tau.

## Why no fully expanded G postpass should be counted

Do NOT generally attach every physical site of G times a fully lifted dual correction to the entropy animal. A level-i correction can lift to K^i times its charged mass, so this would destroy the required O(leaf mass) animal-size bound.

Instead apply G algebraically to each already selected correction contribution. Additivity is automatic, even if different G outputs overlap and cancel. Its column norm multiplies the physical support bound by only a constant. If a literal postpass is desired, place bounded G-gate labels at the original charged scale locations and separately certify their composed lift interpretation; do not claim the fully expanded physical support has constant cost per trace site.

H likewise is linear: its discrepancy contribution is H^2 d_A e and is bounded for a physical single fault. It does not require a nonlinear trace dependency. Optional H^2 prepass gates merge components but preserve linear mass accounting.

## Two-run instability witnesses

Run this augmentation for s and s+d_A e. Their dual input discrepancy is F^2d_Ae=d_BF^1e, supported on a bounded number of dual checks; F^1e is a bounded-weight physical B error. Join its bounded root neighborhood and H-discrepancy neighborhood to the two trace copies using fixed connectors.

Any selected witness used for Gibbs deletion must be closed under **entire original-run augmented trace components**, not just the forward-influence/ancestor skeleton. Its original occupied physical leaves tau are then a removable valid coboundary by the proof above. The root/fault additions and two-run indexing produce only bounded additive leaf losses and constant entropy changes if the full-trace theorem's original-component closure bound holds.

Selected dual input mass is at most c_F times selected physical input mass, with c_F the column weight of F^2. The linear prepass has size O(physical mass). Hence the full augmented animal remains O(physical mass), with constants degraded. Physical single-fault neighborhoods remain bounded. The logical-jump identity from RESULT.md and the column bound of G preserve height/distance support estimates up to constants.

IMPORTANT: a bound for an ancestor skeleton alone does not show that its closure under complete original trace components has O(skeleton mass). Use the complete-trace theorem with mass measured by all occupied leaves after closure, and re-establish its contraction/height estimates there. This is the precise joint interface to the full-trace author.

## Native Gibbs ratio endpoint

For a fixed removable original physical occupied set T=tau with tau in im d_A, deletion s -> s+tau is injective on syndromes containing T. Under an additive nonnegative excitation energy E(s)=sum_j J_j s_j with J_j>=J_min>0, the energy decreases by exactly sum_{j in T}J_j. Therefore

Pr(T subset supp(s)) <= exp(-beta sum_{j in T}J_j)

for this **valid removable** fixed T. More generally use the explicitly assumed Gibbs energy-drop inequality and deletion injection of the native thermal theorem. Combine this bound with counting augmented removable witnesses. No general local-stochastic property is required.

This does not apply automatically to arbitrary noncommuting Hamiltonians, nonadditive syndrome energies, frustrated affine syndrome sectors, or unsupported bath dynamics. The thermal theorem's actual hypotheses remain necessary.

## Outcome

Uniform local duality transfers a certified full-trace removable-witness theorem to physical A syndromes, with constant losses, once the listed deletion/terminal/entropy hypotheses are met. Whole-component nonlinear decisions are permitted. Neither lifetime equality nor bounded-radius nonlinear gates nor an unearned all-subsets Gibbs inclusion inequality is asserted.

## Matched interface with the abstract full-trace theorem

The companion `producer-workspace/FULL_TRACE_REMOVABLE_EXTENSION.md` supplies precisely this interface as F1–F4: deletion-stable component stencils, complete nonzero residual operands, no recursive zero activation, and a fixed finite terminal bag. Add the bottom residual rows `u+F^2 s=0` to its F2 certificate. Activate them only from occupied physical inputs or already charged computed operands. This is one constant-cost noncontracting bottom layer; its charge comparison is `|u_C|<=c_F|tau|`. No modification to its nonlinear component-choice rule is required. Its selected-union estimates then imply the augmented bound with constants depending on F and H. The stated G-postpass caution is compatible with its separate lifted-support accounting.
