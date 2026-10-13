# CRAY: Compressed cooperative modules through balanced path laws

Research record, 13 October 2026.

**Status.** This record gives explicit constructions and proofs, accompanied by exact-arithmetic calculations and finite diagnostic tests. It is not independently peer reviewed, and publication priority is not established. The resulting high-density numerical bound is deliberately reported even though it is scientifically uninformative.

## 1. Result and its limitation

The full configuration graph is no longer needed to acquire a finite hard-Kob–Andersen source–sink module together with a certified energy bound. Two constructive interfaces were developed:

1. A finite cylinder-current representation with normalization by a quantity conserved by every used microscopic exchange. An empty-column exchange current has exactly `8m-10` cylinder terms and an explicit sectorwise energy formula.
2. A balanced stochastic path grammar. Instead of counting all inverse histories, it carries the density of the transported measure and its second moment. For the essential strip operation that second moment satisfies a scalar recurrence. These moments can be composed through a recursive framing program.

The second interface gives an exact source law and an energy upper bound for blocks of side 4096 at particle density p=4/5. Combined with the previous nonlocal completion, the exact arithmetic certifies

\[
D(4/5)\ge 10^{-11593}.
\]

The corresponding zero-corrector upper bound is 0.238144. This is not a meaningful prediction, not a competitive numerical enclosure, and not a new positivity theorem. Existing cooperative-dynamics results already prove positivity at every p<1 and much stronger high-density asymptotic bounds [1]. The useful output of this investigation is the compressed construction and moment interface, together with a precise diagnosis of why full-block framing remains quantitatively unsuitable.

A deterministic history-counting version of the same general framing construction gives only 10^(-52114). Balanced path laws remove the additional factorial-history penalty. They do not remove the probability cost of preparing a macroscopic empty frame.

## 2. Target, hard constraints, and retained nonlocal interface

Let eta be in {0,1}^{Z^2}, with particles denoted by 1, equilibrium product Bernoulli law mu_p, q=1-p, and chi=pq. On a nearest-neighbor bond {x,y}, the original hard KA rate is

\[
c_{xy}(\eta)=
\mathbf1\{\exists z\sim x,\ z\ne y:\eta_z=0\}
\mathbf1\{\exists z\sim y,\ z\ne x:\eta_z=0\}.
\]

No softening, artificial vacancy reservoir, or forbidden transition is introduced. The target is the bulk variational coefficient

\[
D(p)=\frac1{2\chi}\inf_{f\ \mathrm{local}}
\mathbb E_p\sum_{i=1}^2c_i(a_i+G_if)^2,
\qquad a_i=(\eta_0-\eta_{e_i})\mathbf1_{i=1}.
\tag{2.1}
\]

Rate-one simple exclusion has D=1 in this convention. This is not tagged-particle diffusion and is not an additional hard-constraint hydrodynamic-limit assertion. Variational duality is prior art [1,3,4].

The previous construction [5] tiles the lattice by L-square blocks with one fixed port sigma_u and an independent reservoir omega_u per block. A gate g_u=g(omega_u) never depends on sigma_u. A finite module on two adjacent blocks must obey, for every configuration,

\[
\partial H(\eta):=\sum_{b\subset Q}H_b(\eta)
=(\sigma_u-\sigma_v)g_ug_v.
\tag{2.2}
\]

Here H_b is an outgoing current on the finite configuration graph, and the sum is a configuration-space divergence. It is not a spatial divergence. H must be antisymmetric and legal even with the entire exterior occupied. Intermediate gate states are allowed to be bad.

Let gamma=E g, b=1-gamma, and let w_b be the multiplicity of a microscopic bond in overlapping two-block modules: 4 within a block and 1 across a block interface. Set

\[
C_L(p)=\frac{\mathbb E_Q\sum_b w_bH_b^2}{2\chi\gamma^2}.
\tag{2.3}
\]

If b<sqrt(5)-2, define

\[
\mathcal K(b)=1+8\left[4b+
\frac{32b^2(3-4b+b^2)}{(1-4b-b^2)^2}\right].
\tag{2.4}
\]

The earlier component-averaged stream construction and frozen-reservoir lift give

\[
D(p)\ge\frac1{C_L(p)\mathcal K(b)}.
\tag{2.5}
\]

They also give a finite-radius completion tail. This record changes acquisition of the finite module and its energy bound, not the underlying Thomson principle or the nonlocal completion theorem.

Rotation symmetry of a particular gate is not required here. Horizontal and vertical modules are constructed separately with the same gate orientation and the same uniform energy bound. The previous lifting proof then applies with that common bound.

## 3. Different representations considered

A short deterministic path word is not sufficient: many different inputs can pass through the same intermediate configuration. Counting those inverse histories led to the factorial bound in Section 10. It is a valid baseline, not an invention of canonical paths.

