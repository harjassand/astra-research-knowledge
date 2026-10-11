# Exact route acquisition obstruction and the structural-certificate gate

Date: 2026-10-12. Status: independently derived finite-state theorem; exact finite checks pass. No atomistic experiment, formal proof, external correctness review, novelty claim, or transformative invention is established.

## Outcome

No fresh general rare-event acquisition primitive survived this attack. The strongest completed result is a compact reversible continuous-time Markov-chain family in which endpoints, equilibrium, equilibrium sampling, topology, and almost every rate are known, but learning the dominant transition mechanism or the absolute first-passage law still requires exponentially many exact local generator queries. This is a sharper interface than passive simulation. It does not rule out useful improvements under physically justified structure.

The decisive missing positive ingredient is an operationally verifiable restriction on the *effective kinetic response*, strong enough to exclude an uninspected dominant gate. Sparse microscopic forces, a fitted low-order response, finite held-out agreement, and endpoint-only generative proposals do not by themselves provide that restriction.

## Exact input and cost contract

Let M=2^d. The known, succinctly indexed state set is

    {A, B} union {u_j, v_j : j in {0,1}^d}.

The endpoints A and B are supplied. The generator has the following nonzero off-diagonal rates:

    q(A,u_j) = q(B,v_j) = 1/M,
    q(u_j,A) = q(v_j,B) = 1,
    q(u_j,v_j) = q(v_j,u_j) = theta_j.

All other off-diagonal rates are zero. Diagonal rates are minus the row sum. The unknown theta_j are positive rational numbers.

The learner receives all of this structure, M, and the complete stationary law. It may query theta_j at *any* chosen index, adaptively, at unit cost. This query reveals the entire unknown local generator row at u_j and v_j. Exact samples of the known stationary law are free. Known endpoint transitions can be sampled or evaluated freely. Listing all M endpoint successors costs M outputs; it does not reveal any theta_j. Random bits and arithmetic may be free for the lower bound.

This is at least as informative as microscopic dynamics that must inspect a local rate before evolving there. The lower bound charges gate inspections, rather than the enormous physical waiting time. It is not a lower bound against additional symbolic input that identifies the special gate or certifies a restricted response class.

## Theorem 1: all models have exactly the same equilibrium

For every positive theta vector, the chain is irreducible and reversible with

    pi(A)=pi(B)=1/4,
    pi(u_j)=pi(v_j)=1/(4M).

Proof: these masses sum to one. On A--u_j, both directed equilibrium flows equal 1/(4M); likewise on B--v_j. On u_j--v_j, both equal theta_j/(4M). Thus detailed balance holds edge by edge. In particular, neither equilibrium samples nor equilibrium thermodynamic observables identify the kinetic gates.

## Theorem 2: exact committor, capacity, route law, and mean first-passage time

Define f(theta)=theta/(1+2theta) and S=sum_j f(theta_j). Then

    h(u_j)=f(theta_j),
    h(v_j)=(1+theta_j)/(1+2theta_j),
    cap(A,B)=S/(4M),
    P(reactive channel=j)=f(theta_j)/S,
    E_A[tau_B]=2M/S.

Here h(x)=P_x(tau_B<tau_A), with h(A)=0 and h(B)=1. Capacity means the stationary A-to-B reactive flux. The channel means the corridor used by a successful A-to-B excursion; it is not a geometric-path approximation.

Proof of the committor: on corridor j, the harmonic equations are

    (1+theta) h(u) = theta h(v),
    (1+theta) h(v) = 1+theta h(u).

Solving gives the displayed values. The equilibrium flux leaving A and eventually reaching B is sum_j pi(A)q(A,u_j)h(u_j)=S/(4M). Its corridor-specific contributions give the route law.

Proof of the clock: every A holding time has mean one and chooses its corridor uniformly. Starting at u_j, the total hazard of exiting {u_j,v_j} to {A,B} is identically one, regardless of internal flips, so its mean duration is exactly one. An excursion succeeds with probability f(theta_j), hence the unconditional success probability per attempt is S/M. Strong Markov renewal gives

    E_A[tau_B] = 2 + (1-S/M) E_A[tau_B],

