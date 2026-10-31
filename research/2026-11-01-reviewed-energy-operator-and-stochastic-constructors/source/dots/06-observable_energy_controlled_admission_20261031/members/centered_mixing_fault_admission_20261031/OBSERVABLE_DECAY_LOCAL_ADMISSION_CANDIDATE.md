# Observable-decay local fault admission, including thermal sources

Status: new root construction, UNREVIEWED. A proposed finite-rate initialized-dilation theorem, not a new fault-tolerance threshold, hardware claim, or novelty clearance. Independent review must check time interfaces and product-generator receiving. No source reset is introduced.

## 1. Actual model and local interfaces

A finite circuit schedule has active locations with disjoint DATA patches at each time. Each location has an assigned finite source block, with disjoint SOURCE blocks at each time. A source may be reused at later locations. The actual source generator is a sum of generators confined to these blocks (or idle source blocks); there are no omitted cross-block source couplings. Jump input fields are initialized Markov fields. Initial finite source/data/reference correlations are arbitrary. Source state need not be cold, product, stationary, or fully mixing.

At an active location l the unwanted Hamiltonian is the TOTAL Hermitian K_l(t) supported on its actual data/source patch. All unwanted terms are assigned: outside selected locations they remain real and ON. The intended system Hamiltonian H0(t) respects the active circuit patches, or, more generally, every commutator used below is explicitly charged and all other patch operators still commute. No shared spectator that destroys these commutations is admitted for free. Mid-location instruments are not included in the derivative budget. System-only CPTP instruments (with records retained) may be placed at common boundaries after all ending weights are removed and before starting weights are inserted; their initialized Stinespring maps are contractions and source energy is not being used here. Any instrument occurring while a selected weight remains active needs its own weighted inequality. Adaptive branches must share the prescribed source/data support schedule and uniform bounds; otherwise no adaptive extension is asserted.

For each location choose a positive, constant, acquired rate r_l. Let the actual Heisenberg source generator on its block be G_l^*. Define the residual

  J_l(t)=G_l^*(K_l(t))+r_l K_l(t).

For a common bound c, duration tau and variation/residual budget d suppose

  ||K_l(t)||<=c,
  integral_l ( ||partial_t K_l+i[H0,K_l]|| + ||J_l|| ) dt <=d.

Piecewise differentiable K is enough; jumps can be charged by their norm variation at interfaces as described below. The clean exact-eigenoperator case has J=0. The rate is not inferred from a full-environment mixing gap. A nonzero source-independent interaction has J=r K and is therefore NOT suppressed by choosing a large r.

For uniform formulas below use a common r>0 with r_l=r. Unequal rates can be kept in each location's bound, not replaced inside an unverified eigenoperator identity. All rates, interaction norms, generator actions, target controls and schedule supports are input/model-acquisition obligations.

## 2. A positive weight that follows the actual unwanted observable

For a selected location, complexify its coupling by z=x+i y, |z|<=R. During that location set

  V_l(z,t)=I+(2 y/r)K_l(t).

Put q=2Rc/r. If q<=1/2, then (1-q)I<=V_l<=(1+q)I. Outside that selected interval use I. The weight need not be analytic in z; only the common tilted dilation needs to be analytic.

The source and tilted Hamiltonian terms satisfy EXACTLY

  G_l^* V_l + i z* K_l V_l - i V_l z K_l
    = (2 y/r) J_l + (4 y^2/r) K_l^2.

Here G^*I=0, and K_l commutes with its own linear weight. No Gaussian closure, marginal error multiplication, stationary preparation or inverse full source generator is used.

Including intended control and time differentiation, the weighted-generator expression is bounded above by

  [4R^2 c^2/r + (2R/r)(||J_l||+
                    ||partial_t K_l+i[H0,K_l]||)] I
  <= [8R^2 c^2/r + (4R/r)(||J_l||+
                    ||partial_t K_l+i[H0,K_l]||)] V_l.    (1)

This is an operator inequality, valid with arbitrary references.

## 3. Simultaneous selected locations and retained source memory

At time t take V(t)=product of V_l for the currently active selected locations. These factors commute because their actual source/data patches are disjoint. A source generator term acts on only one current factor, so its contribution is the single-factor expression times the other positive factors. Real unwanted interactions outside the selected set commute with all current selected factors and contribute zero. Intended control contributes the charged commutators above. Thus (1) sums over active selected locations.

When a selected interval begins, replacing I by V_l costs at most a factor 1+q in the weighted squared norm. When it ends, replacing V_l by I costs at most 1/(1-q). This remains valid when the same source is immediately handed to another location: remove ending factors, then insert starting factors. It is a proof interface, not a physical reset or measurement.

Every selected location pays at most (1+q)/(1-q) through its two endpoints. Internal jumps Delta K change the weight by (2y/r)Delta K; with the common lower bound 1-q, their multiplicative squared-norm cost is at most exp[(4R/r)||Delta K||]. This is included in d. Finite instantaneous intended unitary controls can instead be represented by conjugating K across the interface and charging the resulting norm difference. They are not assigned zero cost merely because they have zero duration.