Quotienting states by particle number alone cannot certify legality or source balance: the rate depends on vacancy positions. No exact lumpability or unknown coarse transition law is assumed.

Randomizing histories without tracking their transported density is also insufficient. The selected route is a specially balanced ensemble whose endpoint density can be computed exactly, together with bounds valid during its microscopic implementation. This is what allows histories to be summed rather than listed.

The vacancy-column move, frameability, coarse percolation and information-loss methods have substantial prior art [1,2,3]. The contribution candidate is the explicit current/moment calculus and its composition into a completely evaluable module certificate, not those underlying geometric ideas.

## 4. Cylinder currents and normalization by conserved multiplicity

### 4.1 Exact cylinder contraction

A cylinder C=(Z,O) specifies zeros on Z and ones on O, with Z and O disjoint. Its probability is q^|Z| p^|O|. If a fixed word of coordinate permutations P_t is legal on a cylinder, its path current is the sum of terms

\[
\mathbf1_{P_tC}-\mathbf1_{P_{t+1}C}
\]

on its successive physical bonds. The divergence telescopes exactly.

Two cylinder indicators multiply either to zero, when their prescriptions conflict, or to their intersection cylinder. Thus for a compressed current

\[
H_b=\sum_i\alpha_{b,i}\mathbf1_{C_{b,i}},
\]

its energy is the finite contraction

\[
\mathbb E\sum_b w_bH_b^2
=\sum_b w_b\sum_{i,j}\alpha_{b,i}\alpha_{b,j}
\mu(C_{b,i}\cap C_{b,j}).
\tag{4.1}
\]

This is exact, including collisions between histories. It is not a universal polynomial algorithm: the number and intersection complexity of the cylinders still have to be controlled.

### 4.2 Conserved division lemma

Suppose F is an antisymmetric legal current and K is invariant under every exchange on which F is supported. If

\[
\partial F=K h,
\]

then H=F/K on sectors K>0 has divergence h there. Sectors with zero numerator and no required source are assigned H=0.

Proof: at each configuration K is common to all outgoing terms; invariance makes the divided current antisymmetric. This argument does not justify division by a facilitator count that changes during a used move.

### 4.3 Explicit empty-column current

Let A_0,...,A_(m-1) and B_0,...,B_(m-1) be adjacent columns, m>=2. Assume A is empty and B has a vacant pivot r. The following word exchanges their occupation columns:

- Move B_r to B_0 by r adjacent swaps.
- For y=1,...,m-1, swap B_y with B_(y-1), then B_(y-1) with A_(y-1).
- Move the remaining top vacancy in A down to r.

There are exactly 3(m-1) instructions, including possible equal-occupation swaps. Every actual exchange is legal with occupied exterior. The adjacent empty column supplies the extra vacancy for vertical moves; the diagonal transfer has an explicitly maintained pair of supporting vacancies. This geometric move is known [2].

Superpose the word for every vacant pivot, without selecting the first one. Its source multiplicity is

\[
K=m-N,
\]

where N is the total particle number on the two columns. All current terms have at least m+1 specified zeros, so their support has N<=m-1 and K>0. Since N is conserved, divide the summed current by K.

The resulting source is

\[
\partial H=
\mathbf1_{\{A\text{ empty},\ B\text{ nonfull}\}}
-\mathbf1_{\{B\text{ empty},\ A\text{ nonfull}\}}.
\tag{4.2}
\]

The all-pivot numerator F has exactly 8m-10 zero-only cylinder terms after cancellation. Here is a direct description, with I_S denoting that all sites in S are vacant and slice endpoints following Python convention. For y=1,...,m-1:

\[
\begin{aligned}
F_{B_{y-1},B_y}={}&m\left(I_{A[y-1:]\cup B[:y]}
-I_{A[y-1:]\cup B[:y-1]\cup\{B_y\}}\right)\\
&+(m-y)\left(I_{A\cup\{B_y\}}-I_{A\cup\{B_{y-1}\}}\right),\\
F_{A_{y-1},B_{y-1}}={}&m\left(I_{A[y-1:]\cup B[:y-1]\cup\{B_y\}}
-I_{A[y:]\cup B[:y+1]}\right),\\
F_{A_{y-1},A_y}={}&y\left(I_{B\cup\{A_y\}}-I_{B\cup\{A_{y-1}\}}\right).
\end{aligned}
\tag{4.3}
\]

At y=1, the two terms on the first bond cancel down to one difference, accounting for the term count. Path telescoping proves (4.2); (4.3) is obtained by grouping identical pivot-stage cylinders.

Set

\[
a_m=\frac{2m(m-1)(8m-7)}3.
\]

Exact cylinder contraction gives

\[
\mathbb E\sum_bF_b^2
=a_mq^{m+1}-[a_m+4m(m-2)]q^{m+2}
+4m\sum_{z=m+3}^{2m}q^z.
\tag{4.4}
\]