which yields 2M/S. Independence between attempt duration and success is unnecessary for this expectation identity.

## Theorem 3: exact full first-passage transform

For s>=0 define

    b(s) = (1/M) sum_j theta_j/(s+1+2theta_j).

Then

    E_A[exp(-s tau_B)] = b(s)/(s(s+2)+b(s)).

At s=0 the value is understood as one. Proof: let F_x be the transform from x and F_B=1. The backward equations give

    (s+1) F_A = (1/M) sum_j F_u_j,
    (s+1+theta) F_u = F_A+theta F_v,
    (s+1+theta) F_v = 1+theta F_u.

Therefore

    F_u = ((s+1+theta)F_A+theta)/((s+1)(s+1+2theta)).

Substitution, using (s+1+theta)/(s+1+2theta)=1-theta/(s+1+2theta), yields the displayed transform. This verifies that the obstruction concerns the absolute law, rather than just an incorrectly inferred rate or an uncontrolled rare tail.

## Hidden-gate specialization

Set epsilon=M^-2. Model 0 has theta_j=epsilon for all j. Model J has theta_J=1 at one unknown index J and theta_j=epsilon elsewhere. Every endpoint generator row and all stationary information remain identical.

The exact mean times are

    T0 = 2(M^2+2),
    TJ = 6M(M^2+2)/(M^2+3M-1),
    T0/TJ = (M^2+3M-1)/(3M).

Thus T0 is asymptotically 2M^2, whereas TJ is asymptotically 6M. The hidden corridor's reactive-channel probability is

    wJ = (M^2+2)/(M^2+3M-1) >= 1-3/M.

One uninspected kinetic gate can therefore determine nearly the entire mechanism population while changing the absolute time scale by a factor asymptotic to M/3.

## Theorem 4: adaptive exact-query lower bound

Choose J uniformly from {1,...,M}. Couple a learner's internal randomness and known samples under model 0 and model J. Until the learner queries J, the transcripts are identical. Under model 0, the learner inspects at most q distinct labels; the probability that J belongs to that set is at most q/M. Therefore the total-variation distance between model-0 and mixture-model-J transcripts, and between any outputs derived from them, is at most q/M. The same argument gives E_0[number of distinct inspected gates]/M for an expected-cost formulation.

Consequences:

1. **Relative mean-time estimation.** For M>=3, the intervals [3T0/4,5T0/4] and [3TJ/4,5TJ/4] are disjoint. An estimate within 25 percent with failure probability at most alpha on every model distinguishes the two cases with errors at most alpha. Hence q >= (1-2alpha)M. For example alpha=0.05 requires q>=0.9M.

2. **Dominant-route sampling.** If a route-label sampler has total-variation error at most delta on each hidden model, its average probability of outputting J is at least wJ-delta. After at most q distinct queries, even an optimal algorithm identifies J with probability at most (q+1)/M: inspect q labels and, if none is special, make one guess. Hence q >= M(wJ-delta)-1. For fixed small delta this requires almost all M gates.

3. **Full-law sampling.** Under model 0, reaching B requires at least one central crossing. Its total instantaneous rate is at most epsilon, so P_0(tau_B<=12M)<=12/M. Under any hidden model, TJ<=6M, so Markov's inequality gives P_J(tau_B<=12M)>=1/2. The two target laws have TV distance at least 1/2-12/M. If an algorithm approximates each law within TV delta, data processing and the transcript coupling give

       q/M >= 1/2 - 12/M - 2delta.

   Thus M>=96 and delta=1/16 imply q>=M/4.

All bounds allow arbitrary adaptive off-trajectory queries, perfect equilibrium sampling, and supplied endpoints. No pre-generated reactive trajectory or committor is used.

## Equal-interface baseline

The strongest simple baseline queries all M gates, computes S, and returns the exact mean time, capacity, and route weights. Its acquisition cost is M exact gate queries and O(M) arithmetic; the lower bound matches this order. The binary label length d and epsilon bit length O(d) are succinct. Treating M state inspections as polynomial in an explicitly listed graph is correct but does not remove the exponential cost in d.

