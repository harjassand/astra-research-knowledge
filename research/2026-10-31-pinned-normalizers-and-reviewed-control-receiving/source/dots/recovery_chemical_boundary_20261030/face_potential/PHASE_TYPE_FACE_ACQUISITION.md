# Raw finite phase-type face acquisition: ordinary absorption theory removes a search

30 October 2026. New local construction; no full-network conclusion yet.

The two-stage example has a stronger consequence than a bespoke numerator search. For a whole raw class, ordinary finite-state absorption theory supplies the potential exactly. A general rational LP is unnecessary for this class.

## Acquired local architecture

From the D-free hidden reaction list, search for a catalyst C that has count1 on both ends of every edge, and an absorbing output species D absent from every face source. After deleting C, each edge is a single-particle transfer Xi->Xj or Xi->D. All rates are fixed positive rationals. Require every transient type Xi to have a directed path to D. No C,D or ordering of the transient types need be supplied to the finder.

On D=0 the active face is C>=1,z=sum_i Xi>=1. Internal moves preserve C,z and the pool {all Xi,D}; a restoring move exits to D>0. Thus all structural face hypotheses are acquired rather than inferred from a numerical spectral test.

Let Q be the finite transient generator, including absorption rates q_iD in its negative diagonal. Compute the exact rational vector

    -Q t = 1.

Reachability to D makes this finite chain transient and t_i>0. These are ordinary one-particle mean absorption times; no recurrence of the full reaction process is assumed.

## Acquired population-independent face potential

For the ACTUAL many-particle face killed at its FIRST restoring output, define

    psi0(x,C) = (sum_i t_i x_i)/(C z).

Then 0<psi0<=max_i t_i since C>=1. Direct generator calculation gives

    -Q_face psi0 = 1 + (1/z) sum_i q_iD x_i [sum_j t_j x_j - t_i] >=1.

Every summand is nonnegative whenever x_i>=1, since then sum_j t_j x_j>=t_i; if x_i=0 its summand vanishes. This proof covers all integer populations, including repeated types. It does not identify the first-restoration mean with the average one-particle mean: the latter is only a valid supersolution.

Equivalently, choosing one initial particle uniformly and following its ordinary C-speed chain gives an upper bound on first absorption by that particle's absorption time. The displayed generator proof avoids needing independent physical labels in a later coupled process.

Apply the already proved killing combinator

    psi_c=(4/3)psi0/(1+c psi0),  c=(k_seed+k0)(a)_2,

to acquire the face potential required by the trace theorem. It has uniform bound (4/3)max_i t_i, retains actual hidden state, and supplies the actual seed/clear suppression for ingress. The potential is rational in the raw counts and rates.

C+D->C+Xi ingresses have q psi_c <=(4/3)kappa max_i t_i. The a-born ingress is paid by the inverse c_out bound exactly as before. Other raw ingresses still require their actual summed coefficient/potential comparison; the phase-type finder alone does not certify them.

## Costs and limits

The finder enumerates finitely many catalyst/absorber choices, checks graph reachability, solves a finite exact rational linear system and verifies -Qt=1,t>0. This is a genuinely constructive acquisition of a multi-step face potential, with ordinary finite-chain theory as its engine. Rational bit sizes can grow; no practical large-instance guarantee is claimed.

This does not solve arbitrary nonlinear face dynamics, unknown polynomial denominators, or the full global network by itself. It is a composable LOCAL certificate module to be combined with the already acquired trace ingress, positive-D pooling, terminal/activity and phase transfer checks. The failed monolithic coefficient cone is preserved: the killing transform is certified by its square identities, not falsely rediscovered by coefficient positivity.
