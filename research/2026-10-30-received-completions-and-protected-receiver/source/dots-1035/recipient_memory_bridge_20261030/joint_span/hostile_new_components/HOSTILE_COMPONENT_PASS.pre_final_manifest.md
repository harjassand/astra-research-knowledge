# Hostile independent pass on the NEW carrier/activation/split components
2026-10-30. Scoped component check requested by the constructing parent. I authored the separate signed-Bell joint module, so this note **does not re-review that module and is not whole-recipient acceptance**. It audits the following new sources I did not author:

- `FINITE_RAW_MASK_CARRIER.md`, SHA-256 `19048c8154fadd37c2958a23b8dcacf883878e051907ffde358da6697c9b45a6`.
- `FINITE_NATIVE_ACTIVATION_AND_WARM_CHANNEL_V2.md`, SHA-256 `40c4993d0226fa7b303b005d327f4b02a3ad4c90da4d29a861399456b48fdfa2`.
- `EXACT_ENDPOINT_GKLS_SPLIT.md`, SHA-256 `a7ab0a03f4ce799af3ca56b2bbb23b6957f3467efcd6c259671118355a97bc66`.

Exact copies are preserved here. **No substantive counterexample found** under the stated actual hardware/regularity and inherited theorem inputs. The two precision points in Section 6 below should govern the reading.

## 1. WAIT is not truth, and the source actually separates them
The exact pointer adjoint identities follow from sum_b Pi_b=I, so the WAIT algebra closes independently of the DATA state, physical outcomes or bath correlations. Classical COPY maps give L*W_1=nu(OR(W_Q,W_A)-W_1) and L*W_j=nu(W_(j-1)-W_j). With b_j=2^(L-j) and a=2nu b_1/kappa, the coefficients are at most -kappa a/2 on pointer WAIT, -nu b_j/2 on internal carrier WAIT and -nu b_L on the terminal WAIT. Thus L*R<=-min(kappa,nu)R/2 exactly, including coherent label inputs.

This says nothing about a stale non-WAIT value. The actual source repairs that gap: pointer/COPY dynamics are OFF during finite reset-to-WAIT hold/fall; reset coefficients reach zero BEFORE CNOT; pointer/COPY turn on only afterward. Outside the analytically charged boot/fault set, every non-WAIT value is therefore causally descended from the correct physical pointer outcome. COPY continuing during the finite Pauli pulse cannot change a clean completed latch, because all predecessors on that column carry the same fixed p. A fault or boot defect may corrupt an entire private column path, but not an unbounded set of other columns. This requires exactly the declared private fixed-length paths and bounded site load/parallel bandwidth.

Hermitian I,X,Y,Z representatives make the physical finite pulse valid. No real anti-Hermitian XZ is substituted into H=pi(I-P)/(2tau).

## 2. The correlated-outcome moment is genuinely unconditional
For M_S=product A_i, nominal drift is <=-r|S|M_S. A local identity-annihilating term meeting K subset S satisfies N_Z*M_S<=||N_Z*|| M_(S\K), since 0<=product_(i in K) A_i<=I and all remaining factors commute the local joint map. Terms disjoint from S vanish. Summing the actual incident norm budget gives at most eta_ep |S| times the lower-degree majorants.

Induction with p'=-rp+eta_ep p^(1-q), p(0)=1, gives m_S<=p^|S| and the displayed p^q law. This remains a valid upper bound when |S|<q. The conversion A_i>=a0 B_i and subset union then bound the number of unfinished columns. No Bell branch is normalized and no independence of physical outcomes from noise is used. The old DATA bundles annihilate these WAIT observables, although they are still charged for quantum correctness elsewhere.

## 3. Every old DATA bundle is removed from the nominal endpoint
The accepted atomic apparatus is built from complete attempt channels ell(Phi-id). Removing the entire Alice worker bundle removes its READ branch as well as SYNC/disabled branches and the complete loss term. Removing the entire Bob current-read/correct bundle removes every old correction. The remainder consists of classical queue/watchdog/auxiliary channels and is CPTP and DATA-independent. It is allowed to stall in this analytical nominal process; fresh mask delivery uses a different apparatus.

