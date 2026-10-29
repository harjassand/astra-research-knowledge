# Actual syndrome records select the order of logical channel error

Author `/root`, 29 October 2026 Australia/Brisbane. Authored bridge; independent review is separate. This replaces a hard sparse-fault promise by weak completed interactions at every memory interval. It is not a circuit-level fault-tolerance threshold.

## 1. Operation and completed noise

Use the L-pair erasure operation and source code of `exposure_code/CODED_CAUSAL_ERASURE.md`. H has no nonzero kernel word of quaternary block weight <=2t. The actual decoder measures s and applies Z^{e_s}, H e_s=s. For s=He with weight(e)<=t choose e_s=e; this is unique. Complete other lookup entries arbitrarily. Retain the whole actual syndrome and receiver record.

At completed interval j, remove only bath-only baseline evolution and write its dilation as baseline plus F_j, norm(F_j)<=eta_j. Coefficients may act on a persistent noncommuting bath initially correlated with source/field, subject to the reviewed locality/control boundary. A returning bath is additional physical cut memory.

Expand the circuit isometry before source-syndrome measurement as W=sum_J W_J over faulty interval subsets. Norm(W_J)<=a_J=product_(j in J) eta_j, and W_J has source phase support in J. This is an exact finite expansion without stochastic independence or a sum of Pauli-coefficient norms.

Let Phi be the actual CPTP map from logical input and common field/bath E to logical output and O, including all actual records. Define

\[
\mathcal R_{\rm mix}(\sigma)=\operatorname{Tr}_{\rm logical}\Phi(I_K/K\otimes\sigma). \tag{1}
\]

R_mix is CPTP and retains the actual record interface. Its law need not equal an old unencoded common-receiver baseline. This specifies a comparison instrument; the real protocol need not perform another logical measurement or randomization.

## 2. Exact channel-level cancellation

Let T_(J,Q) be the cross map obtained by sending W_J rho W_Q^dagger through the actual syndrome measurement, recovery and decoder. It need not be CP, but its diamond norm is at most a_J a_Q. Put R_(J,Q)(sigma)=Tr_logical T_(J,Q)(I_K/K tensor sigma); its norm is also at most a_J a_Q. The sums are Phi and R_mix.

For design order d=2t+1,

\[
T_{J,Q}=\operatorname{id}_{\rm logical}\otimes R_{J,Q}
\quad\text{if }|J|+|Q|<d. \tag{2}
\]

To prove this, expand only to identify phase characters, not to bound coefficient norms. A cross term has e supported in J and f supported in Q. Actual syndrome measurement kills it unless He=Hf. If e differs from f, e+f is a nonzero kernel word of weight <d, impossible. Hence e=f. Its weight is at most min(|J|,|Q|)<=t, so its chosen recovery acts identically on the logical source. All bath coefficients and receiver records remain intact. Sum these identities. No cancellation between discarded receiver records is needed.

The declared order is 2t+1. Extra actual code distance does not automatically improve it unless the decoder corrects the larger radius.

## 3. A normalized complete-channel bound

The operation projection P(T)=id_logical tensor Tr_logical T(I_K/K tensor .) is diamond-norm contractive: preparation of a maximally mixed input and tracing an output are CPTP, while tensoring the spectator identity preserves the diamond norm. P(Phi)=id tensor R_mix is CPTP, even when the original source and bath may be correlated. Subtract this projection, use (2), and bound each remaining cross term by 2 a_J a_Q. Therefore

\[
\epsilon:=\tfrac12\|\Phi-\operatorname{id}\otimes\mathcal R_{\rm mix}\|_\diamond
\le\min\left(1,\sum_{|J|+|Q|\ge2t+1}a_Ja_Q\right). \tag{3}
\]

The sum is the coefficient tail of degrees >=2t+1 in

\[
P(z)=\prod_{j=1}^L(1+\eta_jz)^2. \tag{4}
\]

For all eta_j<=eta it is at most sum_(m=2t+1)^(2L) binomial(2L,m) eta^m; for any z>=1 it is at most z^[-(2t+1)] P(z).

The generic polar amplitude-tail lemma gives order t+1. Here the actual measured syndrome removes low-total-degree channel cross terms and gives order 2t+1 with the explicit normalized R_mix. Neither bound is an exact operation error. Marginal Pauli twirls or measured infidelity do not supply the eta_j assumptions. Rare conditional syndromes can still be bad; (3) keeps their actual probabilities and output records.