One way to check the formula for all m is to separate the three bond types. Their squared terms before the preparation/diagonal cross terms sum to

\[
4pq^{m+1}\left[(m-1)m^2+\sum_{y=1}^{m-1}y^2\right].
\]

The cross terms are

\[
-4mp\sum_{y=1}^{m-1}(m-y)q^{m+y}.
\]

Finite geometric-sum simplification yields (4.4).

Define out-of-range binomial coefficients to be zero, and

\[
e_n=a_m{m-1\choose n}-[a_m+4m(m-2)]{m-2\choose n}
+4m{m-2\choose n+1}.
\]

Expanding (4.4) into particle-number sectors and dividing by K^2 gives

\[
\boxed{\mathbb E\sum_bH_b^2
=\sum_{n=0}^{m-1}\frac{e_n}{(m-n)^2}p^nq^{2m-n}.}
\tag{4.5}
\]

This requires O(m) summands, with integer bit lengths paid explicitly. The implementation with bit-mask cylinders stores O(m^2) bits; interval descriptions could store the same masks more economically. No compactness of an unknown current is assumed.

For comparison, the first-vacancy selector has energy

\[
2q^{m+1}\sum_{k=1}^{m-1}[3m(2k-1)-k(k-1)]p^k.
\tag{4.6}
\]

At p=.8, dividing both energies by 2q^m(1-p^m), the all-pivot versus first-pivot values are approximately 733.805 versus 1350.387 for m=64, and 2774.508 versus 5497.600 for m=256. These are module-energy comparisons, not diffusion coefficients. The direct m=256 representation has 2038 cylinder terms and its exact energy calculation took about 0.052 seconds in this run.

## 5. Balanced path laws: replace inverse-history counts by densities

### 5.1 A measure-preserving orbit identity

Let a finite group G of size M act by measure-preserving bijections on a probability space, and let E be a target event. Define

\[
K(x)=\#\{g\in G:gx\in E\}.
\]

K is constant along every G-orbit. Starting with the unnormalized measure mu restricted to K>0, choose uniformly among the g that send x into E and output gx. The output density with respect to mu is

\[
\boxed{\rho(y)=\frac{M}{K(y)}\mathbf1_E(y).}
\tag{5.1}
\]

Indeed, for each g the preimage is g^(-1)y and has the same equilibrium weight; summing the M inverse contributions proves (5.1). Periodic configurations cause no exception: distinct group elements are counted with their multiplicity. Furthermore,

\[
\mathbb E\rho^2=M\,\mathbb E\left[\frac{\mathbf1_{K>0}}K\right].
\tag{5.2}
\]

This identity alone does not provide physical control. Every chosen group action still needs a legal microscopic implementation and an intermediate-density bound.

### 5.2 The supported strip operation

For a strip of m sites, let G be the m cyclic rotations and E the event that site zero is vacant. K is the number of strip vacancies. Choose a vacant pivot uniformly and cyclically rotate it to site zero. Then

\[
\rho_m(\eta)=\frac mK\mathbf1_{\{\eta_0=0\}}.
\tag{5.3}
\]

When an adjacent strip is empty, every adjacent transposition within the active strip is hard-KA legal. A cyclic rotation by r can be implemented as r repetitions of adjacent swaps that rotate by one position, using at most m(m-1) instructions. All selected rotations therefore have legal paths.

Let

\[
V_m(p)=\mathbb E\rho_m^2
=m\sum_{k=1}^m\frac1k{m\choose k}q^kp^{m-k}.
\tag{5.4}
\]

There is a scalar recurrence:

\[
\boxed{V_1=q,\qquad V_m=\frac{mp}{m-1}V_{m-1}+1-p^m.}
\tag{5.5}
\]

For a direct derivation, put F_m=V_m/m. Expanding an integral gives

\[
F_m=\int_0^1\frac{(p+qt)^m-p^m}{t}\,dt
=\sum_{k=1}^m\frac{p^{m-k}(1-p^k)}k.
\]

Thus F_m=pF_(m-1)+(1-p^m)/m, which is (5.5).

During the rotation word, the density is bounded by m times the incoming density on the other coordinates: there are at most m pivot branches, each coefficient is at most one, and each branch acts only on the fresh strip by a coordinate permutation. Therefore its squared-density cost is at most m^2 times the already accumulated cost. This intermediate bound is intentionally conservative.

The endpoint density (5.3) is also optimal for squared-density concentration under these exact requirements. In a sector with k vacancies, the target event occupies a fraction k/m of that sector. Any number-preserving kernel that sends the full sector measure into this target has conditional output density with mean m/k on the target. Cauchy–Schwarz makes its contribution to the second moment at least (m/k) times the sector probability. The balanced rotation attains equality in every sector, giving precisely V_m. This is optimality of the endpoint density, not optimality of the microscopic current energy or of the full cooperative module.

