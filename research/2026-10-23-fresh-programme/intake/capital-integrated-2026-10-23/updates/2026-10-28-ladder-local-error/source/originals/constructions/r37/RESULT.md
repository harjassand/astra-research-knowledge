# Local parity-breaking response of the embedded pair

**Closed spectral-density target:** for the exact dressed even pair in the
supplied ladder at `g=1/5` and `V=n_L-n_R`, the infinite-system response is
**finite and strictly positive**. Analytically,

\[
 \rho_g(E_p)=\int_{\max(4,E_p-2)}^{\min(6,E_p)}
 w_+(x)w_-(E_p-x)
 \left|\sqrt{\frac{2}{L_+'(E_p)+L_-'(E_p)}}
 [r_+(E_p-x)+r_-(x)]-\frac{J(E_p+i0)}{K(E_p+i0)}\right|^2dx.
\]

Here `r_sigma` is the complete one-body memory resolvent and `K,J` are the
complete-measure transforms defined in `PROOF.md`, including both bound atoms
and all continuous pieces. The exact odd hard-core resolvent is `Q-J^2/K`.
A scalar limiting-absorption proof establishes finiteness; an analytic
nonconstancy argument using the exact first two one-body moments proves strict
positivity at fixed coupling. No small-`g` substitution or finite-chain limit
is used for that classification.

Independent 40-decimal continuum quadrature gives

- `E_p = 5.9785793151665785452365388939752013`;
- `rho_(1/5)(E_p) ≈ 2.12750672061584e-8`.

These digits are numerical diagnostics; the finite-positive conclusion is an
analytical theorem. Direct physical ladder Fock calculations at 4, 8 and 12
sites per rail verify the dressed source and rank-one resolvent formula to
about `2e-15`. Replacing the pair by `|LR>` would give the incorrect answer
zero, since `V|LR>=0`; omitting the odd hard-core correction gives about
`1.4262e-11`, also a different answer.

The essential imports are the bounded spectral theorem, tensor functional
calculus, elementary Schur elimination, and the Hölder-density
Sokhotski--Plemelj formula. Its hypotheses are verified in the proof; no
resonance or exponential-decay theorem is imported.

**Remaining boundary:** the specified spectral target has no remaining
obligation in this derivation. A resonance expansion and a controlled lifetime
or gate-error law remain separate, unproved claims. If such a theorem applies,
the amplitude half width is `pi eta^2 rho + o(eta^2)` and the probability rate /
Lorentzian full width is `2 pi eta^2 rho + o(eta^2)`, approximately
`1.3367519e-7 eta^2`. The next attack for that distinct claim is a local analytic
continuation of the odd scalar response and a Feshbach resonance theorem with
an explicit time-window remainder. No novelty-priority or device-advantage
claim is made.

Files:

- `PROOF.md`: complete construction, scalar boundary argument, positivity proof,
  numerical scope, and linewidth conventions.
- `spectral_response.py`, `results.json`: double-precision infinite-measure
  evaluation at three quadrature tolerances with consistency assertions.
- `high_precision_check.py`, `high_precision_results.json`: independent
  arbitrary-precision continuum evaluation.
- `finite_volume_check.py`, `finite_volume_results.json`: direct physical-ladder
  checks of the actual source and compressed resolvent, with assertions.

All inputs were read only from the common task and scientific packet; all
written artifacts are in this directory. Reproduce each check with
`/usr/local/bin/python3 <the corresponding script path>`.
