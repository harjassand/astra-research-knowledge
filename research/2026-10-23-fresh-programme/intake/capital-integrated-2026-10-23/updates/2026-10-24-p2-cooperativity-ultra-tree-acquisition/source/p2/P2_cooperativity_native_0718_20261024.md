**Retained sleeve order can control the sign of equilibrium binding cooperativity in a single, explicit contact model.** The strongest construction now has exactly matched single-site affinities in its aligned-guide limit, yet one retained order makes the second connection less favorable and another makes it more favorable. Small positive guide and docking clearances preserve the opposite signs, although exact matching of the single-site affinities is then only a limiting result.

The resulting operation is **a persistent choice of how exchangeable contacts cooperate**. Removing the external guests leaves that choice stored in the sleeve order; restoring the guest reservoir restores the corresponding binding law. This is a local constitutive result. A branching material, a mechanism for rewriting the order, and useful molecular exchange rates remain separate requirements.

## 1. A physical construction that makes the inventory matter

The testbed is a straight, keyed guide carrying three closed collars between end stops. Two collars, \(A_L\) and \(A_R\), can bind external guests. The third, \(B\), is a passive spectator. Compare the prepared orders

\[
A_L\,B\,A_R
\qquad\text{and}\qquad
B\,A_L\,A_R.
\]

The components, binding chemistry, guide length and active-collar orientations are identical. Only the spectator’s retained position in the sequence changes.

A close-fitting square guide permits axial sliding while preventing the collars from freely rotating. The collars cannot pass one another or escape over the stops. Each active collar carries an outboard docking fixture. Its bound guest has a spherical protrusion displaced axially toward the other active collar. The two protrusions occupy opposite sides of the guide, so they can coexist without colliding with each other.

This makes the two orders physically different:

- In \(A_LBA_R\), the guests intrude into **two separate gaps**, one on each side of the spectator.
- In \(BA_LA_R\), both guests require clearance in **the same gap** between the active collars.

The guests therefore either consume separate portions of the available sliding space or share one restriction.

The model uses rigid-body exclusion and a short-range attraction at the docking contact. Forces, permissible docking poses and sleeve restrictions follow from those same bodies. The equilibrium weights are calculated from their accessible configurations; they are not independently assigned binding functions.

For the explicit example, the model dimensions are:

| Quantity | Value |
|---|---:|
| Usable guide length | \(165\ \mathrm{nm}\) |
| Length of each collar | \(35\ \mathrm{nm}\) |
| Total free axial length, \(F\) | \(60\ \mathrm{nm}\) |
| Collar outer half-width | \(12\ \mathrm{nm}\) |
| Guest-sphere radius | \(7\ \mathrm{nm}\) |
| Sphere-center distance from guide axis | \(16\ \mathrm{nm}\) |
| Sphere’s axial offset from its active collar | \(30\ \mathrm{nm}\) |

These specify a rigid-body testbed, not a fabricated DNA structure.

The sphere lies \(4\ \mathrm{nm}\) beyond the neighboring collar’s side face. Its axial intersection with that face extends by

\[
\sqrt{7^2-4^2}=\sqrt{33}\ \mathrm{nm}.
\]

Consequently, binding requires an additional gap

\[
\delta
=30-\frac{35}{2}+\sqrt{33}
=18.24456\ \mathrm{nm}.
\]

The same geometry leaves the sphere clear of its own collar, the guide, the stops and more distant collars. It supplies an actual local contact that converts guest occupancy into a demand on sliding space.

## 2. Full sliding equilibrium gives opposite cooperativity

Three ordered, aligned collars have four nonnegative gaps whose sum is \(F\). Their accessible axial configuration volume is proportional to \(F^3\). Requiring a total additional gap length \(D\) therefore retains the fraction

\[
f(D)=\left(1-\frac{D}{F}\right)_+^3.
\]

This is the hard-body configuration volume. No Gaussian-chain assumption is needed.

