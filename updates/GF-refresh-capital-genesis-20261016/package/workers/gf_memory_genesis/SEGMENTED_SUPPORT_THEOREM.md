# Retained cuts with per-segment propagated error kernels

16 October 2026. New local extension of the supplied support argument, proved here. No new physical boundary is inserted. This is a sufficient algebraic and causal theorem, not a lifetime theorem or a hardware qualification.

## 1. Typed contract

Let S be a commuting Pauli stabilizer code group with no -I, encoding isometry V:L->M, and a persistent finite bath B. A reference R and arbitrary initial L-B-R entanglement are permitted. The probability/effect statement below is stronger in its input domain: it allows arbitrary physical M-B-R inputs.

Fix an exogenous finite schedule. Each clean parent is bounded by its genuine entering instrument/correction and actual completion instrument. Refine its weak part by **actual** intermediate complete syndrome cuts. For segment c, denote its entering/exiting projectors by P_(c,r),P_(c,t) for a commuting G_c subset S. Same-G neighboring segments may share a single actual cut and its classical/latent label. A different G requires the actual corresponding instrument, not a retrospective change of labels. Trusted intended Pauli correction occurs at its actual prescribed start; it is not moved through the weak interval.

An unread cut is allowed only when the complete full-joint channel is the stipulated pinching, with fresh isolated discarded environment and no future use/return. Its canonical environment labels are complete actual-channel Kraus labels. They need not be controller readouts. A finite-rate dephaser is not an exact cut; a genuine complete-pinch mixture component may be used on that component, with every failure branch charged as required by the source.

At every physical time, concurrent selected clean reservations are disjoint on ALL memory, check, detector, controller and reset resources. Sharing B is unrestricted. Every operation touching another active reservation is either part of its specified interface or a conflict. Other active parents and bath dynamics commute with c's memory checks because their full memory supports are disjoint. Parent selection, cut times, geometry and action envelopes are independent of selected private node environments and are fixed under the interpolation used for effect bounds.

For every actual Kraus/environment record, each segment's memory-error factors admit a Pauli expansion in a subgroup H_c of the phase-quotiented Pauli group. H_c must contain all products created within that segment, including actual noisy pulse, controller, reset and refresh effects after propagation through all intended controls. Exact admitted stabilizer-algebra factors may be larger than H_c. Sufficiently, choose H_c=Pauli(C_c) for the full propagated error region C_c. Reserving D_c containing C_c does not itself prove correctability.

Assume the segment kernel condition

`H_c intersect Centralizer(G_c) subset phase times S`.                 (S1)

If errors are arbitrary on C_c, (S1) must hold for all Pauli(C_c). Checking only elementary detectable terms is insufficient. Restricting H_c is legitimate only with an actual restricted error contract stable under multiplication/propagation.

Between the segment's real endpoint cuts, the intended baseline is the correction-first source baseline: admitted exact stabilizer-algebra interventions and disjoint operations. A larger circuit can enter only after proving the stated propagated module representation relative to its intended action. This theorem does not freely commute a non-Pauli gate through an error.

## 2. Fixed-record support proof

Fix the entire schedule, every genuine classical record, and every actual environment/Kraus index, WITHOUT normalizing any branch. Expand every weak/noisy segment factor in memory Paulis and bath operators. For a finite circuit this is exact. Bounded integrable Hamiltonian evolution follows by finite circuit approximation and norm limits.

On an encoded Pauli orbit E V, each code stabilizer g acts as a scalar chi_E(g), independent of the logical vector. Any exact stabilizer-algebra Kraus factor is therefore scalar or zero. This includes projectors, Schur Gram factors, and the actual partial-pinch remainders in the supplied boundary theorem. Merely commuting with G is not enough: a logical unitary may commute while acting nontrivially on L.

Within a segment, commute ONLY memory Pauli factors past operations on disjoint concurrent reservations. Do not interchange bath coefficients, even when parent intervals cross. In each expanded word its bath product remains in precisely its original order. The net memory word E_c belongs to H_c and to Pauli(C_c) in the region version.

The Pauli-sector identity is

`P_t E_c P_r = 0 unless syndrome_(G_c)(E_c)=t xor r`.       (S2)

It holds because E_c commutes or anticommutes with each measured stabilizer. The actual endpoint projections force (S2) termwise, including words with internal return paths. Intermediate stabilizer factors only add scalar selection constraints.

