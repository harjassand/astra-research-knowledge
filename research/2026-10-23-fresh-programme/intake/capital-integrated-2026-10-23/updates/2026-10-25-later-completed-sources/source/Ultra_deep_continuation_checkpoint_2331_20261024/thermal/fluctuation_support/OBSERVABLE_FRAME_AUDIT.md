# Independent audit: observable frames and spectral flow

This is a scoped check of `thermal/OBSERVABLE_FRAME_PRINCIPLE.md`. Under its
analytic, stable, time-reversal-symmetric Bloch assumptions and its stated
finite covariance caps, I find no gap in the spectral-flow channel count or
the concrete frame constants. The result does not extend to a strain-only or
gauge-quotiented cap without a new frame inequality.

## Spectral-flow multiplicity

Let `n_<(q,omega)` count eigenvalues of `D(q)` strictly below `omega^2`, with
algebraic multiplicity. For `a>0`, choose a maximizer `q_*` of
`lambda_min(D(q))`; time reversal makes `lambda_min` even, so take
`q_* in (0,pi]`. For a regular `omega in (0,a)`, avoid the endpoint and
critical/branch-crossing values. Then

`n_<(0,omega)>=d`, `n_<(q_*,omega)=0`.

Along increasing `q` from `0` to `q_*`, an upward eigenvalue crossing removes
one eigenvalue from `n_<`, while a downward crossing adds one. Hence

`U(omega)-D(omega)=n_<(0,omega)-n_<(q_*,omega)>=d`,

so `U(omega)>=d`. At an upward crossing, `d omega_n/dq>0`, which is a
right-moving Bloch mode. Crossings at degeneracies are counted with their
multiplicity. Identical nonconstant analytic branches therefore contribute
their full multiplicity and their common crossing direction; isolated
degeneracies and critical values are exceptional frequencies of measure
zero. A constant branch contributes only at its one frequency, also a null
set. Thus the complete right-moving channel count is at least `d` almost
everywhere on `(0,a)`. There is no need to assume monotone bands or to infer
channels by counting a band union. I found no counterexample within these
assumptions.

The covariance cap and positive frame also rule out `a=0`: that would give a
zero-frequency lowest mode on the positive-measure frame set and hence
infinite `V_F`, contradicting finite `B`. The full Gibbs coefficient
`c_T(omega)` is decreasing, since its derivative is
`-hbar/(2 omega^2) [coth(x)+x csch^2(x)]` with `x=omega/(2 theta)`.

## Concrete scalar displacement frame

For a unit mass-normalized mode, write
`r=x-x_b 1` and `z=sqrt(M)|x_b|`. On `|q|>=pi/2`,
`|exp(iq)-1|^2>=2`, so

`F_q(x)>=||r||_M^2+z^2`,
`1=||x||_M<=||r||_M+z`.

By Cauchy-Schwarz, `F_q(x)>=1/2`. Homogeneity gives the frame inequality for
all modal vectors, so `p=1/2` and `alpha=1/2`. The expectation of the frame
observable is the sum of the centered variances of the listed observables:

`B<=sum_j m_j d_0^2+(M/2)d_0^2=3 M d_0^2/2`.

The general covariance estimate therefore gives
`V_F>=c_T(a)/4`, then `c_T(a)<=6 M d_0^2`, and finally

`a tanh[a/(2 theta)]>=hbar/(12 M d_0^2)`,
`a>=hbar/(12 M d_0^2)`.

This uses total centered quantum Gibbs covariance, including zero-point
motion. In the classical Gibbs model, replacing `c_T` by `k_B T/omega^2`
instead gives `a^2>=k_B T/(6 M d_0^2)`. The constants match the note.

The frame is made of full displacement vectors: each within-cell `r_j` and
the adjacent-cell vector `t`. It is not just a scalar bond extension or
strain tensor. A transverse or torsional mode can be invisible to linear
longitudinal strain; then the all-mode frame lower bound has `alpha=0`, and
the theorem cannot use that cap. A per-cell rotating gauge could likewise
erase the very relative vectors used by the frame, and is not the declared
fixed physical reference frame. Removing exact global zero modes does not
remove nonzero-wave-number rotational/torsional fluctuations; if those make
the centered `r_j` or `t` variance diverge, the finite-range premise fails.

For example, a two-component chain with harmonic energy
`(k/2) sum_l (u^x_(l+1)-u^x_l)^2 + (kappa/2) sum_l
 (u^y_(l+1)-2u^y_l+u^y_(l-1))^2` has a transverse flexural branch that a
frame containing only the linear axial strain `u^x_(l+1)-u^x_l` does not
see. This is a counterexample to upgrading a strain-only cap to the stated
all-mode frame conclusion; it is not a counterexample when the full vector
observables `r_j,t` are actually capped.

For vector-valued coordinates, the same inequalities hold with Euclidean
norms and scalar mass weights, provided the caps apply to the total variance
over every spatial component. A fixed orthogonal change of laboratory axes
preserves these norms. A cap only on lengths, orientation-invariant strain,
or selected components is insufficient unless it independently proves the
same all-mode frame inequality.
