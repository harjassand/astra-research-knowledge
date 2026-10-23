# Local lattice realization and transport gate for registry coupling

24 October 2026. This is a bounded representation/transport check of the selected continuum functional. It proposes no material constants and validates no assembly.

## One explicit local ancestry

Use a one-dimensional binary alloy chain on a fixed periodic substrate. Let `n_i in {0,1}` be the occupation of a mobile species on reference site `i`, with fixed total `sum_i n_i=N nbar`; let `w_i` be the displacement of the host-lattice node at that site. Species labels move between sites, while `w_i` remains a displacement of the material reference lattice. For reference spacing `a`, one local lattice Hamiltonian is

```text
H = sum_i [ -J (n_i-nbar)(n_(i+1)-nbar)
            + (k_b/2) (w_(i+1)-w_i-a alpha phi_(i+1/2))^2
            + V_s (1-cos(2 pi (i a+w_i)/d)) ],
phi_(i+1/2) = (n_i+n_(i+1))/2-nbar.
```

Indices are periodic; each elastic/composition term is a nearest-neighbor pair term, and the last term is the node's interaction with the substrate. A commensurate reference lattice makes `ia/d` an integer and reduces the substrate term to `V_s[1-cos(2 pi w_i/d)]`. In an incommensurate chain, the site phase `2 pi ia/d` varies with `i`; the uniform continuum `V(w)` is then not the literal substrate energy without an additional homogenization/supercell argument.

This is a local FK/Peierls-type construction: `J` supplies a short-range mixing interaction, `k_b` is the bond stiffness, and `a alpha phi_(i+1/2)` is a composition-dependent preferred bond-length shift. The substrate term is a periodic registry energy relative to an anchored second body, not a self-contained chain energy. For slowly varying fields, `w_(i+1)-w_i ~= a w_x` and a coarse-grained composition gives the elastic continuum coefficient `S ~= k_b a`; the registry energy per length is `V_0 ~= V_s/a`. The local mixing entropy plus the pair interaction produces a coarse-grained `f(phi)`, and a positive gradient penalty of order `kappa ~= J a` after fixed-mean terms are absorbed into `f`. These are continuum approximations; a binary site variable is not itself a continuous `phi`, and the exact finite-chain free energy need not equal a quartic Landau density.

## Conserved transport pays the local bond changes

A physical composition move can be a nearest-neighbor Kawasaki exchange `n_i <-> n_(i+1)` (or a vacancy-mediated hop for a dilute adsorbate). It preserves total composition. For a symmetric proposal, for example,

```text
rate(C -> C') = nu_0 min(1, exp[-beta (H(C')-H(C))])
```

satisfies detailed balance at fixed total species count. The energy difference includes the onsite/mixing terms and every affected bond-rest-length term; it is not a free realization of `phi_dot=M partial_xx mu`. A hydrodynamic conserved-gradient equation is a coarse-grained limit and must inherit mobility and noise from these moves. If the mobile species is charged, each hop also needs local electronic/ionic compensation and its electrostatic or reservoir free-energy cost. A neutral substitutional alloy avoids an external charge reservoir only if the electronic and defect background remains equilibrated; that is still part of its measured chemical free energy.

For mechanics, an overdamped lattice law `zeta wdot_i=-partial H/partial w_i+noise` is a plausible thermal model only after its drag, noise, and substrate support are specified; equilibrium noise obeys fluctuation-dissipation. The continuum deterministic gradient flow describes mean drift, not thermal fluctuation rates or phase-slip nucleation. No independent `alpha` actuator is present: composition changes the bond's rest length through the conservative spring energy.

## Registry, winding, support, and return

The `w_i` in this Hamiltonian are **unwrapped** displacements attached to fixed reference indices. The substrate term is periodic, but the bond term is not: changing one `w_i` by one registry period `d` changes its two adjacent bond extensions by `+d` and `-d` and generally costs elastic energy. Treating `w_i` modulo `d` and silently relabeling a neighbor would erase that cost and is not the stated local Hamiltonian. A physical phase slip is a kink/dislocation core with a finite barrier and a transport/reconstruction path. On a periodic fixed-length chain, `sum_i (w_(i+1)-w_i)=0`; slips must preserve total winding, normally by creating or moving a kink/antikink pair. A single net slip requires a boundary, defect, or atom/site relabeling event and its associated energy and composition transport.

The fixed substrate is an anchored support that takes reaction forces. Its stiffness, backing, thermal load, and return energy are absent if `V_s` is simply imposed as an external cosine. For an alloy interpretation, the lattice sites remain the reference nodes only while the crystal stays intact; vacancy motion, dislocations, and changes of site connectivity need explicit degrees of freedom once slips or strains leave the small-deformation regime. For an adsorbate interpretation, the adsorbate inventory, substrate occupancy, and reservoir chemical potential must be tracked instead. Neither interpretation grants free phase-slip partner relabeling.

A repeatable operation must return the composition pattern and inventory, unwrapped displacement/winding, substrate/support, and any temperature or chemical potential to their initial states. It must pay the mixing/reordering work, defect barriers, substrate reaction and support motion, and any thermal or electron/ion exchange. The continuum functional alone does not specify a finite-control protocol or a free reset.

This pins a local Hamiltonian and a detailed-balance transport interpretation that can coarse-grain toward the selected fields. It does not identify a real alloy/adsorbate, show that its measured coefficients produce the desired instability, establish a phase-slip rate, or demonstrate a closed-cycle advantage.

