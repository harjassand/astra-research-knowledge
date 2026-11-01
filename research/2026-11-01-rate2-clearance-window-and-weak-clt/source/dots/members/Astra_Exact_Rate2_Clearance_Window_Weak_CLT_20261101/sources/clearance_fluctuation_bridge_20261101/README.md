# Actual rate-2 clearance fluctuation bridge

**Author theorem, pending independent review.**

`ACTUAL_CLEARANCE_CLT.md` gives a full-channel, stopped-clock proof candidate of

    (tau_clear - s_* N^(1/5))/N^(1/10) ==> Normal(0, integral b_l² dl).

It derives the finite-compact covariance from the actual reaction generator,
transports the remaining clock through a growing `L≈T^(3/2)` cutoff, and receives
actual all-channel macro removal in `o(sqrt(T))` time. The decreasing clock
sensitivity makes tail residuals summable and bounds the tail fluctuation bracket.

**Not claimed:** finite-N CDF error, mean/variance convergence, uniform
integrability, or cost superiority. Omitted marks are a paid admission failure
`O(T^-1/4)`, not silently deleted from the generator. Bad-history moments remain
unpaid, so the displayed limiting normal parameter is not an earned limit of
actual variances.

Reproduce the exact envelope ledger:

```sh
python clearance_fluctuation_bridge_20261101/check_tail_envelopes.py
python clearance_fluctuation_bridge_20261101/verify_saved.py
```

The arithmetic checks are supplementary. The requested next gate is an
independent mathematical review of the actual stopped-path and limit argument.
