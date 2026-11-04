# Scalable output-only acquisition from interacting many-body sources

The supplied construction recovers one arbitrary, initially unencoded quantum register, including its correlations with an external reference, from specified coherently delivered output fields while a known local Hamiltonian continues to act. The complete [proof report](package/Astra_P1_Scalable_Many_Body_Acquisition.pdf), [editable proof](package/Astra_P1_Scalable_Many_Body_Acquisition.tex), [independent construction](package/construction/continuous_hamiltonian_reverse_reset_decoder.txt), and [completed mathematical/interface audit](package/construction/continuous_hamiltonian_interface_audit.txt) are supplied. This is a constructive theorem in its calibrated Markov/control model. Hardware validation, historical priority and competitive economics are not established.

| Result | Direct route |
|---|---|
| General continuous local Hamiltonian with export margin | This page and the complete proofs above |
| Finite acquisition of the actual output, recycling and resource costs | [Interface and resource result](finite-interface.md) |
| Exact ideal acquisition for known product-basis diagonal interactions at every positive export rate | [Separate diagonal result](diagonal-decoder.md) |
| Original package and complete captured return | [Original ZIP](original/Astra_P1_Scalable_Many_Body_Acquisition_Package.zip), [visible return](P1_SCALABLE_MANY_BODY_ACQUISITION_20261105_RETURN.txt), [provenance and hashes](SOURCES.json) |

## Model and quantified guarantee

There are `n` source sites of fixed local dimension `q`, arbitrary initial state `rho_SR`, and a known static `k`-local Hamiltonian `H=sum_X h_X`, with explicit local matrices, supports, precision and norm scales. The ports are **actual calibrated pure-vacuum nonidentity Weyl ports** `L_i,mu=sqrt(r) W_i,mu/q`, all coherently and losslessly delivered to the receiver. A reduced depolarizing generator alone does not grant this interface. The physical photon rate is `c=r(1-q^-2)` per site; the synthetic reset rate is `r`.

Define `osc(h)=lambda_max(h)-lambda_min(h)`, `beta=max_i sum_(X contains i)(|X|-1)osc(h_X)`, `chi=max_i sum_(X contains i)osc(h_X)`, and `kappa=r-beta`. For `kappa>0`, the explicit ideal acquired channel followed by its decoder obeys the **full diamond-norm** bound

```text
||Rbar_T-id||_diamond <= 2 sqrt(n exp(-kappa T)).
```

This is uniform over arbitrary input/reference states, including a retained input-independent classical record. At fixed positive margin, collection time is logarithmic in `n/epsilon`; the mean number of exported qudits is `nrT`. One unknown input is consumed. There is no fresh-input retry, source-side exchange, uncharged source intervention or receiver access to the surviving source. A time-dependent extension needs an efficiently computable Hamiltonian description and a paid finite simulation budget.

## Acquired instrument, physical decoder and proof

The finite local collector captures each noise-only comparison bin's canonical environment at dimension `q`, followed by a fixed-dimensional Kraus isometry. A synthetic flag has probability `p=1-exp(-r Delta)` independent of the input. On a flagged event the old state, with all its correlations, is exported into `B` while the source is replaced by `I/q`; otherwise it is unchanged. The payload label is not measured. These are acquired Kraus flags, rather than assumed photon records.

Conditioned on the known reset history `gamma`, the acquired channel has the mathematical representation `C_gamma(rho)=Tr_S U_gamma(rho tensor I_B/b)U_gamma^dagger`, where `b=q^M`. The receiver prepares a maximally mixed dummy source, reverses the known Hamiltonian/reset history on receiver registers, and returns the dummy:

```text
D_gamma(sigma)=Tr_B U_gamma^dagger(I_S/d tensor sigma)U_gamma,
d=q^n.
```

This is trace preserving; its Petz factor `(b/d) C_gamma^dagger` is not a postselection probability. It reverses neither the field nor the actual source.

In normalized operator Hilbert space, `J_gamma(X)=U_gamma(X tensor I)U_gamma^dagger` is an isometry, `P0` projects onto source-identity operators, and `D_gamma C_gamma=J_gamma^dagger P0 J_gamma`. Its residual quadratic form is exactly the squared source-dependent operator component. With `W=sum_i Q_i` counting nonidentity source support, resets remove support at rate `r`, while a local Hamiltonian term grows it by at most `(|X|-1)osc(h_X)`. Consequently the averaged residual obeys `0 <= I-Rbar_T <= min(1,n exp(-kappa T)) I` in **operator-space order**. This does not assert that `id-Rbar_T` is a completely positive physical map. The bound tensors with an arbitrary reference's operator space and gives pure-state fidelity, then the stated dimension-free diamond bound. No generic Choi-to-diamond dimension factor is inserted.