The random choice is part of the exact definition of an ensemble current. No sampled frequencies are used to certify its energy. Pivot probabilities are stored as 1/K of the original strip state for that history; they are not recomputed from a different microscopic state after the strip has been moved.

### 5.3 Moment composition

Suppose fresh, disjoint input pieces are processed by kernels with known endpoint densities rho_i, and previously processed pieces are merely relocated by fixed coordinate permutations. Their endpoint densities factor, after the corresponding deterministic relabeling. The squared-density moments multiply. Restricting the input further to a gate event only decreases the transported measure, so the same nonnegative upper bounds remain valid.

The frame grammar has exactly this structure for each fixed seed location. A left/down extension relocates the formerly empty frame line and the fresh strip by a fixed permutation of occupation coordinates; a right/up extension has net effect only on the fresh strip. The output pieces remain disjoint, although they need not be contiguous.

This is the substantive compression interface: a path nonterminal carries its source/endpoint law and a second-moment bound, not a list of all its inverse histories. It is not asserted that arbitrary path grammars admit such a composition.

## 6. A port-independent high-probability gate

### 6.1 The gate

Use L=2^j and one fixed port per square. For gate evaluation, replace that port by an occupied site. This gives exact port independence. All following vacancy tests use this occupied-port copy.

A canonical frame is the left column and bottom row vacant, a total of 2L-1 sites. A 2-square is good if at least three sites are vacant. With at most one forced occupied site, its probability is at least q^3. The at most one particle can be moved to the opposite corner by at most two legal moves.

For a 2n-square, divide into four disjoint n-square children. For each child, test whether it is good and whether it can be expanded to the parent by alternating horizontal and vertical extensions. Each newly annexed strip must contain a vacancy. These strip lengths are k and k+1 for k=n,...,2n-1. The parent is good when at least one of the four candidates succeeds. Choose the first successful child only to define an unambiguous program.

### 6.2 Legal frame expansion

Given a frame and a new strip containing a vacancy:

- To expand right or up, move the corresponding empty frame line next to the fresh strip using the known empty-column exchange. The existing perpendicular empty frame supplies a vacancy in each intervening line. Rotate the fresh strip so its first site is empty, then undo the temporary movement of the old frame line.
- To expand left or down, rotate the new strip next to the old empty frame line, then exchange the two full occupation lines.

The old rectangle is restored in the first case. In the second case, the old empty frame line is replaced by the new data strip and the new outer line becomes empty. In both cases the enlarged rectangle has the prescribed frame. All supports lie within the rectangle plus its new strip; occupied exterior is allowed.

The strip tests concern the original unprocessed sites. Earlier expansions have not changed those sites, so no adaptive availability oracle is needed.

### 6.3 A finite recursion for gate probability

Let f_n be a lower bound uniform over the location of at most one forced occupied site. A lower bound on one child's extension probability, independent of that child's interior, is

\[
r_n=
\frac{1-p^{n-1}}{1-p^n}
\prod_{k=n}^{2n-1}(1-p^k)(1-p^{k+1}).
\tag{6.1}
\]

At most one fresh strip contains the protected site. Removing it from a vacancy test changes a length-k factor by (1-p^(k-1))/(1-p^k); this ratio increases with k, so length n is a conservative choice. If the protected site lies in the child, there is no such loss, but the same lower bound remains valid.

Let E_i denote the four successful extension events, gamma_i the four child-good probabilities, S=sum gamma_i, and X=sum 1_(E_i). Child-good events are independent because the children are disjoint. The extension events themselves are not assumed independent. We have

\[
\mathbb E X\ge r_n S,
\qquad
\mathbb E X^2\le\mathbb E X+\frac34 S^2.
\]

The second inequality follows from E_i intersection E_j being contained in the intersection of the two child-good events. Cauchy–Schwarz and monotonicity in S>=4f_n yield

\[
\boxed{f_2=q^3,\qquad
f_{2n}=\frac{4f_nr_n^2}{r_n+3f_n}.}
\tag{6.2}
\]

No independence of overlapping growth routes has been inserted.

For every fixed p<1, r_n tends to one along the dyadic scales and the recursion tends to one. To see this, write

\[
f_{2n}^{-1}=\frac{f_n^{-1}}{4r_n}+\frac3{4r_n^2}.
\]

Eventually this is a strict contraction around one with a vanishing forcing term. Thus some finite L meets the earlier nonlocal-completion threshold. This is an explicit construction, not an improvement over known all-density frameability or diffusion positivity.

At p=4/5, outward-rounded rational computation gives the following lower bounds:

