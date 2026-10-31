# Audit: coarse-rate settling and boxcar readout

Date: 2026-10-31. This is a mathematical continuation of OUTPUT_MODE_AUDIT.md. No root files were edited and no external research was used.

## Verdict

The proposed extension is correct for a fixed but unknown resonant decay rate kappa in a supplied interval [kappa_minus,kappa_plus], positive bounded source gain, fresh Gaussian input, and a finite initial mean receiver excitation bound. The source and receiver may be initially correlated with each other and with an arbitrary reference.

The drive must be on throughout [0,t0+L], as stipulated. The physical boxcar observes only [t0,t0+L]. The total label-error bound is valid on a global receiver-energy constraint; it does not require every normalized sector/history to obey that same energy bound.

## 1. Receiver residue and positive transport kernel

Let T=t0+L and w(t)=1/sqrt(L) on [t0,T], zero elsewhere. The free measured output mode is canonical and has

\[
B=\zeta_\kappa a_0+B_{\rm bath},
\]

\[
\zeta_\kappa=
\frac{2e^{-\kappa t_0/2}(1-e^{-\kappa L/2})}{\sqrt{\kappa L}}.
\]

The bath contribution commutes with a0, has commutator 1-zeta_kappa^2, and under fresh thermal input has quadrature variance (1-zeta_kappa^2)v, no larger than v.

The force-response commutator kernel is

\[
\beta_\kappa(t)=
\frac{\sqrt\kappa}{\sqrt L}
\int_{\max(t,t_0)}^{T}e^{-\kappa(u-t)/2}du\ge0,
\quad 0\le t\le T.
\]

The selected pointer B now contains a0. That does not invalidate the transport argument: G acts on the source factor and commutes with B as an operator. Initial source/receiver entanglement changes the initial pointer distribution, not this commutation relation.

Integrating the positive kernel over the entire driven interval gives

\[
\mu_\kappa=
2g_-\int_0^T\beta_\kappa(t)dt
=4g_-\sqrt{\frac L\kappa}
\left[
1-\frac{2e^{-\kappa t_0/2}(1-e^{-\kappa L/2})}{\kappa L}
\right].
\]

The proposed uniform bounds are valid:

\[
\mu_\kappa\ge\mu_0:=
4g_-\sqrt{\frac L{\kappa_+}}
\left[1-\frac{2e^{-\kappa_-t_0/2}}{\kappa_-L}\right],
\]

provided the displayed bracket is positive, and

\[
\zeta_\kappa^2\le
\zeta_{\max}^2:=
\frac{4e^{-\kappa_-t_0}}{\kappa_-L}.
\]

The conservative zeta_max bound need not itself be below one for all small L; the actual canonical-mode residue is below one. This does not invalidate the probability bound, although the resulting bound can be uninformative.

## 2. Uniform receiver second moment

For Y_a=i(a0^dagger-a0), any receiver state with mean N<=E satisfies

\[
\langle Y_a^2\rangle
\le V_E:=2E+1+2\sqrt{E(E+1)}.
\]

Indeed,

\[
Y_a^2=2N+1-a_0^2-a_0^{\dagger2},
\qquad
|\langle a_0^2\rangle|\le\sqrt{E(E+1)}
\]

by Cauchy-Schwarz. No centering of the receiver state is assumed. Correlations with logical/source/reference systems do not affect this reduced-state inequality.

## 3. The tail union bound works on a global energy constraint

The initial pointer quadrature is

\[
Y_{\rm in}=\zeta_\kappa Y_a+Y_{\rm bath}.
\]

The two summands commute. For 0<r<mu0,

\[
\{Y_{\rm in}\ge\mu_0\}
\subseteq\{\zeta_\kappa Y_a\ge r\}
\cup\{Y_{\rm bath}\ge\mu_0-r\},
\]

and likewise for the opposite tail. Fresh field gives the Gaussian bath tail conditional on the logical sector and actual prior history.

For an arbitrary initial mixture or coherent superposition of the two logical sectors, the two wrong receiver-tail contributions obey

\[
\Pr(\Pi_+,\zeta Y_a\ge r)+
\Pr(\Pi_-,\zeta Y_a\le-r)
\le\frac{\zeta_{\max}^2\langle Y_a^2\rangle}{r^2}.
\]

This uses Pi_++Pi_-=I and their commutation with the receiver quadrature. It avoids imposing E on each normalized sector input.

