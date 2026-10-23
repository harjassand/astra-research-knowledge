# Two-network binary registry: representation and dynamics gate

24 October 2026. Exact-model audit only; no material, kinetics, or assembly is acquired.

## Rest lengths and exact common-strain reduction

Take fixed periodic node indices, `sigma_i in {-1,+1}` with `sum_i sigma_i=0`, and

```text
m_i = m (sigma_i+sigma_(i+1))/2,
H = h sum_i [ C/2 (D_h u_i-m_i)^2
             +D/2 (D_h v_i)^2 + V(u_i-v_i) ]
    - J sum_i sigma_i sigma_(i+1),
D_h z_i=(z_(i+1)-z_i)/h,
V(w)=V0[1-cos(2 pi w/d)].
```

For `sigma_i=sigma_(i+1)=+1`, the upper-network spring has preferred physical bond length `h(1+m)`; for a `--` pair it is `h(1-m)`; for an unlike pair it is `h`. These preferred lengths are positive if `0<=m<1`. The lower-network preferred length is `h`. This positivity check does not constrain the instantaneous harmonic-spring lengths: a literal chain also needs a small-strain regime or a non-crossing/positive-length constraint, since the quadratic energy alone permits unphysical over-compression.

The fixed balanced inventory gives `sum_i m_i=m sum_i sigma_i=0`. Let `w_i=u_i-v_i`, `z_i=D_h w_i`, and `x_i=D_hu_i`. The two spring terms obey the exact identity

```text
C/2 (x_i-m_i)^2 + D/2 (x_i-z_i)^2
 = S/2 (z_i-m_i)^2
   +(C+D)/2 [x_i-(C m_i+D z_i)/(C+D)]^2,
S=CD/(C+D).
```

On the periodic ring, `sum_i z_i=0` and `sum_i m_i=0`; hence both minimizing strains sum to zero and are derivatives of periodic `u,v`. Minimizing out the common strain therefore reduces the spring energy exactly to `S/2(D_h w_i-m_i)^2` on this ring. The two networks remain real degrees of freedom in the unreduced Hamiltonian; this algebra does not remove their mass, drag, frame, or coupling material from a physical implementation.

## What the model's local operation does

An adjacent label exchange `sigma_i <-> sigma_(i+1)` conserves the fixed `+/-` inventory. It leaves the central mismatch `m_i` unchanged and changes only the neighboring mismatches `m_(i-1)` and `m_(i+1)`. The central chemical bond `sigma_i sigma_(i+1)` is unchanged; the two outer chemical bonds can change. At fixed `u,v`, its exact energy change is

```text
Delta H = h C/2 sum_(j=i-1,i+1) [(D_h u_j-m'_j)^2-(D_h u_j-m_j)^2]
          -J [sigma_(i-1)(sigma_(i+1)-sigma_i)
              +sigma_(i+2)(sigma_i-sigma_(i+1))].
```

Subsequent mechanical relaxation changes the spring and relative-registry energy. The displacement nodes stay attached to their original indices: exchanging labels is not free node relabeling or a registry-period reset.

For example, define `e_i=D_hu_i-m_i`, `q_i=D_hv_i`, and `w_i=u_i-v_i`. The exact overdamped mechanics are

```text
Gamma_u u_dot_i = -g_u,i,   g_u,i=C(e_(i-1)-e_i)/h+V'(w_i),
Gamma_v v_dot_i = -g_v,i,   g_v,i=D(q_(i-1)-q_i)/h-V'(w_i),
V'(w)=(2 pi V0/d) sin(2 pi w/d).
```

This dissipates the mechanical energy at fixed labels. A mathematically specified finite-temperature label dynamics can use symmetric nearest-neighbor proposals with Metropolis acceptance `min(1,exp[-beta Delta H])`; each proposal must evaluate the full changed Hamiltonian at the current `u,v`. Together with mechanical Langevin noise satisfying fluctuation-dissipation, this is a detailed-balance model at fixed composition. Its attempt rate and transition-state physics are still inputs. A zero-temperature downhill-energy filter is only an energy-selection rule: it suppresses thermally activated uphill exchanges and cannot supply physical diffusion rates, barriers, or lifetimes.

Actual vacancy-mediated motion would require explicit vacancy states, vacancy formation/migration free energies, and a path through the lattice; these are absent from the two-state labels. Charged species also require electronic/ionic compensation and electrostatic or reservoir work. Even for a neutral alloy, the exchange rate, mechanical drags, thermal noise, defect pathways, and validity of positive bond lengths are not measured by this Hamiltonian.

## Registry is relative, and the support remains counted

As written, `V(u_i-v_i)` is a local interaction between paired nodes of two networks. Its forces are equal and opposite; it is not an external substrate potential. There is no net grounding force, and a common shift of `u` and `v` is a zero mode. Any frame, clamp, or substrate that fixes the common position must be included with its reaction forces, compliance, and return work. The two networks and the material that supplies their node-paired registry coupling are part of the physical inventory.

A single chain on a fixed spatial substrate instead has a term like `V_s(ih+u_i)`. It is site-phase dependent and does not equal a uniform `V(w_i)` unless the spacing is commensurate (`h/d` an integer for this simple one-site form); other rational ratios require an explicit supercell and generally produce multiple phases. The relative two-network potential avoids that external spatial phase only because node pairing is stipulated; an actual interpenetrating lattice must justify the pairing and its local interaction.

Displacements are unwrapped and node indices are fixed. Although `V(w)` repeats every `d`, shifting one node by `d` leaves adjacent bond extensions changed by `+d` and `-d`; their spring energy is not periodic and cannot be erased by taking coordinates modulo `d`. The periodic ring has zero net displacement winding, so local slip structures must respect that topology. Any atom/site relabeling or vacancy-assisted rearrangement needs its own path and energy accounting. The finite Hamiltonian supplies a valid energy for each state, not the barrier or rate for reaching another state.

This pins the exact binary two-network operation: conservative pair-rest-length changes under local composition exchanges, coupled to two passive elastic networks and their relative registry energy. It does not acquire a material, a physically available diffusion path, finite-temperature kinetics, or a closed control-and-reset cycle.
