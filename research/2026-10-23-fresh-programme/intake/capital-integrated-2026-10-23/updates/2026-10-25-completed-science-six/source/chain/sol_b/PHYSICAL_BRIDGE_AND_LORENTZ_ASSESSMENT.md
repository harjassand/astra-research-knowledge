# Chain Theory physical coupling and Lorentz assessment

Private ASTRA assessment for Harjas, 25 October 2026. Sol B.

The finite readout can be embedded in a massless gauge theory, but that embedding leaves a measurable coupling coefficient free. The precise obstruction is a free coefficient of the gauge kinetic term even after the charge generator, its trace norm, the current, the massless pole, the Ward identity, and the dressed-to-bare ratio have all been fixed. This prevents the reported finite readout from being a derivation of the physical fine-structure constant on those premises alone.

The independently selected wider result, the Lorentz algebra, has a valid geometric construction. A real operator space carries a bilinear form with signature one against three, and its isometries give the Lorentz algebra. A deterministic quantum operation implementing its noncompact boosts on the finite link state space does not follow. Both the positive construction and that restricted operational obstruction are proved below.

## Source versions and scope

The primary editions are the 24-page [Alpha letter and supplement](https://alexwg.org/publications/ChainTheoryAlpha.pdf), dated 23 October 2026, and the 754-page [working compendium](https://alexwg.org/publications/ChainTheoryCompendium.pdf), also dated 23 October 2026. The exact PDFs independently downloaded for this assessment have SHA-256 hashes:

| Edition | SHA-256 |
| --- | --- |
| Alpha letter | `4bd42b02d8e7fc986c04a1dd2cb9d31fbf0f25b9df8bcf862b907dd45bc22009` |
| Compendium | `cdd99bf011bd908fc226591d7c69a62c08985dd30e126cf0b26c43b7cc5abbc9` |

The letter explicitly supplies no momentum-dependent propagator; its massless pole and electromagnetic identification enter through the Photon Conjecture. Its passage from hypercharge to electric charge, spacetime, and helicity is outside its scope. The supplement calls the field-theory correspondence a definitional identification. These are material conditions of the author's claim, rather than additional conditions invented by this assessment. See the [letter page 5](https://alexwg.org/publications/ChainTheoryAlpha.pdf#page=5) and [supplement pages 19–20](https://alexwg.org/publications/ChainTheoryAlpha.pdf#page=19).

The compendium's superseded Alpha chapters are not substitutes for the canonical letter. The present assessment of its wider result concerns Theorems 54.1 and 56.1, Open result 56.2, and instrument I.23, at their stated standings.

## A concrete finite realization of the reported readout

Write

\[
r=\frac{79+48\sqrt2+42\sqrt3+3\sqrt6}{31104}.
\]

Accepting the reported record multiplicities as inputs, the scalar has an elementary positive realization. Let \(\mathcal H_R=\mathbb C^{31104}\), equip it with the maximally mixed state \(\rho_R=I/31104\), and define

\[
M=\operatorname{diag}(1^{\times79},\sqrt2^{\times48},
\sqrt3^{\times42},\sqrt6^{\times3},0^{\times30932}).
\]

Then \(\operatorname{Tr}(\rho_R M)=r\) exactly. This constructs a legitimate finite quantum expectation value with the stated count. It does not independently establish that the source's record operators are those orthogonal directions; that is a separate mathematical audit. Since \(\|M\|=\sqrt6\), \(M\) itself is an observable rather than a probability effect. The effect \(M/\sqrt6\) is valid, with expectation \(r/\sqrt6\).

This construction makes a limited positive point: a finite, positive record statistic exists without any field theory. It also makes its physical type explicit. A dimensionless expectation value does not become a pole residue or a charge merely because all three are dimensionless.

The source's local link state is a vector on \(\mathbb C^3\otimes\mathbb C^2\), with Schmidt rank two. Shared ends use separate tensor copies and Bell-type projections. The finite construction has projections, unitary changes of basis, exchanges, and a normalized trace. It has no specified coordinate translation group, physical duration between acts, spatial metric, or dispersion relation. A conditional projection \(P\rho P/\operatorname{Tr}(P\rho)\) also needs its operational reading specified: in ordinary quantum mechanics it is a conditioned branch, whereas the model discards failure branches. That alternative law is permitted as a proposed foundation, but conventional quantum-field probability rules cannot then be imported without establishing compatibility.

## An exact family of electromagnetic completions

The following proposition is an original result of this assessment.

**Conditional bridge nonuniqueness.** Fix a positive number \(r\), a charge generator \(Q\) with \(B(Q,Q)=1\), and a conserved current \(J^\mu\) whose unit charges have been fixed. The requirements of a Lorentz-invariant massless abelian field, gauge invariance, a Ward identity, and a dressed-to-bare propagator ratio \(r\) do not determine the physical coupling. They admit the following family for every \(\kappa>0\).

Use Heaviside–Lorentz natural units \(\hbar=c=1\), keep the coefficient of the same source current equal to one, and take

\[
\mathcal L_{\rm bare}
=-\frac{\kappa}{4}F_{\mu\nu}F^{\mu\nu}-J^\mu A_\mu,
\qquad
\mathcal L_{\rm dressed}
=-\frac{\kappa}{4r}F_{\mu\nu}F^{\mu\nu}-J^\mu A_\mu.
\tag{1}
\]

Equivalently use the fixed invariant form \(B\) in these expressions and write \(F=F_QQ\). Its charge norm remains exactly one for every \(\kappa\).

After gauge fixing, the transverse propagators are

\[
D^{\rm bare}_{\mu\nu}(q)
=\frac{-i}{\kappa}\frac{P^T_{\mu\nu}(q)}{q^2+i0},
\qquad
D^{\rm dressed}_{\mu\nu}(q)
=\frac{-ir}{\kappa}\frac{P^T_{\mu\nu}(q)}{q^2+i0}.
\tag{2}
\]

Thus the same massless pole and the exact ratio \(D^{\rm dressed}/D^{\rm bare}=r\) occur for every positive \(\kappa\). The longitudinal terms vanish between conserved currents. Gauge transformations act as usual, and gauge invariance gives the ordinary Ward identities if charged matter is included with the same covariant derivative. There are two physical transverse polarizations.

For stationary unit charges, the field equation is

\[
\frac{\kappa}{r}\nabla\cdot\mathbf E=\rho.
\]

At separation \(R\), it gives

\[
V(R)=\frac{r}{4\pi\kappa}\frac{q_1q_2}{R},
\qquad
\alpha(0)=\frac{r}{4\pi\kappa}.
\tag{3}
\]

This is an observable difference. In particular,

\[
\kappa_1=\frac1{4\pi}\ \Longrightarrow\ \alpha_1=r,
\qquad
\kappa_2=\frac1{2\pi}\ \Longrightarrow\ \alpha_2=\frac r2.
\]

Both theories have the same normalized charge, current, finite statistic, massless pole, symmetry, and propagator ratio. Their Coulomb force differs by a factor two; their leading current-scattering cross sections differ by a factor four.

These are conditional effective-field completions of the proposed dictionary, not claimed complete models of the finite-qudit axiom. Their purpose is precise: even granting the missing standard propagation structures, the stated normalization data do not imply the desired coupling.

### Why this freedom is physical

The canonical field is

\[
A_{\rm can}=\sqrt{\kappa/r}\,A.
\]

Equation (1) becomes

\[
\mathcal L_{\rm dressed}
=-\frac14F_{\rm can}^2
-\sqrt{r/\kappa}\,J\cdot A_{\rm can}.
\]

Consequently \(e_{\rm physical}^2=r/\kappa\), which reproduces (3). A field rescaling can move the coefficient between the kinetic term and the interaction, but it preserves this measurable combination. Since the charge of \(J\) is held fixed, changing \(\kappa\) cannot be removed by renaming the field.

Likewise, on-shell residue normalization does not fix the coupling. Rescaling the photon to residue one moves its original residue into the vertex coefficient. The Ward identity constrains vertex and charged-field renormalizations; it does not select an overall gauge kinetic coefficient.

The letter's strongest normalization defense, \(B(Q,Q)=1\), fixes a generator norm. It does not prohibit multiplying a gauge-invariant kinetic action by \(\kappa\). A projection's success probability one fixes a probability normalization. Equating that probability to the physical bare fine-structure coupling is a bridge postulate, not a consequence of either normalization. In the family above,

\[
\alpha_{\rm bare}=\frac1{4\pi\kappa},
\qquad
\alpha(0)=r\alpha_{\rm bare}.
\]

Setting the former to one is exactly the extra equation \(\kappa=1/(4\pi)\). No choice of electromagnetic units removes the need for an equivalent physical equation.

The distinction between charge units and physical coupling is consistent with the [2026 Particle Data Group electroweak review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-standard-model.pdf), which treats gauge representations and gauge coupling coefficients separately. Its [physical constants table](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-phys-constants.pdf) specifies the conventional fine-structure constant and the Coulomb-derived observables.

## Momentum dependence and the photon representation

A static ratio cannot select running. For example, in Euclidean momentum the positive spectral family

\[
C_{a,m}(q)=P_T(q)\left[\frac r{\kappa q^2}
+\frac a{q^2+m^2}\right],\qquad a\ge0,\ m>0,
\tag{4}
\]

has the same massless residue for every \(a,m\), while its finite-momentum response varies. The second term is a positive massive-vector spectral contribution; it introduces no negative-residue pole. Local charged matter similarly changes vacuum polarization while leaving gauge invariance intact. Thus the record statistic and the Ward constraint alone do not fix \(q\)-dependence, thresholds, or decoupling.

There is also a representation problem to solve. The letter's supplement identifies the six-dimensional link representation as \((3,2)_{1/6}\), the left-handed quark-doublet representation. Its central \(Q\) acts on that whole link as a scalar, so conjugation on link observables is trivial. This does not supply the neutral helicity-one photon representation. A neutral collective excitation or a composite photon could still emerge; it requires a specified map from the charged link data to that excitation. The obstruction is not a simplistic claim that the model predicts an electrically charged photon: its selected generator has not yet been identified with electric charge.

Finite local Hilbert spaces do not by themselves forbid emergent photons. [Hermele, Fisher and Balents](https://arxiv.org/abs/cond-mat/0305401) give a concrete spin-one-half model with an emergent abelian gauge structure and a linearly dispersing collective photon. [Wiese's quantum-link account](https://arxiv.org/abs/2107.09335) describes finite link Hilbert spaces and their continuum limits. These constructions include a Hamiltonian, gauge constraints, and a controlled limiting argument. They show a viable kind of bridge while leaving the coupling to microscopic dynamics.

For Chain Theory, a sufficient next result would derive a transfer rule or Hamiltonian from the admitted Bell moves, obtain a transverse massless mode and a normalized charged probe, and calculate the current-to-current scattering amplitude. With the charge unit held fixed, the decisive target is

\[
\lim_{q^2\to0}
\frac{q^2\,J_T^\mu D_{\mu\nu}(q)J_T^\nu}
{4\pi\,J_T^\mu J^T_\mu}
=r,
\tag{5}
\]

with the usual continuation and overall \(-i\) removed consistently. This is a focused electromagnetic completion, rather than a requirement to reconstruct all of physics. Equation (2) evaluates its magnitude to \(r/(4\pi\kappa)\), displaying exactly what still needs fixing.

## The Lorentz algebra has a valid geometric completion

The compendium constructs the plain-trace Gram on a Hermitian unit and three anti-Hermitian directions. Theorem 54.1 gives its isometry algebra; Theorem 56.1 finds no order-to-direction mixing in the admitted matching closure; Open result 56.2 retains a condition on the form of the unit. Instrument I.23 repeats the algebra at each end of a qubit pair. See [pages 144–151](https://alexwg.org/publications/ChainTheoryCompendium.pdf#page=144) and [pages 702–703](https://alexwg.org/publications/ChainTheoryCompendium.pdf#page=702).

Here is an explicit independent reconstruction at the qubit pair. Let \(T_a=i\sigma_a/2\), and define the real vector space

\[
V=\operatorname{span}_{\mathbb R}
\{I_4,T_1\otimes I_2,T_2\otimes I_2,T_3\otimes I_2\}.
\]

For \(v=tI_4+\sum_a x_aT_a\otimes I_2\),

\[
\operatorname{Tr}(v^2)=4t^2-\lvert\mathbf x\rvert^2.
\tag{6}
\]

Thus its plain-trace Gram is \(G=\operatorname{diag}(4,-1,-1,-1)\). Rotations \(J_a\) of the three direction coordinates and boosts with nonzero entries

\[
(K_a)_{0a}=\tfrac12,\qquad (K_a)_{a0}=2
\]

obey \(X^TG+GX=0\),

\[
[J_a,J_b]=\epsilon_{abc}J_c,\quad
[J_a,K_b]=\epsilon_{abc}K_c,\quad
[K_a,K_b]=-\epsilon_{abc}J_c.
\tag{7}
\]

This is the Lorentz Lie algebra. More strongly, set

\[
H(v)=2tI_2+\mathbf x\cdot\boldsymbol\sigma.
\]

Then \(\det H=4t^2-\lvert\mathbf x\rvert^2\). The action

\[
H\longmapsto BHB^\dagger,\qquad B\in SL(2,\mathbb C),
\tag{8}
\]

preserves this determinant and gives the usual double cover of the proper orthochronous Lorentz group. This completes the abstract geometric interpretation, including finite boosts. Its validity does not depend on regarding the boost as a physical operation on the qubit.

The corresponding positive Hilbert–Schmidt form is instead

\[
\operatorname{Tr}(v^\dagger v)=4t^2+\lvert\mathbf x\rvert^2.
\tag{9}
\]

The negative signs in (6) result from the mixed Hermitian and anti-Hermitian real space and the choice of plain trace. They are not negative norms in the quantum Hilbert space. This distinction preserves the valid algebraic result without promoting it to spacetime dynamics.

## Two possible boost actions on a Bell pair

### The conjugate action changes its entanglement

Take the exact determinant-one boost spinor

\[
B=\operatorname{diag}(2,1/2),\qquad
|\Phi\rangle=(|00\rangle+|11\rangle)/\sqrt2.
\]

The natural continuation of the unitary matching action gives

\[
(B\otimes\bar B)|\Phi\rangle
=\frac{4|00\rangle+\tfrac14|11\rangle}{\sqrt2}.
\]

After normalization the reduced-state eigenvalues are

\[
\left(\frac{256}{257},\frac1{257}\right),
\]

so this state is not maximally entangled. Generally, under vectorization the output coefficient matrix is \(BB^\dagger\). Equal Schmidt coefficients require \(BB^\dagger\) to be scalar; with determinant one this requires \(B\) to be unitary. A nontrivial boost of this kind is therefore not an automorphism of the axiom's maximally entangled pair states.

This is a conditional no-go for that proposed physical action. It does not refute the coordinate action (8), and it does not imply that the compendium has claimed a deterministic implementation of this action.

### A reciprocal action preserves the pair but requires conditioning or a passive interpretation

The stronger alternative must be tested rather than omitted. For any invertible \(B\),

\[
(B\otimes B^{-T})|\Phi\rangle=|\Phi\rangle.
\tag{10}
\]

So nonunitarity alone does not rule out pair-preserving tensor covariance. For the explicit \(B\) above, however,

\[
K=B\otimes B^{-T},\qquad
K^\dagger K=\operatorname{diag}(1,16,1/16,1).
\]

It is neither a trace-preserving quantum channel with one Kraus operator nor a trace-nonincreasing Kraus branch at that scale. Scaling the local filters to contractions, \(B/2\) and \(B^{-T}/2\), makes the joint filter \(K/4\). Its success probability on \(|\Phi\rangle\) is exactly \(1/16\). The conditional output is again \(|\Phi\rangle\), but the operation is probabilistic on general inputs.

Normalizing a nonunitary filter cannot repair this as a deterministic linear channel. The filter \(B/2\) takes each computational-basis pure state to itself after conditioning. A fifty-fifty mixture of those normalized outputs is therefore \(I/2\). Filtering \(I/2\) and then normalizing gives \(\operatorname{diag}(16/17,1/17)\). The discrepancy proves nonlinearity.

There is a valid passive interpretation. Transform states as \(\rho'=B\rho B^\dagger\) and effects as \(E'=B^{-\dagger}EB^{-1}\). Then \(\operatorname{Tr}(\rho'E')=\operatorname{Tr}(\rho E)\), but a normalized measurement now sums to

\[
\sum_i E_i'=B^{-\dagger}B^{-1}
\]

instead of \(I\). The order unit, or equivalently the normalization and dual structure, has transformed. Equation (10) can likewise be a change of basis on contracted tensor indices. Neither interpretation is a new deterministic physical operation with the original fixed state and measurement normalization.

This separation between Lorentz transformations and conditioned filtering already has a precise antecedent in [Verstraete, Dehaene and De Moor](https://arxiv.org/abs/quant-ph/0011111). Their two-qubit Lorentz correspondence includes the normalization step explicitly.

## The restricted operational no-go and the available exits

A stronger general statement is available under clear assumptions. A connected nontrivial Lorentz group cannot act by reversible deterministic quantum channels on one fixed finite-dimensional quantum state space while preserving its usual probabilities. Such reversible channels are unitary conjugations. A nontrivial finite-dimensional unitary representation of the Lorentz Lie algebra would induce a positive invariant inner product on that algebra. But \(\operatorname{ad}K_3\) sends \(J_1\mapsto K_2\) and \(K_2\mapsto J_1\), so it has real eigenvalues \(+1,-1\). Invariance of a positive inner product would make every adjoint map skew-adjoint, whose eigenvalues are purely imaginary. This is a contradiction.

This does not forbid ordinary finite-dimensional spinor or vector coordinate representations; these are nonunitary and have exactly the distinct role shown in (8). It also does not forbid an emergent spacetime symmetry acting on a larger limiting state space. The available exits are therefore concrete:

1. Retain the Lorentz result as geometric covariance, while deriving how coordinates, clocks, instruments, and translations reconstruct from the network.
2. Supply a controlled continuum or thermodynamic limit in which the physical state space supports a unitary Poincaré action, with the finite spinors remaining local coordinate representations.
3. Adopt conditioned nonunitary operations as fundamental and derive a consistent probability and causal law for them. This changes the operational assumptions and must be carried through the photon and coupling construction.

The compendium's own open conditions around the unit and admitted mixing make the first two routes the strongest conservative interpretations. The finite Lorentz algebra is accepted at its mathematical scope. Operational Lorentz invariance and the photon dynamics remain uncompleted, with the specific obstruction and possible mathematical exits now identified.

## Reproduction and assessed status

Run `replay_physical_bridge.py` in this directory with Python 3. It uses exact rational matrices and the standard library. The saved `replay_results.json` records the source hashes, both Gram matrices, all rotation and boost brackets, an exact finite coordinate boost, both Bell-pair actions, the conditioning probability, and numerical values of the coupling family.

The replay passes. It obtains

\[
r^{-1}=137.0359991895661550291837440208667995664\ldots,
\]

and the reciprocal filter success probability \(1/16\).

| Claim | Assessment |
| --- | --- |
| Positive finite realization of the stated weighted scalar | Constructed, conditional on the source's multiplicities |
| Massless abelian effective propagator incorporating that scalar | Constructed after adding Maxwell dynamics |
| Same charge normalization and propagator ratio force \(\alpha(0)=r\) | Disproved for the stated bridge requirements by the \(\kappa\) family |
| Full finite axiom is inconsistent or has no possible electromagnetic completion | Not established by this assessment |
| Lorentz algebra as the isometries of the selected mixed real space | Independently reconstructed |
| Nontrivial boosts are deterministic operations on the fixed finite pair state space | Ruled out under the stated quantum operational assumptions |
| Physical Lorentz covariance, helicity-one photon, and fixed electromagnetic coupling | Not derived here or supplied by the assessed correspondence |

These results support continued focused mathematical work on a bridge. They do not convert the candidate's experimental agreement into a completed electromagnetic derivation.