The Gaussian bath contributions sum with their sector probabilities to one copy of the same Gaussian tail. Thus the total wrong-label probability satisfies

\[
\boxed{
p_{\rm wrong}\le
Q\!\left(\frac{\mu_0-r}{\sqrt v}\right)
+\frac{\zeta_{\max}^2V_E}{r^2}.
}
\]

The conditional Gaussian statement is supplied by fresh input, not by independently resetting the retained source or by assuming favorable normalized conditional receiver states.

The fixed CP comparator from OUTPUT_MODE_AUDIT.md then gives

\[
d_{\diamond,E}\le p_{\rm wrong}+\sqrt{p_{\rm wrong}},
\]

capped at one. The comparison is logical identity within each measured sector jointly with an allowed source/receiver-output channel, not identity return of those auxiliary systems.

## 4. Explicit window sizing

For a target label error epsilon in (0,1), choose

\[
L\ge
\max\left\{
\frac4{\kappa_-},
\frac{2\kappa_+v}{g_-^2}\log\frac1\epsilon
\right\},
\qquad
r=g_-\sqrt{\frac L{\kappa_+}}.
\]

Then mu0>=2r, even before using a positive t0. Since Q(x)<=exp(-x^2/2)/2 for x>=0, the Gaussian contribution is at most epsilon/2.

Choose

\[
t_0\ge\frac1{\kappa_-}
\left[
\log\frac{8\kappa_+V_E}
{\kappa_-g_-^2L^2\epsilon}
\right]_+.
\]

The receiver contribution is at most epsilon/2. Consequently, for fixed rate bounds, g_- and v,

\[
T=t_0+L=
O\!\left(\log(1/\epsilon)+\log(1+E)\right).
\]

A target full-instrument error delta requires epsilon of order delta^2, not epsilon=delta. For example epsilon=delta^2/4 is sufficient for delta<=1.

The constants can be large when the force is weak or the thermal variance is large. The scaling statement does not certify a practical device window.

## 5. An actual receiver-energy envelope for repeated calls

The same bounded force supplies a useful independent reuse estimate. The operator Langevin solution is

\[
a(T)=a_{\rm free}(T)
-iW\int_0^T e^{-\kappa(T-t)/2}G_H(t)dt.
\]

Unitary conjugation preserves the gain norm. Hence the second term has operator norm at most 2g_+/kappa. Under fresh thermal input of occupation n_th,

\[
\sqrt{\langle N_T\rangle}
\le
\sqrt{e^{-\kappa T}E+
n_{\rm th}(1-e^{-\kappa T})}
+\frac{2g_+}{\kappa}.
\]

Uniformly over the coarse rate interval, a simple affine consequence is

\[
\boxed{
E_{\rm out}\le
2e^{-\kappa_-T}E
+2n_{\rm th}
+\frac{8g_+^2}{\kappa_-^2}.
}
\]

Thus T>log(2)/kappa_minus gives a contracting coefficient on the incoming receiver energy. This is a bound on actual weighted histories; rare normalized homodyne histories can still be arbitrarily hot.

Nonselective measurement of the departed output field does not change the receiver's marginal energy. Any later feedback, switching, loading or holding must have its own energy contribution included. Bounded feedback force is already covered when it is represented by the stated joint model.

This argument bounds receiver excitation, not arbitrary source energy or the continued physical availability of the lower gain bound g_-. Source capacity and the actual-history gain/domain qualifications remain separate resources.

## 6. Remaining boundaries

- The actual kappa is a fixed scalar during a window. Arbitrary quantum or fluctuating poles are not covered.
- The receiver is resonant over the interval. Unknown detuning would require additional robust analysis.
- The force is on for the whole settling-and-readout interval. Turning it on only for the final boxcar changes the shift formula.
- Fresh Gaussian field must be qualified conditional on the actual past. An unconditional marginal cannot replace it.
- The quantum transport proof still needs the valid linear bosonic dilation and bounded positive source gain.
- No claim of source identity return, fine-outcome logical-marginal invariance, or a special advantage over an equally informed ordinary controller follows.
- Wall time, fresh-field preparation, homodyne acquisition, detector inefficiency, and symmetry-breaking exposure remain charged. The ideal logarithmic accuracy scaling does not override fixed physical logical-noise rates.

The independent executable audit includes the residue, integrated-kernel identity, conservative rate bounds, and the explicit sizing inequalities.
