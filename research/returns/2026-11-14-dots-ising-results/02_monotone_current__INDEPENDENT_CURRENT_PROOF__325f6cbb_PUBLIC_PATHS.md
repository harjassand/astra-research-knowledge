# Native monotone-current bound: independent derivation

This lemma is exact for the original heatbath/soft-source process. It does not assume Gibbs entrance laws, killed reflection, or repeatedly refreshed thermal corridors.

## Monotonicity of the original voltage
Order configurations by their plus spins. The actual core A is decreasing: deleting plus sites can split or shrink augmented plus components, and each new component fits the rectangle of its original component. The target B={M>=0} is increasing. Ferromagnetic heatbath has the standard order-preserving common-update coupling. Use one independent rate-kappa Poisson clock for both chains, accepting a ring only when the chain is in A. If the upper chain accepts a clock ring before reaching B, the lower chain has not reached B and must also accept that ring (or have accepted earlier). Thus

 v(x)=P_x(accepted core clock before B)

is decreasing. This is the actual original clock, not an added geometric event.

## Per-coordinate current budget
Orient every native edge upward (one minus spin becomes plus), and define i_e=g_e(v(x)-v(y)). By voltage monotonicity all i_e>=0. Fix site a and let S_a={x:x_a=-1}. Sum Kirchhoff divergence over S_a. Interior currents cancel. Every boundary edge is an upward flip of a. Therefore

 sum_{e:flippedsite(e)=a} i_e
 = sum_{x in A intersect S_a} j(x) - sum_{b in B intersect S_a} drain(b)
 <= sum_{x in A}j(x)=C_kappa.

Target drains are nonnegative. If A overlaps B, the direct soft-source-to-ground contribution is part of total C and does not invalidate the inequality. Equivalently use j only on non-target A, whose sum is at most C.

## Source paths and pointwise congestion
Let G be any source set outside B, and assign each x in G an upward native path gamma_x ending at its first B hit. Give it nonnegative weight a_x (for occupation use a_x=w(x)). Native voltage telescopes:

 sum_x a_x v(x)
 = sum_e i_e [sum_{x:e in gamma_x} a_x/g_e].

Denote the bracket by A_e. If A_e<=K_a for every edge flipping site a, then

 sum_x a_x v(x) <= C_kappa sum_a K_a.

In particular uniform A_e<=K yields N_G<=n K C_kappa. No Cauchy-Schwarz or Gibbs normalization appears. The only nontrivial construction-specific requirement is a POINTWISE congestion bound on actual configurations/edges.

## Nontransferable averaged estimate
An estimate E_source[w(x)/w(x XOR F)]<=exp(4theta) over a conditional core gas does not by itself bound A_e. At a fixed edge the source may be reconstructed and its processed thermal bits fixed. Arbitrary plus bits in a growth prefix contribute exp(4phi Nplus(F)) in the usual energy ratio. A proposed corridor theorem must either pay this factor pointwise, establish an injective weighted reconstruction that sums it at that same edge, or explicitly restrict the corridor to initial minus bits and charge the restricted source mass.

The lemma therefore offers a real route beyond the sqrt(CK) wall, but does not by itself prove general high-area residence control.
