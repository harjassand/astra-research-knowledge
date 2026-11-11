# P1 available return — 12 November 2026 Brisbane

Source: https://chatgpt.com/c/6af464b1-3360-83ec-8c1b-9b4b95c398ff, Pro. Final e07b6d82-bef9-5d3a-aa33-aed7c65a07cc, answering user 7340db3d-5046-473d-8c21-d912bab327f3. Exact actual question is held at `P1_FULL_ORIENTED_PATCHY_GEOMETRIC_ASSEMBLY_PRO_20261112.txt` (posted with one approved terminal LF omitted).

## Available visible activity

Previously observed visible activity items: "Developed a labelled lattice model"; "Developed native input-copy module"; "Checked geometry constraints and designed reversible contact gates"; "Tested two-contact verification limits and defined unique receptor ports". Additional activity and expanded helper contents were not captured. The UI showed 12 subagents and no outputs; original archive availability and identity are unknown. No attachment was listed in the native thread.

## Full response copied from the UI

**I do not have a complete affirmative construction or an obstruction to every admitted architecture.** Physical orientation patches do, however, let me establish native operations that go beyond the previously supplied sensor and accounting results:

- A reversible two-carrier gate can compute an exact finite truth table under the stated rate faults.
- Inactive feedstock can undergo a correctly labelled **physical capture that creates a real energetic bond**, from arbitrary feasible positions and orientations, with a polynomial first-completion deadline and logarithmic reliability overhead.
- A separate fixed-affinity module can create and retain a high fraction of correctly copied material states throughout a prescribed interval, with logarithmic redundancy and every reverse event included.

These results still leave the central geometric step unproved: an autonomously constructed spatial structure that preserves **address, ordering, physical connectivity and shape** while it grows and repairs itself. I cannot legitimately replace that step with an abstract tile decoder, a chemical count computation, or a mixing assertion for an attractive aggregate.

Below I give the new constructions and their proofs, then identify precisely where they stop.

## 1. Finite logical gates can be exact in this model

The permitted channel catalogue is more powerful than a noisy energetic sensor when both inputs are carried by the two participating carriers.

For example, let one carrier have input conformation \(X_a\), and another have conformation \(Y_{b,\varnothing}\), where \(a,b\in\{0,1\}\). Include the four reversible channels

\[
X_a+Y_{b,\varnothing}
\rightleftarrows
X_a+Y_{a,b,a\wedge b}.
\]

The output retains both inputs, so this is an injective local operation. Give these logical conformations identical mechanical interaction energies. On a fixed physical contact patch, use

\[
q_+=\nu e^{\mu/2},
\qquad
q_-=\nu e^{-\mu/2}.
\]

Then \(\Delta E=0\) and

\[
\log(q_+/q_-)=\mu
\]

holds exactly.

Every forward firing computes the correct Boolean value of its **actual two inputs**. Every reverse firing uncomputes. Multiplying these rates by arbitrary predictable factors changes timing and backtracking; it cannot create a transition absent from the catalogue.

This is compatible with the contract’s structural zeros. It does not assume an external neighbourhood evaluator: there are only four explicitly listed two-carrier reactions. Nor does it require an input carrier to be held mechanically fixed.

Immutable input types \(A_0,A_1\) are similarly legitimate: omit channels that change their types, while retaining the reverse of every channel that is present. An interaction can then copy an input without chemically altering it.

The limitation is physical association. A correct gate applied to the wrong tape cell or wrong growth site can still corrupt the computation. Thus the key missing protection is not necessarily Boolean correctness. It is the preservation of the intended physical partners and their addresses.

## 2. A native capture-and-write construction

Here is a concrete fixed module that starts with genuinely inactive feedstock and creates an actual energetic bond.

### 2.1 Fixed geometry and potential

Choose microscopic units with

\[
r_*=1,\qquad R_*=4.
\]

Use immutable input types \(A_0,A_1\), and a reader type \(Y\) with conformations \(I,0,1\). An inactive reader \(Y_I\) has zero interaction energy with every carrier. It is therefore unbonded at every allowed initial placement.

For an input–reader pair define

\[
z=R_A^{\mathsf T}(Q_Y-Q_A),\qquad
T=R_A^{\mathsf T}R_Y,
\]

and

\[
z_*=3e_1,\qquad
\psi(z,T)=|z-z_*|^2+\|T-I\|_F^2.
\]

Choose the following fixed \(C^3\) cutoff:

