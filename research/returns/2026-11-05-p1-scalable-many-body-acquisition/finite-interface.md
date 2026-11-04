# Finite local output acquisition, two-bank recycling and full costs

The [many-body decoder theorem](README.md) requires an acquired quantum instrument. This result constructs it from the **actual continuous pure-vacuum Weyl outputs**, using constant-dimensional collectors rather than a global `q^n` receiver or source-side pulses. Read the [finite local collector construction](package/construction/finite_local_depolarizing_port_collector_note_2026-11-04.md), [completed full-history/recycling audit](package/construction/global_history_and_recycling_audit.txt), [independent interface audit](package/construction/continuous_hamiltonian_interface_audit.txt), and [integrated proof](package/Astra_P1_Scalable_Many_Body_Acquisition.tex).

## Full output comparison

Partition collection time `T` into `K` bins, `Delta=T/K`. Compare the real evolution with noise-only bins followed by exact Hamiltonian bin unitaries. The fictitious kicks are an analysis device; the receiver does not pulse the source. With physical photon rate `R_ph=nr(1-q^-2)` and local `chi=max_i sum_(X contains i)osc(h_X)`, the **entire source-plus-field channel**, with any reference, differs by at most

```text
eta_split <= 2 chi Delta sqrt(R_ph T+(R_ph T)^2).
```

The proof moves a Hamiltonian segment past each local jump within its original bin, costing at most `chi Delta` per event. It squares and integrates over complete orthogonal histories, using the Poisson second moment. The receiver need not measure or retain those histories. A reduced-generator approximation would not suffice. The earlier per-bin triangle estimate is preserved as a valid conservative alternative; the integrated report selects the improved full-history estimate.

## Local collector and finite controls

In each noise-only comparison bin the inherited N1732 collector is applied only at local dimension `q`. Its receiver has `q^2` levels and a local Bell initialization independent of the unknown input. Its guide has eigenvalues `lambda0=[1+(q^2-1)(1-e)exp(-rt)]/q^2` and `lambda1=[1-(1-e)exp(-rt)]/q^2`. For `A_mu=I tensor L_mu`, projectors `P=Phi_q`, `Q=I-P`, its explicit coupling is

```text
C_mu(t)=-[Q A_mu Q
          +sqrt(lambda1/lambda0) P A_mu Q
          +sqrt(lambda0/lambda1) Q A_mu P]^T.
```

Here the local guide commutes in time, so its gauge is identity and receiver Hamiltonian is zero. Finite endpoint completion and the known Kraus isometry yield input-independent reset flags with `p=1-exp(-r Delta)` and coherent payload exports. They are synthetic flags, not physical photon counts.

For allocated local error `eta<=1`, sufficient regularization is `e=eta^2/256`; use a finite mesh `max(1,ceil(88 c^2 q^4 Delta^2/(eta e^2)))` and finite endpoint ramps of duration `min(Delta/4,eta e/(160 c q^2))`. Peak coupling is at most `16 sqrt(r)/eta`; sufficient slew is `O_q(sqrt(r)/(eta Delta)+r^(3/2)/eta^4)` and mesh size `O_q(1+r^2 Delta^2 eta^-5)`. Calibrated phases/labels, coefficient error and any receiver-Hamiltonian error must fit the explicit channel budget. These finite but growing controls do not establish fixed microscopic bandwidth.

## Complete finite allocation and recycling

One sufficient allocation takes `T=kappa^-1 log(400n/epsilon^2)`, `K=max(1,ceil(20 chi T sqrt(nrT+(nrT)^2)/epsilon))`, `B=nK`, and local error `eta=epsilon/(20B)`. Ideal decoding and splitting each cost at most `epsilon/10`; collection plus cycling together cost at most `epsilon/10`. Memory-cap failure, inverse simulation, other gates, protected waiting, calibrated model mismatch and separately bounded loss each have declared additional budgets, with slack. These settings are sufficient rather than optimized.

Two fixed cascaded collector banks per site alternate bins. Their control windows use retarded source time, and the inactive bank's main-field coupling is zero. During the inactive interval, each bank completes the collector, reads its flag, queues any export and reinitializes its local Bell state. Refresh uses isolated ancillas/readout or auxiliary reset ports, not radiation contaminating the main field. The real requirement is

```text
tau_endpoint+tau_queue+tau_readout+tau_refresh <= Delta.
```

Each bank has a separate adjacent queue to handle propagation order and overlapping processing windows. Nearest-neighbour insertion costs `O(m_*)` swaps. A sufficient per-queue capacity is `m_*=ceil((exp(1)-1)rT+log(20n/epsilon))`. A union bound gives ideal overflow probability at most `epsilon/20`; a fixed replacement output costs at most `epsilon/10` in full diamond norm. The physical-vs-ideal front-end error is also included in overflow accounting, rather than assuming actual flags remain exactly binomial. A separate-bank-per-bin implementation is a completed polynomial fallback when recycling deadlines cannot be met; extra banks are charged.

If `g_end` counts all finite endpoint operations, the paid operation rate must be at least order `g_end/Delta`. A unitary gate clock alone does not supply finite readout/refresh latency. Auxiliary pure-reset channels require `Gamma >= (2/tau_refresh)log(2sqrt(2)/eta_refresh)` plus finite Bell preparation. Individual queue-gate precision is `O(eta/(m_*+1))`.

Total protected quantum memory, including dummy source, queues, two collectors per site and ancillary workspace, is `O(n(m_*+1))`, or `O(n log(n/epsilon))` at fixed local scales and positive gap. Sparse records cost `O(nm_* log(nK))` classical bits, but **every `B=nK` flag/interface execution is processed**. At fixed local scales, `B=O(n^2 T^2/epsilon+n)`. The collector's programmed intervals total `O_q(B[1+r^2 Delta^2 eta^-5])`. Small retained memory does not imply small total control work.

## Decoder, precision, waiting and loss

Known local inverse dynamics can use a product formula with `C_H=sum_(a<b)||[h_a,h_b]||` and gate count `O(m[C_H T^2/epsilon_sim+nm_*+1])`, plus at most `2nm_*` reverse swaps. Commuting terms need no product-formula error. Local synthesis, routing and finite-precision gate costs remain paid. Analog replay of `-H` is an alternative only if that receiver interaction is supplied.

Storage covers collection, propagation, endpoint processing and inverse-decoder runtime. For `Q_mem` qudits over wall time `T_wall`, error-generator rate `nu_mem` costs at most `Q_mem T_wall nu_mem`. Fault tolerance can supply protection only with its separately stated overhead. Additional inaccessible source noise costs `T nu_hid`, and integrated Hamiltonian mismatch costs `2 integral ||H-Hhat||dt`.

Uniform field collection efficiency `eta_f` has sufficient loss error at most `2 sqrt(2[1-exp(-R_ph T(1-sqrt(eta_f)))]))`. This requires an increasingly strict loss budget for high-fidelity large-register acquisition; it does not validate a competitive device at fixed loss. The local decomposition's norm scales and `kappa^-1` are actual numerical costs, not logarithmic bit-length or fast-forwarding promises.

The supplied mathematical/interface audits are completed at this scope. No physical prototype, independent hardware benchmark, source-program rerun or new Capital audit was performed. The [exact diagonal result](diagonal-decoder.md) has a separate phase correction and first-export storage reduction; the generic bounds remain sufficient upper bounds. [Original files and hashes](SOURCES.json).