| L | Gate probability lower bound, approximately |
|---:|---:|
| 16 | 0.000119506553 |
| 64 | 0.001468158391 |
| 256 | 0.022984232225 |
| 512 | 0.086006545646 |
| 1024 | 0.273466464658 |
| 2048 | 0.600893332668 |
| 4096 | 0.857598203285 |

The last exact lower endpoint is

\[
f=\frac{33972964910917280332276380933}
{39614081257132168796771975168}.
\tag{6.3}
\]

For n>=256 the supplied calculation uses the weaker but faster union bound

\[
\prod_{k=n}^{2n-1}(1-p^k)(1-p^{k+1})
\ge\max(0,1-2p^n/q).
\]

It is therefore conservative. Fixed 96-bit fractional precision is enough for this instance. Extremely small q may require higher precision and much larger L; no uniform affordable all-density claim is made.

## 7. Exact two-port source balance without enumerating states

For each pair of good blocks, simulate both ports as occupied. Prepare both frames with the balanced grammar. Track the two occupied port tokens through the chosen coordinate words. They lie in the interior of the resulting rectangular frame.

An adjacent horizontal interior transposition can be performed by moving the empty bottom row to the row immediately below it, making the transposition, then undoing the row movement. Vertical transpositions are analogous. A Manhattan chain of adjacent transpositions, followed by the reverse chain except for its final edge, exchanges just the two selected interior coordinates.

Finally undo both preparations. The full coordinate word exchanges the original ports and restores every reservoir occupation. All four actual port assignments follow the same word for the same pivot randomness: replacing a simulated occupied port by a vacancy cannot remove a vacancy witness. The simulator never relies on a port token as a known empty site.

The middle transposition word is palindromic, and the full word has form P S P^(-1), also palindromic as a list of involutive exchanges. Reversing a path has the same pivot probability as the forward path run from the opposite port assignment, since the original reservoirs and occupied-port simulation are unchanged.

Define H by summing the signed microscopic path currents over all positive source inputs sigma_u=1, sigma_v=0, g_u=g_v=1, and over all pivot histories with their exact probabilities. Each path preserves particle number, hence equilibrium weight. Each input's history probabilities sum to one. Its endpoint is the unique input with ports exchanged. Consequently, pointwise,

\[
\partial H=(\sigma_u-\sigma_v)g_ug_v.
\tag{7.1}
\]

This is an implicit but exact finite current. Its definition does not require listing configurations, and the following energy certificate does not require evaluating H pointwise. Affordable exact pointwise evaluation of the fully summed H is not claimed.

## 8. A compressed congestion theorem

### 8.1 A path-density bound

Let rho_t be the density, relative to mu_Q, of the unnormalized positive-source measure at a padded microscopic clock t. Denote its outgoing bond mass density by a_(t,b). Then sum_b a_(t,b)<=rho_t. The current at that clock is

\[
h_{t,b}(\eta)=a_{t,b}(\eta)-a_{t,b}(\eta^b),
\]

because mu_Q is invariant under the exchanges. With w_b<=4,

\[
\mathbb E\sum_bw_bh_{t,b}^2\le16\mathbb E\rho_t^2.
\]

Minkowski gives, for paths of length at most T,

\[
\boxed{\mathbb E\sum_bw_bH_b^2\le
16T^2\sup_t\mathbb E\rho_t^2.}
\tag{8.1}
\]

No worst-case count of individual histories occurs in (8.1). It is essential, however, to construct its density bound rather than assume it.

### 8.2 The frame moment

For a fixed seed location, base preparation of a 2-square has endpoint density at most 4 and squared moment at most 16. Its intermediate densities obey the same bound. Every later fresh strip has one of the lengths k,k+1, k=2,...,L-1, exactly once along the chosen ancestry route.

Define

\[
R_L(p)=16\prod_{k=2}^{L-1}
\max\{1,V_k(p)\}\max\{1,V_{k+1}(p)\}.
\tag{8.2}
\]

The moment-composition argument gives endpoint squared density at most R_L for one block. During a rotation, the extra m^2 bound gives at most L^2 R_L. For two disjoint blocks, any preparation prefix is therefore bounded by L^2 R_L^2.

The deterministic first-success gate restriction may correlate the input pieces. Dropping that restriction only enlarges the nonnegative transported measure for a specified seed. This is why the product-law majorant is legitimate even though the gate events are not independent.

### 8.3 Tracking port independence costs explicitly

There are

\[
N=2L^2
\]

microscopic sites in the pair, and at most

\[
S=(L^2/4)^2=L^4/16
\]

pairs of 2-square seed locations. There is no factorial pivot-history factor: pivots are integrated by the balanced kernels.

There are at most N^2 possible pairs of prepared port-token positions. For each such pair, every prefix of the middle transposition is a fixed coordinate permutation. Dropping its conditioning and applying Minkowski costs at most N^4 in squared density. Thus N^4 L^2 R_L^2 is a common upper bound for the simulated occupied-port evolution at a fixed seed pair, including preparation and middle phases.

