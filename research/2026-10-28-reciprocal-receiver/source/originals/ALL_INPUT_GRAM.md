# Uniform all-input target-Gram recovery from the new reciprocal receiver

28 October 2026. A continuation proof, not an inherited whole-proof audit.

## Contract and acquisition

Use the new calibrated coherent-reference oracle proved in
`mechanisms/COHERENT_THREE_LOAD_OBSERVABLE.md`. Let G=bb* be positive
semidefinite rank one, ||G||<=1. Every unit query u returns p_hat(u) with
simultaneous deterministic error <=delta from p(u)=u*Gu. Include all readout,
load, reference, combiner, preparation, arithmetic and source-stability errors.
At fixed calibrated reference strength and radius, the new delta is proportional
to raw-intensity error. This assertion is not made for the original interface.

Acquire n diagonals d_hat_j. Let D=max_j d_hat_j and choose maximizing k.
If D<=4delta, return G_hat=0. Otherwise query, for j!=k,

    v_j=(e_j+e_k)/sqrt(2), w_j=(e_j+i e_k)/sqrt(2).

For the column q=G e_k, infer

    q_hat_j=p_hat(v_j)-(d_hat_j+D)/2
             +i[(d_hat_j+D)/2-p_hat(w_j)],
    q_hat_k=D,
    G_hat=q_hat q_hat*/D.

The sign convention is q_j=G_jk. Expand both quadratic forms to check it.
The full branch uses 3n-2 scalar queries, hence 36n-24 raw powers with the
twelve-reading receiver, plus twelve if a final verification is desired.
No nonzero pivot or informative pilot is supplied in advance.

## Uniform proof

Each inferred real/imaginary cross coordinate has error <=2delta. Therefore

    ||q_hat-q|| <= e=sqrt(8n-7)delta.

Let d=G_kk and tau=tr G. On the nonzero branch d>=D-delta>0. Rank one gives
q q*=dG and ||q||^2=d tau. The acquired T_upper=sum_j(d_hat_j+delta) bounds
tau above. Adding and subtracting q q*/D yields the data-dependent certificate

    ||G_hat-G|| <= [2sqrt((D+delta)T_upper)e+e^2]/D
                    +T_upper delta/D.                 (1)

Indeed, the numerator perturbation is <=2||q||e+e^2, and the denominator
correction equals tau|D-d|/D. Substitute d<=D+delta and tau<=T_upper.
This argument does not require independent errors.

Since T_upper<=n(D+delta) and delta/D<1/4, (1) is at most

    [(5/2)sqrt(n(8n-7))+(8n-7)/4+5n/4]delta
      <=[(5/2)sqrt(8)+13/4]n delta <11n delta.

In the zero branch each d_j<=D+delta<=5delta, hence ||G||=tr G<=5n delta.
Thus, uniformly including G=0,

    ||G_hat-G|| <=11n delta.                            (2)

For delta=0 the zero source takes the zero branch; every other division is
legal and reconstruction is exact. This closes all later unit-input power
predictions with a linear absolute-error modulus. Relative precision still
requires a resolved signal. The output is PSD of rank at most one; clipping
its norm to one is unnecessary for the proof.

## Conventional control and costs

The original sequential two-mode controller applies directly to p and gives

    tau-p(u_out)<=2(1+2sqrt(2))(n-1)delta+nu_control.

It uses 4(n-1) oracle calls, or 48(n-1) raw powers, plus twelve for verification.
Adding n diagonal queries for trace/optimum certification gives 60n-48+12.
These are alternative schedules to the 3n-2-query column reconstruction,
not obligatory additive costs. Using the top vector of G_hat instead gives
regret <=2||G_hat-G|| before physical command errors.

Actual finite preparation must pay for approximating sqrt(2), normalizing and
rounding commands. Subunit rational mixtures can be used with paid rescaling.
A unit/subunit command discrepancy zeta changes p by <=2zeta. Dense O(n)
mask settings may cost O(n^2) channel writes. Source/reference photons,
actuation and settling remain charged. No universal optimizer or hardware
advantage follows from the linear precision modulus.

## Executable scope

`gram_reconstruction_checks.py` checks exact rational coordinate/noise cases
using exact positive LDL pivots of 11n delta I plus/minus the error matrix,
which certify (2). Frobenius values are diagnostics. These finite checks
support their tested cases; the all-input guarantee rests on the proof above.
