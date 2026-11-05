# Local quantum availability and late-time smoothness

[Return guide](README.md) · [Complete proof in supplied return](P2_AUTONOMOUS_LOCAL_READOUT_20261106_RETURN.txt) · [Interface limits](interfaces-comparators-and-open-construction.md)

## An admissible adversary inside the actual burst source

Bounded density, bounded support and bounded incident-term multiplicity allow a finite coloring of source regions covering local interaction supports. A permitted randomized CPTP assignment selects support replacement streams, plus a port replacement stream, of rate `q=c_src lambda>0` independent of the horizon. Unused marks act as identity. The marks retain their actual geometry and intensity.

This is one allowed memoryless assignment used for a universal converse. It is not an inferred independent effective-noise law for the constructive compiler. Only bounded-radius marks are used, so the new timing obstruction does not require the Pareto tail.

## A finite quantum-availability budget

With inaccessible Bell reference `R`, port `P` and remainder `B`, port replacement discards conditional mutual information `I(R:P|B)`. Total reference/device correlation cannot grow under device-only dynamics. The supplied proof obtains, using natural logarithms,

```
q integral_0^infinity I(R:P|B) dt <= 2 ln 2.
```

The finite-time version is sufficient. Applying the imported corrected Brandao–Christandl–Yard one-way-LOCC bound and an explicit random Pauli-parity Bell witness gives, for decoded Bell fidelity `F(t)`,

```
integral_0^infinity [F(t)-1/2]_+^2 dt <= 9 ln 2 / q.
```

Recovery from other registers and extra blank ancillas cannot restore irreversibly discarded reference correlation. The argument is quantum-specific: a classical bit may have a copied readable local record without the same conditional-information loss. No corresponding classical linear-hardware theorem is inferred.

## A limit on narrow late readout peaks

For an exact channel-jump representation `G=Lambda(Phi-id)`, Poisson uniformization gives `F(t)=E[f_K]`, `K~Poisson(Lambda t)`, with `0<=f_K<=1`. Its score variance yields

```
|F'(t)| <= (1/2) sqrt(Lambda/t)
|F(t)-F(s)| <= sqrt(Lambda)(sqrt(t)-sqrt(s)), 0<=s<=t.
```

This needs neither an unbiased clock estimator nor independent logical cycles. Correctness at one late instant forces nonzero availability over nearby times, even though the operating contract promises accuracy only at the deadline.

A noiseless Hamiltonian generator need not admit finite-rate uniformization. The source explicitly rejects applying the jump bound directly to it. Instead, allowed local depolarizing replacements regularize each bounded-support Lindblad term. A Choi/Schur-complement construction gives an exact CPTP representation of the same noisy generator, with aggregate rate `Lambda<=C_lambda N+q` for fixed positive intensity. This is an algebraic representation, not a proposed global hardware update.

For `g=1/2-delta>0`, combining the availability budget with the late-time smoothness estimate gives, for sufficiently late `t_*`,

```
Lambda >= q^2 g^6 t_* / [324 (ln 2)^2].
```

Thus `N=Omega(t_*)` at fixed positive intensity and fixed accuracy. The displayed sufficient small-intensity prefactors differ for pure jump versus general Lindblad dynamics; their intensity powers/constants are not claimed optimal. The fixed-intensity-before-horizon limit is essential to the stated separation.

The stronger failure statement is

```
F(t) <= min(1, 1/2 + [324(ln2)^2 Lambda/(q^2 t)]^(1/6)).
```

Consequently `N=o(T)` cannot meet the accepted fixed-port Bell-fidelity target at late deterministic time. The decoder may be optimized separately for each device/horizon, but remains fixed when nearby times are compared for that device. This argument grants internal repair mechanisms in the stated dynamical class rather than proving a particular controller deadlocks.