Learned path proposals, committor fitting, weighted ensembles, splitting, temperature acceleration, and generator interpolation cannot remove this query lower bound on the stated family. They may have excellent performance on structured instances. The family is a finite-state kinetic counterexample; no smooth atomistic embedding is claimed, and no universal lower bound against arbitrary richer microscopic model descriptions is claimed.

## Can an acquired local-factor or Walsh certificate evade the obstruction?

There are two distinct gates, and neither is closed by a successful low-order fit.

**Acquisition.** A constant response is a degree-zero Walsh polynomial. Any query transcript that has not covered the cube is also compatible with the hidden-spike alternative above. Finite local mixed-difference tests, random response probes, cross-validation, and fitted low-degree sparsity do not certify absence of that alternative. A one-sided certificate that accepts the true constant model with high probability but rejects every hidden-gate model also inherits the Omega(M) transcript lower bound. Calling low-order structure an assumption is legitimate; calling it acquired from those finite tests is not.

**Aggregation.** Even a genuinely supplied succinct local-factor representation need not make rate decoding cheap. If theta_j is an exponential of a pairwise energy, summing f(theta_j) entails a nonlinear partition-function-type computation. Sparse factor scope alone does not bound treewidth or ensure efficient global inference. Bounded-treewidth elimination is a credible structural certificate if a valid decomposition is explicitly constructed and its width charged, but that is an established inference method, and the needed factorization must concern the actual kinetic response. It does not follow from sparsity of the microscopic force field.

A physically meaningful possible interface would expose a proof-carrying exact local generator, its factor scopes, and a verified bounded-width elimination of the relevant response. Numerical discovery of these objects would count as useful acquisition only if the proof checker rules out omitted terms globally. Ordinary molecular force-field locality certifies energy or force evaluation, not the committor, eliminated generator, effective escape rates, or elimination fill-in. No such bridge was obtained here.

## Primary-source comparison

- FlowRES uses normalizing-flow proposals with path-space Metropolis--Hastings correction and reports passive/active Brownian examples. A routine global learned path move would reproduce this operation rather than create a new primitive. Its finite low-dimensional demonstrations do not supply a hidden-route coverage certificate for the family above. https://www.nature.com/articles/s42256-024-00918-3
- Gen-COMPAS combines diffusion-generated intermediates, learned committor filtering, short unbiased simulations, and reweighting. Its official pipeline also exposes targeted MD before unbiased MD. The accessible preprint calls the framework exploratory and recommends further conventional sampling for high quantitative precision. Those reported capabilities motivate the problem but do not establish a general exact rate or global route-coverage theorem. https://arxiv.org/html/2510.24979v1 ; https://github.com/Tangcyu/Gen-COMPAS
- Automatically constructed basin boosts overlap Voter's hyperdynamics, which already derives boosts without supplied transition-state locations. https://doi.org/10.1103/PhysRevLett.78.3908
- Variational committor/rate learning already exists, including exact stopped multiple-time-step formulations. Merely adding a rate objective is not a new operation. https://pmc.ncbi.nlm.nih.gov/articles/PMC12768578/
- Bounded-treewidth inference and its wider computational boundary are established. https://proceedings.mlr.press/r6/chandrasekaran08a.html

## Reproducible finite checks

Run `python3 work/leverage_rare_invent/verify_corridor.py` from the workspace. The standard-library script independently constructs the full generator and solves exact rational linear systems for M=2,3,4,8,16,32 in both model classes. It checks row sums, detailed balance, committors, capacity, mean hitting time, and three full-law Laplace-transform values against the derivations. These finite checks support implementation consistency; the proof above is what establishes the all-M statements.

## Final scientific status

Completed: exact finite-state construction; complete derivations; adaptive local-query obstruction; mechanism and absolute-law separation; matching acquisition baseline; scoped structural-certificate analysis; primary-source overlap screen; exact finite arithmetic verification.

Unresolved: a new acquisition operation that exploits verifiable atomistic structure to improve on equally informed strong baselines; an efficient global certificate for the actual kinetic response; any physical benchmark; novelty/priority of the counterexample formulation; external or formal proof validation. No positive transformative capability is claimed.