One simulated occupied token represents the actual vacant port. Its position must not be treated as free information. If eta_v=0 and zeta is eta with site v filled, then mu(zeta)/mu(eta)=p/q. The initial positive-source law differs from the corresponding occupied-port law by q/p, so these factors cancel pointwise. Forgetting the marked location gives

\[
\rho^{\rm actual}(\eta)
\le\sum_v\mathbf1_{\eta_v=0}\rho^{\rm simulated}(\eta^{v\gets1}).
\]

Cauchy–Schwarz and the product measure give

\[
\mathbb E(\rho^{\rm actual})^2
\le N^2(q/p)\mathbb E(\rho^{\rm simulated})^2.
\tag{8.3}
\]

Summing the S seed-pair majorants costs at most S^2. Finally, the inverse-preparation phase is controlled by path reversal from negative source inputs. Their reservoir law and history probabilities are identical, so the same bound applies. This avoids assuming that inverse preparation forgets its random history for free.

Consequently,

\[
\sup_t\mathbb E\rho_t^2
\le S^2N^6L^2(q/p)R_L^2.
\tag{8.4}
\]

Padding may be chosen with common phase lengths and symmetric idle instructions around the palindromic middle word. It introduces no physical transition and makes the clock argument independent of random pivot lengths.

### 8.4 Length and full coefficient bound

A strip rotation uses at most L(L-1) swaps. Temporary movement and return of an empty frame line uses at most 6L^2 swaps. Fewer than 2L strip additions give a one-block preparation length below 16L^3. Both preparations and both inverses cost at most 64L^3.

An adjacent interior transposition in the 2L by L rectangle costs at most 12L^2+1 swaps. Fewer than 6L such transpositions suffice to exchange the two tokens. Thus the common padded bound

\[
T=256L^3
\tag{8.5}
\]

is conservative for every history and orientation.

Combine (8.1), (8.4), chi=pq, and the definition of C_L:

\[
\boxed{C_L(p)\le
\frac{8T^2S^2N^6L^2R_L(p)^2}{p^2\gamma^2}.}
\tag{8.6}
\]

If f<=gamma and 1-f<sqrt(5)-2, monotonicity of the positive tail series in (2.4) gives the completely finite certificate

\[
\boxed{
D(p)\ge
\frac{p^2 f^2}
{8T^2S^2N^6L^2R_L(p)^2\mathcal K(1-f)}.
}
\tag{8.7}
\]

Equations (5.5), (6.2), and (8.7) require neither a configuration graph nor a supplied spectral gap, global corrector, completion error, or inverse-path multiplicity oracle.

## 9. Executed p=0.80 instance and exact arithmetic

For p=4/5 and L=4096:

- The exact gate lower bound is (6.3), approximately 0.857598203285.
- The corresponding coarse energy upper bound is approximately 81.1958251981.
- N=33,554,432 microscopic sites in the two-block rectangle.
- S=17,592,186,044,416 seed pairs, accounted for by a polynomial factor, not enumerated.
- T=17,592,186,044,416 microscopic instructions is a worst-case bound, not an executed path length.
- The rounded-up numerator of R_L has 19,171 bits.

The exact rational value of the right side of (8.7) exceeds 10^(-11593). The final decimal exponent is checked by an integer comparison with a power of ten, not inferred from a floating-point logarithm.

`balanced_certificate.py` evaluates the probability and moment recurrences using 96-bit dyadic fractional rounding in the required direction. The numerator of a large moment is not restricted to 96 bits. For the moment recurrence, p^m is rounded down before subtraction; each positive update and product is rounded up. The gate recursion is rounded down. All other displayed comparisons use arbitrary-precision integers and rational numbers.

The ordinary zero-corrector upper bound is

\[
D(p)\le(1-p^3)^2,
\]

which gives 0.238144 at p=.8. Better specialized upper variational methods exist [4]. The enclosure here is much too wide to be a scientific prediction.

### Executed diagnostics

The code checks:

- Direct all-pivot formulas against the expanded cylinder compiler for every m=2,...,32.
- All 1360 configurations for m=2,...,5 for the primitive current's legality, antisymmetry, source identity and exact energy.
- Exact balanced-strip pushforward densities and moments on 2046 configurations over strip lengths 1,...,10.
- Symbolic vacancy-support invariants in 980 balanced growth cases, covering 76,440 microscopic instructions. An additional 980 first-pivot growth cases are checked separately.
- Balanced two-port module words on accepted p=.8 reservoir samples at sides 4,8,16, including both rectangle orientations, two random pivot histories and all four actual port assignments. These tests cover 951,704 microscopic instructions and verify restoration of every reservoir site, exact exchange of the ports, and port-independent planning.
- Rejection of a deliberately corrupted primitive current and outward rounding against exact small-m moments.