For k selected locations the initialized common jump-history dilation W(z), with source-output and all initialized field histories retained, therefore satisfies

  ||W(z)||^2 <= [(1+q)/(1-q)]^k
                exp[k(8R^2 c^2 tau/r+4R d/r)].           (2)

The arbitrary initial source/data vector is covered by the operator bound. Arbitrary mixed inputs follow by purification. This norm is on the initialized-field input subspace, not on arbitrary incoming quantum fields or an arbitrary unitary extension.

## 4. Inclusive fault amplitudes

Use the same exact analytic multivariate expansion as the existing local-admission proof. Each selected location's fault is the difference between its actual evolution and the same evolution with THAT unwanted interaction omitted, with all other actual terms retained. In the common analytic dilation, the inclusive contribution E(S) consists of terms with positive degree in every selected variable, evaluated at all physical variables equal to1. Multivariate Cauchy on |z_l|=R gives the factor (R-1)^(-k), not a product of reduced marginal probabilities.

Combining with (2), for 1<R<=r/(4c),

  ||E(S)|| <= eta(R)^|S|,
  eta(R)= sqrt((1+q)/(1-q))
          exp[4R^2 c^2 tau/r+2R d/r]/(R-1).

Using atanh(q)<=2q for q<=1/2 gives the convenient sufficient form

  eta(R)<=exp[(4c+2d)R/r+4R^2 c^2 tau/r]/(R-1).         (3)

All locations, including idles if needed by the receiver, must be assigned. This supplies only the initialized-isometry local-amplitude premise, not a complete noisy preparation/measurement/gate construction by itself.

For d=0 and R=min(r/(8c), sqrt(r)/(4c sqrt(tau)))>=2, q<=1/4 and the exponent in (3) is <=3/4. Thus

  eta <=2 exp(3/4) max(8c/r,4c sqrt(tau/r)).              (4)

For c=0 the division formulas are replaced by the exact no-interaction statement. A finite derivative/residual budget must be optimized using (3); it does not disappear into a free control oracle.

## 5. Thermal and nonprimitive examples

Thermal qubit source:

  G=lambda D[sigma_minus]+a D[sigma_plus],
  K=c X_source tensor A_data, ||A||<=1.

Then G^*X=-(lambda+a)X/2, so r=(lambda+a)/2. For constant A commuting with its intended gate Hamiltonian, d=0. The bound has no factor exp(a tau), even at fixed-temperature a proportional to lambda. The source may be initially correlated with all other sources/data. This removes a limitation of the occupation-weight proof, not a limitation of thermal physics. The same one-cell reduced dephasing has an ordinary exact solution; no new elimination effect is claimed.

Nonprimitive qubit source:

  G=(r/2)D[Z_source], K=c X_source tensor A_data.

Again G^*X=-rX, but Z_source is conserved and the whole source never converges to one state. Observable-specific damping, rather than full-source return, suffices for this local-amplitude construction under the locality/commutation premises. This does not permit arbitrary hidden noncommuting source interactions: they must be in the actual G^*K residual.

For g independent same-rate thermal source cells in one circuit patch, K=sum_i X_i tensor A_i may have noncommuting data coefficients. Still G^*K=-rK, and the single patch weight is I+(2y/r)K, not a product of noncommuting cell weights. The TOTAL norm c is paid, possibly as the sum of supplied bounds. Different patches must remain disjoint. This avoids an unjustified cellwise-product argument.

The one-axis thermal example has an exact classical telegraph reduced description: the source algebra span{I,X} is invariant under G^* and multiplication by X. It is not evidence of uniquely quantum leverage. A distinct admitted model is isotropic source depolarization G=(r/4)(D[X]+D[Y]+D[Z]), with K=c0(X_source tensor X_data+Y_source tensor Y_data+Z_source tensor Z_data). Then G^*K=-rK and the total interaction norm is3|c0|. The source coefficients do not belong to a common commutative observable algebra. This supplies a noncommuting-source fixture, not a hardness theorem or advantage over ordinary finite-matrix propagation.

## 6. Consequence and honest boundary

The proposed added capability is a finite-rate all-selected fault-amplitude certificate for local observable-decaying environments, including warm sources without vacuum preparation or full mixing. It uses strong ordinary source-generator and circuit machinery. It does not establish historical novelty, an experimental advantage, a new accuracy threshold, or a cure for arbitrary shared-bath correlations.

At fixed c this bound can scale as c sqrt(tau/r). At fixed diffusion c=sqrt(r)b it retains O(b sqrt(tau)), as the exact damped-qubit benchmark requires. The relevant operator decay and locality must be acquired; merely reporting a small bath energy or a two-point correlation curve does not establish the hypotheses.
