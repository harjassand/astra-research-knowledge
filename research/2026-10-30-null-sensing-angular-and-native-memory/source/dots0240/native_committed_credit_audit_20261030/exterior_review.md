# Independent audit: actual committed restriction and exterior commutation

2026-10-30. Reviewer: audit_basin. This reviews Sections 2 and 4 of the frozen `COMMITTED_CHAIN_CP_CREDIT.md` against the actual reset-first generator, forest gauge, repaired alphabet, and finite monitor model. Original sources are unchanged.

## Verdict

**PASS for these two interfaces.** The actual reset-first, forest-gauged apparatus has precisely the isolated killed C generator used by the candidate, and its committed-credit Kraus operators commute with every exterior nominal term, including malformed-mask partial resets and every actual monitor. These conclusions follow from the explicit generator, not from a presumed clean classical clock law. This note does not certify the candidate's entire own-source block inequality or solve acquisition/cleanup service.

## 1. Exact committed projection and local generator

Write

    D_h = P_{C,h} P_{W_h=0} product_{r in R_h} P_{o_h,r}.

All factors commute. On D_h, each C_t consistency test succeeds; hence every C-to-abort Hamiltonian edge vanishes in both directions. Cleanup in C and in R(C) is disabled in the reset-first apparatus. There is no C-to-A Hamiltonian edge, no refresh in C, and no ready reset from C. All acquisition, verification and A/Q terms have zero h-clock support on D_h. The only h exit is the terminal reset from C_L to Q_0.

The forest frame removes every computation payload unitary. Since all target ownership projectors equal one on D_h, the h computation Hamiltonian is the connected scalar path

    H_C = sum_{t=0}^{L-1} g_t (|C_{t+1}><C_t|+h.c.) tensor I_monitor,

with the actual nonzero fixed edge amplitudes. It leaves W_h=0 invariant. The complete terminal bundle has source loss

    A_T = kappa_T |C_L><C_L| tensor I_monitor,

because its workspace labels are separate channels with the same rate. Deleting only its gain leaves exactly this loss, not a conditional or normalized terminal map.

The h monitor is explicitly part of the finite matrix. On the C block it has

    H_m = Omega I_C tensor X,
    M_t = sqrt(kappa_m) |C_t><C_t| tensor |0><1|,
    sum_t M_t^dagger M_t = kappa_m I_C tensor n.

All other label channels vanish upon restriction. Its Hamiltonian and resolved resets are workspace blind. Therefore the actual local killed Schrödinger generator is

    K_C(rho) = -i[H_C+H_m,rho]
               +sum_t D[M_t](rho) - {A_T,rho}/2.

No other effective dephasing or independently sampled clock process appears.

## 2. Resource monitors and exterior environments are genuine spectators

A resource monitor Hamiltonian is I_lock,payload tensor Omega X. On D_h, its only nonzero resolved label reset is the o_h channel, acting on that resource monitor alone. Thus every resource monitor adjoint annihilates an observable on h's clock/monitor tensor identity on the resource monitors. This holds for arbitrary entanglement; product-state preparation is unnecessary. Their omission from K_C is therefore an exact invariant-observable restriction, not elimination of a physical dissipative process.

The same is true of the rest of the apparatus when applied to S_h: exterior terms act trivially on h clock/workspace/monitor, preserve all o_h projectors, and do not change any relevant DATA variable on D_h. Their adjoint actions on D_h times a coefficient on h clock/monitor vanish. Hence R_h and S_h are supported only on h's actual clock plus its own monitor. The D_h multipliers in the extended channel additionally involve h workspace and the finite lock set R_h, exactly as declared.

## 3. Direct finite-matrix proof of strict survival decay

A reset-tail citation is not needed. Retain the genuine trajectory alternatives with no monitor emission before the first terminal event. The no-jump amplitude generator on C times monitor is

    A_eff = -i(H_C+H_m)
            -(kappa_T |C_L><C_L| tensor I
              +kappa_m I_C tensor n)/2.

For any u>0 the effect for terminal absorption by u along this subset of records is

    E_u = integral_0^u exp(t A_eff^dagger) A_T exp(t A_eff) dt.

It is strictly positive. Indeed if v lies in its kernel, then

    (<C_L| tensor I) exp(t A_eff) v = 0

