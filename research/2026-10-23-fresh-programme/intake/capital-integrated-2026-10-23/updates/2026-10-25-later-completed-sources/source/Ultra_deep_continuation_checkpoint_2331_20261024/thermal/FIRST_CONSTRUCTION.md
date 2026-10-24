# Transport and equilibrium range away from exact optimality

## Literal assignment retained once

The principal programme brief is the separately preserved ../BRIEF.txt. The new delegation received by this thermal owner was:

```text
Continue as the warm foundational thermal owner. The literal new principal brief is saved once at /Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/portfolio_20261024/deep_continuation/BRIEF.txt; read it. Retain this assignment verbatim once in an ordinary research note. Preserve all governing proofs and corrections. Choose the next extension that opens genuinely new explanatory/design territory, not a parameter sweep. Test the importance of the one-intercell-link/rank-one scalar harmonic hypothesis and the all-optimal equilibrium compliance cost. Candidates worth weighing include a transport/fluctuation/resource principle away from exact optimality or a genuinely multichannel/multiple-link extension; these are suggestions, not a required next lemma. Own the full construction, seek a theorem/mechanism with a nontrivial consequence, and keep the strongest conventional explanation alive. Use primary science early and read actual sources behind any relevant Astra cards; pinned work/astra-capital stays read-only. Do not expand into protected observed-field/reaction-interface or chemical-memory work. Reactivate and give concrete bounded work to your same four Luna supports: physical_sources, luna_nonnormal, luna_one_probe, luna_circuit_sources. Do not spawn any new agents or a new pool. Luna can calculate, source-check and falsify, but you retain the whole argument. Save science under deep_continuation/thermal/ without replacing old files. Send substantive constructions/obstructions as they stabilize, continue useful attacks through checkpoints; never create a formal goal, automation, or administrative reporting forms.
```

## Owned question and representation

The exact optimum's large equilibrium displacement could conceivably be avoided by giving up some conductance advantage or adding many internal modes. The consequential question is therefore: can ANY finite passive cell, retuned arbitrarily with temperature, keep a fixed fractional reduction in low-temperature intrinsic conductance while its mass and internal relative rms displacement stay bounded?

The representation below connects three observables that must remain distinct: the full bulk passband indicator, a local static compliance, and Gibbs displacement variance. It derives an inequality between them rather than identifying transport noise with displacement noise. An independent support is testing multiple-link models, for which the scalar indicator and its sign structure may fail.

This construction and its inverse-cube moment were independently derived before reading ROOT_COMPLIANCE_MOMENT.md. Root subsequently shared the same moment, and independently checked the one-sided Lipschitz argument. These exposures do not supply a proof premise.

## 1. Complete admitted class

Keep the single-backbone scalar positive harmonic model of FAMILY_THEOREM_v3.md, but assume NO optimality. The backbone mass is m, total cell mass M>m, internal mass ms=M-m, intercell spring K>0, and temperature theta=k_B T/hbar>0. Any finite connected internal positive mass/spring graph, any number of active or dark modes, and arbitrary retuning with T are allowed. Put S=4K and Omega=sqrt(S/M).

Let chi(w) be the complete disjoint-interior passband indicator obtained from the rank-one Bloch pencil

D(q)=D0+s(q)vv^T, s(q)=S sin^2(q/2),
v=e_b/sqrt(m), z=sqrt(masses)/sqrt(M), D0z=0.

The rigid same-M,K comparator has chi0=1_[0,Omega]. The intrinsic Bose-weighted conductance integral is

J=integral g_theta(w)chi(w)dw,
g_theta(w)=[w/(2theta)/sinh(w/(2theta))]^2.

Write DeltaJ=J_rigid-J and delta=chi0-chi. Then

delta>=0 below Omega, delta<=0 above Omega,
integral delta(w)/w dw=0.

The last identity is the prior exact log moment. The sign property uses chi in{0,1}; it is a substantive rank-one restriction, not a generic multichannel assumption.

## 2. Static internal-CM compliance for every cell

For physical displacements define

Y=sum_j m_j x_j/ms-x_b,
w=Mass^(-1/2)(-1,m_j/ms)_j
 =-(M/ms)(v-z/sqrt(M)),
C=w^T D0^+w.

On the positive subspace z^perp let A=D0|z^perp and u=v-z/sqrt(M). The block matrix of D0+s vv^T on span(z) plus z^perp is

[ s/M                 s u^T/sqrt(M) ]
[ s u/sqrt(M)         A+s uu^T      ].

Its Schur complement of the first entry is exactly A. Therefore its inverse restricted as a quadratic form to z^perp is A^(-1), and for every s>0

w^T(D0+s vv^T)^(-1)w=C.

At s=0 the translation-free pseudoinverse gives the same value. Thus a local Y force pair on any periodic ring has static compliance C, independent of intercell K and the number of cells. This identity holds for every admitted cell, not only for the previous two-pole optimum.

Write the internal driving response as its positive spectral measure,

q(t)=v^T(D0+tI)^(-1)v
    =1/(Mt)+sum_l c_l/(t+r_l^2),
c_l>0, r_l>0,
tau=sum_l c_l/r_l^2.

Then C=(M/ms)^2 tau.

## 3. Exact inverse-cube transport moment