For either retained order, either guest alone requires one gap of size \(\delta\), giving

\[
q_L=q_R=q=f(\delta)=0.337043.
\]

The double-bound weights differ:

\[
q_{LR}^{\,A_LBA_R}=f(2\delta)=0.0601662,
\]

whereas

\[
q_{LR}^{\,BA_LA_R}=f(\delta)=0.337043.
\]

Define the site-resolved coupling ratio

\[
\kappa=\frac{q_{LR}}{q_Lq_R}.
\]

The common intrinsic docking affinity cancels:

| Retained order | Single-site factor \(q\) | Double-bound factor \(q_{LR}\) | Coupling \(\kappa\) |
|---|---:|---:|---:|
| \(A_LBA_R\) | 0.337043 | 0.0601662 | **0.529641** |
| \(BA_LA_R\) | 0.337043 | 0.337043 | **2.966980** |

Thus the first order gives negative cooperativity and the second positive cooperativity, after integrating over all allowed axial positions.

I checked the gap reduction against direct sphere–box collision calculations on four million independently sampled collar configurations. The direct contacts and gap conditions disagreed on **zero configurations**; the sampled equilibrium coefficients agreed with the analytic values within sampling error. That check verifies the contact reduction, rather than merely sampling the assumed gap formula.

### A concrete binding consequence

For a dilute guest reservoir, let \(w=cK_{\mathrm{dock}}\) be the common intrinsic association activity. In the dilute association description,

\[
\Xi=1+2wq+w^2q_{LR}.
\]

At the same activity \(w=1/q\), the predicted occupancy distributions are:

| Retained order | Empty | One guest, either site | Two guests |
|---|---:|---:|---:|
| \(A_LBA_R\) | 28.3% | 56.7% | **15.0%** |
| \(BA_LA_R\) | 16.8% | 33.5% | **49.7%** |

These are equilibrium model predictions, not experimental yields.

The useful distinction is that **the low-occupancy, single-contact response is matched while the response to joint occupancy changes substantially**. After all guests leave, the collars recover their unbound sliding space but retain their order. The binding curve associated with that order can reappear on subsequent exposure. The construction does not yet provide an operation that converts one retained order into the other.

## 3. The dock now supplies its own registration and release path

A favorable protrusion position would be insufficient if an ordinary chemical contact allowed the guest to attach in other orientations. I therefore replaced the freely swiveling contact with an explicit key and socket.

The active collar carries an outward-pointing rectangular key, displaced sideways from the intrusive sphere’s path. The guest carries a complementary socket. The only attractive patch is buried on the socket’s closed inner bottom; its partner is on the key tip. The socket walls are thicker than the attraction’s capture range.

This closes two earlier loopholes:

- An exposed shoulder patch could have stabilized attachment without full registration.
- An incorrectly oriented key or connector could have obstructed removal, even when the final bound pose was collision-free.

In the corrected construction, the guest withdraws **radially outward**. That motion removes the socket from the key and moves the intrusive sphere away from the collars, relaxing its exclusion. The connector is routed below the root flange before reaching the socket. The revised fixture geometry was checked with segment–box and segment–segment collision tests.

The registration argument is also explicit. In the zero-clearance limit, contact between patches in the interiors of the opposing flat end faces fixes their axial orientation. A \(16\times4\ \mathrm{nm}\) rectangular key then fits the matching socket only in centered alignment, apart from a possible \(180^\circ\) roll. An off-center patch removes that remaining ambiguity. The right-hand assembly is a proper rotation of the left-hand one, so it uses the same guest chemistry rather than requiring a mirror-image molecule.

### There is an overlapping finite regime

The exact limiting pose is not the entire result. For sufficiently small positive socket clearance and capture range:

1. Every captured pose approaches the uniquely registered pose.
2. The captured set has positive translation-and-rotation volume.
3. Both guests can bind while positive sliding free volume remains.
4. An open set of captured poses has an unobstructed outward release path.