Random reservoirs and histories are test inputs only. No sampled probability or sample variance enters a certificate.

A full regeneration of the two numerical certificates and the complete test suite took **6.66 seconds wall time** and **109,068 KiB peak resident memory (about 106.5 MiB)** under `/usr/bin/time -v` in this container. Within that run, the final scalar certificate calculation took about **0.242 seconds**. These measurements exclude the research and proof development and are not portable performance guarantees.

The tested environment was Python 3.13.5 and NumPy 2.3.5. Scalar certificate evaluation needs only the Python standard library; NumPy is used for the finite path tests. No optimization package or large sparse graph is required.

## 10. A deterministic comparison and complete resource limits

A deterministic first-vacancy framing program has at most

\[
B_L\le\frac{5L^2}{8}(L-1)!L!
\]

histories per block. This follows from B_2<=5 and

\[
B_{2n}\le4B_n\prod_{k=n}^{2n-1}k(k+1).
\]

For fixed history and clock the intermediate map is a permutation, so at most one starting configuration has a given intermediate image. Including the two edge orientations, a crude current bound is

\[
C_L\le8B_L^2(96L^3)^2.
\]

It gives the weaker endpoint 10^(-52114) at the same p and L. This baseline is supplied to distinguish compact path syntax from compact congestion accounting. The balanced calculation replaces B_L^2 by the moment and polynomial factors in (8.6).

The new resource claims have limited scope:

- For a specified reservoir, gate evaluation uses a quadtree and rectangular vacancy queries. Prefix sums give O(L^2) arithmetic work and memory. This is not a constant-cost gate oracle.
- A sampled successful preparation uses O(L) macro instructions with O(log L)-bit coordinates and pivot counts. Computing their net endpoints costs O(L^2), apart from gate evaluation.
- Expanding and executing a complete two-port microscopic word is O(L^3). The L=4096 bound corresponds to trillions of instructions and was not executed.
- The probability/moment certificate uses O(L) scalar updates, plus arbitrary-precision arithmetic. The relevant numerators grow with L and log(1/q); bit complexity is not constant per update.
- The module current is defined as an exact finite ensemble. No affordable general pointwise summation over all its histories is proved. Certificate evaluation avoids that operation.
- The previous nonlocal lift is still genuinely nonlocal. Its proved 2 by 2 matrix tail can be evaluated from this C_L, but a large C_L worsens the cutoff needed for a small current-norm error. Neither a small physical support nor cheap exact expectation of a large cutoff current is claimed.

There is no full enumeration of the 2^(33,554,432) configurations of the dense two-block instance. There is also no claim that polynomial cost in L makes the high-density family practical: the required L itself can be very large as q decreases.

## 11. Why full-block preparation remains a bad quantitative representation

### 11.1 A preparation concentration theorem

Let G have probability gamma and let a positive-mass preparation kernel push mu restricted to G into a density r supported on an event F of probability epsilon. Mass conservation and Cauchy–Schwarz give

\[
\boxed{\mathbb E r^2\ge\gamma^2/\epsilon.}
\tag{11.1}
\]

Keeping additional history labels cannot improve the marginal inequality after the labels are forgotten.

If a legal preparation current P has divergence 1_G-r, apply the finite graph integration-by-parts identity to 1_F. The required net flux through F is at least gamma-epsilon. With at most |E_Q| physical bonds and exchange-invariant equilibrium,

\[
\mathbb E\sum_b P_b^2
\ge\frac{2(\gamma-\epsilon)^2}{|\mathcal E_Q|\epsilon}.
\tag{11.2}
\]

Indeed, the squared gradient sum of 1_F is at most 2|E_Q|epsilon, and the integration-by-parts factor is one half. In an L-square, |E_Q|<=2L^2, so the lower bound is at least (gamma-epsilon)^2/(L^2 epsilon).

For one specified empty frame,

\[
\epsilon=q^{2L-1}.
\]

At q=.2 and L=4096 this is about 10^(-5725.26); two specified frames have probability about 10^(-11450.53).

This theorem applies to positive-density preparation into a specified rare event. It is **not** a lower bound on the energy of every possible signed port-exchange current, nor a no-go theorem for all compressed certificates. Preparation and return currents can cancel; a proof exploiting those cancellations, or avoiding full frames, could escape the preparation bound.

### 11.2 The balanced estimate exposes rather than removes that scale

For fixed p,

\[
\frac{(1-p^m)^2}{q}\le V_m(p)
\le\frac1q+\frac{3m}{(m+1)(m+2)q^2}.
\tag{11.3}
\]

The lower bound follows from Cauchy–Schwarz applied to K and 1/K. For the upper bound use, for k>=1,

\[
\frac1k\le\frac1{k+1}+\frac3{(k+1)(k+2)},
\]

