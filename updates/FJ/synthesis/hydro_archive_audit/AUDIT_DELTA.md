# Physical archive replay delta

## Result

The newly acquired source archive is intact and its copied checker replays successfully. The producer's six symbolic-check labels, fixed random seed/trial/port counts, 40,804 matching-grid count and maximum-excess result, and conditional table match the replay exactly. The four floating-point diagnostics differ only in the last few machine-precision digits (maximum absolute delta (4.45\times10^{-16})); these are consistent with library/runtime numerical variation. The checker exits 0 and emits no warning or error.

No fatal sign or algebra error was found in the stated DC network model. The archive does not change the earlier mathematical or physical verdict. It makes the computation reproducible from the named source, but it remains a finite algebraic/lumped-network check. The archive explicitly says no physical device was built or measured. In particular, the indispensable wet interface remains an unacquired response: no measured steady reciprocal pressure/flow–voltage/current pair with a complete (K,C,G) at the claimed operating point is supplied.

## Cold source and code audit

The archive contains exactly `RESEARCH_NOTE.md`, `check_model.py`, `model_checks.json`, and `MANIFEST.json`. The member hashes match both the archive's internal manifest and the separately preserved intake supplement. The code imports NumPy and SymPy, performs symbolic assertions, 1,000 fixed-seed four-port floating-point trials, and a four-case (101\times101) grid; it writes only `model_checks.json` beside the script and prints the same JSON. Inspection found no network access, subprocesses, external file reads, or other side effects in the copied checker.

The JSON reproduces six output labels, but that is not six independently asserted symbolic results. Five labels correspond directly to symbolic assertions for the two-transmission cross-response ratio, the antisymmetric Schur identity, ideal reverse-response zero, receiver-resistance optimum, and scalar electrical-matching derivative/value. The sixth label names the factorized efficiency ceiling but has no separate symbolic assertion in the script; the factorization follows from the note’s algebra and is checked at four selected input pairs by floating-point matching calculations. This is a reproducibility-description caveat, not a fatal theorem error. These checks support the displayed derivations but are not a formal proof of every general statement. In particular, the general rank-preservation theorem is checked numerically on the sampled full-coupling matrices, not proved for every matrix by the script. The note's invertible-congruence argument supplies that proof when all (C_i\ne0). The random set is one reproducible synthetic distribution, not a physical network ensemble or robustness study. The grid checks four selected pairs over a finite range; it cannot by itself prove a global bound. The analytic derivative argument, not the grid, establishes the scalar global maximum.

The code's output is accurately scoped as model checks only. It does not model liquid interfaces, Hall material/contact fabrication, frequency dependence, noise, auxiliary supply costs, or actual power. The conditional (Z=0.0004) and (Z=11) table entries remain literature-derived theoretical inputs rather than measured complete transducers.

## Corrections and scope notes

The source states that in the ideal-chiral limit $H_{12}=0$ while $H_{21}\ne0$ if $C_1C_2\ne0$. The forward response also requires $g_+>0$; if $g_+=g_-=0$, both cross-responses vanish. My prior assessment already used the sufficient condition $g_-=0<g_+$, so this is a source wording correction rather than a change in the verdict.

The previously derived receiver-multiport maximum was stated for reciprocal resistive loads. Its value and attainability extend to any real, linear passive DC load $L$, including a nonreciprocal one, provided the source row is isolated and the receiver equations are well posed. Let the passive load law be $Q_R=-Lp_R$ with $\operatorname{sym}L\succeq0$, set $S=\operatorname{sym}D\succeq0$, and write $p_R=-xp_0$. The load equation gives $Q_R=Lxp_0=(b-Dx)p_0$. Then

\[
\frac{P_{\rm out}}{p_0^2}=x^T\operatorname{sym}(L)x=x^Tb-x^TSx,
\]

because the skew parts do no real DC work. For $S\succ0$, this is maximized at $x=S^{-1}b/2$, giving

\[
\eta_{\max}=\frac{b^TS^{-1}b}{4h_{00}}.
\]

For $S\succ0$, write $x_*=S^{-1}b/2$ and $y=b-Dx_*$. Since $x_*^Ty=b^TS^{-1}b/4>0$, a symmetric positive-definite load realizing this point is

\[
L=\frac{yy^T}{x_*^Ty}+\alpha\left(I-\frac{x_*x_*^T}{x_*^Tx_*}\right),\qquad \alpha>0,
\]

which obeys $Lx_*=y$. Thus allowing passive nonreciprocal loading cannot increase the value or improve attainability. If $S$ is singular, use $S^+$ with the passivity-required $b\in\operatorname{range}(S)$. This broadens the load class without changing the earlier ceiling or physical status.
## Replay comparison

The replay preserves the producer JSON structure and exact symbolic labels. The seed is 20261014, the network sample is 1,000 four-port trials, and the grid reports 40,804 points and zero excess above the stated bound. The conditional table is byte-for-value equal after JSON parsing. Stored versus replayed numerical diagnostic deltas are:

- minimum symmetric hydraulic eigenvalue: (+2.19\times10^{-16})
- maximum Onsager–Casimir error: (-4.44\times10^{-16})
- maximum power-balance residual: (+1.11\times10^{-16})
- maximum antisymmetric-identity error: (-9.96\times10^{-17})

These are rounding-scale changes, not claim discrepancies. See `REPLAY_RECEIPT.json` for command, environment, exit status, runtime, and SHA-256 hashes; `READ_LEDGER.md` records files and access scope.