For example, allowing each guest’s required gap length to vary within \(\delta\pm2\ \mathrm{nm}\) still leaves

\[
F-2(\delta+2)=19.5109\ \mathrm{nm}
\]

of free length even in the more restrictive double-bound order.

The cooperativity signs survive that variation. If \(D_1,D_2\) are sampled independently from their intrinsic docking-pose distributions **before applying sleeve exclusion**, then

\[
q_{LR}^{\,A_LBA_R}
=\mathbb E[f(D_1+D_2)],
\]

and

\[
q_{LR}^{\,BA_LA_R}
=\mathbb E[f(\max(D_1,D_2))].
\]

The first uses the sum because the restrictions occupy separate gaps. The second uses the maximum because both restrictions occupy one gap.

For nonnegative demands,

\[
f(x+y)\le f(x)f(y),
\]

while

\[
f(\max(x,y))\ge f(x)f(y).
\]

These inequalities preserve negative and positive cooperativity respectively. For demands within \(\delta\pm2\ \mathrm{nm}\), the bounds are

\[
0.4064\le\kappa_{A_LBA_R}\le0.6409,
\]

\[
2.5784\le\kappa_{BA_LA_R}\le3.4377.
\]

Those are bounds on the **actual gap demands**. They are not a claim that an arbitrary fabrication tolerance automatically produces that range.

Small positive collar-to-guide clearance introduces a further qualification. The normalized configuration integrals converge to the aligned-guide values, so the strict opposite signs survive and the single-site coefficients become arbitrarily close. **Exact equality of the single-site coefficients at finite guide clearance has not been established.** Tilt and end-contact correlations can distinguish a middle active collar from an end active collar.

For deformable real components, retained order additionally becomes a lifetime requirement against seam opening, cap loss or deformation-assisted passing. The rigid-body existence argument does not determine that lifetime.

## 4. The broader constitutive rule—and its scaling limit

The useful generalization is a rule for how physical contacts consume a finite inventory of sliding space.

For \(N\) ordered hard objects with total free length \(F\), whenever the actual contact geometry reduces to gap requirements,

\[
Z(S)\propto [F-D(S)]_+^N,
\]

where \(S\) is the occupied-contact set and \(D(S)\) is the total required gap length.

The geometry determines how demands combine:

- Requirements on distinct gaps add.
- Compatible requirements on the same gap combine by their maximum.
- Additional guest–guest or fixture collisions must be included separately; the rule does not license an arbitrary chosen interaction table.

The resulting contribution to the contact free energy is

\[
\Delta G_{\mathrm{inventory}}(S)
=-Nk_BT\log\!\left(1-\frac{D(S)}F\right).
\]

This generally contains interactions involving more than two contacts. It is not equivalent to assigning every external connection a fixed, independent bond energy.

It also exposes an important limitation. Suppose a rail is lengthened while maintaining free length per collar \(f_0\), so \(F=Nf_0\). For two fixed demands \(\delta\) on separate gaps,

\[
\log\kappa_{\mathrm{separate}}
=
N\log\!\left[
\frac{F(F-2\delta)}{(F-\delta)^2}
\right]
\sim-\frac{\delta^2}{Nf_0^2}.
\]

Their negative cooperativity vanishes as the rail becomes large. Competition for a global slack budget becomes weak for two isolated contacts.

For two compatible contacts sharing the same gap,

\[
\kappa_{\mathrm{shared}}
=\left(1-\frac{\delta}{F}\right)^{-N}
\longrightarrow e^{\delta/f_0}.
\]

That cooperative contribution remains finite.

This provides a material-design constraint: **strong antagonism from a finite sliding-space budget requires confinement to finite compartments, while shared local restrictions can retain their cooperative effect on longer structures.** A future bulk construction must respect that distinction. Simply adding more retained sleeves to one long guide does not preserve every small-element response.