For each realized difference d choose one E_(c,d) in H_c with that syndrome, setting E_(c,0)=I. Any two compatible words E,E' have E E'^dagger in H_c intersect Centralizer(G_c), and hence differ by a code stabilizer and phase under (S1). On every incoming Pauli orbit, replace E_c by E_(c,d) and absorb that stabilizer's scalar into the chronological bath/auxiliary coefficient. No sum of absolute Pauli coefficients appears.

Thus a segment with t=r adds zero support; a segment with t!=r contributes one representative supported on C_c at its **actual segment exit time**. This is an equality on encoded Pauli histories, not a stochastic Pauli-mixture representation.

Apply this construction in chronological order through the full record. At a real retained cut, the next segment acquires its own actual entering sector. A temporary excursion inside a previous segment has no effect on the next kernel test after the representative replacement. Products of good segment words are stabilizers on every orbit, even if the union of their possible physical error regions supports a logical operator. The required statement is (S1) for each cut-to-cut word family, not a single test on their union.

Bad/dirty parents and unfinished segments stay charged over their stipulated support at their actual times. A missing terminal cut is never inserted at final readout. If the original receiving proof uses parent rather than segment completion births, either charge each bad parent on its entire bounded reservation or separately check that the segment birth schedule satisfies the receiving geometry; the local proof alone does not choose this geometry.

## 3. Actual good CP subchannel and common decoder

Let K_alpha be the COMPLETE actual-channel Kraus family, with all actual/latent cut labels in alpha. Select an input-independent record/schedule predicate Good. Require one fixed total decoder D such that EVERY representative Pauli history admitted by Good is decoded to a code stabilizer, with the same rule for all coherent summands and bath inputs. This is the universal support-history decoder premise; correcting each history with a separately chosen decoder is insufficient.

Set `Phi_good(X)=sum_(alpha in Good) K_alpha X K_alpha^dagger`. This map is CP TNI and its complement in the actual channel is CP. After encoding and the fixed decoder, the preceding support argument makes each decoded Kraus operator identity on L times an auxiliary/bath operator. Thus

`Psi_good = Id_L tensor Lambda_good`,

where Lambda_good is CP TNI. This holds for joint encoded logical-bath-reference inputs and uses no observation of latent labels. It remains true when good records include leave-and-return words inside a segment that satisfies (S1).

For completeness, suppose the full-input bad-effect bound is delta I. Write Lambda_good^*(I)=A. Total trace preservation gives bad effect `I_L tensor (I-A)`, so 0<=I-A<=delta I_B. Choose a fixed auxiliary output state sigma and let

`Lambda_fill(X)=Tr[(I-A)X] sigma`.

Then Lambda=Lambda_good+Lambda_fill is CPTP and

`||Psi_actual - Id_L tensor Lambda||_diamond <= 2 delta`.     (S3)

Indeed the difference is the difference of two CP maps with effects at most delta I; each has diamond norm at most delta. This handles bath-dependent good weight and arbitrary L-B entanglement. It does not pretend that every joint channel has a scalar (1-delta)Id mixture. If only the logical output is retained, trace out the auxiliary system afterward.

## 4. Why segment tester products survive reuse

Assume each ideal segment has the supplied independent causal tester implementation with singleton endpoint value f_c, uniform on its own actual entering label and bath/reference. Examples are the one-gap sine value and the supplied one-node full-sector or general-Schur value. A nontranslation-invariant kernel uses max_r f_c(r), not an average over correlated generated r labels.

Preallocate all private tester bits good, but keep all physical data and B initially prover-side. A dormant tester makes no rotations and accepts at no time. At c's actual entry, perform the genuine sector instrument/correction on prover-side data and store the genuine r. In that r branch, embed physical sector r into private bit 0 and an auxiliary sector space. Pad sector dimensions as in the source. This change of coordinates is block diagonal in all other currently active private parities because full reservations are disjoint.

While c is active, split its charged Hamiltonian into own-coarse-odd and own-coarse-even parts. The odd part is other-even by disjointness and has no larger norm. Implement the even controls by copy/prover/uncompute and the odd part by the source contraction decomposition into fixed private X rotations. Preserve every actual node in chronological order; fine-sector label gadgets act diagonally on all coarse parities. Independent reference node reservoirs remain tester-private.

At actual c exit, the real final pinching makes endpoint parity and fine label classical. Record its acceptance decision permanently. Controlled on the classical label, invert the local sector-coordinate embedding on the occupied subspace and return the physical factor to the prover; extend on unused padding arbitrarily. This reconstructs its full conditional state and bath correlations without accessing a now-terminal coherent private bit. Later physical reuse begins only afterward. A new segment starts its own good private bit at its own real entry. A shared exact boundary label may be copied classically to the terminal and entering local records; it is not cloned while coherent.