The construction thus provides an acquired quantum register usable in any subsequent finite quantum procedure, with additive acquisition error and the specified overhead. It does not reconstruct every correlation in the discarded output bath.

## Observable record certificate

A separate computable positive-vector bound starts with `v_i=1`, evolves `dot v_i=sum_(X contains i,|X|>=2)osc(h_X) sum_(j in X)v_j`, and sets `v_i=0` on its reset. Values may safely be clamped to one. Each **ideal** acquired record certifies `||D_gamma C_gamma-id||_diamond <= 2 sqrt(min(1,sum_i v_i))`.

For `beta_cert=max_j sum_(X contains j,|X|>=2)|X|osc(h_X)` and `kappa_cert=r-beta_cert>0`, hitting `sum_i v_i<=a` has tail at most `min(1,(n/a)exp(-kappa_cert t))` and mean at most `(log(n/a)+1)/kappa_cert`. Certified upper rounding or interval arithmetic is paid. This certificate uses a stronger sufficient margin than the fixed-time theorem. Unconditional finite-collector error does not give the same bound on every rare conditioned record: conditional accuracy must pay its actual success probability. Earlier prefix identification after deferred readout does not shorten elapsed collection time.

## Costs, comparisons and preserved limits

The [finite-interface result](finite-interface.md) supplies a full source-plus-output comparison, constant-dimensional chronological collectors, finite strength/slew/calibration, two-bank recycling, queue tails, readout/reset deadlines, local inverse simulation and waiting costs. At fixed local scales and positive gap, reusable protected quantum memory is `O(n log(n/epsilon))`; the sufficient total physical control work can be a very large polynomial. This is not a fixed-bandwidth asymptotic device.

If direct parallel source SWAP is supplied, that is a simpler ordinary baseline. Without interactions, ordinary first-reset collection already gives logarithmic waiting, with exact full diamond error `2{1-[1-(1-q^-2)exp(-rT)]^n}`. Petz/inverse-dilation recovery, operator-size methods, percolation and ordinary circuit inversion are credited prior machinery. Globally applying the inherited N1732 collector needs `d^2` levels, only `2n log(q)` qubits, but dense synthesis can be exponential; the present gain concerns executable local controls, not a mistaken exponential qubit count. Optimality over all coherent decoders is not established.

Known-model mismatch costs at most `2 integral ||H-Hhat|| dt`. Additional inaccessible noise costs `T nu_hid`; independent hidden `lambda D[Z_i]` terms give `nu_hid<=2n lambda`. Fixed hidden noise is not thereby harmless at increasing register size. Loss, memory, calibration, phase labels and precision remain charged. General noncommuting weak-export dynamics are unresolved. The [diagonal theorem](diagonal-decoder.md) shows that `r>beta` is sufficient rather than universal.

## Supplied audit and finite evidence

The package contains substantive completed [independent normalization/support/interface audit](package/construction/continuous_hamiltonian_interface_audit.txt) and [global-history/recycling audit](package/construction/global_history_and_recycling_audit.txt). They retain their stated mathematical/control-model scope. No new Capital reproof or scientific execution is performed here.

The [recorded finite-matrix checks](package/verification/reverse_reset_verification.json) and [original program](package/verification/verify_reverse_reset.py) cover decoder/projection and adjoint identities, a support Lyapunov inequality, and positive trace-preserving Choi maps for a two-qubit model. Reported identity errors are below `6e-16`. For `H=XX+0.37 ZI+0.23 IZ`, `r=6`, `beta=2`, `kappa=4`, the recorded Hilbert-Schmidt residuals at times `0.2,0.5,1,2` are approximately `0.517357,0.110668,0.007699,0.00003103`, below `2 exp(-4T)`. They are floating-point diagnostics, not formal certificates, measured hardware error or independently computed diamond norms. No source code or LaTeX build was rerun.

The earlier weak-control theorem keeps its summed-term and full-retained-instrument scope; its source has inaccessible Z noise. The [earlier digital decoder](../2026-11-05-p1-experimental-access/results/causal-reset-decoder.md) and [mixed-output companion](../2026-11-05-p1-experimental-access/results/expander-mixed-output-memory.md) retain their premises. Pure accessible ports and initial-payload recovery do not remove the whole mixed-output storage obstruction with unavailable purifiers. The previous package and companion texts are preserved byte-for-byte under `package/preserved/`.

The files and this result page are directly available on GitHub. Generated current retrieval has not been rebuilt for this return; the resource-limited local build remains stopped.