## 4. Noise at every interval and a robust operation separation

For L divisible by16 the reviewed code existence result gives k>=5L/4, t=L/16, and kernel block distance at least 2t+1. Suppose every complete memory interval has eta_j<=1/128. Set z=8 in (4), with d=L/8+1. No hard sparse-fault promise is now needed:

\[
\epsilon_{\rm quantum}\le\frac18\left[\frac{(17/16)^{16}}8\right]^{L/8}. \tag{5}
\]

The bracket is below one by the exact integer inequality 17^16<8*16^16. The fully coded classical-at-gaps converse still gives

\[
\epsilon_{\rm classical}\ge1-2^{-L/4}. \tag{6}
\]

The receiver uses one controlled qubit at the gaps. The total-one-qubit subclass has no returning fault bath; the theorem also tolerates a persistent adversarial bath when its physical quantum memory is counted. The converse must not set a cut dimension to two while ignoring a returning bath. A worst-case guarantee over the noise family includes its no-return/no-noise instance; an unknown adversarial bath is not an acquired extra resource for the classical strategy.

This is a complete-operation separation under weak completed interactions at every interval. The allowance 1/128 is a convenient conservative sufficient interaction norm, not a measured fault probability, necessary limit, optimized threshold or total device threshold. Source preparation/storage, capture, contacts, analyzer, syndrome and decoding operations remain ideal or separately bounded. At extensive t, code search and decoding may be expensive and checks dense. It is not an advantage over conventional fault-tolerant quantum computing.

## 5. Strong prior constructions

Distance-order suppression of coherent logical errors is known. Huang, Doherty and Flammia [1805.08227](https://arxiv.org/abs/1805.08227), Theorem1 and proof, establish logical diamond suppression by code distance for independent single-qubit unitary errors with ideal correction. The related same-syndrome weight argument is used here. Our scoped bridge retains arbitrary persistent-bath operator coefficients and the complete record and supplies a positive normalized common instrument for this causal task. No historical priority is claimed for coherent error suppression.

Han et al. [2609.20537v1](https://arxiv.org/html/2609.20537v1), SectionsII-III, supplies a strong current qLDPC comparator: code-capacity results for fixed-depth bounded-support coherent circuits and local CPTP noise, with perfect syndrome measurements, using cluster resummation. Their efficient-decoder and noisy-syndrome frontiers remain explicit. That result is not silently applied to an arbitrary persistent global fault bath. Those settings, statements and proof sketch were read, not the full appendices. PDF/abstract retrieval failed locally; official HTML supplied the passages.

Knill–Laflamme–Viola's general-noise grading and Astra N1063's completed-access warning are further ancestry. This tranche contributes the causal receiver/source-code bridge, normalized full-record metric, robust coded comparison and schedule-sensitive architecture, not a new QEC theory from scratch.

## 6. Executable challenge

`channel_order_checks.py/json` verifies low-degree phase-pair cancellation independently of field state and constructs a persistent noncommuting-bath example using the actual code, with source syndrome retained. Exact finite arithmetic tests the construction; it does not replace the all-input norm proof or infer a physical noise rate. The earlier generic tail example distinguishes Pauli weight from identity-plus-F degree; this theorem uses the latter.

## 7. General causal exposure spaces

The channel-order argument also applies beyond disjoint Bell-pair blocks. At fault location j take W_j=Im(chi_j)=Im(B_j), or a specified subspace from the actual exposed memory site. Define E_t as the union, over |J|<=t, of sum_(j in J) W_j. Since each W_j is a binary subspace, E_p+E_q=E_(p+q), up to saturation at the number of locations. If H separates E_t then ker(H) intersects E_(2t) only at zero. A cross term with characters e supported at J and f at Q, equal syndrome and |J|+|Q|<=2t, consequently has e=f. That common character lies in E_min(|J|,|Q|) and is corrected. The same normalized channel bound follows, even for dense source-error patterns and coherent duplicate fault paths.

This uses fixed acquired frames and completed location interfaces. Splitting a full-register fault into local sites requires a physical locality/control contract. For finite E_t a separating phase code exists when 2^b>|E_(2t)|-1 by the binary-check union bound. Gate compatibility and source syndrome costs are still separate. Only the Bell family inherits the stated classical-capacity converse.

All whole-call comparison and reuse claims assume external interventions occur between completed calls. Internal feedback is included in the fixed causal circuit. Arbitrary outside interventions among internal records/arrivals require a separate causal/comb contract.