then sum the binomial identities; adding the k=0 term only enlarges the upper bound. Thus V_m=1/q+O(1/m), and R_L grows like q^(-2L) up to factors polynomial in L for fixed p. The paired frame moment therefore has the q^(-4L) scale visible in the numerical certificate.

The history explosion was partly a representation defect and has been removed. Concentration into a macroscopic empty frame remains a different obstacle. Tightening a few polynomial constants will not make (8.7) a useful dense prediction.

## 12. The consequential unresolved theorem

The next object should not prepare a complete block frame and then treat that preparation as a cheap reversible subroutine. A credible stronger construction must retain an ensemble of smaller active vacancy fronts or partially framed regions and either avoid macroscopic concentration or rigorously exploit signed preparation/return cancellations.

A precise sufficient interface is the following. Construct a port-independent good-block family with gamma bounded above the proved completion threshold and a legal path/current grammar satisfying (7.1). Supply an efficiently evaluable weighted second-moment bound for the resulting **whole signed source–sink current**, not merely a forward-path length or a count of initial facilitators. Its cost must be controlled by the active interfaces rather than the completed empty perimeter of the whole block.

The completed pieces here can be reused: exact cylinder intersections, conserved-multiplicity division when its hypothesis really holds, balanced orbit kernels with explicit pushforward laws, the path-density inequality, the port-tag correction, and the frozen-reservoir nonlocal lift. Their applicability does not establish the missing interface theorem automatically.

A substantial high-density consequence would be an explicit module bound of the form C_L(1-q)<=exp(A/q) together with gate/completion constants bounded sufficiently well, or a numerically informative value at p=.8. No such estimate is proved here. In particular, normalizing by a changing number of currently active fronts would not be justified by the conserved-division lemma; that operation would need a new exact source law.

The local primal variational hierarchy still supplies upper bounds. Improving energy within the present dual family does not prove its density in the optimal current space. There is no demonstrated two-sided convergence theorem or new high-density scaling law.

## 13. Comparison and assessment

Shapira's bulk KA theorem [1] already proves, for d=k=2, bounds of the form

\[
C\exp[-\lambda q^{-1}\log^2(1/q)]
\le D(1-q)\le C'\exp[-\lambda'/q],
\]

with positive constants. Its lower-bound proof uses multistep moves, coarse percolation and information-loss estimates. These asymptotic results are stronger than the full-block family developed here.

Ertul–Shapira [2] provides known empty-column operations, frameability and port-independent coarse connectivity in its tagged-diffusion construction. Only the geometric operations are reused; tagged and bulk coefficients are not identified. Shapira [3] establishes the dual variational principle and unbounded-path lifting framework. Arita–Krapivsky–Mallick [4] supplies specialized primal upper-bound calculations.

The formulas and compressed interfaces in this record were developed during this investigation. That is not a claim of independent literature priority. No optimized external implementation was benchmarked head to head. The scalar certificate's short evaluation time is not a demonstration of fast accurate dense transport prediction.

**What is established in this record:** an explicit arbitrary-length cylinder current and energy formula; a balanced path-law density/moment interface; a recursive port-independent gate; a legal two-port transposition grammar; a fully accounted energy theorem avoiding complete configuration enumeration; a reproducible but extremely weak p=.8 lower bound; and a precise preparation concentration limitation.

**What remains unestablished:** a quantitatively informative dense transport certificate, improved high-density asymptotics, affordable pointwise evaluation of the full current, completeness of a dual hierarchy, or a generally efficient completion theorem for arbitrary cooperative defects.

The next decisive advance is not another larger finite graph. It is a low-concentration, composable source–sink current that uses distributed cooperative facilitation without paying for a fully empty macroscopic frame.

## References

[1] Assaf Shapira, *Hydrodynamic limit for the Kob-Andersen model*, arXiv:2003.08495v2. In particular Theorem 2.3 and Section 4. https://arxiv.org/html/2003.08495v2

[2] Anatole Ertul and Assaf Shapira, *Self-Diffusion Coefficient in the Kob-Andersen Model*, arXiv:2003.02531. In particular the empty-column move, framing constructions and information-loss analysis. https://arxiv.org/abs/2003.02531

[3] Assaf Shapira, *A Thomson-type variational principle for diffusion coefficients*, arXiv:2606.04636v2, revised 30 June 2026. https://arxiv.org/html/2606.04636v2

[4] Chikashi Arita, P. L. Krapivsky and Kirone Mallick, *Bulk diffusion in a kinetically constrained lattice gas*, arXiv:1711.10616. https://arxiv.org/abs/1711.10616

[5] Prior internal research artifact, *CRAY: Frozen-reservoir lifting and constructive nonlocal transport certificates*, 13 October 2026, supplied with this conversation. Its nonlocal completion and source-module interface are retained dependencies, not independent peer review.
