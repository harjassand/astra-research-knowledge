# Finite registry with composition-dependent natural strain: bounded primary check

## Decision boundary

The local continuum functional

`F = ∫[f(φ) + κφ_x²/2 + S(w_x−αφ)²/2 + V₀(1−cos(2πw/d))] dx`

is in the established Frenkel–Kontorova / commensurate–incommensurate family: local preferred spacing competes with periodic substrate registry, and registry walls (solitons) arise beyond a mismatch threshold. The closest source also studies a binary adsorbate and a composition-dependent preferred bond length, so the combined composition-plus-registry mechanism is already directly represented at a discrete and simulated level. This is a strong ancestry/equivalence result, not a novelty or priority conclusion about the exact continuum functional or its parameterization.

## Closest composition-dependent registry prior: Ar–Kr on graphite

Patrykiejew & Sokołowski, “The mechanism of domain-wall structure formation in Ar-Kr submonolayer films on graphite,” *Condensed Matter Physics* 17 (2014), 43601, DOI [10.5488/CMP.17.43601](https://doi.org/10.5488/CMP.17.43601), studies strictly two-dimensional Ar/Kr submonolayer films on graphite. Their molecular model uses truncated Lennard–Jones Ar–Ar, Kr–Kr and mixed interactions plus a three-wave graphite basal-plane potential, with different corrugation barriers for Ar and Kr (8.4 K and 14.4 K). In canonical Metropolis Monte Carlo they move atoms and exchange identities while keeping total composition fixed; the paper examines finite clusters of 343, 601, 931 and 1333 atoms, Ar mole fractions 0.08–0.55 and reduced temperatures 0.01–0.45. The largest-cluster transition is reported near reduced T=0.14±0.02 at x_Ar=0.1 and around T=0.20±0.02 at x_Ar=0.2. The commensurate domains are pure Kr; Ar first covers patch edges, then enters registry walls, whose composition changes from Kr-rich to Ar-rich as x_Ar increases. They distinguish commensurate/incommensurate atoms with a substrate-based order parameter. These are registry-domain walls and composition segregation at walls, not evidence of two coexisting bulk chemical phases governed by a measured binodal.

The same paper’s one-dimensional model is especially close to the local continuum construction: a finite nearest-neighbor harmonic chain has composition-dependent force constants and equilibrium bond lengths plus a periodic substrate cosine; the wall composition also changes those parameters. The authors minimize displacements (and compare wall placement/width), obtaining qualitative agreement with the 2D Monte Carlo. Thus the ingredients “finite periodic registry + composition-dependent natural spacing + soliton walls” are conventional prior art. The remaining distinction is the chosen continuum thermodynamic coupling and any claim for an actual material operation beyond their simulated Ar/Kr model.

This is not an acquired Ar/Kr experiment. The article says the solid-like mixed Ar–Kr/graphite structure had not been experimentally studied; its evidence is computational: canonical Monte Carlo and zero-temperature one-dimensional energy minimization. Atom translation and identity exchange are simulation moves, not a demonstrated deposition/transport/control protocol. (The journal’s official issue page links the paper PDF; the full article text was also readable in its author preprint.)

## Registry-threshold primary: Pokrovsky–Talapov

Pokrovsky & Talapov, “Ground State, Spectrum, and Phase Diagram of Two-Dimensional Incommensurate Crystals,” *Physical Review Letters* 42, 65 (1979), DOI [10.1103/PhysRevLett.42.65](https://doi.org/10.1103/PhysRevLett.42.65), states the classic adsorbed-monolayer scope: for small mismatch between an adatom-lattice reciprocal vector and a crystalline substrate reciprocal vector, a critical mismatch δ_c(T) separates commensurate and incommensurate states, and the superstructure period depends on mismatch. The article page’s abstract is available from APS. Their detailed primary exposition, “The theory of two-dimensional incommensurate crystals,” *Soviet Physics JETP* 51 (1980), 134 (submitted 17 July 1979), treats a 2D elastic adatom lattice in a one-dimensional periodic substrate field. At zero temperature it obtains a periodic soliton superstructure and a continuous C–I transition; the threshold is set by the soliton-energy condition in the model. It also explicitly distinguishes unbounded from bounded-area boundary conditions, which alter critical behavior. This is a theory of registry mismatch and solitons, not a binary composition field or a laboratory protocol.

## Source boundary

- Official journal issue page and linked PDF for Patrykiejew & Sokołowski: https://icmp.lviv.ua/journal/zbirnyk.80/index.html (entry 43601); author preprint: https://arxiv.org/abs/1501.02566
- Pokrovsky & Talapov, 1979 APS abstract: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.42.65
- Full detailed companion theory: https://jetp.ras.ru/cgi-bin/dn/e_051_01_0134.pdf

No new physical acquisition or experimental capability is established by this source check.

## Addendum: species dependence and positive registry floor in the paper's toy chain

The finite-chain FK model in Sec. 4, Eqs. (4.1)–(4.7), does not keep all coefficients composition independent. Equation (4.1) assigns each nearest-neighbor pair a harmonic stiffness `K_{i,i+1}` and preferred distance `b_{i,i+1}` selected by whether the pair is AA, AB or BB; the substrate term has species-specific amplitude `v_i` (`v_A` or `v_B`). With A=Kr and B=Ar, the authors assume reduced toy parameters `K_AA=1`, `b_AA=1.9`, `v_A=0.0055`, `K_BB=0.9`, `b_BB=1.8`, and `v_B=0.003`. For AB pairs, Eq. (4.2) gives geometric stiffness mixing `K_AB=√(K_AA K_BB)` and arithmetic preferred-distance mixing `b_AB=(b_AA+b_BB)/2`.

For a mixed wall of B mole fraction `x_B`, Eq. (4.3) sets `K_w=x_B K_BB+(1−x_B)K_AA`, and Eq. (4.5) clearly sets `v_w=x_B v_B+(1−x_B)v_A`. Thus, for the modeled `x_B∈[0,1]`, this toy parametrization has a strictly positive, composition-uniform substrate-amplitude floor `v_w≥0.003` (in the paper's reduced units), and a positive stiffness floor `K_w≥0.9 K_AA`; the model does not drive the wall barrier arbitrarily to zero. This makes a positive lower-envelope potential mathematically legitimate for this **chosen discrete model**. It does not validate that floor as a measured Ar/Kr material property or as a fabricated-device inequality.

Important equation-text caveat: the arXiv HTML rendering of Eq. (4.4) prints `b_w=x_B b_BB=(1−x_B)b_AA`, and Eq. (4.6) prints an analogous chain of equalities for `b_Aw`. Those equalities cannot both hold for general composition and are inconsistent with a linear mixing expression; do not silently cite them as a valid rest-length interpolation. The surrounding text says the wall parameter depends on mole fraction, while Eq. (4.2) supplies the unambiguous AB-pair arithmetic rule. The exact source supports composition dependence of rest lengths, but its rendered wall-rest-length rule contains an apparent typo/ambiguity that should be preserved as such unless the publisher PDF/erratum resolves it.

The separate 2D Lennard–Jones/graphite Monte Carlo model in Sec. 2 assumes species-dependent graphite barriers `V_b,Ar*=8.4 K` and `V_b,Kr*=14.4 K` in Eq. (2.3); both are positive. These are simulation inputs stated as “assumed,” not measurements made in this paper. The paper explicitly says mixed solid-like Ar–Kr films on graphite had not been experimentally studied at publication time (Sec. 1). Consequently, its positive toy-model lower bound is a valid model-level property only; it supplies no acquired experimental corrugation floor.