## Exact finite-cell registry model and passive transport

This binary FK chain is only a physical ancestry. The exact finite-cell model used for the continuum analysis instead takes continuous mesoscopic composition variables `phi_i` on cells and two periodic displacement fields `u_i,v_i` on fixed nodes:

```text
F_h = h sum_i [ f(phi_i) + kappa/2 (D_h phi_i)^2
                + C/2 (D_h u_i-alpha phi_i)^2
                + D/2 (D_h v_i)^2 + V(u_i-v_i) ],
V(w)=V0[1-cos(2 pi w/d)],
D_h z_i=(z_(i+1)-z_i)/h.
```

This is an exact local Hamiltonian for the stipulated finite-cell model: `f` and `V` are onsite, and the derivative terms couple nearest-neighbor cells. It is not an exact free energy of binary atoms. For periodic fields, fixed `sum_i phi_i=0`, and `w_i=u_i-v_i`, minimizing the two elastic bond terms over their common strain gives

```text
C/2 (D_h u_i-alpha phi_i)^2 + D/2 (D_h v_i)^2
  >= S/2 (D_h w_i-alpha phi_i)^2,
S=CD/(C+D),
```

with equality at `D_h u_i=(C alpha phi_i+D D_h w_i)/(C+D)` and `D_h v_i=C(alpha phi_i-D_h w_i)/(C+D)`. The equality strains have zero sums under the stated zero-mean and periodic conditions, so they are realizable by periodic `u,v`. The reduced relative-coordinate edge energy is therefore exactly of the finite-spacing registry form for this model; this does not identify `S,C,D,alpha` with measured atomistic constants.

An exact local passive ODE is specified by

```text
e_i = D_h u_i-alpha phi_i,  q_i=D_h v_i,  w_i=u_i-v_i,
mu_i = f'(phi_i)-kappa Delta_h phi_i-C alpha e_i,
g_u,i = C(e_(i-1)-e_i)/h + V'(w_i),
g_v,i = D(q_(i-1)-q_i)/h - V'(w_i),
V'(w)= (2 pi V0/d) sin(2 pi w/d),
phi_dot_i = M Delta_h mu_i,
Gamma_u u_dot_i = -g_u,i,
Gamma_v v_dot_i = -g_v,i,
Delta_h z_i=(z_(i+1)-2 z_i+z_(i-1))/h^2,
M,Gamma_u,Gamma_v > 0.
```

Here `g_u,i=h^(-1) partial F_h/partial u_i` and likewise for `v`; the right-hand sides involve only onsite and nearest-neighbor variables.

Periodic summation by parts gives the exact identities

```text
sum_i phi_dot_i = 0,
F_dot_h = -M h sum_i (D_h mu_i)^2
              - h Gamma_u sum_i u_dot_i^2
              - h Gamma_v sum_i v_dot_i^2 <= 0.
```

Thus the ODE conserves the composition inventory and dissipates the stipulated finite-cell free energy. It fixes the reference-node labels and periodic topology; `sum_i D_h u_i=sum_i D_h v_i=0`, so the net winding is zero. Smooth evolution can cross registry barriers and form local kink/antikink structure, but it does not relabel nodes or change that net winding. The common translation of both networks remains a zero mode and must be quotiented or fixed by a stated gauge; any physical frame or clamp adds its own energy and return work. At finite temperature, stochastic conserved and mechanical terms consistent with fluctuation-dissipation are needed to predict rates; this deterministic ODE supplies neither noise nor atomic hopping kinetics.

If a control varies a parameter `p`, the balance becomes `F_dot_h = sum_p (partial F_h/partial p) p_dot - dissipation`. For example, for `f=a phi^2/2+b phi^4/4`, an isothermal change of `a` contributes `(h a_dot/2) sum_i phi_i^2`; varying `V0` contributes `h V0_dot sum_i[1-cos(2 pi w_i/d)]`; varying `d` contributes `-h V0 d_dot sum_i (2 pi w_i/d^2) sin(2 pi w_i/d)`. If instead the registry term is approximated by `K w_i^2/2`, varying `K` contributes `(h K_dot/2) sum_i w_i^2`; in the cosine model the small-displacement stiffness is `K_eff=4 pi^2 V0/d^2`, so it is not an independent parameter unless a separate control is supplied. Varying `alpha,C,D,kappa`, cell spacing, or temperature likewise requires the corresponding chain-rule work and, for a temperature change, heat/entropy accounting. Returning the controls and state is a cycle whose work must include these terms; the Lyapunov identity is not a free reset.

The companion finite-spacing calibration is also a statement about this stipulated mesoscopic registry functional, not about binary atom activation. For the reduced edge energy `S(Delta_i-h m_i)^2/(2h)+hV(w_i)`, the Lipschitz-`R'` Taylor remainder proves the sufficient calibration for every real `Delta_i`, including increments spanning arbitrarily many registry periods. Its local mismatch ratio must satisfy `r^2+nu_h r<=1`, with `r=|m_i|/m_c` and `nu_h=h L_q/S`; for a quartic mixing term the strict support condition is `|alpha| sqrt(-2a/b) < m_c r_h` when `a<0`, together with `a+S alpha^2>0`, where `r_h` solves `r_h^2+nu_h r_h=1`. This removes a small-hop assumption from that energy inequality. It does not make a continuum kink cost an exact atom-scale phase-slip threshold, nor provide a physical slip rate or a material realization.
