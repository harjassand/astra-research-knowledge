# Positive-interior hole reduction beyond M6

Independent derivation of radical's proposed normalization step. This is a partition-function lemma, not a law for actual entrance current or a dynamic growth claim.

## Exact scope
Fix an embedded filled domain D, with an actual plus outer boundary separating its variable interior from the exterior. Fix the needed exterior minus collar. The remaining exterior law may be any of the previously specified small-companion thermal gas constraints; all these constraints depend only on exterior sites. The interior has no extra conditioning besides M_D>0, where M_D counts fixed boundary spins as well. Every variable interior spin has field phi>=0. All bonds are ferromagnetic physical bonds. The diagonal augmentation is only for defining filled components and has zero energy.

Let H be the event that some interior minus component has filled domain of area>R². The filling convention is the same planar augmented convention used for plus domains. The domain D must be filled and embedded so internal filled minus disks stay inside D, including at nonconvex indentations. The outer boundary is plus and cannot belong to such a minus component.

## FKG and field comparison
Conditioning on all exterior spins does not alter the interior Gibbs law: the fixed plus boundary shields it, and exterior energy factors are constants. Denote this ordinary plus-boundary law by mu_phi. The event I={M_D>0} is increasing; H is decreasing. Indeed turning plus to minus enlarges/joins minus components and cannot shrink their filled outer disks. Thus FKG gives

 mu_phi(H | I) <= mu_phi(H).

Increasing the uniform field from0 to phi stochastically increases spins. Therefore

 mu_phi(H) <= mu_0(H).

Neither statement applies after imposing a global magnetization or coupled inside/outside restriction. None is being imposed here.

## Zero-field Peierls estimate
At zero field, flip the entire filled domain of a specified minus contour. All its thermal holes/nested bits are retained by complementing them. The boundary energy gain is2theta P; interior bonds are unchanged and there is no field cost. The fixed plus boundary pins remain outside the flip. The map is injective for a specified contour.

Using the imported physical-contour count <=6n4^P and P>=4sqrt(V), define q=4exp(-2theta). Then

 mu_0(H) <= alpha := 6n q^(4R)/(1-q).

The exponent4R may be rounded down when R is noninteger; the program uses integer R. The estimate requires q<1 and alpha<1. It pays a deliberately loose global n rather than a claimed sharper area-root count.

## Source-normalizer consequence
For the Gibbs source family Omega_D with M_D>0 and the same independent exterior constraints,

 Z_D(no large minus hole) >= (1-alpha) Z_D.

Flip ALL of D in configurations on the left. Every new plus component inside D comes from an old minus component with filled area<=R²; the old plus boundary turns minus and separates it from the exterior. Exterior companions were already <=R². Consequently the image belongs to M1. This is the precise reason the reduction avoids using the much weaker M_c normalizer for a larger source domain.

The source/image weight ratio is still bounded by exp(-2theta P_D+2phi|D|). Hence for each geometric D,

 Z_D <= (1-alpha)^(-1) exp(-2theta P_D+2phi|D|) Z_M1.

The bound is valid for source domains larger than6R² as long as the stated geometry and positive-interior condition hold. Summing contours must still pay the contour multiplicity and the volume/perimeter optimization. It does not make all configurations beyond M6 belong to these source envelopes: negative-magnetization interiors, winding/nonembedded domains, or large exterior companions remain outside the proved coverage.

## Why the alternative monotone-dynamics shortcut fails
Although unconstrained Ising dynamics is attractive, reflection on the complement of a downset need not be. For the two-bit downset {00}, the reflected states x=10<=y=11 have equal first spin. The first-spin death is rejected at x but allowed at y, contrary to the rate condition for an order-preserving coupling. Therefore one cannot simply compare generic exterior reflected dynamics with a hand-picked solid droplet by attractiveness. The partition-function FKG argument above is different and does not use reflected dynamics.