If alpha_j,beta_j are the squared band endpoints, cancel dark factors and use

prod(t+beta_j)/prod(t+alpha_j)=1+S q(t).

Expanding its logarithm at t=0 gives

sum_j1/beta_j-sum_(alpha_j>0)1/alpha_j
 =M/S+M tau.

Subtract the rigid interval before integrating the apparent zero-frequency singularity. Since the two connected spectra coincide near zero,

D3:=integral delta(w)/w^3 dw
   =M tau/2
   =ms^2 C/(2M)>=0.

This is an identity of full acoustic and optical bands. It prices low-frequency spectral removal in terms of a static displacement resource; it does not discard the compensating high-frequency bands.

## 4. A uniform off-optimum transport/range bound

Put h_theta(w)=w g_theta(w) and H_theta(t)=h_theta(t^(-1/2)). Define the finite positive universal constant

C_B=sup_(x>0) x^5[2x coth(x)-3]/sinh^2(x).

The expression tends to0 at both ends and is positive somewhere, so this supremum is finite and positive. Direct differentiation gives

H_theta'(t)=4theta^3 x^3 g(x)[2x coth(x)-3],
x=1/(2theta sqrt(t)), g(x)=(x/sinh x)^2.

Consequently H_theta'(t)<=L_theta:=4C_B theta^3 for every t>0. Anchor the one-sided Lipschitz inequality at t0=Omega^(-2). For w<Omega,

h_theta(w)-h_theta(Omega)
 <=L_theta[w^(-2)-Omega^(-2)],

and the inequality reverses for w>Omega. Multiplying by delta(w)/w preserves the integrated <= sign in both regions. The log moment cancels the anchor terms. Therefore EVERY admitted network obeys

DeltaJ<=L_theta D3
      =2C_B theta^3 (ms^2/M) C.

No closeness to the exact optimum, bounded internal order, or uniform internal stiffness bound was assumed. Negative DeltaJ is allowed: a poor network can conduct more than the rigid comparator.

## 5. Equilibrium displacement cost and low-temperature consequence

On a finite periodic ring remove only its global translation. For a positive mass-normalized normal-mode frequency omega, quantum Gibbs variance is

hbar/(2omega)coth[hbar omega/(2k_B T)]>=k_B T/omega^2.

Thus Cov(eta)>=k_B T D^+ on the translation-free subspace. The exact static compliance in Section2 yields

Var(Y)>=k_B T C.

If each internal relative coordinate y_j=x_j-x_b has rms at most d, then the L2 triangle inequality gives

sqrt(Var(Y))=||sum_j(m_j/ms)y_j||_L2
 <=sum_j(m_j/ms)||y_j||_L2<=d.

Means can equivalently be subtracted throughout; centred Gibbs means vanish. An rms cap directly on Y suffices too. There is NO need to assert individual variance>=CM variance away from optimality.

Combining the two bounds and normalizing by the single-channel Bose integral J_Q=pi^2theta/3 gives

(J_rigid-J)/J_Q
 <=(6C_B/pi^2)(ms^2/M) d^2 k_B T/hbar^2.

At fixed K,M and m>=m0>0, ms<=M-m0 and J_rigid/J_Q tends to1 as T tends to0. Hence a fixed fractional intrinsic-conductance reduction is IMPOSSIBLE with uniformly bounded mass and equilibrium relative-displacement range, even for nonoptimal designs, unbounded finite topology chosen separately at each T, and arbitrary spring retuning. This statement is conditional on the declared scalar one-link harmonic class and Gibbs reference-state range constraint.

The converse order-of-cost statement is narrower: the existing retuned pendant optimum has a fixed nonzero fractional improvement and Var(Y) of order1/T. Deriving its actual quantum variance coefficient will show the necessity exponent is attainable. This does NOT establish that the best bounded-range improvement is asymptotically linear in T; the inequality above is an upper bound, not a full Pareto solution.

## 6. Strong conventional explanation and source boundary

The complete Foster/Stieltjes comparator may realize every finite strict spectrum allowed by the moments, and receives the same mass, K, temperature and displacement budget. The theorem would apply equally to it. Passive network synthesis is not a newly acquired mechanism.

The primary [Das-Dhar harmonic scattering derivation](https://arxiv.org/html/1204.5595), equations1 and5-7 and the model in SectionII, was read early: it treats reservoir-coupled Landauer transmission using the full Green function. That conventional result keeps finite-contact transmittance distinct from our intrinsic bulk indicator; it supplies no inverse-cube CM-compliance identity or the bound proved here. Its standard Landauer operation is ancestry, not an advantage denied to the comparator. Source support is checking FDT/Kramers-Kronig and stronger sum-rule antecedents separately.

Capital lexical routes for thermal/phonon/fluctuation and the N777,N779,N140,N523 dossiers were inspected. Their actual model statements concern controlled ionic motion, local-channel free energy, entanglement variance or electrothermal feedback, respectively. None supplies a compatible theorem premise for this construction, so no source transfer is made. The capital checkout remains read-only.

The open multiple-link question is substantive: generic multichannel spectra need not be indicators bounded by1, and their determinant moments need not have the same scalar null residue. A separate support is attempting a counted positive counterconstruction. No multichannel theorem, finite-device advantage, specimen or historical novelty is inferred here.
