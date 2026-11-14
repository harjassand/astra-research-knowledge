# Thermal-normalized physical-component basin, with the original source unchanged

## Statement
Retain the original Ising Hamiltonian, heatbath rates, acquired fixed-diagonal core A=C_r, soft clock kappa, voltage v and capacity C. Assume theta>=4, r<=R, r<L/4, and5R²<L²/4.

Define a NEW proof basin F: every PHYSICAL nearest-neighbor plus component admits a nonwinding embedded filled outer domain of area<=5R², using the deterministic plus4/minus8 physical filling convention. Filled domains retain all interior thermal spins. The original core definition is NOT changed. Directly from its r-box condition, A subset F.

Let
 b=theta(2-sqrt(5)/2), q=3exp(-b),
 u=100n q^(2r)/(1-q).
If u<1, then

 mu_F(Ac)<=u,
 1<=Z_F/ZA<=1/(1-u),
 TV(mu_F,mu_A)<=u,
 N_(F\A)/ZA<=u/(1-u).                            (1)

F is a down-set. Thus the exact original-source exterior-current identity can use F as its mesoscopic basin, without changing A, kappa, the target or any physical trajectory.

## Proof architecture
The detailed geometry and encoding are in MERGER_CLUSTER_CANDIDATE.md; this statement promotes ONLY the source-normalizer/down-set part, independently reviewed by bridge.

For an original augmented component K failing the r-box core test, choose every distinct GLOBAL outermost physical filled-domain ancestor meeting K. Their disjoint union U covers K and is8-connected. Adjacent original augmented spins either lie in one ancestor or force boundary contact of different ancestors. Each ancestor itself is physically connected; nesting has been contracted, not discarded.

Solidifying U gives disjoint physical filled domains whose outer physical boundary edge sets meet only at square-dual vertices. Different domains cannot share a physical adjacency, since their boundary plus spins would have belonged to one NN component. Hence the outer wall union is connected and even. Orient every boundary with its filled domain on the left; a directed Euler word traverses every physical edge once and cannot immediately reverse. At most4n initial directed edges and3 subsequent choices give the conservative100n3^P label count. The directions retain the side information, including checkerboard contacts; the word reconstructs U, not just an unspecified contour pairing.

Flip every spin in U. This is injective given the label, keeps all complementary interior thermal bits, and maps F to itself: each old boundary plus layer becomes minus, isolating any newly created plus component inside a previously permitted domain. For total physical perimeter P,

 w(x)/w(flip_U x) <=exp[-2theta P+2phi sum_j |Dj|]
                   <=exp[-bP].

The last inequality uses |Dj|/Pj<=sqrt(5)R/4 separately for each permitted domain. A core-test failure needs P>=2r because U covers the component's failing box span. If U winds, its projection covers a full torus coordinate, and the sum of constituent widths/heights gives P>=2L, which is stronger. No nonzero net homology is falsely assigned to the Euler word.

For each fixed label, injectivity bounds its conditional F mass byexp(-bP). Summing labels proves mu_F(Ac)<=100n sum_(P>=2r)q^P=u. Since A subset F, its conditional law is exactly mu_A; all identities(1) follow. No sampler for a rare entrance/current distribution is assumed.

For the down-set property, deleting plus spins only splits physical NN components. Each new component is contained in an old component's filled domain. The exterior8-connected flood can only grow, so its new filled domain is contained in the old one; winding or area cannot increase. This establishes the down-set requirement for the original current identity.

## Original-source consequence, not a changed source
Let D_F=Omega\(F union B). The exact decomposition is

 N/ZA=1-C/(kappa ZA)+eta_F+N_DF/ZA,
 0<=eta_F<=u/(1-u).

The original decreasing voltage gives nonnegative actual entry current j_F, and the original reflected-outside-F, target-killed residence identity applies exactly as in source equation(9). No artificial entrance law or equilibrium reset is introduced.

Choosing r=O(log(n/eta)) makes u<=eta while retaining the acquired polynomial original-core interface where its geometric hypotheses permit. A TV-eta original-core sampler is then a TV-(eta+u) sampler for mu_F. The acquired ZA normalizer brackets Z_F within factor1/(1-u). These are approximate normalizer/sampler transfers, not a reflected-F spectral-gap theorem.

## What this removes and what it does not
This allows the research to work outside a physically defined component basin rather than treating original-diagonal-only mergers as a new dynamical obstruction. It does not silently redefine the original M5. The more specific proposed bound on F\M5 in the candidate note retains its separate original embedded-domain definition check; it is NOT needed for theorem(1).

Outside F still includes genuinely large physical plus filled domains, physical winding components and plus-background webs with large minus regions. No small bound is asserted for all no-essential configurations: the original core contributes approximately ZA. Capacity acquisition and the full growing-R polynomial prediction theorem remain separate obligations.

## Independent review and diagnostics
Bridge's `n1722_merger_encoding_review_20261113/NESTED_ANCESTOR_REVIEW.md` checks laminar ancestor selection, contact connectivity, directed Euler reconstruction, flip-image membership and normalizer logic; its appended review checks the down-set property. GKP's check.py/json tested5044 planar ancestor witnesses, with nested thermal examples and397 original-augmented area failures. Bridge's separate2190-case Euler diagnostic checks directed encoding. These finite checks support, but do not replace, the geometric proof.

`scalar.py/json` contains exact u and Z_F/ZA bounds at the four existing parameter tuples; its extra F\M5 exponents are explicitly conditional and should not be confused with the unconditional normalizer part above. At theta4, q<1/11 and all four displayed u values are below.011.
