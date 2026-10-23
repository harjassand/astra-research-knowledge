# Binary SLD ledger audit

24 October 2026. Bounded audit of `BINARY_SLD_COMPENSATED_LEDGER_OPENING.txt`; no risk-only closure or physical counterexample is attempted.

## Equations (1)--(3)

For normalized complete outputs, `R±Q=rho_{0,1}` gives `-R<=Q<=R`, and `ker R=ker rho_0 intersect ker rho_1`; positivity also makes `Q` vanish on and across `ker R`. On `supp R`, the Lyapunov inverse is

\[
\mathcal S_R^{-1}(B)=2\int_0^\infty e^{-sR}B e^{-sR}\,ds,
\]

so `A=S_R^{-1}(Q)` is Hermitian. Applying the positive inverse to `R±Q` gives `I±A>=0`, hence `||A||<=1`; set `A=0` on `ker R`. Cyclicity gives `Tr(QA)=Tr(RA^2)=C`. With `F=sign(Q)`, weighted Hilbert--Schmidt Cauchy--Schwarz yields `||Q||_1=Tr(QF)<=sqrt(Tr(RA^2) Tr(RF^2))<=sqrt(C)`, since `Tr R=1` and `F^2<=I`. Also `0<=C<=1`.

Variation of `2Tr(QF)-Tr(RF^2)` over Hermitian `F` gives `(RF+FR)/2=Q`; at the canonical solution its value is `C`. The maximum can be restricted to the compact set `||F||<=1`, since a maximizing solution with that bound exists. This proves (1)--(3), including singular `R`, for a finite-dimensional complete state pair. Common CPTP maps contract `C` (the SLD/QFI monotonicity for the affine binary-mixture path); for an instrument, retain all outcomes in one CPTP output. A normalized postselected branch alone need not contract it.

## Differential identity and coefficients

For a common Lindblad generator with Hamiltonian `H` and jumps `L_j` (rates included in `L_j`), the variational envelope derivative at a differentiability time is

\[
\dot C=2Tr(\dot Q A)-Tr(\dot R A^2).
\]

The common Hamiltonian cancels. For each jump, substituting `Q=(RA+AR)/2` into the two dissipator terms gives

\[
\dot C_{L_j}=-Tr\big(R[L_j,A]^\dagger[L_j,A]\big).
\]

Thus nonunital local detector/reset channels have the good sign when treated as common channels. This is not an HS-purity argument and requires no correlated sample/ancilla channel. With `d_s=g_0-g_1` and the displayed R/Q equations, the signal terms are

\[
S=i d_s Tr(R[V,A])-\frac{i d_s}{2}Tr(Q[V,A^2]),
\]

with the signs and factors in (4). Both terms are real. The loss jump contributes `gamma[J,A]†[J,A]` to Gamma when its output flag is part of the common instrument.

## Singular ranks and newly written records

In a fixed finite-dimensional ambient output space, `C(t)` is the maximum of a smooth function over the compact operator interval `||F||<=1`. If `R(t),Q(t)` are absolutely continuous with bounded rates, this maximum is Lipschitz and differentiable almost everywhere. At points where `C` is differentiable, the envelope theorem gives the displayed derivative for a maximizing `A`; at nondifferentiability/rank-change times, use the absolutely-continuous integral and do not assert a pointwise formula. Discrete common instruments at primitive boundaries contract `C` and can be handled as separate downward jumps. A zero-probability orthogonal outcome sector causes no discontinuity in `C`.

There is a real pointwise caveat. The following is an algebraic rank-boundary test, not a physical-control counterexample. For `t>=0` small, take the diagonal pair

\[
\rho_0(t)=diag(1-a_0t,a_0t),\quad
\rho_1(t)=diag(1-a_1t,a_1t),\qquad a_0,a_1>0.
\]

At `t=0`, `R=diag(1,0)`, `Q=0`; the canonical choice `A=0` on `ker R` gives `2Tr(dot Q A)-Tr(dot R A^2)=0`. But for `t>0`,

\[
C(t)=\frac{(\delta a)^2t^2}{1-\bar a t}
      +\frac{(\delta a)^2t}{\bar a},\qquad
\bar a=(a_0+a_1)/2,\quad\delta a=(a_0-a_1)/2,
\]

so `C'(0+)=(delta a)^2/bar a`. The variational maximizer at the boundary may choose `F=diag(0,delta a/bar a)` on the newly populated sector and obtains this right derivative. Thus (4) is an a.e. envelope statement, not a pointwise derivative rule using the zero-on-kernel representative at a rank onset. The single boundary contributes no extra term to the integrated finite-dimensional identity.

For a finite record register/finite outcome resolution, newly populated sectors fit this a.e. treatment. A continuously resolved death-time register is instead a direct-integral output with a moving support boundary; a finite-dimensional Lipschitz argument alone does not establish its boundary-flux term. One must either use the actual finite-resolution instrument (and keep all bins/outcomes) or prove the corresponding direct-integral envelope/flux identity. Merely declaring a finite elapsed-time cap does not make an exact continuous timestamp a finite-dimensional record.

The differential identity is valid for the common Markov channels specified in the opening. More general actual local CPTP resets can be inserted as common CPTP contractions between smooth segments; if modeled by Lindblad jumps, their commutators enter Gamma. No extension is made to parameter-dependent resets, sample-changing crosslinks, or correlated baths. These rank/instrument details do not address the separately open control of the integrated signal source `S` by actual risk.