## 5. The decisive failures still constrain the opportunity

The attempted route from anti-dimer geometry to a branching material failed a stronger test. A spacing design can prevent two rails from using several bonds on each other, yet still admit a finite, fully saturated assembly. I constructed a six-rail \(K_{3,3}\) arrangement—three rails of each kind, all nine cross-connections occupied—with strict clearance margins. It has a finite neighborhood of allowed configurations, so it is not merely an isolated geometric coincidence.

That defeats the claim that suppressing repeated pair bonds necessarily selects an extended network. It does not establish that the finite cage dominates equilibrium.

The original freely swiveling contact also exposed a different failure. Fixed configurations could show strong spectator-mediated coupling of either sign, but integrating over mobile three-dimensional configurations diluted the effect. In the tested ensemble, only about \(0.03\%\) of proposed geometries let both neighbors restrict the same spectator; the resulting joint-weight suppression was approximately \(0.036\%\). The registered guest addresses that specific lack of contact.

The one-contact washout and ordinary-binder comparison remain intact. In particular, an ordinary receptor with the same **full internal steric ensemble** can reproduce the present response. What the construction adds is a physical way for a nonpassing, mobile internal sequence to determine that ensemble and retain it through external bond loss.

## 6. What the primary evidence supports, and what remains molecularly missing

The broad mechanisms have strong precedents. Wang and colleagues’ **SteriDyn** devices already demonstrate steric communication between independently fluctuating DNA-origami arms, including regulation of another arm’s latching. Thus sterically mediated allostery is established experimentally. :chatgpt-content-reference{index="0"} Pinson, Sevick and Williams already showed theoretically that the placement and translational entropy of mobile rings can strongly alter a polyrotaxane’s mechanical response. :chatgpt-content-reference{index="1"}

The narrower contribution here is the explicit compatibility of **retained order, genuine sliding, removable registered guests and opposite contact cooperativity**, with the statistical weights derived from the same contact construction.

DNA provides relevant ingredients. Benson and colleagues demonstrated capped DNA-origami sliders, docking through two or four linker duplexes, and strand-displacement release back to a freely moving state. Their nanometre-scale positioning-fluctuation estimates came from oxDNA simulations; they do not establish the pose distribution of the external socket proposed here. :chatgpt-content-reference{index="2"} Gerling and colleagues demonstrated shape-complementary DNA interfaces and reversible assembly, but also reported a directly relevant tradeoff: stronger hybridization contacts made opening require conditions that compromised structural integrity, while fewer contacts restored reversibility at the cost of a less well-defined closed state. :chatgpt-content-reference{index="3"}

The finite socket calculation makes that tradeoff concrete. With \(0.25\ \mathrm{nm}\) transverse clearance and a \(0.5\ \mathrm{nm}\) capture radius, a restricted orientation integral gave a capture factor of approximately

\[
1.3\times10^{-8}\ \mathrm{nm^3},
\]

using rotations normalized to unit measure. This is a contribution from a checked pose region, not a completed integral over every possible binding orientation. Under a square-well association approximation, if that region alone supplied binding, a \(1\ \mu\mathrm M\) guest reservoir would require roughly \(34\,k_BT\) of stabilization to reach the illustrated occupancy regime.

That estimate exposes a real cost: tight registration can make capture rare and require substantial binding stabilization. It supplies neither a measured chemical affinity nor a dissociation time. Moreover, a strand-displacement mechanism demonstrated on an accessible slider linkage cannot automatically be transferred to a patch buried at the bottom of a close-fitting socket; access for the release strand would itself require a compatible construction.

The completed advance is therefore a **common-contact equilibrium operation with a finite physical regime**, together with a constitutive rule and a scaling limit. The remaining molecular task is to realize its registered bound-pose distribution, retention lifetime and exchange kinetics together. The model now states what that realization must accomplish without borrowing an actuator or a favorable ensemble from a separate idealization.