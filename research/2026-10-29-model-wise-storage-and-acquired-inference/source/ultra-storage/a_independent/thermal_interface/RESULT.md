# Acquired static quantum-Peierls and growing-support interface

The all-size construction is [STATIC_PEIERLS.md](STATIC_PEIERLS.md), independently whole-reviewed by the existing peer at its stated primary/KP scope. Its final source SHA is `f6d5d8896751a0d74800303d26e06dd670b45ffd2071a874e96208e33d0341f0`. It uses the separately accepted frozen RX/RZ retraction theorem; no new finite level is a premise.

For the published recursive passive-memory family, at a fixed low positive temperature and sufficiently small **arbitrary local coherent Hamiltonian perturbations**, the actual Gibbs state's weight in the primary decoder-bad sector remains stretched exponentially small. The explicit construction is:

* Exact-label interaction-picture Dyson activities factor across check-disconnected components.
* Every surviving component below the code-distance cutoff is a **central stabilizer function**. The small gas is therefore an ordinary scalar polymer problem per syndrome.
* Possibly logical large activities are bounded **relative** to the central small gas; no exponentially small partition function is supplied for free.
* Pauli-coefficient-l1 budgets plus the accepted polynomial check filling pay a uniform effective check-incidence norm. The primary's **valid coboundary witness deletion** then works at a reduced beta.
* A union over all Pauli shifts of one physical region supplies a **common** good projector for every operator on that region. Its probability cost is explicit in the region's qubit count.

Writing q_R for the patch qubit count, the static receiver is

`p_bad(X) <= 4 exp(4delta) exp[q_R(log4+beta(1+2zeta)D)] 2^(-2^(k-1))`.

Here delta is the exponentially small relative logical-polymer correction, and zeta is the explicitly bounded effective check-incidence charge. Thus a sufficiently small constant times `q_R=2^k` is admissible. Bounded-density R3 patches have radius proportional to `2^(k/3)` after paying all constants. This is the input needed to balance a separately qualified exponentially decaying quasilocal jump tail; it does not silently require an O(1)-support generator.

The temperature and perturbation domain is nonempty and size-independent, although conservative. For example set `zeta_*=(1-beta_c/beta)/4>0`, and choose

`B_* = min{1/[2(Delta+2)], 1/2, beta*zeta_*/[2e C_geo (3p)!]}`.

Then the sufficient Pauli-l1 input bound

`v <= exp(-beta Dq)/beta * log[1+B_*/((Delta+1)^2 e^2)]`

pays both KP convergence and zeta<=zeta_*. The operator-norm version loses the stated factor 2^q. These formulas are theoretical sufficient parameters, not a useful laboratory threshold or a numerical qualification of the source's enormous embedding constants.

The separate **root_quantum_receiver** construction owns approximate logical twirling, the exact CPTP encoder/decoder and stationary quantum-generator bounds. The separate CKG admission owns an actual already-established exactly Gibbs-stationary quasilocal model. Composition requires those exact generator hypotheses and full-jump tail costs. There is **no** inference that microscopic local couplings give local Davies frequency-resolved jumps, no arbitrary nonstationary-noise theorem, no perturbed two-body-gadget lifetime, no efficient initialization, and no acquired native material/bath.

The same-seed finite matrix consumer is preserved in `polymer_consumer.py` and `POLYMER_EXECUTION.json`. It checks all 16 exact-label subsets for four coherent one-site fields on the 5-qubit seed using ordinary dense binary64 exponentials. Factorization/reconstruction residuals are about 1.3e-14; centrality residual about 6.9e-15; relative full/small norm is 1.53e-10 versus a conservative 4.145e-5 majorant. The full Gibbs/twirled trace distance is 1.34e-5, explicitly demonstrating that the full state was not replaced by its twirl. This is a finite diagnostic, not interval-certified evidence of a storage lifetime or primary beta_c admission.

No practical or historical-priority advantage is claimed. Ordinary scalar KP, stabilizer algebra, the primary witness construction and the ordinary quantum thermalizer remain credited inputs. No physical operation or external write occurred.