\[
s(u)=
\begin{cases}
1,&u\le 1/64,\\[2mm]
1-35t^4+84t^5-70t^6+20t^7,
&1/64<u<1/32,\quad t=64u-1,\\[2mm]
0,&u\ge 1/32.
\end{cases}
\]

Define the active input–reader potential by

\[
U(z,T)=s(\psi(z,T))[-64+16\psi(z,T)].
\]

Both active reader conformations have this potential with either input type. Reader–reader potentials vanish. Reverse type ordering is defined by

\[
U_{Y,A_b}(z,T)=U_{A_b,Y}(-T^{\mathsf T}z,T^{\mathsf T}),
\]

which gives the required exchange symmetry.

This potential has the following properties.

- It lies in \([-64,0]\).
- Its positional support is contained in the range-four interaction ball.
- It has fixed computable \(C^3\) bounds.
- Near \((3e_1,I)\), its Hessian controls all six relative pose directions.
- It uses a body-frame direction, not a prescribed laboratory orientation.

Declare the energetic-bond interval to be

\[
[-64,-64+1/8].
\]

Every pose in this interval lies in the small quadratic neighbourhood \(\psi\le1/128\), where the relative-pose Hessian is uniformly positive. Thus this construction satisfies the stiffness requirement throughout its designated bond region.

Use the fixed reaction-contact condition

\[
\mathcal A=\{\psi\le1/256\}.
\]

This is a physical pose patch with fixed geometry. It does not inspect a larger neighbourhood or depend on the blueprint.

### 2.2 Single occupancy follows from hard exclusion

Throughout the potential support, the reader centre lies within distance \(1/\sqrt{32}<1\) of \(Q_A+R_Az_*\). Two radius-one readers cannot both occupy that region.

Consequently, one input carrier has at most one interacting reader at a time. In particular, with one input and arbitrarily many readers, the total interaction energy remains between \(-64\) and \(0\).

This is useful both mechanically and for event accounting. Single occupancy is enforced by the actual carrier geometry; no software arbitration is supplied.

### 2.3 Reversible activation, copying and genuine power

Fix once

\[
\delta_*=\frac1{16},
\qquad
\nu=2^{-80},
\]

and a fuel/waste chemical-potential difference of \(32\).

For \(b=0,1\), include the pose-gated channel

\[
A_b+Y_I+F
\rightleftarrows
A_b+Y_b+W
\]

with rates, on \(\mathcal A\),

\[
q_{F,+}=\nu \exp\!\left(\frac{32-U}{2}\right),
\qquad
q_{F,-}=\nu \exp\!\left(\frac{U-32}{2}\right).
\]

The carrier energy change is exactly \(U\), so

\[
\log\frac{q_{F,+}}{q_{F,-}}=-U+32.
\]

Use counting measure on the discrete carrier states, feasible Lebesgue measure on centres, and normalized Haar measure on body frames. The transition changes neither positions nor orientations, so the forward and reverse reference measures agree.

Also include a separately labelled zero-affinity channel on the same state pair:

\[
A_b+Y_I
\rightleftarrows
A_b+Y_b,
\]

with rates

\[
q_{0,+}=\nu e^{-U/2},
\qquad
q_{0,-}=\nu e^{U/2}.
\]

The cycle consisting of fuelled activation followed by neutral reset has affinity \(32\). It consumes fuel without a net carrier-state change. This supplies an actual driven cycle, even though combining parallel edges can conceal that cycle in an aggregate two-state description.

All these rates are bounded by one. For example,

\[
q_{F,+}\le 2^{-80}e^{48}<1.
\]

Every admitted transition has its positive reverse at the same physical state pair.

Starting with one \(A_b\) and all readers in \(I\), the only reachable reader states are \(I\) and \(b\). Therefore **the first activation writes the contacted input bit exactly**.

At that event, \(\psi\le1/256\), and the newly activated potential lies inside the declared energetic-bond interval. A real bond is created at the existing relative pose. No carrier is relocated. The activation does exert mechanical backaction afterward, but that backaction is bounded and charged.

This construction assumes a correctly specified input type \(A_b\). It does not yet provide the full seed code tolerating corrupt input blocks.

## 3. Polynomial capture from arbitrary positions and orientations

The first-completion estimate can be proved without a mixing theorem for an attractive aggregate.

Let \(n\ge2\) be the total carrier count. Choose a polynomially dilute cube large enough for the accepted hard-ball Poincaré and all-start mixing bounds.

