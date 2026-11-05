# Bell export with a physical classical history regenerator

This is the operational composition of independent encoded Bell refresh and the static-tree classical regenerator. Its purpose is to remove the correlated syndrome environment exposed by ordinary noisy output interfaces. It uses the companion's actual protected logical fan-out and locally stochastic raw-copy interface; it does not turn an ideal classical decoder into a supplied physical primitive.

## Actual operation

For every computational output qubit i, prepare an independent encoded Bell pair A_i B_i. All factories and the B_i waiting/decoding paths have disjoint fault variables. Perform the protected destructive logical Bell measurement on D_i A_i, but **do not apply its logical Pauli correction to B_i**. Instead produce M protected logical copies of each Bell-result bit and descend those copies through the actual noisy bit interfaces. Their raw error pattern is locally stochastic with rate q, up to the charged global protected-circuit error. Raw copies can be correlated with all old data/controller syndromes and with B_i.

Feed each raw bit pool through its fixed ternary noisy-majority tree. Its leaf copies arrive simultaneously; no raw leaf waits for the protected computation. The fresh quantum half B_i continues its independent protected waiting and descent in the unresolved Bell Pauli frame. Predetermine the timings so the tree roots and B_i's final raw output arrive in the same bounded-duration local terminal cell. Use the regenerated two classical bits only for the final raw local Pauli correction. Discard/reset the Bell-result pools and fine internal transcripts.

No old coherent controller interacts with B_i after the Bell resource is prepared. No raw decoded Bell bit fans out into an encoded correction. All final correction faults affect a bounded number of raw physical locations and remain in the endpoint noise channel.

## Theorem

Let the compiled protected prefix, Bell preparation/measurement and pool generation have total diamond discrepancy at most epsilon_act. Let the actual fan-out interfaces provide an LS(q) error pattern relative to each correct logical Bell bit, with arbitrary quantum side information. Let the independent B_i wait/descent map, after fixing its independent resource syndrome marginal, be a one-qubit channel K_i with

\[
\tfrac12\|K_i-\operatorname{id}\|_\diamond\le c p.
\]

These are the endpoint-companion's noisy compiled operations. Its classical-controller faults are not set to zero. Let p_0=max(q,e,v)<=1/100 for the physical tree primitives described in `static_tree_regenerator.md`. With M=3^L raw copies per Bell bit, the actual n-output channel is within half diamond error

\[
\epsilon_{\rm act}/2+2nq(21p_0)^L
\tag{1}
\]

of the intended logical computation followed by a product of explicitly characterized one-qubit Pauli channels. Their nonidentity probabilities are O(p+p_0), independent of output count and holding duration. Terminal physical Pauli-gate noise is included in those channels. Bounds written with full diamond norm acquire the corresponding factor two.

The guarantee includes arbitrary pre-existing quantum references and retained records. It averages over/discards the newly created internal Bell transcript as part of the declared operation. It does not assert an independent channel conditional on every fine internal syndrome or Bell record.

## Proof

At the virtual logical boundary, an independent resource has form

\[
\Phi_{A_LB_L}\otimes\tau_{S_AS_B}.
\]

The destructive Bell instrument on D,A traces both consumed syndrome systems. Before correction its output is

\[
\frac14\sum_{b\in\{0,1\}^2}|b\rangle\langle b|
\otimes E_B\bigl(P_b\rho_{LR}P_b^\dagger\otimes\tau_{S_B}\bigr)E_B^\dagger.
\tag{2}
\]

The logical Pauli label b is uniform. The surviving syndrome marginal is independent of b, the data and old records. This is true even if the old data logical and syndrome systems were correlated: the consumed syndrome is traced, while the new resource was independent. Local B-side waiting/descent commutes with operations on D,A, so its actual time overlap does not change this argument. Across outputs the syndrome marginals are a product and Bell labels are uniform independently, even for entangled logical inputs.

The real controller/pool interface may expose old syndrome correlations in its raw-copy errors. Apply the static-tree coupling jointly with B and the entire old quantum record included as the reference. For each Bell-result bit, replace its tree output by the same logical bit followed by the explicit fresh BSC reference noise r_L. The change is at most q(21p_0)^L in trace distance. The 2n independent reference trees have independent errors; a union bound gives the second term of (1). This replacement removes controller-history correlations without claiming that raw logical bits can be delivered perfectly.

Let e be the two reference bit errors at one terminal cell. Because e is independent of b and B, independent descent followed by the raw correction has channel

\[
\begin{aligned}
\mathcal O_i(\rho)
&=\frac14\sum_b\sum_e w_i(e)
 P_{b\oplus e}^{\dagger}K_i(P_b\rho P_b^\dagger)P_{b\oplus e}\\
&=\mathcal E_i\circ\left[\frac14\sum_b
 \mathcal P_b^{-1}\circ K_i\circ\mathcal P_b\right](\rho).
\end{aligned}
\tag{3}
\]

The bracket is the Pauli twirl of K_i, hence exactly a Pauli channel. The channel E_i is the independent Pauli error produced by the two tree-root BSCs. The final physical correction gates add their independent Pauli noise. All factors are local and independent across i. Thus there is no need for an additional twirl seed or protected pre-Pauli operation: the ordinary Bell byproduct supplies the uniform twirl.

Twirling contracts diamond distance from identity. Each root error is at most 2p_0, so their union probability is at most 4p_0. The terminal gates add O(p). Therefore each total Pauli channel has nonidentity weight O(p+p_0). The proof is a channel hybrid, not conditioning on global success, so it preserves resource independence. This establishes the claimed comparison.

## Costs and the exact boundary of the construction

Choose L=O(log(n/epsilon)) to give a desired total regeneration discrepancy. The tree uses 3^L physical leaf-copy outputs, O(3^L) voter/link operations and L raw-processing clock steps per logical bit. Its raw error floor remains O(p_0); what vanishes with L is dependence on the old syndrome history. The active processor must produce those copies fault-tolerantly and keep B protected during their production. The output-pool cost can dominate ordinary polylogarithmic interface overhead; it must not be hidden as a constant.

The fixed tree can be reused with fresh component faults and new LS pools. It needs no fresh random permutation. Its local voters can be built from the explicit complement-covariant CNOT/CNOT/Toffoli construction or the bounded-size complement twirl, including all noisy gates, idles, measurements and reset. The current deployment model has paid nonlocal links of specified duration/error. The proof does not establish constant-latency arbitrary routing in bounded-density three-dimensional hardware. If links have growing transit time, that changes their error/channel and must be protected and costed before the tree theorem applies.

The indispensable precursor is LS raw fan-out from an encoded classical logical bit. A single raw bit copied many times fails this condition and cannot be rescued by the tree. The endpoint companion must supply the noisy concatenated fan-out/descent proof; neither this theorem nor its coupling replaces that obligation.

The resulting product channel is exactly the input needed by the positive thermal precompensation and noisy-read prefix theorems. The thermal theorem then prepares the syndrome law before the unknown input arrives. This export operation itself makes no claim about the BDL bath, its lifetime, or total physical-resource superiority over ordinary active error correction.