Consequently the complete physical process is one compatible joint prover strategy against independent testers, even when segments reuse the same physical data or send completed classical outcomes into later fixed controls. Initial bath correlations, old terminal records, and all reused data are prover memory. No normalized outcome conditioning is used.

For each positive local accept operator T_c, source causal duality supplies a normalized causal operator R_c with `T_c <= f_c R_c`. Padding rounds preserves normalization; tensor products of the R_c satisfy the combined partial-trace causal constraints. Thus `tensor_c T_c <= product_c f_c tensor_c R_c`. Pair with the arbitrary joint prover strategy to obtain

`F_R <= product_(c in R) f_c I`                             (S4)

for every selected subset of segment endpoint mismatch flags, uniformly on complete physical input. This is an all-pass product inequality, not an independence assertion about the flags.

For a single parent that accepts on ANY segment mismatch, a no-prior-mismatch history enters the next segment in a definite sector with arbitrary auxiliary state. Its uniform singleton failure bound f_c gives survival at least 1-f_c. Iterate only over own past actual records to obtain a parent singleton value at most

`p_i = 1-product_(c in i)(1-f_c)`.

Treat that whole parent, with segment decisions and retirement/re-entry built in, as one independent tester; the same causal domination gives a product of p_i across parents with disjoint active full reservations. This is not conditioning on another parent's future success. Action-only gaps yield the supplied Q formula.

## 5. Internal imperfections and support are separate

If a segment's actual local slots obey `N_ck <=_CP T_ck + epsilon_ck E_ck` on the full D_c-B boundary, first-fault erasure of c gives the robust value `g_c=min(1,f_c+sum_k epsilon_ck)`. The additive CP-majorant cost equals the full-joint half-diamond distance as proved in the supplied robust packet. Influence locality ensures an erased segment cannot access another active tester's private parity. Patch reuse after its retirement is already arbitrary prover memory for later testers.

This upper comparison supplies the effect version of (S4), with g_c. It does NOT select actual fault Kraus labels. The support proof still needs (S1) for the actual expanded Kraus factors and actual exact endpoints. If those premises hold, noisy non-Schur interior operations may be included. A propagated C_c larger than the weak footprint may fail (S1), and merely being inside D_c does not repair that failure.

Noisy entry/exit instruments need a genuine qualified CP good/fault refinement or a different approximate-QEC argument; closeness alone does not make their reported labels true syndrome projections. If a cut is only an actual skip/complete-pinch mixture, apply this proof on its actual complete components, merge across skipped cuts with the real remainder retained, and retest the enlarged merged H. If that merged kernel is unsafe, charge that branch rather than call its endpoint good. A general Schur node has no invented complete middle cut.

## 6. Strict finite scope gain and its limit

Take the [[4,2,2]] stabilizer code S=<XXXX,ZZZZ>. Let G=S, C_1={1}, C_2={2}, and H_c=Pauli(C_c). Each singleton centralizer is {I}, hence passes (S1). The union contains X_1 X_2, a nontrivial logical commuting with G, hence fails the parent-union condition.

Apply U_1=exp(-i pi X_1/6), the actual complete G pinching, then U_2=exp(-i pi X_2/6), and the actual final G pinching. Initially encode in the zero sector. With c=sqrt(3)/2, s=1/2, the endpoint-zero Kraus operators on the code are

`c^2 I = 3I/4`, `-s^2 L = -L/4`, with L=V^dagger X_1 X_2 V nonidentity.

Thus endpoint-only good records contain the map `(9/16)Id+(1/16)Ad_L`, and are not all correctable by the unchanged zero-support rule. Retaining the middle label and requiring no segment mismatch keeps only `(9/16)Id`. The old ANY mismatch probability is 7/16, endpoint mismatch is 3/8, and the excluded logical return has weight 1/16. The per-segment support theorem has real content beyond the whole-parent sufficient condition.

Removing the actual middle pinching changes the endpoint-zero Kraus operator to `(3I-L)/4`, a rank-one nonidentity Choi ray. It has no positive identity CP minorant. A mathematical cut cannot be added to rescue that channel.

This finite example is neither a toric-code lifetime construction nor a useful circuit advantage. For an asymptotic memory, support radii, full reservations, incidence and timing must remain uniformly bounded, and the actual cut schedule and common decoder must meet their receiving theorem. In particular full arbitrary faults on every qubit of a detector's own check support cannot be certified this way except on a fixed stabilizer factor, as proved in the companion native-interface note.
