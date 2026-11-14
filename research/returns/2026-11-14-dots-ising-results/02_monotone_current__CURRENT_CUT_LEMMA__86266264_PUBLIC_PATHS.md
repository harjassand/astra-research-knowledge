# Monotone native-current cut lemma for the original soft voltage

Independent derivation of GKP's proposed linear-capacity transport mechanism. This is not applicable to a nonmonotone XOR path without additional work.

## Model and voltage monotonicity
Consider an attractive ferromagnetic single-spin heat-bath chain, an increasing target B, and a decreasing source set A. Attach a reservoir star at voltage1 to x in A with conductance kappa*w(x), with one fixed kappa>=0. Set voltage0 on B, including A intersect B. The remaining harmonic voltage is
 v(x)=P_x(a rate-kappa source clock rings while X_t in A before X hits B).

Couple ordered original chains by the standard common update clocks/uniforms and a common rate-kappa source clock. The upper chain reaches the increasing target no later than the lower chain. If the upper chain is in A at a source-clock ring, the lower chain is also in A unless already absorbed. Thus the soft-source success indicator is decreasing in the starting state, and v(x)>=v(y) for x<=y. This argument uses ORIGINAL dynamics, not reflection on the complement of A or M5; such reflection need not preserve attractiveness.

For every native up edge e=(x,x+i), define i_e=g_e[v(x)-v(x+i)]>=0. The core C_r used in the program is decreasing: removing plus spins cannot create winding or enlarge a component's lifted bounding box.

## Coordinate current cut, including source-target overlap
At a non-target vertex x, harmonicity gives native divergence
 div i(x)=kappa*w(x)*1_A(x)*(1-v(x))>=0.
At a target vertex, native divergence is nonpositive because all neighboring voltages are nonnegative. Sum over the coordinate downset H_i={x:x_i=-}. The only crossing native edges flip coordinate i from minus to plus, all with nonnegative current. Hence

 sum_(e flips i) i_e = source_flux(H_i minus B)-native_sink(H_i intersect B)
                     <=source_flux(A minus B)<=C_kappa.

The direct reservoir-to-target flux on A intersect B is included in C_kappa but not in the native-source sum. Omitting it from equality while retaining it in the upper bound is correct. No artificial source clock is introduced.

## Linear-capacity occupation transport
Let E be any source family and assign each x in E minus B a path to its FIRST B visit, consisting entirely of genuine minus-to-plus native flips. Weight it by w(x). Define its nonnegative edge load L_e as the sum of source weights whose paths use e. Zero paths are assigned to sources already in B. Telescoping gives the exact identity

 N_E=sum_(E minus B)w(x)v(x)=sum_upedges i_e (L_e/g_e).

If for each coordinate i every used edge flipping i obeys L_e/g_e<=a_i, then

 N_E <=C_kappa sum_i a_i.

In particular a uniform bound a yields N_E<=n*a*C_kappa. This is stronger in form than the global energy Cauchy inequality and does not discard the actual voltage-current information. It remains necessary to PROVE a finite useful congestion bound for the desired source family.

## Essential restrictions
- Native paths must be monotone spin additions. Exterior bit-preserving XOR paths can remove source plus defects and do not qualify.
- A stochastic path mixture is allowed if its nonnegative expected load is bounded, but unknown-voltage-dependent path choices do not constitute an acquired algorithm automatically.
- Erasing source bits in monotone growth may create many preimages. Their full Gibbs weights must be included in L_e; a unique-preimage claim from XOR transport cannot be transferred.
- The result is a general monotone potential-theory mechanism, not evidence that arbitrary large/winding Ising sectors have small congestion or that the full residence problem is solved.

## Correction: monotone paths are sufficient, not necessary
For a general signed source-to-target flow F, the same integration by parts gives N=sum_upedges i_e F_e/g_e. Since i_e>=0, one may discard negative terms and bound only the positive part (F_e)_+/g_e. Thus a useful pointwise positive-congestion bound suffices even for nonmonotone paths. The old XOR mean-MGF estimate alone is not such a pointwise bound; a separately paid truncation or other argument may supply it. The monotone-path formulation above is a clean sufficient condition, not a no-go theorem against signed flows.
