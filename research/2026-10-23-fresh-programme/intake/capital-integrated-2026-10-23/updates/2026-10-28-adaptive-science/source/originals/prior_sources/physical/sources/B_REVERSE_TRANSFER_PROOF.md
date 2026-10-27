# Finite switched heat-contact networks cannot give perfect DC isolation

## Scope

Consider any finite number of fixed-temperature terminals and internal thermal
stores. Every internal node v has a **constant positive scalar capacity** C_v.
Every edge has a bounded nonnegative reciprocal conductance g_uv(t)=g_vu(t),
piecewise continuous and periodic with finite period P. There is no advection,
coherent-wave interference, internal source, temperature-dependent controller,
capacity modulation or reset. Assume the averaged graph grounds every internal
component at a terminal, so the stable periodic solution is unique.

Let qbar=Y theta be its period-averaged terminal-current response, with current
positive into the network. Let G_union contain an edge exactly when its integrated
conductance over a period is positive. A terminal-avoiding path from i to j may
have arbitrary internal vertices, but no other terminal as an intermediate
vertex. Fixed-temperature terminals absorb a perturbation and are not transit
storage nodes.

Let I denote the set of internal vertices. The stage1 static-comparator theorems allow a general constant SPD storage matrix.
The result here requires diagonal positive capacities. This restriction is
essential to the positive-system proof and is not silently extended to the
larger algebraic class.

## Theorem

For any distinct terminals i and j:

1. Y_ji<=0.
2. Y_ji<0 if and only if there is a terminal-avoiding path from i to j in G_union.
3. In particular, Y_ji=0 if and only if Y_ij=0. The terminal response has exactly
   the same off-diagonal zero pattern as the static Kron reduction of the union
   graph, although its nonzero coefficients can be strongly unequal.

Consequently, a finite circuit in this class cannot have nonzero forward DC
transfer with exactly zero reverse DC transfer. Adding more finite stores,
more finite conductance phases or zero off-state contacts cannot change that
statement. It does not prohibit large **finite** isolation ratios.

There is a quantitative, generally conservative version. Let

\[
 i=v_0,v_1,\ldots,v_k,v_{k+1}=j
\]

be any terminal-avoiding simple path, with k internal vertices. Define

\[
 W_e=\int_0^P g_e(t)\,dt>0,\qquad
 \delta=\mathop{\rm ess\,sup}_{t,v\in I}
             \frac{\sum_wg_{vw}(t)}{C_v}<\infty.
\]

Then **both directions** obey the same positive lower bound:

\[
 \boxed{\min(-Y_{ji},-Y_{ij})\ \geq
 e^{-k\delta P}
 \frac{\prod_{\ell=0}^{k}W_{v_\ell v_{\ell+1}}}
      {P\prod_{\ell=1}^{k}C_{v_\ell}}\ >0.}
 \tag{1}
\]

For a direct terminal edge, k=0 and the bound is its mean conductance. Units are
W/K on both sides. The bound can be extremely weak; it establishes a structural
obstruction and an explicit floor, not a useful universal isolation ceiling from
conductance budget alone.

## Proof

Drive terminal i by a unit temperature offset and set all other terminal offsets
to zero. The internal equations are

\[
 \dot x_v=-d_v(t)x_v+
       \sum_{w\in I,w\ne v}\frac{g_{vw}(t)}{C_v}x_w
       +\frac{g_{vi}(t)}{C_v},
 \qquad d_v(t)=\frac{\sum_wg_{vw}(t)}{C_v}\leq\delta.
 \tag{2}
\]

The off-diagonal state couplings and forcing are nonnegative. Variation of
constants around the diagonal decay therefore preserves nonnegativity. Taking
the stable infinite-past limit gives the nonnegative periodic solution. For
j!=i, the receiving terminal current is

\[
 q_j(t)=-g_{ji}(t)-\sum_{v\in I}g_{jv}(t)x_v(t)\leq0.
 \tag{3}
\]

This proves the first claim.

For a path with k>=1, fix any observation time t. Allocate the injection edge
i-v1 to the full-period window [t-kP,t-(k-1)P]. Allocate the next internal edge
v1-v2 to the next full-period window, and continue so the final internal edge
v(k-1)-vk is in [t-P,t]. These windows enforce the required chronological order
regardless of the original phase order of the contacts. Repeating the schedule
allows a temperature perturbation to wait for the next needed edge. Finite
conductance and positive capacity leave a strictly positive retained fraction.

Repeated substitution in the nonnegative variation-of-constants equation gives
a path contribution to x_vk(t). Its product of diagonal-retention factors is at
least exp(-delta*kP), since total time from injection to observation is at most
kP. All integrations are over independent full-period windows. Periodicity gives

\[
 x_{v_k}(t)\ \geq\ e^{-k\delta P}
       \prod_{\ell=1}^{k}\frac{W_{v_{\ell-1}v_\ell}}{C_{v_\ell}}.
 \tag{4}
\]

This lower bound holds for every t, up to the usual almost-everywhere convention
for piecewise coefficients. Substituting it in (3), averaging the last contact
g_jvk over a period and discarding other nonnegative transfer contributions gives
(1) for -Y_ji. Traverse the same undirected path in reverse: the products of edge
integrals and capacities are unchanged, and the same delta applies. Hence the
same bound holds for -Y_ij.

Conversely, suppose no terminal-avoiding path exists. Deleting the other
terminals separates every internal component forced by i from all internal
neighbors of j, and there is no direct i-j edge of positive period integral.
The stable periodic state of each unforced internal component is zero. Thus
(3) averages to zero. This proves the support characterization and its symmetry.
The equality with the static Kron zero pattern is the established static
terminal-avoiding-path criterion, applied to the union graph. QED.

## Consequential distinctions

- This theorem does **not** restore equal forward/reverse coefficients. The
  stage1 circulator is a valid nonreciprocal example.
- Merely saying that the union graph is connected would be wrong: a path through
  another clamped terminal does not transmit the perturbation. The correct
  terminal-avoiding condition is indispensable.
- Perfect isolation claimed from a small floating-point entry is invalid.
  Strictly positive numbers below the format's range can be printed as zero.
- The proof uses the infinite-past periodic state and pays the complete repeated
  cycle. Finite observation windows or expenditure of a pre-cooled store do not
  establish a periodic isolator.
- Truly zero capacities, instantaneous infinite conductances, non-reciprocal
  primitives, interference or other mechanisms outside (2) require separate
  analysis. Published phase-coherent magnetic heat circulators and ideal radiative
  circulator primitives are not contradicted by this positive diffusion theorem.

This is a completed governing proof for the stated class. Static topology and
positive-system theory are established literature. Novelty of this precise
periodic quantitative formulation has not been established; no invention claim
is inferred from the absence of an exact keyword match.