### 3.1 Before first activation, the energy is zero

Until the first activation, every reader is inactive. Thus

\[
E=0.
\]

The positional process is exactly the accepted unpowered hard-ball process with the unknown inhomogeneous mobilities. The orientations are independent time changes of Brownian motion on \(SO(3)\). Position and orientation processes are independent during this interval.

The common invariant reference for this uninterrupted pre-activation motion is

\[
\pi=
\text{normalized feasible hard-ball volume}
\otimes
\text{product normalized Haar measure}.
\]

Let

\[
C_P\le P_{\rm H}(n,L_{\rm box})
\]

be the explicit polynomial Poincaré bound supplied by the accepted hard-ball theorem, after adding the fixed Haar Poincaré constant by tensorization. No normalizer is evaluated.

### 3.2 A contact patch has inverse-polynomial reference probability

Tag one reader for analysis only. This does not give it a special physical type or address.

For \(L=L_{\rm box}\), consider the event that:

- the input centre lies in \([4,L-4]^3\);
- the tagged reader’s relative displacement lies in \(B_{1/32}(3e_1)\);
- its relative rotation angle is at most \(1/64\).

These conditions imply \(\mathcal A\), wall clearance and pair clearance.

Under independent uniform centre proposals, this event has probability at least a fixed constant times \(L^{-3}\). Conditioned on that allowed input–reader pair, the remaining centres are still independent uniform proposals. An overlap union bound bounds their feasibility failure by

\[
C n^2/L^3.
\]

A sufficiently dilute polynomial cube makes this at most \(1/2\). Dividing by the overall feasibility probability cannot reduce the resulting lower bound, because that denominator is at most one.

A conservative rational bound is

\[
p:=\pi(\mathcal A)\ge 2^{-40}L^{-3}.
\]

The elementary overlap estimate already holds for \(L\ge16n\); the cube can be enlarged further to meet the accepted Poincaré hypothesis.

This conditional argument matters. Subtracting a global excluded-volume error from a contact event of probability \(O(L^{-3})\) would not establish the needed lower bound.

### 3.3 Predictable faults are handled by a lower contact hazard

On \(\mathcal A\), the actual fuelled activation rate is at least the fixed rational constant

\[
q_0=2^{-81}.
\]

Therefore, before first activation, its total hazard dominates

\[
q_0\,1_{\mathcal A}(Q(t),R(t)).
\]

The lower clock can be introduced by thinning. This remains valid when the actual rate multipliers depend on the complete past and external randomness. It does not assert that positions conditioned on survival have equilibrium distribution.

### 3.4 A killed-form estimate

For \(f\in H^1(\pi)\), write \(\bar f=\int f\,d\pi\). Since

\[
p\bar f^{\,2}
\le
2\int_{\mathcal A}f^2\,d\pi
+
2\operatorname{Var}_\pi(f),
\]

the Poincaré inequality gives

\[
\|f\|_2^2
\le
\frac{3C_P}{p}\int|\nabla f|^2\,d\pi
+
\frac2p\int_{\mathcal A}f^2\,d\pi.
\]

The unknown instantaneous diffusion form satisfies

\[
\mathcal E_t(f,f)\ge d_0\int|\nabla f|^2\,d\pi.
\]

Hence the process killed at rate \(q_0 1_{\mathcal A}\) has uniform coercivity

\[
\mathcal E_t(f,f)+q_0\int_{\mathcal A}f^2\,d\pi
\ge
\lambda\|f\|_2^2,
\]

where

\[
\lambda=
\frac{p}{3C_P/d_0+2/q_0}.
\]

Its time-ordered killed evolution consequently contracts in \(L^2(\pi)\) by \(e^{-\lambda(t-s)}\). This uses instantaneous symmetry and the common reference measure; it does not assume that the non-autonomous evolution is selfadjoint.

In particular, \(\lambda^{-1}\) has a fixed polynomial bound in the paid parameters.

### 3.5 From every initial configuration

Use the accepted positional all-start mixing bound to obtain total variation at most \(1/8\), uniformly in the starting time.

