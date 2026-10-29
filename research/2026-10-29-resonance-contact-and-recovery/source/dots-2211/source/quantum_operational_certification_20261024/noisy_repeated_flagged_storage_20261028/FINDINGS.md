# Repeated physical storage: calculated findings

28 October2026. Deterministic numerical CPTP-channel evaluation; independent review pending. See GOVERNING_MODEL.md for all assumptions. No new acquisition, hardware result, diamond certificate or novel-code claim.

The physical32-dimensional state is reused between rounds. Only the terminal diagnostic is decoded. The inherited acquired inverse is frozen at the pilot-selected4096 shots/site model.

| Coherent EC angle (radians) | Infidelity T32 | Infidelity T128 | T32 code-space weight | T32 naive decoded-round PTM discrepancy |
|---:|---:|---:|---:|---:|
| +0 | 0.01640112 | 0.06349650 | 1.00000000 | 0.00000000 |
| +0.0001 | 0.01639539 | 0.06347420 | 0.99999996 | 0.00002194 |
| +0.0003 | 0.01638539 | 0.06343501 | 0.99999963 | 0.00006556 |
| +0.001 | 0.01636536 | 0.06335447 | 0.99999588 | 0.00021564 |
| -0.001 | 0.01648484 | 0.06381943 | 0.99999588 | 0.00022369 |
| +0.003 | 0.01643553 | 0.06360456 | 0.99996297 | 0.00062064 |
| +0.01 | 0.01817954 | 0.07008366 | 0.99958970 | 0.00183606 |
| -0.01 | 0.01961105 | 0.07560236 | 0.99958409 | 0.00247707 |
| +0.03 | 0.04088132 | 0.15219373 | 0.99629434 | 0.01884426 |
| -0.03 | 0.05032572 | 0.18395886 | 0.99614062 | 0.01878487 |

The sign challenge shows the small positive-angle improvement is instance-specific interference, not a general benefit of noisy control. At larger angle both signs worsen protection. The nonzero discrepancy from powering the one-round decoded channel confirms that syndrome memory was retained rather than silently reset.

Matched unencoded site infidelities atT32: 0.506690, 0.381802, 0.447711, 0.874078, 0.909818. Encoded storage uses five native channel calls per round plus many EC controls, whereas each site baseline uses one call. This is not an optimized same-resource code comparison.

Noiseless-control whole-superoperator agreement with idealP has maximum entry error 1.5959455978986625e-16. Every noisy instrument is trace preserving within numerical tolerance, and all recorded logical Choi matrices are checked diagnostically for positivity/trace in results.json.

**Useful distinction:** actual physical repeated recovery under stationary coherent control errors is now constructed and evaluated. The remaining practical gap is hardware-like idling/crosstalk, realistic inverse synthesis, injection/readout and controller faults, not an absent repeated physical-state calculation.