An old auxiliary register may remain entangled with DATA, and resetting it may steer conditional coefficient states. Nevertheless its operator acts as DATA identity and preserves the DATA-error module. It cannot create a further physical DATA action without a subsequent insertion of a removed READ/commit bundle. Thus no hidden fast old DATA map remains nominal. This conclusion would fail for a native-old apparatus with strong coherent payload prefixes; the source correctly excludes that scope.

The forward split also includes every weak first-edge Hamiltonian and all endpoint deviations. The nominal base remains CP on every interval. The norm tail is bounded before finite-system support expansion; no positivity of the signed truncation or inverse dissipative map is needed.

## 4. Strong ready support survives the actual finite activation
I checked the exact ready predicate against `ONSITE_ABORT_BUSY_WITNESS.md`: A0, workspace zero, and no own o_h/z_h tag, with monitor states unrestricted. It is the same predicate used here. With first initiation removed, every actual Hamiltonian preserves it and every resolved reset is noncreating. Other owners can change only their own tag labels and private workspace, so malformed sectors of other owners do not invalidate this statement. Label-preserving monitors are harmless. The boot mode retains only onsite resets and those monitors, as needed for its backwards-reset product test.

Hence the joint Q_S ready subspace is invariant. On it, a C DATA payload outside S has zero source; all other physical jumps are DATA identity. A nominal Kraus coefficient therefore acts on DATA only within D(S), despite arbitrary coherent malformed states inside S. A local insertion changes at most the bounded set of ready tests meeting its physical support and can act directly only on its finite DATA support. Global bath correlations do not alter this finite SYSTEM support statement.

The final forest acts only in C/R(C) of these same busy owners, preserves their ready tests, and has DATA support already contained in D(S). Its support is not an additional extensive copy of D(S). Coherent S,S' blocks are treated on ket and bra separately; the argument does not union all possible masks.

## 5. Positive warm entry and the future ordinary decoder
Primitive boot and carrier compressions act on auxiliary registers and have actual positive/gentle estimates. The signed low-order comparison has bounded DATA support and busy-owner support. The raw radius, energy and strong BUSY tests commute in the chosen forest frame, so their joint P_small is legitimate. Since the signed comparison is supported there, actual outside mass is at most the diamond comparison error. A final positive gentle compression followed by the stated positive ancillary extraction gives an earned warm channel, not an arbitrary dirty restart.

The raw energy bound supplies an extensive exponential moment exp([g+sE_0]N). It is correctly required to have a fixed coefficient gap below the warm barrier; no O(N) moment is inferred merely from correctable weight. The uniform small-epsilon margin can be selected before endpoint durations, since the fast/first-OFF BUSY constants are independent of epsilon, g and q_t tend to zero, and the fixed raw energy barrier stays positive. Choosing epsilon, then ell, then old service/noise respects the small integrated endpoint budget without requiring ell*T_old_service small.

At later requested times, the full-state singleton drift gives a pointwise sparse BUSY tail from the small warm BUSY bound. Combining it with the native killed canonical radius gives the physical common Pauli span alpha_new+r_D beta_out. The ordinary zero-code DATA recovery corrects this span; no Bell-dependent target inverse or later physical forest inverse is being hidden in the decoder. This remains an ideal decoder used to state the quantum channel, not an actual quantum retrieval circuit.

## 6. Two reported precisions
1. The physical forest commutes the BUSY mask M, but the full-Hilbert G_busy witness may depend on DATA on malformed sectors and need not commute the forest. The needed initialization is nevertheless exactly valid:

       Tr[G_busy F sigma F^dagger]
         <=Tr[e^(2C delta M) F sigma F^dagger]
         =Tr[e^(2C delta M) sigma] <=e^(2C delta bN).

   Use this inequality; do not assert that G_busy itself is unchanged by the frame. It is sufficient for Section 6 and requires no new theorem.

2. The governing V2 manifest correctly names activation hash40c4993d..., whereas the manuscript's trailing dependency line still displayed25f4a6ed... at this read. Use the verified manifest/frozen copies or preserve/refreeze a corrected dependency link. This is version bookkeeping, not an algebraic counterexample.

No whole acceptance is issued here. Joint incoming-module correctness, the signed-Bell contraction and all inherited global/native source theorems remain outside this independent component check.