for every t in an interval. Analyticity gives all derivatives at zero equal to zero. At order zero, v_L=0 as a monitor vector. At first order, the only remaining contribution at C_L is the nonzero edge coefficient times v_{L-1}, so v_{L-1}=0. Inductively the nth derivative has the product of the nonzero path-edge coefficients times v_{L-n}, plus terms involving components already shown zero. Hence every v_t=0. The argument includes L=0 trivially and does not depend on the monitor drive being large or on monitor factorization.

Let epsilon_u=lambda_min(E_u)>0. This is a subset of physical terminal records, so the killed trace after u is at most 1-epsilon_u for every initial density matrix. CP iteration gives geometric survival decay and therefore an exponentially decaying norm bound for exp(t K_C^*)I. Thus

    R_h=integral_0^infinity exp(t K_C^*)I dt

exists, is positive definite, and satisfies K_C^*R_h=-I. For example R_h<=u/epsilon_u I. Positive definiteness follows already from the positive near-zero integral; it can also be bounded below using the finite terminal hazard. A finite set of bounded local circuit types permits common positive minimum and finite maximum constants.

This proves the candidate's existence claim using the actual Hamiltonian, actual monitor Kraus family, and actual terminal loss. A disconnected C path, zero edge, or incomplete/unequal-rate terminal bundle would require a fresh check; none is part of the frozen generator.

## 4. Exhaustive exterior commutation check

For g!=h, every exterior term commutes with P_{o_h,r} for every r, as follows directly from the alphabet:

- g acquisition exchanges f and o_g, both orthogonal to o_h;
- g coherent cleanup exchanges o_g and z_g, both orthogonal to o_h;
- g resource cleanup resets z_g to f, likewise;
- g computation, verification, and abort drives are diagonal in resource labels;
- g terminal/abort/ready/refresh resets do not change resource locks;
- all hub/resource monitor resets are clock/lock diagonal, and monitor Hamiltonians are identity on clocks/locks.

These are operator commutations, including adjoints, not just invariant-subspace range inclusions. The reset-first change disabling R cleanup is also sufficient; no old cleanup rule is reintroduced here.

Every exterior term leaves h's clock, workspace, and monitor untouched. Consequently it commutes with D_h and with every coefficient function of S_h (which acts on h clock plus monitor). In particular D_h is a reducing projector for every exterior reset Kraus and its adjoint.

In the forest frame, exterior Hamiltonians are scalar on DATA, so they also commute with K_h,s. Exterior DATA-reset Kraus operators need one additional block argument. On D_h, h owns every resource in R_h, which contains the entire declared DATA/read footprint of K_h,s. The explicit forest unitary of g acts only on resources whose current lock is o_g. It therefore acts on no resource in R_h on this block, even if g has a malformed clock or an incomplete coherent mask. Its workspace and clock factors belong to g. Hence the restricted exterior reset commutes with K_h,s and its adjoint.

Outside D_h the B_h,s branch is zero and A_h is identity. Since every exterior term reduces D_h, the preceding on-block commutation proves globally

    [A_h,J_g]=[A_h,J_g^dagger]=0,
    [B_h,s,J_g]=[B_h,s,J_g^dagger]=0,

and the corresponding Hamiltonian commutators. The conclusion includes coherent superpositions between D_h and its complement: no pinching or measurement of masks is used.

Resource monitors require no exception. Their label projections commute with D_h and K_h,s, and their private monitor lowering operators commute with S_h. Only h's own monitor can fail to commute with S_h; it is included in K_C and is not exterior.

## 5. Pairwise credit commutation

If h and g share a resource, D_hD_g=0 because the shared lock cannot simultaneously be o_h and o_g. K_h,s acts only on DATA and hence commutes every D_g. S_h acts on h clock/monitor and commutes D_g and S_g. Thus the nonidentity B branches multiply to zero in either order, while each A branch is identity on the other active block; all cross Kraus commutators vanish.

If R_h and R_g are disjoint, their DATA actions and controller factors are disjoint. The same commutation conclusion follows directly. Therefore the T_h commute as maps, with a bounded-depth local implementation after fixed overlap-graph coloring.

## Scope retained

This establishes the exact exterior commutation and actual finite committed witness required by the new candidate. It does not by itself prove the candidate's own-generator inequality across every commitment/dirty-source block, and it supplies no uniform active-hub service in A/Q or acquisition contention. Payload idempotence must be implemented by an actual finite native gate list before claiming the whole credit theorem for that revised payload. No native continuous-noise memory threshold is established here.