For orientations, the \(SO(3)\) heat-kernel expansion has spectral factors \(e^{-\ell(\ell+1)t}\), up to the fixed metric normalization. It gives a one-carrier bound \(Ce^{-cd_0t}\) after a fixed initial rotational time. Product total variation is therefore at most \(Cn e^{-cd_0t}\). This adds only \(O(d_0^{-1}[1+\log n])\) to the required mixing time. [mdpi.com](https://www.mdpi.com/2227-7390/11/8/1958?utm_source=chatgpt.com)

Let \(t_0\) be a rational polynomial upper bound making the joint position–orientation law within \(1/4\) of \(\pi\). Let \(\underline\lambda\) be the rational lower bound obtained by inserting

\[
p\ge2^{-40}L^{-3}
\]

and the paid polynomial majorant for \(C_P\).

In an interval of length

\[
B=t_0+2\underline\lambda^{-1},
\]

the probability of no activation is at most

\[
\frac14+e^{-2}<\frac12.
\]

Ignoring killing during the first \(t_0\) only enlarges the mathematical survival bound. That entire interval remains present in the actual process and its costs.

All bounds are uniform in starting configuration, starting time and past history. Iterating therefore gives

\[
\boxed{\Pr(\tau_{\rm cap}>kB)\le2^{-k}},
\qquad
\boxed{\mathbb E\tau_{\rm cap}\le2B}.
\]

A rational deadline

\[
T_{\rm cap}
=
B\left(1+\left\lceil\log_2\frac1{\xi}\right\rceil\right)
\]

ensures a correct physical capture by that time with probability at least \(1-\xi\). Its dependence on the reliability request is logarithmic.

Crucially, this is a **first-completion theorem**. The bond may subsequently break or be reset. It does not say that the bond is present at the deadline, much less throughout a retention interval.

### 3.6 All actual costs of this module

With one input port, at most one reader is eligible at a time. At most two channel labels apply to its current state, so the total faulty event intensity is less than three. Thus, for every physical \(t\),

\[
\mathbb E F_{\rm all}(t)\le3t.
\]

Each fuelled event transfers at most two bath molecules and has absolute bath work \(32\). Hence

\[
\mathbb E F_{\rm transfers}(t)\le6t,
\qquad
\mathbb E W_{\rm bath}(t)\le96t.
\]

The accepted bounded-palette existence and work result applies after activation as well as before it. It pays all escaped readers, resets, rebinding attempts and rare excursions. In particular,

\[
\mathbb E[W_{\rm wall}(t)+W_{\rm pair}(t)]
\le
C_*(1+n)^5(1+\Lambda)^3(1+L)^{12}d_0^{-7}(1+t).
\]

Particle time, positional and rotational quadratic variations, force and torque actions, and drift variations have their stated \(O(n t)\) or \(O(\Lambda n t)\) bounds with fixed palette constants.

Consequently, every charged cost through \(T_{\rm cap}\) is polynomial in

\[
n,\ d_0^{-1},\ \Lambda,\ \log(1/\xi)
\]

when the cube is chosen polynomially. No equilibrium sampler, configuration-volume computation or trajectory search is used.

## 4. Cold-start retention of a pool of copied material states

A second module gives an all-time retention estimate. It also exposes why reliable chemical information is insufficient for the requested object.

Use a reader type whose conformations

\[
Y_\varnothing,\quad Y_0,\quad Y_1
\]

have identical, zero interaction energies. Keep their mobility fields identical by making them conformations of the same carrier type.

There is one immutable input \(A_b\), and \(M\) initially blank readers. Within the same fixed pose-contact window, use fuelled and neutral parallel copying channels. With affinity \(32\), their combined nominal forward and reverse rates are

\[
q_+=\nu(e^{16}+1),
\qquad
q_-=\nu(e^{-16}+1).
\]

The two separately labelled routes retain their respective local detailed-balance identities. The fuelled-copy/neutral-reset cycle has affinity \(32\).

The energy remains zero at all times. Thus the geometric process is independent of the copying and erasure clocks.

### 4.1 A comparison valid for correlated adaptive faults

Put

\[
a=(1-\delta_*)q_+,\qquad
b=(1+\delta_*)q_-,
\qquad
p_{\rm blank}=\frac{b}{a+b}.
\]

For reader \(j\), define its actual contact occupation clock

\[
C_j(t)=\int_0^t1_{\mathcal A_j}(Q(s),R(s))\,ds.
\]

Couple its actual “correctly filled” indicator from below by a two-state chain having forward rate \(a\) and reverse rate \(b\), run on \(C_j\).

The coupling is monotone: actual filling is at least as fast, and actual erasure is at most as fast, as in the comparison chain. This remains true when the actual rate factors inspect all reader histories.

Conditioned on the entire geometric path, the comparison chains are independent. Their blank probabilities are exactly

\[
p_{\rm blank}
+
(1-p_{\rm blank})e^{-(a+b)C_j(t)}.
\]

Independence is used only for these comparison chains. The actual reader states may be strongly correlated by the fault policy.

### 4.2 Filling from a genuinely blank start

Fix a small architecture constant \(\vartheta>0\), for example \(2^{-10}\). The fixed affinity above makes \(p_{\rm blank}\) much smaller than \(\vartheta/16\).

Choose a fixed occupation threshold \(u_0\) so that

\[
p_0:=
p_{\rm blank}
+
(1-p_{\rm blank})e^{-(a+b)u_0}
\le\vartheta/8.
\]

The killed-form argument also bounds contact occupation:

\[
\mathbb E e^{-(a+b)C_j(T)}
\le
2^{-\lfloor T/B'\rfloor},
\]

for a polynomial time constant \(B'\). Therefore

\[
\Pr(C_j(T)<u_0)
\le
C\,2^{-\lfloor T/B'\rfloor}.
\]

A union bound shows that all \(M\) readers have accumulated at least \(u_0\) contact time, except with probability

\[
CM\,2^{-\lfloor T/B'\rfloor}.
\]

No external measurement decides when this happens. The compiler simply chooses a deterministic deadline from the uniform bound.

### 4.3 Retention throughout a continuous interval

On the event above, every comparison reader’s blank probability remains at most \(p_0\) for all later times. Conditional Chernoff bounds make a blank fraction at least \(\vartheta\) exponentially unlikely in \(M\).

To cover every time in a continuous hold interval, count entrances into that bad set. Each entrance occurs at an erasure event. At most \(d_*\) readers can contact the input simultaneously, so the relevant erasure intensity is at most \(bd_*\). Conditional independence of the comparison readers gives

\[
\Pr\!\left(
\exists t\in[T,T+\tau]:
\#\{j:Y_j(t)=Y_b\}<(1-\vartheta)M
\right)
\]

\[
\le
CM\,2^{-\lfloor T/B'\rfloor}
+
C(1+bd_*\tau)e^{-cM}.
\]

Thus choosing

\[
M=O\!\left(\log\frac{1+\tau}{\xi}\right),
\qquad
T=B'\,O\!\left(\log\frac{M}{\xi}\right)
\]

makes the entire-interval failure probability at most \(\xi\).

This is a fixed-palette, fixed-affinity, cold-start retention result for **actual carrier conformations**. Every erasure, recopy and fuel cycle remains in the dynamics. The all-path costs are polynomial.

But these readers are mobile and unbonded. The result supplies neither a spatial address nor a voxel. It therefore cannot serve as the requested fabrication theorem.

## 5. The missing geometric theorem is now more specific

The constructions above remove several possible sources of difficulty: a native contact gate, arbitrary initial orientation, elementary logical correctness, first capture, and retained copied material states.

They do not construct a scalable physical structure whose ports keep their intended identities.

A suitable next theorem would need an autonomously extensible structure, made from the fixed palette, with a bound of the form

\[
\Pr(\text{address, ordering, connectivity or macrogeometry fails})
\le
\operatorname{poly}(B)e^{-c m^\alpha}
\]

over a budget \(B\), using width or redundancy parameter \(m\), while construction, extension and repair take polynomial resources.

The failure event must include:

- bond breaking and peeling;
- pose slips and accumulated deformation;
- joining the wrong ends of broken structures;
- a reader contacting the wrong address;
- incoming feedstock, poisoning and spurious assemblies;
- preparation corruptions;
- disturbance of the support during reading and repair;
- damage to the distinguished root’s connection to the product.

A sufficiently strong theorem of this kind could support a blueprint interpreter and geometric growth programme. A bundle of many bonds suggests an exponential cut-size estimate, but that suggestion does not prove the required dynamics. In particular, a bundle may peel, exchange partners or deform without simultaneously breaking a large predetermined cut.

### Attractive aggregates are a new quantitative problem

The accepted hard-ball theorem controls uniform feasible volume. For a fixed discrete state with an extensive interaction energy, a direct comparison gives only

\[
C_P(e^{-E}\pi_0)
\le
e^{\operatorname{osc}E}C_P(\pi_0).
\]

Fixed packing bounds \(\operatorname{osc}E\) by \(O(n)\), which can still give an exponential estimate.

That estimate is neither a polynomial mixing theorem nor a lower bound proving slow operation. An active architecture may avoid global equilibration entirely. It does show why the uniform hard-ball result cannot simply be reapplied to a growing attractive tape or solid.

### The product-scale restriction needs separate attention

The allowed block scale satisfies

\[
b/r_*
\le
C\left[1+\log\frac{N(1+\tau_{\rm hold})}{\epsilon}\right]^q.
\]

It does not contain \(d_0^{-1}\) or \(\Lambda\).

Consequently, choosing the physical product width from \(\log T_{\rm build}\) is not automatically admissible when the build time grows because transport is slow or irregular. A complete architecture must separate controller redundancy and waiting resources, which may depend on the full \(R\), from the required scale of the product itself.

The module results above do not resolve that separation.

### Abstract universality does not supply the missing physical structure

The primary comparisons remain useful, but their hypotheses matter:

| Result | What it supplies | What remains to be implemented here |
|---|---|---|
| Alseth–Hader–Patitz | A universal abstract 3D decoder with base, shape, filler and decoding tiles | Its tiles occupy discrete lattice poses; signals have one-shot semantics; attachments use a stability threshold; supplies are unbounded. Brownian pose wells do not inherit those guarantees. |
| Gács | Asynchronous fault-tolerant computation and information storage with finite local states | The cellular sites and their adjacency are already part of the model. Here the carriers must construct and preserve that physical adjacency. |
| Zhu–Du–King–Brenner | Patchy-particle proofreading mechanisms and improved simulated assembly yields | Their studied finite assemblies and local state-update rules do not establish a fixed native interpreter or a universal geometric reliability theorem. |

These are scope distinctions, not criticisms of those results. The STAM model explicitly gives lattice embeddings, one-shot signals and threshold-stable supertiles; Gács constructs a reliable cellular automaton; the patchy-particle study uses a finite ladder assembly and programmed neighbourhood-dependent state changes. [Springer Nature Link](https://link.springer.com/article/10.1007/s11047-024-09987-0?utm_source=chatgpt.com)

## 6. I also do not have a universal negative

Several tempting negative arguments fail to cover the allowed class.

**Fixed energies and fixed bath affinities do not by themselves prevent exponentially reliable information.** The retained-pool construction above is a counterexample to that broad claim: growing redundancy and actual repeated fuel use can give exponentially small failure at fixed microscopic parameters.

**Passive bending arguments do not cover all supported products.** Your contract permits support structures assembled during the run. Such structures may influence the product through steric or repulsive contacts without belonging to the root’s energetic-bond component. A theorem for an unsupported thin rod does not exclude that possibility.

**A microscopic root is a serious vulnerability, but I have not turned it into an all-design obstruction.** There is a useful conditional observation. Suppose, more strongly, that for every fixed relative position, all orientations counted as bonded satisfy

\[
\operatorname{Hess}_T U\succeq kI,
\]

while globally \(\|\operatorname{Hess}_T U\|\le M\). Integrating \(\Delta_TU\) over Haar measure then gives

\[
\operatorname{Haar}(\text{unbonded orientations})
\ge \frac{k}{M+k}.
\]

For a held local geometry, rotating a bounded number of neighbours can consequently isolate a microscopic root with a controlled probability. Positional caging does not prevent those rotations.

However, the actual neighbours move, their identities can change, and local channels can alter the wells. A fixed-geometry angular calculation does not provide a lower bound for that full process. Also, stiffness near a preferred pose does not automatically imply the stronger angular hypothesis throughout every configuration an architecture might classify as bonded.

The required lower bound would not have to be constant. With fixed \(N,\tau_{\rm hold},d_0,\Lambda\) and \(\epsilon=2^{-k}\), the resource contract gives

\[
N_{\rm total}\le C(1+k)^q.
\]

A universal failure probability \(N_{\rm total}^{-c}\) would already contradict the requested reliability for large \(k\). I have not proved such a bound for every admitted architecture, including autonomously constructed supports and alternative bond designs.

**The full fabrication question therefore remains unproved in this answer.** The new results supply actual reversible capture, exact local logic and retained copied material states with paid costs. What they do not supply is the native, scalable geometric protection needed to turn a canonical information seed into an addressed growing solid and keep that solid correct for the entire retention interval. I have neither constructed that protection nor ruled out every way of achieving it.