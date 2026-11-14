# Bulk-free soft-capacity upper from M4 and an optimized subcritical cut

## Status, exact model and dependencies
This is a constructive trial-potential bound on the ORIGINAL soft-source capacity, not an exit-time or occupation theorem. It uses the source's fixed zero-coupling diagonal augmentation, physical nearest-neighbor perimeter, full filled-domain convention and contour encoding. Inherited geometric interfaces are explicitly identified below; the scalar finite certificates are independently exact rational calculations. No native configuration enumeration or simulated-clock rescaling occurs.

Original weight w=exp(θΣ_nn x_ix_j+φΣ_i x_i), φ=θ/R; native rate-one clocks at each of n=L² sites; θ≥4,R≥80,L≥8R. A=C_r is the actually acquired core, r+2≤R/3,r<L/4. The reservoir edge to eachx∈A has conductanceκw(x), with the SAME acquiredκ. B={M≥0}. Cκ is soft capacity andZA=Σ_A w. Assumptions below includeu4<1; finite examples verifyu4<1/2.

For1≤s≤2 letM_(s²) consist of configurations whose augmented plus components have nonwinding embedded filled domains of area≤s²R². Choose either s=2 (M4), or s=8/5 (M_(64/25)). The actualA is contained in either cut by its core-size condition.

## 1. Cut/core normalizer without all-minus entropy loss
For a specified filled plus domainD of physical perimeterP and areaV≤s²R², flipping ALL spins insideD is injective and preservesM_(s²), including thermal holes. The outerplus boundary becomes minus and separates all new interior components from exterior companions; any new filled component is contained inD. The source's complete augmented collar/topology convention is required here.

Isoperimetry givesV/P≤sR/4. At the ORIGINAL field,

w(x)/w(F_Dx)≤exp(−2θP+2φV)≤exp[−θ(2−s/2)P]≤exp(−θP).

A component failing the core'sr-box condition hasP≥2r, and the inherited total contour count is≤6n4^P. Consequently, withq4=4e^−θ,

u4=6n q4^(2r)/(1−q4),   Z_M/ZA≤1/(1−u4).

No conditional Gibbs source assumption is made; this is a partition-function comparison for the fullcut ensemble.

## 2. Structural cut edges, including mergers and hole closure
An addition leavingM joins at most8old augmented components. If the addedsite lies inside an old filleddomain, no filled area/topology cutoff can be newly violated. Thus relevant joined filleddomains are outermost and disjoint. Newarea>s²R² implies new outer perimeter>4sR. The new outer boundary is assembled from old outer boundaries plus at most4new physical edges; hence their old perimeter sum≥4sR−4. This includes hole closure: the newly enclosed area changes, but old boundary pieces still pay the perimeter threshold. It does not equate filled area with pluscount.

If winding first appears, a simple noncontractible cycle through the gate has its remainder in one old augmented component. Its liftedspan≥L−2 gives oldphysicalperimeter≥2L−4≥4sR−4. The governing planar resolution treats nonembedded failure by this topology obstruction. These are the same geometric interfaces used in the acquiredM1/M4cut proofs; this note changes cutoff and constants, not the underlying contour convention.

For each specified tuple ofj≤8old domains, flip all their filled interiors. Disjointness makes the map injective and preservesM. At total perimeter S the Gibbs ratio≤exp[−a_s S], a_s=θ(2−s/2). Count tuples with6n4^P per contour. Reserveη=1/R>0. SinceΣ_(P≥1)e^(−P/R)=1/(e^(1/R)−1)≤R,

Z_structural_predecessors/Z_M
 ≤8(6nR)^8 exp[−(a_s−log4−1/R)(4sR−4)] =: T_s.

This is an overcount, not independence of old domains. The atmostn native exit-site rates are paid separately. Assumea_s−log4−1/R>0, valid in the stated regime.

## 3. Target crossing inside the cut: a valid modest tilt
The formerM1density bound at fields up to3φ cannot be silently used forM4. Instead permit arbitrary inhomogeneous fields0≤h_i≤(3/2)φ. Whole-domain flip has ratio≤exp(−2θP+3φV).
- ForP≤R, V≤P²/16 gives ratio≤exp(−29θP/16), so4timesits per-edgefactor<1/160 atθ≥4.
- ForP>R, V/P≤R/2 gives ratio≤exp(−θP/2), so4timesits per-edgefactor<11/20.

The inherited anchored contour count≤8(2P+3)²4^P then gives uniformly inM andthese fields

P(x_i=+) ≤ 8Σ_(P≥4)(2P+3)²(1/160)^P
          +8Σ_(P≥80)(2P+3)²(11/20)^P
          <ρ=1/500000.

The sums intentionally overcount the split. check.py proves the rational series inequality and exponential replacements using finite Taylor sums. This uniform density proof includes arbitrary thermal bits and all small companions; it requires no FKG for the conditionedcut law.

Increase the field fromφ to3φ/2. This tilts Nplus byφ, so integrating the density bound gives
E_M,φ exp(φNplus)≤exp(φρn).
Hence
P_M(Nplus≥n/2−1)≤exp[−φn(1/2−ρ)+φ],
P_M(B)≤exp[−φn(1/2−ρ)].
These include many-small-droplet target entries, not just a singlelarge contour.

## 4. Actual soft-source trial and complete upper
Setf(star)=1, f=1onM\B, f=0elsewhere. Native cut conductances satisfy c(x,x^i)≤w(x), and native outgoing rate≤n. Source edges contribute exactlyκZ_(A∩B), becauseA⊂M. Therefore

Cκ/ZA ≤ U_s := [ n T_s
                  +n exp(−φn(1/2−ρ)+φ)
                  +κ exp(−φn(1/2−ρ)) ] /(1−u4).

The source-target overlap is NOT omitted, andκ is NOT replaced in the model. In finite scalar upperbounds alone, using the knownκ≤1 to dropκ from the lastpositive term is safe. No hardcapacity identification is required.

## 5. Optimization and finite certificates
Ignoring polynomial prefactors and the1/Rslack, the structural exponent is
F(s)=4s[2θ−θs/2−log4],
maximized at s*=2−log4/θ. Atθ4, s=8/5 is a convenient rational near-optimum. Using log4<7/5, its exponent is at least21.76R−20+4/R; M4 gives20.8R−18.4+4/R. These improve the earlier M1 cut constants while paying bulk entropy throughZA, notw_minus.

Exact rational check.py receipts forθ4,L=8R and unchanged acquiredr:

R | r | M4 upper Cκ/ZA | M_(64/25) upper
80 |5 |exp(−1473) |exp(−1548)
200|5 |exp(−3945) |exp(−4136)
1000|6|exp(−20543)|exp(−21502)
10000|7|exp(−207682)|exp(−217281)

The exactlog bounds are retained incheck.json. All four verifyu4<1/2 and the actual core-size condition. These are scalar analytic certificates, not simulations of those tori. The source clock is untouched.

## Limits
This is a standard Peierls/trial-potential construction with optimized cutoff, not a new general metastability principle. It sharpens a usable capacity upper and can strengthen later voltage/flow arguments. It does not establish bad-region occupation after leaving a cut, a mean exit time, entrance coverage, or a new physical simulation capability. Every later consequence must still be compared against direct v≤1 Gibbs mass bounds and use the actual soft clock/normalizer.
